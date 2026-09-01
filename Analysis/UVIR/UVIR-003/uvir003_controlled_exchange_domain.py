#!/usr/bin/env python3
"""Map the controlled real-pole adiabatic exchange domain for UVIR-003.

The audit follows fixed comoving momenta on the representative evolving FRW
branch.  A sampled trajectory is admitted only when

* the finite-q kinetic matrix remains positive;
* every frozen physical pole remains real;
* max |omega_dot/omega^2| is below the declared adiabatic threshold;
* the factorized Pi mode satisfies the same threshold; and
* every physical frequency remains subhorizon by the declared margin.

The same criterion applies independently to each nonzero internal exchange
momentum q_K.  Passing external legs therefore does not automatically admit a
soft exchange channel.  This script establishes the domain and the
mode-projector interface; it does not assemble or normalize a 2-to-2
amplitude.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linear_sum_assignment

from uvir003_mode_resolved_transfer_robustness import (
    build_generator_series,
    local_mode_candidates,
    parallel_align,
    subspace_overlap,
)
from uvir003_physical_quadratic_propagators import symbolic_propagators
from uvir003_scalar_adm_finite_q import (
    background_parameters,
    load_inputs,
)


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
        "--cubic-kernel",
        type=Path,
        default=base / "outputs" / "uvir003_cubic_momentum_kernel_summary.json",
    )
    parser.add_argument(
        "--quartic-kernel",
        type=Path,
        default=(
            base
            / "outputs"
            / "uvir003_reduced_quartic_momentum_kernel_summary.json"
        ),
    )
    parser.add_argument(
        "--ratios",
        type=float,
        nargs="+",
        default=[10.0, 20.0, 30.0, 40.0, 45.0, 47.5, 50.0, 75.0, 100.0],
        help="Initial q_phys/H samples followed at fixed comoving momentum.",
    )
    parser.add_argument("--alignment", type=float, default=1.0)
    parser.add_argument("--K-Q", type=float, default=1.0)
    parser.add_argument("--gamma", type=float, default=1.0)
    parser.add_argument("--M-star-sq", type=float, default=1.0)
    parser.add_argument("--adiabatic-threshold", type=float, default=0.1)
    parser.add_argument("--subhorizon-margin", type=float, default=10.0)
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def mode_frequency(
    eigenvalues: np.ndarray,
    hubble: float,
) -> tuple[float, bool]:
    scale = max(float(np.max(np.abs(eigenvalues))), hubble, 1.0e-30)
    tolerance = 2.0e-7 * scale
    stable = bool(np.all(np.abs(eigenvalues.real) <= tolerance))
    frequency = float(np.max(np.abs(eigenvalues.imag)))
    return frequency, stable


def track_unlabelled_mode_frames(
    frozen_generators: list[np.ndarray],
) -> tuple[list[list[dict[str, Any]]], dict[str, float]]:
    """Track all finite-q physical pairs without imposing an IR label."""
    current, pairing, realification = local_mode_candidates(
        frozen_generators[0]
    )
    current = sorted(
        current,
        key=lambda candidate: float(
            np.max(np.abs(candidate["eigenvalues"].imag))
        ),
    )
    for index, candidate in enumerate(current, start=1):
        candidate["label"] = f"physical_pair_{index}"
    tracked = [current]
    maximum_pairing = pairing
    maximum_realification = realification
    minimum_overlap = 1.0

    for generator in frozen_generators[1:]:
        candidates, pairing, realification = local_mode_candidates(generator)
        maximum_pairing = max(maximum_pairing, pairing)
        maximum_realification = max(maximum_realification, realification)
        cost = np.asarray(
            [
                [
                    1.0 - subspace_overlap(previous["frame"], candidate["frame"])
                    for candidate in candidates
                ]
                for previous in current
            ],
            dtype=float,
        )
        rows, columns = linear_sum_assignment(cost)
        assignment = np.empty(len(current), dtype=int)
        assignment[rows] = columns
        next_modes: list[dict[str, Any]] = []
        for mode_index, candidate_index in enumerate(assignment):
            candidate = candidates[int(candidate_index)]
            overlap = subspace_overlap(
                current[mode_index]["frame"], candidate["frame"]
            )
            minimum_overlap = min(minimum_overlap, overlap)
            candidate["frame"] = parallel_align(
                current[mode_index]["frame"], candidate["frame"]
            )
            candidate["label"] = current[mode_index]["label"]
            candidate["assigned_overlap"] = overlap
            next_modes.append(candidate)
        current = next_modes
        tracked.append(current)

    return tracked, {
        "maximum_pairing_residual": maximum_pairing,
        "maximum_realification_leakage": maximum_realification,
        "minimum_assigned_subspace_overlap": minimum_overlap,
    }


def audit_ratio(
    symbolic: dict[str, object],
    params: dict[str, float],
    rows: list[dict[str, float]],
    ratio: float,
    k_q: float,
    gamma: float,
    mstar2: float,
    adiabatic_threshold: float,
    subhorizon_margin: float,
) -> dict[str, Any]:
    series = build_generator_series(symbolic, params, rows, ratio)
    tracked, tracking = track_unlabelled_mode_frames(
        series["frozen_generators"]
    )
    times = np.asarray(series["times"], dtype=float)
    hubbles = np.asarray(series["hubbles"], dtype=float)

    frequencies = np.zeros((len(times), 3), dtype=float)
    stable = np.ones_like(frequencies, dtype=bool)
    for time_index, modes in enumerate(tracked):
        for mode_index, mode in enumerate(modes):
            frequency, is_stable = mode_frequency(
                mode["eigenvalues"],
                hubbles[time_index],
            )
            frequencies[time_index, mode_index] = frequency
            stable[time_index, mode_index] = is_stable

    frequency_dot = np.gradient(
        frequencies,
        times,
        axis=0,
        edge_order=2,
    )
    adiabaticity = np.abs(frequency_dot) / np.maximum(
        frequencies**2,
        1.0e-30,
    )
    frequency_over_h = frequencies / hubbles[:, None]

    physical_q = np.asarray(series["q_over_h"]) * hubbles
    force_frequency = (
        math.sqrt(gamma / (k_q * mstar2)) * physical_q**2
    )
    force_adiabaticity = 2.0 * hubbles / np.maximum(
        force_frequency,
        1.0e-30,
    )
    force_frequency_over_h = force_frequency / hubbles

    initial_modes = tracked[0]
    initial_projectors: dict[str, list[list[float]]] = {}
    for mode in initial_modes:
        frame = np.asarray(mode["frame"], dtype=float)
        projector = frame @ frame.T
        initial_projectors[mode["label"]] = projector.tolist()
    maximum_projector_idempotence = max(
        float(np.linalg.norm(projector @ projector - projector))
        for projector in (
            np.asarray(value, dtype=float)
            for value in initial_projectors.values()
        )
    )

    all_real = bool(np.all(stable))
    maximum_adiabaticity = float(np.max(adiabaticity))
    minimum_frequency_over_h = float(np.min(frequency_over_h))
    maximum_force_adiabaticity = float(np.max(force_adiabaticity))
    minimum_force_frequency_over_h = float(
        np.min(force_frequency_over_h)
    )
    admitted = bool(
        series["minimum_kinetic_eigenvalue"] > 0.0
        and all_real
        and maximum_adiabaticity < adiabatic_threshold
        and maximum_force_adiabaticity < adiabatic_threshold
        and minimum_frequency_over_h >= subhorizon_margin
        and minimum_force_frequency_over_h >= subhorizon_margin
        and tracking["maximum_pairing_residual"] < 1.0e-8
        and tracking["maximum_realification_leakage"] < 1.0e-8
        and tracking["minimum_assigned_subspace_overlap"] > 0.5
        and maximum_projector_idempotence < 1.0e-10
    )

    return {
        "initial_q_over_H": ratio,
        "final_q_over_H": float(series["q_over_h"][-1]),
        "minimum_kinetic_eigenvalue": series["minimum_kinetic_eigenvalue"],
        "all_frozen_physical_poles_real": all_real,
        "maximum_physical_mode_adiabaticity": maximum_adiabaticity,
        "minimum_physical_abs_omega_over_H": minimum_frequency_over_h,
        "maximum_force_mode_adiabaticity": maximum_force_adiabaticity,
        "minimum_force_abs_omega_over_H": minimum_force_frequency_over_h,
        "maximum_pairing_residual": tracking["maximum_pairing_residual"],
        "maximum_realification_leakage": (
            tracking["maximum_realification_leakage"]
        ),
        "minimum_assigned_subspace_overlap": (
            tracking["minimum_assigned_subspace_overlap"]
        ),
        "maximum_initial_mode_projector_idempotence_residual": (
            maximum_projector_idempotence
        ),
        "admitted_controlled_exchange_trajectory": admitted,
        "initial_phase_space_mode_projectors": initial_projectors,
    }


def write_csv(path: Path, results: list[dict[str, Any]]) -> None:
    excluded = {"initial_phase_space_mode_projectors"}
    rows = [
        {key: value for key, value in result.items() if key not in excluded}
        for result in results
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    require("positive ratios", all(value > 0.0 for value in args.ratios))
    require("positive K_Q", args.K_Q > 0.0)
    require("positive gamma", args.gamma > 0.0)
    require("positive M_star_sq", args.M_star_sq > 0.0)
    require("positive adiabatic threshold", args.adiabatic_threshold > 0.0)
    require("subhorizon margin above unity", args.subhorizon_margin > 1.0)

    frw, rows = load_inputs(args.frw_summary, args.frw_trajectory)
    params = background_parameters(frw, args.alignment)
    params["zeta_align"] = args.alignment
    symbolic = symbolic_propagators()

    cubic = load_json(args.cubic_kernel)
    quartic = load_json(args.quartic_kernel)
    require(
        "verified finite-q cubic kernel",
        cubic["subgate_status"]
        == "PASS_FACTORIZED_FINITE_Q_PHYSICAL_CUBIC_KERNEL",
    )
    require(
        "verified reduced quartic kernel",
        quartic["subgate_status"]
        == "PASS_FACTORIZED_FINITE_Q_REDUCED_QUARTIC_KERNEL",
    )
    require(
        "verified pair source",
        quartic["complete_pair_source_status"] == "DERIVED_AND_VERIFIED",
    )

    results = [
        audit_ratio(
            symbolic,
            params,
            rows,
            ratio,
            args.K_Q,
            args.gamma,
            args.M_star_sq,
            args.adiabatic_threshold,
            args.subhorizon_margin,
        )
        for ratio in sorted(set(args.ratios))
    ]
    admitted = [
        result
        for result in results
        if result["admitted_controlled_exchange_trajectory"]
    ]
    require("nonempty controlled exchange sample", bool(admitted))
    lower_sample = min(
        float(result["initial_q_over_H"]) for result in admitted
    )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_CONTROLLED_EXCHANGE_DOMAIN",
        "calculation_status": "PASS",
        "subgate_status": (
            "PASS_CONTROLLED_REAL_POLE_ADIABATIC_EXCHANGE_DOMAIN"
        ),
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "criteria": {
            "momentum_rule": "fixed comoving k with q_phys=k/a",
            "all_frozen_physical_poles_real": True,
            "minimum_kinetic_eigenvalue": ">0",
            "maximum_physical_mode_adiabaticity": (
                f"<{args.adiabatic_threshold}"
            ),
            "maximum_force_mode_adiabaticity": (
                f"<{args.adiabatic_threshold}"
            ),
            "minimum_abs_omega_over_H": (
                f">={args.subhorizon_margin}"
            ),
            "mode_pairing_residual": "<1e-8",
            "mode_realification_leakage": "<1e-8",
            "mode_assignment_overlap": ">0.5",
        },
        "sampled_domain": {
            "admitted_initial_q_over_H_values": [
                result["initial_q_over_H"] for result in admitted
            ],
            "lowest_admitted_sample": lower_sample,
            "boundary_statement": (
                "The audit establishes only the listed sampled trajectories; "
                "it does not prove every unsampled q/H above the lowest "
                "passing sample is admitted."
            ),
        },
        "kernel_interface": {
            "cubic_kernel_status": cubic["subgate_status"],
            "reduced_quartic_kernel_status": quartic["subgate_status"],
            "external_leg_rule": (
                "Each external finite-q leg must lie on an admitted "
                "trajectory and be projected with its tracked local "
                "phase-space mode projector."
            ),
            "nonzero_internal_channel_rule": (
                "Each q_K=|k_a+k_b| must independently satisfy the same "
                "controlled-domain criteria and det(C(q_K))!=0."
            ),
            "exact_q0_channel_rule": (
                "q_K=0 is excluded from the finite-q propagator domain and "
                "must use the separately audited homogeneous projector."
            ),
            "projector_scope": (
                "The stored unlabelled projectors establish the complete "
                "three-pair finite-q eigenmode interface in kinetic-normalized "
                "phase space. No infrared Xi-pure label is imposed in the "
                "high-q domain. Retained-channel identification, vertex "
                "contraction, external normalization, time/frequency "
                "prescription, and channel summation remain unassembled."
            ),
        },
        "trajectory_results": results,
        "parameter_scope": (
            "Representative dimensionless branch only. K_Q=gamma="
            "M_star_sq=1 remains a diagnostic force-mode normalization."
        ),
        "scientific_boundary": (
            "This pass establishes a nonempty sampled real-pole adiabatic "
            "domain and a verified interface to the existing factorized "
            "interaction kernels. It is not a scattering amplitude, "
            "unitarity bound, strong-coupling scale, physical cutoff, or "
            "all-background stability theorem."
        ),
        "next_required_calculation": [
            "contract the verified cubic pair sources with tracked retained-matter mode legs inside the admitted domain",
            "assemble the nonzero-channel propagator exchange term",
            "apply the separate q_K=0 homogeneous projector where required",
            "combine exchange with the reduced quartic contact before applying any unitarity criterion",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = (
        args.output_dir
        / "uvir003_controlled_exchange_domain_summary.json"
    )
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    write_csv(
        args.output_dir / "uvir003_controlled_exchange_domain.csv",
        results,
    )

    print("Controlled real-pole domain map: COMPLETE")
    print(f"Lowest admitted sampled initial q/H: {lower_sample:g}")
    print("Finite-q cubic/reduced-quartic interface: VERIFIED")
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_CONTROLLED_REAL_POLE_ADIABATIC_EXCHANGE_DOMAIN")


if __name__ == "__main__":
    main()
