#!/usr/bin/env python3
"""Cross-package fail-closed review for the RG1/P2 dependency checkpoint."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "outputs"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_seal(path: Path) -> dict[str, Any]:
    rows = []
    for line in path.read_text(encoding="ascii").splitlines():
        expected, name = line.split("  ", 1)
        target = path.parent / name
        got = digest(target)
        rows.append({"file": name, "expected": expected, "got": got, "ok": got == expected})
    return {"seal": str(path.relative_to(ROOT)), "ok": bool(rows) and all(row["ok"] for row in rows), "files": rows}


def add_check(rows: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    rows.append({"name": name, "ok": bool(ok), **details})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    packages = {
        "M2": {
            "summary": ROOT / "Analysis/MAT/MAT-001/M2_RADIAL_MATCHING/outputs/mat001_m2_radial_heavy_reduction_summary.json",
            "seal": ROOT / "Analysis/MAT/MAT-001/M2_RADIAL_MATCHING/outputs/mat001_m2_radial_heavy_reduction.sha256",
            "expected": "REJECT_MINIMAL_M2_CLASSES_SOFT_RESIDUE_NOT_DERIVED",
        },
        "U2": {
            "summary": ROOT / "Analysis/UVIR/UVIR-003/U2_A0_A2/outputs/uvir003_u2_a0_a2_nonzero_gradient_summary.json",
            "seal": ROOT / "Analysis/UVIR/UVIR-003/U2_A0_A2/outputs/uvir003_u2_a0_a2_nonzero_gradient.sha256",
            "expected": "FREEZE_U2_AT_A0_A2_INCOMPLETE_ACTION_DOMAIN_AND_DOF",
        },
        "S0": {
            "summary": ROOT / "Analysis/CBR/CBR-002/S0_NO_SCREENING/outputs/cbr002_s0_no_screening_control_summary.json",
            "seal": ROOT / "Analysis/CBR/CBR-002/S0_NO_SCREENING/outputs/cbr002_s0_no_screening_control.sha256",
            "expected": "REJECT_S0_AS_COMPLETE_LOCAL_GRAVITY_ROUTE",
        },
        "VOR_TOP_S2": {
            "summary": ROOT / "Analysis/VOR/VOR-001/S2_WINDING_MODULI/outputs/vor_top_s2_winding_moduli_summary.json",
            "seal": ROOT / "Analysis/VOR/VOR-001/S2_WINDING_MODULI/outputs/vor_top_s2_winding_moduli.sha256",
            "expected": "REPAIR_VOR_S2_AND_REJECT_WINDING_ONLY_GENERIC_MODULI_STABILIZATION",
        },
    }
    plan = ROOT / "Theory/Core/ITSM_RG1_P2_DEPENDENCY_CLEARING_PLAN.md"
    plan_text = plan.read_text(encoding="utf-8")
    checks: list[dict[str, Any]] = []
    package_results: dict[str, Any] = {}
    for name, cfg in packages.items():
        summary = load(cfg["summary"])
        seal_result = verify_seal(cfg["seal"])
        add_check(checks, f"{name}_seal_valid", seal_result["ok"], seal=seal_result)
        add_check(
            checks,
            f"{name}_disposition_exact",
            summary.get("route_disposition") == cfg["expected"],
            expected=cfg["expected"],
            got=summary.get("route_disposition"),
        )
        add_check(checks, f"{name}_physics_pass_false", summary.get("physics_pass") is False)
        package_results[name] = {
            "disposition": summary.get("route_disposition"),
            "calculation_status": summary.get("calculation_status"),
            "summary_sha256": digest(cfg["summary"]),
            "seal": seal_result,
        }

    m2 = load(packages["M2"]["summary"])
    u2 = load(packages["U2"]["summary"])
    s0 = load(packages["S0"]["summary"])
    vor = load(packages["VOR_TOP_S2"]["summary"])
    add_check(
        checks,
        "parent_gate_firewall",
        m2.get("MAT_001_status") == "BLOCKED"
        and m2.get("V_status") == "NOT_COMPUTED"
        and u2.get("UVIR_003_status") == "IN_PROGRESS"
        and u2.get("K_Q_status") == "NOT_DERIVED"
        and s0.get("SCR_001_status") == "NOT_OPENED_BY_THIS_CONTROL"
        and vor.get("VOR_001_status") == "OPEN_SCAFFOLD_ONLY"
        and vor.get("TOP_001_status") == "OPEN_SCAFFOLD_ONLY",
    )
    add_check(
        checks,
        "vor_preregistered_failure_preserved",
        vor.get("VOR_S2_tests", {}).get("S2-T02", {}).get("status") == "FAIL_PREREGISTERED_NUMERICAL_CRITERION"
        and vor.get("VOR_S2_tests", {}).get("S2-T02", {}).get("exact_relative_deviation") == "1/200",
    )
    add_check(
        checks,
        "no_downstream_stage_opened",
        "NO_DOWNSTREAM_STAGE_OPENED" in plan_text
        and all(term in plan_text for term in ("Local gravity", "lensing", "SPARC", "cosmology", "publication")),
    )

    all_ok = all(row["ok"] for row in checks)
    summary = {
        "audit": "RG1_P2_DEPENDENCY_CLEARING_REVIEW",
        "calculation_status": "PASS_CROSS_PACKAGE_INTEGRITY_REVIEW" if all_ok else "FAIL_CROSS_PACKAGE_INTEGRITY_REVIEW",
        "checkpoint_disposition": "NO_DOWNSTREAM_STAGE_OPENED" if all_ok else "HOLD_REVIEW_FAILURE",
        "package_results": package_results,
        "parent_status": {
            "UVIR_003": "IN_PROGRESS",
            "MAT_001": "BLOCKED",
            "V": "NOT_COMPUTED",
            "K_Q": "NOT_DERIVED",
            "SCR_001": "NOT_OPENED",
            "VOR_001": "OPEN_SCAFFOLD_ONLY",
            "TOP_001": "OPEN_SCAFFOLD_ONLY",
        },
        "downstream": {
            "local_gravity": "CLOSED",
            "lensing": "CLOSED",
            "disks": "CLOSED",
            "SPARC": "CLOSED",
            "cosmology": "CLOSED",
            "publication": "CLOSED",
        },
        "physics_pass": False,
        "checks": checks,
        "plan_sha256": digest(plan),
        "scientific_boundary": "This review verifies package integrity, deterministic seals, exact dispositions and gate firewalls. It does not independently upgrade any scientific result or authorize downstream execution, commit, push, deployment or publication.",
    }
    json_path = OUT / "rg1_p2_dependency_clearing_review_summary.json"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = f"""# RG1/P2 dependency-clearing hostile review

**Calculation:** `{summary['calculation_status']}`  
**Checkpoint:** `{summary['checkpoint_disposition']}`  
**Physics pass:** `false`

| Package | Disposition |
|---|---|
| M2 | `{m2['route_disposition']}` |
| U2 | `{u2['route_disposition']}` |
| S0 | `{s0['route_disposition']}` |
| VOR/TOP S2 | `{vor['route_disposition']}` |

All four packages preserve their parent firewalls. The prior VOR S2 pass is
superseded because its T02 runner did not execute the preregistered point.
No package clears the prerequisite needed to open local gravity, lensing,
disks, SPARC, cosmology or publication.

This is an integrity/review pass, not a Tier-1 physics pass.
"""
    report_path = OUT / "RG1_P2_DEPENDENCY_CLEARING_REVIEW.md"
    report_path.write_text(report, encoding="utf-8")
    seal = "\n".join(f"{digest(path)}  {path.name}" for path in (json_path, report_path)) + "\n"
    (OUT / "rg1_p2_dependency_clearing_review.sha256").write_text(seal, encoding="ascii")
    print(json.dumps({"checkpoint": summary["checkpoint_disposition"], "checks": len(checks)}))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
