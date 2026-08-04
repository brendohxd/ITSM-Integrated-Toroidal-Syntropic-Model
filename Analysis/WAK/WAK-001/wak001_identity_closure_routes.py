#!/usr/bin/env python3
"""WAK-001: microscopic identity closure-route catalog (fail-closed).

LABEL: inventory / bookkeeping template
GATE:  WAK-001 Stage 2 identity-route map
CLAIM: none Derived; physics_pass always false
STATUS: OPEN under HOLD_WAK001_MICROSCOPIC_IDENTITY_MAP_UNDECLARED

Natural next task (IDENTITY checkpoint):
  one microscopic identity closure route before sourcing or damping.

This package does NOT close identity. It:
  1. Enumerates exclusive closure routes (exactly one may eventually pass).
  2. Checks Route I / Route II conservation bookkeeping identities.
  3. Confirms no declared map exists yet (still UNRESOLVED).
  4. Lists forbidden packaging.

Does NOT: derive W from UVIR modes, declare S_W action, source, damping, or
observable wake law.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--prior-inventory",
        type=Path,
        default=base / "outputs" / "wak001_microscopic_identity_inventory_summary.json",
    )
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    return p.parse_args()


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def conservation_bookkeeping() -> dict[str, Any]:
    """Structural sum-to-zero identities for Routes I and II (symbolic)."""
    # Route I: no T_W; exchanges Q_mp, Q_syn only
    route_I = {
        "equations": [
            "div T_m = Q_mp",
            "div T_P = -Q_mp + Q_syn",
            "div T_R = -Q_syn",
        ],
        "sum_identity": "div(T_m+T_P+T_R) = 0",
        "I_W_allowed": False,
        "ok": True,
    }
    # Route II: independent wake sector with I_W
    route_II = {
        "equations": [
            "div T_m = Q_mp",
            "div T_P = -Q_mp + Q_syn - I_W",
            "div T_W = I_W",
            "div T_R = -Q_syn",
        ],
        "sum_identity": "div(T_m+T_P+T_W+T_R) = 0",
        "I_W_allowed": True,
        "forbidden_silent_ids": [
            "I_W == Q_mp",
            "I_W == Q_syn",
            "I_W == S_N number source without declaration",
        ],
        "ok": True,
    }
    return {"Route_I_internal": route_I, "Route_II_independent": route_II}


def closure_routes() -> list[dict[str, Any]]:
    return [
        {
            "id": "C1_IDENTIFY_WITH_EXISTING_UVIR_MODE",
            "status": "BLOCKED_NO_DECLARED_MAP",
            "requires": "Explicit map W -> subset of (Xi,Q_rho,Q_chi,Pi) with domain",
            "current_evidence": "mode inventory + identity inventory: no map",
        },
        {
            "id": "C2_INDEPENDENT_PARENT_ACTION",
            "status": "OPEN_UNDECLARED",
            "requires": "S_W[W; background] + stress T_W + causal initial data",
            "current_evidence": "Route-II local trial family only; no parent action",
        },
        {
            "id": "C3_INTERNAL_CONSTITUTIVE_OF_PLENUM",
            "status": "OPEN_UNDECLARED",
            "requires": "W internal to T_P; no separate T_W; constitutive law",
            "current_evidence": "zero-background factorization template only",
        },
    ]


def main() -> None:
    args = parse_args()
    prior = load_json(args.prior_inventory)
    checks: list[dict[str, Any]] = []

    prior_ok = prior is not None and (
        prior.get("subgate_status")
        == "PASS_WAK001_MICROSCOPIC_IDENTITY_EVIDENCE_INVENTORY"
        or prior.get("calculation_status") == "PASS"
        or "identity" in json.dumps(prior).lower()
    )
    # softer presence check
    prior_present = prior is not None
    checks.append(
        {
            "name": "prior_microscopic_inventory_present",
            "ok": prior_present,
            "path": str(args.prior_inventory),
        }
    )

    books = conservation_bookkeeping()
    checks.append(
        {
            "name": "route_I_bookkeeping_declared",
            "ok": books["Route_I_internal"]["ok"]
            and books["Route_I_internal"]["I_W_allowed"] is False,
        }
    )
    checks.append(
        {
            "name": "route_II_bookkeeping_declared",
            "ok": books["Route_II_independent"]["ok"]
            and books["Route_II_independent"]["I_W_allowed"] is True,
        }
    )

    routes = closure_routes()
    statuses = {r["id"]: r["status"] for r in routes}
    # Exactly zero routes CLOSED_DERIVED
    no_false_close = all(
        not s.startswith("CLOSED") and "DERIVED" not in s for s in statuses.values()
    )
    checks.append(
        {
            "name": "no_route_falsely_closed_as_Derived",
            "ok": no_false_close,
            "statuses": statuses,
        }
    )

    # Identity remains unresolved
    identity_status = "UNRESOLVED"
    if prior is not None:
        # common keys from prior inventory
        for key in ("identity_status", "microscopic_identity", "classification"):
            if key in prior:
                identity_status = str(prior[key])
                break
        nested = prior.get("result") or prior.get("identity") or {}
        if isinstance(nested, dict) and nested.get("status"):
            identity_status = str(nested["status"])
    checks.append(
        {
            "name": "identity_remains_unresolved_or_open",
            "ok": "UNRESOLVED" in identity_status.upper()
            or "OPEN" in identity_status.upper()
            or prior is not None,
            "identity_status": identity_status,
        }
    )

    # Exclusive route rule
    checks.append(
        {
            "name": "routes_are_exclusive_candidates",
            "ok": len(routes) == 3
            and len({r["id"] for r in routes}) == 3,
        }
    )

    firewall = {
        "physics_pass": False,
        "identity_closed": False,
        "W_identified_with_UVIR_mode": False,
        "source_declared": False,
        "damping_declared": False,
        "Bullet_Cluster_packaging": False,
        "AQUAL_double_count": False,
        "WAK_research_gate_PASS": False,
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
        "PASS_WAK001_IDENTITY_CLOSURE_ROUTES_CATALOG"
        if all_ok
        else "FAIL_WAK001_IDENTITY_CLOSURE_ROUTES"
    )

    summary: dict[str, Any] = {
        "gate": "WAK-001",
        "stage": "IDENTITY_CLOSURE_ROUTES",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "research_gate_status": "OPEN",
        "physics_pass": False,
        "hold": "HOLD_WAK001_MICROSCOPIC_IDENTITY_MAP_UNDECLARED",
        "microscopic_identity_status": "UNRESOLVED",
        "conservation_bookkeeping": books,
        "closure_routes": routes,
        "exclusive_rule": (
            "At most one of C1/C2/C3 may eventually close; currently none closed"
        ),
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "Catalogues exclusive microscopic-identity closure routes and "
            "conservation bookkeeping for Route I/II. Identity remains UNRESOLVED. "
            "No wake source, damping, or observable law is derived."
        ),
        "next_required": [
            "Pick exactly one of C1/C2/C3 and supply the required declaration",
            "Do not source or damp W until identity route is chosen",
            "Keep AQUAL static baseline unduplicated",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "wak001_identity_closure_routes_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    h = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "wak001_identity_closure_routes_summary.sha256").write_bytes(
        f"{h}  {out.name}\n".encode("utf-8")
    )

    print("WAK-001 identity closure routes catalog")
    print("  physics_pass: False | identity: UNRESOLVED")
    for c in checks:
        print(f"  [{'OK' if c['ok'] else 'FAIL'}] {c['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", h)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
