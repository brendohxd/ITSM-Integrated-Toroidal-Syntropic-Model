# Diagnostic audit of the 18 remaining SPARC sampling failures

The [frozen diagnostic](SPARC_18_CHAIN_DIAGNOSTIC_V1_CONTRACT_2026-11-09.md)
reproduced every registered walker-zero Rhat, ESS and chain-length result for
the 18 unresolved galaxies. All 18 still miss Rhat < 1.01. Fourteen have
minimum estimated ESS below 400 and twelve fail the length criterion.
The full-sample diagnostic count remains 157 of 175.

Across the descriptive all-walker sample, the largest separation of ensemble
medians is about 0.081 pooled IQR, and the largest within-ensemble shift
between equal retained windows is about 0.100 pooled IQR. Neither crosses the
frozen one-IQR flag. Seventeen galaxies have at least one ensemble with
absolute pairwise Spearman correlation at or above 0.8. The strongest pairs
reach approximately 0.993 for both UGC00128 and UGC02953. These summaries
can coexist with poor walker-zero diagnostics. They do not resolve tail
mixing or exclude modes the samples failed to visit.

The largest observed inclination-boundary fraction was 0.009948 in UGC08699.
No descriptive sample fell within the frozen 0.05 dex margin of a positive
inward-support floor. The screen covers sampled states only. UGC00128's worst
Rhat is 1.49172 (distance ratio) with minimum ESS 181.1. The best saved
log-density state in at least one ensemble has a prior displacement of about
6.96 prior standard deviations in one coordinate. The smallest raw residual
chi-square across its four best-log-density samples is about 120.2 for 22
radial points. For UGC02953 the worst Rhat is 1.11786 (inclination), minimum
ESS is 118.6, and the corresponding minimum across four sampled residual
chi-squares is about 637.7 for 115 points. These are sample diagnostics and
descriptive residuals. The receipt retains each ensemble's full values.

The next sampling experiment should use UGC00128 and UGC02953 as sentinel
cases for a ridge-aware sampling comparison on the unchanged target. Compare
independently initialized ensembles under a frozen diagnostic and compute
budget. Check whether along-ridge and across-ridge exploration improves.
Analyze prior sensitivity and residual structure separately before
interpreting the fitted parameters. A blanket extension of all 18 has no
specific mechanism for the observed correlation.

The [executable](../../../Analysis/STAT/STAT-001/sparc_diagnose_18_v1.py)
checked both archive manifests, the consumed blocks, the original target
pins and the best sampled log densities. The
[receipt](../../../Analysis/STAT/STAT-001/outputs/sparc_18_diagnostics_v1_20261109/receipt.json)
replayed byte for byte. A10's saved-chain diagnostic is complete in scope.
Sampling clearance for the 18, model adequacy and action-derived predictions
remain open. Review DEFERRED, physics_pass=false, gate_effect=NONE.
