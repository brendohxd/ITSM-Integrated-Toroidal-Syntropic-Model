#!/usr/bin/env python3
"""Assemble the local UVIR-003 exchange-plus-reduced-contact four-leg kernel.

The calculation uses one frozen-time snapshot on the representative FRW
branch. Four residue-normalized coupled modes are placed on shell in an
all-incoming elastic convention,

    (a+, b+, a-, b-),

and assigned equal-magnitude spatial momenta at the vertices of a regular
tetrahedron. The three pair partitions therefore have the same strictly
nonzero internal momentum

    q_K = 2 q / sqrt(3).

Each internal trajectory must independently pass the controlled real-pole,
subhorizon and adiabatic exchange-domain audit. The script then combines:

* the three matched physical cubic-source propagator contractions;
* the polarized analytic quartic contact; and
* the three constraint-induced quartic Schur pairings.

The result is a local frozen-time on-shell four-leg kernel. It is not a
cosmological S-matrix amplitude and does not define a unitarity bound,
strong-coupling scale, or physical cutoff. The nonanalytic |grad(pi)|^3
sector remains held for a declared nonzero-gradient local background.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from uvir003_controlled_exchange_domain import audit_ratio
from uvir003_mode_projected_cubic_pair_source import (
    COUPLED_FIELDS,
    FIELDS,
    CubicEvaluator,
    background_values,
    compile_expression,
    complex_record,
    evaluate_compiled,
    normalized_modes,
    set_leg,
    signed_mode_leg,
)
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


PARTITIONS = (
    ((0, 1), (2, 3), "s"),
    ((0, 2), (1, 3), "t"),
    ((0, 3), (1, 2), "u"),
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
    parser.add_argument("--adiabatic-threshold", type=float, default=0.1)
    parser.add_argument("--subhorizon-margin", type=float, default=10.0)
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fourth_potential_derivative(
    params: dict[str, float],
    rho: float,
) -> float:
    return (
        3.0 * params["lambda4"]
        + 15.0 * params["lambda6"] * rho**2 / params["Lambda"] ** 2
    )


def full_mode_leg(
    mode: dict[str, Any],
    sign: int,
) -> tuple[np.ndarray, float]:
    coupled, frequency = signed_mode_leg(mode, sign)
    vector = np.zeros(4, dtype=complex)
    vector[:3] = coupled
    return vector, frequency


class QuarticEvaluator:
    def __init__(self, summary: dict[str, Any]) -> None:
        result = summary["result"]
        contact = result["analytic_contact_kernel"]
        source = result["complete_pair_source_kernel"]
        self.contact_kernel = compile_expression(
            contact["physical_basis_expression"]
        )
        self.contact_lapse = {}
        self.contact_sigma = {}
        for leg in range(1, 5):
            resolver = contact["constraint_resolvers"][f"leg_{leg}"]
            self.contact_lapse[leg] = compile_expression(
                resolver["physical_basis_delta_N_1"]
            )
            self.contact_sigma[leg] = compile_expression(
                resolver["physical_basis_Sigma_1"]
            )

        self.constraint_source_n = compile_expression(source["B_N_ab"])
        self.constraint_source_sigma = compile_expression(
            source["B_Sigma_ab"]
        )
        self.input_lapse = {}
        self.input_sigma = {}
        for index, label in enumerate(("a", "b"), start=1):
            resolver = source["input_constraint_resolvers"][
                f"input_{label}"
            ]
            self.input_lapse[index] = compile_expression(
                resolver["physical_basis_delta_N_1"]
            )
            self.input_sigma[index] = compile_expression(
                resolver["physical_basis_Sigma_1"]
            )

    def contact(
        self,
        values: dict[str, complex | float],
    ) -> complex:
        complete = dict(values)
        for leg in range(1, 5):
            complete[f"delta_N_1_{leg}"] = evaluate_compiled(
                self.contact_lapse[leg], complete
            )
            complete[f"Sigma_1_{leg}"] = evaluate_compiled(
                self.contact_sigma[leg], complete
            )
        return evaluate_compiled(self.contact_kernel, complete)

    def constraint_source(
        self,
        background: dict[str, complex | float],
        q_external: float,
        q_channel: float,
        first: tuple[np.ndarray, float],
        second: tuple[np.ndarray, float],
    ) -> np.ndarray:
        values = dict(background)
        values.update(
            {
                "q_a": q_external,
                "q_b": q_external,
                "q_K": q_channel,
            }
        )
        set_leg(values, 1, first[0], first[1])
        set_leg(values, 2, second[0], second[1])
        values["delta_N_a"] = evaluate_compiled(
            self.input_lapse[1], values
        )
        values["Sigma_a"] = evaluate_compiled(
            self.input_sigma[1], values
        )
        values["delta_N_b"] = evaluate_compiled(
            self.input_lapse[2], values
        )
        values["Sigma_b"] = evaluate_compiled(
            self.input_sigma[2], values
        )
        return np.asarray(
            [
                evaluate_compiled(self.constraint_source_n, values),
                evaluate_compiled(self.constraint_source_sigma, values),
            ],
            dtype=complex,
        )


def physical_pair_source(
    evaluator: CubicEvaluator,
    background: dict[str, complex | float],
    q_external: float,
    q_channel: float,
    first: tuple[np.ndarray, float],
    second: tuple[np.ndarray, float],
) -> tuple[np.ndarray, float]:
    internal_frequency = -(first[1] + second[1])
    source = np.zeros(4, dtype=complex)
    for component in range(4):
        values = dict(background)
        values.update(
            {
                "q_1": q_external,
                "q_2": q_external,
                "q_3": q_channel,
            }
        )
        set_leg(values, 1, first[0], first[1])
        set_leg(values, 2, second[0], second[1])
        internal = np.zeros(4, dtype=complex)
        internal[component] = 1.0
        set_leg(values, 3, internal, internal_frequency)
        source[component] = evaluator.evaluate(values)
    return source, internal_frequency


def constraint_inverse(
    background: dict[str, complex | float],
    q_channel: float,
) -> np.ndarray:
    matrix = np.asarray(
        [
            [
                background["C_14"] * q_channel**2 - 2.0 * background["V"],
                2.0 * background["M_cos_sq"] * background["H"],
            ],
            [
                2.0 * background["M_cos_sq"] * background["H"],
                -background["D_123"],
            ],
        ],
        dtype=complex,
    )
    return np.linalg.inv(matrix)


def tetrahedral_contact_values(
    background: dict[str, complex | float],
    q: float,
    legs: list[tuple[np.ndarray, float]],
) -> dict[str, complex | float]:
    values = dict(background)
    for index, leg in enumerate(legs, start=1):
        values[f"q_{index}"] = q
        set_leg(values, index, leg[0], leg[1])
    dot = -q**2 / 3.0
    for first in range(1, 5):
        for second in range(first + 1, 5):
            values[f"k{first}_dot_k{second}"] = dot
    return values


def relative_error(first: complex, second: complex) -> float:
    return float(
        abs(first - second)
        / max(abs(first), abs(second), 1.0e-30)
    )


def complex_scalar(value: complex) -> dict[str, float]:
    return {
        "real": float(value.real),
        "imag": float(value.imag),
        "abs": float(abs(value)),
    }


def assemble_case(
    cubic: CubicEvaluator,
    quartic: QuarticEvaluator,
    symbolic: dict[str, object],
    params: dict[str, float],
    background: dict[str, complex | float],
    modes: list[dict[str, Any]],
    ratio: float,
    q: float,
    channel_q: float,
    left_index: int,
    right_index: int,
    k_q: float,
    gamma: float,
    mstar2: float,
    swap_species: bool = False,
) -> dict[str, Any]:
    mode_a = modes[right_index if swap_species else left_index]
    mode_b = modes[left_index if swap_species else right_index]
    legs = [
        full_mode_leg(mode_a, 1),
        full_mode_leg(mode_b, 1),
        full_mode_leg(mode_a, -1),
        full_mode_leg(mode_b, -1),
    ]
    frequency_closure = abs(sum(leg[1] for leg in legs))
    contact = quartic.contact(
        tetrahedral_contact_values(background, q, legs)
    )

    channel_state = np.asarray(
        [
            background["H"],
            background["rho"],
            background["rho_dot"],
            background["mu"],
            channel_q,
        ],
        dtype=float,
    )
    channel_matrices = add_force_block(
        evaluate_physical_matrices(symbolic, params, channel_state),
        channel_q,
        k_q,
        gamma,
        mstar2,
    )
    channel_poles = quadratic_poles(*channel_matrices)
    c_inverse = constraint_inverse(background, channel_q)

    exchange_sum = 0j
    schur_sum = 0j
    channel_results: list[dict[str, Any]] = []
    maximum_source_swap_error = 0.0
    for first_pair, second_pair, name in PARTITIONS:
        first_legs = (legs[first_pair[0]], legs[first_pair[1]])
        second_legs = (legs[second_pair[0]], legs[second_pair[1]])
        left_source, left_frequency = physical_pair_source(
            cubic,
            background,
            q,
            channel_q,
            *first_legs,
        )
        right_source, right_frequency = physical_pair_source(
            cubic,
            background,
            q,
            channel_q,
            *second_legs,
        )
        require(
            f"{name}-channel frequency closure",
            abs(left_frequency + right_frequency) < 1.0e-10,
        )

        swapped_source, swapped_frequency = physical_pair_source(
            cubic,
            background,
            q,
            channel_q,
            first_legs[1],
            first_legs[0],
        )
        require(
            f"{name}-channel swapped frequency",
            abs(swapped_frequency - left_frequency) < 1.0e-12,
        )
        source_swap_error = float(
            np.linalg.norm(left_source - swapped_source)
            / max(
                np.linalg.norm(left_source),
                np.linalg.norm(swapped_source),
                1.0e-30,
            )
        )
        maximum_source_swap_error = max(
            maximum_source_swap_error, source_swap_error
        )

        kernel = inverse_kernel(left_frequency, *channel_matrices)
        propagator = np.linalg.inv(kernel)
        inverse_closure = float(
            np.linalg.norm(kernel @ propagator - np.eye(4))
            / np.linalg.norm(np.eye(4))
        )
        exchange = -complex(
            right_source.T @ propagator @ left_source
        )
        exchange_sum += exchange

        left_constraint = quartic.constraint_source(
            background,
            q,
            channel_q,
            *first_legs,
        )
        right_constraint = quartic.constraint_source(
            background,
            q,
            channel_q,
            *second_legs,
        )
        schur = -complex(
            right_constraint.T @ c_inverse @ left_constraint
        )
        schur_sum += schur

        pole_separation = float(
            np.min(np.abs(channel_poles - left_frequency))
            / max(abs(left_frequency), background["H"])
        )
        channel_results.append(
            {
                "channel": name,
                "pair_partition": [
                    [index + 1 for index in first_pair],
                    [index + 1 for index in second_pair],
                ],
                "q_channel_over_H": channel_q / background["H"],
                "internal_frequency_over_H": (
                    left_frequency / background["H"]
                ),
                "frequency_closure_error": (
                    abs(left_frequency + right_frequency)
                    / background["H"]
                ),
                "left_physical_pair_source": complex_record(left_source),
                "right_physical_pair_source": complex_record(right_source),
                "left_constraint_pair_source": {
                    "delta_N": complex_scalar(left_constraint[0]),
                    "Sigma": complex_scalar(left_constraint[1]),
                },
                "right_constraint_pair_source": {
                    "delta_N": complex_scalar(right_constraint[0]),
                    "Sigma": complex_scalar(right_constraint[1]),
                },
                "physical_exchange": complex_scalar(exchange),
                "constraint_schur": complex_scalar(schur),
                "source_swap_relative_error": source_swap_error,
                "inverse_kernel_condition_number": float(
                    np.linalg.cond(kernel)
                ),
                "inverse_closure_relative_error": inverse_closure,
                "distance_to_nearest_local_pole": pole_separation,
            }
        )

    reduced_contact = contact + schur_sum
    total = reduced_contact + exchange_sum
    scale = max(
        abs(contact)
        + sum(
            item["constraint_schur"]["abs"]
            + item["physical_exchange"]["abs"]
            for item in channel_results
        ),
        1.0e-30,
    )
    return {
        "initial_q_over_H": ratio,
        "channel_q_over_H": channel_q / background["H"],
        "left_mode": mode_a["label"],
        "right_mode": mode_b["label"],
        "kinematics": "regular_tetrahedral_all_incoming_elastic",
        "external_frequency_closure_over_H": (
            frequency_closure / background["H"]
        ),
        "analytic_quartic_contact": complex_scalar(contact),
        "constraint_schur_sum": complex_scalar(schur_sum),
        "reduced_quartic_contact": complex_scalar(reduced_contact),
        "physical_exchange_sum": complex_scalar(exchange_sum),
        "exchange_plus_reduced_contact": complex_scalar(total),
        "total_imaginary_fraction": float(abs(total.imag) / scale),
        "cancellation_ratio": float(abs(total) / scale),
        "maximum_pair_source_swap_relative_error": (
            maximum_source_swap_error
        ),
        "channels": channel_results,
    }


def write_csv(path: Path, cases: list[dict[str, Any]]) -> None:
    fields = [
        "initial_q_over_H",
        "channel_q_over_H",
        "left_mode",
        "right_mode",
        "external_frequency_closure_over_H",
        "analytic_quartic_contact_real",
        "constraint_schur_sum_real",
        "reduced_quartic_contact_real",
        "physical_exchange_sum_real",
        "combined_kernel_real",
        "combined_kernel_abs",
        "total_imaginary_fraction",
        "cancellation_ratio",
        "maximum_pair_source_swap_relative_error",
        "species_permutation_relative_error",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for case in cases:
            writer.writerow(
                {
                    "initial_q_over_H": case["initial_q_over_H"],
                    "channel_q_over_H": case["channel_q_over_H"],
                    "left_mode": case["left_mode"],
                    "right_mode": case["right_mode"],
                    "external_frequency_closure_over_H": (
                        case["external_frequency_closure_over_H"]
                    ),
                    "analytic_quartic_contact_real": (
                        case["analytic_quartic_contact"]["real"]
                    ),
                    "constraint_schur_sum_real": (
                        case["constraint_schur_sum"]["real"]
                    ),
                    "reduced_quartic_contact_real": (
                        case["reduced_quartic_contact"]["real"]
                    ),
                    "physical_exchange_sum_real": (
                        case["physical_exchange_sum"]["real"]
                    ),
                    "combined_kernel_real": (
                        case["exchange_plus_reduced_contact"]["real"]
                    ),
                    "combined_kernel_abs": (
                        case["exchange_plus_reduced_contact"]["abs"]
                    ),
                    "total_imaginary_fraction": (
                        case["total_imaginary_fraction"]
                    ),
                    "cancellation_ratio": case["cancellation_ratio"],
                    "maximum_pair_source_swap_relative_error": (
                        case["maximum_pair_source_swap_relative_error"]
                    ),
                    "species_permutation_relative_error": (
                        case["species_permutation_relative_error"]
                    ),
                }
            )


def main() -> None:
    args = parse_args()
    require("positive ratios", all(value > 0.0 for value in args.ratios))
    require("positive K_Q", args.K_Q > 0.0)
    require("positive gamma", args.gamma > 0.0)
    require("positive M_star_sq", args.M_star_sq > 0.0)

    cubic_summary = load_json(args.cubic_kernel)
    quartic_summary = load_json(args.quartic_kernel)
    domain_summary = load_json(args.exchange_domain)
    require(
        "verified cubic dependency",
        cubic_summary["subgate_status"]
        == "PASS_FACTORIZED_FINITE_Q_PHYSICAL_CUBIC_KERNEL",
    )
    require(
        "verified reduced quartic dependency",
        quartic_summary["subgate_status"]
        == "PASS_FACTORIZED_FINITE_Q_REDUCED_QUARTIC_KERNEL",
    )
    require(
        "controlled external-domain dependency",
        domain_summary["subgate_status"]
        == "PASS_CONTROLLED_REAL_POLE_ADIABATIC_EXCHANGE_DOMAIN",
    )
    admitted_external = set(
        float(value)
        for value in domain_summary["sampled_domain"][
            "admitted_initial_q_over_H_values"
        ]
    )
    require(
        "requested external ratios admitted",
        all(float(value) in admitted_external for value in args.ratios),
    )

    frw, rows = load_inputs(args.frw_summary, args.frw_trajectory)
    params = background_parameters(frw, args.alignment)
    params["zeta_align"] = args.alignment
    symbolic = symbolic_propagators()
    row = rows[0]
    background = background_values(
        params,
        row,
        args.gamma,
        args.K_Q,
        args.M_star_sq,
    )
    background["V_rhorhorhorho"] = fourth_potential_derivative(
        params, row["rho"]
    )

    internal_ratios = sorted(
        {2.0 * ratio / math.sqrt(3.0) for ratio in args.ratios}
    )
    internal_domain_results = [
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
        for ratio in internal_ratios
    ]
    require(
        "all sampled nonzero internal trajectories admitted",
        all(
            result["admitted_controlled_exchange_trajectory"]
            for result in internal_domain_results
        ),
    )

    cubic = CubicEvaluator(cubic_summary)
    quartic = QuarticEvaluator(quartic_summary)
    case_results: list[dict[str, Any]] = []
    permutation_errors: list[float] = []
    mode_results: list[dict[str, Any]] = []
    for ratio in sorted(set(args.ratios)):
        q = ratio * row["H"]
        channel_q = 2.0 * q / math.sqrt(3.0)
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
            result = assemble_case(
                cubic,
                quartic,
                symbolic,
                params,
                background,
                modes,
                ratio,
                q,
                channel_q,
                left_index,
                right_index,
                args.K_Q,
                args.gamma,
                args.M_star_sq,
            )
            swapped = assemble_case(
                cubic,
                quartic,
                symbolic,
                params,
                background,
                modes,
                ratio,
                q,
                channel_q,
                left_index,
                right_index,
                args.K_Q,
                args.gamma,
                args.M_star_sq,
                swap_species=True,
            )
            permutation_error = relative_error(
                complex(
                    result["exchange_plus_reduced_contact"]["real"],
                    result["exchange_plus_reduced_contact"]["imag"],
                ),
                complex(
                    swapped["exchange_plus_reduced_contact"]["real"],
                    swapped["exchange_plus_reduced_contact"]["imag"],
                ),
            )
            result["species_permutation_relative_error"] = permutation_error
            result["contribution_permutation_relative_errors"] = {
                key: relative_error(
                    complex(result[key]["real"], result[key]["imag"]),
                    complex(swapped[key]["real"], swapped[key]["imag"]),
                )
                for key in (
                    "analytic_quartic_contact",
                    "constraint_schur_sum",
                    "reduced_quartic_contact",
                    "physical_exchange_sum",
                    "exchange_plus_reduced_contact",
                )
            }
            permutation_errors.append(permutation_error)
            case_results.append(result)

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
    maximum_frequency_closure = max(
        case["external_frequency_closure_over_H"]
        for case in case_results
    )
    maximum_source_swap = max(
        case["maximum_pair_source_swap_relative_error"]
        for case in case_results
    )
    maximum_species_permutation = max(permutation_errors)
    maximum_contribution_permutation = max(
        error
        for case in case_results
        for error in case["contribution_permutation_relative_errors"].values()
    )
    maximum_inverse_closure = max(
        channel["inverse_closure_relative_error"]
        for case in case_results
        for channel in case["channels"]
    )
    minimum_pole_separation = min(
        channel["distance_to_nearest_local_pole"]
        for case in case_results
        for channel in case["channels"]
    )
    maximum_imaginary_fraction = max(
        case["total_imaginary_fraction"] for case in case_results
    )
    cancellation_ratios = [
        case["cancellation_ratio"] for case in case_results
    ]
    combined_values = [
        case["exchange_plus_reduced_contact"]["real"]
        for case in case_results
    ]
    minimum_cancellation_ratio = min(cancellation_ratios)
    maximum_cancellation_ratio = max(cancellation_ratios)
    all_finite = all(
        math.isfinite(case["exchange_plus_reduced_contact"]["abs"])
        and all(
            math.isfinite(channel["inverse_kernel_condition_number"])
            for channel in case["channels"]
        )
        for case in case_results
    )
    all_nonzero = all(
        case["exchange_plus_reduced_contact"]["abs"] > 1.0e-12
        for case in case_results
    )
    passed = (
        maximum_mode_residual < 1.0e-12
        and maximum_residue_error < 1.0e-12
        and maximum_frequency_closure < 1.0e-12
        and maximum_source_swap < 1.0e-10
        and maximum_species_permutation < 1.0e-9
        and maximum_inverse_closure < 1.0e-9
        and minimum_pole_separation > 1.0e-4
        and maximum_imaginary_fraction < 1.0e-9
        and all_finite
        and maximum_contribution_permutation < 1.0e-9
        and all_nonzero
    )
    require("local four-leg kernel audit", passed)

    summary = {
        "gate": "UVIR-003",
        "stage": "B_LOCAL_FOUR_LEG_KERNEL",
        "calculation_status": "PASS",
        "subgate_status": (
            "PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL"
        ),
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "physical_2_to_2_status": (
            "LOCAL_FROZEN_KERNEL_DERIVED_S_MATRIX_NOT_ESTABLISHED"
        ),
        "parameter_scope": (
            "Representative dimensionless branch at its initial frozen-time "
            "snapshot. K_Q=gamma=M_star_sq=1 remains a diagnostic force-mode "
            "normalization."
        ),
        "kinematics": {
            "spatial_geometry": (
                "Four equal-magnitude momenta at regular-tetrahedron vertices; "
                "sum k_i=0 and every pair dot product is -q^2/3."
            ),
            "all_incoming_frequency_assignment": "(a+,b+,a-,b-)",
            "channel_momentum": "q_K=2q/sqrt(3)>0 for s,t,u",
            "external_mode_labels": (
                "Local coupled positive-frequency pairs ordered by frequency; "
                "no infrared Xi-pure identity is assigned."
            ),
            "normalization": (
                "v_dagger(2 omega K+i(P-P^T))v=1"
            ),
            "polarization_convention": (
                "d^3 L3 and d^4 L4 coefficients at zero leg amplitudes"
            ),
        },
        "internal_exchange_domain_results": internal_domain_results,
        "mode_results": mode_results,
        "case_results": case_results,
        "diagnostics": {
            "case_count": len(case_results),
            "channel_contraction_count": 3 * len(case_results),
            "maximum_on_shell_kernel_residual": maximum_mode_residual,
            "maximum_residue_normalization_error": maximum_residue_error,
            "maximum_external_frequency_closure_over_H": (
                maximum_frequency_closure
            ),
            "maximum_pair_source_swap_relative_error": maximum_source_swap,
            "maximum_species_permutation_relative_error": (
                maximum_species_permutation
            ),
            "maximum_inverse_closure_relative_error": maximum_inverse_closure,
            "minimum_distance_to_nearest_local_pole": minimum_pole_separation,
            "maximum_total_imaginary_fraction": maximum_imaginary_fraction,
            "all_internal_trajectories_admitted": True,
            "maximum_component_permutation_relative_error": (
                maximum_contribution_permutation
            ),
            "minimum_cancellation_ratio": minimum_cancellation_ratio,
            "maximum_cancellation_ratio": maximum_cancellation_ratio,
            "combined_kernel_real_range": [
                min(combined_values), max(combined_values)
            ],
            "all_combined_kernels_finite": all_finite,
            "all_combined_kernels_nonzero": all_nonzero,
        },
        "result": (
            "For 24 elastic coupled-mode cases, all three strictly nonzero "
            "tetrahedral channels independently pass the controlled-domain "
            "criteria. Matched cubic sources are contracted through the full "
            "physical propagator and combined with the analytic quartic "
            "contact and all three constraint-Schur pairings. The resulting "
            "local frozen-time on-shell four-leg kernels are finite, real "
            "within numerical tolerance, nonzero, and permutation consistent. "
            "The combined result is substantially smaller than the sum of "
            "absolute component magnitudes in parts of this slice, so its "
            "cancellation sensitivity must be retained in later interpretation."
        ),
        "scientific_boundary": (
            "This closes the declared local analytic four-leg kernel "
            "assembly only. It does not establish asymptotic cosmological "
            "in/out states, an S-matrix normalization, an optical-theorem "
            "unitarity bound, a strong-coupling scale, or a physical EFT "
            "cutoff. The exact nonanalytic |grad(pi)|^3 interaction remains "
            "held for a declared nonzero-gradient background."
        ),
        "next_required_calculation": [
            "define an adiabatic wave-packet or in-in observable normalization rather than assuming a cosmological S-matrix",
            "extend the local kernel away from the regular-tetrahedral slice and audit channel poles",
            "derive the nonzero-gradient exact-|grad(pi)|^3 interaction contribution",
            "only then formulate and test a declared perturbative-unitarity or EFT-validity criterion",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (
        args.output_dir / "uvir003_local_four_leg_kernel_summary.json"
    ).open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    write_csv(
        args.output_dir / "uvir003_local_four_leg_kernel.csv",
        case_results,
    )

    print("Nonzero tetrahedral internal trajectories: ADMITTED")
    print("Matched physical exchange contractions: ASSEMBLED")
    print("Reduced quartic contact including constraint Schur: ASSEMBLED")
    print("Local frozen-time on-shell four-leg kernel: VERIFIED")
    print("Cosmological S-matrix amplitude: NOT_ESTABLISHED")
    print("Physical cutoff: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print(
        "STATUS: PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL"
    )


if __name__ == "__main__":
    main()
