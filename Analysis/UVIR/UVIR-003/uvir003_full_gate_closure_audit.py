#!/usr/bin/env python3
"""UVIR-003: machine audit of full-gate closure checklist vs summary JSON.

Does **not** close UVIR-003. Reports which Master Plan criteria (M1–M7) have
supporting subgate evidence on disk and which remain OPEN/PARTIAL.

Tier-1 use: reproducible status table for recovery sessions and gate reviews.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_SUBGATES: dict[str, str] = {
    "uvir003_local_four_leg_kernel_summary.json": (
        "PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL"
    ),
    "uvir003_frw_in_in_observable_path_summary.json": (
        "PASS_FRW_IN_IN_OBSERVABLE_PATH_DECLARED"
    ),
    "uvir003_frw_multi_slice_mode_green_summary.json": (
        "PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN"
    ),
    "uvir003_nonzero_gradient_force_local_summary.json": (
        "PASS_NONZERO_GRADIENT_FORCE_LOCAL"
    ),
    "uvir003_declared_unitarity_eft_criterion_summary.json": (
        "PASS_DECLARED_UNITARITY_EFT_CRITERION"
    ),
    "uvir003_kq_matching_inventory_summary.json": (
        "PASS_KQ_MATCHING_INVENTORY_OPEN"
    ),
}

OPTIONAL_SUBGATES: dict[str, str] = {
    "uvir003_local_adiabatic_observable_norm_summary.json": (
        "PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION"
    ),
    "uvir003_four_leg_kinematic_deformation_summary.json": (
        "PASS_FOUR_LEG_KINEMATIC_DEFORMATION_AUDIT"
    ),
    "uvir003_causality_domain_conditional_summary.json": (
        "PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING"
    ),
    "uvir003_matching_route_program_summary.json": (
        "PASS_MATCHING_ROUTE_PROGRAM_OPEN"
    ),
    "uvir003_declared_weak_coupling_domain_summary.json": (
        "PASS_DECLARED_WEAK_COUPLING_DOMAIN"
    ),
    "uvir003_conditional_matching_floor_summary.json": (
        "PASS_CONDITIONAL_MATCHING_FLOOR"
    ),
    "uvir003_stage2c_floor_diagnostics_summary.json": (
        "PASS_STAGE2C_FLOOR_DIAGNOSTICS"
    ),
    "uvir003_stage4_m3m6_conditional_limit_summary.json": (
        "PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT"
    ),
    "uvir003_stage5_full_gate_decision_summary.json": (
        "PASS_STAGE5_DECISION_HOLD_TIER1"
    ),
}


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument("--summaries-dir", type=Path, default=base / "outputs")
    return p.parse_args()


def load_subgate(path: Path) -> str | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        d = json.load(f)
    return (
        d.get("subgate_status")
        or d.get("status")
        or d.get("calculation_status")
    )


def main() -> None:
    args = parse_args()
    evidence: dict[str, Any] = {}
    missing = []
    mismatch = []

    for fname, expected in REQUIRED_SUBGATES.items():
        path = args.summaries_dir / fname
        got = load_subgate(path)
        ok = got == expected
        evidence[fname] = {
            "path": fname,
            "expected": expected,
            "got": got,
            "ok": ok,
            "required": True,
        }
        if got is None:
            missing.append(fname)
        elif not ok:
            mismatch.append(fname)

    optional_ev = {}
    for fname, expected in OPTIONAL_SUBGATES.items():
        path = args.summaries_dir / fname
        got = load_subgate(path)
        optional_ev[fname] = {
            "expected": expected,
            "got": got,
            "ok": got == expected if got is not None else False,
            "present": got is not None,
        }

    required_ok = len(missing) == 0 and len(mismatch) == 0

    # Stage 4/5 optional artefacts used by the fail-closed decision audit
    stage4_ok = optional_ev.get(
        "uvir003_stage4_m3m6_conditional_limit_summary.json", {}
    ).get("ok", False)
    stage5_ok = optional_ev.get(
        "uvir003_stage5_full_gate_decision_summary.json", {}
    ).get("ok", False)
    stage5 = None
    stage5_path = (
        args.summaries_dir / "uvir003_stage5_full_gate_decision_summary.json"
    )
    if stage5_path.exists():
        with stage5_path.open("r", encoding="utf-8") as f:
            stage5 = json.load(f)

    # Master Plan criteria scored fail-closed for tier-1 closure.
    criteria = {
        "M1_selected_action_declared": {
            "status": "PASS_BOUNDED",
            "tier1_met": True,
            "note": "Selected action and bounded Track-A architecture are declared",
        },
        "M2_stability_declared_domain": {
            "status": "PARTIAL_BOUNDED_HIGH_Q_ONLY",
            "tier1_met": False,
            "note": "Relevant IR complex-quartet control remains held",
        },
        "M3_causality_declared_domain": {
            "status": "HOLD_MATCHED_INVARIANT_REQUIRED",
            "tier1_met": False,
            "note": "Conditional domain tables do not replace matched Aq/K_Q",
        },
        "M4_unitarity_path_with_scope": {
            "status": (
                "PASS_SCOPED"
                if evidence["uvir003_declared_unitarity_eft_criterion_summary.json"]["ok"]
                else "FAIL_MISSING"
            ),
            "tier1_met": evidence[
                "uvir003_declared_unitarity_eft_criterion_summary.json"
            ]["ok"],
            "note": "Scoped path only; no optical-theorem claim",
        },
        "M5_invariant_ratios": {
            "status": (
                "PASS_INVENTORY_K_Q_NOT_DERIVED"
                if evidence["uvir003_kq_matching_inventory_summary.json"]["ok"]
                else "FAIL_MISSING"
            ),
            "tier1_met": evidence[
                "uvir003_kq_matching_inventory_summary.json"
            ]["ok"],
            "note": "Invariant combinations identified; matching remains M3/M6 work",
        },
        "M6_physical_cutoff": {
            "status": "HOLD_PHYSICAL_CUTOFF_REQUIRED",
            "tier1_met": False,
            "note": "Conditional NDA diagnostic is not a physical matched cutoff",
        },
        "M7_matter_ready_for_MAT": {
            "status": "PARTIAL_SCOPED_HANDOFF_ONLY",
            "tier1_met": False,
            "note": "MAT engineering handoff exists; MAT PASS and Derived use remain blocked",
        },
    }

    blocking = [key for key, value in criteria.items() if not value["tier1_met"]]

    stage5_consistent = (
        stage5_ok
        and stage5 is not None
        and stage5.get("full_gate_status") == "IN_PROGRESS"
        and stage5.get("decision") == "HOLD_TIER1_CLOSURE"
        and stage5.get("physics_pass_under_declared_conditional_policy") is False
        and stage5.get("physics_pass_derived_theory_closed") is False
    )

    full_gate = "IN_PROGRESS"
    mat001 = "BLOCKED_PASS_TAG_FORBIDDEN"
    # The audit calculation passes only when required evidence is intact and the
    # present Stage-5 decision fails closed. It never copies a physics status.
    audit_pass = required_ok and stage5_consistent

    summary = {
        "gate": "UVIR-003",
        "stage": "FULL_GATE_CLOSURE_AUDIT",
        "calculation_status": "PASS" if audit_pass else "FAIL",
        "subgate_status": (
            "PASS_UVIR003_CLOSURE_CHECKLIST_AUDIT"
            if audit_pass
            else "FAIL_UVIR003_CLOSURE_CHECKLIST_AUDIT"
        ),
        "full_gate_status": full_gate,
        "mat001_status": mat001,
        "master_plan_criteria": criteria,
        "blocking_for_full_pass": blocking,
        "required_subgate_evidence": evidence,
        "optional_subgate_evidence": optional_ev,
        "missing_required_summaries": missing,
        "mismatched_required_summaries": mismatch,
        "stage4_policy_present": stage4_ok,
        "stage5_decision_present": stage5_ok,
        "stage5_decision_consistent": stage5_consistent,
        "scientific_boundary": (
            "Audits evidence integrity and the fail-closed Stage-5 decision. "
            "UVIR-003 remains IN_PROGRESS because M2, M3, M6 and M7 are not "
            "tier-1 complete. This audit does not derive K_Q or V, establish a "
            "physical cutoff, control the relevant IR response, or issue MAT PASS."
        ),
        "next_required_calculation": [
            "Compute V or an equivalent matched invariant from one declared action/field chart",
            "Re-evaluate causality with the matched invariant",
            "Establish the physical cutoff/unitarity result in the claim domain",
            "Control the relevant IR complex-quartet response",
            "Run a later independent Stage-5 closure review",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "uvir003_full_gate_closure_audit_summary.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")

    print("UVIR-003 full gate:", full_gate)
    print("MAT-001:", mat001)
    print("Required subgates OK:", required_ok)
    print("Blocking criteria:", ", ".join(blocking) if blocking else "(none)")
    for k, v in criteria.items():
        print(f"  {k}: {v['status']}")
    print(f"STATUS: {summary['subgate_status']}")
    if not audit_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
