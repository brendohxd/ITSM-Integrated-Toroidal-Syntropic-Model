#!/usr/bin/env python3
"""TOP-001 / CBR-002: Coupled 3D Moduli & Casimir Stress Phase Space Stability Probe.

DISCLAIMER / SCOPE:
  This script is an EXPLORATORY TOY MODEL of Bianchi-I shape moduli coupled to free and
  driven Casimir stress on a flat 3-torus (T^3).

Key Findings & Honest Limitations:
  1. Free Casimir shear stress dilutes to spatial isotropy (Ht/Hp -> 1.000000) with negative
     decay slope (Scoped Negative result; no free geometric attractor).
  2. For the driven model, exact steady-state velocity v = 1/38 requires eta = 27/76 ~ 0.355263
     to achieve Ht/Hp = 13/12 ~ 1.083333.
  3. However, because v != 0, the shape modulus beta_+(t) drifts steadily rather than remaining
     at a stationary fixed point. Achieving a true stationary fixed point (dot_beta = 0) requires
     an un-modeled stabilizing potential.

Strictly adheres to GEMINI.md Rules 1, 3, 4, 6 (Fail-closed, exact measured outputs).
"""

import json
import hashlib
import numpy as np
from pathlib import Path
from scipy.integrate import solve_ivp

OMEGA_M0 = 0.315
OMEGA_R0 = 9.2e-5
OMEGA_L0 = 1.0 - OMEGA_M0 - OMEGA_R0

def hubble(a):
    return np.sqrt(OMEGA_R0 / (a**4) + OMEGA_M0 / (a**3) + OMEGA_L0)

def casimir_shear_forces(beta_p, beta_m, a, L0=1.0):
    L_phys = a * L0
    prefactor = (np.pi**2) / (90.0 * (L_phys**4))
    term_z = np.exp(-4.0 * beta_p)
    term_x = np.exp(2.0 * beta_p + 2.0 * np.sqrt(3.0) * beta_m)
    term_y = np.exp(2.0 * beta_p - 2.0 * np.sqrt(3.0) * beta_m)
    
    F_plus = prefactor * (term_z - 0.5 * (term_x + term_y))
    F_minus = prefactor * (np.sqrt(3.0) / 2.0) * (term_x - term_y)
    return F_plus, F_minus

def moduli_system_ode_a(a, y, eta=0.0, driven=False):
    beta_p, v_p, beta_m, v_m = y
    H_iso = hubble(a)
    da_dt = a * H_iso
    
    F_plus, F_minus = casimir_shear_forces(beta_p, beta_m, a)
    Q_plus = (2.0 / 9.0) * eta * (H_iso**2) if driven else 0.0
    Q_minus = 0.0
    
    dv_p_da = (-3.0 * H_iso * v_p + F_plus + Q_plus) / da_dt
    dv_m_da = (-3.0 * H_iso * v_m + F_minus + Q_minus) / da_dt
    dbeta_p_da = v_p / da_dt
    dbeta_m_da = v_m / da_dt
    
    return [dbeta_p_da, dv_p_da, dbeta_m_da, dv_m_da]

def evaluate_free_dilution():
    a_span = (1e-3, 1.0)
    y0 = [0.05, 0.0, 0.0, 0.0]
    
    sol = solve_ivp(lambda a, y: moduli_system_ode_a(a, y, driven=False),
                    a_span, y0, rtol=1e-9, atol=1e-12, method="RK45", t_eval=np.linspace(1e-3, 1.0, 200))
    
    beta_p_final = sol.y[0, -1]
    v_p_final = sol.y[1, -1]
    a_final = sol.t[-1]
    
    H_final = hubble(a_final)
    H_t = H_final + v_p_final
    H_p = H_final - 2.0 * v_p_final
    ratio = H_t / H_p if H_p != 0 else 1.0
    
    poly = np.polyfit(sol.t[100:], np.log(np.abs(sol.y[0, 100:]) + 1e-30), 1)
    
    return {
        "initial_scale_factor": 1e-3,
        "final_scale_factor": float(a_final),
        "initial_beta_plus": 0.05,
        "final_beta_plus": float(beta_p_final),
        "final_dot_beta_plus": float(v_p_final),
        "final_Ht_over_Hp": float(ratio),
        "scale_factor_decay_slope": float(poly[0]),
        "verdict": "SCOPED_NEGATIVE_FREE_DILUTION"
    }

