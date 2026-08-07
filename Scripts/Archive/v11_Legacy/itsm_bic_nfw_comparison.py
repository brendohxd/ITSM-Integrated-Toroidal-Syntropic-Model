"""
ITSM Diagnostic Script — Bayesian Information Criterion (BIC) Map
Contrasts the parameter-free ITSM geometric yield against the 2-parameter NFW Dark Matter Halo.
"""

import os
import glob
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import sys

# Dynamic pathing
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(os.path.join(repo_root, "Scripts"))
try:
    from itsm_plot_style import apply_tier1_style
    apply_tier1_style()
except ImportError:
    pass

data_dir = os.path.join(repo_root, "Data", "SPARC_data")
galaxy_files = sorted(glob.glob(os.path.join(data_dir, "*_rotmod.dat")))

assert len(galaxy_files) == 175, "Strict adherence to 175 SPARC galaxies is required."

# Constants
a0_sparc = 1.08e-10 * 3.086e13  # m/s^2 to km^2/s^2/kpc
bounds_nfw = ((0.3, 0.8), (0.4, 1.0), (0.8, 1.2), (0.9, 1.1), (10.0, 500.0), (0.1, 100.0)) # u_d, u_b, d_scale, i_scale, V0, Rs
bounds_itsm = ((0.3, 0.8), (0.4, 1.0), (0.8, 1.2), (0.9, 1.1)) # u_d, u_b, d_scale, i_scale

results = []

print("Executing Bayesian Information Criterion (BIC) Map: ITSM vs. NFW Dark Matter...")

for f in galaxy_files:
    df = pd.read_csv(f, sep=r'\s+', comment='#', names=['Rad', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbul', 'SBdisk', 'SBbul'], header=0, engine='python')
    valid = (df['Rad'] > 0) & (df['Vobs'] > 0) & (df['errV'] > 0)
    df_v = df[valid].copy()
    if len(df_v) < 5: continue
        
    r_raw = df_v['Rad'].values
    v_obs_raw = df_v['Vobs'].values
    err_v_raw = df_v['errV'].values
    v_gas_raw = df_v['Vgas'].values
    v_disk_raw = df_v['Vdisk'].values
    v_bul_raw = df_v['Vbul'].values
    
    N = len(r_raw)
    
    # ITSM Optimization (k = 4 parameters)
    def chi2_itsm(params):
        u_d, u_b, d_scale, i_scale = params
        r = r_raw * d_scale
        v_obs = v_obs_raw / i_scale
        err_v = err_v_raw / i_scale
        v_bar_sq = (np.abs(v_gas_raw) * v_gas_raw * d_scale +
                    u_d * np.abs(v_disk_raw) * v_disk_raw * d_scale +
                    u_b * np.abs(v_bul_raw) * v_bul_raw * d_scale)
        g_b = v_bar_sq / r
        if np.any(g_b < 0): return np.inf
        
        g_eff = g_b + (2.0/3.0) * np.sqrt(g_b * a0_sparc)
        
        g_o = (v_obs**2) / r
        g_e = (2 * v_obs * err_v) / r
        chi2 = np.sum(((g_o - g_eff) / g_e)**2)
        return chi2 + ((d_scale - 1.0)/0.10)**2 + ((i_scale - 1.0)/0.05)**2
        
    res_itsm = minimize(chi2_itsm, [0.5, 0.7, 1.0, 1.0], bounds=bounds_itsm, method='L-BFGS-B')
    bic_itsm = res_itsm.fun + 4 * np.log(N)
    
    # NFW Optimization (k = 6 parameters)
    def chi2_nfw(params):
        u_d, u_b, d_scale, i_scale, V0, Rs = params
        r = r_raw * d_scale
        v_obs = v_obs_raw / i_scale
        err_v = err_v_raw / i_scale
        v_bar_sq = (np.abs(v_gas_raw) * v_gas_raw * d_scale +
                    u_d * np.abs(v_disk_raw) * v_disk_raw * d_scale +
                    u_b * np.abs(v_bul_raw) * v_bul_raw * d_scale)
        # NFW Halo velocity squared
        x = r / Rs
        v_halo_sq = V0**2 * (Rs / r) * (np.log(1 + x) - x / (1 + x))
        v_tot_sq = v_bar_sq + v_halo_sq
        
        if np.any(v_tot_sq < 0): return np.inf
        g_eff = v_tot_sq / r
        g_o = (v_obs**2) / r
        g_e = (2 * v_obs * err_v) / r
        chi2 = np.sum(((g_o - g_eff) / g_e)**2)
        return chi2 + ((d_scale - 1.0)/0.10)**2 + ((i_scale - 1.0)/0.05)**2
        
    res_nfw = minimize(chi2_nfw, [0.5, 0.7, 1.0, 1.0, 100.0, 10.0], bounds=bounds_nfw, method='L-BFGS-B')
    bic_nfw = res_nfw.fun + 6 * np.log(N)
    
    delta_bic = bic_nfw - bic_itsm
    results.append(delta_bic)

results = np.array(results)
results = results[np.isfinite(results)]
print(f"Mean DeltaBIC (NFW - ITSM): {np.mean(results):.2f}")
print(f"Galaxies where ITSM is statistically preferred (DeltaBIC > 0): {np.sum(results > 0)} / {len(results)}")

# Plotting
plt.figure(figsize=(10, 6))
plt.hist(results, bins=20, color='darkblue', alpha=0.7, edgecolor='black', linewidth=1.5)
plt.axvline(0, color='red', linestyle='dashed', linewidth=2, label=r'$\Delta$BIC = 0 (ITSM = NFW)')
plt.axvline(np.mean(results), color='gold', linestyle='-', linewidth=2, label=f'Mean $\\Delta$BIC = {np.mean(results):.1f}')

plt.title(r"Bayesian Information Criterion (BIC): ITSM vs $\Lambda$CDM (NFW)", pad=15)
plt.xlabel(r"$\Delta$BIC $(\text{BIC}_{\text{NFW}} - \text{BIC}_{\text{ITSM}})$")
plt.ylabel("Number of Galaxies (SPARC)")
plt.text(0.65, 0.65, f"ITSM Preferred: {np.sum(results > 0)}/{len(results)}", transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))
plt.legend(loc='upper right')

out_dir = os.path.join(repo_root, "Assets", "Figures")
os.makedirs(out_dir, exist_ok=True)
plt.savefig(os.path.join(out_dir, "itsm_bic_nfw_histogram.png"), bbox_inches='tight')
print(f"Exported to Assets/Figures/itsm_bic_nfw_histogram.png")
