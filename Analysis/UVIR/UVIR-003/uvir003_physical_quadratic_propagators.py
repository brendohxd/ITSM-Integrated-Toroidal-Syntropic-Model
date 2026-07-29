#!/usr/bin/env python3
"""UVIR-003 local-adiabatic physical-basis quadratic propagators.

Constructs the frozen-background inverse quadratic kernel for

    p = (Xi, Q_rho, Q_chi, Pi)

at finite physical momentum and the separate exact homogeneous physical
sector

    p_0 = (Q_rho, Q_chi, Pi).

The exact q=0 sector removes both Sigma=-D^2 beta and the homogeneous Xi
time-translation orbit before the remaining lapse constraint is eliminated.
It is therefore not obtained by substituting q=0 into the finite-q inverse.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

from uvir003_scalar_adm_finite_q import (
    background_parameters,
    evaluate_matrices,
    load_inputs,
    symbolic_reduction,
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
        "--alignment",
        type=float,
        default=1.0,
        help="Diagnostic-only alignment value used by the existing branch.",
    )
    parser.add_argument("--K-Q", type=float, default=1.0)
    parser.add_argument("--gamma", type=float, default=1.0)
    parser.add_argument("--M-star-sq", type=float, default=1.0)
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def require_zero(
    name: str,
    expression: sp.Expr | sp.MatrixBase,
) -> None:
    reduced = sp.simplify(expression)
    if isinstance(reduced, sp.MatrixBase):
        if all(sp.factor(value) == 0 for value in reduced):
            return
        raise AssertionError(f"{name} failed: {reduced}")
    if sp.factor(reduced) != 0:
        raise AssertionError(f"{name} failed: {reduced}")


def symbolic_propagators() -> dict[str, object]:
    reduction = symbolic_reduction()
    symbols = reduction["symbols"]
    expressions = reduction["expressions"]

    hubble = symbols["H"]
    rho = symbols["rho"]
    rho_dot = symbols["rho_dot"]
    chemical = symbols["mu"]
    q = symbols["q"]
    arguments = symbols["arguments"]

    mcos2 = arguments[1]
    kinetic = expressions["kinetic"]
    mixed = expressions["velocity_coordinate"]
    coordinate = expressions["coordinate_hessian"]
    potential = expressions["potential"]
    potential_prime = expressions["potential_prime"]
    potential_second = expressions["potential_second"]

    hubble_dot = -(
        rho_dot**2 + rho**2 * chemical**2
    ) / (2 * mcos2)
    rho_ddot = (
        -3 * hubble * rho_dot
        + rho * chemical**2
        - potential_prime
    )
    chemical_dot = chemical * (
        -3 * hubble - 2 * rho_dot / rho
    )

    # y=(R,delta_rho,vartheta)=T p with p=(Xi,Q_rho,Q_chi).
    transform = sp.Matrix(
        [
            [hubble / q, 0, 0],
            [rho_dot / q, 1, 0],
            [chemical / q, 0, 1 / rho],
        ]
    )
    transform_dot = sp.Matrix(
        [
            [(hubble_dot + hubble**2) / q, 0, 0],
            [(rho_ddot + hubble * rho_dot) / q, 0, 0],
            [
                (chemical_dot + hubble * chemical) / q,
                0,
                -rho_dot / rho**2,
            ],
        ]
    )

    physical_kinetic = sp.simplify(
        transform.T * kinetic * transform
    )
    physical_mixed = sp.simplify(
        transform.T * kinetic * transform_dot
        + transform.T * mixed * transform
    )
    physical_coordinate = sp.simplify(
        transform_dot.T * kinetic * transform_dot
        + transform_dot.T * mixed * transform
        + transform.T * mixed.T * transform_dot
        + transform.T * coordinate * transform
    )
    physical_gyroscopic = sp.simplify(
        physical_mixed - physical_mixed.T
    )

    require_zero(
        "finite-q physical kinetic symmetry",
        physical_kinetic - physical_kinetic.T,
    )
    require_zero(
        "finite-q physical coordinate symmetry",
        physical_coordinate - physical_coordinate.T,
    )
    require_zero(
        "finite-q physical gyroscopic antisymmetry",
        physical_gyroscopic + physical_gyroscopic.T,
    )

    physical_matrix_function = sp.lambdify(
        arguments,
        (
            physical_kinetic,
            physical_mixed,
            physical_coordinate,
        ),
        modules="numpy",
    )

    # Exact q=0 physical sector. R and Xi are removed as the homogeneous
    # time-translation gauge orbit; Sigma is absent. Only the homogeneous
    # lapse constraint remains, with C_NN=-2V.
    q_rho, q_chi = sp.symbols("Q_rho Q_chi", real=True)
    q_rho_dot, q_chi_dot = sp.symbols(
        "Q_rho_dot Q_chi_dot", real=True
    )
    phase = q_chi / rho
    phase_dot = (
        q_chi_dot / rho - rho_dot * q_chi / rho**2
    )
    lapse_source = (
        -(potential_prime + rho * chemical**2) * q_rho
        - rho_dot * q_rho_dot
        - rho**2 * chemical * phase_dot
    )
    homogeneous_unconstrained = (
        q_rho_dot**2 / 2
        + rho**2 * phase_dot**2 / 2
        + 2 * rho * chemical * q_rho * phase_dot
        + (
            chemical**2 - potential_second
        ) * q_rho**2 / 2
    )
    homogeneous_reduced = sp.expand(
        homogeneous_unconstrained
        + lapse_source**2 / (4 * potential)
    )
    homogeneous_fields = sp.Matrix([q_rho, q_chi])
    homogeneous_velocities = sp.Matrix(
        [q_rho_dot, q_chi_dot]
    )
    homogeneous_kinetic = sp.hessian(
        homogeneous_reduced, homogeneous_velocities
    )
    homogeneous_mixed = sp.Matrix(
        [
            [
                sp.diff(
                    homogeneous_reduced,
                    homogeneous_velocities[row],
                    homogeneous_fields[column],
                )
                for column in range(2)
            ]
            for row in range(2)
        ]
    )
    homogeneous_coordinate = sp.hessian(
        homogeneous_reduced, homogeneous_fields
    )
    homogeneous_gyroscopic = sp.simplify(
        homogeneous_mixed - homogeneous_mixed.T
    )
    require_zero(
        "q0 physical kinetic symmetry",
        homogeneous_kinetic - homogeneous_kinetic.T,
    )
    require_zero(
        "q0 physical coordinate symmetry",
        homogeneous_coordinate - homogeneous_coordinate.T,
    )
    require_zero(
        "q0 physical gyroscopic antisymmetry",
        homogeneous_gyroscopic + homogeneous_gyroscopic.T,
    )

    homogeneous_matrix_function = sp.lambdify(
        arguments,
        (
            homogeneous_kinetic,
            homogeneous_mixed,
            homogeneous_coordinate,
        ),
        modules="numpy",
    )

    omega, k_q, gamma, mstar2 = sp.symbols(
        "omega K_Q gamma M_star_sq",
        positive=True,
    )
    force_inverse = k_q * omega**2 - gamma * q**4 / mstar2

    return {
        "_reduction": reduction,
        "transform": transform,
        "transform_dot": transform_dot,
        "finite": {
            "kinetic": physical_kinetic,
            "mixed": physical_mixed,
            "coordinate": physical_coordinate,
            "gyroscopic": physical_gyroscopic,
            "matrix_function": physical_matrix_function,
        },
        "q0": {
            "reduced_lagrangian": homogeneous_reduced,
            "kinetic": homogeneous_kinetic,
            "mixed": homogeneous_mixed,
            "coordinate": homogeneous_coordinate,
            "gyroscopic": homogeneous_gyroscopic,
            "matrix_function": homogeneous_matrix_function,
            "projected_constraint_inverse": sp.Matrix(
                [[-1 / (2 * potential), 0], [0, 0]]
            ),
        },
        "force_inverse": force_inverse,
        "inverse_kernel_convention": (
            "D(omega,q)=omega^2 K+i omega(P-P^T)+C; "
            "G_F=i[D+i epsilon]^{-1}"
        ),
    }


def evaluate_physical_matrices(
    symbolic: dict[str, object],
    params: dict[str, float],
    state: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    function = symbolic["finite"]["matrix_function"]
    values = function(
        params["M_P_sq"],
        params["M_cos_sq"],
        params["D_123"],
        params["C_14"],
        state[0],
        state[1],
        state[2],
        state[3],
        state[4],
        params["zeta_align"],
        params["m_squared"],
        params["lambda4"],
        params["lambda6"],
        params["Lambda"],
    )
    return tuple(np.asarray(value, dtype=float) for value in values)


def evaluate_q0_matrices(
    symbolic: dict[str, object],
    params: dict[str, float],
    state: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    function = symbolic["q0"]["matrix_function"]
    values = function(
        params["M_P_sq"],
        params["M_cos_sq"],
        params["D_123"],
        params["C_14"],
        state[0],
        state[1],
        state[2],
        state[3],
        0.0,
        params["zeta_align"],
        params["m_squared"],
        params["lambda4"],
        params["lambda6"],
        params["Lambda"],
    )
    return tuple(np.asarray(value, dtype=float) for value in values)


def add_force_block(
    matrices: tuple[np.ndarray, np.ndarray, np.ndarray],
    q: float,
    k_q: float,
    gamma: float,
    mstar2: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    kinetic, mixed, coordinate = matrices
    size = kinetic.shape[0] + 1
    full_kinetic = np.zeros((size, size), dtype=float)
    full_mixed = np.zeros((size, size), dtype=float)
    full_coordinate = np.zeros((size, size), dtype=float)
    full_kinetic[:-1, :-1] = kinetic
    full_mixed[:-1, :-1] = mixed
    full_coordinate[:-1, :-1] = coordinate
    full_kinetic[-1, -1] = k_q
    full_coordinate[-1, -1] = -gamma * q**4 / mstar2
    return full_kinetic, full_mixed, full_coordinate


def inverse_kernel(
    omega: complex,
    kinetic: np.ndarray,
    mixed: np.ndarray,
    coordinate: np.ndarray,
) -> np.ndarray:
    gyroscopic = mixed - mixed.T
    return (
        omega**2 * kinetic
        + 1j * omega * gyroscopic
        + coordinate
    )


def quadratic_poles(
    kinetic: np.ndarray,
    mixed: np.ndarray,
    coordinate: np.ndarray,
) -> np.ndarray:
    gyroscopic = mixed - mixed.T
    dimension = kinetic.shape[0]
    generator = np.block(
        [
            [
                np.zeros((dimension, dimension), dtype=complex),
                np.eye(dimension, dtype=complex),
            ],
            [
                -np.linalg.solve(kinetic, coordinate),
                -np.linalg.solve(kinetic, 1j * gyroscopic),
            ],
        ]
    )
    return np.linalg.eigvals(generator)


def pole_diagnostics(
    poles: np.ndarray,
    kinetic: np.ndarray,
    mixed: np.ndarray,
    coordinate: np.ndarray,
    scale: float,
) -> tuple[list[dict[str, float]], dict[str, float]]:
    gyroscopic = mixed - mixed.T
    pole_scale = max(float(np.max(np.abs(poles))), scale, 1.0e-12)
    reality_tolerance = 2.0e-7 * pole_scale
    real_poles = sorted(
        float(value.real)
        for value in poles
        if abs(value.imag) <= reality_tolerance
    )
    positive = [
        value
        for value in real_poles
        if value > 1.0e-8 * pole_scale
    ]
    zero_count = sum(
        abs(value) <= 1.0e-8 * pole_scale for value in real_poles
    )

    records: list[dict[str, float]] = []
    minimum_positive_residue = math.inf
    maximum_pole_residual = 0.0
    for mode, omega in enumerate(positive, start=1):
        kernel = inverse_kernel(
            omega, kinetic, mixed, coordinate
        )
        eigenvalues, eigenvectors = np.linalg.eigh(
            (kernel + kernel.conj().T) / 2
        )
        index = int(np.argmin(np.abs(eigenvalues)))
        vector = eigenvectors[:, index]
        derivative = (
            2 * omega * kinetic + 1j * gyroscopic
        )
        residue_denominator = float(
            np.real(vector.conj().T @ derivative @ vector)
        )
        residual = float(
            np.linalg.norm(kernel @ vector)
            / max(
                np.linalg.norm(kernel) * np.linalg.norm(vector),
                1.0e-30,
            )
        )
        minimum_positive_residue = min(
            minimum_positive_residue, residue_denominator
        )
        maximum_pole_residual = max(maximum_pole_residual, residual)
        records.append(
            {
                "mode": float(mode),
                "omega": omega,
                "omega_over_scale": omega / scale,
                "residue_denominator": residue_denominator,
                "relative_kernel_residual": residual,
            }
        )

    ordered = np.sort_complex(poles)
    symmetry_error = max(
        min(abs(value + other) for other in poles)
        for value in poles
    ) / pole_scale
    return records, {
        "pole_count": float(len(poles)),
        "real_pole_count": float(len(real_poles)),
        "positive_pole_count": float(len(positive)),
        "zero_pole_count": float(zero_count),
        "maximum_abs_imaginary_pole_over_scale": float(
            np.max(np.abs(poles.imag)) / pole_scale
        ),
        "plus_minus_pairing_relative_error": float(symmetry_error),
        "minimum_positive_frequency_residue_denominator": (
            minimum_positive_residue
            if records
            else math.nan
        ),
        "maximum_pole_kernel_relative_residual": (
            maximum_pole_residual
        ),
        "ordered_poles_real": [
            float(value.real) for value in ordered
        ],
        "ordered_poles_imag": [
            float(value.imag) for value in ordered
        ],
    }


def scan_propagators(
    symbolic: dict[str, object],
    frw: dict[str, object],
    rows: list[dict[str, float]],
    alignment: float,
    k_q: float,
    gamma: float,
    mstar2: float,
) -> tuple[dict[str, object], list[dict[str, float]]]:
    params = background_parameters(frw, alignment)
    params["zeta_align"] = alignment
    matrix_function = symbolic["_reduction"]["matrix_function"]

    snapshot_indices = sorted(
        {
            0,
            len(rows) // 4,
            len(rows) // 2,
            3 * len(rows) // 4,
            len(rows) - 1,
        }
    )
    ratios = [0.01, 0.1, 1.0, 10.0, 100.0]
    csv_rows: list[dict[str, float]] = []
    finite_samples: list[dict[str, object]] = []
    q0_samples: list[dict[str, object]] = []

    global_minimum_kinetic = math.inf
    global_minimum_residue = math.inf
    global_maximum_pole_imaginary = 0.0
    global_maximum_pairing_error = 0.0
    global_maximum_pole_residual = 0.0
    global_maximum_inverse_residual = 0.0
    global_minimum_constraint_singular = math.inf

    for index in snapshot_indices:
        row = rows[index]
        for ratio in ratios:
            state = np.array(
                [
                    row["H"],
                    row["rho"],
                    row["rho_dot"],
                    row["mu"],
                    ratio * row["H"],
                ],
                dtype=float,
            )
            physical = evaluate_physical_matrices(
                symbolic, params, state
            )
            matrices = add_force_block(
                physical, state[4], k_q, gamma, mstar2
            )
            kinetic, mixed, coordinate = matrices
            kinetic_eigenvalues = np.linalg.eigvalsh(
                (kinetic + kinetic.T) / 2
            )
            minimum_kinetic = float(np.min(kinetic_eigenvalues))
            global_minimum_kinetic = min(
                global_minimum_kinetic, minimum_kinetic
            )

            _, _, _, constraint = evaluate_matrices(
                matrix_function, params, state
            )
            constraint_singular = float(
                np.min(np.linalg.svd(constraint, compute_uv=False))
            )
            global_minimum_constraint_singular = min(
                global_minimum_constraint_singular,
                constraint_singular,
            )

            poles = quadratic_poles(*matrices)
            records, diagnostics = pole_diagnostics(
                poles, *matrices, scale=row["H"]
            )
            global_maximum_pole_imaginary = max(
                global_maximum_pole_imaginary,
                diagnostics[
                    "maximum_abs_imaginary_pole_over_scale"
                ],
            )
            global_maximum_pairing_error = max(
                global_maximum_pairing_error,
                diagnostics[
                    "plus_minus_pairing_relative_error"
                ],
            )
            global_maximum_pole_residual = max(
                global_maximum_pole_residual,
                diagnostics[
                    "maximum_pole_kernel_relative_residual"
                ],
            )
            if records:
                global_minimum_residue = min(
                    global_minimum_residue,
                    diagnostics[
                        "minimum_positive_frequency_residue_denominator"
                    ],
                )

            offshell_omega = 1j * (1.0 + state[4])
            kernel = inverse_kernel(offshell_omega, *matrices)
            propagator = 1j * np.linalg.inv(kernel)
            inverse_residual = float(
                np.linalg.norm(
                    kernel @ (propagator / 1j)
                    - np.eye(kernel.shape[0])
                )
            )
            global_maximum_inverse_residual = max(
                global_maximum_inverse_residual, inverse_residual
            )

            finite_samples.append(
                {
                    "t": row["t"],
                    "q_over_H": ratio,
                    "minimum_kinetic_eigenvalue": minimum_kinetic,
                    "constraint_minimum_singular_value": (
                        constraint_singular
                    ),
                    "offshell_inverse_residual": inverse_residual,
                    "pole_diagnostics": diagnostics,
                }
            )
            for record in records:
                csv_rows.append(
                    {
                        "sector": 1.0,
                        "t": row["t"],
                        "q_over_H": ratio,
                        **record,
                    }
                )

        q0_state = np.array(
            [
                row["H"],
                row["rho"],
                row["rho_dot"],
                row["mu"],
                0.0,
            ],
            dtype=float,
        )
        q0_physical = evaluate_q0_matrices(
            symbolic, params, q0_state
        )
        q0_matrices = add_force_block(
            q0_physical, 0.0, k_q, gamma, mstar2
        )
        q0_kinetic = np.linalg.eigvalsh(
            (q0_matrices[0] + q0_matrices[0].T) / 2
        )
        q0_poles = quadratic_poles(*q0_matrices)
        q0_records, q0_diagnostics = pole_diagnostics(
            q0_poles, *q0_matrices, scale=row["H"]
        )
        q0_samples.append(
            {
                "t": row["t"],
                "variables": ["Q_rho", "Q_chi", "Pi"],
                "minimum_kinetic_eigenvalue": float(
                    np.min(q0_kinetic)
                ),
                "pole_diagnostics": q0_diagnostics,
            }
        )
        for record in q0_records:
            csv_rows.append(
                {
                    "sector": 0.0,
                    "t": row["t"],
                    "q_over_H": 0.0,
                    **record,
                }
            )

    require(
        "finite-q physical kinetic positivity",
        global_minimum_kinetic > 0,
    )
    require(
        "finite-q constraint nonsingularity",
        global_minimum_constraint_singular > 1.0e-8,
    )
    require(
        "finite-q propagator inversion",
        global_maximum_inverse_residual < 1.0e-9,
    )
    require(
        "finite-q pole pairing",
        global_maximum_pairing_error < 1.0e-6,
    )
    require(
        "finite-q pole residuals",
        global_maximum_pole_residual < 1.0e-6,
    )
    require(
        "exact q0 physical kinetic positivity",
        min(
            sample["minimum_kinetic_eigenvalue"]
            for sample in q0_samples
        )
        > 0,
    )

    all_finite_poles_real = (
        global_maximum_pole_imaginary < 1.0e-6
    )
    all_positive_residues = (
        global_minimum_residue > 0
        if math.isfinite(global_minimum_residue)
        else False
    )
    pole_status = (
        "REAL_SIMPLE_POLES_WITH_POSITIVE_FREQUENCY_RESIDUES"
        if all_finite_poles_real and all_positive_residues
        else "HOLD_LOCAL_ADIABATIC_POLE_OR_RESIDUE_AUDIT"
    )

    return {
        "parameter_scope": (
            "Dimensionless representative branch only. K_Q=gamma="
            "M_star_sq=1 is a diagnostic normalization for the factorized "
            "Pi block and is not a physical parameter selection."
        ),
        "finite_q_domain": {
            "snapshot_count": len(snapshot_indices),
            "q_over_H_values": ratios,
            "sample_count": len(finite_samples),
            "variables": ["Xi", "Q_rho", "Q_chi", "Pi"],
        },
        "finite_q_checks": {
            "minimum_kinetic_eigenvalue": global_minimum_kinetic,
            "minimum_constraint_singular_value": (
                global_minimum_constraint_singular
            ),
            "maximum_offshell_inverse_residual": (
                global_maximum_inverse_residual
            ),
            "maximum_plus_minus_pairing_relative_error": (
                global_maximum_pairing_error
            ),
            "maximum_pole_kernel_relative_residual": (
                global_maximum_pole_residual
            ),
            "maximum_abs_imaginary_pole_over_local_pole_scale": (
                global_maximum_pole_imaginary
            ),
            "minimum_positive_frequency_residue_denominator": (
                global_minimum_residue
            ),
            "pole_and_residue_status": pole_status,
        },
        "finite_q_samples": finite_samples,
        "exact_q0": {
            "rule": (
                "Remove Sigma and Xi before inversion; retain the lapse "
                "constraint and (Q_rho,Q_chi,Pi)."
            ),
            "projected_constraint_inverse": (
                "diag(-1/(2V),0), V!=0"
            ),
            "samples": q0_samples,
        },
    }, csv_rows


def serializable_symbolic(
    symbolic: dict[str, object],
) -> dict[str, object]:
    return {
        "variables_finite_q": ["Xi", "Q_rho", "Q_chi", "Pi"],
        "variables_exact_q0": ["Q_rho", "Q_chi", "Pi"],
        "transform": str(symbolic["transform"]),
        "transform_dot": str(symbolic["transform_dot"]),
        "finite_q_kinetic": str(symbolic["finite"]["kinetic"]),
        "finite_q_gyroscopic": str(
            symbolic["finite"]["gyroscopic"]
        ),
        "finite_q_coordinate": str(
            symbolic["finite"]["coordinate"]
        ),
        "exact_q0_reduced_lagrangian": str(
            symbolic["q0"]["reduced_lagrangian"]
        ),
        "exact_q0_kinetic": str(symbolic["q0"]["kinetic"]),
        "exact_q0_gyroscopic": str(
            symbolic["q0"]["gyroscopic"]
        ),
        "exact_q0_coordinate": str(
            symbolic["q0"]["coordinate"]
        ),
        "exact_q0_projected_constraint_inverse": str(
            symbolic["q0"]["projected_constraint_inverse"]
        ),
        "force_inverse": str(symbolic["force_inverse"]),
        "inverse_kernel_convention": (
            symbolic["inverse_kernel_convention"]
        ),
        "determinant_factorization": (
            "det D_4=det D_(Xi,Q_rho,Q_chi)"
            "*(K_Q*omega^2-gamma*q_phys^4/M_star_sq)"
        ),
    }


def write_csv(
    path: Path,
    rows: list[dict[str, float]],
) -> None:
    fieldnames = [
        "sector",
        "t",
        "q_over_H",
        "mode",
        "omega",
        "omega_over_scale",
        "residue_denominator",
        "relative_kernel_residual",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run() -> int:
    args = parse_args()
    require("positive K_Q", args.K_Q > 0)
    require("positive gamma", args.gamma > 0)
    require("positive M_star_sq", args.M_star_sq > 0)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    symbolic = symbolic_propagators()
    frw, rows = load_inputs(
        args.frw_summary, args.frw_trajectory
    )
    representative, csv_rows = scan_propagators(
        symbolic,
        frw,
        rows,
        args.alignment,
        args.K_Q,
        args.gamma,
        args.M_star_sq,
    )
    pole_status = representative["finite_q_checks"][
        "pole_and_residue_status"
    ]
    subgate_status = (
        "PASS_LOCAL_ADIABATIC_PHYSICAL_QUADRATIC_PROPAGATORS"
        if pole_status
        == "REAL_SIMPLE_POLES_WITH_POSITIVE_FREQUENCY_RESIDUES"
        else "HOLD_LOCAL_ADIABATIC_PHYSICAL_QUADRATIC_PROPAGATORS"
    )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_PHYSICAL_QUADRATIC_PROPAGATORS",
        "calculation_status": (
            "PASS" if subgate_status.startswith("PASS") else "HOLD"
        ),
        "subgate_status": subgate_status,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "symbolic_result": serializable_symbolic(symbolic),
        "representative_branch": representative,
        "scientific_boundary": (
            "The local adiabatic inverse quadratic kernels and propagators "
            "are constructed in the finite-q physical basis and in the "
            "separate exact q=0 projected sector. This is a representative "
            "dimensionless pole/residue audit, not a physical parameter "
            "selection, scattering amplitude, unitarity bound, "
            "strong-coupling scale or cutoff."
        ),
        "next_required_calculation": [
            "separate the frozen kernel into leading WKB and first adiabatic corrections",
            "calculate mode-by-mode adiabaticity on fixed comoving momenta",
            "evolve the time-dependent gauge-invariant quadratic initial-value system",
            "decide whether the complex low-q poles persist in transfer matrices",
            "assemble exchange amplitudes only inside the resulting controlled domain",
        ],
    }

    json_path = (
        args.output_dir
        / "uvir003_physical_quadratic_propagators_summary.json"
    )
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    csv_path = (
        args.output_dir
        / "uvir003_physical_quadratic_propagators_poles.csv"
    )
    write_csv(csv_path, csv_rows)

    checks = representative["finite_q_checks"]
    print("Finite-q physical quadratic kernel: CONSTRUCTED")
    print("Exact q0 projected quadratic kernel: CONSTRUCTED")
    print("Propagator convention: VERIFIED")
    print(
        "Representative finite-q kinetic inertia: "
        "4_POSITIVE_0_NEGATIVE"
    )
    print(
        "Representative pole/residue audit: "
        f"{checks['pole_and_residue_status']}"
    )
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print(f"STATUS: {subgate_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
