import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import warnings
warnings.filterwarnings('ignore')

# ---------------------------------------------------------
# ITSM Global RAR Analysis - Refined Version
# ---------------------------------------------------------

plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath}",
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "axes.facecolor": "white",
    "figure.facecolor": "white",
    "font.size": 14
})

# 1. ITSM Yield Threshold
a0_ms2 = 1.08e-10
conv_factor = 3.086e13                    # m/s² → (km/s)²/kpc
a0_sparc = a0_ms2 * conv_factor
print(f"ITSM a0 in SPARC units: {a0_sparc:.1f}")

# 2. Path handling
script_dir = os.path.dirname(os.path.abspath(__file__))
sparc_path = os.path.join(script_dir, "..", "SPARC_data", "*.dat")
sparc_path = os.path.normpath(sparc_path)

file_list = glob.glob(sparc_path)
print(f"Found {len(file_list)} galaxy data files.")

if not file_list:
    raise FileNotFoundError(f"No .dat files found in:\n{sparc_path}")

# M/L ratios (standard SPARC 3.6μm)
upsilon_disk = 0.5
upsilon_bulge = 0.7

g_bar_all = []
g_obs_all = []
g_obs_err_all = []
galaxy_count = 0

print("Parsing galaxies...")

for file in file_list:
    try:
        df = pd.read_csv(file, sep=r'\s+', comment='#', 
                        names=['Rad', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbul', 'SBdisk', 'SBbul'],
                        header=0, engine='python')
        
        if len(df) < 5:  # Skip very sparse galaxies
            continue
            
        # Baryonic contribution
        v_gas_sq = np.abs(df['Vgas']) * df['Vgas']
        v_disk_sq = upsilon_disk * np.abs(df['Vdisk']) * df['Vdisk']
        v_bul_sq = upsilon_bulge * np.abs(df['Vbul']) * df['Vbul']
        
        v_bar_sq = v_gas_sq + v_disk_sq + v_bul_sq
        
        valid = (df['Rad'] > 0) & (df['Vobs'] > 0) & (df['errV'] > 0)
        
        g_bar = v_bar_sq[valid] / df['Rad'][valid]
        g_obs = (df['Vobs'][valid]**2) / df['Rad'][valid]
        g_err = (2 * df['Vobs'][valid] * df['errV'][valid]) / df['Rad'][valid]
        
        # Basic quality filter
        valid2 = (g_bar > 1e-15) & (g_obs > 1e-15) & np.isfinite(g_err)
        
        g_bar_all.extend(g_bar[valid2].values)
        g_obs_all.extend(g_obs[valid2].values)
        g_obs_err_all.extend(g_err[valid2].values)
        
        galaxy_count += 1
        
    except Exception as e:
        print(f"Skipped {os.path.basename(file)}: {e}")

# Final arrays
g_bar_all = np.array(g_bar_all)
g_obs_all = np.array(g_obs_all)
g_err_all = np.array(g_obs_err_all)

# Clean
valid = (g_bar_all > 0) & (g_obs_all > 0) & (g_err_all > 0) & np.isfinite(g_err_all)
g_bar = g_bar_all[valid]
g_obs = g_obs_all[valid]
g_err = g_err_all[valid]

print(f"\nFinal statistics:")
print(f"Galaxies processed: {galaxy_count}")
print(f"Total data points: {len(g_obs)}")

# ITSM prediction (Simple interpolating function)
g_eff_itsm = (g_bar / 2) + np.sqrt((g_bar / 2)**2 + g_bar * a0_sparc)

# Chi-square
chi2 = np.sum(((g_obs - g_eff_itsm) / g_err)**2)
dof = len(g_obs) - 1
reduced_chi2 = chi2 / dof

print(f"Global Reduced chi^2_v = {reduced_chi2:.3f} (dof = {dof})")

# ========================= PLOTTING =========================
plt.figure(figsize=(11, 8))

g_min, g_max = 1e-12 * conv_factor, 1e-8 * conv_factor

hb = plt.hexbin(g_bar, g_obs, gridsize=80, cmap='Blues', bins='log',
                xscale='log', yscale='log', mincnt=1, edgecolors='none', alpha=0.9)

plt.colorbar(hb, label=r'$\log_{10}(\text{Density of Data Points})$')

x_vals = np.logspace(np.log10(g_min), np.log10(g_max), 200)

# Newtonian
plt.plot(x_vals, x_vals, '--', color='gray', lw=2, label=r'Newtonian ($g_{obs}=g_{bar}$)')

# ITSM
itsm_curve = (x_vals/2) + np.sqrt((x_vals/2)**2 + x_vals * a0_sparc)
plt.plot(x_vals, itsm_curve, '-', color='darkred', lw=3, 
         label=f'ITSM ($\\chi^2_\\nu = {reduced_chi2:.2f}$)')

plt.axvline(a0_sparc, color='black', ls=':', alpha=0.6, lw=1.5)
plt.annotate(r'$a_0$ Yield Boundary', xy=(a0_sparc, g_min*8), 
             xytext=(a0_sparc*3, g_min*4),
             arrowprops=dict(arrowstyle='->', color='black'), fontsize=12)

plt.title(r'\textbf{Global Radial Acceleration Relation (SPARC)}', fontsize=18, pad=20)
plt.xlabel(r'Baryonic Acceleration $g_{bar}$ [km$^2$ s$^{-2}$ kpc$^{-1}$]', fontsize=15)
plt.ylabel(r'Observed Acceleration $g_{obs}$ [km$^2$ s$^{-2}$ kpc$^{-1}$]', fontsize=15)

plt.xlim(g_min, g_max)
plt.ylim(g_min, g_max)
plt.legend(loc='upper left', fontsize=12, framealpha=0.95)
plt.grid(True, which='both', ls='-', alpha=0.3)

plt.tight_layout()
plt.savefig('itsm_global_rar_publication.png', dpi=300, bbox_inches='tight')
print("\nPlot saved as 'itsm_global_rar_publication.png'")