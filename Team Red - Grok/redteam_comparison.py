"""
Red-Team Controlled Comparison Script
=====================================
Purpose: Independent, falsification-focused audit of C_proj = 2/3 vs C = 1.0
         on the SPARC RAR under strictly identical conditions.

This script is NOT part of the canonical ITSM codebase.
It was drafted as a diagnostic tool to test the specific claim that the
geometric projection factor C=2/3 can be compared fairly to the standard
AQUAL/MOND limit (C=1) when every other degree of freedom is locked.

Key design principles (Red-Team requirements):
- Identical nuisance parameters (u_d, u_b, d_scale, i_scale)
- Identical bounds and regularization terms
- Identical data cuts and chi-squared definition
- Identical optimizer and starting point
- C is the ONLY thing that changes between the two models
- Both models treated as having exactly 4 parameters (C is fixed, not free)
- Negative results reported with equal weight
- No assumption that either model is "correct"

Author: Grok (Red-Team Lead mode)
Date: 2026-07-14
"""

import os
import glob
import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# =============================================================================
# CONFIGURATION (match existing pipeline as closely as possible)
# =============================================================================
# Resolve paths relative to this script so it runs from anywhere
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "Data", "SPARC_data")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "Outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# a0 in SPARC units (km^2 s^-2 kpc^-1) — same value used in existing scripts
A0_SPARC = 1.08e-10 * 3.086e13

# Same nuisance parameter bounds used in itsm_bic_nfw_comparison.py
BOUNDS = ((0.3, 0.8), (0.4, 1.0), (0.8, 1.2), (0.9, 1.1))

# Regularization terms (identical to existing code)
def regularization(d_scale, i_scale):
    return ((d_scale - 1.0) / 0.10)**2 + ((i_scale - 1.0) / 0.05)**2

# =============================================================================
# CORE CHI-SQUARED FUNCTION (identical structure for both models)
# =============================================================================
def chi2_rar(params, r_raw, v_obs_raw, err_v_raw, v_gas_raw, v_disk_raw, v_bul_raw, C):
    """
    Chi-squared on acceleration scale with fixed C.
    C is the only model difference between the two runs.
    """
    u_d, u_b, d_scale, i_scale = params
    
    r = r_raw * d_scale
    v_obs = v_obs_raw / i_scale
    err_v = err_v_raw / i_scale
    
    v_bar_sq = (np.abs(v_gas_raw) * v_gas_raw * d_scale +
                u_d * np.abs(v_disk_raw) * v_disk_raw * d_scale +
                u_b * np.abs(v_bul_raw) * v_bul_raw * d_scale)
    
    g_b = v_bar_sq / r
    if np.any(g_b < 0):
        return np.inf
    
    # The ONLY difference between the two models
    g_eff = g_b + C * np.sqrt(g_b * A0_SPARC)
    
    g_o = (v_obs**2) / r
    g_e = (2 * v_obs * err_v) / r
    
    chi2 = np.sum(((g_o - g_eff) / g_e)**2)
    return chi2 + regularization(d_scale, i_scale)


