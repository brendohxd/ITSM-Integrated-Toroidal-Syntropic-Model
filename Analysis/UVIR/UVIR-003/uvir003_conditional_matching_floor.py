#!/usr/bin/env python3
"""UVIR-003 Stage 2b: Conditional matching floor (after R3 incomplete).

Serial Stage 2b (UVIR-003_SERIAL_STAGE_ORDER):
  2a exited INCOMPLETE_R3_UV_RESIDUE (no action-level Z_psi, r_rho).
  2b freezes an explicit *Conditional-with-scope* matching floor so M3/M6
  documentation is referee-grade without fake Derived K_Q.

Floor content (Conditional — not Derived)
-----------------------------------------
  Structure: R1/R3 map I_a0 = (2/3) C_IR / P
    where P := k_Q  (R1)  or  P := Z_psi * r_rho  (R3 residual rename)
  Free Conditional parameters: P > 0, C_IR > 0
  Domain tables: reuse causality Conditional scan (Rc <= 1) under R1 structure
  Naive point (P,C_IR)=(1,2/3): labelled NON_DERIVED_COMPARISON_ONLY only

Does NOT:
  - promote R1 naive to Derived
  - unlock MAT-001 PASS
  - close UVIR-003 full gate
  - claim physical cutoff as Derived
  - claim observational results

Exit:
  PASS_CONDITIONAL_MATCHING_FLOOR
  stage_2_exit_status: CONDITIONAL_WITH_SCOPE
  physics_pass: false
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import sympy as sp


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument(
        "--r3-audit",
        type=Path,
        default=base / "outputs" / "uvir003_r3_uv_residue_audit_summary.json",
    )
    p.add_argument(
        "--matching-summary",
        type=Path,
        default=base / "outputs" / "uvir003_matching_route_program_summary.json",
    )
    p.add_argument(
        "--causality-conditional",
        type=Path,
        default=base
        / "outputs"
        / "uvir003_causality_domain_conditional_summary.json",
    )
    p.add_argument(
        "--weak-coupling-domain",
        type=Path,
        default=base
        / "outputs"
        / "uvir003_declared_weak_coupling_domain_summary.json",
    )
    p.add_argument(
        "--inventory",
        type=Path,
        default=base / "outputs" / "uvir003_kq_matching_inventory_summary.json",
    )
    return p.parse_args()


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def require(name: str, ok: bool, detail: str = "") -> None:
    if not ok:
        raise AssertionError(f"{name}" + (f": {detail}" if detail else ""))


def floor_identities() -> dict[str, Any]:
    """Closed-form Conditional floor maps (structure only)."""
    P, C_IR, cos_th, q_over_a0 = sp.symbols(
        "P C_IR cos_theta q_over_a0", positive=True
    )
    # P stands for k_Q (R1) or Z_psi*r_rho (R3 residual rename)
    I_a0 = sp.Rational(2, 3) * C_IR / P
    q_cross_over_a0 = sp.simplify(P / (2 * C_IR * (1 + cos_th**2)))
    R_c = sp.simplify(q_over_a0 / q_cross_over_a0)
    # Lambda_|| / diagnostic: Lambda = K_Q^{3/4}/sqrt(A); under R1 K_Q=P/(8 pi G)
    # leave symbolic flag only — no numeric Derived cutoff
    require(
        "Rc = 2 C_IR (1+c^2) q_over_a0 / P",
        sp.simplify(R_c - 2 * C_IR * (1 + cos_th**2) * q_over_a0 / P) == 0,
    )
    return {
        "product_parameter": "P := k_Q (R1) OR Z_psi*r_rho (R3 residual rename)",
        "I_a0": str(I_a0),
        "q_cross_over_a0": str(q_cross_over_a0),
        "R_c": str(R_c),
        "claim_status": "Conditional_structure_only",
        "is_derived_numeric": False,
    }


def floor_premises() -> list[str]:
    return [
        "Stage 2a R3 audit: INCOMPLETE_R3_UV_RESIDUE (no action-level Z_psi, r_rho)",
        "Matching uses redefinition-invariant A*q/K_Q class objects, not bare K_Q alone",
        "Conditional structure: I_a0 = (2/3)*C_IR/P with free P>0, C_IR>0",
        "P may be interpreted as R1 k_Q or R3 Z_psi*r_rho (same algebra; not Derived)",
        "Causality domain tables under R1 structure remain Conditional documentation",
        "Naive (P,C_IR)=(1,2/3) is NON_DERIVED_COMPARISON_ONLY priority flag",
        "M2 weakly-coupled domain freeze remains in force (IR HOLD excluded)",
        "MAT-001 may receive only a scoped Conditional calculation handoff after Stage 2 exit; no MAT PASS",
    ]


def floor_scope() -> dict[str, Any]:
    return {
        "in_scope_Conditional": [
            "Referee documentation of M3 under free (P, C_IR) with domain tables",
            "NDA Lambda_|| diagnostic expressed in invariants once P,C_IR chosen Conditional",
            "Priority flag that naive O(1) points place q_cross ~ 0.375 a0 (parallel)",
            "Stage 3 scoped MAT calculation of V=C_m/sqrt(K_Q) under named Conditional handoff",
        ],
        "out_of_scope_forbidden": [
            "Derived numeric K_Q or Derived Z_psi, r_rho from this floor",
            "MAT-001 gate PASS or Derived C_obs packaging",
            "UVIR-003 full_gate_status PASS",
            "Physical cutoff as Derived strong-coupling scale",
            "Observational SPARC/H0/cosmology claims",
            "Promoting (P,C_IR)=(1,2/3) to Derived",
        ],
        "M3_status_after_floor": "PARTIAL_DOCUMENTED_CONDITIONAL_WITH_SCOPE",
        "M6_status_after_floor": "OPEN_CONDITIONAL_NDA_DIAGNOSTIC_ONLY",
        "M7_status_after_floor": "OPEN_MAT_BLOCKED_FOR_PASS",
    }


def mat_handoff_amendment() -> dict[str, Any]:
    """Written Conditional handoff for Stage 3 — does not unlock MAT PASS."""
    return {
        "title": "Conditional UVIR domain for scoped MAT calculation only",
        "authorizes": [
            "Declare S_int[Psi_m, psi, U, g] as a calculation task",
            "Compute provisional V = C_m/sqrt(K_Q) and C_obs under named premises",
            "Map results onto invariant list without claiming Derived K_Q alone",
        ],
        "does_not_authorize": [
            "MAT-001 subgate PASS report",
            "Downstream Derived use of C_obs or V before UVIR Stage 5 full-gate PASS",
            "SPARC / H0 validation from MAT alone",
            "UVIR-003 full PASS",
        ],
        "required_inputs_from_UVIR": [
            "Track-A force slice + regulator structure",
            "Redefinition invariants Aq/K_Q, A/K_Q^{3/2}, C_m/sqrt(K_Q)",
            "Declared weak-coupling domain (Stage 1)",
            "This Conditional matching floor (Stage 2b)",
        ],
        "status": "HANDOFF_TEXT_ONLY_NOT_MAT_PASS",
    }


def main() -> None:
    args = parse_args()
    r3 = load_json(args.r3_audit)
    match = load_json(args.matching_summary)
    caus = load_json(args.causality_conditional)
    weak = load_json(args.weak_coupling_domain)
    inv = load_json(args.inventory)

    checks: list[dict[str, Any]] = []

    r3_ok = (
        r3 is not None
        and r3.get("classification_code") == "C"
        and r3.get("classification") == "INCOMPLETE_R3_UV_RESIDUE"
    )
    checks.append(
        {
            "name": "stage_2a_r3_incomplete_present",
            "ok": r3_ok,
            "got": None
            if r3 is None
            else {
                "code": r3.get("classification_code"),
                "classification": r3.get("classification"),
                "subgate": r3.get("subgate_status"),
            },
        }
    )

    match_ok = (
        match is not None
        and match.get("subgate_status") == "PASS_MATCHING_ROUTE_PROGRAM_OPEN"
    )
    checks.append(
        {
            "name": "matching_route_program_present",
            "ok": match_ok,
            "got": None if match is None else match.get("subgate_status"),
        }
    )

    inv_ok = (
        inv is not None
        and inv.get("subgate_status") == "PASS_KQ_MATCHING_INVENTORY_OPEN"
    )
    checks.append(
        {
            "name": "kq_inventory_present",
            "ok": inv_ok,
            "got": None if inv is None else inv.get("subgate_status"),
        }
    )

    caus_ok = (
        caus is not None
        and caus.get("subgate_status")
        == "PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING"
        and caus.get("claim_status") == "Conditional"
    )
    checks.append(
        {
            "name": "causality_conditional_domain_present",
            "ok": caus_ok,
            "got": None
            if caus is None
            else {
                "subgate": caus.get("subgate_status"),
                "claim_status": caus.get("claim_status"),
            },
        }
    )

    weak_ok = (
        weak is not None
        and weak.get("subgate_status") == "PASS_DECLARED_WEAK_COUPLING_DOMAIN"
    )
    checks.append(
        {
            "name": "stage1_weak_coupling_domain_present",
            "ok": weak_ok,
            "got": None if weak is None else weak.get("subgate_status"),
        }
    )

    ident = floor_identities()
    checks.append(
        {
            "name": "floor_identities_symbolic_ok",
            "ok": ident["is_derived_numeric"] is False
            and "P" in ident["I_a0"],
        }
    )

    # Naive comparison labelled only
    naive_I = float(sp.Rational(2, 3) * sp.Rational(2, 3) / 1)
    naive = {
        "label": "NON_DERIVED_COMPARISON_ONLY",
        "P": 1.0,
        "C_IR": float(sp.Rational(2, 3)),
        "I_a0": naive_I,
        "q_cross_parallel_over_a0": 0.375,
        "R_c_parallel_at_q_eq_a0": float(6 * sp.Rational(4, 9)),
        "warning": "Priority flag only — not Derived matching",
    }
    checks.append(
        {
            "name": "naive_point_not_promoted",
            "ok": naive["label"] == "NON_DERIVED_COMPARISON_ONLY"
            and abs(naive["I_a0"] - 4.0 / 9.0) < 1e-15,
        }
    )

    # Causality headline from prior Conditional summary
    naive_qc = None
    if caus is not None:
        naive_qc = (caus.get("analytic") or {}).get(
            "naive_parallel_q_cross_over_a0"
        )
    checks.append(
        {
            "name": "causality_naive_qc_consistent_when_present",
            "ok": naive_qc is None or abs(float(naive_qc) - 0.375) < 1e-12,
            "naive_parallel_q_cross_over_a0": naive_qc,
        }
    )

    scope = floor_scope()
    handoff = mat_handoff_amendment()
    premises = floor_premises()

    # Firewall
    firewall = {
        "numeric_Derived_K_Q": False,
        "R1_naive_promoted_to_Derived": False,
        "MAT001_PASS": False,
        "UVIR003_full_PASS": False,
        "physical_cutoff_Derived": False,
        "observational_claim": False,
        "stage2_authorizes_only_scoped_MAT_calculation": True,
    }
    checks.append(
        {
            "name": "claim_firewall",
            "ok": firewall["numeric_Derived_K_Q"] is False
            and firewall["MAT001_PASS"] is False
            and firewall["UVIR003_full_PASS"] is False
            and firewall["R1_naive_promoted_to_Derived"] is False
            and firewall["stage2_authorizes_only_scoped_MAT_calculation"] is True,
            "flags": firewall,
        }
    )

    # Stage 2 exit: Conditional-with-scope (not Derived close)
    stage2_exit = {
        "status": "CONDITIONAL_WITH_SCOPE",
        "M3": scope["M3_status_after_floor"],
        "M6": scope["M6_status_after_floor"],
        "M7": scope["M7_status_after_floor"],
        "allows_stage3_scoped_MAT_calculation": True,
        "allows_MAT_PASS": False,
        "allows_UVIR_full_PASS": False,
    }
    checks.append(
        {
            "name": "stage2_exit_conditional_with_scope",
            "ok": stage2_exit["status"] == "CONDITIONAL_WITH_SCOPE"
            and stage2_exit["allows_MAT_PASS"] is False,
        }
    )

    all_ok = all(c["ok"] for c in checks)
    subgate = (
        "PASS_CONDITIONAL_MATCHING_FLOOR"
        if all_ok
        else "FAIL_CONDITIONAL_MATCHING_FLOOR"
    )

    summary: dict[str, Any] = {
        "gate": "UVIR-003",
        "stage": "B_CONDITIONAL_MATCHING_FLOOR_STAGE_2B",
        "serial_stage": "2b",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "claim_status": "Conditional_with_scope",
        "physics_pass": False,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "kq_numeric_status": "NOT_DERIVED",
        "stage_2a_input": {
            "required": "INCOMPLETE_R3_UV_RESIDUE",
            "present": r3_ok,
        },
        "floor_premises": premises,
        "floor_identities": ident,
        "floor_scope": scope,
        "naive_comparison_only": naive,
        "mat_scoped_handoff_amendment": handoff,
        "stage_2_exit": stage2_exit,
        "prior_artifacts": {
            "r3_audit": None if r3 is None else r3.get("subgate_status"),
            "matching_program": None if match is None else match.get("subgate_status"),
            "causality_conditional": None
            if caus is None
            else caus.get("subgate_status"),
            "weak_coupling_domain": None
            if weak is None
            else weak.get("subgate_status"),
            "inventory": None if inv is None else inv.get("subgate_status"),
        },
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "Freezes a Conditional matching floor after Stage 2a R3 incomplete. "
            "Documents M3/M6 under Conditional-with-scope structure (free P, C_IR) "
            "without Derived K_Q. Authorizes only a written scoped MAT calculation "
            "handoff text — not MAT PASS, not UVIR full PASS, not observations."
        ),
        "next_required": [
            "Stage 2c: re-evaluate causality + NDA diagnostics under this floor (optional re-run of existing Conditional domain scripts)",
            "Stage 3: scoped MAT calculation of V and C_obs under handoff premises only",
            "No MAT PASS or downstream Derived use before UVIR Stage 5",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "uvir003_conditional_matching_floor_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    h = hashlib.sha256(payload).hexdigest()
    (
        args.output_dir / "uvir003_conditional_matching_floor_summary.sha256"
    ).write_bytes(f"{h}  {out.name}\n".encode("utf-8"))

    print("UVIR-003 Stage 2b Conditional matching floor")
    print("  claim_status: Conditional_with_scope")
    print("  stage_2_exit:", stage2_exit["status"])
    print("  physics_pass: False")
    print("  MAT-001: BLOCKED (scoped calculation handoff text only)")
    print("  UVIR full gate: IN_PROGRESS")
    for c in checks:
        mark = "OK" if c["ok"] else "FAIL"
        print(f"  [{mark}] {c['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", h)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
