#!/usr/bin/env python3
"""Record the non-promoting handoff to a separately designed X4-S4 parent."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


STATUS = "ROUTE_HANDOFF_X4_S4_NEW_PARENT_DESIGN_ONLY"
ERROR_STATUS = "ERROR_TOPX4_H1_COMPENSATED_WARPED_CHILD_DESIGN"

REPO_ROOT = Path(__file__).resolve().parents[4]
BASE = Path(__file__).resolve().parent
OUTPUT_PATH = (
    BASE / "outputs" / "mat001_topx4_h1_compensated_warped_child_design_summary.json"
)
REPORT_PATH = (
    BASE / "MAT001_TOPX4_H1_COMPENSATED_WARPED_CHILD_DESIGN_2026-09-17.md"
)
CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_COMPENSATED_WARPED_CHILD_DESIGN_CONTRACT_2026-09-17.md"
)
DECISION_SUMMARY_PATH = (
    BASE / "outputs" / "mat001_topx4_h1_brane_child_freeze_decision_summary.json"
)
S0_AUDIT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_S0_STABILIZATION_CANDIDATE_AUDIT_2026-09-06.md"
)
PARENT_FREEZE_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md"
)
A1_LEDGER_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md"
)
ARCH_SUMMARY_PATH = (
    BASE / "outputs" / "mat001_topx4_h1_matter_architecture_comparison_summary.json"
)
BRIDGE_SUMMARY_PATH = BASE / "outputs" / "mat001_topx4_h1_bridge_readiness_summary.json"
A2A3_SUMMARY_PATH = (
    REPO_ROOT
    / "Analysis"
    / "TOP"
    / "TOP-X4"
    / "outputs"
    / "topx4_a2a3_reduction_radion_summary.json"
)
HESSIAN_SUMMARY_PATH = (
    REPO_ROOT
    / "Analysis"
    / "TOP"
    / "TOP-X4"
    / "outputs"
    / "topx4_s2f3_physical_hessian_readiness_summary.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    parser.add_argument("--self-test-mutations", action="store_true")
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def sidecar_candidates(path: Path) -> list[Path]:
    values = [Path(str(path) + ".sha256"), path.with_suffix(".sha256")]
    return list(dict.fromkeys(values))


def find_sidecar(path: Path) -> Path | None:
    return next((item for item in sidecar_candidates(path) if item.is_file()), None)


def write_sidecar(path: Path, *, replace_suffix: bool = False) -> Path:
    sidecar = path.with_suffix(".sha256") if replace_suffix else Path(str(path) + ".sha256")
    sidecar.write_text(
        f"{sha256_file(path)}  {path.name}\n", encoding="ascii", newline="\n"
    )
    return sidecar


def artifact_receipt(path: Path, *, sidecar_required: bool = True) -> dict[str, Any]:
    exists = path.is_file()
    digest = sha256_file(path) if exists else None
    sidecar = find_sidecar(path) if exists else None
    expected: str | None = None
    if sidecar is not None:
        tokens = sidecar.read_text(encoding="ascii").split()
        expected = tokens[0].lower() if tokens else "MALFORMED"
    return {
        "path": relative(path),
        "exists": exists,
        "sha256": digest,
        "sidecar_required": sidecar_required,
        "sidecar_path": relative(sidecar) if sidecar is not None else None,
        "sidecar_matches": digest == expected if expected is not None else None,
    }


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"Expected JSON object: {path}")
    return data


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def build_summary(receipts: list[dict[str, Any]]) -> dict[str, Any]:
    decision = load_json(DECISION_SUMMARY_PATH)
    architecture = load_json(ARCH_SUMMARY_PATH)
    bridge = load_json(BRIDGE_SUMMARY_PATH)
    a2a3 = load_json(A2A3_SUMMARY_PATH)
    hessian = load_json(HESSIAN_SUMMARY_PATH)
    s0_text = " ".join(S0_AUDIT_PATH.read_text(encoding="utf-8").lower().split())
    parent_text = " ".join(PARENT_FREEZE_PATH.read_text(encoding="utf-8").lower().split())
    ledger_text = " ".join(A1_LEDGER_PATH.read_text(encoding="utf-8").lower().split())
    contract_text = " ".join(
        CONTRACT_PATH.read_text(encoding="utf-8").lower().split()
    )

    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "all_authority_and_input_files_exist",
        all(item["exists"] for item in receipts),
        missing=[item["path"] for item in receipts if not item["exists"]],
    )
    add_check(
        checks,
        "all_required_sidecars_match_current_bytes",
        all(
            (not item["sidecar_required"]) or item["sidecar_matches"] is True
            for item in receipts
        ),
        failures=[
            item["path"]
            for item in receipts
            if item["sidecar_required"] and item["sidecar_matches"] is not True
        ],
    )
    add_check(
        checks,
        "minimal_child_rejection_is_binding",
        decision.get("status") == "REJECT_MINIMAL_BRANE_CHILD_FREEZE_CONDITIONALLY"
        and decision.get("decision", {}).get("minimal_child")
        == "REJECTED_ZERO_TENSION_DISTRIBUTIONAL_CONTROL"
        and decision.get("status_firewall", {}).get("brane_child_action_frozen")
        is False,
    )
    add_check(
        checks,
        "pre_registered_x4_s4_route_is_deferred_new_parent",
        "x4-s4" in s0_text
        and "orbifold/brane" in s0_text
        and "defer as a different parent" in s0_text,
    )
    add_check(
        checks,
        "smooth_s1_flux_route_has_no_distinct_minimal_repair",
        "x4-s3" in s0_text
        and "no distinct minimal" in s0_text
        and "repair was identified" in s0_text,
    )
    add_check(
        checks,
        "frozen_parent_has_no_hidden_brane_or_portal",
        "brane term" in parent_text
        and "matter portal" in parent_text
        and "all fields are bulk fields" in ledger_text,
    )
    add_check(
        checks,
        "new_parent_boundary_is_explicit",
        "new parent design" in contract_text
        and "not an extension of the frozen x4-s2f3 control" in contract_text
        and "does not freeze x4-s4" in contract_text,
    )
    add_check(
        checks,
        "required_x4_s4_design_inputs_are_listed",
        "junction" in contract_text
        and "brane-bending" in contract_text
        and "global balance" in contract_text
        and "localized quantum counterterms" in contract_text
        and "finite-charge on-shell background" in contract_text,
    )
    add_check(
        checks,
        "route_screen_does_not_select_an_unregistered_compensator",
        "hidden second brane" in contract_text
        and "new flux field" in contract_text
        and "not_authorized" in contract_text,
    )
    add_check(
        checks,
        "downstream_physics_and_gate_holds_remain_binding",
        architecture.get("parent_action_changed") is False
        and bridge.get("status_firewall", {}).get("MAT001_pass") is False
        and bridge.get("status_firewall", {}).get("K_Q_derived") is False
        and bridge.get("status_firewall", {}).get("V_computed") is False
        and a2a3.get("physics_pass") is False
        and hessian.get("physics_pass") is False,
    )

    route = {
        "minimal_unwarped_single_tension_child": "REJECTED",
        "smooth_S1_flux_repair": "NO_DISTINCT_MINIMAL_ROUTE_REGISTERED",
        "brane_route": "OPEN_ONLY_AS_X4-S4_NEW_PARENT_DESIGN",
        "child_action_freeze": "NOT_AUTHORIZED",
        "X4-S4_action_freeze": "NOT_AUTHORIZED",
        "parent_action_changed": False,
        "selected_from_observational_target": False,
    }

    return {
        "schema": "ITSM_MAT001_TOPX4_H1_COMPENSATED_WARPED_CHILD_DESIGN_v1",
        "date": "2026-09-17",
        "status": STATUS,
        "audit_execution_status": "COMPLETE",
        "checks": checks,
        "checks_passed": sum(1 for item in checks if item["ok"]),
        "checks_total": len(checks),
        "route": route,
        "scientific_boundary": (
            "The minimal unwarped brane child is rejected. The registered "
            "X4-S4 orbifold/brane family is only a separate new-parent design "
            "route; no action or compensator is selected."
        ),
        "status_firewall": {
            "parent_action_changed": False,
            "child_action_frozen": False,
            "X4-S4_action_frozen": False,
            "compensator_selected": False,
            "warp_profile_selected": False,
            "global_sum_rule_derived": False,
            "localized_counterterms_normalized": False,
            "physical_hessian_constructed": False,
            "MAT001_pass": False,
            "K_Q_derived": False,
            "V_computed": False,
            "stage4A_reopened": False,
            "rule9_cleared": False,
            "physics_pass": False,
            "gate_effect": "NONE",
        },
        "artifact_receipts": receipts,
        "next_single_gate": {
            "name": "TOPX4_H1_X4-S4_NEW_PARENT_ACTION_CONTRACT",
            "scope": (
                "Choose and derive a complete X4-S4 field content, geometry, "
                "localized action and global balance before freezing it."
            ),
            "stop_before": "NO_CHANGE_TO_X4_S2F3",
        },
    }


def exported_contract_valid(summary: dict[str, Any]) -> bool:
    checks = summary.get("checks", [])
    route = summary.get("route", {})
    firewall = summary.get("status_firewall", {})
    return (
        summary.get("status") == STATUS
        and summary.get("checks_passed") == summary.get("checks_total") == len(checks)
        and all(item.get("ok") is True for item in checks)
        and route.get("minimal_unwarped_single_tension_child") == "REJECTED"
        and route.get("smooth_S1_flux_repair")
        == "NO_DISTINCT_MINIMAL_ROUTE_REGISTERED"
        and route.get("brane_route") == "OPEN_ONLY_AS_X4-S4_NEW_PARENT_DESIGN"
        and route.get("child_action_freeze") == "NOT_AUTHORIZED"
        and route.get("X4-S4_action_freeze") == "NOT_AUTHORIZED"
        and route.get("parent_action_changed") is False
        and route.get("selected_from_observational_target") is False
        and firewall.get("parent_action_changed") is False
        and firewall.get("child_action_frozen") is False
        and firewall.get("X4-S4_action_frozen") is False
        and firewall.get("compensator_selected") is False
        and firewall.get("warp_profile_selected") is False
        and firewall.get("global_sum_rule_derived") is False
        and firewall.get("localized_counterterms_normalized") is False
        and firewall.get("physical_hessian_constructed") is False
        and firewall.get("MAT001_pass") is False
        and firewall.get("K_Q_derived") is False
        and firewall.get("V_computed") is False
        and firewall.get("stage4A_reopened") is False
        and firewall.get("rule9_cleared") is False
        and firewall.get("physics_pass") is False
        and firewall.get("gate_effect") == "NONE"
    )


def mutation_suite(summary: dict[str, Any]) -> list[str]:
    if not exported_contract_valid(summary):
        raise AssertionError("baseline route handoff must be valid")

    mutants: list[tuple[str, dict[str, Any]]] = []

    child = copy.deepcopy(summary)
    child["status_firewall"]["child_action_frozen"] = True
    mutants.append(("child_action_frozen", child))

    parent = copy.deepcopy(summary)
    parent["status_firewall"]["X4-S4_action_frozen"] = True
    mutants.append(("x4_s4_action_frozen_without_contract", parent))

    compensator = copy.deepcopy(summary)
    compensator["status_firewall"]["compensator_selected"] = True
    mutants.append(("compensator_selected_without_field_content", compensator))

    warp = copy.deepcopy(summary)
    warp["status_firewall"]["warp_profile_selected"] = True
    mutants.append(("warp_profile_selected_without_equations", warp))

    changed = copy.deepcopy(summary)
    changed["route"]["parent_action_changed"] = True
    changed["status_firewall"]["parent_action_changed"] = True
    mutants.append(("x4_s2f3_parent_changed", changed))

    target = copy.deepcopy(summary)
    target["route"]["selected_from_observational_target"] = True
    mutants.append(("observational_target_selected_route", target))

    physics = copy.deepcopy(summary)
    physics["status_firewall"]["physics_pass"] = True
    mutants.append(("route_handoff_promoted_to_physics", physics))

    passed: list[str] = []
    for label, mutant in mutants:
        if exported_contract_valid(mutant):
            raise AssertionError(f"mutation must be rejected: {label}")
        passed.append(label)
    return passed


def render_report(summary: dict[str, Any], output_digest: str) -> str:
    checks = "\n".join(
        f"| {row['name']} | {'yes' if row['ok'] else 'no'} |"
        for row in summary["checks"]
    )
    mutations = "\n".join(
        f"- {label}: rejected" for label in summary["mutation_tests"]["labels"]
    )
    return f"""# MAT-001 TOP-X4 compensated or warped child-design handoff

