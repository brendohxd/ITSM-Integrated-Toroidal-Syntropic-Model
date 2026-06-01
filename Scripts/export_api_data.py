import os
import glob
import pandas as pd
import numpy as np
import json

def process_mcmc_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mcmc_results_dir = os.path.join(script_dir, "..", "Analysis", "Experimental", "MCMC_v2", "results")
    out_dir = os.path.join(script_dir, "..", "Assets", "API_Exports")
    os.makedirs(out_dir, exist_ok=True)

    csv_files = glob.glob(os.path.join(mcmc_results_dir, "*_MCMC_Chains.csv"))
    
    summary_data = {}
    corner_samples = {}

    print(f"[*] Processing {len(csv_files)} galaxy MCMC chains...")
    for f in csv_files:
        gal_name = os.path.basename(f).replace("_MCMC_Chains.csv", "")
        df = pd.read_csv(f)
        
        # Calculate percentiles (16, 50, 84)
        summary = {}
        for col in df.columns:
            p16, p50, p84 = np.percentile(df[col].dropna(), [16, 50, 84])
            summary[col] = [round(p16, 4), round(p50, 4), round(p84, 4)]
        
        summary_data[gal_name] = summary
        
        # Thinned sample for corner plots (500 samples)
        if len(df) > 500:
            df_thinned = df.sample(n=500, random_state=42)
        else:
            df_thinned = df
            
        corner_samples[gal_name] = df_thinned.round(4).to_dict(orient='list')

    # Save outputs
    sum_path = os.path.join(out_dir, "sparc_mcmc_summary.json")
    with open(sum_path, 'w') as out:
        json.dump(summary_data, out)
    print(f"[+] Saved summary -> {sum_path}")

    corn_path = os.path.join(out_dir, "sparc_mcmc_corner_samples.json")
    with open(corn_path, 'w') as out:
        json.dump(corner_samples, out)
    print(f"[+] Saved corner samples -> {corn_path}")

    # Process Hierarchical if exists
    hier_path = os.path.join(script_dir, "..", "Analysis", "Experimental", "Joint_MCMC", "itsm_hierarchical_joint_chain.csv")
    if os.path.exists(hier_path):
        print("[*] Processing Hierarchical Joint Chain...")
        df_h = pd.read_csv(hier_path)
        h_summary = {}
        for col in df_h.columns:
            p16, p50, p84 = np.percentile(df_h[col].dropna(), [16, 50, 84])
            h_summary[col] = [round(p16, 4), round(p50, 4), round(p84, 4)]
        
        if len(df_h) > 2000:
            df_h_thin = df_h.sample(n=2000, random_state=42)
        else:
            df_h_thin = df_h
            
        hier_data = {
            "summary": h_summary,
            "samples": df_h_thin.round(4).to_dict(orient='list')
        }
        out_h_path = os.path.join(out_dir, "hierarchical_joint_chain.json")
        with open(out_h_path, 'w') as out:
            json.dump(hier_data, out)
        print(f"[+] Saved hierarchical chain -> {out_h_path}")
    else:
        print("[!] Hierarchical chain not found. (Still running?)")

if __name__ == "__main__":
    process_mcmc_data()
