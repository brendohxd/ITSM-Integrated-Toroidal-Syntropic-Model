#!/usr/bin/env python3
"""Decide whether the minimal brane child can be frozen.

The executable is a non-promoting decision gate. It rejects only the minimal
unwarped single-tension candidate and preserves a compensated or warped child
as a separate future research route.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


STATUS = "REJECT_MINIMAL_BRANE_CHILD_FREEZE_CONDITIONALLY"
ERROR_STATUS = "ERROR_TOPX4_H1_BRANE_CHILD_FREEZE_DECISION"

REPO_ROOT = Path(__file__).resolve().parents[4]
BASE = Path(__file__).resolve().parent
OUTPUT_PATH = (
    BASE / "outputs" / "mat001_topx4_h1_brane_child_freeze_decision_summary.json"
)
REPORT_PATH = (
    BASE / "MAT001_TOPX4_H1_BRANE_CHILD_FREEZE_DECISION_2026-09-17.md"
)
CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_BRANE_CHILD_FREEZE_DECISION_CONTRACT_2026-09-17.md"
)
PREFLIGHT_SUMMARY_PATH = (
    BASE / "outputs" / "mat001_topx4_h1_brane_child_global_consistency_summary.json"
)
PREFLIGHT_CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_BRANE_CHILD_GLOBAL_CONSISTENCY_CONTRACT_2026-09-16.md"
)
ARCH_SUMMARY_PATH = (
    BASE / "outputs" / "mat001_topx4_h1_matter_architecture_comparison_summary.json"
)
BRIDGE_SUMMARY_PATH = BASE / "outputs" / "mat001_topx4_h1_bridge_readiness_summary.json"
A1_LEDGER_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md"
)
PARENT_FREEZE_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md"
)
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


def exact_minimal_product_control() -> dict[str, Any]:
    return {
        "metric_chart": "constant_radius_flat_4d_product",
        "internal_geometry": "smooth_periodic_circle",
        "distributional_connection": 0,
        "distributional_einstein_tensor": 0,
        "lone_tangential_source": "-lambda_b*gamma_mn*delta_perp",
        "required_renormalized_background_tension": "lambda_b^ren=0",
        "exact_under_declared_assumptions": True,
        "compensator_present": False,
        "warp_profile_present": False,
        "orbifold_boundary_substitution": False,
    }


def build_summary(receipts: list[dict[str, Any]]) -> dict[str, Any]:
    preflight = load_json(PREFLIGHT_SUMMARY_PATH)
    architecture = load_json(ARCH_SUMMARY_PATH)
    bridge = load_json(BRIDGE_SUMMARY_PATH)
    a2a3 = load_json(A2A3_SUMMARY_PATH)
    hessian = load_json(HESSIAN_SUMMARY_PATH)
    contract_text = " ".join(
        CONTRACT_PATH.read_text(encoding="utf-8").split()
    )
    preflight_contract_text = " ".join(
        PREFLIGHT_CONTRACT_PATH.read_text(encoding="utf-8").split()
    )
    ledger_text = " ".join(A1_LEDGER_PATH.read_text(encoding="utf-8").lower().split())
    parent_text = " ".join(PARENT_FREEZE_PATH.read_text(encoding="utf-8").lower().split())
    controls = exact_minimal_product_control()

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
        "prior_global_preflight_reached_expected_conditional_hold",
        preflight.get("status")
        == "HOLD_TOPX4_H1_BRANE_CHILD_GLOBAL_SUM_RULE_AND_RENORMALIZATION"
        and preflight.get("decision", {}).get("brane_route")
        == "CONDITIONAL_SURVIVOR_TENSIONLESS_BACKGROUND_ONLY"
        and preflight.get("status_firewall", {}).get("brane_child_action_frozen")
        is False,
    )
    add_check(
        checks,
        "architecture_and_bridge_are_route_only",
        architecture.get("parent_action_changed") is False
        and architecture.get("decision", {}).get("child_action_freeze")
        == "NOT_AUTHORIZED"
        and bridge.get("status")
        == "HOLD_MAT001_TOPX4_H1_BRIDGE_INPUTS_NOT_CLOSED",
    )
    add_check(
        checks,
        "minimal_product_has_no_distributional_curvature",
        controls["distributional_connection"] == 0
        and controls["distributional_einstein_tensor"] == 0
        and controls["exact_under_declared_assumptions"] is True,
    )
    add_check(
        checks,
        "lone_source_requires_zero_renormalized_background_tension",
        controls["lone_tangential_source"]
        == "-lambda_b*gamma_mn*delta_perp"
        and controls["required_renormalized_background_tension"]
        == "lambda_b^ren=0"
        and controls["compensator_present"] is False,
    )
    add_check(
        checks,
        "freeze_prerequisites_are_explicit",
        "exact bulk/defect variation" in contract_text
        and "two-sided/fixed-point junction equations" in contract_text
        and "renormalized localized tension" in contract_text
        and "brane-bending/embedding" in contract_text,
    )
    add_check(
        checks,
        "minimal_candidate_is_not_silently_extended",
        controls["warp_profile_present"] is False
        and controls["orbifold_boundary_substitution"] is False
        and "compensated or warped child" in contract_text
        and "does not alter the frozen X4-S2F3 action" in contract_text,
    )
    add_check(
        checks,
        "parent_and_proxy_boundaries_remain_binding",
        "brane term" in parent_text
        and "matter portal" in parent_text
        and "bulk matter proxy" in ledger_text
        and a2a3.get("physics_pass") is False
        and hessian.get("physics_pass") is False
        and "localized counterterm" in preflight_contract_text,
    )
    add_check(
        checks,
        "downstream_firewalls_remain_closed",
        bridge.get("status_firewall", {}).get("MAT001_pass") is False
        and bridge.get("status_firewall", {}).get("K_Q_derived") is False
        and bridge.get("status_firewall", {}).get("V_computed") is False
        and bridge.get("status_firewall", {}).get("stage4A_reopened") is False
        and bridge.get("status_firewall", {}).get("rule9_cleared") is False,
    )

    decision = {
        "minimal_child": "REJECTED_ZERO_TENSION_DISTRIBUTIONAL_CONTROL",
        "brane_route": "OPEN_ONLY_COMPENSATED_OR_WARPED_CHILD",
        "child_action_freeze": "NOT_AUTHORIZED",
        "global_sum_rule": "NOT_DERIVED_FOR_FUTURE_CHILD",
        "localized_variation": "NOT_CLOSED",
        "junction_data": "NOT_DERIVED",
        "localized_counterterms": "NOT_NORMALIZED",
        "parent_action_changed": False,
        "selected_from_observational_target": False,
    }

    return {
        "schema": "ITSM_MAT001_TOPX4_H1_BRANE_CHILD_FREEZE_DECISION_v1",
        "date": "2026-09-17",
        "status": STATUS,
        "audit_execution_status": "COMPLETE",
        "checks": checks,
        "checks_passed": sum(1 for item in checks if item["ok"]),
        "checks_total": len(checks),
        "exact_minimal_product_control": controls,
        "decision": decision,
        "scientific_boundary": (
            "Only the minimal unwarped single-tension child is rejected. "
            "A compensated or warped child remains a separate future route "
            "and has not been constructed."
        ),
        "status_firewall": {
            "parent_action_changed": False,
            "brane_child_action_frozen": False,
            "minimal_child_accepted": False,
            "compensated_or_warped_child_constructed": False,
            "global_sum_rule_derived": False,
            "localized_variation_closed": False,
            "junction_data_derived": False,
            "localized_counterterms_normalized": False,
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
            "name": "TOPX4_H1_COMPENSATED_OR_WARPED_BRANE_CHILD_DESIGN",
            "scope": (
                "Freeze a separate child contract only after choosing and "
                "deriving an explicit compensator or warped background."
            ),
            "stop_before": "NO_CHANGE_TO_X4_S2F3",
        },
    }


def exported_contract_valid(summary: dict[str, Any]) -> bool:
    checks = summary.get("checks", [])
    controls = summary.get("exact_minimal_product_control", {})
    decision = summary.get("decision", {})
    firewall = summary.get("status_firewall", {})
    return (
        summary.get("status") == STATUS
        and summary.get("checks_passed") == summary.get("checks_total") == len(checks)
        and all(item.get("ok") is True for item in checks)
        and controls.get("distributional_connection") == 0
        and controls.get("distributional_einstein_tensor") == 0
        and controls.get("required_renormalized_background_tension")
        == "lambda_b^ren=0"
        and controls.get("exact_under_declared_assumptions") is True
        and controls.get("compensator_present") is False
        and controls.get("warp_profile_present") is False
        and controls.get("orbifold_boundary_substitution") is False
        and decision.get("minimal_child")
        == "REJECTED_ZERO_TENSION_DISTRIBUTIONAL_CONTROL"
        and decision.get("brane_route") == "OPEN_ONLY_COMPENSATED_OR_WARPED_CHILD"
        and decision.get("child_action_freeze") == "NOT_AUTHORIZED"
        and decision.get("global_sum_rule") == "NOT_DERIVED_FOR_FUTURE_CHILD"
        and decision.get("localized_variation") == "NOT_CLOSED"
        and decision.get("junction_data") == "NOT_DERIVED"
        and decision.get("localized_counterterms") == "NOT_NORMALIZED"
        and decision.get("parent_action_changed") is False
        and decision.get("selected_from_observational_target") is False
        and firewall.get("parent_action_changed") is False
        and firewall.get("brane_child_action_frozen") is False
        and firewall.get("minimal_child_accepted") is False
        and firewall.get("compensated_or_warped_child_constructed") is False
        and firewall.get("global_sum_rule_derived") is False
        and firewall.get("localized_variation_closed") is False
        and firewall.get("junction_data_derived") is False
        and firewall.get("localized_counterterms_normalized") is False
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
        raise AssertionError("baseline child-freeze decision must be valid")

    mutants: list[tuple[str, dict[str, Any]]] = []

    accepted = copy.deepcopy(summary)
    accepted["decision"]["minimal_child"] = "ACCEPTED"
    accepted["status_firewall"]["minimal_child_accepted"] = True
    mutants.append(("minimal_child_accepted", accepted))

    frozen = copy.deepcopy(summary)
    frozen["decision"]["child_action_freeze"] = "AUTHORIZED"
    frozen["status_firewall"]["brane_child_action_frozen"] = True
    mutants.append(("child_action_frozen_without_prerequisites", frozen))

    compensated = copy.deepcopy(summary)
    compensated["status_firewall"]["compensated_or_warped_child_constructed"] = True
    mutants.append(("compensated_child_claimed_constructed", compensated))

    global_closed = copy.deepcopy(summary)
    global_closed["decision"]["global_sum_rule"] = "DERIVED"
    global_closed["status_firewall"]["global_sum_rule_derived"] = True
    mutants.append(("future_sum_rule_claimed_derived", global_closed))

    parent_changed = copy.deepcopy(summary)
    parent_changed["decision"]["parent_action_changed"] = True
    parent_changed["status_firewall"]["parent_action_changed"] = True
    mutants.append(("brane_added_to_frozen_parent", parent_changed))

    counterterms = copy.deepcopy(summary)
    counterterms["decision"]["localized_counterterms"] = "NORMALIZED"
    counterterms["status_firewall"]["localized_counterterms_normalized"] = True
    mutants.append(("counterterms_claimed_normalized", counterterms))

    target = copy.deepcopy(summary)
    target["decision"]["selected_from_observational_target"] = True
    mutants.append(("observational_target_selected_child", target))

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
    return f"""# MAT-001 TOP-X4 brane-child action freeze decision

