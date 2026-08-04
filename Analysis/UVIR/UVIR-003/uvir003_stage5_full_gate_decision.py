#!/usr/bin/env python3
"""UVIR-003 Stage 5: tier-1 full-gate decision audit.

Master Plan §5.1 UVIR-003 pass wording:
  Selected action stable/causal/weakly coupled in declared domain;
  invariant ratios; physical cutoff/unitarity path stated with scope.

Tier-1 / peer-review standard (this package)
--------------------------------------------
Records a successful *decision audit* but holds the physics gate while
mandatory physics remains Conditional or outside the relevant tested domain.

Current output:
  decision = HOLD_TIER1_CLOSURE
  full_gate_status = IN_PROGRESS

Evidence required before a later independent closure review:
  * matched Aq/K_Q (or an equivalent field-redefinition invariant)
  * causality over the physical domain used by downstream claims
  * a gauge-invariant, canonically normalized physical cutoff/unitarity result
  * control of the relevant infrared complex-quartet response

Does NOT:
  - derive K_Q or V
  - issue MAT-001 PASS
  - authorize downstream Derived SCR/LEN/DISK/P3/P4 packaging
  - promote R1 naive (P,C_IR)=(1,2/3)
  - convert an exclusion or policy declaration into a physics pass

Exit:
  PASS_STAGE5_DECISION_HOLD_TIER1
  full_gate_status: IN_PROGRESS
  mat001_status: BLOCKED_PASS_TAG_FORBIDDEN
  physics_pass_under_declared_conditional_policy: false
  physics_pass_derived_theory_closed: false
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parents[1] / "MAT" / "MAT-001" / "outputs"
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument(
        "--summaries-dir",
        type=Path,
        default=base / "outputs",
        help="Directory of UVIR-003 summary JSON artifacts",
    )
    p.add_argument(
        "--mat-summary",
        type=Path,
        default=mat / "mat001_scoped_calculation_summary.json",
    )
    return p.parse_args()


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def subgate(d: dict[str, Any] | None) -> str | None:
    if d is None:
        return None
    return d.get("subgate_status") or d.get("status") or d.get("calculation_status")


def check_eq(
    name: str, got: Any, expected: Any, checks: list[dict[str, Any]]
) -> bool:
    ok = got == expected
    checks.append({"name": name, "ok": ok, "got": got, "expected": expected})
    return ok


def check_true(name: str, ok: bool, checks: list[dict[str, Any]], **extra: Any) -> bool:
    row: dict[str, Any] = {"name": name, "ok": ok}
    row.update(extra)
    checks.append(row)
    return ok


def scoped_or_deferred_items() -> dict[str, Any]:
    """Scoped or deferred items; these never count as positive closure evidence."""
    return {
        "optical_theorem_multi_channel_unitarity": {
            "status": "PERMANENTLY_EXCLUDED_FROM_UVIR003_GATE",
            "rationale": (
                "Master Plan requires unitarity *path stated with scope* (M4), "
                "not a completed optical theorem. Optical theorem deferred to a "
                "later dedicated gate if claimed observationally."
            ),
            "evidence": "PASS_DECLARED_UNITARITY_EFT_CRITERION (tree/NDA only)",
        },
        "full_in_in_nested_integrals": {
            "status": "PERMANENTLY_DEFERRED_FROM_UVIR003_PASS_CLAIMS",
            "rationale": (
                "Path declared (PASS_FRW_IN_IN_OBSERVABLE_PATH_DECLARED); full "
                "nested in-in integrals are not computed and are not smuggled as PASS."
            ),
            "evidence": "PASS_FRW_IN_IN_OBSERVABLE_PATH_DECLARED; multi-slice Green is high-q proxy only",
        },
        "IR_HOLD_complex_quartet_modes": {
            "status": "UNRESOLVED_RELEVANT_IR_HOLD",
            "rationale": "High-q evidence does not control the relevant IR complex-quartet response.",
            "evidence": "PASS_DECLARED_WEAK_COUPLING_DOMAIN",
        },
        "homogeneous_zero_gradient_Y32_S_matrix": {
            "status": "PERMANENTLY_EXCLUDED_FROM_UVIR003_FORCE_PASS_CLAIMS",
            "rationale": "Track-A programme is nonzero-gradient local force only.",
            "evidence": "PASS_NONZERO_GRADIENT_FORCE_LOCAL; Stage 1 exclude list",
        },
        "Derived_numeric_K_Q": {
            "status": "NOT_CLAIMED",
            "rationale": "Inventory Open; R3 incomplete; Stage 3 V NOT_COMPUTED.",
            "evidence": "PASS_KQ_MATCHING_INVENTORY_OPEN; Stage 4 branch B",
        },
    }


def master_plan_wording_map(criteria: dict[str, Any]) -> dict[str, Any]:
    """Map Master Plan one-line pass condition to criterion evidence."""
    return {
        "selected_action": {
            "clause": "Selected action",
            "criterion": "M1",
            "status": criteria["M1"]["status"],
            "met_under_policy": criteria["M1"]["status"] == "PASS_BOUNDED",
        },
        "stable_in_declared_domain": {
            "clause": "stable ... in declared domain",
            "criterion": "M2",
            "status": criteria["M2"]["status"],
            "met_under_policy": criteria["M2"]["status"] == "PASS_BOUNDED",
        },
        "causal_in_declared_domain": {
            "clause": "causal ... in declared domain",
            "criterion": "M3",
            "status": criteria["M3"]["status"],
            "met_under_policy": criteria["M3"]["status"]
            == "PERMANENT_CONDITIONAL_WITH_SCOPE",
            "note": "Conditional domain + floor; not Derived matched Aq/K_Q",
        },
        "weakly_coupled_in_declared_domain": {
            "clause": "weakly coupled in declared domain",
            "criterion": "M2+M4",
            "status": f"{criteria['M2']['status']}+{criteria['M4']['status']}",
            "met_under_policy": (
                criteria["M2"]["status"] == "PASS_BOUNDED"
                and criteria["M4"]["status"] == "PASS_SCOPED"
            ),
        },
        "invariant_ratios": {
            "clause": "invariant ratios",
            "criterion": "M5",
            "status": criteria["M5"]["status"],
            "met_under_policy": criteria["M5"]["status"]
            == "PASS_INVENTORY_K_Q_NOT_DERIVED",
        },
        "physical_cutoff_stated_with_scope": {
            "clause": "physical cutoff ... stated with scope",
            "criterion": "M6",
            "status": criteria["M6"]["status"],
            "met_under_policy": criteria["M6"]["status"]
            == "PERMANENT_CONDITIONAL_NDA_DIAGNOSTIC",
            "note": "NDA diagnostic under floor P; not Derived matched scale",
        },
        "unitarity_path_stated_with_scope": {
            "clause": "unitarity path stated with scope",
            "criterion": "M4 + optical theorem exclusion",
            "status": criteria["M4"]["status"],
            "met_under_policy": criteria["M4"]["status"] == "PASS_SCOPED",
        },
    }


def main() -> None:
    args = parse_args()
    sd = args.summaries_dir
    checks: list[dict[str, Any]] = []

    # --- Load serial chain artifacts ---
    art = {
        "stage1_domain": load_json(sd / "uvir003_declared_weak_coupling_domain_summary.json"),
        "stage2a_r3": load_json(sd / "uvir003_r3_uv_residue_audit_summary.json"),
        "stage2b_floor": load_json(sd / "uvir003_conditional_matching_floor_summary.json"),
        "stage2c": load_json(sd / "uvir003_stage2c_floor_diagnostics_summary.json"),
        "stage4": load_json(sd / "uvir003_stage4_m3m6_conditional_limit_summary.json"),
        "unitarity": load_json(sd / "uvir003_declared_unitarity_eft_criterion_summary.json"),
        "inventory": load_json(sd / "uvir003_kq_matching_inventory_summary.json"),
        "matching_routes": load_json(sd / "uvir003_matching_route_program_summary.json"),
        "causality_cond": load_json(sd / "uvir003_causality_domain_conditional_summary.json"),
        "four_leg": load_json(sd / "uvir003_local_four_leg_kernel_summary.json"),
        "green": load_json(sd / "uvir003_frw_multi_slice_mode_green_summary.json"),
        "track_a": load_json(sd / "uvir003_nonzero_gradient_force_local_summary.json"),
        "in_in_path": load_json(sd / "uvir003_frw_in_in_observable_path_summary.json"),
        "audit": load_json(sd / "uvir003_full_gate_closure_audit_summary.json"),
        "mat": load_json(args.mat_summary),
    }

    # Path-package / Stage 0–1 required presence
    check_eq(
        "alpha10_four_leg",
        subgate(art["four_leg"]),
        "PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL",
        checks,
    )
    check_eq(
        "alpha10_green",
        subgate(art["green"]),
        "PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN",
        checks,
    )
    check_eq(
        "alpha10_track_a",
        subgate(art["track_a"]),
        "PASS_NONZERO_GRADIENT_FORCE_LOCAL",
        checks,
    )
    check_eq(
        "M4_unitarity_criterion",
        subgate(art["unitarity"]),
        "PASS_DECLARED_UNITARITY_EFT_CRITERION",
        checks,
    )
    check_eq(
        "M5_inventory",
        subgate(art["inventory"]),
        "PASS_KQ_MATCHING_INVENTORY_OPEN",
        checks,
    )
    check_eq(
        "M2_domain_freeze",
        subgate(art["stage1_domain"]),
        "PASS_DECLARED_WEAK_COUPLING_DOMAIN",
        checks,
    )
    check_eq(
        "stage2b_floor",
        subgate(art["stage2b_floor"]),
        "PASS_CONDITIONAL_MATCHING_FLOOR",
        checks,
    )
    check_eq(
        "stage2c_diagnostics",
        subgate(art["stage2c"]),
        "PASS_STAGE2C_FLOOR_DIAGNOSTICS",
        checks,
    )
    check_eq(
        "stage4_conditional_record",
        subgate(art["stage4"]),
        "PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT",
        checks,
    )
    check_eq(
        "stage3_mat_scoped_no_pass",
        subgate(art["mat"]),
        "PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL",
        checks,
    )
    check_true(
        "mat001_pass_still_false",
        art["mat"] is not None and art["mat"].get("mat001_pass") is False,
        checks,
        mat001_pass=None if art["mat"] is None else art["mat"].get("mat001_pass"),
    )
    check_true(
        "V_still_not_computed",
        art["mat"] is not None and art["mat"].get("V_status") == "NOT_COMPUTED",
        checks,
        V_status=None if art["mat"] is None else art["mat"].get("V_status"),
    )
    check_eq(
        "in_in_path_declared",
        subgate(art["in_in_path"]),
        "PASS_FRW_IN_IN_OBSERVABLE_PATH_DECLARED",
        checks,
    )
    check_eq(
        "causality_conditional_domain",
        subgate(art["causality_cond"]),
        "PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING",
        checks,
    )
    check_eq(
        "matching_route_program",
        subgate(art["matching_routes"]),
        "PASS_MATCHING_ROUTE_PROGRAM_OPEN",
        checks,
    )

    # Stage 4 exit integrity
    s4_exit = (art["stage4"] or {}).get("stage_4_exit", {})
    check_true(
        "stage4_exit_holds_matched_reopen",
        s4_exit.get("status") == "HOLD_MATCHED_STAGE4A_REQUIRED",
        checks,
        exit=s4_exit.get("status"),
    )
    s4_criteria = (art["stage4"] or {}).get("master_plan_criteria_after_stage4", {})
    check_eq(
        "stage4_M3_status",
        s4_criteria.get("M3"),
        "HOLD_MATCHED_INVARIANT_REQUIRED",
        checks,
    )
    check_eq(
        "stage4_M6_status",
        s4_criteria.get("M6"),
        "HOLD_PHYSICAL_CUTOFF_REQUIRED",
        checks,
    )

    # Criteria assessed against a tier-1 closure standard.
    criteria: dict[str, Any] = {
        "M1": {
            "status": "PASS_BOUNDED",
            "tier1_met": True,
            "note": "Selected action and bounded Track-A architecture are declared",
        },
        "M2": {
            "status": "PARTIAL_BOUNDED_HIGH_Q_ONLY",
            "tier1_met": False,
            "note": "High-q slice is bounded; relevant IR complex-quartet control remains held",
            "evidence": "PASS_DECLARED_WEAK_COUPLING_DOMAIN",
        },
        "M3": {
            "status": "HOLD_MATCHED_INVARIANT_REQUIRED",
            "tier1_met": False,
            "note": "Conditional domain tables do not replace matched Aq/K_Q",
            "evidence": "Stage 4 Conditional programme-limit record",
        },
        "M4": {
            "status": "PASS_SCOPED",
            "tier1_met": True,
            "note": "A scoped tree/NDA unitarity path is declared; no optical-theorem claim",
            "evidence": "PASS_DECLARED_UNITARITY_EFT_CRITERION",
        },
        "M5": {
            "status": "PASS_INVENTORY_K_Q_NOT_DERIVED",
            "tier1_met": True,
            "note": "Field-redefinition invariants are identified; matching remains M3/M6 work",
            "evidence": "PASS_KQ_MATCHING_INVENTORY_OPEN",
        },
        "M6": {
            "status": "HOLD_PHYSICAL_CUTOFF_REQUIRED",
            "tier1_met": False,
            "note": "Conditional NDA diagnostic is not a matched physical cutoff",
            "evidence": "Stage 4 Conditional programme-limit record",
        },
        "M7": {
            "status": "PARTIAL_SCOPED_HANDOFF_ONLY",
            "tier1_met": False,
            "note": "MAT engineering may continue, but MAT PASS and Derived use remain blocked",
            "evidence": "Stage 2b handoff + Stage 3 provisional calculation",
        },
    }

    wording = master_plan_wording_map(criteria)
    wording_ok = all(v.get("met_under_policy") for v in wording.values())
    check_true(
        "master_plan_wording_not_fully_met_for_tier1",
        wording_ok is False,
        checks,
        all_clauses_met=wording_ok,
    )

    exclusions = scoped_or_deferred_items()
    exclusion_statuses = {k: v["status"] for k, v in exclusions.items()}
    check_true(
        "scope_items_include_unresolved_ir_and_do_not_close_gate",
        exclusion_statuses.get("IR_HOLD_complex_quartet_modes")
        == "UNRESOLVED_RELEVANT_IR_HOLD",
        checks,
        statuses=exclusion_statuses,
    )

    # Tier-1 firewall: the decision package must record a hold, not a physics pass.
    firewall = {
        "unqualified_full_gate_PASS": False,
        "bounded_conditional_full_gate_PASS": False,
        "Derived_theory_closed": False,
        "Derived_K_Q": False,
        "Derived_V": False,
        "Derived_matched_Aq_over_KQ": False,
        "Derived_physical_cutoff": False,
        "R1_naive_promoted_to_Derived": False,
        "MAT001_PASS": False,
        "downstream_Derived_SCR_LEN_DISK_P3_P4": False,
        "SPARC_or_H0_validation": False,
        "dual_RAR_a0_cH0_C_2_3": False,
        "optical_theorem_claimed": False,
        "full_in_in_claimed_computed": False,
    }
    check_true(
        "claim_firewall",
        all(v is False for v in firewall.values()),
        checks,
        flags=firewall,
    )

    blocking = [mid for mid, criterion in criteria.items() if not criterion["tier1_met"]]
    check_true(
        "tier1_blockers_recorded",
        blocking == ["M2", "M3", "M6", "M7"],
        checks,
        blocking=blocking,
    )

    # Naive point remains comparison-only.
    floor = art["stage2b_floor"] or {}
    naive_ok = floor.get("claim_firewall", {}).get(
        "R1_naive_promoted_to_Derived", False
    ) is False
    check_true("naive_R1_not_promoted", naive_ok, checks)

    evidence_integrity_ok = all(c["ok"] for c in checks)
    if evidence_integrity_ok:
        full_gate = "IN_PROGRESS"
        subgate_status = "PASS_STAGE5_DECISION_HOLD_TIER1"
        calc = "PASS"
        decision = "HOLD_TIER1_CLOSURE"
    else:
        full_gate = "IN_PROGRESS"
        subgate_status = "FAIL_STAGE5_DECISION_AUDIT"
        calc = "FAIL"
        decision = "HOLD_EVIDENCE_INTEGRITY_FAILURE"

    # MAT: PASS tag still forbidden; handoff for further MAT work is open under Conditional UVIR.
    mat001_status = "BLOCKED_PASS_TAG_FORBIDDEN"
    mat_handoff = {
        "allows_MAT_calculation_work": True,
        "allows_MAT001_PASS": False,
        "allows_downstream_Derived_from_MAT": False,
        "requires_for_MAT_PASS": [
            "Compute V from S_int / force kinetic chart",
            "Report C_obs as Derived from micro S_int or keep Conditional baseline explicit",
            "MAT-001 checklist complete with claim ledger",
        ],
        "note": (
            "The scoped Stage-2/3 handoff permits provisional MAT engineering only; "
            "UVIR remains IN_PROGRESS and no MAT PASS or Derived packaging is authorized."
        ),
    }

    residual_peer_review_risks = [
        {
            "risk": "Referee may demand Derived Aq/K_Q before accepting force-sector claims",
            "mitigation": "Claim status Conditional; no Derived packaging; Stage 4A reopen path documented",
        },
        {
            "risk": "K_Q NOT_DERIVED leaves absolute normalization free",
            "mitigation": "Only redefinition invariants used in domain statements; free P explicit",
        },
        {
            "risk": "V NOT_COMPUTED blocks R2 Derived upgrade",
            "mitigation": "Stated NOT_COMPUTED; MAT PASS forbidden; optional Stage 4A",
        },
        {
            "risk": "Optical theorem absent",
            "mitigation": "Deferred from the present scoped path; M4 records only a path-with-scope",
        },
    ]

    summary: dict[str, Any] = {
        "gate": "UVIR-003",
        "stage": "STAGE5_FULL_GATE_DECISION",
        "serial_stage": 5,
        "calculation_status": calc,
        "subgate_status": subgate_status,
        "decision": decision,
        "full_gate_status": full_gate,
        "claim_status": "Open_tier1_closure_hold",
        "physics_pass_under_declared_conditional_policy": False,
        "physics_pass_derived_theory_closed": False,
        "mat001_status": mat001_status,
        "mat_handoff": mat_handoff,
        "kq_numeric_status": "NOT_DERIVED",
        "V_status": "NOT_COMPUTED",
        "master_plan_criteria": criteria,
        "master_plan_wording_map": wording,
        "unresolved_scope_items": exclusions,
        "blocking_for_tier1_closure": blocking,
        "residual_peer_review_risks": residual_peer_review_risks,
        "prior_artifacts": {k: subgate(v) for k, v in art.items()},
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "Stage 5 decision audit executed successfully but holds UVIR-003 at "
            "IN_PROGRESS for tier-1 closure. The bounded high-q and Track-A evidence "
            "is retained, while matched causality, a physical cutoff, and relevant "
            "infrared control remain mandatory blockers. This is not MAT PASS and "
            "does not authorize downstream Derived observational packaging."
        ),
        "next_required": [
            "Compute V=C_m/sqrt(K_Q), or an equivalent matched invariant, from one declared action/field chart",
            "Reopen Stage 4A and re-evaluate causality with the matched invariant",
            "Establish a gauge-invariant physical cutoff/unitarity result in the declared claim domain",
            "Resolve or control the relevant infrared complex-quartet response",
            "Run a later independent Stage 5 closure review; MAT PASS remains blocked",
        ],    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "uvir003_stage5_full_gate_decision_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    h = hashlib.sha256(payload).hexdigest()
    (args.output_dir / "uvir003_stage5_full_gate_decision_summary.sha256").write_bytes(
        f"{h}  {out.name}\n".encode("utf-8")
    )

    print("UVIR-003 Stage 5 tier-1 closure decision audit")
    print(f"  decision: {decision}")
    print(f"  full_gate_status: {full_gate}")
    print("  physics_pass: False | derived_theory_closed: False")
    print(f"  MAT-001: {mat001_status}")
    print(f"  K_Q: NOT_DERIVED | V: NOT_COMPUTED")
    for mid, c in criteria.items():
        print(f"  {mid}: {c['status']}")
    for c in checks:
        print(f"  [{'OK' if c['ok'] else 'FAIL'}] {c['name']}")
    print("STATUS:", subgate_status)
    print("JSON_SHA256:", h)
    if calc != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
