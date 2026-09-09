#!/usr/bin/env python3
"""Finite-charge entry gate for the TOP-X4 S2F3 Plan-11 continuation.

This is a fail-closed provenance/state gate.  It verifies the already-frozen
classical controls and the static parity-even determinant checkpoint, then
refuses to treat the static Minkowski vacuum determinant as a time-dependent
finite-charge determinant.  It does not calculate a finite-density spectrum,
backreaction stress tensor, physical radion mass, or anomaly clearance.
"""

from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path
from typing import Any


STATUS = "HOLD_TOPX4_S2F3_BEFORE_FINITE_CHARGE_QUANTUM_COMPLETION"
FORBIDDEN_SOURCE_TOKENS = (
    "observed" + "_acceleration",
    "hubble" + "_target",
    "galaxy" + "_target",
    "desired" + "_radius",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sidecar_check(path: Path) -> dict[str, Any]:
    sidecar = Path(str(path) + ".sha256")
    actual = sha256_file(path) if path.is_file() else "MISSING"
    expected = "MISSING"
    if sidecar.is_file():
        expected = sidecar.read_text(encoding="ascii").split()[0].lower()
    return {
        "path": str(path.relative_to(ROOT)),
        "actual": actual,
        "expected": expected,
        "matches": actual == expected,
    }


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "Analysis" / "TOP" / "TOP-X4"
OUTPUT_DIR = BASE / "outputs"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    input_paths = [
        BASE / "outputs" / "topx4_a1_symbolic_audit_summary.json",
        BASE / "outputs" / "topx4_a1_background_summary.json",
        BASE / "outputs" / "topx4_a2a3_reduction_radion_summary.json",
        BASE / "outputs" / "topx4_s2f3_static_determinant_summary.json",
        ROOT / "Theory" / "Gates" / "TOP-X4" / "TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md",
        ROOT / "Theory" / "Gates" / "TOP-X4" / "TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md",
    ]
    input_receipts = [sidecar_check(path) for path in input_paths]
    checks: list[dict[str, Any]] = []

    add_check(
        checks,
        "all_authority_and_input_sidecars_match",
        all(receipt["matches"] for receipt in input_receipts),
        receipts=input_receipts,
    )

    a1_symbolic = load_json(input_paths[0])
    add_check(
        checks,
        "a1_symbolic_action_metric_variation_control_is_complete",
        a1_symbolic.get("status") == "PASS_TOPX4_A1_INDEPENDENT_SYMBOLIC_AUDIT"
        and a1_symbolic.get("checks_passed") == 9
        and a1_symbolic.get("checks_total") == 9,
        status=a1_symbolic.get("status"),
        calculation_checks=f"{a1_symbolic.get('checks_passed')}/{a1_symbolic.get('checks_total')}",
    )

    a1_background = load_json(input_paths[1])
    add_check(
        checks,
        "a1_finite_charge_classical_background_control_is_complete",
        a1_background.get("status") == "PASS_TOPX4_A1_CONTROL_BACKGROUND_ONLY"
        and a1_background.get("checks_passed") == 7
        and a1_background.get("checks_total") == 7,
        status=a1_background.get("status"),
        calculation_checks=f"{a1_background.get('checks_passed')}/{a1_background.get('checks_total')}",
        max_constraint_residual=a1_background.get("max_constraint_residual"),
        max_charge_relative_error=a1_background.get("max_charge_relative_error"),
    )

    a2a3 = load_json(input_paths[2])
    add_check(
        checks,
        "a2a3_classical_radion_boundary_is_explicit",
        a2a3.get("status") == "HOLD_TOPX4_A2A3_UNSTABILIZED_CONTROL"
        and a2a3.get("calculation_checks_passed") == a2a3.get("calculation_checks_total")
        and a2a3.get("a3_disposition") == "HOLD_UNSTABILIZED_RADION",
        status=a2a3.get("status"),
        calculation_checks=f"{a2a3.get('calculation_checks_passed')}/{a2a3.get('calculation_checks_total')}",
        a3_disposition=a2a3.get("a3_disposition"),
    )

    static = load_json(input_paths[3])
    add_check(
        checks,
        "static_parity_even_determinant_checkpoint_is_complete",
        static.get("status") == "PASS_STATIC_PARITY_EVEN_DETERMINANT_HOLD_PARITY_ODD_AND_FINITE_CHARGE"
        and static.get("calculation_checks_passed") == 12
        and static.get("calculation_checks_total") == 12
        and static.get("physics_pass") is False
        and static.get("advance_to_finite_charge") is False,
        status=static.get("status"),
        calculation_checks=f"{static.get('calculation_checks_passed')}/{static.get('calculation_checks_total')}",
        quantum_definition=static.get("quantum_definition"),
    )

    ledger_text = input_paths[5].read_text(encoding="utf-8")
    registered_charge_equation = "d/dt(a^3 b rho^2 mu)=0"
    add_check(
        checks,
        "classical_global_charge_equation_is_registered_before_quantum_extension",
        "a^3b" in ledger_text and "rho^2 mu" in ledger_text and "fixed nonzero global charge" in ledger_text,
        equation=registered_charge_equation,
        ensemble="fixed nonzero global charge; no inserted chemical potential",
    )

    static_state = static.get("quantum_definition", {})
    dynamic_state_ready = bool(
        static_state.get("hadamard_adiabatic_state")
        and static_state.get("adiabatic_order_convergence")
        and static_state.get("finite_density_spectrum")
        and static_state.get("backreaction_stress_tensor")
    )
    add_check(
        checks,
        "finite_charge_quantum_state_and_stress_are_explicitly_unresolved",
        not dynamic_state_ready,
        static_state=static_state,
        required_missing=[
            "Hadamard/adiabatic state",
            "adiabatic-order convergence",
            "finite-density spectrum",
            "state-dependent backreaction stress tensor",
        ],
    )

    # The static checkpoint source is not imported or called as a dynamic
    # solver.  This is a policy firewall, not evidence that the missing
    # finite-charge determinant has been calculated.
    source_text = inspect.getsource(inspect.getmodule(main))
    forbidden_hits = [token for token in FORBIDDEN_SOURCE_TOKENS if token in source_text]
    static_solver_tokens = (
        "topx4_s2f3_" + "static_determinant_checkpoint",
        "shape_" + "polylog",
        "shape_" + "bessel",
    )
    static_solver_imported = any(token in source_text for token in static_solver_tokens)
    add_check(
        checks,
        "no_static_loop_substitution_is_attempted_in_dynamic_background",
        not static_solver_imported,
        policy="static Minkowski determinant is not inserted into evolving A1 background",
        static_solver_imported=static_solver_imported,
    )
    add_check(
        checks,
        "observational_target_firewall",
        not forbidden_hits,
        forbidden_token_hits=forbidden_hits,
    )

    safe_hold_checks = all(check["ok"] for check in checks)
    result = {
        "schema": "ITSM_TOPX4_S2F3_FINITE_CHARGE_ENTRY_GATE_v1",
        "route": "TOP-X4_KK-001",
        "candidate": "X4-S2F3",
        "status": STATUS,
        "audit_execution_status": "COMPLETE" if safe_hold_checks else "ERROR",
        "gate_checks_passed": sum(check["ok"] for check in checks),
        "gate_checks_total": len(checks),
        "physics_pass": False,
        "gate_effect": "NONE",
        "advance_to_finite_charge": False,
        "advance_to_a4": False,
        "checks": checks,
        "bounded_result": (
            "The frozen classical charge control and static parity-even determinant are available as inputs, "
            "but no finite-charge quantum state or state-dependent determinant/stress tensor is defined. "
            "The continuation is held without inserting the static vacuum formula into a time-dependent background."
        ),
        "hold_reasons": [
            "finite-density spectrum and state-dependent one-loop stress tensor are not defined",
            "Hadamard/adiabatic state and order-convergence evidence are absent",
            "parity-odd determinant phase and global-anomaly audit remain open",
            "coupled metric-radion-amplitude-phase Hessian and physical radion mass are absent",
        ],
        "required_next_artifacts": [
            "finite-charge background-field determinant with declared state and counterterms",
            "state-order convergence and cutoff/mass-ratio robustness scan",
            "parity-odd phase/global anomaly and quantized counterterm audit",
            "coupled canonical constraint reduction and Hessian",
        ],
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "topx4_s2f3_finite_charge_entry_gate_summary.json"
    payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output_path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    output_path.with_suffix(output_path.suffix + ".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="ascii", newline="\n"
    )

    print(STATUS)
    print(f"gate_checks={result['gate_checks_passed']}/{result['gate_checks_total']}")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print("advance_to_finite_charge=false")
    print(f"output={output_path}")
    print(f"sha256={digest}")
    return 0 if safe_hold_checks else 1


if __name__ == "__main__":
    raise SystemExit(main())
