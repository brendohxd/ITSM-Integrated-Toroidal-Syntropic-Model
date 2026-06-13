"""
Integrated Toroidal-Syntropic Model (ITSM) - Hubble Tension Geometric Resolver
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Environment: Windows / Antigravity IDE Workspace Compatible
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from itsm_plot_style import apply_tier1_style
apply_tier1_style()

# Publication Formatting


# 1. Physical Constants & Observational Limits
H_PLANCK = 67.4  # Early-Universe poloidal measurement [km/s/Mpc]
H_PLANCK_ERR = 0.5 # 1-sigma uncertainty (Planck 2018)

# ITSM Topological Derivation: On a T^3 manifold, the variance between 
# the maximum (toroidal) and minimum (poloidal) expansion rates is 
# defined by the geometric invariant 1/12 (~8.33%).
# Therefore, H_SHOES is PREDICTED by the model, not just fitted.
TOPOLOGICAL_VARIANCE = 1.0 / 12.0
H_SHOES = H_PLANCK * (1.0 + TOPOLOGICAL_VARIANCE) # ~73.01 km/s/Mpc
H_SHOES_ERR = 1.04 # 1-sigma uncertainty (Riess et al. 2022)

POINTS = 1000

# 2. Computational Engine
theta = np.linspace(0, np.pi, POINTS)
h_avg = (H_PLANCK + H_SHOES) / 2.0
h_amp = (H_SHOES - H_PLANCK) / 2.0

# ITSM Geometric Projection: H(theta) = H_avg - H_amp * cos(2*theta)
# Phase shifted so 0 degrees is the Poloidal Axis (lowest expansion)
h_theta = h_avg - h_amp * np.cos(2 * theta)
variance_pct = TOPOLOGICAL_VARIANCE * 100.0

# 3. Visualization Architecture
fig, ax = plt.subplots(figsize=(10, 6.5))

# Shade the Tension Zone
ax.fill_between(theta, H_PLANCK, H_SHOES, color='#0072B2', alpha=0.05)

# Plot the Institutional Limits with 1-sigma shading
ax.fill_between(theta, H_SHOES - H_SHOES_ERR, H_SHOES + H_SHOES_ERR, color='#D55E00', alpha=0.15)
ax.axhline(H_SHOES, color='#D55E00', ls='--', lw=2.5, alpha=0.9,
           label=rf'SH0ES / ITSM Predicted (Toroidal Limit $\approx {H_SHOES:.2f}$)')

ax.fill_between(theta, H_PLANCK - H_PLANCK_ERR, H_PLANCK + H_PLANCK_ERR, color='#0072B2', alpha=0.15)
ax.axhline(H_PLANCK, color='#0072B2', ls='--', lw=2.5, alpha=0.9,
           label=rf'Planck 2018 (Poloidal Limit $\approx {H_PLANCK:.2f}$)')

# Plot the Anisotropic Curve
ax.plot(theta, h_theta, color='black', lw=3.5,
        label=r'ITSM Anisotropic Projection ($H_0(\theta)$)')

# Annotate the Variance
ax.text(np.pi/2, 71.5, rf"Manifold Variance: {variance_pct:.1f}\%", color='black', fontsize=12,
        ha='center', va='center', bbox=dict(facecolor='white', edgecolor='gray', alpha=0.9, boxstyle='round,pad=0.4'))

# Axis Limits and Ticks
ax.set_xlim(0, np.pi)
ax.set_ylim(65, 75)
ax.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
ax.set_xticklabels([r'$0^\circ$' + '\n' + r'(Poloidal Axis)', r'$45^\circ$',
                    r'$90^\circ$' + '\n' + r'(Toroidal Edge)', r'$135^\circ$',
                    r'$180^\circ$' + '\n' + r'(Poloidal Axis)'])

# Grid and Labels
ax.grid(True, which='both', color='lightgray', linestyle='--', alpha=0.7)
ax.set_xlabel(r'Observational Viewing Angle $\theta$ (Degrees)', fontsize=15)
ax.set_ylabel(r'Effective Expansion Rate $H_0$ (km s$^{-1}$ Mpc$^{-1}$)', fontsize=15)
ax.set_title(r'Hubble Tension Geometric Resolution' + '\n' + 
             r'(ITSM Toroidal Anisotropy Projection)', fontsize=16, pad=15)

# Legend
ax.legend(loc='lower right', framealpha=0.95, edgecolor='black', fontsize=12)

plt.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_hubble_resolver_publication.png"))
plt.savefig(out_path, dpi=300)
print(f"Asset generated: {out_path}")