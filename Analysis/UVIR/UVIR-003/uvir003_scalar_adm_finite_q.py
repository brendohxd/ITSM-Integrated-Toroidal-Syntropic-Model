#!/usr/bin/env python3
"""UVIR-003 Stage B: time-dependent finite-q scalar ADM reduction.

Expands the declared two-derivative Einstein-aether plus canonical condensate
action to quadratic order about the verified evolving flat-FRW branch in
aether-unitary scalar gauge.  The lapse and scalar momentum constraints are
eliminated at every nonzero physical wavenumber.  The reduced kinetic matrix
is then scanned from the subhorizon regime toward q_phys/H -> 0.

The force scalar remains a separately factorized z=2 block because its
declared background is constant and its cubic spatial operator has no
quadratic contribution at zero background gradient.

This is a quadratic finite-q and low-q rank audit.  It is not a cubic
strong-coupling calculation, a matter-coupled perturbation analysis, or a
physical parameter fit.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Callable

import numpy as np
import sympy as sp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=base / "outputs",
        help="Directory for the JSON summary and compact scan CSV.",
    )
    parser.add_argument(
        "--frw-summary",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_summary.json",
        help="Verified representative FRW summary.",
    )
    parser.add_argument(
        "--frw-trajectory",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_trajectory.csv",
        help="Verified representative FRW trajectory.",
    )
    parser.add_argument(
        "--alignment",
        type=float,
        default=1.0,
        help=(
            "Positive diagnostic-only zeta_align value used in the local "
            "equation-generator examples. Kinetic and constraint conclusions "
            "do not depend on this choice."
        ),
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def require_zero(name: str, expression: sp.Expr | sp.MatrixBase) -> None:
    result = sp.simplify(expression)
    if isinstance(result, sp.MatrixBase):
        if all(sp.factor(value) == 0 for value in result):
            return
        raise AssertionError(f"{name} failed: {result}")
    result = sp.factor(result)
    if result != 0:
        raise AssertionError(f"{name} failed: {result}")


def symbolic_reduction() -> dict[str, object]:
    mp2, mu2 = sp.symbols("M_P_sq M_U_sq", positive=True)
    mcos2 = sp.symbols("M_cos_sq", positive=True)
    c13, c2, c123, c14 = sp.symbols(
        "c13 c2 c123 c14", real=True
    )
    d123 = sp.symbols("D_123", positive=True)
    cacc = sp.symbols("C_14", positive=True)
    hubble = sp.symbols("H", real=True)
    rho = sp.symbols("rho", positive=True)
    rho_dot, chemical = sp.symbols("rho_dot mu", real=True)
    q = sp.symbols("q_phys", positive=True)
    alignment = sp.symbols("zeta_align", nonnegative=True)
    mass_sq, quartic, sextic, cutoff = sp.symbols(
        "m_squared lambda4 lambda6 Lambda", positive=True
    )

    curvature, amplitude, phase = sp.symbols(
        "R delta_rho vartheta", real=True
    )
    curvature_dot, amplitude_dot, phase_dot = sp.symbols(
        "R_dot delta_rho_dot vartheta_dot", real=True
    )
    lapse, shear = sp.symbols("delta_N Sigma", real=True)

    potential = (
        mass_sq * rho**2 / 2
        + quartic * rho**4 / 8
        + sextic * rho**6 / (24 * cutoff**2)
    )
    potential_prime = sp.diff(potential, rho)
    potential_second = sp.diff(potential_prime, rho)
    enthalpy = rho_dot**2 + rho**2 * chemical**2
    energy = enthalpy / 2 + potential

    # Sigma=q_phys^2*beta is the scalar shear variable that remains finite for
    # every q_phys>0 after the momentum constraint is solved.  At exactly
    # q_phys=0 it is not an independent homogeneous perturbation.
    constraint_matrix = sp.Matrix(
        [
            [cacc * q**2 - 2 * potential, 2 * mcos2 * hubble],
            [2 * mcos2 * hubble, -d123],
        ]
    )
    constraint_source = sp.Matrix(
        [
            6 * mcos2 * hubble * curvature_dot
            + 2 * mp2 * q**2 * curvature
            - (potential_prime + rho * chemical**2) * amplitude
            - rho_dot * amplitude_dot
            - rho**2 * chemical * phase_dot,
            -2 * mcos2 * curvature_dot
            - rho_dot * amplitude
            - rho**2 * chemical * phase,
        ]
    )

    unconstrained = (
        -3 * mcos2 * curvature_dot**2
        - 18 * mcos2 * hubble * curvature * curvature_dot
        + (mp2 * q**2 - 9 * potential) * curvature**2
        + 3
        * (rho * chemical**2 - potential_prime)
        * curvature
        * amplitude
        + 3 * rho_dot * curvature * amplitude_dot
        + 3 * rho**2 * chemical * curvature * phase_dot
        + 2 * rho * chemical * amplitude * phase_dot
        + amplitude_dot**2 / 2
        + rho**2 * phase_dot**2 / 2
        + (chemical**2 - potential_second - q**2)
        * amplitude**2
        / 2
        - rho**2
        * (1 + alignment * rho**2)
        * q**2
        * phase**2
        / 2
    )
    constraints = sp.Matrix([lapse, shear])
    full_lagrangian = sp.expand(
        unconstrained
        + (constraints.T * constraint_source)[0]
        + (constraints.T * constraint_matrix * constraints)[0] / 2
    )
    # Independent reconstruction from the unsimplified quadratic ADM mode
    # expansion. The first line is the Einstein-Hilbert plus aether
    # extrinsic-curvature block; the next two terms are the spatial-curvature
    # and acceleration blocks; the remainder is the canonical condensate and
    # alignment expansion. The on-shell Friedmann identity must reduce it to
    # the compact constraint form declared above.
    raw_lagrangian = sp.expand(
        -3 * mcos2 * curvature_dot**2
        - 2 * mcos2 * shear * curvature_dot
        - d123 * shear**2 / 2
        + 6 * mcos2 * hubble * lapse * curvature_dot
        + 2 * mcos2 * hubble * lapse * shear
        - 3 * mcos2 * hubble**2 * lapse**2
        + 9 * mcos2 * hubble**2 * lapse * curvature
        - 18 * mcos2 * hubble * curvature * curvature_dot
        - 27 * mcos2 * hubble**2 * curvature**2 / 2
        + mp2 * q**2 * curvature**2
        + 2 * mp2 * q**2 * lapse * curvature
        + cacc * q**2 * lapse**2 / 2
        + enthalpy * lapse**2 / 2
        + lapse
        * (
            -3 * potential * curvature
            - 3 * enthalpy * curvature / 2
            - potential_prime * amplitude
            - rho * chemical**2 * amplitude
            - rho_dot * amplitude_dot
            - rho**2 * chemical * phase_dot
        )
        + curvature**2
        * (-9 * potential / 2 + 9 * enthalpy / 4)
        + curvature
        * (-3 * potential_prime + 3 * rho * chemical**2)
        * amplitude
        + shear
        * (-rho_dot * amplitude - rho**2 * chemical * phase)
        + 3 * rho_dot * curvature * amplitude_dot
        + 3 * rho**2 * chemical * curvature * phase_dot
        + 2 * rho * chemical * amplitude * phase_dot
        + amplitude_dot**2 / 2
        + rho**2 * phase_dot**2 / 2
        + (chemical**2 - potential_second - q**2)
        * amplitude**2
        / 2
        - rho**2
        * (1 + alignment * rho**2)
        * q**2
        * phase**2
        / 2
    )
    require_zero(
        "independent quadratic ADM reconstruction",
        (raw_lagrangian - full_lagrangian).subs(
            {hubble**2: energy / (3 * mcos2)}
        ),
    )

    constraint_solution = sp.simplify(
        -constraint_matrix.inv() * constraint_source
    )
    reduced_lagrangian = sp.factor(
        unconstrained
        - (
            constraint_source.T
            * constraint_matrix.inv()
            * constraint_source
        )[0]
        / 2
    )

    coordinates = sp.Matrix([curvature, amplitude, phase])
    velocities = sp.Matrix(
        [curvature_dot, amplitude_dot, phase_dot]
    )
    kinetic = sp.hessian(reduced_lagrangian, velocities)
    velocity_coordinate = sp.Matrix(
        [
            [
                sp.diff(
                    reduced_lagrangian,
                    velocities[row],
                    coordinates[column],
                )
                for column in range(3)
            ]
            for row in range(3)
        ]
    )
    coordinate_hessian = sp.hessian(
        reduced_lagrangian, coordinates
    )

    # Verify that direct variation and Schur-complement elimination agree.
    direct_solution = sp.solve(
        [
            sp.diff(full_lagrangian, lapse),
            sp.diff(full_lagrangian, shear),
        ],
        [lapse, shear],
        dict=True,
        simplify=False,
    )[0]
    require_zero(
        "lapse Schur solution",
        direct_solution[lapse] - constraint_solution[0],
    )
    require_zero(
        "momentum Schur solution",
        direct_solution[shear] - constraint_solution[1],
    )

    friedmann_substitution = {
        hubble**2: energy / (3 * mcos2)
    }
    kinetic_determinant = sp.factor(kinetic.det())
    expected_kinetic_determinant = sp.factor(
        2
        * mcos2
        * rho**2
        * (2 * mcos2 - 3 * d123)
        * cacc
        * q**2
        / (
            cacc * d123 * q**2
            - 2 * d123 * potential
            + 4 * mcos2**2 * hubble**2
        )
    )
    require_zero(
        "on-shell reduced kinetic determinant",
        (kinetic_determinant - expected_kinetic_determinant).subs(
            friedmann_substitution
        ),
    )
    require_zero(
        "strict homogeneous kinetic determinant",
        expected_kinetic_determinant.subs(q, 0),
    )

    mcos_definition = sp.simplify(
        mp2 + mu2 * (c13 + 3 * c2) / 2
    )
    d123_definition = sp.simplify(mu2 * c123)
    cacc_definition = sp.simplify(mu2 * c14)
    c123_identity = {c123: c13 + c2}
    require_zero(
        "aether coefficient identity",
        (
            2 * mcos_definition
            - 3 * d123_definition
            - 2 * (mp2 - mu2 * c13)
        ).subs(c123_identity),
    )

    high_q_curvature_hessian = sp.factor(
        sp.limit(
            kinetic[0, 0],
            q,
            sp.oo,
        )
    )
    expected_high_q_curvature_hessian = sp.factor(
        2
        * (
            2
            * mcos2
            * (2 * mcos2 - 3 * d123)
            / (2 * d123)
        )
    )
    require_zero(
        "principal curvature Hessian",
        high_q_curvature_hessian
        - expected_high_q_curvature_hessian,
    )
    require_zero(
        "principal amplitude Hessian",
        sp.limit(kinetic[1, 1], q, sp.oo) - 1,
    )
    require_zero(
        "principal phase Hessian",
        sp.limit(kinetic[2, 2], q, sp.oo) - rho**2,
    )

    matrix_arguments = (
        mp2,
        mcos2,
        d123,
        cacc,
        hubble,
        rho,
        rho_dot,
        chemical,
        q,
        alignment,
        mass_sq,
        quartic,
        sextic,
        cutoff,
    )
    matrix_function = sp.lambdify(
        matrix_arguments,
        (
            kinetic,
            velocity_coordinate,
            coordinate_hessian,
            constraint_matrix,
        ),
        modules="numpy",
    )

    return {
        "symbols": {
            "arguments": matrix_arguments,
            "H": hubble,
            "rho": rho,
            "rho_dot": rho_dot,
            "mu": chemical,
            "q": q,
        },
        "expressions": {
            "potential": potential,
            "potential_prime": potential_prime,
            "potential_second": potential_second,
            "constraint_matrix": constraint_matrix,
            "constraint_source": constraint_source,
            "constraint_solution": constraint_solution,
            "reduced_lagrangian": reduced_lagrangian,
            "kinetic": kinetic,
            "velocity_coordinate": velocity_coordinate,
            "coordinate_hessian": coordinate_hessian,
            "kinetic_determinant_on_shell": (
                expected_kinetic_determinant
            ),
            "expected_kinetic_determinant": (
                expected_kinetic_determinant
            ),
            "high_q_curvature_hessian": (
                high_q_curvature_hessian
            ),
        },
        "matrix_function": matrix_function,
    }


def load_inputs(
    summary_path: Path,
    trajectory_path: Path,
) -> tuple[dict[str, object], list[dict[str, float]]]:
    with summary_path.open(encoding="utf-8") as handle:
        frw = json.load(handle)
    rows: list[dict[str, float]] = []
    with trajectory_path.open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            rows.append({key: float(value) for key, value in raw.items()})
    require("verified FRW status", frw["calculation_status"] == "PASS")
    require("nonempty FRW trajectory", bool(rows))
    return frw, rows


def background_parameters(
    frw: dict[str, object],
    alignment: float,
) -> dict[str, float]:
    branch = frw["representative_branch"]
    params = branch["parameters"]
    derived = branch["derived_parameters"]
    result = {
        "M_P_sq": float(params["M_P"]) ** 2,
        "M_cos_sq": float(derived["M_cos_squared"]),
        "D_123": float(params["M_U"]) ** 2
        * float(derived["c123"]),
        "C_14": float(params["M_U"]) ** 2
        * float(derived["c14"]),
        "zeta_align": alignment,
        "m_squared": float(params["m_squared"]),
        "lambda4": float(params["lambda4"]),
        "lambda6": float(params["lambda6"]),
        "Lambda": float(params["Lambda"]),
    }
    require("positive diagnostic alignment", alignment > 0)
    require("positive D_123", result["D_123"] > 0)
    require("positive C_14", result["C_14"] > 0)
    require(
        "positive high-q curvature domain",
        2 * result["M_cos_sq"] - 3 * result["D_123"] > 0,
    )
    return result


def potential_functions(
    params: dict[str, float],
) -> tuple[Callable[[float], float], Callable[[float], float]]:
    def potential(rho: float) -> float:
        return (
            params["m_squared"] * rho**2 / 2
            + params["lambda4"] * rho**4 / 8
            + params["lambda6"]
            * rho**6
            / (24 * params["Lambda"] ** 2)
        )

    def potential_prime(rho: float) -> float:
        return (
            params["m_squared"] * rho
            + params["lambda4"] * rho**3 / 2
            + params["lambda6"]
            * rho**5
            / (4 * params["Lambda"] ** 2)
        )

    return potential, potential_prime


def evaluate_matrices(
    matrix_function: Callable[..., object],
    params: dict[str, float],
    state: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    hubble, rho, rho_dot, chemical, q = state
    values = matrix_function(
        params["M_P_sq"],
        params["M_cos_sq"],
        params["D_123"],
        params["C_14"],
        hubble,
        rho,
        rho_dot,
        chemical,
        q,
        params["zeta_align"],
        params["m_squared"],
        params["lambda4"],
        params["lambda6"],
        params["Lambda"],
    )
    return tuple(np.asarray(value, dtype=float) for value in values)


def background_flow(
    params: dict[str, float],
    state: np.ndarray,
    potential_prime: Callable[[float], float],
) -> np.ndarray:
    hubble, rho, rho_dot, chemical, q = state
    enthalpy = rho_dot**2 + rho**2 * chemical**2
    return np.array(
        [
            -enthalpy / (2 * params["M_cos_sq"]),
            rho_dot,
            -3 * hubble * rho_dot
            + rho * chemical**2
            - potential_prime(rho),
            chemical * (-3 * hubble - 2 * rho_dot / rho),
            -hubble * q,
        ],
        dtype=float,
    )


def directional_time_derivatives(
    matrix_function: Callable[..., object],
    params: dict[str, float],
    state: np.ndarray,
    potential_prime: Callable[[float], float],
    step_scale: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    flow = background_flow(params, state, potential_prime)
    rate = max(
        1.0,
        abs(state[0]),
        abs(state[2] / state[1]),
        abs(state[3]),
    )
    delta_t = step_scale * 1.0e-6 / rate
    plus = state + delta_t * flow
    minus = state - delta_t * flow
    require("directional derivative positive rho", min(plus[1], minus[1]) > 0)
    require("directional derivative positive q", min(plus[4], minus[4]) > 0)
    k_plus, p_plus, _, _ = evaluate_matrices(
        matrix_function, params, plus
    )
    k_minus, p_minus, _, _ = evaluate_matrices(
        matrix_function, params, minus
    )
    return (
        (k_plus - k_minus) / (2 * delta_t),
        (p_plus - p_minus) / (2 * delta_t),
    )


def local_equation_generator(
    matrix_function: Callable[..., object],
    params: dict[str, float],
    state: np.ndarray,
    potential_prime: Callable[[float], float],
) -> tuple[np.ndarray, float]:
    kinetic, mixed, coordinate, _ = evaluate_matrices(
        matrix_function, params, state
    )
    kinetic_dot, mixed_dot = directional_time_derivatives(
        matrix_function, params, state, potential_prime
    )
    damping = kinetic_dot + mixed - mixed.T
    stiffness = mixed_dot - coordinate
    generator = np.block(
        [
            [np.zeros((3, 3)), np.eye(3)],
            [
                -np.linalg.solve(kinetic, stiffness),
                -np.linalg.solve(kinetic, damping),
            ],
        ]
    )

    kinetic_dot_half, mixed_dot_half = (
        directional_time_derivatives(
            matrix_function,
            params,
            state,
            potential_prime,
            step_scale=0.5,
        )
    )
    scale = max(
        np.linalg.norm(kinetic_dot_half),
        np.linalg.norm(mixed_dot_half),
        1.0e-30,
    )
    derivative_error = max(
        np.linalg.norm(kinetic_dot - kinetic_dot_half),
        np.linalg.norm(mixed_dot - mixed_dot_half),
    ) / scale
    return generator, float(derivative_error)


def representative_scan(
    symbolic: dict[str, object],
    frw: dict[str, object],
    rows: list[dict[str, float]],
    alignment: float,
) -> tuple[dict[str, object], list[dict[str, float]]]:
    params = background_parameters(frw, alignment)
    potential, potential_prime = potential_functions(params)
    matrix_function = symbolic["matrix_function"]

    ratios = np.logspace(-3, 3, 61)
    envelopes: list[dict[str, float]] = []
    global_negative_count = 0
    global_zero_count = 0
    global_min_constraint_singular = math.inf
    low_ratio_values: list[float] = []
    low_min_eigenvalues: list[float] = []

    for ratio in ratios:
        minimum_kinetic = math.inf
        minimum_kinetic_time = 0.0
        maximum_condition = 0.0
        maximum_condition_time = 0.0
        minimum_constraint_singular = math.inf
        minimum_constraint_time = 0.0
        negative_count = 0
        zero_count = 0

        for row in rows:
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
            kinetic, _, _, constraint = evaluate_matrices(
                matrix_function, params, state
            )
            normalization = np.diag(
                [1.0, 1.0, 1.0 / row["rho"]]
            )
            kinetic_normalized = (
                normalization.T @ kinetic @ normalization
            )
            eigenvalues = np.linalg.eigvalsh(
                (kinetic_normalized + kinetic_normalized.T) / 2
            )
            tolerance = (
                1.0e-10
                * max(float(np.max(np.abs(eigenvalues))), 1.0)
            )
            negative_count += int(np.sum(eigenvalues < -tolerance))
            zero_count += int(np.sum(np.abs(eigenvalues) <= tolerance))
            smallest = float(np.min(eigenvalues))
            condition = float(
                np.max(np.abs(eigenvalues))
                / max(np.min(np.abs(eigenvalues)), 1.0e-300)
            )
            if smallest < minimum_kinetic:
                minimum_kinetic = smallest
                minimum_kinetic_time = row["t"]
            if condition > maximum_condition:
                maximum_condition = condition
                maximum_condition_time = row["t"]

            constraint_singular = float(
                np.min(np.linalg.svd(constraint, compute_uv=False))
            )
            if constraint_singular < minimum_constraint_singular:
                minimum_constraint_singular = constraint_singular
                minimum_constraint_time = row["t"]

        global_negative_count += negative_count
        global_zero_count += zero_count
        global_min_constraint_singular = min(
            global_min_constraint_singular,
            minimum_constraint_singular,
        )
        envelopes.append(
            {
                "q_over_H": float(ratio),
                "minimum_normalized_kinetic_eigenvalue": (
                    minimum_kinetic
                ),
                "minimum_kinetic_time": minimum_kinetic_time,
                "maximum_normalized_kinetic_condition": (
                    maximum_condition
                ),
                "maximum_condition_time": maximum_condition_time,
                "minimum_constraint_singular_value": (
                    minimum_constraint_singular
                ),
                "minimum_constraint_time": minimum_constraint_time,
                "negative_kinetic_count": float(negative_count),
                "numerical_zero_count": float(zero_count),
            }
        )
        if ratio <= 0.1:
            low_ratio_values.append(float(ratio))
            low_min_eigenvalues.append(minimum_kinetic)

    require("no finite-q kinetic ghosts", global_negative_count == 0)
    require(
        "finite-q constraints remain invertible",
        global_min_constraint_singular > 1.0e-8,
    )
    require(
        "positive low-q eigenvalues for fit",
        min(low_min_eigenvalues) > 0,
    )
    low_q_slope, low_q_intercept = np.polyfit(
        np.log(low_ratio_values),
        np.log(low_min_eigenvalues),
        1,
    )
    require(
        "quadratic low-q kinetic collapse",
        abs(float(low_q_slope) - 2.0) < 0.05,
    )

    snapshot_indices = sorted(
        {
            0,
            len(rows) // 4,
            len(rows) // 2,
            3 * len(rows) // 4,
            len(rows) - 1,
        }
    )
    generator_ratios = [1000.0, 100.0, 10.0, 1.0, 0.1, 0.01, 0.001]
    generator_samples: list[dict[str, object]] = []
    maximum_derivative_error = 0.0
    for index in snapshot_indices:
        row = rows[index]
        for ratio in generator_ratios:
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
            generator, derivative_error = local_equation_generator(
                matrix_function, params, state, potential_prime
            )
            maximum_derivative_error = max(
                maximum_derivative_error, derivative_error
            )
            eigenvalues = np.linalg.eigvals(generator) / row["H"]
            generator_samples.append(
                {
                    "t": row["t"],
                    "q_over_H": ratio,
                    "maximum_real_lambda_over_H": float(
                        np.max(eigenvalues.real)
                    ),
                    "maximum_abs_imag_lambda_over_H": float(
                        np.max(np.abs(eigenvalues.imag))
                    ),
                    "directional_derivative_relative_error": (
                        derivative_error
                    ),
                }
            )
    require(
        "directional derivative convergence",
        maximum_derivative_error < 1.0e-4,
    )

    first = rows[0]
    last = rows[-1]
    q0_eigenvalues: list[dict[str, object]] = []
    for row in (first, last):
        state = np.array(
            [
                row["H"],
                row["rho"],
                row["rho_dot"],
                row["mu"],
                0.0,
            ],
            dtype=float,
        )
        kinetic, _, _, constraint = evaluate_matrices(
            matrix_function, params, state
        )
        normalization = np.diag([1.0, 1.0, 1.0 / row["rho"]])
        kinetic_normalized = normalization.T @ kinetic @ normalization
        eigenvalues = np.linalg.eigvalsh(
            (kinetic_normalized + kinetic_normalized.T) / 2
        )
        q0_eigenvalues.append(
            {
                "t": row["t"],
                "normalized_kinetic_eigenvalues": [
                    float(value) for value in eigenvalues
                ],
                "kinetic_rank_tolerance_1e_9": int(
                    np.linalg.matrix_rank(
                        kinetic_normalized, tol=1.0e-9
                    )
                ),
                "constraint_determinant": float(
                    np.linalg.det(constraint)
                ),
            }
        )
    require(
        "strict q0 kinetic rank loss",
        all(sample["kinetic_rank_tolerance_1e_9"] == 2 for sample in q0_eigenvalues),
    )

    representative = {
        "parameter_scope": (
            "Dimensionless existence example only; not a physical aether, "
            "alignment or cosmological parameter point."
        ),
        "parameters": params,
        "scan_domain": {
            "trajectory_samples": len(rows),
            "q_over_H_minimum": float(ratios[0]),
            "q_over_H_maximum": float(ratios[-1]),
            "q_over_H_samples": len(ratios),
            "total_finite_q_matrix_samples": len(rows) * len(ratios),
        },
        "finite_q_kinetic_inertia": {
            "negative_eigenvalue_count": global_negative_count,
            "numerical_zero_count": global_zero_count,
            "inertia_at_every_scanned_q_gt_0": "3_POSITIVE_0_NEGATIVE",
            "minimum_constraint_singular_value": (
                global_min_constraint_singular
            ),
        },
        "low_q_limit": {
            "fitted_smallest_eigenvalue_power": float(low_q_slope),
            "fitted_log_intercept": float(low_q_intercept),
            "symbolic_kinetic_determinant_power": "q_phys^2",
            "strict_q0_samples": q0_eigenvalues,
            "interpretation": (
                "The reduced kinetic matrix is positive for every scanned "
                "q_phys>0 but loses one rank as q_phys approaches zero. "
                "Because Sigma=q_phys^2 beta is not an independent exactly "
                "homogeneous perturbation, the strict q=0 endpoint is not "
                "classified as a ghost. Cubic normalization is required to "
                "decide whether the approach signals strong coupling."
            ),
        },
        "local_equation_generator": {
            "samples": generator_samples,
            "maximum_directional_derivative_relative_error": (
                maximum_derivative_error
            ),
            "included_background_derivatives": [
                "H_dot",
                "rho_dot",
                "rho_ddot",
                "mu_dot",
                "q_phys_dot=-H*q_phys for fixed comoving k",
            ],
            "interpretation": (
                "These instantaneous first-order eigenvalues retain the "
                "time derivatives of the reduced coefficients. Their real "
                "parts are basis- and background-normalization-dependent and "
                "are recorded as diagnostics, not as invariant instability "
                "rates."
            ),
        },
        "alignment_scope": (
            "zeta_align enters only the phase-gradient stiffness in this "
            "background. The constraint matrix, kinetic inertia and q->0 "
            "rank result are independent of the diagnostic numeric choice."
        ),
    }
    return representative, envelopes


def serializable_symbolic(
    symbolic: dict[str, object],
) -> dict[str, object]:
    expressions = symbolic["expressions"]
    return {
        "variables": {
            "dynamical": ["R", "delta_rho", "vartheta"],
            "velocities": [
                "R_dot",
                "delta_rho_dot",
                "vartheta_dot",
            ],
            "constraints": [
                "delta_N",
                "Sigma=q_phys^2*beta",
            ],
        },
        "potential": str(expressions["potential"]),
        "potential_prime": str(expressions["potential_prime"]),
        "potential_second": str(expressions["potential_second"]),
        "constraint_matrix": str(expressions["constraint_matrix"]),
        "constraint_source": str(expressions["constraint_source"]),
        "constraint_solution": (
            "z=-C_constraint^{-1}*source; full symbolic matrix verified"
        ),
        "independent_quadratic_adm_reconstruction": (
            "VERIFIED_ON_SHELL_AGAINST_UNSIMPLIFIED_MODE_EXPANSION"
        ),
        "reduced_lagrangian": (
            "L_reduced=L_unconstrained"
            "-source^T*C_constraint^{-1}*source/2"
        ),
        "kinetic_determinant_on_shell": str(
            expressions["kinetic_determinant_on_shell"]
        ),
        "high_q_curvature_velocity_hessian": str(
            expressions["high_q_curvature_hessian"]
        ),
        "force_block": (
            "K_Q*pi_dot^2/2"
            "-gamma*q_phys^4*pi^2/(2*M_star^2)"
        ),
    }


def write_scan_csv(
    path: Path,
    rows: list[dict[str, float]],
) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    symbolic = symbolic_reduction()
    frw, rows = load_inputs(args.frw_summary, args.frw_trajectory)
    representative, envelopes = representative_scan(
        symbolic, frw, rows, args.alignment
    )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_SCALAR_ADM_FINITE_Q_TIME_DEPENDENT",
        "calculation_status": "PASS",
        "reduction_status": "PASS_FINITE_Q_CONSTRAINT_ELIMINATION",
        "low_q_status": "HOLD_KINETIC_RANK_LOSS_AT_Q_TO_ZERO",
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "gauge_and_scope": {
            "gauge": (
                "aether-unitary scalar gauge with U^mu equal to the ADM "
                "unit normal"
            ),
            "metric": (
                "N=1+delta_N, N_i=partial_i beta, "
                "h_ij=a^2 exp(2R) delta_ij"
            ),
            "retained": (
                "all quadratic q_phys^4, q_phys^2 and q_phys^0 terms in "
                "the declared two-derivative metric-aether-condensate "
                "sector, plus full evolving-background coefficient "
                "derivatives"
            ),
            "force_background": (
                "psi_bar=constant; the quadratic z=2 force mode remains "
                "factorized"
            ),
        },
        "symbolic_reduction": serializable_symbolic(symbolic),
        "representative_branch": representative,
        "scientific_boundary": (
            "The finite-q algebra and representative kinetic-inertia scan "
            "are verified. The q->0 rank loss is a hold point, not a ghost "
            "claim: the exactly homogeneous momentum constraint has "
            "different gauge content, and the cubic action is required to "
            "measure the canonical interaction scale. Matter coupling, "
            "reservoir response, vector/tensor completion and physical "
            "parameter selection remain open."
        ),
        "next_required_calculation": [
            (
                "expand the scalar action to cubic order in the low-q "
                "eigenbasis and canonically normalize the collapsing mode"
            ),
            (
                "determine whether the inferred interaction scale stays "
                "above H and the physical momenta used by the EFT"
            ),
            (
                "derive the matter/reservoir perturbation response before "
                "testing phenomenology"
            ),
            (
                "complete vector and tensor Hamiltonians and return to the "
                "multicone causal-domain audit"
            ),
        ],
    }

    json_path = (
        args.output_dir / "uvir003_scalar_adm_finite_q_summary.json"
    )
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    csv_path = (
        args.output_dir / "uvir003_scalar_adm_finite_q_scan.csv"
    )
    write_scan_csv(csv_path, envelopes)

    low_q = representative["low_q_limit"]
    inertia = representative["finite_q_kinetic_inertia"]
    print("UVIR-003 finite-q scalar ADM identities: VERIFIED")
    print("Finite-q lapse and momentum constraints: ELIMINATED")
    print(
        "Finite-q kinetic inertia over representative scan: "
        f"{inertia['inertia_at_every_scanned_q_gt_0']}"
    )
    print(
        "Low-q smallest-eigenvalue power: "
        f"{low_q['fitted_smallest_eigenvalue_power']:.8f}"
    )
    print("Strict q->0 reduced kinetic rank: 2_OF_3")
    print(
        "Low-q decision: HOLD_KINETIC_RANK_LOSS_AT_Q_TO_ZERO"
    )
    print("Full UVIR-003 gate: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_FINITE_Q_REDUCTION_WITH_LOW_Q_HOLD")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
