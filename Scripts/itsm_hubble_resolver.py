
import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------
# ITSM Vector 4: Hubble Tension Geometric Resolution
# Quantitative Projection: H_0 as a Function of Viewing Angle
# ---------------------------------------------------------

# 1. Physical Parameters
theta = np.linspace(0, np.pi, 500) # Viewing angle in radians
H_planck = 67.4
H_shoes = 73.0
H_avg = (H_planck + H_shoes) / 2
H_amp = (H_shoes - H_planck) / 2

# ITSM Projection Function: Expansion as a 2nd-rank Tensor projection
# H(theta) = H_avg + Delta_H * cos(2*theta)
H_theta = H_avg + H_amp * np.cos(2 * theta)

# 2. Visualization Architecture
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 7), dpi=200, facecolor='#0d0d0d')
ax.set_facecolor('#0d0d0d')

# Plot the Anisotropic Curve
ax.plot(theta, H_theta, color='cyan', lw=4, label='ITSM Geometric Projection')

# Mark the Institutional Tension Limits
ax.axhline(H_shoes, color='tomato', ls='--', lw=1.5, alpha=0.8)
ax.axhline(H_planck, color='gold', ls='--', lw=1.5, alpha=0.8)

# Add Shaded Error/Tension Region
ax.fill_between(theta, H_planck, H_shoes, color='white', alpha=0.05, label='Institutional Tension Zone')

# Markers for Specific Observational Alignments
ax.scatter([0, np.pi], [H_shoes, H_shoes], color='tomato', s=100, zorder=5)
ax.scatter([np.pi/2], [H_planck], color='gold', s=100, zorder=5)

# Labels and Text
ax.text(0.1, H_shoes + 0.5, "Late-Universe (SH0ES): 73.0", color='tomato', fontweight='bold')
ax.text(0.1, H_planck - 1.2, "Early-Universe (Planck): 67.4", color='gold', fontweight='bold')

# Styling
ax.set_ylim(65, 75)
ax.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
ax.set_xticklabels(['0°\n(Toroidal Edge)', '45°', '90°\n(Poloidal Axis)', '135°', '180°\n(Toroidal Edge)'])

ax.grid(True, which='both', color='#2a2a2a', linestyle=':', alpha=0.5)
ax.set_title("Geometric Resolution of the Hubble Tension\n"
             "Expansion as a Tensor Field Dependent on Viewing Angle (θ)",
             fontsize=18, fontweight='bold', color='white', pad=20)

ax.set_xlabel(r"Observer Viewing Angle relative to Toroidal Manifold $\theta$", fontsize=14, fontweight='bold')
ax.set_ylabel(r"Measured $H_0$ [km/s/Mpc]", fontsize=14, fontweight='bold')

# 3. Save and Output
plt.legend(loc='lower right', fontsize=10, frameon=True, facecolor='#1a1a1a')
os.makedirs('Assets', exist_ok=True)
plt.savefig('Assets/itsm_hubble_resolver.png', dpi=300, bbox_inches='tight')
print("High-Resolution Hubble Resolver saved to Assets/itsm_hubble_resolver.png")
plt.show()
