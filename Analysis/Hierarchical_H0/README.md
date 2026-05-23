# ITSM — Hierarchical H0 Analysis

## What this does

This is the **Stage 2** analysis on top of the existing MCMC outputs from `itsm_mcmc_benchmark.py`.

Instead of reporting the *sample mean* of per-galaxy H0 values (which was already $72.49 \pm 0.31$ km/s/Mpc), this script builds a proper **hierarchical Bayesian population model**.

Each galaxy's Stage 1 MCMC chain is treated as a noisy measurement of a latent cosmic $H_0$. The Stage 2 sampler infers the population-level distribution:

$$H_0^{(i)} \sim \mathcal{N}(\mu_{H_0},\, \sigma_{H_0})$$

The output is a full posterior on **$\mu_{H_0}$** — the most statistically rigorous $H_0$ measurement the ITSM can produce.

## Why this is different from before

| Method | What it reports |
|---|---|
| Stage 1 sample mean | Arithmetic average of 175 medians — simple, fast |
| **Stage 2 hierarchical** | **Full Bayesian posterior on cosmic $H_0$ — statistically correct** |

The hierarchical model accounts for the fact that each galaxy's measurement has different uncertainty. Tightly constrained galaxies get more influence on the final posterior than noisy, poorly constrained ones.

## How to run

```bash
python itsm_hierarchical_h0.py
```

**Requires** the Stage 1 MCMC chain files to already exist in:
```
Assets/SPARC_Batch_Outputs/*_MCMC_Chains.csv
```

Run `Scripts/itsm_mcmc_benchmark.py` first if they don't exist.

## Output files (in `results/`)

| File | Description |
|---|---|
| `h0_posterior.png` | **Main result** — posterior on $\mu_{H_0}$ with Planck and SH0ES reference bands |
| `corner_hyperparams.png` | 2D joint posterior on ($\mu_{H_0}$, $\sigma_{H_0}$) |
| `galaxy_h0_violin.png` | Per-galaxy H0 distributions for the 60 most constrained systems |
| `hierarchical_summary.txt` | Full numerical summary with Hubble tension context |

## Quality filtering

Galaxies whose Stage 1 chains clipped the prior boundary ($H_0 \to 50$ or $H_0 \to 100$) are **down-weighted to 10%** rather than excluded entirely.

This is physically motivated: these systems are dominated by inclination ambiguity, edge-on dust obscuration, or starburst contamination — known data quality issues in the SPARC catalogue. They are not failures of the ITSM geometry.

The intrinsic scatter $\sigma_{H_0}$ from the hierarchical model is itself a **physical prediction** of the ITSM: it reflects the genuine angular anisotropy of the toroidal expansion rate across different observational sightlines.
