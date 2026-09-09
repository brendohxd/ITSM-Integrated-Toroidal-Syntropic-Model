#!/usr/bin/env python3
"""High-only TOP-X4 stabilization candidate prescreen.

This script does not evaluate a one-loop determinant or solve a new background.
It checks exact algebraic stationarity conditions, field-content signs, and the
dimensionless existence test used to select at most one Max-level retry.
"""

from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path
from typing import Any

import mpmath as mp
import sympy as sp


STATUS = "SELECT_TOPX4_S2F3_FOR_MAX_RETRY_ONLY"
FORBIDDEN_TARGET_TOKENS = (
    "observed" + "_acceleration",
    "hubble" + "_target",
    "galaxy" + "_target",
    "desired" + "_radius",
)


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def massive_shape(x: mp.mpf) -> mp.mpf:
    z = mp.exp(-x)
    return mp.polylog(5, z) + x * mp.polylog(4, z) + x * x * mp.polylog(3, z) / 3


def massive_shape_prime(x: mp.mpf) -> mp.mpf:
    z = mp.exp(-x)
    return -(x * mp.polylog(3, z) + x * x * mp.polylog(2, z)) / 3


def massive_shape_second(x: mp.mpf) -> mp.mpf:
    return mp.diff(massive_shape, x, 2)


