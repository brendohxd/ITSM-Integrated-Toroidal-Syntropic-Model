#!/usr/bin/env python3
"""VOR-001 Stage S2 Winding-Sector Energy Audit

This executable checks the S2 smooth-winding sector using the declared 
condensate action EOM. It solves for the shifted amplitude rho_0(n) 
and tests for positive definite energy and reflection symmetry.

LABEL: VOR-001-S2
GATE_STATUS: OPEN_SCAFFOLD_ONLY
PHYSICS_PASS: False
"""

import json
import math
from itertools import permutations
from pathlib import Path
import numpy as np

def validate_params(N: int, L1: float, L2: float, L3: float, lam: float, v: float):
    if N < 4:
        raise ValueError("Grid size N must be >= 4")
    if L1 <= 0 or L2 <= 0 or L3 <= 0:
        raise ValueError("Box lengths must be positive")
    if lam <= 0:
        raise ValueError("lambda must be positive")
    if v <= 0:
        raise ValueError("v must be positive")
    if not (math.isfinite(L1) and math.isfinite(L2) and math.isfinite(L3)):
        raise ValueError("Box lengths must be finite")

def compute_omega_sq(n1: int, n2: int, n3: int, L1: float, L2: float, L3: float) -> float:
    return (2 * math.pi)**2 * ((n1/L1)**2 + (n2/L2)**2 + (n3/L3)**2)

def compute_rho0(omega_sq: float, lam: float, v: float) -> float:
    rho_sq = v**2 - omega_sq / lam
    if rho_sq <= 0:
        return 0.0
    return math.sqrt(rho_sq)

def compute_energy(rho0: float, omega_sq: float, L1: float, L2: float, L3: float, lam: float, v: float) -> float:
    V_T3 = L1 * L2 * L3
    kinetic = 0.5 * rho0**2 * omega_sq
    potential = (lam / 4.0) * (rho0**2 - v**2)**2
    return (kinetic + potential) * V_T3

def run_s2_tests():
    N, L, lam, v = 32, 1.0, 100.0, 1.0
    validate_params(N, L, L, L, lam, v)
    checks = []
    
    # S2-T01: EOM rho correction
    omega_sq_1 = compute_omega_sq(1, 0, 0, L, L, L)
    rho0_1 = compute_rho0(omega_sq_1, lam, v)
    expected_deviation = omega_sq_1 / (lam * v**2) # small parameter
    actual_deviation = v**2 - rho0_1**2
    pass_t01 = abs(actual_deviation - (omega_sq_1/lam)) < 1e-10
    checks.append({"id": "S2-T01", "name": "EOM rho correction", "pass": pass_t01})
    
    # S2-T02: S1 limit recovery (requires lambda >> omega_sq)
    lam_limit = 100000.0
    rho0_1_limit = compute_rho0(omega_sq_1, lam_limit, v)
    e_s1 = 0.5 * v**2 * omega_sq_1 * L**3
    e_s2_limit = compute_energy(rho0_1_limit, omega_sq_1, L, L, L, lam_limit, v)
    pass_t02 = abs(e_s2_limit - e_s1) / e_s1 < 0.001 
    checks.append({"id": "S2-T02", "name": "S1 limit recovery", "pass": pass_t02})

    # S2-T03: Winding increases equilibrium energy
    e_s2 = compute_energy(rho0_1, omega_sq_1, L, L, L, lam, v)
    e_0 = compute_energy(compute_rho0(0, lam, v), 0, L, L, L, lam, v)
    pass_t03 = (e_s2 > e_0)
    checks.append({"id": "S2-T03", "name": "Winding increases energy", "pass": pass_t03})
    
    # S2-T04: Reflection degeneracy
    omega_sq_m1 = compute_omega_sq(-1, 0, 0, L, L, L)
    rho0_m1 = compute_rho0(omega_sq_m1, lam, v)
    e_s2_m1 = compute_energy(rho0_m1, omega_sq_m1, L, L, L, lam, v)
    pass_t04 = abs(e_s2 - e_s2_m1) < 1e-10
    checks.append({"id": "S2-T04", "name": "Reflection degeneracy", "pass": pass_t04})

    # S2-T05: Isotropy covariance
    omega_sq_123 = compute_omega_sq(1, 2, 3, L, L, L)
    rho0_123 = compute_rho0(omega_sq_123, lam, v)
    e_base = compute_energy(rho0_123, omega_sq_123, L, L, L, lam, v)
    pass_t05 = True
    for perm in permutations([1, 2, 3]):
        omega_sq_perm = compute_omega_sq(perm[0], perm[1], perm[2], L, L, L)
        rho0_perm = compute_rho0(omega_sq_perm, lam, v)
        e_perm = compute_energy(rho0_perm, omega_sq_perm, L, L, L, lam, v)
        if abs(e_perm - e_base) / e_base > 1e-10:
            pass_t05 = False
    checks.append({"id": "S2-T05", "name": "Isotropy covariance", "pass": pass_t05})

    # S2-T06: Amplitude variation sourced by winding
    omega_sq_2 = compute_omega_sq(2, 0, 0, L, L, L)
    rho0_2 = compute_rho0(omega_sq_2, lam, v)
    pass_t06 = (rho0_2 < rho0_1 < v)
    checks.append({"id": "S2-T06", "name": "Amplitude suppression", "pass": pass_t06})

    all_pass = all(c["pass"] for c in checks)
    
    result = {
        "physics_pass": False,
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "stage": "S2",
        "forbidden_packaging_not_used": ["a0", "C_obs", "resonance", "UVIR"],
        "scientific_boundary": "Tests EOM and energy for purely smooth winding sector with physical parameters but no observational mapping.",
        "checks": checks
    }
    
    out_dir = Path("Analysis/VOR/VOR-001/outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "vor001_stage_s2_energy_summary.json"
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)

    status = "PASS_VOR001_S2_MATH_TEMPLATE_ONLY" if all_pass else "FAIL_VOR001_S2_MATH_TEMPLATE"
    print(status)
    for c in checks:
        print(f"{c['id']} ({c['name']}): {'PASS' if c['pass'] else 'FAIL'}")

if __name__ == "__main__":
    run_s2_tests()
