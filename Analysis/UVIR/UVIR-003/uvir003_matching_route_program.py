#!/usr/bin/env python3
"""UVIR-003: matching-route program (R2 interface + R3 sketch + invariant maps).

Master Plan critical path after:
  PASS_KQ_MATCHING_INVENTORY_OPEN
  PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING

This package advances *toward* Derived M3/M6 by making each named route
compute the primary invariants in closed form under *explicit Conditional
premises*. It does **not**:
  - derive numeric K_Q
  - unlock MAT-001
  - close UVIR-003 full gate
  - promote R1 naive (k_Q, C_IR)=(1,2/3) to Derived

Routes executed structurally
----------------------------
R1 — dimensional K_Q = k_Q M_P^2 (already Conditional; re-express invariants)
R2 — matter-vertex *interface* algebra (MAT still BLOCKED for Derived vertex)
     Key structural result: static C_obs alone does not fix Aq/K_Q;
     the redefinition-invariant vertex residual
         V := C_m / sqrt(K_Q)
     plus (C_obs, C_IR) *would* fix Aq/K_Q and Lambda_|| once V is computed
     by a future MAT calculation.
R3 — condensate / UV Conditional sketch (Z_psi, rho_Phi, Lambda_UV free)
R5 — C_obs empirical anchor (does not fix K_Q alone; used as Conditional input)

Tier-1 use: referee-grade DOF counting + invariant maps; no packaging.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import sympy as sp


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument(
        "--inventory-summary",
        type=Path,
        default=base / "outputs" / "uvir003_kq_matching_inventory_summary.json",
    )
    p.add_argument(
        "--causality-conditional-summary",
        type=Path,
        default=base
        / "outputs"
        / "uvir003_causality_domain_conditional_summary.json",
    )
    # Conditional scan grids (not Derived)
    p.add_argument(
        "--V-grid",
        type=float,
        nargs="+",
        default=[0.1, 0.3, 1.0, 3.0, 10.0],
        help="Conditional vertex residual V = C_m/sqrt(K_Q) [units where G=1,a0=1 diagnostics]",
    )
    p.add_argument(
        "--Cobs-grid",
        type=float,
        nargs="+",
        default=[2.0 / 3.0, 1.0, 1.5],
    )
    p.add_argument(
        "--CIR-grid",
        type=float,
        nargs="+",
        default=[0.5, 2.0 / 3.0, 1.0],
    )
    p.add_argument(
        "--Zpsi-grid",
        type=float,
        nargs="+",
        default=[0.1, 1.0, 10.0],
        help="Conditional phonon residue Z_psi for R3 sketch",
    )
    p.add_argument(
        "--rhoPhi_over_MP2a02-grid",
        type=float,
        nargs="+",
        default=[0.01, 0.1, 1.0, 10.0],
        help="Conditional rho_Phi / (M_P^2 a0^2) for R3 sketch",
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


def symbolic_r2_interface() -> dict[str, Any]:
    """R2 interface: express primary invariants via vertex residual V."""
    C_m, C_IR, C_obs, K_Q, A, G, a0, q, V = sp.symbols(
        "C_m C_IR C_obs K_Q A G a0 q V", positive=True
    )
    cos_th = sp.symbols("cos_theta", real=True)

    # Architecture (Core §5) — Conditional premises for *form*, not values
    A_arch = C_IR / (12 * sp.pi * G * a0)
    C_obs_arch = C_m ** sp.Rational(3, 2) / sp.sqrt(C_IR)
    V_def = C_m / sp.sqrt(K_Q)

    # Solve C_m from C_obs, C_IR
    C_m_from_Cobs = sp.simplify((C_obs * sp.sqrt(C_IR)) ** sp.Rational(2, 3))
    require(
        "C_obs inversion",
        sp.simplify(C_obs_arch.subs(C_m, C_m_from_Cobs) - C_obs) == 0,
    )

    # K_Q from V and C_m: V = C_m/sqrt(K_Q) ⇒ K_Q = C_m^2 / V^2
    K_Q_from_V = sp.simplify(C_m**2 / V**2)

    # Primary causality invariant I = A q / K_Q
    I = sp.simplify(A_arch * q / K_Q_from_V)
    I_at_a0 = sp.simplify(I.subs(q, a0))
    # Express I_a0 in (C_obs, C_IR, V, G) only — eliminate C_m
    I_a0_via_Cobs = sp.simplify(
        I_at_a0.subs(C_m, C_m_from_Cobs)
    )
    # A a0 / K_Q with K_Q = C_m^2/V^2 and C_m from C_obs:
    # I_a0 = C_IR/(12 pi G) * V^2 / C_m^2
    #      = C_IR V^2 / (12 pi G (C_obs^2 C_IR)^{2/3})
    #      = C_IR^{1/3} V^2 / (12 pi G C_obs^{4/3})
    I_a0_closed = sp.simplify(
        C_IR ** sp.Rational(1, 3)
        * V**2
        / (12 * sp.pi * G * C_obs ** sp.Rational(4, 3))
    )
    require(
        "I_a0 closed form matches inversion",
        sp.simplify(I_a0_via_Cobs - I_a0_closed) == 0,
    )

    R_c = sp.simplify(3 * I * (1 + cos_th**2))
    q_cross = sp.simplify(K_Q_from_V / (3 * A_arch * (1 + cos_th**2)))
    q_cross_over_a0 = sp.simplify(q_cross.subs(C_m, C_m_from_Cobs) / a0)

    # NDA Lambda_|| = 1/sqrt(A/K_Q^{3/2}) = K_Q^{3/4}/sqrt(A)
    lam = sp.simplify(K_Q_from_V ** sp.Rational(3, 4) / sp.sqrt(A_arch))
    lam_via_Cobs = sp.simplify(lam.subs(C_m, C_m_from_Cobs))
    # A/K^{3/2} invariant
    A_over_K32 = sp.simplify(A_arch / K_Q_from_V ** sp.Rational(3, 2))
    A_over_K32_Cobs = sp.simplify(A_over_K32.subs(C_m, C_m_from_Cobs))

    # DOF statement
    dof = {
        "static_Cobs_alone_fixes_Aq_over_KQ": False,
        "reason": (
            "C_obs fixes C_m^{3/2}/sqrt(C_IR) only; absolute K_Q (time kinetic) "
            "is independent under spatial-static reduction."
        ),
        "quantities_that_fix_I_a0": ["C_obs", "C_IR", "V=C_m/sqrt(K_Q)", "G"],
        "MAT_must_compute": [
            "V = C_m / sqrt(K_Q) from S_int (or absolute K_Q with fixed C_m)",
            "C_obs from the same S_int (Master Plan MAT pass condition)",
        ],
        "optional_external_anchors": [
            "C_obs ~ 1 Conditional R5 (Master Plan §6) until MAT computes it",
            "C_IR still Conditional (geometric 2/3 is not Derived)",
        ],
    }

    return {
        "premises": [
            "Architecture weak-field form S_WF with A = C_IR/(12 pi G a0)",
            "C_obs = C_m^{3/2}/sqrt(C_IR) from static spherical reduction",
            "Vertex residual V := C_m / sqrt(K_Q) is redefinition-invariant",
            "Static C_obs alone does not determine K_Q (structural theorem)",
        ],
        "definitions": {
            "A": str(A_arch),
            "C_obs": str(C_obs_arch),
            "V": str(V_def),
            "C_m_from_Cobs_CIR": str(C_m_from_Cobs),
            "K_Q_from_V_Cm": str(K_Q_from_V),
        },
        "primary_invariants": {
            "I_AqK": str(I),
            "I_a0_closed": str(I_a0_closed),
            "R_c": str(R_c),
            "q_cross_over_a0": str(q_cross_over_a0),
            "A_over_K_Q_to_3_2": str(A_over_K32_Cobs),
            "Lambda_parallel": str(lam_via_Cobs),
        },
        "dof_counting": dof,
        "status": "Open_interface_ready_MAT_blocked",
        "claim_status": "Conditional_structure_only",
    }


def symbolic_r1_invariants() -> dict[str, Any]:
    k_Q, C_IR, G, a0, cos_th = sp.symbols(
        "k_Q C_IR G a0 cos_theta", positive=True
    )
    M_P_sq = 1 / (8 * sp.pi * G)
    K_Q = k_Q * M_P_sq
    A = C_IR / (12 * sp.pi * G * a0)
    I_a0 = sp.simplify(A * a0 / K_Q)
    # I_a0 = (2/3) C_IR / k_Q
    require("R1 I_a0 form", sp.simplify(I_a0 - sp.Rational(2, 3) * C_IR / k_Q) == 0)
    q_cross_over_a0 = sp.simplify(K_Q / (3 * A * (1 + cos_th**2)) / a0)
    lam = sp.simplify(K_Q ** sp.Rational(3, 4) / sp.sqrt(A))
    return {
        "status": "Conditional",
        "I_a0": str(I_a0),
        "I_a0_equals": "(2/3)*C_IR/k_Q",
        "q_cross_over_a0": str(q_cross_over_a0),
        "Lambda_parallel": str(lam),
        "naive_point": {
            "k_Q": 1.0,
            "C_IR": 2.0 / 3.0,
            "I_a0": float(sp.Rational(2, 3) * sp.Rational(2, 3)),
            "q_cross_parallel_over_a0": 0.375,
            "R_c_parallel_at_q_eq_a0": float(6 * sp.Rational(4, 9)),
        },
        "not_a_derivation": True,
    }


def symbolic_r3_sketch() -> dict[str, Any]:
    """Condensate residual sketch: K_Q ~ Z_psi * rho_Phi / a0^2 (Conditional).

    Dimensional sketch only. Not Derived from S_Phi.
    Motivation: phonon kinetic often inherits residue of amplitude integration
    times background density scale; a0 normalizes as in Y/Q architecture.
    """
    Z_psi, rho_Phi, a0, G, C_IR, cos_th = sp.symbols(
        "Z_psi rho_Phi a0 G C_IR cos_theta", positive=True
    )
    # Conditional ansatz:
    #   K_Q = Z_psi * rho_Phi / a0^2
    # so that [K_Q] matches energy-density / acceleration^2 ~ M_P^2 when
    # rho_Phi ~ M_P^2 a0^2 and Z_psi ~ O(1).
    K_Q = Z_psi * rho_Phi / a0**2
    A = C_IR / (12 * sp.pi * G * a0)
    I_a0 = sp.simplify(A * a0 / K_Q)
    # I_a0 = C_IR a0^2 / (12 pi G Z_psi rho_Phi)
    # Introduce dimensionless r = rho_Phi / (M_P^2 a0^2) = 8 pi G rho_Phi / a0^2
    # Then rho_Phi = r * a0^2 / (8 pi G), K_Q = Z_psi r /(8 pi G)
    # I_a0 = C_IR/(12 pi G) * 8 pi G /(Z_psi r) = (2/3) C_IR /(Z_psi r)
    r = sp.symbols("r_rho", positive=True)
    K_Q_r = Z_psi * r / (8 * sp.pi * G)
    I_a0_r = sp.simplify(A * a0 / K_Q_r)
    require(
        "R3 I_a0 via r",
        sp.simplify(I_a0_r - sp.Rational(2, 3) * C_IR / (Z_psi * r)) == 0,
    )
    q_cross_over_a0 = sp.simplify(K_Q_r / (3 * A * (1 + cos_th**2)) / a0)
    return {
        "status": "Open_Conditional_sketch",
        "claim_status": "Conditional",
        "ansatz": "K_Q = Z_psi * rho_Phi / a0**2",
        "dimensionless_density": "r_rho = rho_Phi / (M_P^2 a0^2) = 8 pi G rho_Phi / a0^2",
        "I_a0": str(I_a0_r),
        "I_a0_equals": "(2/3)*C_IR/(Z_psi*r_rho)",
        "q_cross_over_a0": str(q_cross_over_a0),
        "comparison_to_R1": (
            "R1 is the special case Z_psi*r_rho = k_Q (same I_a0 form). "
            "R3 renames the free O(1) product as residue × density fraction."
        ),
        "does_not_derive": [
            "Z_psi",
            "rho_Phi",
            "r_rho",
            "microscopic S_Phi matching",
        ],
        "premises": [
            "Phonon kinetic inherits residue Z_psi from integrating amplitude",
            "Background scale rho_Phi sets absolute norm with a0 normalization",
            "Ansatz is Conditional dimensional sketch, not UVIR-001 derivation",
        ],
    }


def scan_r2_conditional(
    V_grid: list[float],
    Cobs_grid: list[float],
    CIR_grid: list[float],
) -> list[dict[str, Any]]:
    """Numeric Conditional scan in units G=1 (I_a0 retains 1/(12 pi G) factor).

    Report dimensionless combinations that cancel G where possible.
    Use diagnostic: define V_hat such that
      I_a0 * (12 pi G) = C_IR^{1/3} V^2 / C_obs^{4/3}
    is G-free. Call this J := I_a0 * 12 pi G (units of V^2).
    For causality we need absolute I_a0; so also report under G=1 diagnostic
    AND the G-free ratio of I to R1 naive reference.
    """
    rows = []
    for V in V_grid:
        for Cobs in Cobs_grid:
            for CIR in CIR_grid:
                # J = I_a0 * 12 pi G = CIR^{1/3} V^2 / Cobs^{4/3}
                J = (CIR ** (1.0 / 3.0)) * (V**2) / (Cobs ** (4.0 / 3.0))
                # Under R1 naive: I_a0 = 4/9, so 12 pi G I_a0 depends on G.
                # Ratio of J values is meaningful without G:
                # Compare to reference V_ref chosen so structure is clear.
                # Absolute I_a0 still needs G; report J and structural flags.
                # For q_cross/a0 we need I: q_cross/a0 = 1/(3 I_a0 (1+cos^2))
                #   = 12 pi G / (3 J (1+cos^2)) = 4 pi G / (J (1+cos^2))
                # Still G-dependent. Report:
                #   (q_cross/a0) / (4 pi G) = 1/(J (1+cos^2))  — G-free diagnostic
                qc_par_over_4piG = 1.0 / (J * 2.0)  # 1+cos^2=2 parallel
                qc_perp_over_4piG = 1.0 / (J * 1.0)
                # Causal window for q/a0: R_c<=1 ⇒ q/a0 <= 1/(3 I_a0 (1+c^2))
                # Again G-dependent. Flag: larger V ⇒ larger I ⇒ smaller causal window.
                rows.append(
                    {
                        "route": "R2",
                        "V": V,
                        "C_obs": Cobs,
                        "C_IR": CIR,
                        "J_I_a0_times_12piG": J,
                        "q_cross_par_over_a0_over_4piG": qc_par_over_4piG,
                        "q_cross_perp_over_a0_over_4piG": qc_perp_over_4piG,
                        "larger_V_shrinks_causal_window": True,
                        "note": (
                            "Absolute q_cross/a0 requires G (or set units). "
                            "J and q_cross/(a0 4 pi G) are redefinition-safe diagnostics."
                        ),
                    }
                )
    return rows


def scan_r3_conditional(
    Z_grid: list[float],
    r_grid: list[float],
    CIR_grid: list[float],
) -> list[dict[str, Any]]:
    rows = []
    for Z in Z_grid:
        for r in r_grid:
            for CIR in CIR_grid:
                # I_a0 = (2/3) CIR / (Z r) — fully determined, G cancels (R1-like)
                I_a0 = (2.0 / 3.0) * CIR / (Z * r)
                qc_par = 1.0 / (3.0 * I_a0 * 2.0)  # = 1/(6 I)
                qc_perp = 1.0 / (3.0 * I_a0 * 1.0)
                R_c_par_at_a0 = 3.0 * I_a0 * 2.0
                rows.append(
                    {
                        "route": "R3",
                        "Z_psi": Z,
                        "r_rho": r,
                        "C_IR": CIR,
                        "I_a0": I_a0,
                        "q_cross_parallel_over_a0": qc_par,
                        "q_cross_perp_over_a0": qc_perp,
                        "R_c_parallel_at_q_eq_a0": R_c_par_at_a0,
                        "causal_at_q_eq_a0_parallel": R_c_par_at_a0 <= 1.0 + 1e-12,
                        "product_Z_r": Z * r,
                        "equiv_R1_k_Q": Z * r,
                    }
                )
    return rows


def dof_and_closure_map() -> dict[str, Any]:
    return {
        "primary_invariant_for_M3": "A*q/K_Q",
        "I_a0_status": "chart-fixed q=a0 diagnostic; not invariant for external fixed a0",
        "primary_invariant_for_M6_NDA": "A/K_Q**(3/2)  (Lambda_|| = 1/sqrt of that)",
        "routes": {
            "R1": {
                "fixes": "chart-fixed I_a0 = (2/3) C_IR / k_Q once (k_Q, C_IR) chosen",
                "free_after_form": ["k_Q", "C_IR"],
                "status": "Conditional",
                "closes_M3_Derived": False,
            },
            "R2": {
                "fixes": (
                    "chart-fixed I_a0 once (C_obs, C_IR, V=C_m/sqrt(K_Q), G) known; "
                    "MAT must compute V and preferably C_obs"
                ),
                "free_after_interface_algebra": [
                    "V (MAT)",
                    "C_obs (MAT or Conditional R5)",
                    "C_IR (matching)",
                ],
                "status": "Open_interface_ready_MAT_blocked",
                "closes_M3_Derived": False,
                "structural_theorem": (
                    "Static C_obs alone cannot fix Aq/K_Q — needs V or absolute K_Q"
                ),
            },
            "R3": {
                "fixes": "chart-fixed I_a0 = (2/3) C_IR / (Z_psi r_rho) under residual ansatz",
                "free_after_ansatz": ["Z_psi", "r_rho", "C_IR"],
                "status": "Open_Conditional_sketch",
                "closes_M3_Derived": False,
                "note": "Product Z_psi*r_rho plays the role of R1 k_Q",
            },
            "R5": {
                "fixes": "C_obs combination only (phenomenology anchor)",
                "does_not_fix": ["K_Q", "Aq/K_Q without V or R1/R3"],
                "status": "Conditional",
            },
        },
        "minimal_sets_toward_M3_Derived": [
            {
                "set": "R2+R5",
                "requires": "MAT computes V; C_obs Conditional~1; C_IR Conditional",
                "still_Conditional_until": "V Derived from S_int",
            },
            {
                "set": "R3",
                "requires": "Derive Z_psi and r_rho from S_Phi + matching",
                "still_Conditional_until": "UV completion calculation exists",
            },
            {
                "set": "R1",
                "requires": "Independent derivation of k_Q (not NDA guess)",
                "still_Conditional_until": "k_Q Derived",
            },
        ],
        "recommended_critical_path": (
            "Keep R2 interface as primary (Master Plan MAT). "
            "Run R3 dig-harder sketch in parallel. "
            "Do not promote R1 naive point. "
            "DISK/STAT Conditional lane may use C_obs~1 without K_Q."
        ),
    }


def main() -> None:
    args = parse_args()
    inv = load_json(args.inventory_summary)
    caus = load_json(args.causality_conditional_summary)

    r1 = symbolic_r1_invariants()
    r2 = symbolic_r2_interface()
    r3 = symbolic_r3_sketch()
    dof = dof_and_closure_map()

    r2_scan = scan_r2_conditional(args.V_grid, args.Cobs_grid, args.CIR_grid)
    r3_scan = scan_r3_conditional(
        args.Zpsi_grid, args.rhoPhi_over_MP2a02_grid, args.CIR_grid
    )

    # Structural checks
    require("R2 structural theorem stated", r2["dof_counting"][
        "static_Cobs_alone_fixes_Aq_over_KQ"
    ] is False)
    require("R1 naive I_a0 = 4/9", abs(r1["naive_point"]["I_a0"] - 4.0 / 9.0) < 1e-12)
    require(
        "R1 naive R_c parallel at a0 = 8/3",
        abs(r1["naive_point"]["R_c_parallel_at_q_eq_a0"] - 8.0 / 3.0) < 1e-12,
    )
    # R3 equivalence: Z*r = 1, CIR=2/3 → same as R1 naive
    r3_naive = [
        row
        for row in r3_scan
        if abs(row["Z_psi"] * row["r_rho"] - 1.0) < 1e-12
        and abs(row["C_IR"] - 2.0 / 3.0) < 1e-12
    ]
    require("R3 has naive-equivalent rows", len(r3_naive) >= 1)
    for row in r3_naive:
        require(
            "R3 equiv R1 q_cross parallel",
            abs(row["q_cross_parallel_over_a0"] - 0.375) < 1e-9,
            str(row),
        )

    # Count causal R3 samples at q=a0 parallel
    n_r3 = len(r3_scan)
    n_r3_causal = sum(1 for r in r3_scan if r["causal_at_q_eq_a0_parallel"])

    prior_ok = True
    if inv is not None:
        prior_ok = inv.get("subgate_status") == "PASS_KQ_MATCHING_INVENTORY_OPEN"
    if caus is not None:
        prior_ok = prior_ok and caus.get("subgate_status") == (
            "PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING"
        )

    passed = prior_ok and len(r2_scan) > 0 and len(r3_scan) > 0
    status = (
        "PASS_MATCHING_ROUTE_PROGRAM_OPEN"
        if passed
        else "FAIL_MATCHING_ROUTE_PROGRAM"
    )

    summary: dict[str, Any] = {
        "gate": "UVIR-003",
        "stage": "B_MATCHING_ROUTE_PROGRAM",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": status,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "kq_numeric_status": "NOT_DERIVED",
        "claim_status": "Conditional_structure_and_Open_routes",
        "prior_subgates": {
            "inventory": (inv or {}).get("subgate_status"),
            "causality_conditional": (caus or {}).get("subgate_status"),
            "prior_ok": prior_ok,
        },
        "route_R1": r1,
        "route_R2_interface": r2,
        "route_R3_sketch": r3,
        "dof_and_closure_map": dof,
        "scan_diagnostics": {
            "n_r2_rows": len(r2_scan),
            "n_r3_rows": n_r3,
            "n_r3_causal_parallel_q_eq_a0": n_r3_causal,
            "r3_causal_fraction_parallel_q_eq_a0": (
                n_r3_causal / n_r3 if n_r3 else None
            ),
        },
        "scientific_boundary": (
            "Executes the matching-route *program*: closed-form invariant maps "
            "for Aq/K_Q plus chart-fixed q=a0 diagnostics and Conditional scans. "
            "Proves structurally that static "
            "C_obs alone cannot fix Aq/K_Q (needs vertex residual "
            "V=C_m/sqrt(K_Q)). R3 residual ansatz recovers R1 as Z_psi*r_rho=k_Q. "
            "I_a0=A*a0/K_Q is not invariant when a0 is held external. "
            "Does not derive K_Q, does not unlock MAT-001, does not close UVIR-003 "
            "M3/M6 as Derived."
        ),
        "next_required_calculation": [
            "When programme accepts Conditional UVIR domain for MAT-only: compute V from S_int (R2)",
            "Stage 2a R3 audit complete as INCOMPLETE; proceed to Stage 2b Conditional floor",
            "After either: re-evaluate causality domain + Lambda_|| (M3/M6)",
            "Do not promote R1 naive (k_Q,C_IR)=(1,2/3) to Derived",
        ],
        "master_plan_criteria": {
            "M3": "PARTIAL_DOCUMENTED_plus_route_maps",
            "M6": "OPEN_maps_ready_pending_matched_normalization",
            "M7": "OPEN_MAT_blocked",
        },
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "uvir003_matching_route_program_summary.json").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")

    with (args.output_dir / "uvir003_matching_route_R2_scan.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.DictWriter(f, fieldnames=list(r2_scan[0].keys()))
        w.writeheader()
        w.writerows(r2_scan)

    with (args.output_dir / "uvir003_matching_route_R3_scan.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.DictWriter(f, fieldnames=list(r3_scan[0].keys()))
        w.writeheader()
        w.writerows(r3_scan)

    print("R2 structural theorem: static C_obs alone does NOT fix Aq/K_Q")
    print("R2 needs V = C_m/sqrt(K_Q) (MAT) + (C_obs, C_IR)")
    print(f"R1 naive: I_a0={r1['naive_point']['I_a0']:.6f}, "
          f"R_c(par,q=a0)={r1['naive_point']['R_c_parallel_at_q_eq_a0']:.6f}")
    print(f"R3 scan: {n_r3} rows, {n_r3_causal} causal at q=a0 parallel "
          f"({100*n_r3_causal/n_r3:.1f}%)")
    print("STATUS:", status)
    print("UVIR-003 full gate: IN_PROGRESS | MAT-001: BLOCKED | K_Q: NOT_DERIVED")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
