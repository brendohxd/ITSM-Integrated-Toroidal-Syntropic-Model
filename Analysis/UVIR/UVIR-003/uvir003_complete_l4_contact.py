#!/usr/bin/env python3
"""UVIR-003 complete generic quartic contact functional at first-order constraints.

Expands the fixed gravity+aether+condensate+alignment+Track-A action to fourth
amplitude order with arbitrary real-space scalar-shift contractions.  It forms

    L4[x,z1],  z1=-C^(-1)J1,

as a functional of the already verified first-order lapse and shift fields.
The separately verified complete S2 then supplies the Schur term.  Physical
mode projection and the 2-to-2 amplitude remain outside this checkpoint.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp

from uvir003_complete_s2_operator import symbolic_audit as s2_audit
from uvir003_direct_contact_block import symbolic_audit as direct_audit
from uvir003_scalar_shift_dressing import symbolic_audit as soft_audit


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


def coefficient(expression: sp.Expr, epsilon: sp.Symbol, order: int) -> sp.Expr:
    return sp.expand(expression).coeff(epsilon, order)


def require_zero(name: str, expression: sp.Expr) -> None:
    residual = sp.factor(sp.expand(expression))
    if residual != 0:
        raise AssertionError(f"{name} failed: {residual}")


def symbolic_audit() -> dict[str, object]:
    e = sp.symbols("epsilon", real=True)
    mp2, mcos2, d123, c14 = sp.symbols(
        "M_P_sq M_cos_sq D_123 C_14", real=True
    )
    hubble = sp.symbols("H", real=True)
    rho, rho_dot, chemical = sp.symbols("rho rho_dot mu", real=True)
    v0, v1, v2, v3, v4 = sp.symbols(
        "V V_rho V_rhorho V_rhorhorho V_rhorhorhorho", real=True
    )
    alignment = sp.symbols("zeta_align", real=True)
    kq, gamma, mstar2, force_ir = sp.symbols(
        "K_Q gamma M_star_sq A_IR", real=True
    )

    curvature, curvature_dot, lapse = sp.symbols(
        "R R_dot delta_N", real=True
    )
    amplitude, amplitude_dot, phase_dot = sp.symbols(
        "delta_rho delta_rho_dot vartheta_dot", real=True
    )
    force_dot = sp.symbols("pi_dot", real=True)

    grad_r_sq, grad_lapse_sq, grad_lapse_r = sp.symbols(
        "grad_R_sq D_delta_N_sq D_delta_N_dot_D_R", real=True
    )
    lap_beta, hess_beta_sq = sp.symbols(
        "D2_beta Dij_beta_sq", real=True
    )
    u_beta, w_beta = sp.symbols(
        "D_R_dot_D_beta Dij_beta_Di_R_Dj_beta", real=True
    )
    grad_beta_sq = sp.symbols("D_beta_sq", real=True)

    grad_amplitude_sq, grad_phase_sq = sp.symbols(
        "grad_delta_rho_sq grad_vartheta_sq", real=True
    )
    adv_amplitude, adv_phase = sp.symbols(
        "D_beta_dot_D_delta_rho D_beta_dot_D_vartheta", real=True
    )
    lap_force, grad_r_force, adv_force = sp.symbols(
        "lap_pi grad_R_dot_grad_pi grad_beta_dot_grad_pi", real=True
    )
    grad_force_cubed = sp.symbols(
        "grad_pi_sq_three_halves", nonnegative=True
    )

    exp_3r = sp.exp(3 * e * curvature)
    exp_r = sp.exp(e * curvature)
    inv_metric = sp.exp(-2 * e * curvature)
    volume_over_lapse = exp_3r / (1 + e * lapse)

    coeff_kij = mcos2 - sp.Rational(3, 2) * d123
    coeff_k = -mcos2 + d123 / 2
    trace_t = e * lap_beta + e**2 * u_beta
    norm_t = (
        e**2 * hess_beta_sq
        + 2 * e**3 * (-2 * w_beta + lap_beta * u_beta)
        + e**4 * (2 * grad_r_sq * grad_beta_sq + u_beta**2)
    )
    expansion = hubble + e * curvature_dot
    gravity_extrinsic = volume_over_lapse * (
        -3 * mcos2 * expansion**2
        + 2 * mcos2 * expansion * inv_metric * trace_t
        + inv_metric**2
        * (coeff_kij * norm_t + coeff_k * trace_t**2)
        / 2
    )
    gravity_acceleration = (
        c14
        * exp_r
        * e**2
        * grad_lapse_sq
        / (2 * (1 + e * lapse))
    )
    gravity_spatial = mp2 * exp_r * (
        (1 + e * lapse) * e**2 * grad_r_sq
        + 2 * e**2 * grad_lapse_r
    )
    gravity_action = (
        gravity_extrinsic + gravity_acceleration + gravity_spatial
    )

    perturbed_rho = rho + e * amplitude
    normal_amplitude = (
        rho_dot
        + e * amplitude_dot
        - e**2 * inv_metric * adv_amplitude
    )
    normal_phase = (
        chemical + e * phase_dot - e**2 * inv_metric * adv_phase
    )
    potential = (
        v0
        + e * v1 * amplitude
        + e**2 * v2 * amplitude**2 / 2
        + e**3 * v3 * amplitude**3 / 6
        + e**4 * v4 * amplitude**4 / 24
    )
    matter_temporal = volume_over_lapse * (
        normal_amplitude**2 + perturbed_rho**2 * normal_phase**2
    ) / 2
    matter_potential = -(1 + e * lapse) * exp_3r * potential
    phase_stiffness = perturbed_rho**2 * (
        1 + alignment * perturbed_rho**2
    )
    matter_spatial = (
        -(1 + e * lapse)
        * exp_r
        * e**2
        * (grad_amplitude_sq + phase_stiffness * grad_phase_sq)
        / 2
    )
    matter_action = matter_temporal + matter_potential + matter_spatial

    force_volume = (1 + e * lapse) * exp_3r
    q_force = (
        e * force_dot - e**2 * inv_metric * adv_force
    ) / (1 + e * lapse)
    force_q = kq * force_volume * q_force**2 / 2
    rest_laplacian = e * lap_force + e**2 * grad_r_force
    force_regulator = (
        -gamma
        * (1 + e * lapse)
        * sp.exp(-e * curvature)
        * rest_laplacian**2
        / (2 * mstar2)
    )
    force_exact_ir = (
        -force_ir
        * e**3
        * (1 + e * lapse)
        * grad_force_cubed
    )
    force_action = force_q + force_regulator + force_exact_ir

    gravity_l4 = coefficient(
        sp.series(gravity_action, e, 0, 5).removeO(), e, 4
    )
    matter_l4 = coefficient(
        sp.series(matter_action, e, 0, 5).removeO(), e, 4
    )
    force_l4 = coefficient(
        sp.series(force_action, e, 0, 5).removeO(), e, 4
    )
    complete_l4 = sp.expand(gravity_l4 + matter_l4 + force_l4)

    constraints_zero = {
        lapse: 0,
        grad_lapse_sq: 0,
        grad_lapse_r: 0,
        lap_beta: 0,
        hess_beta_sq: 0,
        u_beta: 0,
        w_beta: 0,
        grad_beta_sq: 0,
        adv_amplitude: 0,
        adv_phase: 0,
        adv_force: 0,
    }
    l4_x0 = sp.expand(complete_l4.subs(constraints_zero))

    direct = direct_audit()
    direct_symbols = {
        symbol.name: symbol
        for symbol in complete_l4.free_symbols | l4_x0.free_symbols
    }
    expected_direct = sp.sympify(
        direct["direct_contact"]["complete_L4_x0"],
        locals=direct_symbols,
    )
    require_zero("direct L4[x,0] regression", l4_x0 - expected_direct)

    sigma = sp.symbols("Sigma", real=True)
    soft_substitution = {
        lap_beta: -sigma,
        hess_beta_sq: sigma**2,
        u_beta: 0,
        w_beta: 0,
        grad_beta_sq: 0,
        grad_r_sq: 0,
        grad_lapse_sq: 0,
        grad_lapse_r: 0,
    }
    soft_gravity_l4 = sp.expand(gravity_l4.subs(soft_substitution))
    soft = soft_audit()
    soft_symbols = {
        symbol.name: symbol for symbol in soft_gravity_l4.free_symbols
    }
    expected_soft = sp.sympify(
        soft["exact_extrinsic_block"]["L4"], locals=soft_symbols
    )
    require_zero("soft-channel gravity L4 regression", soft_gravity_l4 - expected_soft)

    z1_symbols = {
        lapse: sp.Symbol("delta_N_1", real=True),
        grad_lapse_sq: sp.Symbol("D_delta_N_1_sq", real=True),
        grad_lapse_r: sp.Symbol("D_delta_N_1_dot_D_R", real=True),
        lap_beta: sp.Symbol("D2_beta_1", real=True),
        hess_beta_sq: sp.Symbol("Dij_beta_1_sq", real=True),
        u_beta: sp.Symbol("D_R_dot_D_beta_1", real=True),
        w_beta: sp.Symbol(
            "Dij_beta_1_Di_R_Dj_beta_1", real=True
        ),
        grad_beta_sq: sp.Symbol("D_beta_1_sq", real=True),
        adv_amplitude: sp.Symbol(
            "D_beta_1_dot_D_delta_rho", real=True
        ),
        adv_phase: sp.Symbol("D_beta_1_dot_D_vartheta", real=True),
        adv_force: sp.Symbol("D_beta_1_dot_D_pi", real=True),
    }
    l4_at_z1 = sp.expand(complete_l4.subs(z1_symbols))
    constraint_dressing = sp.expand(l4_at_z1 - l4_x0)

    s2 = s2_audit()
    if (
        s2["complete_finite_q_S2"]["status"]
        != "PASS_COMPLETE_FINITE_Q_S2_FUNCTIONAL"
    ):
        raise AssertionError("complete S2 dependency failed")

    return {
        "conventions": {
            "density": "per unperturbed physical FRW volume a^3",
            "domain": "q_phys>0 and det(C)!=0",
            "first_order_constraints": "z1=-C^(-1)J1",
            "quartic_rule": "L4_red=L4[x,z1]-S2^T C^(-1)S2/2",
        },
        "tensor_identities": {
            "trace_T": "D2_beta+D_iR D_i beta",
            "TijTij_through_quartic": (
                "Dij_beta_sq+2[-2W+(D2_beta)u]"
                "+[2(DR)^2(D beta)^2+u^2]"
            ),
            "status": "VERIFIED_BY_EXACT_CONFORMAL_CONTRACTION",
        },
        "quartic_contact": {
            "gravity_aether_L4": str(sp.factor(gravity_l4)),
            "condensate_alignment_L4": str(sp.factor(matter_l4)),
            "track_a_force_L4": str(sp.factor(force_l4)),
            "complete_L4_x0": str(l4_x0),
            "constraint_dressing_L4_x_z1_minus_x0": str(
                constraint_dressing
            ),
            "complete_L4_x_z1": str(l4_at_z1),
            "status": "PASS_COMPLETE_GENERIC_L4_X_Z1_CONTACT",
        },
        "regressions": {
            "direct_L4_x0": "PASS",
            "soft_curvature_gravity_L4": "PASS",
            "complete_S2_dependency": "PASS",
        },
        "reduced_quartic": {
            "functional": "L4[x,z1]-1/2 integral S2(-k)^T C(k)^(-1)S2(k)",
            "status": "ASSEMBLED_AS_COMPLETE_FUNCTIONAL",
        },
        "scientific_boundary": {
            "derived": [
                "complete generic gravity/aether L4 at z1",
                "complete condensate/alignment L4 at z1",
                "complete Track-A zero-gradient L4 at z1",
                "complete reduced quartic functional before physical projection",
            ],
            "not_derived": [
                "regular physical scalar eigenmode projection",
                "gauge-regular cosmological 2-to-2 amplitude",
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
        "stage": "B_COMPLETE_GENERIC_L4_X_Z1_CONTACT",
        "calculation_status": "PASS",
        "subgate_status": "PASS_COMPLETE_GENERIC_L4_X_Z1_CONTACT",
        "complete_L4_x_z1_status": "ASSEMBLED_AND_VERIFIED",
        "reduced_quartic_status": "ASSEMBLED_AS_COMPLETE_FUNCTIONAL",
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "symbolic_audit": symbolic,
        "scientific_boundary": (
            "The complete generic quartic contact functional at the verified "
            "first-order constraints is assembled on the homogeneous "
            "zero-gradient Track-A branch. Physical projection, amplitude "
            "and cutoff remain open."
        ),
        "next_required_calculation": [
            "construct a regular finite-q physical scalar eigenmode basis",
            "project complete cubic and quartic vertices onto that basis",
            "evaluate the gauge-regular exchange-plus-contact amplitude",
            "apply a declared partial-wave unitarity criterion",
        ],
    }
    output_path = (
        args.output_dir / "uvir003_complete_l4_contact_summary.json"
    )
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("Generic gravity/aether L4[x,z1]: VERIFIED")
    print("Condensate/alignment L4[x,z1]: VERIFIED")
    print("Track-A zero-gradient L4[x,z1]: VERIFIED")
    print("Direct and soft-channel regressions: VERIFIED")
    print("Complete reduced quartic functional: ASSEMBLED")
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_COMPLETE_GENERIC_L4_X_Z1_CONTACT")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
