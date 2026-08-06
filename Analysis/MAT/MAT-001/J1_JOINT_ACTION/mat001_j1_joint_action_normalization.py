#!/usr/bin/env python3
"""MAT-001 J1: same-action normalization identity for the invariant V.

LABEL: symbolic interface audit, not microscopic matching
GATE:  MAT-001 blocked preparation
CLAIM: the one-action template gives V = g_phi/sqrt(Z_phi), but neither
       coefficient is fixed; V remains NOT_COMPUTED and physics_pass is false.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import sympy as sp


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory",
        type=Path,
        default=base.parent / "outputs" / "mat001_v_kinetic_chart_inventory_summary.json",
    )
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.is_file():
        return None, "missing"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, f"{type(exc).__name__}:{exc}"
    if not isinstance(value, dict):
        return None, "top_level_not_object"
    return value, None


def inventory_contract(data: dict[str, Any] | None) -> bool:
    firewall = None if data is None else data.get("claim_firewall")
    return bool(
        data
        and data.get("subgate_status") == "PASS_MAT001_V_KINETIC_CHART_INVENTORY_OPEN"
        and data.get("inventory_status") == "COMPLETE_BLOCKER_MAP_V_OPEN"
        and data.get("V_status") == "NOT_COMPUTED"
        and data.get("kq_numeric_status") == "NOT_DERIVED"
        and data.get("mat001_gate_status") == "BLOCKED_PASS_TAG_FORBIDDEN"
        and data.get("mat001_pass") is False
        and data.get("physics_pass") is False
        and isinstance(firewall, dict)
        and firewall.get("V_computed") is False
        and firewall.get("stage4A_unblocked") is False
    )


def admissible_coefficients(z_phi: Any, f_phi: Any, g_phi: Any) -> bool:
    """Domain check for real finite template coefficients."""
    values = (z_phi, f_phi, g_phi)
    if any(isinstance(value, bool) for value in values):
        return False
    try:
        z_value, f_value, g_value = (float(value) for value in values)
    except (TypeError, ValueError, OverflowError):
        return False
    return bool(
        all(math.isfinite(value) for value in (z_value, f_value, g_value))
        and z_value > 0.0
        and f_value > 0.0
        and g_value != 0.0
    )


def negative_controls() -> list[dict[str, Any]]:
    wrong_inventory = {
        "subgate_status": "PASS_MAT001_V_KINETIC_CHART_INVENTORY_OPEN",
        "inventory_status": "COMPLETE_BLOCKER_MAP_V_OPEN",
        "V_status": "COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "mat001_gate_status": "BLOCKED_PASS_TAG_FORBIDDEN",
        "mat001_pass": False,
        "physics_pass": False,
        "claim_firewall": {"V_computed": False, "stage4A_unblocked": False},
    }
    cases = [
        ("missing_inventory_rejected", not inventory_contract(None)),
        ("premature_computed_V_rejected", not inventory_contract(wrong_inventory)),
        ("zero_Z_phi_rejected", not admissible_coefficients(0.0, 1.0, 1.0)),
        ("negative_Z_phi_rejected", not admissible_coefficients(-1.0, 1.0, 1.0)),
        ("zero_chart_scale_rejected", not admissible_coefficients(1.0, 0.0, 1.0)),
        ("zero_matter_coefficient_rejected", not admissible_coefficients(1.0, 1.0, 0.0)),
        ("negative_matter_coefficient_admitted", admissible_coefficients(1.0, 1.0, -1.0)),
        ("nonfinite_coefficient_rejected", not admissible_coefficients(1.0, 1.0, float("nan"))),
        ("boolean_coefficient_rejected", not admissible_coefficients(True, 1.0, 1.0)),
    ]
    return [
        {"case": name, "ok": observed, "expected_behavior_observed": observed}
        for name, observed in cases
    ]


def main() -> None:
    args = parse_args()
    inventory, inventory_error = load_json(args.inventory)

    z_phi, f_phi, r, s = sp.symbols(
        "Z_phi f_phi r s", positive=True, finite=True
    )
    g_phi = sp.symbols("g_phi", real=True, finite=True, nonzero=True)

    # Parent chart: L_kin = Z_phi/2 (U.grad phi)^2 and L_int = -g_phi rho_b phi.
    # IR chart definition psi = f_phi*phi implies phi = psi/f_phi.
    k_q = z_phi / f_phi**2
    c_m = g_phi / f_phi
    v_ir = sp.simplify(c_m / sp.sqrt(k_q))
    v_parent = g_phi / sp.sqrt(z_phi)

    # Parent-field rescaling phi_prime = r*phi.
    z_prime = z_phi / r**2
    g_prime = g_phi / r
    v_parent_prime = sp.simplify(g_prime / sp.sqrt(z_prime))

    # IR-chart rescaling psi_prime = s*psi.
    k_q_prime = k_q / s**2
    c_m_prime = c_m / s
    v_ir_prime = sp.simplify(c_m_prime / sp.sqrt(k_q_prime))

    # Canonical field phi_c = sqrt(Z_phi)*phi exposes the source residue.
    canonical_source_residue = sp.simplify(g_phi / sp.sqrt(z_phi))

    negatives = negative_controls()
    firewall = {
        "V_numeric_computed": False,
        "K_Q_numeric_derived": False,
        "microscopic_coefficients_matched": False,
        "mat001_pass": False,
        "stage4A_unblocked": False,
        "UVIR003_pass": False,
        "physics_pass": False,
        "downstream_Derived": False,
    }
    checks = [
        {
            "name": "upstream_inventory_exact_open_contract",
            "ok": inventory_contract(inventory),
            "source": args.inventory.name,
            "error": inventory_error,
        },
        {"name": "IR_chart_K_Q_equals_Z_over_f_squared", "ok": sp.simplify(k_q - z_phi / f_phi**2) == 0},
        {"name": "IR_chart_C_m_equals_g_over_f", "ok": sp.simplify(c_m - g_phi / f_phi) == 0},
        {"name": "same_action_V_identity", "ok": sp.simplify(v_ir - v_parent) == 0},
        {"name": "parent_field_rescaling_covariance", "ok": sp.simplify(v_parent_prime - v_parent) == 0},
        {"name": "IR_chart_rescaling_covariance", "ok": sp.simplify(v_ir_prime - v_ir) == 0},
        {"name": "canonical_source_residue_equals_V", "ok": sp.simplify(canonical_source_residue - v_parent) == 0},
        {
            "name": "field_orientation_reversal_flips_signed_residue",
            "ok": sp.simplify(v_parent.subs(g_phi, -g_phi) + v_parent) == 0,
            "orientation_rule": "phi_or_mode -> -(phi_or_mode) implies V_signed -> -V_signed",
        },
        {"name": "negative_controls_fail_closed", "ok": all(row["ok"] for row in negatives), "cases": negatives},
        {"name": "claim_firewall", "ok": all(value is False for value in firewall.values()), "flags": firewall},
    ]

    all_ok = all(check["ok"] for check in checks)
    subgate = (
        "PASS_MAT001_J1_JOINT_ACTION_NORMALIZATION_IDENTITY"
        if all_ok
        else "FAIL_MAT001_J1_JOINT_ACTION_NORMALIZATION"
    )
    summary: dict[str, Any] = {
        "gate": "MAT-001",
        "stage": "J1_JOINT_ACTION_NORMALIZATION",
        "subgate_status": subgate,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "research_gate_status": "BLOCKED_MATCHING_INPUTS_OPEN",
        "mat001_pass": False,
        "physics_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_unlock": False,
        "V_status": "NOT_COMPUTED",
        "V_form_status": "SAME_ACTION_IDENTITY_DERIVED",
        "kq_numeric_status": "NOT_DERIVED",
        "joint_action_template": {
            "kinetic_term": "(Z_phi/2)*(U.grad(phi))^2",
            "matter_vertex": "-g_phi*rho_b*phi",
            "IR_chart_definition": "psi=f_phi*phi",
            "induced_K_Q": str(k_q),
            "induced_C_m": str(c_m),
            "invariant_V": str(v_ir),
            "signed_invariant_V": str(v_ir),
            "canonical_source_residue": str(canonical_source_residue),
            "orientation_anchor": "parent field phi and IR field psi have aligned positive orientation because f_phi>0",
        },
        "field_rescaling_covariance": {
            "parent_chart": {
                "map": "phi_prime=r*phi",
                "Z_phi_prime": str(z_prime),
                "g_phi_prime": str(g_prime),
                "V_prime": str(v_parent_prime),
            },
            "IR_chart": {
                "map": "psi_prime=s*psi",
                "K_Q_prime": str(k_q_prime),
                "C_m_prime": str(c_m_prime),
                "V_prime": str(v_ir_prime),
            },
            "scope": "r>0 and s>0 are orientation-preserving; an orientation reversal flips the signed residue",
        },
        "unmatched_physical_inputs": [
            "Z_phi from a declared microscopic parent action",
            "g_phi from the matter coupling in that same parent action",
            "a justified map from the parent field phi to the live IR force field psi",
        ],
        "prior_artifact": {
            "source": args.inventory.name,
            "subgate_status": None if inventory is None else inventory.get("subgate_status"),
            "parse_error": inventory_error,
        },
        "negative_controls": negatives,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS proves only the algebraic equivalence between the same-action "
            "canonical matter residue and C_m/sqrt(K_Q). It does not supply Z_phi "
            "or g_phi, compute a numerical V, validate a microscopic action, unlock "
            "UVIR Stage 4A, or issue MAT/UVIR/physics PASS."
        ),
        "next_required": [
            "Identify a declared microscopic action containing both Z_phi and g_phi",
            "derive both coefficients in one field chart or extract the equivalent on-shell residue",
            "only then compute V and reopen the MAT-to-UVIR Stage 4A handoff",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "mat001_j1_joint_action_normalization_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    sidecar = args.output_dir / "mat001_j1_joint_action_normalization_summary.sha256"
    sidecar.write_bytes(f"{digest}  {out.name}\n".encode("utf-8"))

    print("MAT-001 J1 same-action normalization identity")
    print("  V form: g_phi/sqrt(Z_phi) | V numeric: NOT_COMPUTED")
    print("  MAT PASS: false | UVIR: IN_PROGRESS | Stage 4A: closed")
    for check in checks:
        print(f"  [{'OK' if check['ok'] else 'FAIL'}] {check['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", digest)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
