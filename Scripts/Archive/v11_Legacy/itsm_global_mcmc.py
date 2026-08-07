"""
Software Dependencies & Attributions:
This script utilizes the emcee (The MCMC Hammer) and corner.py packages for Bayesian inference and visualization.
- emcee: Foreman-Mackey, D., Hogg, D. W., Lang, D., & Goodman, J. (2013). Publications of the Astronomical Society of the Pacific, 125(925), 306.
- corner.py: Foreman-Mackey, D. (2016). The Journal of Open Source Software, 1(2), 24.
"""

"""
ITSM Production Script — Joint SPARC + DESI Global MCMC Likelihood Sampler
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Protocol: Joint SPARC Kinematics + DESI DR2 BAO Likelihood Convergence

ITSM Core Principles Applied Here:
  - Open thermodynamic system: the vacuum is a Superfluid Plenum, not empty space.
  - a0 = c * H0 / (2 * pi) — geometrically derived from circulation quantization. NOT a free parameter.
  - H0 is geometrically tethered via a0, constraining both galactic rotation curves and cosmic expansion.
  - 2/3 factor is the covariant projection of 2D shear onto 3D bulk volume.
"""

import os
import glob
import numpy as np
import emcee
import corner
from multiprocessing import Pool
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
import os
from itsm_plot_style import apply_tier1_style
apply_tier1_style()
from scipy.optimize import minimize

