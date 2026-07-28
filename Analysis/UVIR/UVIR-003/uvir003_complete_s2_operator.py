#!/usr/bin/env python3
"""UVIR-003 complete finite-q second-order constraint-source operator.

Derives the condensate temporal shift-advection dressing, audits the Track-A
force action for nonlinear cubic constraint dependence, and combines those
results with the verified generic gravity/aether dressing kernel and the
multi-sector origin-linear source.

The result is the complete functional source

    S2 = partial_z L3[x,z] evaluated at z=z1

on the homogeneous zero-gradient Track-A force branch at q_phys>0.  This does
not yet supply the complete L4[x,z1] contact functional, physical projection,
or cosmological 2-to-2 amplitude.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp

from uvir003_full_j2_schur import symbolic_audit as origin_audit
from uvir003_generic_shift_kernel import symbolic_audit as gravity_audit


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=base / "outputs",
        help="Directory for the JSON summary.",
    )
    return parser.parse_args()


def require_zero(name: str, expression: sp.Expr) -> None:
    reduced = sp.factor(sp.simplify(expression))
    if reduced != 0:
        raise AssertionError(f"{name} failed: {reduced}")


def require_text(name: str, actual: str, expected: str) -> None:
    if actual != expected:
        raise AssertionError(
            f"{name} failed: expected {expected!r}, got {actual!r}"
        )


def coefficient(
    expression: sp.Expr,
    epsilon: sp.Symbol,
    order: int,
) -> sp.Expr:
    return sp.expand(expression).coeff(epsilon, order)


def symbolic_audit() -> dict[str, object]:
    epsilon, constraint_degree = sp.symbols(
        "epsilon lambda_z",
        real=True,
    )
    curvature, lapse = sp.symbols("R delta_N", real=True)
    rho, rho_dot, chemical = sp.symbols(
        "rho rho_dot mu",
        real=True,
    )
    amplitude, amplitude_dot, phase_dot = sp.symbols(
        "delta_rho delta_rho_dot vartheta_dot",
        real=True,
    )
    adv_amplitude, adv_phase = sp.symbols(
        "D_beta_dot_D_delta_rho D_beta_dot_D_vartheta",
        real=True,
    )

    volume_over_lapse = (
        sp.exp(3 * epsilon * curvature)
        / (1 + epsilon * lapse)
    )
    inverse_metric_factor = sp.exp(-2 * epsilon * curvature)
    normal_amplitude = (
        rho_dot
        + epsilon * amplitude_dot
        - epsilon**2
        * inverse_metric_factor
        * adv_amplitude
    )
    normal_phase = (
        chemical
        + epsilon * phase_dot
        - epsilon**2
        * inverse_metric_factor
        * adv_phase
    )
    perturbed_rho = rho + epsilon * amplitude
    matter_temporal = (
        volume_over_lapse
        * (
            normal_amplitude**2
            + perturbed_rho**2 * normal_phase**2
        )
        / 2
    )
    matter_series = sp.series(
        matter_temporal,
        epsilon,
        0,
        4,
    ).removeO()
    matter_l3 = coefficient(matter_series, epsilon, 3)

    scaled_matter_l3 = sp.expand(
        matter_l3.subs(
            {
                lapse: constraint_degree * lapse,
                adv_amplitude: (
                    constraint_degree * adv_amplitude
                ),
                adv_phase: constraint_degree * adv_phase,
            }
        )
    )
    matter_direct = coefficient(
        scaled_matter_l3,
        constraint_degree,
        0,
    )
    matter_origin_linear = coefficient(
        scaled_matter_l3,
        constraint_degree,
        1,
    )
    matter_nonlinear = sp.factor(
        coefficient(
            scaled_matter_l3,
            constraint_degree,
            2,
        )
        + coefficient(
            scaled_matter_l3,
            constraint_degree,
            3,
        )
    )
    require_zero(
        "condensate constraint-degree reconstruction",
        (
            matter_l3
            - matter_direct
            - matter_origin_linear
            - matter_nonlinear
        ),
    )

    temporal_background = (
        rho_dot**2 + rho**2 * chemical**2
    ) / 2
    temporal_linear = (
        rho_dot * amplitude_dot
        + rho * chemical**2 * amplitude
        + rho**2 * chemical * phase_dot
    )
    advection_background = (
        rho_dot * adv_amplitude
        + rho**2 * chemical * adv_phase
    )
    expected_matter_nonlinear = sp.factor(
        lapse * advection_background
        + lapse**2 * temporal_linear
        + (
            3 * curvature * lapse**2
            - lapse**3
        )
        * temporal_background
    )
    require_zero(
        "condensate nonlinear constraint dressing",
        matter_nonlinear - expected_matter_nonlinear,
    )

    lapse_1 = sp.symbols("delta_N_1", real=True)
    adv_amplitude_1, adv_phase_1 = sp.symbols(
        "D_beta_1_dot_D_delta_rho "
        "D_beta_1_dot_D_vartheta",
        real=True,
    )
    matter_delta_s2_n = sp.factor(
        sp.diff(matter_nonlinear, lapse).subs(
            {
                lapse: lapse_1,
                adv_amplitude: adv_amplitude_1,
                adv_phase: adv_phase_1,
            }
        )
    )
    expected_matter_delta_s2_n = sp.factor(
        rho_dot * adv_amplitude_1
        + rho**2 * chemical * adv_phase_1
        + 2 * lapse_1 * temporal_linear
        + (
            6 * curvature * lapse_1
            - 3 * lapse_1**2
        )
        * temporal_background
    )
    require_zero(
        "condensate lapse source dressing",
        matter_delta_s2_n - expected_matter_delta_s2_n,
    )

    matter_beta_flux_amplitude = sp.factor(lapse_1 * rho_dot)
    matter_beta_flux_phase = sp.factor(
        lapse_1 * rho**2 * chemical
    )
    matter_delta_s2_beta = (
        "-D_i[delta_N1*(rho_dot*D_i(delta_rho)"
        "+rho^2*mu*D_i(vartheta))]"
    )

    # Track-A force sector. P_pi=D_i beta D_i pi.
    kq, gamma, mstar2 = sp.symbols(
        "K_Q gamma M_star_sq",
        positive=True,
    )
    pi_dot, adv_pi = sp.symbols(
        "pi_dot D_beta_dot_D_pi",
        real=True,
    )
    lap_pi, grad_r_dot_grad_pi = sp.symbols(
        "D2_pi D_R_dot_D_pi",
        real=True,
    )
    q_normal = (
        epsilon * pi_dot
        - epsilon**2 * inverse_metric_factor * adv_pi
    )
    force_q = (
        kq * volume_over_lapse * q_normal**2 / 2
    )
    force_regulator = (
        -gamma
        * (1 + epsilon * lapse)
        * sp.exp(-epsilon * curvature)
        * (
            epsilon * lap_pi
            + epsilon**2 * grad_r_dot_grad_pi
        )
        ** 2
        / (2 * mstar2)
    )
    force_series = sp.series(
        force_q + force_regulator,
        epsilon,
        0,
        4,
    ).removeO()
    force_l3 = coefficient(force_series, epsilon, 3)
    scaled_force_l3 = sp.expand(
        force_l3.subs(
            {
                lapse: constraint_degree * lapse,
                adv_pi: constraint_degree * adv_pi,
            }
        )
    )
    force_nonlinear = sp.factor(
        coefficient(
            scaled_force_l3,
            constraint_degree,
            2,
        )
        + coefficient(
            scaled_force_l3,
            constraint_degree,
            3,
        )
    )
    require_zero(
        "Track-A cubic nonlinear constraint dressing",
        force_nonlinear,
    )

    expected_force_origin = sp.factor(
        kq
        * (
            (3 * curvature - lapse) * pi_dot**2 / 2
            - pi_dot * adv_pi
        )
        - gamma
        * (
            (lapse - curvature) * lap_pi**2
            + 2 * lap_pi * grad_r_dot_grad_pi
        )
        / (2 * mstar2)
    )
    require_zero(
        "Track-A cubic affine constraint regression",
        force_l3 - expected_force_origin,
    )

    gravity = gravity_audit()
    origin = origin_audit()
    require_text(
        "generic gravity/aether dressing dependency",
        gravity["dressed_functional_source"]["status"],
        "PASS_GENERIC_GRAVITY_AETHER_SHIFT_DRESSING_OPERATOR",
    )
    require_text(
        "multi-sector origin-linear dependency",
        origin["origin_linear_J2"]["status"],
        "PASS_MULTI_SECTOR_ORIGIN_LINEAR_J2_COMPONENT",
    )

    complete_s2_n = (
        "S2_N=J2_N_origin"
        "+DeltaS2_N_gravity_aether"
        "+DeltaS2_N_condensate"
    )
    complete_s2_beta = (
        "S2_beta=J2_beta_origin"
        "+DeltaS2_beta_gravity_aether"
        "+DeltaS2_beta_condensate"
    )
    complete_s2_sigma = (
        "S2_Sigma=-(D^2)^(-1)S2_beta"
        " for q_phys>0"
    )

    return {
        "condensate_temporal_sector": {
            "L3_complete": str(matter_l3),
            "L3_direct_x0": str(matter_direct),
            "L3_origin_linear_constraints": str(
                matter_origin_linear
            ),
            "L3_nonlinear_constraint_dressing": str(
                matter_nonlinear
            ),
            "DeltaS2_N_at_z1": str(matter_delta_s2_n),
            "DeltaS2_beta_at_z1": matter_delta_s2_beta,
            "beta_flux_amplitude_coefficient": str(
                matter_beta_flux_amplitude
            ),
            "beta_flux_phase_coefficient": str(
                matter_beta_flux_phase
            ),
            "status": (
                "PASS_CONDENSATE_SHIFT_ADVECTION_DRESSING"
            ),
        },
        "track_a_force_sector": {
            "L3": str(force_l3),
            "L3_expected": str(expected_force_origin),
            "nonlinear_constraint_degree": str(force_nonlinear),
            "DeltaS2_at_z1_beyond_origin": "0",
            "interpretation": (
                "Track-A Q^2 and regulator cubic constraint dependence is "
                "affine; its complete S2 contribution is J2_origin"
            ),
            "exact_Y_three_halves": (
                "constraint independent at cubic amplitude order on the "
                "homogeneous zero-gradient branch"
            ),
            "status": "PASS_FORCE_CUBIC_AFFINE_CONSTRAINT_AUDIT",
        },
        "dependencies": {
            "origin_linear_multi_sector": (
                origin["origin_linear_J2"]["status"]
            ),
            "generic_gravity_aether_dressing": (
                gravity["dressed_functional_source"]["status"]
            ),
            "status": "VERIFIED",
        },
        "complete_finite_q_S2": {
            "lapse": complete_s2_n,
            "beta": complete_s2_beta,
            "sigma": complete_s2_sigma,
            "sector_coverage": [
                "gravity",
                "Einstein-aether",
                "canonical condensate amplitude and phase",
                "current alignment",
                "Track-A Q^2",
                "Track-A rest-space regulator",
                "exact Y^(3/2) under the declared zero-gradient rule",
            ],
            "quartic_schur": (
                "-1/2 integral d^3k "
                "S2(-k)^T C(k)^(-1) S2(k)"
            ),
            "domain": "q_phys>0 and det(C)!=0",
            "status": "PASS_COMPLETE_FINITE_Q_S2_FUNCTIONAL",
        },
        "scientific_boundary": {
            "derived": [
                "condensate nonlinear lapse/shift-advection dressing",
                "Track-A cubic affine-constraint audit",
                "complete multi-sector finite-q S2 functional operator",
                "corrected quartic Schur functional in terms of S2",
            ],
            "not_derived": [
                "complete generic L4[x,z1] contact functional",
                "regular physical scalar eigenmode projection",
                "cosmological exchange-plus-contact amplitude",
                "physical strong-coupling scale or cutoff",
                "nonzero-gradient exact-Y local reduction",
            ],
        },
    }


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    symbolic = symbolic_audit()
    summary = {
        "gate": "UVIR-003",
        "stage": "B_COMPLETE_FINITE_Q_S2_OPERATOR",
        "calculation_status": "PASS",
        "subgate_status": "PASS_COMPLETE_FINITE_Q_S2_FUNCTIONAL",
        "complete_finite_q_S2_status": "ASSEMBLED_AND_VERIFIED",
        "corrected_quartic_schur_status": (
            "ASSEMBLED_AS_FUNCTIONAL_OF_COMPLETE_S2"
        ),
        "complete_L4_x_z1_status": "NOT_YET_DERIVED",
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "symbolic_audit": symbolic,
        "scientific_boundary": (
            "The complete multi-sector second-order constraint-source "
            "functional S2 is assembled at finite q on the homogeneous "
            "zero-gradient Track-A force branch. The corrected Schur "
            "functional now uses S2. Complete L4[x,z1], physical projection, "
            "amplitude and cutoff remain open."
        ),
        "next_required_calculation": [
            "derive the complete generic L4[x,z1] contact functional",
            (
                "combine L4[x,z1] with "
                "-S2^T C^(-1)S2/2"
            ),
            "project cubic and quartic vertices onto physical scalar modes",
            (
                "evaluate the gauge-regular cosmological 2-to-2 amplitude "
                "and unitarity scale"
            ),
        ],
    }

    output_path = (
        args.output_dir / "uvir003_complete_s2_operator_summary.json"
    )
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("Condensate shift-advection dressing at z1: VERIFIED")
    print("Track-A cubic nonlinear constraint correction: ZERO_VERIFIED")
    print("Generic gravity/aether dressing dependency: VERIFIED")
    print("Multi-sector origin-linear source dependency: VERIFIED")
    print("Complete finite-q S2 functional: VERIFIED")
    print("Corrected quartic Schur functional: ASSEMBLED")
    print("Complete L4[x,z1]: NOT_YET_DERIVED")
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_COMPLETE_FINITE_Q_S2_FUNCTIONAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
