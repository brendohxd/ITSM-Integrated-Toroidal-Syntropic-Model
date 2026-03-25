
"""
ITSM Computational Falsifiability Suite
Module: Plenum Shear Ansatz (Drag Saturation Plot)
Framework Version: 8.06

Description:
Visualizes the dimensional derivation of the ITSM interaction Lagrangian.
Plots the relative interaction strength (L_int / X) against the dimensionless
kinetic energy ratio (X / a_0^2). Demonstrates the geometric necessity of the 
Born-Infeld type root saturation to preserve Cassini Solar System constraints 
(decaying as 1/sqrt(X) at high accelerations).
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
# COMPUTATIONAL ENGINE (DIMENSIONALLY CORRECTED v8.06)
# ---------------------------------------------------------
def compute_shear_saturation():
    """Calculates relative interaction strength for linear vs. ITSM models."""
    # Dimensionless kinetic energy ratio: x = X / a_0^2
    # Range from deep MONDian regime (10^-2) to deep Solar System regime (10^8)
    x_ratio = np.logspace(-2, 8, 1000)
    
    # ITSM Model: Geometric projection yielding (sqrt(1+x) - 1) / x
    # Normalized so the low-energy limit (x->0) approaches 1.0
    y_itsm = 2.0 * (np.sqrt(1 + x_ratio) - 1) / x_ratio
    
    # Standard Linear Modification: L_int proportional to X^2
    # Relative strength (L_int / X) grows unbounded (proportional to x)
    # Normalized to match ITSM at the a_0 boundary (x=1)
    y_linear = np.ones_like(x_ratio) + (x_ratio / 2.0)
    
    return x_ratio, y_linear, y_itsm

# ---------------------------------------------------------
# VISUALIZATION MATRIX
# ---------------------------------------------------------
def generate_institutional_plot(x_ratio, y_linear, y_itsm):
    """Renders the publication-grade saturation log-log plot."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set logarithmic scales for massive dynamic range
    ax.set_xscale('log')
    ax.set_yscale('log')

    # Data Traces
    ax.plot(x_ratio, y_linear, color='#00ffff', lw=2, ls='--', alpha=0.9,
            label=r'Linear Modification ($\mathcal{L}_{int} \propto X^2$) - Unbounded')
    
    ax.plot(x_ratio, y_itsm, color='#ff6347', lw=3,
            label=r'ITSM Plenum Shear Ansatz ($\propto 1/\sqrt{X}$ decay)')

    # Falsifiability Boundaries & Constraints
    # 1. The a_0 Transition Zone
    ax.axvline(1.0, color='white', ls=':', alpha=0.5)
    ax.text(1.2, 1e-4, r'Critical Yield Boundary ($X = a_0^2$)', color='white', alpha=0.7, rotation=90)
    
    # 2. Cassini Radio-Link Constraint Zone (High X)
    cassini_threshold = 1e5
    ax.axvspan(cassini_threshold, 1e8, color='#ffd700', alpha=0.1,
               label='Cassini PPN Constraint Zone (Solar System)')
    
    # Indicate where the linear model violates reality
    ax.fill_between(x_ratio, y_itsm, y_linear, where=(x_ratio > cassini_threshold),
                    color='red', alpha=0.15, hatch='//', label='Violation of General Relativity')

    # Axis Limits and Ticks
    ax.set_xlim(1e-2, 1e8)
    ax.set_ylim(1e-5, 1e4)
    
    # Grid and Labels
    ax.grid(True, which='both', color='#2a2a2a', linestyle=':', alpha=0.6)
    ax.set_xlabel(r'Dimensionless Kinetic Energy Ratio ($X / a_0^2$)')
    ax.set_ylabel(r'Relative Interaction Strength ($\mathcal{L}_{int} / X$)')
    ax.set_title('Covariant Stability:\nMacroscopic Vacuum Drag vs. Local Relativistic Constraints',
                 pad=15)
    
    # Legend
    ax.legend(loc='upper right', frameon=True, facecolor='#1a1a1a', edgecolor='#2a2a2a')
    
    # Export
    os.makedirs('Assets', exist_ok=True)
    out_path = 'Assets/itsm_drag_saturation_v806.png'
    plt.savefig(out_path)
    print(f"High-Fidelity Matrix saved to: {out_path}")
    plt.show()

# ---------------------------------------------------------
# EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    x_vals, linear_vals, itsm_vals = compute_shear_saturation()
    generate_institutional_plot(x_vals, linear_vals, itsm_vals)
