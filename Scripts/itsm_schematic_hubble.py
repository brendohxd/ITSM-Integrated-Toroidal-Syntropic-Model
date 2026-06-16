import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from itsm_plot_style import apply_tier1_style
apply_tier1_style()

plt.rcParams.update({
    'font.size': 18,
    'axes.labelsize': 18,
    'axes.titlesize': 20,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'legend.fontsize': 14,
    'figure.titlesize': 24
})

fig, ax = plt.subplots(figsize=(10, 8))

# Draw concentric circles
theta = np.linspace(0, 2*np.pi, 200)
r_p = 1.0
r_t = 13.0/12.0

ax.plot(r_p*np.cos(theta), r_p*np.sin(theta), 'b--', lw=3, label=r'Global Expansion ($H_p \approx 67.4$)')
ax.plot(r_t*np.cos(theta), r_t*np.sin(theta), 'r-', lw=3, label=r'Local Expansion ($H_t \approx 73.0$)')

# Fill area between them
# We can't use fill_between easily in polar with plot unless we use ax.fill
ax.fill(np.concatenate([r_t*np.cos(theta), r_p*np.cos(theta)[::-1]]),
        np.concatenate([r_t*np.sin(theta), r_p*np.sin(theta)[::-1]]), color='red', alpha=0.1)

# Add outward arrows
for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
    ax.arrow(0, 0, 0.9*np.cos(angle), 0.9*np.sin(angle), head_width=0.05, head_length=0.1, fc='blue', ec='blue', alpha=0.6)
    
for angle in np.linspace(np.pi/8, 2*np.pi+np.pi/8, 8, endpoint=False):
    ax.arrow(0, 0, (r_t-0.1)*np.cos(angle), (r_t-0.1)*np.sin(angle), head_width=0.05, head_length=0.1, fc='red', ec='red', alpha=0.8)

ax.text(0, 0, r'Planck CMB Anchor', ha='center', va='center', fontsize=16, bbox=dict(facecolor='white', alpha=0.8, edgecolor='blue'))
ax.text(0, 1.15, r'Casimir Stress Anisotropy ($\frac{13}{12}$ factor)', color='darkred', fontsize=16, fontweight='bold', ha='center', va='center', rotation=0, bbox=dict(facecolor='white', alpha=0.9, edgecolor='none'))

ax.set_aspect('equal')
ax.axis('off')

ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.05))
plt.title(r'Hubble Tension Resolution via $T^3$ Casimir Anisotropy', pad=20)

script_dir = os.path.dirname(os.path.abspath(__file__))
out_pdf = os.path.normpath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_hubble_tension_schematic.pdf"))
out_png = os.path.normpath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_hubble_tension_schematic.png"))

plt.savefig(out_pdf, bbox_inches='tight', format='pdf', dpi=300)
plt.savefig(out_png, bbox_inches='tight', dpi=300)

print(f"Generated {out_pdf}")
