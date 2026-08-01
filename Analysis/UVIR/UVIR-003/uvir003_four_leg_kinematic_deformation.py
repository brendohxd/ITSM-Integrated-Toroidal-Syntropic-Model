#!/usr/bin/env python3
"""UVIR-003 alpha.10 substep: four-leg kernel off the regular tetrahedron.

Equal-magnitude external spatial momenta with sum k_i = 0 are deformed as an
isosceles disphenoid. Opposite-edge pair dots are

    alpha = beta = -q^2/3 + delta,
    gamma = -q^2/3 - 2 delta,

so alpha + beta + gamma = -q^2 (required by |sum k_i|^2 = 0). The regular
tetrahedron is delta = 0. Channel momenta become

    q_s = sqrt(2 q^2 + 2 alpha),
    q_t = sqrt(2 q^2 + 2 beta),
    q_u = sqrt(2 q^2 + 2 gamma),

and are no longer forced equal. As delta approaches the homogeneous edge
gamma -> -q^2, one channel momentum approaches zero.

This audit records domain admission, pole distance, and kernel finiteness on a
small deformation grid. It is not a cosmological S-matrix, unitarity bound, or
physical cutoff.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from uvir003_controlled_exchange_domain import audit_ratio
from uvir003_local_four_leg_kernel import (
    PARTITIONS,
    QuarticEvaluator,
    complex_scalar,
    constraint_inverse,
    full_mode_leg,
    physical_pair_source,
    relative_error,
    require,
)
from uvir003_mode_projected_cubic_pair_source import (
    CubicEvaluator,
    background_values,
    normalized_modes,
    set_leg,
)
from uvir003_physical_quadratic_propagators import (
    add_force_block,
    evaluate_physical_matrices,
    inverse_kernel,
    quadratic_poles,
    symbolic_propagators,
)
from uvir003_scalar_adm_finite_q import background_parameters, load_inputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
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
        default=[50.0, 75.0],
        help="External q/H samples (must be domain-admitted).",
    )
    parser.add_argument(
        "--deltas",
        type=float,
        nargs="+",
        default=[0.0, 0.05, 0.10, 0.15, 0.20],
        help="Disphenoid deformation in units of q^2 (delta/q^2 values).",
    )
    parser.add_argument(
        "--mode-pairs",
        type=str,
        default="0,0;0,1;1,1",
        help="Semicolon-separated left,right mode index pairs (0..2).",
    )
    parser.add_argument("--alignment", type=float, default=1.0)
    parser.add_argument("--K-Q", type=float, default=1.0)
    parser.add_argument("--gamma", type=float, default=1.0)
    parser.add_argument("--M-star-sq", type=float, default=1.0)
    parser.add_argument("--adiabatic-threshold", type=float, default=0.1)
    parser.add_argument("--subhorizon-margin", type=float, default=10.0)
    parser.add_argument(
        "--homogeneous-fraction-threshold",
        type=float,
        default=0.15,
        help="Flag channel as near-homogeneous if q_K/q below this.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_mode_pairs(spec: str) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for chunk in spec.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        left_s, right_s = chunk.split(",")
        pairs.append((int(left_s), int(right_s)))
    return pairs


def disphenoid_dots(q: float, delta_over_q2: float) -> dict[str, float]:
    """Return opposite-edge pair dots and channel momenta."""
    q2 = q * q
    delta = delta_over_q2 * q2
    alpha = -q2 / 3.0 + delta
    beta = -q2 / 3.0 + delta
    gamma = -q2 / 3.0 - 2.0 * delta
    # Reality: |pair sum|^2 = 2q^2 + 2*dot > 0  =>  dot > -q^2
    # Also |k_i - k_j| style: typically |dot| < q^2 for non-collinear.
    require("alpha > -q^2", alpha > -q2 + 1.0e-14)
    require("beta > -q^2", beta > -q2 + 1.0e-14)
    require("gamma > -q^2", gamma > -q2 + 1.0e-14)
    require("alpha < q^2", alpha < q2 - 1.0e-14)
    require("beta < q^2", beta < q2 - 1.0e-14)
    require("gamma < q^2", gamma < q2 - 1.0e-14)
    require("dot sum identity", abs(alpha + beta + gamma + q2) < 1.0e-12 * max(q2, 1.0))
    q_s = math.sqrt(max(2.0 * q2 + 2.0 * alpha, 0.0))
    q_t = math.sqrt(max(2.0 * q2 + 2.0 * beta, 0.0))
    q_u = math.sqrt(max(2.0 * q2 + 2.0 * gamma, 0.0))
    return {
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "q_s": q_s,
        "q_t": q_t,
        "q_u": q_u,
        "delta_over_q2": delta_over_q2,
    }


def contact_values_disphenoid(
    background: dict[str, complex | float],
    q: float,
    legs: list[tuple[np.ndarray, float]],
    dots: dict[str, float],
) -> dict[str, complex | float]:
    """Assign opposite-edge dots for s=(12|34), t=(13|24), u=(14|23)."""
    values = dict(background)
    for index, leg in enumerate(legs, start=1):
        values[f"q_{index}"] = q
        set_leg(values, index, leg[0], leg[1])
    alpha = dots["alpha"]
    beta = dots["beta"]
    gamma = dots["gamma"]
    # opposite edges share the same dot
    pair_dots = {
        (1, 2): alpha,
        (3, 4): alpha,
        (1, 3): beta,
        (2, 4): beta,
        (1, 4): gamma,
        (2, 3): gamma,
    }
    for first, second in pair_dots:
        values[f"k{first}_dot_k{second}"] = pair_dots[(first, second)]
    return values


def assemble_deformed_case(
    cubic: CubicEvaluator,
    quartic: QuarticEvaluator,
    symbolic: dict[str, object],
    params: dict[str, float],
    background: dict[str, complex | float],
    modes: list[dict[str, Any]],
    ratio: float,
    q: float,
    left_index: int,
    right_index: int,
    dots: dict[str, float],
    k_q: float,
    gamma: float,
    mstar2: float,
    domain_by_ratio: dict[float, dict[str, Any]],
    homogeneous_fraction_threshold: float,
) -> dict[str, Any]:
    mode_a = modes[left_index]
    mode_b = modes[right_index]
    legs = [
        full_mode_leg(mode_a, 1),
        full_mode_leg(mode_b, 1),
        full_mode_leg(mode_a, -1),
        full_mode_leg(mode_b, -1),
    ]
    frequency_closure = abs(sum(leg[1] for leg in legs))
    contact = quartic.contact(
        contact_values_disphenoid(background, q, legs, dots)
    )

    channel_q_map = {
        "s": dots["q_s"],
        "t": dots["q_t"],
        "u": dots["q_u"],
    }

    exchange_sum = 0j
    schur_sum = 0j
    channel_results: list[dict[str, Any]] = []
    maximum_source_swap_error = 0.0
    min_pole_separation = float("inf")
    all_channels_admitted = True

    for first_pair, second_pair, name in PARTITIONS:
        channel_q = channel_q_map[name]
        first_legs = (legs[first_pair[0]], legs[first_pair[1]])
        second_legs = (legs[second_pair[0]], legs[second_pair[1]])

        channel_ratio = channel_q / background["H"]
        if channel_ratio in domain_by_ratio:
            domain_hit = domain_by_ratio[channel_ratio]
            admitted = bool(domain_hit["admitted_controlled_exchange_trajectory"])
        else:
            nearest = min(
                domain_by_ratio.keys(), key=lambda r: abs(r - channel_ratio)
            )
            domain_hit = domain_by_ratio[nearest]
            admitted = False
            all_channels_admitted = False

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

        left_source, left_frequency = physical_pair_source(
            cubic, background, q, channel_q, *first_legs
        )
        right_source, right_frequency = physical_pair_source(
            cubic, background, q, channel_q, *second_legs
        )
        require(
            f"{name}-channel frequency closure",
            abs(left_frequency + right_frequency) < 1.0e-10,
        )

        swapped_source, swapped_frequency = physical_pair_source(
            cubic, background, q, channel_q, first_legs[1], first_legs[0]
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
        exchange = -complex(right_source.T @ propagator @ left_source)
        exchange_sum += exchange

        left_constraint = quartic.constraint_source(
            background, q, channel_q, *first_legs
        )
        right_constraint = quartic.constraint_source(
            background, q, channel_q, *second_legs
        )
        schur = -complex(right_constraint.T @ c_inverse @ left_constraint)
        schur_sum += schur

        pole_separation = float(
            np.min(np.abs(channel_poles - left_frequency))
            / max(abs(left_frequency), background["H"])
        )
        min_pole_separation = min(min_pole_separation, pole_separation)

        near_homogeneous = (channel_q / q) < homogeneous_fraction_threshold
        channel_results.append(
            {
                "channel": name,
                "pair_partition": [
                    [index + 1 for index in first_pair],
                    [index + 1 for index in second_pair],
                ],
                "q_channel": channel_q,
                "q_channel_over_H": channel_q / background["H"],
                "q_channel_over_q": channel_q / q,
                "domain_admitted_at_exact_ratio": admitted,
                "near_homogeneous_flag": near_homogeneous,
                "internal_frequency_over_H": left_frequency / background["H"],
                "frequency_closure_error": abs(left_frequency + right_frequency)
                / background["H"],
                "physical_exchange": complex_scalar(exchange),
                "constraint_schur": complex_scalar(schur),
                "source_swap_relative_error": source_swap_error,
                "inverse_kernel_condition_number": float(np.linalg.cond(kernel)),
                "inverse_closure_relative_error": inverse_closure,
                "distance_to_nearest_local_pole": pole_separation,
            }
        )
        if not admitted:
            all_channels_admitted = False

    reduced_contact = contact + schur_sum
    total = reduced_contact + exchange_sum
    scale = max(
        abs(contact)
        + sum(
            item["constraint_schur"]["abs"] + item["physical_exchange"]["abs"]
            for item in channel_results
        ),
        1.0e-30,
    )
    return {
        "initial_q_over_H": ratio,
        "delta_over_q2": dots["delta_over_q2"],
        "left_mode": mode_a["label"],
        "right_mode": mode_b["label"],
        "kinematics": "isosceles_disphenoid_all_incoming_elastic",
        "dots": {
            "alpha_over_q2": dots["alpha"] / (q * q),
            "beta_over_q2": dots["beta"] / (q * q),
            "gamma_over_q2": dots["gamma"] / (q * q),
        },
        "channel_q_over_q": {
            "s": dots["q_s"] / q,
            "t": dots["q_t"] / q,
            "u": dots["q_u"] / q,
        },
        "external_frequency_closure_over_H": frequency_closure / background["H"],
        "analytic_quartic_contact": complex_scalar(contact),
        "constraint_schur_sum": complex_scalar(schur_sum),
        "reduced_quartic_contact": complex_scalar(reduced_contact),
        "physical_exchange_sum": complex_scalar(exchange_sum),
        "exchange_plus_reduced_contact": complex_scalar(total),
        "total_imaginary_fraction": float(abs(total.imag) / scale),
        "cancellation_ratio": float(abs(total) / scale),
        "maximum_pair_source_swap_relative_error": maximum_source_swap_error,
        "minimum_distance_to_nearest_local_pole": min_pole_separation,
        "all_channels_domain_admitted_exact": all_channels_admitted,
        "channels": channel_results,
    }


def fourth_potential_derivative(params: dict[str, float], rho: float) -> float:
    return (
        3.0 * params["lambda4"]
        + 15.0 * params["lambda6"] * rho**2 / params["Lambda"] ** 2
    )


def write_csv(path: Path, cases: list[dict[str, Any]]) -> None:
    fields = [
        "initial_q_over_H",
        "delta_over_q2",
        "left_mode",
        "right_mode",
        "q_s_over_q",
        "q_t_over_q",
        "q_u_over_q",
        "combined_kernel_real",
        "combined_kernel_abs",
        "cancellation_ratio",
        "total_imaginary_fraction",
        "minimum_pole_separation",
        "all_channels_domain_admitted_exact",
        "near_homogeneous_any",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for case in cases:
            writer.writerow(
                {
                    "initial_q_over_H": case["initial_q_over_H"],
                    "delta_over_q2": case["delta_over_q2"],
                    "left_mode": case["left_mode"],
                    "right_mode": case["right_mode"],
                    "q_s_over_q": case["channel_q_over_q"]["s"],
                    "q_t_over_q": case["channel_q_over_q"]["t"],
                    "q_u_over_q": case["channel_q_over_q"]["u"],
                    "combined_kernel_real": case["exchange_plus_reduced_contact"][
                        "real"
                    ],
                    "combined_kernel_abs": case["exchange_plus_reduced_contact"][
                        "abs"
                    ],
                    "cancellation_ratio": case["cancellation_ratio"],
                    "total_imaginary_fraction": case["total_imaginary_fraction"],
                    "minimum_pole_separation": case[
                        "minimum_distance_to_nearest_local_pole"
                    ],
                    "all_channels_domain_admitted_exact": case[
                        "all_channels_domain_admitted_exact"
                    ],
                    "near_homogeneous_any": any(
                        ch["near_homogeneous_flag"] for ch in case["channels"]
                    ),
                }
            )


def main() -> None:
    args = parse_args()
    mode_pairs = parse_mode_pairs(args.mode_pairs)
    require("positive ratios", all(v > 0 for v in args.ratios))
    require("mode pairs present", len(mode_pairs) > 0)

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
        float(v)
        for v in domain_summary["sampled_domain"][
            "admitted_initial_q_over_H_values"
        ]
    )
    require(
        "requested external ratios admitted",
        all(float(v) in admitted_external for v in args.ratios),
    )

    frw, rows = load_inputs(args.frw_summary, args.frw_trajectory)
    params = background_parameters(frw, args.alignment)
    params["zeta_align"] = args.alignment
    symbolic = symbolic_propagators()
    row = rows[0]
    background = background_values(
        params, row, args.gamma, args.K_Q, args.M_star_sq
    )
    background["V_rhorhorhorho"] = fourth_potential_derivative(
        params, row["rho"]
    )

    # Precompute domain audits for all channel ratios that appear
    channel_ratios: set[float] = set()
    kinematics_table: list[dict[str, Any]] = []
    for ratio in args.ratios:
        q = ratio * row["H"]
        for d in args.deltas:
            dots = disphenoid_dots(q, d)
            kinematics_table.append(
                {
                    "initial_q_over_H": ratio,
                    "delta_over_q2": d,
                    "q_s_over_H": dots["q_s"] / row["H"],
                    "q_t_over_H": dots["q_t"] / row["H"],
                    "q_u_over_H": dots["q_u"] / row["H"],
                    "q_s_over_q": dots["q_s"] / q,
                    "q_t_over_q": dots["q_t"] / q,
                    "q_u_over_q": dots["q_u"] / q,
                }
            )
            for key in ("q_s", "q_t", "q_u"):
                channel_ratios.add(dots[key] / row["H"])

    domain_by_ratio: dict[float, dict[str, Any]] = {}
    for ch_ratio in sorted(channel_ratios):
        domain_by_ratio[ch_ratio] = audit_ratio(
            symbolic,
            params,
            rows,
            ch_ratio,
            args.K_Q,
            args.gamma,
            args.M_star_sq,
            args.adiabatic_threshold,
            args.subhorizon_margin,
        )

    cubic = CubicEvaluator(cubic_summary)
    quartic = QuarticEvaluator(quartic_summary)
    case_results: list[dict[str, Any]] = []
    tetra_reference: dict[tuple[float, int, int], complex] = {}

    for ratio in sorted(set(args.ratios)):
        q = ratio * row["H"]
        state = np.asarray(
            [row["H"], row["rho"], row["rho_dot"], row["mu"], q],
            dtype=float,
        )
        matrices = evaluate_physical_matrices(symbolic, params, state)
        modes = normalized_modes(*matrices, row["H"])
        for left_index, right_index in mode_pairs:
            for d in args.deltas:
                dots = disphenoid_dots(q, d)
                result = assemble_deformed_case(
                    cubic,
                    quartic,
                    symbolic,
                    params,
                    background,
                    modes,
                    ratio,
                    q,
                    left_index,
                    right_index,
                    dots,
                    args.K_Q,
                    args.gamma,
                    args.M_star_sq,
                    domain_by_ratio,
                    args.homogeneous_fraction_threshold,
                )
                case_results.append(result)
                if abs(d) < 1.0e-15:
                    tetra_reference[(ratio, left_index, right_index)] = complex(
                        result["exchange_plus_reduced_contact"]["real"],
                        result["exchange_plus_reduced_contact"]["imag"],
                    )

    # Tetra limit vs baseline file if present
    baseline_path = (
        args.output_dir / "uvir003_local_four_leg_kernel_summary.json"
    )
    tetra_match_errors: list[float] = []
    if baseline_path.exists():
        baseline = load_json(baseline_path)
        for case in baseline.get("case_results", []):
            if case.get("kinematics") != (
                "regular_tetrahedral_all_incoming_elastic"
            ):
                continue
            key_ratio = float(case["initial_q_over_H"])
            # map labels to indices via mode order
            # compare absolute values for matching left/right labels at d=0
            for deformed in case_results:
                if deformed["delta_over_q2"] != 0.0:
                    continue
                if deformed["initial_q_over_H"] != key_ratio:
                    continue
                if (
                    deformed["left_mode"] == case["left_mode"]
                    and deformed["right_mode"] == case["right_mode"]
                ):
                    err = relative_error(
                        complex(
                            deformed["exchange_plus_reduced_contact"]["real"],
                            deformed["exchange_plus_reduced_contact"]["imag"],
                        ),
                        complex(
                            case["exchange_plus_reduced_contact"]["real"],
                            case["exchange_plus_reduced_contact"]["imag"],
                        ),
                    )
                    tetra_match_errors.append(err)

    finite = all(
        math.isfinite(c["exchange_plus_reduced_contact"]["abs"])
        for c in case_results
    )
    nonzero = all(
        c["exchange_plus_reduced_contact"]["abs"] > 1.0e-12 for c in case_results
    )
    imag_ok = all(c["total_imaginary_fraction"] < 1.0e-8 for c in case_results)
    pole_ok = all(
        c["minimum_distance_to_nearest_local_pole"] > 1.0e-6 for c in case_results
    )
    swap_ok = all(
        c["maximum_pair_source_swap_relative_error"] < 1.0e-9 for c in case_results
    )
    tetra_ok = (not tetra_match_errors) or (
        max(tetra_match_errors) < 1.0e-8
    )
    # Domain admission may fail near homogeneous — record, do not hard-fail whole gate
    domain_failures = [
        c
        for c in case_results
        if not c["all_channels_domain_admitted_exact"]
    ]
    near_homog = [
        c
        for c in case_results
        if any(ch["near_homogeneous_flag"] for ch in c["channels"])
    ]

    core_pass = finite and nonzero and imag_ok and pole_ok and swap_ok and tetra_ok
    status = (
        "PASS_FOUR_LEG_KINEMATIC_DEFORMATION_AUDIT"
        if core_pass
        else "FAIL_FOUR_LEG_KINEMATIC_DEFORMATION_AUDIT"
    )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_FOUR_LEG_KINEMATIC_DEFORMATION",
        "calculation_status": "PASS" if core_pass else "FAIL",
        "subgate_status": status,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "physical_2_to_2_status": (
            "LOCAL_DEFORMED_KERNEL_AUDITED_S_MATRIX_NOT_ESTABLISHED"
        ),
        "kinematics": {
            "family": "isosceles_disphenoid",
            "tetrahedron_limit": "delta_over_q2 = 0 => q_s=q_t=q_u=2/sqrt(3) q",
            "dot_sum_identity": "alpha+beta+gamma = -q^2",
            "homogeneous_approach": "gamma -> -q^2 when delta_over_q2 -> 1/3",
            "sampled_deltas_over_q2": list(args.deltas),
            "sampled_external_q_over_H": list(args.ratios),
            "mode_pairs": [list(p) for p in mode_pairs],
        },
        "kinematics_table": kinematics_table,
        "internal_domain_results": [
            {
                "q_over_H": r,
                "admitted": domain_by_ratio[r][
                    "admitted_controlled_exchange_trajectory"
                ],
            }
            for r in sorted(domain_by_ratio)
        ],
        "case_results": case_results,
        "diagnostics": {
            "case_count": len(case_results),
            "all_combined_kernels_finite": finite,
            "all_combined_kernels_nonzero": nonzero,
            "maximum_total_imaginary_fraction": max(
                c["total_imaginary_fraction"] for c in case_results
            ),
            "minimum_pole_separation_over_all_cases": min(
                c["minimum_distance_to_nearest_local_pole"] for c in case_results
            ),
            "maximum_source_swap_error": max(
                c["maximum_pair_source_swap_relative_error"] for c in case_results
            ),
            "tetra_baseline_match_errors": tetra_match_errors,
            "maximum_tetra_baseline_match_error": (
                max(tetra_match_errors) if tetra_match_errors else None
            ),
            "domain_failure_case_count": len(domain_failures),
            "near_homogeneous_case_count": len(near_homog),
            "cancellation_ratio_range": [
                min(c["cancellation_ratio"] for c in case_results),
                max(c["cancellation_ratio"] for c in case_results),
            ],
        },
        "scientific_boundary": (
            "Off-tetrahedron local kernel audit only. Not an S-matrix, "
            "unitarity bound, strong-coupling scale, or physical cutoff. "
            "Domain admission at exact deformed channel ratios is reported "
            "separately and may fail as homogeneous channels are approached."
        ),
        "next_required_calculation": [
            "tighten pole/homogeneous approach with denser delta scan if needed",
            "define adiabatic wave-packet or in-in observable normalization",
            "derive nonzero-gradient |grad(pi)|^3 contribution",
            "only then formulate declared unitarity / EFT-validity criterion",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_json = args.output_dir / "uvir003_four_leg_kinematic_deformation_summary.json"
    out_csv = args.output_dir / "uvir003_four_leg_kinematic_deformation.csv"
    with out_json.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    write_csv(out_csv, case_results)

    print(f"Cases: {len(case_results)}")
    print(
        "Tetra baseline match max error:",
        summary["diagnostics"]["maximum_tetra_baseline_match_error"],
    )
    print(
        "Domain failure cases:",
        summary["diagnostics"]["domain_failure_case_count"],
    )
    print(
        "Near-homogeneous cases:",
        summary["diagnostics"]["near_homogeneous_case_count"],
    )
    print(f"Min pole separation: {summary['diagnostics']['minimum_pole_separation_over_all_cases']}")
    print("Cosmological S-matrix amplitude: NOT_ESTABLISHED")
    print("Physical cutoff: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print(f"STATUS: {status}")
    if not core_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
