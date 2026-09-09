#!/usr/bin/env python3
"""Independent symbolic Einstein-frame audit for TOP-X4 A2.

Builds the five-dimensional Ricci scalar directly for a time-dependent radion
over a flat four-dimensional Einstein-frame metric, removes the explicit total
derivative, and independently checks zero-mode and KK normalization factors.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


PASS_STATUS = "PASS_TOPX4_A2_RADION_SYMBOLIC_IDENTITIES_ONLY"
FAIL_STATUS = "FAIL_TOPX4_A2_RADION_SYMBOLIC_IDENTITIES"


def add_check(checks: list[dict[str, Any]], name: str, residual: sp.Expr, **details: Any) -> None:
    simplified = sp.factor(sp.simplify(residual))
    checks.append({"name": name, "ok": bool(simplified == 0), "residual": str(simplified), **details})


def ricci_scalar_for_metric(metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]) -> sp.Expr:
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

    return sp.simplify(
        sum(inverse[left, right] * ricci[left][right] for left in range(dimension) for right in range(dimension))
    )


def main() -> int:
    checks: list[dict[str, Any]] = []
    t, x1, x2, x3, y = sp.symbols("t x1 x2 x3 y", real=True)
    coordinates = (t, x1, x2, x3, y)
    u = sp.Function("u", real=True)(t)
    radius_ref = sp.symbols("R_ref", positive=True)
    metric = sp.diag(
        -sp.exp(-u),
        sp.exp(-u),
        sp.exp(-u),
        sp.exp(-u),
        radius_ref**2 * sp.exp(2 * u),
    )
    determinant_factor = sp.simplify(sp.sqrt(-metric.det()))
    add_check(
        checks,
        "five_dimensional_measure",
        determinant_factor - radius_ref * sp.exp(-u),
        expected="sqrt(-G)=R_ref exp(-u)",
    )

    ricci_scalar = ricci_scalar_for_metric(metric, coordinates)
    raw_eh_density = sp.simplify(determinant_factor * ricci_scalar)
    u_ddot = sp.diff(u, t, 2)
    coefficient_of_u_ddot = sp.simplify(sp.diff(raw_eh_density, u_ddot))
    boundary_term = sp.diff(coefficient_of_u_ddot * sp.diff(u, t), t)
    bulk_density = sp.factor(sp.simplify(raw_eh_density - boundary_term))
    expected_bulk_density = sp.Rational(3, 2) * radius_ref * sp.diff(u, t) ** 2
    add_check(
        checks,
        "einstein_hilbert_radion_bulk_kinetic",
        bulk_density - expected_bulk_density,
        raw_density=str(raw_eh_density),
        removed_total_derivative=str(boundary_term),
        expected_bulk_density=str(expected_bulk_density),
    )

    m_pl, sigma = sp.symbols("M_Pl sigma", positive=True)
    sigma_dot_from_u = sp.sqrt(sp.Rational(3, 2)) * m_pl * sp.diff(u, t)
    reduced_radion_density = sp.Rational(1, 2) * m_pl**2 * bulk_density / radius_ref
    canonical_density = sp.Rational(1, 2) * sigma_dot_from_u**2
    add_check(
        checks,
        "canonical_radion_definition",
        reduced_radion_density - canonical_density,
        definition="sigma=sqrt(3/2) M_Pl ln(r)",
    )

    # Independent measure/inverse-metric factors for a Fourier mode normalized
    # as Psi=ell_ref^-1/2 psi_n exp(i n y).
    r, n, mass = sp.symbols("r n m_5", positive=True)
    ell_ref = 2 * sp.pi * radius_ref
    normalization_squared = 1 / ell_ref
    integrated_measure = ell_ref / r
    inverse_four_metric_factor = r
    inverse_circle_metric_factor = 1 / (radius_ref**2 * r**2)
    four_kinetic_coefficient = sp.simplify(
        integrated_measure * inverse_four_metric_factor * normalization_squared
    )
    kk_mass_squared = sp.simplify(
        integrated_measure * inverse_circle_metric_factor * n**2 * normalization_squared
    )
    parent_mass_squared = sp.simplify(integrated_measure * mass**2 * normalization_squared)
    add_check(checks, "four_dimensional_mode_kinetic_normalization", four_kinetic_coefficient - 1)
    add_check(
        checks,
        "einstein_frame_kk_mass_factor",
        kk_mass_squared - n**2 / (radius_ref**2 * r**3),
    )
    add_check(checks, "einstein_frame_parent_mass_factor", parent_mass_squared - mass**2 / r)

    all_ok = all(check["ok"] for check in checks)
    result = {
        "schema": "ITSM_TOPX4_A2_RADION_SYMBOLIC_v1",
        "route": "TOP-X4_KK-001",
        "parent": "X4-I1C_bulk_scalar_control",
        "status": PASS_STATUS if all_ok else FAIL_STATUS,
        "audit_execution_status": "COMPLETE" if all_ok else "ERROR",
        "physics_pass": False,
        "gate_effect": "NONE",
        "checks": checks,
        "checks_passed": sum(check["ok"] for check in checks),
        "checks_total": len(checks),
        "explicit_nonclaims": [
            "no stationary radion background",
            "no full coupled physical pole spectrum",
            "no EFT hierarchy",
            "no phenomenology",
        ],
    }

    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "topx4_a2_radion_symbolic_summary.json"
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
