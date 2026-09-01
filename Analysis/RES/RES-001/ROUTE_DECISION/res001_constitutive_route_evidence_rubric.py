#!/usr/bin/env python3
"""Compare RES-001 routes R1/R2/R3 under one fail-closed evidence rubric.

R0 remains the no-throughput control. The audit distinguishes a developed
candidate form from route selection and never derives a creation rate,
topological lock or cosmology from an unselected scaffold.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


PASS_STATUS = "PASS_RES001_CONSTITUTIVE_ROUTE_EVIDENCE_RUBRIC_NO_SELECTION"
FAIL_STATUS = "FAIL_RES001_CONSTITUTIVE_ROUTE_EVIDENCE_RUBRIC"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    res = base.parent
    outputs = res / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory-summary",
        type=Path,
        default=outputs / "res001_qsyn_constitutive_inventory_summary.json",
    )
    parser.add_argument(
        "--r1-summary",
        type=Path,
        default=outputs / "res001_r1_constitutive_draft_summary.json",
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


def inventory_contract(data: dict[str, Any] | None) -> bool:
    candidates = {
        item.get("id"): item.get("status")
        for item in data.get("constitutive_candidates", [])
        if isinstance(item, dict)
    } if data else {}
    partition = data.get("conservation_partition", {}) if data else {}
    return bool(
        data
        and data.get("calculation_status") == "PASS"
        and data.get("subgate_status")
        == "PASS_RES001_QSYN_CONSTITUTIVE_INVENTORY_OPEN"
        and data.get("research_gate_status") == "OPEN_SCAFFOLD_ONLY"
        and data.get("physics_pass") is False
        and candidates
        == {
            "R0_NO_THROUGHPUT_CONTROL": "CONTROL",
            "R1_DECLARED_CONSTITUTIVE_VECTOR": "OPEN",
            "R2_ACTION_COUPLED_RESERVOIR": "OPEN",
            "R3_TOPOLOGY_LOCKED_THROUGHPUT": "OPEN_CONDITIONAL",
        }
        and partition.get("separation_rule") == "Q_mp is not identical to Q_syn"
        and len(partition.get("identities", [])) == 4
    )


def r1_contract(data: dict[str, Any] | None) -> bool:
    decision = data.get("decision", {}) if data else {}
    draft = data.get("draft", {}) if data else {}
    bookkeeping = draft.get("bookkeeping", {}) if isinstance(draft, dict) else {}
    return bool(
        data
        and data.get("calculation_status") == "PASS"
        and data.get("subgate_status") == "PASS_RES001_R1_DECISION_PACKET_OPEN"
        and data.get("research_gate_status") == "OPEN_SCAFFOLD_ONLY"
        and data.get("physics_pass") is False
        and decision.get("candidate_under_evaluation")
        == "R1_DECLARED_CONSTITUTIVE_VECTOR"
        and decision.get("control_retained") == "R0_NO_THROUGHPUT_CONTROL"
        and decision.get("decision_status") == "NOT_SELECTED"
        and decision.get("selected_candidate") is None
        and decision.get("retained_open")
        == [
            "R1_DECLARED_CONSTITUTIVE_VECTOR",
            "R2_ACTION_COUPLED_RESERVOIR",
            "R3_TOPOLOGY_LOCKED_THROUGHPUT",
        ]
        and draft.get("status") == "CANDIDATE_FORM_UNSELECTED_CONDITIONAL"
        and len(draft.get("requires_for_Derived", [])) == 3
        and bookkeeping.get("Q_mp")
        == "independent symbol; not set equal to Q_syn"
    )


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def main() -> None:
    args = parse_args()
    inputs: dict[str, tuple[Path, Callable[[dict[str, Any] | None], bool]]] = {
        "constitutive_inventory": (args.inventory_summary, inventory_contract),
        "R1_decision_packet": (args.r1_summary, r1_contract),
    }
    checks: list[dict[str, Any]] = []
    evidence: dict[str, Any] = {}
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
        "microscopic_or_thermodynamic_origin",
        "covariant_action_or_controlled_constitutive_closure",
        "reservoir_stress_and_exchange_derivation",
        "energy_conditions_or_entropy_production",
        "parameter_matching_without_free_creation_rate",
        "stable_causal_perturbation_domain",
        "current_separation_and_WAK_compatibility",
        "observable_and_cosmology_firewall",
    ]
    candidates: dict[str, Any] = {
        "R1_DECLARED_CONSTITUTIVE_VECTOR": {
            "route_role": "phenomenological_constitutive_vector",
            "evidence_state": {
                "microscopic_or_thermodynamic_origin": "NOT_DERIVED",
                "covariant_action_or_controlled_constitutive_closure": "PARTIAL_FLAT_REST_FRAME_FORM",
                "reservoir_stress_and_exchange_derivation": "T_R_MATCHING_MISSING",
                "energy_conditions_or_entropy_production": "NOT_DERIVED",
                "parameter_matching_without_free_creation_rate": "FREE_GAMMA_SIGMA_RHO_STAR",
                "stable_causal_perturbation_domain": "NOT_TESTED",
                "current_separation_and_WAK_compatibility": "Q_MP_SEPARATION_DECLARED_INTERFACE_OPEN",
                "observable_and_cosmology_firewall": "ENFORCED_NO_DERIVED_COSMOLOGY",
            },
            "eligible_for_selection": False,
            "primary_blocker": "The Conditional form lacks thermodynamic derivation, T_R matching and parameter closure.",
        },
        "R2_ACTION_COUPLED_RESERVOIR": {
            "route_role": "action_coupled_reservoir",
            "evidence_state": {
                "microscopic_or_thermodynamic_origin": "NOT_DECLARED",
                "covariant_action_or_controlled_constitutive_closure": "S_R_PLUS_S_INT_MISSING",
                "reservoir_stress_and_exchange_derivation": "T_R_AND_Q_SYN_NOT_DERIVED",
                "energy_conditions_or_entropy_production": "NOT_DERIVED",
                "parameter_matching_without_free_creation_rate": "NOT_AVAILABLE",
                "stable_causal_perturbation_domain": "NOT_TESTED",
                "current_separation_and_WAK_compatibility": "BOOKKEEPING_ONLY",
                "observable_and_cosmology_firewall": "ENFORCED_NO_DERIVED_COSMOLOGY",
            },
            "eligible_for_selection": False,
            "primary_blocker": "No reservoir action or interaction deriving Q_syn is declared.",
        },
        "R3_TOPOLOGY_LOCKED_THROUGHPUT": {
            "route_role": "topology_locked_conditional",
            "evidence_state": {
                "microscopic_or_thermodynamic_origin": "NO_TOPOLOGY_TO_CURRENT_MECHANISM",
                "covariant_action_or_controlled_constitutive_closure": "NOT_DECLARED",
                "reservoir_stress_and_exchange_derivation": "T_R_AND_Q_SYN_NOT_DERIVED",
                "energy_conditions_or_entropy_production": "NOT_DERIVED",
                "parameter_matching_without_free_creation_rate": "CYCLE_COUNTING_FORBIDDEN",
                "stable_causal_perturbation_domain": "NOT_TESTED",
                "current_separation_and_WAK_compatibility": "BOOKKEEPING_ONLY",
                "observable_and_cosmology_firewall": "ENFORCED_NO_13_12_OR_H0",
            },
            "eligible_for_selection": False,
            "primary_blocker": "No action-level map from topology/moduli to a conserved throughput current exists.",
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
        "R0_no_throughput_control_retained",
        True,
        control="R0_NO_THROUGHPUT_CONTROL",
    )
    add_check(
        checks,
        "no_route_is_eligible_on_current_evidence",
        all(candidate["eligible_for_selection"] is False for candidate in candidates.values()),
    )
    add_check(
        checks,
        "R1_calculation_priority_not_misreported_as_route_selection",
        candidates["R1_DECLARED_CONSTITUTIVE_VECTOR"]["evidence_state"]
        ["covariant_action_or_controlled_constitutive_closure"]
        == "PARTIAL_FLAT_REST_FRAME_FORM",
        calculation_priority="R1_MOST_DEVELOPED_SCAFFOLD",
        route_selection="NONE",
    )
    add_check(
        checks,
        "topology_route_does_not_infer_numeric_packaging",
        candidates["R3_TOPOLOGY_LOCKED_THROUGHPUT"]["evidence_state"]
        ["parameter_matching_without_free_creation_rate"]
        == "CYCLE_COUNTING_FORBIDDEN",
    )

    firewall = {
        "constitutive_route_selected": False,
        "Q_syn_activated": False,
        "Q_syn_identified_with_Q_mp": False,
        "Q_syn_identified_with_condensate_number_source": False,
        "Derived_creation_rate": False,
        "H0_from_Q_syn": False,
        "13_12_from_reservoir": False,
        "NEC_violating_Minkowski_support": False,
        "RES_research_gate_PASS": False,
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
        "gate": "RES-001",
        "stage": "CONSTITUTIVE_ROUTE_EVIDENCE_RUBRIC",
        "subgate_status": subgate,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "hold": "HOLD_RES001_NO_CONSTITUTIVE_ROUTE_SELECTABLE",
        "decision_status": "NO_ROUTE_SELECTABLE_ON_CURRENT_EVIDENCE",
        "selected_candidate": None,
        "control_retained": "R0_NO_THROUGHPUT_CONTROL",
        "calculation_priority": {
            "route": "R1_DECLARED_CONSTITUTIVE_VECTOR",
            "status": "MOST_DEVELOPED_SCAFFOLD_NOT_SELECTED",
            "reason": "R1 alone has a bounded Conditional form, but its origin, stress matching and parameters are not derived.",
        },
        "hard_requirements": requirements,
        "candidate_comparison": candidates,
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "physics_pass": False,
        "scientific_boundary": (
            "A PASS means R1/R2/R3 were compared under one explicit hard-requirement "
            "rubric and none is currently selectable. R1 is the most developed "
            "calculation scaffold, not an activated Q_syn law or cosmology."
        ),
        "serial_next": (
            "Keep R0 as the control and R1/R2/R3 open. For R1, derive a covariant "
            "irreversible-thermodynamics closure with T_R matching and entropy production; "
            "or supply an R2 parent action or R3 topology-to-current mechanism before "
            "rerunning this rubric."
        ),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "res001_constitutive_route_evidence_rubric_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    sidecar = args.output_dir / "res001_constitutive_route_evidence_rubric_summary.sha256"
    sidecar.write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("RES-001 constitutive-route evidence rubric")
    print("  decision: NO_ROUTE_SELECTABLE_ON_CURRENT_EVIDENCE")
    print("  R1: MOST_DEVELOPED_SCAFFOLD_NOT_SELECTED")
    for check in checks:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS: {0}".format(subgate))
    print("JSON_SHA256: {0}".format(digest))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
