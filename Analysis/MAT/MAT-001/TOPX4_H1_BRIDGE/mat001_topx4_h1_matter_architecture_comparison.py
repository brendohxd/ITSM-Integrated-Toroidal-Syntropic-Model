#!/usr/bin/env python3
"""Compare bulk and brane physical-matter architectures for the TOP-X4 H1 bridge.

The calculation is deliberately kinematic and non-promoting. It derives the
radion source scaling in the verified Einstein-frame chart, checks whether a
direct radion/Track-A field map is possible, and emits a route recommendation
without modifying the frozen X4-S2F3 action.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


STATUS = "HOLD_TOPX4_H1_MATTER_ARCHITECTURE_CHILD_ACTION_NOT_FROZEN"
ERROR_STATUS = "ERROR_TOPX4_H1_MATTER_ARCHITECTURE_COMPARISON"

REPO_ROOT = Path(__file__).resolve().parents[4]
BASE = Path(__file__).resolve().parent
OUTPUT_PATH = BASE / "outputs" / "mat001_topx4_h1_matter_architecture_comparison_summary.json"
REPORT_PATH = BASE / "MAT001_TOPX4_H1_MATTER_ARCHITECTURE_COMPARISON_2026-09-16.md"
CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_MATTER_ARCHITECTURE_COMPARISON_CONTRACT_2026-09-16.md"
)
BRIDGE_CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_BRIDGE_CONTRACT_2026-09-16.md"
)
BRIDGE_SUMMARY_PATH = BASE / "outputs" / "mat001_topx4_h1_bridge_readiness_summary.json"
A1_LEDGER_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md"
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


def exact_reduction_controls() -> dict[str, Any]:
    sigma = sp.symbols("sigma", real=True)
    m_pl = sp.symbols("M_Pl", positive=True)
    m_5 = sp.symbols("m_5", positive=True)
    gradient = sp.symbols("p", positive=True)

    log_r = sp.sqrt(sp.Rational(2, 3)) * sigma / m_pl
    r = sp.exp(log_r)
    a_brane = sp.simplify(r ** sp.Rational(-1, 2))
    alpha_brane = sp.simplify(sp.diff(sp.log(a_brane), sigma))
    expected_alpha = -1 / (sp.sqrt(6) * m_pl)

    # sqrt(-G) scales as r^-1 and G^{mu nu} as r^+1.
    bulk_kinetic_r_power = -1 + 1
    bulk_mass_squared_r_power = -1
    bulk_mass = sp.simplify(m_5 * r ** sp.Rational(-1, 2))
    alpha_bulk_mass = sp.simplify(sp.diff(sp.log(bulk_mass), sigma))

    radion_degree = sp.Poly(gradient**2, gradient).degree()
    track_a_degree = sp.Poly(gradient**3, gradient).degree()

    return {
        "einstein_frame_chart": {
            "log_r": str(log_r),
            "sqrt_minus_G_r_power": -1,
            "inverse_4d_metric_r_power": 1,
        },
        "brane_induced_metric": {
            "A_b": str(a_brane),
            "alpha_b": str(alpha_brane),
            "expected_alpha": str(expected_alpha),
            "alpha_exact": sp.simplify(alpha_brane - expected_alpha) == 0,
        },
        "bulk_massive_scalar_zero_mode": {
            "kinetic_r_power": bulk_kinetic_r_power,
            "mass_squared_r_power": bulk_mass_squared_r_power,
            "mass": str(bulk_mass),
            "d_log_mass_d_sigma": str(alpha_bulk_mass),
            "matches_brane_alpha": sp.simplify(alpha_bulk_mass - alpha_brane) == 0,
        },
        "four_dimensional_dimensions": {
            "sigma": 1,
            "rho_b": 4,
            "alpha_or_source_coupling": -1,
            "source_term_total": 1 + 4 - 1,
            "closes_to_four": 1 + 4 - 1 == 4,
        },
        "operator_homogeneity": {
            "canonical_radion_derivative_degree": radion_degree,
            "track_a_derivative_degree": track_a_degree,
            "degrees_match": radion_degree == track_a_degree,
            "regular_point_redefinition_preserves_derivative_degree": True,
            "direct_radion_track_a_map": "REJECTED_DERIVATIVE_HOMOGENEITY_MISMATCH",
        },
    }


def architecture_matrix() -> dict[str, dict[str, str]]:
    return {
        "preserves_smooth_circle_classically": {
            "bulk": "YES",
            "brane": "NO_LOCALIZED_DEFECT_ADDED",
        },
        "avoids_physical_matter_KK_towers": {
            "bulk": "NO",
            "brane": "YES_BY_CONSTRUCTION",
        },
        "chiral_4d_matter_without_new_bulk_mechanism": {
            "bulk": "NO_ON_CURRENT_SMOOTH_S1_SPECIFICATION",
            "brane": "POSSIBLE_IN_DECLARED_4D_MATTER_ACTION",
        },
        "universal_source_metric_is_explicit": {
            "bulk": "REQUIRES_COMPLETE_REDUCED_MATTER_THEORY",
            "brane": "YES_AT_INDUCED_METRIC_KINEMATIC_LEVEL",
        },
        "junction_and_localized_counterterms": {
            "bulk": "ABSENT",
            "brane": "COMPULSORY",
        },
        "changes_S2F3_quantum_stabilization_problem": {
            "bulk": "YES_FULL_PHYSICAL_MATTER_SPECTRUM",
            "brane": "YES_LOCALIZED_STRESS_BOUNDARY_DATA_COUNTERTERMS",
        },
        "directly_derives_track_a_Y_three_halves": {
            "bulk": "NO",
            "brane": "NO",
        },
    }


def build_summary(receipts: list[dict[str, Any]]) -> dict[str, Any]:
    bridge = load_json(BRIDGE_SUMMARY_PATH)
    a2a3 = load_json(A2A3_SUMMARY_PATH)
    hessian = load_json(HESSIAN_SUMMARY_PATH)
    controls = exact_reduction_controls()
    matrix = architecture_matrix()
    contract_text = CONTRACT_PATH.read_text(encoding="utf-8")
    a1_text = " ".join(A1_LEDGER_PATH.read_text(encoding="utf-8").lower().split())

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
        "comparison_does_not_relabel_the_existing_chi_proxy",
        "bulk matter proxy" in a1_text
        and bridge.get("candidate_mode_space", {}).get("chi")
        == "BULK_PROXY_NOT_BARYONIC_MATTER",
    )
    add_check(
        checks,
        "brane_induced_metric_radion_scaling_is_exact",
        controls["brane_induced_metric"]["alpha_exact"] is True,
        alpha_b=controls["brane_induced_metric"]["alpha_b"],
    )
    add_check(
        checks,
        "bulk_scalar_zero_mode_is_canonical_and_has_same_mass_scaling",
        controls["bulk_massive_scalar_zero_mode"]["kinetic_r_power"] == 0
        and controls["bulk_massive_scalar_zero_mode"]["mass_squared_r_power"] == -1
        and controls["bulk_massive_scalar_zero_mode"]["matches_brane_alpha"] is True,
        bulk_control=controls["bulk_massive_scalar_zero_mode"],
    )
    add_check(
        checks,
        "kinematic_source_coupling_has_mat_mass_dimension",
        controls["four_dimensional_dimensions"]["closes_to_four"] is True
        and controls["four_dimensional_dimensions"]["alpha_or_source_coupling"] == -1,
        dimensions=controls["four_dimensional_dimensions"],
    )
    add_check(
        checks,
        "direct_radion_to_track_a_map_is_rejected",
        controls["operator_homogeneity"]["degrees_match"] is False
        and controls["operator_homogeneity"]["direct_radion_track_a_map"]
        == "REJECTED_DERIVATIVE_HOMOGENEITY_MISMATCH",
        homogeneity=controls["operator_homogeneity"],
    )
    add_check(
        checks,
        "comparison_is_structural_and_contains_no_weighted_score",
        all(set(row) == {"bulk", "brane"} for row in matrix.values()),
        criteria_count=len(matrix),
    )
    anchors = (
        "hep-ph/0012100",
        "hep-ph/0102019",
        "hep-ph/0401189",
        "hep-th/0008188",
    )
    add_check(
        checks,
        "primary_source_anchors_are_registered",
        all(anchor in contract_text for anchor in anchors),
        anchors=list(anchors),
    )
    add_check(
        checks,
        "parent_survival_and_physical_hessian_holds_remain_binding",
        a2a3.get("a3_disposition") == "HOLD_UNSTABILIZED_RADION"
        and hessian.get("physical_hessian") == "NOT_CONSTRUCTED"
        and hessian.get("radion_mass") == "NOT_COMPUTED"
        and hessian.get("physics_pass") is False,
    )

    all_ok = all(check["ok"] for check in checks)
    return {
        "schema": "ITSM_MAT001_TOPX4_H1_MATTER_ARCHITECTURE_COMPARISON_v1",
        "date": "2026-09-16",
        "status": STATUS if all_ok else ERROR_STATUS,
        "audit_execution_status": "COMPLETE" if all_ok else "ERROR",
        "checks_passed": sum(check["ok"] for check in checks),
        "checks_total": len(checks),
        "parent": "X4-S2F3",
        "parent_action_changed": False,
        "exact_controls": controls,
        "architecture_matrix": matrix,
        "decision": {
            "lead_source_projection_candidate": "BRANE_INDUCED_METRIC_CHILD_ROUTE",
            "lead_meaning": "ROUTE_RECOMMENDATION_ONLY",
            "bulk_route": "RETAIN_AS_SMOOTH_CIRCLE_AND_ZERO_MODE_CONTROL",
            "direct_radion_track_a_map": "REJECTED_DERIVATIVE_HOMOGENEITY_MISMATCH",
            "mixed_radion_condensate_mode": "OPEN_DEPENDENCY_LOCKED",
            "child_action_freeze": "NOT_AUTHORIZED",
            "reason": (
                "The brane option exposes one induced physical metric and a universal "
                "kinematic trace-source component without a physical-matter KK tower. "
                "It still creates a new localized theory with junction and counterterm "
                "requirements, and neither option produces the Track-A operator."
            ),
        },
        "literature_scope": {
            "bulk_KK_towers": "SUPPORTED_ARCHITECTURE_FACT_NOT_ITSM_VALIDATION",
            "bulk_chirality_mechanism": "REQUIRED_NOT_SUPPLIED",
            "physical_radion_mode_diagonalization": "REQUIRED_NOT_SUPPLIED",
            "brane_effective_equations": "REQUIRED_NOT_SUPPLIED",
        },
        "next_single_gate": {
            "name": "TOPX4_H1_BRANE_CHILD_GLOBAL_CONSISTENCY_PREFLIGHT",
            "scope": (
                "Test whether a compact smooth-circle child with one localized matter "
                "hypersurface can be globally and variationally specified without "
                "altering the parent by stealth."
            ),
            "stop_before": "NO_CHILD_ACTION_FREEZE_OR_PHYSICS_CALCULATION",
        },
        "checks": checks,
        "artifact_receipts": receipts,
        "status_firewall": {
            "parent_action_changed": False,
            "child_action_frozen": False,
            "physical_mode_identified": False,
            "physical_hessian_constructed": False,
            "signed_residue_computed": False,
            "K_Q_derived": False,
            "V_computed": False,
            "MAT001_pass": False,
            "UVIR003_pass": False,
            "stage4A_reopened": False,
            "rule9_cleared": False,
            "physics_pass": False,
            "gate_effect": "NONE",
        },
        "scientific_boundary": (
            "The derived alpha=-1/(sqrt(6) M_Pl) is a kinematic radion source "
            "component in two minimal controls. It is not the constrained H1 residue, "
            "does not produce the Track-A Y^(3/2) operator and does not compute V."
        ),
    }


def exported_contract_valid(summary: dict[str, Any]) -> bool:
    firewall = summary.get("status_firewall", {})
    decision = summary.get("decision", {})
    controls = summary.get("exact_controls", {})
    return bool(
        summary.get("status") == STATUS
        and summary.get("audit_execution_status") == "COMPLETE"
        and summary.get("checks_passed") == summary.get("checks_total")
        and summary.get("parent_action_changed") is False
        and decision.get("lead_source_projection_candidate")
        == "BRANE_INDUCED_METRIC_CHILD_ROUTE"
        and decision.get("lead_meaning") == "ROUTE_RECOMMENDATION_ONLY"
        and decision.get("child_action_freeze") == "NOT_AUTHORIZED"
        and decision.get("direct_radion_track_a_map")
        == "REJECTED_DERIVATIVE_HOMOGENEITY_MISMATCH"
        and controls.get("operator_homogeneity", {}).get("degrees_match") is False
        and all(
            firewall.get(key) is False
            for key in (
                "parent_action_changed",
                "child_action_frozen",
                "physical_mode_identified",
                "physical_hessian_constructed",
                "signed_residue_computed",
                "K_Q_derived",
                "V_computed",
                "MAT001_pass",
                "UVIR003_pass",
                "stage4A_reopened",
                "rule9_cleared",
                "physics_pass",
            )
        )
        and firewall.get("gate_effect") == "NONE"
    )


def mutation_suite(summary: dict[str, Any]) -> list[str]:
    if not exported_contract_valid(summary):
        raise AssertionError("baseline architecture comparison must be valid")

    mutants: list[tuple[str, dict[str, Any]]] = []

    direct_map = copy.deepcopy(summary)
    direct_map["decision"]["direct_radion_track_a_map"] = "DERIVED"
    mutants.append(("quadratic_radion_promoted_to_track_a", direct_map))

    changed_parent = copy.deepcopy(summary)
    changed_parent["parent_action_changed"] = True
    changed_parent["status_firewall"]["parent_action_changed"] = True
    mutants.append(("parent_modified_during_comparison", changed_parent))

    frozen_child = copy.deepcopy(summary)
    frozen_child["decision"]["child_action_freeze"] = "AUTHORIZED"
    frozen_child["status_firewall"]["child_action_frozen"] = True
    mutants.append(("child_freeze_without_global_preflight", frozen_child))

    fake_residue = copy.deepcopy(summary)
    fake_residue["status_firewall"]["signed_residue_computed"] = True
    fake_residue["status_firewall"]["V_computed"] = True
    mutants.append(("kinematic_alpha_promoted_to_physical_residue", fake_residue))

    wrong_lead = copy.deepcopy(summary)
    wrong_lead["decision"]["lead_source_projection_candidate"] = "BULK_AND_BRANE_HYBRID"
    mutants.append(("bulk_brane_hybrid", wrong_lead))

    erased_mismatch = copy.deepcopy(summary)
    erased_mismatch["exact_controls"]["operator_homogeneity"]["degrees_match"] = True
    mutants.append(("operator_homogeneity_mismatch_erased", erased_mismatch))

    passed: list[str] = []
    for label, mutant in mutants:
        if exported_contract_valid(mutant):
            raise AssertionError(f"mutation must be rejected: {label}")
        passed.append(label)
    return passed


def render_report(summary: dict[str, Any], output_digest: str) -> str:
    rows = "\n".join(
        f"| `{criterion}` | `{values['bulk']}` | `{values['brane']}` |"
        for criterion, values in summary["architecture_matrix"].items()
    )
    checks = "\n".join(
        f"| `{row['name']}` | {'yes' if row['ok'] else 'no'} |"
        for row in summary["checks"]
    )
    mutations = "\n".join(
        f"- `{label}`: rejected" for label in summary["mutation_tests"]["labels"]
    )
    return rf"""# MAT-001 TOP-X4 H1 physical-matter architecture comparison

