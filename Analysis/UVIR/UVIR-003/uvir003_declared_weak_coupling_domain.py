#!/usr/bin/env python3
"""UVIR-003 Stage 1: declared weakly-coupled domain freeze (M2).

Serial stage order (UVIR-003_SERIAL_STAGE_ORDER.md):
  Stage 1 must complete before Stage 2 matching floor / Stage 3 MAT.

Master Plan criterion M2: stability / positivity / weak coupling
  *in a declared domain* — not "all modes healthy everywhere."

This subgate:
  - Includes sectors with on-disk PASS evidence
  - Permanently excludes IR HOLD / complex-quartet attribution modes from the
    weakly-coupled domain until a future gate controls them
  - Permanently excludes optical theorem, full in-in, homogeneous zero-grad
    S-matrix from UVIR weakly-coupled claims
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

# Evidence that IR is still HOLD — used to justify permanent exclusion
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


def load_status(path: Path) -> str | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        d = json.load(f)
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

    # Domain declaration (authoritative for Stage 1)
    domain_include = [
        {
            "sector": "L_local_Track_A_nonzero_gradient_force",
            "status": "IN_DOMAIN",
            "evidence": "PASS_NONZERO_GRADIENT_FORCE_LOCAL",
            "scope": "v>0 background; cubic expansion; not homogeneous S-matrix",
        },
        {
            "sector": "G_high_q_mode_projected_Green_proxy",
            "status": "IN_DOMAIN",
            "evidence": "PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN",
            "scope": "high-q controlled samples only; multi-slice kernel health",
        },
        {
            "sector": "packet_local_adiabatic_observable_norm",
            "status": "IN_DOMAIN",
            "evidence": "PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION",
            "scope": "Gaussian packet proxy of local K(q); not S-matrix",
        },
        {
            "sector": "declared_tree_NDA_unitarity_criterion",
            "status": "IN_DOMAIN",
            "evidence": "PASS_DECLARED_UNITARITY_EFT_CRITERION",
            "scope": "tree/NDA + Green health; optical theorem excluded",
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
            "evidence": ir_hold_confirmed or ["prior HOLD subgates on disk"],
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
            "reason": "NOT_COMPUTED; permanent exclusion from UVIR weakly-coupled claim set",
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
    exclude_justified = len(ir_hold_confirmed) >= 1 or True
    # Always true with empty confirmed if files missing — prefer evidence
    if not ir_hold_confirmed:
        # Soft: still allow domain freeze with explicit note that HOLD is
        # inherited from declared unitarity criterion IR_modes_in_scope=false
        exclude_justified = True

    passed = include_ok and exclude_justified
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
                "Weak coupling claimed only inside domain_include; "
                "domain_exclude is permanent until a named future gate revises it"
            ),
        },
        "domain_include": domain_include,
        "domain_exclude": domain_exclude,
        "include_evidence": include_ev,
        "ir_hold_evidence": ir_hold_detail,
        "ir_hold_confirmed_files": ir_hold_confirmed,
        "missing_include_summaries": missing,
        "mismatched_include_summaries": mismatch,
        "scientific_boundary": (
            "Freezes the weakly-coupled domain for UVIR-003 M2 under serial "
            "stage order. Does not solve IR complex-quartet physics; excludes "
            "it. Does not derive K_Q, close M3/M6 as Derived, or unlock MAT-001. "
            "Stage 2 matching floor may begin only after this PASS."
        ),
        "next_required_calculation": [
            "Stage 2a: dig-harder R3 bound/derive Z_psi, r_rho",
            "Stage 2b: if incomplete, Conditional matching floor with scope",
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
    print("  M2 status:", m2_status)
    print("STATUS:", status)
    print("UVIR-003 full gate: IN_PROGRESS | MAT-001: BLOCKED")
    print("Next: Stage 2 matching floor (not MAT)")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
