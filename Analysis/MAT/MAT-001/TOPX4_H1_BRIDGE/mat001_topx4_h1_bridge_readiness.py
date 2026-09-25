#!/usr/bin/env python3
"""Audit the non-promoting TOP-X4 -> MAT-001 H1 bridge boundary.

This executable does not calculate a physical Hessian or a matter residue. It
verifies the bounded TOP-X4 and MAT evidence, tests the invariant signed-source
algebra, and records the exact missing inputs for a future same-action bridge.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


BRIDGE_STATUS = "HOLD_MAT001_TOPX4_H1_BRIDGE_INPUTS_NOT_CLOSED"
ERROR_STATUS = "ERROR_MAT001_TOPX4_H1_BRIDGE_READINESS_AUDIT"

REPO_ROOT = Path(__file__).resolve().parents[4]
BASE = Path(__file__).resolve().parent
OUTPUT_PATH = BASE / "outputs" / "mat001_topx4_h1_bridge_readiness_summary.json"
REPORT_PATH = BASE / "MAT001_TOPX4_H1_BRIDGE_READINESS_2026-09-16.md"
CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_BRIDGE_CONTRACT_2026-09-16.md"
)

TOP_GATE = REPO_ROOT / "Theory" / "Gates" / "TOP-X4"
TOP_OUTPUTS = REPO_ROOT / "Analysis" / "TOP" / "TOP-X4" / "outputs"
MAT_GATE = REPO_ROOT / "Theory" / "Gates" / "MAT-001"
MAT_ANALYSIS = REPO_ROOT / "Analysis" / "MAT" / "MAT-001"

A1_LEDGER_PATH = TOP_GATE / "TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md"
PARENT_FREEZE_PATH = TOP_GATE / "TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md"
A2A3_PATH = TOP_OUTPUTS / "topx4_a2a3_reduction_radion_summary.json"
HESSIAN_PATH = TOP_OUTPUTS / "topx4_s2f3_physical_hessian_readiness_summary.json"
GLOBAL_STATE_PATH = TOP_OUTPUTS / "topx4_s2f3_global_state_construction_summary.json"
COVARIANT_PATH = TOP_OUTPUTS / "topx4_s2f3_covariant_scalar_matrix_summary.json"
DIRAC_PATH = TOP_OUTPUTS / "topx4_s2f3_curved_dirac_operator_summary.json"
J1_PATH = (
    MAT_ANALYSIS
    / "J1_JOINT_ACTION"
    / "outputs"
    / "mat001_j1_joint_action_normalization_summary.json"
)
R5_PATH = (
    MAT_ANALYSIS
    / "R5_IDENTIFIABILITY"
    / "outputs"
    / "mat001_r5_microscopic_matching_decision_summary.json"
)
R4_PATH = MAT_GATE / "MAT-001_R4_SIGNED_RESIDUE_CONTRACT.md"


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
    candidates = [Path(str(path) + ".sha256"), path.with_suffix(".sha256")]
    unique: list[Path] = []
    for candidate in candidates:
        if candidate not in unique:
            unique.append(candidate)
    return unique


def find_sidecar(path: Path) -> Path | None:
    return next((candidate for candidate in sidecar_candidates(path) if candidate.is_file()), None)


def write_sidecar(path: Path, *, replace_suffix: bool = False) -> Path:
    sidecar = path.with_suffix(".sha256") if replace_suffix else Path(str(path) + ".sha256")
    digest = sha256_file(path)
    sidecar.write_text(f"{digest}  {path.name}\n", encoding="ascii", newline="\n")
    return sidecar


def artifact_receipt(path: Path, *, sidecar_required: bool) -> dict[str, Any]:
    exists = path.is_file()
    actual = sha256_file(path) if exists else None
    sidecar = find_sidecar(path) if exists else None
    expected: str | None = None
    if sidecar is not None:
        tokens = sidecar.read_text(encoding="ascii").split()
        expected = tokens[0].lower() if tokens else "MALFORMED"
    sidecar_matches = actual == expected if expected is not None else None
    return {
        "path": relative(path),
        "exists": exists,
        "sha256": actual,
        "sidecar_path": relative(sidecar) if sidecar is not None else None,
        "sidecar_required": sidecar_required,
        "sidecar_matches": sidecar_matches,
    }


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"Expected a JSON object: {path}")
    return data


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def signed_projection_identities() -> dict[str, Any]:
    z_phi = sp.symbols("Z_phi", positive=True)
    g_phi = sp.symbols("g_phi", real=True, nonzero=True)
    scale = sp.symbols("s", positive=True)
    d, b_mix, c_aux, h = sp.symbols("d B C h", real=True, nonzero=True)

    invariant = sp.simplify(g_phi / sp.sqrt(z_phi))
    transformed = sp.simplify((g_phi / scale) / sp.sqrt(z_phi / scale**2))
    c_eff = sp.simplify(d - b_mix * h / c_aux)

    return {
        "same_action_residue": str(invariant),
        "positive_rescaling_map": {
            "Z_phi_prime": str(z_phi / scale**2),
            "g_phi_prime": str(g_phi / scale),
            "residue_prime": str(transformed),
            "invariant": sp.simplify(transformed - invariant) == 0,
        },
        "one_auxiliary_source_reduction": {
            "c_eff": str(c_eff),
            "matches_R4_form": sp.simplify(c_eff - (d - b_mix * h / c_aux)) == 0,
        },
        "orientation_reversal": {
            "g_of_minus_u": str(-invariant),
            "sign_flips": sp.simplify((-invariant) + invariant) == 0,
        },
        "track_a_signed_condition": "g_H1=-V_signed=-C_m/sqrt(K_Q)",
        "four_dimensional_mass_dimensions": {
            "phi_c": 1,
            "rho_b": 4,
            "g_H1": -1,
            "interaction_total": 4,
            "dimension_closes": 1 + 4 - 1 == 4,
        },
    }


def closure_requirements() -> list[dict[str, Any]]:
    rows = [
        ("physical_matter_architecture_and_action", "UNSELECTED"),
        ("complete_same_action_variation", "NOT_AVAILABLE"),
        ("stabilized_finite_charge_on_shell_background", "NOT_AVAILABLE"),
        ("complete_renormalized_effective_action", "NOT_AVAILABLE"),
        ("canonical_constraint_reduction", "NOT_AVAILABLE"),
        ("oriented_positive_norm_source_mode", "NOT_IDENTIFIED"),
        ("signed_matter_residue", "NOT_COMPUTED"),
        ("track_a_field_and_unit_chart_map", "NOT_DERIVED"),
        ("registered_domain_robustness", "NOT_RUN"),
        ("independent_rule9_clearance", "THREE_WAY_CLEARANCE_NOT_MET"),
    ]
    return [
        {"requirement": name, "status": status, "satisfied": False}
        for name, status in rows
    ]


def build_summary(receipts: list[dict[str, Any]]) -> dict[str, Any]:
    a2a3 = load_json(A2A3_PATH)
    hessian = load_json(HESSIAN_PATH)
    global_state = load_json(GLOBAL_STATE_PATH)
    covariant = load_json(COVARIANT_PATH)
    dirac = load_json(DIRAC_PATH)
    j1 = load_json(J1_PATH)
    r5 = load_json(R5_PATH)

    a1_text = A1_LEDGER_PATH.read_text(encoding="utf-8").lower()
    a1_words = " ".join(a1_text.split())
    parent_text = PARENT_FREEZE_PATH.read_text(encoding="utf-8").lower()
    r4_text = R4_PATH.read_text(encoding="utf-8")
    algebra = signed_projection_identities()

    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "all_declared_authority_and_evidence_files_exist",
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
        "frozen_parent_does_not_contain_physical_baryonic_matter",
        "bulk matter proxy" in a1_words
        and "no four-dimensional portal or brane term is permitted" in a1_words
        and "no scalar coupling" in parent_text
        and "matter portal" in parent_text
        and "brane term" in parent_text,
        chi_role="BULK_MATTER_PROXY_NOT_PHYSICAL_BARYONIC_SOURCE",
    )
    add_check(
        checks,
        "canonical_radion_chart_is_bounded_but_parent_is_unstabilized",
        a2a3.get("a2_disposition") == "PARTIAL_FIXED_BACKGROUND_CONTROL_ONLY"
        and a2a3.get("a3_disposition") == "HOLD_UNSTABILIZED_RADION"
        and a2a3.get("advance_to_a4") is False
        and a2a3.get("physics_pass") is False,
        a2_disposition=a2a3.get("a2_disposition"),
        a3_disposition=a2a3.get("a3_disposition"),
    )
    add_check(
        checks,
        "scalar_state_and_fixed_metric_operator_are_not_a_physical_hessian",
        global_state.get("construction_status", {}).get(
            "global_scalar_matrix_hadamard_state"
        )
        == "THEOREM_BACKED_CONSTRUCTED"
        and covariant.get("scalar_matrix_operator") == "DERIVED_FIXED_METRIC_OFF_SHELL"
        and hessian.get("physical_hessian") == "NOT_CONSTRUCTED"
        and hessian.get("radion_mass") == "NOT_COMPUTED",
        scalar_state=global_state.get("construction_status", {}).get(
            "global_scalar_matrix_hadamard_state"
        ),
        physical_hessian=hessian.get("physical_hessian"),
    )
    add_check(
        checks,
        "renormalized_stress_and_counterterm_normalizations_remain_open",
        covariant.get("determinant") == "NOT_COMPUTED"
        and covariant.get("renormalized_stress") == "NOT_COMPUTED"
        and covariant.get("counterterm_normalizations") == "NOT_FIXED",
        determinant=covariant.get("determinant"),
        renormalized_stress=covariant.get("renormalized_stress"),
        counterterm_normalizations=covariant.get("counterterm_normalizations"),
    )
    add_check(
        checks,
        "curved_dirac_result_is_operator_scoped_only",
        dirac.get("operator_status")
        == "DERIVED_HAMILTONIAN_FORM_ON_REGISTERED_HOMOGENEOUS_METRIC"
        and dirac.get("covariant_completion") == "SCOPED_ONLY_NOT_FULL"
        and dirac.get("advance_to_physical_hessian") is False
        and dirac.get("physics_pass") is False,
        operator_status=dirac.get("operator_status"),
        covariant_completion=dirac.get("covariant_completion"),
    )
    add_check(
        checks,
        "mat_same_action_invariant_exists_but_numeric_matching_is_open",
        j1.get("V_form_status") == "SAME_ACTION_IDENTITY_DERIVED"
        and j1.get("V_status") == "NOT_COMPUTED"
        and j1.get("kq_numeric_status") == "NOT_DERIVED"
        and r5.get("matching_verdict") == "HOLD_DECLARED_ACTION_UNDERDETERMINES_V"
        and r5.get("mat001_status") == "BLOCKED",
        V_form_status=j1.get("V_form_status"),
        matching_verdict=r5.get("matching_verdict"),
    )
    add_check(
        checks,
        "signed_projection_and_positive_rescaling_identities_close",
        algebra["positive_rescaling_map"]["invariant"] is True
        and algebra["one_auxiliary_source_reduction"]["matches_R4_form"] is True
        and algebra["orientation_reversal"]["sign_flips"] is True
        and "g_{\\rm can}=-\\frac{C_m}{\\sqrt{K_Q}}" in r4_text,
        track_a_condition=algebra["track_a_signed_condition"],
    )
    add_check(
        checks,
        "four_dimensional_source_vertex_mass_dimension_closes",
        algebra["four_dimensional_mass_dimensions"]["dimension_closes"] is True
        and algebra["four_dimensional_mass_dimensions"]["g_H1"] == -1,
        dimensions=algebra["four_dimensional_mass_dimensions"],
    )
    add_check(
        checks,
        "all_live_gate_and_review_firewalls_remain_closed",
        hessian.get("physics_pass") is False
        and hessian.get("gate_effect") == "NONE"
        and global_state.get("rule9_review", {}).get("status")
        == "THREE_WAY_CLEARANCE_NOT_MET"
        and r5.get("V_status") == "NOT_COMPUTED"
        and r5.get("kq_numeric_status") == "NOT_DERIVED"
        and r5.get("stage4A_status") == "CLOSED",
        rule9=global_state.get("rule9_review", {}).get("status"),
    )

    closure = closure_requirements()
    foundation_ok = all(check["ok"] for check in checks)
    closure_count = sum(row["satisfied"] for row in closure)
    status = BRIDGE_STATUS if foundation_ok else ERROR_STATUS

    return {
        "schema": "ITSM_MAT001_TOPX4_H1_BRIDGE_READINESS_v1",
        "date": "2026-09-16",
        "route": "TOP-X4_TO_MAT-001_H1",
        "candidate_parent": "X4-S2F3",
        "route_disposition": "TOPX4_PRIMARY_RESEARCH_CANDIDATE_HELD",
        "fallback_route": "VERSIONED_M1_R5_P1_PARENT_REDESIGN",
        "status": status,
        "audit_execution_status": "COMPLETE" if foundation_ok else "ERROR",
        "foundation_checks_passed": sum(check["ok"] for check in checks),
        "foundation_checks_total": len(checks),
        "bridge_closure_requirements_satisfied": closure_count,
        "bridge_closure_requirements_total": len(closure),
        "bridge_ready": False,
        "matter_architecture": {
            "selected_option": "UNSELECTED",
            "mixing_rule": "EXACTLY_ONE_OF_BULK_OR_BRANE_IN_A_NEW_CHILD_FREEZE",
            "options": {
                "bulk_physical_matter": "OPEN_NOT_SELECTED",
                "brane_localized_physical_matter": "OPEN_NOT_SELECTED",
                "inserted_four_dimensional_portal": "REJECTED_INSIDE_FROZEN_PARENT",
            },
        },
        "candidate_mode_space": {
            "radion_sigma": "CANONICAL_FIXED_BACKGROUND_DIRECTION_ONLY",
            "condensate_amplitude_phase": "FIXED_METRIC_OPERATOR_ONLY",
            "chi": "BULK_PROXY_NOT_BARYONIC_MATTER",
            "metric_scalar_auxiliaries": "CONSTRAINT_BLOCK_NOT_AVAILABLE",
            "oriented_source_carrying_mode": "NOT_IDENTIFIED",
        },
        "projection_contract": algebra,
        "closure_requirements": closure,
        "checks": checks,
        "artifact_receipts": receipts,
        "next_single_gate": {
            "name": "TOPX4_H1_PHYSICAL_MATTER_ARCHITECTURE_COMPARISON",
            "scope": "Compare one bulk and one brane physical-matter child action without modifying X4-S2F3.",
            "allowed_effect": "ROUTE_RECOMMENDATION_ONLY",
            "forbidden_effects": [
                "no parent-action mutation",
                "no K_Q or V promotion",
                "no MAT or UVIR promotion",
                "no Stage 4A reopening",
            ],
        },
        "status_firewall": {
            "physical_hessian_constructed": False,
            "radion_mass_computed": False,
            "physical_matter_action_frozen": False,
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
            "TOP-X4 can be a microscopic H1 parent only after one physical matter action, "
            "a stabilized on-shell background, the complete constrained reduction and a "
            "signed source projection exist in one versioned chain. Current artifacts provide "
            "bounded prerequisites only; chi is not relabelled as baryonic matter."
        ),
    }


def exported_contract_valid(summary: dict[str, Any]) -> bool:
    firewall = summary.get("status_firewall", {})
    modes = summary.get("candidate_mode_space", {})
    matter = summary.get("matter_architecture", {})
    projection = summary.get("projection_contract", {})
    closure = summary.get("closure_requirements", [])
    return bool(
        summary.get("status") == BRIDGE_STATUS
        and summary.get("audit_execution_status") == "COMPLETE"
        and summary.get("foundation_checks_passed")
        == summary.get("foundation_checks_total")
        and summary.get("bridge_closure_requirements_satisfied") == 0
        and summary.get("bridge_ready") is False
        and matter.get("selected_option") == "UNSELECTED"
        and modes.get("chi") == "BULK_PROXY_NOT_BARYONIC_MATTER"
        and modes.get("oriented_source_carrying_mode") == "NOT_IDENTIFIED"
        and projection.get("track_a_signed_condition")
        == "g_H1=-V_signed=-C_m/sqrt(K_Q)"
        and all(row.get("satisfied") is False for row in closure)
        and all(
            firewall.get(key) is False
            for key in (
                "physical_hessian_constructed",
                "radion_mass_computed",
                "physical_matter_action_frozen",
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
        raise AssertionError("baseline bridge contract must be valid")

    mutants: list[tuple[str, dict[str, Any]]] = []

    relabelled_chi = copy.deepcopy(summary)
    relabelled_chi["candidate_mode_space"]["chi"] = "PHYSICAL_BARYONIC_MATTER"
    mutants.append(("chi_proxy_relabelled_as_baryonic_matter", relabelled_chi))

    hybrid_matter = copy.deepcopy(summary)
    hybrid_matter["matter_architecture"]["selected_option"] = "BULK_AND_BRANE"
    mutants.append(("bulk_and_brane_hybrid", hybrid_matter))

    premature_ready = copy.deepcopy(summary)
    premature_ready["bridge_ready"] = True
    mutants.append(("premature_bridge_readiness", premature_ready))

    fake_residue = copy.deepcopy(summary)
    fake_residue["status_firewall"]["V_computed"] = True
    fake_residue["status_firewall"]["signed_residue_computed"] = True
    mutants.append(("unbacked_residue_promotion", fake_residue))

    unsigned_projection = copy.deepcopy(summary)
    unsigned_projection["projection_contract"]["track_a_signed_condition"] = (
        "abs(g_H1)=abs(V_signed)"
    )
    mutants.append(("signed_orientation_erased", unsigned_projection))

    fake_hessian = copy.deepcopy(summary)
    fake_hessian["status_firewall"]["physical_hessian_constructed"] = True
    mutants.append(("fixed_metric_operator_promoted_to_physical_hessian", fake_hessian))

    passed: list[str] = []
    for label, mutant in mutants:
        if exported_contract_valid(mutant):
            raise AssertionError(f"mutation must be rejected: {label}")
        passed.append(label)
    return passed


def render_report(summary: dict[str, Any], output_digest: str) -> str:
    closure_rows = "\n".join(
        f"| `{row['requirement']}` | `{row['status']}` | no |"
        for row in summary["closure_requirements"]
    )
    check_rows = "\n".join(
        f"| `{row['name']}` | {'yes' if row['ok'] else 'no'} |"
        for row in summary["checks"]
    )
    mutation_rows = "\n".join(
        f"- `{label}`: rejected" for label in summary["mutation_tests"]["labels"]
    )
    return rf"""# MAT-001 TOP-X4 to H1 bridge readiness receipt