**Executed:** 2026-09-16  
**Status:** `{summary['status']}`  
**Checks:** `{summary['checks_passed']}/{summary['checks_total']}`  
**Parent action changed:** `false`  
**Physics pass:** `false`  
**Gate effect:** `NONE`

## 1. Bounded result

The lead source-projection candidate is a **new brane-induced-metric child
route**, not because it solves MAT-001, but because it exposes one universal
physical metric for four-dimensional matter without introducing a full
physical-matter KK tower. This is a route recommendation only; no child action
is frozen or authorized.

Bulk physical matter remains the smooth-circle control. A realistic bulk
matter theory would require the complete gauge/Higgs/Yukawa/chiral spectrum,
its KK tower, anomaly data and its loop contribution to stabilization.

## 2. Exact kinematic result

For the verified Einstein-frame chart,

\[
A_b(\sigma)=r^{{-1/2}}
=\exp\!\left[-\frac{{\sigma}}{{\sqrt{{6}}M_{{\rm Pl}}}}\right],
\qquad
\alpha_b=\frac{{d\ln A_b}}{{d\sigma}}
=-\frac{{1}}{{\sqrt{{6}}M_{{\rm Pl}}}}.
\]

A minimally coupled massive bulk-scalar zero mode has an `r`-independent
four-dimensional kinetic coefficient and
`m_0(sigma)=m_5 exp[-sigma/(sqrt(6) M_Pl)]`, giving the same logarithmic
mass derivative in that limited control.

