#!/usr/bin/env python3
"""MAT-001 unit-chart contract for natural and SI coefficient conventions.

This is a dimensional and provenance audit, not microscopic matching. It keeps
V NOT_COMPUTED, MAT-001 BLOCKED, UVIR-003 IN_PROGRESS, and Stage 4A closed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Dim = tuple[Fraction, Fraction, Fraction]  # SI base exponents (M, L, T)
ZERO: Dim = (Fraction(0), Fraction(0), Fraction(0))


def dim(m: int = 0, length: int = 0, time: int = 0) -> Dim:
    return (Fraction(m), Fraction(length), Fraction(time))


def add(*values: Dim) -> Dim:
    return tuple(sum(parts, Fraction(0)) for parts in zip(*values))  # type: ignore[return-value]


def neg(value: Dim) -> Dim:
    return tuple(-part for part in value)  # type: ignore[return-value]


def sub(left: Dim, right: Dim) -> Dim:
    return add(left, neg(right))


def scale(value: Dim, factor: Fraction) -> Dim:
    return tuple(factor * part for part in value)  # type: ignore[return-value]


def format_power(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def format_dim(value: Dim) -> dict[str, str]:
    return {name: format_power(power) for name, power in zip(("M", "L", "T"), value)}


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--j1-summary",
        type=Path,
        default=mat / "J1_JOINT_ACTION" / "outputs" / "mat001_j1_joint_action_normalization_summary.json",
    )
    parser.add_argument(
        "--r2-summary",
        type=Path,
        default=mat / "R2_DIRECT_RESIDUE" / "outputs" / "mat001_r2_direct_residue_audit_summary.json",
    )
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.is_file():
        return None, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, f"{type(exc).__name__}:{exc}"
    if not isinstance(data, dict):
        return None, "top_level_not_object"
    return data, None


def j1_contract(data: dict[str, Any] | None) -> bool:
    return bool(
        data
        and data.get("subgate_status") == "PASS_MAT001_J1_JOINT_ACTION_NORMALIZATION_IDENTITY"
        and data.get("V_status") == "NOT_COMPUTED"
        and data.get("V_form_status") == "SAME_ACTION_IDENTITY_DERIVED"
        and data.get("mat001_pass") is False
        and data.get("physics_pass") is False
    )


def r2_contract(data: dict[str, Any] | None) -> bool:
    return bool(
        data
        and data.get("subgate_status") == "PASS_MAT001_R2_DIRECT_RESIDUE_AUDIT"
        and data.get("V_status") == "NOT_COMPUTED"
        and data.get("mat001_status") == "BLOCKED"
        and data.get("uv_ir_full_gate_status") == "IN_PROGRESS"
        and data.get("mat001_pass") is False
        and data.get("physics_pass") is False
    )


def main() -> None:
    args = parse_args()
    j1, j1_error = load_json(args.j1_summary)
    r2, r2_error = load_json(args.r2_summary)

    # Natural units: dimensions are mass/energy powers with c=hbar=1.
    natural = {
        "psi": 0,
        "a0": 1,
        "q": 1,
        "Q_unnormalized": 1,
        "Y_unnormalized": 2,
        "K_Q": 2,
        "A": 1,
        "gamma": 2,
        "C_m": 0,
        "rho_b": 4,
        "V": -1,
        "L_density": 4,
    }

    # SI chart x: x^0=ct, psi has gravitational-potential units.
    c = dim(length=1, time=-1)
    G = dim(m=-1, length=3, time=-2)
    psi = dim(length=2, time=-2)
    a0 = dim(length=1, time=-2)
    rho_mass = dim(m=1, length=-3)
    density = dim(m=1, length=-1, time=-2)
    q = sub(psi, dim(length=1))
    Q_x = q
    Q_t = sub(psi, dim(time=1))
    A = neg(add(G, a0))
    K_x = neg(G)
    K_t = sub(K_x, scale(c, Fraction(2)))
    C_m = ZERO
    V_x = scale(K_x, Fraction(-1, 2))
    V_t = scale(K_t, Fraction(-1, 2))

    checks: list[dict[str, Any]] = [
        {
            "name": "upstream_J1_exact_contract",
            "ok": j1_contract(j1),
            "source": args.j1_summary.name,
            "error": j1_error,
        },
        {
            "name": "upstream_R2_exact_contract",
            "ok": r2_contract(r2),
            "source": args.r2_summary.name,
            "error": r2_error,
        },
        {"name": "natural_Q2_term_has_dimension_4", "ok": natural["K_Q"] + 2 * natural["Q_unnormalized"] == 4},
        {"name": "natural_Y32_term_has_dimension_4", "ok": natural["A"] + 3 * natural["q"] == 4},
        {"name": "natural_matter_vertex_has_dimension_4", "ok": natural["C_m"] + natural["rho_b"] + natural["psi"] == 4},
        {"name": "natural_Aq_over_KQ_dimensionless", "ok": natural["A"] + natural["q"] - natural["K_Q"] == 0},
        {"name": "natural_Aa0_over_KQ_dimensionless", "ok": natural["A"] + natural["a0"] - natural["K_Q"] == 0},
        {"name": "natural_V_has_mass_dimension_minus_1", "ok": natural["V"] == -1},
        {"name": "SI_x0_kinetic_term_is_energy_density", "ok": add(K_x, scale(Q_x, Fraction(2))) == density},
        {"name": "SI_t_kinetic_term_is_energy_density", "ok": add(K_t, scale(Q_t, Fraction(2))) == density},
        {"name": "SI_spatial_term_is_energy_density", "ok": add(A, scale(q, Fraction(3))) == density},
        {"name": "SI_mass_density_vertex_is_energy_density", "ok": add(C_m, rho_mass, psi) == density},
        {"name": "SI_conformal_exponent_dimensionless", "ok": sub(psi, scale(c, Fraction(2))) == ZERO},
        {"name": "SI_Kt_equals_Kx_over_c2", "ok": K_t == sub(K_x, scale(c, Fraction(2)))},
        {"name": "SI_x0_Aq_over_Kx_dimensionless", "ok": sub(add(A, q), K_x) == ZERO},
        {"name": "SI_x0_Aa0_over_Kx_dimensionless", "ok": sub(add(A, a0), K_x) == ZERO},
        {"name": "SI_t_Aq_over_Kt_c2_dimensionless", "ok": sub(add(A, q), add(K_t, scale(c, Fraction(2)))) == ZERO},
        {"name": "SI_t_Aa0_over_Kt_c2_dimensionless", "ok": sub(add(A, a0), add(K_t, scale(c, Fraction(2)))) == ZERO},
        {"name": "SI_x0_V_has_sqrtG_dimensions", "ok": V_x == scale(G, Fraction(1, 2))},
        {"name": "SI_t_V_has_sqrtG_times_c_dimensions", "ok": V_t == add(scale(G, Fraction(1, 2)), c)},
    ]

    negative_controls = [
        {"case": "missing_J1_rejected", "ok": not j1_contract(None)},
        {"case": "missing_R2_rejected", "ok": not r2_contract(None)},
        {
            "case": "premature_R2_V_computed_rejected",
            "ok": not r2_contract(
                {
                    "subgate_status": "PASS_MAT001_R2_DIRECT_RESIDUE_AUDIT",
                    "V_status": "COMPUTED",
                    "mat001_status": "BLOCKED",
                    "uv_ir_full_gate_status": "IN_PROGRESS",
                    "mat001_pass": False,
                    "physics_pass": False,
                }
            ),
        },
        {
            "case": "extra_c2_in_x0_chart_not_dimensionless",
            "ok": sub(add(A, q), add(K_x, scale(c, Fraction(2)))) != ZERO,
        },
        {
            "case": "missing_c2_in_t_chart_not_dimensionless",
            "ok": sub(add(A, q), K_t) != ZERO,
        },
    ]
    checks.append(
        {
            "name": "negative_controls_fail_closed",
            "ok": all(row["ok"] for row in negative_controls),
            "cases": negative_controls,
        }
    )

    firewall = {
        "V_numeric_computed": False,
        "K_Q_numeric_derived": False,
        "mat001_pass": False,
        "UVIR003_pass": False,
        "stage4A_unblocked": False,
        "physics_pass": False,
        "SI_chart_selected_for_observables": False,
    }
    checks.append(
        {
            "name": "claim_firewall",
            "ok": all(value is False for value in firewall.values()),
            "flags": firewall,
        }
    )

    all_ok = all(check["ok"] for check in checks)
    subgate = (
        "PASS_MAT001_UNIT_CHART_CONTRACT_OPEN"
        if all_ok
        else "FAIL_MAT001_UNIT_CHART_CONTRACT"
    )
    summary: dict[str, Any] = {
        "gate": "MAT-001",
        "stage": "UNIT_CHART_CONTRACT",
        "subgate_status": subgate,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "unit_contract_status": "FORMALIZED_COEFFICIENT_CHARTS_MATCHING_OPEN",
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_unlock": False,
        "physics_pass": False,
        "natural_unit_mass_dimensions": natural,
        "SI_dimensions_M_L_T": {
            "c": format_dim(c),
            "G": format_dim(G),
            "psi_SI": format_dim(psi),
            "a0_SI": format_dim(a0),
            "q_SI": format_dim(q),
            "A_SI": format_dim(A),
            "K_Q_x0": format_dim(K_x),
            "K_Q_t": format_dim(K_t),
            "V_x0": format_dim(V_x),
            "V_t": format_dim(V_t),
        },
        "coefficient_chart_map": {
            "repository_chart": "natural units; covariant derivative U^mu nabla_mu with c=hbar=1",
            "SI_x0_chart": "x^0=ct; K_Q_x0 multiplies (U.grad psi_SI)^2",
            "SI_t_chart": "coordinate time t; K_Q_t multiplies (d psi_SI/dt)^2",
            "relation": "K_Q_t = K_Q_x0/c^2",
            "x0_causality_ratio": "3*A*q*(1+cos(theta)^2)/K_Q_x0",
            "t_causality_ratio": "3*A*q*(1+cos(theta)^2)/(K_Q_t*c^2)",
            "x0_vertex_invariant": "V_x0=C_m/sqrt(K_Q_x0), dimensions sqrt(G)",
            "t_vertex_invariant": "V_t=C_m/sqrt(K_Q_t)=c*V_x0, dimensions sqrt(G)*c",
        },
        "interpretation": {
            "current_repository_formulas": "dimensionally closed in the declared natural/covariant chart",
            "universal_extra_c_minus_2": "REJECTED",
            "reason": "a c^2 factor belongs to the definition change K_Q_x0 <-> K_Q_t, not to every chart",
            "SI_observable_packaging": "OPEN until one coordinate, action-measure, density, and coefficient chart is selected",
        },
        "prior_artifacts": {
            "J1": {"source": args.j1_summary.name, "parse_error": j1_error},
            "R2": {"source": args.r2_summary.name, "parse_error": r2_error},
        },
        "negative_controls": negative_controls,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS establishes dimensional consistency and the relation between "
            "covariant-length and coordinate-time coefficient charts. It does not "
            "select an SI observable chart, derive K_Q or C_m, compute V, unlock "
            "Stage 4A, or issue MAT/UVIR/physics PASS."
        ),
        "next_required": [
            "derive the kinetic and matter coefficients from one declared action",
            "state whether the final SI action uses x0=ct or coordinate time t",
            "project the source onto the physical canonical mode",
            "then compute V in that named chart and reopen UVIR Stage 4A",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "mat001_unit_chart_contract_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    sidecar = args.output_dir / "mat001_unit_chart_contract_summary.sha256"
    sidecar.write_bytes(f"{digest}  {out.name}\n".encode("utf-8"))

    print("MAT-001 unit-chart contract")
    print("  natural/covariant chart: current formulas dimensionally closed")
    print("  SI map: K_Q_t = K_Q_x0/c^2")
    print("  V_status: NOT_COMPUTED | MAT: BLOCKED | Stage4A: CLOSED")
    for check in checks:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS: {0}".format(subgate))
    print("JSON_SHA256: {0}".format(digest))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
