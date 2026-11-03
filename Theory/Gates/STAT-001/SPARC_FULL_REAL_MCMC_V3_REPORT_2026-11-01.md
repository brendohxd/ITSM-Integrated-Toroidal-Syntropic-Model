# Full SPARC conditional MCMC — 1 November 2026

## Result

All **175 galaxies**, **3,391 radial measurements** and **700 independent
ensemble jobs** completed. The run used **16 distinct worker processes**,
four 64-walker ensembles per galaxy, 10,000 steps and 2,000 discarded warm-up.
The 448 million walker states before warm-up are correlated samples, not
448 million independent measurements or effective samples.

**121 galaxies met the registered convergence criteria; 54 did not.** No galaxy
was removed for a poor fit, low quality, low inclination or failed convergence.
No significance or ITSM model preference is established by this result.

| Catalogue quality | Included | Convergence criteria met | Not met |
|---|---:|---:|---:|
| 1 | 99 | 73 | 26 |
| 2 | 64 | 40 | 24 |
| 3 | 12 | 8 | 4 |
| Total | 175 | 121 | 54 |

Acceptance fractions ranged from 0.24764 to 0.64859. Acceptance rate alone is
not a convergence or fit-quality test. Posterior estimates for the 54 failures
remain provisional. The failed names and parameter-wise diagnostics are fully
retained in `diagnostics.json`, not suppressed by this summary.

## What was actually fitted

This is a **conditional algebraic simple-nu comparator**, fixed empirical
a0=1.2e-10 m/s2 and C=1. Stellar disk and applicable bulge mass-to-light ratios,
distance and inclination were sampled under the priors frozen in
`SPARC_REAL_MCMC_V1_CONTRACT_2026-11-01.md`. Distances/inclinations used each
galaxy's measured catalogue errors. Gaussianity, independence, simplified
inclination treatment and the stellar-population priors remain assumptions.
No unreported velocity-error floor or clipping of signed gas contributions was
applied. The likelihood uses fixed nominal data coordinates with shared
galaxy-level nuisance parameters. Truncated prior normalization constants cancel
within a fixed galaxy's posterior; no Bayesian evidence was calculated.

It is not an action-derived ITSM prediction, solved disk AQUAL field, full dust
or photometry forward model, lensing test, H0 measurement, or comparison with
competing gravity/halo models. Radial covariance and gas-template uncertainties
were not inferred. No AIC/BIC/global p-value or posterior-predictive goodness of
fit is reported. The per-ensemble raw chi2 at marginal medians is not the
minimum chi2, a posterior average, reduced chi2 or a likelihood-ratio statistic.
Convergence does not establish physical plausibility or an adequate fit.

## Pilot, failed attempts and implementation controls

The v1 pilot completed 12 jobs but could not initialize UGC01281's four jobs
from ordinary prior draws. Its scalar inward domain requires U_disk above about
15.21, far from the fiducial .5 under the declared 0.1-dex lognormal prior.
This is a serious model-domain/prior conflict, not evidence for such a stellar
mass ratio. v2 used an analytically determined, stable truncated-normal tail
initializer without changing the prior, likelihood or dropping radial points.
See `SPARC_REAL_MCMC_V2_INITIALIZATION_NOTE_2026-11-01.md`.

The v2 pilot sampled all jobs and saved diagnostics: NGC7814 narrowly missed
Rhat<1.01 at 10,000 steps (1.012204). A console-print bug then returned a nonzero
exit after saving results. v3 corrects only that print call. Both older versions
and attempts are retained. The unchanged four-member pilot at 20,000 steps met
all registered criteria; its largest Rhat was 1.005427. This is a favorable
bounded pilot, not general simulation calibration or prior-sensitivity proof.

Scalar formula/likelihood controls independently agreed on the 174 galaxies
with supported fiducial inward accelerations. UGC01281 was explicitly checked
for support at a larger mass ratio, not silently skipped from sampling. All 175
loaders passed and have strictly positive disk templates; 11 have nominal i=90
degrees and were handled with truncated inclination initialization.

All 16 first-1,000-step pilot blocks matched between v2 and v3, including saved
states. All four CamB first-block arrays also matched between the full run and
pilot using their identical seeds. This is bounded deterministic replay, not
independent replay of all 700 jobs. Every full-run input/producer pin was checked
after completion and matched. No producer or input was changed during the run.

Diagnostics use the preselected walker zero from each independently seeded
ensemble; interacting walkers are not treated as independent chains. Registered
criteria: rank-normalized/folded split Rhat<1.01, estimated summed ESS>=400 per
parameter, retained length>=50*tau with finite positive tau. These estimates
are necessary diagnostics, not proof of complete exploration or tail accuracy.

## Reproducibility and delivery

- Producer: `Analysis/STAT/STAT-001/sparc_real_mcmc_v3.py`.
- Full output: `Analysis/STAT/STAT-001/outputs/full_sparc_real_v3_20261101/`.
- `run_contract.json`: exact inputs, script pins, names, settings and versions.
- `diagnostics.json`: all 175 convergence outcomes and all 54 failed names.
- `verification_summary.json`: job/worker/measurement accounting and pin checks.
- `ensemble_summary.csv`: all 700 ensemble summaries; posterior quantiles are in
  each job's `result.json`, with parameter names and seeds.
- Incremental NPZ blocks retain chains, log probabilities and random states.
  They remain local and ignored by Git; none were deleted. Each attempt's
  `artifact_manifest.json` seals its files, including failure records.

The archived uncertainty candidate matches its record checksum and all 175
local nominal catalogue rows, but is not a fresh CDS byte comparison. Its bad
embedded column offsets and the historical 152-versus-153 cut discrepancy remain
documented in the input-check report. The full run avoids making an unexplained
one-galaxy exclusion: all 175 are included.

## Next work and meaning for ITSM

The full database now has actual new nuisance-marginalized posterior chains for
this declared comparator. The next useful calculation is targeted continuation
and diagnosis of the 54 unmet convergence cases, retaining these initial results,
followed by prior/domain sensitivity, posterior-predictive and held-out checks.
Do not repeat the 121 passing cases without a new reason. A matched ITSM model
comparison still needs its physical force/metric inputs; these chains cannot
supply microscopic matching, universal acceleration or a toroidal projection.

DISK remains methods-only; STAT is not promoted as a closed physical gate.
MAT/action-derived holds persist. Rule-9 review is deferred. Original inputs,
sidecars, failed attempts and unrelated dirty work remain preserved. No commit,
push, publication, external review dispatch or vault mutation was performed.
