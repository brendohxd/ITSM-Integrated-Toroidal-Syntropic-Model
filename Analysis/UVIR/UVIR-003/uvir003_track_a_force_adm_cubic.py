#!/usr/bin/env python3
"""UVIR-003 Track A: force-sector ADM expansion through quartic order.

Track A adopts the covariant rest-space Laplacian

    Delta_U psi = D_mu D^mu psi

and retains the exact non-analytic Y^(3/2) operator.  This audit expands the
force sector on the homogeneous zero-spatial-gradient FRW branch in
aether-unitary scalar ADM variables.  It verifies the quadratic action, the
cubic lapse/shift source from Q^2 plus the regulator, and the direct quartic
terms needed for the next Schur-complement calculation.

The exact Y^(3/2) term is retained as a nonlinear functional.  Its leading
zero-gradient contribution is constraint independent at cubic order, so it
does not contribute to J2 there; this does not make it an ordinary analytic
three-point vertex or a homogeneous perturbative S-matrix interaction.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs",
        help="Directory for the JSON summary.",
    )
    return parser.parse_args()


def require_zero(name: str, expression: sp.Expr) -> None:
    residual = sp.factor(sp.simplify(expression))
    if residual != 0:
        raise AssertionError(f"{name} failed: {residual}")


def coefficient(
    expression: sp.Expr, epsilon: sp.Symbol, order: int
) -> sp.Expr:
    return sp.expand(expression).coeff(epsilon, order)


def symbolic_audit() -> dict[str, object]:
    epsilon = sp.symbols("epsilon", positive=True)
    scale_factor = sp.symbols("a", positive=True)
    lapse, curvature = sp.symbols("delta_N R", real=True)
    pi_dot = sp.symbols("pi_dot", real=True)
    lap_pi = sp.symbols("lap_pi", real=True)
    grad_r_dot_grad_pi = sp.symbols(
        "grad_R_dot_grad_pi", real=True
    )
    grad_beta_dot_grad_pi = sp.symbols(
        "grad_beta_dot_grad_pi", real=True
    )
    grad_pi_sq = sp.symbols("grad_pi_sq", nonnegative=True)

    k_q, gamma, m_star_sq, amplitude = sp.symbols(
        "K_Q gamma M_star_sq A", positive=True
    )
    regulator_coefficient = sp.simplify(gamma / m_star_sq)

    # Aether-unitary scalar ADM ansatz:
    # N=1+epsilon*delta_N,
    # N_i=epsilon*partial_i beta,
    # h_ij=a^2 exp(2 epsilon R) delta_ij,
    # psi=psi_bar+epsilon*pi, with spatially constant psi_bar.
    #
    # For the conformally flat leaf,
    # D^2 psi = a^-2 exp(-2R)[partial^2 psi + partial R.partial psi].
    rest_laplacian = (
        scale_factor**-2
        * sp.exp(-2 * epsilon * curvature)
        * (
            epsilon * lap_pi
            + epsilon**2 * grad_r_dot_grad_pi
        )
    )
    volume = (
        (1 + epsilon * lapse)
        * scale_factor**3
        * sp.exp(3 * epsilon * curvature)
    )
    regulator_density = sp.simplify(
        -regulator_coefficient * volume * rest_laplacian**2 / 2
    )
    regulator_series = sp.series(
        regulator_density, epsilon, 0, 5
    ).removeO()

    regulator_l2 = sp.expand(
        -regulator_coefficient * lap_pi**2
        / (2 * scale_factor)
    )
    regulator_l3 = sp.expand(
        -regulator_coefficient
        / (2 * scale_factor)
        * (
            (lapse - curvature) * lap_pi**2
            + 2 * lap_pi * grad_r_dot_grad_pi
        )
    )
    regulator_l4 = sp.expand(
        -regulator_coefficient
        / (2 * scale_factor)
        * (
            (curvature**2 / 2 - lapse * curvature) * lap_pi**2
            + 2
            * (lapse - curvature)
            * lap_pi
            * grad_r_dot_grad_pi
            + grad_r_dot_grad_pi**2
        )
    )
    require_zero(
        "rest-space regulator quadratic expansion",
        coefficient(regulator_series, epsilon, 2) - regulator_l2,
    )
    require_zero(
        "rest-space regulator cubic expansion",
        coefficient(regulator_series, epsilon, 3) - regulator_l3,
    )
    require_zero(
        "rest-space regulator quartic expansion",
        coefficient(regulator_series, epsilon, 4) - regulator_l4,
    )

    # Q=n^mu nabla_mu psi=(dot psi-N^i partial_i psi)/N.
    # N^i partial_i psi starts at second perturbative order.
    shift_advection = (
        epsilon**2
        * scale_factor**-2
        * sp.exp(-2 * epsilon * curvature)
        * grad_beta_dot_grad_pi
    )
    q_invariant = (
        epsilon * pi_dot - shift_advection
    ) / (1 + epsilon * lapse)
    q_density = sp.simplify(k_q * volume * q_invariant**2 / 2)
    q_series = sp.series(q_density, epsilon, 0, 5).removeO()

    q_l2 = sp.expand(k_q * scale_factor**3 * pi_dot**2 / 2)
    q_l3 = sp.expand(
        k_q
        * scale_factor**3
        * (3 * curvature - lapse)
        * pi_dot**2
        / 2
        - k_q
        * scale_factor
        * pi_dot
        * grad_beta_dot_grad_pi
    )
    q_l4 = sp.expand(
        k_q
        * scale_factor**3
        / 2
        * (
            (
                sp.Rational(9, 2) * curvature**2
                - 3 * curvature * lapse
                + lapse**2
            )
            * pi_dot**2
            + 2
            * (lapse - curvature)
            * scale_factor**-2
            * pi_dot
            * grad_beta_dot_grad_pi
            + scale_factor**-4 * grad_beta_dot_grad_pi**2
        )
    )
    require_zero(
        "Q squared quadratic expansion",
        coefficient(q_series, epsilon, 2) - q_l2,
    )
    require_zero(
        "Q squared cubic expansion",
        coefficient(q_series, epsilon, 3) - q_l3,
    )
    require_zero(
        "Q squared quartic expansion",
        coefficient(q_series, epsilon, 4) - q_l4,
    )

    # The conformal factors cancel exactly from
    # N sqrt(h) Y^(3/2) in three spatial dimensions.  This calculation uses
    # epsilon>0 only to expose amplitude order; the functional remains
    # non-analytic at grad(pi)=0.
    y_invariant = (
        epsilon**2
        * scale_factor**-2
        * sp.exp(-2 * epsilon * curvature)
        * grad_pi_sq
    )
    y_density = sp.simplify(
        -amplitude * volume * y_invariant ** sp.Rational(3, 2)
    )
    y_expected = sp.expand(
        -amplitude
        * epsilon**3
        * (1 + epsilon * lapse)
        * grad_pi_sq ** sp.Rational(3, 2)
    )
    require_zero(
        "Y three-halves conformal cancellation",
        y_density - y_expected,
    )
    y_l3 = coefficient(y_expected, epsilon, 3)
    y_l4 = coefficient(y_expected, epsilon, 4)
    require_zero(
        "Y three-halves cubic constraint independence",
        sp.diff(y_l3, lapse),
    )

    force_l2 = sp.expand(q_l2 + regulator_l2)
    force_l3 = sp.expand(q_l3 + regulator_l3 + y_l3)
    force_l4_direct = sp.expand(q_l4 + regulator_l4 + y_l4)

    # J2 is the coefficient of the first-order constraint variable in L3.
    # The beta source is stated after spatial integration by parts:
    # -a K_Q pi_dot partial_i beta partial_i pi
    # -> beta [a K_Q partial_i(pi_dot partial_i pi)].
    lapse_j2_comoving = sp.expand(sp.diff(force_l3, lapse))
    expected_lapse_j2 = sp.expand(
        -k_q * scale_factor**3 * pi_dot**2 / 2
        - regulator_coefficient
        * lap_pi**2
        / (2 * scale_factor)
    )
    require_zero(
        "force lapse J2",
        lapse_j2_comoving - expected_lapse_j2,
    )
    beta_j2_integrated_by_parts = (
        "a*K_Q*partial_i(pi_dot*partial_i(pi))"
    )

    # Dividing the lapse source by a^3 and using
    # lap_comoving(pi)=a^2 lap_physical(pi) gives the local physical-density
    # form used alongside the finite-q constraint matrix.
    lapse_j2_physical = (
        "-K_Q*pi_dot^2/2"
        "-gamma*(lap_physical(pi))^2/(2*M_star^2)"
    )

    return {
        "track_a_action": {
            "status": "ADOPTED_FOR_DERIVATION",
            "Delta_U": "D_mu D^mu psi",
            "force_lagrangian": (
                "K_Q*Q^2/2-A*Y^(3/2)"
                "-gamma*(D_mu D^mu psi)^2/(2*M_star^2)"
            ),
            "background": (
                "flat FRW; U^mu=n^mu; spatially constant psi_bar"
            ),
            "interpretation": (
                "exact Y^(3/2) is retained; its perturbative force test is "
                "assigned to a declared local nonzero-gradient background"
            ),
        },
        "exact_adm_building_blocks": {
            "gauge": (
                "N=1+delta_N; N_i=partial_i beta; "
                "h_ij=a^2 exp(2R) delta_ij; psi=psi_bar+pi"
            ),
            "rest_laplacian": (
                "D^2 psi=a^-2 exp(-2R)"
                "*(partial^2 pi+partial_i R partial_i pi)"
            ),
            "Q": (
                "Q=[pi_dot-a^-2 exp(-2R)"
                "*partial_i beta partial_i pi]/N"
            ),
            "Y": "Y=a^-2 exp(-2R)*partial_i pi partial_i pi",
        },
        "verified_expansion": {
            "quadratic_force_density": str(force_l2),
            "cubic_force_density": str(force_l3),
            "direct_quartic_force_density": str(force_l4_direct),
            "regulator_quadratic": str(regulator_l2),
            "regulator_cubic": str(regulator_l3),
            "regulator_quartic": str(regulator_l4),
            "Q_squared_cubic": str(q_l3),
            "Q_squared_quartic": str(q_l4),
            "Y_three_halves_cubic": str(y_l3),
            "Y_three_halves_quartic": str(y_l4),
            "status": "VERIFIED_THROUGH_QUARTIC_ORDER",
        },
        "constraint_source": {
            "variables": (
                "delta_N and beta before finite-q scalar-shift normalization"
            ),
            "lapse_J2_comoving_density": str(lapse_j2_comoving),
            "lapse_J2_physical_density": lapse_j2_physical,
            "beta_J2_after_spatial_integration_by_parts": (
                beta_j2_integrated_by_parts
            ),
            "regulator_shift_J2": "0",
            "Y_three_halves_J2_at_zero_gradient": "0",
            "status": "PASS_FORCE_SECTOR_J2_COMPONENT",
        },
        "scientific_boundary": {
            "derived": (
                "complete homogeneous zero-gradient force-sector ADM "
                "expansion through direct quartic order and its J2 component"
            ),
            "not_derived": [
                (
                    "assembled J2 for the complete "
                    "g+U+Phi+alignment+psi scalar system"
                ),
                (
                    "nonzero-gradient local constraint reduction for the "
                    "exact Y^(3/2) branch"
                ),
                "gauge-regular physical 2-to-2 amplitude",
                "physical cutoff or unitarity bound",
            ],
            "nonanalytic_rule": (
                "Y^(3/2) is kept as an exact classical functional. Its "
                "ordinary perturbative force analysis is performed only "
                "about a declared nonzero spatial gradient."
            ),
        },
    }


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    audit = symbolic_audit()
    summary = {
        "gate": "UVIR-003",
        "stage": "B_TRACK_A_FORCE_ADM_CUBIC",
        "date": "2026-07-26",
        "track_a_status": "SELECTED",
        "calculation_status": "PASS",
        "subgate_status": "PASS_FORCE_SECTOR_J2_COMPONENT",
        "full_J2_status": "NOT_YET_ASSEMBLED",
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "symbolic_audit": audit,
        "next_required_calculation": [
            (
                "assemble the already fixed g+U+Phi+alignment cubic ADM "
                "vertices with this force-sector J2 component"
            ),
            (
                "form the complete finite-q J2 vector in the existing "
                "lapse/scalar-shift convention"
            ),
            (
                "evaluate the quartic Schur complement and direct quartic "
                "contact block on the regular physical scalar basis"
            ),
            (
                "separately reduce the exact Y^(3/2) sector on a declared "
                "local nonzero-gradient background"
            ),
        ],
    }

    output_path = (
        args.output_dir
        / "uvir003_track_a_force_adm_cubic_summary.json"
    )
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("Track A rest-space regulator: ADOPTED_FOR_DERIVATION")
    print("Force ADM expansion through quartic order: VERIFIED")
    print("Force-sector lapse/shift J2 component: VERIFIED")
    print("Exact Y^(3/2): RETAINED_NONANALYTIC_LOCAL_TRACK")
    print("Complete cosmological J2: NOT_YET_ASSEMBLED")
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_FORCE_SECTOR_J2_COMPONENT")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
