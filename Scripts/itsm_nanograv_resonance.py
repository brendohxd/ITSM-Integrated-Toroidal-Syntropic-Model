import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 12})

f_nHz = np.logspace(-1, 2, 500)
h_c_baseline = 1e-14 * (f_nHz / 1.0)**(-2/3)

f_peak = 2.0 
resonance_width = 0.5
resonance_amplitude = 1.5e-14

resonance = resonance_amplitude * np.exp(-0.5 * ((f_nHz - f_peak) / resonance_width)**2)
h_c_itsm = h_c_baseline + resonance

upper_bound = h_c_itsm * 1.2
lower_bound = h_c_itsm * 0.8

plt.figure(figsize=(10, 6))

plt.plot(f_nHz, h_c_baseline, '--', color='gray', linewidth=2, label=r'$\Lambda$CDM: Stochastic SMBHB Background')
plt.plot(f_nHz, h_c_itsm, '-', color='darkblue', linewidth=3, label=r'ITSM: Toroidal Acoustic Resonance')
plt.fill_between(f_nHz, lower_bound, upper_bound, color='blue', alpha=0.1)

plt.axvspan(1.08, 3.14, color='gray', alpha=0.15, label=r'ITSM Prediction Horizon')
plt.axvline(x=1.08, color='black', linestyle=':', alpha=0.5)
plt.axvline(x=3.14, color='black', linestyle=':', alpha=0.5)

plt.xscale('log'); plt.yscale('log')
plt.xlim(0.5, 100); plt.ylim(1e-16, 1e-13)

plt.title(r'\textbf{Stochastic Gravitational Wave Background: Strain PSD}', fontsize=16, pad=15)
plt.xlabel(r'Gravitational Wave Frequency $f$ [nHz]', fontsize=14)
plt.ylabel(r'Characteristic Strain $h_c(f)$', fontsize=14)

plt.legend(loc='lower left', framealpha=0.9, fontsize=12)
plt.grid(True, which="major", ls="-", alpha=0.4)
plt.grid(True, which="minor", ls=":", alpha=0.2)

plt.tight_layout()
plt.savefig('itsm_nanograv_resonance.png', dpi=300)