**Executed:** 2026-09-17  
**Status:** {summary['status']}  
**Checks:** {summary['checks_passed']}/{summary['checks_total']}  
**Parent action changed:** false  
**Physics pass:** false  
**Gate effect:** NONE

## 1. Route handoff

The minimal unwarped single-tension brane child is rejected. The registered
brane-family continuation is a separately designed X4-S4 new parent:

    minimal_unwarped_single_tension_child=REJECTED
    smooth_S1_flux_repair=NO_DISTINCT_MINIMAL_ROUTE_REGISTERED
    brane_route=OPEN_ONLY_AS_X4-S4_NEW_PARENT_DESIGN
    child_action_freeze=NOT_AUTHORIZED
    X4-S4_action_freeze=NOT_AUTHORIZED

This is a route handoff only. No compensator, warp profile, field content or
new parent action has been selected.

## 2. Why X4-S4 is separate

The earlier stabilization audit records X4-S4 orbifold/brane fixed points as
a geometry-changing route requiring localized actions, counterterms and
junction conditions. It explicitly defers that route as a different parent.
The smooth X4-S3 one-dimensional flux candidate has no distinct minimal
internal flux repair registered. These findings prevent an unregistered
brane, second source or flux field from being inserted into X4-S2F3.

## 3. Required X4-S4 design inputs

