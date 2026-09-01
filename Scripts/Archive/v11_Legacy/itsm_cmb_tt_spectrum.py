"""
Software Dependencies & Attributions:
This script utilizes a modified version of the CAMB Boltzmann solver.
Original Source: Lewis, A., Challinor, A., & Lasenby, A. (2000). Efficient computation of CMB anisotropies in closed FRW models. The Astrophysical Journal, 538(2), 473.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import camb
from camb import model, initialpower

# Ensure the plots match the paper's style
plt.style.use('seaborn-v0_8-darkgrid')

def run_camb(w_eff, H0=67.36, lmax=2500):
    """
    Run the custom natively-integrated CAMB solver for a given effective w and H0.
    w_eff = -1.0 for Lambda-CDM
    w_eff = -1.27 for ITSM (triggering the a^4.81 integration)
    """
    pars = camb.CAMBparams()
    
    # Set standard cosmological parameters. We keep the physical densities ombh2 and omch2 
    # fixed to Planck 2018 values because they are determined by early universe physics.
    # Changing H0 will automatically adjust the fractional density Omega_Lambda to keep flat.
    pars.set_cosmology(H0=H0, ombh2=0.02237, omch2=0.1200, mnu=0.06, omk=0, tau=0.0544)
    
    # Set dark energy properties natively via w
    pars.set_dark_energy(w=w_eff, wa=0, dark_energy_model='ppf')
    
    # Set initial power spectrum parameters
    pars.InitPower.set_params(As=2.1e-9, ns=0.9649, r=0)
    
    # Set accuracies and lmax
    pars.set_for_lmax(lmax, lens_potential_accuracy=1)
    
    # Calculate results
    results = camb.get_results(pars)
    
    # Get CMB power spectra in muK^2
    powers = results.get_cmb_power_spectra(pars, CMB_unit='muK')
    
    # Return the unlensed total spectrum
    return powers['total']

def main():
    print("Initializing CMB TT Spectrum comparison...")
    
    # 1. Run CAMB for both models
    lmax = 2500
    print("Running CAMB for Lambda-CDM with w = -1.0, H0 = 67.36...")
    totcl_lcdm = run_camb(w_eff=-1.0, H0=67.36, lmax=lmax)
    
    print("Running CAMB for ITSM with w = -1.27, H0 = 72.97 (Geometric Prediction)...")
    totcl_itsm = run_camb(w_eff=-1.27, H0=72.97, lmax=lmax)
    
    # Extract TT spectra (first column) and corresponding l values
    # CAMB arrays are indexed by l, from 0 to lmax
    ls_camb = np.arange(totcl_lcdm.shape[0])
    dl_tt_lcdm = totcl_lcdm[:, 0]
    dl_tt_itsm = totcl_itsm[:, 0]
    
    # 2. Load Planck PR3 Data
    print("Loading Planck PR3 2018 binned TT data...")
    planck_file = os.path.join("Data", "Planck_data", "COM_PowerSpect_CMB-TT-binned_R3.01.txt")
    if not os.path.exists(planck_file):
        print(f"Error: Planck data file not found at {planck_file}")
        sys.exit(1)
        
    planck_data = np.loadtxt(planck_file)
    l_planck = planck_data[:, 0]
    dl_planck = planck_data[:, 1]
    err_down = planck_data[:, 2]
    err_up = planck_data[:, 3]
    
    # 3. Compute Residuals (Theory - Data)
    # We interpolate the theoretical models onto the exact effective l bins of Planck
    dl_lcdm_interp = np.interp(l_planck, ls_camb, dl_tt_lcdm)
    dl_itsm_interp = np.interp(l_planck, ls_camb, dl_tt_itsm)
    
    res_lcdm = dl_lcdm_interp - dl_planck
    res_itsm = dl_itsm_interp - dl_planck
    
    # Average errors for residual plot normalization if needed, but plotting raw Delta Dl is standard
    err_avg = (err_down + err_up) / 2.0
    
    # Calculate chi-squared values
    chi2_lcdm = np.sum((res_lcdm / err_avg)**2)
    chi2_itsm = np.sum((res_itsm / err_avg)**2)
    dof = len(l_planck)
    print(f"Lambda-CDM Chi-Squared: {chi2_lcdm:.2f} / {dof} dof")
    print(f"ITSM Chi-Squared: {chi2_itsm:.2f} / {dof} dof")
    
    # 4. Plotting
    print("Generating figures...")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    fig.subplots_adjust(hspace=0.05)
    
    # Top Panel: Absolute Spectra
    ax1.plot(ls_camb, dl_tt_lcdm, color='gray', linestyle='--', linewidth=2, label=rf'$\Lambda$CDM ($w=-1.0, \chi^2_\nu={chi2_lcdm/dof:.1f}$)')
    ax1.plot(ls_camb, dl_tt_itsm, color='#d62728', linestyle='-', linewidth=2, label=rf'ITSM ($w_{{eff}}=-1.27, \chi^2_\nu={chi2_itsm/dof:.1f}$)')

    
    ax1.errorbar(l_planck, dl_planck, yerr=[err_down, err_up], fmt='.', color='black',
                 markersize=4, elinewidth=1, capsize=2, label='Planck 2018 (PR3) Binned')
    
    ax1.set_ylabel(r'$\mathcal{D}_\ell^{TT} = \ell(\ell+1)C_\ell^{TT} / 2\pi \quad [\mu K^2]$', fontsize=14)
    ax1.set_title('Cosmic Microwave Background Temperature Power Spectrum', fontsize=16)
    ax1.set_xlim(2, 2500)
    ax1.set_ylim(0, 6500)
    ax1.legend(loc='upper right', fontsize=12)
    
    # Bottom Panel: Residuals
    ax2.axhline(0, color='black', linewidth=1, linestyle='-')
    ax2.errorbar(l_planck, np.zeros_like(l_planck), yerr=[err_down, err_up], fmt='none', color='black', alpha=0.3)
    
    ax2.plot(l_planck, res_lcdm, color='gray', linestyle='--', linewidth=1.5, marker='o', markersize=3, label=r'$\Lambda$CDM Residual')
    ax2.plot(l_planck, res_itsm, color='#d62728', linestyle='-', linewidth=1.5, marker='o', markersize=3, label=r'ITSM Residual')
    
    ax2.set_xlabel(r'Multipole moment $\ell$', fontsize=14)
    ax2.set_ylabel(r'$\Delta \mathcal{D}_\ell^{TT} \quad [\mu K^2]$', fontsize=14)
    ax2.set_ylim(-150, 150)
    ax2.legend(loc='lower left', fontsize=10)
    
    plt.tight_layout()
    output_path = 'itsm_cmb_tt_spectrum.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {os.path.abspath(output_path)}")
    plt.close()

if __name__ == '__main__':
    main()
