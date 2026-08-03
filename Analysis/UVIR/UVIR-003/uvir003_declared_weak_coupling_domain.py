#!/usr/bin/env python3
"""UVIR-003 Stage 1: declared weakly-coupled domain freeze (M2).

Serial stage order (UVIR-003_SERIAL_STAGE_ORDER.md):
  Stage 1 must complete before Stage 2 matching floor / Stage 3 MAT.

Master Plan criterion M2: stability / positivity / weak coupling
  *in a declared domain* — not "all modes healthy everywhere."

This subgate:
  - Includes sectors with on-disk PASS evidence
  - Excludes IR HOLD / complex-quartet attribution modes from the current
    weakly-coupled claim domain until a future gate controls them
  - Excludes optical theorem, full in-in, and the homogeneous zero-gradient
    S-matrix from the current UVIR weakly-coupled claim domain
  - Does not close M3/M6 as Derived
  - Does not unlock MAT-001

Exit: PASS_DECLARED_WEAK_COUPLING_DOMAIN → M2 scored PASS_BOUNDED.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_INCLUDE_EVIDENCE: dict[str, str] = {
    "uvir003_nonzero_gradient_force_local_summary.json": (
        "PASS_NONZERO_GRADIENT_FORCE_LOCAL"
    ),
    "uvir003_frw_multi_slice_mode_green_summary.json": (
        "PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN"
    ),
    "uvir003_declared_unitarity_eft_criterion_summary.json": (
        "PASS_DECLARED_UNITARITY_EFT_CRITERION"
    ),
    "uvir003_local_adiabatic_observable_norm_summary.json": (
        "PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION"
    ),
    "uvir003_kq_matching_inventory_summary.json": (
        "PASS_KQ_MATCHING_INVENTORY_OPEN"
    ),
    "uvir003_matching_route_program_summary.json": (
        "PASS_MATCHING_ROUTE_PROGRAM_OPEN"
    ),
}

# Evidence that IR is still HOLD — required to justify bounded exclusion
IR_HOLD_EVIDENCE: dict[str, list[str]] = {
    "uvir003_mode_resolved_transfer_robustness_summary.json": [
        "HOLD_COMPLEX_QUARTET_IR_MODE_ATTRIBUTION",
        "HOLD",
    ],
    "uvir003_propagator_adiabaticity_transfer_summary.json": [
        "HOLD_TIME_DEPENDENT_INFRARED_TRANSFER_INTERPRETATION",
        "HOLD",
    ],
}


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument("--summaries-dir", type=Path, default=base / "outputs")
    return p.parse_args()


def load_summary(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_status(path: Path) -> str | None:
    d = load_summary(path)
    if d is None:
        return None
    return (
        d.get("subgate_status")
        or d.get("status")
        or d.get("calculation_status")
    )


def main() -> None:
    args = parse_args()
    include_ev: dict[str, Any] = {}
    missing = []
    mismatch = []

    for fname, expected in REQUIRED_INCLUDE_EVIDENCE.items():
        path = args.summaries_dir / fname
        got = load_status(path)
        ok = got == expected
        include_ev[fname] = {
            "expected": expected,
            "got": got,
            "ok": ok,
        }
        if got is None:
            missing.append(fname)
        elif not ok:
            mismatch.append(fname)

    ir_hold_confirmed = []
    ir_hold_detail: dict[str, Any] = {}
    for fname, acceptable in IR_HOLD_EVIDENCE.items():
        path = args.summaries_dir / fname
        got = load_status(path)
        ir_hold_detail[fname] = {"got": got, "path": str(path)}
        if got is not None and (
            got in acceptable or str(got).startswith("HOLD")
        ):
            ir_hold_confirmed.append(fname)

    force = load_summary(
        args.summaries_dir / "uvir003_nonzero_gradient_force_local_summary.json"
    ) or {}
    green = load_summary(
        args.summaries_dir / "uvir003_frw_multi_slice_mode_green_summary.json"
    ) or {}
    packet = load_summary(
        args.summaries_dir / "uvir003_local_adiabatic_observable_norm_summary.json"
    ) or {}
    criterion = load_summary(
        args.summaries_dir / "uvir003_declared_unitarity_eft_criterion_summary.json"
    ) or {}

    force_samples = force.get("numerical_samples", [])
    force_v = sorted(
        float(row["v"]) for row in force_samples if row.get("v") is not None
    )
    force_domain_ok = bool(
        force.get("analytic", {}).get("hessian_positive_for_A_v_positive")
        and force.get("diagnostics", {}).get("all_samples_positive")
        and force_v
        and min(force_v) > 0.0
    )

    admitted_q_over_h = sorted(
        float(x)
        for x in green.get("dependencies", {}).get(
            "admitted_external_q_over_H", []
        )
    )
    green_times = [
        float(x) for x in green.get("mode_projected_green", {}).get("times", [])
    ]
    green_domain_ok = bool(
        green.get("diagnostics", {}).get("green_ok")
        and green.get("diagnostics", {}).get("diag_ok")
        and admitted_q_over_h
        and min(admitted_q_over_h) >= 47.5
        and max(admitted_q_over_h) >= 100.0
        and green_times
        and min(green_times) == 0.0
        and max(green_times) == 8.0
    )

    packet_q_over_h = sorted(float(x) for x in packet.get("sampled_ratios", []))
    packet_diag = packet.get("diagnostics", {})
    packet_domain_ok = bool(
        packet_diag.get("narrow_ok")
        and packet_q_over_h == admitted_q_over_h
        and float(packet.get("q0_over_H", -1.0)) == 50.0
    )

    sector_l = criterion.get("sector_L", {})
    sector_g = criterion.get("sector_G", {})
    r_eff_window = float(
        criterion.get("diagnostics", {}).get("r_eff_window", float("inf"))
    )
    criterion_domain_ok = bool(
        sector_l.get("pass")
        and sector_g.get("pass")
        and sector_g.get("IR_modes_in_scope") is False
        and 0.0 < r_eff_window <= 0.3
        and criterion.get("joint", {}).get("physical_cutoff_status")
        == "NOT_ESTABLISHED_K_Q_MATCHING_OPEN"
    )

    quantitative_domain_checks = {
        "force_A_IR_positive_and_v_positive": force_domain_ok,
        "force_tested_v_support_present": bool(force_v),
        "green_discrete_q_over_H_support_and_time_interval": green_domain_ok,
        "packet_support_matches_green_support": packet_domain_ok,
        "tree_NDA_diagnostic_window_scoped_and_unmatched": criterion_domain_ok
    }
    quantitative_domain_ok = all(quantitative_domain_checks.values())

    # Domain declaration (authoritative for Stage 1)
    domain_include = [
        {
            "sector": "L_local_Track_A_nonzero_gradient_force",
            "status": "IN_DOMAIN",
            "evidence": "PASS_NONZERO_GRADIENT_FORCE_LOCAL",
            "scope": "analytic A_IR>0, v>0; sampled v=[0.05,2.0] at A_IR=1",
        },
        {
            "sector": "G_high_q_mode_projected_Green_proxy",
            "status": "IN_DOMAIN",
            "evidence": "PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN",
            "scope": "discrete q/H={47.5,50,75,100}; proxy time t=[0,8]",
        },
        {
            "sector": "packet_local_adiabatic_observable_norm",
            "status": "IN_DOMAIN",
            "evidence": "PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION",
            "scope": "packet q0/H=50, sigma_ln=0.02 on same discrete support",
        },
        {
            "sector": "declared_tree_NDA_unitarity_criterion",
            "status": "IN_DOMAIN",
            "evidence": "PASS_DECLARED_UNITARITY_EFT_CRITERION",
            "scope": "diagnostic q/Lambda<=0.3, u_L<=1; normalization unmatched",
        },
        {
            "sector": "redefinition_invariants_and_route_maps",
            "status": "IN_DOMAIN",
            "evidence": "PASS_KQ_MATCHING_INVENTORY_OPEN + PASS_MATCHING_ROUTE_PROGRAM_OPEN",
            "scope": "invariants + R2 V target; numeric K_Q not Derived",
        },
    ]

    domain_exclude = [
        {
            "sector": "IR_transfer_HOLD_complex_quartet_modes",
            "status": "OUT_OF_DOMAIN",
            "evidence": ir_hold_confirmed,
            "reason": (
                "Complex-quartet nonseparability / IR gain attribution HOLD; "
                "not weakly coupled under present diagnostics"
            ),
            "until": "Future gate controls or reclassifies IR modes",
        },
        {
            "sector": "homogeneous_zero_gradient_Y32_S_matrix",
            "status": "OUT_OF_DOMAIN",
            "reason": "Exact Y^{3/2} at zero gradient not a healthy homogeneous S-matrix sector",
            "until": "Not claimed under Track-A nonzero-gradient programme",
        },
        {
            "sector": "full_in_in_nested_time_integrals",
            "status": "OUT_OF_DOMAIN",
            "reason": "Path declared only; integrals not computed",
            "until": "Later gate or explicit Open schedule",
        },
        {
            "sector": "optical_theorem_multi_channel_unitarity",
            "status": "OUT_OF_DOMAIN",
            "reason": "NOT_COMPUTED; excluded from current UVIR weakly-coupled claim set",
            "until": "Optional later gate; not required for Stage 1 exit",
        },
        {
            "sector": "Derived_K_Q_and_matched_physical_cutoff",
            "status": "OUT_OF_DOMAIN",
            "reason": "Matching Stage 2–4; K_Q NOT_DERIVED",
            "until": "Stage 2 floor + Stage 3–4 MAT upgrade",
        },
        {
            "sector": "MAT001_Derived_vertex",
            "status": "OUT_OF_DOMAIN",
            "reason": "Serial order: MAT is Stage 3 after domain freeze + matching floor",
            "until": "Stage 3",
        },
    ]

    include_ok = len(missing) == 0 and len(mismatch) == 0
    # Require at least one IR HOLD artifact so exclusion is evidence-based
    exclude_justified = len(ir_hold_confirmed) >= 1
    # Missing evidence is a hard failure; no fallback is permitted.
    passed = include_ok and exclude_justified and quantitative_domain_ok
    status = (
        "PASS_DECLARED_WEAK_COUPLING_DOMAIN"
        if passed
        else "FAIL_DECLARED_WEAK_COUPLING_DOMAIN"
    )

    m2_status = "PASS_BOUNDED" if passed else "PARTIAL"
    summary = {
        "gate": "UVIR-003",
        "stage": "B_DECLARED_WEAK_COUPLING_DOMAIN",
        "serial_stage": 1,
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": status,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "master_plan_M2": {
            "status": m2_status,
            "meaning": (
                "Evidence-bounded diagnostic claim only inside domain_include; "
                "no continuum-neighbourhood or no-leakage theorem is claimed"
            ),
        },
        "quantitative_domain": {
            "force": {
                "analytic_conditions": ["A_IR>0", "v>0"],
                "tested_A_IR": 1.0,
                "tested_v_values": force_v
            },
            "green_and_packet": {
                "admitted_discrete_q_over_H": admitted_q_over_h,
                "packet_q0_over_H": packet.get("q0_over_H"),
                "packet_narrow_sigma_ln": packet_diag.get("narrow_sigma"),
                "representative_time_interval": (
                    [min(green_times), max(green_times)] if green_times else []
                ),
            },
            "tree_NDA_diagnostic": {
                "q_over_Lambda_parallel_max": r_eff_window,
                "u_L_max": sector_l.get("parameters", {}).get("u_max"),
                "normalization": "A_IR=K_Q=1 diagnostic only",
                "physical_cutoff": "NOT_ESTABLISHED_K_Q_MATCHING_OPEN"
            },
            "checks": quantitative_domain_checks
        },
        "domain_include": domain_include,
        "domain_exclude": domain_exclude,
        "include_evidence": include_ev,
        "ir_hold_evidence": ir_hold_detail,
        "ir_hold_confirmed_files": ir_hold_confirmed,
        "missing_include_summaries": missing,
        "mismatched_include_summaries": mismatch,
        "scientific_boundary": (
            "Freezes an evidence-bounded diagnostic claim domain for UVIR-003 M2. "
            "Does not solve IR complex-quartet physics; excludes it. Does not derive "
            "K_Q, close M3/M6 as Derived, or unlock MAT-001. The admitted high-q "
            "support is discrete and representative; no open-neighbourhood stability "
            "or dynamical no-leakage theorem is claimed. Stage 2 matching floor may "
            "begin only after this PASS."
        ),
        "next_required_calculation": [
            "Stage 2a: COMPLETE as INCOMPLETE_R3_UV_RESIDUE",
            "Stage 2b: write Conditional matching floor with scope",
            "Stage 2c: re-run causality/NDA under floor",
            "Only then Stage 3 MAT-001",
        ],
        "serial_order_doc": (
            "Theory/Gates/UVIR-003/UVIR-003_SERIAL_STAGE_ORDER.md"
        ),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "uvir003_declared_weak_coupling_domain_summary.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")

    print("Stage 1 — declared weakly-coupled domain")
    print("  Include evidence OK:", include_ok)
    print("  IR HOLD files confirmed:", len(ir_hold_confirmed))
    print("  Quantitative domain checks OK:", quantitative_domain_ok)
    print("  M2 status:", m2_status)
    print("STATUS:", status)
    print("UVIR-003 full gate: IN_PROGRESS | MAT-001: BLOCKED")
    print("Next: Stage 2 matching floor (not MAT)")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
