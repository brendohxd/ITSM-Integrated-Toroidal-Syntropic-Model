import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ====================== v8.2 PARAMETERS ======================
# Simple 2D grid for acoustic wake visualization (baryonic node at center)
x = np.linspace(-10, 10, 400)
y = np.linspace(-10, 10, 400)
X, Y = np.meshgrid(x, y)

# Baryonic node at origin (strong central displacement)
R = np.sqrt(X**2 + Y**2)
density = np.exp(-R**2 / 8) * 5.0                     # Gaussian density peak
v_x = -Y / (R + 1e-8) * np.exp(-R / 4)               # Rotational + radial wake flow
v_y =  X / (R + 1e-8) * np.exp(-R / 4)

# ==================== PUBLICATION-QUALITY PLOT ====================
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 11,
    'axes.linewidth': 1.2
})

fig, ax = plt.subplots(figsize=(8.5, 7))

# Density background (subtle purple-to-cyan colormap)
cmap = LinearSegmentedColormap.from_list('wake', ['#2a0a4a', '#4a2a8a', '#00b4d8'])
im = ax.imshow(density, extent=[-10, 10, -10, 10], origin='lower', cmap=cmap, alpha=0.7)

# Cyan streamlines (the plenum flow around the node)
ax.streamplot(X, Y, v_x, v_y, color='cyan', linewidth=1.2, density=1.8, arrowsize=1.2)

# Baryonic node marker
ax.plot(0, 0, '*', color='#ffeb3b', markersize=18, markeredgecolor='black', markeredgewidth=1.5, label='Baryonic Node ($M_b$)')

# Labels and formatting
ax.set_xlabel('Spatial Coordinate X (kpc)')
ax.set_ylabel('Spatial Coordinate Y (kpc)')
ax.set_title('Acoustic Metric Wake Generation\n'
             'Baryonic Node Displacing the Superfluid Plenum (v8.2)', pad=20)
ax.legend(loc='upper right')
ax.grid(False)

# Colorbar for density
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Relative Plenum Density')

plt.tight_layout()

# Save high-resolution version
plt.savefig('itms_acoustic_wake_v8.2.png', dpi=600, bbox_inches='tight')
plt.show()

print("✅ Fig. 2 saved as itms_acoustic_wake_v8.2.png (600 dpi, publication quality)")
