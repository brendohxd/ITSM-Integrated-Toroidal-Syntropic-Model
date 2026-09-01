
import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------
# ITSM Vector 2: JADES-GS-z14-0 Timeline Analysis
# Quantitative Assembly: Toroidal Scaffolding vs. LCDM Merging
# ---------------------------------------------------------

# 1. Physical Parameters
z_range = np.linspace(30, 10, 500)
# Time from Big Bang in Megayears (Approximate for high-z)
t_myr = 28000 * (1 + z_range)**(-1.5)

# -- LCDM Model: Hierarchical Merging (Power Law) --
# M(t) ~ t^alpha where alpha is related to halo growth
m_lcdm = 10**4 * (t_myr / 50)**2.5

# -- ITSM Model: Toroidal Scaffolding (Exponential Condensation) --
# Fast nucleation at vortex cores + syntropic scaling
m_itsm = 10**6 * np.exp((t_myr - 50) / 45)

# 2. Observational Data Point: JADES-GS-z14-0
z_obs = 14.32
t_obs = 290 # Myr after Big Bang
m_obs = 10**8.5 # Estimated Stellar Mass (Solar Masses)

# 3. Visualization Architecture
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 8), dpi=200, facecolor='#0d0d0d')
ax.set_facecolor('#0d0d0d')

# Log-Linear Plotting
ax.plot(z_range, m_itsm, color='cyan', lw=3, label='ITSM: Toroidal Scaffolding (Predictive)')
ax.plot(z_range, m_lcdm, color='tomato', lw=2, ls='--', label='ΛCDM: Hierarchical Merging (Standard)')

# Plot Observational Anchor
ax.scatter(z_obs, m_obs, color='gold', s=250, marker='*', edgecolors='white',
           zorder=5, label='JADES-GS-z14-0 (Observed)')

# Axes and Limits
ax.set_yscale('log')
ax.set_xlim(25, 10)
ax.set_ylim(10**4, 10**11)
ax.invert_xaxis() # Redshift goes from high to low

# Grid and Styling
ax.grid(True, which='both', color='#2a2a2a', linestyle=':', alpha=0.5)
ax.set_title("Mass Assembly Timeline: The High-Redshift Maturity Crisis\n"
             "Toroidal Superfluid Nucleation vs. Hierarchical Merging",
             fontsize=18, fontweight='bold', color='white', pad=20)

ax.set_xlabel(r"Redshift ($z$)", fontsize=14, fontweight='bold')
ax.set_ylabel(r"Stellar Mass ($M_{\odot}$)", fontsize=14, fontweight='bold')

# Annotations (The "Why it works")
ax.annotate('ΛCDM Growth Lag\n(Dark Matter Bottleneck)', xy=(18, 10**6), xytext=(22, 10**4.5),
            arrowprops=dict(arrowstyle="->", color='tomato', lw=1.5), color='tomato', fontweight='bold')

ax.annotate('ITSM Accelerated Nucleation\n(Syntropic Scaffolding)', xy=(16, 10**8.5), xytext=(20, 10**10),
            arrowprops=dict(arrowstyle="->", color='cyan', lw=1.5), color='cyan', fontweight='bold')

# The "Forbidden Zone"
ax.fill_between([30, 13], 10**8, 10**11, color='red', alpha=0.1, label='ΛCDM Forbidden Zone')

# 4. Save and Output
plt.legend(loc='upper left', fontsize=10, frameon=True, facecolor='#1a1a1a')
os.makedirs('Assets', exist_ok=True)
plt.savefig('Assets/itsm_z14_assembly.png', dpi=300, bbox_inches='tight')
print("High-Resolution Assembly Matrix saved to Assets/itsm_z14_assembly.png")
plt.show()
