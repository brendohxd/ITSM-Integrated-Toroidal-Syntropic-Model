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
# ITSM STRICT ENFORCEMENT: No Dark Matter. Om is purely Baryonic (Omega_b h^2 = 0.02237)
h_itsm = H0_itsm / 100.0
Om_itsm = 0.02237 / (h_itsm**2)

# Planck 2018 ΛCDM baseline for comparison
H0_lcdm = 67.4
Om_lcdm = 0.315

# LambdaCDM Framework
H_lcdm = H0_lcdm * np.sqrt(Om_lcdm * (1+z)**3 + (1-Om_lcdm))

from scipy.integrate import odeint

def itsm_ode_plot(y, z_val, H0, n):
    Om_m, Om_p = y
    E2 = Om_m + Om_p
    if E2 <= 1e-10:
        E = 1e-5
    else:
        E = np.sqrt(E2)
        
    Q_term = n * (1 + z_val)**(-3) / (E * (1 + z_val))
    
    dOmdz = 3 * Om_m / (1 + z_val) + Q_term
    dOpdz = -Q_term
    return [dOmdz, dOpdz]

# ITSM Syntropic Decay: True ODE Integration
n_itsm = 3.0
y0 = [Om_itsm, 1.0 - Om_itsm]
sol = odeint(itsm_ode_plot, y0, z, args=(H0_itsm, n_itsm))
E_z = np.sqrt(np.maximum(sol[:, 0] + sol[:, 1], 1e-10))
H_itsm = H0_itsm * E_z

plt.figure(figsize=(10, 6))
plt.plot(z, H_lcdm, '--', color='#D55E00', lw=2.5, label=r'$\Lambda$CDM ($H_0=67.4$, Planck 2018)')
plt.plot(z, H_itsm, '-', color='#0072B2', lw=3, label=rf'ITSM Syntropic Decay ($H_0={H0_itsm}$, $\Omega_b={Om_itsm:.3f}$)')

plt.title(r'Effective Hubble Parameter Evolution: DESI 2024 Confrontation', fontsize=16, pad=15)
plt.xlabel(r'Redshift ($z$)', fontsize=15)
plt.ylabel(r'$H(z)$ [km s$^{-1}$ Mpc$^{-1}$]', fontsize=15)
plt.legend(loc='upper left', framealpha=0.9, edgecolor='black', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_desi_bao_publication.png"))
plt.savefig(out_path)
print(f"Asset generated: {out_path}")
