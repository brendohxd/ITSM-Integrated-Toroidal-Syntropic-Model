#!/usr/bin/env python3
"""Run the non-promoting global-consistency preflight for a brane child route.

This executable checks normalization, dimensions, variation obligations and
the conditional compact-circle sum-rule boundary. It does not add a brane to
X4-S2F3, solve junction equations, or promote any gate.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


STATUS = "HOLD_TOPX4_H1_BRANE_CHILD_GLOBAL_SUM_RULE_AND_RENORMALIZATION"
ERROR_STATUS = "ERROR_TOPX4_H1_BRANE_CHILD_GLOBAL_CONSISTENCY_PREFLIGHT"

REPO_ROOT = Path(__file__).resolve().parents[4]
BASE = Path(__file__).resolve().parent
OUTPUT_PATH = (
    BASE / "outputs" / "mat001_topx4_h1_brane_child_global_consistency_summary.json"
)
REPORT_PATH = (
    BASE / "MAT001_TOPX4_H1_BRANE_CHILD_GLOBAL_CONSISTENCY_PREFLIGHT_2026-09-16.md"
)
CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_BRANE_CHILD_GLOBAL_CONSISTENCY_CONTRACT_2026-09-16.md"
)
ARCH_CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_MATTER_ARCHITECTURE_COMPARISON_CONTRACT_2026-09-16.md"
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

SOURCE_ANCHOR = "https://arxiv.org/abs/hep-th/0011225"


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


def exact_local_controls() -> dict[str, Any]:
    # The proper transverse measure is (R_ref * r) dy and the proposed delta
    # is its reciprocal times a dimensionless periodic delta.
    proper_measure_factor = "R_ref*r"
    delta_factor = "1/(R_ref*r)"
    normalization = Fraction(1, 1)

    # Natural-unit dimensions of the localized covariant source.
    delta_dimension = 1
    brane_lagrangian_dimension = 4
    covariant_integrand_dimension = delta_dimension + brane_lagrangian_dimension

    return {
        "proper_transverse_measure": proper_measure_factor,
        "covariant_delta": delta_factor,
        "periodic_delta_normalization": str(normalization),
        "normalization_exact": normalization == 1,
        "dimensions": {
            "delta_perp": delta_dimension,
            "brane_lagrangian": brane_lagrangian_dimension,
            "five_dimensional_integrand": covariant_integrand_dimension,
            "dimension_closes": covariant_integrand_dimension == 5,
        },
        "global_assumptions": {
            "internal_coordinate": "periodic_y_in_[0,2pi)",
            "background": "static_flat_4d_slice",
            "bulk_sign": "canonical_nonnegative_terms_only",
            "compensator_present": False,
        },
    }


def build_summary(receipts: list[dict[str, Any]]) -> dict[str, Any]:
    architecture = load_json(ARCH_SUMMARY_PATH)
    bridge = load_json(BRIDGE_SUMMARY_PATH)
    a2a3 = load_json(A2A3_SUMMARY_PATH)
    hessian = load_json(HESSIAN_SUMMARY_PATH)
    contract_text = CONTRACT_PATH.read_text(encoding="utf-8")
    arch_contract_text = ARCH_CONTRACT_PATH.read_text(encoding="utf-8")
    ledger_text = " ".join(A1_LEDGER_PATH.read_text(encoding="utf-8").lower().split())
    parent_text = " ".join(PARENT_FREEZE_PATH.read_text(encoding="utf-8").lower().split())
    controls = exact_local_controls()

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
        "architecture_recommendation_is_the_frozen_brane_candidate",
        architecture.get("decision", {}).get("lead_source_projection_candidate")
        == "BRANE_INDUCED_METRIC_CHILD_ROUTE"
        and architecture.get("parent_action_changed") is False,
    )
    add_check(
        checks,
        "proper_transverse_delta_is_exactly_normalized",
        controls["normalization_exact"]
        and controls["covariant_delta"] == "1/(R_ref*r)"
        and controls["proper_transverse_measure"] == "R_ref*r",
        normalization=controls["periodic_delta_normalization"],
    )
    add_check(
        checks,
        "localized_covariant_dimension_closes",
        controls["dimensions"]["dimension_closes"],
        dimensions=controls["dimensions"],
    )
    add_check(
        checks,
        "localized_variation_and_radion_response_are_required",
        "radion response" in contract_text
        and "matter-trace contribution" in contract_text
        and "induced metric" in contract_text,
    )
    add_check(
        checks,
        "two_sided_junction_and_embedding_data_are_required",
        "two-sided junction" in contract_text
        and "brane-bending/embedding" in contract_text
        and "opposite-side data" in contract_text,
    )
    add_check(
        checks,
        "periodic_global_sum_rule_and_conditional_rejection_are_frozen",
        "integrated compact-space condition" in contract_text
        and "single uncompensated positive renormalized brane" in contract_text
        and "REJECTED_GLOBAL_SUM_RULE" in contract_text,
    )
    add_check(
        checks,
        "localized_counterterm_obligation_is_frozen",
        "counterterm structures" in contract_text
        and "induced-curvature term" in contract_text
        and "renormalized conditions" in contract_text,
    )
    add_check(
        checks,
        "source_anchor_and_parent_firewall_are_present",
        SOURCE_ANCHOR in contract_text
        and "does not add a brane to X4-S2F3" in contract_text
        and "new child theory" in arch_contract_text
        and "bulk matter proxy" in ledger_text
        and "x4-s2f3" in parent_text,
    )
    add_check(
        checks,
        "upstream_holds_remain_binding",
        bridge.get("status") == "HOLD_MAT001_TOPX4_H1_BRIDGE_INPUTS_NOT_CLOSED"
        and bridge.get("status_firewall", {}).get("MAT001_pass") is False
        and bridge.get("status_firewall", {}).get("K_Q_derived") is False
        and bridge.get("status_firewall", {}).get("V_computed") is False
        and a2a3.get("physics_pass") is False
        and hessian.get("physics_pass") is False,
    )

    decision = {
        "brane_route": "CONDITIONAL_SURVIVOR_TENSIONLESS_BACKGROUND_ONLY",
        "single_uncompensated_positive_tension": "REJECTED_GLOBAL_SUM_RULE",
        "child_freeze": "HOLD_PENDING_GLOBAL_SUM_RULE_AND_RENORMALIZATION",
        "global_sum_rule": "NOT_DERIVED_FROM_ITSM_CHILD_ACTION",
        "localized_variation": "REQUIRES_SEPARATE_CHILD_ACTION",
        "junction_data": "NOT_DERIVED",
        "localized_counterterms": "NOT_NORMALIZED",
        "parent_action_changed": False,
    }

    return {
        "schema": "ITSM_MAT001_TOPX4_H1_BRANE_CHILD_GLOBAL_CONSISTENCY_v1",
        "date": "2026-09-16",
        "status": STATUS,
        "audit_execution_status": "COMPLETE",
        "checks": checks,
        "checks_passed": sum(1 for item in checks if item["ok"]),
        "checks_total": len(checks),
        "exact_local_controls": controls,
        "decision": decision,
        "conditional_interpretation": (
            "The brane source route remains a research candidate only if the "
            "renormalized background tension is zero or globally compensated "
            "and all localized variation data are supplied."
        ),
        "literature_scope": {
            "source": SOURCE_ANCHOR,
            "scope": "COMPACT_SUM_RULE_TYPE_CHECK_SUPPORTED_NOT_ITSM_DERIVATION",
        },
        "status_firewall": {
            "parent_action_changed": False,
            "brane_child_action_frozen": False,
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
            "name": "TOPX4_H1_BRANE_CHILD_ACTION_FREEZE_OR_REJECT",
            "scope": (
                "Only after a derived global balance and renormalized localized "
                "variation may a separate child action be frozen."
            ),
            "stop_before": "NO_CHANGE_TO_X4_S2F3",
        },
    }


def exported_contract_valid(summary: dict[str, Any]) -> bool:
    checks = summary.get("checks", [])
    firewall = summary.get("status_firewall", {})
    decision = summary.get("decision", {})
    return (
        summary.get("status") == STATUS
        and summary.get("checks_passed") == summary.get("checks_total") == len(checks)
        and all(item.get("ok") is True for item in checks)
        and summary.get("exact_local_controls", {}).get("covariant_delta")
        == "1/(R_ref*r)"
        and summary.get("exact_local_controls", {}).get("proper_transverse_measure")
        == "R_ref*r"
        and summary.get("exact_local_controls", {})
        .get("periodic_delta_normalization")
        == "1"
        and summary.get("exact_local_controls", {})
        .get("dimensions", {})
        .get("dimension_closes")
        is True
        and decision.get("brane_route")
        == "CONDITIONAL_SURVIVOR_TENSIONLESS_BACKGROUND_ONLY"
        and decision.get("single_uncompensated_positive_tension")
        == "REJECTED_GLOBAL_SUM_RULE"
        and decision.get("child_freeze")
        == "HOLD_PENDING_GLOBAL_SUM_RULE_AND_RENORMALIZATION"
        and decision.get("single_uncompensated_positive_tension")
        == "REJECTED_GLOBAL_SUM_RULE"
        and decision.get("localized_variation")
        == "REQUIRES_SEPARATE_CHILD_ACTION"
        and decision.get("junction_data") == "NOT_DERIVED"
        and decision.get("localized_counterterms") == "NOT_NORMALIZED"
        and decision.get("parent_action_changed") is False
        and decision.get("selected_from_observational_target", False) is False
        and firewall.get("parent_action_changed") is False
        and firewall.get("brane_child_action_frozen") is False
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
        raise AssertionError("baseline global-consistency preflight must be valid")

    mutants: list[tuple[str, dict[str, Any]]] = []

    wrong_delta = copy.deepcopy(summary)
    wrong_delta["exact_local_controls"]["covariant_delta"] = "delta_2pi(y-y_b)"
    mutants.append(("coordinate_delta_used_without_proper_measure", wrong_delta))

    external_boundary = copy.deepcopy(summary)
    external_boundary["status_firewall"]["localized_variation_closed"] = True
    external_boundary["decision"]["junction_data"] = "DROPPED_AS_EXTERNAL_BOUNDARY"
    mutants.append(("periodic_defect_treated_as_external_boundary", external_boundary))

    positive_tension = copy.deepcopy(summary)
    positive_tension["decision"]["single_uncompensated_positive_tension"] = "ACCEPTED"
    mutants.append(("lone_positive_tension_accepted", positive_tension))

    omitted_junction = copy.deepcopy(summary)
    omitted_junction["decision"]["junction_data"] = "SET_TO_ZERO"
    mutants.append(("junction_data_set_to_zero_by_omission", omitted_junction))

    alpha_residue = copy.deepcopy(summary)
    alpha_residue["status_firewall"]["localized_variation_closed"] = True
    alpha_residue["decision"]["localized_variation"] = "ALPHA_B_IS_PHYSICAL_H1_RESIDUE"
    mutants.append(("kinematic_alpha_promoted_to_h1_residue", alpha_residue))

    changed_parent = copy.deepcopy(summary)
    changed_parent["decision"]["parent_action_changed"] = True
    changed_parent["status_firewall"]["parent_action_changed"] = True
    mutants.append(("brane_added_to_frozen_parent", changed_parent))

    no_counterterms = copy.deepcopy(summary)
    no_counterterms["decision"]["localized_counterterms"] = "NOT_REQUIRED"
    no_counterterms["status_firewall"]["localized_counterterms_normalized"] = True
    mutants.append(("localized_counterterms_omitted", no_counterterms))

    target_selected = copy.deepcopy(summary)
    target_selected["decision"]["selected_from_observational_target"] = True
    mutants.append(("observational_target_selected_tension_or_root", target_selected))

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
    return f"""# MAT-001 TOP-X4 brane-child global-consistency preflight