Before freezing a new parent, the work must specify the manifold and
fixed-point/defect structure, all bulk and localized fields, induced metrics,
localized stress, radion source, junction and brane-bending equations, the
exact compact-space balance, localized renormalization and counterterms, and
a controlled finite-charge on-shell background. No desired a0, H0, SPARC
result or MAT coefficient may choose those ingredients.

## 4. Evidence checks

| Check | Satisfied |
|---|---|
{checks}

## 5. Rejection controls

{mutations}

All {summary['mutation_tests']['passed']}/{summary['mutation_tests']['total']}
registered mutations were rejected. This is local contract validation, not
independent Rule-9 review.

## 6. Next single gate

{summary['next_single_gate']['name']}: freeze a complete X4-S4 new-parent
action contract only after choosing its field content and deriving its
localized/global equations. Stop before changing X4-S2F3.

## 7. Artifact record

- JSON: {relative(OUTPUT_PATH)}
- JSON SHA-256: {output_digest}
- contract: {relative(CONTRACT_PATH)}
- executable: {relative(Path(__file__))}

## 8. Binding boundary

    route_handoff_status=COMPLETE_NON_PROMOTING
    minimal_unwarped_single_tension_child=REJECTED
    smooth_S1_flux_repair=NOT_REGISTERED_AS_DISTINCT_ROUTE
    brane_route=OPEN_ONLY_AS_X4-S4_NEW_PARENT_DESIGN
    parent_action_changed=false
    child_action_freeze=NOT_AUTHORIZED
    X4-S4_action_freeze=NOT_AUTHORIZED
    global_sum_rule=NOT_DERIVED_FOR_X4-S4
    localized_counterterms=NOT_NORMALIZED
    physical_hessian=NOT_CONSTRUCTED
    MAT-001=BLOCKED
    K_Q=NOT_DERIVED
    V=NOT_COMPUTED
    Stage4A=CLOSED
    physics_pass=false
    gate_effect=NONE
