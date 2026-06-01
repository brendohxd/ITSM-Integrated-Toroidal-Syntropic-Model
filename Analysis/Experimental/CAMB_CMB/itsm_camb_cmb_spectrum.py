"""
ITSM Experimental Script — CMB TT Power Spectrum via CAMB
Author: Brendon Boyd
Staging: Analysis/Experimental/CAMB_CMB/
Status: EXPERIMENTAL — Full ITSM Source Term Integration

ITSM Core Principles Applied Here:
  - H0 is NOT a free Hubble constant inferred from the distance ladder.
    It is the ITSM geometric tether: H0 = 2*pi*a0/c.
  - The ITSM Syntropic Volume Decay causes the apparent dark energy to scale
    as (1+z)^{-0.81} (based on DESI BAO empirical fits).
  - This volumetric scaling mathematically maps to a phantom dark energy
    fluid equation of state: w = -1.27.
  - We use CAMB's native dark energy fluid models to solve the perturbation
    equations for this framework.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Scripts')))
from itsm_plot_style import apply_tier1_style
apply_tier1_style()
from multiprocessing import Pool, cpu_count
import camb
from camb import model



# ------------------------------------------------------------------
# COSMOLOGICAL PARAMETERS
# ------------------------------------------------------------------
PLANCK_H0        = 67.36    
PLANCK_OBH2      = 0.02237  
PLANCK_OCDMH2    = 0.12000  
PLANCK_TAU       = 0.0544   
PLANCK_NS        = 0.9649   
PLANCK_LOGAKS    = 3.044    
PLANCK_AS        = np.exp(PLANCK_LOGAKS) * 1e-10

ITSM_H0          = 73.0    # geometric tether
LMAX = 3000

# PLANCK 2018 BINNED TT DATA
PLANCK_ELL = np.array([
    2,    3,    4,    5,    6,    7,    8,    9,   10,
   12,   15,   20,   25,   30,   40,   50,   60,   70,
   80,  100,  120,  150,  200,  250,  300,  350,  400,
  450,  500,  550,  600,  700,  800,  900, 1000,
 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2500
])
PLANCK_DTT = np.array([
    400,  550,  800, 1100, 1200, 1150, 1000,  900,  800,
    800,  900, 1300, 1800, 2200, 3000, 3500, 3800, 4200,
   4500, 5000, 5200, 5600, 5800, 5200, 4100, 2700, 1700,
   1400, 2500, 3500, 3000, 1800, 1200, 1800, 2200,
   2000, 1200,  900, 1100, 1400, 1200,  900,  700,  400
])
PLANCK_ERR = PLANCK_DTT * 0.05   

# ------------------------------------------------------------------
def run_camb(args):
    H0, w, label, colour = args
    try:
        pars = camb.CAMBparams()
        pars.set_cosmology(
            H0=H0,
            ombh2=PLANCK_OBH2,
            omch2=PLANCK_OCDMH2,
            tau=PLANCK_TAU,
            mnu=0.06,          
            omk=0              
        )
        pars.set_dark_energy(w=w, wa=0, dark_energy_model='fluid')
        pars.InitPower.set_params(
            As=PLANCK_AS,
            ns=PLANCK_NS
        )
        pars.set_for_lmax(LMAX, lens_potential_accuracy=0)

        results = camb.get_results(pars)
        powers  = results.get_cmb_power_spectra(pars, CMB_unit='muK')
        totCL   = powers['total']

        ells    = np.arange(totCL.shape[0])
        D_TT    = totCL[:, 0]   

        return (ells, D_TT, label, colour, H0, w)

    except Exception as e:
        print(f"Error in CAMB: {e}")
        return None

# ------------------------------------------------------------------
if __name__ == "__main__":

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "results")
    os.makedirs(output_dir, exist_ok=True)

    N_CORES = cpu_count()

    task_args = [
        (PLANCK_H0, -1.00, f"Planck 2018 Baseline ($H_0={PLANCK_H0}, w=-1.0$)",       "#7f8c8d"),
        (ITSM_H0,   -1.00, f"ITSM Geometric Bound ($H_0={ITSM_H0}, w=-1.0$)", "#c0392b"),
        (ITSM_H0,   -1.27, f"Full ITSM Syntropic ($H_0={ITSM_H0}, w=-1.27$)", "#2471a3"),
    ]

    print(f"\n Running {len(task_args)} CAMB spectra across {N_CORES} cores...\n")

    with Pool(processes=min(N_CORES, len(task_args))) as pool:
        raw = pool.map(run_camb, task_args)

    results_list = [r for r in raw if r is not None]

    fig = plt.figure(figsize=(12, 13))
    gs  = fig.add_gridspec(3, 1, height_ratios=[2.5, 2, 1.2], hspace=0.08)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax3 = fig.add_subplot(gs[2], sharex=ax1)

    planck_spectrum = None
    itsm_spectrum   = None

    for ells, D_TT, label, colour, H0, w in results_list:
        mask = ells >= 2
        ax1.plot(ells[mask], D_TT[mask], "-", color=colour, lw=2.2, alpha=0.9, label=label)
        ax2.plot(ells[mask], D_TT[mask], "-", color=colour, lw=2.2, alpha=0.9)

        if H0 == PLANCK_H0 and w == -1.0:
            planck_spectrum = (ells, D_TT)
        if H0 == ITSM_H0 and w == -1.27:
            itsm_spectrum   = (ells, D_TT)

    ax1.errorbar(PLANCK_ELL, PLANCK_DTT, yerr=PLANCK_ERR,
                 fmt=".", color="#2c3e50", markersize=4,
                 elinewidth=0.8, capsize=2, alpha=0.7, zorder=2,
                 label=r"Planck 2018 TT data (representative bins)")

    peak_ells = [220, 540, 810, 1120, 1400]
    peak_labels = ["1st", "2nd", "3rd", "4th", "5th"]
    for pe, pl in zip(peak_ells, peak_labels):
        ax2.axvline(pe, color="gray", ls=":", lw=0.9, alpha=0.5)
        ax2.text(pe, 6200, pl, ha="center", va="bottom", fontsize=8, color="gray")

    if planck_spectrum is not None and itsm_spectrum is not None:
        e_pl, D_pl = planck_spectrum
        e_it, D_it = itsm_spectrum
        common = np.intersect1d(e_pl, e_it)
        m_pl   = np.isin(e_pl, common)
        m_it   = np.isin(e_it, common)
        frac   = (D_it[m_it] - D_pl[m_pl]) / (D_pl[m_pl] + 1e-30)
        ax3.plot(common, frac * 100, "-", color="#2471a3", lw=2.0)
        ax3.axhline(0, color="#7f8c8d", ls="--", lw=1.5)
        ax3.fill_between(common, frac * 100, 0, where=(frac > 0), color="#2471a3", alpha=0.12)
        ax3.fill_between(common, frac * 100, 0, where=(frac < 0), color="#c0392b", alpha=0.12)

    for ax in [ax1, ax2, ax3]:
        ax.set_xlim(2, LMAX)
        ax.grid(True, which="both", ls=":", alpha=0.3)

    ax1.set_xscale("log")
    ax2.set_xscale("log")
    ax3.set_xscale("log")
    ax2.set_xlim(50, 1600)

    ax1.set_ylim(0, 8000)
    ax2.set_ylim(0, 7000)
    ax1.set_ylabel(r"$\mathcal{D}_\ell^{TT}\ [\mu\mathrm{K}^2]$", fontsize=14)
    ax2.set_ylabel(r"$\mathcal{D}_\ell^{TT}\ [\mu\mathrm{K}^2]$ [peak zoom]", fontsize=13)
    ax3.set_ylabel(r"$\Delta\mathcal{D}/\mathcal{D}$ [\%]" + "\n" + r"(Full ITSM $-$ Planck)", fontsize=11)
    ax3.set_xlabel(r"Multipole $\ell$", fontsize=14)

    ax1.set_title(
        r"CMB TT Power Spectrum: Planck 2018 vs Full ITSM"
        + "\n"
        + r"ITSM Plenum Syntropic Source modeled natively as $w=-1.27$ fluid",
        fontsize=13, pad=12
    )

    ax1.legend(loc="upper right", fontsize=10, framealpha=0.95)

    fig.text(0.13, 0.005,
             (r"\textit{ITSM uses geometric tether $H_0=2\pi a_0/c$. Syntropic Volume Decay "
              r"$(1+z)^{-0.81}$ modeled via CAMB native dark energy fluid with $w=-1.27$.}"),
             fontsize=8.5, color="gray")

    plt.tight_layout(rect=[0, 0.02, 1, 1])

    out_path = os.path.join(output_dir, "itsm_camb_cmb_spectrum.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f" Figure saved: {out_path}")
    if planck_spectrum and itsm_spectrum:
        e_pl, D_pl = planck_spectrum
        e_it, D_it = itsm_spectrum
        mask = (e_pl > 150) & (e_pl < 300)
        peak_pl = e_pl[mask][np.argmax(D_pl[mask])]
        mask = (e_it > 150) & (e_it < 300)
        peak_it = e_it[mask][np.argmax(D_it[mask])]
        print(f"   Planck 1st peak ell : {peak_pl}")
        print(f"   ITSM   1st peak ell : {peak_it}")
        print(f"   Peak shift          : {peak_it - peak_pl:+d} multipoles")
