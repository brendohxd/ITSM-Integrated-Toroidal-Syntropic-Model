#!/usr/bin/env python3
"""UVIR-003 Stage B item 9 (partial): longitudinal force-sector IR NDA estimate.

Order-of-magnitude NDA estimate only, restricted to:
  - the longitudinal (x, i.e. background-gradient direction) mode,
  - the k^2-dominated regime below the k^4 regulator's crossover k_cross,
following the same method UVIR-001 Section 7 already used for the condensate
sector (canonically normalize, read off the scale from the cubic vertex
coefficient). This does not attempt the anisotropic transverse directions,
the k^4-dominated (Lifshitz) regime, or a full unitarity/loop calculation.
The resulting time-normalized derivative scale is not a completed physical
strong-coupling cutoff.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs",
        help="Directory for the strong-coupling estimate JSON summary.",
    )
    return parser.parse_args()


def require_zero(name: str, expression: sp.Expr) -> None:
    if sp.simplify(expression) != 0:
        raise AssertionError(f"{name} failed: {sp.simplify(expression)}")


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    A, q, K_Q, G, a0, C_IR = sp.symbols("A q K_Q G a0 C_IR", positive=True)
    dx, dy, dz = sp.symbols("d_x d_y d_z", real=True)

    # ------------------------------------------------------------------
    # 1. Cubic vertex tensor, verified via direct series expansion (not
    #    just differentiation) of E=A|v+grad(pi)|^3 around v=(q,0,0).
    # ------------------------------------------------------------------
    eps = sp.symbols("epsilon", positive=True)
    energy = A * ((q + eps * dx) ** 2 + (eps * dy) ** 2 + (eps * dz) ** 2) ** sp.Rational(3, 2)
    series = sp.expand(sp.series(energy, eps, 0, 4).removeO())
    poly = sp.Poly(series, eps)
    quad_term = poly.coeff_monomial(eps**2)
    cubic_term = poly.coeff_monomial(eps**3)

    expected_quad = sp.Rational(1, 2) * (6 * A * q * dx**2 + 3 * A * q * dy**2 + 3 * A * q * dz**2)
    expected_cubic = A * dx**3 + sp.Rational(3, 2) * A * dx * dy**2 + sp.Rational(3, 2) * A * dx * dz**2
    require_zero("quadratic term matches Stage-A Hessian", quad_term - expected_quad)
    require_zero("cubic term matches hand derivation", cubic_term - expected_cubic)

    # ------------------------------------------------------------------
    # 2. Longitudinal (x) mode only. Quadratic Lagrangian coefficient (from
    #    L = -E, spatial part): -3Aq(d_x pi)^2. Canonically normalize the
    #    time-kinetic term via chi = sqrt(K_Q) pi (verified dimensionally:
    #    psi/pi is dimensionless, K_Q ~ mass^2, so chi ~ mass, canonical).
    # ------------------------------------------------------------------
    # Cubic term in terms of chi: -A/K_Q^(3/2) * (d_x chi)^3 (x-direction only).
    # Mass dimensions (asserted in prose, not checked symbolically here): psi
    # and its fluctuation pi are dimensionless (grad psi ~ acceleration ~
    # mass^1), so chi=sqrt(K_Q)*pi canonical (mass^1) requires [K_Q]=mass^2;
    # A(d_x pi)^3 having Lagrangian dimension 4 with [d_x pi]=mass^1 requires
    # [A]=mass^1 — consistent with A=C_IR/(12 pi G a0) and [G]=mass^-2.
    g3 = A / K_Q ** sp.Rational(3, 2)
    lambda_nda_longitudinal_ir = sp.simplify(1 / sp.sqrt(g3))  # ~ K_Q^(3/4)/sqrt(A)

    # ------------------------------------------------------------------
    # 3. Substitute A = C_IR/(12 pi G a0) (Core Architecture Section 3.4/4,
    #    cross-checked in UVIR-003_STAGE_A_CAUSALITY_ADDENDUM.md Section 1).
    # ------------------------------------------------------------------
    A_value = C_IR / (12 * sp.pi * G * a0)
    lambda_nda_explicit = sp.simplify(lambda_nda_longitudinal_ir.subs(A, A_value))

    summary = {
        "gate": "UVIR-003",
        "stage": "B_ITEM_9_PARTIAL_LONGITUDINAL_IR_ONLY",
        "method": "NDA_order_of_magnitude_only",
        "cubic_vertex": {
            "quadratic_term_check": "PASS",
            "cubic_term_xxx": "A",
            "cubic_term_xyy": "3A/2",
            "cubic_term_xzz": "3A/2",
        },
        "longitudinal_ir_nda_scale": {
            "formula_in_K_Q_A": str(lambda_nda_longitudinal_ir),
            "formula_with_A_substituted": str(lambda_nda_explicit),
            "interpretation": "time-normalized longitudinal derivative scale in the k^2-dominated IR truncation; not a completed physical EFT cutoff",
            "blocked_by": "K_Q has no matching condition in the current architecture (same gap as the causality addendum's long-wavelength check)",
        },
        "scope_explicitly_excluded": [
            "transverse (y,z) directions — anisotropic normalization not carried through",
            "k^4-dominated (Lifshitz, above k_cross) regime — different NDA structure entirely, not attempted",
            "any loop-level or unitarity-bound calculation — this is O(1)-only NDA, matching the precedent set in UVIR-001 Section 7",
        ],
        "connects_to": "UVIR-003_STAGE_A_CAUSALITY_ADDENDUM.md and ITSM_Claim_Migration_Ledger.csv — both the long-wavelength causality check and this longitudinal IR NDA estimate is blocked on the same missing K_Q matching condition",
        "status": "OPEN_PENDING_K_Q_MATCHING_CONDITION",
    }
    json_path = args.output_dir / "uvir003_force_strong_coupling_estimate_summary.json"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("UVIR-003 Stage B item 9 (longitudinal, IR-only): cubic vertex VERIFIED")
    print(f"Longitudinal IR NDA scale (time-normalized, not physical cutoff): {lambda_nda_longitudinal_ir}")
    print("Numeric evaluation: BLOCKED on missing K_Q matching condition")
    print("STATUS: OPEN_PENDING_K_Q_MATCHING_CONDITION")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
