"""
ITSM Cosmological Evolution: a0(z) Running Parameter
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Protocol: Plots the deterministic geometric tether a0 = c*H(z)/(2*pi) across cosmic time.
Environment: Windows / Antigravity IDE Workspace Compatible
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, '..', 'Scripts')))
try:
    from itsm_plot_style import apply_tier1_style
    apply_tier1_style()
except ImportError:
    pass

# Constants
c_km_s = 299792.458
c_m_s = 299792458.0
MPC_TO_M = 3.085677581e22
KPC_TO_M = 3.085677581e19

# ITSM Parameters (From Joint Hierarchical Fit)
H0 = 73.97
Om = 0.24
n = 1.44

z = np.linspace(0, 14, 500)
H_z = H0 * np.sqrt(Om * (1 + z)**3 + (1 - Om) * (1 + z)**(-n))

# a0(z) in m/s^2
H_z_si = (H_z * 1e3) / MPC_TO_M
a0_z_ms2 = (c_m_s * H_z_si) / (2 * np.pi)

# Convert to standard units: m/s^2 and (km/s)^2/kpc
# 1 m/s^2 = 3.086e13 (km/s)^2 / kpc
a0_z_sparc = a0_z_ms2 * 3.085677581e13

fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.plot(z, a0_z_ms2, color='darkblue', lw=3, label=r'ITSM Prediction: $a_0(z) = \frac{c \cdot H(z)}{2\pi}$')

# Present-day a0 marker
ax1.axhline(a0_z_ms2[0], color='gray', linestyle='--', lw=2, label=rf'Present Day $a_0 = {a0_z_ms2[0]:.2e}$ m/s$^2$')
ax1.plot(0, a0_z_ms2[0], 'ro', markersize=8)

ax1.set_xlabel(r'Redshift ($z$)', fontsize=15)
ax1.set_ylabel(r'Syntropic Yield Boundary $a_0(z)$ [m s$^{-2}$]', fontsize=15, color='darkblue')
ax1.tick_params(axis='y', labelcolor='darkblue')

# Secondary axis for SPARC units
ax2 = ax1.twinx()
ax2.plot(z, a0_z_sparc, alpha=0) # Invisible plot just to set the scale
ax2.set_ylabel(r'$a_0(z)$ [(km/s)$^2$ kpc$^{-1}$]', fontsize=15, color='darkred')
ax2.tick_params(axis='y', labelcolor='darkred')

ax1.set_title(r'Redshift Evolution of the ITSM Syntropic Yield Boundary $a_0(z)$', fontsize=16, pad=15)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='upper left', fontsize=12)

out_dir = os.path.join(script_dir, "..", "Assets", "Figures")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "itsm_a0_redshift_evolution.png")
plt.savefig(out_path, bbox_inches='tight')
print(f"Exported a0(z) redshift evolution figure to {out_path}")
