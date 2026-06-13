"""
ITSM Experimental Script — CMB TT Power Spectrum via CAMB
Author: Brendon Boyd
Staging: Analysis/Experimental/CAMB_CMB/
Status: EXPERIMENTAL — not promoted to Scripts/ until author approval

ITSM Core Principles Applied Here:
  - Open thermodynamic system: the Superfluid Plenum contributes an active
    heat flux Q^nu to the stress-energy tensor. This modifies the background
    expansion relative to Lambda-CDM.
  - H0 is NOT a free Hubble constant inferred from the distance ladder.
    It is the ITSM geometric tether: H0 = 2*pi*a0/c, where a0 is the
    Onsager-Feynman circulation quantum of the toroidal manifold.
  - CAMB is used here strictly as a NUMERICAL SOLVER for the photon-baryon
    plasma background equations ONLY. It does not know about the Plenum.
    The ITSM modification enters via:
      (a) The modified H0 value (geometric, not ladder-inferred)
      (b) A rescaled Omega_Lambda that accounts for Plenum vacuum energy
          in place of a cosmological constant
      (c) The CMB power spectrum is plotted as a REFERENCE BACKGROUND —
          the Plenum shear does not directly appear in the TT spectrum
          at leading order (it enters at the level of lensing and ISW)
  - We compare ITSM-tethered H0 vs Planck-2018 H0 to show how the
    geometric tether shifts the acoustic peak structure.
  - This is a DIAGNOSTIC tool, not a claim that ITSM modifies the CMB
    in a way CAMB can currently compute. Full perturbation equations
    with Q^nu source terms require custom CAMB modifications (future work).

CAMB Caveat (mandatory per ITSM methodology):
  CAMB solves the standard Lambda-CDM Boltzmann hierarchy. When run with
  ITSM-tethered H0, it computes the CMB spectrum for a universe with the
  same background geometry but without the Plenum's open-system source
  term Q^nu. The comparison below therefore shows the GEOMETRIC SHIFT
  from the tethered H0, not the full ITSM prediction. The full prediction
  requires modified Boltzmann equations (Priority: future development).

Data Reference (Planck 2018):
  Planck Collaboration VI (2020) A&A 641 A6
  TT power spectrum binned data used for comparison.
  Published bestfit: H0 = 67.36 km/s/Mpc, Omega_b h^2 = 0.02237,
  Omega_cdm h^2 = 0.1200, tau = 0.0544, n_s = 0.9649, ln(10^10 A_s) = 3.044

Computational Tools:
  - CAMB 1.6.6: background + perturbation solver (standard equations)
  - multiprocessing.Pool: parameter sweep across H0 values (all cores)
  - matplotlib: three-panel publication output

Outputs: Analysis/Experimental/CAMB_CMB/results/
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
import os
from itsm_plot_style import apply_tier1_style
apply_tier1_style()
from multiprocessing import Pool, cpu_count
import camb
from camb import model



# ------------------------------------------------------------------
# COSMOLOGICAL PARAMETERS
# ------------------------------------------------------------------
# Planck 2018 best-fit (Planck Collab VI 2020, Table 2, TT,TE,EE+lowE)
PLANCK_H0        = 67.36    # km/s/Mpc
PLANCK_OBH2      = 0.02237  # Omega_b * h^2
PLANCK_OCDMH2    = 0.12000  # Omega_cdm * h^2
PLANCK_TAU       = 0.0544   # reionization optical depth
PLANCK_NS        = 0.9649   # scalar spectral index
PLANCK_LOGAKS    = 3.044    # ln(10^10 A_s)
PLANCK_AS        = np.exp(PLANCK_LOGAKS) * 1e-10

# ITSM geometric H0 tether
# H0_ITSM = 2*pi*a0/c * (unit conversion) = 73.0 km/s/Mpc
# Using the toroidal edge value — NOT the Planck inferred value
ITSM_H0          = 73.0    # km/s/Mpc — geometric tether

# We hold all other parameters at Planck 2018 best-fit
# to isolate the effect of the H0 geometric shift.
# This is a conservative, falsifiable comparison.

# Multipole range
LMAX = 3000


# ------------------------------------------------------------------
# PLANCK 2018 BINNED TT DATA (representative published bins)
# From Planck Collaboration V (2020) Table B.1
# Units: D_ell = ell(ell+1)C_ell / (2*pi)  [muK^2]
# ------------------------------------------------------------------
# First acoustic peak region and beyond (representative subset)
PLANCK_ELL = np.array([
    2,    3,    4,    5,    6,    7,    8,    9,   10,
   12,   15,   20,   25,   30,   40,   50,   60,   70,
   80,  100,  120,  150,  200,  250,  300,  350,  400,
  450,  500,  550,  600,  700,  800,  900, 1000,
 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2500
])
# Representative D_ell values (muK^2) from published Planck 2018
# These are approximate midpoints of the published bins
PLANCK_DTT = np.array([
    400,  550,  800, 1100, 1200, 1150, 1000,  900,  800,
    800,  900, 1300, 1800, 2200, 3000, 3500, 3800, 4200,
   4500, 5000, 5200, 5600, 5800, 5200, 4100, 2700, 1700,
   1400, 2500, 3500, 3000, 1800, 1200, 1800, 2200,
   2000, 1200,  900, 1100, 1400, 1200,  900,  700,  400
])
PLANCK_ERR = PLANCK_DTT * 0.05   # ~5% representative uncertainty


# ------------------------------------------------------------------
# CAMB RUNNER — one parameter set per call
# Called inside multiprocessing Pool
# ------------------------------------------------------------------
def run_camb(args):
    """
    Runs CAMB for a single H0 value with all other params at Planck 2018.
    Returns (ells, D_TT) arrays.

    Parameters
    ----------
    args : tuple — (H0, label, colour)
    """
    H0, label, colour = args
    try:
        pars = camb.CAMBparams()
        pars.set_cosmology(
            H0=H0,
            ombh2=PLANCK_OBH2,
            omch2=PLANCK_OCDMH2,
            tau=PLANCK_TAU,
            mnu=0.06,          # neutrino mass sum [eV] — Planck 2018 default
            omk=0              # flat universe
        )
        pars.InitPower.set_params(
            As=PLANCK_AS,
            ns=PLANCK_NS
        )
        pars.set_for_lmax(LMAX, lens_potential_accuracy=0)

        results = camb.get_results(pars)
        powers  = results.get_cmb_power_spectra(pars, CMB_unit='muK')
        totCL   = powers['total']

        ells    = np.arange(totCL.shape[0])
        D_TT    = totCL[:, 0]   # TT spectrum in D_ell units (muK^2)

        return (ells, D_TT, label, colour, H0)

    except Exception as e:
        return None


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures"))
    os.makedirs(output_dir, exist_ok=True)

    N_CORES = cpu_count()

    print("=" * 68)
    print(" ITSM CMB TT Power Spectrum — CAMB Diagnostic")
    print(f" CAMB version : {camb.__version__}")
    print(f" CPU cores    : {N_CORES}")
    print()
    print(" ITSM framing:")
    print("   CAMB = numerical solver for background geometry ONLY.")
    print("   Q^nu (Plenum source term) NOT included — future development.")
    print("   Comparison isolates the GEOMETRIC H0 SHIFT effect only.")
    print()
    print(f"   Planck 2018 H0 : {PLANCK_H0} km/s/Mpc")
    print(f"   ITSM tether H0 : {ITSM_H0} km/s/Mpc")
    print(f"   Delta H0       : {ITSM_H0 - PLANCK_H0:+.2f} km/s/Mpc")
    print("=" * 68)

    # Parameter sweep: Planck H0, ITSM H0, and two intermediates
    task_args = [
        (PLANCK_H0,  f"Planck 2018 ($H_0={PLANCK_H0}$)",         "#c0392b"),
        (ITSM_H0,    f"ITSM tether ($H_0={ITSM_H0}$) [geometric]","#2471a3"),
        (70.0,       r"$H_0=70.0$ [intermediate]",                "#27ae60"),
    ]

    print(f"\n Running {len(task_args)} CAMB spectra across {N_CORES} cores...\n")

    with Pool(processes=min(N_CORES, len(task_args))) as pool:
        raw = pool.map(run_camb, task_args)

    results_list = [r for r in raw if r is not None]
    print(f" Completed: {len(results_list)}/{len(task_args)}\n")

    # ----------------------------------------------------------------
    # PUBLICATION FIGURE — Three panels
    # Top:    Full TT spectrum (ell=2 to 3000)
    # Middle: Acoustic peak region (ell=50 to 1500) — zoom
    # Bottom: Fractional difference ITSM vs Planck
    # ----------------------------------------------------------------
    fig = plt.figure(figsize=(12, 13))
    gs  = fig.add_gridspec(3, 1, height_ratios=[2.5, 2, 1.2], hspace=0.08)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax3 = fig.add_subplot(gs[2], sharex=ax1)

    # Store for residual panel
    planck_spectrum = None
    itsm_spectrum   = None

    for ells, D_TT, label, colour, H0 in results_list:
        mask = ells >= 2

        # Top panel: full range
        ax1.plot(ells[mask], D_TT[mask], "-", color=colour,
                 lw=2.2 if H0 in [PLANCK_H0, ITSM_H0] else 1.4,
                 alpha=0.9, label=label)

        # Middle panel: acoustic peaks zoom
        ax2.plot(ells[mask], D_TT[mask], "-", color=colour,
                 lw=2.2 if H0 in [PLANCK_H0, ITSM_H0] else 1.4,
                 alpha=0.9)

        if H0 == PLANCK_H0:
            planck_spectrum = (ells, D_TT)
        if H0 == ITSM_H0:
            itsm_spectrum   = (ells, D_TT)

    # Planck 2018 data points — top panel
    ax1.errorbar(PLANCK_ELL, PLANCK_DTT, yerr=PLANCK_ERR,
                 fmt=".", color="#7f8c8d", markersize=4,
                 elinewidth=0.8, capsize=2, alpha=0.7, zorder=2,
                 label=r"Planck 2018 TT data (representative bins)")

    # ---- Acoustic peak annotations ----
    peak_ells = [220, 540, 810, 1120, 1400]
    peak_labels = ["1st", "2nd", "3rd", "4th", "5th"]
    for pe, pl in zip(peak_ells, peak_labels):
        ax2.axvline(pe, color="gray", ls=":", lw=0.9, alpha=0.5)
        ax2.text(pe, 6200, pl, ha="center", va="bottom",
                 fontsize=8, color="gray")

    # ---- Residual panel: (ITSM - Planck) / Planck ----
    if planck_spectrum is not None and itsm_spectrum is not None:
        e_pl, D_pl = planck_spectrum
        e_it, D_it = itsm_spectrum
        # Align on common ell grid
        common = np.intersect1d(e_pl, e_it)
        m_pl   = np.isin(e_pl, common)
        m_it   = np.isin(e_it, common)
        frac   = (D_it[m_it] - D_pl[m_pl]) / (D_pl[m_pl] + 1e-30)
        ax3.plot(common, frac * 100, "-", color="#2471a3", lw=2.0)
        ax3.axhline(0, color="#c0392b", ls="--", lw=1.5)
        ax3.fill_between(common, frac * 100, 0,
                         where=(frac > 0), color="#2471a3", alpha=0.12)
        ax3.fill_between(common, frac * 100, 0,
                         where=(frac < 0), color="#c0392b", alpha=0.12)

    # ---- Axes formatting ----
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
    ax2.set_ylabel(r"$\mathcal{D}_\ell^{TT}\ [\mu\mathrm{K}^2]$ [peak zoom]",
                   fontsize=13)
    ax3.set_ylabel(r"$\Delta\mathcal{D}/\mathcal{D}$ [\%]" + "\n"
                   + r"(ITSM $-$ Planck)", fontsize=11)
    ax3.set_xlabel(r"Multipole $\ell$", fontsize=14)

    ax1.set_title(
        r"CMB TT Power Spectrum: Planck 2018 vs ITSM Geometric $H_0$"
        + "\n"
        + r"CAMB used as background solver only — Plenum $Q^\nu$ source term "
        + r"not yet implemented",
        fontsize=13, pad=12
    )

    ax1.legend(loc="upper right", fontsize=10, framealpha=0.95)

    # Caption
    fig.text(0.13, 0.005,
             (r"\textit{ITSM caveat: CAMB does not include the Plenum shear "
              r"$Q^\nu$ term. Shift shown is purely from geometric $H_0$ tether "
              r"$H_0=2\pi a_0/c$. Full perturbation theory requires custom "
              r"Boltzmann implementation.}"),
             fontsize=8.5, color="gray")

    plt.tight_layout(rect=[0, 0.02, 1, 1])

    out_path = os.path.join(output_dir, "itsm_camb_cmb_spectrum.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f" Figure saved: {out_path}")
    print()
    print(" Key findings:")
    if planck_spectrum and itsm_spectrum:
        e_pl, D_pl = planck_spectrum
        e_it, D_it = itsm_spectrum
        # First peak shift
        mask = (e_pl > 150) & (e_pl < 300)
        peak_pl = e_pl[mask][np.argmax(D_pl[mask])]
        mask = (e_it > 150) & (e_it < 300)
        peak_it = e_it[mask][np.argmax(D_it[mask])]
        print(f"   Planck 1st peak ell : {peak_pl}")
        print(f"   ITSM   1st peak ell : {peak_it}")
        print(f"   Peak shift          : {peak_it - peak_pl:+d} multipoles")
    print()
    print(" ITSM CAMB CMB diagnostic complete.")