**Executed:** 2026-09-16  
**Bridge status:** `{summary['status']}`  
**Foundation evidence checks:** `{summary['foundation_checks_passed']}/{summary['foundation_checks_total']}`  
**Closure requirements satisfied:** `{summary['bridge_closure_requirements_satisfied']}/{summary['bridge_closure_requirements_total']}`  
**Bridge ready:** `false`  
**Physics pass:** `false`  
**Gate effect:** `NONE`

## 1. Result

TOP-X4 remains a credible microscopic candidate for MAT-001 H1, but the live
artifacts do not yet provide the physical matter action, stabilized constrained
mode or signed residue needed for matching. The audit executed successfully;
the successful foundation count is not a physics pass.

The existing `chi` field remains a bulk matter proxy, not a baryonic source.
The fixed-metric scalar operator and theorem-backed scalar state remain
prerequisites, not the constrained physical Hessian.

## 2. Exact bridge target

After canonical constraint reduction, an oriented positive-norm mode must
satisfy

\[
g_{{H1}}=\frac{{c_{{\rm phys}}^T u_{{H1}}}}
{{\sqrt{{u_{{H1}}^T K_{{\rm phys}}u_{{H1}}}}}}
=-\frac{{C_m}}{{\sqrt{{K_Q}}}}=-V_{{\rm signed}}.
\]

