"""
Integrated Toroidal-Syntropic Model (ITSM) - Syntropic Volume Decay (DESI 2024)
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Environment: Windows / Antigravity IDE Workspace Compatible
"""

import numpy as np
import matplotlib.pyplot as plt
import os

plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 14})

z = np.linspace(0, 3, 100)
H0 = 67.4
Om = 0.315

# LambdaCDM Framework
H_lcdm = H0 * np.sqrt(Om * (1+z)**3 + (1-Om))

# ITSM Syntropic Decay: Omega_syn scales as (1+z)^{-3}
H_itsm = H0 * np.sqrt(Om * (1+z)**3 + (1-Om) * (1+z)**-3)

plt.figure(figsize=(10, 6))
plt.plot(z, H_lcdm, '--', color='#D55E00', lw=2.5, label=r'$\Lambda$CDM (Static Dark Energy)')
plt.plot(z, H_itsm, '-', color='#0072B2', lw=3, label=r'ITSM Syntropic Volume Decay ($\propto (1+z)^{-3}$)')

plt.title(r'\textbf{Effective Hubble Parameter Evolution: DESI 2024 Confrontation}', fontsize=16, pad=15)
plt.xlabel(r'Redshift ($z$)', fontsize=15)
plt.ylabel(r'$H(z)$ [km s$^{-1}$ Mpc$^{-1}$]', fontsize=15)
plt.legend(loc='upper left', framealpha=0.9, edgecolor='black', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_desi_bao_publication.png"))
plt.savefig(out_path, dpi=300)
print(f"Asset generated: {out_path}")
