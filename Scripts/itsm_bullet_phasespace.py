import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.patches import Patch

# Publication Formatting
plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath}",
    "font.family": "serif",
    "font.size": 12
})

np.random.seed(42) # Absolute reproducibility established
N_SAMPLES = 5000
LEVELS = 6

def get_kde(x, y):
    """Generates the Kernel Density Estimation grid for contour mapping."""
    positions = np.vstack([x, y])
    kernel = gaussian_kde(positions)
    
    xmin, xmax = x.min() - 200, x.max() + 200
    ymin, ymax = y.min() - 500, y.max() + 500
    
    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    Z = np.reshape(kernel(np.vstack([X.ravel(), Y.ravel()])), X.shape)
    return X, Y, Z

# 1. Kinematic Distributions (Position vs Velocity)
# The Main Cluster
main_wake_x = np.random.normal(-400, 80, N_SAMPLES)
main_wake_v = np.random.normal(-2500, 400, N_SAMPLES)
main_gas_x = np.random.normal(-100, 60, N_SAMPLES)
main_gas_v = np.random.normal(-500, 300, N_SAMPLES)

# The Bullet Cluster
bullet_wake_x = np.random.normal(500, 60, int(N_SAMPLES * 0.6))
bullet_wake_v = np.random.normal(4000, 500, int(N_SAMPLES * 0.6))
bullet_gas_x = np.random.normal(150, 40, int(N_SAMPLES * 0.6))
bullet_gas_v = np.random.normal(1200, 400, int(N_SAMPLES * 0.6))

# Generate Density Grids
mw_grid = get_kde(main_wake_x, main_wake_v)
mg_grid = get_kde(main_gas_x, main_gas_v)
bw_grid = get_kde(bullet_wake_x, bullet_wake_v)
bg_grid = get_kde(bullet_gas_x, bullet_gas_v)

# 2. Visualization Architecture
fig, ax = plt.subplots(figsize=(10, 7))

ax.set_xlim(-1000, 1000)
ax.set_ylim(-5000, 6000)
ax.axhline(0, color='gray', linewidth=1, linestyle='--', alpha=0.5)
ax.axvline(0, color='gray', linewidth=1, linestyle='--', alpha=0.5)
ax.grid(True, color='lightgray', linestyle=':', linewidth=1)

X_mw, Y_mw, Z_mw = mw_grid
X_mg, Y_mg, Z_mg = mg_grid
X_bw, Y_bw, Z_bw = bw_grid
X_bg, Y_bg, Z_bg = bg_grid

# Plot Contours: Stalled Gas (Red Phase Space)
ax.contourf(X_mg, Y_mg, Z_mg, levels=LEVELS, cmap='Reds', alpha=0.8)
ax.contour(X_mg, Y_mg, Z_mg, levels=LEVELS, colors='darkred', linewidths=0.5)
ax.contourf(X_bg, Y_bg, Z_bg, levels=LEVELS, cmap='Reds', alpha=0.8)
ax.contour(X_bg, Y_bg, Z_bg, levels=LEVELS, colors='darkred', linewidths=0.5)

# Plot Contours: Macroscopic Metric Wake (Blue Phase Space)
ax.contourf(X_mw, Y_mw, Z_mw, levels=LEVELS, cmap='Blues', alpha=0.7)
ax.contour(X_mw, Y_mw, Z_mw, levels=LEVELS, colors='midnightblue', linewidths=0.5)
ax.contourf(X_bw, Y_bw, Z_bw, levels=LEVELS, cmap='Blues', alpha=0.7)
ax.contour(X_bw, Y_bw, Z_bw, levels=LEVELS, colors='midnightblue', linewidths=0.5)

# Academic Annotations and Labels
ax.set_title(r"\textbf{Kinetic Phase-Space Decoupling in the Bullet Cluster (1E 0657-56)}" + "\n" +
             r"ITSM Gravitational Wake vs. Stalled Baryonic Fluid", pad=20, fontsize=15)

ax.set_xlabel(r"Spatial Position Relative to Collision Center $x$ [kpc]", fontsize=14)
ax.set_ylabel(r"Line-of-Sight Velocity $v_x$ [km s$^{-1}$]", fontsize=14)

legend_elements = [
    Patch(facecolor='#1e90ff', alpha=0.7, edgecolor='midnightblue', label=r'ITSM Macroscopic Wake (Lensing)'),
    Patch(facecolor='#ff6347', alpha=0.8, edgecolor='darkred', label=r'Stalled Baryonic Gas (X-ray)')
]
ax.legend(handles=legend_elements, loc='upper left', frameon=True, facecolor='white', edgecolor='black', fontsize=12)

# Decoupling Gap Annotations
ax.annotate('', xy=(150, 1200), xytext=(500, 4000),
            arrowprops=dict(arrowstyle="<->", color='black', lw=1.5, ls='--'))
ax.text(350, 2400, r"\textbf{Kinetic Decoupling Gap}" + "\n" + r"(Fluid Friction)", color='black', fontsize=10,
        rotation=68, ha='center', bbox=dict(facecolor='white', edgecolor='gray', alpha=0.9))

ax.annotate('', xy=(-100, -500), xytext=(-400, -2500),
            arrowprops=dict(arrowstyle="<->", color='black', lw=1.5, ls='--'))
ax.text(-250, -1500, r"\textbf{Kinetic Decoupling Gap}" + "\n" + r"(Fluid Friction)", color='black', fontsize=10,
        rotation=63, ha='center', bbox=dict(facecolor='white', edgecolor='gray', alpha=0.9))

plt.tight_layout()
plt.savefig('itsm_bullet_phasespace_publication.png', dpi=300)
print("Asset generated: itsm_bullet_phasespace_publication.png")
