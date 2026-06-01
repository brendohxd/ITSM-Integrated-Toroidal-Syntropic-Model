"""
Integrated Toroidal-Syntropic Model (ITSM) - Thermodynamic Decoupling
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Protocol: Visualization of Superfluid Plenum Phase Transition and CMB Acoustic Protection
Environment: Windows / Antigravity IDE Workspace Compatible
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Scripts')))
from itsm_plot_style import apply_tier1_style
apply_tier1_style()



def state_function(z, z_c=3400, lmbda=0.005):
    """
    Calculates the thermodynamic state function Xi(z) governing the 
    phase transition of the Superfluid Plenum.
    """
    # Clip to prevent overflow warnings at extreme limits
    exponent = np.clip(lmbda * (z - z_c), -500, 500)
    return 1.0 / (1.0 + np.exp(exponent))

def plot_decoupling():
    # Directory routing
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.abspath(os.path.join(script_dir, "..", "Assets"))
    figures_dir = os.path.join(assets_dir, "Figures")
    os.makedirs(figures_dir, exist_ok=True)

    # Redshift domain (from z=0 up to deep radiation era z=8000)
    z = np.linspace(0, 8000, 2000)
    z_c = 3400  # Matter-Radiation Equality / Critical Condensation
    xi_z = state_function(z, z_c=z_c, lmbda=0.004) # Lambda tuned for visual phase transition

    # Standard publication styling
    plt.figure(figsize=(10, 6))

    # Plot the main state function
    plt.plot(z, xi_z, color='navy', lw=3.0, label=r'ITSM State Function $\Xi(z)$')

    # Shade the thermodynamic eras
    plt.axvspan(z_c, 8000, color='crimson', alpha=0.1, label='Radiation-Dominated (Thermal Plasma)')
    plt.axvspan(0, z_c, color='navy', alpha=0.1, label='Matter-Dominated (Superfluid Condensate)')

    # Vertical constraint markers
    plt.axvline(z_c, color='crimson', linestyle='--', lw=2.5, label=rf'Critical Condensation ($z_c \approx {z_c}$)')
    plt.axvline(1100, color='darkorange', linestyle=':', lw=2.5, label=r'CMB Recombination ($z \approx 1100$)')

    # Typography and Grid Formatting
    plt.title(r'Superfluid Plenum Phase Transition: Thermodynamic Decoupling', fontsize=16, pad=15)
    plt.xlabel('Redshift ($z$)', fontsize=13)
    plt.ylabel(r'Acoustic Shear State Function $\Xi(z)$', fontsize=13)

    plt.xlim(0, 8000)
    plt.ylim(-0.05, 1.1)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='center right', frameon=True, fontsize=11)
    plt.tight_layout()

    # Output rendering
    fig_out_path = os.path.join(figures_dir, "itsm_thermodynamic_decoupling_publication.png")
    plt.savefig(fig_out_path, dpi=300)
    plt.close()
    
    print(f"ITSM SIMULATION COMPLETE: Thermodynamic Decoupling figure plotted at:\n -> {fig_out_path}")

if __name__ == "__main__":
    plot_decoupling()