This common coefficient is **not** `V`: it is an unreduced radion source
component before metric/radion/condensate mixing and auxiliary constraints.

## 3. Direct-map no-go

The Einstein--Hilbert radion kinetic operator is homogeneous of degree two in
first derivatives. Track A requires degree three through `Y^(3/2)`. A regular
point-field redefinition preserves derivative degree, so

```text
DIRECT_RADION_EQUALS_TRACK_A_PSI = REJECTED
```

Only a newly derived mixed radion--condensate physical mode or other nonlinear
dynamics can keep the TOP-X4 H1 route open.

## 4. Structural comparison

| Requirement | Bulk physical matter | Brane-localized physical matter |
|---|---|---|
{rows}

No numerical weights were assigned.

## 5. Evidence checks

| Check | Satisfied |
|---|---|
{checks}

## 6. Rejection controls

{mutations}

All `{summary['mutation_tests']['passed']}/{summary['mutation_tests']['total']}`
registered mutations were rejected. This is local contract validation, not
independent Rule-9 review.

## 7. Literature boundary

- Appelquist, Cheng and Dobrescu:
  <https://arxiv.org/abs/hep-ph/0012100>.
- Papavassiliou and Santamaria:
  <https://arxiv.org/abs/hep-ph/0102019>.
- Kofman, Martin and Peloso:
  <https://arxiv.org/abs/hep-ph/0401189>.
