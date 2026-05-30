"""
Integrated Toroidal-Syntropic Model (ITSM) - Empirical BAO Confrontation
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Protocol: Empirical Validation using MCMC-Optimized Syntropic Decay Index (n=0.8090)
Environment: Windows / Antigravity IDE Workspace Compatible
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Unified Publication Formatting (Removed redundancy to preserve LaTeX preamble)
plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath}",
    "font.family": "serif",
    "axes.facecolor": "white",
    "figure.facecolor": "white",
    "font.size": 14
})

# 2. Configuration & Pathing (Targeting DR2 Consensus)
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.abspath(os.path.join(
    script_dir, "..", "DESI_data", "bao_data-master", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_mean.txt"
))
cov_path = os.path.abspath(os.path.join(
    script_dir, "..", "DESI_data", "bao_data-master", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_cov.txt"
))

# 3. Optimized ITSM Parameters (Derived from Global MCMC Convergence)
H0 = 78.63
Om = 0.240
n_opt = 0.8090  # Optimized Syntropic Decay Index
rs = 147.09     # Fiducial sound horizon in Mpc

# 4. Ingestion & Transformation Protocol
if os.path.exists(data_path) and os.path.exists(cov_path):
    df = pd.read_csv(data_path, sep=r'\s+', comment='#', names=['z', 'value', 'observable'], header=None)
    
    # Load covariance matrix and extract diagonal variances
    cov = np.loadtxt(cov_path)
    df['variance'] = np.diag(cov)
    
    # Filter for Hubble observable (DH/rs) and transform: H(z) = c / (DH_over_rs * rs)
    df_h = df[df['observable'] == 'DH_over_rs'].copy()
    df_h['H_obs'] = 299792.458 / (df_h['value'] * rs)
    
    # Error propagation: err_H = H_obs * (err_value / value) where err_value = sqrt(variance)
    df_h['err_H'] = df_h['H_obs'] * (np.sqrt(df_h['variance']) / df_h['value'])
    
    z_obs, H_obs, err_H = df_h['z'].values, df_h['H_obs'].values, df_h['err_H'].values

    # 5. ITSM Empirical Validation Engine
    # Exponent strictly encapsulated to prevent linter syntax errors
    H_itsm_calc = H0 * np.sqrt(Om * (1 + z_obs)**3 + (1 - Om) * (1 + z_obs)**(-n_opt))
    chi2_nu = np.sum(((H_obs - H_itsm_calc) / err_H)**2) / len(z_obs)

    print("--- BAO EMPIRICAL VALIDATOR: DESI DR2 ---")
    print(f"Optimized n: {n_opt:.4f}")
    print(f"ITSM Chi^2_nu: {chi2_nu:.4f}")
    
    # 6. Visualization Architecture
    plt.figure(figsize=(10, 6))
    plt.errorbar(z_obs, H_obs, yerr=err_H, fmt='ok', capsize=4, label='DESI 2024 DR2 BAO H(z) Mapping', zorder=5)
    
    z_smooth = np.linspace(0, 2.5, 100)
    H_smooth = H0 * np.sqrt(Om * (1 + z_smooth)**3 + (1 - Om) * (1 + z_smooth)**(-n_opt))
    
    # Bypassing rf-string linter conflicts via standard formatting
    plot_label = r'ITSM Optimized ($n={:.2f}$) [$\chi^2_\nu \approx {:.2f}$]'.format(n_opt, chi2_nu)
    plt.plot(z_smooth, H_smooth, '-', lw=3, label=plot_label)
    
    plt.title(r'\textbf{ITSM vs. DESI DR2: Global Likelihood Convergence}', fontsize=16, pad=15)
    plt.xlabel(r'Redshift ($z$)', fontsize=15)
    plt.ylabel(r'$H(z)$ [km s$^{-1}$ Mpc$^{-1}$]', fontsize=15)
    plt.legend(loc='upper left', framealpha=0.9, edgecolor='black', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()

    out_path = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_desi_bao_empirical_validation.png"))
    plt.savefig(out_path, dpi=300)
    print(f"Asset generated: {out_path}")
else:
    print(f"CRITICAL ANOMALY: Data path unreachable: {data_path}")