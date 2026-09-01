# STAT-001: Statistical Inference Pipeline

**Status:** `NOT_STARTED_AS_CLOSED_GATE`

**Authority:** `STAT-001_READINESS.md` and `active_research.md`

**G0 note (2026-08-25):** the existing L-BFGS-B pipeline and gate report are exploratory artifacts, not a STAT-001 PASS.

## Context & Objectives
This gate defines a preregistered, matched evaluation of rotation curves such as SPARC after the upstream model prediction and matter coupling exist. MAT-001 has not computed the invariant residue and DISK-001 has not supplied a closed disk prediction, so current coefficient choices are comparators rather than Derived inputs.

Historically, the ITSM pipeline suffered from B9 dual RAR packaging (arbitrarily forcing $C_{obs} = 2/3$ and $a_0 = cH_0/2\pi$). 

STAT-001 establishes an honest statistical test comparing:
1. **Nested control:** Newtonian baryons under the same data and nuisance policy.
2. **Preregistered comparators:** declared $(a_0,C_{obs})$ choices such as $C=1$ and $C=2/3$, explicitly labelled empirical or historical.
3. **ITSM prediction:** only after MAT-001 and DISK-001 export a same-action, source-to-observable prediction.

## Methodology
- **Data**: SPARC rotation curve `.dat` files.
- **Model**: Algebraic deep-MOND approximation derived from the AQUAL nonlinear field. $V_{bar}^2 = V_{gas}^2 + \Upsilon_{disk} V_{disk}^2 + \Upsilon_{bulge} V_{bulge}^2$.
- **Map**: $V_{obs} = \sqrt{R \cdot g_{obs}}$ where $g_{obs} = |g_N| \nu(|g_N|/a_{0,eff})$.
- **Nuisance Parameters**: stellar mass-to-light ratios, distances and inclinations must follow one preregistered policy; per-galaxy flexibility is counted in model complexity.
- **Prior**: Strict log-normal priors on mass-to-light ratios ($\log_{10} \Upsilon_{disk} \sim \mathcal{N}(-0.301, 0.1^2)$, $\log_{10} \Upsilon_{bulge} \sim \mathcal{N}(-0.155, 0.1^2)$) as per Lelli et al.
- **Inference engine**: distinguish optimization, profile likelihood, bootstrap and posterior sampling exactly. An optimizer must never be described as MCMC or Bayesian posterior inference.
- **Objective accounting**: raw data $\chi^2$ must be stored separately from prior or penalty terms. AIC/BIC and reduced-$\chi^2$ definitions must name which objective and parameter count they use.
- **Reproducibility**: freeze sample/exclusions, code, environment, seeds, input hashes and final-output sidecars before the gate run.

## Pass Criteria
- All prerequisites and the readiness checklist pass before unblinding the gate metric.
- Data likelihood, priors, hard bounds, exclusions and nuisance policy are mathematically and textually aligned.
- Raw likelihood terms, penalties and diagnostics are exported separately and independently recomputed.
- Mock injection/recovery and negative controls pass under the same pipeline.
- The ITSM and comparator branches use matched data and nuisance treatment; parameter counts are explicit.
- Claims report exact raw results, uncertainty, failure modes and sensitivity to declared alternatives.
- A script-level success or competitive fit does not itself clear STAT-001; the signed report must satisfy every checklist item and retain upstream claim boundaries.
