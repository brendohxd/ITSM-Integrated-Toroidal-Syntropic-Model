"""
ITSM Cosmological Expansion: Pantheon+ SN1a MCMC Validator
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Protocol: Multicore MCMC using Full Covariance Matrix
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

def itsm_ode(y, z, H0, n):
    Om_m, Om_p, Dc = y
    E2 = Om_m + Om_p
    if E2 <= 1e-10:
        E = 1e-5
    else:
        E = np.sqrt(E2)
        
    H = H0 * E
    
    # Q couples matter and plenum: dt/dz = -1/(H(1+z))
    # dOmdz = 3*Om_m/(1+z) + Q_term
    # dOpdz = -Q_term
    Q_term = n * (1 + z)**(-3) / (E * (1 + z))
    
    dOmdz = 3 * Om_m / (1 + z) + Q_term
    dOpdz = -Q_term
    dDcdz = c / H
    
    return [dOmdz, dOpdz, dDcdz]

def mu_itsm(z_array, H0, Om0, n):
    """Calculate theoretical distance modulus via coupled ODEs"""
    z_sort_idx = np.argsort(z_array)
    z_sorted = z_array[z_sort_idx]
    
    if z_sorted[0] != 0:
        z_int = np.concatenate(([0.0], z_sorted))
        slice_idx = slice(1, None)
    else:
        z_int = z_sorted
        slice_idx = slice(None)
        
    Op0 = 1.0 - Om0
    y0 = [Om0, Op0, 0.0]
    
    sol = integrate.odeint(itsm_ode, y0, z_int, args=(H0, n))
    Dc_sorted = sol[slice_idx, 2]
    
    Dc = np.zeros_like(Dc_sorted)
    Dc[z_sort_idx] = Dc_sorted
    
    dL = (1 + z_array) * Dc
    mu_theory = 5 * np.log10(dL) + 25
    return mu_theory

def log_prior(theta):
    H0, n = theta
    if 60.0 < H0 < 80.0 and 0.0 < n < 6.0:
        return 0.0
    return -np.inf

# We need a global variable for the data so the multiprocessing workers can access it without pickling overhead
_zHD = None
_mu_obs = None
_cov_inv = None

def init_worker(zHD, mu_obs, cov_inv):
    global _zHD, _mu_obs, _cov_inv
    _zHD = zHD
    _mu_obs = mu_obs
    _cov_inv = cov_inv

def log_likelihood(theta):
    H0, n = theta
    # ITSM: Om is purely baryonic, no dark matter
    h = H0 / 100.0
    Om = 0.02237 / (h**2)
    try:
        mu_th = mu_itsm(_zHD, H0, Om, n)
    except:
        return -np.inf
    
    delta = _mu_obs - mu_th
    # Matrix multiplication: delta.T * C^{-1} * delta
    chi2 = np.dot(delta.T, np.dot(_cov_inv, delta))
    return -0.5 * chi2

def log_probability(theta):
    lp = log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "..", "Assets", "Pantheon_Data")
    
    dat_path = os.path.join(assets_dir, "Pantheon_SH0ES.dat")
    cov_path = os.path.join(assets_dir, "Pantheon_SH0ES_STAT_SYS.cov")
    
    print("Loading Pantheon+ SH0ES Dataset...")
    df = pd.read_csv(dat_path, sep=r'\s+')
    
    # We use zHD for redshift and MU_SH0ES for the calibrated distance modulus
    zHD = df['zHD'].values
    mu_obs = df['MU_SH0ES'].values
    N = len(zHD)
    
    print(f"Loaded {N} Supernovae. Loading covariance matrix (this may take a moment)...")
    
    # The Pantheon+ covariance matrix text file format:
    # Line 1: N
    # Line 2 to end: Flattened N*N matrix or matrix rows. Usually it's just the flat list.
    with open(cov_path, 'r') as f:
        first_line = f.readline().strip()
        # Some versions have the number of elements on the first line
        if len(first_line.split()) == 1:
            cov_flat = np.loadtxt(f)
        else:
            # Re-read from beginning if the first line is data
            cov_flat = np.loadtxt(cov_path)
            
    cov_matrix = cov_flat.reshape((N, N))
    print(f"Covariance matrix shape: {cov_matrix.shape}")
    
    print("Inverting full covariance matrix...")
    cov_inv = np.linalg.inv(cov_matrix)
    print("Inversion complete.")
    
    # MCMC Setup
    ndim = 2
    nwalkers = 32
    nsteps = 3000  # Increased for proper convergence and sampling
    
    # Initial guess around SPARC/ITSM predictions
    # H0 ~ 72, n ~ 3.0
    initial_guess = [72.0, 3.0]
    pos = initial_guess + 1e-4 * np.random.randn(nwalkers, ndim)
    
    print(f"Starting Multicore MCMC ({nwalkers} walkers, {nsteps} steps)...")
    start_time = time.time()
    
    # Launch pool with 16 cores
    with Pool(processes=16, initializer=init_worker, initargs=(zHD, mu_obs, cov_inv)) as pool:
        sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, pool=pool)
        sampler.run_mcmc(pos, nsteps, progress=True)
        
    end_time = time.time()
    print(f"MCMC Complete! Computed in {(end_time-start_time)/60:.2f} minutes.")
    
    # Analyze chains
    flat_samples = sampler.get_chain(discard=500, thin=15, flat=True)
    H0_m, n_m = np.median(flat_samples, axis=0)

    print("\n--- CONVERGENCE DIAGNOSTICS ---")
    try:
        tau = sampler.get_autocorr_time(quiet=True)
        print(f"Integrated autocorrelation times: H0={tau[0]:.1f}, n={tau[1]:.1f}")
        print(f"Effective samples: {len(flat_samples)}")
        if np.any(tau > (nsteps - 500) / 50):
            print("[WARNING] Chain may not be fully converged. Consider increasing n_steps.")
        else:
            print("[OK] Chain convergence looks good (tau << n_steps).")
    except Exception:
        print("[WARNING] Could not estimate autocorrelation time — chain may be too short.")
    
    
    print("\n--- ITSM PANTHEON+ POSTERIOR MEDIANS ---")
    print(f"H0: {H0_m:.2f} km/s/Mpc")
    print(f"n : {n_m:.3f}")
    print("----------------------------------------")
    
    try:
        import corner
        fig = corner.corner(
            flat_samples, labels=[r"$H_0$", r"$n$"],
            truths=[None, 3.0],
            quantiles=[0.16, 0.5, 0.84],
            show_titles=True, title_kwargs={"fontsize": 12}
        )
        
        # Add Descriptive Elements
        fig.suptitle("Pantheon+ SN1a Cosmology MCMC", fontsize=18, y=1.02)
        fig.text(0.6, 0.8, "Supernova Optimization\nITSM Background Expansion", fontsize=12,
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', boxstyle='round,pad=0.5'))
        
        out_path = os.path.join(script_dir, "..", "Assets", "Figures", "itsm_pantheon_corner.png")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path)
        print(f"Corner plot saved to {out_path}")
    except ImportError:
        print("Install 'corner' package via pip to generate the corner plot.")