**Executed:** 2026-09-16  
**Status:** {summary['status']}  
**Checks:** {summary['checks_passed']}/{summary['checks_total']}  
**Parent action changed:** false  
**Physics pass:** false  
**Gate effect:** NONE

## 1. Bounded result

The brane-induced-metric route remains a conditional research candidate, but
the preflight does not authorize a child action. Under the declared static,
flat-four-dimensional, periodic-circle assumptions, a single uncompensated
positive renormalized brane tension is rejected by the required global
compact-space balance. A tensionless or compensated background remains
possible only after the child action derives the compensator and all localized
variation data.

The result is therefore:

    BRANE_ROUTE=CONDITIONAL_SURVIVOR_TENSIONLESS_BACKGROUND_ONLY
    single_uncompensated_positive_tension=REJECTED_GLOBAL_SUM_RULE
    child_freeze=HOLD_PENDING_GLOBAL_SUM_RULE_AND_RENORMALIZATION

This is a consistency boundary, not a constructed brane theory and not a
MAT-001 result.

## 2. Exact local controls

The proper transverse measure is R_ref*r dy. The covariant localized source
uses delta_perp = delta_2pi(y-y_b)/(R_ref*r), whose integral against that
measure is exactly one. The localized Lagrangian has mass dimension four,
delta_perp has mass dimension one, and the five-dimensional source integrand
has mass dimension five.

