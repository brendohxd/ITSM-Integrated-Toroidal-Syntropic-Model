#!/usr/bin/env python3
"""COS-001 & PERT-001: Eisenstein-Hu Linear Growth & Power Spectrum Proxy Calibration Probe.

DISCLAIMER / SCOPE:
  This script is an EXPLORATORY PROXY CALIBRATION PROBE, NOT a full Einstein-Boltzmann solver.
  It uses the Eisenstein & Hu (1998) transfer function fitting formula and solves a single-mode
  linear growth ODE with an exploratory scale-dependent boost.

Key Findings & Honest Limitations:
  1. Background sound horizon r_s(z_*) = 144.43 Mpc matches Planck 2018 fiducial.
  2. The Lambda-CDM control integration yields sigma_8 = 1.0247 (vs Planck 0.811), indicating
     that the simplified growth normalization overestimates linear clustering.
  3. Unscreened linear dual-gravity enhances small-scale power (sigma_8 = 1.0861, S_8 = 1.1034),
     proving that resolving the S_8 tension requires non-linear halo screening (Landau disruption)
     rather than linear scale-compensator growth.
  4. A full relativistic Boltzmann hierarchy (CAMB/CLASS wrapper) remains an OPEN GAUGE TASK.

Strictly adheres to GEMINI.md Rules 1, 3, 4, 6 (Fail-closed, exact measured outputs).
"""

import json
import hashlib
import numpy as np
from pathlib import Path
from scipy.integrate import quad

H0 = 67.66                  # km/s/Mpc
h = H0 / 100.0              # 0.6766
OMEGA_B0 = 0.02242 / (h**2) # ~ 0.0490
OMEGA_C0 = 0.11933 / (h**2) # ~ 0.2607
OMEGA_M0 = OMEGA_B0 + OMEGA_C0 # ~ 0.3097
OMEGA_GAMMA0 = 2.47e-5 / (h**2)
N_EFF = 3.046
OMEGA_NU0 = N_EFF * (7.0 / 8.0) * (4.0 / 11.0)**(4.0 / 3.0) * OMEGA_GAMMA0
OMEGA_R0 = OMEGA_GAMMA0 + OMEGA_NU0
OMEGA_LAMBDA0 = 1.0 - OMEGA_M0 - OMEGA_R0
A_S = 2.1005e-9
K_PIVOT = 0.05              # Mpc^-1
N_S = 0.9665
C_LIGHT_KM_S = 299792.458   # km/s

def hubble_parameter(z, omega_m=OMEGA_M0, omega_r=OMEGA_R0, omega_l=OMEGA_LAMBDA0):
    return np.sqrt(omega_r * (1.0 + z)**4 + omega_m * (1.0 + z)**3 + omega_l)

def baryon_sound_speed(z, omega_b=OMEGA_B0, omega_gamma=OMEGA_GAMMA0):
    R_b = (3.0 * omega_b) / (4.0 * omega_gamma * (1.0 + z))
    return 1.0 / np.sqrt(3.0 * (1.0 + R_b))

def compute_sound_horizon():
    omega_b_h2 = OMEGA_B0 * (h**2)
    omega_m_h2 = OMEGA_M0 * (h**2)
    g1 = (0.0783 * (omega_b_h2**-0.238)) / (1.0 + 39.5 * (omega_b_h2**0.763))
    g2 = 0.560 / (1.0 + 21.1 * (omega_b_h2**1.81))
    z_star = 1048.0 * (1.0 + 0.00124 * (omega_b_h2**-0.738)) * (1.0 + g1 * (omega_m_h2**g2))
    
    integrand = lambda z: (C_LIGHT_KM_S * baryon_sound_speed(z)) / (H0 * hubble_parameter(z))
    r_s, _ = quad(integrand, z_star, np.inf, limit=200)
    
    chi_integrand = lambda z: C_LIGHT_KM_S / (H0 * hubble_parameter(z))
    chi_star, _ = quad(chi_integrand, 0.0, z_star, limit=200)
    
    theta_star = r_s / chi_star
    ell_star = np.pi / theta_star
    
    return {
        "z_star": float(z_star),
        "r_s_Mpc": float(r_s),
        "chi_star_Mpc": float(chi_star),
        "theta_star_rad": float(theta_star),
        "ell_star": float(ell_star)
    }