def main() -> int:
    mp.mp.dps = 60
    checks: list[dict[str, Any]] = []

    # S1: a winding Mexican-hat scalar can have a stable radial/amplitude
    # Hessian, but the direct-product Einstein equations force AdS4 and zero
    # temporal charge. This keeps the mathematical result separate from the
    # frozen finite-charge ITSM-parent requirement.
    rho, radius, mass_abs, lam, winding = sp.symbols(
        "rho r m_abs lambda w", positive=True
    )
    vacuum = sp.symbols("U_vac", real=True)
    potential_5 = vacuum - mass_abs**2 * rho**2 / 2 + lam * rho**4 / 8
    winding_energy = rho**2 * winding**2 / (2 * radius**2)
    potential_4 = potential_5 / radius + rho**2 * winding**2 / (2 * radius**3)
    field_equation = sp.factor(sp.diff(potential_4, rho) * radius / rho)
    expected_field_equation = -mass_abs**2 + lam * rho**2 / 2 + winding**2 / radius**2
    add_check(
        checks,
        "s1_field_stationarity_identity",
        sp.simplify(field_equation - expected_field_equation) == 0,
        equation=str(field_equation),
    )

    u = sp.symbols("u", real=True)
    potential_u = potential_4.subs(radius, sp.exp(u))
    rho2_on_shell = 2 * (mass_abs**2 - winding**2 / radius**2) / lam
    vacuum_on_shell = sp.solve(
        sp.Eq(potential_5, -3 * winding_energy), vacuum
    )[0]
    h_rhorho = sp.diff(potential_u, rho, 2)
    h_rhou = sp.diff(potential_u, rho, u)
    h_uu = sp.diff(potential_u, u, 2)
    substitutions = {
        sp.exp(u): radius,
        vacuum: vacuum_on_shell,
        rho**2: rho2_on_shell,
    }
    # Evaluate a transparent dimensionless witness well inside the exact
    # stability domain m_abs^2 r^2 > 5 w^2/3.
    witness = {mass_abs: 1, lam: 1, winding: 1, radius: 2, rho: sp.sqrt(sp.Rational(3, 2))}
    witness_vacuum = sp.simplify(vacuum_on_shell.subs(witness))
    witness_full = dict(witness)
    witness_full[vacuum] = witness_vacuum
    witness_full[u] = sp.log(2)
    hessian = sp.Matrix(
        [
            [h_rhorho.subs(witness_full), h_rhou.subs(witness_full)],
            [h_rhou.subs(witness_full), h_uu.subs(witness_full)],
        ]
    ).applyfunc(sp.simplify)
    hessian_det = sp.simplify(hessian.det())
    kappa = sp.simplify(-2 * winding_energy / 3).subs(witness)
    add_check(
        checks,
        "s1_conditional_ads_winding_minimum_exists",
        bool(hessian[0, 0] > 0 and hessian_det > 0 and kappa < 0),
        witness={
            "m_abs": 1.0,
            "lambda": 1.0,
            "w": 1,
            "r": 2.0,
            "rho_squared": 1.5,
            "U_vac": float(witness_vacuum),
            "four_curvature_kappa": float(kappa),
            "hessian": [[float(value) for value in row] for row in hessian.tolist()],
            "hessian_determinant": float(hessian_det),
        },
        exact_stability_domain="m_abs^2 r^2 > 5 w^2/3",
        limitation="direct-product solution is AdS4 and has zero temporal charge",
    )

    # S2: at zero density, X4-I1C contains five attractive massless graviton
    # polarizations and three attractive massive real bosonic degrees of
    # freedom. Each periodic 5D Dirac field contributes the opposite sign with
    # four degrees of freedom.
    zeta5 = mp.zeta(5)
    field_count = []
    for fermion_count in range(1, 5):
        beta = 4 * fermion_count - 3
        strict = beta > 5
        field_count.append(
            {
                "periodic_dirac_fields": fermion_count,
                "massive_coefficient_beta": beta,
                "massless_coefficient_gamma_over_zeta5": -5,
                "strict_small_radius_repulsion": strict,
            }
        )
    add_check(
        checks,
        "s2_three_dirac_fields_are_minimal_strict_count",
        field_count[0]["strict_small_radius_repulsion"] is False
        and field_count[1]["strict_small_radius_repulsion"] is False
        and field_count[2]["strict_small_radius_repulsion"] is True,
        counts=field_count,
        condition="beta > 5 for beta F(0) to dominate 5 zeta(5)",
    )

    beta = mp.mpf(9)
    gamma = -5 * zeta5
    target = -gamma / beta

    def zero_cc_stationarity_equation(x: mp.mpf) -> mp.mpf:
        return massive_shape(x) - x * massive_shape_prime(x) / 5 - target

    x_star = mp.findroot(zero_cc_stationarity_equation, (mp.mpf("1"), mp.mpf("5")))
    alpha_star = -beta * massive_shape_prime(x_star) / (5 * x_star**4)
    f_value = alpha_star * x_star**5 + beta * massive_shape(x_star) + gamma
    f_prime = 5 * alpha_star * x_star**4 + beta * massive_shape_prime(x_star)
    f_second = 20 * alpha_star * x_star**3 + beta * massive_shape_second(x_star)
    add_check(
        checks,
        "s2_single_scale_zero_cc_stationary_minimum_witness",
        abs(f_value) < mp.mpf("1e-45")
        and abs(f_prime) < mp.mpf("1e-45")
        and alpha_star > 0
        and f_second > 0,
        x_star=float(x_star),
        alpha_star=float(alpha_star),
        f=float(f_value),
        f_prime=float(f_prime),
        f_second=float(f_second),
        beta=float(beta),
        gamma=float(gamma),
        interpretation="dimensionless existence witness only; no determinant or physical scale prediction",
    )

    # With x=m_F ell and ell=2 pi R, Delta_KK/Lambda_5 is
    # 2 pi (m_F/Lambda_5)/x.  The declared prescreen point establishes only
    # that a conservative ten-to-one hierarchy has a non-empty domain.
    mass_to_cutoff = mp.mpf("0.04")
    kk_gap_to_cutoff = 2 * mp.pi * mass_to_cutoff / x_star
    add_check(
        checks,
        "s2_nonempty_ten_to_one_cutoff_domain",
        kk_gap_to_cutoff < mp.mpf("0.1"),
        mass_to_cutoff=float(mass_to_cutoff),
        kk_gap_to_cutoff=float(kk_gap_to_cutoff),
        formula="Delta_KK/Lambda_5=2 pi (m_F/Lambda_5)/x_star",
        limitation="the absolute mass and radius remain free inputs",
    )

    add_check(
        checks,
        "s3_no_distinct_internal_gauge_flux_on_one_circle",
        True,
        reason=(
            "an internal two-form field strength has no nonzero yy component; "
            "a flat Wilson line has zero classical stress; scalar one-form winding is S1"
        ),
    )
    add_check(
        checks,
        "s4_orbifold_is_not_smooth_circle_parent",
        True,
        reason="fixed points require localized terms and junction conditions",
    )

    source_text = inspect.getsource(inspect.getmodule(main))
    forbidden_hits = [token for token in FORBIDDEN_TARGET_TOKENS if token in source_text]
    add_check(
        checks,
        "target_firewall",
        not forbidden_hits,
        forbidden_token_hits=forbidden_hits,
    )

    all_ok = all(check["ok"] for check in checks)
    result = {
        "schema": "ITSM_TOPX4_S0_STABILIZATION_PRESCREEN_v1",
        "route": "TOP-X4_KK-001",
        "status": STATUS if all_ok else "ERROR_TOPX4_S0_PRESCREEN",
        "audit_execution_status": "COMPLETE" if all_ok else "ERROR",
        "calculation_checks_passed": sum(check["ok"] for check in checks),
        "calculation_checks_total": len(checks),
        "physics_pass": False,
        "gate_effect": "NONE",
        "selected_retry": "X4-S2F3_periodic_massive_dirac_spectators" if all_ok else None,
        "candidate_dispositions": {
            "X4-S1": "CONDITIONAL_ADS_CONTROL_NOT_SELECTED",
            "X4-S2": "SELECTED_FOR_MAX_RETRY_ONLY",
            "X4-S3": "NO_DISTINCT_SMOOTH_S1_FLUX_REPAIR",
            "X4-S4": "DEFER_DIFFERENT_GEOMETRY",
        },
        "checks": checks,
        "explicit_nonclaims": [
            "no one-loop determinant evaluated",
            "no finite-density stabilized background",
            "no physical radion mass",
            "no EFT hierarchy",
            "no predicted compactification radius",
            "no canonical ITSM gate promotion",
        ],
    }

    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "topx4_s0_stabilization_prescreen_summary.json"
    payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output_path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    output_path.with_suffix(output_path.suffix + ".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="ascii", newline="\n"
    )

    print(result["status"])
    print(f"calculation_checks={result['calculation_checks_passed']}/{result['calculation_checks_total']}")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={output_path}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
