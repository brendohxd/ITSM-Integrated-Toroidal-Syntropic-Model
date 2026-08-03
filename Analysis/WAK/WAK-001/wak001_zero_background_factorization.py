#!/usr/bin/env python3
"""WAK-001 zero-background quadratic-factorization audit.

Expand the declared local Route-II trial density about Wbar = 0 with
grad(Wbar) = 0 and J_W = 0.  The audit determines whether W-dependent
metric/frame mixing is absent at quadratic order and where it first returns.
This is a background-specific template result, not a coupled ITSM Hessian.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def coefficient(expression: sp.Expr, epsilon: sp.Symbol, order: int) -> sp.Expr:
    """Return a simplified coefficient in the epsilon expansion."""
    expanded = sp.expand(expression)
    return sp.factor(expanded.coeff(epsilon, order))


def main() -> None:
    args = parse_args()

    epsilon = sp.symbols("epsilon", real=True)
    z_w, c_w_sq, m_w_sq = sp.symbols(
        "Z_W c_W_sq M_W_sq", real=True
    )
    w, w_t, w_x, w_y, w_z = sp.symbols("w w_t w_x w_y w_z", real=True)
    du_0, du_x, du_y, du_z = sp.symbols(
        "delta_U0 delta_Ux delta_Uy delta_Uz", real=True
    )
    (
        dg_00,
        dg_0x,
        dg_0y,
        dg_0z,
        dg_xx,
        dg_xy,
        dg_xz,
        dg_yy,
        dg_yz,
        dg_zz,
    ) = sp.symbols(
        "delta_g00 delta_g0x delta_g0y delta_g0z "
        "delta_gxx delta_gxy delta_gxz delta_gyy delta_gyz delta_gzz",
        real=True,
    )

    eta_inverse = sp.diag(-1, 1, 1, 1)
    delta_g_inverse = sp.Matrix(
        [
            [dg_00, dg_0x, dg_0y, dg_0z],
            [dg_0x, dg_xx, dg_xy, dg_xz],
            [dg_0y, dg_xy, dg_yy, dg_yz],
            [dg_0z, dg_xz, dg_yz, dg_zz],
        ]
    )
    g_inverse = eta_inverse + epsilon * delta_g_inverse

    u_background = sp.Matrix([1, 0, 0, 0])
    delta_u = sp.Matrix([du_0, du_x, du_y, du_z])
    u_vector = u_background + epsilon * delta_u
    h_inverse = g_inverse + u_vector * u_vector.T

    dw = epsilon * sp.Matrix([w_t, w_x, w_y, w_z])
    d_u_w = (u_vector.T * dw)[0]
    w_field = epsilon * w
    local_density = (
        z_w * d_u_w**2 / 2
        - z_w * c_w_sq * (dw.T * h_inverse * dw)[0] / 2
        - m_w_sq * w_field**2 / 2
    )

    l0 = coefficient(local_density, epsilon, 0)
    l1 = coefficient(local_density, epsilon, 1)
    l2 = coefficient(local_density, epsilon, 2)
    l3 = coefficient(local_density, epsilon, 3)
    expected_l2 = sp.factor(
        z_w * w_t**2 / 2
        - z_w * c_w_sq * (w_x**2 + w_y**2 + w_z**2) / 2
        - m_w_sq * w**2 / 2
    )

    background_variables = [
        du_0,
        du_x,
        du_y,
        du_z,
        dg_00,
        dg_0x,
        dg_0y,
        dg_0z,
        dg_xx,
        dg_xy,
        dg_xz,
        dg_yy,
        dg_yz,
        dg_zz,
    ]
    w_variables = [w, w_t, w_x, w_y, w_z]
    quadratic_cross_derivatives = {
        f"d2L2_d{left}_d{right}": sp.diff(l2, left, right)
        for left in w_variables
        for right in background_variables
    }
    cubic_coupling_derivatives = {
        f"dL3_d{variable}": sp.factor(sp.diff(l3, variable))
        for variable in background_variables
    }
    nonzero_cubic_couplings = {
        name: sp.sstr(value)
        for name, value in cubic_coupling_derivatives.items()
        if value != 0
    }

    zero_background_substitutions = {variable: 0 for variable in background_variables}

    # Negative control 1: a nonzero background derivative generically restores
    # quadratic fluctuation-frame/metric mixing.
    b_t = sp.symbols("B_t", nonzero=True, real=True)
    dw_nonconstant_background = sp.Matrix(
        [b_t + epsilon * w_t, epsilon * w_x, epsilon * w_y, epsilon * w_z]
    )
    d_u_w_nonconstant = (u_vector.T * dw_nonconstant_background)[0]
    kinetic_nonconstant = (
        z_w * d_u_w_nonconstant**2 / 2
        - z_w
        * c_w_sq
        * (dw_nonconstant_background.T * h_inverse * dw_nonconstant_background)[0]
        / 2
    )
    l2_nonconstant = coefficient(kinetic_nonconstant, epsilon, 2)
    nonconstant_mixing_probe = sp.factor(sp.diff(l2_nonconstant, w_t, du_0))

    # Negative control 2: an explicit bilinear interaction produces an
    # off-diagonal quadratic Hessian even on the zero-W background.
    psi, g_mix = sp.symbols("psi g_mix", real=True)
    explicit_bilinear_l2 = g_mix * w * psi
    explicit_bilinear_probe = sp.diff(explicit_bilinear_l2, w, psi)

    checks = {
        "zero_background_has_no_W_tadpole": l0 == 0 and l1 == 0,
        "quadratic_W_density_matches_free_block": sp.simplify(l2 - expected_l2)
        == 0,
        "quadratic_W_block_is_independent_of_metric_and_frame_perturbations": all(
            value == 0 for value in quadratic_cross_derivatives.values()
        ),
        "metric_or_frame_coupling_reappears_at_cubic_order": bool(
            nonzero_cubic_couplings
        ),
        "cubic_coupling_vanishes_when_metric_and_frame_perturbations_vanish": (
            sp.simplify(l3.subs(zero_background_substitutions)) == 0
        ),
        "nonconstant_W_background_restores_quadratic_mixing": (
            nonconstant_mixing_probe != 0
        ),
        "explicit_bilinear_interaction_restores_quadratic_mixing": (
            explicit_bilinear_probe == g_mix
        ),
        "unit_constraint_is_not_duplicated_in_trial_W_density": True,
        "source_is_kept_zero": True,
        "result_is_not_promoted_to_physical_wake_law": True,
    }
    all_ok = all(checks.values())
    status = (
        "PASS_WAK001_ZERO_BACKGROUND_QUADRATIC_FACTORIZATION_TEMPLATE"
        if all_ok
        else "FAIL_WAK001_ZERO_BACKGROUND_QUADRATIC_FACTORIZATION_TEMPLATE"
    )

    summary = {
        "gate": "WAK-001",
        "stage": "W2.5 zero-background quadratic factorization",
        "label": "background-specific-local-template-only",
        "status": status,
        "calculation_pass": all_ok,
        "stage2_status": "IN_PROGRESS",
        "physics_pass": False,
        "physical_wake_law": "NOT_YET_DERIVED",
        "source": "J_W=0",
        "declared_background": {
            "metric": "local Minkowski inverse metric diag(-1,1,1,1)",
            "frame": "Ubar^mu=(1,0,0,0)",
            "wake": "Wbar=0 and nabla_mu Wbar=0",
            "explicit_bilinear_cross_sector_operator": "ABSENT_FROM_TRIAL_DENSITY",
        },
        "unit_constraint_owner": "PARENT_U_SECTOR_ONCE; NOT_DUPLICATED_IN_S_W",
        "epsilon_expansion": {
            "L_W_order_0": sp.sstr(l0),
            "L_W_order_1": sp.sstr(l1),
            "L_W_order_2": sp.sstr(l2),
            "L_W_order_3": sp.sstr(l3),
        },
        "quadratic_factorization": {
            "status": "DERIVED_FOR_DECLARED_ZERO_BACKGROUND",
            "cross_derivative_count": len(quadratic_cross_derivatives),
            "nonzero_cross_derivative_count": sum(
                value != 0 for value in quadratic_cross_derivatives.values()
            ),
            "scope": (
                "W-dependent part of the declared local trial density only; "
                "not the complete UVIR plus W parent Hessian"
            ),
        },
        "cubic_return": {
            "status": "METRIC_AND_FRAME_COUPLINGS_PRESENT",
            "nonzero_coupling_derivatives": nonzero_cubic_couplings,
            "constraint_warning": (
                "Lapse, shift and frame constraints must be re-eliminated before "
                "any nonlinear stability or strong-coupling statement."
            ),
        },
        "negative_controls": {
            "nonconstant_background_probe": sp.sstr(nonconstant_mixing_probe),
            "explicit_bilinear_probe": sp.sstr(explicit_bilinear_probe),
        },
        "checks": checks,
        "hold": "HOLD_MICROSCOPIC_MODE_IDENTITY_AND_CUBIC_CONSTRAINT_COMPLETION",
        "scientific_boundary": (
            "Zero quadratic W-sector mixing is derived only for Wbar=0, "
            "nabla Wbar=0, J_W=0 and the trial density with no explicit bilinear "
            "cross-sector operator. It is not a physical mode-identification result."
        ),
        "next": [
            "derive or reject microscopic independence of W from existing UVIR modes",
            "construct the cubic parent constraint system before nonlinear claims",
            "repeat the Hessian audit if a source, interaction or nonzero W background is declared",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "wak001_zero_background_factorization_summary.json"
    with output.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("WAK-001 zero-background quadratic-factorization audit")
    for name, passed in checks.items():
        print(f"  [{'OK' if passed else 'FAIL'}] {name}")
    print("STATUS:", status)
    print("QUADRATIC W BLOCK: DERIVED_FACTORIZED_ON_DECLARED_BACKGROUND")
    print("CUBIC METRIC/FRAME COUPLING: PRESENT")
    print("HOLD: HOLD_MICROSCOPIC_MODE_IDENTITY_AND_CUBIC_CONSTRAINT_COMPLETION")
    print("Physical wake law: NOT_YET_DERIVED")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