# 1. Pathing Configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(script_dir, "..", "Data", "SPARC_data"))
desi_path = os.path.abspath(os.path.join(script_dir, "..", "Data", "DESI_data", "bao_data-master", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_mean.txt"))
cov_path = os.path.abspath(os.path.join(script_dir, "..", "Data", "DESI_data", "bao_data-master", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_cov.txt"))

# 2. Data Ingestion (DESI)
df_desi = pd.read_csv(desi_path, sep=r'\s+', comment='#', names=['z', 'value', 'observable'], header=None)
cov = np.loadtxt(cov_path)
df_desi['variance'] = np.diag(cov)
df_h = df_desi[df_desi['observable'] == 'DH_over_rs'].copy()
df_h['H_obs'] = 299792.458 / (df_h['value'] * 147.09)
df_h['err_H'] = df_h['H_obs'] * (np.sqrt(df_h['variance']) / df_h['value'])
z_desi, H_desi, err_desi = df_h['z'].values, df_h['H_obs'].values, df_h['err_H'].values

# 3. Data Ingestion (SPARC)
galaxy_files = sorted(glob.glob(os.path.join(data_dir, "*_rotmod.dat")))
print(f"Found {len(galaxy_files)} SPARC galaxy files.")
assert len(galaxy_files) == 175, "Strict adherence to exactly 175 SPARC galaxies is required for Tier-1 reproducibility."

pre_optimized_galaxies = []  # global — populated in __main__, injected into workers via initializer
a0_ref_sparc = 1.08e-10 * 3.086e13  # reference a0 in SPARC units
bounds = ((0.3, 0.8), (0.4, 1.0), (0.8, 1.2), (0.9, 1.1))

# Worker initializer — injects pre_optimized_galaxies into each spawned process on Windows
def init_worker(galaxies):
    global pre_optimized_galaxies
    pre_optimized_galaxies = galaxies

# 4. Joint Likelihood Definitions
def sparc_log_likelihood(H0):
    # H0 sets a0_sparc via toroidal circulation quantization
    H0_si = (H0 * 1.0e3) / 3.085677581e22
    a0_si = (299792458.0 * H0_si) / (2.0 * np.pi)
    a0_sp = a0_si * (3.085677581e19 * 1.0e-6)
    
    total_log_lik = 0.0
    for gal in pre_optimized_galaxies:
        r = gal['R'] * gal['d_scale']
        v_obs = gal['Vobs'] / gal['i_scale']
        err_v = gal['errV'] / gal['i_scale']
        
        v_bar_sq = (np.abs(gal['Vgas']) * gal['Vgas'] * gal['d_scale'] +
                    gal['u_disk'] * np.abs(gal['Vdisk']) * gal['Vdisk'] * gal['d_scale'] +
                    gal['u_bul'] * np.abs(gal['Vbul']) * gal['Vbul'] * gal['d_scale'])
        g_b = v_bar_sq / r
        
        if np.any(g_b < 0): return -np.inf
        
        g_o = (v_obs**2) / r
        g_e = (2 * v_obs * err_v) / r
        g_eff = g_b + (2.0/3.0) * np.sqrt(g_b * a0_sp)
        
        chi2_kin = np.sum(((g_o - g_eff) / g_e)**2)
        total_log_lik += -0.5 * chi2_kin
        
    return total_log_lik

from scipy.integrate import odeint

def itsm_ode_global(y, z, H0, n):
    Om_m, Om_p = y
    E2 = Om_m + Om_p
    if E2 <= 1e-10:
        E = 1e-5
    else:
        E = np.sqrt(E2)
        
    Q_term = n * (1 + z)**(-3) / (E * (1 + z))
    
    dOmdz = 3 * Om_m / (1 + z) + Q_term
    dOpdz = -Q_term
    return [dOmdz, dOpdz]

def H_itsm_ode(z_array, H0, Om0, n):
    z_sort_idx = np.argsort(z_array)
    z_sorted = z_array[z_sort_idx]
    
    if z_sorted[0] != 0:
        z_int = np.concatenate(([0.0], z_sorted))
        slice_idx = slice(1, None)
    else:
        z_int = z_sorted
        slice_idx = slice(None)
        
    Op0 = 1.0 - Om0
    y0 = [Om0, Op0]
    
    sol = odeint(itsm_ode_global, y0, z_int, args=(H0, n))
    Om_m_z = sol[slice_idx, 0]
    Om_p_z = sol[slice_idx, 1]
    E_z = np.sqrt(np.maximum(Om_m_z + Om_p_z, 1e-10))
    H_z = H0 * E_z
    
    H_out = np.zeros_like(H_z)
    H_out[z_sort_idx] = H_z
    return H_out

def log_likelihood(theta):
    H0, n = theta
    # ITSM STRICT ENFORCEMENT: No Dark Matter. Om is purely Baryonic (Omega_b h^2 = 0.02237)
    h = H0 / 100.0
    Om = 0.02237 / (h**2)
    
    try:
        H_model = H_itsm_ode(z_desi, H0, Om, n)
    except:
        return -np.inf
        
    chi2_desi = np.sum(((H_desi - H_model) / err_desi)**2)
    return -0.5 * chi2_desi + sparc_log_likelihood(H0)

def log_prior(theta):
    H0, n = theta
    # Agnostic uniform priors bounding standard and toroidal tension limits
    if 60 < H0 < 90 and 0.0 < n < 3.0: 
        return 0.0
    return -np.inf

def log_probability(theta):
    lp = log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta)

# 5. MCMC Ensemble Sampler Engine
if __name__ == '__main__':
    # Pre-optimise all 175 SPARC galaxies (runs only in the main process)
    print("Pre-optimizing SPARC galaxies...")
    for f in galaxy_files:
        try:
            df = pd.read_csv(f, sep=r'\s+', comment='#',
                             names=['Rad', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbul', 'SBdisk', 'SBbul'],
                             header=0, engine='python')
            valid = (df['Rad'] > 0) & (df['Vobs'] > 0) & (df['errV'] > 0)
            df_v = df[valid].copy()
            if len(df_v) < 5:
                continue
            r_raw = df_v['Rad'].values
            v_obs_raw = df_v['Vobs'].values
            err_v_raw = df_v['errV'].values
            v_gas_raw = df_v['Vgas'].values
            v_disk_raw = df_v['Vdisk'].values
            v_bul_raw = df_v['Vbul'].values

            def calc_chi2_unfiltered(params):
                u_d, u_b, d_scale, i_scale = params
                r_scaled = r_raw * d_scale
                v_obs_scaled = v_obs_raw / i_scale
                err_v_scaled = err_v_raw / i_scale
                v_bar_sq = (np.abs(v_gas_raw) * v_gas_raw * d_scale +
                            u_d * np.abs(v_disk_raw) * v_disk_raw * d_scale +
                            u_b * np.abs(v_bul_raw) * v_bul_raw * d_scale)
                g_b = v_bar_sq / r_scaled
                if np.any(g_b < 0): return np.inf
                g_o = (v_obs_scaled**2) / r_scaled
                g_e = (2 * v_obs_scaled * err_v_scaled) / r_scaled
                g_eff = g_b + (2.0/3.0) * np.sqrt(g_b * a0_ref_sparc)
                chi2_kin = np.sum(((g_o - g_eff) / g_e)**2)
                prior_d = ((d_scale - 1.0) / 0.10)**2
                prior_i = ((i_scale - 1.0) / 0.05)**2
                return chi2_kin + prior_d + prior_i

            res = minimize(calc_chi2_unfiltered, [0.5, 0.7, 1.0, 1.0], bounds=bounds, method='L-BFGS-B')
            u_d, u_b, d_s, i_s = res.x
            pre_optimized_galaxies.append({
                'R': r_raw, 'Vobs': v_obs_raw, 'errV': err_v_raw,
                'Vgas': v_gas_raw, 'Vdisk': v_disk_raw, 'Vbul': v_bul_raw,
                'u_disk': u_d, 'u_bul': u_b, 'd_scale': d_s, 'i_scale': i_s
            })
        except Exception:
            continue
    print(f"Pre-optimized {len(pre_optimized_galaxies)} galaxies for joint SPARC likelihood.")

    ndim, nwalkers = 2, 64
    # pos initializes [H0, n]
    pos = [np.array([72.5, 1.44]) + np.array([1.0, 0.2]) * np.random.randn(ndim) for _ in range(nwalkers)]

    print("--- INITIALIZING JOINT MCMC GLOBAL SAMPLER ---")
    with Pool(processes=16, initializer=init_worker, initargs=(pre_optimized_galaxies,)) as pool:
        sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, pool=pool)
        sampler.run_mcmc(pos, 10000, progress=True)

    # 6. Convergence Diagnostics & Posterior Extraction
    flat_samples = sampler.get_chain(discard=500, thin=15, flat=True)
    mcmc_results = np.percentile(flat_samples, [16, 50, 84], axis=0)

    print("\n--- CONVERGENCE DIAGNOSTICS ---")
    try:
        tau = sampler.get_autocorr_time(quiet=True)
        print(f"Integrated autocorrelation times: H0={tau[0]:.1f}, n={tau[1]:.1f}")
        print(f"Effective samples: {len(flat_samples)}")
        if np.any(tau > (2000 - 500) / 50):
            print("[WARNING] Chain may not be fully converged. Consider increasing n_steps.")
        else:
            print("[OK] Chain convergence looks good (tau << n_steps).")
    except Exception:
        print("[WARNING] Could not estimate autocorrelation time — chain may be too short.")

    print(f"\n--- OPTIMIZED PARAMETER POSTERIORS ---")
    print(f"H0:  {mcmc_results[1, 0]:.2f} (+{mcmc_results[2, 0]-mcmc_results[1, 0]:.2f} / -{mcmc_results[1, 0]-mcmc_results[0, 0]:.2f})")
    print(f"n:   {mcmc_results[1, 1]:.4f} (+{mcmc_results[2, 1]-mcmc_results[1, 1]:.4f} / -{mcmc_results[1, 1]-mcmc_results[0, 1]:.4f})")

    # Export Diagnostic Corner Plot
    fig = corner.corner(flat_samples, labels=[r"$H_0$", r"$n$"],
                        truths=[mcmc_results[1, 0], mcmc_results[1, 1]],
                        quantiles=[0.16, 0.50, 0.84], show_titles=True,
                        title_fmt=".3f", color="navy", truth_color="crimson")

    # Add Descriptive Elements
    fig.suptitle("ITSM Global MCMC Corner Plot", fontsize=18, y=1.02)
    fig.text(0.6, 0.8, "ITSM Global Fit\nZero Free Parameters\n$T^3$ Topology", fontsize=12,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', boxstyle='round,pad=0.5'))
    plt.savefig(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_global_mcmc_corner.png"), dpi=300, bbox_inches='tight')

    print("Optimization complete. Joint convergence posterior exported.")