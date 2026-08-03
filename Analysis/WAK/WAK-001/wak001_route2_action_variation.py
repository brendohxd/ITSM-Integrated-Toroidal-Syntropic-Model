#!/usr/bin/env python3
"""WAK-001 W2.1 local action-variation identity audit.

This checks one constrained conservative Route-II calculation family. It is a
symbolic local-background audit, not a derived ITSM wake action or physics pass.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import sympy as sp


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def is_zero(expression: sp.Expr) -> bool:
    return sp.simplify(expression) == 0


def main() -> None:
    args = parse_args()

    Z, c2, mass2 = sp.symbols("Z_W c_W_sq M_W_sq", positive=True, finite=True)
    field, field_t = sp.symbols("W W_t", real=True, finite=True)
    field_x, field_y, field_z = sp.symbols(
        "W_x W_y W_z", real=True, finite=True
    )
    omega2, wave_number2 = sp.symbols("omega_sq k_sq", nonnegative=True)
    lagrange = sp.symbols("lambda_U", real=True, finite=True)

    metric_inverse = sp.diag(-1, 1, 1, 1)
    metric = metric_inverse
    frame_up = sp.Matrix([1, 0, 0, 0])
    frame_down = metric * frame_up
    projector_up = metric_inverse + frame_up * frame_up.T
    gradient_down = sp.Matrix([field_t, field_x, field_y, field_z])

    frame_derivative = (frame_up.T * gradient_down)[0]
    spatial_gradient_sq = (gradient_down.T * projector_up * gradient_down)[0]
    lagrangian = sp.expand(
        sp.Rational(1, 2) * Z * frame_derivative**2
        - sp.Rational(1, 2) * Z * c2 * spatial_gradient_sq
        - sp.Rational(1, 2) * mass2 * field**2
    )
    expected_lagrangian = sp.Rational(1, 2) * (
        Z * field_t**2
        - Z * c2 * (field_x**2 + field_y**2 + field_z**2)
        - mass2 * field**2
    )

    momentum = sp.diff(lagrangian, field_t)
    hamiltonian = sp.expand(momentum * field_t - lagrangian)
    expected_hamiltonian = sp.Rational(1, 2) * (
        Z * field_t**2
        + Z * c2 * (field_x**2 + field_y**2 + field_z**2)
        + mass2 * field**2
    )

    dispersion_residual = Z * omega2 - Z * c2 * wave_number2 - mass2
    expected_omega2 = c2 * wave_number2 + mass2 / Z

    # Derive the rest-frame metric and frame variations from the constrained
    # density while holding contravariant U^mu independent. The multiplier
    # enforces g_{mu nu} U^mu U^nu = -1.
    inverse_g00, frame_0 = sp.symbols("g00_inv U0", nonzero=True, finite=True)
    covariant_g00 = 1 / inverse_g00
    constrained_density = (
        sp.Rational(1, 2) * Z * (frame_0 * field_t) ** 2
        - sp.Rational(1, 2)
        * Z
        * c2
        * (inverse_g00 + frame_0**2)
        * field_t**2
        - sp.Rational(1, 2)
        * Z
        * c2
        * (field_x**2 + field_y**2 + field_z**2)
        - sp.Rational(1, 2) * mass2 * field**2
        + lagrange * (covariant_g00 * frame_0**2 + 1)
    )
    rest_substitution = {inverse_g00: -1, frame_0: 1}
    frame_equation_0 = sp.simplify(
        sp.diff(constrained_density, frame_0).subs(rest_substitution)
    )
    lagrange_solution = sp.solve(frame_equation_0, lagrange)[0]

    rest_constrained_density = sp.simplify(
        constrained_density.subs(rest_substitution).subs(lagrange, lagrange_solution)
    )
    hilbert_t00 = sp.simplify(
        (
            -2 * sp.diff(constrained_density, inverse_g00)
            + covariant_g00 * constrained_density
        )
        .subs(rest_substitution)
        .subs(lagrange, lagrange_solution)
    )
    hilbert_without_constraint_response = sp.simplify(
        (
            Z * c2 * field_t**2
            - lagrangian
        )
    )
    missing_response = sp.simplify(
        hilbert_without_constraint_response - hamiltonian
    )
    expected_missing_response = -Z * (1 - c2) * field_t**2

    frame_response_down = sp.simplify(
        Z * (1 - c2) * frame_derivative * gradient_down
        + 2 * lagrange_solution * frame_down
    )
    frame_temporal_residual = sp.simplify(frame_response_down[0])
    frame_spatial_response = tuple(
        sp.simplify(frame_response_down[index]) for index in range(1, 4)
    )

    static_susceptibility = 1 / (Z * c2 * wave_number2 + mass2)
    existing_static_form = 1 / (Z * expected_omega2)

    sample = {
        Z: sp.Rational(6, 5),
        c2: sp.Rational(9, 25),
        mass2: sp.Rational(4, 5),
        field: sp.Rational(7, 10),
        field_t: sp.Rational(2, 5),
        field_x: sp.Rational(3, 10),
        field_y: sp.Rational(-1, 5),
        field_z: sp.Rational(1, 10),
        wave_number2: sp.Rational(9, 4),
    }
    sample_energy = sp.simplify(hamiltonian.subs(sample))
    sample_missing_response = sp.simplify(missing_response.subs(sample))
    sample_spatial_response = tuple(
        sp.simplify(component.subs(sample)) for component in frame_spatial_response
    )

    checks = {
        "unit_frame_normalization": is_zero((frame_up.T * metric * frame_up)[0] + 1),
        "rest_projector_is_spatial": projector_up == sp.diag(0, 1, 1, 1),
        "covariant_density_reduces_to_declared_rest_lagrangian": is_zero(
            lagrangian - expected_lagrangian
        ),
        "canonical_momentum_is_Z_times_W_t": is_zero(momentum - Z * field_t),
        "canonical_hamiltonian_matches_positive_quadratic_form": is_zero(
            hamiltonian - expected_hamiltonian
        ),
        "sample_hamiltonian_is_positive": bool(sample_energy > 0),
        "dispersion_matches_free_field_screen": is_zero(
            dispersion_residual.subs(omega2, expected_omega2)
        ),
        "constraint_multiplier_solves_temporal_frame_equation": is_zero(
            frame_temporal_residual
        ),
        "constrained_density_returns_free_rest_lagrangian": is_zero(
            rest_constrained_density - lagrangian
        ),
        "hilbert_T00_matches_canonical_energy_with_constraint_response": is_zero(
            hilbert_t00 - hamiltonian
        ),
        "negative_control_omitting_constraint_response_mismatches_energy": (
            is_zero(missing_response - expected_missing_response)
            and sample_missing_response != 0
        ),
        "generic_spatial_gradient_sources_shared_frame_equation": any(
            component != 0 for component in sample_spatial_response
        ),
        "static_susceptibility_matches_free_field_screen": is_zero(
            static_susceptibility - existing_static_form
        ),
        "luminal_limit_removes_wake_frame_response": all(
            is_zero(component.subs(c2, 1)) for component in frame_response_down
        ),
    }
    all_ok = all(checks.values())
    status = (
        "PASS_WAK001_W2_1_LOCAL_VARIATION_IDENTITIES"
        if all_ok
        else "FAIL_WAK001_W2_1_LOCAL_VARIATION_IDENTITIES"
    )

    summary: dict[str, Any] = {
        "gate": "WAK-001",
        "stage": "W2.1 local constrained action variation",
        "label": "symbolic-local-action-template-only",
        "status": status,
        "calculation_pass": all_ok,
        "stage2_status": "IN_PROGRESS",
        "physics_pass": False,
        "physical_wake_law": "NOT_YET_DERIVED",
        "source": "J_W=0",
        "conventions": {
            "metric_signature": "(-,+,+,+)",
            "frame_constraint": "g_mu_nu U^mu U^nu = -1",
            "projector": "h^{mu nu} = g^{mu nu} + U^mu U^nu",
            "metric_variation": "contravariant U^mu held independent; lambda_U enforces unit norm",
        },
        "variation_identities": {
            "field_equation": (
                "nabla_mu[Z_W (D_U W) U^mu - Z_W c_W^2 h^{mu nu} "
                "nabla_nu W] + M_W^2 W = 0"
            ),
            "frame_response_covector": (
                "R_mu^(W) = Z_W (1-c_W^2) (D_U W) nabla_mu W "
                "+ 2 lambda_U U_mu"
            ),
            "metric_stress_with_constraint": (
                "T_mu_nu^(W+constraint) = Z_W c_W^2 nabla_mu W nabla_nu W "
                "+ g_mu_nu L_W + 2 lambda_U U_mu U_nu"
            ),
            "rest_constraint_multiplier": str(lagrange_solution),
            "rest_hamiltonian": str(hamiltonian),
            "missing_T00_if_constraint_response_omitted": str(missing_response),
            "spatial_frame_response": [str(value) for value in frame_spatial_response],
        },
        "sample_exact": {
            "hamiltonian": str(sample_energy),
            "missing_constraint_response": str(sample_missing_response),
            "spatial_frame_response": [str(value) for value in sample_spatial_response],
        },
        "checks": checks,
        "hold": "HOLD_COUPLED_FRAME_COMPLETION_AND_MODE_INVENTORY",
        "scientific_boundary": (
            "The constrained local identities and rest-frame energy accounting pass. "
            "A generic W gradient sources the shared U equation, so allocation of "
            "constraint stress and independence from existing Phi/U/psi modes require "
            "the coupled parent action. No exchange current or dissipation is derived."
        ),
        "next": [
            "perform W2.5 coupled mode inventory against Phi, U and psi",
            "fix parent-action ownership of the unit constraint before naming a separate T_W",
            "retain J_W=0 and do not open W2.6 exchange until mode independence is established",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "wak001_route2_action_variation_summary.json"
    with output.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("WAK-001 W2.1 local constrained action-variation audit")
    for name, passed in checks.items():
        print(f"  [{'OK' if passed else 'FAIL'}] {name}")
    print("STATUS:", status)
    print("STAGE-2: IN_PROGRESS")
    print("HOLD: HOLD_COUPLED_FRAME_COMPLETION_AND_MODE_INVENTORY")
    print("Physical wake law: NOT_YET_DERIVED")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
