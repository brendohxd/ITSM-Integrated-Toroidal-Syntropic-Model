#!/usr/bin/env python3
"""UVIR-003 Stage B: screen background completions for scalar ADM work.

The declared finite-density Minkowski condensate needs a support sector with
negative enthalpy.  This script checks the minimal covariant candidates and
records the least-assumptive on-shell route for the next calculation.

This is a route-selection audit.  It does not solve the selected FRW
background or perform the scalar ADM constraint reduction.
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
        help="Directory for the machine-readable background screen.",
    )
    return parser.parse_args()


def require_zero(name: str, expression: sp.Expr) -> None:
    result = sp.simplify(expression)
    if result != 0:
        raise AssertionError(f"{name} failed: {result}")


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Exact Minkowski support requirement.
    # ------------------------------------------------------------------
    s, mu = sp.symbols("s mu", positive=True)
    condensate_enthalpy = s * mu**2
    required_support_enthalpy = -condensate_enthalpy
    require_zero(
        "exact Minkowski support condition",
        condensate_enthalpy + required_support_enthalpy,
    )

    # A constant vacuum term always has rho+p=0.
    lambda_vac = sp.symbols("Lambda_vac", real=True)
    vacuum_rho = lambda_vac
    vacuum_pressure = -lambda_vac
    require_zero(
        "vacuum enthalpy",
        vacuum_rho + vacuum_pressure,
    )
    require_zero(
        "vacuum term leaves condensate enthalpy",
        condensate_enthalpy + vacuum_rho + vacuum_pressure
        - condensate_enthalpy,
    )

    # ------------------------------------------------------------------
    # 2. Minimal local P(X) reservoir.
    #
    # Convention: signature (-,+,+,+) and
    # X=-g^{mu nu} partial_mu chi partial_nu chi / 2 > 0
    # on a homogeneous timelike background.
    #
    # rho_R+p_R = 2 X P_X.
    # The quadratic fluctuation is
    # 1/2 (P_X+2 X P_XX) dot(pi)^2 - 1/2 P_X |grad pi|^2.
    # ------------------------------------------------------------------
    x = sp.symbols("X_R", positive=True)
    p_x, p_xx = sp.symbols("P_X P_XX", real=True)
    px_enthalpy = 2 * x * p_x
    required_px = sp.simplify(required_support_enthalpy / (2 * x))
    require_zero(
        "P(X) support assignment",
        px_enthalpy.subs(p_x, required_px) - required_support_enthalpy,
    )

    kinetic_coefficient = sp.simplify(p_x + 2 * x * p_xx)
    gradient_coefficient = p_x
    required_gradient_coefficient = sp.simplify(
        gradient_coefficient.subs(p_x, required_px)
    )
    if required_px.is_negative is not True:
        raise AssertionError(
            "Required P_X should be negative for positive s, mu and X_R."
        )
    if required_gradient_coefficient.is_negative is not True:
        raise AssertionError(
            "Required spatial-gradient coefficient should be negative."
        )

    # The ghost-condensate point P_X=0 has vanishing enthalpy.  Higher-
    # derivative operators may stabilize its k^4 dispersion but cannot turn
    # this zero into the required nonzero support enthalpy by themselves.
    ghost_point_enthalpy = sp.simplify(px_enthalpy.subs(p_x, 0))
    require_zero("ghost-condensate-point enthalpy", ghost_point_enthalpy)

    # ------------------------------------------------------------------
    # 3. Self-consistent flat-FRW route.
    # ------------------------------------------------------------------
    m_planck, hubble, hubble_dot = sp.symbols(
        "M_P H H_dot", real=True
    )
    rho_total, pressure_total = sp.symbols(
        "rho_total p_total", real=True
    )
    friedmann_energy_residual = sp.simplify(
        3 * m_planck**2 * hubble**2 - rho_total
    )
    friedmann_enthalpy_residual = sp.simplify(
        -2 * m_planck**2 * hubble_dot
        - (rho_total + pressure_total)
    )

    # For condensate number density n, an isolated U(1) sector obeys
    # dot(n)+3Hn=0.  If a separately declared charge-transfer source S_N is
    # present, exact constant n in an expanding background requires S_N=3Hn.
    number_density, number_density_dot, number_source = sp.symbols(
        "n n_dot S_N", real=True
    )
    charge_balance = sp.simplify(
        number_density_dot + 3 * hubble * number_density - number_source
    )
    isolated_number_density_dot = sp.solve(
        sp.Eq(charge_balance.subs(number_source, 0), 0),
        number_density_dot,
    )[0]
    constant_density_source = sp.solve(
        sp.Eq(charge_balance.subs(number_density_dot, 0), 0),
        number_source,
    )[0]
    require_zero(
        "isolated charge dilution",
        isolated_number_density_dot + 3 * hubble * number_density,
    )
    require_zero(
        "constant-density source",
        constant_density_source - 3 * hubble * number_density,
    )

    route_matrix = [
        {
            "candidate": "constant_vacuum_energy",
            "verdict": "REJECTED",
            "reason": (
                "rho_R+p_R=0, so it cannot cancel the positive finite-density "
                "condensate enthalpy."
            ),
        },
        {
            "candidate": "minimal_local_shift_symmetric_P_of_X_scalar",
            "verdict": "REJECTED_AS_HEALTHY_EXACT_MINKOWSKI_SUPPORT",
            "reason": (
                "Negative support enthalpy requires P_X<0, whereas the "
                "two-derivative spatial-gradient coefficient is P_X and must "
                "be positive for short-wavelength gradient health."
            ),
        },
        {
            "candidate": "ghost_condensate_point_P_X_equals_zero",
            "verdict": "REJECTED_AS_INSUFFICIENT",
            "reason": (
                "The point has rho_R+p_R=0; a k^4 regulator does not itself "
                "supply the missing nonzero background enthalpy."
            ),
        },
        {
            "candidate": "rigid_or_external_support_stress",
            "verdict": "DECOUPLING_ONLY",
            "reason": (
                "It may define a local approximation but supplies no "
                "action-derived lapse/shift response for the full ADM gate."
            ),
        },
        {
            "candidate": "higher_derivative_NEC_violating_support",
            "verdict": "OPEN_NEW_THEORY_REQUIRED",
            "reason": (
                "Stable examples require additional higher-derivative or "
                "nonminimal structure and an independent constraint and "
                "stability audit."
            ),
        },
        {
            "candidate": "self_consistent_evolving_flat_FRW_background",
            "verdict": "SELECTED_ROUTE_BACKGROUND_NOT_YET_SOLVED",
            "reason": (
                "It keeps the declared sectors and satisfies Einstein's "
                "background equations dynamically without postulating an "
                "unvalidated negative-enthalpy support field."
            ),
        },
    ]

    summary = {
        "gate": "UVIR-003",
        "stage": "B_BACKGROUND_COMPLETION_SCREEN",
        "calculation_status": "PASS",
        "exact_minkowski_requirement": {
            "condensate_enthalpy": str(condensate_enthalpy),
            "required_support_enthalpy": str(required_support_enthalpy),
        },
        "minimal_P_of_X_screen": {
            "convention": (
                "X_R=-(partial chi)^2/2>0 on the timelike background"
            ),
            "support_enthalpy": str(px_enthalpy),
            "required_P_X": str(required_px),
            "quadratic_time_kinetic_coefficient": str(kinetic_coefficient),
            "quadratic_spatial_gradient_coefficient": str(
                gradient_coefficient
            ),
            "required_spatial_gradient_coefficient": str(
                required_gradient_coefficient
            ),
            "health_conditions": [
                "P_X+2*X_R*P_XX>0",
                "P_X>0",
            ],
            "verdict": (
                "NO_HEALTHY_TWO_DERIVATIVE_P_OF_X_EXACT_MINKOWSKI_SUPPORT"
            ),
        },
        "ghost_condensate_point": {
            "P_X": "0",
            "enthalpy": str(ghost_point_enthalpy),
            "verdict": "INSUFFICIENT_FOR_REQUIRED_NONZERO_ENTHALPY",
        },
        "selected_route": {
            "name": "SELF_CONSISTENT_EVOLVING_FLAT_FRW_BACKGROUND",
            "friedmann_energy_equation_zero": str(
                friedmann_energy_residual
            ),
            "friedmann_enthalpy_equation_zero": str(
                friedmann_enthalpy_residual
            ),
            "charge_balance_zero": str(charge_balance),
            "isolated_charge_law": (
                f"n_dot={isolated_number_density_dot}"
            ),
            "constant_density_requires": (
                f"S_N={constant_density_source}"
            ),
            "status": "ROUTE_SELECTED_BACKGROUND_NOT_YET_SOLVED",
        },
        "route_matrix": route_matrix,
        "scientific_boundary": (
            "The screen rejects an unspecified minimal reservoir as an exact "
            "Minkowski counterstress. It does not reject the reservoir "
            "ontology or prove that all higher-derivative NEC-violating "
            "theories are unstable."
        ),
        "next_required_calculation": [
            "derive the homogeneous flat-FRW equations for a(t), rho(t), Theta(t), U^mu and any declared reservoir variables",
            "keep condensate charge conserved or declare a distinct charge-transfer source S_N; Q_syn^nu alone is not automatically S_N",
            "construct and verify at least one on-shell evolving background branch",
            "perform the metric-aether-condensate scalar constraint reduction on that branch",
            "use a subhorizon limit only for k/a>>H; reserve the strict low-k cosmological audit for the full perturbation system",
        ],
        "adm_reduction_status": (
            "BLOCKED_PENDING_SOLVED_ON_SHELL_FRW_BACKGROUND"
        ),
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
    }

    output_path = args.output_dir / "uvir003_background_completion_summary.json"
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("UVIR-003 background-completion identities: VERIFIED")
    print("Vacuum-energy exact Minkowski support: REJECTED")
    print("Healthy two-derivative P(X) exact Minkowski support: REJECTED")
    print("Rigid support: DECOUPLING_ONLY")
    print("Selected route: SELF_CONSISTENT_EVOLVING_FLAT_FRW_BACKGROUND")
    print("Background solution: NOT_YET_DERIVED")
    print("Scalar ADM reduction: BLOCKED_PENDING_SOLVED_ON_SHELL_FRW_BACKGROUND")
    print("Full UVIR-003 gate: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_BACKGROUND_ROUTE_SELECTION")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
