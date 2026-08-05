#!/usr/bin/env python3
"""Fail-closed UVIR-003 to MAT-001 scoped-handoff contract audit.

This audit distinguishes a structurally valid engineering handoff from
authorization to claim a matched vertex or MAT/UVIR physics pass. It consumes
the current UVIR closure records and MAT structural contracts, verifies their
status boundaries exactly, and keeps V NOT_COMPUTED.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


PASS_STATUS = "PASS_MAT001_UVIR_HANDOFF_CONTRACT_BLOCKED"
FAIL_STATUS = "FAIL_MAT001_UVIR_HANDOFF_CONTRACT"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    repo = base.parents[3]
    uvir = repo / "Analysis" / "UVIR" / "UVIR-003" / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stage5-summary",
        type=Path,
        default=uvir / "uvir003_stage5_full_gate_decision_summary.json",
    )
    parser.add_argument(
        "--closure-summary",
        type=Path,
        default=uvir / "uvir003_full_gate_closure_audit_summary.json",
    )
    parser.add_argument(
        "--floor-summary",
        type=Path,
        default=uvir / "uvir003_conditional_matching_floor_summary.json",
    )
    parser.add_argument(
        "--stage4-summary",
        type=Path,
        default=uvir / "uvir003_stage4_m3m6_conditional_limit_summary.json",
    )
    parser.add_argument(
        "--j1-summary",
        type=Path,
        default=mat
        / "J1_JOINT_ACTION"
        / "outputs"
        / "mat001_j1_joint_action_normalization_summary.json",
    )
    parser.add_argument(
        "--r2-summary",
        type=Path,
        default=mat
        / "R2_DIRECT_RESIDUE"
        / "outputs"
        / "mat001_r2_direct_residue_audit_summary.json",
    )
    parser.add_argument(
        "--unit-summary",
        type=Path,
        default=mat
        / "UNIT_CHART"
        / "outputs"
        / "mat001_unit_chart_contract_summary.json",
    )
    parser.add_argument(
        "--kinetic-inventory-summary",
        type=Path,
        default=mat / "outputs" / "mat001_v_kinetic_chart_inventory_summary.json",
    )
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
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


def sidecar_contract(path: Path, digest: str | None) -> dict[str, Any]:
    sidecar = path.with_suffix(".sha256")
    if not sidecar.is_file():
        return {
            "present": False,
            "required": False,
            "ok": True,
            "recorded": None,
        }
    try:
        recorded = sidecar.read_text(encoding="utf-8").split()[0].upper()
    except (OSError, UnicodeError, IndexError) as exc:
        return {
            "present": True,
            "required": True,
            "ok": False,
            "recorded": None,
            "error": f"{type(exc).__name__}:{exc}",
        }
    return {
        "present": True,
        "required": True,
        "ok": bool(digest and recorded == digest),
        "recorded": recorded,
    }


def contains_all(values: Any, required: set[str]) -> bool:
    return isinstance(values, list) and required.issubset(set(values))


def stage5_contract(data: dict[str, Any] | None) -> bool:
    return bool(
        data
        and data.get("subgate_status") == "PASS_STAGE5_DECISION_HOLD_TIER1"
        and data.get("calculation_status") == "PASS"
        and data.get("decision") == "HOLD_TIER1_CLOSURE"
        and data.get("full_gate_status") == "IN_PROGRESS"
        and data.get("mat001_status") == "BLOCKED_PASS_TAG_FORBIDDEN"
        and data.get("kq_numeric_status") == "NOT_DERIVED"
        and data.get("V_status") == "NOT_COMPUTED"
        and data.get("physics_pass_under_declared_conditional_policy") is False
        and data.get("physics_pass_derived_theory_closed") is False
        and contains_all(data.get("blocking_for_tier1_closure"), {"M2", "M3", "M6", "M7"})
    )


def closure_contract(data: dict[str, Any] | None) -> bool:
    return bool(
        data
        and data.get("subgate_status") == "PASS_UVIR003_CLOSURE_CHECKLIST_AUDIT"
        and data.get("calculation_status") == "PASS"
        and data.get("full_gate_status") == "IN_PROGRESS"
        and data.get("mat001_status") == "BLOCKED_PASS_TAG_FORBIDDEN"
        and data.get("stage5_decision_present") is True
        and data.get("stage5_decision_consistent") is True
        and contains_all(
            data.get("blocking_for_full_pass"),
            {
                "M2_stability_declared_domain",
                "M3_causality_declared_domain",
                "M6_physical_cutoff",
                "M7_matter_ready_for_MAT",
            },
        )
    )


def floor_contract(data: dict[str, Any] | None) -> bool:
    stage2 = data.get("stage_2_exit", {}) if data else {}
    return bool(
        data
        and data.get("subgate_status") == "PASS_CONDITIONAL_MATCHING_FLOOR"
        and data.get("calculation_status") == "PASS"
        and data.get("full_gate_status") == "IN_PROGRESS"
        and data.get("mat001_status") == "BLOCKED"
        and data.get("kq_numeric_status") == "NOT_DERIVED"
        and data.get("physics_pass") is False
        and stage2.get("allows_stage3_scoped_MAT_calculation") is True
        and stage2.get("allows_MAT_PASS") is False
        and stage2.get("allows_UVIR_full_PASS") is False
    )


def stage4_contract(data: dict[str, Any] | None) -> bool:
    stage4 = data.get("stage_4_exit", {}) if data else {}
    return bool(
        data
        and data.get("subgate_status") == "PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT"
        and data.get("calculation_status") == "PASS"
        and data.get("full_gate_status") == "IN_PROGRESS"
        and data.get("mat001_status") == "BLOCKED"
        and data.get("kq_numeric_status") == "NOT_DERIVED"
        and data.get("V_status") == "NOT_COMPUTED"
        and data.get("physics_pass") is False
        and data.get("tier1_closure_sufficient") is False
        and stage4.get("status") == "HOLD_MATCHED_STAGE4A_REQUIRED"
        and stage4.get("allows_MAT_PASS") is False
        and stage4.get("allows_UVIR_full_PASS") is False
        and stage4.get("allows_downstream_Derived") is False
    )


def j1_contract(data: dict[str, Any] | None) -> bool:
    return bool(
        data
        and data.get("subgate_status") == "PASS_MAT001_J1_JOINT_ACTION_NORMALIZATION_IDENTITY"
        and data.get("V_form_status") == "SAME_ACTION_IDENTITY_DERIVED"
        and data.get("V_status") == "NOT_COMPUTED"
        and data.get("mat001_pass") is False
        and data.get("physics_pass") is False
    )


def r2_contract(data: dict[str, Any] | None) -> bool:
    return bool(
        data
        and data.get("subgate_status") == "PASS_MAT001_R2_DIRECT_RESIDUE_AUDIT"
        and data.get("V_status") == "NOT_COMPUTED"
        and data.get("mat001_status") == "BLOCKED"
        and data.get("uv_ir_full_gate_status") == "IN_PROGRESS"
        and data.get("stage4A_status") == "CLOSED"
        and data.get("mat001_pass") is False
        and data.get("physics_pass") is False
    )


def unit_contract(data: dict[str, Any] | None) -> bool:
    return bool(
        data
        and data.get("subgate_status") == "PASS_MAT001_UNIT_CHART_CONTRACT_OPEN"
        and data.get("V_status") == "NOT_COMPUTED"
        and data.get("kq_numeric_status") == "NOT_DERIVED"
        and data.get("mat001_status") == "BLOCKED"
        and data.get("stage4A_unlock") is False
        and data.get("mat001_pass") is False
        and data.get("physics_pass") is False
    )


def kinetic_contract(data: dict[str, Any] | None) -> bool:
    return bool(
        data
        and data.get("subgate_status") == "PASS_MAT001_V_KINETIC_CHART_INVENTORY_OPEN"
        and data.get("inventory_status") == "COMPLETE_BLOCKER_MAP_V_OPEN"
        and data.get("kq_numeric_status") == "NOT_DERIVED"
        and data.get("mat001_gate_status") == "BLOCKED_PASS_TAG_FORBIDDEN"
        and data.get("V_status") == "NOT_COMPUTED"
        and data.get("mat001_pass") is False
        and data.get("physics_pass") is False
    )


def main() -> None:
    args = parse_args()
    inputs: dict[str, tuple[Path, Callable[[dict[str, Any] | None], bool]]] = {
        "UVIR_stage5": (args.stage5_summary, stage5_contract),
        "UVIR_closure": (args.closure_summary, closure_contract),
        "UVIR_matching_floor": (args.floor_summary, floor_contract),
        "UVIR_stage4": (args.stage4_summary, stage4_contract),
        "MAT_J1": (args.j1_summary, j1_contract),
        "MAT_R2": (args.r2_summary, r2_contract),
        "MAT_unit_chart": (args.unit_summary, unit_contract),
        "MAT_kinetic_inventory": (args.kinetic_inventory_summary, kinetic_contract),
    }

    evidence: dict[str, Any] = {}
    checks: list[dict[str, Any]] = []
    for name, (path, contract) in inputs.items():
        data, error, digest = load_json(path)
        sidecar = sidecar_contract(path, digest)
        contract_ok = contract(data)
        evidence[name] = {
            "source": path.name,
            "sha256": digest,
            "parse_error": error,
            "sidecar": sidecar,
            "exact_contract_ok": contract_ok,
        }
        checks.append(
            {
                "name": f"{name}_exact_contract",
                "ok": error is None and contract_ok and sidecar["ok"],
                "source": path.name,
                "parse_error": error,
                "sidecar_ok": sidecar["ok"],
            }
        )

    boundary = {
        "structural_handoff_ready": True,
        "scoped_projection_audit_authorized": True,
        "numeric_V_matching_ready": False,
        "stage4A_reopen_ready": False,
        "MAT_pass_authorized": False,
        "UVIR_full_pass_authorized": False,
        "downstream_Derived_authorized": False,
        "physics_pass": False,
    }
    checks.append(
        {
            "name": "handoff_boundary_fail_closed",
            "ok": (
                boundary["structural_handoff_ready"]
                and boundary["scoped_projection_audit_authorized"]
                and all(
                    boundary[key] is False
                    for key in (
                        "numeric_V_matching_ready",
                        "stage4A_reopen_ready",
                        "MAT_pass_authorized",
                        "UVIR_full_pass_authorized",
                        "downstream_Derived_authorized",
                        "physics_pass",
                    )
                )
            ),
            "boundary": boundary,
        }
    )

    all_ok = all(check["ok"] for check in checks)
    subgate = PASS_STATUS if all_ok else FAIL_STATUS
    summary: dict[str, Any] = {
        "gate": "MAT-001",
        "interface": "UVIR-003_TO_MAT-001",
        "stage": "FAIL_CLOSED_HANDOFF_CONTRACT",
        "subgate_status": subgate,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "handoff_audit_pass": all_ok,
        "structural_handoff_status": (
            "READY_FOR_SCOPED_PROJECTION_AUDIT" if all_ok else "INVALID_INPUT_CONTRACT"
        ),
        "numeric_matching_status": "BLOCKED_INPUTS_NOT_DERIVED",
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "blocking_requirements": {
            "M2": "relevant IR complex-quartet response control",
            "M3": "causality re-evaluated with a matched invariant",
            "M6": "gauge-invariant physical cutoff/unitarity result",
            "M7": "same-action physical-mode matter vertex and kinetic normalization",
        },
        "authorized_next_operations": [
            "derive and audit the basis-covariant physical-mode source projection symbolically",
            "identify the exact action-level source vector and kinetic metric required from the live UVIR reduction",
            "keep every numerical matching output disabled until both inputs are present in one declared chart",
        ],
        "forbidden_next_operations": [
            "assign a numerical V from the structural identities",
            "reopen Stage 4A before a matched invariant exists",
            "issue MAT-001 or UVIR-003 physics PASS",
            "use the handoff for downstream Derived observables",
        ],
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "scientific_boundary": (
            "A PASS means the current UVIR and MAT records form a consistent, fail-closed "
            "engineering handoff for a symbolic physical-mode projection audit. It does not "
            "supply the missing action-level coefficients, compute V, reopen Stage 4A, close "
            "UVIR-003, pass MAT-001, or authorize downstream Derived claims."
        ),
        "serial_next": (
            "Construct the basis-covariant physical-mode vertex projection identity and "
            "negative controls; then test whether the live UVIR action exports the required "
            "source vector and kinetic metric in one chart."
        ),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_uvir_handoff_contract_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    sidecar = args.output_dir / "mat001_uvir_handoff_contract_summary.sha256"
    sidecar.write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("MAT-001 UVIR handoff contract audit")
    print("  structural handoff: READY_FOR_SCOPED_PROJECTION_AUDIT")
    print("  V_status: NOT_COMPUTED | MAT: BLOCKED | Stage4A: CLOSED")
    for check in checks:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS: {0}".format(subgate))
    print("JSON_SHA256: {0}".format(digest))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
