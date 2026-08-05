#!/usr/bin/env python3
"""Compare WAK-001 identity routes C1/C2/C3 under one evidence rubric.

The audit consumes the current route catalog and bounded WAK evidence packets.
It distinguishes calculation priority from identity selection. No candidate is
selected unless every hard requirement is supported by declared evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


PASS_STATUS = "PASS_WAK001_IDENTITY_ROUTE_EVIDENCE_RUBRIC_NO_SELECTION"
FAIL_STATUS = "FAIL_WAK001_IDENTITY_ROUTE_EVIDENCE_RUBRIC"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    wak = base.parent
    outputs = wak / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--routes-summary",
        type=Path,
        default=outputs / "wak001_identity_closure_routes_summary.json",
    )
    parser.add_argument(
        "--identity-inventory-summary",
        type=Path,
        default=outputs / "wak001_microscopic_identity_inventory_summary.json",
    )
    parser.add_argument(
        "--c2-summary",
        type=Path,
        default=outputs / "wak001_c2_independent_parent_candidate_summary.json",
    )
    parser.add_argument(
        "--hessian-summary",
        type=Path,
        default=outputs / "wak001_coupled_hessian_readiness_summary.json",
    )
    parser.add_argument(
        "--factorization-summary",
        type=Path,
        default=outputs / "wak001_zero_background_factorization_summary.json",
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


def routes_contract(data: dict[str, Any] | None) -> bool:
    routes = {
        item.get("id"): item.get("status")
        for item in data.get("closure_routes", [])
        if isinstance(item, dict)
    } if data else {}
    return bool(
        data
        and data.get("calculation_status") == "PASS"
        and data.get("subgate_status")
        == "PASS_WAK001_IDENTITY_CLOSURE_ROUTES_CATALOG"
        and data.get("microscopic_identity_status") == "UNRESOLVED"
        and data.get("hold")
        == "HOLD_WAK001_MICROSCOPIC_IDENTITY_MAP_UNDECLARED"
        and data.get("physics_pass") is False
        and routes
        == {
            "C1_IDENTIFY_WITH_EXISTING_UVIR_MODE": "BLOCKED_NO_DECLARED_MAP",
            "C2_INDEPENDENT_PARENT_ACTION": "OPEN_UNDECLARED",
            "C3_INTERNAL_CONSTITUTIVE_OF_PLENUM": "OPEN_UNDECLARED",
        }
    )


def identity_inventory_contract(data: dict[str, Any] | None) -> bool:
    dispositions = data.get("candidate_dispositions", {}) if data else {}
    return bool(
        data
        and data.get("status")
        == "PASS_WAK001_MICROSCOPIC_IDENTITY_EVIDENCE_INVENTORY"
        and data.get("calculation_pass") is True
        and data.get("identity_status") == "UNRESOLVED"
        and data.get("stage2_status") == "IN_PROGRESS"
        and data.get("physical_wake_law") == "NOT_YET_DERIVED"
        and data.get("physics_pass") is False
        and "no gauge-regular identification map" in dispositions.get(
            "W_equals_existing_finite_q_combination", ""
        )
        and "UNRESOLVED" in dispositions.get(
            "W_is_independent_microscopic_mode", ""
        )
        and "UNRESOLVED" in dispositions.get(
            "W_is_internal_constitutive_variable", ""
        )
    )


def c2_contract(data: dict[str, Any] | None) -> bool:
    decision = data.get("decision", {}) if data else {}
    parent = data.get("parent_template", {}) if data else {}
    return bool(
        data
        and data.get("calculation_status") == "PASS"
        and data.get("subgate_status")
        == "PASS_WAK001_C2_DECISION_PACKET_OPEN"
        and data.get("research_gate_status") == "OPEN_SCAFFOLD_ONLY"
        and data.get("physics_pass") is False
        and decision.get("decision_status") == "NOT_SELECTED"
        and decision.get("identity_status") == "UNRESOLVED"
        and decision.get("selected_candidate") is None
        and decision.get("retained_open")
        == [
            "C1_IDENTIFY_WITH_EXISTING_UVIR_MODE",
            "C2_INDEPENDENT_PARENT_ACTION",
            "C3_INTERNAL_CONSTITUTIVE_OF_PLENUM",
        ]
        and parent.get("status") == "CANDIDATE_TEMPLATE_INCOMPLETE"
        and len(parent.get("completeness_missing", [])) == 4
        and any(
            "covariant completion" in item
            for item in parent.get("completeness_missing", [])
        )
        and any(
            "stress tensor" in item and "metric variation" in item
            for item in parent.get("completeness_missing", [])
        )
        and any(
            "interaction S_int generating I_W" == item
            for item in parent.get("completeness_missing", [])
        )
        and any(
            "initial-data well-posedness theorem" == item
            for item in parent.get("completeness_missing", [])
        )
    )


def hessian_contract(data: dict[str, Any] | None) -> bool:
    missing = set(data.get("missing_coupled_inputs", [])) if data else set()
    return bool(
        data
        and data.get("status") == "PASS_WAK001_COUPLED_HESSIAN_READINESS_AUDIT"
        and data.get("calculation_pass") is True
        and data.get("coupled_hessian_status")
        == "NOT_CONSTRUCTIBLE_FROM_DECLARED_INPUTS"
        and data.get("mode_independence_status") == "NOT_YET_ESTABLISHED"
        and data.get("stage2_status") == "IN_PROGRESS"
        and data.get("physics_pass") is False
        and missing
        == {
            "W_cross_kinetic_mixing",
            "W_constraint_mixing",
            "W_gradient_mass_mixing",
            "unit_constraint_parent_owner",
            "joined_reduced_hessian",
        }
    )


def factorization_contract(data: dict[str, Any] | None) -> bool:
    quadratic = data.get("quadratic_factorization", {}) if data else {}
    cubic = data.get("cubic_return", {}) if data else {}
    return bool(
        data
        and data.get("status")
        == "PASS_WAK001_ZERO_BACKGROUND_QUADRATIC_FACTORIZATION_TEMPLATE"
        and data.get("calculation_pass") is True
        and data.get("stage2_status") == "IN_PROGRESS"
        and data.get("physical_wake_law") == "NOT_YET_DERIVED"
        and data.get("physics_pass") is False
        and quadratic.get("status") == "DERIVED_FOR_DECLARED_ZERO_BACKGROUND"
        and quadratic.get("nonzero_cross_derivative_count") == 0
        and cubic.get("status") == "METRIC_AND_FRAME_COUPLINGS_PRESENT"
    )


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def main() -> None:
    args = parse_args()
    inputs: dict[str, tuple[Path, Callable[[dict[str, Any] | None], bool]]] = {
        "routes_catalog": (args.routes_summary, routes_contract),
        "identity_inventory": (
            args.identity_inventory_summary,
            identity_inventory_contract,
        ),
        "C2_candidate": (args.c2_summary, c2_contract),
        "coupled_hessian_readiness": (args.hessian_summary, hessian_contract),
        "zero_background_factorization": (
            args.factorization_summary,
            factorization_contract,
        ),
    }

    evidence: dict[str, Any] = {}
    checks: list[dict[str, Any]] = []
    for name, (path, contract) in inputs.items():
        data, error, digest = load_json(path)
        exact_ok = contract(data)
        evidence[name] = {
            "source": path.name,
            "sha256": digest,
            "parse_error": error,
            "exact_contract_ok": exact_ok,
        }
        add_check(
            checks,
            f"{name}_exact_contract",
            error is None and exact_ok,
            source=path.name,
            parse_error=error,
        )

    requirements = [
        "microscopic_identity_or_constitutive_origin",
        "complete_parent_action_or_controlled_constitutive_closure",
        "stress_energy_or_entropy_accounting",
        "exact_conservation_exchange_bookkeeping",
        "coupled_mode_independence_or_no_added_rank",
        "controlled_static_limit_without_AQUAL_double_count",
        "interaction_derived_source_and_observable",
        "covariant_completion_in_declared_domain",
    ]
    candidates: dict[str, Any] = {
        "C1_IDENTIFY_WITH_EXISTING_UVIR_MODE": {
            "route_role": "identified_existing_mode",
            "evidence_state": {
                "microscopic_identity_or_constitutive_origin": "MISSING_GAUGE_REGULAR_MAP",
                "complete_parent_action_or_controlled_constitutive_closure": "NOT_TESTABLE_BEFORE_MAP",
                "stress_energy_or_entropy_accounting": "MISSING_SINGLE_ALLOCATION_PROOF",
                "exact_conservation_exchange_bookkeeping": "STRUCTURE_ONLY",
                "coupled_mode_independence_or_no_added_rank": "NOT_ESTABLISHED",
                "controlled_static_limit_without_AQUAL_double_count": "NOT_ESTABLISHED",
                "interaction_derived_source_and_observable": "NOT_DERIVED",
                "covariant_completion_in_declared_domain": "NOT_DERIVED",
            },
            "eligible_for_selection": False,
            "primary_blocker": "No declared W=F[Xi,Q_rho,Q_chi,Pi] map.",
        },
        "C2_INDEPENDENT_PARENT_ACTION": {
            "route_role": "independent_wake_sector",
            "evidence_state": {
                "microscopic_identity_or_constitutive_origin": "MISSING_INDEPENDENT_ORIGIN",
                "complete_parent_action_or_controlled_constitutive_closure": "PARTIAL_FREE_TEMPLATE_ONLY",
                "stress_energy_or_entropy_accounting": "FREE_HAMILTONIAN_ONLY_TW_MISSING",
                "exact_conservation_exchange_bookkeeping": "STRUCTURE_DECLARED_IW_UNDERIVED",
                "coupled_mode_independence_or_no_added_rank": "NOT_ESTABLISHED_HESSIAN_UNAVAILABLE",
                "controlled_static_limit_without_AQUAL_double_count": "FIREWALL_DECLARED_NOT_MATCHED",
                "interaction_derived_source_and_observable": "NOT_DERIVED",
                "covariant_completion_in_declared_domain": "NOT_DERIVED",
            },
            "eligible_for_selection": False,
            "primary_blocker": "Free template exists, but T_W, I_W, the joined Hessian and microscopic independence are not derived.",
        },
        "C3_INTERNAL_CONSTITUTIVE_OF_PLENUM": {
            "route_role": "internal_plenum_variable",
            "evidence_state": {
                "microscopic_identity_or_constitutive_origin": "MISSING_INTERNAL_CONSTITUTIVE_ORIGIN",
                "complete_parent_action_or_controlled_constitutive_closure": "NOT_DECLARED",
                "stress_energy_or_entropy_accounting": "PLENUM_FREE_ENERGY_OR_ENTROPY_LAW_MISSING",
                "exact_conservation_exchange_bookkeeping": "ROUTE_I_STRUCTURE_ONLY_NO_SEPARATE_TW",
                "coupled_mode_independence_or_no_added_rank": "NOT_ESTABLISHED",
                "controlled_static_limit_without_AQUAL_double_count": "NOT_ESTABLISHED",
                "interaction_derived_source_and_observable": "NOT_DERIVED",
                "covariant_completion_in_declared_domain": "NOT_DERIVED",
            },
            "eligible_for_selection": False,
            "primary_blocker": "No plenum free-energy or constitutive closure with entropy production is declared.",
        },
    }

    add_check(
        checks,
        "rubric_covers_every_hard_requirement_for_every_route",
        all(
            list(candidate["evidence_state"].keys()) == requirements
            for candidate in candidates.values()
        ),
    )
    add_check(
        checks,
        "no_route_is_eligible_on_current_evidence",
        all(candidate["eligible_for_selection"] is False for candidate in candidates.values()),
    )
    add_check(
        checks,
        "C2_calculation_priority_not_misreported_as_identity_selection",
        candidates["C2_INDEPENDENT_PARENT_ACTION"]["evidence_state"]
        ["complete_parent_action_or_controlled_constitutive_closure"]
        == "PARTIAL_FREE_TEMPLATE_ONLY",
        calculation_priority="C2_ROUTE_II_MOST_DEVELOPED_SCAFFOLD",
        identity_selection="NONE",
    )
    add_check(
        checks,
        "zero_background_factorization_not_extrapolated_to_cubic_decoupling",
        candidates["C2_INDEPENDENT_PARENT_ACTION"]["evidence_state"]
        ["coupled_mode_independence_or_no_added_rank"]
        == "NOT_ESTABLISHED_HESSIAN_UNAVAILABLE",
    )

    firewall = {
        "identity_route_selected": False,
        "W_identified_with_UVIR_mode": False,
        "independent_W_mode_derived": False,
        "internal_constitutive_law_derived": False,
        "source_or_damping_activated": False,
        "AQUAL_double_count_allowed": False,
        "Bullet_Cluster_packaging": False,
        "WAK_research_gate_PASS": False,
        "physics_pass": False,
    }
    add_check(
        checks,
        "decision_and_claim_firewall_fail_closed",
        all(value is False for value in firewall.values()),
        flags=firewall,
    )

    all_ok = all(check["ok"] for check in checks)
    subgate = PASS_STATUS if all_ok else FAIL_STATUS
    summary: dict[str, Any] = {
        "gate": "WAK-001",
        "stage": "IDENTITY_ROUTE_EVIDENCE_RUBRIC",
        "subgate_status": subgate,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "hold": "HOLD_WAK001_NO_IDENTITY_ROUTE_SELECTABLE",
        "decision_status": "NO_ROUTE_SELECTABLE_ON_CURRENT_EVIDENCE",
        "selected_candidate": None,
        "identity_status": "UNRESOLVED",
        "calculation_priority": {
            "route": "C2_INDEPENDENT_PARENT_ACTION",
            "status": "MOST_DEVELOPED_SCAFFOLD_NOT_SELECTED",
            "reason": "Only C2 has a bounded free parent template; the evidence required for identity selection remains absent.",
        },
        "hard_requirements": requirements,
        "candidate_comparison": candidates,
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "physics_pass": False,
        "scientific_boundary": (
            "A PASS means C1/C2/C3 were compared under one explicit hard-requirement "
            "rubric and none is currently selectable. C2 is the most developed "
            "calculation scaffold, not a chosen identity or physical wake law."
        ),
        "serial_next": (
            "Keep all routes open. If C2 continues as the calculation priority, derive "
            "T_W and I_W from one covariant S_W+S_int and construct the joined constrained "
            "Hessian before any identity selection; alternatively supply the missing C1 "
            "map or C3 constitutive closure and rerun this rubric."
        ),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "wak001_identity_route_evidence_rubric_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    sidecar = args.output_dir / "wak001_identity_route_evidence_rubric_summary.sha256"
    sidecar.write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("WAK-001 identity-route evidence rubric")
    print("  decision: NO_ROUTE_SELECTABLE_ON_CURRENT_EVIDENCE")
    print("  C2: MOST_DEVELOPED_SCAFFOLD_NOT_SELECTED")
    for check in checks:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS: {0}".format(subgate))
    print("JSON_SHA256: {0}".format(digest))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
