#!/usr/bin/env python3
"""WAK-001 fail-closed microscopic-identity evidence inventory."""

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
        "--core-architecture",
        type=Path,
        default=repo / "Theory" / "Core" / "ITSM_Core_Architecture.md",
    )
    parser.add_argument(
        "--core-recovery-plan",
        type=Path,
        default=repo / "Theory" / "Core" / "ITSM_Core_Recovery_Plan.md",
    )
    parser.add_argument(
        "--physical-basis-summary",
        type=Path,
        default=repo
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_physical_scalar_basis_summary.json",
    )
    parser.add_argument(
        "--force-summary",
        type=Path,
        default=repo
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_track_a_force_adm_cubic_summary.json",
    )
    parser.add_argument(
        "--mode-inventory-summary",
        type=Path,
        default=base / "outputs" / "wak001_route2_mode_inventory_prescreen_summary.json",
    )
    parser.add_argument(
        "--factorization-summary",
        type=Path,
        default=base / "outputs" / "wak001_zero_background_factorization_summary.json",
    )
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def load_text(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    normalized = " ".join(raw.decode("utf-8").split())
    return normalized, hashlib.sha256(raw).hexdigest().upper()


def load_json(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    document = json.loads(raw.decode("utf-8"))
    if not isinstance(document, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return document, hashlib.sha256(raw).hexdigest().upper()


def classify_identity(
    identification_map: bool,
    independent_parent: bool,
    internal_closure: bool,
) -> str:
    route_count = sum([identification_map, independent_parent, internal_closure])
    if route_count > 1:
        return "CONFLICTING_IDENTITY_DECLARATIONS"
    if identification_map:
        return "IDENTIFIED_WITH_EXISTING_MODE"
    if independent_parent:
        return "INDEPENDENT_MICROSCOPIC_MODE_DERIVED"
    if internal_closure:
        return "INTERNAL_CONSTITUTIVE_VARIABLE_DERIVED"
    return "UNRESOLVED"


def source_record(path: Path, digest: str) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": digest}


def main() -> None:
    args = parse_args()
    architecture, architecture_hash = load_text(args.core_architecture)
    recovery, recovery_hash = load_text(args.core_recovery_plan)
    physical, physical_hash = load_json(args.physical_basis_summary)
    force, force_hash = load_json(args.force_summary)
    inventory, inventory_hash = load_json(args.mode_inventory_summary)
    factorization, factorization_hash = load_json(args.factorization_summary)

    existing_modes = inventory.get("existing_declared_modes", [])
    existing_labels = [item.get("label") for item in existing_modes]
    physical_variables = physical.get("symbolic_result", {}).get("variables", [])
    forbidden = inventory.get("forbidden_inferences", {})

    # No canonical input supplies any of these three closure objects.
    actual_identity = classify_identity(False, False, False)

    checks = {
        "architecture_retains_wake_as_research_hypothesis": (
            "historical ITSM wake is retained only as a research hypothesis"
            in architecture
        ),
        "architecture_requires_autonomous_wake_data_and_dynamics": (
            "Any wake variable must have an equation of motion" in architecture
            and "initial data" in architecture
            and "energy accounting" in architecture
        ),
        "recovery_plan_requires_new_causal_wake_derivation": (
            "hyperbolic, retarded or relaxation equation with a positive energy "
            "and causal characteristics"
            in recovery
        ),
        "finite_q_physical_basis_is_verified_but_gate_is_open": (
            physical.get("subgate_status")
            == "PASS_REGULAR_FINITE_Q_PHYSICAL_SCALAR_BASIS"
            and physical.get("full_gate_status") == "IN_PROGRESS"
        ),
        "finite_q_basis_has_no_declared_W_coordinate": (
            existing_labels == ["Xi", "Q_rho", "Q_chi", "Pi"]
            and all("W=" not in variable for variable in physical_variables)
        ),
        "track_a_force_field_is_pi_not_a_declared_W_map": (
            force.get("track_a_status") == "SELECTED"
            and "pi" in force.get("symbolic_audit", {})
            .get("exact_adm_building_blocks", {})
            .get("Q", "")
        ),
        "mode_inventory_withholds_W_distinctness": (
            inventory.get("mode_independence_status") == "NOT_YET_ESTABLISHED"
            and forbidden.get("wake_is_distinct_from_Phi_U_psi") is False
            and forbidden.get("independent_physical_wake_exists") is False
        ),
        "quadratic_factorization_is_template_not_identity": (
            factorization.get("status")
            == "PASS_WAK001_ZERO_BACKGROUND_QUADRATIC_FACTORIZATION_TEMPLATE"
            and factorization.get("physics_pass") is False
        ),
        "actual_identity_is_unresolved": actual_identity == "UNRESOLVED",
        "control_identification_map_changes_classification": (
            classify_identity(True, False, False)
            == "IDENTIFIED_WITH_EXISTING_MODE"
        ),
        "control_parent_derivation_changes_classification": (
            classify_identity(False, True, False)
            == "INDEPENDENT_MICROSCOPIC_MODE_DERIVED"
        ),
        "control_conflicting_routes_fail_closed": (
            classify_identity(True, True, False)
            == "CONFLICTING_IDENTITY_DECLARATIONS"
        ),
    }
    all_ok = all(checks.values())
    status = (
        "PASS_WAK001_MICROSCOPIC_IDENTITY_EVIDENCE_INVENTORY"
        if all_ok
        else "FAIL_WAK001_MICROSCOPIC_IDENTITY_EVIDENCE_INVENTORY"
    )

    summary: dict[str, Any] = {
        "gate": "WAK-001",
        "stage": "W2.5 microscopic identity evidence inventory",
        "label": "fail-closed-canonical-evidence-inventory",
        "status": status,
        "calculation_pass": all_ok,
        "stage2_status": "IN_PROGRESS",
        "physics_pass": False,
        "physical_wake_law": "NOT_YET_DERIVED",
        "source": "J_W=0",
        "identity_status": actual_identity,
        "route_status": "ROUTE_II_CONDITIONAL; ROUTE_I_REMAINS_FALLBACK",
        "input_files": {
            "core_architecture": source_record(args.core_architecture, architecture_hash),
            "core_recovery_plan": source_record(args.core_recovery_plan, recovery_hash),
            "uvir_physical_basis": source_record(
                args.physical_basis_summary, physical_hash
            ),
            "track_a_force": source_record(args.force_summary, force_hash),
            "wak_mode_inventory": source_record(
                args.mode_inventory_summary, inventory_hash
            ),
            "wak_zero_background_factorization": source_record(
                args.factorization_summary, factorization_hash
            ),
        },
        "declared_existing_modes": existing_modes,
        "identity_route_evidence": {
            "map_W_to_existing_mode": "NOT_DECLARED",
            "independent_parent_action_derivation": "NOT_DECLARED",
            "internal_constitutive_closure_derivation": "NOT_DECLARED",
            "free_zero_background_W": (
                "adds a coordinate by construction; does not establish origin"
            ),
        },
        "candidate_dispositions": {
            "W_equals_static_force_field_psi": (
                "NOT_ESTABLISHED; static psi has no independent memory"
            ),
            "W_equals_existing_finite_q_combination": (
                "UNRESOLVED; no gauge-regular identification map is declared"
            ),
            "W_is_independent_microscopic_mode": (
                "UNRESOLVED; Route II is a Conditional calculation route"
            ),
            "W_is_internal_constitutive_variable": (
                "UNRESOLVED; Route I remains the fallback"
            ),
        },
        "checks": checks,
        "hold": "HOLD_WAK001_MICROSCOPIC_IDENTITY_MAP_UNDECLARED",
        "scientific_boundary": (
            "The canon permits a wake research sector and requires autonomous "
            "causal dynamics, but it neither identifies W with an existing "
            "finite-q mode nor derives an independent microscopic field."
        ),
        "minimum_closure_packet": {
            "identified_route": [
                "declare a gauge-regular W=F[Xi,Q_rho,Q_chi,Pi] map",
                "show no added kinetic rank and allocate stress once",
            ],
            "independent_route": [
                "derive W and its cross operators from one parent action",
                "show one additional healthy constrained canonical pair",
                "state the microscopic symmetry or constitutive origin",
            ],
            "internal_route": [
                "derive a plenum free-energy or constitutive closure",
                "derive entropy production and keep W inside T_P",
            ],
        },
        "next": (
            "Choose one closure packet only after a microscopic construction is "
            "available; do not infer the choice from the free template."
        ),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "wak001_microscopic_identity_inventory_summary.json"
    with output.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("WAK-001 microscopic identity evidence inventory")
    for name, passed in checks.items():
        print(f"  [{'OK' if passed else 'FAIL'}] {name}")
    print("STATUS:", status)
    print("MICROSCOPIC IDENTITY:", actual_identity)
    print("HOLD: HOLD_WAK001_MICROSCOPIC_IDENTITY_MAP_UNDECLARED")
    print("Physical wake law: NOT_YET_DERIVED")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
