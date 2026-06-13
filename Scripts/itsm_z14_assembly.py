"""
Integrated Toroidal-Syntropic Model (ITSM) - JADES-GS-z14-0 Timeline Analysis
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Environment: Windows / Antigravity IDE Workspace Compatible
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from itsm_plot_style import apply_tier1_style
apply_tier1_style()
import os

# Publication Formatting


# 1. Physical Parameters
z_range = np.linspace(30, 10, 500)
# Time from Big Bang in Megayears (Approximate scale for high-z)
t_myr = 28000 * (1 + z_range)**(-1.5)

# -- Standard Model: Hierarchical Merging (Power Law) --
m_lcdm = 10**4 * (t_myr / 50)**2.5

# -- ITSM Model: Toroidal Scaffolding (Exponential Condensation) --
# Growth exponent derived from the ITSM syntropic decay parameter n = 1.44
n_itsm = 1.44
# Characteristic e-folding time proportional to n_itsm
gamma_n = n_itsm / 65.0 
m_itsm = 10**6 * np.exp((t_myr - 50) * gamma_n)

# 2. Observational Data Points
# JWST JADES-GS-z14-0 (Carniani et al. 2024)
z_obs_jades = 14.32
t_obs_jades = 290 # Myr after Big Bang
m_obs_jades = 10**8.5 # Estimated Stellar Mass (Solar Masses)

# JWST UNCOVER candidates (Labbé et al. 2023)
z_obs_labbe = np.array([7.5, 9.1])
m_obs_labbe = np.array([10**10.5, 10**10.8])

# 3. Visualization Architecture
fig, ax = plt.subplots(figsize=(11, 7.5))

# Plot Growth Curves
ax.plot(z_range, m_itsm, color='#0099CC', lw=3, label=r'ITSM: Toroidal Scaffolding (Predictive)')
ax.plot(z_range, m_lcdm, color='#C00000', lw=2.5, ls='--', label=r'$\Lambda$CDM: Hierarchical Merging (Standard)')

# Plot Observational Anchors
ax.scatter(z_obs_jades, m_obs_jades, color='#F0E442', s=350, marker='*', edgecolors='black',
           linewidths=1.5, zorder=5, label=r'JADES-GS-z14-0 (Carniani et al. 2024)')

ax.scatter(z_obs_labbe, m_obs_labbe, color='#E69F00', s=200, marker='D', edgecolors='black',
           linewidths=1.2, zorder=4, label=r'Massive Candidates (Labbé et al. 2023)')

# The Lambda-CDM "Forbidden Zone"
ax.fill_between([30, 13], 10**8, 10**11, color='#C00000', alpha=0.08, label=r'$\Lambda$CDM Forbidden Zone')

# Annotations
ax.annotate(r'$\Lambda$CDM Growth Lag' + '\n' + r'(Dark Matter Bottleneck)', 
            xy=(18, 10**6), xytext=(21.5, 10**4.5),
            arrowprops=dict(arrowstyle="->", color='#C00000', lw=2), color='#C00000', fontsize=12)

ax.annotate(r'ITSM Accelerated Nucleation' + '\n' + r'(Syntropic Scaffolding)', 
            xy=(16, 10**8.5), xytext=(19.5, 10**10),
            arrowprops=dict(arrowstyle="->", color='#0099CC', lw=2), color='#0099CC', fontsize=12)

# Axes and Limits
ax.set_yscale('log')
ax.set_xlim(25, 10)
ax.set_ylim(10**4, 10**11)
ax.invert_xaxis() # Redshift decays from left to right

ax.grid(True, which='major', linestyle='-', alpha=0.3)
ax.grid(True, which='minor', linestyle=':', alpha=0.2)

ax.set_title(r"Mass Assembly Timeline: The High-Redshift Maturity Crisis" + "\n" +
             r"Toroidal Superfluid Nucleation vs. Hierarchical Merging",
             fontsize=16, pad=15)

ax.set_xlabel(r"Redshift ($z$)", fontsize=15)
ax.set_ylabel(r"Stellar Mass ($M_{\odot}$)", fontsize=15)

plt.legend(loc='lower left', fontsize=12, framealpha=0.95, edgecolor='black')

plt.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_z14_assembly_publication.png"))
plt.savefig(out_path, dpi=300)
print(f"Asset generated: {out_path}")