"""
Integrated Toroidal-Syntropic Model (ITSM) - Dual-Panel Fluid Dynamics
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework
Environment: Windows / Antigravity IDE Workspace Compatible
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
import os

# Set up dark-theme compatible LaTeX rendering
plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath} \usepackage{xcolor}",
    "font.family": "serif",
    "font.size": 13,
    "text.color": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "axes.edgecolor": "white"
})

# 1. Normalized Grid Setup (r / r_a0)
# High resolution for rendering
x = np.linspace(-3.5, 7.5, 500)
y = np.linspace(-4.5, 4.5, 500)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
Theta = np.arctan2(Y, X)

# Kinematic Yield Boundary Radius
R_yield = 1.0

# 2. Metric Perturbation Density (The Wake)
wake_mask = (X > R_yield)
X_safe_envelope = np.clip(X, R_yield, None)
wake_envelope = np.exp(-(Y**2) / (0.4 + 0.3 * X_safe_envelope)) * np.exp(-(X_safe_envelope - R_yield) / 6.0)

# Smoother fluid-like Phonon oscillations
k_phonon = 4.0
wake_oscillation = (0.5 * np.cos(k_phonon * np.sqrt((X - R_yield)**2 + Y**2)) + 0.5)

base_stress = 0.05 * np.exp(-R / 2.0)
metric_density = base_stress.copy()
metric_density[wake_mask] += (wake_envelope * wake_oscillation * 0.4)[wake_mask]

# 3. Superfluid Kinematic Vector Field (Streamlines)
U_inf = 1.0
R_safe = np.where(R < 0.05, 0.05, R)
# Ideal flow around the yield boundary
u = U_inf * (1 - (R_yield**2 / R_safe**2) * np.cos(2*Theta))
v = U_inf * (-(R_yield**2 / R_safe**2) * np.sin(2*Theta))

# 4. Dual-Panel Visualization Architecture
fig = plt.figure(figsize=(22, 10), facecolor='#0d1117')

# Custom Colormap
colors_array = ['#020205', '#0a1532', '#005f8e', '#00b4d8', '#88e7fb']
cmap_wake = mcolors.LinearSegmentedColormap.from_list('AcousticWake', colors_array, N=256)

# ==========================================
# PANEL 1: 2D Kinematic Vector Flow Field
# ==========================================
ax1 = fig.add_subplot(121)
ax1.set_facecolor('#0d1117')

# Plot Base Density
im1 = ax1.pcolormesh(X, Y, metric_density, cmap=cmap_wake, shading='auto', vmin=0, vmax=0.45)

# Plot Vector Streamlines
ax1.streamplot(X, Y, u, v, color=(1.0, 1.0, 1.0, 0.4), linewidth=0.8, density=1.5, 
               arrowstyle='-|>', arrowsize=1.2)

# Plot Baryonic Node & Yield Boundary
node_2d = ax1.scatter([0], [0], color='#ffde21', s=120, edgecolor='white', zorder=5)
yield_circle_2d = Circle((0, 0), R_yield, color='#ff0055', fill=False, linestyle='--', linewidth=2.5, zorder=4)
ax1.add_patch(yield_circle_2d)

ax1.set_title(r"\textbf{A. Superfluid Kinematic Vector Field}" + "\n" + r"Streamline flow decoupling around $g_N = a_0$", fontsize=18, pad=15)
ax1.set_xlabel(r"Normalized Spatial Coordinate ($x/r_{a_0}$)", labelpad=10)
ax1.set_ylabel(r"Normalized Spatial Coordinate ($y/r_{a_0}$)", labelpad=10)
ax1.set_xlim(-3, 7)
ax1.set_ylim(-4, 4)
ax1.set_aspect('equal')

circle_line = Line2D([0], [0], color='#ff0055', linestyle='--', linewidth=2.5)
ax1.legend([circle_line, node_2d], [r"Kinematic Yield Boundary ($g_N = a_0$)", r"Baryonic Node ($M_b$)"], 
           loc='upper right', framealpha=0.3, facecolor='black', edgecolor='white', fontsize=12)

# ==========================================
# PANEL 2: 3D Topological Phase-Space
# ==========================================
ax2 = fig.add_subplot(122, projection='3d')
ax2.set_facecolor('#0d1117')

# Apply Physical Light Source Shading
ls = LightSource(azdeg=315, altdeg=45)
rgb_shaded = ls.shade(metric_density, cmap=cmap_wake, vert_exag=1.5, blend_mode='soft')

surf = ax2.plot_surface(X, Y, metric_density, facecolors=rgb_shaded, rstride=2, cstride=2, 
                        linewidth=0, antialiased=True, alpha=0.95)

# Plot Node & Yield Boundary on the surface
z_node = np.max(base_stress)
ax2.scatter([0], [0], [z_node], color='#ffde21', s=150, edgecolor='white', zorder=5)

theta_array = np.linspace(0, 2*np.pi, 100)
x_circle = R_yield * np.cos(theta_array)
y_circle = R_yield * np.sin(theta_array)
z_circle = 0.05 * np.exp(-R_yield / 2.0) * np.ones_like(theta_array)
ax2.plot(x_circle, y_circle, z_circle, color='#ff0055', linestyle='--', linewidth=3, zorder=4)

ax2.set_title(r"\textbf{B. Topological Metric Distortion ($\Delta\rho_{eff}$)}" + "\n" + r"Acoustic metric wake replicating dark matter", fontsize=18, pad=15)
ax2.set_xlabel(r"Norm. Coord ($x/r_{a_0}$)", labelpad=15)
ax2.set_ylabel(r"Norm. Coord ($y/r_{a_0}$)", labelpad=15)
ax2.set_zlabel(r"Metric Density ($\Delta\rho_{eff}$)", labelpad=15)

ax2.view_init(elev=35, azim=-120)

ax2.xaxis.pane.fill = False
ax2.yaxis.pane.fill = False
ax2.zaxis.pane.fill = False
ax2.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.15)
ax2.xaxis.pane.set_edgecolor('white')
ax2.yaxis.pane.set_edgecolor('white')
ax2.zaxis.pane.set_edgecolor('white')

# Adjust layout and save
plt.tight_layout()
fig.subplots_adjust(wspace=0.1)

script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_3d_fluid_dynamics_publication.png"))
plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor=fig.get_facecolor())
print(f"Asset generated: {out_path}")
