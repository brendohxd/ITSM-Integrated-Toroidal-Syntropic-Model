"""
================================================================================
ITSM — Stage 2 FAST: Hierarchical Bayesian H0 (Gaussian Approximation)
================================================================================
Author  : Brendon Boyd
Purpose : Fast comparison version of itsm_hierarchical_h0.py using the
          analytic Gaussian-convolution likelihood instead of full sample loops.

Scientific Context
------------------
For well-converged MCMC posteriors, the marginal H0 distribution per galaxy
is approximately Gaussian. The hierarchical likelihood then has an analytic
closed form:

    P(mean_i, std_i | mu, sigma) = Normal(mean_i; mu, sqrt(sigma^2 + std_i^2))

This is ~40,000x faster than the raw-sample loop and produces results
that are scientifically equivalent for Gaussian-distributed posteriors.

Outputs saved to results_fast/ (does NOT overwrite results/ from the full run).

Run time: < 2 minutes on Ryzen 7 / 16 GB RAM.
================================================================================
"""

import os
import glob
import warnings
import numpy as np
import pandas as pd
import emcee
import corner
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Scripts')))
from itsm_plot_style import apply_tier1_style
apply_tier1_style()
from scipy.stats import norm, gaussian_kde

warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────────────────────────────────────
# PATHS — saves to results_fast/ to avoid overwriting the full 5-hour run
# ─────────────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR     = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
CHAINS_DIR   = os.path.join(ROOT_DIR, "Assets", "SPARC_Batch_Outputs")
RESULTS_DIR  = os.path.join(SCRIPT_DIR, "results_fast")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# THRESHOLDS (identical to full version for apples-to-apples comparison)
# ─────────────────────────────────────────────────────────────────────────────
H0_LOWER_BOUNDARY    = 52.0
H0_UPPER_BOUNDARY    = 97.0
MIN_EFFECTIVE_SAMPLES = 100
H0_PRIOR_LO          = 55.0
H0_PRIOR_HI          = 90.0
SIGMA_PRIOR_LO       = 0.1
SIGMA_PRIOR_HI       = 20.0

# Global arrays — set once, reused every MCMC evaluation
_MEANS   = None
_STDS    = None
_WEIGHTS = None


def load_galaxy_chains(chains_dir):
    chain_files = sorted(glob.glob(os.path.join(chains_dir, "*_MCMC_Chains.csv")))

    if not chain_files:
        raise FileNotFoundError(f"No chain files in: {chains_dir}")

    print(f"\n[LOAD] Found {len(chain_files)} per-galaxy chain files.")

    galaxies     = []
    plot_samples = {}
    skipped      = []

    for fp in chain_files:
        galaxy_name = os.path.basename(fp).replace("_MCMC_Chains.csv", "")
        try:
            df = pd.read_csv(fp)
            if "H0" not in df.columns:
                skipped.append((galaxy_name, "No H0 column")); continue
            h0 = df["H0"].dropna().values
            if len(h0) < MIN_EFFECTIVE_SAMPLES:
                skipped.append((galaxy_name, "Too few samples")); continue
            m, s = float(np.mean(h0)), float(np.std(h0))
            if s < 1e-6:
                skipped.append((galaxy_name, "Degenerate chain")); continue
            clipped = m < H0_LOWER_BOUNDARY or m > H0_UPPER_BOUNDARY
            galaxies.append({"name": galaxy_name, "mean_h0": m, "std_h0": s,
                              "n_samples": len(h0), "clipped": clipped})
            plot_samples[galaxy_name] = np.random.choice(
                h0, size=min(500, len(h0)), replace=False)
        except Exception as e:
            skipped.append((galaxy_name, str(e)))

    n_good    = sum(1 for g in galaxies if not g["clipped"])
    n_clipped = sum(1 for g in galaxies if g["clipped"])
    print(f"[LOAD] Loaded {len(galaxies)} galaxies | good: {n_good} | clipped: {n_clipped}")
    return galaxies, plot_samples, skipped


def _precompute_arrays(galaxies, clipped_weight=0.1):
    global _MEANS, _STDS, _WEIGHTS
    _MEANS   = np.array([g["mean_h0"] for g in galaxies])
    _STDS    = np.array([g["std_h0"]  for g in galaxies])
    _WEIGHTS = np.array([clipped_weight if g["clipped"] else 1.0 for g in galaxies])


def log_probability_fast(theta):
    """
    Analytic Gaussian-convolution likelihood.
    P(mean_i | mu, sigma) = Normal(mean_i; mu, sqrt(sigma^2 + std_i^2))
    """
    mu, sig = theta
    if not (H0_PRIOR_LO < mu < H0_PRIOR_HI and SIGMA_PRIOR_LO < sig < SIGMA_PRIOR_HI):
        return -np.inf
    sig_eff = np.sqrt(sig**2 + _STDS**2)
    return float(np.dot(_WEIGHTS, norm.logpdf(_MEANS, loc=mu, scale=sig_eff)))


