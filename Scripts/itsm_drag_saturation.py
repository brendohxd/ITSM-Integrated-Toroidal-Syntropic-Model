"""
Integrated Toroidal-Syntropic Model (ITSM) - Covariant Stability (Drag Saturation)
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



X_ratio = np.logspace(-2, 8, 1000)
linear_drag = X_ratio
itsm_drag = (2/3) * (np.sqrt(1 + X_ratio) - 1) / X_ratio

plt.figure(figsize=(10, 6))

plt.plot(X_ratio, linear_drag, '--', color='gray', linewidth=2.5, label=r'Linear Modification ($\mathcal{L}_{int} \propto X^2$)')
plt.plot(X_ratio, itsm_drag, '-', color='darkred', linewidth=3, label=r'ITSM Plenum Shear Ansatz ($\propto 1/\sqrt{X}$)')

plt.axvspan(1e5, 1e8, color='gray', alpha=0.2, label=r'Cassini PPN Constraint Zone')
plt.axvline(x=1.0, color='black', linestyle=':', label=r'Critical Yield Boundary ($X=a_0^2$)')

plt.xscale('log'); plt.yscale('log')
plt.xlim(1e-2, 1e8); plt.ylim(1e-5, 1e4)

plt.title(r'Covariant Stability: Macroscopic Vacuum Drag', fontsize=16, pad=15)
plt.xlabel(r'Dimensionless Kinetic Energy Ratio ($X/a_0^2$)', fontsize=14)
plt.ylabel(r'Relative Interaction Strength ($\mathcal{L}_{int}/X$)', fontsize=14)

plt.legend(loc='upper right', framealpha=0.9, fontsize=12)
plt.grid(True, which="both", ls=":", alpha=0.6)

plt.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_drag_saturation_publication.png"))
plt.savefig(out_path, dpi=300)
print(f"Asset generated: {out_path}")