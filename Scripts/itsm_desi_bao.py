"""
Integrated Toroidal-Syntropic Model (ITSM) - Syntropic Volume Decay (DESI 2024)
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



z = np.linspace(0, 3, 100)

# ITSM Globally-Optimised Parameters (Joint Pantheon+ & DESI DR2 Hierarchical MCMC)
H0_itsm = 73.97
Om_itsm = 0.240

# Planck 2018 ΛCDM baseline for comparison
H0_lcdm = 67.4
Om_lcdm = 0.315

# LambdaCDM Framework
H_lcdm = H0_lcdm * np.sqrt(Om_lcdm * (1+z)**3 + (1-Om_lcdm))

# ITSM Syntropic Decay: Omega_syn scales as (1+z)^{-3}
H_itsm = H0_itsm * np.sqrt(Om_itsm * (1+z)**3 + (1-Om_itsm) * (1+z)**-3)

plt.figure(figsize=(10, 6))
plt.plot(z, H_lcdm, '--', color='#D55E00', lw=2.5, label=r'$\Lambda$CDM ($H_0=67.4$, Planck 2018)')
plt.plot(z, H_itsm, '-', color='#0072B2', lw=3, label=r'ITSM Syntropic Decay ($H_0=73.97$, $\Omega_m=0.240$)')

plt.title(r'Effective Hubble Parameter Evolution: DESI 2024 Confrontation', fontsize=16, pad=15)
plt.xlabel(r'Redshift ($z$)', fontsize=15)
plt.ylabel(r'$H(z)$ [km s$^{-1}$ Mpc$^{-1}$]', fontsize=15)
plt.legend(loc='upper left', framealpha=0.9, edgecolor='black', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_desi_bao_publication.png"))
plt.savefig(out_path, dpi=600)
print(f"Asset generated: {out_path}")
