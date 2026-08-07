#!/usr/bin/env python3
"""STAT-001: SPARC Statistical Inference Pipeline

Rigorous statistical comparison of the Derived Geometric Path vs the Phenomenological Path 
using the SPARC rotation curve database. Parallelized across galaxies to utilize all cores.
"""

import os
import glob
import json
import numpy as np
from pathlib import Path
from multiprocessing import Pool, cpu_count
from scipy.optimize import minimize
import time

# We must import the IR laws from the DISK-001 gate to avoid duplication
import sys
disk001_path = Path(__file__).resolve().parent.parent.parent / "DISK" / "DISK-001"
sys.path.append(str(disk001_path))

from disk001_ir_law import (
    derived_geometric_ir,
    derived_phenomenological_ir,
    aqual_g_magnitude,
    DeclaredIR
)

# Constants
SPARC_DIR = Path(__file__).resolve().parent.parent.parent.parent / "Data" / "SPARC_data"
V_EFF_MAT001 = 0.6666666666666666  # Derived from MAT-001 V = C_m / f

# Priors from Lelli et al. 2016 (3.6 micron)
LOG10_UPS_DISK_MEAN = -0.301  # 0.5 Msun/Lsun
LOG10_UPS_BULGE_MEAN = -0.155 # 0.7 Msun/Lsun
LOG10_UPS_STD = 0.1

import pandas as pd

def load_sparc_data(filepath: Path) -> dict:
    """Load a SPARC .dat file."""
    data = np.loadtxt(filepath, comments="#")
    # Columns: Rad, Vobs, errV, Vgas, Vdisk, Vbul, SBdisk, SBbul
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

def fit_galaxy(args) -> dict:
    gal, ir, float_dist, float_inc, i_nom, flat_priors = args
    
    Rad = gal["Rad"]
    Vobs_orig = gal["Vobs"]
    errV = gal["errV"]
    Vgas = gal["Vgas"]
    Vdisk = gal["Vdisk"]
    Vbul = gal["Vbul"]
    has_bulge = gal["has_bulge"]
    
    def nll(params):
        ups_disk = params[0]
        idx = 1
        
        ups_bulge = 0.0
        if has_bulge:
            ups_bulge = params[idx]
            idx += 1
            
        delta_D = params[idx] if float_dist else 1.0
        if float_dist:
            idx += 1
            
        i_fit = params[idx] if float_inc else i_nom
        
        # Prior penalties
        prior_penalty = 0.0
        if not flat_priors:
            prior_penalty += 0.5 * ((np.log10(ups_disk) - LOG10_UPS_DISK_MEAN) / LOG10_UPS_STD)**2
            if has_bulge:
                prior_penalty += 0.5 * ((np.log10(ups_bulge) - LOG10_UPS_BULGE_MEAN) / LOG10_UPS_STD)**2
                
            if float_dist:
                # 10% gaussian prior on distance
                prior_penalty += 0.5 * ((delta_D - 1.0) / 0.10)**2
                
            if float_inc:
                # 5 degree gaussian prior on inclination
                prior_penalty += 0.5 * ((i_fit - i_nom) / 5.0)**2
            
        # Physics: scale radial and velocity components by delta_D
        R_fit = Rad * delta_D
        Vgas_fit = Vgas * np.sqrt(delta_D)
        Vdisk_fit = Vdisk * np.sqrt(delta_D)
        Vbul_fit = Vbul * np.sqrt(delta_D)
            
        Vbar_sq = Vgas_fit * np.abs(Vgas_fit) + ups_disk * Vdisk_fit * np.abs(Vdisk_fit) + ups_bulge * Vbul_fit * np.abs(Vbul_fit)
        Vbar_sq = np.maximum(Vbar_sq, 0.0) # Physical only
        
        g_N = Vbar_sq / R_fit
        # g_obs using deep-MOND simple-mu
        g_obs = aqual_g_magnitude(g_N, ir)
        Vpred = np.sqrt(R_fit * g_obs)
        
        # Scale Vobs based on inclination correction
        sin_ratio = np.sin(np.radians(i_nom)) / np.sin(np.radians(i_fit))
        Vobs_fit = Vobs_orig * sin_ratio
        
        # Chi2
        chi2 = np.sum(((Vobs_fit - Vpred) / errV)**2)
        return chi2 + prior_penalty
        
    x0 = [0.5]
    bounds = [(0.1, 5.0)]
    
    if has_bulge:
        x0.append(0.7)
        bounds.append((0.1, 5.0))
    if float_dist:
        x0.append(1.0)
        bounds.append((0.5, 1.5))
    if float_inc:
        x0.append(i_nom)
        bounds.append((max(10.0, i_nom - 20.0), min(90.0, i_nom + 20.0)))
    
    res = minimize(nll, x0, bounds=bounds, method="L-BFGS-B")
    
    chi2_val = res.fun
    k = len(res.x)
    n = len(Rad)
    
    return {
        "name": gal["name"],
        "chi2": chi2_val,
        "n_points": n,
        "k_params": k,
        "success": res.success
    }

