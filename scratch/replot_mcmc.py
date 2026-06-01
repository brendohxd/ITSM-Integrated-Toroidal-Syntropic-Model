import os
import pandas as pd
import corner
import matplotlib.pyplot as plt
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Scripts')))
from itsm_plot_style import apply_tier1_style

# Apply global styling
apply_tier1_style()

def plot_hierarchical_joint():
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Analysis", "Experimental", "Joint_MCMC", "itsm_hierarchical_joint_chain.csv"))
    if not os.path.exists(csv_path):
        print("MCMC joint chain CSV not found.")
        return
        
    df = pd.read_csv(csv_path)
    samples = df[["H0", "Om", "n"]].values
    
    fig = corner.corner(
        samples, labels=[r"$H_0$", r"$\Omega_m$", r"$n$"],
        truths=[None, None, None],
        quantiles=[0.16, 0.5, 0.84],
        show_titles=True,
        # Our engine handles the fonts now
    )
    
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Assets", "Figures", "itsm_hierarchical_joint_corner.png"))
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Updated joint MCMC corner plot saved to {out_path}")

if __name__ == "__main__":
    plot_hierarchical_joint()
