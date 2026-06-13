"""
ITSM Joint Hierarchical Bayesian Inference
Author: Brendon Boyd
Combines Pantheon+ SN1a covariance matrix and SPARC kinematics.
Evaluates the joint posterior of [H0, Om, n].
For SPARC, it uses a Profile Likelihood approach: optimizing M/L ratios 
for all 175 galaxies on the fly for each proposed H0.
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
from scipy.optimize import minimize
import os
import time
from multiprocessing import Pool, cpu_count
import glob
import warnings

warnings.filterwarnings('ignore')


# Constants
c = 299792.458  # Speed of light in km/s
KPC_TO_M = 3.085677581e19
MPC_TO_M = 3.085677581e22

# ====================================================================
# ITSM PHYSICS ENGINES
# ====================================================================
def H_itsm(z, H0, Om, n):
    radicand = Om * (1 + z)**3 + (1 - Om) * (1 + z)**(-n)
    if radicand <= 0: return np.inf
    return H0 * np.sqrt(radicand)

def dL_integrand(z, H0, Om, n):
    return c / H_itsm(z, H0, Om, n)

def mu_itsm(z_array, H0, Om, n):
    mu_theory = np.zeros_like(z_array)
    for i, z in enumerate(z_array):
        Dc, _ = integrate.quad(dL_integrand, 0, z, args=(H0, Om, n), epsrel=1e-3)
        mu_theory[i] = 5 * np.log10((1 + z) * Dc) + 25
    return mu_theory

def compute_sparc_vcalc(R_kpc, V_gas, V_disk, V_bulge, ups_disk, ups_bulge, H0):
    R_m = R_kpc * KPC_TO_M
    V_bar_sq = (V_gas * np.abs(V_gas) + ups_disk * V_disk * np.abs(V_disk) + ups_bulge * V_bulge * np.abs(V_bulge))
    V_bar_sq = np.maximum(V_bar_sq, 0.0)
    g_bar = (V_bar_sq * 1.0e6) / R_m
    
    H0_si = (H0 * 1.0e3) / MPC_TO_M
    a0 = (c * 1000 * H0_si) / (2.0 * np.pi)  # c in m/s here: 299792458
    
    g_eff = g_bar + (2.0 / 3.0) * np.sqrt(g_bar * a0)
    V_calc_km_s = np.sqrt(g_eff * R_m) / 1.0e3
    return V_calc_km_s

# ====================================================================
# GLOBAL DATA CONTAINERS FOR MULTIPROCESSING
# ====================================================================
_zHD = None
_mu_obs = None
_cov_inv = None
_sparc_data = None

def init_worker(zHD, mu_obs, cov_inv, sparc_data):
    global _zHD, _mu_obs, _cov_inv, _sparc_data
    _zHD = zHD
    _mu_obs = mu_obs
    _cov_inv = cov_inv
    _sparc_data = sparc_data

# ====================================================================
# LIKELIHOOD FUNCTIONS
# ====================================================================
def log_prior(theta):
    H0, Om, n = theta
    if 65.0 < H0 < 80.0 and 0.1 < Om < 0.5 and 0.0 < n < 5.0:
        return 0.0
    return -np.inf

def sparc_galaxy_nll(upsilons, R, Vobs, errV, Vgas, Vdisk, Vbulge, H0):
    u_d, u_b = upsilons
    V_calc = compute_sparc_vcalc(R, Vgas, Vdisk, Vbulge, u_d, u_b, H0)
    return 0.5 * np.sum(((Vobs - V_calc) / errV)**2)

def get_sparc_ll(H0):
    total_ll = 0.0
    for gal in _sparc_data:
        # Profile likelihood: optimize M/L for this H0
        res = minimize(sparc_galaxy_nll, x0=[0.5, 0.7], 
                       args=(gal['R'], gal['Vobs'], gal['errV'], gal['Vgas'], gal['Vdisk'], gal['Vbulge'], H0),
                       bounds=[(0.1, 3.0), (0.0, 3.0)], method='L-BFGS-B')
        total_ll -= res.fun  # res.fun is the minimum NLL, so LL is -NLL
    return total_ll

def log_likelihood(theta):
    H0, Om, n = theta
    
    # 1. Pantheon+ LL
    try:
        mu_th = mu_itsm(_zHD, H0, Om, n)
        delta = _mu_obs - mu_th
        ll_pantheon = -0.5 * np.dot(delta.T, np.dot(_cov_inv, delta))
    except:
        return -np.inf
        
    # 2. SPARC LL
    ll_sparc = get_sparc_ll(H0)
    
    return ll_pantheon + ll_sparc

def log_probability(theta):
    lp = log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta)

# ====================================================================
# MAIN EXECUTION
# ====================================================================
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "..", "Assets")
    
    # --- LOAD PANTHEON ---
    pantheon_dat = os.path.join(assets_dir, "Pantheon_Data", "Pantheon_SH0ES.dat")
    pantheon_cov = os.path.join(assets_dir, "Pantheon_Data", "Pantheon_SH0ES_STAT_SYS.cov")
    
    df_p = pd.read_csv(pantheon_dat, sep=r'\s+')
    zHD = df_p['zHD'].values
    mu_obs = df_p['MU_SH0ES'].values
    
    with open(pantheon_cov, 'r') as f:
        first_line = f.readline().strip()
        if len(first_line.split()) == 1:
            cov_flat = np.loadtxt(f)
        else:
            cov_flat = np.loadtxt(pantheon_cov)
            
    cov_matrix = cov_flat.reshape((len(zHD), len(zHD)))
    cov_inv = np.linalg.inv(cov_matrix)
    
    # --- LOAD SPARC ---
    sparc_path = os.path.normpath(os.path.join(script_dir, "..", "SPARC_data", "*.dat"))
    file_list = glob.glob(sparc_path)
    sparc_data = []
    
    for f in file_list:
        df_s = pd.read_csv(f, sep=r'\s+', comment='#', header=None,
                           names=['R', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbulge'])
        df_s = df_s.dropna()
        if len(df_s) > 4:
            sparc_data.append({
                'R': df_s['R'].values,
                'Vobs': df_s['Vobs'].values,
                'errV': df_s['errV'].values,
                'Vgas': df_s['Vgas'].values,
                'Vdisk': df_s['Vdisk'].values,
                'Vbulge': df_s['Vbulge'].values
            })
            
    print(f"Loaded {len(zHD)} SN1a and {len(sparc_data)} SPARC galaxies.")
    
    # --- MCMC CONFIG ---
    ndim = 3
    nwalkers = 32
    
    # TEST MODE TOGGLE
    TEST_MODE = False
    if TEST_MODE:
        nsteps = 50
        print(f"--- RUNNING IN TEST MODE ({nsteps} steps) ---")
    else:
        nsteps = 3000
        print(f"--- RUNNING IN TIER-1 PRODUCTION MODE ({nsteps} steps) ---")
        
    initial_guess = [73.0, 0.3, 3.0]
    pos = initial_guess + 1e-3 * np.random.randn(nwalkers, ndim)
    
    start_time = time.time()
    cores = min(16, cpu_count())
    
    with Pool(processes=cores, initializer=init_worker, initargs=(zHD, mu_obs, cov_inv, sparc_data)) as pool:
        sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, pool=pool)
        sampler.run_mcmc(pos, nsteps, progress=True)
        
    end_time = time.time()
    t_min = (end_time - start_time) / 60.0
    print(f"MCMC Complete! Computed {nsteps} steps in {t_min:.2f} minutes.")
    
    if TEST_MODE:
        print(f"Estimated time for 3000 steps: {t_min * (3000/nsteps):.2f} minutes.")
        print("Set TEST_MODE = False in script to run production.")
    else:
        flat_samples = sampler.get_chain(discard=600, thin=15, flat=True)
        H0_m, Om_m, n_m = np.median(flat_samples, axis=0)
        
        print("\n--- CONVERGENCE DIAGNOSTICS ---")
        try:
            tau = sampler.get_autocorr_time(quiet=True)
            print(f"Integrated autocorrelation times: H0={tau[0]:.1f}, Om={tau[1]:.1f}, n={tau[2]:.1f}")
            print(f"Effective samples: {len(flat_samples)}")
            if np.any(tau > (nsteps - 600) / 50):
                print("[WARNING] Chain may not be fully converged. Consider increasing n_steps.")
            else:
                print("[OK] Chain convergence looks good (tau << n_steps).")
        except Exception:
            print("[WARNING] Could not estimate autocorrelation time — chain may be too short.")
        
        print("\n--- JOINT HIERARCHICAL POSTERIOR MEDIANS ---")
        print(f"H0: {H0_m:.2f} km/s/Mpc")
        print(f"Om: {Om_m:.3f}")
        print(f"n : {n_m:.3f}")
        
        try:
            import corner
            fig = corner.corner(
                flat_samples, labels=[r"$H_0$", r"$\Omega_m$", r"$n$"],
                truths=[None, None, None],
                quantiles=[0.16, 0.5, 0.84],
                show_titles=True, title_kwargs={"fontsize": 12}
            )
            
            # Add Descriptive Elements
            fig.suptitle("ITSM Hierarchical Joint Cosmology MCMC", fontsize=18, y=1.02)
            fig.text(0.6, 0.8, "Pantheon+ & DESI BAO\nSyntropic Decay Model", fontsize=12,
                     bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', boxstyle='round,pad=0.5'))
                     
            out_path = os.path.join(script_dir, "..", "Assets", "Figures", "itsm_hierarchical_joint_corner.png")
            fig.savefig(out_path, dpi=300)
            print(f"Corner plot saved to {out_path}")
        except:
            pass
        
        # Save raw chains for API export
        chain_path = os.path.join(script_dir, "..", "Analysis", "Experimental", "Joint_MCMC")
        os.makedirs(chain_path, exist_ok=True)
        df_chain = pd.DataFrame(flat_samples, columns=["H0", "Om", "n"])
        csv_out = os.path.join(chain_path, "itsm_hierarchical_joint_chain.csv")
        df_chain.to_csv(csv_out, index=False)
        print(f"Raw chains saved to {csv_out}")
