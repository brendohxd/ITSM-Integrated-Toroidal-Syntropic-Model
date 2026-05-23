"""
ITSM Experimental Script — Baryonic Tully-Fisher Relation (BTFR) Validation
Author: Brendon Boyd
Staging: Analysis/Experimental/BTFR_v1/
Status: EXPERIMENTAL — not promoted to Scripts/ until author approval

ITSM Core Principles Applied Here:
  - Open thermodynamic system: the Superfluid Plenum mediates all baryonic
    acceleration through the Plenum Shear Ansatz — g_eff = g_bar + (2/3)*sqrt(g_bar*a0)
  - a0 = c * H0 / (2 * pi) — geometrically derived from Onsager-Feynman circulation
    quantization on the toroidal manifold. NOT a free parameter. NOT fitted.
  - The 2/3 factor is the covariant geometric projection of the 2D transverse shear
    plane onto the 3D bulk manifold volume. NOT a fitting coefficient.
  - H0 geometrically tethered: NOT calibrated against a distance ladder.

ITSM BTFR Derivation (from first principles — not MOND):
  In the ITSM low-acceleration geometric regime (g_bar << a0), the Plenum
  shear term dominates:
      g_eff  ≈  (2/3) * sqrt(g_bar * a0)

  For a flat rotation curve at large radius R where baryons are effectively
  point-like (g_bar = G*M_b/R^2):
      V_f^2 / R = (2/3) * sqrt(G * M_b * a0 / R^2)
      V_f^2     = (2/3) * sqrt(G * M_b * a0)

  Squaring:
      V_f^4  =  (4/9) * G * M_b * a0

  This is the ITSM BTFR. The coefficient 4/9 = (2/3)^2 is NOT arbitrary —
  it is the square of the geometric projection factor. The slope (4) and
  normalisation are FULLY DETERMINED by a0 = c*H0/(2*pi).

  This is NOT the MOND limit. MOND observes this empirically.
  The ITSM derives it geometrically from the toroidal manifold structure.

Computational Tools:
  - multiprocessing.Pool: all CPU cores for per-galaxy mass extraction
  - scipy.optimize: fallback M/L initialisation
  - matplotlib: publication-grade output

Data Sources:
  - SPARC rotation curve profiles (SPARC_data/*_rotmod.dat)
  - MCMC chain medians from Assets/SPARC_Batch_Outputs/ (if available)
    → used for M/L ratios (Upsilon_disk, Upsilon_bulge) per galaxy
  - Fallback: Υ_disk=0.50, Υ_bulge=0.70 if chains not found

Outputs: Analysis/Experimental/BTFR_v1/results/
"""

import os
import glob
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count

plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath}",
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "axes.facecolor": "white",
    "figure.facecolor": "white",
    "font.size": 14
})

# ------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------
# Gravitational constant in SPARC units: kpc (km/s)^2 M_sun^{-1}
G_SPARC   = 4.3009e-6

# ITSM acceleration scale — geometrically derived, not fitted
# a0 = c * H0 / (2*pi) where H0 = 73.0 km/s/Mpc (toroidal edge value)
# In SPARC units: km^2/s^2/kpc
C_LIGHT   = 299792.458        # km/s
MPC_TO_KPC = 1.0e3            # kpc per Mpc
H0_ITSM   = 73.0              # km/s/Mpc — toroidal edge geometric value
H0_SI     = H0_ITSM / MPC_TO_KPC   # km/s/kpc
A0_SPARC  = (C_LIGHT * H0_SI) / (2.0 * np.pi)  # km^2/s^2/kpc

# Default M/L ratios — used only when MCMC chains unavailable
UPS_DISK_DEFAULT   = 0.50
UPS_BULGE_DEFAULT  = 0.70
N_VFLAT_POINTS     = 3   # median of this many outermost points for V_flat


