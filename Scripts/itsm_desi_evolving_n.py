"""
ITSM Cosmological Expansion: Redshift-Evolving Syntropic Decay Index MCMC Estimator
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Protocol: Multicore MCMC Joint Likelihood Estimation for n(z) = n0 + na * z / (1 + z)
Environment: Windows / Antigravity IDE Workspace Compatible
"""

import numpy as np
import pandas as pd
import emcee
import matplotlib.pyplot as plt
import sys
import os
import time
from scipy.integrate import cumulative_trapezoid
from multiprocessing import Pool, cpu_count

# Configure styling
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from itsm_plot_style import apply_tier1_style
    apply_tier1_style()
except ImportError:
    pass

# Constants
c = 299792.458  # Speed of light in km/s

def H_itsm(z, H0, Om, n0, na):
    """ITSM Evolving Syntropic Decay Expansion History"""
    n_z = n0 + na * z / (1.0 + z)
    radicand = Om * (1 + z)**3 + (1 - Om) * (1 + z)**(-n_z)
    if np.any(radicand <= 0):
        return np.inf
    return H0 * np.sqrt(radicand)

def mu_itsm_fast(z_array, H0, Om, n0, na):
    """Optimized distance modulus computation using grid interpolation"""
    z_max = np.max(z_array)
    z_grid = np.linspace(0.0, z_max * 1.01, 300) # 300 grid points
    
    n_z_grid = n0 + na * z_grid / (1.0 + z_grid)
    radicand_grid = Om * (1 + z_grid)**3 + (1 - Om) * (1 + z_grid)**(-n_z_grid)
    if np.any(radicand_grid <= 0):
        raise ValueError("Negative energy density")
        
    integrand_grid = c / (H0 * np.sqrt(radicand_grid))
    
    # Cumulative integration using trapezoidal rule
    Dc_grid = np.zeros_like(z_grid)
    Dc_grid[1:] = cumulative_trapezoid(integrand_grid, z_grid)
    
    # Interpolate to actual redshifts
    Dc_actual = np.interp(z_array, z_grid, Dc_grid)
    dL_actual = (1 + z_array) * Dc_actual
    dL_actual = np.maximum(dL_actual, 1e-10)
    
    return 5 * np.log10(dL_actual) + 25

def log_prior(theta):
    H0, Om, n0, na = theta
    if 60.0 < H0 < 80.0 and 0.1 < Om < 0.5 and 0.0 < n0 < 6.0 and -3.0 < na < 3.0:
        return 0.0
    return -np.inf

# Global variables for multiprocessing workers
_zHD_sn1a = None
_mu_obs_sn1a = None
_cov_inv_sn1a = None
_z_bao = None
_H_obs_bao = None
_err_H_bao = None

def init_worker(zHD_sn1a, mu_obs_sn1a, cov_inv_sn1a, z_bao, H_obs_bao, err_H_bao):
    global _zHD_sn1a, _mu_obs_sn1a, _cov_inv_sn1a
    global _z_bao, _H_obs_bao, _err_H_bao
    
    _zHD_sn1a = zHD_sn1a
    _mu_obs_sn1a = mu_obs_sn1a
    _cov_inv_sn1a = cov_inv_sn1a
    
    _z_bao = z_bao
    _H_obs_bao = H_obs_bao
    _err_H_bao = err_H_bao

def log_likelihood(theta):
    H0, Om, n0, na = theta
    
    # Check physical constraints on BAO points first
    n_z_bao = n0 + na * _z_bao / (1.0 + _z_bao)
    radicand_bao = Om * (1 + _z_bao)**3 + (1 - Om) * (1 + _z_bao)**(-n_z_bao)
    if np.any(radicand_bao <= 0):
        return -np.inf
        
    # SN1a Log Likelihood (Pantheon+)
    try:
        mu_th = mu_itsm_fast(_zHD_sn1a, H0, Om, n0, na)
    except:
        return -np.inf
        
    delta_sn1a = _mu_obs_sn1a - mu_th
    chi2_sn1a = np.dot(delta_sn1a.T, np.dot(_cov_inv_sn1a, delta_sn1a))
    ll_sn1a = -0.5 * chi2_sn1a
    
    # BAO Log Likelihood (DESI DR2)
    H_th = H0 * np.sqrt(radicand_bao)
    chi2_bao = np.sum(((_H_obs_bao - H_th) / _err_H_bao)**2)
    ll_bao = -0.5 * chi2_bao
    
    return ll_sn1a + ll_bao

