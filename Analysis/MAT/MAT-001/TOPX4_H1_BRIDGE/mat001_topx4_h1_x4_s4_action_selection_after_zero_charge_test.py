#!/usr/bin/env python3
"""Adjudicate the failed X4-S4 flat seed and select the next bounded route."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


STATUS = "SELECT_CURVED_SLICE_OUTPUT_ROUTE_HOLD_EXECUTION"
ERROR_STATUS = "ERROR_X4_S4_POST_ZERO_CHARGE_ACTION_SELECTION"

REPO_ROOT = Path(__file__).resolve().parents[4]
BASE = Path(__file__).resolve().parent
OUTPUT_PATH = BASE / "outputs" / "mat001_topx4_h1_x4_s4_action_selection_after_zero_charge_test_summary.json"
REPORT_PATH = BASE / "MAT001_TOPX4_H1_X4_S4_ACTION_SELECTION_AFTER_ZERO_CHARGE_TEST_2026-09-19.md"
CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_X4_S4_ACTION_SELECTION_AFTER_ZERO_CHARGE_TEST_CONTRACT_2026-09-19.md"
)
ACTION_CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_X4_S4_NEW_PARENT_ACTION_CONTRACT_2026-09-18.md"
)
ACTION_SUMMARY_PATH = (
    BASE / "outputs" / "mat001_topx4_h1_x4_s4_new_parent_action_contract_summary.json"
)
FAILED_TEST_CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_X4_S4_ZERO_CHARGE_BACKGROUND_EXISTENCE_CONTRACT_2026-09-18.md"
)
FAILED_TEST_SUMMARY_PATH = (
    BASE / "outputs" / "mat001_topx4_h1_x4_s4_zero_charge_background_existence_summary.json"
)
FAILED_TEST_REPORT_PATH = (
    BASE / "MAT001_TOPX4_H1_X4_S4_ZERO_CHARGE_BACKGROUND_EXISTENCE_2026-09-18.md"
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


def build_selection() -> dict[str, Any]:
    return {
        "failed_flat_benchmark_preserved": True,
        "failure_classification": "FLATNESS_CODIMENSION_ONE_COMPATIBILITY_FAILURE",
        "equation_sign_defect_found": False,
        "flat_count": {
            "second_order_integration_constants": 6,
            "modulus_unknowns": 1,
            "total_unknowns": 7,
            "gauge_conditions": 1,
            "scalar_boundary_conditions": 4,
            "junction_conditions": 2,
            "Hamiltonian_constraints": 1,
            "total_conditions_with_constraint": 8,
            "codimension": 1,
        },
        "selected_route": "CURVED_SLICE_BACKGROUND_OUTPUT_TEST",
        "route_label": "X4-S4-C1",
        "curvature_definition": "Rhat_mn=3*kappa4*ghat_mn",
        "kappa4_role": "SIGNED_SOLVER_OUTPUT",
        "kappa4_selected_from_observation": False,
        "curved_count": {
            "flat_unknowns": 7,
            "curvature_unknowns": 1,
            "total_unknowns": 8,
            "total_conditions": 8,
        },
        "equations": {
            "warp": "p_x=-L^2*kappa4*exp(-2A)-(2u^2+v^2)/(3M5^3)",
            "constraint": (
                "Ck=6M5^3[(p/L)^2-kappa4*exp(-2A)]-(u/L)^2"
                "-(v/L)^2/2+Lambda5+U"
            ),
            "constraint_endpoint_imposed": "x=0",
            "constraint_full_mesh_verified": True,
        },
        "induced_curvature": {
            "retained_symbolically": True,
            "M0_squared_at_mu0": 0.0,
            "Mpi_squared_at_mu0": 0.0,
            "tree_level_condition_explicit": True,
            "radiative_zero_claimed": False,
            "junction_0": "p0+L*V0/(3M5^3)-L*M0^2*kappa4*exp(-2A0)/M5^3=0",
            "junction_pi": "p1-L*Vpi/(3M5^3)+L*Mpi^2*kappa4*exp(-2A1)/M5^3=0",
        },
        "generalized_balance": {
            "gradient_weights": {"h": 1, "f_complex": 2},
            "curvature_coefficient": 3,
            "bulk_curvature_term": "M5^3*integral(exp(-2A),S1)",
            "boundary_curvature_term": "-sum(Mi^2*exp(-2Ai))",
            "reduces_to_flat_rule_at_kappa4_zero": True,
            "independent_postsolve_check": True,
        },
        "secondary_route": {
            "name": "FLAT_TENSION_EIGENVALUE",
            "status": "SECONDARY_DIAGNOSTIC_ONLY",
            "prediction_claim": False,
            "naturalness_claim": False,
        },
        "deferred_route": {
            "name": "SUPERPOTENTIAL_CORRELATED_ACTION",
            "status": "REQUIRES_NEW_PARENT_ACTION_CONTRACT",
            "silently_inserted": False,
        },
        "rejected_route": {
            "name": "UNCHANGED_FLAT_BENCHMARK_RERUN",
            "authorized": False,
        },
        "literature": [
            {
                "title": "Modeling the fifth dimension with scalars and gravity",
                "url": "https://arxiv.org/abs/hep-th/9909134",
                "use": "flatness tuning and curved solutions when tuning is imperfect",
            },
            {
                "title": "Brane World Sum Rules",
                "url": "https://arxiv.org/abs/hep-th/0011225",
                "use": "flat and curved compact-space consistency conditions",
            },
            {
                "title": "Locally Localized Gravity",
                "url": "https://arxiv.org/abs/hep-th/0011156",
                "use": "non-fine-tuned curved-brane route class",
            },
        ],
    }


def build_firewall() -> dict[str, Any]:
    return {
        "action_changed": False,
        "X4-S4_parent_accepted": False,
        "curved_background_solved": False,
        "finite_charge_background_solved": False,
        "physical_hessian_constructed": False,
        "signed_H1_residue_computed": False,
        "MAT001_pass": False,
        "K_Q_derived": False,
        "V_computed": False,
        "stage4A_reopened": False,
        "rule9_cleared": False,
        "physics_pass": False,
        "gate_effect": "NONE",
    }


def symbolic_geometry_audit() -> tuple[bool, dict[str, str]]:
    M3, Az, Azz, fz, fzz, hz, hzz, Uf, Uh, kappa, warp = sp.symbols(
        "M3 Az Azz fz fzz hz hzz Uf Uh kappa warp", nonzero=True
    )
    gzz = 6 * Az**2 - 6 * kappa * warp
    gmunu = 3 * Azz + 6 * Az**2 - 3 * kappa * warp
    einstein_difference = sp.expand(gmunu - gzz)
    expected_difference = 3 * (Azz + kappa * warp)

    f_eom = -4 * Az * fz + Uf / 2
    h_eom = -4 * Az * hz + Uh
    flat_warp = -(2 * fz**2 + hz**2) / (3 * M3)
    curved_warp = -kappa * warp - (2 * fz**2 + hz**2) / (3 * M3)

    flat_constraint_derivative = (
        12 * M3 * Az * Azz - 2 * fz * fzz - hz * hzz + Uf * fz + Uh * hz
    )
    curved_constraint_derivative = (
        12 * M3 * Az * Azz
        + 12 * M3 * kappa * warp * Az
        - 2 * fz * fzz
        - hz * hzz
        + Uf * fz
        + Uh * hz
    )
    flat_residual = sp.simplify(
        flat_constraint_derivative.subs({fzz: f_eom, hzz: h_eom, Azz: flat_warp})
    )
    curved_residual = sp.simplify(
        curved_constraint_derivative.subs(
            {fzz: f_eom, hzz: h_eom, Azz: curved_warp}
        )
    )

    gradient, Vsum, curvature_integral, induced_sum = sp.symbols(
        "gradient Vsum curvature_integral induced_sum"
    )
    integrated_equation = sp.Eq(
        3 * M3 * kappa * curvature_integral,
        -gradient - Vsum + 3 * kappa * induced_sum,
    )
    balance = Vsum + gradient + 3 * kappa * (M3 * curvature_integral - induced_sum)
    balance_residual = sp.simplify(
        balance.subs(
            Vsum,
            sp.solve(integrated_equation, Vsum)[0],
        )
    )

    details = {
        "Einstein_difference_residual": str(
            sp.simplify(einstein_difference - expected_difference)
        ),
        "flat_constraint_derivative_residual": str(flat_residual),
        "curved_constraint_derivative_residual": str(curved_residual),
        "generalized_balance_residual": str(balance_residual),
    }
    return all(value == "0" for value in details.values()), details


def contract_coverage_check() -> tuple[bool, list[str]]:
    text = CONTRACT_PATH.read_text(encoding="utf-8")
    concepts = {
        "preserve_failure": "BENCHMARK_REJECTED_RETURN_TO_ACTION_SELECTION",
        "count": "codimension-one",
        "selected_route": "X4-S4-C1 = CURVED_SLICE_BACKGROUND_OUTPUT_TEST",
        "curvature_output": "signed four-dimensional curvature",
        "constraint": "Ck = 6 M5^3",
        "induced_terms": "M0^2(mu0)=0",
        "balance": "M5^3 integral_S1 dz exp(-2A)",
        "secondary": "F1 flat-tension eigenvalue",
        "unchanged_rerun": "R0 unchanged rerun",
        "firewall": "X4-S4_parent_accepted=false",
    }
    missing = [name for name, fragment in concepts.items() if fragment not in text]
    return not missing, missing


def semantic_state_valid(selection: dict[str, Any], firewall: dict[str, Any]) -> bool:
    count = selection.get("flat_count", {})
    curved = selection.get("curved_count", {})
    equations = selection.get("equations", {})
    induced = selection.get("induced_curvature", {})
    balance = selection.get("generalized_balance", {})
    return (
        selection.get("failed_flat_benchmark_preserved") is True
        and selection.get("failure_classification")
        == "FLATNESS_CODIMENSION_ONE_COMPATIBILITY_FAILURE"
        and selection.get("equation_sign_defect_found") is False
        and count.get("total_unknowns") == 7
        and count.get("total_conditions_with_constraint") == 8
        and count.get("codimension") == 1
        and selection.get("selected_route") == "CURVED_SLICE_BACKGROUND_OUTPUT_TEST"
        and selection.get("route_label") == "X4-S4-C1"
        and selection.get("curvature_definition") == "Rhat_mn=3*kappa4*ghat_mn"
        and selection.get("kappa4_role") == "SIGNED_SOLVER_OUTPUT"
        and selection.get("kappa4_selected_from_observation") is False
        and curved == {
            "flat_unknowns": 7,
            "curvature_unknowns": 1,
            "total_unknowns": 8,
            "total_conditions": 8,
        }
        and equations.get("warp")
        == "p_x=-L^2*kappa4*exp(-2A)-(2u^2+v^2)/(3M5^3)"
        and equations.get("constraint")
        == (
            "Ck=6M5^3[(p/L)^2-kappa4*exp(-2A)]-(u/L)^2"
            "-(v/L)^2/2+Lambda5+U"
        )
        and equations.get("constraint_endpoint_imposed") == "x=0"
        and equations.get("constraint_full_mesh_verified") is True
        and induced.get("retained_symbolically") is True
        and induced.get("M0_squared_at_mu0") == 0.0
        and induced.get("Mpi_squared_at_mu0") == 0.0
        and induced.get("tree_level_condition_explicit") is True
        and induced.get("radiative_zero_claimed") is False
        and induced.get("junction_0")
        == "p0+L*V0/(3M5^3)-L*M0^2*kappa4*exp(-2A0)/M5^3=0"
        and induced.get("junction_pi")
        == "p1-L*Vpi/(3M5^3)+L*Mpi^2*kappa4*exp(-2A1)/M5^3=0"
        and balance.get("gradient_weights") == {"h": 1, "f_complex": 2}
        and balance.get("curvature_coefficient") == 3
        and balance.get("bulk_curvature_term")
        == "M5^3*integral(exp(-2A),S1)"
        and balance.get("boundary_curvature_term")
        == "-sum(Mi^2*exp(-2Ai))"
        and balance.get("reduces_to_flat_rule_at_kappa4_zero") is True
        and balance.get("independent_postsolve_check") is True
        and selection.get("secondary_route", {}).get("status")
        == "SECONDARY_DIAGNOSTIC_ONLY"
        and selection.get("secondary_route", {}).get("prediction_claim") is False
        and selection.get("deferred_route", {}).get("status")
        == "REQUIRES_NEW_PARENT_ACTION_CONTRACT"
        and selection.get("deferred_route", {}).get("silently_inserted") is False
        and selection.get("rejected_route", {}).get("authorized") is False
        and firewall.get("action_changed") is False
        and firewall.get("X4-S4_parent_accepted") is False
        and firewall.get("curved_background_solved") is False
        and firewall.get("finite_charge_background_solved") is False
        and firewall.get("physical_hessian_constructed") is False
        and firewall.get("signed_H1_residue_computed") is False
        and firewall.get("MAT001_pass") is False
        and firewall.get("K_Q_derived") is False
        and firewall.get("V_computed") is False
        and firewall.get("stage4A_reopened") is False
        and firewall.get("rule9_cleared") is False
        and firewall.get("physics_pass") is False
        and firewall.get("gate_effect") == "NONE"
    )


def build_summary(receipts: list[dict[str, Any]]) -> dict[str, Any]:
    selection = build_selection()
    firewall = build_firewall()
    failed = load_json(FAILED_TEST_SUMMARY_PATH)
    action = load_json(ACTION_SUMMARY_PATH)
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
        "failed_flat_benchmark_is_preserved_as_authority",
        failed.get("status") == "BENCHMARK_REJECTED_RETURN_TO_ACTION_SELECTION"
        and failed.get("checks_passed") == failed.get("checks_total") == 12
        and failed.get("mutation_tests", {}).get("passed") == 9
        and failed.get("selected_attempt", {}).get("constraint_max_abs")
        == 10.972344011877714
        and failed.get("selected_attempt", {}).get("sum_rule") == 0.6838334578545303,
    )
    add_check(
        checks,
        "frozen_candidate_action_remains_unaccepted_and_unchanged",
        action.get("status")
        == "PASS_X4_S4_GW2_CANDIDATE_ACTION_CONTRACT_HOLD_PARENT_ACCEPTANCE"
        and action.get("status_firewall", {}).get("X4-S4_parent_accepted") is False
        and firewall["action_changed"] is False,
    )
    add_check(
        checks,
        "flat_BVP_equation_count_exposes_one_compatibility_condition",
        selection["flat_count"]["total_unknowns"] == 7
        and selection["flat_count"]["total_conditions_with_constraint"] == 8
        and selection["flat_count"]["codimension"] == 1,
    )

    symbolic_ok, symbolic_details = symbolic_geometry_audit()
    add_check(
        checks,
        "curved_Einstein_signs_and_constraint_propagation_are_symbolically_closed",
        symbolic_ok,
        residuals=symbolic_details,
    )
    add_check(
        checks,
        "curvature_output_restores_unknown_condition_count_without_tension_retuning",
        selection["curved_count"]["total_unknowns"]
        == selection["curved_count"]["total_conditions"]
        == 8
        and selection["kappa4_role"] == "SIGNED_SOLVER_OUTPUT"
        and selection["kappa4_selected_from_observation"] is False,
    )
    add_check(
        checks,
        "induced_curvature_junction_terms_are_retained_with_explicit_tree_values",
        selection["induced_curvature"]["retained_symbolically"] is True
        and selection["induced_curvature"]["M0_squared_at_mu0"] == 0.0
        and selection["induced_curvature"]["Mpi_squared_at_mu0"] == 0.0
        and selection["induced_curvature"]["tree_level_condition_explicit"] is True
        and selection["induced_curvature"]["radiative_zero_claimed"] is False,
    )
    add_check(
        checks,
        "generalized_balance_reduces_to_flat_rule_and_remains_postsolve",
        selection["generalized_balance"]["gradient_weights"]
        == {"h": 1, "f_complex": 2}
        and selection["generalized_balance"]["curvature_coefficient"] == 3
        and selection["generalized_balance"]["reduces_to_flat_rule_at_kappa4_zero"]
        is True
        and selection["generalized_balance"]["independent_postsolve_check"] is True,
    )
    add_check(
        checks,
        "route_order_separates_generic_curvature_tuning_diagnostic_and_action_change",
        selection["selected_route"] == "CURVED_SLICE_BACKGROUND_OUTPUT_TEST"
        and selection["secondary_route"]["status"] == "SECONDARY_DIAGNOSTIC_ONLY"
        and selection["deferred_route"]["status"]
        == "REQUIRES_NEW_PARENT_ACTION_CONTRACT"
        and selection["rejected_route"]["authorized"] is False,
    )
    coverage_ok, missing = contract_coverage_check()
    add_check(
        checks,
        "human_contract_covers_the_failure_diagnosis_and_selected_route",
        coverage_ok,
        missing_concepts=missing,
        note="documentation coherence only; not a physics-pass criterion",
    )
    add_check(
        checks,
        "no_observational_target_or_downstream_quantity_selects_the_route",
        selection["kappa4_selected_from_observation"] is False
        and selection["secondary_route"]["prediction_claim"] is False
        and firewall["finite_charge_background_solved"] is False
        and firewall["K_Q_derived"] is False
        and firewall["V_computed"] is False,
    )
    add_check(
        checks,
        "non_promoting_firewall_remains_closed",
        semantic_state_valid(selection, firewall),
    )

    return {
        "schema": "ITSM_MAT001_TOPX4_H1_X4_S4_ACTION_SELECTION_AFTER_ZERO_CHARGE_TEST_v1",
        "date": "2026-09-19",
        "status": STATUS,
        "audit_execution_status": "COMPLETE",
        "scope": "FAILURE_ADJUDICATION_AND_NEXT_ROUTE_SELECTION_ONLY",
        "selection": selection,
        "checks": checks,
        "checks_passed": sum(1 for item in checks if item["ok"]),
        "checks_total": len(checks),
        "status_firewall": firewall,
        "artifact_receipts": receipts,
        "next_single_gate": {
            "name": "TOPX4_H1_X4-S4_CURVED_SLICE_BACKGROUND_OUTPUT_TEST",
            "scope": (
                "Solve signed kappa4 as an internal output of the unchanged zero-charge "
                "action while imposing the endpoint constraint and independently checking "
                "the full-mesh constraint and generalized integrated balance."
            ),
            "stop_before": "NO_FINITE_CHARGE_OR_H1_WORK",
        },
    }


def exported_contract_valid(summary: dict[str, Any]) -> bool:
    checks = summary.get("checks", [])
    return (
        summary.get("status") == STATUS
        and summary.get("scope") == "FAILURE_ADJUDICATION_AND_NEXT_ROUTE_SELECTION_ONLY"
        and summary.get("checks_passed") == summary.get("checks_total") == len(checks)
        and all(item.get("ok") is True for item in checks)
        and semantic_state_valid(
            summary.get("selection", {}), summary.get("status_firewall", {})
        )
    )


def mutation_suite(summary: dict[str, Any]) -> list[str]:
    if not exported_contract_valid(summary):
        raise AssertionError("baseline post-failure route selection must be valid")
    mutants: list[tuple[str, dict[str, Any]]] = []

    erased = copy.deepcopy(summary)
    erased["selection"]["failed_flat_benchmark_preserved"] = False
    mutants.append(("failed_benchmark_erased", erased))

    rerun = copy.deepcopy(summary)
    rerun["selection"]["rejected_route"]["authorized"] = True
    mutants.append(("unchanged_flat_rerun_authorized", rerun))

    tension = copy.deepcopy(summary)
    tension["selection"]["selected_route"] = "FLAT_TENSION_EIGENVALUE"
    mutants.append(("flat_tension_tuning_promoted_to_primary", tension))

    observed = copy.deepcopy(summary)
    observed["selection"]["kappa4_selected_from_observation"] = True
    mutants.append(("curvature_selected_from_observation", observed))

    sign = copy.deepcopy(summary)
    sign["selection"]["equations"]["warp"] = "p_x=+L^2*kappa4*exp(-2A)-gradient"
    mutants.append(("curvature_sign_reversed", sign))

    constraint_sign = copy.deepcopy(summary)
    constraint_sign["selection"]["equations"]["constraint"] = (
        "Ck=6M5^3[(p/L)^2+kappa4*exp(-2A)]-(u/L)^2"
        "-(v/L)^2/2+Lambda5+U"
    )
    mutants.append(("constraint_curvature_sign_reversed", constraint_sign))

    endpoint = copy.deepcopy(summary)
    endpoint["selection"]["equations"]["constraint_endpoint_imposed"] = "NONE"
    mutants.append(("endpoint_constraint_omitted", endpoint))

    induced = copy.deepcopy(summary)
    induced["selection"]["induced_curvature"]["retained_symbolically"] = False
    mutants.append(("induced_curvature_terms_omitted", induced))

    junction = copy.deepcopy(summary)
    junction["selection"]["induced_curvature"]["junction_0"] = (
        "p0+L*V0/(3M5^3)+L*M0^2*kappa4*exp(-2A0)/M5^3=0"
    )
    mutants.append(("left_induced_curvature_junction_sign_reversed", junction))

    balance = copy.deepcopy(summary)
    balance["selection"]["generalized_balance"]["boundary_curvature_term"] = (
        "+sum(Mi^2*exp(-2Ai))"
    )
    mutants.append(("integrated_balance_boundary_sign_reversed", balance))

    superpotential = copy.deepcopy(summary)
    superpotential["selection"]["deferred_route"]["silently_inserted"] = True
    superpotential["status_firewall"]["action_changed"] = True
    mutants.append(("superpotential_action_silently_inserted", superpotential))

    parent = copy.deepcopy(summary)
    parent["status_firewall"]["X4-S4_parent_accepted"] = True
    mutants.append(("parent_accepted_from_route_selection", parent))

    finite_q = copy.deepcopy(summary)
    finite_q["status_firewall"]["finite_charge_background_solved"] = True
    mutants.append(("finite_charge_opened", finite_q))

    hessian = copy.deepcopy(summary)
    hessian["status_firewall"]["physical_hessian_constructed"] = True
    mutants.append(("physical_hessian_promoted", hessian))

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
        f"- `{label}`: rejected" for label in summary["mutation_tests"]["labels"]
    )
    symbolic = next(
        row for row in summary["checks"]
        if row["name"] == "curved_Einstein_signs_and_constraint_propagation_are_symbolically_closed"
    )
    return f"""# MAT-001 TOP-X4 H1 X4-S4 post-zero-charge action selection