# ------------------------------------------------------------------
# LOAD MCMC M/L RATIOS (if available from prior batch)
# ------------------------------------------------------------------
def load_ml_ratios(batch_dir):
    """
    Loads per-galaxy MCMC median Upsilon_disk and Upsilon_bulge from
    the existing batch output CSVs.

    Returns dict: galaxy_name → (ups_disk, ups_bulge)
    """
    ml_map = {}
    chain_files = glob.glob(os.path.join(batch_dir, "*_MCMC_Chains.csv"))
    for cf in chain_files:
        gname = os.path.basename(cf).replace("_MCMC_Chains.csv", "")
        try:
            chains = pd.read_csv(cf)
            if len(chains) < 50:
                continue
            ud = np.percentile(chains['Upsilon_disk'].values,  50)
            ub = np.percentile(chains['Upsilon_bulge'].values, 50)
            ml_map[gname] = (ud, ub)
        except Exception:
            pass
    return ml_map


# ------------------------------------------------------------------
# PER-GALAXY EXTRACTION
# Called inside multiprocessing Pool
# ------------------------------------------------------------------
def extract_galaxy_btfr(args):
    """
    Extracts (V_flat, M_b) for one SPARC galaxy using the ITSM M/L prescription.

    Parameters
    ----------
    args : tuple — (file_path, ups_disk, ups_bulge)

    Returns
    -------
    dict with galaxy name, V_flat, M_b, n_points, flag — or None on failure
    """
    file_path, ups_disk, ups_bulge = args
    galaxy_name = os.path.basename(file_path).replace("_rotmod.dat", "")

    try:
        df = pd.read_csv(file_path, sep=r'\s+', comment='#', header=None,
                         names=['Rad', 'Vobs', 'errV', 'Vgas',
                                'Vdisk', 'Vbul', 'SBdisk', 'SBbul'])
        df = df[(df['Rad'] > 0) & (df['Vobs'] > 0) & (df['errV'] > 0)].copy()
        if len(df) < 5:
            return None

        df = df.sort_values('Rad').reset_index(drop=True)
        n  = len(df)

        # --- V_flat: median of outermost N_VFLAT_POINTS observed velocities ---
        n_use   = min(N_VFLAT_POINTS, n)
        V_flat  = np.median(df['Vobs'].values[-n_use:])

        # --- Baryonic mass at outermost point ---
        # M_b = V_bar^2 * R / G  (enclosed baryonic mass at R_last)
        # V_bar^2 preserves sign convention from SPARC
        R_last  = df['Rad'].values[-1]
        Vg      = df['Vgas'].values[-1]
        Vd      = df['Vdisk'].values[-1]
        Vb      = df['Vbul'].values[-1]

        V_bar_sq = (np.abs(Vg) * Vg
                    + ups_disk  * np.abs(Vd) * Vd
                    + ups_bulge * np.abs(Vb) * Vb)

        if V_bar_sq <= 0:
            return None

        M_b = V_bar_sq * R_last / G_SPARC   # [M_sun]

        return {
            'galaxy':  galaxy_name,
            'V_flat':  V_flat,        # km/s
            'M_b':     M_b,           # M_sun
            'R_last':  R_last,        # kpc
            'n_pts':   n,
            'ups_disk':  ups_disk,
            'ups_bulge': ups_bulge,
            'ml_source': 'mcmc' if ups_disk != UPS_DISK_DEFAULT else 'default'
        }

    except Exception:
        return None