def log_probability(theta):
    lp = log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # --- 1. Load Pantheon+ SN1a Data ---
    print("Loading Pantheon+ SH0ES Dataset...")
    pan_assets_dir = os.path.join(script_dir, "..", "Assets", "Pantheon_Data")
    df_pan = pd.read_csv(os.path.join(pan_assets_dir, "Pantheon_SH0ES.dat"), sep=r'\s+')
    zHD_sn1a = df_pan['zHD'].values
    mu_obs_sn1a = df_pan['MU_SH0ES'].values
    N_sn1a = len(zHD_sn1a)
    
    print("Loading Pantheon+ Covariance matrix...")
    with open(os.path.join(pan_assets_dir, "Pantheon_SH0ES_STAT_SYS.cov"), 'r') as f:
        first_line = f.readline().strip()
        if len(first_line.split()) == 1:
            cov_flat = np.loadtxt(f)
        else:
            cov_flat = np.loadtxt(os.path.join(pan_assets_dir, "Pantheon_SH0ES_STAT_SYS.cov"))
            
    cov_matrix_sn1a = cov_flat.reshape((N_sn1a, N_sn1a))
    cov_inv_sn1a = np.linalg.inv(cov_matrix_sn1a)
    print("Pantheon+ matrix inversion complete.")
    
    # --- 2. Load DESI BAO Data ---
    print("Loading DESI DR2 BAO Dataset...")
    bao_data_path = os.path.join(script_dir, "..", "DESI_data", "bao_data-master", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_mean.txt")
    bao_cov_path = os.path.join(script_dir, "..", "DESI_data", "bao_data-master", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_cov.txt")
    
    df_bao = pd.read_csv(bao_data_path, sep=r'\s+', comment='#', names=['z', 'value', 'observable'], header=None)
    bao_cov = np.loadtxt(bao_cov_path)
    df_bao['variance'] = np.diag(bao_cov)
    
    df_h = df_bao[df_bao['observable'] == 'DH_over_rs'].copy()
    df_h['H_obs'] = 299792.458 / (df_h['value'] * 147.09)
    df_h['err_H'] = df_h['H_obs'] * (np.sqrt(df_h['variance']) / df_h['value'])
    
    z_bao = df_h['z'].values
    H_obs_bao = df_h['H_obs'].values
    err_H_bao = df_h['err_H'].values
    print(f"Loaded {len(z_bao)} DESI BAO Hubble distance points.")
    
    # --- 3. MCMC Setup ---
    ndim = 4
    nwalkers = 32
    nsteps = 2000
    
    # Initial guess centered around optimized static n = 0.81 with no evolution (na = 0)
    initial_guess = [74.0, 0.24, 0.81, 0.0]
    pos = initial_guess + 1e-4 * np.random.randn(nwalkers, ndim)
    
    # Bound check for initial guess
    pos[:, 0] = np.clip(pos[:, 0], 61.0, 79.0)
    pos[:, 1] = np.clip(pos[:, 1], 0.11, 0.49)
    pos[:, 2] = np.clip(pos[:, 2], 0.1, 5.9)
    pos[:, 3] = np.clip(pos[:, 3], -2.9, 2.9)
    
    n_cores = cpu_count()
    print(f"Starting Joint Multicore MCMC on {n_cores} cores ({nwalkers} walkers, {nsteps} steps)...")
    start_time = time.time()
    
    # Multiprocessing Pool
    with Pool(processes=n_cores, initializer=init_worker, initargs=(zHD_sn1a, mu_obs_sn1a, cov_inv_sn1a, z_bao, H_obs_bao, err_H_bao)) as pool:
        sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, pool=pool)
        sampler.run_mcmc(pos, nsteps, progress=True)
        
    end_time = time.time()
    print(f"Joint MCMC Complete! Computed in {(end_time-start_time)/60:.2f} minutes.")
    
    # --- 4. Plotting & Results ---
    flat_samples = sampler.get_chain(discard=500, thin=15, flat=True)
    H0_m, Om_m, n0_m, na_m = np.median(flat_samples, axis=0)
    H0_std, Om_std, n0_std, na_std = np.std(flat_samples, axis=0)
    
    print("\n--- CONVERGENCE DIAGNOSTICS ---")
    try:
        tau = sampler.get_autocorr_time(quiet=True)
        print(f"Integrated autocorrelation times: H0={tau[0]:.1f}, Om={tau[1]:.1f}, n0={tau[2]:.1f}, na={tau[3]:.1f}")
        print(f"Effective samples: {len(flat_samples)}")
        if np.any(tau > (nsteps - 500) / 50):
            print("[WARNING] Chain may not be fully converged. Consider increasing n_steps.")
        else:
            print("[OK] Chain convergence looks good (tau << n_steps).")
    except Exception:
        print("[WARNING] Could not estimate autocorrelation time — chain may be too short.")
    
    print("\n--- ITSM JOINT COSMOLOGY POSTERIOR MEDIANS (EVOLVING N) ---")
    print(f"H0: {H0_m:.4f} +/- {H0_std:.4f} km/s/Mpc")
    print(f"Om: {Om_m:.4f} +/- {Om_std:.4f}")
    print(f"n0: {n0_m:.4f} +/- {n0_std:.4f}")
    print(f"na: {na_m:.4f} +/- {na_std:.4f}")
    print("----------------------------------------------")
    
    try:
        import corner
        # Using raw string formatting for latex symbols to avoid backslash escape warning
        labels = [r"$H_0$", r"$\Omega_m$", r"$n_0$", r"$n_a$"]
        fig = corner.corner(
            flat_samples, labels=labels,
            truths=[H0_m, Om_m, n0_m, na_m],
            quantiles=[0.16, 0.5, 0.84],
            show_titles=True, title_kwargs={"fontsize": 14},
            color='#0072B2', truth_color='darkred'
        )
        
        fig.suptitle(r"ITSM Constraints with Evolving Syntropic Index $n(z) = n_0 + n_a \frac{z}{1+z}$", fontsize=16, y=1.02)
        fig.subplots_adjust(top=0.92)
        
        out_path = os.path.join(script_dir, "..", "Assets", "Figures", "itsm_evolving_n_corner.png")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=300, bbox_inches='tight')
        print(f"Evolving-n Corner plot saved to {out_path}")
    except Exception as e:
        print(f"Could not generate corner plot: {e}")
