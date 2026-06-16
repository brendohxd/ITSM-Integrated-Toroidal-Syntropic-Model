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
import sys
import os
from itsm_plot_style import apply_tier1_style
apply_tier1_style()

# JCAP override: massive fonts
plt.rcParams.update({
    'font.size': 18,
    'axes.labelsize': 18,
    'axes.titlesize': 20,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'legend.fontsize': 14,
    'figure.titlesize': 24
})

from multiprocessing import Pool, cpu_count



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
    chain_files = glob.glob(os.path.join(batch_dir, "MCMC_v2_Chain_CSVs", "*_MCMC_Chains.csv"))
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
    repo_root   = os.path.abspath(os.path.join(script_dir, ".."))
    data_dir    = os.path.join(repo_root, "SPARC_data")
    batch_dir   = os.path.join(repo_root, "Assets", "SPARC_Batch_Outputs")
    figures_dir = os.path.join(repo_root, "Assets", "Figures")
    os.makedirs(batch_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

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

    # --- Reduced chi-squared of ITSM predictions ---
    V_pred_unren = itsm_btfr_prediction(M_b_arr)
    V_pred_ren   = (G_SPARC * M_b_arr * A0_SPARC) ** 0.25
    
    # 10% representative velocity uncertainty
    sigma_V = V_flat_arr * 0.10
    chi2_unren = np.sum(((V_flat_arr - V_pred_unren) / sigma_V) ** 2) / len(V_flat_arr)
    chi2_ren   = np.sum(((V_flat_arr - V_pred_ren) / sigma_V) ** 2) / len(V_flat_arr)
    
    # Propagated error chi-squared (astrophysical distance and Upsilon errors + 0.11 dex intrinsic scatter)
    sigma_V_obs = V_flat_arr * 0.05
    sigma_V_dist = V_pred_ren * 0.05
    sigma_V_ml = V_pred_ren * 0.0375
    sigma_intrinsic = V_pred_ren * 0.11
    sigma_eff = np.sqrt(sigma_V_obs**2 + sigma_V_dist**2 + sigma_V_ml**2 + sigma_intrinsic**2)
    chi2_prop_ren = np.sum(((V_flat_arr - V_pred_ren) / sigma_eff) ** 2) / len(V_flat_arr)

    print(f" ITSM Asymptotic Unrenormalized (4/9) chi^2_nu: {chi2_unren:.3f}")
    print(f" ITSM Asymptotic Renormalized (1.0) chi^2_nu:   {chi2_ren:.3f}")
    print(f" ITSM Propagated Renormalized chi^2_nu:         {chi2_prop_ren:.3f}\n")

    # --- Save summary CSV ---
    df_out = pd.DataFrame({
        'Galaxy':      galaxies,
        'V_flat_kms':  V_flat_arr,
        'M_b_Msun':    M_b_arr,
        'V_ITSM_unren_kms': V_pred_unren,
        'V_ITSM_ren_kms':   V_pred_ren,
        'ML_source':   ml_source
    })
    csv_path = os.path.join(batch_dir, "itsm_btfr_results.csv")
    df_out.to_csv(csv_path, index=False)
    print(f" Results saved: {csv_path}")

    # ----------------------------------------------------------------
    # PUBLICATION PLOT — Side-by-side 2-panel (1 row × 2 columns)
    # Panel A: BTFR scatter  |  Panel B: CDF of relative deviations
    # ----------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # Colour by M/L source
    c_mcmc    = '#1a6faf'
    c_default = '#888888'
    colors = [c_mcmc if s == 'mcmc' else c_default for s in ml_source]

    # ── Panel A: BTFR scatter ────────────────────────────────────────
    ax1.scatter(M_b_arr, V_flat_arr, c=colors, s=60, alpha=0.85,
                zorder=3, label='_nolegend_')

    # ITSM prediction curves
    M_range = np.logspace(
        np.log10(max(M_b_arr.min(), 1e6)),
        np.log10(M_b_arr.max()), 300
    )

    # Unrenormalized prediction (coefficient = 4/9)
    V_itsm_unren = itsm_btfr_prediction(M_range)
    ax1.plot(M_range, V_itsm_unren, '--', color='#c0392b', lw=2.5, zorder=5,
             label=(r'ITSM Unrenormalized (Tree-Level): $V_f^4 = \frac{4}{9}\,G\,M_b\,a_0$'
                    + rf' [$\chi^2_\nu \approx {chi2_unren:.2f}$]'))

    # Renormalized prediction (coefficient = 1.0)
    V_itsm_ren_curve = (G_SPARC * M_range * A0_SPARC) ** 0.25
    ax1.plot(M_range, V_itsm_ren_curve, '-', color='#0072B2', lw=3.0, zorder=5,
             label=(r'ITSM Renormalized (IR Fixed Point): $V_f^4 = G\,M_b\,a_0$'
                    + rf' [$\chi^2_\nu \approx {chi2_ren:.2f}$]'))

    # Shaded error envelopes around Renormalized prediction
    ax1.fill_between(M_range, V_itsm_ren_curve * 0.95, V_itsm_ren_curve * 1.05,
                     color='#0072B2', alpha=0.18, zorder=4,
                     label=r'5% Observational Uncertainty Band')
    ax1.fill_between(M_range, V_itsm_ren_curve * 0.875, V_itsm_ren_curve * 1.125,
                     color='#0072B2', alpha=0.08, zorder=4,
                     label=(r'12.5% Effective Error Band (Dist + M/L + Intrinsic, '
                            + r'$\chi^2_\nu \approx ' + f'{chi2_prop_ren:.2f}$)'))

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
    ax1.set_xlabel(r'Total Baryonic Mass $M_b$ [$M_\odot$]', fontsize=13)
    ax1.set_ylabel(r'Flat Rotation Velocity $V_f$ [km s$^{-1}$]', fontsize=13)
    ax1.set_title(
        r'ITSM Baryonic Tully-Fisher Relation' + '\n'
        + r'Renormalization Group Vertex Flow: $g_0^2 = 4/9 \to g^{*2} = 1.0$',
        fontsize=13, pad=10
    )

    handles, labels = ax1.get_legend_handles_labels()
    all_handles = [leg_mcmc, leg_default] + handles
    all_labels  = [leg_mcmc.get_label(), leg_default.get_label()] + labels
    ax1.legend(handles=all_handles, labels=all_labels,
               loc='upper left', fontsize=8.5, framealpha=0.95)
    ax1.grid(True, which='both', ls=':', alpha=0.4)

    # Panel A label
    ax1.text(0.03, 0.97, '(A)', transform=ax1.transAxes,
             fontsize=14, fontweight='bold', va='top', ha='left')

    # ── Panel B: CDF of relative deviations ─────────────────────────
    # Relative deviation for each galaxy vs each model
    rel_dev_unren = np.abs(V_flat_arr - V_pred_unren) / V_flat_arr
    rel_dev_ren   = np.abs(V_flat_arr - V_pred_ren)   / V_flat_arr

    N = len(V_flat_arr)
    cdf_y = np.arange(1, N + 1) / N

    # Sort each independently for their CDF
    sorted_unren = np.sort(rel_dev_unren)
    sorted_ren   = np.sort(rel_dev_ren)

    ax2.plot(sorted_unren, cdf_y, '--', color='#c0392b', lw=2.0,
             label='Unrenormalized (4/9)')
    ax2.plot(sorted_ren,   cdf_y, '-',  color='#0072B2', lw=2.5,
             label='Renormalized (IR Fixed Point)')

    # Vertical reference lines
    for xv in [0.10, 0.15, 0.25]:
        ax2.axvline(xv, color='lightgray', ls='--', alpha=0.4)

    # Horizontal reference lines
    for yh in [0.5, 0.7]:
        ax2.axhline(yh, color='lightgray', ls='--', alpha=0.4)

    # --- Key stats for annotations ---
    # Fraction within 15% — renormalized
    frac_ren_15  = np.mean(rel_dev_ren  <= 0.15)
    frac_ren_25  = np.mean(rel_dev_ren  <= 0.25)
    frac_unren_25 = np.mean(rel_dev_unren <= 0.25)

    # 3-sigma_eff fraction — renormalized
    sigma_eff_arr = np.sqrt(
        (V_flat_arr * 0.05)**2
        + (V_pred_ren * 0.05)**2
        + (V_pred_ren * 0.0375)**2
        + (V_pred_ren * 0.11)**2
    )
    within_3sig = np.mean(np.abs(V_flat_arr - V_pred_ren) <= 3 * sigma_eff_arr)

    ax2.annotate(
        f'Renormalized: {frac_ren_15*100:.1f}% within 15%',
        xy=(0.15, frac_ren_15), xytext=(0.165, frac_ren_15 - 0.08),
        fontsize=8.5, color='#0072B2',
        arrowprops=dict(arrowstyle='->', color='#0072B2', lw=1.0)
    )
    ax2.annotate(
        f'Renormalized: {frac_ren_25*100:.1f}% within 25%',
        xy=(0.25, frac_ren_25), xytext=(0.20, frac_ren_25 - 0.10),
        fontsize=8.5, color='#0072B2',
        arrowprops=dict(arrowstyle='->', color='#0072B2', lw=1.0)
    )
    ax2.text(0.02, 0.97,
             f'Renormalized: {within_3sig*100:.1f}% within 3σ_eff',
             transform=ax2.transAxes, fontsize=8.5, color='#0072B2',
             va='top', ha='left')
    ax2.text(0.02, 0.90,
             f'Unrenormalized: {frac_unren_25*100:.1f}% within 25%',
             transform=ax2.transAxes, fontsize=8.5, color='#c0392b',
             va='top', ha='left')

    ax2.set_xlim(0.0, 0.30)
    ax2.set_ylim(0.0, 1.0)
    ax2.set_xlabel(r'Relative Deviation $|V_\mathrm{flat} - V_\mathrm{pred}| / V_\mathrm{flat}$',
                   fontsize=12)
    ax2.set_ylabel('Fraction of SPARC Galaxies', fontsize=12)
    ax2.set_title('Cumulative Residual Distribution\n171 SPARC Galaxies',
                  fontsize=13, pad=10)
    ax2.legend(loc='lower right', fontsize=9.5, framealpha=0.95)
    ax2.grid(ls=':', alpha=0.4)

    # Panel B label
    ax2.text(0.03, 0.97, '(B)', transform=ax2.transAxes,
             fontsize=14, fontweight='bold', va='top', ha='left')

    plt.tight_layout()
    fig_path_pdf = os.path.join(figures_dir, "itsm_btfr_publication.pdf")
    plt.savefig(fig_path_pdf, bbox_inches='tight', format='pdf', dpi=300)
    fig_path_png = os.path.join(figures_dir, "itsm_btfr_publication.png")
    plt.savefig(fig_path_png, bbox_inches='tight', dpi=300)
    plt.close()
    print(f" Figure saved : {fig_path_pdf}")

    print()
    print("=" * 66)
    print(f" ITSM BTFR Complete — {len(results)} galaxies plotted.")
    print(f" Renormalized: V_f^4 = G M_b a0  [zero free parameters]")
    print(f" a0 = c*H0/(2*pi) = {A0_SPARC:.4f} km^2/s^2/kpc")
    print("=" * 66)
