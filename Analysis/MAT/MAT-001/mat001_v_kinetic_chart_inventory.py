#!/usr/bin/env python3
"""MAT-001: fail-closed inventory of requirements for computing V.

LABEL: evidence-integrity audit / blocker map toward UVIR Stage 4A
GATE:  MAT-001 pre-computation chart
CLAIM: V remains NOT_COMPUTED; physics_pass false; mat001_pass false

Audits the exact upstream contracts needed to define

    V := C_m / sqrt(K_Q)

in one field-normalization chart. This package does not compute V, derive K_Q,
or authorize MAT/UVIR/downstream passes. A PASS means only that the blocker map
and its source evidence are internally consistent.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    uvir = base.parents[1] / "UVIR" / "UVIR-003" / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument(
        "--scoped",
        type=Path,
        default=base / "outputs" / "mat001_scoped_calculation_summary.json",
    )
    parser.add_argument(
        "--inventory",
        type=Path,
        default=uvir / "uvir003_kq_matching_inventory_summary.json",
    )
    parser.add_argument(
        "--matching",
        type=Path,
        default=uvir / "uvir003_matching_route_program_summary.json",
    )
    parser.add_argument(
        "--force",
        type=Path,
        default=uvir / "uvir003_nonzero_gradient_force_local_summary.json",
    )
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


def nested(data: dict[str, Any] | None, *keys: str) -> Any:
    value: Any = data
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def scoped_contract(data: dict[str, Any] | None) -> bool:
    return bool(
        data
        and data.get("subgate_status") == "PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL"
        and data.get("serial_stage_status") == "PARTIAL_PROVISIONAL_V_NOT_COMPUTED"
        and data.get("V_status") == "NOT_COMPUTED"
        and data.get("kq_numeric_status") == "NOT_DERIVED"
        and data.get("mat001_pass") is False
        and data.get("physics_pass") is False
        and data.get("uv_ir_full_gate_status") == "IN_PROGRESS"
    )


def inventory_contract(data: dict[str, Any] | None) -> bool:
    return bool(
        data
        and data.get("subgate_status") == "PASS_KQ_MATCHING_INVENTORY_OPEN"
        and data.get("kq_numeric_status") == "NOT_DERIVED"
        and data.get("full_gate_status") == "IN_PROGRESS"
        and nested(data, "invariants", "invariants", "C_m_over_sqrt_K_Q")
        == "C_m/sqrt(K_Q)"
        and nested(data, "invariants", "invariance_checks", "C_m_over_sqrt_K_Q")
        is True
    )


def matching_contract(data: dict[str, Any] | None) -> bool:
    return bool(
        data
        and data.get("subgate_status") == "PASS_MATCHING_ROUTE_PROGRAM_OPEN"
        and data.get("kq_numeric_status") == "NOT_DERIVED"
        and data.get("full_gate_status") == "IN_PROGRESS"
        and nested(data, "route_R2_interface", "definitions", "V")
        == "C_m/sqrt(K_Q)"
        and nested(data, "route_R2_interface", "dof_counting", "static_Cobs_alone_fixes_Aq_over_KQ")
        is False
        and nested(data, "route_R2_interface", "status")
        == "Open_interface_ready_MAT_blocked"
    )


def force_contract(data: dict[str, Any] | None) -> bool:
    mat_status = None if data is None else data.get("mat001_status")
    return bool(
        data
        and data.get("subgate_status") == "PASS_NONZERO_GRADIENT_FORCE_LOCAL"
        and data.get("full_gate_status") == "IN_PROGRESS"
        and isinstance(mat_status, str)
        and mat_status.startswith("BLOCKED")
    )


def negative_contract_tests() -> list[dict[str, Any]]:
    cases: list[tuple[str, bool]] = [
        ("scoped_missing_rejected", not scoped_contract(None)),
        (
            "scoped_false_V_claim_rejected",
            not scoped_contract(
                {
                    "subgate_status": "PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL",
                    "serial_stage_status": "PARTIAL_PROVISIONAL_V_NOT_COMPUTED",
                    "V_status": "COMPUTED",
                    "kq_numeric_status": "NOT_DERIVED",
                    "mat001_pass": False,
                    "physics_pass": False,
                    "uv_ir_full_gate_status": "IN_PROGRESS",
                }
            ),
        ),
        (
            "inventory_wrong_subgate_rejected",
            not inventory_contract({"subgate_status": "PASS"}),
        ),
        (
            "matching_letter_V_only_rejected",
            not matching_contract(
                {
                    "subgate_status": "PASS_MATCHING_ROUTE_PROGRAM_OPEN",
                    "note": "V",
                }
            ),
        ),
        (
            "force_presence_without_contract_rejected",
            not force_contract({"subgate_status": "PASS_NONZERO_GRADIENT_FORCE_LOCAL"}),
        ),
    ]
    return [{"case": name, "rejected": rejected, "ok": rejected} for name, rejected in cases]


def main() -> None:
    args = parse_args()
    sources = {
        "scoped": args.scoped,
        "inventory": args.inventory,
        "matching": args.matching,
        "force": args.force,
    }
    loaded: dict[str, dict[str, Any] | None] = {}
    errors: dict[str, str | None] = {}
    checks: list[dict[str, Any]] = []

    for name, path in sources.items():
        loaded[name], errors[name] = load_json(path)
        checks.append(
            {
                "name": f"{name}_summary_present_parseable_object",
                "ok": loaded[name] is not None,
                "source": path.name,
                "error": errors[name],
            }
        )

    contracts: list[tuple[str, Callable[[dict[str, Any] | None], bool]]] = [
        ("scoped_mat_exact_open_contract", scoped_contract),
        ("kq_inventory_exact_open_contract", inventory_contract),
        ("matching_route_R2_exact_V_contract", matching_contract),
        ("force_local_exact_open_contract", force_contract),
    ]
    for (check_name, contract), source_name in zip(contracts, sources):
        checks.append(
            {
                "name": check_name,
                "ok": contract(loaded[source_name]),
                "source": sources[source_name].name,
            }
        )

    required_for_V = [
        {
            "item": "C_m normalization from one declared dynamical S_int in the chosen psi chart",
            "status": "NOT_DERIVED_STATIC_FORM_ONLY",
        },
        {
            "item": "K_Q time-kinetic normalization in the same psi chart",
            "status": "NOT_DERIVED",
        },
        {
            "item": "Alternative direct on-shell invariant vertex residual V",
            "status": "NOT_COMPUTED",
        },
        {
            "item": "Field-rescaling/gauge convention connecting C_m and K_Q",
            "status": "INVARIANT_IDENTIFIED_CHART_MATCHING_OPEN",
        },
    ]
    downstream_not_required_to_define_V = [
        {
            "item": "C_IR matching for C_obs/I_a0 maps",
            "status": "OPEN_CONDITIONAL",
        },
        {
            "item": "Stage 4A causality, relevant IR response, and physical cutoff",
            "status": "BLOCKED_UNTIL_MATCHED_V_OR_EQUIVALENT",
        },
    ]
    expected_blocker_statuses = {
        "NOT_DERIVED_STATIC_FORM_ONLY",
        "NOT_DERIVED",
        "NOT_COMPUTED",
        "INVARIANT_IDENTIFIED_CHART_MATCHING_OPEN",
    }
    checks.append(
        {
            "name": "V_blocker_map_complete_and_non_derived",
            "ok": {row["status"] for row in required_for_V} == expected_blocker_statuses,
        }
    )

    negative_controls = negative_contract_tests()
    checks.append(
        {
            "name": "negative_contract_controls_fail_closed",
            "ok": all(row["ok"] for row in negative_controls),
            "cases": negative_controls,
        }
    )

    firewall = {
        "mat001_pass": False,
        "V_computed": False,
        "Derived_K_Q": False,
        "stage4A_unblocked": False,
        "UVIR003_pass": False,
        "downstream_Derived": False,
        "SPARC_H0": False,
        "dual_RAR": False,
    }
    checks.append(
        {
            "name": "claim_firewall",
            "ok": all(value is False for value in firewall.values()),
            "flags": firewall,
        }
    )

    all_ok = all(check["ok"] for check in checks)
    subgate = (
        "PASS_MAT001_V_KINETIC_CHART_INVENTORY_OPEN"
        if all_ok
        else "FAIL_MAT001_V_CHART_INVENTORY"
    )
    summary: dict[str, Any] = {
        "gate": "MAT-001",
        "stage": "V_KINETIC_CHART_INVENTORY",
        "inventory_status": "COMPLETE_BLOCKER_MAP_V_OPEN" if all_ok else "EVIDENCE_INTEGRITY_FAILURE",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "mat001_gate_status": "BLOCKED_PASS_TAG_FORBIDDEN",
        "mat001_pass": False,
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "physics_pass": False,
        "required_for_V": required_for_V,
        "downstream_not_required_to_define_V": downstream_not_required_to_define_V,
        "prior_artifacts": {
            name: {
                "source": path.name,
                "subgate_status": None if loaded[name] is None else loaded[name].get("subgate_status"),
                "parse_error": errors[name],
            }
            for name, path in sources.items()
        },
        "negative_controls": negative_controls,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "Fail-closed inventory of blockers for V=C_m/sqrt(K_Q). PASS means "
            "the blocker map matches exact upstream Open/Partial evidence; it does "
            "not compute V, derive K_Q, close Stage 4A, or issue MAT/UVIR PASS."
        ),
        "next_required": [
            "Choose one declared action and psi field-normalization chart",
            "Derive C_m and K_Q in that same chart, or compute the invariant on-shell residual V directly",
            "Then reopen UVIR Stage 4A; C_IR matching is downstream of defining V",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "mat001_v_kinetic_chart_inventory_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "mat001_v_kinetic_chart_inventory_summary.sha256").write_bytes(
        f"{digest}  {out.name}\n".encode("utf-8")
    )

    print("MAT-001 V kinetic-chart blocker inventory")
    print("  V_status: NOT_COMPUTED | MAT PASS: forbidden | UVIR: IN_PROGRESS")
    for check in checks:
        print(f"  [{'OK' if check['ok'] else 'FAIL'}] {check['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", digest)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()