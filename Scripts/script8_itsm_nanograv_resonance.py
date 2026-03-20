import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# ---------------------------------------------------------
# ITSM Vector 8: NANOGrav Toroidal Strain PSD
# Simulating the Acoustic Metric Resonance Confidence Intervals
# ---------------------------------------------------------

# Frequency range in nanohertz (nHz)
f_nHz = np.linspace(0.5, 5.0, 500)

# 1. LambdaCDM Standard Model (Chaotic Binary Mergers)
# Modeled as a standard decreasing power-law (no structural resonance)
lcdm_psd = 2.5 * (f_nHz)**(-4/3)

# 2. ITSM Toroidal Acoustic Resonance
# The macro-vortex cores (SMBHs) strike the 2pi Superfluid Manifold.
# The resonance is mathematically bounded between a_0 (1.08) and pi (3.14).
# We model the peak at the geometric center with a normal probability distribution.
mu = 2.11  # Geometric midpoint of the harmonic boundary
sigma = 0.34 # Configured so 1.08 and 3.14 represent strict >3-sigma bounds

# Calculate the resonant energy spike
resonance = 3.5 * np.exp(-0.5 * ((f_nHz - mu) / sigma)**2)
itsm_psd = lcdm_psd + resonance

# High-Fidelity Visualization
plt.figure(figsize=(12, 7))
plt.style.use('dark_background')

# Plot the PSD models
plt.plot(f_nHz, lcdm_psd, '--', color='cyan', linewidth=2.5, label=r'$\Lambda$CDM (Chaotic Power-Law)')
plt.plot(f_nHz, itsm_psd, '-', color='red', linewidth=3.5, label=r'ITSM (Toroidal Acoustic Resonance)')

# Shade the Falsifiability Boundaries (1.08 to 3.14 nHz)
plt.axvspan(1.08, 3.14, color='magenta', alpha=0.15, label=r'Toroidal Harmonic Boundary ($1.08 - 3.14$ nHz)')

# Mark the specific physical limits
plt.axvline(1.08, color='white', linestyle=':', alpha=0.6)
plt.text(1.12, 3.5, r'$a_0$ Base ($1.08$ nHz)', color='white', rotation=90, verticalalignment='center', fontsize=12)

plt.axvline(3.14, color='white', linestyle=':', alpha=0.6)
plt.text(3.18, 3.5, r'$\pi$ Harmonic ($3.14$ nHz)', color='white', rotation=90, verticalalignment='center', fontsize=12)

# Fill the confidence interval of the peak
plt.fill_between(f_nHz, lcdm_psd, itsm_psd, where=((f_nHz >= 1.08) & (f_nHz <= 3.14)), 
                 color='red', alpha=0.2)

# Formatting for Publication
plt.title(r'Predicted Stochastic Gravitational Wave Background (NANOGrav)' + '\n' + r'(Acoustic Resonance vs. Chaotic Mergers)', fontsize=16, pad=15)
plt.xlabel(r'Frequency ($f$) [nHz]', fontsize=14)
plt.ylabel(r'Strain Power Spectral Density ($S_h(f)$)', fontsize=14)

plt.xticks(np.arange(0.5, 5.5, 0.5), fontsize=12)
plt.yticks(fontsize=12)
plt.xlim(0.5, 5.0)
plt.ylim(0, 5)

plt.legend(loc='upper right', framealpha=0.15, fontsize=12)
plt.grid(True, linestyle=':', alpha=0.2)

plt.tight_layout()
plt.savefig('itsm_nanograv_resonance.png', dpi=300)
plt.show()
