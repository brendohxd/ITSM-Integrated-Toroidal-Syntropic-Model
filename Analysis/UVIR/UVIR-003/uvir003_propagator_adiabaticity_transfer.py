#!/usr/bin/env python3
"""UVIR-003 fixed-comoving adiabaticity and time-domain transfer audit.

This follows the finite-q physical variables

    p = (Xi, Q_rho, Q_chi)

along the verified evolving FRW branch at fixed comoving momentum k, so that
q_phys=k/a.  It tracks the local frozen-time poles, evaluates
|omega_dot/omega^2| where a real-frequency interpretation exists, and evolves
the full gauge-invariant second-order system while independently verifying its
canonical Hamiltonian form.

The factorized force scalar Pi is audited analytically.  No scattering
amplitude, unitarity scale, strong-coupling scale, or physical cutoff is
derived here.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import linear_sum_assignment

from uvir003_physical_quadratic_propagators import (
    evaluate_physical_matrices,
    quadratic_poles,
    symbolic_propagators,
)
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
    parser.add_argument("--alignment", type=float, default=1.0)
    parser.add_argument("--K-Q", type=float, default=1.0)
    parser.add_argument("--gamma", type=float, default=1.0)
    parser.add_argument("--M-star-sq", type=float, default=1.0)
    parser.add_argument(
        "--substeps",
        type=int,
        default=4,
        help="Fine midpoint-Magnus substeps per trajectory interval.",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def symmetrize(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.T) / 2


def positive_matrix_sqrt(
    matrix: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float]:
    eigenvalues, eigenvectors = np.linalg.eigh(symmetrize(matrix))
    require("positive normalization kinetic matrix", np.min(eigenvalues) > 0)
    square_root = (
        eigenvectors
        @ np.diag(np.sqrt(eigenvalues))
        @ eigenvectors.T
    )
    inverse_square_root = (
        eigenvectors
        @ np.diag(1 / np.sqrt(eigenvalues))
        @ eigenvectors.T
    )
    return square_root, inverse_square_root, float(np.min(eigenvalues))


def canonical_generator(
    kinetic: np.ndarray,
    mixed: np.ndarray,
    coordinate: np.ndarray,
    scale_factor: float,
) -> np.ndarray:
    """Return the Hamiltonian generator for z=(p,canonical momentum).

    The quadratic action is

        integral dt a^3 [
          1/2 p_dot^T K p_dot + p_dot^T P p + 1/2 p^T C p
        ].
    """

    inverse_kinetic = np.linalg.inv(kinetic)
    volume = scale_factor**3
    return np.block(
        [
            [
                -inverse_kinetic @ mixed,
                inverse_kinetic / volume,
            ],
            [
                volume
                * (
                    coordinate
                    - mixed.T @ inverse_kinetic @ mixed
                ),
                mixed.T @ inverse_kinetic,
            ],
        ]
    )


def observable_normalization(
    kinetic: np.ndarray,
    hubble: float,
) -> tuple[np.ndarray, float]:
    """Map x=(p,p_dot) to u=(K^1/2 p,K^1/2 p_dot/H)."""

    root, _, minimum_kinetic = positive_matrix_sqrt(kinetic)
    dimension = kinetic.shape[0]
    zero = np.zeros((dimension, dimension))
    transform = np.block([[root, zero], [zero, root / hubble]])
    return transform, minimum_kinetic


def second_order_generator(
    kinetic: np.ndarray,
    kinetic_dot: np.ndarray,
    mixed: np.ndarray,
    mixed_dot: np.ndarray,
    coordinate: np.ndarray,
    hubble: float,
) -> np.ndarray:
    """Return the exact x=(p,p_dot) generator including a^3 dilution."""

    dimension = kinetic.shape[0]
    damping = kinetic_dot + 3 * hubble * kinetic + mixed - mixed.T
    stiffness = mixed_dot + 3 * hubble * mixed - coordinate
    return np.block(
        [
            [np.zeros((dimension, dimension)), np.eye(dimension)],
            [
                -np.linalg.solve(kinetic, stiffness),
                -np.linalg.solve(kinetic, damping),
            ],
        ]
    )


def hamiltonian_generator_defect(generator: np.ndarray) -> float:
    dimension = generator.shape[0] // 2
    identity = np.eye(dimension)
    zero = np.zeros_like(identity)
    symplectic_form = np.block([[zero, identity], [-identity, zero]])
    return float(
        np.linalg.norm(
            generator.T @ symplectic_form
            + symplectic_form @ generator
        )
        / max(np.linalg.norm(generator), 1.0)
    )


def representative_poles(poles: np.ndarray) -> np.ndarray:
    scale = max(float(np.max(np.abs(poles))), 1.0)
    tolerance = 1.0e-9 * scale
    selected = [
        pole
        for pole in poles
        if (
            pole.real > tolerance
            or (
                abs(pole.real) <= tolerance
                and pole.imag >= -tolerance
            )
        )
    ]
    if len(selected) != len(poles) // 2:
        ordered = sorted(
            poles,
            key=lambda value: (
                value.real < 0,
                abs(value),
                value.imag,
            ),
        )
        selected = ordered[: len(poles) // 2]
    require(
        "one representative per pole pair",
        len(selected) == len(poles) // 2,
    )
    return np.asarray(sorted(selected, key=abs), dtype=complex)


def track_poles(poles_by_time: list[np.ndarray]) -> np.ndarray:
    tracked = np.empty(
        (len(poles_by_time), len(poles_by_time[0]) // 2),
        dtype=complex,
    )
    tracked[0] = representative_poles(poles_by_time[0])
    for index in range(1, len(poles_by_time)):
        candidates = representative_poles(poles_by_time[index])
        scale = np.maximum(
            np.maximum(np.abs(tracked[index - 1])[:, None], np.abs(candidates)),
            1.0e-12,
        )
        cost = np.abs(
            tracked[index - 1][:, None] - candidates[None, :]
        ) / scale
        rows, columns = linear_sum_assignment(cost)
        ordering = np.empty(len(columns), dtype=int)
        ordering[rows] = columns
        tracked[index] = candidates[ordering]
    return tracked


def propagate_magnus(
    generators: list[np.ndarray],
    times: np.ndarray,
    normalizations: list[np.ndarray],
    substeps: int,
    record: bool,
) -> tuple[np.ndarray, list[dict[str, float]]]:
    dimension = generators[0].shape[0]
    transfer = np.eye(dimension)
    initial_inverse = np.linalg.inv(normalizations[0])
    records: list[dict[str, float]] = []

    def record_state(index: int) -> None:
        normalized = (
            normalizations[index] @ transfer @ initial_inverse
        )
        singular_values = np.linalg.svd(
            normalized, compute_uv=False
        )
        records.append(
            {
                "t": float(times[index]),
                "largest_normalized_singular_value": float(
                    singular_values[0]
                ),
                "smallest_normalized_singular_value": float(
                    singular_values[-1]
                ),
                "normalized_condition_number": float(
                    singular_values[0] / singular_values[-1]
                ),
            }
        )

    if record:
        record_state(0)
    for index in range(len(times) - 1):
        interval = float(times[index + 1] - times[index])
        for substep in range(substeps):
            fraction = (substep + 0.5) / substeps
            generator = (
                (1 - fraction) * generators[index]
                + fraction * generators[index + 1]
            )
            transfer = expm(generator * interval / substeps) @ transfer
        if record:
            record_state(index + 1)
    return transfer, records


def evaluate_fixed_comoving_mode(
    symbolic: dict[str, object],
    params: dict[str, float],
    rows: list[dict[str, float]],
    initial_ratio: float,
    k_q: float,
    gamma: float,
    mstar2: float,
    substeps: int,
) -> tuple[dict[str, object], list[dict[str, float]]]:
    times = np.asarray([row["t"] for row in rows], dtype=float)
    hubbles = np.asarray([row["H"] for row in rows], dtype=float)
    scale_factors = np.asarray([row["a"] for row in rows], dtype=float)
    comoving_momentum = (
        initial_ratio * hubbles[0] * scale_factors[0]
    )

    matrices: list[tuple[np.ndarray, np.ndarray, np.ndarray]] = []
    normalizations: list[np.ndarray] = []
    poles_by_time: list[np.ndarray] = []
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
            symbolic, params, state
        )
        matrices.append((kinetic, mixed, coordinate))
        normalization, local_minimum = observable_normalization(
            kinetic, row["H"]
        )
        normalizations.append(normalization)
        minimum_kinetic = min(minimum_kinetic, local_minimum)
        poles_by_time.append(
            quadratic_poles(kinetic, mixed, coordinate)
        )

    kinetic_series = np.stack([item[0] for item in matrices])
    mixed_series = np.stack([item[1] for item in matrices])
    kinetic_dot_series = np.gradient(
        kinetic_series, times, axis=0, edge_order=2
    )
    mixed_dot_series = np.gradient(
        mixed_series, times, axis=0, edge_order=2
    )

    second_order_generators: list[np.ndarray] = []
    canonical_generators: list[np.ndarray] = []
    canonical_maps: list[np.ndarray] = []
    dimension = kinetic_series.shape[1]
    identity = np.eye(dimension)
    zero = np.zeros_like(identity)
    for index, (kinetic, mixed, coordinate) in enumerate(matrices):
        second_order_generators.append(
            second_order_generator(
                kinetic,
                kinetic_dot_series[index],
                mixed,
                mixed_dot_series[index],
                coordinate,
                hubbles[index],
            )
        )
        canonical_generators.append(
            canonical_generator(
                kinetic,
                mixed,
                coordinate,
                scale_factors[index],
            )
        )
        volume = scale_factors[index] ** 3
        canonical_maps.append(
            np.block(
                [
                    [identity, zero],
                    [volume * mixed, volume * kinetic],
                ]
            )
        )

    canonical_map_dot = np.gradient(
        np.stack(canonical_maps), times, axis=0, edge_order=2
    )
    canonical_equivalence_residuals: list[float] = []
    for index, canonical_map in enumerate(canonical_maps):
        inverse_map = np.linalg.inv(canonical_map)
        transformed = (
            canonical_map_dot[index] @ inverse_map
            + canonical_map
            @ second_order_generators[index]
            @ inverse_map
        )
        canonical_equivalence_residuals.append(
            float(
                np.linalg.norm(
                    transformed - canonical_generators[index]
                )
                / max(np.linalg.norm(canonical_generators[index]), 1.0)
            )
        )

    normalization_dot = np.gradient(
        np.stack(normalizations), times, axis=0, edge_order=2
    )
    generators: list[np.ndarray] = []
    for index, normalization in enumerate(normalizations):
        inverse_normalization = np.linalg.inv(normalization)
        generators.append(
            normalization_dot[index] @ inverse_normalization
            + normalization
            @ second_order_generators[index]
            @ inverse_normalization
        )

    tracked = track_poles(poles_by_time)
    pole_derivative = np.gradient(tracked, times, axis=0)
    transfer_normalizations = [
        np.eye(2 * dimension) for _ in times
    ]

    pole_scale = np.maximum(np.abs(tracked), hubbles[:, None])
    complex_mask = (
        np.abs(tracked.imag) > 2.0e-7 * pole_scale
    )
    real_mask = ~complex_mask
    adiabaticity = np.abs(pole_derivative) / np.maximum(
        np.abs(tracked) ** 2, 1.0e-30
    )
    real_adiabaticity = adiabaticity[real_mask]
    real_frequency_ratio = (
        np.abs(tracked) / hubbles[:, None]
    )[real_mask]
    positive_imaginary = np.max(
        np.maximum(tracked.imag, 0.0), axis=1
    )
    frozen_growth_exponent = float(
        np.trapezoid(positive_imaginary, times)
    )

    effective_substeps = max(
        substeps, int(math.ceil(0.32 / initial_ratio))
    )
    fine_transfer, transfer_records = propagate_magnus(
        generators,
        times,
        transfer_normalizations,
        substeps=effective_substeps,
        record=True,
    )
    coarse_substeps = max(1, effective_substeps // 2)
    coarse_transfer, _ = propagate_magnus(
        generators,
        times,
        transfer_normalizations,
        substeps=coarse_substeps,
        record=False,
    )
    fine_normalized = fine_transfer
    coarse_normalized = coarse_transfer
    convergence_error = float(
        np.linalg.norm(fine_normalized - coarse_normalized)
        / max(np.linalg.norm(fine_normalized), 1.0e-30)
    )
    fine_singular = np.linalg.svd(
        fine_normalized, compute_uv=False
    )
    maximum_transfer_gain = max(
        record["largest_normalized_singular_value"]
        for record in transfer_records
    )

    physical_q = comoving_momentum / scale_factors
    q_over_h = physical_q / hubbles
    force_frequency = (
        math.sqrt(gamma / (k_q * mstar2)) * physical_q**2
    )
    force_adiabaticity = 2 * hubbles / np.maximum(
        force_frequency, 1.0e-30
    )

    maximum_hamiltonian_defect = max(
        hamiltonian_generator_defect(generator)
        for generator in canonical_generators
    )
    maximum_canonical_equivalence_residual = max(
        canonical_equivalence_residuals
    )
    numerical_status = (
        "CONVERGED_GAUGE_INVARIANT_TRANSFER"
        if (
            convergence_error < 5.0e-4
            and maximum_hamiltonian_defect < 1.0e-10
            and maximum_canonical_equivalence_residual < 2.0e-3
        )
        else "HOLD_TRANSFER_NUMERICS"
    )
    frozen_status = (
        "COMPLEX_FROZEN_POLES_PRESENT"
        if np.any(complex_mask)
        else "ALL_TRACKED_FROZEN_POLES_REAL"
    )

    for index, record in enumerate(transfer_records):
        record.update(
            {
                "initial_q_over_H": initial_ratio,
                "q_over_H": float(q_over_h[index]),
                "complex_mode_count": float(
                    np.count_nonzero(complex_mask[index])
                ),
                "maximum_abs_imaginary_omega_over_H": float(
                    np.max(np.abs(tracked[index].imag))
                    / hubbles[index]
                ),
                "maximum_real_mode_adiabaticity": float(
                    np.max(
                        np.where(
                            real_mask[index],
                            adiabaticity[index],
                            np.nan,
                        )
                    )
                    if np.any(real_mask[index])
                    else math.nan
                ),
                "force_mode_adiabaticity": float(
                    force_adiabaticity[index]
                ),
            }
        )

    return {
        "initial_q_over_H": initial_ratio,
        "final_q_over_H": float(q_over_h[-1]),
        "comoving_momentum": float(comoving_momentum),
        "minimum_kinetic_eigenvalue": minimum_kinetic,
        "frozen_pole_status": frozen_status,
        "complex_time_fraction": float(
            np.mean(np.any(complex_mask, axis=1))
        ),
        "maximum_abs_imaginary_omega_over_H": float(
            np.max(np.abs(tracked.imag) / hubbles[:, None])
        ),
        "integrated_positive_imaginary_omega": (
            frozen_growth_exponent
        ),
        "maximum_real_mode_adiabaticity": (
            float(np.max(real_adiabaticity))
            if real_adiabaticity.size
            else math.nan
        ),
        "median_real_mode_adiabaticity": (
            float(np.median(real_adiabaticity))
            if real_adiabaticity.size
            else math.nan
        ),
        "minimum_real_abs_omega_over_H": (
            float(np.min(real_frequency_ratio))
            if real_frequency_ratio.size
            else math.nan
        ),
        "maximum_force_mode_adiabaticity": float(
            np.max(force_adiabaticity)
        ),
        "minimum_force_abs_omega_over_H": float(
            np.min(force_frequency / hubbles)
        ),
        "endpoint_normalized_singular_values": [
            float(value) for value in fine_singular
        ],
        "maximum_normalized_phase_space_gain": float(
            maximum_transfer_gain
        ),
        "endpoint_normalized_phase_space_gain": float(
            fine_singular[0]
        ),
        "endpoint_normalized_condition_number": float(
            fine_singular[0] / fine_singular[-1]
        ),
        "midpoint_magnus_substeps": effective_substeps,
        "coarse_to_fine_relative_error": convergence_error,
        "maximum_local_hamiltonian_generator_defect": maximum_hamiltonian_defect,
        "maximum_second_order_to_canonical_residual": (
            maximum_canonical_equivalence_residual
        ),
        "numerical_status": numerical_status,
    }, transfer_records


def write_csv(path: Path, rows: list[dict[str, float]]) -> None:
    require("nonempty transfer CSV", bool(rows))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    require("positive K_Q", args.K_Q > 0)
    require("positive gamma", args.gamma > 0)
    require("positive M_star_sq", args.M_star_sq > 0)
    require("at least two Magnus substeps", args.substeps >= 2)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    frw, rows = load_inputs(args.frw_summary, args.frw_trajectory)
    params = background_parameters(frw, args.alignment)
    params["zeta_align"] = args.alignment
    symbolic = symbolic_propagators()

    ratios = [0.01, 0.1, 1.0, 10.0, 100.0]
    mode_results: list[dict[str, object]] = []
    csv_rows: list[dict[str, float]] = []
    for ratio in ratios:
        result, records = evaluate_fixed_comoving_mode(
            symbolic,
            params,
            rows,
            ratio,
            args.K_Q,
            args.gamma,
            args.M_star_sq,
            args.substeps,
        )
        mode_results.append(result)
        csv_rows.extend(records)

    require(
        "positive kinetic inertia",
        min(
            result["minimum_kinetic_eigenvalue"]
            for result in mode_results
        )
        > 0,
    )
    all_transfers_converged = all(
        result["numerical_status"]
        == "CONVERGED_GAUGE_INVARIANT_TRANSFER"
        for result in mode_results
    )

    complex_modes_present = any(
        result["frozen_pole_status"]
        == "COMPLEX_FROZEN_POLES_PRESENT"
        for result in mode_results
    )
    high_q = mode_results[-1]
    high_q_controlled = (
        high_q["frozen_pole_status"]
        == "ALL_TRACKED_FROZEN_POLES_REAL"
        and high_q["maximum_real_mode_adiabaticity"] < 0.1
        and high_q["maximum_force_mode_adiabaticity"] < 0.1
    )
    if not all_transfers_converged:
        subgate_status = "HOLD_TIME_DEPENDENT_TRANSFER_NUMERICS"
    elif complex_modes_present:
        subgate_status = (
            "HOLD_TIME_DEPENDENT_INFRARED_TRANSFER_INTERPRETATION"
        )
    else:
        subgate_status = "PASS_FIXED_COMOVING_ADIABATIC_TRANSFER_AUDIT"

    summary = {
        "gate": "UVIR-003",
        "stage": "B_FIXED_COMOVING_ADIABATIC_TRANSFER",
        "calculation_status": (
            "HOLD" if subgate_status.startswith("HOLD") else "PASS"
        ),
        "subgate_status": subgate_status,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "parameter_scope": (
            "Representative dimensionless branch only. K_Q=gamma="
            "M_star_sq=1 is a diagnostic force-mode normalization, not a "
            "physical parameter selection."
        ),
        "method": {
            "momentum_rule": "fixed comoving k with q_phys=k/a",
            "physical_variables": ["Xi", "Q_rho", "Q_chi"],
            "canonical_state": [
                "p",
                "a^3(K p_dot + P p)",
            ],
            "observable_normalization": [
                "K^(1/2) p",
                "K^(1/2) p_dot/H",
            ],
            "transfer_integrator": (
                "piecewise-linear coefficient interpolation with "
                "midpoint Magnus matrix exponentials"
            ),
            "force_mode": (
                "factorized analytic omega_Pi=sqrt(gamma/(K_Q "
                "M_star_sq))*q_phys^2"
            ),
        },
        "mode_results": mode_results,
        "all_transfer_numerics_converged": all_transfers_converged,
        "high_q_controlled_adiabatic_subset": high_q_controlled,
        "scientific_boundary": (
            "This is a finite-duration transfer audit on one representative "
            "dimensionless background. A normalized transfer gain is not a "
            "Lyapunov exponent, an all-background stability proof, or an "
            "S-matrix amplitude. Complex frozen poles are not classified as "
            "physical instabilities unless their gauge-invariant transfer "
            "signature is separated from basis and background evolution."
        ),
        "next_required_calculation": [
            "classify transfer growth by tracked physical eigenmode rather than only a full phase-space singular value",
            "repeat any candidate growing mode under trajectory and parameter variations",
            "declare a controlled exchange domain only after that robustness audit",
            "then assemble exchange plus reduced contact inside the controlled domain",
        ],
    }

    json_path = (
        args.output_dir
        / "uvir003_propagator_adiabaticity_transfer_summary.json"
    )
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    write_csv(
        args.output_dir
        / "uvir003_propagator_adiabaticity_transfer.csv",
        csv_rows,
    )

    print("Fixed-comoving physical mode tracking: COMPLETE")
    print("Frozen-pole adiabaticity audit: COMPLETE")
    print("Gauge-invariant time-dependent transfer: COMPLETE")
    print(
        "Transfer Hamiltonian/equivalence/convergence checks: "
        + ("PASS" if all_transfers_converged else "HOLD")
    )
    print(
        "High-q controlled adiabatic subset: "
        + ("PASS" if high_q_controlled else "HOLD")
    )
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print(f"STATUS: {subgate_status}")


if __name__ == "__main__":
    main()
