"""
ITSM Production Script — Multicore SPARC MCMC Batch Processor
Author: Brendon Boyd
Status: PRODUCTION — Live in Scripts/ (promoted from Analysis/Experimental/MCMC_v2/)

ITSM Core Principles Applied Here:
  - Open thermodynamic system: the vacuum is a Superfluid Plenum, not empty space.
  - a0 = c * H0 / (2 * pi) — geometrically derived from Onsager-Feynman circulation
    quantization on the toroidal manifold. NOT a free parameter.
  - H0 is geometrically tethered via a0. We are NOT measuring H0 from galaxies.
    We are testing whether the geometric tether a0 = c*H0/(2*pi) is consistent
    across the SPARC sample.
  - The 2/3 factor is the covariant geometric projection of the 2D transverse shear
    plane onto the 3D bulk manifold volume. NOT a fitting coefficient.
  - g_eff = g_bar + (2/3) * sqrt(g_bar * a0)  — the Plenum Shear Ansatz.

Computational Tools:
  - emcee: ensemble sampler for per-galaxy posterior
  - multiprocessing.Pool: all CPU cores utilised (cpu_count() auto-detected)
  - MANDATORY Windows guard: all execution inside if __name__ == "__main__"

Outputs: Assets/SPARC_Batch_Outputs/
"""

import os
import glob
import numpy as np
import pandas as pd
import emcee
import corner
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend — safe for multicore on Windows
import matplotlib.pyplot as plt
import sys
import os
from itsm_plot_style import apply_tier1_style
apply_tier1_style()
from scipy.optimize import minimize
from multiprocessing import Pool, cpu_count



# ------------------------------------------------------------------
# ABSOLUTE SI CONVERSION CONSTANTS
# ------------------------------------------------------------------
KPC_TO_M   = 3.085677581e19   # metres per kiloparsec
MPC_TO_M   = 3.085677581e22   # metres per megaparsec
C_LIGHT    = 299792458.0      # speed of light [m/s]

# ------------------------------------------------------------------
# ITSM PHYSICS ENGINE
# The Plenum Shear Ansatz — canonical formula, locked.
# g_eff = g_bar + (2/3) * sqrt(g_bar * a0)
# a0    = c * H0 / (2 * pi)   [geometrically derived, not fitted]
# ------------------------------------------------------------------
def compute_itsm_velocity(R_kpc, V_gas, V_disk, V_bulge,
                          ups_disk, ups_bulge, H0_kms_mpc):
    """
    Computes the ITSM predicted rotation velocity via the Plenum Shear Ansatz.

    Parameters
    ----------
    R_kpc       : array, galactocentric radii [kpc]
    V_gas       : array, gas velocity profile [km/s]
    V_disk      : array, stellar disk profile [km/s]
    V_bulge     : array, bulge profile [km/s]
    ups_disk    : float, disk mass-to-light ratio
    ups_bulge   : float, bulge mass-to-light ratio
    H0_kms_mpc  : float, Hubble parameter [km/s/Mpc] — sets a0 via geometry

    Returns
    -------
    V_calc_km_s : array, ITSM predicted rotation velocity [km/s]
    """
    R_m = R_kpc * KPC_TO_M

    # Baryonic velocity squared [km^2/s^2] — preserves sign convention
    V_bar_sq = (V_gas   * np.abs(V_gas)
              + ups_disk  * V_disk  * np.abs(V_disk)
              + ups_bulge * V_bulge * np.abs(V_bulge))
    V_bar_sq = np.maximum(V_bar_sq, 0.0)

    # Convert to SI [m^2/s^2]
    V_bar_m_s = V_bar_sq * 1.0e6

    # Baryonic centripetal acceleration [m/s^2]
    g_bar = V_bar_m_s / R_m

    # Geometric tether: a0 derived from H0 — NOT fitted
    H0_si = (H0_kms_mpc * 1.0e3) / MPC_TO_M
    a0    = (C_LIGHT * H0_si) / (2.0 * np.pi)

    # Plenum Shear Ansatz [m/s^2]
    # The 2/3 is the covariant geometric projection factor — not arbitrary
    g_eff = g_bar + (2.0 / 3.0) * np.sqrt(g_bar * a0)

    V_calc_m_s  = np.sqrt(g_eff * R_m)
    V_calc_km_s = V_calc_m_s / 1.0e3
    return V_calc_km_s


