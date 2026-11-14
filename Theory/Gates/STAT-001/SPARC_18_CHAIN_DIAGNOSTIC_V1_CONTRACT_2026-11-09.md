# SPARC residual 18 chain diagnostic V1

Scope is A10 of the [research routes](../../../RESEARCH_ROUTES.md). Diagnose
the 18 cases held by the
[54-galaxy continuation](SPARC_54_CONTINUATION_V1_REPORT_2026-11-01.md)
at Medium using saved samples and the same empirical comparator.

Verify both artifact manifests against their sidecars, all consumed files
against the corresponding manifests, and the evaluated target/data against
the original run pins. Require exact block order and dimensions. Reproduce
the saved walker-zero Rhat, ESS and length results using the declared warm-up
and diagnose drift with two equal retained windows.

For descriptive inspection, take all 64 walkers at a fixed stride of 20
within each block. Compare separate ensemble medians and first/last window
medians in units of the pooled descriptive IQR. Flag a span of at least one
IQR for follow-up. Report per-ensemble pairwise rank correlations, using
absolute 0.8 as a descriptive flag, and the fractions within one degree of
the inclination limits or 0.05 dex above the signed-gas inward-support
floor where that floor is positive. These cutoffs classify diagnostics only.
Walkers in one ensemble are dependent. Quantiles of nonconverged samples are
descriptive, and neither correlations nor trace disagreement prove modes.

Reevaluate the best retained log-density state from each ensemble against
the unchanged target. Separate raw residual chi-square and standardized
prior displacement at that sampled state from sampling diagnostics.
Acceptance requires coverage of all 18 cases, reproduction of the original
criteria, an input-preserving deterministic receipt, and a concrete next
action keyed to the observed problems. Likelihood redesign, physical
interpretation and convergence clearance are outside this calculation.
Rule-9 review is deferred. Physics and parent-gate holds carry forward.
