#!/usr/bin/env python3
"""Project the UVIR-003 cubic kernel onto two on-shell physical mode legs.

At an admitted local frozen-time point, the coupled finite-q poles are
residue-normalized and ordered by frequency. Two such external legs are
inserted into the verified factorized cubic kernel. The third leg is kept
off shell and evaluated on each physical coordinate basis vector with

    p_dot_K = -i Omega_K p_K,
    Omega_K = -(Omega_1 + Omega_2).

This returns the four-component cubic pair-source covector for

    p_K = (Xi, Q_rho, Q_chi, Pi).

The script then applies the already verified finite-q inverse quadratic
kernel as a response diagnostic. It does not contract two pair sources,
add the reduced quartic contact, define a cosmological S-matrix, or infer a
unitarity/strong-coupling scale.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
from pathlib import Path
from typing import Any, Callable

import numpy as np
import sympy as sp

from uvir003_physical_quadratic_propagators import (
    add_force_block,
    evaluate_physical_matrices,
    inverse_kernel,
    quadratic_poles,
    symbolic_propagators,
)
from uvir003_scalar_adm_finite_q import (
    background_parameters,
    load_inputs,
)


FIELDS = ("Xi", "Q_rho", "Q_chi", "Pi")
COUPLED_FIELDS = FIELDS[:3]


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
        "--exchange-domain",
        type=Path,
        default=base / "outputs" / "uvir003_controlled_exchange_domain_summary.json",
    )
    parser.add_argument(
        "--ratios",
        type=float,
        nargs="+",
        default=[47.5, 50.0, 75.0, 100.0],
    )
    parser.add_argument("--alignment", type=float, default=1.0)
    parser.add_argument("--K-Q", type=float, default=1.0)
    parser.add_argument("--gamma", type=float, default=1.0)
    parser.add_argument("--M-star-sq", type=float, default=1.0)
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def compile_expression(
    expression: str,
) -> tuple[tuple[sp.Symbol, ...], Callable[..., Any]]:
    parsed = sp.sympify(
        expression,
        locals={"gamma": sp.Symbol("gamma", real=True)},
    )
    symbols = tuple(sorted(parsed.free_symbols, key=lambda item: item.name))
    return symbols, sp.lambdify(symbols, parsed, modules="numpy", cse=True)


def evaluate_compiled(
    compiled: tuple[tuple[sp.Symbol, ...], Callable[..., Any]],
    values: dict[str, complex | float],
) -> complex:
    symbols, function = compiled
    missing = [symbol.name for symbol in symbols if symbol.name not in values]
    require("complete numerical substitution", not missing)
    result = complex(function(*(values[symbol.name] for symbol in symbols)))
    require(
        "finite compiled expression",
        math.isfinite(result.real) and math.isfinite(result.imag),
    )
    return result


def potential_values(
    params: dict[str, float],
    rho: float,
) -> tuple[float, float, float, float]:
    mass = params["m_squared"]
    quartic = params["lambda4"]
    sextic = params["lambda6"]
    cutoff2 = params["Lambda"] ** 2
    potential = (
        mass * rho**2 / 2
        + quartic * rho**4 / 8
        + sextic * rho**6 / (24 * cutoff2)
    )
    first = (
        mass * rho
        + quartic * rho**3 / 2
        + sextic * rho**5 / (4 * cutoff2)
    )
    second = (
        mass
        + 3 * quartic * rho**2 / 2
        + 5 * sextic * rho**4 / (4 * cutoff2)
    )
    third = 3 * quartic * rho + 5 * sextic * rho**3 / cutoff2
    return potential, first, second, third


def background_values(
    params: dict[str, float],
    row: dict[str, float],
    gamma: float,
    k_q: float,
    mstar2: float,
) -> dict[str, complex | float]:
    hubble = row["H"]
    rho = row["rho"]
    rho_dot = row["rho_dot"]
    chemical = row["mu"]
    potential, first, second, third = potential_values(params, rho)
    hubble_dot = -(
        rho_dot**2 + rho**2 * chemical**2
    ) / (2 * params["M_cos_sq"])
    rho_ddot = -3 * hubble * rho_dot + rho * chemical**2 - first
    chemical_dot = chemical * (-3 * hubble - 2 * rho_dot / rho)
    return {
        **params,
        "H": hubble,
        "rho": rho,
        "rho_dot": rho_dot,
        "mu": chemical,
        "H_dot": hubble_dot,
        "rho_ddot": rho_ddot,
        "mu_dot": chemical_dot,
        "V": potential,
        "V_rho": first,
        "V_rhorho": second,
        "V_rhorhorho": third,
        "gamma": gamma,
        "K_Q": k_q,
        "M_star_sq": mstar2,
    }


def normalized_modes(
    kinetic: np.ndarray,
    mixed: np.ndarray,
    coordinate: np.ndarray,
    hubble: float,
) -> list[dict[str, Any]]:
    poles = quadratic_poles(kinetic, mixed, coordinate)
    scale = max(float(np.max(np.abs(poles))), hubble, 1.0e-30)
    positive = sorted(
        float(pole.real)
        for pole in poles
        if (
            pole.real > 1.0e-8 * scale
            and abs(pole.imag) <= 2.0e-7 * scale
        )
    )
    require("three positive coupled poles", len(positive) == 3)
    gyroscopic = mixed - mixed.T
    modes: list[dict[str, Any]] = []
    for index, omega in enumerate(positive, start=1):
        kernel = inverse_kernel(omega, kinetic, mixed, coordinate)
        eigenvalues, eigenvectors = np.linalg.eigh(
            (kernel + kernel.conj().T) / 2
        )
        vector = eigenvectors[:, int(np.argmin(np.abs(eigenvalues)))]
        derivative = 2 * omega * kinetic + 1j * gyroscopic
        residue = float(np.real(vector.conj().T @ derivative @ vector))
        require("positive pole residue", residue > 0.0)
        vector = vector / math.sqrt(residue)
        pivot = int(np.argmax(np.abs(vector)))
        vector = vector * np.exp(-1j * np.angle(vector[pivot]))
        normalized_residue = float(
            np.real(vector.conj().T @ derivative @ vector)
        )
        residual = float(
            np.linalg.norm(kernel @ vector)
            / max(np.linalg.norm(kernel) * np.linalg.norm(vector), 1.0e-30)
        )
        weights = np.abs(vector) ** 2
        weights = weights / np.sum(weights)
        modes.append(
            {
                "label": f"physical_pair_{index}",
                "omega": omega,
                "omega_over_H": omega / hubble,
                "vector": vector,
                "residue_normalization": normalized_residue,
                "kernel_residual": residual,
                "field_weights": {
                    field: float(weights[field_index])
                    for field_index, field in enumerate(COUPLED_FIELDS)
                },
            }
        )
    return modes


def set_leg(
    values: dict[str, complex | float],
    leg: int,
    vector: np.ndarray,
    signed_frequency: float,
) -> None:
    for field_index, field in enumerate(FIELDS):
        component = complex(vector[field_index])
        values[f"{field}_{leg}"] = component
        values[f"{field}_dot_{leg}"] = -1j * signed_frequency * component


def signed_mode_leg(
    mode: dict[str, Any],
    sign: int,
) -> tuple[np.ndarray, float]:
    require("frequency sign", sign in (-1, 1))
    vector = np.asarray(mode["vector"], dtype=complex)
    if sign < 0:
        vector = vector.conj()
    return vector, sign * float(mode["omega"])


class CubicEvaluator:
    def __init__(self, summary: dict[str, Any]) -> None:
        result = summary["result"]
        self.kernel = compile_expression(
            result["physical_basis_kernel"]["expression"]
        )
        self.lapse = {}
        self.sigma = {}
        for leg in range(1, 4):
            resolver = result["constraint_resolvers"][f"leg_{leg}"]
            self.lapse[leg] = compile_expression(
                resolver["physical_basis_delta_N_1"]
            )
            self.sigma[leg] = compile_expression(
                resolver["physical_basis_Sigma_1"]
            )

    def evaluate(
        self,
        values: dict[str, complex | float],
    ) -> complex:
        complete = dict(values)
        for leg in range(1, 4):
            complete[f"delta_N_1_{leg}"] = evaluate_compiled(
                self.lapse[leg], complete
            )
            complete[f"Sigma_1_{leg}"] = evaluate_compiled(
                self.sigma[leg], complete
            )
        return evaluate_compiled(self.kernel, complete)


def pair_source(
    evaluator: CubicEvaluator,
    background: dict[str, complex | float],
    q: float,
    left_mode: dict[str, Any],
    left_sign: int,
    right_mode: dict[str, Any],
    right_sign: int,
    swap_external: bool = False,
) -> tuple[np.ndarray, float]:
    left_vector, left_frequency = signed_mode_leg(left_mode, left_sign)
    right_vector, right_frequency = signed_mode_leg(right_mode, right_sign)
    if swap_external:
        left_vector, right_vector = right_vector, left_vector
        left_frequency, right_frequency = right_frequency, left_frequency
    internal_frequency = -(left_frequency + right_frequency)
    source = np.zeros(4, dtype=complex)
    for component in range(4):
        values = dict(background)
        values.update({"q_1": q, "q_2": q, "q_3": q})
        full_left = np.zeros(4, dtype=complex)
        full_right = np.zeros(4, dtype=complex)
        full_left[:3] = left_vector
        full_right[:3] = right_vector
        set_leg(values, 1, full_left, left_frequency)
        set_leg(values, 2, full_right, right_frequency)
        internal = np.zeros(4, dtype=complex)
        internal[component] = 1.0
        set_leg(values, 3, internal, internal_frequency)
        source[component] = evaluator.evaluate(values)
    return source, internal_frequency


def complex_record(values: np.ndarray) -> dict[str, dict[str, float]]:
    return {
        field: {
            "real": float(values[index].real),
            "imag": float(values[index].imag),
            "abs": float(abs(values[index])),
        }
        for index, field in enumerate(FIELDS)
    }


def audit_case(
    evaluator: CubicEvaluator,
    background: dict[str, complex | float],
    matrices: tuple[np.ndarray, np.ndarray, np.ndarray],
    modes: list[dict[str, Any]],
    q: float,
    hubble: float,
    ratio: float,
    left_index: int,
    right_index: int,
    sign_pattern: tuple[int, int],
    k_q: float,
    gamma: float,
    mstar2: float,
) -> dict[str, Any]:
    left = modes[left_index]
    right = modes[right_index]
    source, internal_frequency = pair_source(
        evaluator,
        background,
        q,
        left,
        sign_pattern[0],
        right,
        sign_pattern[1],
    )
    swapped, swapped_frequency = pair_source(
        evaluator,
        background,
        q,
        left,
        sign_pattern[0],
        right,
        sign_pattern[1],
        swap_external=True,
    )
    require(
        "swapped internal frequency",
        abs(swapped_frequency - internal_frequency) < 1.0e-12,
    )
    permutation_error = float(
        np.linalg.norm(source - swapped)
        / max(np.linalg.norm(source), np.linalg.norm(swapped), 1.0e-30)
    )

    full_matrices = add_force_block(matrices, q, k_q, gamma, mstar2)
    kernel = inverse_kernel(internal_frequency, *full_matrices)
    condition = float(np.linalg.cond(kernel))
    response = np.linalg.solve(kernel, source)
    inverse_residual = float(
        np.linalg.norm(kernel @ response - source)
        / max(np.linalg.norm(source), 1.0e-30)
    )
    poles = quadratic_poles(*full_matrices)
    pole_separation = float(
        np.min(np.abs(poles - internal_frequency))
        / max(abs(internal_frequency), hubble)
    )
    determinant = (
        -background["C_14"] * background["D_123"] * q**2
        + 2 * background["D_123"] * background["V"]
        - 4 * hubble**2 * background["M_cos_sq"] ** 2
    )
    determinant_scale = max(
        abs(background["C_14"] * background["D_123"] * q**2),
        abs(2 * background["D_123"] * background["V"]),
        abs(4 * hubble**2 * background["M_cos_sq"] ** 2),
        1.0e-30,
    )
    determinant_margin = float(abs(determinant) / determinant_scale)
    force_fraction = float(
        abs(source[3]) / max(np.linalg.norm(source), 1.0e-30)
    )
    return {
        "initial_q_over_H": ratio,
        "q": q,
        "external_geometry": "equilateral_spatial_triangle",
        "left_mode": left["label"],
        "right_mode": right["label"],
        "left_frequency_sign": sign_pattern[0],
        "right_frequency_sign": sign_pattern[1],
        "channel_frequency": internal_frequency,
        "channel_abs_frequency_over_H": abs(internal_frequency) / hubble,
        "constraint_determinant_relative_margin": determinant_margin,
        "pair_source_norm": float(np.linalg.norm(source)),
        "pair_source": complex_record(source),
        "force_source_fraction": force_fraction,
        "external_swap_relative_error": permutation_error,
        "inverse_kernel_condition_number": condition,
        "distance_to_nearest_local_pole": pole_separation,
        "inverse_response_norm": float(np.linalg.norm(response)),
        "inverse_response": complex_record(response),
        "inverse_closure_relative_error": inverse_residual,
    }


def write_csv(path: Path, cases: list[dict[str, Any]]) -> None:
    fields = [
        "initial_q_over_H",
        "left_mode",
        "right_mode",
        "left_frequency_sign",
        "right_frequency_sign",
        "channel_abs_frequency_over_H",
        "constraint_determinant_relative_margin",
        "pair_source_norm",
        "force_source_fraction",
        "external_swap_relative_error",
        "inverse_kernel_condition_number",
        "distance_to_nearest_local_pole",
        "inverse_response_norm",
        "inverse_closure_relative_error",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(
            {field: case[field] for field in fields}
            for case in cases
        )


def main() -> None:
    args = parse_args()
    require("positive ratios", all(value > 0.0 for value in args.ratios))
    require("positive K_Q", args.K_Q > 0.0)
    require("positive gamma", args.gamma > 0.0)
    require("positive M_star_sq", args.M_star_sq > 0.0)

    cubic = load_json(args.cubic_kernel)
    domain = load_json(args.exchange_domain)
    require(
        "verified cubic dependency",
        cubic["subgate_status"]
        == "PASS_FACTORIZED_FINITE_Q_PHYSICAL_CUBIC_KERNEL",
    )
    require(
        "controlled exchange-domain dependency",
        domain["subgate_status"]
        == "PASS_CONTROLLED_REAL_POLE_ADIABATIC_EXCHANGE_DOMAIN",
    )
    admitted = set(
        float(value)
        for value in domain["sampled_domain"][
            "admitted_initial_q_over_H_values"
        ]
    )
    require(
        "requested ratios admitted",
        all(float(value) in admitted for value in args.ratios),
    )

    frw, rows = load_inputs(args.frw_summary, args.frw_trajectory)
    params = background_parameters(frw, args.alignment)
    params["zeta_align"] = args.alignment
    symbolic = symbolic_propagators()
    evaluator = CubicEvaluator(cubic)
    row = rows[0]
    background = background_values(
        params,
        row,
        args.gamma,
        args.K_Q,
        args.M_star_sq,
    )

    case_results: list[dict[str, Any]] = []
    mode_results: list[dict[str, Any]] = []
    sign_patterns = ((1, 1), (1, -1))
    for ratio in sorted(set(args.ratios)):
        q = ratio * row["H"]
        state = np.asarray(
            [row["H"], row["rho"], row["rho_dot"], row["mu"], q],
            dtype=float,
        )
        matrices = evaluate_physical_matrices(symbolic, params, state)
        modes = normalized_modes(*matrices, row["H"])
        mode_results.append(
            {
                "initial_q_over_H": ratio,
                "modes": [
                    {
                        key: value
                        for key, value in mode.items()
                        if key != "vector"
                    }
                    for mode in modes
                ],
            }
        )
        for left_index, right_index in itertools.combinations_with_replacement(
            range(3), 2
        ):
            for sign_pattern in sign_patterns:
                case_results.append(
                    audit_case(
                        evaluator,
                        background,
                        matrices,
                        modes,
                        q,
                        row["H"],
                        ratio,
                        left_index,
                        right_index,
                        sign_pattern,
                        args.K_Q,
                        args.gamma,
                        args.M_star_sq,
                    )
                )

    maximum_mode_residual = max(
        mode["kernel_residual"]
        for result in mode_results
        for mode in result["modes"]
    )
    maximum_residue_error = max(
        abs(mode["residue_normalization"] - 1.0)
        for result in mode_results
        for mode in result["modes"]
    )
    maximum_permutation_error = max(
        case["external_swap_relative_error"] for case in case_results
    )
    maximum_inverse_error = max(
        case["inverse_closure_relative_error"] for case in case_results
    )
    minimum_constraint_margin = min(
        case["constraint_determinant_relative_margin"]
        for case in case_results
    )
    minimum_pole_separation = min(
        case["distance_to_nearest_local_pole"] for case in case_results
    )
    maximum_force_fraction = max(
        case["force_source_fraction"] for case in case_results
    )
    all_sources_nonzero = all(
        case["pair_source_norm"] > 1.0e-12 for case in case_results
    )
    all_finite = all(
        math.isfinite(case["inverse_kernel_condition_number"])
        and math.isfinite(case["inverse_response_norm"])
        for case in case_results
    )
    passed = (
        maximum_mode_residual < 1.0e-12
        and maximum_residue_error < 1.0e-12
        and maximum_permutation_error < 1.0e-11
        and maximum_inverse_error < 1.0e-10
        and minimum_constraint_margin > 1.0e-4
        and minimum_pole_separation > 1.0e-4
        and maximum_force_fraction < 1.0e-12
        and all_sources_nonzero
        and all_finite
    )
    require("mode-projected cubic pair-source audit", passed)

    summary = {
        "gate": "UVIR-003",
        "stage": "B_MODE_PROJECTED_CUBIC_PAIR_SOURCE",
        "calculation_status": "PASS",
        "subgate_status": "PASS_MODE_PROJECTED_CUBIC_PAIR_SOURCE",
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "parameter_scope": (
            "Representative dimensionless branch at its initial frozen-time "
            "snapshot. K_Q=gamma=M_star_sq=1 remains a diagnostic force-mode "
            "normalization."
        ),
        "kinematics": {
            "spatial_geometry": (
                "q1=q2=qK with k1+k2+kK=0; pairwise angle 120 degrees"
            ),
            "external_time_dependence": "p_dot=-i Omega p",
            "external_frequency_sign_patterns": ["(+,+)", "(+,-)"],
            "channel_frequency_rule": "Omega_K=-(Omega_1+Omega_2)",
            "mode_labels": (
                "Local coupled physical pairs ordered by positive frequency; "
                "no infrared Xi-pure identity is assigned."
            ),
            "normalization": (
                "v_dagger(2 omega K+i(P-P^T))v=1"
            ),
        },
        "mode_results": mode_results,
        "case_results": case_results,
        "diagnostics": {
            "case_count": len(case_results),
            "maximum_on_shell_kernel_residual": maximum_mode_residual,
            "maximum_residue_normalization_error": maximum_residue_error,
            "maximum_external_swap_relative_error": maximum_permutation_error,
            "maximum_inverse_closure_relative_error": maximum_inverse_error,
            "minimum_constraint_determinant_relative_margin": (
                minimum_constraint_margin
            ),
            "minimum_distance_to_nearest_local_pole": minimum_pole_separation,
            "maximum_force_pair_source_fraction": maximum_force_fraction,
            "all_pair_sources_nonzero": all_sources_nonzero,
            "all_responses_finite": all_finite,
        },
        "result": (
            "The verified analytic cubic kernel produces finite, nonzero "
            "four-component pair-source covectors when two admitted "
            "residue-normalized coupled modes are inserted. For two coupled "
            "external legs the factorized Pi source vanishes at this cubic "
            "order. The nonzero-channel inverse-kernel responses close "
            "numerically and remain separated from sampled local poles."
        ),
        "scientific_boundary": (
            "This is a local frozen-time pair-source and propagator-response "
            "audit, not a completed exchange amplitude. It has not contracted "
            "left and right pair sources, summed channels, included the "
            "reduced quartic contact, selected an in/out cosmological state, "
            "or applied a unitarity criterion. The held nonanalytic "
            "|grad(pi)|^3 vertex still requires a declared nonzero-gradient "
            "local background."
        ),
        "next_required_calculation": [
            "construct matched left/right pair sources for a declared four-leg in/out kinematic configuration",
            "contract each nonzero channel through the finite-q propagator",
            "apply the separate homogeneous projector to exact q_K=0 channels",
            "add the reduced quartic contact before interpreting the combined result",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = (
        args.output_dir
        / "uvir003_mode_projected_cubic_pair_source_summary.json"
    )
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    write_csv(
        args.output_dir / "uvir003_mode_projected_cubic_pair_source.csv",
        case_results,
    )

    print("Residue-normalized coupled mode legs: VERIFIED")
    print("Mode-projected cubic pair sources: NONZERO_AND_FINITE")
    print("External-leg permutation audit: PASS")
    print("Nonzero-channel inverse response: VERIFIED")
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_MODE_PROJECTED_CUBIC_PAIR_SOURCE")


if __name__ == "__main__":
    main()