# ------------------------------------------------------------------
# MCMC PROBABILITY FUNCTIONS
# ------------------------------------------------------------------
def log_prior(theta):
    """
    Agnostic boundary protocol — wide priors to avoid standard-paradigm truncation.
    H0 range [50, 100]: tests the geometric tether across the full Hubble tension span.
    ups bounds [0.01, 8.0]: physically motivated M/L range for spiral galaxies.
    """
    ups_disk, ups_bulge, H0 = theta
    if (0.01 < ups_disk  < 8.0 and
        0.00 < ups_bulge < 8.0 and
        50.0 < H0        < 100.0):
        return 0.0
    return -np.inf


def log_likelihood(theta, R, Vobs, errV, Vgas, Vdisk, Vbulge):
    ups_disk, ups_bulge, H0 = theta
    V_model  = compute_itsm_velocity(R, Vgas, Vdisk, Vbulge,
                                     ups_disk, ups_bulge, H0)
    sigma_sq = errV ** 2
    return -0.5 * np.sum(
        ((Vobs - V_model) ** 2) / sigma_sq
        + np.log(2.0 * np.pi * sigma_sq)
    )


def log_probability(theta, R, Vobs, errV, Vgas, Vdisk, Vbulge):
    lp = log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta, R, Vobs, errV, Vgas, Vdisk, Vbulge)


