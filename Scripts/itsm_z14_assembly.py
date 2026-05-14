import numpy as np
import matplotlib.pyplot as plt
import os

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

# 1. Physical Parameters
z_range = np.linspace(30, 10, 500)
# Time from Big Bang in Megayears (Approximate scale for high-z)
t_myr = 28000 * (1 + z_range)**(-1.5)

# -- Standard Model: Hierarchical Merging (Power Law) --
m_lcdm = 10**4 * (t_myr / 50)**2.5

# -- ITSM Model: Toroidal Scaffolding (Exponential Condensation) --
m_itsm = 10**6 * np.exp((t_myr - 50) / 45)

# 2. Observational Data Point: JADES-GS-z14-0
z_obs = 14.32
t_obs = 290 # Myr after Big Bang
m_obs = 10**8.5 # Estimated Stellar Mass (Solar Masses)

# 3. Visualization Architecture
fig, ax = plt.subplots(figsize=(11, 7.5))

# Plot Growth Curves
ax.plot(z_range, m_itsm, color='#0099CC', lw=3, label=r'\textbf{ITSM:} Toroidal Scaffolding (Predictive)')
ax.plot(z_range, m_lcdm, color='#C00000', lw=2.5, ls='--', label=r'\textbf{$\Lambda$CDM:} Hierarchical Merging (Standard)')

# Plot Observational Anchor
ax.scatter(z_obs, m_obs, color='#F0E442', s=350, marker='*', edgecolors='black',
           linewidths=1.5, zorder=5, label=r'\textbf{JADES-GS-z14-0} (Observed)')

# The Lambda-CDM "Forbidden Zone"
ax.fill_between([30, 13], 10**8, 10**11, color='#C00000', alpha=0.08, label=r'$\Lambda$CDM Forbidden Zone')

# Annotations
ax.annotate(r'\textbf{$\Lambda$CDM Growth Lag}' + '\n' + r'\textbf{(Dark Matter Bottleneck)}', 
            xy=(18, 10**6), xytext=(21.5, 10**4.5),
            arrowprops=dict(arrowstyle="->", color='#C00000', lw=2), color='#C00000', fontsize=12)

ax.annotate(r'\textbf{ITSM Accelerated Nucleation}' + '\n' + r'\textbf{(Syntropic Scaffolding)}', 
            xy=(16, 10**8.5), xytext=(19.5, 10**10),
            arrowprops=dict(arrowstyle="->", color='#0099CC', lw=2), color='#0099CC', fontsize=12)

# Axes and Limits
ax.set_yscale('log')
ax.set_xlim(25, 10)
ax.set_ylim(10**4, 10**11)
ax.invert_xaxis() # Redshift decays from left to right

ax.grid(True, which='major', linestyle='-', alpha=0.3)
ax.grid(True, which='minor', linestyle=':', alpha=0.2)

ax.set_title(r"\textbf{Mass Assembly Timeline: The High-Redshift Maturity Crisis}" + "\n" +
             r"Toroidal Superfluid Nucleation vs. Hierarchical Merging",
             fontsize=18, pad=20)

ax.set_xlabel(r"Redshift ($z$)", fontsize=15)
ax.set_ylabel(r"Stellar Mass ($M_{\odot}$)", fontsize=15)

plt.legend(loc='lower left', fontsize=12, framealpha=0.95, edgecolor='black')

plt.tight_layout()
plt.savefig('itsm_z14_assembly_publication.png', dpi=300)
print("Asset generated: itsm_z14_assembly_publication.png")