#!/usr/bin/env python3
"""UVIR-003 Stage B: direct physical-field cubic/quartic contact block.

Expands the exact gravity+aether+condensate+alignment parent action and the
adopted Track-A force action with the lapse and scalar shift set to their
background values.  This derives the complete x-only direct contact component

    L3[x,0],  L4[x,0],

for x=(R,delta_rho,vartheta,pi).

This is a bounded component of the constrained cosmological interaction
problem.  The full reduced vertices require L3[x,z1] and L4[x,z1], with the
verified first-order constraint solution z1=-C^{-1}J1. The quartic
constraint term must use the dressed source S2=partial_z L3[x,z1], not only
the previously verified origin-linear J2 component.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


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
    reduced = sp.factor(sp.expand(expression))
    if reduced != 0:
        raise AssertionError(f"{name} failed: {reduced}")


def coefficient(
    expression: sp.Expr,
    epsilon: sp.Symbol,
    order: int,
) -> sp.Expr:
    return sp.expand(expression).coeff(epsilon, order)


def symbolic_audit() -> dict[str, object]:
    epsilon = sp.symbols("epsilon", real=True)
    mp2, mcos2 = sp.symbols("M_P_sq M_cos_sq", positive=True)
    hubble = sp.symbols("H", real=True)
    rho, rho_dot, chemical = sp.symbols(
        "rho rho_dot mu", real=True
    )
    v0, v1, v2, v3, v4 = sp.symbols(
        "V V_rho V_rhorho V_rhorhorho V_rhorhorhorho",
        real=True,
    )
    alignment = sp.symbols("zeta_align", nonnegative=True)
    kq, gamma, mstar2 = sp.symbols(
        "K_Q gamma M_star_sq", positive=True
    )
    force_ir = sp.symbols("A_IR", positive=True)

    curvature, curvature_dot = sp.symbols("R R_dot", real=True)
    amplitude, amplitude_dot = sp.symbols(
        "delta_rho delta_rho_dot", real=True
    )
    phase_dot = sp.symbols("vartheta_dot", real=True)
    force_dot = sp.symbols("pi_dot", real=True)

    grad_curvature_sq = sp.symbols("grad_R_sq", real=True)
    grad_amplitude_sq = sp.symbols(
        "grad_delta_rho_sq", real=True
    )
    grad_phase_sq = sp.symbols("grad_vartheta_sq", real=True)
    lap_force = sp.symbols("lap_pi", real=True)
    grad_r_dot_grad_pi = sp.symbols(
        "grad_R_dot_grad_pi", real=True
    )
    grad_force_cubed = sp.symbols(
        "grad_pi_sq_three_halves", nonnegative=True
    )

    exp_r = sum(
        epsilon**n * curvature**n / sp.factorial(n)
        for n in range(5)
    )
    exp_3r = sum(
        epsilon**n * (3 * curvature) ** n / sp.factorial(n)
        for n in range(5)
    )
    exp_minus_r = sum(
        epsilon**n * (-curvature) ** n / sp.factorial(n)
        for n in range(5)
    )

    potential_series = (
        v0
        + epsilon * v1 * amplitude
        + epsilon**2 * v2 * amplitude**2 / 2
        + epsilon**3 * v3 * amplitude**3 / 6
        + epsilon**4 * v4 * amplitude**4 / 24
    )

    # Up to a spatial boundary term,
    # sqrt(h) R3 / 2 -> a^3 M_P^2 exp(R) (D R)^2.
    gravity = (
        -3
        * mcos2
        * exp_3r
        * (hubble + epsilon * curvature_dot) ** 2
        + mp2 * exp_r * epsilon**2 * grad_curvature_sq
    )

    matter_temporal = (
        exp_3r
        * (
            (rho_dot + epsilon * amplitude_dot) ** 2 / 2
            + (rho + epsilon * amplitude) ** 2
            * (chemical + epsilon * phase_dot) ** 2
            / 2
            - potential_series
        )
    )
    phase_stiffness = (
        (rho + epsilon * amplitude) ** 2
        * (
            1
            + alignment * (rho + epsilon * amplitude) ** 2
        )
    )
    matter_spatial = (
        -exp_r
        * epsilon**2
        * (
            grad_amplitude_sq
            + phase_stiffness * grad_phase_sq
        )
        / 2
    )

    force_temporal = (
        exp_3r * kq * epsilon**2 * force_dot**2 / 2
    )
    force_regulator = (
        -gamma
        * exp_minus_r
        * (
            epsilon * lap_force
            + epsilon**2 * grad_r_dot_grad_pi
        )
        ** 2
        / (2 * mstar2)
    )

    analytic_action = sp.expand(
        gravity
        + matter_temporal
        + matter_spatial
        + force_temporal
        + force_regulator
    )
    l3_analytic = coefficient(analytic_action, epsilon, 3)
    l4_analytic = coefficient(analytic_action, epsilon, 4)

    b0 = (
        (rho_dot**2 + rho**2 * chemical**2) / 2 - v0
    )
    b1 = (
        rho_dot * amplitude_dot
        + rho * chemical**2 * amplitude
        + rho**2 * chemical * phase_dot
        - v1 * amplitude
    )
    b2 = (
        amplitude_dot**2 / 2
        + chemical**2 * amplitude**2 / 2
        + 2 * rho * chemical * amplitude * phase_dot
        + rho**2 * phase_dot**2 / 2
        - v2 * amplitude**2 / 2
    )
    b3 = (
        rho * amplitude * phase_dot**2
        + chemical * amplitude**2 * phase_dot
        - v3 * amplitude**3 / 6
    )
    b4 = (
        amplitude**2 * phase_dot**2 / 2
        - v4 * amplitude**4 / 24
    )

    phase_f0 = rho**2 * (1 + alignment * rho**2)
    phase_f1 = 2 * rho + 4 * alignment * rho**3
    phase_f2 = 2 + 12 * alignment * rho**2

    gravity_l3 = (
        -3
        * mcos2
        * (
            3 * curvature * curvature_dot**2
            + 9 * hubble * curvature**2 * curvature_dot
            + sp.Rational(9, 2) * hubble**2 * curvature**3
        )
        + mp2 * curvature * grad_curvature_sq
    )
    gravity_l4 = (
        -3
        * mcos2
        * (
            sp.Rational(9, 2)
            * curvature**2
            * curvature_dot**2
            + 9 * hubble * curvature**3 * curvature_dot
            + sp.Rational(27, 8)
            * hubble**2
            * curvature**4
        )
        + mp2 * curvature**2 * grad_curvature_sq / 2
    )

    matter_l3 = (
        b3
        + 3 * curvature * b2
        + sp.Rational(9, 2) * curvature**2 * b1
        + sp.Rational(9, 2) * curvature**3 * b0
        - (
            curvature
            * (grad_amplitude_sq + phase_f0 * grad_phase_sq)
            + phase_f1 * amplitude * grad_phase_sq
        )
        / 2
    )
    matter_l4 = (
        b4
        + 3 * curvature * b3
        + sp.Rational(9, 2) * curvature**2 * b2
        + sp.Rational(9, 2) * curvature**3 * b1
        + sp.Rational(27, 8) * curvature**4 * b0
        - (
            curvature**2
            * (grad_amplitude_sq + phase_f0 * grad_phase_sq)
            / 2
            + curvature
            * phase_f1
            * amplitude
            * grad_phase_sq
            + phase_f2 * amplitude**2 * grad_phase_sq / 2
        )
        / 2
    )

    force_l3_analytic = (
        3 * kq * curvature * force_dot**2 / 2
        + gamma * curvature * lap_force**2 / (2 * mstar2)
        - gamma
        * lap_force
        * grad_r_dot_grad_pi
        / mstar2
    )
    force_l4 = (
        9 * kq * curvature**2 * force_dot**2 / 4
        - gamma * curvature**2 * lap_force**2 / (4 * mstar2)
        + gamma
        * curvature
        * lap_force
        * grad_r_dot_grad_pi
        / mstar2
        - gamma
        * grad_r_dot_grad_pi**2
        / (2 * mstar2)
    )

    expected_l3_analytic = sp.expand(
        gravity_l3 + matter_l3 + force_l3_analytic
    )
    expected_l4 = sp.expand(
        gravity_l4 + matter_l4 + force_l4
    )
    require_zero(
        "direct analytic cubic contact block",
        l3_analytic - expected_l3_analytic,
    )
    require_zero(
        "direct analytic quartic contact block",
        l4_analytic - expected_l4,
    )

    # The retained exact IR functional is order |epsilon|^3 rather than an
    # ordinary homogeneous cubic Taylor vertex.  It belongs to the classical
    # direct contact functional but remains on the declared Track-A boundary.
    force_l3_with_exact_ir = (
        force_l3_analytic - force_ir * grad_force_cubed
    )
    complete_l3 = sp.expand(
        gravity_l3 + matter_l3 + force_l3_with_exact_ir
    )

    return {
        "conventions": {
            "background_constraints": "delta_N=0; beta=0",
            "physical_fields": [
                "R",
                "delta_rho",
                "vartheta",
                "pi",
            ],
            "density": "per unperturbed physical FRW volume a^3",
            "spatial_curvature_boundary_rule": (
                "integral sqrt(h) M_P^2 R3/2 "
                "= integral a^3 M_P^2 exp(R) D_iR D_iR"
            ),
        },
        "building_blocks": {
            "B0": str(b0),
            "B1": str(b1),
            "B2": str(b2),
            "B3": str(b3),
            "B4": str(b4),
            "phase_stiffness_F0": str(phase_f0),
            "phase_stiffness_F1": str(phase_f1),
            "phase_stiffness_F2": str(phase_f2),
        },
        "direct_contact": {
            "gravity_L3_x0": str(gravity_l3),
            "gravity_L4_x0": str(gravity_l4),
            "condensate_alignment_L3_x0": str(matter_l3),
            "condensate_alignment_L4_x0": str(matter_l4),
            "force_L3_x0_analytic": str(force_l3_analytic),
            "force_L3_x0_with_exact_IR_functional": str(
                force_l3_with_exact_ir
            ),
            "force_L4_x0": str(force_l4),
            "complete_L3_x0": str(complete_l3),
            "complete_L4_x0": str(expected_l4),
            "status": "PASS_X_ONLY_DIRECT_CONTACT_BLOCK",
        },
        "regressions": {
            "Track_A_Q_squared_cubic": (
                "3*K_Q*R*pi_dot^2/2"
            ),
            "Track_A_Q_squared_quartic": (
                "9*K_Q*R^2*pi_dot^2/4"
            ),
            "Track_A_regulator_cubic": str(
                force_l3_analytic
                - 3 * kq * curvature * force_dot**2 / 2
            ),
            "Track_A_regulator_quartic": str(
                force_l4
                - 9 * kq * curvature**2 * force_dot**2 / 4
            ),
            "status": "PASS",
        },
        "scientific_boundary": {
            "derived": [
                "complete direct L3[x,0] physical-field contact block",
                "complete direct L4[x,0] physical-field contact block",
                "gravity, condensate, alignment and Track-A force decomposition",
            ],
            "not_derived": [
                "constraint-dressed L3[x,z1]",
                "constraint-dressed direct quartic block L4[x,z1]",
                "regular physical scalar eigenmode projection",
                "cosmological 2-to-2 amplitude or cutoff",
            ],
            "required_combination": (
                "Lred4=L4[x,z1]-S2^T*C^(-1)*S2/2"
            ),
            "exact_Y_three_halves_rule": (
                "retained as a classical |epsilon|^3 functional; "
                "not promoted to a homogeneous analytic cubic vertex"
            ),
        },
    }


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    symbolic = symbolic_audit()
    summary = {
        "gate": "UVIR-003",
        "stage": "B_DIRECT_X_ONLY_CONTACT_BLOCK",
        "calculation_status": "PASS",
        "subgate_status": "PASS_X_ONLY_DIRECT_CONTACT_BLOCK",
        "origin_linear_finite_q_J2_status": (
            "VERIFIED_PREVIOUS_CHECKPOINT"
        ),
        "complete_finite_q_S2_status": "NOT_YET_DERIVED",
        "constraint_dressed_contact_status": "NOT_YET_DERIVED",
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "symbolic_audit": symbolic,
        "scientific_boundary": (
            "The complete x-only direct cubic and quartic physical-field "
            "contact blocks are verified. They are components, not the full "
            "constrained vertices. The next calculation must retain the "
            "first-order lapse/shift solution in L3[x,z1] and L4[x,z1] before "
            "combining the latter with the dressed-source Schur functional "
            "-S2^T C^(-1) S2/2."
        ),
        "next_required_calculation": [
            (
                "expand the complete action through quartic order while "
                "retaining terms that depend on first-order delta_N and beta"
            ),
            (
                "substitute z1=-C^(-1)J1 to form L3[x,z1] and L4[x,z1]"
            ),
            (
                "combine L4[x,z1] with -S2^T C^(-1)S2/2"
            ),
            (
                "project onto the regular physical scalar basis and derive "
                "the gauge-regular 2-to-2 amplitude"
            ),
        ],
    }

    output_path = (
        args.output_dir / "uvir003_direct_contact_block_summary.json"
    )
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("Direct gravity cubic/quartic contact block: VERIFIED")
    print("Direct condensate/alignment contact block: VERIFIED")
    print("Direct Track-A force contact block: VERIFIED")
    print("Complete L3[x,0] and L4[x,0]: VERIFIED")
    print("Constraint-dressed L4[x,z1]: NOT_YET_DERIVED")
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_X_ONLY_DIRECT_CONTACT_BLOCK")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