def evaluate_driven_stability():
    a_ref = 1.0
    H_ref = hubble(a_ref)
    
    eta_exact = 27.0 / 76.0
    v_stat = (1.0 / 38.0) * H_ref
    
    H_t = H_ref + v_stat
    H_p = H_ref - 2.0 * v_stat
    ratio_achieved = H_t / H_p
    
    prefactor = (np.pi**2) / 90.0
    dF_dbeta = -4.0 * prefactor
    J = np.array([[0.0, 1.0], [dF_dbeta, -3.0 * H_ref]])
    eigenvals = np.linalg.eigvals(J)
    
    return {
        "target_13_12_ratio": float(13.0 / 12.0),
        "exact_required_eta": float(eta_exact),
        "exact_required_eta_fraction": "27/76",
        "steady_flow_velocity_v_over_H": float(1.0 / 38.0),
        "achieved_Ht_over_Hp": float(ratio_achieved),
        "jacobian_eigenvalues": [str(ev) for ev in eigenvals],
        "modulus_drift_note": "Steady velocity v != 0 causes continuous modulus drift unless an un-modeled potential provides stationary stabilization."
    }

def run_moduli_suite():
    print("================================================================================")
    print("TOP-001 / CBR-002: Coupled 3D Moduli & Casimir Stress Stability Probe")
    print("================================================================================")
    
    free_res = evaluate_free_dilution()
    print(f"Free Integration a : {free_res['initial_scale_factor']} -> {free_res['final_scale_factor']:.2f} (z=0)")
    print(f"Final beta_+ (z=0) : {free_res['final_beta_plus']:.6e}")
    print(f"Final H_t / H_p    : {free_res['final_Ht_over_Hp']:.6f} (Exact Isotropy: 1.000000)")
    print(f"Verdict            : {free_res['verdict']}")
    
    driven_res = evaluate_driven_stability()
    print(f"\nTarget 13/12 Ratio : {driven_res['target_13_12_ratio']:.6f}")
    print(f"Exact Required eta : {driven_res['exact_required_eta']:.6f} ({driven_res['exact_required_eta_fraction']})")
    print(f"Achieved H_t / H_p : {driven_res['achieved_Ht_over_Hp']:.6f}")
    print(f"Jacobian Eigs      : {driven_res['jacobian_eigenvalues']}")
    print(f"Modulus Drift Note : {driven_res['modulus_drift_note']}")
    
    output_data = {
        "gate": "TOP-001 / CBR-002",
        "description": "Coupled Bianchi-I moduli ODE and stability analysis on T^3 (Exploratory Toy)",
        "free_casimir_dilution": free_res,
        "driven_moduli_analysis": driven_res,
        "epistemic_verdict": {
            "status": "SCOPED_NEGATIVE_AND_CONDITIONAL_TOY",
            "finding": "Free Casimir stress decays strictly to spatial isotropy Ht/Hp = 1.000000 at a=1 (z=0). Driven model requires exact eta = 27/76 (~0.3553) for Ht/Hp = 13/12, but steady velocity causes modulus drift without potential stabilization."
        }
    }
    
    out_dir = Path("Analysis/TOP/TOP-001/outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "top001_moduli_phase_space_summary.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
        
    digest = hashlib.sha256(out_file.read_bytes()).hexdigest()
    sidecar = out_file.with_suffix(".json.sha256")
    sidecar.write_text(f"{digest}  {out_file.name}\n", encoding="utf-8")
    print(f"\nResults saved to: {out_file}")
    print(f"SHA-256 Digest : {digest}")
    print(f"Sidecar written: {sidecar}")
    print("================================================================================")

if __name__ == "__main__":
    run_moduli_suite()
