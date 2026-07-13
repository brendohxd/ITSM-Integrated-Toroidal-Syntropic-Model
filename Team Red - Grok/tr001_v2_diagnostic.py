"""
TR-001-v2 Diagnostic
Locked version for independent reproduction.
Do not modify this file.
"""

import os
import sys
import hashlib
import numpy as np
import pandas as pd
from scipy.optimize import minimize, differential_evolution
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt
from scipy.stats import trim_mean

# ====================== PATH RESOLUTION ======================
# Paths are resolved relative to this script's location so it runs
# correctly regardless of the working directory.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.join(SCRIPT_DIR, "..")

# ====================== LOCKED CONFIGURATION ======================
INPUT_CSV  = os.path.join(SCRIPT_DIR, "Outputs", "redteam_C23_vs_C1_comparison.csv")
DATA_DIR   = os.path.join(REPO_ROOT,  "Data", "SPARC_data")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "Outputs", "TR001_v2_Results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TOP_N = 30
N_CORES = cpu_count()
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

A0_SPARC = 1.08e-10 * 3.086e13
BOUNDS = ((0.3, 0.8), (0.4, 1.0), (0.8, 1.2), (0.9, 1.1))

# ====================== CORE FUNCTIONS (LOCKED) ======================
def chi2_rar(params, r_raw, v_obs_raw, err_v_raw, v_gas_raw, v_disk_raw, v_bul_raw, C):
    u_d, u_b, d_scale, i_scale = params
    r = r_raw * d_scale
    v_obs = v_obs_raw / i_scale
    err_v = err_v_raw / i_scale
    v_bar_sq = (np.abs(v_gas_raw)*v_gas_raw*d_scale +
                u_d*np.abs(v_disk_raw)*v_disk_raw*d_scale +
                u_b*np.abs(v_bul_raw)*v_bul_raw*d_scale)
    g_b = v_bar_sq / r
    if np.any(g_b < 0): return np.inf
    g_eff = g_b + C * np.sqrt(g_b * A0_SPARC)
    g_o = (v_obs**2) / r
    g_e = (2 * v_obs * err_v) / r
    chi2 = np.sum(((g_o - g_eff) / g_e)**2)
    reg = ((d_scale - 1.0)/0.10)**2 + ((i_scale - 1.0)/0.05)**2
    return chi2 + reg

def reoptimize_galaxy(args):
    file_path, C = args
    try:
        df = pd.read_csv(file_path, sep=r'\s+', comment='#', header=None,
                         names=['Rad', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbul'])
        valid = (df['Rad'] > 0) & (df['Vobs'] > 0) & (df['errV'] > 0)
        df = df[valid]
        if len(df) < 5: return None

        r_raw = df['Rad'].values
        v_obs_raw = df['Vobs'].values
        err_v_raw = df['errV'].values
        v_gas_raw = df['Vgas'].values
        v_disk_raw = df['Vdisk'].values
        v_bul_raw = df['Vbul'].values

        best_chi2 = np.inf
        best_params = None

        for _ in range(5):
            x0 = np.random.uniform([b[0] for b in BOUNDS], [b[1] for b in BOUNDS])
            res = minimize(chi2_rar, x0, args=(r_raw, v_obs_raw, err_v_raw, v_gas_raw, v_disk_raw, v_bul_raw, C),
                           bounds=BOUNDS, method='L-BFGS-B', tol=1e-12)
            if res.fun < best_chi2:
                best_chi2 = res.fun
                best_params = res.x

        res_de = differential_evolution(chi2_rar, bounds=BOUNDS,
                                        args=(r_raw, v_obs_raw, err_v_raw, v_gas_raw, v_disk_raw, v_bul_raw, C),
                                        popsize=20, tol=1e-8, seed=RANDOM_SEED)
        if res_de.fun < best_chi2:
            best_chi2 = res_de.fun
            best_params = res_de.x

        return {'chi2': best_chi2, 'params': best_params}
    except Exception:
        return None

# ====================== MAIN EXECUTION ======================
if __name__ == "__main__":
    print("=== TR-001-v2 Diagnostic Starting ===")
    print(f"Random seed: {RANDOM_SEED}")
    print(f"Cores: {N_CORES}")

    df = pd.read_csv(INPUT_CSV)
    delta = df['delta_chi2'].values

    # Robust statistics
    results = {
        'mean_delta': float(np.mean(delta)),
        'median_delta': float(np.median(delta)),
        'trimmed_mean_10': float(trim_mean(delta, 0.1)),
        'n_galaxies': len(delta),
        'n_worse_C23': int((delta < 0).sum()),
        'n_better_C23': int((delta > 0).sum())
    }

    # Top outliers
    df_sorted = df.sort_values('delta_chi2').head(TOP_N)
    df_sorted.to_csv(os.path.join(OUTPUT_DIR, "top_worst_galaxies.csv"), index=False)

    # Re-optimization of worst galaxies using multiprocessing
    galaxy_files = {row['galaxy']: os.path.join(DATA_DIR, row['galaxy'] + "_rotmod.dat")
                    for _, row in df_sorted.iterrows()}

    tasks = [(galaxy_files[g], 2.0/3.0) for g in df_sorted['galaxy']]
    with Pool(N_CORES) as pool:
        reopt_results = pool.map(reoptimize_galaxy, tasks)

    reopt_df = pd.DataFrame([r for r in reopt_results if r is not None])
    reopt_df['galaxy'] = df_sorted['galaxy'].values[:len(reopt_df)]
    reopt_df.to_csv(os.path.join(OUTPUT_DIR, "reoptimized_worst_galaxies.csv"), index=False)

    # Save summary
    pd.DataFrame([results]).to_csv(os.path.join(OUTPUT_DIR, "summary_statistics.csv"), index=False)

    print("\n=== TR-001-v2 Complete ===")
    print(f"Results written to: {OUTPUT_DIR}")
