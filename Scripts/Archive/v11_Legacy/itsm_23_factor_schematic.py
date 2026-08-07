import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform
import os
import sys

from itsm_plot_style import apply_tier1_style
apply_tier1_style()

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        return np.min(zs)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Draw the 3D isotropic bulk (sphere)
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))

ax.plot_surface(x, y, z, color='lightblue', alpha=0.1, edgecolor='none')
ax.plot_wireframe(x, y, z, color='blue', alpha=0.05, linewidth=0.5)

# Draw the 2D shear plane (disk)
r = np.linspace(0, 1, 50)
theta = np.linspace(0, 2 * np.pi, 50)
R, Theta = np.meshgrid(r, theta)
X = R * np.cos(Theta)
Y = R * np.sin(Theta)
Z = np.zeros_like(X)

ax.plot_surface(X, Y, Z, color='navy', alpha=0.4, edgecolor='none')
ax.plot_wireframe(X, Y, Z, color='darkblue', alpha=0.2, linewidth=0.5)

# Add vectors
ax.add_artist(Arrow3D([0, 1.2], [0, 0], [0, 0], mutation_scale=15, lw=2, arrowstyle="-|>", color="red"))
ax.add_artist(Arrow3D([0, 0], [0, 1.2], [0, 0], mutation_scale=15, lw=2, arrowstyle="-|>", color="red"))
ax.add_artist(Arrow3D([0, 0], [0, 0], [0, 1.2], mutation_scale=15, lw=2, arrowstyle="-|>", color="grey", linestyle='dashed'))

# Text labels
ax.text(1.3, 0, 0, "X (Toroidal)", color='red', fontsize=12, fontweight='bold')
ax.text(0, 1.3, 0, "Y (Toroidal)", color='red', fontsize=12, fontweight='bold')
ax.text(0, 0, 1.3, "Z (Poloidal)", color='grey', fontsize=12)

# Informational text
ax.text2D(0.05, 0.95, "3D Bulk Isotropic Space (3 degrees of freedom)", transform=ax.transAxes, fontsize=12, color='darkblue', fontweight='bold')
ax.text2D(0.05, 0.90, "2D Acoustic Shear Plane (2 degrees of freedom)", transform=ax.transAxes, fontsize=12, color='red', fontweight='bold')
ax.text2D(0.05, 0.85, "Geometric Projection Factor: 2/3", transform=ax.transAxes, fontsize=14, color='black', fontweight='bold')

ax.set_xlim([-1.2, 1.2])
ax.set_ylim([-1.2, 1.2])
ax.set_zlim([-1.2, 1.2])
ax.axis('off')

script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_23_factor_schematic.png"))
plt.savefig(out_path, dpi=300, bbox_inches='tight')
print(f"Saved {out_path}")
