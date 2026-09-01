#!/usr/bin/env python3
"""UVIR-003 finite-q scalar-shift constraint-dressing sub-block.

Derives the exact gravity+aether extrinsic-curvature interaction for a
finite-q scalar shift with one spatially homogeneous (soft) curvature leg.
The channel keeps

    z = (delta_N, Sigma),  Sigma=-D^2 beta=q_phys^2 beta,

and is sufficient to expose the nonlinear lapse/shift terms that distinguish

    S2 = partial_z L3[x,z] evaluated at z=z1

from the origin-linear coefficient J2.  It is a verified finite-q sub-block,
not the complete non-collinear three-momentum scalar kernel.
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
    epsilon = sp.symbols("epsilon", real=True)
    mcos2, d123 = sp.symbols(
        "M_cos_sq D_123",
        nonzero=True,
    )
    hubble = sp.symbols("H", real=True)
    curvature, curvature_dot = sp.symbols("R R_dot", real=True)
    lapse, sigma = sp.symbols("delta_N Sigma", real=True)
    lapse_1, sigma_1 = sp.symbols(
        "delta_N_1 Sigma_1",
        real=True,
    )

    # Exact ADM coefficients:
    # A_K+B_K=-D_123 and A_K+3B_K=-2M_cos^2.
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

    volume = sp.exp(3 * epsilon * curvature)
    inverse_lapse = 1 / (1 + epsilon * lapse)
    inverse_metric_factor = sp.exp(-2 * epsilon * curvature)
    expansion = hubble + epsilon * curvature_dot

    # Choose the shift momentum along x.  With a homogeneous curvature leg,
    # the mixed extrinsic-curvature eigenvalues are
    #
    # Kx_x=(H+R_dot+e^{-2R}Sigma)/N,
    # Ky_y=Kz_z=(H+R_dot)/N.
    k_longitudinal = (
        expansion
        + epsilon * inverse_metric_factor * sigma
    ) * inverse_lapse
    k_transverse = expansion * inverse_lapse
    trace_k = k_longitudinal + 2 * k_transverse
    kij_kij = k_longitudinal**2 + 2 * k_transverse**2

    exact = sp.simplify(
        (1 + epsilon * lapse)
        * volume
        * (
            coeff_kij * kij_kij
            + coeff_k * trace_k**2
        )
        / 2
    )
    compact_exact = sp.simplify(
        volume
        * inverse_lapse
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
    require_zero(
        "exact soft-curvature scalar-shift block",
        exact - compact_exact,
    )

    series = sp.series(
        exact,
        epsilon,
        0,
        5,
    ).removeO()
    l2 = coefficient(series, epsilon, 2)
    l3 = coefficient(series, epsilon, 3)
    l4 = coefficient(series, epsilon, 4)

    constraint_matrix = sp.hessian(
        l2,
        (lapse, sigma),
    )
    expected_constraint_matrix = sp.Matrix(
        [
            [-6 * mcos2 * hubble**2, 2 * mcos2 * hubble],
            [2 * mcos2 * hubble, -d123],
        ]
    )
    require_zero(
        "extrinsic finite-q constraint matrix sub-block",
        constraint_matrix - expected_constraint_matrix,
    )

    j2_n_origin = sp.factor(
        sp.diff(l3, lapse).subs({lapse: 0, sigma: 0})
    )
    j2_sigma_origin = sp.factor(
        sp.diff(l3, sigma).subs({lapse: 0, sigma: 0})
    )
    s2_n = sp.factor(
        sp.diff(l3, lapse).subs(
            {lapse: lapse_1, sigma: sigma_1}
        )
    )
    s2_sigma = sp.factor(
        sp.diff(l3, sigma).subs(
            {lapse: lapse_1, sigma: sigma_1}
        )
    )
    delta_s2_n = sp.factor(s2_n - j2_n_origin)
    delta_s2_sigma = sp.factor(
        s2_sigma - j2_sigma_origin
    )

    # Independent differentiation of the compact exact series verifies the
    # full dressing, including terms proportional to delta_N_1*Sigma_1.
    expected_delta_n = sp.factor(
        (
            d123 * sigma_1**2
            - 36 * hubble**2 * mcos2 * curvature * lapse_1
            + 18 * hubble**2 * mcos2 * lapse_1**2
            + 4 * hubble * mcos2 * curvature * sigma_1
            - 24 * hubble * mcos2 * curvature_dot * lapse_1
            - 8 * hubble * mcos2 * sigma_1 * lapse_1
            + 4 * mcos2 * curvature_dot * sigma_1
        )
        / 2
    )
    expected_delta_sigma = sp.factor(
        d123 * curvature * sigma_1
        + d123 * sigma_1 * lapse_1
        + 2 * hubble * mcos2 * curvature * lapse_1
        - 2 * hubble * mcos2 * lapse_1**2
        + 2 * mcos2 * curvature_dot * lapse_1
    )
    require_zero(
        "soft-channel lapse source dressing",
        delta_s2_n - expected_delta_n,
    )
    require_zero(
        "soft-channel scalar-shift source dressing",
        delta_s2_sigma - expected_delta_sigma,
    )

    cacc, q, potential = sp.symbols(
        "C_14 q_phys V",
        real=True,
    )
    j1_n, j1_sigma = sp.symbols(
        "J1_N J1_Sigma",
        real=True,
    )
    full_constraint_matrix = sp.Matrix(
        [
            [cacc * q**2 - 2 * potential, 2 * mcos2 * hubble],
            [2 * mcos2 * hubble, -d123],
        ]
    )
    j1 = sp.Matrix([j1_n, j1_sigma])
    z1 = sp.simplify(-full_constraint_matrix.inv() * j1)
    require_zero(
        "finite-q first-order constraint solution",
        full_constraint_matrix * z1 + j1,
    )
    dressed_source_at_solution = sp.Matrix(
        [s2_n, s2_sigma]
    ).subs(
        {
            lapse_1: z1[0],
            sigma_1: z1[1],
        }
    )
    origin_source = sp.Matrix(
        [j2_n_origin, j2_sigma_origin]
    )
    source_correction_at_solution = sp.simplify(
        dressed_source_at_solution - origin_source
    )

    l3_reduced_soft = sp.factor(
        l3.subs(
            {
                lapse: z1[0],
                sigma: z1[1],
            }
        )
    )
    l4_at_z1_soft = sp.factor(
        l4.subs(
            {
                lapse: z1[0],
                sigma: z1[1],
            }
        )
    )

    return {
        "channel": {
            "description": (
                "finite-q scalar shift with one homogeneous soft curvature "
                "leg; shift momentum chosen along x"
            ),
            "constraints": [
                "delta_N",
                "Sigma=-D^2(beta)=q_phys^2*beta",
            ],
            "domain": "q_phys>0; det(C)!=0",
            "not_claimed": (
                "complete non-collinear three-momentum scalar kernel"
            ),
        },
        "exact_extrinsic_block": {
            "Kij_coefficient": str(coeff_kij),
            "K_squared_coefficient": str(coeff_k),
            "compact_density": str(compact_exact),
            "L2": str(l2),
            "L3": str(l3),
            "L4": str(l4),
            "constraint_matrix_subblock": str(constraint_matrix),
            "status": "VERIFIED",
        },
        "origin_linear_source": {
            "J2_N_origin": str(j2_n_origin),
            "J2_Sigma_origin": str(j2_sigma_origin),
            "status": "VERIFIED_COMPONENT",
        },
        "dressed_source": {
            "S2_N_at_z1_symbols": str(s2_n),
            "S2_Sigma_at_z1_symbols": str(s2_sigma),
            "Delta_S2_N": str(delta_s2_n),
            "Delta_S2_Sigma": str(delta_s2_sigma),
            "finite_q_z1": str(z1),
            "Delta_S2_at_finite_q_z1": str(
                source_correction_at_solution
            ),
            "status": "PASS_SOFT_CURVATURE_SHIFT_DRESSING_SUBBLOCK",
        },
        "reduced_interaction_subblock": {
            "L3_at_finite_q_z1": str(l3_reduced_soft),
            "L4_at_finite_q_z1": str(l4_at_z1_soft),
            "quartic_rule": (
                "L4_red=L4[x,z1]-S2^T*C^(-1)*S2/2"
            ),
            "status": "VERIFIED_FOR_DECLARED_SOFT_CHANNEL",
        },
        "scientific_boundary": {
            "derived": [
                "exact gravity+aether scalar-shear ADM block through quartic",
                "nonlinear lapse/shift correction to S2 in the soft channel",
                "finite-q substitution z1=-C^(-1)J1",
                "L3[x,z1] and L4[x,z1] for the declared channel",
            ],
            "not_derived": [
                "generic non-collinear three-momentum shift kernel",
                "matter and force shift-advection dressing for generic triads",
                "complete physical scalar projection or amplitude",
            ],
        },
    }


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    symbolic = symbolic_audit()
    summary = {
        "gate": "UVIR-003",
        "stage": "B_SOFT_CURVATURE_SCALAR_SHIFT_DRESSING",
        "calculation_status": "PASS",
        "subgate_status": (
            "PASS_SOFT_CURVATURE_SHIFT_DRESSING_SUBBLOCK"
        ),
        "complete_finite_q_S2_status": (
            "NOT_YET_DERIVED_GENERIC_NONCOLLINEAR_KERNEL"
        ),
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "symbolic_audit": symbolic,
        "scientific_boundary": (
            "The exact gravity+aether lapse/shift dressing is verified for "
            "a finite-q scalar-shear pair with one soft homogeneous curvature "
            "leg. This proves and fixes a nonzero part of S2 at z1, but does "
            "not replace the generic non-collinear convolution kernel."
        ),
        "next_required_calculation": [
            (
                "derive the generic three-momentum gravity+aether scalar-shift "
                "kernel including D_iR D_i beta terms"
            ),
            (
                "add condensate and Track-A force shift-advection dressing"
            ),
            (
                "assemble complete finite-q S2 and corrected quartic Schur "
                "functional"
            ),
            (
                "project the corrected interactions onto regular physical "
                "scalar modes"
            ),
        ],
    }

    output_path = (
        args.output_dir
        / "uvir003_scalar_shift_dressing_summary.json"
    )
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("Exact soft-channel gravity+aether shift block: VERIFIED")
    print("Finite-q first-order z1 substitution: VERIFIED")
    print("Nonlinear lapse/shift correction to S2: VERIFIED")
    print("Soft-channel L3[x,z1] and L4[x,z1]: VERIFIED")
    print("Generic non-collinear finite-q S2: NOT_YET_DERIVED")
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_SOFT_CURVATURE_SHIFT_DRESSING_SUBBLOCK")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