# ------------------------------------------------------------------
# DATA LOADER
# ------------------------------------------------------------------
def load_sparc_galaxy(file_path):
    """Parses standard SPARC rotation curve profiles."""
    data = pd.read_csv(file_path, sep=r'\s+', comment='#', header=None,
                       names=['R', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbulge'])
    return data.dropna().reset_index(drop=True)


# ------------------------------------------------------------------
# PER-GALAXY MCMC PIPELINE
# Designed to be called inside a multiprocessing Pool
# ------------------------------------------------------------------
def run_single_galaxy(args):
    """
    Runs the full ITSM MCMC pipeline for one SPARC galaxy.
    Packaged as a single-argument function for Pool.map compatibility.

    Parameters
    ----------
    args : tuple — (file_path, output_dir, n_walkers, n_steps, n_discard)
    """
    file_path, output_dir, n_walkers, n_steps, n_discard = args
    galaxy_name = os.path.basename(file_path).replace("_rotmod.dat", "")

    try:
        df = load_sparc_galaxy(file_path)
        if len(df) < 4:
            return f"SKIP {galaxy_name}: insufficient data points ({len(df)})"

        R      = df['R'].values
        Vobs   = df['Vobs'].values
        errV   = df['errV'].values
        Vgas   = df['Vgas'].values
        Vdisk  = df['Vdisk'].values
        Vbulge = df['Vbulge'].values

        # MAP initialisation via scipy — seeds MCMC walkers near the optimum
        nll    = lambda *a: -log_likelihood(*a)
        x0     = [0.5, 0.5, 70.0]
        bounds = [(0.01, 8.0), (0.00, 8.0), (50.0, 100.0)]
        soln   = minimize(nll, x0,
                          args=(R, Vobs, errV, Vgas, Vdisk, Vbulge),
                          bounds=bounds)

        ndim = 3
        pos  = soln.x + 1e-4 * np.random.randn(n_walkers, ndim)
        pos[:, 0] = np.clip(pos[:, 0], 0.01, 8.0)
        pos[:, 1] = np.clip(pos[:, 1], 0.00, 8.0)
        pos[:, 2] = np.clip(pos[:, 2], 50.0, 100.0)

        # NOTE: No pool= here — this function IS already running inside a
        # Pool worker. Nested multiprocessing causes deadlocks on Windows.
        sampler = emcee.EnsembleSampler(
            n_walkers, ndim, log_probability,
            args=(R, Vobs, errV, Vgas, Vdisk, Vbulge)
        )
        sampler.run_mcmc(pos, n_steps, progress=False)

        flat = sampler.get_chain(discard=n_discard, flat=True)
        
        try:
            tau = sampler.get_autocorr_time(quiet=True)
            tau_max = np.max(tau)
        except Exception:
            tau_max = np.nan

        labels  = [r"$\Upsilon_{\rm disk}$", r"$\Upsilon_{\rm bulge}$", r"$H_0$"]
        medians = np.percentile(flat, 50, axis=0)
        lo      = np.percentile(flat, 16, axis=0)
        hi      = np.percentile(flat, 84, axis=0)

        # Chi-squared at posterior median
        V_fit = compute_itsm_velocity(R, Vgas, Vdisk, Vbulge,
                                      medians[0], medians[1], medians[2])
        dof   = len(R) - ndim
        chi2  = np.sum(((Vobs - V_fit) / errV) ** 2)
        chi2n = chi2 / dof if dof > 0 else np.nan

        # --- Outputs ---
        safe = galaxy_name.replace('_', r'\_')

        # 1. Corner plot
        fig_c = corner.corner(flat, labels=labels, truths=medians,
                               quantiles=[0.16, 0.50, 0.84],
                               show_titles=True, title_fmt=".3f",
                               color="navy", truth_color="crimson")

    # Add Descriptive Elements
    fig_c.suptitle("SPARC Galaxy MCMC Rotation Curve Fit", fontsize=18, y=1.02)
    fig_c.text(0.6, 0.8, "Zero Free Global Parameters\nIndividual Halo Fits", fontsize=12,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', boxstyle='round,pad=0.5'))
    fig_c.savefig(os.path.join(output_dir, f"{galaxy_name}_corner.png"), dpi=150)

        plt.close(fig_c)

        # 2. Rotation curve + residuals
        fig_r, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(10, 8), sharex=True,
            gridspec_kw={'height_ratios': [3, 1]}
        )
        fig_r.subplots_adjust(hspace=0.05)

        ax1.errorbar(R, Vobs, yerr=errV, fmt='ok', capsize=3, alpha=0.8,
                     label='SPARC Observed')
        inds = np.random.randint(len(flat), size=80)
        for ind in inds:
            s = flat[ind]
            ax1.plot(R,
                     compute_itsm_velocity(R, Vgas, Vdisk, Vbulge, s[0], s[1], s[2]),
                     color='crimson', alpha=0.025)
        ax1.plot(R, V_fit, '-', color='crimson', lw=2.5,
                 label=rf'ITSM Plenum Shear Ansatz ($H_0={medians[2]:.2f}$)')
        ax1.set_ylabel(r'Orbital Velocity $V$ [km s$^{-1}$]', fontsize=13)
        ax1.set_title(
            r'ITSM Rotation Curve: ' + safe + r'' + '\n'
            + rf'$\chi^2_\nu = {chi2n:.3f}$ | '
            + rf'$\Upsilon_{{disk}}={medians[0]:.3f}$ | '
            + rf'$H_0={medians[2]:.2f}$ km/s/Mpc',
            fontsize=14, pad=12
        )
        ax1.legend(fontsize=11, loc='lower right')
        ax1.grid(True, ls=':', alpha=0.5)

        resid = Vobs - V_fit
        ax2.errorbar(R, resid, yerr=errV, fmt='ok', capsize=3, alpha=0.8)
        ax2.axhline(0, color='crimson', ls='--', lw=2)
        ax2.set_xlabel(r'Galactocentric Radius $R$ [kpc]', fontsize=13)
        ax2.set_ylabel(r'Residual [km s$^{-1}$]', fontsize=13)
        ax2.grid(True, ls=':', alpha=0.5)
        lim = np.max(np.abs(resid) + errV) * 1.3 if len(resid) > 0 else 10.0
        ax2.set_ylim(-lim, lim)

        plt.tight_layout()
        fig_r.savefig(os.path.join(output_dir, f"{galaxy_name}_rotation_curve.png"), dpi=150)
        plt.close(fig_r)

        # 3. Chain CSV
        pd.DataFrame(flat, columns=['Upsilon_disk', 'Upsilon_bulge', 'H0']).to_csv(
            os.path.join(output_dir, f"{galaxy_name}_MCMC_Chains.csv"), index=False
        )

        return (f"OK  {galaxy_name:30s}  "
                f"H0={medians[2]:.2f} (+{hi[2]-medians[2]:.2f}/-{medians[2]-lo[2]:.2f})  "
                f"chi2_nu={chi2n:.3f}  tau_max={tau_max:.1f}")

    except Exception as exc:
        return f"FAIL {galaxy_name}: {exc}"


# ------------------------------------------------------------------
# MAIN — ALL-CORE BATCH EXECUTION
# Windows multiprocessing REQUIRES the if __name__ == "__main__" guard.
# Without it, every spawned worker re-imports and re-executes the module,
# causing an infinite process fork explosion.
# ------------------------------------------------------------------
if __name__ == "__main__":

    # --- Paths ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root  = os.path.abspath(os.path.join(script_dir, ".."))
    data_dir   = os.path.join(repo_root, "SPARC_data")
    output_dir = os.path.join(repo_root, "Assets", "SPARC_Batch_Outputs")
    os.makedirs(output_dir, exist_ok=True)

    galaxy_files = sorted(glob.glob(os.path.join(data_dir, "*_rotmod.dat")))
    if not galaxy_files:
        raise FileNotFoundError(
            f"No SPARC *_rotmod.dat files found at:\n  {data_dir}"
        )

    # --- MCMC Configuration ---
    N_WALKERS = 32     # ensemble walkers — must be >= 2 * ndim (6)
    N_STEPS   = 3000   # total steps per walker (publication quality)
    N_DISCARD = 600    # burn-in steps discarded (20% of total)

    # --- Core Detection ---
    N_CORES = cpu_count()
    print("=" * 62)
    print(" ITSM MULTICORE MCMC BATCH ENGINE")
    print(f" Galaxies loaded : {len(galaxy_files)}")
    print(f" CPU cores       : {N_CORES}")
    print(f" Walkers         : {N_WALKERS}")
    print(f" Steps / galaxy  : {N_STEPS}  (burn-in: {N_DISCARD})")
    print(f" Output dir      : {output_dir}")
    print("=" * 62)
    print()
    print(" ITSM Physics:")
    print("   g_eff = g_bar + (2/3) * sqrt(g_bar * a0)")
    print("   a0    = c * H0 / (2 * pi)  [geometrically derived]")
    print()

    # Build argument tuples for Pool.map
    task_args = [
        (fp, output_dir, N_WALKERS, N_STEPS, N_DISCARD)
        for fp in galaxy_files
    ]

    # --- Launch all-core pool ---
    # Each galaxy runs independently on its own worker.
    # emcee inside each worker runs single-threaded (no nested pool).
    with Pool(processes=N_CORES) as pool:
        results = pool.map(run_single_galaxy, task_args)

    # --- Summary ---
    print()
    print("=" * 62)
    print(" RESULTS SUMMARY")
    print("=" * 62)
    ok_count   = 0
    fail_count = 0
    for r in results:
        print(r)
        if r.startswith("OK"):
            ok_count += 1
        else:
            fail_count += 1

    print()
    print(f" Completed : {ok_count}")
    print(f" Failed    : {fail_count}")
    print(f" Outputs   : {output_dir}")
    print("=" * 62)
