"""
Integrated Toroidal-Syntropic Model (ITSM) - 3D Fluid Dynamics
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework
Environment: Windows / Antigravity IDE Workspace Compatible
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D
import os

from matplotlib.colors import LightSource

# Set up dark-theme compatible LaTeX rendering
plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath} \usepackage{xcolor}",
    "font.family": "serif",
    "font.size": 12,
    "text.color": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "axes.edgecolor": "white"
})

# 1. Normalized Grid Setup (r / r_a0)
x = np.linspace(-3.5, 7.5, 500)
y = np.linspace(-4.5, 4.5, 500)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)

# Kinematic Yield Boundary Radius (Normalized to 1)
R_yield = 1.0

# 2. Metric Perturbation Density (The Wake)
wake_mask = (X > R_yield)

# Safely clamp X to prevent exponential overflow in the negative domain before masking
X_safe_envelope = np.clip(X, R_yield, None)

# Exponential expansion of the wake cone
wake_envelope = np.exp(-(Y**2) / (0.4 + 0.3 * X_safe_envelope)) * np.exp(-(X_safe_envelope - R_yield) / 6.0)

# Smoother fluid-like Phonon oscillations
k_phonon = 4.0
wake_oscillation = (0.5 * np.cos(k_phonon * np.sqrt((X - R_yield)**2 + Y**2)) + 0.5)

# Base metric tensor stress
base_stress = 0.05 * np.exp(-R / 2.0)

metric_density = base_stress.copy()
metric_density[wake_mask] += (wake_envelope * wake_oscillation * 0.4)[wake_mask]

# 3. 3D Visualization Architecture
fig = plt.figure(figsize=(14, 10), facecolor='#0d1117')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#0d1117')

# Custom Colormap (Deep Space to Cyan Acoustic Energy)
colors_array = ['#020205', '#0a1532', '#005f8e', '#00b4d8', '#88e7fb']
cmap_wake = mcolors.LinearSegmentedColormap.from_list('AcousticWake', colors_array, N=256)

# Apply Physical Light Source Shading for Fluid Dynamics
ls = LightSource(azdeg=315, altdeg=45)
rgb_shaded = ls.shade(metric_density, cmap=cmap_wake, vert_exag=1.5, blend_mode='soft')

# Plot the 3D Surface with Shading
surf = ax.plot_surface(X, Y, metric_density, facecolors=rgb_shaded, rstride=2, cstride=2, 
                       linewidth=0, antialiased=True, alpha=0.95)

# Plot Baryonic Node
z_node = np.max(base_stress)
ax.scatter([0], [0], [z_node], color='#ffde21', s=120, edgecolor='white', 
           linewidths=1.0, zorder=5, label=r"Baryonic Node ($M_b$)")

# Plot Yield Boundary on the surface
theta = np.linspace(0, 2*np.pi, 100)
x_circle = R_yield * np.cos(theta)
y_circle = R_yield * np.sin(theta)
z_circle = 0.05 * np.exp(-R_yield / 2.0) * np.ones_like(theta)
ax.plot(x_circle, y_circle, z_circle, color='#ff0055', linestyle='--', 
        linewidth=2.5, zorder=4, label=r"Kinematic Yield Boundary ($g_N = a_0$)")

# Formatting
ax.set_title(r"\textbf{3D Topographic Phase-Space of the Acoustic Metric Wake}" + "\n" + 
             r"Toroidal Superfluid Plenum Distortion at $a_0 = c H_0 / 2\pi$", fontsize=16, pad=20)
ax.set_xlabel(r"Normalized Spatial Coordinate ($x/r_{a_0}$)", fontsize=13, labelpad=15)
ax.set_ylabel(r"Normalized Spatial Coordinate ($y/r_{a_0}$)", fontsize=13, labelpad=15)
ax.set_zlabel(r"Metric Perturbation Density ($\Delta\rho_{eff}$)", fontsize=13, labelpad=15)

# Set dramatic view angle
ax.view_init(elev=35, azim=-120)

# Format axes and panes for dark mode
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.15)
ax.xaxis.pane.set_edgecolor('white')
ax.yaxis.pane.set_edgecolor('white')
ax.zaxis.pane.set_edgecolor('white')
ax.tick_params(colors='white')

# Custom Legend Assembly
ax.legend(loc='upper right', framealpha=0.2, facecolor='black', edgecolor='white', fontsize=11)

plt.tight_layout()

# Save Asset
script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_3d_fluid_dynamics_publication.png"))
plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor=fig.get_facecolor())
print(f"Asset generated: {out_path}")