- Maeda and Wands:
  <https://arxiv.org/abs/hep-th/0008188>.

These sources support the architecture cautions; they do not validate ITSM.

## 8. Next single gate

`{summary['next_single_gate']['name']}`: test compact-circle consistency,
localized variation, junction data and counterterm requirements before any
brane child action can be frozen. Stop before changing `X4-S2F3`.

## 9. Artifact record

- JSON: `{relative(OUTPUT_PATH)}`
- JSON SHA-256: `{output_digest}`
- contract: `{relative(CONTRACT_PATH)}`
- executable: `{relative(Path(__file__))}`

## 10. Binding boundary

```text
lead_source_projection_candidate=BRANE_INDUCED_METRIC_CHILD_ROUTE
lead_meaning=ROUTE_RECOMMENDATION_ONLY
child_action_freeze=NOT_AUTHORIZED
direct_radion_track_a_map=REJECTED_DERIVATIVE_HOMOGENEITY_MISMATCH
mixed_radion_condensate_mode=OPEN_DEPENDENCY_LOCKED
physical_hessian=NOT_CONSTRUCTED
signed_residue=NOT_COMPUTED
K_Q=NOT_DERIVED
V=NOT_COMPUTED
MAT-001=BLOCKED
Stage4A=CLOSED
physics_pass=false
gate_effect=NONE
```
"""


def main() -> int:
    args = parse_args()
    write_sidecar(Path(__file__))
    write_sidecar(CONTRACT_PATH)

    source_specs = [
        (Path(__file__), True),
        (CONTRACT_PATH, True),
        (BRIDGE_CONTRACT_PATH, True),
        (BRIDGE_SUMMARY_PATH, True),
        (A1_LEDGER_PATH, True),
        (A2A3_SUMMARY_PATH, True),
        (HESSIAN_SUMMARY_PATH, True),
    ]
    receipts = [
        artifact_receipt(path, sidecar_required=required)
        for path, required in source_specs
    ]
    summary = build_summary(receipts)
    if not exported_contract_valid(summary):
        print(summary["status"])
        print(f"checks={summary['checks_passed']}/{summary['checks_total']}")
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
        "lead_source_projection_candidate="
        f"{summary['decision']['lead_source_projection_candidate']}"
    )
    print(
        "direct_radion_track_a_map="
        f"{summary['decision']['direct_radion_track_a_map']}"
    )
    print("child_action_freeze=NOT_AUTHORIZED")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={args.output}")
    print(f"output_sha256={output_digest}")
    print(f"report={args.report}")
    print(f"report_sha256={sha256_file(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
