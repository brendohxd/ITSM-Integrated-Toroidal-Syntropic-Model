import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# ITSM Vector 5: The Acoustic Wake (Figure 1 Generator)
# Visualizing the Stirrer, the Plenum, and Macroscopic Drag
# ---------------------------------------------------------

# 1. Spatial Grid Setup (Superfluid Plenum)
x = np.linspace(-10, 5, 500)
y = np.linspace(-5, 5, 500)
X, Y = np.meshgrid(x, y)

# 2. The Baryonic Node (The "Stirrer")
# Moving right (relative fluid flow moves left)
node_x, node_y = 0.0, 0.0
r = np.sqrt((X - node_x)**2 + (Y - node_y)**2)
baryonic_density = np.exp(-r**2 / 0.8) # Gaussian mass concentration

# 3. The Acoustic Metric Wake (Torsional Drag below a_0)
# A Mach-like cone extending behind the moving mass
wake_angle = np.pi / 4.5 
wake_region = (X < 0) & (np.abs(Y) < np.abs(X) * np.tan(wake_angle))

# Acoustic Phonon ripples (The metric perturbation)
k = 4.0 # Wave number of the acoustic shear
wake_ripples = np.cos(k * np.sqrt(X**2 + Y**2)) * np.exp(X / 4.0) 
acoustic_wake = wake_ripples * wake_region

# Combine into a single metric scalar field
metric_field = baryonic_density + 0.35 * acoustic_wake 

# 4. Superfluid Velocity Streamlines
# Background flow + geometric deflection around the node
U = -1.0 + X*0 
V = 0.0 + Y*0

# Dipole-like deflection (fluid parting around the dense mass)
deflection_strength = 2.0
U += deflection_strength * (X / (r**3 + 0.5)) * np.exp(-r/2)
V += deflection_strength * (Y / (r**3 + 0.5)) * np.exp(-r/2)

# 5. Execution and High-Fidelity Visualization
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 7))

# Plot the underlying metric density (The Vacuum Stress)
# 'inferno' creates a glowing core fading into deep space/fluid
im = ax.pcolormesh(X, Y, metric_field, cmap='inferno', shading='auto', vmin=-0.3, vmax=1.0)

# Overlay the Plenum flow lines (The Toroidal Current)
# Using RGBA (0, 1, 1, 0.4) for Cyan with 40% opacity to bypass matplotlib alpha kwarg error
ax.streamplot(X, Y, U, V, color=(0.0, 1.0, 1.0, 0.4), linewidth=1.0, density=1.5, 
              arrowstyle='->', arrowsize=1.2)

# Plot the hard Baryonic Core
ax.scatter([node_x], [node_y], color='white', s=150, edgecolor='cyan', 
           linewidths=2, zorder=5, label="Baryonic Node ($M_b$)")

# Formatting
ax.set_title("Acoustic Metric Wake Generation\n(Baryonic Node Displacing the Superfluid Plenum)", 
             fontsize=16, pad=20, color='white', fontweight='bold')
ax.set_xlabel("Spatial Coordinate X (kpc)", fontsize=12)
ax.set_ylabel("Spatial Coordinate Y (kpc)", fontsize=12)
ax.legend(loc='upper right', framealpha=0.2, fontsize=11)
ax.set_aspect('equal')
ax.grid(False)

# Save the asset for the LaTeX Manuscript
plt.tight_layout()
plt.savefig('wake_illustration.png', dpi=300, bbox_inches='tight')
plt.show()
