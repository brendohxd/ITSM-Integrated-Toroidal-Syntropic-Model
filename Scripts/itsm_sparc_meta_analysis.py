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
import sys
import os
from itsm_plot_style import apply_tier1_style
apply_tier1_style()

# Publication plot style — usetex disabled so f-string labels render correctly


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

    chain_files = glob.glob(os.path.join(batch_dir, "MCMC_v2_Chain_CSVs", "*_MCMC_Chains.csv"))
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
    tex_path = os.path.join(script_dir, "..", "Manuscript", "Supplementary", "appendix_sparc_table.tex")
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

    # Plot clipped (low-H0) galaxies separately in a muted colour
    df_clipped = df_master[df_master['Prior_Clipped'] == 1]
    if not df_clipped.empty:
        plt.hist(df_clipped['H0'], bins=20, range=(50, 100),
                 color='#d9534f', edgecolor='white', alpha=0.45,
                 label=f'Prior-clipped galaxies (n={len(df_clipped)})')

    plt.hist(df_hi_fi['H0'], bins=20, range=(50, 100),
             color='#1f77b4', edgecolor='white', alpha=0.75,
             label=f'High-fidelity SPARC sample (n={len(df_hi_fi)})')

    # Statistical annotations — use Unicode +/- so f-strings work cleanly
    mean_h0   = df_hi_fi['H0'].mean()
    median_h0 = df_hi_fi['H0'].median()
    stderr_h0 = df_hi_fi['H0'].std() / np.sqrt(len(df_hi_fi))

    plt.axvline(median_h0, color='#e07b00', linestyle='-', lw=2.5,
                label=f'ITSM ensemble median:  H\u2080 = {median_h0:.2f} \u00b1 {stderr_h0:.2f}  km/s/Mpc')
    plt.axvspan(median_h0 - stderr_h0, median_h0 + stderr_h0,
                color='#e07b00', alpha=0.15)
    plt.axvline(67.4, color='#d62728', linestyle='--', lw=2,
                label='Planck 2018 CMB:  H\u2080 = 67.4 \u00b1 0.5  km/s/Mpc')
    plt.axvspan(66.9, 67.9, color='#d62728', alpha=0.08)
    plt.axvline(73.04, color='#2ca02c', linestyle='-.', lw=2,
                label='SH0ES (Riess et al. 2022):  H\u2080 = 73.04 \u00b1 1.04  km/s/Mpc')
    plt.axvspan(72.0, 74.08, color='#2ca02c', alpha=0.08)

    plt.xlabel('Inferred Hubble Parameter  H\u2080  [km s\u207b\u00b9 Mpc\u207b\u00b9]',
               fontsize=12, fontweight='bold')
    plt.ylabel('Number of galaxies', fontsize=12, fontweight='bold')
    plt.title(
        'ITSM MCMC: Global H\u2080 Distribution \u2014 175 SPARC Galaxies\n'
        '32 walkers \u00d7 3000 steps per galaxy (multicore, 16 cores)',
        fontsize=13, pad=12
    )
    plt.xlim(50, 100)
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.legend(loc='upper right', frameon=True, fontsize=9.5)
    plt.tight_layout()
    
    figures_dir = os.path.join(assets_dir, "Figures")
    os.makedirs(figures_dir, exist_ok=True)
    fig_out_path = os.path.join(figures_dir, "ITSM_H0_Convergence_Histogram.png")
    plt.savefig(fig_out_path, bbox_inches='tight')
    plt.close()
    
    print(f"Publication-ready figure saved to: {fig_out_path}")

if __name__ == "__main__":
    analyze_batch_data()