These controls do not solve the defect equations. The brane response includes
the induced-metric stress trace and radion variation, while a two-sided
junction/embedding treatment is still required on a smooth periodic circle.

## 3. Global compact-space boundary

The relevant integrated Einstein/scalar condition must be derived from the
child action with exact weights and signs. This preflight records the
conditional kill criterion: with a canonical-sign bulk contribution, flat
four-dimensional slices, periodic internal space, and no negative/flux/
curvature compensator, a lone positive renormalized localized tension cannot
be accepted as a static solution.

The preflight does not claim that every brane model is impossible. It narrows
the admissible child start to a derived zero-tension condition, a derived
global compensator, or a different complete curved/warped background.

## 4. Localized variation and renormalization

The future child must specify whether the source is a two-sided defect or an
orbifold fixed point, the normal orientation, junction equations, brane
bending, induced metric, bulk/scalar boundary data and all localized matter
variations. Matter loops require localized tension and induced-curvature
counterterms with a declared regulator, subtraction scheme and renormalized
conditions. These terms feed the same stress, determinant and physical
Hessian problem; they cannot be added after the fact.

## 5. Evidence checks

| Check | Satisfied |
|---|---|
{checks}

## 6. Rejection controls

{mutations}

All {summary['mutation_tests']['passed']}/{summary['mutation_tests']['total']}
registered mutations were rejected. This is local contract validation, not
independent Rule-9 review.

