import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ====================== ITSM DUAL YIELD DIAGNOSTIC ======================
# Logic 1: Divisor (a0 = cH0 / 2pi) - The "Tuned" Model
# Logic 2: Multiplier (a0 = 2pi * c * H0) - The "Welded" Model
# Goal: Find where the Superfluid Plenum "unlocks"
# ========================================================================

def run_dual_yield(data_dir):
    all_g_bar = []
    all_g_obs = []
    
    print("Gathering data for 175-Galaxy Yield Analysis...")
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith((".txt", ".dat")):
                try:
                    df = pd.read_csv(os.path.join(root, file), sep=r'\s+', comment='#', header=None)
                    df = df[(df[1] > 0) & (df[0] > 0)].dropna()
                    # Calculate baryonic and observed acceleration
                    v_bar_sq = df[3]**2 + 0.5 * df[4]**2 + 0.7 * df[5]**2
                    all_g_bar.extend(v_bar_sq / df[0])
                    all_g_obs.extend(df[1]**2 / df[0])
                except: continue

    g_bar = np.array(all_g_bar)
    g_obs = np.array(all_g_obs)
    obs_ratio = g_obs / g_bar
    
    # Constants
    H0_si = 70 * 1000 / 3.08567758e22
    c = 299792458
    conv = 3.08567758e13
    
    a0_div = (c * H0_si / (2 * np.pi)) * conv
    a0_mult = (2 * np.pi * c * H0_si) * conv

    # Prediction Ratios
    # R = 1 + (a0/g_bar) * (sqrt(1 + 2*g_bar/a0) - 1)
    ratio_div = (g_bar + a0_div * (np.sqrt(1 + 2 * g_bar / a0_div) - 1)) / g_bar
    ratio_mult = (g_bar + a0_mult * (np.sqrt(1 + 2 * g_bar / a0_mult) - 1)) / g_bar

    # VISUALIZATION
    plt.figure(figsize=(12, 7), facecolor='white')
    
    # 1. The Raw Truth (SPARC Data)
    plt.scatter(g_bar, obs_ratio, alpha=0.05, color='black', label='Observed (SPARC)')
    
    # 2. The Theoretical Contenders
    sort_idx = np.argsort(g_bar)
    plt.plot(g_bar[sort_idx], ratio_div[sort_idx], color='#e63946', lw=4, label=rf'Divisor Variant ($a_0 \approx {a0_div:.0f}$)')
    plt.plot(g_bar[sort_idx], ratio_mult[sort_idx], color='#ffb703', lw=3, linestyle='--', label=rf'Multiplier Variant ($a_0 \approx {a0_mult:.0f}$)')

    # 3. The Newtonian Horizon
    plt.axhline(y=1, color='#1f77b4', lw=2, linestyle='-', label='Newtonian Baseline (Ratio = 1)')

    plt.xscale('log')
    plt.ylim(0, 5) # Focus on the primary anomaly zone
    plt.xlabel(r'Baryonic Acceleration ($g_{bar}$)')
    plt.ylabel(r'Anomaly Ratio ($g_{obs} / g_{bar}$)')
    plt.title('The Plenum Yield Test: Which Model "Unlocks" First?')
    plt.legend(frameon=True, facecolor='white', edgecolor='black')
    plt.grid(True, which='both', linestyle=':', alpha=0.4)
    
    plt.tight_layout()
    plt.savefig('itsm_dual_yield_diagnostic.png', dpi=300)
    plt.show()

run_dual_yield('SPARC_Data')