# P2 release-sensitivity report — 1 October 2026

## Result

**FAIL under the preregistered numerical reproducibility threshold: 18/19
checks passed.** The failed check is bounded and does not alter the qualitative
no-attractor result, but it must not be silently relabelled as a pass.

The registered tight Stage-3B rerun passed all seven internal validations. For
`r0 = 1.1, 1.5, 3.0`, every baseline and tight run remained a
`TRANSIENT_CROSSING`, no run became an attractor, and the one-percent dwell-time
changes were at most `0.010` e-fold. The `r0=1.5` threshold amplitude shifted by
`8.7384e-5` relative, exceeding the deliberately stringent registered bound of
`1e-8`. The other two relative threshold changes were below `5e-10`.

The initial 17/19 receipt also exposed a harness bookkeeping error: the Stage-3B
receipt field is `validations`, not `validation`. That key was corrected without
changing a threshold or numerical result; the replay then returned 18/19. The
original failed receipt was overwritten only within this new, noncanonical
sensitivity-attempt directory and its final sidecar matches the final 18/19
receipt.

## Static extrapolation result

Against the independent heat-kernel/Mellin cube value
`rho = -0.837536910696079`:

| fit | extrapolated rho | relative discrepancy |
|---|---:|---:|
| full window, order 1 | -0.837374058510674 | 1.9444e-4 |
| full window, order 2 | -0.837535892991726 | 1.2151e-6 |
| full window, order 3 | -0.837536917297790 | 7.8823e-9 |
| tail window, order 1 | -0.837443775079707 | 1.1120e-4 |
| tail window, order 2 | -0.837536469494363 | 5.2678e-7 |

All four preregistered static checks passed. The order-1 diagnostic is visibly
insufficient for six-decimal publication precision. Paper 2 therefore reports
the cube value only to six decimal places and separately identifies the direct
and heat-kernel/Mellin values.

## Interpretation

The sensitivity work supports the paper's bounded qualitative conclusion:
within the declared instantaneous closure, the registered candidate crossings
are transient and decay toward isotropy. It does not support quoting threshold
amplitudes to high precision, and it does not turn the closure into a dynamical
renormalized-QFT calculation.

The sensitivity suite is **complete but not all-pass**. Deferred independent
review, the zero-mode state, and dynamical renormalized backreaction remain
publication or physics boundaries as declared in the manuscript.

## Artifacts

- Contract: `Theory/Verification/P2_RELEASE_SENSITIVITY_CONTRACT_2026-10-01.md`
- Aggregator: `Analysis/Casimir/CBR-001/p2_release_sensitivity.py`
- Final receipt: `Analysis/Casimir/CBR-001/release_sensitivity_outputs/p2_release_sensitivity_attempt_01/summary.json`
- Tight Stage-3B receipt: `Analysis/Casimir/CBR-001/release_sensitivity_outputs/p2_release_sensitivity_attempt_01/stage3b_tight/cbr001_stage3b_summary.json`
- Optimized-run output SHA-256: `f47da651bbdc3c2b1a5139822180de284b30aefa750149fde05765573d030efa`

The final aggregate receipt SHA-256 is
`6109a3591ea4b4d6493da77406bea932fe97b27f5fd6800b1d061b630b526216`.
