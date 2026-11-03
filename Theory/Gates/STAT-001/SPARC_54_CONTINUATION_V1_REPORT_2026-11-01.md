# SPARC targeted continuation — 1 November 2026

## Result

All 216 continuation jobs completed: four 64-walker ensembles for each of the
54 initial diagnostic failures, extended from 10,000 to **20,000 total steps**.
The initial 2,000-step warm-up alone was discarded. No prior, likelihood, input,
diagnostic threshold or sample membership was changed.

**36 of the 54 now meet the registered criteria; 18 still do not.** Together
with the original 121 passing galaxies, **157 of 175** meet these diagnostics.
The original 121 were not rerun or modified. Longer sampling was useful for
these 36; it did not resolve every case or establish adequate physical fits.

The initial failure inventory had 51 Rhat failures and 25 estimated ESS failures
(overlapping). After continuation, all remaining 18 miss Rhat<1.01. Other
criteria can fail as well. The worst case, UGC00128, improves from Rhat 1.63066
to 1.49172, with minimum estimated ESS 181.1 and a failed length/tau check.
It remains seriously unresolved. UGC02953's Rhat changes from 1.10237 to
1.11786: more steps do not guarantee monotonic diagnostic improvement.

Remaining names:
DDO161, NGC6674, NGC6946, UGC00128, UGC00634, UGC00891, UGC02487,
UGC02916, UGC02953, UGC03546, UGC03580, UGC05253, UGC05716, UGC05764,
UGC08699, UGC09133, UGC11820, UGC11914.

## Preservation and verification

Producer: `Analysis/STAT/STAT-001/sparc_continue_54_v1.py`.
Contract: `SPARC_54_CONTINUATION_V1_CONTRACT_2026-11-01.md`.
Output: `Analysis/STAT/STAT-001/outputs/sparc_54_continue_v1_20261101/`.

Each ensemble restored its step-10,000 positions, log probabilities and saved
MT19937 state. Its restored density was checked against the unchanged target.
Only new incremental blocks were written, with no copied/overwritten parent
chain. All parent input pins and selected checkpoint hashes were checked before
launch. A post-run check verifies all original parent artifacts unchanged,
including the 121 passing cases. One DDO154 ensemble's first 1,000 continued
steps independently replayed exactly for chain and log-probability arrays.
This is bounded deterministic replay, not an independent full-run reproduction.

`diagnostics.json` retains every outcome and parameter-wise diagnostic;
`continuation_contract.json` records selection and parent identity;
`artifact_manifest.json` seals the continued job outputs. The separate replay
verification record and artifact manifest receive their own SHA-256 sidecars.
Original failed attempts, old diagnostics and unrelated edits remain intact.

## Interpretation and next decision

This remains the fixed empirical simple-nu algebraic comparator with measured
catalogue distance/inclination errors and declared nuisance priors. Passing
Rhat/ESS/length criteria is not a good-fit statistic, proof of physical
identifiability, model preference, or action-derived ITSM result. The original
gas/inward-support issue and simplified geometry remain unchanged. No physical
gate is promoted; Rule-9 review is deferred.

Do not blindly double the whole sample again. Next inspect parameter traces,
ensemble disagreement, boundaries and posterior geometry for the remaining 18,
especially UGC00128 and UGC02953. Assess prior/domain sensitivity and residuals
separately from sampling length. A new likelihood or substantive statistical
derivation needs High confirmation; routine diagnostics can remain at Medium.
No further extension, commit, push, publication or vault mutation was performed.
