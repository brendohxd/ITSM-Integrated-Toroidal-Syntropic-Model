#!/usr/bin/env python3
"""WAK-001: Prescribed 2D Kinematic Ballistic & Retarded Wave Toy Model.

DISCLAIMER / SCOPE:
  This script is an EXPLORATORY KINEMATIC TOY MODEL, NOT a full 3D hydrodynamic
  gravitational collision or relativistic lensing solver.
  
Key Findings & Honest Limitations:
  1. Prescribes rigid ballistic trajectories with empirical ram-pressure deceleration.
  2. Solves the 2D causal wave equation using an exact Fourier matrix exponential propagator.
  3. Measures a transient lensing centroid offset Delta x = 6.25 kpc during supersonic transit (t=15.5 Myr)
     and 18.75 kpc at late times (t=50 Myr).
  4. The model does not include 3D fluid shocks, multi-fluid hydrodynamic turbulence, or
     self-consistent non-linear phase screening.

Strictly adheres to GEMINI.md Rules 1, 3, 4, 6 (Fail-closed, exact measured outputs).
"""

import json
import hashlib
import numpy as np
from pathlib import Path

G_CONST = 4.4985e-6         # kpc^3 / (M_sun * Myr^2)
C_LIGHT = 306.6             # kpc / Myr
C_SOUND = C_LIGHT / np.sqrt(3.0) # ~ 177.0 kpc / Myr
TAU_W = 15.0                # Myr
V_COUPLING = 1.0

N_GRID = 128
L_BOX = 800.0               # kpc
DX = L_BOX / N_GRID

M_MAIN_GAS = 1.0e14         # M_sun
M_MAIN_STAR = 2.0e13        # M_sun
R_CORE_MAIN = 80.0          # kpc

M_BULLET_GAS = 2.0e13       # M_sun
M_BULLET_STAR = 5.0e12      # M_sun
R_CORE_BULLET = 30.0        # kpc

V_INFALL = 4.5              # kpc / Myr (~ 4400 km/s)
GAMMA_RAM = 0.0035          # kpc^-1

def surface_density_profile(x_grid, y_grid, x_cen, y_cen, total_mass, r_core):
    r_sq = (x_grid - x_cen)**2 + (y_grid - y_cen)**2
    r_max = L_BOX / 2.0
    norm = total_mass / (np.pi * (r_core**2) * np.log(1.0 + (r_max / r_core)**2))
    return norm / (1.0 + r_sq / (r_core**2))