def run_fast_mcmc(galaxies, n_walkers=32, n_steps=2000, burn_in=300):
    _precompute_arrays(galaxies, clipped_weight=0.1)

    print(f"\n[MCMC] Fast hierarchical sampler")
    print(f"       Walkers    : {n_walkers}")
    print(f"       Steps      : {n_steps}  (burn-in: {burn_in})")
    print(f"       Likelihood : Gaussian-approximation (vectorised)")

    good = [g for g in galaxies if not g["clipped"]]
    seed_mu  = float(np.mean([g["mean_h0"] for g in good]))
    seed_sig = float(np.std( [g["mean_h0"] for g in good]))
    print(f"[MCMC] Seed: mu={seed_mu:.2f}, sigma={seed_sig:.2f}")

    pos = np.column_stack([
        np.clip(seed_mu  + 0.5 * np.random.randn(n_walkers), H0_PRIOR_LO+0.1, H0_PRIOR_HI-0.1),
        np.clip(seed_sig + 0.1 * np.random.randn(n_walkers), SIGMA_PRIOR_LO+0.01, SIGMA_PRIOR_HI-0.1),
    ])

    sampler = emcee.EnsembleSampler(n_walkers, 2, log_probability_fast)
    print("\n[MCMC] Running...")
    sampler.run_mcmc(pos, n_steps, progress=True)

    flat = sampler.get_chain(discard=burn_in, flat=True)
    print(f"[MCMC] Complete. Effective samples: {len(flat)}")

    try:
        tau = sampler.get_autocorr_time(quiet=True)
        print(f"[MCMC] Autocorr: mu={tau[0]:.1f} steps, sigma={tau[1]:.1f} steps")
    except Exception:
        pass

    return flat, sampler


