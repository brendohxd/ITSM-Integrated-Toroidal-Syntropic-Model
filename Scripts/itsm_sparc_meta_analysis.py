"""
Integrated Toroidal-Syntropic Model (ITSM) - SPARC Meta-Analysis & Quality Filter
Author: Absolute Truth Seeker & Analyst Operational Node
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Protocol: Automated Post-Processing, Quality Cuts, and Cosmological Synthesis
Environment: Windows / Antigravity IDE Workspace Compatible
"""

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Absolute SI Conversion Constants
KPC_TO_M = 3.085677581e19
MPC_TO_M = 3.085677581e22
C_LIGHT = 299792458.0

def load_sparc_data(file_path):
    """Safely ingests raw SPARC telemetry matrices for residual validation."""
    try:
        data = pd.read_csv(file_path, sep=r'\s+', comment='#', header=None,
                           names=['R', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbulge'])
        return data.dropna().reset_index(drop=True)
    except Exception as e:
        return None

def compute_itsm_velocity(R_kpc, V_gas, V_disk, V_bulge, ups_disk, ups_bulge, H0_kms_mpc):
    """Executes Plenum Shear Ansatz mapping vector transformations in SI metric."""
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
    return V_calc_m_s / 1e3

def analyze_batch_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    batch_dir = os.path.abspath(os.path.join(script_dir, "..", "Assets", "SPARC_Batch_Outputs"))
    raw_data_dir = os.path.abspath(os.path.join(script_dir, "..", "SPARC_data"))
    assets_dir = os.path.abspath(os.path.join(script_dir, "..", "Assets"))

    chain_files = glob.glob(os.path.join(batch_dir, "*_MCMC_Chains.csv"))
    if not chain_files:
        print(f"CRITICAL ERROR: No MCMC trace records detected at: {batch_dir}")
        return

    print(f"==================================================")
    print(f" ATS META-ANALYSIS: Processing {len(chain_files)} Galactic Records")
    print(f"==================================================")

    master_records = []

    for idx, chain_path in enumerate(chain_files, 1):
        g_name = os.path.basename(chain_path).replace("_MCMC_Chains.csv", "")
        
        # 1. Parse and extract stats from the flattened MCMC chain
        try:
            chains = pd.read_csv(chain_path)
            if chains.empty or len(chains) < 100:
                continue
        except Exception:
            continue

        # Compute quantiles [16th, 50th, 84th] for parameter tracking
        p_disk = np.percentile(chains['Upsilon_disk'].values, [16, 50, 84])
        p_bulge = np.percentile(chains['Upsilon_bulge'].values, [16, 50, 84])
        p_h0 = np.percentile(chains['H0'].values, [16, 50, 84])

        u_disk_med, u_disk_min, u_disk_max = p_disk[1], p_disk[1] - p_disk[0], p_disk[2] - p_disk[1]
        u_bulge_med, u_bulge_min, u_bulge_max = p_bulge[1], p_bulge[1] - p_bulge[0], p_bulge[2] - p_bulge[1]
        h0_med, h0_min, h0_max = p_h0[1], p_h0[1] - p_h0[0], p_h0[2] - p_h0[1]

        # 2. Cross-verify kinematic performance against raw SPARC telemetry files
        raw_file = os.path.join(raw_data_dir, f"{g_name}_rotmod.dat")
        df_raw = load_sparc_data(raw_file)
        
        chi2, chi2_nu, dof = np.nan, np.nan, 0
        if df_raw is not None and not df_raw.empty:
            R = df_raw['R'].values
            Vobs = df_raw['Vobs'].values
            errV = df_raw['errV'].values
            Vgas = df_raw['Vgas'].values
            Vdisk = df_raw['Vdisk'].values
            Vbulge = df_raw['Vbulge'].values

            V_fit = compute_itsm_velocity(R, Vgas, Vdisk, Vbulge, u_disk_med, u_bulge_med, h0_med)
            dof = len(R) - 3
            if dof > 0:
                chi2 = np.sum(((Vobs - V_fit) / errV) ** 2)
                chi2_nu = chi2 / dof

        # 3. Categorize quality framework status
        is_prior_clipped = (h0_med <= 51.0)
        is_high_fidelity = (not is_prior_clipped) and (chi2_nu <= 5.0) and (dof > 0)

        master_records.append({
            'Galaxy': g_name,
            'Upsilon_disk': u_disk_med, 'Ups_disk_minus': u_disk_min, 'Ups_disk_plus': u_disk_max,
            'Upsilon_bulge': u_bulge_med, 'Ups_bulge_minus': u_bulge_min, 'Ups_bulge_plus': u_bulge_max,
            'H0': h0_med, 'H0_minus': h0_min, 'H0_plus': h0_max,
            'Chi2': chi2, 'Chi2_nu': chi2_nu, 'dof': dof,
            'High_Fidelity': 1 if is_high_fidelity else 0,
            'Prior_Clipped': 1 if is_prior_clipped else 0
        })

    # Create master DataFrames
    df_master = pd.DataFrame(master_records)
    df_hi_fi = df_master[df_master['High_Fidelity'] == 1].reset_index(drop=True)
    df_clipped = df_master[df_master['Prior_Clipped'] == 1].reset_index(drop=True)

    # Export consolidated summary ledger to SPARC_Batch_Outputs
    csv_out_path = os.path.join(batch_dir, "ITSM_SPARC_Meta_Analysis_Summary.csv")
    df_master.to_csv(csv_out_path, index=False)

    # 3.5 Generate LaTeX Table for Manuscript Integration
    manuscript_dir = os.path.abspath(os.path.join(script_dir, "..", "Manuscript"))
    tex_out_path = os.path.join(manuscript_dir, "appendix_sparc_table.tex")
    
    with open(tex_out_path, "w") as f:
        f.write("\\begin{longtable}{lcccccc}\n")
        f.write("\\caption{Comprehensive SPARC MCMC Parameter Ledger} \\label{tab:full_ledger} \\\\\n")
        f.write("\\toprule\n")
        f.write("Galaxy & $\\Upsilon_{\\text{disk}}$ & $\\Upsilon_{\\text{bulge}}$ & $H_0$ (km/s/Mpc) & $\\chi^2_\\nu$ & DoF & Quality \\\\\n")
        f.write("\\midrule\n")
        f.write("\\endfirsthead\n")
        f.write("\\multicolumn{7}{c} {{\\tablename\\ \\thetable{} -- continued from previous page}} \\\\\n")
        f.write("\\toprule\n")
        f.write("Galaxy & $\\Upsilon_{\\text{disk}}$ & $\\Upsilon_{\\text{bulge}}$ & $H_0$ (km/s/Mpc) & $\\chi^2_\\nu$ & DoF & Quality \\\\\n")
        f.write("\\midrule\n")
        f.write("\\endhead\n")
        f.write("\\midrule\n")
        f.write("\\multicolumn{7}{r}{{Continued on next page}} \\\\\n")
        f.write("\\endfoot\n")
        f.write("\\bottomrule\n")
        f.write("\\endlastfoot\n")
        
        for _, row in df_master.iterrows():
            quality = "High-Fi" if row['High_Fidelity'] == 1 else ("Clipped" if row['Prior_Clipped'] == 1 else "Standard")
            f.write(f"{row['Galaxy']} & {row['Upsilon_disk']:.3f} & {row['Upsilon_bulge']:.3f} & {row['H0']:.2f} & {row['Chi2_nu']:.3f} & {row['dof']} & {quality} \\\\\n")
            
        f.write("\\end{longtable}\n")

    print(f"ATS META-ANALYSIS: LaTeX ledger written to: {tex_out_path}")

    # 4. Global Cosmological Syntropic Evaluation Output
    print("\n" + "="*50)
    print("   GLOBAL ITSM COSMOLOGICAL SYNTHESIS RESULTS")
    print("="*50)
    print(f"Total Systems Analyzed:      {len(df_master)}")
    print(f"Prior Wall Clipping Omissions: {len(df_clipped)}")
    print(f"High-Fidelity Sample Size:   {len(df_hi_fi)}")
    print("-" * 50)
    
    if not df_hi_fi.empty:
        h0_array = df_hi_fi['H0'].values
        mean_h0 = np.mean(h0_array)
        median_h0 = np.median(h0_array)
        std_h0 = np.std(h0_array, ddof=1)
        stderr_h0 = std_h0 / np.sqrt(len(h0_array))
        mean_chi2_nu = np.mean(df_hi_fi['Chi2_nu'].values)

        print(f"Ensemble Mean H0:    {mean_h0:.3f} km/s/Mpc")
        print(f"Ensemble Median H0:  {median_h0:.3f} km/s/Mpc")
        print(f"Standard Deviation:  {std_h0:.3f} km/s/Mpc")
        print(f"Standard Error (SE):  ±{stderr_h0:.3f} km/s/Mpc")
        print(f"Mean High-Fi Chi2_nu: {mean_chi2_nu:.4f}")
        print("-" * 50)
        print(f"ITSM CONVERGENCE MANIFOLD: H0 = {mean_h0:.2f} ± {stderr_h0:.2f} km/s/Mpc")
    else:
        print("ANOMALY: High-Fidelity filter tracking array returned empty entries.")
    print("="*50 + "\n")

    # 5. Generate Publication-Ready Verification Visual Histogram
    if not df_hi_fi.empty:
        plt.figure(figsize=(9, 6))
        
        # Plot distribution configuration
        counts, bins, patches = plt.hist(df_hi_fi['H0'].values, bins=15, color='navy', 
                                         edgecolor='black', alpha=0.75, label='High-Fidelity SPARC Sample')
        
        # Apply visual indicators matching Hubble Tension values
        plt.axvline(mean_h0, color='crimson', linestyle='-', lw=2.5, 
                    label=f'ITSM Mean $H_0 = {mean_h0:.2f}$ km/s/Mpc')
        plt.axvspan(mean_h0 - stderr_h0, mean_h0 + stderr_h0, color='crimson', alpha=0.15, 
                    label=f'ITSM $1\\sigma$ Standard Error (±{stderr_h0:.2f})')
        
        # Standard Distance Ladder Benchmark Context Box
        plt.axvline(73.04, color='darkorange', linestyle=':', lw=2, label='Local Distance Ladder (Riess et al. 2022)')
        
        plt.xlabel(r'Inferred Hubble Parameter $H_0$ (km/s/Mpc)', fontsize=13)
        plt.ylabel('Galaxy Count', fontsize=13)
        plt.title(r'ITSM Metric Anchor Convergence Summary ($a_0 = \frac{c \cdot H_0}{2\pi}$)', fontsize=14, fontweight='bold')
        plt.xlim(55, 90)
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.legend(loc='upper right', frameon=True, fontsize=10)
        plt.tight_layout()
        
        figures_dir = os.path.join(assets_dir, "Figures")
        os.makedirs(figures_dir, exist_ok=True)
        fig_out_path = os.path.join(figures_dir, "ITSM_H0_Convergence_Histogram.png")
        plt.savefig(fig_out_path, dpi=300)
        plt.close()
        print(f"ATS META-ANALYSIS: Analytical summary table written to: {csv_out_path}")
        print(f"ATS META-ANALYSIS: High-fidelity histogram plotted at: {fig_out_path}")

if __name__ == "__main__":
    analyze_batch_data()