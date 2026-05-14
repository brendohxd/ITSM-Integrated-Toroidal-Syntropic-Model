import pandas as pd
import numpy as np
import os

# ====================== ITSM DIAGNOSTIC EXPORTER ======================
# Purpose: Export raw calculation samples to resolve the "Parallelism" bug.
# ======================================================================

# 1. CONSTANTS
H0_si = 70.0 * 1000 / 3.08567758e22
c = 299792458
sparc_conv = 3.08567758e13

# Both derivations in one script for direct comparison
a0_divisor = (c * H0_si / (2 * np.pi)) * sparc_conv
a0_multiplier = (2 * np.pi * c * H0_si) * sparc_conv

def get_diagnostics(data_dir):
    if not os.path.exists(data_dir):
        return "Folder not found."

    file_list = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(('.txt', '.dat'))]
    
    all_g_bar = []
    all_g_obs = []

    for file_path in file_list[:20]: # Sample first 20 galaxies for speed
        try:
            df = pd.read_csv(file_path, sep=r'\s+', comment='#', header=None, on_bad_lines='skip')
            if df.shape[1] >= 6:
                df = df[(df[1] > 0) & (df[0] > 0)].dropna()
                v_bar_sq = df[3]**2 + 0.5 * df[4]**2 + 0.7 * df[5]**2
                all_g_bar.extend(v_bar_sq / df[0])
                all_g_obs.extend(df[1]**2 / df[0])
        except: continue

    g_bar = np.array(all_g_bar)
    g_obs = np.array(all_g_obs)

    # ITSM Calculations
    pred_div = g_bar + a0_divisor * (np.sqrt(1 + 2 * g_bar / a0_divisor) - 1)
    pred_mult = g_bar + a0_multiplier * (np.sqrt(1 + 2 * g_bar / a0_multiplier) - 1)

    print("\n" + "="*80)
    print(f"{'G_BAR':<15} | {'G_OBS':<15} | {'DIVISOR PRED':<20} | {'MULT PRED':<20}")
    print("-" * 80)
    
    # Pick 10 points across the range (low to high acceleration)
    indices = np.linspace(0, len(g_bar)-1, 10).astype(int)
    for i in indices:
        print(f"{g_bar[i]:<15.4f} | {g_obs[i]:<15.4f} | {pred_div[i]:<20.4f} | {pred_mult[i]:<20.4f}")
    
    print("="*80)
    print(f"DIAGNOSTIC a0 (Divisor):    {a0_divisor:.4f}")
    print(f"DIAGNOSTIC a0 (Multiplier): {a0_multiplier:.4f}")
    
    # RMSE check in log space
    rmse_div = np.sqrt(np.mean((np.log10(g_obs) - np.log10(pred_div))**2))
    rmse_mult = np.sqrt(np.mean((np.log10(g_obs) - np.log10(pred_mult))**2))
    
    print(f"RMSE (Divisor):            {rmse_div:.4f}")
    print(f"RMSE (Multiplier):         {rmse_mult:.4f}")
    print("="*80 + "\n")

get_diagnostics('SPARC_Data')