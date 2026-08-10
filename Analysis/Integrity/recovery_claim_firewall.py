#!/usr/bin/env python3
"""Fail-closed consistency checks for the ITSM recovery authority surface.

This is a repository-integrity check, not a physics calculation or physics pass.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OUTPUT_JSON = OUTPUT_DIR / "recovery_claim_firewall_summary.json"
OUTPUT_SHA = OUTPUT_DIR / "recovery_claim_firewall_summary.sha256"


def load_json(relative: str) -> dict[str, Any]:
    with (ROOT / relative).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TypeError(f"Expected a JSON object: {relative}")
    return value


def record(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def main() -> int:
    checks: list[dict[str, Any]] = []

    r5_path = (
        "Analysis/MAT/MAT-001/R5_IDENTIFIABILITY/outputs/"
        "mat001_r5_microscopic_matching_decision_summary.json"
    )
    plan_path = (
        "Analysis/MAT/MAT-001/PLAN_COMPLETION/outputs/"
        "mat001_plan_rr2_through_h7_summary.json"
    )
    tier1_path = (
        "Analysis/UVIR/UVIR-003/outputs/"
        "uvir003_tier1_peer_review_readiness_summary.json"
    )
    r5p1_path = (
        "Analysis/MAT/MAT-001/R5_P1/outputs/"
        "mat001_r5_p1_scaffold_summary.json"
    )

    r5 = load_json(r5_path)
    record(
        checks,
        "r5_identifiability_hold",
        r5.get("matching_verdict") == "HOLD_DECLARED_ACTION_UNDERDETERMINES_V"
        and r5.get("mat001_status") == "BLOCKED"
        and r5.get("V_status") == "NOT_COMPUTED"
        and r5.get("kq_numeric_status") == "NOT_DERIVED"
        and r5.get("stage4A_status") == "CLOSED"
        and r5.get("mat001_pass") is False
        and r5.get("physics_pass") is False,
        source=r5_path,
    )

    plan = load_json(plan_path)
    record(
        checks,
        "bounded_plan_remains_fail_closed",
        plan.get("mat001_status") == "BLOCKED"
        and plan.get("V_status") == "NOT_COMPUTED"
        and plan.get("kq_numeric_status") == "NOT_DERIVED"
        and plan.get("stage4A_status") == "CLOSED"
        and plan.get("mat001_pass") is False
        and plan.get("physics_pass") is False,
        source=plan_path,
    )

    tier1 = load_json(tier1_path)
    record(
        checks,
        "uvir_tier1_hold",
        tier1.get("tier1_closure_status") == "NOT_MET"
        and tier1.get("uv_ir_full_gate_status") == "IN_PROGRESS"
        and tier1.get("mat001_status") == "BLOCKED"
        and tier1.get("V_status") == "NOT_COMPUTED"
        and tier1.get("kq_numeric_status") == "NOT_DERIVED"
        and tier1.get("stage4A_status") == "CLOSED"
        and tier1.get("mat001_pass") is False
        and tier1.get("physics_pass") is False,
        source=tier1_path,
    )

    r5p1 = load_json(r5p1_path)
    artifact_states = [item.get("status") for item in r5p1.get("artifacts", [])]
    record(
        checks,
        "r5_p1_is_scaffold_only",
        r5p1.get("research_gate_status") == "OPEN_RESEARCH_CANDIDATE"
        and r5p1.get("physics_pass") is False
        and r5p1.get("stubs_remaining") == 8
        and r5p1.get("artifacts_total") == 8
        and artifact_states == ["STUB"] * 8,
        source=r5p1_path,
    )

    spec_path = ROOT / "Theory/Gates/MAT-001/MAT-001_R5_P1_SPEC.md"
    spec = spec_path.read_text(encoding="utf-8")
    record(
        checks,
        "r5_p1_spec_all_artifacts_todo",
        "**Status:** `OPEN_RESEARCH_CANDIDATE`" in spec
        and spec.count("| TODO |") == 8,
        source=str(spec_path.relative_to(ROOT)).replace("\\", "/"),
    )

    version_path = ROOT / "Manuscript/CoreRecovery/VERSION"
    version = version_path.read_text(encoding="utf-8").strip()
    alpha12_pdf = (
        ROOT
        / "Manuscript/CoreRecovery/releases/v12.0-alpha.12/ITSM_Core_v12.0-alpha.12.pdf"
    )
    record(
        checks,
        "frozen_release_boundary_alpha12",
        version == "12.0-alpha.12" and alpha12_pdf.is_file(),
        version=version,
    )

    forbidden_paths = [
        "Analysis/STAT/STAT-001/stat001_inference_pipeline.py",
        "Theory/Gates/STAT-001/STAT-001_GATE_REPORT.md",
        "Analysis/UVIR/UVIR-003/uvir003_r5_p1_2to2_amplitude.py",
        "Analysis/UVIR/UVIR-003/uvir003_r5_p1_cubic_exchange.py",
        "Analysis/UVIR/UVIR-003/uvir003_r5_p1_physical_quadratic_propagators.py",
        "Analysis/UVIR/UVIR-003/uvir003_r5_p1_q0_channel.py",
        "Manuscript/ITSM_Core_Cosmology_v12.0-alpha.13.tex",
        "Manuscript/ITSM_Core_Cosmology_v12.0-alpha.13.pdf",
        "active_research_updated.md",
    ]
    present_forbidden = [path for path in forbidden_paths if (ROOT / path).exists()]
    record(
        checks,
        "known_pseudo_closure_artifacts_absent",
        not present_forbidden,
        forbidden_paths_present=present_forbidden,
    )

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    record(
        checks,
        "readme_retains_recovery_boundary",
        "v12.0-alpha.12" in readme
        and "| **UVIR-003** | **In progress** |" in readme
        and "| **MAT-001** | **Blocked; $V$ not computed** |" in readme,
    )

    all_ok = all(item["ok"] for item in checks)
    summary = {
        "gate": "RECOVERY_CLAIM_FIREWALL",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": (
            "PASS_RECOVERY_AUTHORITY_CONSISTENT_FAIL_CLOSED"
            if all_ok
            else "FAIL_RECOVERY_AUTHORITY_INCONSISTENT"
        ),
        "physics_pass": False,
        "scientific_boundary": (
            "This check verifies repository status consistency and known quarantine "
            "guards. It does not validate an action, derivation, stability domain, "
            "physical amplitude, cutoff, observation, or physics gate."
        ),
        "reconstruction_anchor": "4682a51",
        "quarantined_scientific_range": "c3386f0..4310a9a",
        "checks": checks,
        "n_checks": len(checks),
        "n_failed": sum(not item["ok"] for item in checks),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    OUTPUT_JSON.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    OUTPUT_SHA.write_text(f"{digest}  {OUTPUT_JSON.name}\n", encoding="ascii")
    print(summary["subgate_status"])
    print(f"physics_pass={summary['physics_pass']}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
