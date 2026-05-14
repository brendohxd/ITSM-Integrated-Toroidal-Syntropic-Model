import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ====================== ITSM v12.0: THE ULTIMATE COMPARISON ======================
# ITSM Logic: a0 = cH0 / 2pi (The Saturable Superfluid)
# Lambda-CDM Logic: Empirical Fit (The "Ghost Motor" Approximation)
# Goal: Identify the "Superior Truth" in the SPARC Census.
# =================================================================================

def run_ultimate_comparison(data_dir):
    all_g_bar, all_g_obs = [], []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith((".txt", ".dat")):
                try:
                    df = pd.read_csv(os.path.join(root, file), sep=r'\s+', comment='#', header=None)
                    df = df[(df[1] > 0) & (df[0] > 0)].dropna()
                    # Calculate accelerations
                    v_bar_sq = df[3]**2 + 0.5*df[4]**2 + 0.7*df[5]**2
                    all_g_bar.extend(v_bar_sq / df[0])
                    all_g_obs.extend(df[1]**2 / df[0])
                except: continue

    g_bar = np.array(all_g_bar)
    g_obs = np.array(all_g_obs)
    obs_ratio = g_obs / g_bar
    
    # 1. ITSM Constants & Formula (Integrated Transition)
    a0_itsm = (299792458 * (70*1000/3.08567758e22) / (2*np.pi)) * 3.08567758e13
    x = np.sqrt(g_bar / a0_itsm)
    ratio_itsm = 1 + (1 / (x + np.exp(x - 1))) 

    # 2. Lambda-CDM / Standard Narrative Proxy
    # This is the "Standard Interpolation Function" (McGaugh et al. 2016)
    # This is what Lambda-CDM tries to replicate with 'Feedback' tuning.
    # a0_standard is typically 1.2e-10 m/s^2
    a0_std = 1.2e-10 * 3.08567758e13 
    ratio_lcdm = 1 / (1 - np.exp(-np.sqrt(g_bar / a0_std)))

    # 3. VISUALIZATION
    plt.figure(figsize=(14, 9), facecolor='white')
    
    # The SPARC Census (Raw Truth)
    plt.scatter(g_bar, obs_ratio, alpha=0.04, color='black', label='SPARC Observations (175 Galaxies)')
    
    sort_idx = np.argsort(g_bar)
    
    # The Contenders
    plt.plot(g_bar[sort_idx], ratio_itsm[sort_idx], color='#e63946', lw=5, 
             label=r'ITSM: Integrated Transition ($a_0 = \frac{cH_0}{2\pi}$)')
    
    plt.plot(g_bar[sort_idx], ratio_lcdm[sort_idx], color='#3a86ff', lw=3, linestyle='--', 
             label=r'$\Lambda$CDM / Standard Empirical Fit')

    # The Newtonian Horizon
    plt.axhline(y=1, color='#000000', lw=1.5, alpha=0.5, label='Newtonian Baseline')