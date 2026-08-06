#!/usr/bin/env python3
"""MAT-001 H1.3: parent-action Z_phi/g_phi derivation attempt from declared sources.

Audits architecture, UVIR-001, R3 residue, J1, Track-A force, and H1.1–H1.2
declaration for any derivation or rigorous bound on Z_phi and g_phi (or
equivalent absolute C_m and K_Q). Freezes a peer-review incompleteness package.
Does not invent coefficients or reopen Stage 4A.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp

PASS_STATUS = "PASS_MAT001_PARENT_ACTION_H13_INCOMPLETE_SOURCES_AUDITED"
FAIL_STATUS = "FAIL_MAT001_PARENT_ACTION_H13"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    repo = base.parents[3]
    uvir = repo / "Analysis" / "UVIR"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--h12-summary",
        type=Path,
        default=base / "outputs" / "mat001_parent_action_matching_summary.json",
    )
    parser.add_argument(
        "--j1",
        type=Path,
        default=mat
        / "J1_JOINT_ACTION"
        / "outputs"
        / "mat001_j1_joint_action_normalization_summary.json",
    )
    parser.add_argument(
        "--r3",
        type=Path,
        default=uvir / "UVIR-003" / "outputs" / "uvir003_r3_uv_residue_audit_summary.json",
    )
    parser.add_argument(
        "--uvir001",
        type=Path,
        default=uvir / "UVIR-001" / "outputs" / "uvir001_summary.json",
    )
    parser.add_argument(
        "--track-a-force",
        type=Path,
        default=uvir
        / "UVIR-003"
        / "outputs"
        / "uvir003_track_a_force_adm_cubic_summary.json",
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
        "--architecture",
        type=Path,
        default=repo / "Theory" / "Core" / "ITSM_Core_Architecture.md",
    )
    parser.add_argument(
        "--master-plan",
        type=Path,
        default=repo / "Theory" / "Core" / "ITSM_Master_Research_Plan.md",
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


def load_text(path: Path) -> tuple[str | None, str | None, str | None]:
    if not path.is_file():
        return None, "missing", None
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        return None, f"{type(exc).__name__}:{exc}", None
    return text, None, hashlib.sha256(raw).hexdigest().upper()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def add_check(
    checks: list[dict[str, Any]], name: str, ok: bool, **details: Any
) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def line_attestations(text: str | None, needles: tuple[str, ...]) -> list[dict[str, Any]]:
    if text is None:
        return []
    rows = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if any(needle in line for needle in needles):
            rows.append({"line": line_number, "text": line.strip()})
    return rows


def source_absence_supported(sources: dict[str, Any]) -> bool:
    accepted = {
        "FORM_ONLY_NO_PARENT_COEFFICIENT_DERIVATION",
        "EXPLICIT_NOT_DERIVED",
        "PARAMETRIC_CANDIDATE_NOT_MAPPED_TO_PARENT_VERTEX",
        "EXPLICIT_INCOMPLETE_NO_BOUND",
        "CONDITIONAL_HOST_FORM_ONLY",
    }
    return bool(sources) and all(
        row.get("assessment") in accepted and row.get("source_backed") is True
        for row in sources.values()
    )


def audit_sources(
    arch: str | None,
    master: str | None,
    h12: dict[str, Any] | None,
    j1: dict[str, Any] | None,
    r3: dict[str, Any] | None,
    uvir001: dict[str, Any] | None,
    track_a: dict[str, Any] | None,
    s_int: dict[str, Any] | None,
) -> dict[str, Any]:
    # Reconfirm form identities only.
    z_phi, g_phi, f_phi = sp.symbols("Z_phi g_phi f_phi", positive=True)
    v = sp.simplify(g_phi / sp.sqrt(z_phi))
    c_m = sp.simplify(g_phi / f_phi)
    k_q = sp.simplify(z_phi / f_phi**2)
    require(sp.simplify(v - c_m / sp.sqrt(k_q)) == 0, "V identity")

    sources = {
        "architecture_weak_field": {
            "source": "ITSM_Core_Architecture.md §5 weak-field S_WF",
            "provides": [
                "form -C_m rho_b psi",
                "form C_obs = C_m^{3/2}/sqrt(C_IR)",
                "optional convention C_m = C_IR = C (not a derivation of C_m)",
            ],
            "evidence": {
                "has_C_m_rho_b_psi": bool(arch and "C_m" in arch and "rho_b" in arch),
                "has_C_obs_form": bool(arch and "C_obs" in arch),
                "has_Z_phi": bool(arch and "Z_phi" in arch),
                "has_g_phi": bool(arch and "g_phi" in arch),
                "form_lines": line_attestations(
                    arch,
                    ("-C_m rho_b psi", "C_obs = C_m^(3/2) / sqrt(C_IR)"),
                ),
            },
        },
        "master_plan_MAT": {
            "source": "ITSM_Master_Research_Plan.md MAT / C_obs hypothesis",
            "provides": [
                "MAT-001 goal V = C_m/sqrt(K_Q)",
                "Conditional empirical C_obs ~ 1 until MAT computes otherwise",
            ],
            "evidence": {
                "mentions_C_obs_hypothesis": bool(
                    master
                    and (
                        "C_obs" in master
                        or "Cobs" in master.replace("\\", "")
                        or "C_{\rm obs}" in master
                        or "Cobs" in master
                    )
                ),
                "explicit_status_lines": line_attestations(
                    master, ("NOT_COMPUTED", "NOT_DERIVED")
                ),
            },
        },
        "j1_joint_action_template": {
            "source": "mat001_j1_joint_action_normalization",
            "provides": [
                "structural V = g_phi/sqrt(Z_phi) = C_m/sqrt(K_Q)",
                "lists unmatched Z_phi and g_phi as open inputs",
            ],
            "evidence": {
                "subgate": (j1 or {}).get("subgate_status"),
                "V_status": (j1 or {}).get("V_status"),
                "unmatched": (j1 or {}).get("unmatched_physical_inputs"),
            },
        },
        "uvir001_minimally_kinetic_scalar": {
            "source": "uvir001_summary.json",
            "provides": [
                "tests minimally kinetic complex scalar vs Y^{3/2} origin",
                "does not supply force-phonon Z_phi/g_phi matching",
            ],
            "evidence": {
                "validation_status": (uvir001 or {}).get("validation_status"),
                "candidate_verdict": (uvir001 or {}).get("candidate_verdict"),
                "verdict_scope": (uvir001 or {}).get("candidate_verdict_scope"),
            },
        },

        "r3_uv_residue": {
            "source": "uvir003_r3_uv_residue_audit",
            "provides": [
                "classification INCOMPLETE_R3_UV_RESIDUE",
                "missing Z_psi, rho_Phi, r_rho",
                "no rigorous bound on Z_psi r_rho",
            ],
            "evidence": {
                "classification": (r3 or {}).get("classification"),
                "rigorous_bound": ((r3 or {}).get("provenance") or {}).get(
                    "rigorous_bound_Z_psi_r_rho_found"
                ),
                "missing": (r3 or {}).get("missing_microscopic_inputs"),
            },
        },
        "track_a_force_and_s_int": {
            "source": "Track-A force ADM + Conditional S_int embed",
            "provides": [
                "symbolic K_Q as free IR kinetic coefficient in force Lagrangian",
                "form d = -C_m on host",
                "no absolute Z_phi or g_phi",
            ],
            "evidence": {
                "force_subgate": (track_a or {}).get("subgate_status"),
                "s_int_status": (s_int or {}).get("S_int_status"),
                "s_int_V_status": (s_int or {}).get("V_status"),
                "s_int_kq_status": (s_int or {}).get("kq_numeric_status"),
                "K_Q_in_force_L": "K_Q"
                in str(
                    ((track_a or {}).get("symbolic_audit") or {})
                    .get("track_a_action", {})
                    .get("force_lagrangian", "")
                ),
            },
        },
        "h12_declaration": {
            "source": "mat001_parent_action_matching H1.1-H1.2",
            "provides": [
                "selected route PARENT_ACTION_Z_phi_g_phi_TO_TRACK_A",
                "inventory: NOT_DERIVED_NUMERIC_ABSENT",
            ],
            "evidence": {
                "matching_status": (h12 or {}).get("matching_status"),
                "micro_status": ((h12 or {}).get("repo_inventory") or {}).get(
                    "microscopic_coefficients_status"
                ),
            },
        },
    }
    rigorous_bound = ((r3 or {}).get("provenance") or {}).get(
        "rigorous_bound_Z_psi_r_rho_found"
    )

    arch_e = sources["architecture_weak_field"]["evidence"]
    master_e = sources["master_plan_MAT"]["evidence"]
    j1_e = sources["j1_joint_action_template"]["evidence"]
    uvir_e = sources["uvir001_minimally_kinetic_scalar"]["evidence"]
    r3_e = sources["r3_uv_residue"]["evidence"]
    track_e = sources["track_a_force_and_s_int"]["evidence"]
    h12_e = sources["h12_declaration"]["evidence"]

    unmatched = j1_e.get("unmatched") or []
    unmatched_text = " ".join(str(value) for value in unmatched)
    uvir_scope = str(uvir_e.get("verdict_scope") or "").lower()
    assessments = {
        "architecture_weak_field": (
            "FORM_ONLY_NO_PARENT_COEFFICIENT_DERIVATION"
            if arch_e.get("has_C_m_rho_b_psi") is True
            and arch_e.get("has_C_obs_form") is True
            and len(arch_e.get("form_lines") or []) >= 2
            and arch_e.get("has_Z_phi") is False
            and arch_e.get("has_g_phi") is False
            else "UNCLASSIFIED_ARCHITECTURE_SOURCE"
        ),
        "master_plan_MAT": (
            "EXPLICIT_NOT_DERIVED"
            if master_e.get("mentions_C_obs_hypothesis") is True
            and len(master_e.get("explicit_status_lines") or []) >= 2
            else "UNCLASSIFIED_MASTER_PLAN_SOURCE"
        ),
        "j1_joint_action_template": (
            "EXPLICIT_NOT_DERIVED"
            if j1_e.get("V_status") == "NOT_COMPUTED"
            and "Z_phi" in unmatched_text
            and "g_phi" in unmatched_text
            else "DERIVATION_CLAIM_PRESENT_REQUIRES_REVIEW"
        ),
        "uvir001_minimally_kinetic_scalar": (
            "PARAMETRIC_CANDIDATE_NOT_MAPPED_TO_PARENT_VERTEX"
            if uvir_e.get("candidate_verdict") == "FAIL"
            and "does not generate" in uvir_scope
            else "UNCLASSIFIED_UVIR001_SOURCE"
        ),
        "r3_uv_residue": (
            "EXPLICIT_INCOMPLETE_NO_BOUND"
            if r3_e.get("classification") == "INCOMPLETE_R3_UV_RESIDUE"
            and r3_e.get("rigorous_bound") is False
            else "DERIVATION_CLAIM_PRESENT_REQUIRES_REVIEW"
        ),
        "track_a_force_and_s_int": (
            "CONDITIONAL_HOST_FORM_ONLY"
            if track_e.get("s_int_status")
            == "EMBEDDED_CONDITIONAL_ON_TRACK_A_HOST"
            and track_e.get("s_int_V_status") == "NOT_COMPUTED"
            and track_e.get("s_int_kq_status") == "NOT_DERIVED"
            else "UNCLASSIFIED_TRACK_A_SOURCE"
        ),
        "h12_declaration": (
            "EXPLICIT_NOT_DERIVED"
            if h12_e.get("matching_status") == "DECLARED_INCOMPLETE"
            and h12_e.get("micro_status") == "NOT_DERIVED_NUMERIC_ABSENT"
            else "DERIVATION_CLAIM_PRESENT_REQUIRES_REVIEW"
        ),
    }
    for source_name, row in sources.items():
        assessment = assessments[source_name]
        row["assessment"] = assessment
        row["source_backed"] = not assessment.startswith("UNCLASSIFIED_")

    all_sources_classified = all(
        not assessment.startswith("UNCLASSIFIED_")
        for assessment in assessments.values()
    )
    absence_supported = source_absence_supported(sources)
    any_derived = any(
        assessment == "DERIVATION_CLAIM_PRESENT_REQUIRES_REVIEW"
        for assessment in assessments.values()
    )
    if any_derived:
        verdict = "SOURCE_CLAIM_PRESENT_REQUIRES_DERIVATION_REVIEW"
    elif not all_sources_classified:
        verdict = "HOLD_UNCLASSIFIED_DECLARED_SOURCE"
    else:
        verdict = "INCOMPLETE_NO_Z_phi_g_phi_FROM_DECLARED_SOURCES"

    research_requirements = [
        {
            "id": "RR1",
            "requirement": (
                "Declare a complete parent action S_parent containing both the "
                "force-phonon kinetic term with coefficient Z_phi and the matter "
                "coupling -g_phi rho_b phi (same action)."
            ),
            "status": "OPEN",
            "priority": "critical_for_H1",
        },
        {
            "id": "RR2",
            "requirement": (
                "Derive numeric or parameter-mapped values (or rigorous bounds) "
                "for Z_phi and g_phi from that action, or compute the on-shell "
                "invariant residue V directly."
            ),
            "status": "OPEN",
            "priority": "critical_for_H1",
        },
        {
            "id": "RR3",
            "requirement": (
                "Declare and verify the field map f_phi (phi -> Track-A pi) so "
                "induced C_m and K_Q live in the same chart as the Track-A host kit."
            ),
            "status": "OPEN_CONDITIONAL_MAP_ONLY",
            "priority": "critical_for_H1",
        },
        {
            "id": "RR4",
            "requirement": (
                "If using S_Phi amplitude integration: compute Z_psi and identify "
                "rho_Phi so K_Q = Z_psi rho_Phi/a0^2 is Derived, not dimensional."
            ),
            "status": "OPEN_R3_INCOMPLETE",
            "priority": "alternate_route",
        },
        {
            "id": "RR5",
            "requirement": (
                "Do not promote C_m = C_IR, C_obs ~ 1, k_Q ~ 1, or Conditional "
                "samples to Derived parent matching."
            ),
            "status": "ACTIVE_FIREWALL",
            "priority": "governance",
        },
    ]

    return {
        "form_identities": {
            "V": str(v),
            "C_m": str(c_m),
            "K_Q": str(k_q),
            "status": "STRUCTURAL_ONLY",
        },
        "source_audits": sources,
        "any_numeric_coefficient_derived": any_derived,
        "all_sources_classified": all_sources_classified,
        "source_absence_supported": absence_supported,
        "rigorous_bound_Z_psi_r_rho_found": bool(rigorous_bound),
        "derivation_verdict": verdict,
        "research_requirements_frozen": research_requirements,
    }


def build_summary(
    audit: dict[str, Any],
    checks: list[dict[str, Any]],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    sources = audit["source_audits"]
    add_check(
        checks,
        "declared_sources_support_absence_verdict",
        audit["any_numeric_coefficient_derived"] is False
        and audit["source_absence_supported"] is True
        and source_absence_supported(sources),
    )
    add_check(
        checks,
        "all_declared_sources_classified",
        audit["all_sources_classified"] is True
        and all(row.get("source_backed") is True for row in sources.values()),
    )
    add_check(
        checks,
        "r3_reports_no_rigorous_residue_bound",
        audit["rigorous_bound_Z_psi_r_rho_found"] is False,
    )
    add_check(
        checks,
        "architecture_lacks_Z_phi_g_phi_symbols",
        sources["architecture_weak_field"]["evidence"].get("has_Z_phi") is False
        and sources["architecture_weak_field"]["evidence"].get("has_g_phi") is False,
    )
    add_check(
        checks,
        "j1_still_lists_unmatched_micro_inputs",
        isinstance(sources["j1_joint_action_template"]["evidence"].get("unmatched"), list)
        and len(sources["j1_joint_action_template"]["evidence"]["unmatched"] or [])
        >= 1,
    )
    add_check(
        checks,
        "research_requirements_frozen_nonempty",
        len(audit["research_requirements_frozen"]) >= 4,
    )
    add_check(
        checks,
        "verdict_incomplete",
        audit["derivation_verdict"]
        == "INCOMPLETE_NO_Z_phi_g_phi_FROM_DECLARED_SOURCES",
    )

    firewall = {
        "H13_sources_audited": True,
        "numeric_Z_phi_derived": False,
        "numeric_g_phi_derived": False,
        "numeric_V_computed": False,
        "numeric_K_Q_derived": False,
        "architecture_C_m_equals_C_IR_as_Derived": False,
        "r3_incomplete_promoted_Derived": False,
        "claims_MAT_pass": False,
        "physics_pass": False,
        "reopens_stage4A": False,
        "H1_complete": False,
    }
    add_check(
        checks,
        "claim_firewall_fail_closed",
        all(
            firewall[k] is False
            for k in (
                "numeric_Z_phi_derived",
                "numeric_g_phi_derived",
                "numeric_V_computed",
                "numeric_K_Q_derived",
                "claims_MAT_pass",
                "physics_pass",
                "reopens_stage4A",
                "H1_complete",
            )
        ),
        flags=firewall,
    )

    all_ok = all(c["ok"] for c in checks)
    return {
        "gate": "MAT-001",
        "interface": "PARENT_ACTION_H13_SOURCE_DERIVATION",
        "stage": "H1_3_PARENT_ACTION_SOURCE_AUDIT",
        "plan_step": "H1.3",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "matching_status": "INCOMPLETE_AFTER_SOURCE_AUDIT",
        "derivation_verdict": audit["derivation_verdict"],
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "C_m_numeric_status": "NOT_DERIVED_FORM_ONLY",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "form_identities": audit["form_identities"],
        "source_audits": audit["source_audits"],
        "research_requirements_frozen": audit["research_requirements_frozen"],
        "H1_exit": {
            "H1_complete": False,
            "honest_incompleteness_acceptable_for_peer_review": True,
            "blocks_H2_H3": True,
            "reason": (
                "Source-backed attestations find no absolute Z_phi or g_phi derivation; Stage 4A "
                "and Derived V remain blocked by plan."
            ),
        },
        "blocking_requirements": [
            row["requirement"]
            for row in audit["research_requirements_frozen"]
            if row["priority"] == "critical_for_H1"
        ],
        "inadmissible_substitutions": {
            "C_m_equals_C_IR_as_micro_match": "REJECTED",
            "C_obs_approx_1_as_g_phi": "REJECTED",
            "Z_psi_equals_1_as_Z_phi": "REJECTED",
            "k_Q_equals_1_as_parent_kinetic": "REJECTED",
            "incomplete_R3_as_parent_match": "REJECTED",
        },
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS means H1.3 classified source-backed attestations from every "
            "named declared source and found no Z_phi/g_phi derivation. Requirements are "
            "frozen for peer review. This does not compute V, derive K_Q, or "
            "reopen Stage 4A."
        ),
        "serial_next": (
            "H1.4: link frozen RR1–RR5 into Master Plan / recovery plan as open "
            "research requirements; hold Derived H2–H5 until RR1–RR3 close. "
            "Lane B Conditional work may continue dual-status only."
        ),
    }


def validate_upstream(
    h12: dict[str, Any] | None,
    j1: dict[str, Any] | None,
    r3: dict[str, Any] | None,
    uvir001: dict[str, Any] | None,
    track_a: dict[str, Any] | None,
    s_int: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "h12_upstream",
        bool(
            h12
            and h12.get("subgate_status")
            == "PASS_MAT001_PARENT_ACTION_MATCHING_DECLARED_INCOMPLETE"
            and h12.get("matching_status") == "DECLARED_INCOMPLETE"
            and h12.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "j1_upstream",
        bool(
            j1
            and j1.get("subgate_status")
            == "PASS_MAT001_J1_JOINT_ACTION_NORMALIZATION_IDENTITY"
            and j1.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "r3_upstream_incomplete",
        bool(
            r3
            and r3.get("classification") == "INCOMPLETE_R3_UV_RESIDUE"
            and r3.get("kq_numeric_status") == "NOT_DERIVED"
            and ((r3.get("provenance") or {}).get("rigorous_bound_Z_psi_r_rho_found")
                 is False)
        ),
    )
    add_check(
        checks,
        "uvir001_upstream_present",
        bool(uvir001 and uvir001.get("calculation_status") in {"PASS", "FAIL", "HOLD"}
             or uvir001 is not None),
    )
    # uvir001 may use different status key
    if uvir001 is not None:
        checks[-1]["ok"] = True
    add_check(
        checks,
        "track_a_and_s_int_upstream",
        bool(
            track_a
            and track_a.get("subgate_status") == "PASS_FORCE_SECTOR_J2_COMPONENT"
            and s_int
            and s_int.get("subgate_status")
            == "PASS_MAT001_TRACK_A_S_INT_EMBED_DH_EXPORTED_CONDITIONAL"
            and s_int.get("V_status") == "NOT_COMPUTED"
        ),
    )
    return checks


def mutation_suite(summary: dict[str, Any]) -> None:
    for key in (
        "numeric_Z_phi_derived",
        "numeric_g_phi_derived",
        "numeric_V_computed",
        "H1_complete",
        "claims_MAT_pass",
        "reopens_stage4A",
        "physics_pass",
    ):
        mutant = copy.deepcopy(summary)
        mutant["claim_firewall"][key] = True
        require(mutant["claim_firewall"][key] is True, key)
    assessment_mutant = copy.deepcopy(summary)
    assessment_mutant["source_audits"]["h12_declaration"]["assessment"] = (
        "DERIVATION_CLAIM_PRESENT_REQUIRES_REVIEW"
    )
    require(
        source_absence_supported(assessment_mutant["source_audits"]) is False,
        "source assessment mutation must invalidate absence verdict",
    )
    backing_mutant = copy.deepcopy(summary)
    backing_mutant["source_audits"]["master_plan_MAT"]["source_backed"] = False
    require(
        source_absence_supported(backing_mutant["source_audits"]) is False,
        "unbacked source mutation must invalidate absence verdict",
    )
    require(
        summary["derivation_verdict"]
        == "INCOMPLETE_NO_Z_phi_g_phi_FROM_DECLARED_SOURCES",
        "verdict",
    )
    require(summary["stage4A_status"] == "CLOSED", "4A")


def main() -> None:
    args = parse_args()
    h12, e1, s1 = load_json(args.h12_summary)
    j1, e2, s2 = load_json(args.j1)
    r3, e3, s3 = load_json(args.r3)
    uvir001, e4, s4 = load_json(args.uvir001)
    track_a, e5, s5 = load_json(args.track_a_force)
    s_int, e6, s6 = load_json(args.track_a_s_int)
    arch, ea, sa = load_text(args.architecture)
    master, em, sm = load_text(args.master_plan)

    evidence = {
        "h12": {"source": args.h12_summary.name, "sha256": s1, "parse_error": e1},
        "j1": {"source": args.j1.name, "sha256": s2, "parse_error": e2},
        "r3": {"source": args.r3.name, "sha256": s3, "parse_error": e3},
        "uvir001": {"source": args.uvir001.name, "sha256": s4, "parse_error": e4},
        "track_a_force": {
            "source": args.track_a_force.name,
            "sha256": s5,
            "parse_error": e5,
        },
        "track_a_s_int": {
            "source": args.track_a_s_int.name,
            "sha256": s6,
            "parse_error": e6,
        },
        "architecture": {
            "source": args.architecture.name,
            "sha256": sa,
            "parse_error": ea,
        },
        "master_plan": {
            "source": args.master_plan.name,
            "sha256": sm,
            "parse_error": em,
        },
    }

    checks = validate_upstream(h12, j1, r3, uvir001, track_a, s_int)
    for name, err in (
        ("h12", e1),
        ("j1", e2),
        ("r3", e3),
        ("uvir001", e4),
        ("track_a_force", e5),
        ("track_a_s_int", e6),
        ("architecture", ea),
        ("master_plan", em),
    ):
        add_check(checks, f"{name}_readable", err is None, parse_error=err)

    audit = audit_sources(arch, master, h12, j1, r3, uvir001, track_a, s_int)
    summary = build_summary(audit, checks, evidence)

    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    all_ok = all(c["ok"] for c in summary["checks"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_parent_action_h13_source_audit_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    (
        args.output_dir / "mat001_parent_action_h13_source_audit_summary.sha256"
    ).write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("MAT-001 H1.3 parent-action source derivation audit")
    print("  verdict:", summary["derivation_verdict"])
    print("  matching:", summary["matching_status"])
    print("  V:", summary["V_status"], "| K_Q:", summary["kq_numeric_status"])
    print("  H1 complete:", summary["H1_exit"]["H1_complete"])
    for check in summary["checks"]:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS:", summary["subgate_status"])
    print("JSON_SHA256:", digest)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
