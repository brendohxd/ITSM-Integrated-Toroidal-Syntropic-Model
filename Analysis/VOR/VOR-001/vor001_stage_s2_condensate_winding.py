#!/usr/bin/env python3
"""VOR-001 Stage S2 — winding-sector energy from declared condensate action.

LABEL: VOR-001_STAGE_S2_CONDENSATE_WINDING_ENERGY
GATE: VOR-001
STAGE: S2
CLAIM: None Derived
physics_pass: false
research_gate_status: OPEN_SCAFFOLD_ONLY
branch: recovery/v12-core-architecture

Predecessor: VOR-001 S1 (PASS_VOR001_S1_MATH_TEMPLATE_ONLY)

Key advance over S1: amplitude rho is NO LONGER FIXED to the constant v.
The winding gradient acts as an effective mass term that shifts the equilibrium
amplitude rho_0(n) away from v. This tests whether smooth winding backgrounds
are self-consistent solutions to the condensate EOM.

Forbidden packaging: no force law, no resonance, no observable prediction,
no UVIR/MAT gate advancement, no a0/H0/C_obs/PTA/SPARC/lensing claims.
"""

from __future__ import annotations

import json
import math
import sys
from itertools import permutations
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import brentq


def validate_params(
    N: int,
    L1: float,
    L2: float,
    L3: float,
    lam: float,
    v: float,
    mu: float,
) -> None:
    """Validate all input parameters."""
    if isinstance(N, bool) or not isinstance(N, int) or N < 8:
        raise ValueError("N must be an integer >= 8")
    for name, val in [("L1", L1), ("L2", L2), ("L3", L3)]:
        if not math.isfinite(val) or val <= 0:
            raise ValueError(f"{name} must be finite and positive")
    if not math.isfinite(lam) or lam <= 0:
        raise ValueError("lambda must be finite and positive")
    if not math.isfinite(v) or v <= 0:
        raise ValueError("v must be finite and positive")
    if not math.isfinite(mu) or mu < 0:
        raise ValueError("mu must be finite and non-negative")


def omega_squared(
    n1: int, n2: int, n3: int,
    L1: float, L2: float, L3: float,
) -> float:
    """Squared winding gradient frequency omega_n^2 = (2pi)^2 * sum(ni^2/Li^2)."""
    return (2 * math.pi) ** 2 * (n1**2 / L1**2 + n2**2 / L2**2 + n3**2 / L3**2)


def dVeff_drho(rho: float, lam: float, v: float, mu: float) -> float:
    """Derivative of V_eff = (lambda/4)(rho^2 - v^2)^2 - (1/2) mu^2 rho^2."""
    return lam * rho * (rho**2 - v**2) - mu**2 * rho


def eom_residual(rho: float, omega_n2: float, lam: float, v: float, mu: float) -> float:
    """EOM residual for constant-amplitude winding background.

    EOM: rho * omega_n^2 + dV_eff/drho = 0
    Rearranged: dV_eff/drho + rho * omega_n^2 = 0
    """
    return dVeff_drho(rho, lam, v, mu) + rho * omega_n2


def solve_eom_rho(
    n1: int, n2: int, n3: int,
    L1: float, L2: float, L3: float,
    lam: float, v: float, mu: float,
) -> float:
    """Solve for rho_0(n) satisfying the winding-corrected EOM.

    For n=(0,0,0): recovers the standard finite-density equilibrium.
    For n != 0: winding gradient shifts rho_0 below v.
    """
    omega2 = omega_squared(n1, n2, n3, L1, L2, L3)

    if omega2 == 0.0:
        # Trivial winding: standard EOM -> rho_0 = v (at mu=0)
        if mu == 0.0:
            return v
        # With mu: solve lam*rho*(rho^2 - v^2) - mu^2*rho = 0
        # => rho^2 = v^2 + mu^2/lam
        return math.sqrt(v**2 + mu**2 / lam)

    # For nonzero winding: use Brent's method
    # Bracket: rho in (epsilon, v) since winding suppresses amplitude
    eps = 1e-10
    hi = v * 2  # allow rho > v in case mu is large

    f_lo = eom_residual(eps, omega2, lam, v, mu)
    f_hi = eom_residual(hi, omega2, lam, v, mu)

    if f_lo * f_hi > 0:
        # Try wider bracket
        hi = v * 10
        f_hi = eom_residual(hi, omega2, lam, v, mu)

    if f_lo * f_hi > 0:
        # No sign change found; return v as fallback (will fail S2-T06)
        return float("nan")

    return brentq(eom_residual, eps, hi, args=(omega2, lam, v, mu), xtol=1e-12)


