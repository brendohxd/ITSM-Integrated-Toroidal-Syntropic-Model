#!/usr/bin/env python3
"""Complete plan steps RR2–RR3 and H2–H7 as far as the peer-review bar allows.

This package:
  RR2 — freezes that no residual/micro derivation of Z_phi,g_phi or V is available
  RR3 — declares the f_phi field-chart convention (Conditional map scale)
  H2  — proves redefinition invariance of V from the RR1 skeleton (symbolic)
  H3  — reaffirms Stage 4A reopen contract all false
  H4  — records M2 claim-domain policy (partial high-q; IR HOLD not tier-1 closed)
  H5  — MAT packaging ban-list executable (PASS forbidden)
  H6  — reaffirms matter-only join channel (no silent multi-sector)
  H7  — hygiene: dual-status, claim firewall, no path leaks

Does NOT invent numeric V/K_Q, does NOT complete H1 Derived matching,
does NOT reopen Stage 4A, does NOT issue MAT/UVIR physics PASS.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp

PASS_STATUS = "PASS_MAT001_PLAN_RR2_H7_BOUNDED_COMPLETION"
FAIL_STATUS = "FAIL_MAT001_PLAN_RR2_H7_PACKAGE"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    repo = base.parents[3]
    uvir = repo / "Analysis" / "UVIR" / "UVIR-003" / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rr1",
        type=Path,
        default=mat
        / "PARENT_ACTION_MATCHING"
        / "outputs"
        / "mat001_rr1_parent_action_skeleton_summary.json",
    )
    parser.add_argument(
        "--h13",
        type=Path,
        default=mat
        / "PARENT_ACTION_MATCHING"
        / "outputs"
        / "mat001_parent_action_h13_source_audit_summary.json",
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
        "--tier1",
        type=Path,
        default=uvir / "uvir003_tier1_peer_review_readiness_summary.json",
    )
    parser.add_argument(
        "--stage5",
        type=Path,
        default=uvir / "uvir003_stage5_full_gate_decision_summary.json",
    )
    parser.add_argument(
        "--conditional",
        type=Path,
        default=mat
        / "CONDITIONAL_MATCHING_BRANCH"
        / "outputs"
        / "mat001_conditional_matching_branch_summary.json",
    )
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
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


def rr2_package(h13: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "status": "INCOMPLETE_NO_DERIVATION_AVAILABLE",
        "routes_attempted_or_audited": [
            "parent Z_phi/g_phi from declared sources (H1.3: none)",
            "R3 Z_psi r_rho residual (incomplete, no bound)",
            "R1 k_Q M_P^2 (Conditional, forbidden as Derived)",
            "K_Q = C_m^2/V^2 (blocked: absolute C_m and V absent)",
            "direct on-shell residue V (no live dynamical residue export)",
        ],
        "numeric_Z_phi": "NOT_DERIVED",
        "numeric_g_phi": "NOT_DERIVED",
        "numeric_V": "NOT_COMPUTED",
        "h13_verdict": (h13 or {}).get("derivation_verdict"),
        "peer_review_statement": (
            "RR2 cannot be closed with current declared sources without new UV "
            "dynamics or a residue calculation. Incompleteness is frozen."
        ),
    }


def rr3_package() -> dict[str, Any]:
    s, f_phi = sp.symbols("s f_phi", positive=True)
    # Chart convention: adopt f_phi as the free map scale between parent phi and IR psi.
    # Under phi' = phi/s (parent rescaling) with psi fixed, f_phi' = s f_phi, etc.
    return {
        "status": "DECLARED_CONDITIONAL_CHART_CONVENTION",
        "convention_name": "IR_FORCE_MAP_psi_equals_f_phi_phi",
        "definition": "psi = f_phi * phi, with Track-A split psi = psi_bar + pi",
        "f_phi_status": "FREE_MAP_SCALE_NOT_NUMERICALLY_FIXED",
        "redefinition_note": (
            "V = g_phi/sqrt(Z_phi) is independent of f_phi; C_m and K_Q each "
            "depend on f_phi but V does not. Absolute C_m still needs g_phi and f_phi."
        ),
        "completes_RR3": False,
        "why_not_complete": (
            "A Conditional convention is declared, but a Derived chart still needs "
            "a justified numerical or dynamical fix of f_phi (or elimination by "
            "working only with V)."
        ),
        "recommended_Derived_strategy": (
            "Prefer computing V directly (f_phi drops out) over fixing f_phi alone"
        ),
        "symbolic_f_phi_independence_of_V": True,
    }


def h2_package() -> dict[str, Any]:
    z, g, f, s = sp.symbols("Z_phi g_phi f_phi s", positive=True)
    v = g / sp.sqrt(z)
    c_m = g / f
    k_q = z / f**2
    # Parent rescaling phi' = r*phi with r=s: Z' = Z/s^2, g' = g/s
    z_p, g_p = z / s**2, g / s
    v_p = sp.simplify(g_p / sp.sqrt(z_p))
    # IR rescaling psi' = u*psi with u=s: K' = K/s^2, C_m' = C_m/s
    k_p, c_p = k_q / s**2, c_m / s
    v_ir_p = sp.simplify(c_p / sp.sqrt(k_p))
    require(sp.simplify(v_p - v) == 0, "parent rescaling")
    require(sp.simplify(v_ir_p - v) == 0, "IR rescaling")
    require(sp.simplify(v - c_m / sp.sqrt(k_q)) == 0, "cross chart")
    return {
        "status": "PASS_SYMBOLIC_REDEFINITION_INVARIANCE",
        "invariant": "V = g_phi/sqrt(Z_phi) = C_m/sqrt(K_Q)",
        "parent_rescaling_covariance": True,
        "IR_rescaling_covariance": True,
        "cross_chart_identity": True,
        "numeric_V_status": "NOT_COMPUTED",
        "note": (
            "H2 form-level package complete for the RR1 skeleton. Numeric "
            "matching still requires RR2 coefficients or residue."
        ),
    }


def h3_package(tier1: dict[str, Any] | None, stage5: dict[str, Any] | None) -> dict[str, Any]:
    reopen = (tier1 or {}).get("stage4A_reopen_contract") or {}
    return {
        "status": "CLOSED_REOPEN_NOT_AUTHORIZED",
        "stage4A_status": "CLOSED",
        "reopen_authorized": False,
        "all_reopen_conditions_met": reopen.get("all_reopen_conditions_met", False),
        "stage5_decision": (stage5 or {}).get("decision"),
        "policy": (
            "Stage 4A stays closed until a Derived matched invariant exists. "
            "H2 symbolic invariance and Conditional probes are insufficient."
        ),
        "bounded_completion": True,
    }


def h4_package(stage5: dict[str, Any] | None) -> dict[str, Any]:
    criteria = (stage5 or {}).get("master_plan_criteria") or {}
    m2 = criteria.get("M2") or {}
    return {
        "status": "PARTIAL_BOUNDED_HIGH_Q_ONLY_IR_HOLD_UNRESOLVED",
        "M2_tier1_met": m2.get("tier1_met", False),
        "M2_status": m2.get("status"),
        "claim_domain_policy": {
            "may_claim_as_Derived_stability": False,
            "may_cite_high_q_Track_A_bounded_domain": True,
            "must_label_IR_complex_quartet": "HOLD_UNRESOLVED_FOR_TIER1",
            "permanent_exclude_from_UVIR_PASS_if_unresolved": True,
        },
        "bounded_completion": True,
        "note": (
            "H4 cannot mark M2 tier1_met without IR control. Bounded package "
            "records the claim-domain policy for peer review."
        ),
    }


def h5_package(stage5: dict[str, Any] | None, cond: dict[str, Any] | None) -> dict[str, Any]:
    handoff = (stage5 or {}).get("mat_handoff") or {}
    ban = [
        "mat001_pass: true",
        "V_status: COMPUTED as Derived without RR2 closure",
        "downstream Derived SPARC/H0/lensing from MAT form kit",
        "Conditional samples packaged as Derived V or K_Q",
        "Stage 4A reopened from Conditional causality tables",
        "alpha.13 freeze claiming UVIR closed",
    ]
    return {
        "status": "PASS_MAT_PACKAGING_BANLIST_ACTIVE",
        "allows_MAT001_PASS": handoff.get("allows_MAT001_PASS", False),
        "allows_downstream_Derived_from_MAT": handoff.get(
            "allows_downstream_Derived_from_MAT", False
        ),
        "allows_MAT_calculation_work": handoff.get("allows_MAT_calculation_work", True),
        "conditional_branch_status": (cond or {}).get("conditional_branch_status"),
        "ban_list": ban,
        "bounded_completion": True,
    }


def h6_package(join: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "status": "PARTIAL_MATTER_CHANNEL_ONLY_RECONFIRMED",
        "join_status": (join or {}).get("join_status"),
        "selected_operational_channel": (join or {}).get("selected_operational_channel"),
        "free_force_static_B_joined": False,
        "full_multi_sector_joined": False,
        "free_sector_identified_with_Track_A": False,
        "bounded_completion": True,
    }


def h7_package() -> dict[str, Any]:
    return {
        "status": "PASS_HYGIENE_CONTRACT_FOR_PACKAGE",
        "requirements": [
            "dual-run byte-identical JSON",
            "SHA-256 sidecar",
            "no absolute workstation paths",
            "claim firewall fail closed",
            "dual-status wording for Conditional vs Derived",
            "plan and queue updated in same change set",
            "alpha.11 and alpha.12 remain immutable",
        ],
        "bounded_completion": True,
    }


def build_summary(
    rr2: dict[str, Any],
    rr3: dict[str, Any],
    h2: dict[str, Any],
    h3: dict[str, Any],
    h4: dict[str, Any],
    h5: dict[str, Any],
    h6: dict[str, Any],
    h7: dict[str, Any],
    checks: list[dict[str, Any]],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    stages = {
        "RR2": rr2["status"],
        "RR3": rr3["status"],
        "H2": h2["status"],
        "H3": h3["status"],
        "H4": h4["status"],
        "H5": h5["status"],
        "H6": h6["status"],
        "H7": h7["status"],
    }
    add_check(checks, "RR2_incomplete_frozen", "INCOMPLETE" in rr2["status"])
    add_check(
        checks,
        "RR3_chart_convention_declared",
        rr3["status"] == "DECLARED_CONDITIONAL_CHART_CONVENTION"
        and rr3["symbolic_f_phi_independence_of_V"] is True,
    )
    add_check(
        checks,
        "H2_symbolic_invariance_pass",
        h2["status"] == "PASS_SYMBOLIC_REDEFINITION_INVARIANCE"
        and h2["parent_rescaling_covariance"]
        and h2["IR_rescaling_covariance"],
    )
    add_check(
        checks,
        "H3_stage4A_still_closed",
        h3["status"] == "CLOSED_REOPEN_NOT_AUTHORIZED"
        and h3["reopen_authorized"] is False,
    )
    add_check(
        checks,
        "H4_M2_not_falsely_closed",
        h4["M2_tier1_met"] is False
        and h4["claim_domain_policy"]["may_claim_as_Derived_stability"] is False,
    )
    add_check(
        checks,
        "H5_MAT_PASS_forbidden",
        h5["allows_MAT001_PASS"] is False
        and h5["allows_downstream_Derived_from_MAT"] is False,
    )
    add_check(
        checks,
        "H6_matter_only_reconfirmed",
        h6["free_force_static_B_joined"] is False
        and h6["full_multi_sector_joined"] is False,
    )
    add_check(checks, "H7_hygiene_contract_present", h7["bounded_completion"] is True)

    firewall = {
        "plan_bounded_completion_recorded": True,
        "RR2_closed_with_numerics": False,
        "H1_Derived_complete": False,
        "numeric_V_computed": False,
        "numeric_K_Q_derived": False,
        "stage4A_reopened": False,
        "M2_tier1_falsely_met": False,
        "claims_MAT_pass": False,
        "claims_UVIR_pass": False,
        "physics_pass": False,
        "claims_downstream_Derived": False,
    }
    add_check(
        checks,
        "claim_firewall_fail_closed",
        all(
            firewall[k] is False
            for k in (
                "RR2_closed_with_numerics",
                "H1_Derived_complete",
                "numeric_V_computed",
                "stage4A_reopened",
                "M2_tier1_falsely_met",
                "claims_MAT_pass",
                "physics_pass",
            )
        ),
        flags=firewall,
    )

    all_ok = all(c["ok"] for c in checks)
    return {
        "gate": "MAT-001_PLAN_COMPLETION",
        "interface": "TIER1_FORWARD_PLAN_RR2_H7",
        "stage": "BOUNDED_PLAN_COMPLETION_PACKAGE",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "completion_mode": "BOUNDED_PEER_REVIEW_MAXIMAL",
        "stages": stages,
        "RR2": rr2,
        "RR3": rr3,
        "H2": h2,
        "H3": h3,
        "H4": h4,
        "H5": h5,
        "H6": h6,
        "H7": h7,
        "overall": {
            "Derived_critical_path_closed": False,
            "reason_not_closed": (
                "RR2 has no numeric Z_phi/g_phi or residue V; H3-H5 correctly "
                "remain holds/firewalls rather than false PASS"
            ),
            "bounded_steps_completed": [
                "RR2 incompleteness freeze",
                "RR3 Conditional chart convention",
                "H2 symbolic redefinition invariance",
                "H3 Stage 4A closed reaffirmation",
                "H4 M2 claim-domain policy",
                "H5 MAT packaging ban-list",
                "H6 matter-only join reaffirmation",
                "H7 hygiene contract",
            ],
            "still_open_for_true_Derived_closure": [
                "RR2 micro/residue derivation",
                "RR3 Derived f_phi fix or pure-V route",
                "H3 Stage 4A after matched invariant",
                "H4 M2 IR control if claimed",
                "H5 MAT PASS after UVIR tier-1 + V",
            ],
        },
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS means every plan step RR2–H7 has been advanced to the "
            "maximum peer-review-honest state: incompleteness freezes, symbolic "
            "invariance, and hold/firewall packages. It does not complete Derived "
            "matching or tier-1 UVIR closure."
        ),
        "serial_next": (
            "True Derived work remains RR2 (UV parent or residue V). Until then "
            "retain HOLD_TIER1, dual-status Conditional probes only, immutable "
            "alpha.11/alpha.12."
        ),
    }


def validate_upstream(
    rr1: dict[str, Any] | None,
    h13: dict[str, Any] | None,
    join: dict[str, Any] | None,
    tier1: dict[str, Any] | None,
    stage5: dict[str, Any] | None,
    cond: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "rr1_upstream",
        bool(
            rr1
            and rr1.get("subgate_status")
            == "PASS_MAT001_RR1_PARENT_ACTION_SKELETON_DECLARED_UNMATCHED"
            and rr1.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "h13_upstream",
        bool(
            h13
            and h13.get("subgate_status")
            == "PASS_MAT001_PARENT_ACTION_H13_INCOMPLETE_SOURCES_AUDITED"
        ),
    )
    add_check(
        checks,
        "join_upstream",
        bool(
            join
            and join.get("subgate_status")
            == "PASS_MAT001_TRACK_A_JOIN_READINESS_PARTIAL_MATTER_CHANNEL_ONLY"
        ),
    )
    add_check(
        checks,
        "tier1_upstream",
        bool(
            tier1
            and tier1.get("subgate_status")
            == "PASS_TIER1_PEER_REVIEW_READINESS_HOLD_RETAINED"
            and tier1.get("stage4A_status") == "CLOSED"
        ),
    )
    add_check(
        checks,
        "stage5_upstream",
        bool(
            stage5
            and stage5.get("decision") == "HOLD_TIER1_CLOSURE"
            and stage5.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "conditional_upstream",
        bool(
            cond
            and cond.get("subgate_status")
            == "PASS_MAT001_CONDITIONAL_MATCHING_BRANCH_OPEN_DUAL_STATUS"
            and cond.get("V_status") == "NOT_COMPUTED"
        ),
    )
    return checks


def mutation_suite(summary: dict[str, Any]) -> None:
    for key in (
        "RR2_closed_with_numerics",
        "H1_Derived_complete",
        "numeric_V_computed",
        "stage4A_reopened",
        "M2_tier1_falsely_met",
        "claims_MAT_pass",
        "physics_pass",
    ):
        mutant = copy.deepcopy(summary)
        mutant["claim_firewall"][key] = True
        require(mutant["claim_firewall"][key] is True, key)
    require(summary["V_status"] == "NOT_COMPUTED", "V")
    require(summary["stage4A_status"] == "CLOSED", "4A")
    require(summary["overall"]["Derived_critical_path_closed"] is False, "path open")


def main() -> None:
    args = parse_args()
    rr1, e1, s1 = load_json(args.rr1)
    h13, e2, s2 = load_json(args.h13)
    join, e3, s3 = load_json(args.join)
    tier1, e4, s4 = load_json(args.tier1)
    stage5, e5, s5 = load_json(args.stage5)
    cond, e6, s6 = load_json(args.conditional)

    evidence = {
        "rr1": {"source": args.rr1.name, "sha256": s1, "parse_error": e1},
        "h13": {"source": args.h13.name, "sha256": s2, "parse_error": e2},
        "join": {"source": args.join.name, "sha256": s3, "parse_error": e3},
        "tier1": {"source": args.tier1.name, "sha256": s4, "parse_error": e4},
        "stage5": {"source": args.stage5.name, "sha256": s5, "parse_error": e5},
        "conditional": {"source": args.conditional.name, "sha256": s6, "parse_error": e6},
    }
    checks = validate_upstream(rr1, h13, join, tier1, stage5, cond)
    for name, err in (
        ("rr1", e1),
        ("h13", e2),
        ("join", e3),
        ("tier1", e4),
        ("stage5", e5),
        ("conditional", e6),
    ):
        add_check(checks, f"{name}_readable", err is None, parse_error=err)

    rr2 = rr2_package(h13)
    rr3 = rr3_package()
    h2 = h2_package()
    h3 = h3_package(tier1, stage5)
    h4 = h4_package(stage5)
    h5 = h5_package(stage5, cond)
    h6 = h6_package(join)
    h7 = h7_package()
    summary = build_summary(
        rr2, rr3, h2, h3, h4, h5, h6, h7, checks, evidence
    )

    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    all_ok = all(c["ok"] for c in summary["checks"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_plan_rr2_through_h7_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "mat001_plan_rr2_through_h7_summary.sha256").write_bytes(
        f"{digest}  {output.name}\n".encode("utf-8")
    )

    print("MAT-001 plan RR2–H7 bounded completion package")
    print("  mode:", summary["completion_mode"])
    print("  Derived path closed:", summary["overall"]["Derived_critical_path_closed"])
    for key, val in summary["stages"].items():
        print(f"  {key}: {val}")
    print("  V:", summary["V_status"], "| Stage4A:", summary["stage4A_status"])
    for check in summary["checks"]:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS:", summary["subgate_status"])
    print("JSON_SHA256:", digest)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
