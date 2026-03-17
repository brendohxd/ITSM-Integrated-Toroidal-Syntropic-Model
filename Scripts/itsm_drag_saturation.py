import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# ITSM Vector 7: Dimensional Scaffolding (Drag Saturation)
# Minimalist, publication-ready output
# ---------------------------------------------------------

x = np.linspace(0.1, 10, 500)

# The Models
linear_drag = x 
itsm_drag = (np.sqrt(1 + x**2) - 1) / x

plt.figure(figsize=(10, 6))
plt.style.use('dark_background')

# Plot the lines
plt.plot(x, linear_drag, '--', color='cyan', linewidth=2.5, label=r'Linear Drag (Exploding Viscosity)')
plt.plot(x, itsm_drag, '-', color='red', linewidth=3, label=r'ITSM Plenum Shear ($1/\sqrt{X}$ Decay)')

# Minimalist Boundary Markers
plt.axvline(1.0, color='white', linestyle=':', alpha=0.5)
plt.text(1.1, 4.6, r'$a_0$ Yield Threshold', color='white', fontsize=12)

plt.axvspan(5, 10, color='grey', alpha=0.15)
plt.text(7.5, 4.6, r'Cassini Limit ($X \gg a_0$)', color='white', horizontalalignment='center', fontsize=12)

# Clean Axes and Legend
plt.xlabel(r'Kinetic Energy Ratio ($X / a_0$)', fontsize=14)
plt.ylabel(r'Relative Fractional Drag ($\mathcal{L}_{int} / X$)', fontsize=14)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlim(0, 10)
plt.ylim(0, 5)

# Place legend where it doesn't obstruct the crossing point
plt.legend(loc='center left', bbox_to_anchor=(0.02, 0.65), framealpha=0.1, fontsize=12)
plt.grid(True, linestyle=':', alpha=0.2)

plt.tight_layout()
plt.savefig('itsm_drag_saturation.png', dpi=300)
plt.show()
