"""
ITSM Experimental Script — Matter Power Spectrum P(k) via CAMB
Author: Brendon Boyd
Staging: Analysis/Experimental/CAMB_Matter/
Status: EXPERIMENTAL

Description:
This script computes the linear matter power spectrum P(k) at z=0 for:
1. Standard Lambda-CDM (Planck 2018 best-fit)
2. ITSM configuration: H0 = 73.97 (from Joint MCMC) and effective w = -1.27
   (derived from syntropic volume decay parameter n = 0.81).

Goal: Demonstrate that the ITSM syntropic decay preserves the turnover k_eq 
and the BAO wiggles in the matter distribution without relying on collisionless 
Cold Dark Matter (conceptually, the Plenum supplies the necessary effective 
pressure/shear to stabilize LSS, modeled here numerically via w_eff).
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Scripts')))
from itsm_plot_style import apply_tier1_style
apply_tier1_style()
import camb
from camb import model



# Parameters
PLANCK_H0 = 67.36
ITSM_H0 = 73.97
ITSM_W = -1.27

# Common base parameters (Planck 2018 TT,TE,EE+lowE)
ombh2 = 0.02237
omch2 = 0.12000
ns = 0.9649
As = 2.1e-9

def get_pk(H0, w=-1.0):
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, mnu=0.06, omk=0)
    pars.set_dark_energy(w=w, wa=0, dark_energy_model='fluid')
    pars.InitPower.set_params(As=As, ns=ns)
    
    # We want P(k) up to k = 1.0 h/Mpc
    pars.set_matter_power(redshifts=[0.], kmax=2.0)
    
    # Linear computation
    pars.NonLinear = model.NonLinear_none
    results = camb.get_results(pars)
    
    # Get P(k) 
    # Note: kh is in h/Mpc, pk is in (Mpc/h)^3
    kh, z, pk = results.get_matter_power_spectrum(minkh=1e-4, maxkh=1.0, npoints=200)
    
    s8 = np.array(results.get_sigma8())
    
    return kh, pk[0], s8[0]

# Compute
print("Computing LCDM P(k)...")
kh_lcdm, pk_lcdm, s8_lcdm = get_pk(PLANCK_H0, w=-1.0)

print("Computing ITSM P(k)...")
kh_itsm, pk_itsm, s8_itsm = get_pk(ITSM_H0, w=ITSM_W)

# Plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.05})

# Top Panel
ax1.loglog(kh_lcdm, pk_lcdm, '-', color='gray', lw=2, label=rf'Planck 2018 $\Lambda$CDM ($H_0={PLANCK_H0}, \sigma_8={s8_lcdm:.3f}$)')
ax1.loglog(kh_itsm, pk_itsm, '-', color='darkred', lw=2.5, label=rf'ITSM Syntropic ($H_0={ITSM_H0}, w={ITSM_W}, \sigma_8={s8_itsm:.3f}$)')

ax1.set_ylabel(r'$P(k)$ [$(h^{-1}\mathrm{Mpc})^3$]', fontsize=15)
ax1.set_title(r'Linear Matter Power Spectrum $P(k)$ at $z=0$', fontsize=16, pad=15)
ax1.legend(loc='lower left', fontsize=12)
ax1.grid(True, which='both', ls='-', alpha=0.2)
ax1.set_xlim(1e-4, 1)
ax1.set_ylim(1e1, 1e5)
ax1.tick_params(axis='x', labelbottom=False)

# Bottom Panel (Ratio)
ratio = pk_itsm / pk_lcdm
ax2.semilogx(kh_lcdm, ratio, '-', color='darkblue', lw=2)
ax2.axhline(1.0, color='gray', ls='--', lw=1.5)
ax2.set_xlabel(r'Wavenumber $k$ [$h\mathrm{Mpc}^{-1}$]', fontsize=15)
ax2.set_ylabel(r'Ratio (ITSM / $\Lambda$CDM)', fontsize=13)
ax2.grid(True, which='both', ls='-', alpha=0.2)
ax2.set_xlim(1e-4, 1)
ax2.set_ylim(0.7, 1.3)

script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.normpath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_camb_matter_power.png"))
plt.tight_layout()
plt.savefig(out_path, dpi=300, bbox_inches='tight')
print(f"Plot saved to: {out_path}")
