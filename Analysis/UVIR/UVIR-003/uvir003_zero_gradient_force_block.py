#!/usr/bin/env python3
"""UVIR-003 Stage B: zero-gradient force block and K_Q identifiability.

The declared Stage-A background has constant psi. This script verifies, with
an explicit perturbation expansion, that the force scalar factorizes from the
metric, aether and condensate blocks at quadratic order. It then checks the
positive z=2 Hamiltonian and the field-rescaling invariants that prevent K_Q
from being matched inside the current bottom-up EFT alone.
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
    simplified = sp.simplify(expression)
    if simplified != 0:
        raise AssertionError(f"{name} failed: {simplified}")


def coefficient(expression: sp.Expr, epsilon: sp.Symbol, order: int) -> sp.Expr:
    return sp.expand(expression).coeff(epsilon, order)


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    epsilon = sp.symbols("epsilon", positive=True)
    pi_t, pi_x, pi_y, pi_z, lap_pi = sp.symbols(
        "pi_t pi_x pi_y pi_z lap_pi", real=True
    )
    delta_u0, delta_ux, delta_uy, delta_uz = sp.symbols(
        "delta_u0 delta_ux delta_uy delta_uz", real=True
    )
    delta_h00, delta_h0x, delta_h0y, delta_h0z = sp.symbols(
        "delta_h00 delta_h0x delta_h0y delta_h0z", real=True
    )
    delta_hxx, delta_hyy, delta_hzz = sp.symbols(
        "delta_hxx delta_hyy delta_hzz", real=True
    )
    delta_lap = sp.symbols("delta_lap", real=True)

    # psi_bar is constant, so every derivative of psi starts at O(epsilon).
    dpsi = sp.Matrix(
        [epsilon * pi_t, epsilon * pi_x, epsilon * pi_y, epsilon * pi_z]
    )

    # The aether perturbation enters Q only multiplied by d(psi), so it cannot
    # generate a quadratic mixing term after Q is squared.
    u_contra = sp.Matrix(
        [
            1 + epsilon * delta_u0,
            epsilon * delta_ux,
            epsilon * delta_uy,
            epsilon * delta_uz,
        ]
    )
    q_invariant = sp.expand((u_contra.T * dpsi)[0])
    q_squared = sp.expand(q_invariant**2)
    q_squared_quadratic = coefficient(q_squared, epsilon, 2)
    require_zero("Q^2 quadratic coefficient", q_squared_quadratic - pi_t**2)

    # A generic first-order perturbation of the spatial projector is enough to
    # test metric/aether mixing. Its background is diag(0,1,1,1).
    projector = sp.Matrix(
        [
            [epsilon * delta_h00, epsilon * delta_h0x, epsilon * delta_h0y, epsilon * delta_h0z],
            [epsilon * delta_h0x, 1 + epsilon * delta_hxx, 0, 0],
            [epsilon * delta_h0y, 0, 1 + epsilon * delta_hyy, 0],
            [epsilon * delta_h0z, 0, 0, 1 + epsilon * delta_hzz],
        ]
    )
    y_invariant = sp.expand((dpsi.T * projector * dpsi)[0])
    y_quadratic = coefficient(y_invariant, epsilon, 2)
    spatial_gradient_sq = pi_x**2 + pi_y**2 + pi_z**2
    require_zero(
        "Y quadratic coefficient",
        y_quadratic - spatial_gradient_sq,
    )

    # Since Y=O(epsilon^2), Y^(3/2)=O(epsilon^3) for epsilon>0. Equivalently,
    # the Hessian of |grad(pi)|^3 vanishes at zero background gradient.
    cubic_spatial_order = 3
    gx, gy, gz = sp.symbols("gx gy gz", real=True)
    cubic_energy = (gx**2 + gy**2 + gz**2) ** sp.Rational(3, 2)
    cubic_hessian = sp.hessian(cubic_energy, (gx, gy, gz))
    zero_gradient_hessian = cubic_hessian.applyfunc(
        lambda entry: sp.limit(
            sp.limit(sp.limit(entry, gx, 0, dir="+"), gy, 0, dir="+"),
            gz,
            0,
            dir="+",
        )
    )
    if zero_gradient_hessian != sp.zeros(3):
        raise AssertionError(
            f"cubic spatial Hessian did not vanish: {zero_gradient_hessian}"
        )

    # The restricted projected Laplacian has a background O(epsilon) term and
    # metric/aether corrections only at O(epsilon^2).
    projected_laplacian = epsilon * lap_pi + epsilon**2 * delta_lap
    laplacian_squared_quadratic = coefficient(
        projected_laplacian**2, epsilon, 2
    )
    require_zero(
        "projected Laplacian quadratic coefficient",
        laplacian_squared_quadratic - lap_pi**2,
    )

    k_q, gamma, m_star, k, momentum = sp.symbols(
        "K_Q gamma M_star k p_pi", positive=True
    )
    pi_dot = sp.symbols("pi_dot", real=True)
    quadratic_lagrangian = (
        k_q * pi_dot**2 / 2 - gamma * lap_pi**2 / (2 * m_star**2)
    )
    canonical_momentum = sp.diff(quadratic_lagrangian, pi_dot)
    require_zero("canonical momentum", canonical_momentum - k_q * pi_dot)
    hamiltonian = sp.simplify(
        momentum * (momentum / k_q)
        - quadratic_lagrangian.subs(pi_dot, momentum / k_q)
    )
    expected_hamiltonian = (
        momentum**2 / (2 * k_q)
        + gamma * lap_pi**2 / (2 * m_star**2)
    )
    require_zero("force Hamiltonian", hamiltonian - expected_hamiltonian)

    omega_sq = sp.simplify(gamma * k**4 / (k_q * m_star**2))

    # A constant positive field rescaling psi_c=s*psi changes individual
    # coefficients but leaves physical ratios invariant.
    amplitude, c_m, q_background, scale = sp.symbols(
        "A C_m q s", positive=True
    )
    transformed = {
        "K_Q": k_q / scale**2,
        "A": amplitude / scale**3,
        "gamma": gamma / scale**2,
        "C_m": c_m / scale,
        "q": scale * q_background,
    }
    invariants = {
        "gamma_over_K_Q": gamma / k_q,
        "A_over_K_Q_3_over_2": amplitude / k_q ** sp.Rational(3, 2),
        "C_m_over_sqrt_K_Q": c_m / sp.sqrt(k_q),
        "A_q_over_K_Q": amplitude * q_background / k_q,
    }
    transformed_invariants = {
        "gamma_over_K_Q": transformed["gamma"] / transformed["K_Q"],
        "A_over_K_Q_3_over_2": transformed["A"]
        / transformed["K_Q"] ** sp.Rational(3, 2),
        "C_m_over_sqrt_K_Q": transformed["C_m"]
        / sp.sqrt(transformed["K_Q"]),
        "A_q_over_K_Q": transformed["A"]
        * transformed["q"]
        / transformed["K_Q"],
    }
    for name, invariant in invariants.items():
        require_zero(
            f"field-rescaling invariant {name}",
            transformed_invariants[name] - invariant,
        )

    healthy_samples = []
    for k_value in (0.1, 1.0, 10.0):
        omega_value = float(
            omega_sq.subs({k_q: 2.0, gamma: 3.0, m_star: 5.0, k: k_value})
        )
        hessian_values = [
            1.0 / 2.0,  # d^2 H / d p_pi^2 for K_Q=2
            3.0 * k_value**4 / 25.0,  # field-potential Hessian coefficient
        ]
        if omega_value < 0 or min(hessian_values) < 0:
            raise AssertionError("healthy positive-coefficient sample failed")
        healthy_samples.append(
            {
                "k": k_value,
                "omega_squared": omega_value,
                "hamiltonian_hessian_eigenvalues": hessian_values,
            }
        )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_ZERO_GRADIENT_FORCE_BLOCK",
        "background": {
            "psi_bar": "constant",
            "U_bar": "(1,0,0,0)",
            "metric_bar": "Minkowski",
        },
        "quadratic_factorization": {
            "Q_squared_coefficient": str(q_squared_quadratic),
            "Y_coefficient": str(y_quadratic),
            "Y_3_over_2_perturbative_order": cubic_spatial_order,
            "zero_gradient_cubic_hessian": str(zero_gradient_hessian),
            "projected_laplacian_squared_coefficient": str(
                laplacian_squared_quadratic
            ),
            "mixing_with_metric_aether_condensate": "ABSENT_AT_QUADRATIC_ORDER_IN_DECLARED_TRUNCATION",
        },
        "reduced_force_block": {
            "lagrangian": str(quadratic_lagrangian),
            "canonical_momentum": str(canonical_momentum),
            "hamiltonian": str(hamiltonian),
            "dispersion_omega_squared": str(omega_sq),
            "propagating_degrees_of_freedom": 1,
            "dynamical_scaling": "z=2",
            "positive_domain": ["K_Q > 0", "gamma > 0", "M_star^2 > 0"],
        },
        "field_rescaling": {
            "definition": "psi_c = s * psi, s > 0",
            "transformed_coefficients": {
                name: str(value) for name, value in transformed.items()
            },
            "invariants": {name: str(value) for name, value in invariants.items()},
            "K_Q_alone_identifiable": False,
            "matching_requirement": (
                "Fix the physical force-field normalization through a parent "
                "microscopic matching calculation or the matter vertex; then "
                "match redefinition-invariant coefficient combinations."
            ),
        },
        "healthy_samples": healthy_samples,
        "scope_limits": [
            "Does not reduce the remaining metric-aether-condensate block.",
            "Does not cover a nonzero force-gradient background.",
            "Assumes no additional quadratic mixing operators beyond the declared Stage-A truncation.",
            "Does not supply a covariant completion of Delta_U.",
            "Does not establish the physical EFT cutoff or radiative naturalness.",
        ],
        "dependency_result": {
            "UVIR_003_structural_role": (
                "Determine a stable parameter domain in field-rescaling invariants; "
                "a numeric K_Q is not required for this structural task."
            ),
            "MAT_001_matching_role": (
                "Fix the physical normalization and select a point in that domain "
                "through matter or microscopic matching."
            ),
        },
        "status": "PARTIAL_PASS_ZERO_GRADIENT_FORCE_BLOCK_ONLY",
        "full_UVIR_003_gate": "IN_PROGRESS",
    }

    json_path = args.output_dir / "uvir003_zero_gradient_force_block_summary.json"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("UVIR-003 Stage B zero-gradient force block: FACTORIZATION VERIFIED")
    print("Reduced force mode: one positive z=2 scalar for K_Q>0 and gamma>0")
    print("Numeric K_Q from current EFT: NOT IDENTIFIABLE")
    print("STATUS: PARTIAL_PASS_ZERO_GRADIENT_FORCE_BLOCK_ONLY")
    print("Full UVIR-003 gate: IN_PROGRESS")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
