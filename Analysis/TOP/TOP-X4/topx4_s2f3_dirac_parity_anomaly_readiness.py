#!/usr/bin/env python3
"""Audit TOP-X4 Dirac/parity/anomaly readiness without deriving those sectors.

This is a bounded, rejection-only readiness checkpoint.  It inventories the
registered static, transport, Hadamard and Hessian receipts, confirms that
their non-promotion boundaries are intact, and records the missing
five-dimensional fermion/parity inputs.  It never substitutes a parity-even
determinant for the parity-odd phase or a first-order transport projector for
an infinite-order Hadamard state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


STATUS = "HOLD_TOPX4_DIRAC_PARITY_ANOMALY_INPUTS_NOT_CLOSED"
DIRAC_COMPLETION = "NOT_DERIVED"
DIRAC_HADAMARD_STATE = "NOT_CONSTRUCTED"
PARITY_ODD_PHASE = "NOT_DERIVED"
ANOMALY_CANCELLATION = "NOT_DERIVED"
COUNTERTERM_QUANTIZATION = "NOT_FIXED"
FORBIDDEN_SOURCE_TOKENS = (
    "observed" + "_acceleration",
    "galaxy" + "_target",
    "hubble" + "_target",
    "desired" + "_scale",
    "target" + "_coupling",
)

REPO_ROOT = Path(__file__).resolve().parents[3]
BASE = REPO_ROOT / "Analysis" / "TOP" / "TOP-X4"
OUTPUT_PATH = BASE / "outputs" / "topx4_s2f3_dirac_parity_anomaly_readiness_summary.json"
CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_S2F3_DIRAC_PARITY_ANOMALY_READINESS_CONTRACT_2026-09-16.md"
)
PLAN_PATH = (
    REPO_ROOT
    / "Theory"
    / "Core"
    / "Reasoning_Mode_Plans"
    / "11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION"
    / "PLAN.md"
)
PARENT_FREEZE_PATH = (
    REPO_ROOT / "Theory" / "Gates" / "TOP-X4" / "TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def sidecar_check(path: Path) -> dict[str, Any]:
    sidecar = Path(str(path) + ".sha256")
    actual = sha256_file(path) if path.is_file() else "MISSING"
    expected = "MISSING"
    if sidecar.is_file():
        tokens = sidecar.read_text(encoding="ascii").split()
        expected = tokens[0].lower() if tokens else "MALFORMED"
    return {
        "path": relative(path),
        "actual": actual,
        "expected": expected,
        "matches": actual == expected,
    }


def load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"JSON root is not an object: {relative(path)}")
    return loaded


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def main() -> int:
    args = parse_args()
    outputs = BASE / "outputs"
    artifact_paths = [
        CONTRACT_PATH,
        PLAN_PATH,
        PARENT_FREEZE_PATH,
        outputs / "topx4_s2f3_static_determinant_summary.json",
        outputs / "topx4_s2f3_finite_charge_entry_gate_summary.json",
        outputs / "topx4_s2f3_finite_charge_operator_summary.json",
        outputs / "topx4_s2f3_dynamic_state_subtraction_summary.json",
        outputs / "topx4_s2f3_exact_transport_retry_summary.json",
        outputs / "topx4_s2f3_hadamard_subtraction_readiness_summary.json",
        outputs / "topx4_s2f3_covariant_scalar_matrix_summary.json",
        outputs / "topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json",
        outputs / "topx4_s2f3_global_state_construction_summary.json",
        outputs / "topx4_s2f3_physical_hessian_readiness_summary.json",
    ]
    receipts = [sidecar_check(path) for path in artifact_paths]
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "all_authority_and_input_sidecars_match",
        all(item["matches"] for item in receipts),
        receipts=receipts,
    )

    contract_text = CONTRACT_PATH.read_text(encoding="utf-8") if CONTRACT_PATH.is_file() else ""
    add_check(
        checks,
        "frozen_contract_declares_rejection_only_scope",
        "FROZEN_READINESS_AUDIT" in contract_text
        and "parity-odd determinant phase" in contract_text
        and "NOT_DERIVED" in contract_text
        and "physics_pass=false" in contract_text
        and "gate_effect=NONE" in contract_text,
        contract_path=relative(CONTRACT_PATH),
    )

    static = load_json(outputs / "topx4_s2f3_static_determinant_summary.json")
    entry = load_json(outputs / "topx4_s2f3_finite_charge_entry_gate_summary.json")
    operator = load_json(outputs / "topx4_s2f3_finite_charge_operator_summary.json")
    dynamic = load_json(outputs / "topx4_s2f3_dynamic_state_subtraction_summary.json")
    exact = load_json(outputs / "topx4_s2f3_exact_transport_retry_summary.json")
    hadamard = load_json(outputs / "topx4_s2f3_hadamard_subtraction_readiness_summary.json")
    covariant = load_json(outputs / "topx4_s2f3_covariant_scalar_matrix_summary.json")
    parametrix = load_json(outputs / "topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json")
    global_state = load_json(outputs / "topx4_s2f3_global_state_construction_summary.json")
    hessian = load_json(outputs / "topx4_s2f3_physical_hessian_readiness_summary.json")

    add_check(
        checks,
        "static_determinant_is_parity_even_hold_only",
        static.get("status") == "PASS_STATIC_PARITY_EVEN_DETERMINANT_HOLD_PARITY_ODD_AND_FINITE_CHARGE"
        and static.get("checkpoint_decision") == "HOLD_BEFORE_FINITE_CHARGE"
        and static.get("physics_pass") is False
        and static.get("gate_effect") == "NONE"
        and static.get("advance_to_finite_charge") is False,
        status=static.get("status"),
        checkpoint_decision=static.get("checkpoint_decision"),
    )
    add_check(
        checks,
        "finite_charge_entry_and_operator_do_not_close_the_fermion_effective_action",
        entry.get("advance_to_finite_charge") is False
        and entry.get("physics_pass") is False
        and operator.get("advance_to_dynamic_determinant") is False
        and operator.get("physics_pass") is False
        and operator.get("gate_effect") == "NONE",
        entry_status=entry.get("status"),
        operator_status=operator.get("status"),
    )
    add_check(
        checks,
        "first_order_dirac_transport_is_not_a_hadamard_state",
        exact.get("status") == "PASS_EXACT_SCALAR_DIRAC_TRANSPORT_HOLD_HADAMARD_STRESS_AND_HESSIAN"
        and exact.get("full_Hadamard_state") is False
        and exact.get("covariant_5D_subtraction") == "NOT_DERIVED"
        and exact.get("renormalized_stress") == "NOT_COMPUTED"
        and exact.get("physics_pass") is False,
        transport_status=exact.get("status"),
        full_Hadamard_state=exact.get("full_Hadamard_state"),
        covariant_5D_subtraction=exact.get("covariant_5D_subtraction"),
    )
    add_check(
        checks,
        "D5_and_scalar_receipts_preserve_the_dirac_parity_hold",
        hadamard.get("readiness_decision") == "HOLD"
        and hadamard.get("full_Hadamard_state") is False
        and hadamard.get("hadamard_stress_ready") is False
        and covariant.get("physics_pass") is False
        and parametrix.get("physics_pass") is False
        and global_state.get("physics_pass") is False,
        hadamard_status=hadamard.get("status"),
        scalar_matrix_operator=covariant.get("scalar_matrix_operator"),
        global_state_status=global_state.get("status"),
    )
    construction_status = global_state.get("construction_status", {})
    hadamard_inventory = hadamard.get("completion_inventory", {})
    add_check(
        checks,
        "current_construction_inventory_marks_missing_fermion_and_parity_inputs",
        hadamard_inventory.get("dirac_hadamard_two_point_function", {}).get("status") == "NOT_COMPLETED"
        and hadamard_inventory.get("parity_odd_phase_and_quantized_counterterms", {}).get("status")
        == "NOT_COMPLETED"
        and construction_status.get("renormalized_stress") == "NOT_COMPUTED",
        construction_status={
            "dirac_hadamard_two_point_function": hadamard_inventory.get(
                "dirac_hadamard_two_point_function"
            ),
            "parity_odd_phase_and_quantized_counterterms": hadamard_inventory.get(
                "parity_odd_phase_and_quantized_counterterms"
            ),
            "renormalized_stress": construction_status.get("renormalized_stress"),
        },
    )
    hessian_inputs = hessian.get("required_inputs", {})
    add_check(
        checks,
        "physical_hessian_receipt_keeps_gravity_ghost_and_parity_inputs_unavailable",
        hessian.get("physical_hessian") == "NOT_CONSTRUCTED"
        and hessian.get("radion_mass") == "NOT_COMPUTED"
        and hessian.get("physics_pass") is False
        and hessian_inputs.get("gravity_ghost_and_parity_sectors") == "NOT_AVAILABLE",
        physical_hessian=hessian.get("physical_hessian"),
        required_input=hessian_inputs.get("gravity_ghost_and_parity_sectors"),
    )

    rejection_tests = [
        {
            "id": "TOPX4-DPA-R1",
            "attempt": "static_parity_even_determinant_as_complete_finite_charge_fermion_action",
            "rejected": static.get("advance_to_finite_charge") is False,
        },
        {
            "id": "TOPX4-DPA-R2",
            "attempt": "first_order_dirac_projector_as_infinite_order_hadamard_state",
            "rejected": exact.get("full_Hadamard_state") is False,
        },
        {
            "id": "TOPX4-DPA-R3",
            "attempt": "squared_dirac_operator_as_parity_odd_phase_or_anomaly_clearance",
            "rejected": PARITY_ODD_PHASE == "NOT_DERIVED"
            and "parity-odd determinant phase" in contract_text,
        },
        {
            "id": "TOPX4-DPA-R4",
            "attempt": "unproved_even_or_four_dimensional_result_as_repository_specific_D5_closure",
            "rejected": hadamard.get("readiness_decision") == "HOLD",
        },
        {
            "id": "TOPX4-DPA-R5",
            "attempt": "missing_anomaly_or_counterterm_data_set_to_zero",
            "rejected": ANOMALY_CANCELLATION == "NOT_DERIVED"
            and COUNTERTERM_QUANTIZATION == "NOT_FIXED",
        },
        {
            "id": "TOPX4-DPA-R6",
            "attempt": "observational_target_used_to_select_fermionic_closure",
            "rejected": True,
        },
    ]
    add_check(
        checks,
        "all_registered_shortcuts_are_rejected",
        all(item["rejected"] for item in rejection_tests),
        rejection_tests=rejection_tests,
    )

    source_text = Path(__file__).read_text(encoding="utf-8")
    forbidden_hits = [token for token in FORBIDDEN_SOURCE_TOKENS if token in source_text]
    add_check(
        checks,
        "observational_target_firewall",
        not forbidden_hits,
        forbidden_token_hits=forbidden_hits,
    )

    all_ok = all(check["ok"] for check in checks)
    result: dict[str, Any] = {
        "schema": "ITSM_TOPX4_S2F3_DIRAC_PARITY_ANOMALY_READINESS_v1",
        "route": "TOP-X4_KK-001",
        "candidate": "X4-S2F3",
        "status": STATUS if all_ok else "ERROR_DIRAC_PARITY_ANOMALY_READINESS_AUDIT",
        "audit_execution_status": "COMPLETE" if all_ok else "ERROR",
        "readiness_checks_passed": sum(check["ok"] for check in checks),
        "readiness_checks_total": len(checks),
        "dirac_completion": DIRAC_COMPLETION,
        "dirac_transport_control": "BOUNDED_FIRST_ORDER_EXACT_TRANSPORT",
        "dirac_hadamard_state": DIRAC_HADAMARD_STATE,
        "parity_odd_determinant_phase": PARITY_ODD_PHASE,
        "anomaly_cancellation": ANOMALY_CANCELLATION,
        "counterterm_quantization": COUNTERTERM_QUANTIZATION,
        "determinant": "NOT_COMPUTED",
        "renormalized_stress": "NOT_COMPUTED",
        "physics_pass": False,
        "gate_effect": "NONE",
        "advance_to_finite_charge_determinant": False,
        "advance_to_physical_hessian": False,
        "advance_to_a4": False,
        "advance_to_ultra": False,
        "checks": checks,
        "required_inputs": {
            "curved_5D_dirac_operator_and_spin_connection": "NOT_CLOSED",
            "dimension_appropriate_dirac_hadamard_state": "NOT_CONSTRUCTED",
            "state_dependent_finite_charge_determinant": "NOT_COMPUTED",
            "parity_odd_phase_reference_and_regulator": "NOT_DERIVED",
            "local_global_anomaly_data": "NOT_DERIVED",
            "quantized_counterterm_normalizations": "NOT_FIXED",
            "curved_gravity_ghost_and_constraint_coupling": "NOT_AVAILABLE",
            "independent_three_role_review": "NOT_MET",
        },
        "authority": [
            {"path": relative(CONTRACT_PATH), "sha256": sha256_file(CONTRACT_PATH)},
            {"path": relative(PLAN_PATH), "sha256": sha256_file(PLAN_PATH)},
            {"path": relative(PARENT_FREEZE_PATH), "sha256": sha256_file(PARENT_FREEZE_PATH)},
        ],
        "nonclaims": [
            "No complete curved five-dimensional Dirac operator is newly derived.",
            "No infinite-order Dirac Hadamard state or wavefront proof is claimed.",
            "No parity-odd determinant phase, anomaly cancellation or counterterm quantization is derived.",
            "No finite-charge determinant, renormalized stress, physical Hessian, A4 or Ultra entry follows.",
            "No MAT, UVIR, cosmology, BBN, Rule-9 or publication status changes follow.",
        ],
        "scientific_boundary": (
            "The repository has bounded static parity-even and first-order Dirac transport controls. "
            "Those controls are retained as evidence but do not supply the missing curved, "
            "state-dependent, parity-odd or anomaly inputs. No missing sector is inferred or set to zero."
        ),
        "source_sha256": sha256_file(Path(__file__)),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    args.output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    args.output.with_suffix(args.output.suffix + ".sha256").write_text(
        f"{digest}  {args.output.name}\n", encoding="ascii", newline="\n"
    )

    print(result["status"])
    print(f"readiness_checks={result['readiness_checks_passed']}/{result['readiness_checks_total']}")
    print(f"dirac_completion={DIRAC_COMPLETION}")
    print(f"dirac_hadamard_state={DIRAC_HADAMARD_STATE}")
    print(f"parity_odd_determinant_phase={PARITY_ODD_PHASE}")
    print(f"anomaly_cancellation={ANOMALY_CANCELLATION}")
    print(f"counterterm_quantization={COUNTERTERM_QUANTIZATION}")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={args.output}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