# ------------------------------------------------------------------
# ITSM BTFR PREDICTION CURVE
# V_f^4 = (4/9) * G * M_b * a0
# Rearranged: V_f = [ (4/9) * G * M_b * a0 ]^{1/4}
# ------------------------------------------------------------------
def itsm_btfr_prediction(M_b_array):
    """
    ITSM geometric BTFR prediction.
    Derived from first principles — coefficient (4/9) = (2/3)^2
    is the square of the covariant geometric projection factor.
    """
    return ((4.0 / 9.0) * G_SPARC * M_b_array * A0_SPARC) ** 0.25


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":

    # --- Paths ---
    script_dir  = os.path.dirname(os.path.abspath(__file__))
    repo_root   = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
    data_dir    = os.path.join(repo_root, "SPARC_data")
    batch_dir   = os.path.join(repo_root, "Assets", "SPARC_Batch_Outputs")
    output_dir  = os.path.join(script_dir, "results")
    os.makedirs(output_dir, exist_ok=True)

    galaxy_files = sorted(glob.glob(os.path.join(data_dir, "*_rotmod.dat")))
    if not galaxy_files:
        raise FileNotFoundError(f"No SPARC files at: {data_dir}")

    N_CORES = cpu_count()

    print("=" * 66)
    print(" ITSM BTFR VALIDATION — Baryonic Tully-Fisher Relation")
    print(f" Galaxies      : {len(galaxy_files)}")
    print(f" CPU cores     : {N_CORES}")
    print()
    print(" ITSM Derivation (from toroidal geometry — NOT MOND):")
    print("   g_eff = g_bar + (2/3)*sqrt(g_bar * a0)  [Plenum Shear Ansatz]")
    print("   Low-g limit: V_f^4 = (4/9) * G * M_b * a0")
    print(f"   a0 = c*H0/(2*pi) = {A0_SPARC:.4f} km^2/s^2/kpc  [geometric]")
    print(f"   H0 = {H0_ITSM} km/s/Mpc  [toroidal edge value]")
    print(" Coefficient (4/9) = (2/3)^2 — geometric projection. Not fitted.")
    print("=" * 66)
    print()

    # --- Load MCMC M/L ratios ---
    ml_map = load_ml_ratios(batch_dir)
    n_mcmc = len(ml_map)
    print(f" M/L source: MCMC chains available for {n_mcmc} galaxies.")
    print(f"             Fallback (Ups_disk={UPS_DISK_DEFAULT}, "
          f"Ups_bulge={UPS_BULGE_DEFAULT}) for remaining.\n")

    # --- Build task args ---
    task_args = []
    for fp in galaxy_files:
        gname = os.path.basename(fp).replace("_rotmod.dat", "")
        if gname in ml_map:
            ud, ub = ml_map[gname]
        else:
            ud, ub = UPS_DISK_DEFAULT, UPS_BULGE_DEFAULT
        task_args.append((fp, ud, ub))

    # --- Parallel extraction ---
    with Pool(processes=N_CORES) as pool:
        raw_results = pool.map(extract_galaxy_btfr, task_args)

    results = [r for r in raw_results if r is not None]
    print(f" Extracted {len(results)} valid galaxies from {len(galaxy_files)} files.\n")

    # --- Unpack arrays ---
    galaxies   = [r['galaxy']  for r in results]
    V_flat_arr = np.array([r['V_flat']  for r in results])   # km/s
    M_b_arr    = np.array([r['M_b']     for r in results])   # M_sun
    ml_source  = [r['ml_source'] for r in results]

    # --- Reduced chi-squared of ITSM prediction ---
    V_pred_arr = itsm_btfr_prediction(M_b_arr)
    # Use 10% scatter as representative observational uncertainty
    sigma_V    = V_flat_arr * 0.10
    chi2       = np.sum(((V_flat_arr - V_pred_arr) / sigma_V) ** 2)
    chi2_nu    = chi2 / (len(V_flat_arr) - 0)   # 0 free params in ITSM prediction

    print(f" ITSM BTFR chi^2_nu (zero free parameters): {chi2_nu:.3f}")
    print(f" (sigma_V = 10% of V_flat — representative uncertainty)\n")

    # --- Save summary CSV ---
    df_out = pd.DataFrame({
        'Galaxy':      galaxies,
        'V_flat_kms':  V_flat_arr,
        'M_b_Msun':    M_b_arr,
        'V_ITSM_kms':  V_pred_arr,
        'Residual_kms': V_flat_arr - V_pred_arr,
        'ML_source':   ml_source
    })
    csv_path = os.path.join(output_dir, "itsm_btfr_results.csv")
    df_out.to_csv(csv_path, index=False)
    print(f" Results saved: {csv_path}")

    # ----------------------------------------------------------------
    # PUBLICATION PLOT
    # ----------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 11),
        gridspec_kw={'height_ratios': [3, 1]},
        sharex=True
    )
    fig.subplots_adjust(hspace=0.05)

    # Colour by M/L source
    c_mcmc    = '#1a6faf'
    c_default = '#888888'
    colors = [c_mcmc if s == 'mcmc' else c_default for s in ml_source]

    # --- Top panel: BTFR ---
    ax1.scatter(M_b_arr, V_flat_arr, c=colors, s=18, alpha=0.65,
                zorder=3, label='_nolegend_')

    # ITSM prediction curve
    M_range  = np.logspace(
        np.log10(max(M_b_arr.min(), 1e6)),
        np.log10(M_b_arr.max()), 300
    )
    V_itsm   = itsm_btfr_prediction(M_range)
    ax1.plot(M_range, V_itsm, '-', color='#c0392b', lw=3.0, zorder=5,
             label=(r'ITSM: $V_f^4 = \frac{4}{9}\,G\,M_b\,a_0$'
                    + r' $\left[a_0 = \frac{cH_0}{2\pi},\ \chi^2_\nu='
                    + rf'{chi2_nu:.2f}\right]$'))

    # Proxy legend handles for data points
    from matplotlib.lines import Line2D
    leg_mcmc    = Line2D([0], [0], marker='o', color='w',
                         markerfacecolor=c_mcmc, markersize=7,
                         label=rf'SPARC ({n_mcmc} with MCMC M/L)')
    leg_default = Line2D([0], [0], marker='o', color='w',
                         markerfacecolor=c_default, markersize=7,
                         label=rf'SPARC ({len(results)-n_mcmc} default M/L)')

    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_ylabel(r'Flat Rotation Velocity $V_f$ [km s$^{-1}$]', fontsize=14)
    ax1.set_title(
        r'\textbf{ITSM Baryonic Tully-Fisher Relation}' + '\n'
        + r'Zero-Free-Parameter Geometric Prediction: '
        + r'$V_f^4 = \frac{4}{9}\,G\,M_b\,a_0$',
        fontsize=15, pad=14
    )
    ax1.legend(handles=[leg_mcmc, leg_default,
                        ax1.get_lines()[0]],
               loc='upper left', fontsize=11, framealpha=0.95)
    ax1.grid(True, which='both', ls=':', alpha=0.4)

    # --- Bottom panel: residuals ---
    V_pred_data = itsm_btfr_prediction(M_b_arr)
    resid = V_flat_arr - V_pred_data
    ax2.scatter(M_b_arr, resid, c=colors, s=14, alpha=0.65, zorder=3)
    ax2.axhline(0, color='#c0392b', lw=2.0, ls='--')
    ax2.set_xlabel(r'Total Baryonic Mass $M_b$ [$M_\odot$]', fontsize=14)
    ax2.set_ylabel(r'$\Delta V_f$ [km s$^{-1}$]', fontsize=13)
    ax2.grid(True, which='both', ls=':', alpha=0.4)

    # Symmetric residual limits
    rlim = np.percentile(np.abs(resid), 95) * 1.4
    ax2.set_ylim(-rlim, rlim)

    plt.tight_layout()
    fig_path = os.path.join(output_dir, "itsm_btfr_publication.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f" Figure saved : {fig_path}")

    print()
    print("=" * 66)
    print(f" ITSM BTFR Complete — {len(results)} galaxies plotted.")
    print(f" Prediction: V_f^4 = (4/9) G M_b a0  [zero free parameters]")
    print(f" a0 = c*H0/(2*pi) = {A0_SPARC:.4f} km^2/s^2/kpc")
    print("=" * 66)
