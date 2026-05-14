import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath}",
    "font.family": "serif",
    "font.size": 12
})

# 1. Normalized Grid Setup (r / r_a0)
x = np.linspace(-3.5, 7.5, 600)
y = np.linspace(-4.5, 4.5, 500)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
Theta = np.arctan2(Y, X)

# Kinematic Yield Boundary Radius (Normalized to 1)
R_yield = 1.0

# 2. Custom Colormap (Deep Space to Cyan Acoustic Energy)
colors_array = ['#020205', '#0a1532', '#005f8e', '#00b4d8', '#88e7fb']
cmap_wake = mcolors.LinearSegmentedColormap.from_list('AcousticWake', colors_array, N=256)

# 3. Metric Perturbation Density (The Wake)
wake_mask = (X > R_yield)

# Safely clamp X to prevent exponential overflow in the negative domain before masking
X_safe_envelope = np.clip(X, R_yield, None)

# Exponential expansion of the wake cone
wake_envelope = np.exp(-(Y**2) / (0.4 + 0.3 * X_safe_envelope)) * np.exp(-(X_safe_envelope - R_yield) / 6.0)

# Phonon oscillations
k_phonon = 4.0
wake_oscillation = np.cos(k_phonon * np.sqrt((X - R_yield)**2 + Y**2))**2

# Base metric tensor stress
base_stress = 0.05 * np.exp(-R / 2.0)

metric_density = base_stress.copy()
metric_density[wake_mask] += (wake_envelope * wake_oscillation * 0.5)[wake_mask]

# 4. Superfluid Streamlines (Flow past the yield boundary)
U_inf = 1.0
R_safe = np.where(R < 0.05, 0.05, R)

# Ideal fluid flow equations past a cylinder
u = U_inf * (1 - (R_yield**2 / R_safe**2) * np.cos(2*Theta))
v = U_inf * (-(R_yield**2 / R_safe**2) * np.sin(2*Theta))

# 5. Visualization Architecture
fig, ax = plt.subplots(figsize=(12, 8))

# Plot Density
im = ax.pcolormesh(X, Y, metric_density, cmap=cmap_wake, shading='auto', vmin=0, vmax=0.55)
cb = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cb.set_label(r'Metric Perturbation Density ($\Delta\rho_{eff}$)', fontsize=13)

# Plot Streamlines (Using RGBA to bypass streamplot alpha kwarg limitations)
ax.streamplot(X, Y, u, v, color=(1.0, 1.0, 1.0, 0.35), linewidth=0.6, density=1.4, 
              arrowstyle='-|>', arrowsize=1.0)

# Plot Baryonic Node
node = ax.scatter([0], [0], color='#ffde21', s=80, edgecolor='white', 
                  linewidths=1.0, zorder=5, label=r"Baryonic Node ($M_b$)")

# Plot Yield Boundary
yield_circle = Circle((0, 0), R_yield, color='#ff0055', fill=False, linestyle='--', 
                      linewidth=2.5, zorder=4, label=r"Kinematic Yield Boundary ($g_N = a_0$)")
ax.add_patch(yield_circle)

# Formatting
ax.set_title(r"\textbf{Macroscopic Torsional Entrainment (Acoustic Metric Wake)}" + "\n" + 
             r"Superfluid Plenum Transition at $a_0 = c H_0 / 2\pi$", fontsize=15, pad=15)
ax.set_xlabel(r"Normalized Spatial Coordinate ($r/r_{a_0}$)", fontsize=13)
ax.set_ylabel(r"Normalized Spatial Coordinate ($r/r_{a_0}$)", fontsize=13)

# Custom Legend Assembly
circle_line = Line2D([0], [0], color='#ff0055', linestyle='--', linewidth=2.5)
ax.legend([circle_line, node], [r"Kinematic Yield Boundary ($g_N = a_0$)", r"Baryonic Node ($M_b$)"], 
          loc='upper right', framealpha=0.9, fontsize=11, edgecolor='black')

ax.set_aspect('equal')
ax.set_xlim(-3, 7)
ax.set_ylim(-4.2, 4.2)

plt.tight_layout()
plt.savefig('itsm_acoustic_wake_publication.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
print("Asset generated: itsm_acoustic_wake_publication.png")