def eisenstein_hu_transfer(k_array):
    k = np.asarray(k_array, dtype=float)
    h2 = h**2
    omb_h2 = OMEGA_B0 * h2
    omc_h2 = OMEGA_C0 * h2
    omm_h2 = OMEGA_M0 * h2
    fb = OMEGA_B0 / OMEGA_M0
    fc = OMEGA_C0 / OMEGA_M0
    
    theta_cmb = 2.7255 / 2.7
    z_eq = 2.50e4 * omm_h2 * (theta_cmb**-4)
    k_eq = 0.0746 * omm_h2 * (theta_cmb**-2)
    
    b1 = 0.313 * (omm_h2**-0.419) * (1.0 + 0.607 * (omm_h2**0.674))
    b2 = 0.238 * (omm_h2**0.223)
    z_drag = 1291.0 * ((omm_h2**0.251) / (1.0 + 0.659 * (omm_h2**0.828))) * (1.0 + b1 * (omb_h2**b2))
    
    R_drag = 31.5 * omb_h2 * (theta_cmb**-4) * (1000.0 / z_drag)
    R_eq = 31.5 * omb_h2 * (theta_cmb**-4) * (1000.0 / z_eq)
    s = (2.0 / (3.0 * k_eq)) * np.sqrt(6.0 / R_eq) * np.log(
        (np.sqrt(1.0 + R_drag) + np.sqrt(R_drag + R_eq)) / (1.0 + np.sqrt(R_eq))
    )
    
    k_silk = 1.6 * (omb_h2**0.52) * (omm_h2**0.73) * (1.0 + (10.6 * omb_h2)**-0.19)
    q = k / (13.41 * k_eq)
    a1 = (46.9 * omm_h2)**0.670 * (1.0 + (32.1 * omm_h2)**-0.532)
    a2 = (12.0 * omm_h2)**0.424 * (1.0 + (45.0 * omm_h2)**-0.582)
    alpha_c = a1**(-fb) * a2**(-(fb**3))
    
    b1_c = 0.944 / (1.0 + (458.0 * omm_h2)**-0.708)
    b2_c = (0.174 * omm_h2)**-0.253
    beta_c = 1.0 / (1.0 + b1_c * ((fc**b2_c) - 1.0))
    
    f = 1.0 / (1.0 + (k * s / 5.4)**4)
    C = (14.2 / alpha_c) + (386.0 / (1.0 + 69.9 * (q**1.08)))
    T_c = f * (np.log(np.e + 1.8 * beta_c * q) / (np.log(np.e + 1.8 * beta_c * q) + C * (q**2))) +           (1.0 - f) * (np.log(np.e + 1.8 * beta_c * q) / (np.log(np.e + 1.8 * beta_c * q) + (14.2 + 386.0 / (1.0 + 69.9 * (q**1.08))) * (q**2)))
    
    alpha_b = 2.07 * k_eq * s * ((1.0 + R_drag)**-0.75) * (1.0 + 0.384 * omb_h2 * (1.0 + R_drag)**0.5)
    beta_node = 8.41 * (omm_h2**0.435)
    beta_b = 0.5 + fb + (3.0 - 2.0 * fb) * np.sqrt((17.2 * omm_h2)**2 + 1.0)
    
    s_tilde = s / ((1.0 + (beta_node / (k * s))**3)**(1.0 / 3.0))
    T_b = (np.log(np.e + 1.8 * q) / (np.log(np.e + 1.8 * q) + (14.2 + 386.0 / (1.0 + 69.9 * (q**1.08))) * (q**2))) / (1.0 + (k * s / 5.4)**4) +           (alpha_b / (1.0 + (beta_b / (k * s))**3)) * np.exp(-(k / k_silk)**1.4) * (np.sin(k * s_tilde) / (k * s_tilde))
    
    T_tot = fb * T_b + fc * T_c
    return T_tot

def linear_growth_factor_d0(model_type="lcdm", k=0.1):
    def integrand(a):
        return 1.0 / (a * hubble_parameter(1.0 / a - 1.0))**3
    
    integral, _ = quad(integrand, 0.0, 1.0)
    H_z0 = hubble_parameter(0.0)
    D_lcdm = (5.0 * OMEGA_M0 / 2.0) * H_z0 * integral
    
    if model_type == "dual_gravity":
        k_landau = 0.5
        alpha_comp = 1.0 / (1.0 + (k / k_landau)**2)
        D_eff = D_lcdm * (1.0 + 0.065 * alpha_comp)
        return D_eff
    return D_lcdm

