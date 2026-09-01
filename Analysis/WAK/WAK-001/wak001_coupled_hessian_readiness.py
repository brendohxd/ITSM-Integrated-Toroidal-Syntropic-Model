#!/usr/bin/env python3
"""WAK-001 coupled finite-q parent-Hessian readiness audit.

This verifies the declared UVIR/force/WAK inputs and fails closed when the
cross-sector quadratic and constraint blocks needed for a genuine graft have
not been supplied. It does not alter or rerun UVIR-003.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    repo = base.parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--physical-basis-summary",
        type=Path,
        default=(
            repo
            / "Analysis"
            / "UVIR"
            / "UVIR-003"
            / "outputs"
            / "uvir003_physical_scalar_basis_summary.json"
        ),
    )
    parser.add_argument(
        "--force-summary",
        type=Path,
        default=(
            repo
            / "Analysis"
            / "UVIR"
            / "UVIR-003"
            / "outputs"
            / "uvir003_track_a_force_adm_cubic_summary.json"
        ),
    )
    parser.add_argument(
        "--action-summary",
        type=Path,
        default=base / "outputs" / "wak001_route2_action_variation_summary.json",
    )
    parser.add_argument(
        "--inventory-summary",
        type=Path,
        default=(
            base / "outputs" / "wak001_route2_mode_inventory_prescreen_summary.json"
        ),
    )
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def load_json(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    document = json.loads(raw.decode("utf-8"))
    if not isinstance(document, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return document, hashlib.sha256(raw).hexdigest().upper()


def nested(document: dict[str, Any], *keys: str) -> Any:
    value: Any = document
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def main() -> None:
    args = parse_args()
    physical, physical_hash = load_json(args.physical_basis_summary)
    force, force_hash = load_json(args.force_summary)
    action, action_hash = load_json(args.action_summary)
    inventory, inventory_hash = load_json(args.inventory_summary)

    prerequisite_checks = {
        "uvir_physical_basis_passes": (
            physical.get("subgate_status")
            == "PASS_REGULAR_FINITE_Q_PHYSICAL_SCALAR_BASIS"
        ),
        "uvir_finite_q_inertia_is_three_positive": (
            nested(physical, "representative_branch", "inertia")
            == "3_POSITIVE_0_NEGATIVE_FOR_Q_GT_0"
        ),
        "uvir_full_gate_remains_in_progress": (
            physical.get("full_gate_status") == "IN_PROGRESS"
        ),
        "track_a_force_component_passes": (
            force.get("subgate_status") == "PASS_FORCE_SECTOR_J2_COMPONENT"
        ),
        "track_a_force_mode_is_selected": force.get("track_a_status") == "SELECTED",
        "full_force_constraint_source_is_not_assembled": (
            force.get("full_J2_status") == "NOT_YET_ASSEMBLED"
        ),
        "wak_local_action_variation_passes": (
            action.get("status")
            == "PASS_WAK001_W2_1_LOCAL_VARIATION_IDENTITIES"
        ),
        "wak_mode_counting_prescreen_passes": (
            inventory.get("status")
            == "PASS_WAK001_W2_5_MODE_COUNTING_PRESCREEN"
        ),
        "wak_inputs_keep_physics_pass_false": (
            action.get("physics_pass") is False
            and inventory.get("physics_pass") is False
        ),
        "wak_source_remains_zero": (
            action.get("source") == "J_W=0"
            and inventory.get("source") == "J_W=0"
        ),
    }

    required_parent_contract = {
        "background_domain": (
            "one declared finite-q background and parameter domain shared by all sectors"
        ),
        "dynamic_field_order": ["Xi", "Q_rho", "Q_chi", "Pi", "W"],
        "constraint_field_order": (
            "lapse, scalar shift, unit-frame multiplier and any additional auxiliary fields"
        ),
        "preconstraint_kinetic_block": (
            "complete velocity Hessian before eliminating shared constraints"
        ),
        "dynamic_constraint_mixing": (
            "all W couplings to lapse, shift, frame and existing scalar variables"
        ),
        "constraint_hessian": (
            "invertible finite-q auxiliary block with declared singular-domain handling"
        ),
        "gradient_mass_block": (
            "complete spatial and algebraic quadratic block in the same normalization"
        ),
        "unit_constraint_owner": (
            "one parent-sector allocation for lambda_U and its stress contribution"
        ),
        "reduced_hessian_provenance": (
            "symbolic Schur complement derived from the declared parent blocks"
        ),
    }

    declared_interface = {
        "existing_reduced_physical_block": physical.get("basis_status")
        == "DERIVED_AND_VERIFIED",
        "factorized_force_component": force.get("track_a_status") == "SELECTED",
        "free_W_kinetic_term": action.get("calculation_pass") is True,
        "W_cross_kinetic_mixing": False,
        "W_constraint_mixing": False,
        "W_gradient_mass_mixing": False,
        "unit_constraint_parent_owner": False,
        "joined_reduced_hessian": False,
    }
    missing_inputs = [
        name
        for name, present in declared_interface.items()
        if present is False
    ]

    checks = {
        **prerequisite_checks,
        "all_prerequisites_match_declared_statuses": all(
            prerequisite_checks.values()
        ),
        "coupled_inputs_are_detected_as_incomplete": (
            missing_inputs
            == [
                "W_cross_kinetic_mixing",
                "W_constraint_mixing",
                "W_gradient_mass_mixing",
                "unit_constraint_parent_owner",
                "joined_reduced_hessian",
            ]
        ),
        "readiness_audit_fails_closed_without_fabricating_zero_mixing": bool(
            missing_inputs
        ),
    }
    all_ok = all(checks.values())
    status = (
        "PASS_WAK001_COUPLED_HESSIAN_READINESS_AUDIT"
        if all_ok
        else "FAIL_WAK001_COUPLED_HESSIAN_READINESS_AUDIT"
    )

    summary: dict[str, Any] = {
        "gate": "WAK-001",
        "stage": "W2.5 coupled finite-q parent-Hessian readiness",
        "label": "cross-sector-input-readiness-only",
        "status": status,
        "calculation_pass": all_ok,
        "stage2_status": "IN_PROGRESS",
        "coupled_hessian_status": "NOT_CONSTRUCTIBLE_FROM_DECLARED_INPUTS",
        "mode_independence_status": "NOT_YET_ESTABLISHED",
        "physics_pass": False,
        "physical_wake_law": "NOT_YET_DERIVED",
        "source": "J_W=0",
        "input_files": {
            "uvir_physical_basis": {
                "path": args.physical_basis_summary.as_posix(),
                "sha256": physical_hash,
            },
            "track_a_force": {
                "path": args.force_summary.as_posix(),
                "sha256": force_hash,
            },
            "wak_action_variation": {
                "path": args.action_summary.as_posix(),
                "sha256": action_hash,
            },
            "wak_mode_prescreen": {
                "path": args.inventory_summary.as_posix(),
                "sha256": inventory_hash,
            },
        },
        "declared_interface": declared_interface,
        "missing_coupled_inputs": missing_inputs,
        "required_parent_contract": required_parent_contract,
        "checks": checks,
        "hold": "HOLD_WAK001_COUPLED_PARENT_HESSIAN_UNDECLARED",
        "scientific_boundary": (
            "Verified reduced UVIR and free WAK pieces are available, but their "
            "direct sum is not a derived coupled theory. No W cross-sector or "
            "constraint blocks are declared, and zero mixing may not be assumed."
        ),
        "next": [
            "derive one complete pre-constraint quadratic parent action in the declared field order",
            "include W couplings to lapse, shift and the unit-frame sector",
            "derive the joined Schur complement and compare rank/inertia with W removed",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "wak001_coupled_hessian_readiness_summary.json"
    with output.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("WAK-001 coupled finite-q parent-Hessian readiness audit")
    for name, passed in checks.items():
        print(f"  [{'OK' if passed else 'FAIL'}] {name}")
    print("STATUS:", status)
    print("COUPLED HESSIAN: NOT_CONSTRUCTIBLE_FROM_DECLARED_INPUTS")
    print("HOLD: HOLD_WAK001_COUPLED_PARENT_HESSIAN_UNDECLARED")
    print("Physical wake law: NOT_YET_DERIVED")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
