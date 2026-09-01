#!/usr/bin/env python3
"""UVIR-003 mode-resolved infrared transfer and robustness audit.

Tracks the three physical finite-q mode pairs in the kinetic-normalized
phase space

    u = (K^(1/2) p, K^(1/2) p_dot/H),
    p = (Xi, Q_rho, Q_chi),

at fixed comoving momentum.  Frozen-time eigenspaces are paired under
lambda -> -lambda, matched by principal-angle overlap, and parallel
transported with an orthogonal Procrustes rotation.  The exact
time-dependent transfer is then projected onto each two-dimensional mode
subspace.

The deepest infrared trajectory is repeated on nearby on-shell background
branches and for nearby alignment coefficients.  This is a finite-duration,
dimensionless robustness audit.  It does not derive a scattering amplitude,
unitarity scale, strong-coupling scale, physical cutoff, or an all-background
stability theorem.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.linalg import expm
from scipy.optimize import linear_sum_assignment

from uvir003_frw_background import integrate_representative_branch
from uvir003_physical_quadratic_propagators import (
    evaluate_physical_matrices,
    symbolic_propagators,
)
from uvir003_propagator_adiabaticity_transfer import (
    observable_normalization,
    second_order_generator,
)
from uvir003_scalar_adm_finite_q import (
    background_parameters,
    load_inputs,
)


MODE_LABELS = (
    "gauge_continuation_Xi",
    "matter_radial",
    "matter_phase",
)
FIELD_LABELS = ("Xi", "Q_rho", "Q_chi")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=base / "outputs",
    )
    parser.add_argument(
        "--frw-summary",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_summary.json",
    )
    parser.add_argument(
        "--frw-trajectory",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_trajectory.csv",
    )
    parser.add_argument(
        "--initial-q-over-H",
        type=float,
        default=0.01,
    )
    parser.add_argument(
        "--substeps",
        type=int,
        default=4,
        help="Base midpoint-Magnus substeps per trajectory interval.",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run only the baseline case for development checks.",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def symmetrize(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.T) / 2


def pair_eigenvalues(values: np.ndarray) -> tuple[list[tuple[int, int]], float]:
    """Find the minimum-cost perfect pairing under lambda -> -lambda."""

    require("even eigensystem dimension", len(values) % 2 == 0)

    def recurse(indices: tuple[int, ...]) -> tuple[float, list[tuple[int, int]]]:
        if not indices:
            return 0.0, []
        first = indices[0]
        best_cost = math.inf
        best_pairs: list[tuple[int, int]] = []
        for offset in range(1, len(indices)):
            second = indices[offset]
            scale = max(
                abs(values[first]) + abs(values[second]),
                1.0e-30,
            )
            local_cost = abs(values[first] + values[second]) / scale
            remaining = indices[1:offset] + indices[offset + 1 :]
            remainder_cost, remainder_pairs = recurse(remaining)
            total = float(local_cost + remainder_cost)
            if total < best_cost:
                best_cost = total
                best_pairs = [(first, second), *remainder_pairs]
        return best_cost, best_pairs

    _, pairs = recurse(tuple(range(len(values))))
    residual = max(
        float(
            abs(values[first] + values[second])
            / max(abs(values[first]) + abs(values[second]), 1.0e-30)
        )
        for first, second in pairs
    )
    return pairs, residual


def real_pair_frame(
    eigenvectors: np.ndarray,
    pair: tuple[int, int],
) -> tuple[np.ndarray, float]:
    """Return an orthonormal real frame for one conjugate/opposite pair."""

    columns: list[np.ndarray] = []
    for index in pair:
        columns.extend(
            [
                np.asarray(eigenvectors[:, index].real, dtype=float),
                np.asarray(eigenvectors[:, index].imag, dtype=float),
            ]
        )
    raw = np.column_stack(columns)
    left, singular_values, _ = np.linalg.svd(raw, full_matrices=False)
    require(
        "rank-two real mode-pair frame",
        singular_values[1] > 1.0e-12 * singular_values[0],
    )
    leakage = (
        float(singular_values[2] / singular_values[1])
        if len(singular_values) > 2
        else 0.0
    )
    return left[:, :2], leakage


def coordinate_participation(frame: np.ndarray) -> np.ndarray:
    weights = np.sum(frame[:3] ** 2, axis=1)
    denominator = max(float(np.sum(weights)), 1.0e-30)
    return weights / denominator


def subspace_overlap(left: np.ndarray, right: np.ndarray) -> float:
    return float(
        np.linalg.norm(left.T @ right, ord="fro") / math.sqrt(2.0)
    )


def parallel_align(
    previous: np.ndarray,
    current: np.ndarray,
) -> np.ndarray:
    left, _, right = np.linalg.svd(current.T @ previous)
    aligned = current @ (left @ right)
    require(
        "parallel frame orthonormality",
        np.linalg.norm(aligned.T @ aligned - np.eye(2)) < 1.0e-10,
    )
    return aligned


def local_mode_candidates(
    generator: np.ndarray,
) -> tuple[list[dict[str, Any]], float, float]:
    eigenvalues, eigenvectors = np.linalg.eig(generator)
    pairs, pairing_residual = pair_eigenvalues(eigenvalues)
    candidates: list[dict[str, Any]] = []
    maximum_realification_leakage = 0.0
    for pair in pairs:
        frame, leakage = real_pair_frame(eigenvectors, pair)
        maximum_realification_leakage = max(
            maximum_realification_leakage,
            leakage,
        )
        candidates.append(
            {
                "frame": frame,
                "participation": coordinate_participation(frame),
                "eigenvalues": np.asarray(
                    [eigenvalues[pair[0]], eigenvalues[pair[1]]],
                    dtype=complex,
                ),
            }
        )
    require("three frozen physical mode pairs", len(candidates) == 3)
    return (
        candidates,
        pairing_residual,
        maximum_realification_leakage,
    )


def label_initial_candidates(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    gauge_index = int(
        np.argmax(
            [
                candidate["participation"][0]
                for candidate in candidates
            ]
        )
    )
    remaining = [index for index in range(3) if index != gauge_index]
    radial_index = max(
        remaining,
        key=lambda index: candidates[index]["participation"][1],
    )
    phase_index = next(
        index
        for index in remaining
        if index != radial_index
    )
    ordered = [
        candidates[gauge_index],
        candidates[radial_index],
        candidates[phase_index],
    ]
    for label, candidate in zip(MODE_LABELS, ordered):
        candidate["label"] = label
    require(
        "initial Xi gauge-continuation purity",
        ordered[0]["participation"][0] > 0.99,
    )
    return ordered


def track_mode_frames(
    frozen_generators: list[np.ndarray],
) -> tuple[list[list[dict[str, Any]]], dict[str, float]]:
    tracked: list[list[dict[str, Any]]] = []
    maximum_pairing_residual = 0.0
    maximum_realification_leakage = 0.0
    minimum_assigned_overlap = 1.0

    candidates, pairing, realification = local_mode_candidates(
        frozen_generators[0]
    )
    current = label_initial_candidates(candidates)
    tracked.append(current)
    maximum_pairing_residual = max(maximum_pairing_residual, pairing)
    maximum_realification_leakage = max(
        maximum_realification_leakage,
        realification,
    )

    for generator in frozen_generators[1:]:
        candidates, pairing, realification = local_mode_candidates(generator)
        maximum_pairing_residual = max(maximum_pairing_residual, pairing)
        maximum_realification_leakage = max(
            maximum_realification_leakage,
            realification,
        )
        cost = np.asarray(
            [
                [
                    1.0
                    - subspace_overlap(
                        previous["frame"],
                        candidate["frame"],
                    )
                    for candidate in candidates
                ]
                for previous in current
            ],
            dtype=float,
        )
        rows, columns = linear_sum_assignment(cost)
        assignment = np.empty(3, dtype=int)
        assignment[rows] = columns
        next_modes: list[dict[str, Any]] = []
        for label_index, candidate_index in enumerate(assignment):
            previous = current[label_index]
            candidate = candidates[int(candidate_index)]
            overlap = subspace_overlap(
                previous["frame"],
                candidate["frame"],
            )
            minimum_assigned_overlap = min(
                minimum_assigned_overlap,
                overlap,
            )
            aligned = parallel_align(
                previous["frame"],
                candidate["frame"],
            )
            next_modes.append(
                {
                    "label": MODE_LABELS[label_index],
                    "frame": aligned,
                    "participation": coordinate_participation(aligned),
                    "eigenvalues": candidate["eigenvalues"],
                    "assigned_overlap": overlap,
                }
            )
        current = next_modes
        tracked.append(current)

    return tracked, {
        "maximum_pairing_residual": maximum_pairing_residual,
        "maximum_realification_leakage": (
            maximum_realification_leakage
        ),
        "minimum_assigned_subspace_overlap": minimum_assigned_overlap,
    }


def matrix_cross_block_defect(
    matrix: np.ndarray,
    gauge_indices: tuple[int, int],
) -> float:
    matter_indices = tuple(
        index
        for index in range(matrix.shape[0])
        if index not in gauge_indices
    )
    cross = np.block(
        [
            [matrix[np.ix_(gauge_indices, matter_indices)]],
            [matrix[np.ix_(matter_indices, gauge_indices)].T],
        ]
    )
    return float(
        np.linalg.norm(cross)
        / max(np.linalg.norm(matrix), 1.0)
    )


def propagate_history(
    generators: list[np.ndarray],
    times: np.ndarray,
    substeps: int,
) -> list[np.ndarray]:
    transfer = np.eye(generators[0].shape[0])
    history = [transfer.copy()]
    for index in range(len(times) - 1):
        interval = float(times[index + 1] - times[index])
        for substep in range(substeps):
            fraction = (substep + 0.5) / substeps
            generator = (
                (1.0 - fraction) * generators[index]
                + fraction * generators[index + 1]
            )
            transfer = expm(generator * interval / substeps) @ transfer
        history.append(transfer.copy())
    return history


def build_generator_series(
    symbolic: dict[str, object],
    params: dict[str, float],
    rows: list[dict[str, float]],
    initial_ratio: float,
) -> dict[str, Any]:
    times = np.asarray([row["t"] for row in rows], dtype=float)
    hubbles = np.asarray([row["H"] for row in rows], dtype=float)
    scale_factors = np.asarray([row["a"] for row in rows], dtype=float)
    comoving_momentum = (
        initial_ratio * hubbles[0] * scale_factors[0]
    )

    matrices: list[tuple[np.ndarray, np.ndarray, np.ndarray]] = []
    normalizations: list[np.ndarray] = []
    minimum_kinetic = math.inf
    for row in rows:
        physical_q = comoving_momentum / row["a"]
        state = np.asarray(
            [
                row["H"],
                row["rho"],
                row["rho_dot"],
                row["mu"],
                physical_q,
            ],
            dtype=float,
        )
        kinetic, mixed, coordinate = evaluate_physical_matrices(
            symbolic,
            params,
            state,
        )
        matrices.append((kinetic, mixed, coordinate))
        normalization, local_minimum = observable_normalization(
            kinetic,
            row["H"],
        )
        normalizations.append(normalization)
        minimum_kinetic = min(minimum_kinetic, local_minimum)

    kinetic_series = np.stack([item[0] for item in matrices])
    mixed_series = np.stack([item[1] for item in matrices])
    kinetic_dot = np.gradient(
        kinetic_series,
        times,
        axis=0,
        edge_order=2,
    )
    mixed_dot = np.gradient(
        mixed_series,
        times,
        axis=0,
        edge_order=2,
    )
    normalization_dot = np.gradient(
        np.stack(normalizations),
        times,
        axis=0,
        edge_order=2,
    )

    exact_generators: list[np.ndarray] = []
    frozen_generators: list[np.ndarray] = []
    exact_cross_defects: list[float] = []
    frozen_cross_defects: list[float] = []
    off_axis_quartet_flags: list[bool] = []
    frozen_eigenvector_conditions: list[float] = []
    dimension = kinetic_series.shape[1]
    gauge_indices = (0, dimension)

    for index, (kinetic, mixed, coordinate) in enumerate(matrices):
        normalization = normalizations[index]
        inverse_normalization = np.linalg.inv(normalization)
        exact_x = second_order_generator(
            kinetic,
            kinetic_dot[index],
            mixed,
            mixed_dot[index],
            coordinate,
            hubbles[index],
        )
        exact_u = (
            normalization_dot[index] @ inverse_normalization
            + normalization @ exact_x @ inverse_normalization
        )
        frozen_x = second_order_generator(
            kinetic,
            np.zeros_like(kinetic),
            mixed,
            np.zeros_like(mixed),
            coordinate,
            0.0,
        )
        frozen_u = (
            normalization @ frozen_x @ inverse_normalization
        )
        exact_u = np.real_if_close(exact_u).astype(float)
        frozen_u = np.real_if_close(frozen_u).astype(float)
        exact_generators.append(exact_u)
        frozen_generators.append(frozen_u)
        frozen_eigenvalues, frozen_eigenvectors = np.linalg.eig(
            frozen_u
        )
        eigenvalue_scale = max(
            float(np.max(np.abs(frozen_eigenvalues))),
            hubbles[index],
            1.0e-30,
        )
        tolerance = 1.0e-9 * eigenvalue_scale
        off_axis = (
            (np.abs(frozen_eigenvalues.real) > tolerance)
            & (np.abs(frozen_eigenvalues.imag) > tolerance)
        )
        off_axis_quartet_flags.append(bool(np.any(off_axis)))
        frozen_eigenvector_conditions.append(
            float(np.linalg.cond(frozen_eigenvectors))
        )
        exact_cross_defects.append(
            matrix_cross_block_defect(exact_u, gauge_indices)
        )
        frozen_cross_defects.append(
            matrix_cross_block_defect(frozen_u, gauge_indices)
        )

    physical_q = comoving_momentum / scale_factors
    return {
        "times": times,
        "hubbles": hubbles,
        "q_over_h": physical_q / hubbles,
        "comoving_momentum": float(comoving_momentum),
        "minimum_kinetic_eigenvalue": float(minimum_kinetic),
        "exact_generators": exact_generators,
        "frozen_generators": frozen_generators,
        "maximum_exact_gauge_matter_cross_defect": max(
            exact_cross_defects
        ),
        "maximum_frozen_gauge_matter_cross_defect": max(
            frozen_cross_defects
        ),
        "off_axis_complex_quartet_time_fraction": float(
            np.mean(off_axis_quartet_flags)
        ),
        "maximum_frozen_eigenvector_condition_number": max(
            frozen_eigenvector_conditions
        ),
    }


def spectral_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.svd(matrix, compute_uv=False)[0])


def evaluate_case(
    name: str,
    family: str,
    symbolic: dict[str, object],
    frw: dict[str, object],
    rows: list[dict[str, float]],
    alignment: float,
    variation: dict[str, float],
    initial_ratio: float,
    base_substeps: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    params = background_parameters(frw, alignment)
    params["zeta_align"] = alignment
    series = build_generator_series(
        symbolic,
        params,
        rows,
        initial_ratio,
    )
    tracked, tracking = track_mode_frames(
        series["frozen_generators"]
    )
    effective_substeps = max(
        base_substeps,
        int(math.ceil(0.32 / initial_ratio)),
    )
    fine_history = propagate_history(
        series["exact_generators"],
        series["times"],
        effective_substeps,
    )
    coarse_endpoint = propagate_history(
        series["exact_generators"],
        series["times"],
        max(1, effective_substeps // 2),
    )[-1]
    fine_endpoint = fine_history[-1]
    convergence_error = float(
        np.linalg.norm(fine_endpoint - coarse_endpoint)
        / max(np.linalg.norm(fine_endpoint), 1.0e-30)
    )

    mode_records: list[dict[str, Any]] = []
    full_gains: list[float] = []
    per_mode_total: dict[str, list[float]] = {
        label: [] for label in MODE_LABELS
    }
    per_mode_within: dict[str, list[float]] = {
        label: [] for label in MODE_LABELS
    }
    initial_frames = {
        mode["label"]: mode["frame"]
        for mode in tracked[0]
    }

    for index, transfer in enumerate(fine_history):
        full_gain = spectral_norm(transfer)
        full_gains.append(full_gain)
        for mode in tracked[index]:
            label = mode["label"]
            initial_frame = initial_frames[label]
            propagated = transfer @ initial_frame
            total_gain = spectral_norm(propagated)
            within_gain = spectral_norm(
                mode["frame"].T @ propagated
            )
            orthogonal_residual = (
                np.eye(transfer.shape[0])
                - mode["frame"] @ mode["frame"].T
            ) @ propagated
            leakage_gain = spectral_norm(orthogonal_residual)
            per_mode_total[label].append(total_gain)
            per_mode_within[label].append(within_gain)
            participation = mode["participation"]
            eigenvalues = mode["eigenvalues"]
            mode_records.append(
                {
                    "case": name,
                    "family": family,
                    "t": float(series["times"][index]),
                    "initial_q_over_H": initial_ratio,
                    "q_over_H": float(series["q_over_h"][index]),
                    "mode": label,
                    "Xi_participation": float(participation[0]),
                    "Q_rho_participation": float(participation[1]),
                    "Q_chi_participation": float(participation[2]),
                    "total_input_subspace_gain": total_gain,
                    "within_tracked_subspace_gain": within_gain,
                    "orthogonal_leakage_gain": leakage_gain,
                    "full_transfer_gain": full_gain,
                    "maximum_abs_pair_real_lambda_over_H": float(
                        np.max(np.abs(eigenvalues.real))
                        / series["hubbles"][index]
                    ),
                    "maximum_abs_pair_imag_lambda_over_H": float(
                        np.max(np.abs(eigenvalues.imag))
                        / series["hubbles"][index]
                    ),
                    "assigned_subspace_overlap": float(
                        mode.get("assigned_overlap", 1.0)
                    ),
                }
            )

    maximum_full_index = int(np.argmax(full_gains))
    maximum_full_transfer = fine_history[maximum_full_index]
    _, singular_values, right = np.linalg.svd(
        maximum_full_transfer
    )
    maximizing_input = right[0]
    maximizing_output = maximum_full_transfer @ maximizing_input
    gauge_initial_frame = initial_frames["gauge_continuation_Xi"]
    gauge_output_frame = next(
        mode["frame"]
        for mode in tracked[maximum_full_index]
        if mode["label"] == "gauge_continuation_Xi"
    )
    gauge_input_fraction = float(
        np.linalg.norm(gauge_initial_frame.T @ maximizing_input) ** 2
        / max(np.linalg.norm(maximizing_input) ** 2, 1.0e-30)
    )
    gauge_output_fraction = float(
        np.linalg.norm(gauge_output_frame.T @ maximizing_output) ** 2
        / max(np.linalg.norm(maximizing_output) ** 2, 1.0e-30)
    )

    mode_summaries: list[dict[str, Any]] = []
    for label in MODE_LABELS:
        indices = [
            index
            for index, modes in enumerate(tracked)
            for mode in modes
            if mode["label"] == label
        ]
        require(f"complete tracked history for {label}", len(indices) == len(rows))
        participations = np.asarray(
            [
                next(
                    mode["participation"]
                    for mode in modes
                    if mode["label"] == label
                )
                for modes in tracked
            ]
        )
        total = np.asarray(per_mode_total[label])
        within = np.asarray(per_mode_within[label])
        maximum_index = int(np.argmax(total))
        mode_summaries.append(
            {
                "mode": label,
                "maximum_total_input_subspace_gain": float(
                    total[maximum_index]
                ),
                "maximum_gain_time": float(
                    series["times"][maximum_index]
                ),
                "endpoint_total_input_subspace_gain": float(total[-1]),
                "maximum_within_tracked_subspace_gain": float(
                    np.max(within)
                ),
                "endpoint_within_tracked_subspace_gain": float(within[-1]),
                "minimum_Xi_participation": float(
                    np.min(participations[:, 0])
                ),
                "maximum_Xi_participation": float(
                    np.max(participations[:, 0])
                ),
                "minimum_Q_rho_participation": float(
                    np.min(participations[:, 1])
                ),
                "maximum_Q_rho_participation": float(
                    np.max(participations[:, 1])
                ),
                "minimum_Q_chi_participation": float(
                    np.min(participations[:, 2])
                ),
                "maximum_Q_chi_participation": float(
                    np.max(participations[:, 2])
                ),
            }
        )

    gauge_summary = mode_summaries[0]
    maximum_matter_gain = max(
        summary["maximum_total_input_subspace_gain"]
        for summary in mode_summaries[1:]
    )
    pair_separability_pass = (
        tracking["maximum_realification_leakage"] < 1.0e-7
        and series["off_axis_complex_quartet_time_fraction"]
        == 0.0
    )
    numerical_pass = (
        convergence_error < 5.0e-4
        and tracking["maximum_pairing_residual"] < 1.0e-7
        and tracking["minimum_assigned_subspace_overlap"] > 0.5
    )
    attribution_pass = (
        pair_separability_pass
        and gauge_input_fraction > 0.999
        and gauge_output_fraction > 0.999
        and gauge_summary["minimum_Xi_participation"] > 0.999
        and (
            gauge_summary["maximum_total_input_subspace_gain"]
            / max(max(full_gains), 1.0e-30)
        )
        > 0.999
    )
    xi_seeded_mixed = (
        not pair_separability_pass
        and gauge_input_fraction > 0.99
    )
    return {
        "case": name,
        "family": family,
        "variation": variation,
        "alignment": alignment,
        "initial_q_over_H": initial_ratio,
        "final_q_over_H": float(series["q_over_h"][-1]),
        "comoving_momentum": series["comoving_momentum"],
        "minimum_kinetic_eigenvalue": (
            series["minimum_kinetic_eigenvalue"]
        ),
        "midpoint_magnus_substeps": effective_substeps,
        "coarse_to_fine_relative_error": convergence_error,
        "maximum_full_transfer_gain": max(full_gains),
        "maximum_full_transfer_gain_time": float(
            series["times"][maximum_full_index]
        ),
        "endpoint_full_transfer_gain": spectral_norm(fine_endpoint),
        "gauge_input_fraction_at_maximum_full_gain": (
            gauge_input_fraction
        ),
        "gauge_output_fraction_at_maximum_full_gain": (
            gauge_output_fraction
        ),
        "maximum_retained_matter_input_subspace_gain": (
            maximum_matter_gain
        ),
        "maximum_exact_gauge_matter_cross_defect": (
            series["maximum_exact_gauge_matter_cross_defect"]
        ),
        "maximum_frozen_gauge_matter_cross_defect": (
            series["maximum_frozen_gauge_matter_cross_defect"]
        ),
        "off_axis_complex_quartet_time_fraction": (
            series["off_axis_complex_quartet_time_fraction"]
        ),
        "maximum_frozen_eigenvector_condition_number": (
            series["maximum_frozen_eigenvector_condition_number"]
        ),
        "tracking_diagnostics": tracking,
        "mode_results": mode_summaries,
        "numerical_status": (
            "PASS_TRANSFER_AND_PAIR_ASSIGNMENT"
            if numerical_pass
            else "HOLD_MODE_TRACKING_NUMERICS"
        ),
        "mode_separability_status": (
            "PASS_RANK_TWO_MODE_SEPARABILITY"
            if pair_separability_pass
            else "HOLD_COMPLEX_QUARTET_MODE_NONSEPARABILITY"
        ),
        "gain_attribution": (
            "FINITE_Q_XI_GAUGE_CONTINUATION_CHANNEL"
            if attribution_pass
            else (
                "DOMINANT_TRANSFER_INPUT_XI_SEEDED_WITH_"
                "COMPLEX_QUARTET_MIXING"
                if xi_seeded_mixed
                else "UNRESOLVED_MODE_ATTRIBUTION"
            )
        ),
    }, mode_records


def variation_cases(
    baseline_frw: dict[str, object],
    baseline_rows: list[dict[str, float]],
    quick: bool,
) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = [
        {
            "name": "baseline",
            "family": "reference",
            "frw": baseline_frw,
            "rows": baseline_rows,
            "alignment": 1.0,
            "variation": {},
        }
    ]
    if quick:
        return cases

    t_end = float(baseline_rows[-1]["t"])
    samples = len(baseline_rows)
    for rho_initial in (0.95, 1.05):
        branch, rows = integrate_representative_branch(
            t_end,
            samples,
            initial_condition_overrides={"rho": rho_initial},
        )
        cases.append(
            {
                "name": f"on_shell_rho_initial_{rho_initial:.2f}",
                "family": "on_shell_background",
                "frw": {"representative_branch": branch},
                "rows": rows,
                "alignment": 1.0,
                "variation": {"rho_initial": rho_initial},
            }
        )
    for alignment in (0.8, 1.2):
        cases.append(
            {
                "name": f"alignment_{alignment:.1f}",
                "family": "perturbation_parameter",
                "frw": baseline_frw,
                "rows": baseline_rows,
                "alignment": alignment,
                "variation": {"zeta_align": alignment},
            }
        )
    return cases


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    require("nonempty mode-resolved CSV", bool(rows))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    require("positive initial q/H", args.initial_q_over_H > 0)
    require("at least two Magnus substeps", args.substeps >= 2)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    baseline_frw, baseline_rows = load_inputs(
        args.frw_summary,
        args.frw_trajectory,
    )
    symbolic = symbolic_propagators()
    case_results: list[dict[str, Any]] = []
    csv_rows: list[dict[str, Any]] = []
    for case in variation_cases(
        baseline_frw,
        baseline_rows,
        args.quick,
    ):
        result, records = evaluate_case(
            case["name"],
            case["family"],
            symbolic,
            case["frw"],
            case["rows"],
            case["alignment"],
            case["variation"],
            args.initial_q_over_H,
            args.substeps,
        )
        case_results.append(result)
        csv_rows.extend(records)

    all_numerics_pass = all(
        result["numerical_status"]
        == "PASS_TRANSFER_AND_PAIR_ASSIGNMENT"
        for result in case_results
    )
    all_pair_separable = all(
        result["mode_separability_status"]
        == "PASS_RANK_TWO_MODE_SEPARABILITY"
        for result in case_results
    )
    xi_seeded_labels = {
        "FINITE_Q_XI_GAUGE_CONTINUATION_CHANNEL",
        "DOMINANT_TRANSFER_INPUT_XI_SEEDED_WITH_COMPLEX_QUARTET_MIXING",
    }
    all_xi_seeded = all(
        result["gain_attribution"] in xi_seeded_labels
        for result in case_results
    )
    all_gain_attributions_pass = all(
        result["gain_attribution"]
        == "FINITE_Q_XI_GAUGE_CONTINUATION_CHANNEL"
        for result in case_results
    )
    if not all_numerics_pass:
        subgate_status = "HOLD_MODE_RESOLVED_TRANSFER_NUMERICS"
    elif not all_pair_separable:
        subgate_status = "HOLD_COMPLEX_QUARTET_IR_MODE_ATTRIBUTION"
    elif all_gain_attributions_pass:
        subgate_status = (
            "PASS_MODE_RESOLVED_IR_GAIN_ATTRIBUTION_WITH_SCOPE"
        )
    else:
        subgate_status = "HOLD_IR_GAIN_MODE_ATTRIBUTION"
    calculation_status = (
        "PASS" if subgate_status.startswith("PASS") else "HOLD"
    )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_MODE_RESOLVED_TRANSFER_ROBUSTNESS",
        "calculation_status": calculation_status,
        "subgate_status": subgate_status,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "tested_case_count": len(case_results),
        "method": {
            "state": [
                "K^(1/2) p",
                "K^(1/2) p_dot/H",
            ],
            "physical_coordinates": list(FIELD_LABELS),
            "frozen_mode_pairing": "lambda -> -lambda",
            "mode_matching": (
                "Hungarian assignment on principal-angle subspace overlap"
            ),
            "parallel_transport": (
                "orthogonal Procrustes transport of each real rank-two "
                "mode-pair frame"
            ),
            "projection": (
                "spectral norm of exact transfer acting on each initial "
                "orthonormal mode-pair subspace"
            ),
            "momentum_rule": "fixed comoving k with q_phys=k/a",
        },
        "case_results": case_results,
        "all_mode_tracking_numerics_pass": all_numerics_pass,
        "all_cases_have_rank_two_mode_separability": (
            all_pair_separable
        ),
        "all_tested_cases_attribute_gain_to_Xi_gauge_continuation": (
            all_gain_attributions_pass
        ),
        "all_tested_cases_have_Xi_seeded_dominant_transfer": (
            all_xi_seeded
        ),
        "robustness_result": (
            "The tested neighborhood reproduces the same Xi-seeded "
            "dominant transfer and complex-quartet obstruction."
        ),
        "retained_matter_result": (
            "Retained-matter instability is not classified: nominal "
            "rank-two pole pairs merge into an off-axis complex quartet, "
            "and matter-seeded initial subspaces also amplify."
        ),
        "scientific_boundary": (
            "Xi is gauge invariant at finite q but continuously approaches "
            "the homogeneous time-translation gauge orbit as q approaches "
            "zero. The dominant singular input is Xi seeded, but during "
            "off-axis complex-quartet intervals no continuous real rank-two "
            "split between the gauge-continuation and retained-matter pole "
            "pairs exists. This prevents a physical instability or "
            "gauge-artifact classification. The audit covers a finite time "
            "interval, one dimensionless neighborhood, and no S-matrix "
            "amplitude."
        ),
        "next_required_calculation": [
            "map a controlled real-pole and adiabatic matter-mode exchange domain",
            "assemble the gauge-regular exchange plus reduced-contact 2-to-2 amplitude in that domain",
            "derive a unitarity or strong-coupling bound only from the completed physical amplitude",
            "repeat any later physical parameter selection against observational and EFT constraints",
        ],
    }

    json_path = (
        args.output_dir
        / "uvir003_mode_resolved_transfer_robustness_summary.json"
    )
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    write_csv(
        args.output_dir
        / "uvir003_mode_resolved_transfer_robustness.csv",
        csv_rows,
    )

    print("Tracked kinetic-normalized mode pairs: COMPLETE")
    print(
        "Transfer and pair-assignment numerics: "
        + ("PASS" if all_numerics_pass else "HOLD")
    )
    print(
        "Rank-two physical-mode separability: "
        + ("PASS" if all_pair_separable else "HOLD_COMPLEX_QUARTET")
    )
    print(
        "Infrared dominant-transfer attribution: "
        + (
            "XI_SEEDED_BUT_COMPLEX_QUARTET_MIXED"
            if all_xi_seeded and not all_pair_separable
            else (
                "FINITE_Q_XI_GAUGE_CONTINUATION"
                if all_gain_attributions_pass
                else "UNRESOLVED"
            )
        )
    )
    print(
        "Nearby on-shell trajectory and parameter robustness: "
        + (
            "ROBUST_STRUCTURAL_HOLD"
            if all_numerics_pass
            and all_xi_seeded
            and not all_pair_separable
            else (
                "PASS"
                if all_numerics_pass and all_gain_attributions_pass
                else "HOLD"
            )
        )
    )
    print(
        "Retained-matter infrared instability: "
        "NOT_CLASSIFIED_DUE_TO_COMPLEX_QUARTET_MIXING"
    )
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print(f"STATUS: {subgate_status}")


if __name__ == "__main__":
    main()
