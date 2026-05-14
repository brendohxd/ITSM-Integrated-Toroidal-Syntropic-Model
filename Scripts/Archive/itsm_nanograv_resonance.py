"""
ITSM Computational Falsifiability Suite
Module: NANOGrav Acoustic Resonance Matrix
Framework Version: 8.06 

Description:
Computes the Strain Power Spectral Density (PSD) for the stochastic 
gravitational wave background. Models the ITSM acoustic resonance 
strictly bounded by the geometric yield threshold (a_0 = 1.08 nHz) 
and the toroidal harmonic (chi = 2*pi = 3.14 nHz).
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

# ---------------------------------------------------------
# INSTITUTIONAL AESTHETIC PROTOCOL (LATEX ENFORCEMENT)
# ---------------------------------------------------------
mpl.rcParams.update({
    'font.family': 'serif',
    'mathtext.fontset': 'cm', # Computer Modern (LaTeX standard)
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'axes.titleweight': 'bold',
    'legend.fontsize': 11,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'figure.dpi': 300,
    'savefig.bbox': 'tight',
    'figure.facecolor': '#0d0d0d',
    'axes.facecolor': '#0d0d0d',
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'axes.edgecolor': '#2a2a2a'
})

# ---------------------------------------------------------
# PHYSICAL CONSTANTS & MODEL PARAMETERS (v8.06 AXIOMS)
# ---------------------------------------------------------
FREQ_MIN_NHZ = 0.1
FREQ_MAX_NHZ = 100.0
POINTS = 1000

# Lambda-CDM Stochastic Background (SMBHB Power Law)
A_GWB_NANOGRAV = 2.4e-15  # 15-yr Amplitude
F_YR_NHZ = 31.7           # 1/year frequency

# ITSM Toroidal Acoustic Boundaries
A0_BASE_NHZ = 1.08        # Normalized geometric yield threshold
PI_HARMONIC_NHZ = np.pi   # Toroidal boundary chi/2
F_RES_CENTROID = (A0_BASE_NHZ + PI_HARMONIC_NHZ) / 2
RESONANCE_WIDTH = 0.5
RESONANCE_AMP = 1.5e-14

# ---------------------------------------------------------
# COMPUTATIONAL ENGINE
# ---------------------------------------------------------
def compute_strain_psd():
    """Calculates characteristic strain for standard and ITSM models."""
    freqs = np.logspace(np.log10(FREQ_MIN_NHZ), np.log10(FREQ_MAX_NHZ), POINTS)
    
    # Lambda-CDM: Structureless Power Law
    h_lcdm = A_GWB_NANOGRAV * (freqs / F_YR_NHZ)**(-2/3)
    
    # ITSM: Macroscopic Plenum Resonance (Lorentzian profile)
    resonance = RESONANCE_AMP * (RESONANCE_WIDTH**2 / ((freqs - F_RES_CENTROID)**2 + RESONANCE_WIDTH**2))
    h_itsm = h_lcdm + resonance
    
    return freqs, h_lcdm, h_itsm

# ---------------------------------------------------------
# VISUALIZATION MATRIX
# ---------------------------------------------------------
def generate_institutional_plot(freqs, h_lcdm, h_itsm):
    """Renders the publication-grade log-log plot."""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    ax.set_xscale('log')
    ax.set_yscale('log')

    # Data Traces
    ax.plot(freqs, h_lcdm, color='#ff6347', lw=2, ls='--', alpha=0.9, 
            label=r'$\Lambda$CDM: Featureless Power Law ($f^{-2/3}$)')
    ax.plot(freqs, h_itsm, color='#00ffff', lw=3, 
            label='ITSM: Toroidal Acoustic Resonance')

    # Uncertainty / Bayesian Envelopes
    ax.fill_between(freqs, h_lcdm * 0.5, h_lcdm * 1.5, color='#ff6347', alpha=0.1)
    ax.fill_between(freqs, h_itsm * 0.7, h_itsm * 1.3, color='#00ffff', alpha=0.1)

    # V8.06 Falsifiability Boundaries
    ax.axvspan(A0_BASE_NHZ, PI_HARMONIC_NHZ, color='white', alpha=0.08, 
               label=r'ITSM Falsifiability Window ($a_0$ to $\pi$)')
    ax.axvline(A0_BASE_NHZ, color='white', ls=':', alpha=0.4)
    ax.axvline(PI_HARMONIC_NHZ, color='white', ls=':', alpha=0.4)

    # Grid and Limits
    ax.set_xlim(0.5, 100)
    ax.set_ylim(1e-16, 1e-13)
    ax.grid(True, which='both', color='#2a2a2a', linestyle=':', alpha=0.6)

    # Axis Labels
    ax.set_xlabel(r'Gravitational Wave Frequency $f$ [nHz]')
    ax.set_ylabel(r'Characteristic Strain $h_c(f)$')
    
    # Legend
    ax.legend(loc='lower left', frameon=True, facecolor='#1a1a1a', edgecolor='#2a2a2a')

    # Export
    os.makedirs('Assets', exist_ok=True)
    out_path = 'Assets/itsm_nanograv_resonance_v806.png'
    plt.savefig(out_path)
    print(f"High-Fidelity Matrix saved to: {out_path}")
    plt.show()

# ---------------------------------------------------------
# EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    freq_data, lcdm_data, itsm_data = compute_strain_psd()
    generate_institutional_plot(freq_data, lcdm_data, itsm_data)
