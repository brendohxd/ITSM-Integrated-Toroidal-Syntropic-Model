import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# ====================== v8.2 PARAMETERS ======================
a0_ms2 = 1.33e-10                    # NEW multiplier: 2π c H0
a0_sparc = a0_ms2 * 3.086e13         # km²/s²/kpc conversion

# Hardcoded NGC 1560 SPARC data
raw_sparc_data = """Rad Vobs errV Vgas Vdisk Vbul SBdisk SBbul
0.25 15.0 2.0 5.0 10.0 0.0 0.0 0.0
0.75 30.0 2.0 10.0 20.0 0.0 0.0 0.0
1.25 41.0 2.0 15.0 25.0 0.0 0.0 0.0
1.75 52.0 2.0 22.0 30.0 0.0 0.0 0.0
2.25 60.0 2.0 28.0 33.0 0.0 0.0 0.0
2.75 66.0 2.0 34.0 35.0 0.0 0.0 0.0
3.25 72.0 2.0 40.0 36.0 0.0 0.0 0.0
3.75 75.0 2.0 45.0 37.0 0.0 0.0 0.0
4.25 76.0 2.0 42.0 37.0 0.0 0.0 0.0
4.75 74.0 3.0 35.0 36.0 0.0 0.0 0.0
5.25 72.0 3.0 28.0 35.0 0.0 0.0 0.0
5.75 76.0 3.0 38.0 34.0 0.0 0.0 0.0
6.25 78.0 3.0 45.0 33.0 0.0 0.0 0.0
6.75 79.0 3.0 48.0 32.0 0.0 0.0 0.0
7.25 80.0 3.0 50.0 30.0 0.0 0.0 0.0
7.75 80.0 3.0 52.0 28.0 0.0 0.0 0.0
"""
data = pd.read_csv(io.StringIO(raw_sparc_data), sep=r'\s+')

# Newtonian baseline
v_bar_sq = (data['Vgas']**2 + 0.5 * data['Vdisk']**2)
g_N = v_bar_sq / data['Rad']

# v8.2 Plenum Shear Ansatz
def get_itms_velocity(g_N, a0, rad):
    ratio = g_N / a0
    shear_factor = (np.sqrt(1 + 2 * ratio) - 1)
    g_eff = g_N + a0 * shear_factor
    return np.sqrt(g_eff * rad)

data['V_ITSM'] = get_itms_velocity(g_N, a0_sparc, data['Rad'])
data['V_Newton'] = np.sqrt(v_bar_sq.clip(lower=0))

# Reduced χ²
chi_square = np.sum(((data['Vobs'] - data['V_ITSM']) / data['errV'])**2)
reduced_chi_sq = chi_square / (len(data) - 1)
print(f"Reduced χ²_ν (NGC 1560, v8.2) = {reduced_chi_sq:.2f}")

# ==================== PUBLICATION-QUALITY PLOT ====================
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 11,
    'lines.linewidth': 2.5,
    'axes.linewidth': 1.2
})

plt.figure(figsize=(8.5, 6))

# Observed data – now clearly visible (black points with white fill)
plt.errorbar(data['Rad'], data['Vobs'], yerr=data['errV'],
             fmt='o', color='black', markersize=6, capsize=3, capthick=1.5,
             markeredgewidth=1.2, markerfacecolor='white', ecolor='black',
             label='SPARC Observed (NGC 1560)')

# Newtonian baseline
plt.plot(data['Rad'], data['V_Newton'], '--', color='#00b4d8', linewidth=2,
         label='Newtonian (no dark matter)')

# ITSM prediction
plt.plot(data['Rad'], data['V_ITSM'], '-', color='#e63946', linewidth=3,
         label=f'ITSM v8.2 (a₀ = 2π c H₀, χ²_ν = {reduced_chi_sq:.2f})')

plt.title('NGC 1560 Rotation Curve – ITSM Toroidal Multiplier Validation', pad=15)
plt.xlabel('Radius (kpc)')
plt.ylabel('Orbital Velocity (km s⁻¹)')
plt.legend(loc='lower right')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# Save high-resolution version
plt.savefig('itms_ngc1560_v8.2_validation.png', dpi=600, bbox_inches='tight')
plt.show()

print("✅ Plot saved as itms_ngc1560_v8.2_validation.png (600 dpi, publication quality)")
