#!/usr/bin/env python3
"""Independent symbolic audit of the frozen TOP-X4 X4-I1C background.

Constructs the five-dimensional Einstein tensor directly from the metric and
derives the homogeneous matter equations and stress components from the
reduced action. It does not import equations from the numerical integrator.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


PASS_STATUS = "PASS_TOPX4_A1_INDEPENDENT_SYMBOLIC_AUDIT"
FAIL_STATUS = "FAIL_TOPX4_A1_INDEPENDENT_SYMBOLIC_AUDIT"


def add_check(checks: list[dict[str, Any]], name: str, residual: sp.Expr) -> None:
    simplified = sp.factor(sp.simplify(residual))
    checks.append({"name": name, "ok": bool(simplified == 0), "residual": str(simplified)})


def einstein_tensor() -> tuple[list[list[sp.Expr]], tuple[sp.Symbol, ...], sp.Expr, sp.Expr]:
    t, x1, x2, x3, y = sp.symbols("t x1 x2 x3 y", real=True)
    coordinates = (t, x1, x2, x3, y)
    a = sp.Function("a", positive=True)(t)
    b = sp.Function("b", positive=True)(t)
    metric = sp.diag(-1, a**2, a**2, a**2, b**2)
    inverse = metric.inv()
    dimension = len(coordinates)

    gamma = [[[sp.S.Zero for _ in range(dimension)] for _ in range(dimension)] for _ in range(dimension)]
    for upper in range(dimension):
        for left in range(dimension):
            for right in range(dimension):
                gamma[upper][left][right] = sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        inverse[upper, lower]
                        * (
                            sp.diff(metric[lower, right], coordinates[left])
                            + sp.diff(metric[lower, left], coordinates[right])
                            - sp.diff(metric[left, right], coordinates[lower])
                        )
                        for lower in range(dimension)
                    )
                )

    ricci = [[sp.S.Zero for _ in range(dimension)] for _ in range(dimension)]
    for left in range(dimension):
        for right in range(dimension):
            expression = sp.S.Zero
            for lam in range(dimension):
                expression += sp.diff(gamma[lam][left][right], coordinates[lam])
                expression -= sp.diff(gamma[lam][left][lam], coordinates[right])
                for sigma in range(dimension):
                    expression += gamma[lam][left][right] * gamma[sigma][lam][sigma]
                    expression -= gamma[sigma][left][lam] * gamma[lam][right][sigma]
            ricci[left][right] = sp.simplify(expression)

    scalar = sp.simplify(
        sum(inverse[left, right] * ricci[left][right] for left in range(dimension) for right in range(dimension))
    )
    einstein = [
        [sp.simplify(ricci[left][right] - sp.Rational(1, 2) * metric[left, right] * scalar)
         for right in range(dimension)]
        for left in range(dimension)
    ]
    return einstein, coordinates, a, b


def matter_audit(checks: list[dict[str, Any]]) -> None:
    t = sp.symbols("t", real=True)
    a = sp.Function("a", positive=True)(t)
    b = sp.Function("b", positive=True)(t)
    lapse = sp.Function("N", positive=True)(t)
    rho = sp.Function("rho", positive=True)(t)
    theta = sp.Function("theta", real=True)(t)
    chi = sp.Function("chi", real=True)(t)
    m_phi2, m_chi2, lambda_phi, lambda_chi, g5, u0, winding = sp.symbols(
        "m_phi2 m_chi2 lambda_phi lambda_chi g5 u0 w", real=True
    )

    s = rho**2 / 2
    u_phi = u0 + m_phi2 * s + lambda_phi * s**2 / 2
    w_chi = m_chi2 * chi**2 / 2 + lambda_chi * chi**4 / 24
    interaction = g5 * rho**2 * chi**2 / 4
    kinetic_time = (sp.diff(rho, t) ** 2 + rho**2 * sp.diff(theta, t) ** 2 + sp.diff(chi, t) ** 2) / 2
    kinetic_winding = rho**2 * winding**2 / (2 * b**2)
    potential = u_phi + w_chi + interaction
    lagrangian = lapse * a**3 * b * (kinetic_time / lapse**2 - kinetic_winding - potential)

    gauge = {lapse: 1, sp.diff(lapse, t): 0}
    expansion = 3 * sp.diff(a, t) / a + sp.diff(b, t) / b

    def euler_lagrange(field: sp.Expr) -> sp.Expr:
        return sp.diff(sp.diff(lagrangian, sp.diff(field, t)), t) - sp.diff(lagrangian, field)

    rho_derived = sp.simplify(euler_lagrange(rho).subs(gauge) / (a**3 * b))
    rho_target = (
        sp.diff(rho, t, 2)
        + expansion * sp.diff(rho, t)
        - rho * sp.diff(theta, t) ** 2
        + winding**2 * rho / b**2
        + m_phi2 * rho
        + lambda_phi * rho**3 / 2
        + g5 * rho * chi**2 / 2
    )
    add_check(checks, "matter_radial_euler_lagrange", rho_derived - rho_target)

    phase_derived = sp.simplify(euler_lagrange(theta).subs(gauge))
    phase_target = sp.diff(a**3 * b * rho**2 * sp.diff(theta, t), t)
    add_check(checks, "global_phase_euler_lagrange", phase_derived - phase_target)

    chi_derived = sp.simplify(euler_lagrange(chi).subs(gauge) / (a**3 * b))
    chi_target = (
        sp.diff(chi, t, 2)
        + expansion * sp.diff(chi, t)
        + m_chi2 * chi
        + lambda_chi * chi**3 / 6
        + g5 * rho**2 * chi / 2
    )
    add_check(checks, "matter_proxy_euler_lagrange", chi_derived - chi_target)

    energy_derived = sp.simplify((-sp.diff(lagrangian, lapse) / (a**3 * b)).subs(gauge))
    energy_target = kinetic_time + kinetic_winding + potential
    add_check(checks, "lapse_variation_energy_density", energy_derived - energy_target)

    pressure_a_derived = sp.simplify((sp.diff(lagrangian, a) / (3 * lapse * a**2 * b)).subs(gauge))
    pressure_a_target = kinetic_time - kinetic_winding - potential
    add_check(checks, "scale_factor_variation_pressure_a", pressure_a_derived - pressure_a_target)

    pressure_y_derived = sp.simplify((sp.diff(lagrangian, b) / (lapse * a**3)).subs(gauge))
    pressure_y_target = kinetic_time + kinetic_winding - potential
    add_check(checks, "circle_scale_variation_pressure_y", pressure_y_derived - pressure_y_target)


def main() -> int:
    checks: list[dict[str, Any]] = []
    einstein, coordinates, a, b = einstein_tensor()
    t = coordinates[0]
    h_a = sp.diff(a, t) / a
    h_b = sp.diff(b, t) / b

    target_00 = 3 * h_a * (h_a + h_b)
    target_a = -2 * sp.diff(h_a, t) - sp.diff(h_b, t) - 3 * h_a**2 - 2 * h_a * h_b - h_b**2
    target_y = -3 * sp.diff(h_a, t) - 6 * h_a**2
    add_check(checks, "einstein_00_hamiltonian", einstein[0][0] - target_00)
    add_check(checks, "einstein_observed_space_pressure", einstein[1][1] / a**2 - target_a)
    add_check(checks, "einstein_circle_pressure", einstein[4][4] / b**2 - target_y)

    matter_audit(checks)

    all_ok = all(check["ok"] for check in checks)
    result = {
        "schema": "ITSM_TOPX4_A1_SYMBOLIC_v1",
        "route": "TOP-X4_KK-001",
        "parent": "X4-I1C_bulk_scalar_control",
        "status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "physics_pass": False,
        "gate_effect": "NONE",
        "audit_independence": "metric tensor construction and action variation; no import from numerical RHS",
        "checks": checks,
        "checks_passed": sum(check["ok"] for check in checks),
        "checks_total": len(checks),
        "derived_claims": [],
        "explicit_nonclaims": [
            "no perturbation or pole calculation",
            "no radion stabilization",
            "no physical-matter universality",
            "no nonzero transfer-current derivation",
            "no phenomenology",
        ],
    }

    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "topx4_a1_symbolic_audit_summary.json"
    payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output_path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    output_path.with_suffix(output_path.suffix + ".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="ascii", newline="\n"
    )

    print(result["status"])
    print(f"checks={result['checks_passed']}/{result['checks_total']}")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={output_path}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