In the four-dimensional natural-unit density chart, `[g_H1]=-1`, matching the
existing MAT unit chart. No absolute-value or squared residue is accepted as
the signed vertex.

## 3. Closure inventory

| Requirement | Current status | Satisfied |
|---|---|---|
{closure_rows}

## 4. Foundation evidence audit

| Check | Satisfied |
|---|---|
{check_rows}

## 5. Rejection controls

{mutation_rows}

All `{summary['mutation_tests']['passed']}/{summary['mutation_tests']['total']}`
registered mutations were rejected. These are contract controls, not
independent Rule-9 reviewers.

## 6. Next single gate

`{summary['next_single_gate']['name']}`: compare one universal bulk-matter
child action with one brane-localized child action without modifying the
frozen `X4-S2F3` parent. The comparison may recommend one new child freeze; it
may not compute or promote `K_Q`, `V`, MAT-001, UVIR-003 or Stage 4A.

The current Plan-11 parent-survival holds remain binding. A matter architecture
decision alone does not bypass stabilization, renormalized stress or the
physical-Hessian requirements.

## 7. Artifact record

- JSON: `{relative(OUTPUT_PATH)}`
- JSON SHA-256: `{output_digest}`
- contract: `{relative(CONTRACT_PATH)}`
- executable: `{relative(Path(__file__))}`