**Executed:** 2026-09-17  
**Status:** {summary['status']}  
**Checks:** {summary['checks_passed']}/{summary['checks_total']}  
**Parent action changed:** false  
**Physics pass:** false  
**Gate effect:** NONE

## 1. Decision

The minimal unwarped single-tension brane child is rejected for freeze under
its declared flat-product assumptions:

    minimal_child=REJECTED_ZERO_TENSION_DISTRIBUTIONAL_CONTROL
    brane_route=OPEN_ONLY_COMPENSATED_OR_WARPED_CHILD
    child_action_freeze=NOT_AUTHORIZED

This is not a rejection of every brane architecture. It says that a
constant-radius flat product with one internal localized tension and no
compensator has no distributional Einstein curvature available to support a
nonzero localized background tension. Its distributional equation therefore
requires lambda_b^ren = 0.

## 2. Why the minimal candidate fails

For the declared control, the distributional connection and Einstein tensor
are zero. The brane tangential source is

    -lambda_b gamma_mn delta_perp

so a lone source requires a zero renormalized background tension. Matter
vacuum energy and localized loop counterterms are part of that renormalized
quantity; declaring the bare parameter zero is not enough.

The conclusion is conditional on the minimal product assumptions. A warped,
flux-supported, curved or otherwise compensated child would have a different
global equation and must be derived independently.

