"""
Diagnostic: Per-galaxy H0 posterior shape analysis.
Plots 12 representative galaxies (tight / mid / broad constraint).
Also prints Shapiro-Wilk normality p-values and std distribution stats.
"""
import glob, os, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Scripts')))
from itsm_plot_style import apply_tier1_style
apply_tier1_style()
from scipy.stats import norm, gaussian_kde, shapiro

CHAINS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                      "Assets", "SPARC_Batch_Outputs")
OUT    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_correct")
os.makedirs(OUT, exist_ok=True)

files = sorted(glob.glob(os.path.join(CHAINS, "*_MCMC_Chains.csv")))

stats = []
for fp in files:
    try:
        df = pd.read_csv(fp)
        if "H0" not in df.columns: continue
        h0 = df["H0"].dropna().values
        if len(h0) < 100: continue
        stats.append({
            "name": os.path.basename(fp).replace("_MCMC_Chains.csv", ""),
            "h0":   h0,
            "std":  float(np.std(h0)),
            "med":  float(np.median(h0)),
            "mean": float(np.mean(h0)),
        })
    except:
        pass

stats.sort(key=lambda x: x["std"])
n     = len(stats)
picks = stats[:4] + stats[n//4:n//4+4] + stats[-4:]   # tight / mid / broad

fig, axes = plt.subplots(3, 4, figsize=(16, 10))
fig.suptitle(
    "Per-Galaxy H0 Posteriors: Shape Diagnostic\n"
    "Row 1: Tightly constrained  |  Row 2: Mid  |  Row 3: Broadly constrained",
    fontsize=12
)

for ax, g in zip(axes.flat, picks):
    h0 = g["h0"]
    ax.hist(h0, bins=60, density=True, color="navy", alpha=0.45)
    try:
        kde = gaussian_kde(h0, bw_method=0.2)
        x   = np.linspace(max(49, h0.min()-1), min(101, h0.max()+1), 300)
        ax.plot(x, kde(x), "navy", lw=2.0)
    except:
        pass
    mu_g, sig_g = g["mean"], g["std"]
    xg = np.linspace(max(49, mu_g - 4*sig_g), min(101, mu_g + 4*sig_g), 200)
    ax.plot(xg, norm.pdf(xg, mu_g, sig_g), "crimson", lw=1.5,
            linestyle="--", label="Gaussian fit")
    ax.axvline(67.4, color="gold",   lw=1.0, linestyle=":", alpha=0.8)
    ax.axvline(73.0, color="tomato", lw=1.0, linestyle=":", alpha=0.8)
    try:
        _, p = shapiro(np.random.choice(h0, min(500, len(h0)), replace=False))
        sw_txt = f"  SW-p={p:.3f}"
    except:
        sw_txt = ""
    ax.set_title(
        f"{g['name']}\nmed={g['med']:.1f}  std={g['std']:.1f}{sw_txt}",
        fontsize=7
    )
    ax.set_xlim(49, 101)
    ax.set_xlabel("H0 (km/s/Mpc)", fontsize=7)
    ax.tick_params(labelsize=7)

axes[0, 0].legend(fontsize=7)
plt.tight_layout()
out_path = os.path.join(OUT, "per_galaxy_h0_shape_diagnostic.png")
plt.savefig(out_path, dpi=200)
plt.close()
print(f"[PLOT] Saved: {out_path}")

# ── Summary statistics
stds = np.array([g["std"] for g in stats])
meds = np.array([g["med"] for g in stats])

print("\n=== Chain Shape Summary ===")
print(f"Total galaxies analysed     : {n}")
print(f"Tightest std  : {stats[0]['name']:20s}  std={stats[0]['std']:.2f}  med={stats[0]['med']:.1f}")
print(f"Median galaxy : {stats[n//2]['name']:20s}  std={stats[n//2]['std']:.2f}  med={stats[n//2]['med']:.1f}")
print(f"Broadest std  : {stats[-1]['name']:20s}  std={stats[-1]['std']:.2f}  med={stats[-1]['med']:.1f}")
print()
print(f"Mean std  across all galaxies : {stds.mean():.2f} km/s/Mpc")
print(f"Median std across all galaxies: {np.median(stds):.2f} km/s/Mpc")
print(f"Fraction std > 5  km/s/Mpc   : {(stds > 5).mean()*100:.1f}%")
print(f"Fraction std > 10 km/s/Mpc   : {(stds > 10).mean()*100:.1f}%")
print(f"Fraction std > 15 km/s/Mpc   : {(stds > 15).mean()*100:.1f}%")
print(f"Fraction std > 20 km/s/Mpc   : {(stds > 20).mean()*100:.1f}%")
print()
print(f"Mean  median H0 across all galaxies: {meds.mean():.2f} km/s/Mpc")
print(f"Std of medians across galaxies     : {meds.std():.2f} km/s/Mpc")
print()
print("KEY QUESTION: are posteriors peaked or flat?")
print(f"  If mean std >> (100-50)/sqrt(12) = {50/3.464:.1f}: chains are nearly FLAT (uninformative)")
print(f"  If mean std <<  14.4             : chains are PEAKED (informative)")
print(f"  Your mean std = {stds.mean():.2f} km/s/Mpc  ->  ", end="")
if stds.mean() > 12:
    print("NEARLY FLAT — individual galaxies barely constrain H0")
elif stds.mean() > 6:
    print("MODERATELY PEAKED — partial H0 constraint per galaxy")
else:
    print("STRONGLY PEAKED — good H0 constraint per galaxy")
