
import numpy as np
import matplotlib.pyplot as plt

# ====================== v8.2 PARAMETERS ======================
a0 = 1.33e-10                    # NEW multiplier: 2π c H0 (m/s²)

# Dimensionless kinetic energy ratio X/a0 (log-spaced for smooth curve)
ratio = np.logspace(-2, 8, 1000)   # X/a0 from 0.01 to 1e8

# 1. Linear modification (explodes at high X) - cyan
linear = ratio                     # L_int/X ∝ X  → grows unbounded

# 2. ITSM Plenum Shear Ansatz (decays as 1/√X) - red
# From the saturating form: L_int = (2/3) a0 (√(1 + X/a0) - 1)
# Relative strength = L_int / X
itms = (2/3) * (np.sqrt(1 + ratio) - 1) / ratio

# ==================== PUBLICATION-QUALITY PLOT ====================
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 11,
    'lines.linewidth': 2.8,
    'axes.linewidth': 1.2
})

plt.figure(figsize=(8.5, 6))

# Linear (exploding) - cyan
plt.plot(ratio, linear, '--', color='#00b4d8', linewidth=2.5, label='Linear Modification (L ∝ X²)')

# ITSM Plenum Shear Ansatz - red
plt.plot(ratio, itms, '-', color='#e63946', linewidth=3.0, label='ITSM Plenum Shear Ansatz (1/√X decay)')

# Cassini / Solar System high-acceleration regime
plt.axvline(x=1e4, color='black', linestyle=':', linewidth=1.5, label='Cassini PPN Constraint Zone')

# Labels and formatting
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'Dimensionless Kinetic Energy Ratio $X/a_0$')
plt.ylabel(r'Relative Interaction Strength $\mathcal{L}_{\rm int}/X$')
plt.title('Relative Interaction Strength – Linear vs. ITSM Plenum Shear Ansatz\n'
          r'(v8.2 Toroidal Multiplier $a_0 = 2\pi c H_0$)', pad=15)
plt.legend(loc='upper left')
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.ylim(1e-4, 1e2)

plt.tight_layout()

# Save high-resolution version for LaTeX
plt.savefig('itms_drag_saturation_v8.2.png', dpi=600, bbox_inches='tight')
plt.show()

print("✅ Fig. 1 saved as itms_drag_saturation_v8.2.png (600 dpi, publication quality)")    # Grid and Labels
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