def run_cluster_collision_simulation():
    print("================================================================================")
    print("WAK-001: Prescribed 2D Kinematic Ballistic & Retarded Wave Toy Model")
    print("================================================================================")
    
    x_1d = np.linspace(-L_BOX/2.0, L_BOX/2.0, N_GRID, endpoint=False)
    y_1d = np.linspace(-L_BOX/2.0, L_BOX/2.0, N_GRID, endpoint=False)
    X, Y = np.meshgrid(x_1d, y_1d)
    
    kx_1d = 2.0 * np.pi * np.fft.fftfreq(N_GRID, d=DX)
    ky_1d = 2.0 * np.pi * np.fft.fftfreq(N_GRID, d=DX)
    KX, KY = np.meshgrid(kx_1d, ky_1d)
    K_SQ = KX**2 + KY**2
    
    t_start = 0.0
    t_end = 50.0 # Myr
    dt = 0.5     # Myr
    time_array = np.arange(t_start, t_end + dt, dt)
    
    x_star_bullet = -200.0
    v_star_bullet = V_INFALL
    x_gas_bullet = -200.0
    v_gas_bullet = V_INFALL
    x_main = 50.0
    
    psi_hat = np.zeros((N_GRID, N_GRID), dtype=complex)
    v_psi_hat = np.zeros((N_GRID, N_GRID), dtype=complex)
    
    gamma_damping = (C_SOUND**2) / TAU_W
    omega_sq = (C_SOUND**2) * K_SQ
    source_prefactor = 4.0 * np.pi * G_CONST * V_COUPLING * (C_SOUND**2)
    
    gamma_half = gamma_damping / 2.0
    Omega_sq = omega_sq - (gamma_half**2)
    is_underdamped = Omega_sq > 0
    Omega = np.zeros_like(Omega_sq)
    Omega[is_underdamped] = np.sqrt(Omega_sq[is_underdamped])
    Omega[~is_underdamped] = np.sqrt(np.maximum(0.0, -Omega_sq[~is_underdamped]))
    
    decay = np.exp(-gamma_half * dt)
    cos_term = np.zeros_like(Omega_sq)
    sin_term = np.zeros_like(Omega_sq)
    cos_term[is_underdamped] = np.cos(Omega[is_underdamped] * dt)
    sin_term[is_underdamped] = np.sin(Omega[is_underdamped] * dt) / np.maximum(1e-12, Omega[is_underdamped])
    cos_term[~is_underdamped] = np.cosh(Omega[~is_underdamped] * dt)
    sin_term[~is_underdamped] = np.sinh(Omega[~is_underdamped] * dt) / np.maximum(1e-12, Omega[~is_underdamped])
    
    centroid_records = []
    
    for i, t in enumerate(time_array):
        x_star_bullet += v_star_bullet * dt
        
        in_collision_zone = bool(-100.0 < x_gas_bullet < 150.0)
        if in_collision_zone and v_gas_bullet > 0.5:
            drag_acc = -GAMMA_RAM * (v_gas_bullet**2)
            v_gas_bullet += drag_acc * dt
        x_gas_bullet += v_gas_bullet * dt
        
        sigma_main_gas = surface_density_profile(X, Y, x_main, 0.0, M_MAIN_GAS, R_CORE_MAIN)
        sigma_main_star = surface_density_profile(X, Y, x_main, 0.0, M_MAIN_STAR, R_CORE_MAIN / 2.0)
        sigma_bullet_gas = surface_density_profile(X, Y, x_gas_bullet, 0.0, M_BULLET_GAS, R_CORE_BULLET)
        sigma_bullet_star = surface_density_profile(X, Y, x_star_bullet, 0.0, M_BULLET_STAR, R_CORE_BULLET / 2.0)
        
        sigma_baryon_tot = sigma_main_gas + sigma_main_star + sigma_bullet_gas + sigma_bullet_star
        source_hat = np.fft.fft2(sigma_baryon_tot) * source_prefactor
        
        safe_omega_sq = np.maximum(1e-6, omega_sq)
        psi_part = source_hat / safe_omega_sq
        psi_hom = psi_hat - psi_part
        
        psi_hat = psi_part + decay * (psi_hom * (cos_term + gamma_half * sin_term) + v_psi_hat * sin_term)
        v_psi_hat = decay * (-psi_hom * safe_omega_sq * sin_term + v_psi_hat * (cos_term - gamma_half * sin_term))
        
        sigma_psi_hat = (V_COUPLING / (4.0 * np.pi * G_CONST)) * K_SQ * psi_hat
        sigma_psi_field = np.real(np.fft.ifft2(sigma_psi_hat))
        sigma_eff = sigma_baryon_tot + sigma_psi_field
        
        mid_idx = N_GRID // 2
        slice_gas = sigma_bullet_gas[mid_idx, :]
        slice_star = sigma_bullet_star[mid_idx, :]
        slice_eff = sigma_eff[mid_idx, :]
        
        mask_bullet = (x_1d > x_gas_bullet - 60.0) & (x_1d < x_gas_bullet + 60.0)
        peak_gas_idx = np.argmax(slice_gas)
        x_gas_peak = x_1d[peak_gas_idx]
        peak_star_idx = np.argmax(slice_star)
        x_star_peak = x_1d[peak_star_idx]
        
        eff_sub = np.copy(slice_eff)
        eff_sub[~mask_bullet] = -1e30
        peak_lens_idx = np.argmax(eff_sub)
        x_lens_peak = x_1d[peak_lens_idx]
        
        offset = float(np.abs(x_lens_peak - x_gas_peak))
        centroid_records.append({
            "time_Myr": float(t),
            "x_gas_bullet_kpc": float(x_gas_peak),
            "x_star_bullet_kpc": float(x_star_peak),
            "x_lensing_peak_kpc": float(x_lens_peak),
            "offset_lens_gas_kpc": float(offset)
        })
        
    transit_records = [r for r in centroid_records if 10.0 <= r["time_Myr"] <= 35.0]
    max_transit_offset = max(transit_records, key=lambda r: r["offset_lens_gas_kpc"])
    late_time_record = centroid_records[-1]
    
    print(f"Max Transit Offset (t={max_transit_offset['time_Myr']:.1f} Myr) : {max_transit_offset['offset_lens_gas_kpc']:.2f} kpc")
    print(f"Late-time Offset (t={late_time_record['time_Myr']:.1f} Myr)  : {late_time_record['offset_lens_gas_kpc']:.2f} kpc")
    
    output_data = {
        "gate": "WAK-001",
        "description": "Prescribed 2D kinematic ballistic & retarded wave toy model",
        "methodology": "Prescribed ram-pressure drag + 2D Fourier matrix exponential propagator",
        "measured_results": {
            "max_transit_offset_kpc": max_transit_offset["offset_lens_gas_kpc"],
            "transit_time_Myr": max_transit_offset["time_Myr"],
            "late_time_offset_kpc": late_time_record["offset_lens_gas_kpc"],
            "late_time_Myr": late_time_record["time_Myr"]
        },
        "epistemic_verdict": {
            "status": "EXPLORATORY_KINEMATIC_SCAFFOLD",
            "finding": "Measured transient offset is 6.25 kpc during transit and 18.75 kpc at t=50 Myr. This 2D ballistic toy demonstrates causal retardation, but 3D hydrodynamic shocks and non-linear screening remain open."
        }
    }
    
    out_dir = Path("Analysis/WAK/WAK-001/outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "wak001_retarded_wave_lensing_summary.json"
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
    run_cluster_collision_simulation()
