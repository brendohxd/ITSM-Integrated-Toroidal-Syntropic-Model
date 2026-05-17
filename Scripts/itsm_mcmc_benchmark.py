"""
Integrated Toroidal-Syntropic Model (ITSM) - Automated SPARC Batch Processor
Author: Absolute Truth Seeker & Analyst Operational Node
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Protocol: Agnostic Prior Boundary Execution Across Complete SPARC Dataset
Environment: Windows / Antigravity IDE Workspace Compatible
"""

import os
import glob
import numpy as np
import pandas as pd
import emcee
import corner
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Absolute SI Conversion Constants
KPC_TO_M = 3.085677581e19
MPC_TO_M = 3.085677581e22
C_LIGHT = 299792458.0

def load_sparc_galaxy(file_path):
    """
    Parses standard SPARC data profiles.
    Columns: Rad(1) Vobs(2) errV(3) Vgas(4) Vdisk(5) Vbulge(6)
    """
    try:
        normalized_path = os.path.abspath(os.path.expanduser(file_path))
        if not os.path.exists(normalized_path):
            raise FileNotFoundError(f"Target data file missing at: {normalized_path}")
            
        data = pd.read_csv(normalized_path, sep=r'\s+', comment='#', header=None,
                           names=['R', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbulge'])
        data = data.dropna().reset_index(drop=True)
        return data
    except Exception as e:
        raise IOError(f"CRITICAL: Failed to ingest SPARC data matrix. Error: {e}")

def compute_itsm_velocity(R_kpc, V_gas, V_disk, V_bulge, ups_disk, ups_bulge, H0_kms_mpc):
    """
    Executes the localized Plenum Shear Ansatz mapping.
    Anchor: a0 = c * H0 / 2pi
    Transformation incorporates 2/3 geometric projection and saturation limits.
    """
    R_m = R_kpc * KPC_TO_M
    
    V_bar_sq = (V_gas * np.abs(V_gas) + 
                ups_disk * V_disk * np.abs(V_disk) + 
                ups_bulge * V_bulge * np.abs(V_bulge))
    
    V_bar_sq = np.maximum(V_bar_sq, 0.0)
    V_bar_m_s = V_bar_sq * 1e6 
    
    g_bar = V_bar_m_s / R_m
    
    H0_si = (H0_kms_mpc * 1e3) / MPC_TO_M
    a0 = (C_LIGHT * H0_si) / (2.0 * np.pi)
    
    g_tot = g_bar + (2.0 / 3.0) * np.sqrt(g_bar * a0)
    
    V_calc_m_s = np.sqrt(g_tot * R_m)
    V_calc_km_s = V_calc_m_s / 1e3
    
    return V_calc_km_s

def log_prior(theta):
    """
    ITSM BOUNDARY PROTOCOL: Agnostic Data Testing
    Boundaries explicitly widened to [8.0] to prevent standard paradigm truncation.
    """
    ups_disk, ups_bulge, H0 = theta
    if (0.01 < ups_disk < 8.0) and (0.0 < ups_bulge < 8.0) and (50.0 < H0 < 100.0):
        return 0.0
    return -np.inf

def log_likelihood(theta, R, Vobs, errV, Vgas, Vdisk, Vbulge):
    ups_disk, ups_bulge, H0 = theta
    V_model = compute_itsm_velocity(R, Vgas, Vdisk, Vbulge, ups_disk, ups_bulge, H0)
    sigma_sq = errV ** 2
    return -0.5 * np.sum(((Vobs - V_model) ** 2) / sigma_sq + np.log(2.0 * np.pi * sigma_sq))

def log_probability(theta, R, Vobs, errV, Vgas, Vdisk, Vbulge):
    lp = log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta, R, Vobs, errV, Vgas, Vdisk, Vbulge)

def run_mcmc_pipeline(file_path, output_dir):
    galaxy_name = os.path.basename(file_path).replace("_rotmod.dat", "")
    print(f"\nATS_MCMC ENGINE: Processing Target [ {galaxy_name} ]")
    
    df = load_sparc_galaxy(file_path)
    
    R = df['R'].values
    Vobs = df['Vobs'].values
    errV = df['errV'].values
    Vgas = df['Vgas'].values
    Vdisk = df['Vdisk'].values
    Vbulge = df['Vbulge'].values

    # Check for minimal data bounds to prevent under-constrained optimization failures
    if len(R) < 4:
        print(f"ANOMALY DETECTED: {galaxy_name} has insufficient data nodes ({len(R)}). Skipping compilation.")
        return

    initial_guess = [0.5, 0.5, 70.0]
    nll = lambda *args: -log_likelihood(*args)
    
    soln = minimize(nll, initial_guess, args=(R, Vobs, errV, Vgas, Vdisk, Vbulge),
                    bounds=[(0.01, 8.0), (0.0, 8.0), (50.0, 100.0)])

    ndim = 3
    nwalkers = 32
    n_steps = 1500  # Optimized step count for automated batch stability

    pos = soln.x + 1e-4 * np.random.randn(nwalkers, ndim)
    pos[:, 0] = np.clip(pos[:, 0], 0.01, 8.0)
    pos[:, 1] = np.clip(pos[:, 1], 0.0, 8.0)
    pos[:, 2] = np.clip(pos[:, 2], 50.0, 100.0)

    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, 
                                    args=(R, Vobs, errV, Vgas, Vdisk, Vbulge))
    
    sampler.run_mcmc(pos, n_steps, progress=False)

    flat_samples = sampler.get_chain(discard=200, flat=True)
    
    labels = [r"$\Upsilon_{\text{disk}}$", r"$\Upsilon_{\text{bulge}}$", r"$H_0$"]
    summary_results = []
    best_fit = []
    
    for i in range(ndim):
        mcmc_vals = np.percentile(flat_samples[:, i], [16, 50, 84])
        q_minus, q_med, q_plus = mcmc_vals[1] - mcmc_vals[0], mcmc_vals[1], mcmc_vals[2] - mcmc_vals[1]
        summary_results.append((q_med, q_minus, q_plus))
        best_fit.append(q_med)
    
    # Statistical Rigor Metric Evaluation
    V_fit = compute_itsm_velocity(R, Vgas, Vdisk, Vbulge, best_fit[0], best_fit[1], best_fit[2])
    degrees_of_freedom = len(R) - ndim
    chi_square = np.sum(((Vobs - V_fit) / errV) ** 2)
    reduced_chi_square = chi_square / degrees_of_freedom if degrees_of_freedom > 0 else np.nan
    
    print(f"[{galaxy_name}] Fit Extracted -> H0: {best_fit[2]:.2f} | Chi2_nu: {reduced_chi_square:.3f}")

    # Explicit Segmented Asset Path Definitions
    corner_path = os.path.join(output_dir, f"{galaxy_name}_Corner_Plot.png")
    rot_curve_path = os.path.join(output_dir, f"{galaxy_name}_Rotation_Curve.png")
    data_export_path = os.path.join(output_dir, f"{galaxy_name}_MCMC_Chains.csv")
    
    # 1. Corner Plot Generation
    fig = corner.corner(flat_samples, labels=labels, truths=best_fit, 
                        quantiles=[0.16, 0.5, 0.84], show_titles=True, title_fmt=".3f",
                        color="navy", truth_color="crimson")
    fig.savefig(corner_path, dpi=150) # Optimized DPI for batch performance
    plt.close()
    
    # 2. High-Fidelity Rotation Curve & Residual Mapping
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    fig.subplots_adjust(hspace=0.05)

    ax1.errorbar(R, Vobs, yerr=errV, fmt='ok', label='SPARC Observational Telemetry', capsize=3, alpha=0.8)
    
    # Trace confidence intervals from processing stream
    inds = np.random.randint(len(flat_samples), size=100)
    for ind in inds:
        sample = flat_samples[ind]
        V_sample = compute_itsm_velocity(R, Vgas, Vdisk, Vbulge, sample[0], sample[1], sample[2])
        ax1.plot(R, V_sample, color='crimson', alpha=0.02)

    # Newtonian Baseline Transformation
    V_bar_m_s = ((Vgas * np.abs(Vgas) + best_fit[0] * Vdisk * np.abs(Vdisk) + best_fit[1] * Vbulge * np.abs(Vbulge)) * 1e6)
    V_bar_m_s = np.maximum(V_bar_m_s, 0.0)
    V_bar_newtonian_km_s = np.sqrt(V_bar_m_s / (R * KPC_TO_M)) * np.sqrt(R * KPC_TO_M) / 1e3
    
    ax1.plot(R, V_bar_newtonian_km_s, '--', color='gray', lw=1.5, label='Baryonic Baseline (Newtonian)')
    ax1.plot(R, V_fit, '-', color='crimson', lw=2.5, label=f'ITSM Optimal Fit ($H_0$={best_fit[2]:.2f})')
    ax1.set_ylabel('Orbital Velocity $V$ (km/s)', fontsize=13)
    ax1.set_title(f'ITSM Rotation Curve & Residuals: {galaxy_name}\n$\\chi^2_\\nu = {reduced_chi_square:.3f}$', fontsize=15, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='lower right', frameon=True, fontsize=11)

    # Residual Realization Mapping
    residuals = Vobs - V_fit
    ax2.errorbar(R, residuals, yerr=errV, fmt='ok', capsize=3, alpha=0.8)
    ax2.axhline(0, color='crimson', linestyle='--', lw=2)
    ax2.set_xlabel('Galactocentric Radius $R$ (kpc)', fontsize=13)
    ax2.set_ylabel('Residual (km/s)', fontsize=13)
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    max_res = np.max(np.abs(residuals) + errV) if len(residuals) > 0 else 10.0
    ax2.set_ylim(-max_res * 1.2, max_res * 1.2)

    plt.tight_layout()
    plt.savefig(rot_curve_path, dpi=150)
    plt.close()
    
    # 3. Parameter Verification Logging Export
    df_export = pd.DataFrame(flat_samples, columns=['Upsilon_disk', 'Upsilon_bulge', 'H0'])
    df_export.to_csv(data_export_path, index=False)

