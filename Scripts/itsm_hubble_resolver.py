
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# ITSM Vector 4: The Hubble Tension Resolver
# Modeling Anisotropic Expansion in a Toroidal Plenum
# ---------------------------------------------------------

# 1. Physics Parameters
H_early = 67.4  # Planck/CMB (Global/Integrated)
H_late  = 73.0  # SH0ES/Supernovae (Local/Directional)

# Toroidal Geometry Constants
# Expansion varies by the angle theta relative to the toroidal axis
# V_exp = H_0 * d * [1 + epsilon * cos(theta)]
epsilon = (H_late - H_early) / H_early  # The Tension Coefficient

# 2. Setup Visualization
plt.style.use('dark_background')
fig = plt.figure(figsize=(18, 6), facecolor='black')

# Panel 1: The Toroidal Manifold (Expansion Map)
ax1 = fig.add_subplot(131, projection='3d')
ax1.set_facecolor('black')

# Create Torus geometry
u = np.linspace(0, 2 * np.pi, 50)
v = np.linspace(0, 2 * np.pi, 50)
U, V = np.meshgrid(u, v)
R_major = 20
r_minor = 8

X = (R_major + r_minor * np.cos(V)) * np.cos(U)
Y = (R_major + r_minor * np.cos(V)) * np.sin(U)
Z = r_minor * np.sin(V)

# Map the apparent Hubble constant to the surface color
# H_obs varies from the center (hole) to the outer rim
H_map = H_early + (H_late - H_early) * (np.abs(np.cos(V)))

# Plot the manifold
surf = ax1.plot_surface(X, Y, Z, facecolors=plt.cm.plasma((H_map - 67)/(74-67)),
                       shade=False, alpha=0.8)
ax1.set_title("Toroidal Superfluid Plenum\n(Geometric Expansion Map)", color='white', pad=20)
ax1.axis('off')

# Panel 2: The Angular Profile (The "Tension" Plot)
ax2 = fig.add_subplot(132)
angles = np.linspace(0, np.pi, 100)
# Expansion rate as a function of viewing angle relative to the poloidal axis
h_obs_profile = H_early + (H_late - H_early) * np.abs(np.cos(angles))

ax2.plot(np.degrees(angles), h_obs_profile, color='cyan', linewidth=2, label='ITSM Prediction')
ax2.axhline(H_early, color='white', linestyle='--', alpha=0.5, label='Planck (67.4)')
ax2.axhline(H_late, color='red', linestyle='--', alpha=0.5, label='SH0ES (73.0)')

ax2.set_title("Expansion Rate vs. Viewing Angle", color='white')
ax2.set_xlabel("Angle from Poloidal Axis (degrees)")
ax2.set_ylabel("H_0 (km/s/Mpc)")
ax2.legend(frameon=False, fontsize=9)
ax2.grid(True, alpha=0.2)

# Panel 3: Resolving the Conflict (Probability Distribution)
ax3 = fig.add_subplot(133)
# Simulate random observer orientations in a Toroidal Universe
samples = H_early + (H_late - H_early) * np.abs(np.cos(np.random.uniform(0, np.pi, 10000)))

ax3.hist(samples, bins=40, color='magenta', alpha=0.6, density=True)
ax3.set_title("Statistical Distribution of H_0\n(Resolving the Tension)", color='white')
ax3.set_xlabel("Measured Expansion Rate (km/s/Mpc)")
ax3.set_ylabel("Probability Density")
ax3.axvline(H_early, color='white', linewidth=2)
ax3.axvline(H_late, color='red', linewidth=2)

plt.tight_layout()
plt.show()