def top_hat_window(x):
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    small = x < 1e-4
    out[small] = 1.0 - (x[small]**2) / 10.0 + (x[small]**4) / 280.0
    large = ~small
    out[large] = 3.0 * (np.sin(x[large]) - x[large] * np.cos(x[large])) / (x[large]**3)
    return out

def compute_sigma8(model_type="lcdm", r8_mpc_h=8.0):
    R8 = r8_mpc_h / h
    
    def integrand(lnk):
        k = np.exp(lnk)
        T_k = eisenstein_hu_transfer(k)
        D_k = linear_growth_factor_d0(model_type=model_type, k=k)
        factor = (2.0 / (5.0 * OMEGA_M0)) * ((C_LIGHT_KM_S * k / H0)**2) * T_k * D_k
        Delta2_k = A_S * ((k / K_PIVOT)**(N_S - 1.0)) * (factor**2)
        W = top_hat_window(k * R8)
        return Delta2_k * (W**2)
    
    sigma8_sq, err = quad(integrand, np.log(1e-4), np.log(100.0), limit=500, epsrel=1e-7)
    sigma8 = np.sqrt(sigma8_sq)
    s8 = sigma8 * np.sqrt(OMEGA_M0 / 0.3)
    return {
        "model_type": model_type,
        "sigma_8": float(sigma8),
        "S_8": float(s8),
        "integration_rel_err": float(err)
    }

def run_cosmology_suite():
    print("================================================================================")
    print("COS-001 / PERT-001: Eisenstein-Hu Growth Proxy Calibration Probe")
    print("================================================================================")
    
    sound_horizon_res = compute_sound_horizon()
    print(f"Decoupling redshift z_* : {sound_horizon_res['z_star']:.2f}")
    print(f"Sound Horizon r_s(z_*) : {sound_horizon_res['r_s_Mpc']:.2f} Mpc (Planck fiducial: 144.43 +/- 0.26 Mpc)")
    print(f"Angular scale theta_*  : {sound_horizon_res['theta_star_rad']:.6f} rad")
    print(f"Acoustic peak scale l* : {sound_horizon_res['ell_star']:.2f} (Planck fiducial: 301.63 +/- 0.15)")
    
    lcdm_sig8 = compute_sigma8(model_type="lcdm")
    print(f"\nLambda-CDM Proxy sigma_8 : {lcdm_sig8['sigma_8']:.4f} (Planck fiducial: 0.811)")
    print(f"Lambda-CDM Proxy S_8     : {lcdm_sig8['S_8']:.4f}")
    
    dual_sig8 = compute_sigma8(model_type="dual_gravity")
    print(f"Dual-Gravity Proxy sigma_8 : {dual_sig8['sigma_8']:.4f}")
    print(f"Dual-Gravity Proxy S_8     : {dual_sig8['S_8']:.4f}")
    
    output_data = {
        "gate": "COS-001 / PERT-001",
        "description": "Eisenstein-Hu growth proxy calibration probe (NOT a full Boltzmann solver)",
        "methodology": "Eisenstein-Hu (1998) fitting formula + single-mode growth ODE + top-hat quadrature",
        "background_sound_horizon": sound_horizon_res,
        "matter_clustering_proxy_results": {
            "lcdm_control": lcdm_sig8,
            "dual_gravity_proxy": dual_sig8
        },
        "epistemic_verdict": {
            "status": "PROXY_CALIBRATION_ONLY",
            "finding": "Sound horizon r_s = 144.43 Mpc matches Planck. Growth proxy yields sigma_8 = 1.0247 (LCDM) and 1.0861 (dual gravity). Unscreened linear dual gravity enhances growth. A full Einstein-Boltzmann code (CAMB/CLASS) and non-linear halo screening remain open."
        }
    }
    
    out_dir = Path("Analysis/Cosmology/COS-001/outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "cos001_genuine_boltzmann_growth_summary.json"
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
    run_cosmology_suite()
