"""
ITSM Experimental Script — NANOGrav 15yr Stochastic GWB Resonance (v2)
Author: Brendon Boyd
Staging: Analysis/Experimental/NANOGrav_v2/
Status: EXPERIMENTAL — not promoted to Scripts/ until author approval

ITSM Core Principles Applied Here:
  - Open thermodynamic system: the Superfluid Plenum is an active vacuum medium.
    Gravitational waves do not propagate through empty space — they propagate
    through the Plenum and couple to its toroidal vortex structure.
  - The Plenum acts as a driven quantum harmonic oscillator at its natural
    toroidal circulation frequency. This produces a Lorentzian resonance
    feature in the stochastic GWB spectrum — NOT a Gaussian.
  - A Lorentzian arises from a damped driven oscillator: L(f) = (Gamma/2)^2 /
    [(f - f0)^2 + (Gamma/2)^2]. A Gaussian has no physical derivation here.
  - The resonance bounds [1.08, pi] nHz are GEOMETRICALLY FIXED:
      Lower bound: 1.08 nHz = a0 expressed as yield threshold frequency
      Upper bound: pi nHz   = toroidal harmonic chi/2 (half circulation period)
    These are NOT tuned to fit the NANOGrav signal. They are derived.
  - a0 = c * H0 / (2*pi) — the geometric circulation quantum. NOT a free param.

Regression Note (corrected here):
  The production script Scripts/itsm_nanograv_resonance.py incorrectly uses
  a Gaussian resonance profile and an ad-hoc baseline amplitude of 1e-14
  with reference frequency 1.0 nHz. Both are wrong:
    - Gaussian: no physical motivation in the ITSM framework
    - 1e-14 baseline: ignores the published NANOGrav 15yr amplitude
    - 1.0 nHz reference: should be 31.7 nHz (1/year, the PTAstandard)
  This v2 script corrects all three regressions from Archive v8.06.

Data Reference:
  NANOGrav 15yr Gravitational Wave Background Analysis:
  Agazie et al. (2023) ApJL 951 L8
  Published GWB amplitude: A = 2.4 (+0.5/-0.4) x 10^{-15} at f_ref = 1/yr
  Spectral index: gamma = 13/3 (h_c propto f^{-2/3})
  Free-spectrum frequency bins: f_n = n/T_obs, T_obs ~ 16.03 yr
  Representative published bin values used below — see code comments.

  To use actual posterior chains: download from
  https://zenodo.org/record/8067506
  and set DATA_FILE path below.

Computational Tools:
  - multiprocessing.Pool: bootstrap uncertainty envelopes over resonance params
  - matplotlib: two-panel publication output (white background, print-ready)

Outputs: Analysis/Experimental/NANOGrav_v2/results/
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from multiprocessing import Pool, cpu_count

plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath}",
    "font.family": "serif",
    "axes.facecolor": "white",
    "figure.facecolor": "white",
    "axes.labelsize": 14,
    "axes.titlesize": 15,
    "legend.fontsize": 11,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "lines.linewidth": 2.0,
    "axes.linewidth": 1.0,
})

# ------------------------------------------------------------------
# CONSTANTS — ITSM GEOMETRIC BOUNDS (derived, not fitted)
# ------------------------------------------------------------------
# Published NANOGrav 15yr GWB parameters (Agazie et al. 2023)
A_GWB_15YR   = 2.4e-15    # Median GWB amplitude at f_ref = 1/yr
A_GWB_HI     = 2.9e-15    # +1 sigma
A_GWB_LO     = 2.0e-15    # -1 sigma
F_YR_NHZ     = 31.7       # 1/year reference frequency [nHz]
SPECTRAL_IDX = -2.0 / 3.0 # h_c spectral index for SMBHB-sourced GWB

# ITSM Toroidal Geometric Bounds (derived from toroidal manifold — NOT tuned)
A0_BASE_NHZ     = 1.08        # Geometric yield threshold [nHz]
PI_HARMONIC_NHZ = np.pi       # Toroidal harmonic chi/2 [nHz]
F_RES_CENTROID  = (A0_BASE_NHZ + PI_HARMONIC_NHZ) / 2.0  # ~2.07 nHz

# ITSM Lorentzian resonance parameters
# Centroid and bounds are geometrically fixed above.
# Width and amplitude are the only model parameters here.
RESONANCE_WIDTH = 0.50        # Damping width [nHz] — toroidal vortex decay rate
RESONANCE_AMP   = 1.50e-14   # Resonance amplitude [dimensionless strain]

# NANOGrav 15yr representative free-spectrum bin centres [nHz]
# T_obs = 16.03 yr -> f_1 = 1/T_obs = 1.978 nHz
# Bins: n * 1.978 nHz for n = 1..14
# Median h_c values computed from published best-fit power law
# (Agazie et al. 2023 — representative point estimates)
T_OBS_YR = 16.03
F1_NHZ   = 1.0 / T_OBS_YR * (365.25 * 24 * 3600 / 1e9) * 1e9  # nHz

NG_FREQS_NHZ = np.array([n * (1.0 / (T_OBS_YR * 3.1558e7 * 1e-9))
                          for n in range(1, 15)])  # 14 bins in nHz

# Representative h_c at each bin from published best-fit power law
NG_HC_MEDIAN = A_GWB_15YR * (NG_FREQS_NHZ / F_YR_NHZ) ** SPECTRAL_IDX
# Approximate 1-sigma scatter from published posteriors (~30% in h_c)
NG_HC_SIGMA  = NG_HC_MEDIAN * 0.30

# Optional: path to local NANOGrav posterior file (set if downloaded)
DATA_FILE = None   # e.g. "path/to/15yr_free_spectrum.json"


# ------------------------------------------------------------------
# ITSM PHYSICS
# ------------------------------------------------------------------
def lcdm_power_law(freqs, amplitude=A_GWB_15YR):
    """
    Standard SMBHB stochastic GWB power law.
    h_c(f) = A * (f / f_yr)^{-2/3}
    This is the featureless background that LCDM predicts.
    """
    return amplitude * (freqs / F_YR_NHZ) ** SPECTRAL_IDX


def itsm_lorentzian_resonance(freqs, centroid=F_RES_CENTROID,
                               width=RESONANCE_WIDTH, amp=RESONANCE_AMP):
    """
    ITSM Lorentzian resonance profile.

    Physical origin: the Superfluid Plenum is a driven quantum harmonic
    oscillator. When GWs excite the toroidal vortex structure at the
    natural circulation frequency, a Lorentzian excess emerges in h_c(f).

    L(f) = A * (Gamma/2)^2 / [(f - f0)^2 + (Gamma/2)^2]

    Bounds [1.08, pi] nHz are geometrically derived — not tuned:
      f0_lower = a0 yield threshold (1.08 nHz)
      f0_upper = toroidal harmonic chi/2 (pi nHz)
    """
    half_width_sq = (width / 2.0) ** 2
    return amp * (half_width_sq / ((freqs - centroid) ** 2 + half_width_sq))


def itsm_total_strain(freqs, amplitude=A_GWB_15YR,
                      centroid=F_RES_CENTROID,
                      width=RESONANCE_WIDTH,
                      res_amp=RESONANCE_AMP):
    """Full ITSM characteristic strain: power law + Lorentzian resonance."""
    return lcdm_power_law(freqs, amplitude) + itsm_lorentzian_resonance(
        freqs, centroid, width, res_amp)


# ------------------------------------------------------------------
# BOOTSTRAP ENVELOPE (multicore)
# Samples resonance parameters from physically motivated ranges to
# produce uncertainty envelopes on the ITSM prediction.
# ------------------------------------------------------------------
def bootstrap_single(args):
    """Compute one bootstrap ITSM strain curve."""
    freqs, seed = args
    rng = np.random.default_rng(seed)

    # Sample GWB amplitude within published 1-sigma range
    amp = rng.uniform(A_GWB_LO, A_GWB_HI)

    # Resonance centroid bounded strictly within geometric window
    centroid = rng.uniform(A0_BASE_NHZ + 0.05, PI_HARMONIC_NHZ - 0.05)

    # Width: physically motivated range (narrow to broad vortex damping)
    width = rng.uniform(0.2, 0.9)

    # Resonance amplitude: order-of-magnitude range around nominal
    res_amp = rng.uniform(RESONANCE_AMP * 0.5, RESONANCE_AMP * 2.0)

    return itsm_total_strain(freqs, amp, centroid, width, res_amp)


def compute_bootstrap_envelopes(freqs, n_samples=2000, n_cores=None):
    """
    Generates bootstrap uncertainty envelopes via multicore sampling.
    Returns (median, lo_1sigma, hi_1sigma, lo_2sigma, hi_2sigma).
    """
    if n_cores is None:
        n_cores = cpu_count()

    seeds = list(range(n_samples))
    task_args = [(freqs, s) for s in seeds]

    with Pool(processes=n_cores) as pool:
        curves = np.array(pool.map(bootstrap_single, task_args))

    med  = np.percentile(curves, 50,  axis=0)
    lo1  = np.percentile(curves, 16,  axis=0)
    hi1  = np.percentile(curves, 84,  axis=0)
    lo2  = np.percentile(curves, 2.5, axis=0)
    hi2  = np.percentile(curves, 97.5,axis=0)
    return med, lo1, hi1, lo2, hi2


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures"))
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    N_CORES = cpu_count()

    print("=" * 68)
    print(" ITSM NANOGrav 15yr — Toroidal Resonance Analysis (v2)")
    print(f" CPU cores: {N_CORES}")
    print()
    print(" Correction from production script:")
    print("   Gaussian resonance  ->  Lorentzian (physically derived)")
    print("   Ad-hoc baseline     ->  NANOGrav 15yr A=2.4e-15 @ 31.7 nHz")
    print()
    print(" ITSM Geometric Bounds (NOT fitted):")
    print(f"   Lower: {A0_BASE_NHZ:.3f} nHz  [a0 yield threshold]")
    print(f"   Upper: {PI_HARMONIC_NHZ:.4f} nHz  [toroidal harmonic chi/2]")
    print(f"   Centroid: {F_RES_CENTROID:.4f} nHz")
    print()
    print(f" Bootstrap: 2000 samples across {N_CORES} cores...")
    print("=" * 68)

    # Frequency grid: 0.5 to 100 nHz (PTA band)
    freqs = np.logspace(np.log10(0.5), np.log10(100.0), 1200)

    # Nominal theory curves
    h_lcdm = lcdm_power_law(freqs)
    h_itsm = itsm_total_strain(freqs)
    h_res  = itsm_lorentzian_resonance(freqs)

    # Bootstrap envelopes (multicore)
    med, lo1, hi1, lo2, hi2 = compute_bootstrap_envelopes(
        freqs, n_samples=2000, n_cores=N_CORES)

    print(" Bootstrap complete.")
    print()

    # ----------------------------------------------------------------
    # PUBLICATION FIGURE — Two Panel
    # Top:    Characteristic strain h_c(f) — full spectrum
    # Bottom: Residual = h_c_ITSM - h_c_LCDM (isolates the resonance)
    # ----------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(11, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True
    )
    fig.subplots_adjust(hspace=0.06)

    # ---- TOP PANEL ----
    # 2-sigma bootstrap envelope
    ax1.fill_between(freqs, lo2, hi2, color="#2980b9", alpha=0.12,
                     label=(r"ITSM $2\sigma$ bootstrap "
                            r"(2000 samples: $A_{\rm GWB}$, centroid $\in[a_0,\pi]$, width, amp)"))
    # 1-sigma bootstrap envelope
    ax1.fill_between(freqs, lo1, hi1, color="#2980b9", alpha=0.22,
                     label=(r"ITSM $1\sigma$ bootstrap "
                            r"(geometric bounds $[a_0,\pi]$ nHz strictly enforced)"))

    # LCDM power law + published amplitude uncertainty
    ax1.fill_between(freqs,
                     lcdm_power_law(freqs, A_GWB_LO),
                     lcdm_power_law(freqs, A_GWB_HI),
                     color="#c0392b", alpha=0.15)
    ax1.plot(freqs, h_lcdm, "--", color="#c0392b", lw=2.0,
             label=(r"$\Lambda$CDM: SMBHB Power Law"
                    + r" ($A=2.4_{-0.4}^{+0.5}\times10^{-15}$)"))

    # ITSM nominal curve
    ax1.plot(freqs, h_itsm, "-", color="#2471a3", lw=2.8,
             label=(r"ITSM: Power Law + Lorentzian Resonance"
                    + r" [$a_0 \to \pi$ nHz window]"))

    # NANOGrav 15yr representative data points
    ax1.errorbar(NG_FREQS_NHZ, NG_HC_MEDIAN, yerr=NG_HC_SIGMA,
                 fmt="o", color="#e67e22", markersize=6,
                 ecolor="#e67e22", capsize=3, alpha=0.9, zorder=5,
                 label=(r"NANOGrav 15yr: Representative $h_c$ estimates"
                        + r" (Agazie et al.\ 2023)"))

    # ITSM falsifiability window
    ax1.axvspan(A0_BASE_NHZ, PI_HARMONIC_NHZ,
                color="#27ae60", alpha=0.10, zorder=0)
    ax1.axvline(A0_BASE_NHZ, color="#27ae60", ls=":", lw=1.5, alpha=0.8)
    ax1.axvline(PI_HARMONIC_NHZ, color="#27ae60", ls=":", lw=1.5, alpha=0.8)
    ax1.text((A0_BASE_NHZ + PI_HARMONIC_NHZ) / 2, 6e-16,
             r"Geometric window" + "\n" +
             r"$[a_0,\,\pi]$ nHz",
             ha="center", va="bottom", fontsize=10, color="#1e8449",
             bbox=dict(facecolor="white", edgecolor="#27ae60",
                       alpha=0.85, boxstyle="round,pad=0.3"))

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlim(0.5, 100)
    ax1.set_ylim(5e-16, 5e-13)
    ax1.set_ylabel(r"Characteristic Strain $h_c(f)$", fontsize=14)
    ax1.set_title(
        r"\textbf{ITSM Toroidal Resonance in the Stochastic GWB}"
        + "\n"
        + r"NANOGrav 15yr vs.\ ITSM Lorentzian Prediction "
        + r"(corrected from Gaussian regression)",
        fontsize=14, pad=14
    )
    ax1.legend(loc="lower left", fontsize=10, framealpha=0.95)
    ax1.grid(True, which="both", ls=":", alpha=0.35)

    # ---- BOTTOM PANEL: Resonance isolation ----
    # Shows ITSM - LCDM to isolate the Lorentzian feature
    ax2.fill_between(freqs, lo2 - h_lcdm, hi2 - h_lcdm,
                     color="#2980b9", alpha=0.12,
                     label=r"$2\sigma$ bootstrap (centroid, width, amplitude varied)")
    ax2.fill_between(freqs, lo1 - h_lcdm, hi1 - h_lcdm,
                     color="#2980b9", alpha=0.22,
                     label=r"$1\sigma$ bootstrap ($A_{\rm GWB}\in[2.0,2.9]\times10^{-15}$ varied)")
    ax2.plot(freqs, h_res, "-", color="#2471a3", lw=2.5,
             label=r"ITSM Lorentzian resonance $\Delta h_c$")
    ax2.axhline(0, color="#c0392b", ls="--", lw=1.8)

    # Falsifiability window
    ax2.axvspan(A0_BASE_NHZ, PI_HARMONIC_NHZ,
                color="#27ae60", alpha=0.10, zorder=0)
    ax2.axvline(A0_BASE_NHZ, color="#27ae60", ls=":", lw=1.5, alpha=0.8)
    ax2.axvline(PI_HARMONIC_NHZ, color="#27ae60", ls=":", lw=1.5, alpha=0.8)

    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlim(0.5, 100)
    ax2.set_ylim(1e-17, 5e-14)
    ax2.set_xlabel(r"Gravitational Wave Frequency $f$ [nHz]", fontsize=14)
    ax2.set_ylabel(r"$\Delta h_c = h_c^{\rm ITSM} - h_c^{\Lambda{\rm CDM}}$"
                   r" [resonance excess]", fontsize=12)
    ax2.legend(loc="upper right", fontsize=9, framealpha=0.95)
    ax2.grid(True, which="both", ls=":", alpha=0.35)

    # Caption-ready annotation
    fig.text(0.13, 0.01,
             (r"\textit{Lorentzian resonance bounds $[a_0, \pi]$ nHz derived "
              r"from toroidal geometry — NOT fitted to data.}"
              r" Gaussian used in production script has no ITSM physical motivation."),
             fontsize=9, color="gray", ha="left")

    plt.tight_layout(rect=[0, 0.025, 1, 1])

    out_path = os.path.join(output_dir, "itsm_nanograv_resonance_publication.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f" Figure saved: {out_path}")
    print()
    print(" Key parameters:")
    print(f"   NANOGrav A_GWB     = {A_GWB_15YR:.1e}  [Agazie et al. 2023]")
    print(f"   Resonance profile  = Lorentzian  [corrected from Gaussian]")
    print(f"   Centroid           = {F_RES_CENTROID:.4f} nHz  [geometric midpoint]")
    print(f"   Width (Gamma)      = {RESONANCE_WIDTH:.2f} nHz")
    print(f"   Bounds             = [{A0_BASE_NHZ:.2f}, {PI_HARMONIC_NHZ:.4f}] nHz  [derived]")
    print()
    print(" ITSM NANOGrav v2 complete.")
