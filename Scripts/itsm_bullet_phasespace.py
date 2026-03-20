import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.stats import gaussian_kde

# ---------------------------------------------------------
# ITSM Vector 4: Bullet Cluster Kinetic Phase-Space
# Quantitative Decoupling of Baryonic Gas and Metric Wake
# ---------------------------------------------------------

# 1. Observational Parameters (Approximating 1E 0657-56)
# Units: Position X [kpc], Velocity Vx [km/s]

n_samples = 5000

# -- The Main Cluster (Larger, Slower, Moving Left) --
# Wake (Follows the collisionless galaxies)
main_wake_x = np.random.normal(-400, 80, n_samples)
main_wake_v = np.random.normal(-2500, 400, n_samples)
# Gas (Stalled near the collision center)
main_gas_x = np.random.normal(-100, 60, n_samples)
main_gas_v = np.random.normal(-500, 300, n_samples)

# -- The Bullet (Smaller, Faster, Moving Right) --
# Wake (Follows the collisionless galaxies)
bullet_wake_x = np.random.normal(500, 60, int(n_samples * 0.6))
bullet_wake_v = np.random.normal(4000, 500, int(n_samples * 0.6))
# Gas (Violently shocked, heavily stalled)
bullet_gas_x = np.random.normal(150, 40, int(n_samples * 0.6))
bullet_gas_v = np.random.normal(1200, 400, int(n_samples * 0.6))

# 2. Kernel Density Estimation (Creating the Contours)
def get_kde(x, y):
    positions = np.vstack([x, y])
    kernel = gaussian_kde(positions)
    # Define the grid
    xmin, xmax = x.min() - 200, x.max() + 200
    ymin, ymax = y.min() - 500, y.max() + 500
    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    Z = np.reshape(kernel(np.vstack([X.ravel(), Y.ravel()])), X.shape)
    return X, Y, Z

X_mw, Y_mw, Z_mw = get_kde(main_wake_x, main_wake_v)
X_mg, Y_mg, Z_mg = get_kde(main_gas_x, main_gas_v)
X_bw, Y_bw, Z_bw = get_kde(bullet_wake_x, bullet_wake_v)
X_bg, Y_bg, Z_bg = get_kde(bullet_gas_x, bullet_gas_v)

# 3. Visualization Architecture
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 8), dpi=200, facecolor='#0d0d0d')
ax.set_facecolor('#0d0d0d')

# Axes Limits and Formatting
ax.set_xlim(-1000, 1000)
ax.set_ylim(-5000, 6000)
ax.axhline(0, color='white', linewidth=1, linestyle='--', alpha=0.3)
ax.axvline(0, color='white', linewidth=1, linestyle='--', alpha=0.3)

# Grid
ax.grid(True, color='#2a2a2a', linestyle=':', linewidth=1)

# Plot Contours (Academic Standard)
levels = 6

# Gas (Tomato Red)
ax.contourf(X_mg, Y_mg, Z_mg, levels=levels, cmap='Reds_r', alpha=0.7)
ax.contour(X_mg, Y_mg, Z_mg, levels=levels, colors='tomato', linewidths=0.8)

ax.contourf(X_bg, Y_bg, Z_bg, levels=levels, cmap='Reds_r', alpha=0.7)
ax.contour(X_bg, Y_bg, Z_bg, levels=levels, colors='tomato', linewidths=0.8)

# Metric Wake (Dodger Blue)
ax.contourf(X_mw, Y_mw, Z_mw, levels=levels, cmap='Blues_r', alpha=0.6)
ax.contour(X_mw, Y_mw, Z_mw, levels=levels, colors='dodgerblue', linewidths=0.8)

ax.contourf(X_bw, Y_bw, Z_bw, levels=levels, cmap='Blues_r', alpha=0.6)
ax.contour(X_bw, Y_bw, Z_bw, levels=levels, colors='dodgerblue', linewidths=0.8)

# 4. Academic Annotations and Labels
ax.set_title("Kinetic Phase-Space Decoupling in the Bullet Cluster (1E 0657-56)\n"
             "ITSM Gravitational Wake vs. Stalled Baryonic Fluid",
             fontsize=18, fontweight='bold', color='white', pad=20)

ax.set_xlabel(r"Spatial Position Relative to Collision Center $x$ [kpc]", fontsize=14, fontweight='bold', labelpad=10)
ax.set_ylabel(r"Line-of-Sight Velocity $v_x$ [km/s]", fontsize=14, fontweight='bold', labelpad=10)

# Custom Legends via Text (Cleaner than bounding boxes)
ax.text(-950, 5200, "■ ITSM Macroscopic Wake (Lensing)", color='dodgerblue', fontsize=12, fontweight='bold')
ax.text(-950, 4600, "■ Stalled Baryonic Gas (X-ray)", color='tomato', fontsize=12, fontweight='bold')

# Decoupling Gap Annotations
# Bullet Gap
ax.annotate('', xy=(150, 1200), xytext=(500, 4000),
            arrowprops=dict(arrowstyle="<->", color='white', lw=1.5, ls='--'))
ax.text(350, 2000, "Kinetic Decoupling Gap\n(Fluid Friction)", color='white', fontsize=10,
        fontweight='bold', rotation=70, ha='center')

# Main Cluster Gap
ax.annotate('', xy=(-100, -500), xytext=(-400, -2500),
            arrowprops=dict(arrowstyle="<->", color='white', lw=1.5, ls='--'))
ax.text(-200, -2000, "Kinetic Decoupling Gap\n(Fluid Friction)", color='white', fontsize=10,
        fontweight='bold', rotation=65, ha='center')

# Polish Tick Parameters
ax.tick_params(axis='both', which='major', labelsize=12, colors='lightgray')

# 5. Output Generation
plt.tight_layout()

# Automatically create the 'Assets' folder if it does not exist
os.makedirs('Assets', exist_ok=True)

# Save the figure
plt.savefig('Assets/itsm_bullet_phasespace.png', dpi=300, bbox_inches='tight')
print("High-Resolution Phase-Space Matrix saved to Assets/itsm_bullet_phasespace.png")
plt.show()
