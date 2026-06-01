"""
Integrated Toroidal-Syntropic Model (ITSM) - Global SPARC RAR Parser
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Protocol: Unfiltered Hierarchical Nuisance Marginalization across 175 SPARC galaxies
Environment: Windows / Antigravity IDE Workspace Compatible
"""

import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Scripts')))
from itsm_plot_style import apply_tier1_style
apply_tier1_style()
import glob
import os
import warnings
from scipy.optimize import minimize
warnings.filterwarnings('ignore')

# ---------------------------------------------------------
# ITSM Global RAR Analysis - Unfiltered High-Fidelity Version
# ---------------------------------------------------------



# 1. ITSM Yield Threshold (Locked Physics)
a0_ms2 = 1.08e-10
conv_factor = 3.086e13                    # m/s² → (km/s)²/kpc
a0_sparc = a0_ms2 * conv_factor
print(f"ITSM a0 in SPARC units: {a0_sparc:.1f}")

# 2. Path handling
script_dir = os.path.dirname(os.path.abspath(__file__))
sparc_path = os.path.join(script_dir, "..", "SPARC_data", "*.dat")
sparc_path = os.path.normpath(sparc_path)

file_list = glob.glob(sparc_path)
print(f"Found {len(file_list)} galaxy data files.")

if not file_list:
    raise FileNotFoundError(f"No .dat files found in:\n{sparc_path}")

# M/L bounds (Disk: 0.3-0.8, Bulge: 0.4-1.0) and Nuisance factors (Distance: +/- 20%, Inclination: +/- 10%)
bounds = ((0.3, 0.8), (0.4, 1.0), (0.8, 1.2), (0.9, 1.1))

g_bar_all = []
g_obs_all = []
g_obs_err_all = []
galaxy_count = 0

print("Parsing galaxies using Unfiltered Hierarchical Nuisance Marginalization...")

