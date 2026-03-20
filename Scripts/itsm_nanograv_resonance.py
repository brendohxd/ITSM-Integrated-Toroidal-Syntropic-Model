import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------
# ITSM Vector 5: NANOGrav Acoustic Resonance
# Quantitative Strain PSD: Power Law vs. Toroidal Resonance
# ---------------------------------------------------------

# 1. Frequency Domain (nHz)
# Typically 1 nHz to 100 nHz for PTA data
freqs = np.logspace(-1, 2, 1000) 

# -- LCDM Model: Stochastic GWB (Power Law) --
# Characteristic Strain h_c(f) = A * (f / f_yr)^(-2/3)
A_gwb = 2.4e-15  # NANOGrav 15-yr Amplitude
f_yr = 31.7      # 1/year in nHz
h_lcdm = A_gwb * (freqs / f_yr)**(-2/3)

# -- ITSM Model: Power Law + Acoustic Resonance --
# Predicted peak between 1.08 and 3.14 nHz
f_res = 2.11  # Centroid of the predicted range
width = 0.5   # Resonance width
# Lorentzian Resonance Peak
resonance = 1.5e-14 * (width**2 / ((freqs - f_res)**2 + width**2))
h_itsm = h_lcdm + resonance

# 2. Visualization Architecture
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 8), dpi=200, facecolor='#0d0d0d')
ax.set_facecolor('#0d0d0d')

# Log-Log Scaling (Crucial for PTA)
ax.set_xscale('log')
ax.set_yscale('log')

# Plotting the Frameworks
ax.plot(freqs, h_lcdm, color='tomato', lw=2, ls='--', alpha=0.8, label='ΛCDM: Stochastic SMBHB Background')
ax.plot(freqs, h_itsm, color='cyan', lw=3, label='ITSM: Toroidal Acoustic Resonance')

# Add "Violin" Error Envelopes (Simulated Confidence Intervals)
ax.fill_between(freqs, h_lcdm * 0.5, h_lcdm * 1.5, color='tomato', alpha=0.1)
ax.fill_between(freqs, h_itsm * 0.7, h_itsm * 1.3, color='cyan', alpha=0.1)

# Highlight the Predicted Falsifiability Window (1.08 - 3.14 nHz)
ax.axvspan(1.08, 3.14, color='white', alpha=0.1, label='ITSM Prediction Horizon')
ax.axvline(1.08, color='white', ls=':', alpha=0.3)
ax.axvline(3.14, color='white', ls=':', alpha=0.3)

# Annotations
ax.annotate('Toroidal Mode Resonance\n(Predicted Spectral Excess)', 
            xy=(f_res, 1.8e-14), xytext=(8, 4e-14),
            arrowprops=dict(arrowstyle="->", color='cyan', lw=1.5), 
            color='cyan', fontweight='bold', fontsize=11)

ax.annotate('Standard SMBHB Power Law\n(No Structural Excess)', 
            xy=(50, 2e-15), xytext=(20, 5e-16),
            arrowprops=dict(arrowstyle="->", color='tomato', lw=1.5), 
            color='tomato', fontweight='bold', fontsize=10)

# Styling and Labels
ax.set_xlim(0.5, 100)
ax.set_ylim(1e-16, 1e-13)
ax.grid(True, which='both', color='#2a2a2a', linestyle=':', alpha=0.4)

ax.set_title("Stochastic Gravitational Wave Background: Strain PSD\n"
             "NANOGrav 15-Year Data vs. ITSM Acoustic Prediction", 
             fontsize=18, fontweight='bold', color='white', pad=20)

ax.set_xlabel(r"Gravitational Wave Frequency $f$ [nHz]", fontsize=14, fontweight='bold')
ax.set_ylabel(r"Characteristic Strain $h_c(f)$", fontsize=14, fontweight='bold')

# 3. Output Generation
plt.legend(loc='lower left', fontsize=10, frameon=True, facecolor='#1a1a1a')
os.makedirs('Assets', exist_ok=True)
plt.savefig('Assets/itsm_nanograv_resonance.png', dpi=300, bbox_inches='tight')
print("High-Resolution NANOGrav Matrix saved to Assets/itsm_nanograv_resonance.png")
plt.show()
