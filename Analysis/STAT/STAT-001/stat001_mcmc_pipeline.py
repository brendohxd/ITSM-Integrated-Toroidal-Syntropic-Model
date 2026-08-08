#!/usr/bin/env python3
"""STAT-001: SPARC Bayesian MCMC Pipeline

Rigorous Bayesian MCMC sampling (emcee) of the SPARC dataset using the 
Fully Floated (Free D, Free i) phenomenological mode to derive formal 
uncertainty bounds.
"""

import os
import glob
import json
import numpy as np
import pandas as pd
from pathlib import Path
from multiprocessing import Pool, cpu_count
import time
import emcee

# Import IR laws
import sys
disk001_path = Path(__file__).resolve().parent.parent.parent / "DISK" / "DISK-001"
sys.path.append(str(disk001_path))

from disk001_ir_law import (
    derived_geometric_ir,
    derived_phenomenological_ir,
    aqual_g_magnitude
)

SPARC_DIR = Path(__file__).resolve().parent.parent.parent.parent / "Data" / "SPARC_data"
V_EFF_MAT001 = 0.6666666666666666

LOG10_UPS_DISK_MEAN = -0.301
LOG10_UPS_BULGE_MEAN = -0.155
LOG10_UPS_STD = 0.1

def load_sparc_data(filepath: Path) -> dict:
    data = np.loadtxt(filepath, comments="#")
    has_bulge = data.shape[1] > 5 and np.any(data[:, 5] > 0)
    return {
        "name": filepath.name.replace("_rotmod.dat", "").replace("-ITSM-Cosmologist", ""),
        "Rad": data[:, 0],
        "Vobs": data[:, 1],
        "errV": data[:, 2],
        "Vgas": data[:, 3],
        "Vdisk": data[:, 4],
        "Vbul": data[:, 5] if has_bulge else np.zeros_like(data[:, 0]),
        "has_bulge": has_bulge
    }

def fit_galaxy_mcmc(args) -> dict:
    gal, ir, i_nom = args
    
    Rad = gal["Rad"]
    Vobs_orig = gal["Vobs"]
    errV = gal["errV"]
    Vgas = gal["Vgas"]
    Vdisk = gal["Vdisk"]
    Vbul = gal["Vbul"]
    has_bulge = gal["has_bulge"]
    
    # Mode: Fully Floated
    # Params: [ups_disk, ups_bulge (if has_bulge), delta_D, i_fit]
    
    def log_prior(theta):
        idx = 0
        ups_disk = theta[idx]
        idx += 1
        
        ups_bulge = 0.0
        if has_bulge:
            ups_bulge = theta[idx]
            idx += 1
            
        delta_D = theta[idx]
        idx += 1
        
        i_fit = theta[idx]
        
        # Hard bounds
        if not (0.1 < ups_disk < 5.0): return -np.inf
        if has_bulge and not (0.1 < ups_bulge < 5.0): return -np.inf
        if not (0.5 < delta_D < 1.5): return -np.inf
        if not (max(10.0, i_nom - 20.0) < i_fit < min(90.0, i_nom + 20.0)): return -np.inf
        
        # Lognormal/Gaussian priors penalty (log probability)
        lp = 0.0
        lp -= 0.5 * ((np.log10(ups_disk) - LOG10_UPS_DISK_MEAN) / LOG10_UPS_STD)**2
        if has_bulge:
            lp -= 0.5 * ((np.log10(ups_bulge) - LOG10_UPS_BULGE_MEAN) / LOG10_UPS_STD)**2
        lp -= 0.5 * ((delta_D - 1.0) / 0.10)**2
        lp -= 0.5 * ((i_fit - i_nom) / 5.0)**2
        
        return lp
        
    def log_likelihood(theta):
        idx = 0
        ups_disk = theta[idx]
        idx += 1
        ups_bulge = theta[idx] if has_bulge else 0.0
        if has_bulge: idx += 1
        delta_D = theta[idx]
        idx += 1
        i_fit = theta[idx]
        
        R_fit = Rad * delta_D
        Vgas_fit = Vgas * np.sqrt(delta_D)
        Vdisk_fit = Vdisk * np.sqrt(delta_D)
        Vbul_fit = Vbul * np.sqrt(delta_D)
            
        Vbar_sq = Vgas_fit * np.abs(Vgas_fit) + ups_disk * Vdisk_fit * np.abs(Vdisk_fit) + ups_bulge * Vbul_fit * np.abs(Vbul_fit)
        Vbar_sq = np.maximum(Vbar_sq, 0.0)
        
        g_N = Vbar_sq / R_fit
        g_obs = aqual_g_magnitude(g_N, ir)
        Vpred = np.sqrt(R_fit * g_obs)
        
        sin_ratio = np.sin(np.radians(i_nom)) / np.sin(np.radians(i_fit))
        Vobs_fit = Vobs_orig * sin_ratio
        
        chi2 = np.sum(((Vobs_fit - Vpred) / errV)**2)
        return -0.5 * chi2
        
    def log_prob(theta):
        lp = log_prior(theta)
        if not np.isfinite(lp):
            return -np.inf
        return lp + log_likelihood(theta)
        
    # Init walkers
    ndim = 3 if not has_bulge else 4
    nwalkers = 100
    nsteps = 3000
    
    pos = []
    for _ in range(nwalkers):
        p = [np.random.normal(0.5, 0.05)]
        if has_bulge:
            p.append(np.random.normal(0.7, 0.05))
        p.append(np.random.normal(1.0, 0.05))
        p.append(np.random.normal(i_nom, 1.0))
        pos.append(p)
    pos = np.array(pos)
    
    # Suppress emcee warnings for tiny move steps
    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob)
    sampler.run_mcmc(pos, nsteps, progress=False)
    
    # Discard 500 steps burn-in, thin by 15
    flat_samples = sampler.get_chain(discard=500, thin=15, flat=True)
    
    # Calculate best fit (median) and 1-sigma percentiles
    mcmc_res = {}
    
    idx = 0
    ups_disk_mcmc = np.percentile(flat_samples[:, idx], [16, 50, 84])
    mcmc_res["ups_disk"] = [ups_disk_mcmc[0], ups_disk_mcmc[1], ups_disk_mcmc[2]]
    idx += 1
    
    if has_bulge:
        ups_bulge_mcmc = np.percentile(flat_samples[:, idx], [16, 50, 84])
        mcmc_res["ups_bulge"] = [ups_bulge_mcmc[0], ups_bulge_mcmc[1], ups_bulge_mcmc[2]]
        idx += 1
        
    delta_D_mcmc = np.percentile(flat_samples[:, idx], [16, 50, 84])
    mcmc_res["delta_D"] = [delta_D_mcmc[0], delta_D_mcmc[1], delta_D_mcmc[2]]
    idx += 1
    
    i_fit_mcmc = np.percentile(flat_samples[:, idx], [16, 50, 84])
    mcmc_res["i_fit"] = [i_fit_mcmc[0], i_fit_mcmc[1], i_fit_mcmc[2]]
    
    # Calculate chi2 at median
    median_theta = [mcmc_res["ups_disk"][1]]
    if has_bulge: median_theta.append(mcmc_res["ups_bulge"][1])
    median_theta.append(mcmc_res["delta_D"][1])
    median_theta.append(mcmc_res["i_fit"][1])
    
    best_chi2 = -2.0 * log_likelihood(median_theta)
    
    return {
        "name": gal["name"],
        "chi2": best_chi2,
        "n_points": len(Rad),
        "k_params": ndim,
        "mcmc": mcmc_res
    }

