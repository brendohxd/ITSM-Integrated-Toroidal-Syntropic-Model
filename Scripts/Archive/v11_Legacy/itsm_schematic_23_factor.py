import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from itsm_plot_style import apply_tier1_style
apply_tier1_style()

# JCAP font overrides
plt.rcParams.update({
    'font.size': 18,
    'axes.labelsize': 18,
    'axes.titlesize': 20,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'legend.fontsize': 14,
    'figure.titlesize': 24
})

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Draw a 2D shear plane (z=0)
xx, yy = np.meshgrid(np.linspace(-2, 2, 10), np.linspace(-2, 2, 10))
zz = np.zeros_like(xx)
ax.plot_surface(xx, yy, zz, alpha=0.2, color='steelblue', edgecolor='none')

# Draw the 3D isotropic bulk sphere (representing 3 DOF)
u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax.plot_wireframe(x, y, z, color='gray', alpha=0.3, linewidth=0.5)

# Highlight the 2D equatorial circle (projection onto the shear plane)
theta = np.linspace(0, 2*np.pi, 100)
ax.plot(np.cos(theta), np.sin(theta), 0, color='darkred', linewidth=3, label=r'2D Shear Plane Projection (2 DOF)')

# Vectors showing projection
ax.quiver(0, 0, 0, 1, 1, 1, color='black', linewidth=2, arrow_length_ratio=0.1)
ax.quiver(0, 0, 0, 1, 1, 0, color='darkred', linewidth=2, arrow_length_ratio=0.1)
ax.plot([1, 1], [1, 1], [0, 1], 'k--', alpha=0.5)

ax.text(1.1, 1.1, 1.1, r'$\vec{v}_{\mathrm{bulk}}$ (3D)', fontsize=16)
ax.text(1.1, 1.1, -0.2, r'$\vec{v}_{\mathrm{shear}}$ (2D)', color='darkred', fontsize=16)

# Add formulas
ax.text2D(0.05, 0.90, r"$\mathbf{Topological\ Projection\ Factor}$", transform=ax.transAxes, fontsize=18, fontweight='bold')
ax.text2D(0.05, 0.82, r"$C_{\mathrm{proj}} = \frac{\mathrm{Tr}(P_{2D})}{\mathrm{Tr}(I_{3D})} = \frac{2}{3}$", transform=ax.transAxes, fontsize=20)
ax.text2D(0.05, 0.74, r"Vacuum drag acts strictly within the", transform=ax.transAxes, fontsize=14)
ax.text2D(0.05, 0.69, r"2D transverse shear plane of the plenum.", transform=ax.transAxes, fontsize=14)

ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.set_zlim([-1.5, 1.5])

ax.set_axis_off()

# Save
script_dir = os.path.dirname(os.path.abspath(__file__))
out_pdf = os.path.normpath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_23_factor_schematic.pdf"))
out_png = os.path.normpath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_23_factor_schematic.png"))

plt.savefig(out_pdf, bbox_inches='tight', format='pdf', dpi=300)
plt.savefig(out_png, bbox_inches='tight', dpi=300)

print(f"Generated {out_pdf}")
