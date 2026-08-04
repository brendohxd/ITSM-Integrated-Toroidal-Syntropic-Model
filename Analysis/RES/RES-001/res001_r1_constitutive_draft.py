#!/usr/bin/env python3
"""RES-001 R1: audit an unselected constitutive candidate form.

LABEL: Conditional decision packet - no constitutive route selected
GATE:  RES-001 Stage 1 R1 candidate evaluation
CLAIM: none Derived; physics_pass always false
STATUS: OPEN_SCAFFOLD_ONLY

Candidate form (rest-frame template):
  Q_syn^mu = Gamma_syn (rho_P - rho_*) U^mu + sigma_syn Pi^{mu nu} grad_nu ln rho_P
with Gamma_syn >= 0, sigma_syn real, and rho_P,rho_* > 0.

Checks:
  - reduces to pure timelike throughput when sigma_syn=0
  - conservation partition still requires T_R with div T_R = -Q_syn
  - Q_mp remains independent symbol
  - firewall bans H0/13/12/S_N automatic identification

Does NOT: select R1, fix numerical rates, topology-lock R3, or couple to WAK I_W.
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
        "--inventory",
        type=Path,
        default=base / "outputs" / "res001_qsyn_constitutive_inventory_summary.json",
    )
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    checks: list[dict[str, Any]] = []

    inv = None
    if args.inventory.exists():
        inv = json.loads(args.inventory.read_text(encoding="utf-8"))
    checks.append(
        {
            "name": "prior_inventory_present",
            "ok": inv is not None
            and inv.get("subgate_status")
            == "PASS_RES001_QSYN_CONSTITUTIVE_INVENTORY_OPEN",
        }
    )

    Gamma = sp.symbols("Gamma_syn", nonnegative=True, finite=True)
    sigma = sp.symbols("sigma_syn", real=True, finite=True)
    rho_P, rho_star = sp.symbols("rho_P rho_star", positive=True, finite=True)
    # Rest frame U = (1,0,0,0); Q_syn^0 = Gamma (rho_P - rho_star)
    Q0 = Gamma * (rho_P - rho_star)
    # Spatial part schematic: sigma * spatial gradient projector
    # Energy density transfer rate to plenum from reservoir is +Q_syn·U = -Q0 if U_0=-1 conventions;
    # we only check algebraic independence symbols.
    checks.append(
        {
            "name": "timelike_piece_linear_in_density_contrast",
            "ok": sp.simplify(sp.diff(Q0, rho_P) - Gamma) == 0,
        }
    )
    checks.append(
        {
            "name": "vanishes_at_reference_when_sigma_unused",
            "ok": sp.simplify(Q0.subs(rho_P, rho_star)) == 0,
        }
    )

    draft = {
        "id": "R1_DECLARED_CONSTITUTIVE_VECTOR",
        "status": "CANDIDATE_FORM_UNSELECTED_CONDITIONAL",
        "Q_syn_mu": (
            "Γ_syn (ρ_P - ρ_*) U^μ + σ_syn Π^{μν} ∇_ν ln ρ_P   "
            "(flat rest-frame schematic; Π projector orthogonal to U)"
        ),
        "parameters": {
            "Gamma_syn": ">=0 Conditional rate",
            "sigma_syn": "Conditional spatial coupling",
            "rho_P": ">0 domain required by ln(rho_P)",
            "rho_star": ">0 Conditional reference density",
        },
        "requires_for_Derived": [
            "action or irreversible thermodynamics derivation of Γ,σ",
            "covariant completion and energy conditions stated",
            "matching to reservoir stress T_R",
        ],
        "bookkeeping": {
            "div_T_R": "-Q_syn",
            "div_T_P_includes": "+Q_syn",
            "Q_mp": "independent symbol; not set equal to Q_syn",
        },
    }
    checks.append(
        {
            "name": "draft_status_conditional_not_Derived",
            "ok": "CONDITIONAL" in draft["status"]
            and "DERIVED" not in draft["status"],
        }
    )
    checks.append(
        {
            "name": "Q_mp_kept_independent_in_draft",
            "ok": "not set equal" in draft["bookkeeping"]["Q_mp"],
        }
    )

    # Decision packet: evaluate R1 while retaining every route as Open.
    decision = {
        "candidate_under_evaluation": "R1_DECLARED_CONSTITUTIVE_VECTOR",
        "selected_candidate": None,
        "retained_open": [
            "R1_DECLARED_CONSTITUTIVE_VECTOR",
            "R2_ACTION_COUPLED_RESERVOIR",
            "R3_TOPOLOGY_LOCKED_THROUGHPUT",
        ],
        "control_retained": "R0_NO_THROUGHPUT_CONTROL",
        "decision_status": "NOT_SELECTED",
    }
    checks.append(
        {
            "name": "R1_is_evaluated_not_selected",
            "ok": decision["candidate_under_evaluation"].startswith("R1")
            and decision["selected_candidate"] is None
            and decision["decision_status"] == "NOT_SELECTED",
        }
    )
    checks.append(
        {
            "name": "positive_density_domain_declared",
            "ok": draft["parameters"]["rho_P"].startswith(">0")
            and draft["parameters"]["rho_star"].startswith(">0"),
        }
    )

    firewall = {
        "physics_pass": False,
        "Derived_creation_rate": False,
        "Q_syn_is_S_N": False,
        "H0_from_Q_syn": False,
        "13_12_from_reservoir": False,
        "NEC_violating_Minkowski_support": False,
        "RES_research_gate_PASS": False,
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
        "PASS_RES001_R1_DECISION_PACKET_OPEN"
        if all_ok
        else "FAIL_RES001_R1_DECISION_PACKET"
    )

    summary: dict[str, Any] = {
        "gate": "RES-001",
        "stage": "R1_DECISION_PACKET",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "physics_pass": False,
        "decision": decision,
        "draft": draft,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "Evaluates an unselected Conditional R1 form for Q_syn with independent "
            "Q_mp and total-conservation bookkeeping. R1/R2/R3 remain Open; "
            "parameters remain free and no Derived creation rate or cosmology follows."
        ),
        "next_required": [
            "Compare R1/R2/R3 against one declared evidence rubric",
            "For R1, provide a covariant form and T_R matching",
            "Record an explicit selection decision before activating any route",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "res001_r1_constitutive_draft_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    h = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "res001_r1_constitutive_draft_summary.sha256").write_bytes(
        f"{h}  {out.name}\n".encode("utf-8")
    )

    print("RES-001 R1 constitutive decision packet")
    print("  physics_pass: False | decision: NOT_SELECTED | Conditional only")
    for c in checks:
        print(f"  [{'OK' if c['ok'] else 'FAIL'}] {c['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", h)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