def compute_winding_energy(
    n1: int, n2: int, n3: int,
    L1: float, L2: float, L3: float,
    lam: float, v: float, mu: float,
    rho_0: float | None = None,
) -> dict[str, float]:
    """Compute total winding-sector energy at EOM-consistent rho_0.

    E = [(1/2) rho_0^2 * omega_n^2 + V_eff(rho_0)] * V_T3

    where V_eff = (lambda/4)(rho_0^2 - v^2)^2 - (1/2) mu^2 rho_0^2.
    """
    V_T3 = L1 * L2 * L3
    omega2 = omega_squared(n1, n2, n3, L1, L2, L3)

    if rho_0 is None:
        rho_0 = solve_eom_rho(n1, n2, n3, L1, L2, L3, lam, v, mu)

    Veff = lam / 4 * (rho_0**2 - v**2) ** 2 - 0.5 * mu**2 * rho_0**2
    E_winding = 0.5 * rho_0**2 * omega2 * V_T3
    E_potential = Veff * V_T3
    E_total = E_winding + E_potential

    return {
        "rho_0": rho_0,
        "omega_n2": omega2,
        "E_winding": E_winding,
        "E_potential": E_potential,
        "E_total": E_total,
        "V_T3": V_T3,
    }


def analytic_S1_energy(
    n1: int, n2: int, n3: int,
    L1: float, L2: float, L3: float,
    lam: float, v: float,
) -> float:
    """S1 analytic energy at rho_0 = v (potential term vanishes).

    E_S1 = (1/2) v^2 (2pi)^2 [n1^2/L1^2 + n2^2/L2^2 + n3^2/L3^2] * V_T3
    """
    V_T3 = L1 * L2 * L3
    omega2 = omega_squared(n1, n2, n3, L1, L2, L3)
    return 0.5 * v**2 * omega2 * V_T3


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

CheckResult = dict[str, Any]


def test_S2_T01_eom_amplitude_correction(
    L: float, lam: float, v: float, mu: float,
) -> CheckResult:
    """S2-T01: EOM rho_0(n) deviates from v; recovers v for large lambda."""
    windings = [(1, 0, 0), (0, 1, 0), (1, 1, 0), (1, 1, 1)]
    results = []
    for n in windings:
        rho_0 = solve_eom_rho(*n, L, L, L, lam, v, mu)
        omega2 = omega_squared(*n, L, L, L)
        # Expected correction: first-order estimate delta_rho ~ -omega2 * v / (2*lam*v^2)
        expected_sign = rho_0 < v  # winding suppresses amplitude (mu=0 case)
        results.append({
            "n": n,
            "rho_0": rho_0,
            "rho_0_vs_v": rho_0 - v,
            "omega2": omega2,
            "is_finite": math.isfinite(rho_0),
        })

    # Large-lambda limit: rho_0 should approach v
    rho_large_lam = solve_eom_rho(1, 0, 0, L, L, L, 1000.0 * lam, v, mu)
    large_lam_ok = abs(rho_large_lam - v) / v < 0.01  # within 1% for 1000x lambda

    all_finite = all(r["is_finite"] for r in results)
    status = "PASS" if all_finite and large_lam_ok else "FAIL"
    return {
        "test": "S2-T01",
        "description": "EOM amplitude correction finite; large-lambda limit recovers v",
        "status": status,
        "results": results,
        "large_lambda_recovery": {"rho_0": rho_large_lam, "deviation": abs(rho_large_lam - v) / v},
    }


