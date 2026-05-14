import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ====================== ITSM v9.0: SHARP-YIELD ANALYSIS ======================
# Logic: a0 = cH0 / 2pi (Divisor)
# Modification: Replacing "Simple" Interpolation with "Syntropic Shear"
# Goal: Force the model to "Snatch" the Newtonian floor at high-g
# =============================================================================

def run_sharp_yield(data_dir):
    all_g_bar, all_g_obs = [], []
    
    # 1. DATA GATHERING
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith((".txt", ".dat")):
                try:
                    df = pd.read_csv(os.path.join(root, file), sep=r'\s+', comment='#', header=None)
                    df = df[(df[1] > 0) & (df[0] > 0)].dropna()
                    v_bar_sq = df[3]**2 + 0.5 * df[4]**2 + 0.7 * df[5]**2
                    all_g_bar.extend(v_bar_sq / df[0])
                    all_g_obs.extend(df[1]**2 / df[0])
                except: continue

    g_bar = np.array(all_g_bar)
    g_obs = np.array(all_g_obs)
    obs_ratio = g_obs / g_bar
    
    # 2. CONSTANTS
    H0_si = 70 * 1000 / 3.08567758e22
    c = 299792458
    conv = 3.08567758e13
    a0 = (c * H0_si / (2 * np.pi)) * conv

    # 3. THE INTERPOLATION MODELS
    # Standard (The "Lazy" one in your image)
    ratio_standard = (g_bar + a0 * (np.sqrt(1 + 2 * g_bar / a0) - 1)) / g_bar
    
    # Sharp-Yield (The "Syntropic Shear" - Approaches 1.0 faster)
    # Formula: g_total = g_bar / (1 - exp(-sqrt(g_bar/a0)))
    # This represents a vacuum that 'shatters' its grip exponentially.
    x = np.sqrt(g_bar / a0)
    ratio_sharp = 1 / (1 - np.exp(-x))

    # 4. VISUALIZATION
    plt.figure(figsize=(14, 8), facecolor='white')
    plt.scatter(g_bar, obs_ratio, alpha=0.04, color='black', label='SPARC Data')
    
    sort_idx = np.argsort(g_bar)
    plt.plot(g_bar[sort_idx], ratio_standard[sort_idx], color='grey', lw=2, label='Standard "Lazy" Yield')
    plt.plot(g_bar[sort_idx], ratio_sharp[sort_idx], color='#e63946', lw=4, label='ITSM Sharp-Yield (Syntropic Shear)')

    plt.axhline(y=1, color='#1f77b4', lw=2, label='Newtonian Floor')
    
    plt.xscale('log')
    plt.ylim(0, 5)
    plt.xlabel(r'Baryonic Acceleration ($g_{bar}$)')
    plt.ylabel(r'Anomaly Ratio ($g_{obs} / g_{bar}$)')
    plt.title('Syntropic Shear Test: Does the Vacuum "Shatter" or "Stretch"?')
    plt.legend(loc='upper right', frameon=True, edgecolor='black')
    plt.grid(True, which='both', linestyle=':', alpha=0.3)
    
    plt.show()

run_sharp_yield('SPARC_Data')