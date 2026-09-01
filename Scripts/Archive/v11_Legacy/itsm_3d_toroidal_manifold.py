"""
ITSM Diagnostic Script — 3D Toroidal Vortex Manifold
Renders a high-resolution 3D mathematical manifold of the T^3 topology,
overlaying the Syntropic Source Vector (Q^v) flow.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

# Torus parameters
R = 3.0  # Major radius
r = 1.0  # Minor radius

# Meshgrid for Torus surface
theta = np.linspace(0, 2.*np.pi, 50)
phi = np.linspace(0, 2.*np.pi, 50)
theta, phi = np.meshgrid(theta, phi)

X = (R + r * np.cos(phi)) * np.cos(theta)
Y = (R + r * np.cos(phi)) * np.sin(theta)
Z = r * np.sin(phi)

# Syntropic Source Vectors Q^v (Flow lines)
u = np.linspace(0, 2.*np.pi, 15)
v = np.linspace(0, 2.*np.pi, 15)
u, v = np.meshgrid(u, v)

# Vector origins on the surface
X_v = (R + r * np.cos(v)) * np.cos(u)
Y_v = (R + r * np.cos(v)) * np.sin(u)
Z_v = r * np.sin(v)

# Vector directions (Poloidal flow for Syntropy Intake)
# Poloidal means flow wraps around the minor radius
# dX/dv, dY/dv, dZ/dv
U_vec = -r * np.sin(v) * np.cos(u)
V_vec = -r * np.sin(v) * np.sin(u)
W_vec = r * np.cos(v)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the Toroidal Surface
ax.plot_surface(X, Y, Z, color='lightsteelblue', alpha=0.4, edgecolor='slategray', linewidth=0.5, rstride=2, cstride=2)

# Plot the Syntropic Flow Quivers
ax.quiver(X_v, Y_v, Z_v, U_vec, V_vec, W_vec, length=0.6, color='deepskyblue', linewidth=1.0, normalize=True, alpha=1.0, arrow_length_ratio=0.3)

# Aesthetics
ax.set_title(r"Topological Phase-Space: $T^3$ Toroidal Manifold & Syntropic Flow $Q^\nu$", pad=20)
ax.set_xlabel("X (Mpc)")
ax.set_ylabel("Y (Mpc)")
ax.set_zlabel("Z (Mpc)")

# Set limits for aspect ratio
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_zlim(-4, 4)
ax.view_init(elev=30, azim=45)

# Academic Peer-Review Aesthetics
ax.set_facecolor('white')
fig.patch.set_facecolor('white')
ax.grid(True, linestyle=':', alpha=0.6)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('black')
ax.yaxis.pane.set_edgecolor('black')
ax.zaxis.pane.set_edgecolor('black')

out_dir = os.path.join(repo_root, "Assets", "Figures")
os.makedirs(out_dir, exist_ok=True)
plt.savefig(os.path.join(out_dir, "itsm_3d_toroidal_manifold.png"), bbox_inches='tight', facecolor='white')
print("3D Toroidal Manifold generated successfully. Graphic exported.")
