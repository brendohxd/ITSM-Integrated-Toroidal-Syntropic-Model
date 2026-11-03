# Conditional synthetic MCMC pilot v1 — 1 November 2026

## Outcome

Real SPARC inference has not run. A synthetic sampler validation completed with
16 distinct worker processes, four fixtures, four independent ensembles per
fixture, 64 walkers and 10,000 steps (2,000 discarded). Three fixtures met the
predeclared convergence criteria; the fourth remains unaccepted.

| Fixture | Bulge | Nominal inclination | Largest rank/folded split Rhat | Smallest estimated ESS | Criteria |
|---|---|---|---|---|---|
| 0 | No | 45 deg | 1.007073 | 756.0 | Met |
| 1 | Yes | 45 deg | 1.011218 | 616.8 | Not met: bulge log mass-to-light Rhat |
| 2 | No | 70 deg | 1.008020 | 603.5 | Met |
| 3 | Yes | 70 deg | 1.007998 | 706.6 | Met |

All retained-length checks met 50 times estimated autocorrelation time. These
finite-chain estimates do not prove mixing. Acceptance fractions ranged from
0.58356 to 0.64067. All injected truths lay in their ensemble-specific 95%
intervals; four favorable synthetic fixtures with truth at prior centers are
not a population calibration experiment or validation of real-data accuracy.

## Verification

The independent scalar acceleration formula, inclination displacement,
nonphysical-support rejection and fixed-coordinate likelihood Jacobian checks
passed before sampling. One newly initialized case-0/ensemble-0 replay matched
the first 1,000-step checkpoint exactly for chain, log densities, positions and
stored random-state arrays. This is a bounded replay, not a replay of all jobs.
No failure was repaired by moving a convergence threshold or selecting a seed.

Executable: `Analysis/STAT/STAT-001/sparc_conditional_pilot_v1.py`.
Contract: `SPARC_SYNTHETIC_PILOT_V1_CONTRACT_2026-11-01.md`.
Fresh output: `Analysis/STAT/STAT-001/outputs/synthetic_pilot_v1_20261101/`.
Receipt contains versions, seeds, worker PIDs, all interval/acceptance values and
source hash. `artifact_manifest.json` pins 162 artifacts, including the exact
seed replay and receipt. The 160 cumulative original checkpoints occupy about
1,149.2 MiB, plus the replay. All are retained locally; a directory-local ignore
rule prevents accidental inclusion of NPZ chains in commits. Do not delete or
rewrite these records to make the run appear successful. Future checkpoint
storage should avoid this cumulative size growth while retaining restart state.

## Scientific boundary and next steps

The fixed empirical acceleration scale and algebraic simple-nu model are
conditional inputs, not a solved disk AQUAL field or a theory-fixed ITSM law.
The implemented likelihood uses fixed nominal data coordinates and shared
galaxy-level distance/inclination nuisances. It neither removes dust effects
nor reconstructs inclination-dependent photometry or thickness. No H0, model
preference, physical gate clearance or new matching result is reported.

The official CDS archive retrieval also failed this session with a connection
reset. No catalogue uncertainty values were downloaded or invented. A further
real-data run needs measured uncertainty inputs, the 152/153 sample discrepancy
resolved, provenance/units checked, real-data parameter/prior sensitivity, and
a reviewed scope for the simplified disk approximation. Synthetic fixture 1
also needs convergence follow-up without replacing this failed run. The other
fixtures' diagnostic success does not authorize a full real-data batch.

The v1 executable saves checkpoint restart ingredients but does not yet offer
a resume CLI. No existing scientific files or sidecars were modified, and no
commit, push, publication, provider dispatch or vault mutation was performed.
Rule-9 remains deferred; DISK/STAT/MAT holds remain unchanged.