## 8. Binding non-promotion boundary

```text
matter_architecture=UNSELECTED
physical_mode=NOT_IDENTIFIED
signed_residue=NOT_COMPUTED
track_a_map=NOT_DERIVED
K_Q=NOT_DERIVED
V=NOT_COMPUTED
MAT-001=BLOCKED
UVIR-003=IN_PROGRESS
Stage4A=CLOSED
Rule9=THREE_WAY_CLEARANCE_NOT_MET
physics_pass=false
gate_effect=NONE
```
"""


def main() -> int:
    args = parse_args()

    # Rule-9 artifact-integrity requirement: hash authored executable/contract
    # immediately. Generated JSON/report sidecars are written after generation.
    write_sidecar(Path(__file__))
    write_sidecar(CONTRACT_PATH)

    source_specs = [
        (Path(__file__), True),
        (CONTRACT_PATH, True),
        (A1_LEDGER_PATH, True),
        (PARENT_FREEZE_PATH, True),
        (A2A3_PATH, True),
        (HESSIAN_PATH, True),
        (GLOBAL_STATE_PATH, True),
        (COVARIANT_PATH, True),
        (DIRAC_PATH, True),
        (J1_PATH, True),
        (R5_PATH, True),
        (R4_PATH, False),
    ]
    receipts = [
        artifact_receipt(path, sidecar_required=required)
        for path, required in source_specs
    ]
    summary = build_summary(receipts)

    if not exported_contract_valid(summary):
        print(summary["status"])
        print(
            "foundation_checks="
            f"{summary['foundation_checks_passed']}/{summary['foundation_checks_total']}"
        )
        return 1

    mutation_labels = mutation_suite(summary)
    summary["mutation_tests"] = {
        "passed": len(mutation_labels),
        "total": len(mutation_labels),
        "labels": mutation_labels,
    }
    summary["script_sha256"] = sha256_file(Path(__file__))
    summary["contract_sha256"] = sha256_file(CONTRACT_PATH)

    if args.self_test_mutations:
        print(f"MUTATION_SUITE: {len(mutation_labels)}/{len(mutation_labels)}")
        for label in mutation_labels:
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
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8", newline="\n")
    report_sidecar = write_sidecar(args.report)

    print(summary["status"])
    print(
        "foundation_checks="
        f"{summary['foundation_checks_passed']}/{summary['foundation_checks_total']}"
    )
    print(
        "closure_requirements="
        f"{summary['bridge_closure_requirements_satisfied']}/"
        f"{summary['bridge_closure_requirements_total']}"
    )
    print(f"mutation_tests={len(mutation_labels)}/{len(mutation_labels)}")
    print("bridge_ready=false")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={args.output}")
    print(f"output_sha256={output_digest}")
    print(f"report={args.report}")
    print(f"report_sha256={sha256_file(args.report)}")
    print(f"report_sidecar={report_sidecar}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