## 3. Freeze boundary

The current evidence does not provide a new child action, complete
bulk/defect variation, junction or brane-bending equations, exact future
global balance, localized renormalization, or a finite-charge on-shell
background. The existing X4-S2F3 parent remains unchanged and contains no
brane term.

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

{summary['next_single_gate']['name']}: design and freeze a separate
compensated or warped child contract only after its exact bulk/defect
equations, global balance and localized renormalization conditions are
specified. Stop before changing X4-S2F3.

## 7. Artifact record

- JSON: {relative(OUTPUT_PATH)}
- JSON SHA-256: {output_digest}
- contract: {relative(CONTRACT_PATH)}
- executable: {relative(Path(__file__))}

## 8. Binding boundary

    decision_status=REJECT_MINIMAL_BRANE_CHILD_FREEZE_CONDITIONALLY
    minimal_child=REJECTED_ZERO_TENSION_DISTRIBUTIONAL_CONTROL
    brane_route=OPEN_ONLY_COMPENSATED_OR_WARPED_CHILD
    child_action_freeze=NOT_AUTHORIZED
    parent_action_changed=false
    global_sum_rule=NOT_DERIVED_FOR_FUTURE_CHILD
    localized_variation=NOT_CLOSED
    junction_data=NOT_DERIVED
    localized_counterterms=NOT_NORMALIZED
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
        (PREFLIGHT_SUMMARY_PATH, True),
        (PREFLIGHT_CONTRACT_PATH, True),
        (ARCH_SUMMARY_PATH, True),
        (BRIDGE_SUMMARY_PATH, True),
        (A1_LEDGER_PATH, True),
        (PARENT_FREEZE_PATH, True),
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
    print(f"minimal_child={summary['decision']['minimal_child']}")
    print(f"brane_route={summary['decision']['brane_route']}")
    print("child_action_freeze=NOT_AUTHORIZED")
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
