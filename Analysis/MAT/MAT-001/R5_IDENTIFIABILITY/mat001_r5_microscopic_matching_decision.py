#!/usr/bin/env python3
"""MAT-001 remediation R5: action-level matching identifiability decision.

This calculation asks whether the declared conformal matter action and the
Track-A force action determine the invariant signed residue

    V = C_m / sqrt(K_Q).

It proves the field-redefinition invariance of V and tests identifiability of
the independent Wilson coefficients.  A successful audit may return a HOLD;
it must not manufacture a coefficient relation or infer one from a
phenomenological normalization convention.

"R5" here names the post-R1--R4 MAT remediation item.  It is not UVIR-003's
pre-existing R5 AQUAL-class Conditional matching route.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


PASS_STATUS = "PASS_MAT001_R5_IDENTIFIABILITY_AUDIT_HOLD"
FAIL_STATUS = "FAIL_MAT001_R5_IDENTIFIABILITY_AUDIT"
HOLD_VERDICT = "HOLD_DECLARED_ACTION_UNDERDETERMINES_V"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--r3-matter",
        type=Path,
        default=mat
        / "COVARIANT_MATTER_ACTION"
        / "outputs"
        / "mat001_r3_covariant_matter_action_summary.json",
    )
    parser.add_argument(
        "--rr1",
        type=Path,
        default=mat
        / "PARENT_ACTION_MATCHING"
        / "outputs"
        / "mat001_rr1_parent_action_skeleton_summary.json",
    )
    parser.add_argument(
        "--rr2",
        type=Path,
        default=mat
        / "PARENT_ACTION_MATCHING"
        / "outputs"
        / "mat001_rr2_residue_pathway_summary.json",
    )
    parser.add_argument(
        "--unit-chart",
        type=Path,
        default=mat
        / "UNIT_CHART"
        / "outputs"
        / "mat001_unit_chart_contract_summary.json",
    )
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument("--self-test-mutations", action="store_true")
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def add_check(
    checks: list[dict[str, Any]], name: str, ok: bool, **details: Any
) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


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


def symbolic_identifiability() -> dict[str, Any]:
    k_q = sp.symbols("K_Q", positive=True)
    c_m = sp.symbols("C_m", real=True, nonzero=True)
    scale = sp.symbols("s", positive=True)
    target_v = sp.symbols("V_target", real=True, nonzero=True)
    kappa = sp.symbols("kappa", positive=True)
    c_ir, c_obs = sp.symbols("C_IR C_obs", positive=True)

    v_signed = sp.simplify(c_m / sp.sqrt(k_q))
    k_q_prime = sp.simplify(k_q / scale**2)
    c_m_prime = sp.simplify(c_m / scale)
    v_prime = sp.simplify(c_m_prime / sp.sqrt(k_q_prime))

    # The declared action form permits a continuous family with any nonzero
    # signed V: choose any kappa>0 and C_m=V_target*sqrt(kappa).
    family_c_m = sp.simplify(target_v * sp.sqrt(kappa))
    family_v = sp.simplify(family_c_m / sp.sqrt(kappa))

    jacobian = sp.Matrix([v_signed]).jacobian(sp.Matrix([c_m, k_q]))
    jacobian_rank = int(jacobian.rank())

    # Two common proposed closures still leave K_Q free.
    v_if_c_m_equals_c_ir = sp.simplify(c_ir / sp.sqrt(k_q))
    c_m_from_c_obs = sp.simplify(c_obs ** sp.Rational(2, 3) * c_ir ** sp.Rational(1, 3))
    v_if_c_obs_and_c_ir_fixed = sp.simplify(c_m_from_c_obs / sp.sqrt(k_q))

    return {
        "declared_joint_EFT": {
            "force_time_kinetic": "K_Q*(U.nabla(psi))^2/2",
            "matter_metric": "g_tilde_munu=exp(2*C_m*(psi-psi_star))*g_munu",
            "signed_canonical_residue": str(v_signed),
            "independent_wilson_coefficients": ["C_m", "K_Q"],
            "n_independent_wilson_coefficients": 2,
            "n_declared_action_relations_between_C_m_and_K_Q": 0,
        },
        "field_redefinition": {
            "map": "psi_prime=s*psi with s>0",
            "K_Q_prime": str(k_q_prime),
            "C_m_prime": str(c_m_prime),
            "V_prime": str(v_prime),
            "V_invariant": sp.simplify(v_prime - v_signed) == 0,
            "meaning": (
                "Field normalization removes neither the physical residue nor "
                "the need to determine it."
            ),
        },
        "identifiability": {
            "map": "F(C_m,K_Q)=C_m/sqrt(K_Q)",
            "jacobian": [[str(value) for value in jacobian.row(0)]],
            "jacobian_rank": jacobian_rank,
            "parameter_dimension": 2,
            "fixed_V_fibre_dimension": 2 - jacobian_rank,
            "continuous_family": {
                "domain": "kappa>0 and V_target real nonzero",
                "K_Q": str(kappa),
                "C_m": str(family_c_m),
                "V": str(family_v),
                "recovers_arbitrary_target_V": sp.simplify(family_v - target_v) == 0,
            },
            "V_identified_by_declared_action_form": False,
        },
        "proposed_shortcuts": {
            "C_m_equals_C_IR": {
                "V": str(v_if_c_m_equals_c_ir),
                "still_depends_on_K_Q": k_q in v_if_c_m_equals_c_ir.free_symbols,
                "disposition": "REJECTED_AS_DERIVED_CLOSURE",
            },
            "fixed_C_obs_and_C_IR": {
                "C_m_positive_branch": str(c_m_from_c_obs),
                "V": str(v_if_c_obs_and_c_ir_fixed),
                "still_depends_on_K_Q": k_q in v_if_c_obs_and_c_ir_fixed.free_symbols,
                "disposition": "INSUFFICIENT_WITHOUT_K_Q_OR_RESIDUE",
            },
            "set_K_Q_equal_1": {
                "disposition": "FIELD_NORMALIZATION_NOT_A_PHYSICAL_MATCH",
            },
            "UVIR_R5_AQUAL_anchor": {
                "disposition": "CONDITIONAL_PHENOMENOLOGY_FIXES_C_obs_NOT_V",
            },
        },
    }


def exported_contract_valid(summary: dict[str, Any]) -> bool:
    ident = summary.get("symbolic_result", {}).get("identifiability", {})
    redef = summary.get("symbolic_result", {}).get("field_redefinition", {})
    joint = summary.get("symbolic_result", {}).get("declared_joint_EFT", {})
    family = ident.get("continuous_family", {})
    firewall = summary.get("status_firewall", {})
    return bool(
        summary.get("subgate_status") == PASS_STATUS
        and summary.get("decision_status") == "HOLD"
        and summary.get("matching_verdict") == HOLD_VERDICT
        and joint.get("n_independent_wilson_coefficients") == 2
        and joint.get("n_declared_action_relations_between_C_m_and_K_Q") == 0
        and redef.get("V_invariant") is True
        and ident.get("jacobian_rank") == 1
        and ident.get("fixed_V_fibre_dimension") == 1
        and family.get("recovers_arbitrary_target_V") is True
        and ident.get("V_identified_by_declared_action_form") is False
        and summary.get("direct_residue_route", {}).get(
            "live_normalized_residue_available"
        )
        is False
        and all(
            firewall.get(key) is False
            for key in (
                "C_m_numeric_derived",
                "K_Q_numeric_derived",
                "V_computed",
                "MAT001_pass",
                "UVIR003_pass",
                "stage4A_reopened",
                "physics_pass",
            )
        )
    )


def build_summary(
    r3: dict[str, Any] | None,
    rr1: dict[str, Any] | None,
    rr2: dict[str, Any] | None,
    unit: dict[str, Any] | None,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "r3_covariant_matter_action_scoped",
        bool(
            r3
            and r3.get("subgate_status")
            == "PASS_MAT001_R3_COVARIANT_MATTER_ACTION_SCOPED"
            and (r3.get("status_firewall") or {}).get("C_m_numeric_derived") is False
        ),
    )
    add_check(
        checks,
        "rr1_parent_skeleton_unmatched",
        bool(
            rr1
            and rr1.get("subgate_status")
            == "PASS_MAT001_RR1_PARENT_ACTION_SKELETON_DECLARED_UNMATCHED"
            and rr1.get("V_status") == "NOT_COMPUTED"
            and rr1.get("kq_numeric_status") == "NOT_DERIVED"
        ),
    )
    add_check(
        checks,
        "rr2_live_residue_absent",
        bool(
            rr2
            and rr2.get("subgate_status")
            == "PASS_MAT001_RR2_RESIDUE_PATHWAY_ATTEMPTED_INCOMPLETE"
            and rr2.get("V_status") == "NOT_COMPUTED"
            and (rr2.get("claim_firewall") or {}).get("numeric_V_computed") is False
            and (rr2.get("claim_firewall") or {}).get("RR2_closed") is False
        ),
    )
    add_check(
        checks,
        "unit_chart_keeps_matching_open",
        bool(
            unit
            and unit.get("subgate_status") == "PASS_MAT001_UNIT_CHART_CONTRACT_OPEN"
            and unit.get("V_status") == "NOT_COMPUTED"
            and unit.get("kq_numeric_status") == "NOT_DERIVED"
        ),
    )

    symbolic = symbolic_identifiability()
    add_check(
        checks,
        "signed_residue_redefinition_invariant",
        symbolic["field_redefinition"]["V_invariant"] is True,
    )
    add_check(
        checks,
        "declared_action_has_two_independent_wilson_coefficients",
        symbolic["declared_joint_EFT"]["n_independent_wilson_coefficients"] == 2
        and symbolic["declared_joint_EFT"][
            "n_declared_action_relations_between_C_m_and_K_Q"
        ]
        == 0,
    )
    add_check(
        checks,
        "arbitrary_signed_V_family_exists",
        symbolic["identifiability"]["continuous_family"]["recovers_arbitrary_target_V"]
        is True,
    )
    add_check(
        checks,
        "shortcut_closures_leave_K_Q_or_matching_open",
        symbolic["proposed_shortcuts"]["C_m_equals_C_IR"]["still_depends_on_K_Q"]
        is True
        and symbolic["proposed_shortcuts"]["fixed_C_obs_and_C_IR"][
            "still_depends_on_K_Q"
        ]
        is True,
    )

    all_ok = all(row["ok"] for row in checks)
    summary = {
        "gate": "MAT-001",
        "remediation_item": "R5_MICROSCOPIC_MATCHING_DECISION",
        "route_namespace_note": (
            "This remediation R5 is distinct from UVIR-003 K_Q route R5 "
            "(Conditional AQUAL-class IR anchor)."
        ),
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "decision_status": "HOLD",
        "matching_verdict": HOLD_VERDICT,
        "mat001_status": "BLOCKED",
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "C_m_numeric_status": "NOT_DERIVED_FORM_ONLY",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "physics_pass": False,
        "stage4A_status": "CLOSED",
        "symbolic_result": symbolic,
        "direct_residue_route": {
            "live_normalized_residue_available": False,
            "reason": (
                "RR2 has no action-derived Track-A matter response or amplitude "
                "that isolates the normalized signed residue."
            ),
        },
        "tier1_decision": {
            "finding": (
                "Placing C_m and K_Q in one declared EFT action is necessary but "
                "does not relate independent Wilson coefficients. The action "
                "class admits a continuous one-parameter family at fixed V and "
                "admits arbitrary nonzero signed V across the family."
            ),
            "minimum_new_physics_for_closure": [
                "a microscopic calculation of g_phi/sqrt(Z_phi) in a named parent action",
                "or a live on-shell signed matter-to-physical-mode residue",
                "or an independently justified coefficient relation plus enough physical input to fix V",
            ],
            "next_action": (
                "Do not perform another coefficient inventory. Supply one named "
                "microscopic completion or derive the live normalized residue; "
                "otherwise retain HOLD."
            ),
        },
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "status_firewall": {
            "C_m_numeric_derived": False,
            "K_Q_numeric_derived": False,
            "V_computed": False,
            "MAT001_pass": False,
            "UVIR003_pass": False,
            "stage4A_reopened": False,
            "physics_pass": False,
        },
        "scientific_boundary": (
            "The audit proves non-identifiability within the declared action "
            "class. It is not a theorem that no UV completion can predict V; it "
            "states exactly what the current declared action does not predict."
        ),
    }
    return summary


def mutation_suite(summary: dict[str, Any]) -> None:
    require(exported_contract_valid(summary), "baseline exported R5 contract")

    mutants: list[tuple[str, dict[str, Any]]] = []
    promoted_v = copy.deepcopy(summary)
    promoted_v["status_firewall"]["V_computed"] = True
    mutants.append(("premature V promotion", promoted_v))

    invented_relation = copy.deepcopy(summary)
    invented_relation["symbolic_result"]["declared_joint_EFT"][
        "n_declared_action_relations_between_C_m_and_K_Q"
    ] = 1
    mutants.append(("invented coefficient relation", invented_relation))

    erased_family = copy.deepcopy(summary)
    erased_family["symbolic_result"]["identifiability"]["continuous_family"][
        "recovers_arbitrary_target_V"
    ] = False
    mutants.append(("erased non-identifiability family", erased_family))

    fake_residue = copy.deepcopy(summary)
    fake_residue["direct_residue_route"]["live_normalized_residue_available"] = True
    mutants.append(("unbacked live residue", fake_residue))

    wrong_namespace = copy.deepcopy(summary)
    wrong_namespace["matching_verdict"] = "DERIVED_FROM_UVIR_R5_AQUAL"
    mutants.append(("UVIR R5 namespace collision", wrong_namespace))

    for label, mutant in mutants:
        require(not exported_contract_valid(mutant), f"mutation must fail: {label}")


def main() -> None:
    args = parse_args()
    r3, e_r3, s_r3 = load_json(args.r3_matter)
    rr1, e_rr1, s_rr1 = load_json(args.rr1)
    rr2, e_rr2, s_rr2 = load_json(args.rr2)
    unit, e_unit, s_unit = load_json(args.unit_chart)
    evidence = {
        "r3_matter": {
            "source": args.r3_matter.name,
            "sha256": s_r3,
            "parse_error": e_r3,
        },
        "rr1_parent_skeleton": {
            "source": args.rr1.name,
            "sha256": s_rr1,
            "parse_error": e_rr1,
        },
        "rr2_residue_pathway": {
            "source": args.rr2.name,
            "sha256": s_rr2,
            "parse_error": e_rr2,
        },
        "unit_chart": {
            "source": args.unit_chart.name,
            "sha256": s_unit,
            "parse_error": e_unit,
        },
    }
    summary = build_summary(r3, rr1, rr2, unit, evidence)
    require(summary["calculation_status"] == "PASS", "R5 identifiability checks")
    require(exported_contract_valid(summary), "exported R5 contract")

    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_r5_microscopic_matching_decision_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    sidecar = output.with_suffix(".sha256")
    sidecar.write_bytes(f"{digest}  {output.name}\n".encode("ascii"))

    print("MAT-001 R5 microscopic matching identifiability decision")
    print("  verdict:", summary["matching_verdict"])
    print("  V:", summary["V_status"], "| K_Q:", summary["kq_numeric_status"])
    print("  next:", summary["tier1_decision"]["next_action"])
    for row in summary["checks"]:
        print(f"  [{'OK' if row['ok'] else 'FAIL'}] {row['name']}")
    print("STATUS:", summary["subgate_status"])
    print("JSON_SHA256:", digest)


if __name__ == "__main__":
    main()
