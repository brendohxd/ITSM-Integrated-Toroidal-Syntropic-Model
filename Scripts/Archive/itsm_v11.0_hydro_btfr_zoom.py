import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit

# ====================== ITSM v11.0: HYDRO & ZOOM-IN ======================
# Logic: a0 = cH0 / 2pi
# Purpose: Validate the BTFR (Baryonic Tully-Fisher Relation)
# Goal: Prove gas/star ratios follow Plenum Drag without "Feedback Tuning"
# =========================================================================

def run_btfr_simulation(data_dir):
    galaxy_masses = []
    final_velocities = []
    
    # 1. CENSUS DATA GATHERING (The "Hydro" Evidence)
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith((".txt", ".dat")):
                try:
                    df = pd.read_csv(os.path.join(root, file), sep=r'\s+', comment='#', header=None)
                    df = df[(df[1] > 0) & (df[0] > 0)].dropna()
                    
                    # Extract total Baryonic Mass (Stars + Gas)
                    # We use the furthest data point (flat part of the curve)
                    v_flat = df[1].iloc[-1] 
                    rad_max = df[0].iloc[-1]
                    
                    # Estimate total mass from the profile
                    # Mb = Integral of luminosity + gas
                    m_stars = np.sum(df[4]**2 * df[0]) # Simplified proxy
                    m_gas = np.sum(df[3]**2 * df[0])
                    total_mb = m_stars + m_gas
                    
                    galaxy_masses.append(total_mb)
                    final_velocities.append(v_flat)
                except: continue

    m_b = np.array(galaxy_masses)
    v_f = np.array(final_velocities)

    # 2. THE ITSM PREDICTION (The Analytical Law)
    # Law: Vf^4 = G * Mb * a0
    G = 4.3009e-6 # kpc (km/s)^2 / M_sun
    a0_ms2 = (299792458 * (70 * 1000 / 3.08567758e22)) / (2 * np.pi)
    a0_kpc = a0_ms2 * 3.08567758e13 # km/s^2/kpc
    
    m_range = np.logspace(np.log10(min(m_b)), np.log10(max(m_b)), 100)
    v_pred = (G * m_range * a0_kpc)**(1/4) # The BTFR Slope

    # 3. VISUALIZATION
    plt.figure(figsize=(10, 8), facecolor='white')
    plt.scatter(m_b, v_f, color='black', alpha=0.5, label='SPARC Hydro Data')
    plt.plot(m_range, v_pred, color='#e63946', lw=3, label='ITSM BTFR Prediction')
    
    plt.xscale('log'); plt.yscale('log')
    plt.xlabel(r'Total Baryonic Mass ($M_{\odot}$)'); plt.ylabel(r'Flat Rotation Velocity $V_f$ (km/s)')
    plt.title('Validation 2 & 3: Hydrodynamical BTFR Scaling')
    plt.legend(); plt.grid(True, which='both', linestyle=':', alpha=0.3)
    plt.show()

run_btfr_simulation('SPARC_Data')