def plot_and_summarise(flat_samples, galaxies, plot_samples, results_dir):
    mu_s   = flat_samples[:, 0]
    sig_s  = flat_samples[:, 1]
    mu_med = np.median(mu_s)
    mu_lo  = np.percentile(mu_s, 16)
    mu_hi  = np.percentile(mu_s, 84)
    mu_err = (mu_hi - mu_lo) / 2.0
    sig_med = np.median(sig_s)

    # ── Posterior plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(mu_s, bins=80, density=True, color="darkcyan", alpha=0.75,
            label=r"ITSM Fast Posterior $P(\mu_{H_0})$")
    kde = gaussian_kde(mu_s, bw_method=0.15)
    g = np.linspace(mu_s.min()-2, mu_s.max()+2, 500)
    ax.plot(g, kde(g), color="darkcyan", lw=2.5)
    ax.axvspan(67.4-0.5, 67.4+0.5, color="gold",   alpha=0.35,
               label=r"Planck 2018: $67.4 \pm 0.5$")
    ax.axvline(67.4, color="goldenrod", lw=2, linestyle="--")
    ax.axvspan(73.0-1.0, 73.0+1.0, color="tomato", alpha=0.35,
               label=r"SH0ES: $73.0 \pm 1.0$")
    ax.axvline(73.0, color="firebrick", lw=2, linestyle="--")
    ax.axvline(mu_med, color="darkcyan", lw=2.5,
               label=rf"ITSM Fast: $H_0 = {mu_med:.2f} \pm {mu_err:.2f}$")
    ax.axvspan(mu_lo, mu_hi, color="darkcyan", alpha=0.12)
    # Overlay the full-run result for direct comparison
    ax.axvline(69.089, color="navy", lw=2, linestyle=":",
               label=r"ITSM Full (5hr): $69.089$")
    ax.set_xlabel(r"$H_0$ (km/s/Mpc)", fontsize=14)
    ax.set_ylabel(r"Posterior Probability Density", fontsize=14)
    ax.set_title(
        r"ITSM Fast Hierarchical H0 — Comparison with Full Run",
        fontsize=13, pad=12)
    ax.legend(fontsize=10, frameon=True)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.set_xlim(60, 82)
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "h0_posterior_fast.png"), dpi=300)
    plt.close()

    # ── Corner plot
    labels = [r"$\mu_{H_0}$", r"$\sigma_{H_0}$"]
    fig = corner.corner(flat_samples, labels=labels,
                        quantiles=[0.16, 0.50, 0.84], show_titles=True,
                        title_fmt=".2f", color="darkcyan", truth_color="crimson",
                        truths=[mu_med, sig_med])
    fig.suptitle(r"ITSM Fast: Hyperparameter Corner", fontsize=13, y=1.01)
    fig.savefig(os.path.join(results_dir, "corner_hyperparams_fast.png"),
                dpi=300, bbox_inches="tight")
    plt.close()

    # ── Violin plot
    sorted_g  = sorted(galaxies, key=lambda g: g["std_h0"])
    good      = [g for g in sorted_g if not g["clipped"]][:60]
    names     = [g["name"].replace("_", r"\_") for g in good]
    data_pts  = [plot_samples.get(g["name"], np.array([g["mean_h0"]])) for g in good]
    fig, ax   = plt.subplots(figsize=(14, 8))
    parts     = ax.violinplot(data_pts, positions=range(len(good)),
                               showmedians=True, showextrema=False)
    for pc in parts["bodies"]: pc.set_facecolor("darkcyan"); pc.set_alpha(0.5)
    parts["cmedians"].set_color("white"); parts["cmedians"].set_linewidth(2)
    ax.axhline(mu_med,  color="darkcyan",  lw=2.5, linestyle="--",
               label=rf"ITSM Fast $\mu_{{H_0}} = {mu_med:.2f}$")
    ax.axhline(69.089,  color="navy",      lw=2,   linestyle=":",
               label=r"ITSM Full (5hr) $= 69.089$")
    ax.axhline(67.4,    color="goldenrod", lw=1.5, linestyle=":",
               label=r"Planck 67.4")
    ax.axhline(73.0,    color="tomato",    lw=1.5, linestyle=":",
               label=r"SH0ES 73.0")
    ax.set_xticks(range(len(good)))
    ax.set_xticklabels(names, rotation=90, fontsize=6)
    ax.set_ylabel(r"$H_0$ (km/s/Mpc)", fontsize=13)
    ax.set_title(r"Per-Galaxy $H_0$: Fast Version", fontsize=13, pad=10)
    ax.legend(fontsize=10, frameon=True, loc="upper right")
    ax.grid(True, axis="y", linestyle=":", alpha=0.5)
    ax.set_ylim(45, 100)
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "galaxy_h0_violin_fast.png"), dpi=300)
    plt.close()

    # ── Summary
    summary = f"""
================================================================================
ITSM HIERARCHICAL H0 - FAST VERSION SUMMARY
================================================================================

METHOD : Gaussian-approximation likelihood (analytic convolution)
         Each galaxy summarised as (mean_H0, std_H0)
         Likelihood = Normal(mean_i; mu, sqrt(sigma^2 + std_i^2))
WALKERS: {32}   STEPS: {2000}   BURN-IN: {300}

FAST RESULT (Gaussian approximation)
  mu_H0    = {mu_med:.3f}  [{mu_lo:.3f}, {mu_hi:.3f}]  km/s/Mpc
  sigma_H0 = {sig_med:.3f}  km/s/Mpc
  Offset from Planck (67.4) : {mu_med - 67.4:+.2f} km/s/Mpc
  Offset from SH0ES  (73.0) : {mu_med - 73.0:+.2f} km/s/Mpc

FULL RESULT (raw-sample, 5 hours)
  mu_H0    = 69.089  [69.083, 69.094]  km/s/Mpc
  sigma_H0 = 14.565  km/s/Mpc
  Offset from Planck (67.4) : +1.69 km/s/Mpc
  Offset from SH0ES  (73.0) : -3.91 km/s/Mpc

DELTA (Fast - Full)
  mu_H0    : {mu_med - 69.089:+.3f} km/s/Mpc
  sigma_H0 : {sig_med - 14.565:+.3f} km/s/Mpc

VERDICT
  {'CONSISTENT — Gaussian approximation validated.' if abs(mu_med - 69.089) < 0.5 else 'DIVERGENT — inspect posteriors.'}
================================================================================
"""
    print(summary)
    with open(os.path.join(results_dir, "comparison_summary.txt"), "w") as f:
        f.write(summary)
    print(f"[DONE] Fast results saved to: {results_dir}")
    return mu_med, mu_err, sig_med


if __name__ == "__main__":
    print("=" * 64)
    print("  ITSM — Fast Hierarchical H0 (Comparison Run)")
    print("  Saves to results_fast/ — does NOT touch results/")
    print("=" * 64)

    galaxies, plot_samples, skipped = load_galaxy_chains(CHAINS_DIR)

    if len(galaxies) < 10:
        raise RuntimeError("Too few galaxies. Run itsm_mcmc_benchmark.py first.")

    flat_samples, sampler = run_fast_mcmc(galaxies, n_walkers=32,
                                          n_steps=2000, burn_in=300)
    plot_and_summarise(flat_samples, galaxies, plot_samples, RESULTS_DIR)
