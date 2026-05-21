"""
ITSM Diagnostic: Running Syntropic Decay Index (Stabilized + Visualized)
Protocol: Testing local stability of n(z) and plotting the evolutionary trend
"""

import numpy as np
import emcee
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Configuration
H0_fixed = 78.63
Om_fixed = 0.240
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.abspath(os.path.join(script_dir, "..", "DESI_data", "bao_data-master", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_mean.txt"))

df = pd.read_csv(data_path, sep=r'\s+', comment='#', names=['z', 'value', 'observable'], header=None)
df_h = df[df['observable'] == 'DH_over_rs'].copy()
df_h['H_obs'] = 299792.458 / (df_h['value'] * 147.09)
df_h['err_H'] = df_h['H_obs'] * 0.05

def log_likelihood(n, z_b, H_b, err_b):
    if n < 0.0 or n > 5.0: return -np.inf
    radicand = Om_fixed * (1 + z_b)**3 + (1 - Om_fixed) * (1 + z_b)**-n
    if np.any(radicand <= 0): return -np.inf
    H_model = H0_fixed * np.sqrt(radicand)
    return -0.5 * np.sum(((H_b - H_model) / err_b)**2)

# 2. Binning and Data Storage
bins = [(0.0, 0.8), (0.8, 1.6), (1.6, 2.5)]
z_centers = []
n_means = []
n_stds = []

print(f"--- DETECTING REDSHIFT-DEPENDENT PHASE TRANSITIONS (STABILIZED) ---")

for z_min, z_max in bins:
    df_bin = df_h[(df_h['z'] >= z_min) & (df_h['z'] < z_max)]
    if len(df_bin) < 2: continue
    
    z_b, H_b, err_b = df_bin['z'].values, df_bin['H_obs'].values, df_bin['err_H'].values
    
    sampler = emcee.EnsembleSampler(32, 1, lambda p: log_likelihood(p[0], z_b, H_b, err_b))
    sampler.run_mcmc(np.random.uniform(0.5, 1.5, size=(32, 1)), 1000, progress=False)
    
    samples = sampler.get_chain(discard=200, flat=True)
    z_centers.append((z_min + z_max) / 2)
    n_means.append(np.mean(samples))
    n_stds.append(np.std(samples))
    print(f"Bin {z_min}-{z_max}: Optimized n = {n_means[-1]:.4f} +/- {n_stds[-1]:.4f}")

# 3. Visualization
plt.figure(figsize=(8, 5))
plt.errorbar(z_centers, n_means, yerr=n_stds, fmt='-o', capsize=5, color='darkblue', label=r'ITSM Running Index $n(z)$')
plt.xlabel(r'Redshift ($z$)')
plt.ylabel(r'Syntropic Decay Index ($n$)')
plt.title(r'\textbf{ITSM: Redshift-Dependent Vacuum Evolution}')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()

out_path = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_n_evolution.png"))
plt.savefig(out_path, dpi=300)
print(f"Visualization generated: {out_path}")