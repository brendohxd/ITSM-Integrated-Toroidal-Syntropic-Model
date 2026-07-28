#!/usr/bin/env python3
"""Audit the constraint dressing required beyond the origin-linear J2.

The earlier finite-q source calculation extracted the coefficient linear in
the lapse and scalar shift at vanishing constraints.  This script checks
whether that coefficient is the complete second-order source after the
first-order constraint solution z1=-C^{-1}J1 is inserted.

An exact homogeneous lapse sub-block is sufficient to answer the question:
the cubic ADM action contains lapse-squared and lapse-cubed terms.  Therefore

    S2(x) = partial_z L3[x,z] evaluated at z=z1

is not generally equal to the origin-linear coefficient J2.  The quartic
constraint elimination must use S2, not J2 at z=0.
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
    lapse, lapse_1 = sp.symbols("delta_N delta_N_1", real=True)

    mcos2, hubble = sp.symbols("M_cos_sq H", real=True)
    rho, rho_dot, chemical = sp.symbols(
        "rho rho_dot mu",
        real=True,
    )
    curvature, curvature_dot = sp.symbols("R R_dot", real=True)
    amplitude, amplitude_dot = sp.symbols(
        "delta_rho delta_rho_dot",
        real=True,
    )
    phase_dot = sp.symbols("vartheta_dot", real=True)
    v0, v1, v2, v3, v4 = sp.symbols(
        "V V_rho V_rhorho V_rhorhorho V_rhorhorhorho",
        real=True,
    )

    exp_3r = sum(
        epsilon**order
        * (3 * curvature) ** order
        / sp.factorial(order)
        for order in range(5)
    )
    potential = (
        v0
        + epsilon * v1 * amplitude
        + epsilon**2 * v2 * amplitude**2 / 2
        + epsilon**3 * v3 * amplitude**3 / 6
        + epsilon**4 * v4 * amplitude**4 / 24
    )
    numerator = (
        -3
        * mcos2
        * (hubble + epsilon * curvature_dot) ** 2
        + (rho_dot + epsilon * amplitude_dot) ** 2 / 2
        + (rho + epsilon * amplitude) ** 2
        * (chemical + epsilon * phase_dot) ** 2
        / 2
    )

    b_series = sp.expand(exp_3r * numerator)
    p_series = sp.expand(exp_3r * potential)
    b = [coefficient(b_series, epsilon, order) for order in range(5)]
    p = [coefficient(p_series, epsilon, order) for order in range(5)]

    exact_lapse_action = (
        b_series / (1 + epsilon * lapse)
        - (1 + epsilon * lapse) * p_series
    )
    series = sp.series(
        exact_lapse_action,
        epsilon,
        0,
        5,
    ).removeO()
    l2 = coefficient(series, epsilon, 2)
    l3 = coefficient(series, epsilon, 3)
    l4 = coefficient(series, epsilon, 4)

    expected_l2 = (
        b[2]
        - p[2]
        - lapse * (b[1] + p[1])
        + lapse**2 * b[0]
    )
    expected_l3 = (
        b[3]
        - p[3]
        - lapse * (b[2] + p[2])
        + lapse**2 * b[1]
        - lapse**3 * b[0]
    )
    expected_l4 = (
        b[4]
        - p[4]
        - lapse * (b[3] + p[3])
        + lapse**2 * b[2]
        - lapse**3 * b[1]
        + lapse**4 * b[0]
    )
    require_zero("homogeneous lapse L2", l2 - expected_l2)
    require_zero("homogeneous lapse L3", l3 - expected_l3)
    require_zero("homogeneous lapse L4", l4 - expected_l4)

    friedmann = {
        v0: (
            3 * mcos2 * hubble**2
            - (rho_dot**2 + rho**2 * chemical**2) / 2
        )
    }
    require_zero(
        "on-shell background numerator",
        (b[0] + v0).subs(friedmann),
    )

    constraint_c_nn = sp.diff(l2, lapse, 2).subs(friedmann)
    require_zero(
        "quadratic lapse matrix entry",
        constraint_c_nn + 2 * v0.subs(friedmann),
    )

    j1_origin = sp.diff(l2, lapse).subs(lapse, 0)
    j2_origin = sp.diff(l3, lapse).subs(lapse, 0)
    s2_dressed = sp.diff(l3, lapse).subs(lapse, lapse_1)
    dressing_delta = sp.factor(
        (s2_dressed - j2_origin).subs(friedmann)
    )
    expected_delta = sp.factor(
        (
            2 * b[1] * lapse_1
            + 3 * v0 * lapse_1**2
        ).subs(friedmann)
    )
    require_zero(
        "nonlinear second-order lapse-source correction",
        dressing_delta - expected_delta,
    )

    direct_l4_origin = l4.subs(lapse, 0)
    l4_at_lapse_1 = l4.subs(lapse, lapse_1)
    quartic_dressing = sp.factor(
        (l4_at_lapse_1 - direct_l4_origin).subs(friedmann)
    )
    expected_quartic_dressing = sp.factor(
        (
            -lapse_1 * (b[3] + p[3])
            + lapse_1**2 * b[2]
            - lapse_1**3 * b[1]
            - lapse_1**4 * v0
        ).subs(friedmann)
    )
    require_zero(
        "quartic first-order lapse dressing",
        quartic_dressing - expected_quartic_dressing,
    )

    c11, c12, c22 = sp.symbols("C_11 C_12 C_22", real=True)
    s_n, s_sigma = sp.symbols("S2_N S2_Sigma", real=True)
    z2_n, z2_sigma = sp.symbols(
        "delta_N_2 Sigma_2",
        real=True,
    )
    matrix = sp.Matrix([[c11, c12], [c12, c22]])
    source = sp.Matrix([s_n, s_sigma])
    z2 = sp.Matrix([z2_n, z2_sigma])
    solution = sp.simplify(-matrix.inv() * source)
    quartic_z2_block = (
        (z2.T * matrix * z2)[0] / 2
        + (z2.T * source)[0]
    )
    schur_correct = sp.factor(
        -(source.T * matrix.inv() * source)[0] / 2
    )
    require_zero(
        "correct dressed quartic Schur identity",
        quartic_z2_block.subs(
            {
                z2_n: solution[0],
                z2_sigma: solution[1],
            }
        )
        - schur_correct,
    )

    return {
        "homogeneous_lapse_subblock": {
            "L2": str(l2.subs(friedmann)),
            "L3": str(l3.subs(friedmann)),
            "L4": str(l4.subs(friedmann)),
            "C_NN": str(constraint_c_nn),
            "J1_at_origin": str(j1_origin.subs(friedmann)),
            "J2_at_origin": str(j2_origin.subs(friedmann)),
            "S2_at_delta_N_1": str(s2_dressed.subs(friedmann)),
            "S2_minus_J2_origin": str(dressing_delta),
            "L4_at_delta_N_1_minus_L4_x0": str(
                quartic_dressing
            ),
            "status": "NONLINEAR_CONSTRAINT_DRESSING_VERIFIED",
        },
        "general_reduction_identity": {
            "first_order_solution": "z1=-C^(-1)J1",
            "second_order_source": "S2=partial_z L3[x,z]|z=z1",
            "second_order_solution": "z2=-C^(-1)S2",
            "cubic_reduced": "L3_red=L3[x,z1]",
            "quartic_reduced": (
                "L4_red=L4[x,z1]-S2^T C^(-1) S2/2"
            ),
            "verified_schur": str(schur_correct),
        },
        "checkpoint_correction": {
            "origin_linear_source": (
                "J2_origin=partial_z L3[x,z]|z=0"
            ),
            "finding": (
                "J2_origin is not the complete second-order source when "
                "L3 contains z^2*x or z^3 terms"
            ),
            "explicit_counterterm": (
                "S2_N-J2_N_origin="
                "2*B1*delta_N_1+3*V*delta_N_1^2"
            ),
            "previous_schur_interpretation": (
                "PROVISIONAL_ORIGIN_LINEAR_COMPONENT_ONLY"
            ),
            "full_constraint_dressing": "NOT_YET_DERIVED",
        },
        "scientific_boundary": {
            "derived": [
                "exact homogeneous lapse L2, L3 and L4 dressing",
                "nonzero correction from J2_origin to S2 at z1",
                "general second-order constraint-elimination identity",
            ],
            "not_derived": [
                "complete finite-q S2 including scalar-shift dressing",
                "complete L3[x,z1] and L4[x,z1]",
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
        "stage": "B_CONSTRAINT_DRESSING_COMPLETENESS_AUDIT",
        "calculation_status": "PASS",
        "subgate_status": "PASS_CONSTRAINT_DRESSING_COMPLETENESS_AUDIT",
        "origin_linear_J2_status": (
            "VERIFIED_COMPONENT_NOT_COMPLETE_SECOND_ORDER_SOURCE"
        ),
        "previous_quartic_schur_status": (
            "RECLASSIFIED_PROVISIONAL_ORIGIN_LINEAR_COMPONENT"
        ),
        "complete_finite_q_S2_status": "NOT_YET_DERIVED",
        "constraint_dressed_contact_status": "NOT_YET_DERIVED",
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "symbolic_audit": symbolic,
        "scientific_boundary": (
            "The previous origin-linear J2 and its algebraic Schur functional "
            "remain verified as components. They are not the complete "
            "second-order source and quartic constraint correction because "
            "the exact ADM cubic action contains nonlinear first-order "
            "constraint terms. The full finite-q S2 must be evaluated at z1."
        ),
        "next_required_calculation": [
            (
                "expand the full finite-q cubic ADM action including all "
                "lapse and scalar-shift powers"
            ),
            "substitute z1=-C^(-1)J1 and derive S2=partial_z L3[x,z1]",
            (
                "derive L3[x,z1] and L4[x,z1], then combine L4 with "
                "-S2^T C^(-1) S2/2"
            ),
            (
                "project the corrected vertices onto the regular physical "
                "scalar basis"
            ),
        ],
    }

    output_path = (
        args.output_dir
        / "uvir003_constraint_dressing_audit_summary.json"
    )
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("Exact homogeneous lapse L2/L3/L4 dressing: VERIFIED")
    print("Origin-linear J2 as a component: VERIFIED")
    print("Origin-linear J2 as complete S2: REJECTED")
    print("Correct source S2=partial_z L3[x,z1]: VERIFIED")
    print(
        "Previous quartic Schur: "
        "RECLASSIFIED_PROVISIONAL_ORIGIN_LINEAR_COMPONENT"
    )
    print("Complete finite-q S2: NOT_YET_DERIVED")
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_CONSTRAINT_DRESSING_COMPLETENESS_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
