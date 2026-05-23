"""
Integrated Toroidal-Syntropic Model (ITSM) - SPARC Meta-Analysis & Quality Filter
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Protocol: Automated Post-Processing, Quality Cuts, and Cosmological Synthesis
"""

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set plotting standards for Tier-1 publication
plt.rcParams.update({"text.usetex": True, "font.family": "serif"})

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
    except Exception:
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

    master_records = []
    
    print(f"Processing {len(chain_files)} Galactic Records...")

    for chain_path in chain_files:
        g_name = os.path.basename(chain_path).replace("_MCMC_Chains.csv", "")
        try:
            chains = pd.read_csv(chain_path)
            if chains.empty or len(chains) < 100: continue
            
            p_disk = np.percentile(chains['Upsilon_disk'].values, [16, 50, 84])
            p_bulge = np.percentile(chains['Upsilon_bulge'].values, [16, 50, 84])
            p_h0 = np.percentile(chains['H0'].values, [16, 50, 84])

            raw_file = os.path.join(raw_data_dir, f"{g_name}_rotmod.dat")
            df_raw = load_sparc_data(raw_file)
            
            chi2, chi2_nu, dof = np.nan, np.nan, 0
            if df_raw is not None and not df_raw.empty:
                V_fit = compute_itsm_velocity(df_raw['R'], df_raw['Vgas'], df_raw['Vdisk'], 
                                              df_raw['Vbulge'], p_disk[1], p_bulge[1], p_h0[1])
                dof = len(df_raw['R']) - 3
                if dof > 0:
                    chi2 = np.sum(((df_raw['Vobs'] - V_fit) / df_raw['errV']) ** 2)
                    chi2_nu = chi2 / dof

            master_records.append({
                'Galaxy': g_name, 'Upsilon_disk': p_disk[1], 'Upsilon_bulge': p_bulge[1],
                'H0': p_h0[1], 'Chi2_nu': chi2_nu, 'dof': dof,
                'High_Fidelity': 1 if (p_h0[1] > 51.0 and chi2_nu <= 5.0 and dof > 0) else 0,
                'Prior_Clipped': 1 if p_h0[1] <= 51.0 else 0
            })
        except Exception: 
            continue

    if not master_records:
        print("CRITICAL: No valid records found.")
        return

    df_master = pd.DataFrame(master_records)
    df_hi_fi = df_master[df_master['High_Fidelity'] == 1].reset_index(drop=True)

    # 1. Export CSV
    df_master.to_csv(os.path.join(batch_dir, "ITSM_SPARC_Meta_Analysis_Summary.csv"), index=False)

    # 2. Write LaTeX Table
    tex_path = os.path.join(script_dir, "..", "Manuscript", "appendix_sparc_table.tex")
    with open(tex_path, "w") as f:
        f.write("\\begin{longtable}{lcccccc}\n\\toprule\nGalaxy & $\\Upsilon_{\\text{disk}}$ & $\\Upsilon_{\\text{bulge}}$ & $H_0$ & $\\chi^2_\\nu$ & DoF & Quality \\\\\n\\midrule\n")
        for _, r in df_master.iterrows():
            q = "High-Fi" if r['High_Fidelity'] else ("Clipped" if r['Prior_Clipped'] else "Standard")
            f.write(f"{r['Galaxy'].replace('_', '\\_')} & {r['Upsilon_disk']:.3f} & {r['Upsilon_bulge']:.3f} & {r['H0']:.1f} & {r['Chi2_nu']:.2f} & {r['dof']} & {q} \\\\\n")
        f.write("\\bottomrule\n\\end{longtable}\n")

    # 3. Output Synthesis
    print(f"Synthesis Complete. High-Fi Sample Size: {len(df_hi_fi)}")
    if not df_hi_fi.empty:
        h0_mean = df_hi_fi['H0'].mean()
        h0_err = df_hi_fi['H0'].std() / np.sqrt(len(df_hi_fi))
        print(f"H0 Convergence: {h0_mean:.2f} ± {h0_err:.2f}")

    # 4. Generate Histogram
    plt.figure(figsize=(10, 6))
    plt.hist(df_hi_fi['H0'], bins=20, color='#1f77b4', edgecolor='black', alpha=0.6, label='ITSM SPARC Sample')
    
    # Statistical Annotations
    mean_h0 = df_hi_fi['H0'].mean()
    stderr_h0 = df_hi_fi['H0'].std() / np.sqrt(len(df_hi_fi))
    plt.axvline(mean_h0, color='#d62728', linestyle='-', lw=3, label=f'ITSM Mean $H_0 = {mean_h0:.2f} \\pm {stderr_h0:.2f}$')
    plt.axvspan(mean_h0 - stderr_h0, mean_h0 + stderr_h0, color='#d62728', alpha=0.2, label='ITSM $1\\sigma$ Uncertainty')
    plt.axvline(73.04, color='#ff7f0e', linestyle='--', lw=2.5, label='Local Distance Ladder (Riess et al. 2022)')
    
    plt.xlabel(r'Inferred Hubble Parameter $H_0$ [km s$^{-1}$ Mpc$^{-1}$]', fontsize=12, fontweight='bold')
    plt.ylabel('Galaxy Count', fontsize=12, fontweight='bold')
    plt.title(r'\textbf{ITSM Convergence Manifold: SPARC Statistical Anchor}', fontsize=14, pad=15)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right', frameon=True, fontsize=10, shadow=True)
    plt.tight_layout()
    
    figures_dir = os.path.join(assets_dir, "Figures")
    os.makedirs(figures_dir, exist_ok=True)
    fig_out_path = os.path.join(figures_dir, "ITSM_H0_Convergence_Histogram.png")
    plt.savefig(fig_out_path, dpi=600, bbox_inches='tight')
    plt.close()
    
    print(f"Publication-ready figure saved to: {fig_out_path}")

if __name__ == "__main__":
    analyze_batch_data()