# =============================================================================
# PER-GALAXY OPTIMIZATION
# =============================================================================
def optimize_galaxy(file_path):
    """Run both C=2/3 and C=1.0 on one galaxy with identical setup."""
    try:
        df = pd.read_csv(file_path, sep=r'\s+', comment='#', header=None,
                         names=['Rad', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbul', 'SBdisk', 'SBbul'])
        
        valid = (df['Rad'] > 0) & (df['Vobs'] > 0) & (df['errV'] > 0)
        df = df[valid].copy()
        
        if len(df) < 5:
            return None
        
        r_raw = df['Rad'].values
        v_obs_raw = df['Vobs'].values
        err_v_raw = df['errV'].values
        v_gas_raw = df['Vgas'].values
        v_disk_raw = df['Vdisk'].values
        v_bul_raw = df['Vbul'].values
        
        N = len(r_raw)
        initial = [0.5, 0.7, 1.0, 1.0]
        
        # Model 1: C = 2/3 (geometric projection)
        res_23 = minimize(
            chi2_rar, initial, args=(r_raw, v_obs_raw, err_v_raw, v_gas_raw, v_disk_raw, v_bul_raw, 2.0/3.0),
            bounds=BOUNDS, method='L-BFGS-B'
        )
        
        # Model 2: C = 1.0 (standard AQUAL/MOND limit)
        res_1 = minimize(
            chi2_rar, initial, args=(r_raw, v_obs_raw, err_v_raw, v_gas_raw, v_disk_raw, v_bul_raw, 1.0),
            bounds=BOUNDS, method='L-BFGS-B'
        )
        
        chi2_23 = res_23.fun
        chi2_1 = res_1.fun
        delta_chi2 = chi2_1 - chi2_23          # positive = C=2/3 preferred
        
        # BIC (same k=4 for both models since C is fixed)
        bic_23 = chi2_23 + 4 * np.log(N)
        bic_1 = chi2_1 + 4 * np.log(N)
        delta_bic = bic_1 - bic_23
        
        return {
            'galaxy': os.path.basename(file_path).replace('_rotmod.dat', ''),
            'N_points': N,
            'chi2_C23': chi2_23,
            'chi2_C1': chi2_1,
            'delta_chi2': delta_chi2,
            'delta_bic': delta_bic,
            'success_23': res_23.success,
            'success_1': res_1.success
        }
        
    except Exception as e:
        print(f"Failed on {file_path}: {e}")
        return None


# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    import concurrent.futures
    galaxy_files = sorted(glob.glob(os.path.join(DATA_DIR, "*_rotmod.dat")))
    
    print(f"Found {len(galaxy_files)} SPARC galaxy files.")
    assert len(galaxy_files) == 175, "Expected exactly 175 galaxies."
    
    results = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {executor.submit(optimize_galaxy, f): f for f in galaxy_files}
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            res = future.result()
            if res is not None:
                results.append(res)
            if (i + 1) % 20 == 0:
                print(f"Processed {i+1}/{len(galaxy_files)} galaxies...")
    
    df = pd.DataFrame(results)
    df = df[np.isfinite(df['delta_chi2'])]
    
    # Summary statistics
    print("\n" + "="*70)
    print("RED-TEAM CONTROLLED COMPARISON: C=2/3 vs C=1.0")
    print("="*70)
    print(f"Galaxies successfully processed : {len(df)}")
    print(f"Mean Delta-chi^2 (C1 - C23)           : {df['delta_chi2'].mean():.3f}")
    print(f"Median Delta-chi^2                    : {df['delta_chi2'].median():.3f}")
    print(f"Galaxies where C=2/3 preferred (Delta-chi^2 > 0) : {(df['delta_chi2'] > 0).sum()} / {len(df)}")
    print(f"Galaxies where C=1 preferred   (Delta-chi^2 < 0) : {(df['delta_chi2'] < 0).sum()} / {len(df)}")
    print(f"Mean Delta-BIC (C1 - C23)          : {df['delta_bic'].mean():.3f}")
    print("="*70)
    
    # Save detailed results
    csv_path = os.path.join(OUTPUT_DIR, "redteam_C23_vs_C1_comparison.csv")
    df.to_csv(csv_path, index=False)
    print(f"\nDetailed per-galaxy results saved to: {csv_path}")
    
    # Histogram of Δχ²
    plt.figure(figsize=(10, 6))
    plt.hist(df['delta_chi2'], bins=30, color='#2c3e50', edgecolor='white', alpha=0.85)
    plt.axvline(0, color='red', linestyle='--', linewidth=2, label='Δχ² = 0 (equal fit)')
    plt.axvline(df['delta_chi2'].mean(), color='gold', linestyle='-', linewidth=2, 
                label=f'Mean Δχ² = {df["delta_chi2"].mean():.2f}')
    plt.xlabel(r'$\Delta\chi^2$ (C=1 minus C=2/3)')
    plt.ylabel('Number of SPARC Galaxies')
    plt.title('Red-Team Diagnostic: Controlled C=2/3 vs C=1 Comparison\n(Identical nuisances, data cuts, likelihood)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    fig_path = os.path.join(OUTPUT_DIR, "redteam_delta_chi2_histogram.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    print(f"Histogram saved to: {fig_path}")
    
    print("\nRed-Team note: Positive Delta-chi^2 means C=2/3 fits better under these controlled conditions.")
    print("This script makes no claim about physical correctness — only relative fit quality.")