for file in file_list:
    try:
        df = pd.read_csv(file, sep=r'\s+', comment='#', 
                        names=['Rad', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbul', 'SBdisk', 'SBbul'],
                        header=0, engine='python')
        
        # 1. Unfiltered Quality Check (Only exclude mathematically invalid zero-points)
        valid = (df['Rad'] > 0) & (df['Vobs'] > 0) & (df['errV'] > 0)
        df_v = df[valid].copy()
        
        if len(df_v) < 5:
            continue

        # 2. Extract Raw Arrays
        r_raw = df_v['Rad'].values
        v_obs_raw = df_v['Vobs'].values
        err_v_raw = df_v['errV'].values
        v_gas_raw = df_v['Vgas'].values
        v_disk_raw = df_v['Vdisk'].values
        v_bul_raw = df_v['Vbul'].values

        # 3. Define Objective Function with Gaussian Priors
        def calc_chi2_unfiltered(params):
            u_d, u_b, d_scale, i_scale = params
            
            # Apply astronomical scaling to raw data
            r_scaled = r_raw * d_scale
            v_obs_scaled = v_obs_raw / i_scale
            err_v_scaled = err_v_raw / i_scale
            
            v_gas_sq = np.abs(v_gas_raw) * v_gas_raw * d_scale
            v_disk_sq = u_d * np.abs(v_disk_raw) * v_disk_raw * d_scale
            v_bul_sq = u_b * np.abs(v_bul_raw) * v_bul_raw * d_scale
            
            v_bar_sq = v_gas_sq + v_disk_sq + v_bul_sq
            g_b = v_bar_sq / r_scaled
            
            if np.any(g_b < 0): return np.inf 
            
            g_o = (v_obs_scaled**2) / r_scaled
            g_e = (2 * v_obs_scaled * err_v_scaled) / r_scaled
            
            # ITSM Locked Physics: 2/3 Geometric Projection
            g_eff = g_b + (2/3) * np.sqrt(g_b * a0_sparc)
            
            # Kinematic Chi-Square
            chi2_kin = np.sum(((g_o - g_eff) / g_e)**2)
            
            # Gaussian Priors (Penalty for deviating from standard telescope observations)
            prior_d = ((d_scale - 1.0) / 0.10)**2  # 10% distance uncertainty prior
            prior_i = ((i_scale - 1.0) / 0.05)**2  # 5% inclination uncertainty prior
            
            return chi2_kin + prior_d + prior_i

        # 4. Run Optimizer with Nuisance Parameters
        res = minimize(calc_chi2_unfiltered, [0.5, 0.7, 1.0, 1.0], bounds=bounds, method='L-BFGS-B')
        opt_u_disk, opt_u_bulge, opt_d_scale, opt_i_scale = res.x

        # 5. Apply Final Optimized State
        r_final = r_raw * opt_d_scale
        v_obs_final = v_obs_raw / opt_i_scale
        err_v_final = err_v_raw / opt_i_scale
        
        v_bar_sq_final = (np.abs(v_gas_raw) * v_gas_raw * opt_d_scale) + \
                         (opt_u_disk * np.abs(v_disk_raw) * v_disk_raw * opt_d_scale) + \
                         (opt_u_bulge * np.abs(v_bul_raw) * v_bul_raw * opt_d_scale)

        g_bar = v_bar_sq_final / r_final
        g_obs = (v_obs_final**2) / r_final
        g_err = (2 * v_obs_final * err_v_final) / r_final

        # 6. Unfiltered Append (NO CLIPPING)
        valid_points = (g_bar > 1e-15) & (g_obs > 1e-15) & np.isfinite(g_err)
        
        g_bar_all.extend(g_bar[valid_points])
        g_obs_all.extend(g_obs[valid_points])
        g_obs_err_all.extend(g_err[valid_points])
        
        galaxy_count += 1
        
    except Exception as e:
        print(f"Skipped {os.path.basename(file)}: {e}")

# Final arrays
g_bar_all = np.array(g_bar_all)
g_obs_all = np.array(g_obs_all)
g_err_all = np.array(g_obs_err_all)

# Clean
valid = (g_bar_all > 0) & (g_obs_all > 0) & (g_err_all > 0) & np.isfinite(g_err_all)
g_bar = g_bar_all[valid]
g_obs = g_obs_all[valid]
g_err = g_err_all[valid]

print(f"\nFinal statistics:")
print(f"Galaxies processed: {galaxy_count}")
print(f"Total valid kinematic data points (UNFILTERED): {len(g_obs)}")

# ITSM prediction (2/3 Geometric Projection RESTORED)
g_eff_itsm = g_bar + (2/3) * np.sqrt(g_bar * a0_sparc)

# Chi-square
chi2 = np.sum(((g_obs - g_eff_itsm) / g_err)**2)
dof = len(g_obs) - 1
reduced_chi2 = chi2 / dof

print(f"Global Optimized Reduced chi^2_v = {reduced_chi2:.3f} (dof = {dof})")

# ========================= PLOTTING =========================
plt.figure(figsize=(11, 8))

g_min, g_max = 1e-12 * conv_factor, 1e-8 * conv_factor

hb = plt.hexbin(g_bar, g_obs, gridsize=80, cmap='Blues', bins='log',
                xscale='log', yscale='log', mincnt=1, edgecolors='none', alpha=0.9)

plt.colorbar(hb, label=r'$\log_{10}(\text{Density of Data Points})$')

x_vals = np.logspace(np.log10(g_min), np.log10(g_max), 200)

# Newtonian
plt.plot(x_vals, x_vals, '--', color='gray', lw=2, label=r'Newtonian ($g_{obs}=g_{bar}$)')

# ITSM
itsm_curve = x_vals + (2/3) * np.sqrt(x_vals * a0_sparc)
plt.plot(x_vals, itsm_curve, '-', color='darkred', lw=3, 
         label=f'ITSM ($\\chi^2_\\nu = {reduced_chi2:.2f}$)')

plt.axvline(a0_sparc, color='black', ls=':', alpha=0.6, lw=1.5)
plt.annotate(r'$a_0$ Yield Boundary', xy=(a0_sparc, g_min*8), 
             xytext=(a0_sparc*3, g_min*4),
             arrowprops=dict(arrowstyle='->', color='black'), fontsize=12)

plt.title(r'Global Radial Acceleration Relation (SPARC)', fontsize=16, pad=15)
plt.xlabel(r'Baryonic Acceleration $g_{bar}$ [km$^2$ s$^{-2}$ kpc$^{-1}$]', fontsize=15)
plt.ylabel(r'Observed Acceleration $g_{obs}$ [km$^2$ s$^{-2}$ kpc$^{-1}$]', fontsize=15)

plt.xlim(g_min, g_max)
plt.ylim(g_min, g_max)
plt.legend(loc='upper left', fontsize=12, framealpha=0.95)
plt.grid(True, which='both', ls='-', alpha=0.3)

plt.tight_layout()

out_path = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_global_rar_publication.png"))
plt.savefig(out_path, dpi=300, bbox_inches='tight')
print(f"\nPlot saved to: {out_path}")