"""
Integrated Toroidal-Syntropic Model (ITSM) - Bootstrapped RAR Validation
Author: Brendon Boyd
Protocol: Forward-Modeled Monte Carlo Error Propagation across 175 SPARC galaxies
Description: Generates the 1-sigma and 2-sigma theoretical scatter envelopes 
assuming the ITSM is perfectly true, perturbed by known SPARC observational noise.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath}",
    "font.family": "serif",
    "axes.facecolor": "white",
    "figure.facecolor": "white",
    "font.size": 14
})

# 1. ITSM Yield Threshold (Locked Physics)
a0_ms2 = 1.08e-10
conv_factor = 3.086e13                    # m/s² → (km/s)²/kpc
a0_sparc = a0_ms2 * conv_factor

# 2. Path handling
script_dir = os.path.dirname(os.path.abspath(__file__))
sparc_path = os.path.normpath(os.path.join(script_dir, "..", "..", "..", "SPARC_data", "*.dat"))
file_list = glob.glob(sparc_path)

if not file_list:
    raise FileNotFoundError(f"No .dat files found in:\n{sparc_path}")

print(f"Loading {len(file_list)} SPARC galaxies for Monte Carlo Bootstrapping...")

g_bar_raw_all = []
g_obs_raw_all = []
err_v_all = []
r_all = []
v_obs_all = []

# Nominal M/L ratios
u_d = 0.5
u_b = 0.7

for file in file_list:
    try:
        df = pd.read_csv(file, sep=r'\s+', comment='#', 
                        names=['Rad', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbul', 'SBdisk', 'SBbul'],
                        header=0, engine='python')
        
        valid = (df['Rad'] > 0) & (df['Vobs'] > 0) & (df['errV'] > 0)
        df_v = df[valid]
        if len(df_v) < 5: continue

        r = df_v['Rad'].values
        v_obs = df_v['Vobs'].values
        errV = df_v['errV'].values
        v_gas = df_v['Vgas'].values
        v_disk = df_v['Vdisk'].values
        v_bul = df_v['Vbul'].values

        v_bar_sq = (np.abs(v_gas)*v_gas) + u_d*(np.abs(v_disk)*v_disk) + u_b*(np.abs(v_bul)*v_bul)
        g_bar = v_bar_sq / r
        g_obs = (v_obs**2) / r
        
        valid_pts = (g_bar > 1e-15) & (g_obs > 1e-15)
        
        g_bar_raw_all.extend(g_bar[valid_pts])
        g_obs_raw_all.extend(g_obs[valid_pts])
        err_v_all.extend(errV[valid_pts])
        r_all.extend(r[valid_pts])
        v_obs_all.extend(v_obs[valid_pts])
        
    except Exception:
        pass

g_bar_raw = np.array(g_bar_raw_all)
g_obs_raw = np.array(g_obs_raw_all)
err_v = np.array(err_v_all)
r_arr = np.array(r_all)
v_obs_arr = np.array(v_obs_all)

# Forward Model: Assume ITSM is the Ground Truth
# g_obs_true = g_bar_raw + (2/3) * sqrt(g_bar_raw * a0)
g_obs_true = g_bar_raw + (2/3) * np.sqrt(g_bar_raw * a0_sparc)
v_obs_true = np.sqrt(g_obs_true * r_arr)

# Monte Carlo Bootstrapping
N_boot = 500
g_bar_bins = np.logspace(np.log10(1e-12*conv_factor), np.log10(1e-8*conv_factor), 40)
mock_g_obs_binned = {i: [] for i in range(len(g_bar_bins)-1)}

print(f"Executing Forward-Modeled Monte Carlo ({N_boot} realizations)...")

for _ in tqdm(range(N_boot)):
    # Inject SPARC Observational Noise
    # 10% distance uncertainty -> scales g_bar by D, g_obs by 1/D
    D_scale = np.random.normal(1.0, 0.10, len(g_bar_raw))
    
    # 5% inclination uncertainty -> scales velocities
    I_scale = np.random.normal(1.0, 0.05, len(g_bar_raw))
    
    # Gaussian velocity measurement errors
    v_obs_mock = np.random.normal(v_obs_true, err_v)
    v_obs_mock = np.maximum(v_obs_mock, 0.1) # prevent negative velocities
    
    # Apply perturbations
    # D_scale shifts R -> R*D. So g_bar = V^2 / R -> g_bar * D.
    g_bar_mock = g_bar_raw * D_scale
    
    # V_obs is scaled by 1/sin(i). Perturbing i_scale means V_mock = V_true / I_scale
    g_obs_mock = (v_obs_mock / I_scale)**2 / (r_arr * D_scale)
    
    # Bin the mock data
    indices = np.digitize(g_bar_mock, g_bar_bins) - 1
    for k in range(len(g_obs_mock)):
        idx = indices[k]
        if 0 <= idx < len(g_bar_bins)-1:
            mock_g_obs_binned[idx].append(g_obs_mock[k])

# Extract Envelopes
bin_centers = 0.5 * (g_bar_bins[:-1] + g_bar_bins[1:])
env_median = np.full(len(bin_centers), np.nan)
env_1sig_low = np.full(len(bin_centers), np.nan)
env_1sig_high = np.full(len(bin_centers), np.nan)
env_2sig_low = np.full(len(bin_centers), np.nan)
env_2sig_high = np.full(len(bin_centers), np.nan)

for i in range(len(bin_centers)):
    vals = np.array(mock_g_obs_binned[i])
    if len(vals) > 50:
        env_median[i] = np.median(vals)
        env_1sig_low[i] = np.percentile(vals, 16)
        env_1sig_high[i] = np.percentile(vals, 84)
        env_2sig_low[i] = np.percentile(vals, 2.5)
        env_2sig_high[i] = np.percentile(vals, 97.5)

# Plotting
plt.figure(figsize=(11, 8))
g_min, g_max = 1e-12 * conv_factor, 1e-8 * conv_factor

# Plot actual SPARC data
plt.scatter(g_bar_raw, g_obs_raw, s=15, alpha=0.3, color='steelblue', edgecolors='none', label='SPARC Empirical Data (Unoptimized)')

# Newtonian
plt.plot(bin_centers, bin_centers, '--', color='gray', lw=2, label=r'Newtonian Expectation')

# ITSM True Curve
itsm_curve = bin_centers + (2/3) * np.sqrt(bin_centers * a0_sparc)

# Plot Envelopes
plt.fill_between(bin_centers, env_2sig_low, env_2sig_high, color='darkred', alpha=0.15, label=r'ITSM Forward Model ($2\sigma$ scatter)')
plt.fill_between(bin_centers, env_1sig_low, env_1sig_high, color='darkred', alpha=0.35, label=r'ITSM Forward Model ($1\sigma$ scatter)')
plt.plot(bin_centers, itsm_curve, '-', color='darkred', lw=3, label='ITSM Theoretical Base')

plt.axvline(a0_sparc, color='black', ls=':', alpha=0.6, lw=1.5)
plt.annotate(r'$a_0$ Yield Boundary', xy=(a0_sparc, g_min*8), 
             xytext=(a0_sparc*3, g_min*4),
             arrowprops=dict(arrowstyle='->', color='black'), fontsize=12)

plt.xscale('log')
plt.yscale('log')
plt.xlim(g_min, g_max)
plt.ylim(g_min, g_max)
plt.title(r'\textbf{Bootstrapped RAR: Observational Noise Envelope validation}', fontsize=16, pad=15)
plt.xlabel(r'Baryonic Acceleration $g_{bar}$ [km$^2$ s$^{-2}$ kpc$^{-1}$]', fontsize=15)
plt.ylabel(r'Observed Acceleration $g_{obs}$ [km$^2$ s$^{-2}$ kpc$^{-1}$]', fontsize=15)
plt.legend(loc='upper left', fontsize=12, framealpha=0.95)
plt.grid(True, which='both', ls='-', alpha=0.3)

plt.tight_layout()

out_path = os.path.normpath(os.path.join(script_dir, "..", "..", "..", "Assets", "Figures", "itsm_bootstrapped_rar.png"))
plt.savefig(out_path, dpi=300, bbox_inches='tight')
print(f"Plot saved to: {out_path}")
