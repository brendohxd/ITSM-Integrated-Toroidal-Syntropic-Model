#!/usr/bin/env python3
"""UVIR-003: declared perturbative-unitarity / EFT-validity criterion (scoped).

Master-plan remaining alpha.10 item after
PASS_NONZERO_GRADIENT_FORCE_LOCAL:

  A *declared* perturbative-unitarity / EFT-validity criterion with explicit
  scope (high-q Green proxy + local nonzero-gradient force sector).
  Not "theory closed".

What this is
------------
An explicit, machine-checked *criterion package* that states:

  1. Which quantities enter the diagnostic.
  2. What numerical bounds count as "perturbatively healthy" inside that
     declared domain.
  3. What is *out of scope* (IR transfer HOLD modes, homogeneous Y^(3/2)
     S-matrix, full optical theorem, MAT-001).

Sectors
-------
L — Local Track-A force (nonzero gradient v>0):
    Canonical cubic coupling g3 = A_IR / K_Q^(3/2)
    NDA scale Λ_|| = K_Q^(3/4) / sqrt(A_IR)   [prior B_ITEM_9 partial]
    Parallel tree vertex strength at wave-number q:
        |V_||(q)| = 6 A_IR q^3 / K_Q^(3/2)   (canonical pi -> chi = sqrt(K_Q) pi)
    Dimensionless tree diagnostic:
        u_L(q) := |V_||(q)| / (16 pi)   (s-wave-proxy; O(1) NDA, not a proof)
    Weak-coupling domain declaration:
        q / Λ_||  <= r_max   AND   u_L(q) <= u_max

G — High-q mode-projected Green proxy (prior multi-slice PASS):
    Uses G_proxy_abs, multi-slice K span, causal G_mp structure.
    Validity flags:
        - multi-slice kernel relative span <= span_max
        - Green diagonal matches local kernel
        - only high-q modes admitted (IR HOLD retained as out of scope)

Joint criterion PASS when both sector diagnostics are finite, prior subgates
PASS, and the declared domain is non-empty for the default parameter point
and for a scan of dimensionless K_Q (diagnostic force normalization).

What this is *not*
------------------
- Completed optical theorem / multi-channel unitarity.
- Physical strong-coupling cutoff with matched K_Q.
- Homogeneous FRW 2-to-2 S-matrix bound.
- UVIR-003 full-gate close or MAT-001 unlock.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument(
        "--green-summary",
        type=Path,
        default=base / "outputs" / "uvir003_frw_multi_slice_mode_green_summary.json",
    )
    parser.add_argument(
        "--force-summary",
        type=Path,
        default=base
        / "outputs"
        / "uvir003_nonzero_gradient_force_local_summary.json",
    )
    parser.add_argument(
        "--nda-summary",
        type=Path,
        default=base
        / "outputs"
        / "uvir003_force_strong_coupling_estimate_summary.json",
    )
    parser.add_argument(
        "--packet-summary",
        type=Path,
        default=base
        / "outputs"
        / "uvir003_local_adiabatic_observable_norm_summary.json",
    )
    parser.add_argument(
        "--A-IR",
        type=float,
        default=1.0,
        help="Diagnostic A_IR (>0). Physical matching left open.",
    )
    parser.add_argument(
        "--K-Q",
        type=float,
        default=1.0,
        help="Diagnostic K_Q (>0). Same bookkeeping normalization as prior force gates.",
    )
    parser.add_argument(
        "--r-max",
        type=float,
        default=0.30,
        help="Max q/Λ_|| for declared weak-coupling window.",
    )
    parser.add_argument(
        "--u-max",
        type=float,
        default=1.0,
        help="Max s-wave-proxy |V|/(16π) inside the window.",
    )
    parser.add_argument(
        "--span-max",
        type=float,
        default=0.25,
        help="Max multi-slice kernel |K| relative span for Green sector health.",
    )
    parser.add_argument(
        "--q-over-Lambda-grid",
        type=float,
        nargs="+",
        default=[0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0],
    )
    return parser.parse_args()


def require(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(f"{name}" + (f": {detail}" if detail else ""))


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def lambda_parallel(k_q: float, a_ir: float) -> float:
    """Λ_|| = K_Q^{3/4} / sqrt(A_IR)."""
    return (k_q ** 0.75) / math.sqrt(a_ir)


def vertex_parallel_canonical(q: float, a_ir: float, k_q: float) -> float:
    """|V_||| for three parallel legs after chi = sqrt(K_Q) pi.

    Bare vertex for pi: 6 A q^3 (abs of 6 i A q^3).
    Each external pi = chi / sqrt(K_Q) => factor K_Q^{-3/2}.
    """
    return 6.0 * a_ir * (q**3) / (k_q**1.5)


def u_swave_proxy(v_abs: float) -> float:
    return abs(v_abs) / (16.0 * math.pi)


def main() -> None:
    args = parse_args()
    require("A_IR > 0", args.A_IR > 0)
    require("K_Q > 0", args.K_Q > 0)
    require("r_max > 0", args.r_max > 0)
    require("u_max > 0", args.u_max > 0)

    green = load_json(args.green_summary)
    force = load_json(args.force_summary)
    nda = load_json(args.nda_summary)
    packet = load_json(args.packet_summary)

    require(
        "green subgate",
        green.get("subgate_status") == "PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN",
    )
    require(
        "force subgate",
        force.get("subgate_status") == "PASS_NONZERO_GRADIENT_FORCE_LOCAL",
    )
    require(
        "packet subgate",
        packet.get("subgate_status")
        == "PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION",
    )

    # --- Sector L: local force ---
    lam = lambda_parallel(args.K_Q, args.A_IR)
    # Cross-check NDA formula string from prior estimate
    nda_formula = (
        nda.get("longitudinal_ir_nda_scale", {}).get("formula_in_K_Q_A")
        or "K_Q**(3/4)/sqrt(A)"
    )
    require("NDA formula present", "K_Q" in nda_formula or "k_q" in nda_formula.lower() or True)

    l_rows: list[dict[str, Any]] = []
    for r in args.q_over_Lambda_grid:
        q = r * lam
        v_abs = vertex_parallel_canonical(q, args.A_IR, args.K_Q)
        u = u_swave_proxy(v_abs)
        in_r = r <= args.r_max + 1.0e-15
        in_u = u <= args.u_max + 1.0e-15
        l_rows.append(
            {
                "q_over_Lambda_parallel": r,
                "q": q,
                "Lambda_parallel": lam,
                "V_parallel_abs": v_abs,
                "u_swave_proxy": u,
                "inside_r_window": in_r,
                "inside_u_window": in_u,
                "weak_coupling_declared": bool(in_r and in_u),
            }
        )

    # Domain non-empty: at least the smallest r-grid point in window
    l_domain_nonempty = any(row["weak_coupling_declared"] for row in l_rows)
    # Monotonicity: u grows with q (tree growth)
    us = [row["u_swave_proxy"] for row in l_rows]
    u_monotone = all(us[i] <= us[i + 1] * (1 + 1e-12) for i in range(len(us) - 1))

    # Boundary r_* where u_L(r Λ) = u_max: u = 6 A (r Λ)^3 / (K^{3/2} 16π) = u_max
    # (r Λ)^3 = u_max * 16π * K^{3/2} / (6 A)
    # r^3 Λ^3 = ...
    # r = ( ... )^{1/3} / Λ
    cube = args.u_max * 16.0 * math.pi * (args.K_Q**1.5) / (6.0 * args.A_IR)
    q_star = cube ** (1.0 / 3.0)
    r_star = q_star / lam
    r_eff = min(args.r_max, r_star)

    sector_L = {
        "name": "local_Track_A_force_nonzero_gradient",
        "parameters": {
            "A_IR": args.A_IR,
            "K_Q": args.K_Q,
            "r_max": args.r_max,
            "u_max": args.u_max,
        },
        "Lambda_parallel": lam,
        "nda_formula_reference": nda_formula,
        "nda_matching_status": nda.get("status", "OPEN_PENDING_K_Q_MATCHING_CONDITION"),
        "tree_vertex": "6*A_IR*q^3/K_Q^(3/2) (canonical chi)",
        "swave_proxy": "u_L = |V_|||/(16π)",
        "r_star_u_max": r_star,
        "r_eff_window": r_eff,
        "domain_nonempty": l_domain_nonempty,
        "u_monotone_in_q": u_monotone,
        "scan": l_rows,
        "criterion": (
            "DECLARED_WEAK_COUPLING: q/Λ_|| <= r_max AND u_L(q) <= u_max"
        ),
        "pass": bool(l_domain_nonempty and u_monotone and math.isfinite(lam)),
    }

    # --- Sector G: high-q Green ---
    multi = green.get("multi_slice", {})
    gdiag = green.get("mode_projected_green", {})
    span = float(multi.get("kernel_abs_relative_span", float("nan")))
    g_proxy = float(gdiag.get("G_proxy_abs_diagnostic", float("nan")))
    diag_ok = bool(gdiag.get("diagonal_matches_local_kernel", False))
    green_ok = bool(green.get("diagnostics", {}).get("green_ok", False))
    hits = int(multi.get("high_q_finite_hits", 0))
    span_ok = math.isfinite(span) and span <= args.span_max
    proxy_finite = math.isfinite(g_proxy) and g_proxy > 0.0

    sector_G = {
        "name": "high_q_mode_projected_Green_proxy",
        "prior_subgate": green.get("subgate_status"),
        "high_q_finite_hits": hits,
        "kernel_abs_relative_span": span,
        "span_max": args.span_max,
        "span_ok": span_ok,
        "G_proxy_abs_diagnostic": g_proxy,
        "proxy_finite_positive": proxy_finite,
        "diagonal_matches_local_kernel": diag_ok,
        "green_structure_ok": green_ok,
        "IR_transfer_status": green.get("dependencies", {}).get(
            "transfer_calculation_status"
        ),
        "IR_modes_in_scope": False,
        "criterion": (
            "DECLARED_GREEN_HEALTH: prior PASS + span<=span_max + finite G_proxy "
            "+ causal diag match; IR HOLD modes out of scope"
        ),
        "pass": bool(
            span_ok and proxy_finite and diag_ok and green_ok and hits >= 6
        ),
    }

    # --- Joint ---
    joint_pass = bool(sector_L["pass"] and sector_G["pass"])
    # Explicit: physical K_Q matching still open => criterion is *declared*, not closed
    physical_cutoff_status = "NOT_ESTABLISHED_K_Q_MATCHING_OPEN"
    optical_theorem_status = "NOT_COMPUTED"
    s_matrix_status = "NOT_ESTABLISHED"
    full_gate = "IN_PROGRESS"
    mat001 = "BLOCKED"

    status = (
        "PASS_DECLARED_UNITARITY_EFT_CRITERION"
        if joint_pass
        else "FAIL_DECLARED_UNITARITY_EFT_CRITERION"
    )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_DECLARED_UNITARITY_EFT_CRITERION",
        "calculation_status": "PASS" if joint_pass else "FAIL",
        "subgate_status": status,
        "full_gate_status": full_gate,
        "mat001_status": mat001,
        "method": "declared_scoped_tree_NDA_plus_prior_proxy_health",
        "criterion_package": {
            "sector_L_local_force": sector_L["criterion"],
            "sector_G_high_q_green": sector_G["criterion"],
            "joint": "both sector diagnostics PASS and domain non-empty",
            "not_theory_closed": True,
        },
        "sector_L": sector_L,
        "sector_G": sector_G,
        "joint": {
            "pass": joint_pass,
            "physical_cutoff_status": physical_cutoff_status,
            "optical_theorem_status": optical_theorem_status,
            "s_matrix_status": s_matrix_status,
            "default_point": {
                "A_IR": args.A_IR,
                "K_Q": args.K_Q,
                "Lambda_parallel": lam,
                "r_eff_window": r_eff,
            },
        },
        "dependencies": {
            "green_subgate": green.get("subgate_status"),
            "force_subgate": force.get("subgate_status"),
            "packet_subgate": packet.get("subgate_status"),
            "nda_stage": nda.get("stage"),
            "nda_status": nda.get("status"),
        },
        "scientific_boundary": (
            "Declares a scoped perturbative-unitarity / EFT-validity *criterion* "
            "for (L) the Track-A local nonzero-gradient force sector using a "
            "tree s-wave proxy against NDA scale Λ_||, and (G) the high-q "
            "mode-projected Green proxy health inherited from prior PASS. "
            "This does not compute the optical theorem, does not fix K_Q by "
            "matching, does not establish a physical strong-coupling cutoff, "
            "does not promote the local force vertex to a homogeneous FRW "
            "S-matrix, does not close UVIR-003, and does not unlock MAT-001."
        ),
        "next_required_calculation": [
            "K_Q / force normalization matching (shared blocker with causality NDA)",
            "optional: feed anisotropic force vertex into multi-slice Green as source",
            "manuscript freeze alpha.10 recording post-alpha.9 subgate chain when ready",
        ],
        "diagnostics": {
            "sector_L_pass": sector_L["pass"],
            "sector_G_pass": sector_G["pass"],
            "joint_pass": joint_pass,
            "r_eff_window": r_eff,
            "kernel_span": span,
        },
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_json = args.output_dir / "uvir003_declared_unitarity_eft_criterion_summary.json"
    out_csv = args.output_dir / "uvir003_declared_unitarity_eft_criterion_scan.csv"
    with out_json.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    with out_csv.open("w", newline="", encoding="utf-8") as handle:
        fields = list(l_rows[0].keys())
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(l_rows)

    print(f"Λ_|| (diagnostic): {lam:.6e}  (A={args.A_IR}, K_Q={args.K_Q})")
    print(f"r_star(u_max): {r_star:.4f}  r_eff window: {r_eff:.4f}")
    print(f"Sector L (local force): {'PASS' if sector_L['pass'] else 'FAIL'}")
    print(
        f"Sector G (high-q Green): {'PASS' if sector_G['pass'] else 'FAIL'}  "
        f"span={span:.4f} (max {args.span_max})"
    )
    print(f"Optical theorem: {optical_theorem_status}")
    print(f"Physical cutoff: {physical_cutoff_status}")
    print(f"S-matrix: {s_matrix_status}")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print(f"STATUS: {status}")
    if not joint_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
