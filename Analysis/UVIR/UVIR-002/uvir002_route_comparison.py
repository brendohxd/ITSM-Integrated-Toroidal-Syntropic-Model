#!/usr/bin/env python3
"""UVIR-002 symbolic route comparison.

This calculation compares three successor routes after UVIR-001 rejected the
canonical single-complex-scalar matching candidate.  A PASS means that the
algebraic checks and report generation succeeded.  It does not mean that a
microscopic UV completion has been found.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import sympy as sp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs",
        help="Directory for the JSON summary and route score CSV.",
    )
    return parser.parse_args()


def require_zero(name: str, expression: sp.Expr) -> None:
    simplified = sp.simplify(expression)
    if isinstance(simplified, sp.MatrixBase):
        is_zero = simplified == sp.zeros(*simplified.shape)
    else:
        is_zero = simplified == 0
    if not is_zero:
        raise AssertionError(f"{name} failed: {simplified}")


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Route A: nonrelativistic P(X) on the static, gradient-dominated branch.
    # Write u=-X>0 so that the branch is real and all sign tests are explicit.
    u, kappa_nr, mass, q = sp.symbols("u kappa_nr m q", positive=True)
    p_minus_u = -kappa_nr * u ** sp.Rational(3, 2)
    # Since X=-u, d/dX=-d/du.
    p_x = sp.simplify(-sp.diff(p_minus_u, u))
    p_xx = sp.simplify(sp.diff(p_x, u) * (-1))
    p_static = sp.simplify(p_minus_u.subs(u, q**2 / (2 * mass)))
    expected_static = -kappa_nr * q**3 / (2 * mass) ** sp.Rational(3, 2)
    require_zero("route A static cubic", p_static - expected_static)
    require_zero(
        "route A P_X",
        p_x - sp.Rational(3, 2) * kappa_nr * sp.sqrt(u),
    )
    require_zero(
        "route A P_XX",
        p_xx + sp.Rational(3, 4) * kappa_nr / sp.sqrt(u),
    )
    route_a_time_kinetic_sign = sp.signsimp(p_xx)
    if route_a_time_kinetic_sign != -1:
        # SymPy does not always reduce a manifestly negative positive-symbol
        # expression to -1, so check its numerator sign explicitly as well.
        if not p_xx.could_extract_minus_sign():
            raise AssertionError(f"route A ghost sign not established: {p_xx}")

    # Route C: separate temporal Q and spatial Y invariants.  Around a nonzero
    # background spatial gradient v=(q,0,0), E=A|v+grad(phi)|^3 has a positive
    # Hessian.  This is a local branch test, not a full constraint analysis.
    amplitude, f_time = sp.symbols("A F", positive=True)
    dx, dy, dz = sp.symbols("dx dy dz", real=True)
    energy = amplitude * ((q + dx) ** 2 + dy**2 + dz**2) ** sp.Rational(3, 2)
    fluctuations = (dx, dy, dz)
    hessian = sp.Matrix(
        [[sp.diff(energy, a, b) for b in fluctuations] for a in fluctuations]
    ).subs({dx: 0, dy: 0, dz: 0})
    hessian = sp.simplify(hessian)
    expected_hessian = sp.diag(6 * amplitude * q, 3 * amplitude * q, 3 * amplitude * q)
    require_zero("route C spatial Hessian", hessian - expected_hessian)

    speed_sq_longitudinal = sp.simplify(hessian[0, 0] / f_time**2)
    speed_sq_transverse = sp.simplify(hessian[1, 1] / f_time**2)
    require_zero(
        "route C longitudinal speed",
        speed_sq_longitudinal - 6 * amplitude * q / f_time**2,
    )
    require_zero(
        "route C transverse speed",
        speed_sq_transverse - 3 * amplitude * q / f_time**2,
    )
    require_zero("route C zero-gradient longitudinal limit", sp.limit(speed_sq_longitudinal, q, 0))
    require_zero("route C zero-gradient transverse limit", sp.limit(speed_sq_transverse, q, 0))

    rows = [
        {
            "route": "A_NONREL_SINGLE_FIELD",
            "spatial_cubic": "YES",
            "healthy_time_kinetic": "NO",
            "stable_target_branch": "NO",
            "controlled_zero_gradient": "NO",
            "coefficient_derived": "NO",
            "matter_lensing_path": "INCOMPLETE",
            "preserves_itsm_core": "PARTIAL",
            "classification": "REJECTED",
            "notes": "Static X<0 branch is cubic, but P_XX<0 gives a ghost in the zero-temperature single-field theory.",
        },
        {
            "route": "B_TWO_FIELD_SPLIT",
            "spatial_cubic": "BY_POSTULATE",
            "healthy_time_kinetic": "POSSIBLE",
            "stable_target_branch": "CONDITIONAL",
            "controlled_zero_gradient": "INCOMPLETE",
            "coefficient_derived": "NO",
            "matter_lensing_path": "INCOMPLETE",
            "preserves_itsm_core": "YES",
            "classification": "CONDITIONAL",
            "notes": "Separates density and force roles, but does not itself derive or regularize the force operator.",
        },
        {
            "route": "C_PREFERRED_FRAME_FORCE_EFT",
            "spatial_cubic": "YES",
            "healthy_time_kinetic": "POSSIBLE",
            "stable_target_branch": "CONDITIONAL",
            "controlled_zero_gradient": "NO_IN_TRUNCATION",
            "coefficient_derived": "NO",
            "matter_lensing_path": "YES_IN_FULL_METRIC_VECTOR_THEORY",
            "preserves_itsm_core": "PARTIAL",
            "classification": "CONDITIONAL",
            "notes": "Independent Q and Y invariants avoid the single-invariant no-go; the cubic truncation degenerates at zero gradient.",
        },
        {
            "route": "SELECTED_TWO_SECTOR_PREFERRED_FRAME",
            "spatial_cubic": "YES_AS_EFT_INPUT",
            "healthy_time_kinetic": "POSSIBLE",
            "stable_target_branch": "TO_TEST",
            "controlled_zero_gradient": "TO_TEST",
            "coefficient_derived": "NO",
            "matter_lensing_path": "CANDIDATE",
            "preserves_itsm_core": "YES",
            "classification": "PROVISIONALLY_SELECTED",
            "notes": "Retain Phi for condensate/topology and use a separate preferred-frame force sector; requires UVIR-003.",
        },
    ]

    score_path = args.output_dir / "uvir002_route_scores.csv"
    with score_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "gate": "UVIR-002",
        "validation_status": "PASS",
        "microscopic_closure": "OPEN",
        "route_a": {
            "verdict": "REJECTED",
            "static_lagrangian": str(p_static),
            "P_X": str(p_x),
            "P_XX": str(p_xx),
            "reason": "The target X<0 branch has negative quadratic time kinetic coefficient.",
        },
        "route_b": {
            "verdict": "CONDITIONAL",
            "reason": "Role separation is useful but does not derive the spatial cubic or its coefficient.",
        },
        "route_c": {
            "verdict": "CONDITIONAL",
            "spatial_hessian": [[str(value) for value in row] for row in hessian.tolist()],
            "longitudinal_speed_squared": str(speed_sq_longitudinal),
            "transverse_speed_squared": str(speed_sq_transverse),
            "reason": "Independent temporal and spatial invariants admit a healthy local nonzero-gradient branch, but the minimal cubic truncation degenerates at zero gradient.",
        },
        "selected_route": "TWO_SECTOR_PREFERRED_FRAME_FORCE_EFT",
        "selection_status": "PROVISIONAL",
        "selected_architecture": {
            "background_sector": "Complex condensate Phi retains finite density, circulation, defects, and topology.",
            "force_sector": "Separate psi and preferred frame U define independent temporal Q and spatial Y invariants.",
        },
        "next_gate": "UVIR-003",
        "mat001_status": "BLOCKED_PENDING_UVIR_003",
        "interpretation": "PASS validates the comparison calculation; it does not establish a microscopic completion.",
    }
    summary_path = args.output_dir / "uvir002_summary.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("UVIR-002 calculation validation: PASS")
    print("Route A verdict: REJECTED")
    print("Route B verdict: CONDITIONAL")
    print("Route C verdict: CONDITIONAL")
    print("Selected route: TWO_SECTOR_PREFERRED_FRAME_FORCE_EFT (PROVISIONAL)")
    print("Microscopic closure: OPEN")
    print("MAT-001: BLOCKED_PENDING_UVIR_003")
    print("STATUS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
