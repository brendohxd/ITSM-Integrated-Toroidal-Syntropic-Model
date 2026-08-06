#!/usr/bin/env python3
"""Fail-closed runner for the MAT-001 R1 convention remediation cone."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--full-cone",
        action="store_true",
        help="Regenerate reviewed direct and transitive consumers after R1.",
    )
    return parser.parse_args()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def run(repo: Path, script: str, seed: str = "1", *extra: str) -> None:
    env = os.environ.copy()
    env["PYTHONHASHSEED"] = seed
    command = [sys.executable, "-B", str(repo / script), *extra]
    completed = subprocess.run(command, cwd=repo, env=env, check=False)
    if completed.returncode != 0:
        raise SystemExit(
            "FAIL: {0} exited {1}".format(script, completed.returncode)
        )


def verify_sidecar(output: Path) -> str:
    digest = sha256(output)
    sidecar = output.with_suffix(".sha256")
    if not sidecar.is_file():
        raise SystemExit("FAIL: missing sidecar {0}".format(sidecar))
    recorded = sidecar.read_text(encoding="utf-8").split()[0].upper()
    if recorded != digest:
        raise SystemExit("FAIL: stale sidecar for {0}".format(output))
    return digest


def main() -> None:
    args = parse_args()
    repo = Path(__file__).resolve().parents[4]
    exporter = (
        "Analysis/MAT/MAT-001/SAME_CHART_EXPORT/"
        "mat001_same_chart_quadratic_export.py"
    )
    output = repo / (
        "Analysis/MAT/MAT-001/SAME_CHART_EXPORT/outputs/"
        "mat001_same_chart_quadratic_export_summary.json"
    )

    run(repo, exporter, "1", "--self-test-mutations")
    digests = []
    for seed in ("1", "987654"):
        run(repo, exporter, seed)
        digests.append(verify_sidecar(output))
    if len(set(digests)) != 1:
        raise SystemExit("FAIL: exporter is not deterministic across hash seeds")

    summary = json.loads(output.read_text(encoding="utf-8"))
    required = {
        "subgate_status": "PASS_MAT001_SAME_CHART_FREE_QUADRATIC_EXPORT_PARTIAL",
        "V_status": "NOT_COMPUTED",
        "mat001_status": "BLOCKED",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
    }
    for key, expected in required.items():
        if summary.get(key) != expected:
            raise SystemExit(
                "FAIL: {0} expected {1!r}, got {2!r}".format(
                    key, expected, summary.get(key)
                )
            )

    if args.full_cone:
        scripts = [
            "Analysis/MAT/MAT-001/S_INT_DH_EXPORT/mat001_s_int_dh_export_audit.py",
            "Analysis/MAT/MAT-001/FORCE_HOSTING/mat001_force_hosting_readiness_audit.py",
            "Analysis/MAT/MAT-001/TRACK_A_S_INT/mat001_track_a_s_int_embed_audit.py",
            "Analysis/MAT/MAT-001/TRACK_A_KQ/mat001_track_a_kq_readiness_audit.py",
            "Analysis/MAT/MAT-001/KQ_DERIVATION_DIG/mat001_kq_derivation_dig_audit.py",
            "Analysis/MAT/MAT-001/CONDITIONAL_MATCHING_BRANCH/mat001_conditional_matching_branch.py",
            "Analysis/MAT/MAT-001/TRACK_A_JOIN/mat001_track_a_join_readiness_audit.py",
            "Analysis/MAT/MAT-001/PARENT_ACTION_MATCHING/mat001_parent_action_matching_attempt.py",
            "Analysis/MAT/MAT-001/PARENT_ACTION_MATCHING/mat001_parent_action_h13_source_derivation_audit.py",
            "Analysis/MAT/MAT-001/PARENT_ACTION_MATCHING/mat001_rr1_parent_action_skeleton_declaration.py",
            "Analysis/MAT/MAT-001/PARENT_ACTION_MATCHING/mat001_rr2_residue_pathway_attempt.py",
            "Analysis/MAT/MAT-001/PLAN_COMPLETION/mat001_plan_rr2_through_h7_package.py",
        ]
        for script in scripts:
            run(repo, script)

    print("PASS_R1_REMEDIATION_REPRODUCIBLE")
    print("JSON_SHA256={0}".format(digests[0]))
    print("MAT=BLOCKED | V=NOT_COMPUTED | Stage4A=CLOSED")


if __name__ == "__main__":
    main()
