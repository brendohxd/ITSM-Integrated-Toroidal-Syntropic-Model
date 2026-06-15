import os
import sys

# Add build directory to path for local classy import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'build', 'lib.win-amd64-cpython-313')))

# Ensure compiler path is added for DLL load on Windows
if sys.platform == 'win32':
    for path in os.environ.get('PATH', '').split(';'):
        if os.path.isdir(path):
            if os.path.exists(os.path.join(path, 'g++.exe')) or os.path.exists(os.path.join(path, 'gcc.exe')) or os.path.exists(os.path.join(path, 'libstdc++-6.dll')):
                try:
                    os.add_dll_directory(path)
                except Exception:
                    pass

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from classy import Class

def compute_models():
    # 1. Standard Lambda-CDM
    print("Computing Lambda-CDM...")
    lcdm = Class()
    lcdm.set({
        'H0': 67.36,
        'Omega_b': 0.0493,
        'Omega_cdm': 0.2644,
        'output': 'tCl,pCl,lCl,mPk',
        'l_max_scalars': 2500,
        'P_k_max_1/Mpc': 10.0,
        'z_max_pk': 1.0
    })
    lcdm.compute()
    
    # 2. ITSM Engine
    print("Computing ITSM...")
    itsm = Class()
    itsm.set({
        'H0': 73.97,
        'Omega_b': 0.048,
        'Omega_cdm': 0.192,
        'Omega_fld': 0.760,
        'fluid_equation_of_state': 'ITSM',
        'itsm_n0': 3.0,
        'itsm_na': 0.0,
        'use_ppf': 'yes',
        'output': 'tCl,pCl,lCl,mPk',
        'l_max_scalars': 2500,
        'P_k_max_1/Mpc': 10.0,
        'z_max_pk': 1.0
    })
    itsm.compute()
    
    return lcdm, itsm

def main():
    lcdm, itsm = compute_models()
    
    # CMB Power Spectrum
    cl_lcdm = lcdm.raw_cl(2500)
    cl_itsm = itsm.raw_cl(2500)
    
    ell = cl_itsm['ell']
    # CLASS returns l*(l+1)*C_l/2pi in units of (1e6 * T_cmb)^2 = muK^2 (if T_cmb is set) or dimensionless.
    # In classy, lensed_cl returns Cls with factor l*(l+1)/(2*pi) already included.
    cl_tt_lcdm = cl_lcdm['tt']
    cl_tt_itsm = cl_itsm['tt']
    
    # Matter Power Spectrum P(k)
    # k in h/Mpc
    kh = np.logspace(-4, 0, 200)
    
    h_lcdm = 67.36 / 100.0
    h_itsm = 73.97 / 100.0
    
    pk_lcdm = []
    pk_itsm = []
    
    for k in kh:
        # CLASS expects k in Mpc^-1, returns P(k) in Mpc^3
        # We convert kh (h/Mpc) -> k (Mpc^-1)
        # Then convert P(k) (Mpc^3) -> P(kh) ((Mpc/h)^3) by multiplying by h^3
        try:
            p_l = lcdm.pk(k * h_lcdm, 0.0) * (h_lcdm ** 3)
        except Exception:
            p_l = 0.0
        try:
            p_i = itsm.pk(k * h_itsm, 0.0) * (h_itsm ** 3)
        except Exception:
            p_i = 0.0
        pk_lcdm.append(p_l)
        pk_itsm.append(p_i)
        
    pk_lcdm = np.array(pk_lcdm)
    pk_itsm = np.array(pk_itsm)
    
    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
    
    # Left Panel: CMB Power Spectrum
    # Filter for ell >= 2
    mask = ell >= 2
    # CLASS Cls are in units of 1e10 * C_l or muK^2 depending on scaling.
    # Usually l*(l+1)*C_l/2pi is plotted.
    # We plot the raw returned values
    ax1.plot(ell[mask], cl_tt_lcdm[mask] * 1e10, '-', color='gray', label='Standard $\\Lambda$CDM', lw=2)
    ax1.plot(ell[mask], cl_tt_itsm[mask] * 1e10, '-', color='darkred', label='Modified ITSM Engine', lw=2)
    ax1.set_xlabel('Multipole $\\ell$', fontsize=12)
    ax1.set_ylabel('$D_\\ell^{TT} \\times 10^{10}$', fontsize=12)
    ax1.set_title('CMB Temperature Power Spectrum', fontsize=13)
    ax1.legend(fontsize=10)
    ax1.grid(True, which='both', ls=':', alpha=0.5)
    ax1.set_xlim(2, 2500)
    
    # Right Panel: Matter Power Spectrum
    ax2.loglog(kh, pk_lcdm, '-', color='gray', label='Standard $\\Lambda$CDM', lw=2)
    ax2.loglog(kh, pk_itsm, '-', color='darkred', label='Modified ITSM Engine', lw=2)
    ax2.set_xlabel('Wavenumber $k$ [$h\\mathrm{Mpc}^{-1}$]', fontsize=12)
    ax2.set_ylabel('$P(k)$ [$(h^{-1}\\mathrm{Mpc})^3$]', fontsize=12)
    ax2.set_title('Matter Power Spectrum (z=0)', fontsize=13)
    ax2.legend(fontsize=10)
    ax2.grid(True, which='both', ls=':', alpha=0.5)
    ax2.set_xlim(1e-4, 1.0)
    ax2.set_ylim(1e0, 1e5)
    
    plt.suptitle('Cosmological Spectra: Standard $\\Lambda$CDM vs Modified ITSM CLASS Engine', fontsize=15, y=0.98)
    plt.tight_layout()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, "itsm_class_spectra.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Spectra plot saved successfully to: {out_path}")

if __name__ == '__main__':
    main()
