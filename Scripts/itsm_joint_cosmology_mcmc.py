"""
Software Dependencies & Attributions:
This script utilizes the emcee (The MCMC Hammer) and corner.py packages for Bayesian inference and visualization.
- emcee: Foreman-Mackey, D., Hogg, D. W., Lang, D., & Goodman, J. (2013). Publications of the Astronomical Society of the Pacific, 125(925), 306.
- corner.py: Foreman-Mackey, D. (2016). The Journal of Open Source Software, 1(2), 24.
"""

"""
ITSM Cosmological Expansion: Joint DESI BAO & Pantheon+ SN1a MCMC Validator
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Protocol: Multicore MCMC Joint Likelihood Estimation
Environment: Windows / Antigravity IDE Workspace Compatible
"""

import numpy as np
import pandas as pd
import emcee
import matplotlib.pyplot as plt
import sys
import os
from itsm_plot_style import apply_tier1_style
apply_tier1_style()
import scipy.integrate as integrate
import os
import time
from multiprocessing import Pool

# Configure matplotlib for physics journals


# Constants
c = 299792.458  # Speed of light in km/s

def H_itsm(z, H0, Om, n):
    """ITSM Syntropic Decay Expansion History"""
    radicand = Om * (1 + z)**3 + (1 - Om) * (1 + z)**(-n)
    if radicand <= 0:
        return np.inf
    return H0 * np.sqrt(radicand)

def dL_integrand(z, H0, Om, n):
    return c / H_itsm(z, H0, Om, n)

def mu_itsm(z_array, H0, Om, n):
    """Calculate theoretical distance modulus for an array of redshifts"""
    mu_theory = np.zeros_like(z_array)
    for i, z in enumerate(z_array):
        Dc, _ = integrate.quad(dL_integrand, 0, z, args=(H0, Om, n), epsrel=1e-4)
        dL = (1 + z) * Dc
        mu_theory[i] = 5 * np.log10(dL) + 25
    return mu_theory

def log_prior(theta):
    H0, Om, n = theta
    if 60.0 < H0 < 80.0 and 0.1 < Om < 0.5 and 0.0 < n < 6.0:
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
    H0, Om, n = theta
    
    # SN1a Log Likelihood (Pantheon+)
    try:
        mu_th = mu_itsm(_zHD_sn1a, H0, Om, n)
    except:
        return -np.inf
    delta_sn1a = _mu_obs_sn1a - mu_th
    chi2_sn1a = np.dot(delta_sn1a.T, np.dot(_cov_inv_sn1a, delta_sn1a))
    ll_sn1a = -0.5 * chi2_sn1a
    
    # BAO Log Likelihood (DESI DR2)
    radicand = Om * (1 + _z_bao)**3 + (1 - Om) * (1 + _z_bao)**(-n)
    if np.any(radicand <= 0):
        return -np.inf
    H_th = H0 * np.sqrt(radicand)
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
    bao_data_path = os.path.join(script_dir, "..", "Data", "DESI_data", "bao_data-master", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_mean.txt")
    bao_cov_path = os.path.join(script_dir, "..", "Data", "DESI_data", "bao_data-master", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_cov.txt")
    
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
    ndim = 3
    nwalkers = 32
    nsteps = 2000  # Increased for proper convergence
    
    initial_guess = [72.0, 0.3, 3.0]
    pos = initial_guess + 1e-4 * np.random.randn(nwalkers, ndim)
    
    print(f"Starting Joint Multicore MCMC ({nwalkers} walkers, {nsteps} steps)...")
    start_time = time.time()
    
    with Pool(processes=16, initializer=init_worker, initargs=(zHD_sn1a, mu_obs_sn1a, cov_inv_sn1a, z_bao, H_obs_bao, err_H_bao)) as pool:
        sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, pool=pool)
        sampler.run_mcmc(pos, nsteps, progress=True)
        
    end_time = time.time()
    print(f"Joint MCMC Complete! Computed in {(end_time-start_time)/60:.2f} minutes.")
    
    # --- 4. Plotting & Results ---
    flat_samples = sampler.get_chain(discard=500, thin=15, flat=True)
    H0_m, Om_m, n_m = np.median(flat_samples, axis=0)
    
    print("\n--- CONVERGENCE DIAGNOSTICS ---")
    try:
        tau = sampler.get_autocorr_time(quiet=True)
        print(f"Integrated autocorrelation times: H0={tau[0]:.1f}, Om={tau[1]:.1f}, n={tau[2]:.1f}")
        print(f"Effective samples: {len(flat_samples)}")
        if np.any(tau > (nsteps - 500) / 50):
            print("[WARNING] Chain may not be fully converged. Consider increasing n_steps.")
        else:
            print("[OK] Chain convergence looks good (tau << n_steps).")
    except Exception:
        print("[WARNING] Could not estimate autocorrelation time — chain may be too short.")
    
    print("\n--- ITSM JOINT COSMOLOGY POSTERIOR MEDIANS ---")
    print(f"H0: {H0_m:.2f} km/s/Mpc")
    print(f"Om: {Om_m:.3f}")
    print(f"n : {n_m:.3f}")
    print("----------------------------------------------")
    
    try:
        import corner
        fig = corner.corner(
            flat_samples, labels=[r"$H_0$", r"$\Omega_m$", r"$n$"],
            truths=[None, None, 3.0],
            quantiles=[0.16, 0.5, 0.84],
            show_titles=True, title_kwargs={"fontsize": 14},
            color='#0072B2', truth_color='darkred'
        )
        
        # Add a title to the figure and adjust top margin to prevent overlap
        fig.suptitle(r"ITSM Joint Cosmological Constraints (Pantheon+ SN1a & DESI BAO)", fontsize=16, y=1.05)
        fig.subplots_adjust(top=0.90)
        
        out_path = os.path.join(script_dir, "..", "Assets", "Figures", "itsm_joint_cosmology_corner.png")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, bbox_inches='tight')
        print(f"Joint Corner plot saved to {out_path}")
    except ImportError:
        print("Install 'corner' package via pip to generate the corner plot.")
