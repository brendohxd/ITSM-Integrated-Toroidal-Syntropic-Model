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
            "path": str(path),
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

    # Master Plan criteria scoring (manual policy encoded explicitly)
    criteria = {
        "M1_selected_action_declared": {
            "status": "PASS_BOUNDED",
            "note": "Stage A + Track A force architecture on branch",
        },
        "M2_stability_declared_domain": {
            "status": (
                "PASS_BOUNDED"
                if (
                    args.summaries_dir
                    / "uvir003_declared_weak_coupling_domain_summary.json"
                ).exists()
                and load_subgate(
                    args.summaries_dir
                    / "uvir003_declared_weak_coupling_domain_summary.json"
                )
                == "PASS_DECLARED_WEAK_COUPLING_DOMAIN"
                else "PARTIAL"
            ),
            "note": (
                "PASS_BOUNDED if Stage-1 domain freeze present: high-q+Track-A in; "
                "IR HOLD excluded from weakly-coupled domain"
            ),
        },
        "M3_causality_declared_domain": {
            "status": "PARTIAL",
            "note": (
                "Documented Conditional R1 domain + route maps (R2 V target); "
                "Derived close still needs matched A q / K_Q"
            ),
        },
        "M4_unitarity_path_with_scope": {
            "status": "PASS_SCOPED" if evidence[
                "uvir003_declared_unitarity_eft_criterion_summary.json"
            ]["ok"] else "FAIL_MISSING",
            "note": "Declared tree/NDA criterion; optical theorem not computed",
        },
        "M5_invariant_ratios": {
            "status": "PASS_INVENTORY" if evidence[
                "uvir003_kq_matching_inventory_summary.json"
            ]["ok"] else "FAIL_MISSING",
            "note": "Invariants listed; numeric K_Q NOT_DERIVED",
        },
        "M6_physical_cutoff": {
            "status": "OPEN",
            "note": "Blocked on matching; NDA Lambda_parallel only",
        },
        "M7_matter_ready_for_MAT": {
            "status": "OPEN",
            "note": "MAT-001 remains BLOCKED for Derived vertex",
        },
    }

    # Full gate: all of M1–M6 closed at least PARTIAL→PASS without OPEN musts
    # Policy: full PASS requires M1 ok, M2 not OPEN, M3 not OPEN, M4 pass,
    # M5 pass, M6 not OPEN. Today M3 and M6 OPEN/PARTIAL → full not closed.
    open_musts = [
        k
        for k, v in criteria.items()
        if v["status"] in ("OPEN", "FAIL_MISSING")
        or str(v["status"]).startswith("PARTIAL")
        and k in ("M3_causality_declared_domain", "M2_stability_declared_domain")
    ]
    # Stricter: full gate closed only if no OPEN and no PARTIAL on M2,M3,M6
    # PASS_BOUNDED is allowed for M2 (declared domain)
    blocking = [
        k
        for k, v in criteria.items()
        if v["status"] in ("OPEN", "FAIL_MISSING", "PARTIAL")
        and k
        in (
            "M2_stability_declared_domain",
            "M3_causality_declared_domain",
            "M6_physical_cutoff",
            "M7_matter_ready_for_MAT",
        )
    ]

    full_gate = "IN_PROGRESS"
    mat001 = "BLOCKED"
    # Audit of *checklist infrastructure* passes if required subgates present
    audit_pass = required_ok

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
        "scientific_boundary": (
            "Audits presence of post-alpha.9/10 subgate summaries and scores "
            "Master Plan UVIR-003 criteria as PASS_BOUNDED/PARTIAL/OPEN. "
            "Does not close UVIR-003, derive K_Q, compute optical theorem, "
            "or unlock MAT-001."
        ),
        "next_required_calculation": [
            "Serial Stage 2a: dig-harder R3 Z_psi, r_rho (or 2b Conditional floor)",
            "Stage 2c: re-evaluate causality + Lambda_|| under floor",
            "Stage 3 MAT only after Stage 2 exit (compute V from S_int)",
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