"""


def main() -> int:
    args = parse_args()
    write_sidecar(Path(__file__))
    write_sidecar(CONTRACT_PATH)

    source_specs = [
        (Path(__file__), True),
        (CONTRACT_PATH, True),
        (DECISION_SUMMARY_PATH, True),
        (S0_AUDIT_PATH, True),
        (PARENT_FREEZE_PATH, True),
        (A1_LEDGER_PATH, True),
        (ARCH_SUMMARY_PATH, True),
        (BRIDGE_SUMMARY_PATH, True),
        (A2A3_SUMMARY_PATH, True),
        (HESSIAN_SUMMARY_PATH, True),
    ]
    receipts = [
        artifact_receipt(path, sidecar_required=required)
        for path, required in source_specs
    ]
    summary = build_summary(receipts)
    if not exported_contract_valid(summary):
        print(ERROR_STATUS)
        print(f"checks={summary['checks_passed']}/{summary['checks_total']}")
        for row in summary["checks"]:
            if not row["ok"]:
                print(f"FAILED_CHECK={row['name']}")
        return 1

    labels = mutation_suite(summary)
    summary["mutation_tests"] = {
        "passed": len(labels),
        "total": len(labels),
        "labels": labels,
    }
    summary["script_sha256"] = sha256_file(Path(__file__))
    summary["contract_sha256"] = sha256_file(CONTRACT_PATH)

    if args.self_test_mutations:
        print(f"MUTATION_SUITE: {len(labels)}/{len(labels)}")
        for label in labels:
            print(f"  REJECTED: {label}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = (
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")
    args.output.write_bytes(payload)
    output_digest = hashlib.sha256(payload).hexdigest()
    write_sidecar(args.output, replace_suffix=True)

    report = render_report(summary, output_digest)
    args.report.write_text(report, encoding="utf-8", newline="\n")
    write_sidecar(args.report)

    print(summary["status"])
    print(f"checks={summary['checks_passed']}/{summary['checks_total']}")
    print(f"mutation_tests={len(labels)}/{len(labels)}")
    print(f"minimal_child={summary['route']['minimal_unwarped_single_tension_child']}")
    print(f"brane_route={summary['route']['brane_route']}")
    print("child_action_freeze=NOT_AUTHORIZED")
    print("X4-S4_action_freeze=NOT_AUTHORIZED")
    print("parent_action_changed=false")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={args.output}")
    print(f"output_sha256={output_digest}")
    print(f"report={args.report}")
    print(f"report_sha256={sha256_file(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
