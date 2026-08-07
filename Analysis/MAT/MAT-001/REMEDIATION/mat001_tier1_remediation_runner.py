#!/usr/bin/env python3
"""Regenerate and verify the fail-closed MAT-001 Tier-1 R1-R5 evidence cone."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import NamedTuple


class Step(NamedTuple):
    script: str
    output: str
    mutations: bool = False


STEPS = (
    Step(
        "Analysis/MAT/MAT-001/COVARIANT_MATTER_ACTION/mat001_r3_covariant_matter_action.py",
        "Analysis/MAT/MAT-001/COVARIANT_MATTER_ACTION/outputs/mat001_r3_covariant_matter_action_summary.json",
        True,
    ),
    Step(
        "Analysis/MAT/MAT-001/J1_JOINT_ACTION/mat001_j1_joint_action_normalization.py",
        "Analysis/MAT/MAT-001/J1_JOINT_ACTION/outputs/mat001_j1_joint_action_normalization_summary.json",
    ),
    Step(
        "Analysis/MAT/MAT-001/R2_DIRECT_RESIDUE/mat001_r2_direct_residue_audit.py",
        "Analysis/MAT/MAT-001/R2_DIRECT_RESIDUE/outputs/mat001_r2_direct_residue_audit_summary.json",
    ),
    Step(
        "Analysis/MAT/MAT-001/UNIT_CHART/mat001_unit_chart_contract.py",
        "Analysis/MAT/MAT-001/UNIT_CHART/outputs/mat001_unit_chart_contract_summary.json",
    ),
    Step(
        "Analysis/MAT/MAT-001/HANDOFF/mat001_uvir_handoff_contract_audit.py",
        "Analysis/MAT/MAT-001/HANDOFF/outputs/mat001_uvir_handoff_contract_summary.json",
    ),
    Step(
        "Analysis/MAT/MAT-001/J2_MODE_PROJECTION/mat001_j2_basis_covariant_mode_projection.py",
        "Analysis/MAT/MAT-001/J2_MODE_PROJECTION/outputs/mat001_j2_basis_covariant_mode_projection_summary.json",
    ),
    Step(
        "Analysis/MAT/MAT-001/LIVE_EXPORT_INVENTORY/mat001_live_uvir_export_inventory.py",
        "Analysis/MAT/MAT-001/LIVE_EXPORT_INVENTORY/outputs/mat001_live_uvir_export_inventory_summary.json",
    ),
    Step(
        "Analysis/MAT/MAT-001/SAME_CHART_EXPORT/mat001_same_chart_quadratic_export.py",
        "Analysis/MAT/MAT-001/SAME_CHART_EXPORT/outputs/mat001_same_chart_quadratic_export_summary.json",
        True,
    ),
    Step(
        "Analysis/MAT/MAT-001/S_INT_DH_EXPORT/mat001_s_int_dh_export_audit.py",
        "Analysis/MAT/MAT-001/S_INT_DH_EXPORT/outputs/mat001_s_int_dh_export_summary.json",
        True,
    ),
    Step(
        "Analysis/MAT/MAT-001/FORCE_HOSTING/mat001_force_hosting_readiness_audit.py",
        "Analysis/MAT/MAT-001/FORCE_HOSTING/outputs/mat001_force_hosting_readiness_summary.json",
        True,
    ),
    Step(
        "Analysis/MAT/MAT-001/TRACK_A_S_INT/mat001_track_a_s_int_embed_audit.py",
        "Analysis/MAT/MAT-001/TRACK_A_S_INT/outputs/mat001_track_a_s_int_embed_summary.json",
        True,
    ),
    Step(
        "Analysis/MAT/MAT-001/TRACK_A_KQ/mat001_track_a_kq_readiness_audit.py",
        "Analysis/MAT/MAT-001/TRACK_A_KQ/outputs/mat001_track_a_kq_readiness_summary.json",
        True,
    ),
    Step(
        "Analysis/MAT/MAT-001/KQ_DERIVATION_DIG/mat001_kq_derivation_dig_audit.py",
        "Analysis/MAT/MAT-001/KQ_DERIVATION_DIG/outputs/mat001_kq_derivation_dig_summary.json",
        True,
    ),
    Step(
        "Analysis/MAT/MAT-001/CONDITIONAL_MATCHING_BRANCH/mat001_conditional_matching_branch.py",
        "Analysis/MAT/MAT-001/CONDITIONAL_MATCHING_BRANCH/outputs/mat001_conditional_matching_branch_summary.json",
        True,
    ),
    Step(
        "Analysis/MAT/MAT-001/TRACK_A_JOIN/mat001_track_a_join_readiness_audit.py",
        "Analysis/MAT/MAT-001/TRACK_A_JOIN/outputs/mat001_track_a_join_readiness_summary.json",
        True,
    ),
    Step(
        "Analysis/UVIR/UVIR-003/uvir003_tier1_peer_review_readiness.py",
        "Analysis/UVIR/UVIR-003/outputs/uvir003_tier1_peer_review_readiness_summary.json",
        True,
    ),
    Step(
        "Analysis/MAT/MAT-001/PARENT_ACTION_MATCHING/mat001_parent_action_matching_attempt.py",
        "Analysis/MAT/MAT-001/PARENT_ACTION_MATCHING/outputs/mat001_parent_action_matching_summary.json",
        True,
    ),
    Step(
        "Analysis/MAT/MAT-001/PARENT_ACTION_MATCHING/mat001_parent_action_h13_source_derivation_audit.py",
        "Analysis/MAT/MAT-001/PARENT_ACTION_MATCHING/outputs/mat001_parent_action_h13_source_audit_summary.json",
        True,
    ),
    Step(
        "Analysis/MAT/MAT-001/PARENT_ACTION_MATCHING/mat001_rr1_parent_action_skeleton_declaration.py",
        "Analysis/MAT/MAT-001/PARENT_ACTION_MATCHING/outputs/mat001_rr1_parent_action_skeleton_summary.json",
        True,
    ),
    Step(
        "Analysis/MAT/MAT-001/PARENT_ACTION_MATCHING/mat001_rr2_residue_pathway_attempt.py",
        "Analysis/MAT/MAT-001/PARENT_ACTION_MATCHING/outputs/mat001_rr2_residue_pathway_summary.json",
        True,
    ),
    Step(
        "Analysis/MAT/MAT-001/R5_IDENTIFIABILITY/mat001_r5_microscopic_matching_decision.py",
        "Analysis/MAT/MAT-001/R5_IDENTIFIABILITY/outputs/mat001_r5_microscopic_matching_decision_summary.json",
        True,
    ),
    Step(
        "Analysis/MAT/MAT-001/PLAN_COMPLETION/mat001_plan_rr2_through_h7_package.py",
        "Analysis/MAT/MAT-001/PLAN_COMPLETION/outputs/mat001_plan_rr2_through_h7_summary.json",
        True,
    ),
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def run(repo: Path, step: Step, *extra: str) -> None:
    env = os.environ.copy()
    env["PYTHONHASHSEED"] = "1"
    command = [sys.executable, "-B", str(repo / step.script), *extra]
    for attempt in (1, 2):
        completed = subprocess.run(
            command, cwd=repo, env=env, text=True, capture_output=True, check=False
        )
        if completed.stdout:
            print(completed.stdout, end="")
        if completed.returncode == 0:
            return
        transient = (
            "OSError: [Errno 22]" in completed.stderr
            or "WinError 32" in completed.stderr
        )
        if not transient or attempt == 2:
            if completed.stderr:
                print(completed.stderr, file=sys.stderr, end="")
            raise SystemExit(f"FAIL: {step.script} exited {completed.returncode}")
        print(f"RETRY_ONEDRIVE_TRANSIENT: {step.script}", file=sys.stderr)


def verify(repo: Path, step: Step) -> str:
    output = repo / step.output
    if not output.is_file():
        raise SystemExit(f"FAIL: missing output {step.output}")
    sidecar = output.with_suffix(".sha256")
    if not sidecar.is_file():
        raise SystemExit(f"FAIL: missing sidecar {sidecar.relative_to(repo)}")
    actual = digest(output)
    recorded = sidecar.read_text(encoding="utf-8").split()[0].upper()
    if actual != recorded:
        raise SystemExit(f"FAIL: stale sidecar for {step.output}")
    json.loads(output.read_text(encoding="utf-8"))
    return actual


def main() -> None:
    repo = Path(__file__).resolve().parents[4]
    results: dict[str, str] = {}
    for step in STEPS:
        print(f"RUN: {step.script}")
        if step.mutations:
            run(repo, step, "--self-test-mutations")
        run(repo, step)
        results[step.output] = verify(repo, step)

    plan_path = (
        repo
        / "Analysis/MAT/MAT-001/PLAN_COMPLETION/outputs/mat001_plan_rr2_through_h7_summary.json"
    )
    tier1_path = (
        repo
        / "Analysis/UVIR/UVIR-003/outputs/uvir003_tier1_peer_review_readiness_summary.json"
    )
    r5_path = (
        repo
        / "Analysis/MAT/MAT-001/R5_IDENTIFIABILITY/outputs/mat001_r5_microscopic_matching_decision_summary.json"
    )
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    tier1 = json.loads(tier1_path.read_text(encoding="utf-8"))
    r5 = json.loads(r5_path.read_text(encoding="utf-8"))
    expected = {
        "mat001_status": "BLOCKED",
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "stage4A_status": "CLOSED",
        "mat001_pass": False,
        "physics_pass": False,
    }
    for label, summary in (("plan", plan), ("tier1", tier1)):
        for key, value in expected.items():
            if summary.get(key) != value:
                raise SystemExit(
                    f"FAIL: {label}.{key} expected {value!r}, got {summary.get(key)!r}"
                )
    if tier1.get("tier1_closure_status") != "NOT_MET":
        raise SystemExit(
            "FAIL: Tier-1 closure was promoted without the open physics gates"
        )
    if r5.get("matching_verdict") != "HOLD_DECLARED_ACTION_UNDERDETERMINES_V":
        raise SystemExit(
            "FAIL: R5 identifiability HOLD changed without new matching evidence"
        )
    for key, value in expected.items():
        if r5.get(key) != value:
            raise SystemExit(f"FAIL: r5.{key} expected {value!r}, got {r5.get(key)!r}")

    print("PASS_MAT001_TIER1_R1_R5_REMEDIATION_CONE")
    print(f"VERIFIED_OUTPUTS={len(results)}")
    print("MAT=BLOCKED | V=NOT_COMPUTED | K_Q=NOT_DERIVED | Stage4A=CLOSED")


if __name__ == "__main__":
    main()
