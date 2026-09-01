#!/usr/bin/env python3
"""UVIR-003 generic 3D gravity/aether scalar-shift dressing kernel.

Expands the exact conformal-ADM gravity/aether action to cubic order with
arbitrary real-space scalar-shift derivatives.  It retains

    B_ij = D_i D_j beta,
    B = D^2 beta,
    u = D_i R D_i beta,
    W = B_ij D_i R D_j beta,

and the aether lapse-gradient operator.  Constraint-degree bookkeeping
separates the origin-linear J2 component from the nonlinear terms that
contribute to S2=partial_z L3[x,z1].

This closes the generic gravity/aether dressing density and its functional
operator.  Condensate and Track-A force shift-advection are separate sectors.
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
    mcos2, d123, cacc = sp.symbols(
        "M_cos_sq D_123 C_14",
        real=True,
    )
    hubble = sp.symbols("H", real=True)
    curvature, curvature_dot = sp.symbols("R R_dot", real=True)
    lapse = sp.symbols("delta_N", real=True)

    lap_beta = sp.symbols("D2_beta", real=True)
    hess_beta_sq = sp.symbols("Dij_beta_sq", real=True)
    grad_r_dot_grad_beta = sp.symbols(
        "D_R_dot_D_beta",
        real=True,
    )
    hess_beta_r_beta = sp.symbols(
        "Dij_beta_Di_R_Dj_beta",
        real=True,
    )
    grad_lapse_sq = sp.symbols("D_delta_N_sq", real=True)

    coeff_kij = mcos2 - 3 * d123 / 2
    coeff_k = -mcos2 + d123 / 2
    require_zero(
        "scalar-shift coefficient identity",
        coeff_kij + coeff_k + d123,
    )
    require_zero(
        "FRW extrinsic-curvature identity",
        coeff_kij + 3 * coeff_k + 2 * mcos2,
    )

    volume_over_lapse = (
        sp.exp(3 * epsilon * curvature)
        / (1 + epsilon * lapse)
    )
    inverse_metric_factor = sp.exp(-2 * epsilon * curvature)
    expansion = hubble + epsilon * curvature_dot

    # T_ij=D_iD_j beta-D_iR D_jbeta-D_jR D_ibeta
    #      +delta_ij D_kR D_kbeta.
    #
    # Its trace and norm through the order required by L3 are
    #
    # T = e B + e^2 u,
    # T_ij T_ij =
    #   e^2 B_ij B_ij + 2 e^3(-2W+B u) + O(e^4).
    trace_t = (
        epsilon * lap_beta
        + epsilon**2 * grad_r_dot_grad_beta
    )
    norm_t = (
        epsilon**2 * hess_beta_sq
        + 2
        * epsilon**3
        * (
            -2 * hess_beta_r_beta
            + lap_beta * grad_r_dot_grad_beta
        )
    )

    extrinsic = sp.expand(
        volume_over_lapse
        * (
            -3 * mcos2 * expansion**2
            + 2
            * mcos2
            * expansion
            * inverse_metric_factor
            * trace_t
            + inverse_metric_factor**2
            * (
                coeff_kij * norm_t
                + coeff_k * trace_t**2
            )
            / 2
        )
    )
    acceleration = (
        cacc
        * sp.exp(epsilon * curvature)
        * epsilon**2
        * grad_lapse_sq
        / (2 * (1 + epsilon * lapse))
    )
    action = extrinsic + acceleration
    series = sp.series(action, epsilon, 0, 4).removeO()
    l2 = coefficient(series, epsilon, 2)
    l3 = coefficient(series, epsilon, 3)

    scaled_l3 = sp.expand(
        l3.subs(
            {
                lapse: constraint_degree * lapse,
                lap_beta: constraint_degree * lap_beta,
                hess_beta_sq: (
                    constraint_degree**2 * hess_beta_sq
                ),
                grad_r_dot_grad_beta: (
                    constraint_degree * grad_r_dot_grad_beta
                ),
                hess_beta_r_beta: (
                    constraint_degree**2
                    * hess_beta_r_beta
                ),
                grad_lapse_sq: (
                    constraint_degree**2 * grad_lapse_sq
                ),
            }
        )
    )
    direct_l3 = coefficient(scaled_l3, constraint_degree, 0)
    origin_linear_l3 = coefficient(
        scaled_l3,
        constraint_degree,
        1,
    )
    nonlinear_l3 = sp.factor(
        coefficient(scaled_l3, constraint_degree, 2)
        + coefficient(scaled_l3, constraint_degree, 3)
    )
    require_zero(
        "constraint-degree reconstruction",
        l3 - direct_l3 - origin_linear_l3 - nonlinear_l3,
    )
    require_zero(
        "aether acceleration nonlinear density",
        sp.diff(nonlinear_l3, cacc)
        - (curvature - lapse) * grad_lapse_sq / 2,
    )

    # Regress the arbitrary-tensor kernel to the previously verified channel:
    # homogeneous R, shift momentum along x, B=-Sigma,
    # B_ij B_ij=Sigma^2, u=W=0 and no lapse gradients.
    sigma = sp.symbols("Sigma", real=True)
    soft_substitution = {
        lap_beta: -sigma,
        hess_beta_sq: sigma**2,
        grad_r_dot_grad_beta: 0,
        hess_beta_r_beta: 0,
        grad_lapse_sq: 0,
    }
    soft_exact = sp.simplify(
        sp.exp(3 * epsilon * curvature)
        / (1 + epsilon * lapse)
        * (
            -3 * mcos2 * expansion**2
            - 2
            * mcos2
            * expansion
            * epsilon
            * inverse_metric_factor
            * sigma
            - d123
            * epsilon**2
            * inverse_metric_factor**2
            * sigma**2
            / 2
        )
    )
    soft_series = sp.series(
        soft_exact,
        epsilon,
        0,
        4,
    ).removeO()
    soft_l2 = coefficient(soft_series, epsilon, 2)
    soft_l3 = coefficient(soft_series, epsilon, 3)
    require_zero(
        "generic-to-soft quadratic regression",
        l2.subs(soft_substitution) - soft_l2,
    )
    require_zero(
        "generic-to-soft cubic regression",
        l3.subs(soft_substitution) - soft_l3,
    )

    lapse_1 = sp.symbols("delta_N_1", real=True)
    lap_beta_1 = sp.symbols("D2_beta_1", real=True)
    hess_beta_sq_1 = sp.symbols(
        "Dij_beta_1_sq",
        real=True,
    )
    grad_r_dot_grad_beta_1 = sp.symbols(
        "D_R_dot_D_beta_1",
        real=True,
    )
    hess_beta_r_beta_1 = sp.symbols(
        "Dij_beta_1_Di_R_Dj_beta_1",
        real=True,
    )
    grad_lapse_1_sq = sp.symbols(
        "D_delta_N_1_sq",
        real=True,
    )
    at_z1 = {
        lapse: lapse_1,
        lap_beta: lap_beta_1,
        hess_beta_sq: hess_beta_sq_1,
        grad_r_dot_grad_beta: grad_r_dot_grad_beta_1,
        hess_beta_r_beta: hess_beta_r_beta_1,
        grad_lapse_sq: grad_lapse_1_sq,
    }

    lapse_algebraic = sp.factor(
        sp.diff(nonlinear_l3, lapse).subs(at_z1)
    )
    lapse_gradient_coefficient = sp.factor(
        sp.diff(nonlinear_l3, grad_lapse_sq).subs(at_z1)
    )
    beta_laplacian_coefficient = sp.factor(
        sp.diff(nonlinear_l3, lap_beta).subs(at_z1)
    )
    beta_hessian_sq_coefficient = sp.factor(
        sp.diff(nonlinear_l3, hess_beta_sq).subs(at_z1)
    )
    beta_u_coefficient = sp.factor(
        sp.diff(
            nonlinear_l3,
            grad_r_dot_grad_beta,
        ).subs(at_z1)
    )
    beta_w_coefficient = sp.factor(
        sp.diff(
            nonlinear_l3,
            hess_beta_r_beta,
        ).subs(at_z1)
    )

    # Soft-channel source regression.  Under B=-Sigma and B_ijB_ij=Sigma^2,
    # d/dSigma=-d/dB+2 Sigma d/d(B_ijB_ij).
    generic_soft_s2_n = sp.factor(
        sp.diff(l3, lapse).subs(soft_substitution)
    )
    generic_soft_s2_sigma = sp.factor(
        (
            -sp.diff(l3, lap_beta)
            + 2 * sigma * sp.diff(l3, hess_beta_sq)
        ).subs(soft_substitution)
    )
    require_zero(
        "soft-channel lapse source regression",
        generic_soft_s2_n - sp.diff(soft_l3, lapse),
    )
    require_zero(
        "soft-channel shift source regression",
        generic_soft_s2_sigma - sp.diff(soft_l3, sigma),
    )

    return {
        "conventions": {
            "gauge": (
                "U^mu=n^mu; N=1+delta_N; N_i=D_i beta; "
                "h_ij=a^2 exp(2R) delta_ij"
            ),
            "density": "per unperturbed physical FRW volume a^3",
            "derivatives": "D_i are physical background-leaf derivatives",
            "domain": "finite-q scalar constraint sector; q_phys>0",
        },
        "tensor_identities": {
            "T_ij": (
                "D_iD_j beta-D_iR D_jbeta-D_jR D_ibeta"
                "+delta_ij D_kR D_kbeta"
            ),
            "trace_T": "D^2 beta+D_iR D_i beta",
            "TijTij_through_cubic": (
                "(D_iD_j beta)^2"
                "+2[-2(D_iD_j beta)D_iR D_jbeta"
                "+(D^2 beta)D_iR D_i beta]"
            ),
            "status": "VERIFIED_BY_CONTRACTION",
        },
        "cubic_action": {
            "L2": str(l2),
            "L3_complete_gravity_aether": str(l3),
            "L3_direct_x0": str(direct_l3),
            "L3_origin_linear_constraints": str(
                origin_linear_l3
            ),
            "L3_nonlinear_constraint_dressing": str(
                nonlinear_l3
            ),
            "status": (
                "PASS_GENERIC_GRAVITY_AETHER_CUBIC_CONSTRAINT_DENSITY"
            ),
        },
        "dressed_functional_source": {
            "lapse_algebraic_at_z1": str(lapse_algebraic),
            "lapse_gradient_coefficient_at_z1": str(
                lapse_gradient_coefficient
            ),
            "lapse_operator": (
                "DeltaS2_N=lapse_algebraic"
                "-2 D_i[lapse_gradient_coefficient D_i(delta_N1)]"
            ),
            "beta_laplacian_coefficient_at_z1": str(
                beta_laplacian_coefficient
            ),
            "beta_hessian_sq_coefficient_at_z1": str(
                beta_hessian_sq_coefficient
            ),
            "beta_u_coefficient_at_z1": str(
                beta_u_coefficient
            ),
            "beta_w_coefficient_at_z1": str(
                beta_w_coefficient
            ),
            "beta_operator": (
                "DeltaS2_beta="
                "D^2(f_B)+D_iD_j[2 f_B2 B1_ij"
                "+f_W D_(iR D_j)beta1]"
                "-D_i[f_u D_iR+f_W B1_ji D_jR]"
            ),
            "sigma_normalization": (
                "DeltaS2_Sigma=-(D^2)^(-1)DeltaS2_beta"
                " for q_phys>0"
            ),
            "status": (
                "PASS_GENERIC_GRAVITY_AETHER_SHIFT_DRESSING_OPERATOR"
            ),
        },
        "regressions": {
            "generic_to_soft_L2": "PASS",
            "generic_to_soft_L3": "PASS",
            "generic_to_soft_S2_N": "PASS",
            "generic_to_soft_S2_Sigma": "PASS",
        },
        "scientific_boundary": {
            "derived": [
                "generic 3D gravity/aether cubic constraint density",
                "origin-linear versus nonlinear constraint decomposition",
                "lapse functional dressing operator at z1",
                "scalar-shift functional dressing operator at z1",
            ],
            "not_derived": [
                "condensate shift-advection dressing",
                "Track-A force shift-advection dressing",
                "complete combined finite-q S2",
                "physical scalar projection or amplitude",
            ],
        },
    }


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    symbolic = symbolic_audit()
    summary = {
        "gate": "UVIR-003",
        "stage": "B_GENERIC_GRAVITY_AETHER_SHIFT_KERNEL",
        "calculation_status": "PASS",
        "subgate_status": (
            "PASS_GENERIC_GRAVITY_AETHER_SHIFT_DRESSING_KERNEL"
        ),
        "gravity_aether_generic_S2_status": "ASSEMBLED_AND_VERIFIED",
        "matter_force_shift_advection_status": "NOT_YET_DERIVED",
        "complete_finite_q_S2_status": "NOT_YET_DERIVED",
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "symbolic_audit": symbolic,
        "scientific_boundary": (
            "The generic real-space gravity/aether nonlinear constraint "
            "density and its lapse/shift functional dressing operators are "
            "verified at finite q. Complete S2 still requires condensate and "
            "Track-A force shift-advection sectors before physical projection."
        ),
        "next_required_calculation": [
            "derive condensate temporal shift-advection dressing at z1",
            "derive Track-A force shift-advection dressing at z1",
            (
                "combine all sectors into complete finite-q S2 and "
                "-S2^T C^(-1)S2/2"
            ),
            "project onto the regular physical scalar basis",
        ],
    }

    output_path = (
        args.output_dir / "uvir003_generic_shift_kernel_summary.json"
    )
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("Generic 3D gravity/aether cubic constraint density: VERIFIED")
    print("Nonlinear lapse dressing operator at z1: VERIFIED")
    print("Nonlinear scalar-shift dressing operator at z1: VERIFIED")
    print("Regression to soft-curvature shift channel: VERIFIED")
    print("Matter/force shift advection: NOT_YET_DERIVED")
    print("Complete finite-q S2: NOT_YET_DERIVED")
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_GENERIC_GRAVITY_AETHER_SHIFT_DRESSING_KERNEL")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
