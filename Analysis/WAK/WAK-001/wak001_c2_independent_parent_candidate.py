#!/usr/bin/env python3
"""WAK-001: audit C2 as an unselected identity-route candidate.

LABEL: Conditional decision packet - no identity route selected
GATE:  WAK-001 Stage 2 C2 candidate evaluation
CLAIM: none Derived; physics_pass always false
STATUS: OPEN_SCAFFOLD_ONLY under HOLD_WAK001_IDENTITY_ROUTE_UNSELECTED

From the exclusive catalog (C1/C2/C3), this package evaluates C2 without
selecting or activating it:
  C2_INDEPENDENT_PARENT_ACTION
  requires S_W[W] + T_W + causal initial data

It records a minimal hyperbolic parent *template* (aligned with existing
Route-II local variation family) and bookkeeping I_W, without closing
identity or enabling sources beyond the free field.

Does NOT: identify W with UVIR modes (C1), claim internal constitutive
closure (C3), derive Bullet Cluster offsets, or double-count AQUAL.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--routes-summary",
        type=Path,
        default=base / "outputs" / "wak001_identity_closure_routes_summary.json",
    )
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    return p.parse_args()


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    args = parse_args()
    routes = load_json(args.routes_summary)
    checks: list[dict[str, Any]] = []

    checks.append(
        {
            "name": "prior_routes_catalog_present",
            "ok": routes is not None
            and routes.get("subgate_status")
            == "PASS_WAK001_IDENTITY_CLOSURE_ROUTES_CATALOG",
        }
    )

    # Decision packet: evaluate C2 while retaining every route as Open.
    decision = {
        "candidate_under_evaluation": "C2_INDEPENDENT_PARENT_ACTION",
        "selected_candidate": None,
        "retained_open": [
            "C1_IDENTIFY_WITH_EXISTING_UVIR_MODE",
            "C2_INDEPENDENT_PARENT_ACTION",
            "C3_INTERNAL_CONSTITUTIVE_OF_PLENUM",
        ],
        "rule": "No route activates before an explicit evidence-backed comparison decision",
        "decision_status": "NOT_SELECTED",
        "identity_status": "UNRESOLVED",
    }
    checks.append(
        {
            "name": "C2_is_evaluated_not_selected",
            "ok": decision["candidate_under_evaluation"].startswith("C2")
            and decision["selected_candidate"] is None
            and decision["decision_status"] == "NOT_SELECTED",
        }
    )
    checks.append(
        {
            "name": "all_identity_routes_retained_open",
            "ok": set(decision["retained_open"])
            == {
                "C1_IDENTIFY_WITH_EXISTING_UVIR_MODE",
                "C2_INDEPENDENT_PARENT_ACTION",
                "C3_INTERNAL_CONSTITUTIVE_OF_PLENUM",
            }
            and decision["identity_status"] == "UNRESOLVED",
        }
    )

    # Minimal parent template (flat rest frame)
    Z, c2, M2 = sp.symbols("Z_W c_W_sq M_W_sq", positive=True)
    W, Wt, Wx = sp.symbols("W W_t W_x", real=True)
    L = sp.Rational(1, 2) * Z * Wt**2 - sp.Rational(1, 2) * Z * c2 * Wx**2 - sp.Rational(
        1, 2
    ) * M2 * W**2
    pi_W = sp.diff(L, Wt)
    H = sp.expand(pi_W * Wt - L)
    H_expected = (
        sp.Rational(1, 2) * Z * Wt**2
        + sp.Rational(1, 2) * Z * c2 * Wx**2
        + sp.Rational(1, 2) * M2 * W**2
    )
    checks.append(
        {
            "name": "hamiltonian_positive_definite_structure",
            "ok": sp.simplify(H - H_expected) == 0,
        }
    )
    omega2, k2 = sp.symbols("omega_sq k_sq", nonnegative=True)
    disp = Z * omega2 - Z * c2 * k2 - M2
    checks.append(
        {
            "name": "dispersion_hyperbolic_template",
            "ok": sp.simplify(sp.solve(disp, omega2)[0] - (c2 * k2 + M2 / Z)) == 0,
        }
    )

    bookkeeping = {
        "route": "II_independent_wake_sector",
        "div_T_W": "I_W",
        "plenum": "div T_P = -Q_mp + Q_syn - I_W",
        "forbidden": [
            "silent I_W = Q_mp",
            "silent I_W = Q_syn",
            "static AQUAL double-count as wake",
        ],
        "source_J_W": "UNDECLARED_IN_THIS_PACKAGE",
        "damping": "UNDECLARED_IN_THIS_PACKAGE",
    }
    checks.append(
        {
            "name": "source_and_damping_still_undeclared",
            "ok": bookkeeping["source_J_W"].startswith("UNDECLARED")
            and bookkeeping["damping"].startswith("UNDECLARED"),
        }
    )

    parent = {
        "S_W_template": (
            "∫ ½ Z_W (U·∇W)² - ½ Z_W c_W² |h·∇W|² - ½ M_W² W²   "
            "(flat rest-frame reduction audited)"
        ),
        "parameters_positive": ["Z_W", "c_W²", "M_W²"],
        "status": "CANDIDATE_TEMPLATE_INCOMPLETE",
        "completeness_missing": [
            "covariant completion on curved/FRW backgrounds",
            "stress tensor T_W^{μν} from Noether/metric variation",
            "interaction S_int generating I_W",
            "initial-data well-posedness theorem",
        ],
    }
    checks.append(
        {
            "name": "parent_marked_incomplete",
            "ok": parent["status"] == "CANDIDATE_TEMPLATE_INCOMPLETE",
        }
    )

    firewall = {
        "physics_pass": False,
        "identity_closed": False,
        "C1_identification_claimed": False,
        "C3_internal_claimed": False,
        "source_derived": False,
        "Bullet_Cluster": False,
        "AQUAL_double_count": False,
        "WAK_research_gate_PASS": False,
        "route_selected": False,
    }
    checks.append(
        {
            "name": "claim_firewall",
            "ok": all(v is False for v in firewall.values()),
            "flags": firewall,
        }
    )

    all_ok = all(c["ok"] for c in checks)
    subgate = (
        "PASS_WAK001_C2_DECISION_PACKET_OPEN"
        if all_ok
        else "FAIL_WAK001_C2_DECISION_PACKET"
    )

    summary: dict[str, Any] = {
        "gate": "WAK-001",
        "stage": "C2_DECISION_PACKET",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "physics_pass": False,
        "hold": "HOLD_WAK001_IDENTITY_ROUTE_UNSELECTED",
        "decision": decision,
        "parent_template": parent,
        "bookkeeping": bookkeeping,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "Evaluates C2 as one unselected identity candidate and records a "
            "minimal hyperbolic S_W comparison template. C1/C2/C3 remain Open; "
            "identity is unresolved and no source, damping, or observable follows."
        ),
        "next_required": [
            "Compare C1/C2/C3 against one declared evidence rubric",
            "For C2, derive T_W^{mu nu} and I_W from S_W + S_int",
            "Record an explicit selection decision before activating any route",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "wak001_c2_independent_parent_candidate_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    h = hashlib.sha256(payload).hexdigest().upper()
    (
        args.output_dir / "wak001_c2_independent_parent_candidate_summary.sha256"
    ).write_bytes(f"{h}  {out.name}\n".encode("utf-8"))

    print("WAK-001 C2 decision packet")
    print("  physics_pass: False | identity: UNRESOLVED | decision: NOT_SELECTED")
    for c in checks:
        print(f"  [{'OK' if c['ok'] else 'FAIL'}] {c['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", h)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
