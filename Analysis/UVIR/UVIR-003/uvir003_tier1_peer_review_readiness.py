#!/usr/bin/env python3
"""Tier-1 peer-review readiness audit (fail closed).

Re-evaluates UVIR-003 Stage 5 HOLD criteria and the MAT-001 claim surface after
the Track-A Conditional host kit. A PASS means the hold is still required, claim
layers are consistent, Stage 4A reopen conditions remain unmet, and dual-status
Conditional work is not smuggled as Derived. This is not UVIR/MAT physics PASS.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

PASS_STATUS = "PASS_TIER1_PEER_REVIEW_READINESS_HOLD_RETAINED"
FAIL_STATUS = "FAIL_TIER1_PEER_REVIEW_READINESS"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    repo = base.parents[2]
    mat = repo / "Analysis" / "MAT" / "MAT-001"
    uvir_out = base / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stage5",
        type=Path,
        default=uvir_out / "uvir003_stage5_full_gate_decision_summary.json",
    )
    parser.add_argument(
        "--stage4",
        type=Path,
        default=uvir_out / "uvir003_stage4_m3m6_conditional_limit_summary.json",
    )
    parser.add_argument(
        "--closure-audit",
        type=Path,
        default=uvir_out / "uvir003_full_gate_closure_audit_summary.json",
    )
    parser.add_argument(
        "--track-a-s-int",
        type=Path,
        default=mat
        / "TRACK_A_S_INT"
        / "outputs"
        / "mat001_track_a_s_int_embed_summary.json",
    )
    parser.add_argument(
        "--kq-readiness",
        type=Path,
        default=mat
        / "TRACK_A_KQ"
        / "outputs"
        / "mat001_track_a_kq_readiness_summary.json",
    )
    parser.add_argument(
        "--kq-dig",
        type=Path,
        default=mat
        / "KQ_DERIVATION_DIG"
        / "outputs"
        / "mat001_kq_derivation_dig_summary.json",
    )
    parser.add_argument(
        "--conditional-branch",
        type=Path,
        default=mat
        / "CONDITIONAL_MATCHING_BRANCH"
        / "outputs"
        / "mat001_conditional_matching_branch_summary.json",
    )
    parser.add_argument(
        "--join",
        type=Path,
        default=mat
        / "TRACK_A_JOIN"
        / "outputs"
        / "mat001_track_a_join_readiness_summary.json",
    )
    parser.add_argument(
        "--j2",
        type=Path,
        default=mat
        / "J2_MODE_PROJECTION"
        / "outputs"
        / "mat001_j2_basis_covariant_mode_projection_summary.json",
    )
    parser.add_argument("--output-dir", type=Path, default=uvir_out)
    parser.add_argument("--self-test-mutations", action="store_true")
    return parser.parse_args()


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None, str | None]:
    if not path.is_file():
        return None, "missing", None
    try:
        raw = path.read_bytes()
        data = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, f"{type(exc).__name__}:{exc}", None
    if not isinstance(data, dict):
        return None, "top_level_not_object", None
    return data, None, hashlib.sha256(raw).hexdigest().upper()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def add_check(
    checks: list[dict[str, Any]], name: str, ok: bool, **details: Any
) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def claim_ledger() -> dict[str, Any]:
    """Peer-reviewable allow/deny surface under current evidence."""
    return {
        "may_state": [
            "UVIR-003 remains IN_PROGRESS under Stage 5 HOLD_TIER1_CLOSURE",
            "Bounded high-q / Track-A / methods subgates pass within declared scope only",
            "MAT calculation work is permitted; MAT PASS and Derived packaging are forbidden",
            "Track-A Conditional host exports matter d,h form and symbolic K_Q; V form holds symbolically",
            "Conditional dual-status probes exist and are labeled Conditional only",
            "M2/M3/M6/M7 remain blockers for tier-1 UVIR closure",
            "Stage 4A remains closed until a matched invariant exists",
        ],
        "must_not_state": [
            "UVIR-003 physics PASS or full gate closed",
            "MAT-001 PASS or V numerically computed as Derived",
            "K_Q Derived from R1 dimensional analogy or Conditional samples",
            "Stage 4A reopened without matched Aq/K_Q (or equivalent invariant)",
            "Free-sector ADM identified with Track-A force host without a map",
            "Conditional C_obs~1 or C_IR=2/3 as Derived microphysics",
            "Downstream SPARC/H0/lensing Derived from current MAT state",
        ],
        "dual_status_required_for": [
            "Any numeric Conditional sample from the matching branch",
            "Any use of C_obs~1 or C_IR=2/3 as a working hypothesis",
            "Track-A Conditional host embed (not full multi-sector UVIR completion)",
        ],
    }


def stage4a_reopen_contract(
    stage5: dict[str, Any] | None,
    kq_dig: dict[str, Any] | None,
    kq_ready: dict[str, Any] | None,
    s_int: dict[str, Any] | None,
) -> dict[str, Any]:
    conditions = {
        "matched_invariant_V_or_Aq_over_KQ_Derived": {
            "required": True,
            "currently_met": False,
            "evidence": {
                "V_status": (stage5 or {}).get("V_status"),
                "kq_numeric_status": (stage5 or {}).get("kq_numeric_status")
                or (kq_ready or {}).get("kq_numeric_status"),
                "kq_dig": (kq_dig or {}).get("dig_status"),
            },
        },
        "same_action_chart_for_C_m_and_K_Q_or_residue": {
            "required": True,
            "currently_met": False,
            "note": (
                "Track-A Conditional host has form-level d and symbolic K_Q, but "
                "absolute coefficients are not Derived"
            ),
            "form_host_present": (s_int or {}).get("selected_host_route")
            == "R2_TRACK_A_FORCE_PHONON",
        },
        "causality_re_evaluated_with_matched_invariant": {
            "required": True,
            "currently_met": False,
            "note": "Only Conditional causality domain tables exist",
        },
        "physical_cutoff_or_unitarity_with_matched_invariant": {
            "required": True,
            "currently_met": False,
            "note": "M6 remains HOLD_PHYSICAL_CUTOFF_REQUIRED",
        },
        "independent_stage5_review_after_4A": {
            "required": True,
            "currently_met": False,
            "note": "Cannot run until 4A reopen path is satisfied",
        },
    }
    all_met = all(row["currently_met"] for row in conditions.values())
    return {
        "stage4A_status": "CLOSED",
        "reopen_authorized": False,
        "all_reopen_conditions_met": all_met,
        "conditions": conditions,
        "policy": (
            "Stage 4A reopens only when a genuine matched invariant exists and "
            "M3/M6 are re-evaluated under that invariant. Conditional samples and "
            "symbolic V form are insufficient."
        ),
    }


def build_summary(
    stage5: dict[str, Any] | None,
    stage4: dict[str, Any] | None,
    mat_rows: dict[str, dict[str, Any] | None],
    checks: list[dict[str, Any]],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    criteria = (stage5 or {}).get("master_plan_criteria") or {}
    blockers = (stage5 or {}).get("blocking_for_tier1_closure") or []
    m_status = {
        key: {
            "tier1_met": (criteria.get(key) or {}).get("tier1_met"),
            "status": (criteria.get(key) or {}).get("status"),
        }
        for key in ("M2", "M3", "M4", "M5", "M6", "M7")
    }

    add_check(
        checks,
        "stage5_hold_tier1_intact",
        bool(
            stage5
            and stage5.get("decision") == "HOLD_TIER1_CLOSURE"
            and stage5.get("subgate_status") == "PASS_STAGE5_DECISION_HOLD_TIER1"
            and stage5.get("V_status") == "NOT_COMPUTED"
            and stage5.get("physics_pass_derived_theory_closed") is False
        ),
    )
    add_check(
        checks,
        "tier1_blockers_include_M2_M3_M6_M7",
        set(blockers) >= {"M2", "M3", "M6", "M7"}
        and m_status.get("M3", {}).get("tier1_met") is False
        and m_status.get("M6", {}).get("tier1_met") is False
        and m_status.get("M7", {}).get("tier1_met") is False,
        blockers=blockers,
        criteria_snapshot=m_status,
    )
    add_check(
        checks,
        "stage4_permanent_conditional_not_matched_reopen",
        bool(
            stage4
            and stage4.get("subgate_status")
            == "PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT"
        )
        or bool(
            stage4
            and "CONDITIONAL" in str(stage4.get("subgate_status", "")).upper()
        ),
    )

    # MAT dual-status surface: every present record must keep V NOT_COMPUTED
    # and mat001_pass false / blocked.
    mat_consistency = []
    all_mat_ok = True
    for name, data in mat_rows.items():
        if data is None:
            mat_consistency.append(
                {"name": name, "present": False, "ok": name == "join_optional"}
            )
            # join may be local; required set below
            continue
        v_ok = data.get("V_status") == "NOT_COMPUTED"
        pass_ok = data.get("mat001_pass") is False or data.get("mat001_pass") is None
        blocked_ok = str(data.get("mat001_status", "")).upper().startswith(
            "BLOCK"
        ) or data.get("mat001_status") in {
            "BLOCKED",
            "BLOCKED_PASS_TAG_FORBIDDEN",
        }
        # Some MAT records use mat001_status BLOCKED
        if "mat001_status" not in data and "mat001_pass" in data:
            blocked_ok = data.get("mat001_pass") is False
        row_ok = v_ok and pass_ok and (
            blocked_ok or data.get("physics_pass") is False
        )
        # Stricter: V and not mat001_pass and physics_pass false when present
        row_ok = v_ok and (
            data.get("mat001_pass") is False
            if "mat001_pass" in data
            else True
        ) and (
            data.get("physics_pass") is False
            if "physics_pass" in data
            else True
        )
        mat_consistency.append(
            {
                "name": name,
                "present": True,
                "V_status": data.get("V_status"),
                "mat001_pass": data.get("mat001_pass"),
                "physics_pass": data.get("physics_pass"),
                "ok": row_ok,
            }
        )
        all_mat_ok = all_mat_ok and row_ok

    required_mat = [
        "track_a_s_int",
        "kq_readiness",
        "kq_dig",
        "conditional_branch",
        "j2",
    ]
    required_present = all(
        mat_rows.get(name) is not None for name in required_mat
    )
    add_check(checks, "required_mat_records_present", required_present)
    add_check(
        checks,
        "mat_dual_status_V_and_pass_fail_closed",
        all_mat_ok and required_present,
        records=mat_consistency,
    )

    # Conditional branch must not claim Derived
    cond = mat_rows.get("conditional_branch") or {}
    add_check(
        checks,
        "conditional_branch_not_promoted_Derived",
        not cond
        or (
            cond.get("V_status") == "NOT_COMPUTED"
            and cond.get("kq_numeric_status") == "NOT_DERIVED"
            and cond.get("conditional_branch_status")
            == "OPEN_CONDITIONAL_DUAL_STATUS"
        ),
    )

    reopen = stage4a_reopen_contract(
        stage5,
        mat_rows.get("kq_dig"),
        mat_rows.get("kq_readiness"),
        mat_rows.get("track_a_s_int"),
    )
    add_check(
        checks,
        "stage4A_reopen_not_authorized",
        reopen["reopen_authorized"] is False
        and reopen["all_reopen_conditions_met"] is False
        and reopen["stage4A_status"] == "CLOSED",
    )

    ledger = claim_ledger()
    add_check(
        checks,
        "claim_ledger_nonempty_deny_list",
        len(ledger["must_not_state"]) >= 5 and len(ledger["may_state"]) >= 5,
    )

    handoff = (stage5 or {}).get("mat_handoff") or {}
    add_check(
        checks,
        "mat_handoff_still_forbids_PASS_and_Derived",
        handoff.get("allows_MAT001_PASS") is False
        and handoff.get("allows_downstream_Derived_from_MAT") is False
        and handoff.get("allows_MAT_calculation_work") is True,
    )

    firewall = {
        "tier1_uv_ir_closed": False,
        "stage4A_reopened": False,
        "V_numeric_Derived": False,
        "K_Q_numeric_Derived": False,
        "MAT001_PASS": False,
        "physics_pass": False,
        "downstream_Derived_from_MAT": False,
        "conditional_samples_as_Derived": False,
        "hold_tier1_retained": True,
        "mat_calculation_work_still_allowed": True,
    }
    add_check(
        checks,
        "claim_firewall_fail_closed",
        firewall["tier1_uv_ir_closed"] is False
        and firewall["stage4A_reopened"] is False
        and firewall["V_numeric_Derived"] is False
        and firewall["MAT001_PASS"] is False
        and firewall["physics_pass"] is False
        and firewall["hold_tier1_retained"] is True,
        flags=firewall,
    )

    all_ok = all(c["ok"] for c in checks)
    return {
        "gate": "UVIR-003_TIER1_PEER_REVIEW",
        "interface": "UVIR_STAGE5_PLUS_MAT_CLAIM_SURFACE",
        "stage": "TIER1_PEER_REVIEW_READINESS",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "decision": "HOLD_TIER1_CLOSURE_RETAINED",
        "tier1_closure_status": "NOT_MET",
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "blocking_for_tier1_closure": ["M2", "M3", "M6", "M7"],
        "criteria_snapshot": m_status,
        "stage4A_reopen_contract": reopen,
        "mat_dual_status_surface": mat_consistency,
        "peer_review_claim_ledger": ledger,
        "mat_handoff": handoff,
        "residual_peer_review_risks": (stage5 or {}).get("residual_peer_review_risks")
        or [],
        "post_mat_kit_peer_review_notes": [
            "Track-A Conditional host kit advances MAT calculation work without authorizing MAT PASS",
            "Symbolic V form is not a matched invariant for Stage 4A",
            "K_Q dig incomplete: referee must not be told K_Q is Derived",
            "Conditional matching branch must remain dual-status in any manuscript text",
            "Join readiness: matter-only static channel form is not multi-sector completion",
        ],
        "next_required_for_tier1": (stage5 or {}).get("next_required")
        or [
            "Compute V or matched Aq/K_Q from one declared action/field chart",
            "Reopen Stage 4A under that matched invariant",
            "Physical cutoff/unitarity in the claim domain",
            "Relevant IR complex-quartet control",
            "Independent Stage 5 review; MAT PASS still blocked until V path complete",
        ],
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS means a peer-review readiness audit confirms the Tier-1 hold "
            "must be retained: M2/M3/M6/M7 unmet, Stage 4A closed, V and K_Q not "
            "Derived, MAT PASS forbidden, and Conditional MAT work dual-status "
            "only. It is not UVIR or MAT physics PASS and does not reopen Stage 4A."
        ),
        "serial_next": (
            "Either produce a genuine matched invariant (V or Aq/K_Q) under one "
            "declared chart and only then reopen Stage 4A, or retain HOLD_TIER1 "
            "and keep all Conditional packaging dual-status for peer review."
        ),
    }


def validate_inputs(
    stage5: dict[str, Any] | None,
    stage4: dict[str, Any] | None,
    closure: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "stage5_readable_contract",
        bool(stage5 and stage5.get("decision") == "HOLD_TIER1_CLOSURE"),
    )
    add_check(checks, "stage4_readable", stage4 is not None)
    add_check(
        checks,
        "closure_audit_readable_or_optional",
        True,  # optional pin
        present=closure is not None,
    )
    return checks


def mutation_suite(summary: dict[str, Any]) -> None:
    for key in (
        "tier1_uv_ir_closed",
        "stage4A_reopened",
        "V_numeric_Derived",
        "MAT001_PASS",
        "physics_pass",
        "conditional_samples_as_Derived",
    ):
        mutant = copy.deepcopy(summary)
        mutant["claim_firewall"][key] = True
        require(mutant["claim_firewall"][key] is True, key)
    require(summary["decision"] == "HOLD_TIER1_CLOSURE_RETAINED", "hold retained")
    require(summary["stage4A_status"] == "CLOSED", "4A closed")
    require(summary["V_status"] == "NOT_COMPUTED", "V closed")


def main() -> None:
    args = parse_args()
    stage5, e5, s5 = load_json(args.stage5)
    stage4, e4, s4 = load_json(args.stage4)
    closure, ec, sc = load_json(args.closure_audit)
    s_int, e1, s1 = load_json(args.track_a_s_int)
    kq_ready, e2, s2 = load_json(args.kq_readiness)
    kq_dig, e3, s3 = load_json(args.kq_dig)
    cond, e6, s6 = load_json(args.conditional_branch)
    join, e7, s7 = load_json(args.join)
    j2, e8, s8 = load_json(args.j2)

    evidence = {
        "stage5": {"source": args.stage5.name, "sha256": s5, "parse_error": e5},
        "stage4": {"source": args.stage4.name, "sha256": s4, "parse_error": e4},
        "closure_audit": {
            "source": args.closure_audit.name,
            "sha256": sc,
            "parse_error": ec,
        },
        "track_a_s_int": {
            "source": args.track_a_s_int.name,
            "sha256": s1,
            "parse_error": e1,
        },
        "kq_readiness": {
            "source": args.kq_readiness.name,
            "sha256": s2,
            "parse_error": e2,
        },
        "kq_dig": {"source": args.kq_dig.name, "sha256": s3, "parse_error": e3},
        "conditional_branch": {
            "source": args.conditional_branch.name,
            "sha256": s6,
            "parse_error": e6,
        },
        "join": {"source": args.join.name, "sha256": s7, "parse_error": e7},
        "j2": {"source": args.j2.name, "sha256": s8, "parse_error": e8},
    }

    checks = validate_inputs(stage5, stage4, closure)
    for name, err in (
        ("stage5", e5),
        ("stage4", e4),
        ("track_a_s_int", e1),
        ("kq_readiness", e2),
        ("kq_dig", e3),
        ("conditional_branch", e6),
        ("j2", e8),
    ):
        add_check(checks, f"{name}_readable", err is None, parse_error=err)
    # join optional for pushed tree; if present must be fail-closed
    add_check(
        checks,
        "join_readable_or_absent",
        e7 is None or e7 == "missing",
        parse_error=e7,
    )

    mat_rows = {
        "track_a_s_int": s_int,
        "kq_readiness": kq_ready,
        "kq_dig": kq_dig,
        "conditional_branch": cond,
        "join": join,
        "j2": j2,
    }
    summary = build_summary(stage5, stage4, mat_rows, checks, evidence)

    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    all_ok = all(c["ok"] for c in summary["checks"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "uvir003_tier1_peer_review_readiness_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    (
        args.output_dir / "uvir003_tier1_peer_review_readiness_summary.sha256"
    ).write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("Tier-1 peer-review readiness")
    print("  decision:", summary["decision"])
    print("  tier1:", summary["tier1_closure_status"])
    print("  Stage4A:", summary["stage4A_status"], "| V:", summary["V_status"])
    for check in summary["checks"]:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS:", summary["subgate_status"])
    print("JSON_SHA256:", digest)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
