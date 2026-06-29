import camb
from camb import model, initialpower
import matplotlib.pyplot as plt
import numpy as np
import os
import concurrent.futures
import multiprocessing

# Explicitly ensure multicore utilization for underlying C/Fortran numeric engines
os.environ["OMP_NUM_THREADS"] = str(multiprocessing.cpu_count())

def run_cosmology(w_de, name):
    print(f"Running CAMB for {name} with w = {w_de}...")
    pars = camb.CAMBparams()
    # Baseline Planck 2018 cosmology values
    pars.set_cosmology(H0=67.4, ombh2=0.0224, omch2=0.120)
    pars.InitPower.set_params(As=2.1e-9, ns=0.965)
    
    # Configure Dark Energy
    # Use PPF model to safely cross the phantom divide (w < -1) without scalar ghost instabilities.
    # In ITSM, w = -1.27 is emergent from Creation Pressure (Pc), not a ghost scalar field.
    pars.set_dark_energy(w=w_de, wa=0, dark_energy_model='ppf')
    
    pars.set_matter_power(redshifts=[0.], kmax=10.0)
    
    pars.NonLinear = model.NonLinear_both
    
    results = camb.get_results(pars)
    kh, z, pk = results.get_matter_power_spectrum(minkh=1e-4, maxkh=10, npoints=200)
    
    return kh, pk[0], results

def plot_power_spectra(output_path="itsm_camb_matter_power.png"):
    print(f"Utilizing {multiprocessing.cpu_count()} cores for parallel CAMB OpenMP execution.")
    
    kh_lcdm, pk_lcdm, res_lcdm = run_cosmology(-1.0, "Lambda-CDM")
    kh_itsm, pk_itsm, res_itsm = run_cosmology(-1.27, "ITSM (Phantom Regime)")
    
    plt.figure(figsize=(10, 6))
    plt.loglog(kh_lcdm, pk_lcdm, color='red', label=r'$\Lambda$CDM ($w = -1.0$)')
    plt.loglog(kh_itsm, pk_itsm, color='blue', linestyle='--', label=r'ITSM ($w_{\rm eff} = -1.27$)')
    
    plt.title("Linear Matter Power Spectrum (z=0)")
    plt.xlabel('k/h [Mpc$^{-1}$]')
    plt.ylabel('P(k) [Mpc/h]$^3$')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_plot = os.path.join(base_dir, "itsm_camb_matter_power.png")
    plot_power_spectra(out_plot)