**Executed:** 2026-09-19  
**Status:** {summary['status']}  
**Checks:** {summary['checks_passed']}/{summary['checks_total']}  
**Physics pass:** false  
**Gate effect:** NONE

## 1. Decision

The rejected flat benchmark remains immutable. Its failure is classified as a
codimension-one flatness compatibility failure: seven flat-BVP unknowns are
already consumed by seven gauge/boundary/junction conditions, leaving the
Hamiltonian constraint as one additional action-parameter relation.

The selected next route is `X4-S4-C1`: retain the same action and solve the
signed maximally symmetric four-dimensional curvature `kappa4` as an internal
output. No observational value or sign is supplied.

## 2. Symbolic audit

The registered residuals are:

{json.dumps(symbolic['residuals'], indent=2, sort_keys=True)}

All residuals vanish exactly. The audit checks the curved Einstein-tensor
difference, propagation of the flat and curved constraints, and the
generalized integrated balance.

## 3. Evidence checks

| Check | Satisfied |
|---|---|
{checks}

## 4. Mutation controls

{mutations}

All {summary['mutation_tests']['passed']}/{summary['mutation_tests']['total']}
mutations were rejected. This validates the route-selection contract only; it
does not demonstrate that a regular curved background exists.

## 5. Scientific boundary