def run_pipeline():
    print(f"STAT-001 Inference Pipeline started (using {cpu_count()} cores).")
    
    # Load master catalog for nominal inclinations
    master_cat = pd.read_csv(SPARC_DIR / "SPARC_MassModels.csv")
    inc_dict = dict(zip(master_cat["Name"], master_cat["i"]))
    
    # Load Qual catalog
    qual_cat = pd.read_csv(SPARC_DIR / "SPARC_Qual.csv")
    qual_dict = dict(zip(qual_cat["Name"], qual_cat["Qual"]))
    
    dat_files = glob.glob(str(SPARC_DIR / "*_rotmod.dat"))
    dat_files = [f for f in dat_files if "ITSM-Cosmologist" not in f]
    
    galaxies = [load_sparc_data(Path(f)) for f in dat_files]
    print(f"Loaded {len(galaxies)} SPARC galaxies.")
    
    ir_models = {
        "Geometric": derived_geometric_ir(V_eff=V_EFF_MAT001),
        "Phenomenological": derived_phenomenological_ir(V_eff=V_EFF_MAT001)
    }
    
    results = {}
    
    modes = [
        ("Rigid (Fixed D, Fixed i)", False, False, False, False), 
        ("Floated (Free D ±10%, Fixed i)", True, False, False, False),
        ("Fully Floated (Free D ±10%, Free i ±5°)", True, True, False, False),
        ("Rigid [Q1+Q2 Only, Flat Priors]", False, False, True, True),
        ("Fully Floated [Q1+Q2 Only, Flat Priors]", True, True, True, True)
    ]
    
    for mode_name, float_dist, float_inc, filter_q3, flat_priors in modes:
        print(f"\n{'='*60}\nRUNNING MODE: {mode_name}\n{'='*60}")
        
        # Filter galaxies if needed
        active_galaxies = []
        for gal in galaxies:
            if filter_q3 and qual_dict.get(gal["name"], 1) == 3:
                continue
            active_galaxies.append(gal)
            
        print(f"Using {len(active_galaxies)} galaxies for this mode.")
        
        for name, ir in ir_models.items():
            print(f"\nEvaluating IR Law: {name} (a0={ir.a0:.3f}, C_obs={ir.C_obs:.3f})")
            t0 = time.time()
            
            pool = Pool(processes=cpu_count())
            # Inject nominal inclination and flat_priors for each galaxy
            fit_args = [(gal, ir, float_dist, float_inc, inc_dict.get(gal["name"], 60.0), flat_priors) for gal in active_galaxies]
            fits = pool.map(fit_galaxy, fit_args)
            pool.close()
            pool.join()
            
            total_chi2 = sum(f["chi2"] for f in fits)
            total_n = sum(f["n_points"] for f in fits)
            total_k = sum(f["k_params"] for f in fits)
            
            bic = total_chi2 + total_k * np.log(total_n)
            aic = total_chi2 + 2 * total_k
            reduced_chi2 = total_chi2 / (total_n - total_k)
            
            print(f"  Time: {time.time() - t0:.2f}s")
            print(f"  Total Chi2: {total_chi2:.1f}")
            print(f"  Reduced Chi2: {reduced_chi2:.3f}")
            print(f"  BIC: {bic:.1f}")
            print(f"  AIC: {aic:.1f}")
            
            results[f"{name} | {mode_name}"] = {
                "a0": ir.a0,
                "C_obs": ir.C_obs,
                "total_chi2": total_chi2,
                "reduced_chi2": reduced_chi2,
                "BIC": bic,
                "AIC": aic,
                "total_n": total_n,
                "total_k": total_k
            }
        
    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "stat001_inference_summary.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_dir / 'stat001_inference_summary.json'}")
        
    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "stat001_inference_summary.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_dir / 'stat001_inference_summary.json'}")

if __name__ == "__main__":
    run_pipeline()