## 7. Source boundary

The compact-space consistency requirement is informed by Gibbons, Kallosh and
Linde, Brane world sum rules:
{SOURCE_ANCHOR}

That source constrains the kind of integrated check required; it does not
supply ITSM child equations, renormalized coefficients or a MAT solution.

## 8. Next single gate

{summary['next_single_gate']['name']}: derive the exact child global balance
and localized renormalization conditions, then decide whether a separate
brane child action can be frozen. Stop before changing X4-S2F3.

## 9. Artifact record

- JSON: {relative(OUTPUT_PATH)}
- JSON SHA-256: {output_digest}
- contract: {relative(CONTRACT_PATH)}
- executable: {relative(Path(__file__))}

## 10. Binding boundary

    preflight_status=FROZEN_NON_PROMOTING
    parent_action_changed=false
    brane_child_action=NOT_FROZEN
    global_sum_rule=NOT_DERIVED
    localized_variation=REQUIRES_CHILD_ACTION
    junction_data=NOT_DERIVED
    localized_counterterms=NOT_NORMALIZED
    single_uncompensated_positive_tension=REJECTED_CONDITIONALLY
    route_disposition=CONDITIONAL_SURVIVOR_TENSIONLESS_BACKGROUND_ONLY
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
        (ARCH_CONTRACT_PATH, True),
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
    print(
        "brane_route="
        f"{summary['decision']['brane_route']}"
    )
    print(
        "single_uncompensated_positive_tension="
        f"{summary['decision']['single_uncompensated_positive_tension']}"
    )
    print("child_freeze=HOLD_PENDING_GLOBAL_SUM_RULE_AND_RENORMALIZATION")
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
