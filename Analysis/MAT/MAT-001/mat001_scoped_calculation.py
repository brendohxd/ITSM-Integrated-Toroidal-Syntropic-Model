#!/usr/bin/env python3
"""MAT-001 Stage 3 (UVIR serial): scoped calculation under Conditional handoff.

Authorized by UVIR-003 Stage 2b CONDITIONAL_WITH_SCOPE handoff text only.

Computes / freezes under named premises:
  1. Architecture static weak-field reduction → C_obs form
  2. Provisional Conditional C_obs baseline (Master Plan §6 C_obs ~ 1 option)
  3. Vertex residual V := C_m/sqrt(K_Q) left NOT_COMPUTED without Derived K_Q
     but maps I_a0(C_obs, C_IR, V) from matching-route identities
  4. Declared S_int form from architecture

Does NOT:
  - issue MAT-001 PASS
  - unlock downstream Derived use
  - claim Derived K_Q or Derived C_obs from matching
  - SPARC / H0 validation
  - close UVIR-003

physics_pass: false
mat001_gate_status: SCOPED_CALCULATION_ONLY_PASS_TAG_FORBIDDEN
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    uvir = base.parents[1] / "UVIR" / "UVIR-003" / "outputs"
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument(
        "--floor-summary",
        type=Path,
        default=uvir / "uvir003_conditional_matching_floor_summary.json",
    )
    p.add_argument(
        "--stage2c-summary",
        type=Path,
        default=uvir / "uvir003_stage2c_floor_diagnostics_summary.json",
    )
    p.add_argument(
        "--matching-summary",
        type=Path,
        default=uvir / "uvir003_matching_route_program_summary.json",
    )
    return p.parse_args()


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def require(name: str, ok: bool, detail: str = "") -> None:
    if not ok:
        raise AssertionError(f"{name}" + (f": {detail}" if detail else ""))


def static_reduction() -> dict[str, Any]:
    """Architecture §5 weak-field reduction identities."""
    C_m, C_IR, C_obs, K_Q, A, G, a0, V = sp.symbols(
        "C_m C_IR C_obs K_Q A G a0 V", positive=True
    )
    C_obs_form = C_m ** sp.Rational(3, 2) / sp.sqrt(C_IR)
    # invert C_m from C_obs, C_IR
    C_m_from = sp.simplify((C_obs * sp.sqrt(C_IR)) ** sp.Rational(2, 3))
    require(
        "C_obs inversion",
        sp.simplify(C_obs_form.subs(C_m, C_m_from) - C_obs) == 0,
    )
    V_def = C_m / sp.sqrt(K_Q)
    K_Q_from_V = sp.simplify(C_m**2 / V**2)
    A_arch = C_IR / (12 * sp.pi * G * a0)
    I_a0 = sp.simplify(A_arch * a0 / K_Q_from_V)
    I_a0_closed = sp.simplify(
        C_IR ** sp.Rational(1, 3)
        * V**2
        / (12 * sp.pi * G * C_obs ** sp.Rational(4, 3))
    )
    require(
        "I_a0 closed form",
        sp.simplify(I_a0.subs(C_m, C_m_from) - I_a0_closed) == 0,
    )
    # Special convention C_m = C_IR = C => C_obs = C
    C = sp.symbols("C", positive=True)
    cobs_eq = sp.simplify(C_obs_form.subs({C_m: C, C_IR: C}))
    require("C_m=C_IR implies C_obs=C", sp.simplify(cobs_eq - C) == 0)

    return {
        "S_int_declared_form": "S_int contains -C_m rho_b psi (architecture weak-field)",
        "C_obs_form": str(C_obs_form),
        "C_m_from_Cobs_CIR": str(C_m_from),
        "V_definition": str(V_def),
        "I_a0_in_Cobs_CIR_V": str(I_a0_closed),
        "special_convention_Cm_eq_CIR": "C_obs = C",
        "form_status": "Derived_under_architecture_premises",
        "numeric_C_obs_status": "NOT_DERIVED_from_S_int_microphysics",
        "numeric_V_status": "NOT_COMPUTED_requires_K_Q_or_vertex_dynamics",
    }


def main() -> None:
    args = parse_args()
    floor = load_json(args.floor_summary)
    s2c = load_json(args.stage2c_summary)
    match = load_json(args.matching_summary)

    checks: list[dict[str, Any]] = []

    floor_ok = (
        floor is not None
        and floor.get("subgate_status") == "PASS_CONDITIONAL_MATCHING_FLOOR"
        and (floor.get("stage_2_exit") or {}).get(
            "allows_stage3_scoped_MAT_calculation"
        )
        is True
        and (floor.get("stage_2_exit") or {}).get("allows_MAT_PASS") is False
    )
    checks.append(
        {
            "name": "uv_stage2b_handoff_authorizes_scoped_calc_only",
            "ok": floor_ok,
            "got": None
            if floor is None
            else floor.get("stage_2_exit"),
        }
    )

    s2c_ok = s2c is not None and s2c.get("subgate_status") in (
        "PASS_STAGE2C_FLOOR_DIAGNOSTICS",
        None,
    )
    # 2c preferred but allow if floor alone (if 2c not yet run fail softly)
    if s2c is None:
        s2c_ok = False
    checks.append(
        {
            "name": "stage2c_diagnostics_present",
            "ok": s2c is not None
            and s2c.get("subgate_status") == "PASS_STAGE2C_FLOOR_DIAGNOSTICS",
            "got": None if s2c is None else s2c.get("subgate_status"),
        }
    )

    match_ok = (
        match is not None
        and match.get("subgate_status") == "PASS_MATCHING_ROUTE_PROGRAM_OPEN"
    )
    checks.append(
        {
            "name": "matching_route_R2_interface_present",
            "ok": match_ok,
        }
    )

    red = static_reduction()
    checks.append(
        {
            "name": "static_reduction_identities_ok",
            "ok": red["form_status"] == "Derived_under_architecture_premises",
        }
    )

    # Conditional baseline (Master Plan §6) — not Derived matching
    conditional_baseline = {
        "label": "CONDITIONAL_AQUAL_IR_BASELINE",
        "C_obs_hypothesis": 1.0,
        "convention_note": (
            "Under C_m = C_IR = C, C_obs = C; Master Plan default empirical "
            "hypothesis C_obs ~ 1 until MAT computes otherwise — Conditional, "
            "not Derived from S_int in this package"
        ),
        "C_IR_status": "OPEN_Wilson",
        "V_status": "NOT_COMPUTED",
        "K_Q_status": "NOT_DERIVED",
        "claim_status": "Conditional",
    }
    checks.append(
        {
            "name": "conditional_Cobs_baseline_not_labelled_Derived",
            "ok": conditional_baseline["claim_status"] == "Conditional"
            and conditional_baseline["V_status"] == "NOT_COMPUTED",
        }
    )

    # Provisional maps under free Conditional (C_obs, C_IR, V)
    C_obs, C_IR, V, G = sp.symbols("C_obs C_IR V G", positive=True)
    I_a0 = (
        C_IR ** sp.Rational(1, 3)
        * V**2
        / (12 * sp.pi * G * C_obs ** sp.Rational(4, 3))
    )
    provisional_map = {
        "I_a0": str(I_a0),
        "note": (
            "Once V is computed from S_int (requires force kinetic chart / K_Q), "
            "substitute Conditional or matched (C_obs, C_IR, V) here"
        ),
        "V_computed_this_stage": False,
        "C_obs_computed_from_micro_S_int": False,
    }
    checks.append(
        {
            "name": "V_not_falsely_claimed_computed",
            "ok": provisional_map["V_computed_this_stage"] is False,
        }
    )

    firewall = {
        "MAT001_PASS": False,
        "Derived_C_obs_from_this_gate": False,
        "Derived_K_Q": False,
        "Derived_V_from_S_int": False,
        "UVIR_full_PASS": False,
        "SPARC_or_H0_validation": False,
        "dual_RAR_a0_cH0_C_2_3": False,
        "downstream_Derived_use_authorized": False,
    }
    checks.append(
        {
            "name": "claim_firewall_MAT_PASS_forbidden",
            "ok": firewall["MAT001_PASS"] is False
            and firewall["downstream_Derived_use_authorized"] is False,
            "flags": firewall,
        }
    )

    # Dual RAR ban check: must not set both
    checks.append(
        {
            "name": "no_dual_RAR_packaging",
            "ok": firewall["dual_RAR_a0_cH0_C_2_3"] is False,
        }
    )

    all_ok = all(c["ok"] for c in checks)
    # Scoped calculation "passes" as honest structural package; not MAT gate PASS
    subgate = (
        "PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL"
        if all_ok
        else "FAIL_MAT001_SCOPED_CALCULATION"
    )

    summary: dict[str, Any] = {
        "gate": "MAT-001",
        "stage": "SCOPED_CALCULATION_UVIR_SERIAL_STAGE_3",
        "serial_stage": 3,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "mat001_gate_status": "BLOCKED_PASS_TAG_FORBIDDEN",
        "mat001_pass": False,
        "physics_pass": False,
        "claim_status": "Conditional_provisional_structure",
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "kq_numeric_status": "NOT_DERIVED",
        "V_status": "NOT_COMPUTED",
        "C_obs_micro_status": "NOT_DERIVED",
        "static_reduction": red,
        "conditional_baseline": conditional_baseline,
        "provisional_invariant_map": provisional_map,
        "declared_S_int": {
            "form": "-C_m rho_b psi (+ architecture completion terms as declared)",
            "status": "DECLARED_FORM_NOT_FULL_MICRO_MATCHING",
            "source": "ITSM_Core_Architecture.md §3.5 / §5 weak-field",
        },
        "uv_handoff": {
            "floor_subgate": None if floor is None else floor.get("subgate_status"),
            "stage2c_subgate": None if s2c is None else s2c.get("subgate_status"),
            "allows_this_calculation": floor_ok,
            "allows_MAT_PASS": False,
        },
        "checklist": {
            "stage2_exit_and_handoff": floor_ok,
            "declare_S_int_form": True,
            "static_reduction_C_obs_form": True,
            "report_C_obs_Derived_from_S_int": False,
            "compute_V_from_S_int": False,
            "map_I_a0_Lambda_formula": True,
            "MAT_PASS": False,
            "SPARC_H0_ban": True,
        },
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "Scoped MAT-001 calculation under UVIR Stage 2 Conditional handoff. "
            "Freezes architecture static-reduction identities and Conditional "
            "C_obs~1 baseline hypothesis. Does not compute V from S_int (K_Q open), "
            "does not issue MAT PASS, does not authorize downstream Derived use, "
            "does not close UVIR-003."
        ),
        "next_required": [
            "Compute V from declared S_int once force kinetic chart / K_Q matching available",
            "UVIR Stages 4–5 before any MAT PASS or Derived downstream packaging",
            "Optional: explicit interaction Lagrangian beyond static -C_m rho psi",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "mat001_scoped_calculation_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    h = hashlib.sha256(payload).hexdigest()
    (
        args.output_dir / "mat001_scoped_calculation_summary.sha256"
    ).write_bytes(f"{h}  {out.name}\n".encode("utf-8"))

    print("MAT-001 scoped calculation (UVIR serial Stage 3)")
    print("  mat001_pass: False (PASS tag forbidden)")
    print("  V_status: NOT_COMPUTED | C_obs micro: NOT_DERIVED")
    print("  physics_pass: False | UVIR: IN_PROGRESS")
    for c in checks:
        print(f"  [{'OK' if c['ok'] else 'FAIL'}] {c['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", h)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