def test_S2_T02_S1_limit_recovery(
    L: float, lam_large: float, v: float,
) -> CheckResult:
    """S2-T02: S2 energy reduces to S1 analytic in strong-coupling limit (mu=0)."""
    windings = [(1, 0, 0), (0, 1, 0), (1, 1, 1)]
    results = []
    mu = 0.0
    for n in windings:
        result = compute_winding_energy(*n, L, L, L, lam_large, v, mu)
        E_S1 = analytic_S1_energy(*n, L, L, L, lam_large, v)
        if E_S1 > 0:
            rel_dev = abs(result["E_total"] - E_S1) / E_S1
        else:
            rel_dev = abs(result["E_total"] - E_S1)
        results.append({
            "n": n,
            "E_S2": result["E_total"],
            "E_S1_analytic": E_S1,
            "rel_deviation": rel_dev,
            "rho_0": result["rho_0"],
        })

    all_pass = all(r["rel_deviation"] < 0.001 for r in results)
    return {
        "test": "S2-T02",
        "description": "S2 energy reduces to S1 analytic in strong-coupling (lambda>>1, mu=0)",
        "status": "PASS" if all_pass else "FAIL",
        "lambda": lam_large,
        "results": results,
    }


def test_S2_T03_positive_winding_energy(
    L: float, lam: float, v: float, mu: float,
) -> CheckResult:
    """S2-T03: E(n) > E(0) for all nonzero n at EOM-consistent rho_0."""
    E_0 = compute_winding_energy(0, 0, 0, L, L, L, lam, v, mu)["E_total"]
    windings = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 1, 1), (2, 0, 0)]
    results = []
    for n in windings:
        E_n = compute_winding_energy(*n, L, L, L, lam, v, mu)["E_total"]
        results.append({"n": n, "E_n": E_n, "E_0": E_0, "E_n_gt_E_0": E_n > E_0})
    all_pass = all(r["E_n_gt_E_0"] for r in results)
    return {
        "test": "S2-T03",
        "description": "E(n) > E(0) for all nonzero winding vectors at EOM rho_0",
        "status": "PASS" if all_pass else "FAIL",
        "results": results,
    }


def test_S2_T04_reflection_degeneracy(
    L: float, lam: float, v: float, mu: float,
) -> CheckResult:
    """S2-T04: E(n) = E(-n) to machine precision."""
    windings = [(1, 0, 0), (1, 1, 0), (1, 2, 3), (2, 0, 1)]
    results = []
    for n in windings:
        E_n = compute_winding_energy(*n, L, L, L, lam, v, mu)["E_total"]
        E_mn = compute_winding_energy(*(-x for x in n), L, L, L, lam, v, mu)["E_total"]
        if E_n > 0:
            rel_diff = abs(E_n - E_mn) / E_n
        else:
            rel_diff = abs(E_n - E_mn)
        results.append({"n": n, "E_n": E_n, "E_neg_n": E_mn, "rel_diff": rel_diff})
    all_pass = all(r["rel_diff"] < 1e-10 for r in results)
    return {
        "test": "S2-T04",
        "description": "E(n) = E(-n) exact degeneracy",
        "status": "PASS" if all_pass else "FAIL",
        "tolerance": 1e-10,
        "results": results,
    }


def test_S2_T05_permutation_covariance(
    L: float, lam: float, v: float, mu: float,
) -> CheckResult:
    """S2-T05: E(n1,n2,n3) invariant under permutations (isotropic box)."""
    n_test = (1, 2, 0)
    E_ref = compute_winding_energy(*n_test, L, L, L, lam, v, mu)["E_total"]
    perms = set(permutations(n_test))
    results = []
    for p in perms:
        E_p = compute_winding_energy(*p, L, L, L, lam, v, mu)["E_total"]
        rel_diff = abs(E_p - E_ref) / E_ref if E_ref > 0 else abs(E_p - E_ref)
        results.append({"perm": p, "E_perm": E_p, "rel_diff": rel_diff})
    all_pass = all(r["rel_diff"] < 1e-10 for r in results)
    return {
        "test": "S2-T05",
        "description": "Axis-permutation covariance (isotropic box)",
        "status": "PASS" if all_pass else "FAIL",
        "n_test": n_test,
        "E_ref": E_ref,
        "results": results,
    }


