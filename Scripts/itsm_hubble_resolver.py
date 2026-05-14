import numpy as np
import matplotlib.pyplot as plt

# Publication Formatting
plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath}",
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "axes.facecolor": "white",
    "figure.facecolor": "white",
    "text.color": "black",
    "axes.labelcolor": "black",
    "xtick.color": "black",
    "ytick.color": "black",
    "font.size": 14
})

# 1. Physical Constants & Observational Limits
H_PLANCK = 67.4  # Early-Universe poloidal measurement [km/s/Mpc]
H_SHOES = 73.0   # Late-Universe toroidal measurement [km/s/Mpc]
POINTS = 1000

# 2. Computational Engine
theta = np.linspace(0, np.pi, POINTS)
h_avg = (H_PLANCK + H_SHOES) / 2.0
h_amp = (H_SHOES - H_PLANCK) / 2.0

# ITSM Geometric Projection: H(theta) = H_avg - H_amp * cos(2*theta)
# Phase shifted so 0 degrees is the Poloidal Axis (lowest expansion)
h_theta = h_avg - h_amp * np.cos(2 * theta)
variance_pct = ((H_SHOES - H_PLANCK) / H_PLANCK) * 100.0

# 3. Visualization Architecture
fig, ax = plt.subplots(figsize=(10, 6.5))

# Shade the Tension Zone
ax.fill_between(theta, H_PLANCK, H_SHOES, color='#0072B2', alpha=0.1)

# Plot the Institutional Limits
ax.axhline(H_SHOES, color='#D55E00', ls='--', lw=2.5, alpha=0.9,
           label=r'SH0ES (Toroidal Limit $\approx 73.0$)')
ax.axhline(H_PLANCK, color='#0072B2', ls='--', lw=2.5, alpha=0.9,
           label=r'Planck 2018 (Poloidal Limit $\approx 67.4$)')

# Plot the Anisotropic Curve
ax.plot(theta, h_theta, color='black', lw=3.5,
        label=r'ITSM Anisotropic Projection ($H_0(\theta)$)')

# Annotate the Variance
ax.text(np.pi/2, 71.5, r"\textbf{Manifold Variance: 8.3\%}", color='black', fontsize=12,
        ha='center', va='center', bbox=dict(facecolor='white', edgecolor='gray', alpha=0.9, boxstyle='round,pad=0.4'))

# Axis Limits and Ticks
ax.set_xlim(0, np.pi)
ax.set_ylim(65, 75)
ax.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
ax.set_xticklabels([r'$0^\circ$' + '\n' + r'(Poloidal Axis)', r'$45^\circ$',
                    r'$90^\circ$' + '\n' + r'(Toroidal Edge)', r'$135^\circ$',
                    r'$180^\circ$' + '\n' + r'(Poloidal Axis)'])

# Grid and Labels
ax.grid(True, which='both', color='lightgray', linestyle='--', alpha=0.7)
ax.set_xlabel(r'Observational Viewing Angle $\theta$ (Degrees)', fontsize=15)
ax.set_ylabel(r'Effective Expansion Rate $H_0$ (km s$^{-1}$ Mpc$^{-1}$)', fontsize=15)
ax.set_title(r'\textbf{Hubble Tension Geometric Resolution}' + '\n' + 
             r'(ITSM Toroidal Anisotropy Projection)', fontsize=17, pad=15)

# Legend
ax.legend(loc='lower right', framealpha=0.95, edgecolor='black', fontsize=12)

plt.tight_layout()
plt.savefig('itsm_hubble_resolver_publication.png', dpi=300)
print("Asset generated: itsm_hubble_resolver_publication.png")