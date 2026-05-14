import numpy as np
import matplotlib.pyplot as plt

# --- Publication Quality Settings ---
plt.rcParams.update({
    "text.usetex": True,            # Uses your MiKTeX to render text in the plot
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "legend.fontsize": 10,
    "figure.figsize": (6, 4),       # Standard single-column width
    "savefig.dpi": 300              # High-res for printing
})

# --- ITSM vs LambdaCDM Model Definitions ---
def hubble_lambda_cdm(z, H0=67.4, Om=0.315):
    """Standard Model: LambdaCDM"""
    return H0 * np.sqrt(Om * (1 + z)**3 + (1 - Om))

def hubble_itsm(z, H0_base=70.0, variance=0.083):
    """Integrated Toroidal-Syntropic Model (Assumed Tensor Variance)"""
    # Assuming a simplified 1st-order toroidal correction based on your project
    correction = 1 + (variance * np.cos(z / (1 + z))) 
    return H0_base * np.sqrt(0.315 * (1 + z)**3 + 0.685) * correction

# --- Data for Comparison (Real Markers) ---
# Planck (Early Universe) vs SHOES (Late Universe)
z_points = np.array([0, 1.1]) 
H_points = np.array([73.0, 67.4]) 
H_errors = np.array([1.4, 0.5])

# --- Plotting ---
z_range = np.linspace(0, 2.5, 100)

fig, ax = plt.subplots()

# ITSM Curve
ax.plot(z_range, hubble_itsm(z_range), color='navy', label='ITSM (Toroidal Variance)', linewidth=1.5)

# LambdaCDM Curve
ax.plot(z_range, hubble_lambda_cdm(z_range), color='red', linestyle='--', label=r'$\Lambda$CDM (Planck Baseline)', linewidth=1.5)

# Observational Data
ax.errorbar(0, 73.0, yerr=1.4, fmt='o', color='black', capsize=3, label='SHOES $H_0$ (Local)')
ax.errorbar(0, 67.4, yerr=0.5, fmt='s', color='darkorange', capsize=3, label='Planck $H_0$ (CMB)')

# Formatting for Peer Review
ax.set_xlabel(r'Redshift ($z$)')
ax.set_ylabel(r'$H(z)$ [km s$^{-1}$ Mpc$^{-1}$]')
ax.set_title('Hubble Tension: ITSM vs. Standard Model')
ax.legend(frameon=False) # Professional papers rarely use boxes around legends
ax.grid(alpha=0.2, linestyle=':')

plt.tight_layout()
plt.savefig('ITSM_Hubble_Expansion.pdf') # Always save as PDF for journals
plt.show()