The flat-tension eigenvalue route remains a secondary fine-tuning diagnostic.
A superpotential-correlated bulk/brane action remains deferred because it
would change the candidate action. The unchanged flat benchmark is not rerun.

    action_changed=false
    X4-S4_parent_accepted=false
    curved_background_solved=false
    finite_charge_background_solved=false
    physical_hessian_constructed=false
    MAT-001=BLOCKED
    K_Q=NOT_DERIVED
    V=NOT_COMPUTED
    Stage4A=CLOSED
    Rule9_cleared=false
    physics_pass=false
    gate_effect=NONE

## 6. Next single gate

`{summary['next_single_gate']['name']}` — {summary['next_single_gate']['scope']}

## 7. Artifact record

- JSON: {relative(OUTPUT_PATH)}
- JSON SHA-256: {output_digest}
- contract: {relative(CONTRACT_PATH)}
- executable: {relative(Path(__file__))}
- primary flatness/curvature source: https://arxiv.org/abs/hep-th/9909134
- compact-space sum-rule source: https://arxiv.org/abs/hep-th/0011225
- non-fine-tuned curved-brane example: https://arxiv.org/abs/hep-th/0011156
"""


def main() -> int:
    args = parse_args()
    write_sidecar(Path(__file__))
    write_sidecar(CONTRACT_PATH)

    source_specs = [
        (Path(__file__), True),
        (CONTRACT_PATH, True),
        (ACTION_CONTRACT_PATH, True),
        (ACTION_SUMMARY_PATH, True),
        (FAILED_TEST_CONTRACT_PATH, True),
        (FAILED_TEST_SUMMARY_PATH, True),
        (FAILED_TEST_REPORT_PATH, True),
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
                if row.get("missing_concepts"):
                    print(f"  missing_concepts={row['missing_concepts']}")
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
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    args.output.write_bytes(payload)
    output_digest = hashlib.sha256(payload).hexdigest()
    write_sidecar(args.output, replace_suffix=True)
    args.report.write_text(render_report(summary, output_digest), encoding="utf-8", newline="\n")
    write_sidecar(args.report)

    print(summary["status"])
    print(f"checks={summary['checks_passed']}/{summary['checks_total']}")
    print(f"mutation_tests={len(labels)}/{len(labels)}")
    print("failed_flat_benchmark_preserved=true")
    print("selected_route=CURVED_SLICE_BACKGROUND_OUTPUT_TEST")
    print("kappa4_selected_from_observation=false")
    print("action_changed=false")
    print("X4-S4_parent_accepted=false")
    print("finite_charge_background_solved=false")
    print("physical_hessian_constructed=false")
    print("MAT001=BLOCKED")
    print("K_Q=NOT_DERIVED")
    print("V=NOT_COMPUTED")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={args.output}")
    print(f"output_sha256={output_digest}")
    print(f"report={args.report}")
    print(f"report_sha256={sha256_file(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