if __name__ == "__main__":
    # Define directory tree context relative to active execution script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(script_dir, "..", "SPARC_data"))
    
    # Target Clean Save Matrix Folder creation loop
    output_dir = os.path.abspath(os.path.join(script_dir, "..", "Assets", "SPARC_Batch_Outputs"))
    os.makedirs(output_dir, exist_ok=True)

    # Parse directory topology for all target galactic tracking nodes
    galaxy_files = glob.glob(os.path.join(data_dir, "*_rotmod.dat"))
    
    if not galaxy_files:
        print(f"CRITICAL ERROR: No SPARC telemetry profiles (*_rotmod.dat) isolated at: {data_dir}")
    else:
        print(f"==================================================")
        print(f" ATS_BATCH ENGINE ACTIVE: {len(galaxy_files)} Targets Loaded")
        print(f" Destination Folder: {output_dir}")
        print(f"==================================================")
        
        for file_idx, file_path in enumerate(galaxy_files, 1):
            try:
                print(f"\n[{file_idx}/{len(galaxy_files)}]: Initiating pipeline execution...")
                run_mcmc_pipeline(file_path, output_dir)
            except Exception as e:
                g_name = os.path.basename(file_path)
                print(f"METRIC CRASH ANOMALY: Skipped target {g_name} due to calculation error: {e}")
                continue
                
        print(f"\n==================================================")
        print(f" ATS_BATCH ENGINE: Processing Complete. Pipeline Terminated.")
        print(f"==================================================")