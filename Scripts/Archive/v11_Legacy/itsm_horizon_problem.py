"""
Integrated Toroidal-Syntropic Model (ITSM) - Horizon Problem & Cosmic Inflation Deletion
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import os
import sys

# Import custom plot style if available, otherwise use defaults
try:
    from itsm_plot_style import apply_tier1_style
    apply_tier1_style()
except ImportError:
    pass

# Constants
c = 299792.458  # km/s

# LambdaCDM Parameters (Planck 2018)
H0_lcdm = 67.4
Om_lcdm = 0.315
Or_lcdm = 9.2e-5
Ol_lcdm = 1.0 - Om_lcdm - Or_lcdm

# ITSM Parameters (Joint MCMC)
H0_itsm = 73.97
Om_itsm = 0.240
Or_itsm = 9.2e-5
Osyn_itsm = 1.0 - Om_itsm - Or_itsm

def E_lcdm(z):
    return np.sqrt(Or_lcdm*(1+z)**4 + Om_lcdm*(1+z)**3 + Ol_lcdm)

def E_itsm(z):
    # Syntropic decay (1+z)^-3
    return np.sqrt(Or_itsm*(1+z)**4 + Om_itsm*(1+z)**3 + Osyn_itsm*(1+z)**-3)

def comoving_horizon(z_target, model='itsm'):
    def integrand(z):
        if model == 'itsm':
            return c / (H0_itsm * E_itsm(z))
        else:
            return c / (H0_lcdm * E_lcdm(z))
    
    # Integrate from z_target to infinity (approx 1e6 is fine for numerical stability)
    # The horizon is the distance a photon could have traveled from the Big Bang to redshift z
    r_H, _ = quad(integrand, z_target, 1e6)
    return r_H

# Calculate comoving horizon at recombination
z_rec = 1090
r_H_lcdm_rec = comoving_horizon(z_rec, 'lcdm')
r_H_itsm_rec = comoving_horizon(z_rec, 'itsm')

print("-" * 50)
print("HORIZON PROBLEM COMPUTATION (z=1090)")
print("-" * 50)
print(f"LambdaCDM Comoving Horizon: {r_H_lcdm_rec:.2f} Mpc")
print(f"ITSM Comoving Horizon:      {r_H_itsm_rec:.2f} Mpc")

# Toroidal Fundamental Domain (comoving)
# In ITSM, the toroidal circumference is L_T = c/H_0
L_T = c / H0_itsm
print("-" * 50)
print(f"ITSM Toroidal Fundamental Length L_T: {L_T:.2f} Mpc")

# To solve the horizon problem without inflation, the causal horizon must be 
# large enough that opposite points on the torus are in thermal contact.
# Because the universe wraps around, the maximum distance between any two points is L_T / 2.
print(f"Maximum Topological Distance (L_T / 2): {L_T/2:.2f} Mpc")
print("-" * 50)
if r_H_itsm_rec >= (L_T / 2):
    print("RESULT: THERMAL EQUILIBRIUM ACHIEVED.")
    print("The causal horizon at recombination exceeds the maximum topological distance.")
    print("Cosmic Inflation is mathematically OBSOLETE.")
else:
    print("RESULT: The horizon is smaller than the topological domain.")
    print(f"Ratio r_H / (L_T/2) = {r_H_itsm_rec / (L_T/2):.4f}")
print("-" * 50)


# Generate diagnostic plot
z_vals = np.logspace(0, 4, 200)
r_H_lcdm_array = [comoving_horizon(z, 'lcdm') for z in z_vals]
r_H_itsm_array = [comoving_horizon(z, 'itsm') for z in z_vals]

plt.figure(figsize=(10, 6))
plt.plot(z_vals, r_H_lcdm_array, '--', color='#D55E00', lw=2.5, label=r'$\Lambda$CDM Horizon (Planck 2018)')
plt.plot(z_vals, r_H_itsm_array, '-', color='#0072B2', lw=3, label=r'ITSM Horizon ($H_0=73.97$)')

# Add Toroidal Boundary limits
plt.axhline(y=L_T, color='k', linestyle=':', lw=2, label=r'Toroidal Boundary $L_T = c/H_0$')
plt.axhline(y=L_T/2, color='green', linestyle='-.', lw=2, label=r'Thermal Contact Threshold ($L_T/2$)')

plt.xscale('log')
plt.yscale('log')
plt.axvline(x=1090, color='gray', linestyle='-.', lw=1.5, alpha=0.7)
plt.text(1090*1.1, 50, r'Recombination\n($z \approx 1090$)', color='gray', fontsize=11)

plt.title(r'Comoving Causal Horizon vs Redshift: Inflation Deletion', fontsize=16, pad=15)
plt.xlabel(r'Redshift ($z$)', fontsize=15)
plt.ylabel(r'Comoving Horizon $r_H(z)$ [Mpc]', fontsize=15)
plt.legend(loc='lower left', framealpha=0.9, edgecolor='black', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_horizon_problem.png"))
plt.savefig(out_path)
print(f"Asset generated: {out_path}")