def test_S2_T06_amplitude_suppression(
    L: float, lam: float, v: float,
) -> CheckResult:
    """S2-T06: rho_0(n) decreases monotonically with |n| (isotropic box, mu=0)."""
    mu = 0.0
    sequence = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)]
    rhos = []
    for n in sequence:
        rho_0 = solve_eom_rho(*n, L, L, L, lam, v, mu)
        rhos.append({"n": n, "rho_0": rho_0})
    # Must be monotonically non-increasing
    monotone = all(
        rhos[i + 1]["rho_0"] <= rhos[i]["rho_0"]
        for i in range(len(rhos) - 1)
    )
    return {
        "test": "S2-T06",
        "description": "rho_0(n) monotonically suppressed by increasing winding norm",
        "status": "PASS" if monotone else "FAIL",
        "rho_0_sequence": rhos,
    }


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def main() -> int:
    import argparse
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument("--L", type=float, default=1.0)
    parser.add_argument("--lam", type=float, default=1000.0)  # strong coupling for S1 limit
    parser.add_argument("--lam-large", type=float, default=100000.0)  # S2-T02 large lambda
    parser.add_argument("--v", type=float, default=1.0)
    parser.add_argument("--mu", type=float, default=0.0)
    args = parser.parse_args()

    try:
        validate_params(8, args.L, args.L, args.L, args.lam, args.v, args.mu)
    except ValueError as exc:
        print(f"VALIDATION ERROR: {exc}")
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)

    checks: list[dict[str, Any]] = [
        test_S2_T01_eom_amplitude_correction(args.L, args.lam, args.v, args.mu),
        test_S2_T02_S1_limit_recovery(args.L, args.lam_large, args.v),
        test_S2_T03_positive_winding_energy(args.L, args.lam, args.v, args.mu),
        test_S2_T04_reflection_degeneracy(args.L, args.lam, args.v, args.mu),
        test_S2_T05_permutation_covariance(args.L, args.lam, args.v, args.mu),
        test_S2_T06_amplitude_suppression(args.L, args.lam, args.v),
    ]

    n_pass = sum(1 for c in checks if c["status"] == "PASS")
    n_fail = sum(1 for c in checks if c["status"] == "FAIL")
    overall = "PASS_VOR001_S2_CONDENSATE_WINDING_MATH_TEMPLATE_ONLY" if n_fail == 0 \
        else "FAIL_VOR001_S2_CONDENSATE_WINDING"

    summary = {
        "label": "VOR-001_STAGE_S2_CONDENSATE_WINDING_ENERGY",
        "gate": "VOR-001",
        "stage": "S2",
        "physics_pass": False,
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "status_string": overall,
        "n_pass": n_pass,
        "n_fail": n_fail,
        "n_total": len(checks),
        "forbidden_packaging_not_used": [
            "force_law", "resonance_spectrum", "UVIR_gate_advance",
            "MAT_gate_advance", "a0_claim", "H0_claim", "C_obs_claim",
            "PTA_claim", "SPARC_claim", "lensing_claim",
        ],
        "scientific_boundary": (
            "Tests whether smooth winding backgrounds are self-consistent solutions "
            "to the declared condensate EOM, with amplitude allowed to vary. "
            "Does NOT validate a force law, connect winding to any observable, "
            "or advance any gate above OPEN_SCAFFOLD_ONLY."
        ),
        "checks": checks,
    }

    out_path = args.output_dir / "vor001_stage_s2_condensate_winding_summary.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    for c in checks:
        print(f"  [{c['status']:4s}] {c['test']}: {c['description']}")
    print(f"\nOverall: {overall}")
    print(f"Output: {out_path}")

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
