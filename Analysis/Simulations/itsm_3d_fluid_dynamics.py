"""
ITSM Phase 4 Simulation: Acoustic Wake & Fluid Dynamics
Author: Brendon Boyd
Description: Generates the 2D/3D dual-panel phase-space diagnostic of the 
Acoustic Metric Wake described in the ITSM manuscript.
Models the Superfluid Plenum flowing past a baryonic node using 
modified potential flow with an acoustic lock radius at g_N = a0.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Scripts'))
try:
    from itsm_plot_style import apply_tier1_style
    apply_tier1_style()
except ImportError:
    pass

# Parameters
R_A0 = 1.0       # Radius where g_N = a_0 (Normalized to 1)
V_INF = 1.0      # Free stream velocity of the Plenum (galaxy moving relative to it)
GRID_SIZE = 4.0
RESOLUTION = 200

# Create Grid
x = np.linspace(-GRID_SIZE, GRID_SIZE, RESOLUTION)
y = np.linspace(-GRID_SIZE, GRID_SIZE, RESOLUTION)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
Theta = np.arctan2(Y, X)

# Initialize velocity fields
# In the rest frame of the galaxy, the plenum flows from left to right (positive x)
Vr = np.zeros_like(R)
Vt = np.zeros_like(R)

# 1. Potential Flow outside the acoustic lock radius R_A0
mask_out = R > R_A0
Vr[mask_out] = V_INF * (1 - (R_A0**2 / R[mask_out]**2)) * np.cos(Theta[mask_out])
Vt[mask_out] = -V_INF * (1 + (R_A0**2 / R[mask_out]**2)) * np.sin(Theta[mask_out])

# 2. Inside the acoustic lock, fluid is rigidly attached (velocity is 0 in galaxy frame)
mask_in = R <= R_A0
Vr[mask_in] = 0.0
Vt[mask_in] = 0.0

# Convert back to Cartesian velocities
Vx = Vr * np.cos(Theta) - Vt * np.sin(Theta)
Vy = Vr * np.sin(Theta) + Vt * np.cos(Theta)

# Add a trailing "wake" modification to break the front-back symmetry
# ITSM predicts energy loss into the wake behind the mass (x > 0)
wake_region = (X > 0) & (R > R_A0) & (np.abs(Y) < R_A0 * 1.5)
wake_damping = np.exp(-0.5 * (X[wake_region] / R_A0))
Vx[wake_region] *= (1.0 - 0.4 * wake_damping)
Vy[wake_region] *= (1.0 + 0.2 * wake_damping * np.sign(Y[wake_region]))

# Calculate velocity magnitude
V_mag = np.sqrt(Vx**2 + Vy**2)

# Calculate Effective Metric Perturbation Density (using Bernoulli-like pressure relation)
# Delta rho_eff ~ (V_inf^2 - V^2)
Delta_rho_eff = V_INF**2 - V_mag**2
# Ensure inside the core it is uniformly deep
Delta_rho_eff[mask_in] = V_INF**2

# ====================================================================
# VISUALIZATION: Dual-Panel Phase-Space Diagnostic
# ====================================================================
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
out_dir = os.path.join(repo_root, "Assets", "Figures")
os.makedirs(out_dir, exist_ok=True)

fig = plt.figure(figsize=(18, 8))

# --- Panel A: 2D Kinematic Vector Field ---
ax1 = fig.add_subplot(1, 2, 1)

# Plot velocity magnitude as background color
cp = ax1.pcolormesh(X, Y, V_mag, cmap='viridis', shading='auto', alpha=0.8)
plt.colorbar(cp, ax=ax1, label='Plenum Velocity $|v|$')

# Plot streamlines
# We increase density in the wake region to highlight the shearing
ax1.streamplot(x, y, Vx, Vy, color='white', linewidth=1.0, density=1.5, arrowsize=1.5)

# Plot the fundamental yield boundary g_N = a_0
circle = plt.Circle((0, 0), R_A0, color='red', fill=False, linestyle='--', linewidth=2.5, 
                   label=r'Yield Boundary ($g_N = a_0$)')
ax1.add_patch(circle)

ax1.set_title("2D Kinematic Vector Field: Streamlines", fontsize=16)
ax1.set_xlabel(r"Distance $x / r_{a0}$", fontsize=14)
ax1.set_ylabel(r"Distance $y / r_{a0}$", fontsize=14)
ax1.set_xlim(-GRID_SIZE, GRID_SIZE)
ax1.set_ylim(-GRID_SIZE, GRID_SIZE)
ax1.legend(loc='upper right')

# --- Panel B: 3D Topographical Representation ---
ax2 = fig.add_subplot(1, 2, 2, projection='3d')

# Downsample for 3D plot performance
stride = 2
surf = ax2.plot_surface(X[::stride, ::stride], Y[::stride, ::stride], Delta_rho_eff[::stride, ::stride], 
                        cmap='plasma', edgecolor='none', alpha=0.9)

# Plot the yield boundary cylinder in 3D
theta_cyl = np.linspace(0, 2*np.pi, 50)
z_cyl = np.linspace(0, V_INF**2, 10)
Theta_cyl, Z_cyl = np.meshgrid(theta_cyl, z_cyl)
X_cyl = R_A0 * np.cos(Theta_cyl)
Y_cyl = R_A0 * np.sin(Theta_cyl)
ax2.plot_surface(X_cyl, Y_cyl, Z_cyl, color='red', alpha=0.3)

ax2.set_title("3D Topographical Representation: Metric Wake", fontsize=16)
ax2.set_xlabel(r"$x / r_{a0}$", fontsize=12)
ax2.set_ylabel(r"$y / r_{a0}$", fontsize=12)
ax2.set_zlabel(r"Effective Metric Perturbation $\Delta\rho_{eff}$", fontsize=12)

# Adjust viewing angle for best perspective of the wake
ax2.view_init(elev=35, azim=-45)

# Overall Figure Title
fig.suptitle("Dual-Panel Phase-Space Diagnostic of the Acoustic Metric Wake", fontsize=20, y=1.02)
plt.tight_layout()

out_file = os.path.join(out_dir, "itsm_3d_wake_analogy.png")
plt.savefig(out_file, dpi=300, bbox_inches='tight')
print(f"Saved: {out_file}")
