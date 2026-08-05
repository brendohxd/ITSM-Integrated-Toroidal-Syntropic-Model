#!/usr/bin/env python3
"""Inventory live UVIR-003 exports required by the MAT-001 J2 projection.

This audit consumes current UVIR evidence records and classifies whether the
same-action objects K, C, B, d, h and u are available in one declared field
chart. It is intentionally fail closed: partial symbolic exports and
diagnostic impulse covectors are recorded, but they are not promoted into a
matter vertex and V remains NOT_COMPUTED.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


PASS_STATUS = "PASS_MAT001_LIVE_UVIR_EXPORT_INVENTORY_BLOCKED"
FAIL_STATUS = "FAIL_MAT001_LIVE_UVIR_EXPORT_INVENTORY"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    repo = base.parents[3]
    uvir = repo / "Analysis" / "UVIR" / "UVIR-003" / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--finite-q-summary",
        type=Path,
        default=uvir / "uvir003_scalar_adm_finite_q_summary.json",
    )
    parser.add_argument(
        "--physical-basis-summary",
        type=Path,
        default=uvir / "uvir003_physical_scalar_basis_summary.json",
    )
    parser.add_argument(
        "--source-response-summary",
        type=Path,
        default=uvir / "uvir003_source_observable_retarded_response_summary.json",
    )
    parser.add_argument(
        "--stage5-summary",
        type=Path,
        default=uvir / "uvir003_stage5_full_gate_decision_summary.json",
    )
    parser.add_argument(
        "--j2-summary",
        type=Path,
        default=mat
        / "J2_MODE_PROJECTION"
        / "outputs"
        / "mat001_j2_basis_covariant_mode_projection_summary.json",
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


def finite_q_contract(data: dict[str, Any] | None) -> bool:
    symbolic = data.get("symbolic_reduction", {}) if data else {}
    variables = symbolic.get("variables", {}) if isinstance(symbolic, dict) else {}
    return bool(
        data
        and data.get("calculation_status") == "PASS"
        and data.get("reduction_status") == "PASS_FINITE_Q_CONSTRAINT_ELIMINATION"
        and data.get("full_gate_status") == "IN_PROGRESS"
        and data.get("mat001_status") == "BLOCKED"
        and variables.get("dynamical") == ["R", "delta_rho", "vartheta"]
        and variables.get("constraints")
        == ["delta_N", "Sigma=q_phys^2*beta"]
        and isinstance(symbolic.get("constraint_matrix"), str)
        and symbolic.get("constraint_matrix", "").startswith("Matrix(")
        and isinstance(symbolic.get("constraint_source"), str)
        and symbolic.get("constraint_source", "").startswith("Matrix(")
        and "kinetic" not in symbolic
    )


def physical_basis_contract(data: dict[str, Any] | None) -> bool:
    symbolic = data.get("symbolic_result", {}) if data else {}
    return bool(
        data
        and data.get("calculation_status") == "PASS"
        and data.get("subgate_status")
        == "PASS_REGULAR_FINITE_Q_PHYSICAL_SCALAR_BASIS"
        and data.get("basis_status") == "DERIVED_AND_VERIFIED"
        and data.get("projected_vertex_status") == "NOT_YET_EVALUATED"
        and data.get("full_gate_status") == "IN_PROGRESS"
        and data.get("mat001_status") == "BLOCKED"
        and symbolic.get("variables")
        == [
            "Xi=(q_phys/H)R",
            "Q_rho=delta_rho-(rho_dot/H)R",
            "Q_chi=rho[vartheta-(mu/H)R]",
        ]
        and isinstance(symbolic.get("physical_kinetic_matrix"), str)
        and symbolic.get("physical_kinetic_matrix", "").startswith("Matrix(")
    )


def source_response_contract(data: dict[str, Any] | None) -> bool:
    method = data.get("method", {}) if data else {}
    boundary = data.get("scientific_boundary", "") if data else ""
    return bool(
        data
        and data.get("calculation_status") == "PASS"
        and data.get("subgate_status")
        == "PASS_GAUGE_PROJECTED_MATTER_RESPONSE_SURVIVES_WITH_SCOPE"
        and data.get("full_gate_status") == "IN_PROGRESS"
        and data.get("mat001_status") == "BLOCKED"
        and method.get("source_covectors") == ["Q_rho", "Q_chi"]
        and "Generalized impulses" in method.get("source_rule", "")
        and "not by itself" in boundary
        and "S-matrix amplitude" in boundary
    )


def stage5_contract(data: dict[str, Any] | None) -> bool:
    handoff = data.get("mat_handoff", {}) if data else {}
    return bool(
        data
        and data.get("calculation_status") == "PASS"
        and data.get("subgate_status") == "PASS_STAGE5_DECISION_HOLD_TIER1"
        and data.get("decision") == "HOLD_TIER1_CLOSURE"
        and data.get("full_gate_status") == "IN_PROGRESS"
        and data.get("V_status") == "NOT_COMPUTED"
        and data.get("kq_numeric_status") == "NOT_DERIVED"
        and handoff.get("allows_MAT001_PASS") is False
        and handoff.get("allows_MAT_calculation_work") is True
        and handoff.get("allows_downstream_Derived_from_MAT") is False
    )


def j2_contract(data: dict[str, Any] | None) -> bool:
    live = data.get("live_action_export", {}) if data else {}
    return bool(
        data
        and data.get("calculation_status") == "PASS"
        and data.get("subgate_status")
        == "PASS_MAT001_J2_BASIS_COVARIANT_MODE_PROJECTION_TEMPLATE"
        and data.get("live_action_export_status") == "NOT_PROVIDED"
        and data.get("numeric_matching_status")
        == "BLOCKED_LIVE_ACTION_EXPORT_REQUIRED"
        and data.get("V_status") == "NOT_COMPUTED"
        and data.get("mat001_pass") is False
        and data.get("physics_pass") is False
        and live.get("action_level_matter_source_covectors")
        == "NOT_PROVIDED_TO_THIS_TEMPLATE"
        and live.get("physical_mode_direction_in_same_chart")
        == "NOT_PROVIDED_TO_THIS_TEMPLATE"
    )


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def main() -> None:
    args = parse_args()
    inputs: dict[str, tuple[Path, Callable[[dict[str, Any] | None], bool]]] = {
        "finite_q_reduction": (args.finite_q_summary, finite_q_contract),
        "physical_scalar_basis": (args.physical_basis_summary, physical_basis_contract),
        "projected_source_response": (
            args.source_response_summary,
            source_response_contract,
        ),
        "stage5_decision": (args.stage5_summary, stage5_contract),
        "MAT_J2_template": (args.j2_summary, j2_contract),
    }

    checks: list[dict[str, Any]] = []
    evidence: dict[str, Any] = {}
    loaded: dict[str, dict[str, Any] | None] = {}
    for name, (path, contract) in inputs.items():
        data, error, digest = load_json(path)
        loaded[name] = data
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

    finite = loaded["finite_q_reduction"] or {}
    finite_symbolic = finite.get("symbolic_reduction", {})
    physical = loaded["physical_scalar_basis"] or {}
    physical_symbolic = physical.get("symbolic_result", {})
    response = loaded["projected_source_response"] or {}
    response_method = response.get("method", {})

    inventory: dict[str, Any] = {
        "K": {
            "status": "PARTIAL_EXPORTED_PHYSICAL_CHART",
            "source": "uvir003_physical_scalar_basis_summary.json",
            "chart": ["Xi", "Q_rho", "Q_chi"],
            "representation": "exact_symbolic_physical_kinetic_matrix",
            "action_level_provenance": "UVIR_scalar_ADM_reduction",
            "dimensions_in_export": "NOT_EXPLICIT",
            "ready_for_J2_live_matching": False,
        },
        "C": {
            "status": "PARTIAL_EXPORTED_ORIGINAL_CHART",
            "source": "uvir003_scalar_adm_finite_q_summary.json",
            "dynamical_chart": ["R", "delta_rho", "vartheta"],
            "constraint_chart": ["delta_N", "Sigma=q_phys^2*beta"],
            "representation": "exact_symbolic_constraint_matrix",
            "dimensions_in_export": "NOT_EXPLICIT",
            "ready_for_J2_live_matching": False,
        },
        "B": {
            "status": "PARTIAL_EMBEDDED_IN_CONSTRAINT_SOURCE",
            "source": "uvir003_scalar_adm_finite_q_summary.json",
            "chart": ["R", "delta_rho", "vartheta", "delta_N", "Sigma"],
            "representation": "field_and_velocity_dependent_J1_constraint_source",
            "isolated_template_block": False,
            "dimensions_in_export": "NOT_EXPLICIT",
            "ready_for_J2_live_matching": False,
        },
        "d": {
            "status": "NOT_EXPORTED",
            "required_role": "direct_matter_source_covector_on_dynamical_fields",
            "ready_for_J2_live_matching": False,
        },
        "h": {
            "status": "NOT_EXPORTED",
            "required_role": "matter_source_covector_on_algebraic_constraints",
            "ready_for_J2_live_matching": False,
        },
        "u": {
            "status": "NOT_SELECTED_IN_SAME_CHART",
            "available_precursor": "physical_basis_map_only",
            "projected_vertex_status": physical.get("projected_vertex_status"),
            "ready_for_J2_live_matching": False,
        },
    }

    add_check(
        checks,
        "partial_K_C_and_constraint_source_exports_detected",
        isinstance(physical_symbolic.get("physical_kinetic_matrix"), str)
        and isinstance(finite_symbolic.get("constraint_matrix"), str)
        and isinstance(finite_symbolic.get("constraint_source"), str),
    )
    add_check(
        checks,
        "diagnostic_impulses_not_relabelled_as_matter_vertex_covectors",
        response_method.get("source_covectors") == ["Q_rho", "Q_chi"]
        and inventory["d"]["status"] == "NOT_EXPORTED"
        and inventory["h"]["status"] == "NOT_EXPORTED",
    )
    add_check(
        checks,
        "same_chart_bundle_absent",
        inventory["K"]["chart"]
        != inventory["C"]["dynamical_chart"]
        and not any(item["ready_for_J2_live_matching"] for item in inventory.values()),
        kinetic_chart=inventory["K"]["chart"],
        constraint_dynamical_chart=inventory["C"]["dynamical_chart"],
    )

    blocker_map = [
        "K is exported in the physical Xi/Q_rho/Q_chi chart while C and the embedded constraint source are exported in the original R/delta_rho/vartheta chart.",
        "The mixing block B is not isolated under the J2 quadratic convention and the live constraint source contains velocity-dependent terms.",
        "The action-level matter source covectors d and h are not exported.",
        "No physical eigenmode direction u is selected in the same chart as a complete K,C,B,d,h bundle.",
        "Object dimensions and one shared normalization convention are not explicit across the live exports.",
        "Gauge-projected Q_rho/Q_chi diagnostic impulses are response probes, not the missing matter interaction covectors.",
    ]
    firewall = {
        "live_same_chart_bundle_complete": False,
        "numeric_matching_ready": False,
        "computes_numeric_V": False,
        "derives_numeric_K_Q": False,
        "reopens_stage4A": False,
        "claims_MAT_pass": False,
        "claims_UVIR_pass": False,
        "claims_downstream_Derived": False,
        "physics_pass": False,
    }
    add_check(
        checks,
        "inventory_decision_and_claim_firewall_fail_closed",
        all(value is False for value in firewall.values()),
        flags=firewall,
    )

    all_ok = all(check["ok"] for check in checks)
    subgate = PASS_STATUS if all_ok else FAIL_STATUS
    summary: dict[str, Any] = {
        "gate": "MAT-001",
        "interface": "UVIR-003_TO_MAT-001",
        "stage": "LIVE_UVIR_QUADRATIC_EXPORT_INVENTORY",
        "subgate_status": subgate,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "inventory_status": (
            "COMPLETE_BLOCKER_MAP_LIVE_BUNDLE_NOT_READY"
            if all_ok
            else "INVALID_OR_DRIFTED_INPUT_CONTRACT"
        ),
        "live_action_export_status": "PARTIAL_NOT_SAME_CHART",
        "numeric_matching_status": "BLOCKED_LIVE_ACTION_EXPORT_REQUIRED",
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "required_object_inventory": inventory,
        "inadmissible_substitutions": {
            "Q_rho_Q_chi_response_impulses_for_d_h": "REJECTED_ROLE_MISMATCH",
            "basis_map_for_selected_mode_u": "REJECTED_MAP_IS_NOT_MODE_SELECTION",
            "constraint_source_for_static_B_without_decomposition": "REJECTED_CONVENTION_MISMATCH",
        },
        "blocking_requirements": blocker_map,
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS means the repository's current live UVIR outputs have been "
            "inventoried against the MAT J2 contract and the missing same-chart bundle "
            "has been identified without substitution. It is a blocker-map pass, not a "
            "matter-coupling calculation or physics pass."
        ),
        "serial_next": (
            "Derive and export d and h from one declared matter interaction in the live "
            "quadratic action, transform K/C/B into that same named chart with explicit "
            "dimensions, then select u and rerun the J2 projection."
        ),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_live_uvir_export_inventory_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    sidecar = args.output_dir / "mat001_live_uvir_export_inventory_summary.sha256"
    sidecar.write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("MAT-001 live UVIR export inventory")
    print("  live bundle: PARTIAL_NOT_SAME_CHART")
    print("  V_status: NOT_COMPUTED | MAT: BLOCKED | Stage4A: CLOSED")
    for check in checks:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS: {0}".format(subgate))
    print("JSON_SHA256: {0}".format(digest))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
