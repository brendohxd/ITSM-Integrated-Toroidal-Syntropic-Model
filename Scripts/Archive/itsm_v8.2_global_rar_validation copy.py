import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error

# ====================== v8.2 MULTIPLIER VARIANT ======================
# Logic: a0 = 2pi * c * H0 (The Multiplier Derivation)
# Purpose: Comparative RAR Analysis across 175 galaxies
# Data Source: Local SPARC Mirror (extracted to 'SPARC_Data')
# =====================================================================

# 1. THE CLEAN SLATE PROTOCOL
plt.close('all')

# 2. THE MASTER CONSTANTS
H0_km_s_mpc = 70.0
H0_si = H0_km_s_mpc * 1000 / 3.08567758e22  # Hubble flow in s^-1
c = 299792458                               # Speed of light

# THE MULTIPLIER LOGIC: a0 as magnified circulation
# This version treats 2pi as a scaling factor rather than a divisor
a0_ms2 = (2 * np.pi) * c * H0_si             # Result: ~4.28e-09 m/s^2
a0_sparc = a0_ms2 * 3.08567758e13           # Conversion to km^2/s^2/kpc

# 3. ROBUST DATA COMPILATION ENGINE
def compile_rar_matrix(data_dir):
    all_g_bar = []
    all_g_obs = []
    galaxy_count = 0
    
    if not os.path.exists(data_dir):
        print(f"❌ Target directory '{data_dir}' not found.")
        return None, None, 0

    file_list = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith((".txt", ".dat")):
                file_list.append(os.path.join(root, file))

    if not file_list:
        print("❌ No valid .txt or .dat files found.")
        return None, None, 0

    print(f"Aggregating {len(file_list)} files for Multiplier Variant Analysis...")
    
    for file_path in file_list:
        try:
            df = pd.read_csv(file_path, sep=r'\s+', comment='#', header=None, on_bad_lines='skip')
            if df.shape[1] >= 6:
                df = df[(df[1] > 0) & (df[0] > 0)].dropna()
                
                # Baryonic Acceleration (g_bar)
                v_bar_sq = df[3]**2 + 0.5 * df[4]**2 + 0.7 * df[5]**2
                g_bar = v_bar_sq / df[0]
                
                # Observed Acceleration (g_obs)
                g_obs = df[1]**2 / df[0]
                
                all_g_bar.extend(g_bar)
                all_g_obs.extend(g_obs)
                galaxy_count += 1
        except Exception:
            continue
                
    return np.array(all_g_bar), np.array(all_g_obs), galaxy_count

# 4. EXECUTION
data_path = 'SPARC_Data' 
g_bar, g_obs, total_galaxies = compile_rar_matrix(data_path)

if g_bar is not None and len(g_bar) > 0:
    # 5. ITSM PREDICTIVE MODEL (Multiplier Variant)
    g_predicted = g_bar + a0_sparc * (np.sqrt(1 + 2 * g_bar / a0_sparc) - 1)
    
    # Calculate Statistical Fit (Residuals)
    # Using log-space to handle the wide range of astronomical scales
    rmse = np.sqrt(mean_squared_error(np.log10(g_obs), np.log10(g_predicted)))
    mae = mean_absolute_error(np.log10(g_obs), np.log10(g_predicted))

    # 6. TEXTUAL REPORTING
    print("\n" + "="*50)
    print("   ITSM v8.2 MULTIPLIER VARIANT REPORT")
    print("="*50)
    print(f"Total Galaxies Processed:   {total_galaxies}")
    print(f"Total Data Points (N):      {len(g_bar)}")
    print("-" * 50)
    print(f"Derived a0 (SI):            {a0_ms2:.4e} m/s^2")
    print(f"Derived a0 (SPARC units):   {a0_sparc:.4f}")
    print("-" * 50)
    print(f"Log-Space RMSE:             {rmse:.4f}")
    print(f"Log-Space MAE:              {mae:.4f}")
    print("-" * 50)
    # The multiplier version usually results in much higher error (lower accuracy)
    print("STATUS: " + ("✅ CORRELATED" if rmse < 0.15 else "⚠️ DIVERGENT"))
    print("="*50 + "\n")

    # 7. VISUALIZATION
    g_bar_smooth = np.logspace(-3, 2, 1000)
    g_itsm_curve = g_bar_smooth + a0_sparc * (np.sqrt(1 + 2 * g_bar_smooth / a0_sparc) - 1)

    plt.rcParams.update({'font.family': 'serif', 'figure.facecolor': 'white'})
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor('white')

    # Density mapping of the actual data
    hb = ax.hexbin(g_bar, g_obs, gridsize=70, bins='log', cmap='Greys', alpha=0.5, label='SPARC Global Census')
    cb = fig.colorbar(hb, ax=ax)
    cb.set_label('Sample Density (log10)')

    # Predictive line for the Multiplier Variant
    ax.plot(g_bar_smooth, g_itsm_curve, color='#e63946', lw=3.5, 
            label=r'ITSM Multiplier ($a_0 = 2\pi c H_0$)')

    ax.plot(g_bar_smooth, g_bar_smooth, '--', color='#1f77b4', alpha=0.8, label='Newtonian Limit')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel(r'Baryonic Acceleration $g_{bar}$')
    ax.set_ylabel(r'Observed Acceleration $g_{obs}$')
    ax.set_title('Global RAR: Multiplier Variant Analysis', pad=20)
    ax.legend(loc='upper left', frameon=True, edgecolor='black')
    ax.grid(True, which='both', linestyle=':', alpha=0.3)

    plt.tight_layout()
    plt.savefig('itsm_v8.2_multiplier_validation.png', dpi=300)
    plt.show()
else:
    print("❌ Critical Failure: No data points available for analysis.")