def run_pipeline():
    print(f"STAT-001 MCMC Pipeline started (using {cpu_count()} cores).")
    
    master_cat = pd.read_csv(SPARC_DIR / "SPARC_MassModels.csv")
    inc_dict = dict(zip(master_cat["Name"], master_cat["i"]))
    
    dat_files = glob.glob(str(SPARC_DIR / "*_rotmod.dat"))
    dat_files = [f for f in dat_files if "ITSM-Cosmologist" not in f]
    galaxies = [load_sparc_data(Path(f)) for f in dat_files]
    print(f"Loaded {len(galaxies)} SPARC galaxies.")
    
    ir_models = {
        "Geometric": derived_geometric_ir(V_eff=V_EFF_MAT001),
        "Phenomenological": derived_phenomenological_ir(V_eff=V_EFF_MAT001)
    }
    
    results = {}
    
    # We are running ONLY Fully Floated on all 175 galaxies
    mode_name = "Fully Floated (Free D ±10%, Free i ±5°)"
    print(f"\n{'='*60}\nRUNNING MODE: MCMC {mode_name}\n{'='*60}")
    
    for name, ir in ir_models.items():
        print(f"\nEvaluating IR Law: {name} (a0={ir.a0:.3f}, C_obs={ir.C_obs:.3f})")
        print(f"MCMC: 100 walkers, 3000 steps per galaxy...")
        t0 = time.time()
        
        pool = Pool(processes=cpu_count())
        fit_args = [(gal, ir, inc_dict.get(gal["name"], 60.0)) for gal in galaxies]
        fits = pool.map(fit_galaxy_mcmc, fit_args)
        pool.close()
        pool.join()
        
        total_chi2 = sum(f["chi2"] for f in fits)
        total_n = sum(f["n_points"] for f in fits)
        total_k = sum(f["k_params"] for f in fits)
        
        reduced_chi2 = total_chi2 / (total_n - total_k)
        
        print(f"  Time: {time.time() - t0:.2f}s")
        print(f"  Total Chi2 (at median): {total_chi2:.1f}")
        print(f"  Reduced Chi2: {reduced_chi2:.3f}")
        
        results[name] = {
            "a0": ir.a0,
            "C_obs": ir.C_obs,
            "total_chi2": total_chi2,
            "reduced_chi2": reduced_chi2,
            "total_n": total_n,
            "total_k": total_k,
            "galaxies": {f["name"]: f for f in fits}
        }
    
    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "stat001_mcmc_summary.json"
    
    # Convert numpy types to python native for JSON serialization
    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer): return int(obj)
            if isinstance(obj, np.floating): return float(obj)
            if isinstance(obj, np.ndarray): return obj.tolist()
            return super(NpEncoder, self).default(obj)
            
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, cls=NpEncoder)
        
    print(f"\nResults saved to {out_path}")

if __name__ == "__main__":
    run_pipeline()
