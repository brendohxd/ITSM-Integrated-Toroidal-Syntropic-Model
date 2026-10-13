# P2 release-sensitivity contract — 1 October 2026

## Purpose and status boundary

This contract freezes a bounded numerical sensitivity check for Paper 2 before
the registered run. It tests whether the paper's stated precision and its
no-attractor classification survive reasonable changes of extrapolation window,
fit order, ODE tolerance, and temporal sampling.

Passing this contract is a **local control only**. It does not derive a
renormalized state on evolving Bianchi-I spacetime, select the compact zero
mode, close Rule 9, or establish publication readiness.

## Frozen inputs

- `Analysis/Casimir/CBR-001/cbr001_stage1.csv`
  - SHA-256 `57847f382bafa562827413f19f416dbc3da004c95996413d05e0cb7fde0bb47c`
- `Analysis/Casimir/CBR-001/stage2_outputs/cbr001_stage2_scan.csv`
  - SHA-256 `fe648629545f40a29ca3bdc93a5978c59d85210d9157918eb191d45e2056a4d9`
- `Analysis/Casimir/CBR-001/stage3b_outputs/cbr001_stage3b_summary.json`
  - SHA-256 `9a5e80d2f713f01b02b7ea14c2460a344bcb2fcfdf814ea6696677d465c2ce3b`
- `Analysis/Casimir/CBR-001/cbr001_stage3b_ratio_test.py`
  - SHA-256 `63d6b0c3ac76fb93d68388205fa6cdea9563796faec48ccaacf1b81eff0e21c5`
- independent heat-kernel cube value from the 30 September literature control:
  `rho_HK = -0.837536910696079`.

The literature-control report is
`Theory/Verification/ITSM_ALPHAXIV_LITERATURE_CONTROLS_REPORT_2026-09-30.md`
(SHA-256 `8485a94d7b0dec2502534af3ea2a77037978cc5569c016bf7f1ab2e48d0d0953`).

## Registered calculations

### Static extrapolation sensitivity

Re-fit the frozen cube sequence with:

1. all six cutoffs and orders 1, 2, and 3;
2. the five-point tail (drop `N=20`) and orders 1 and 2.

The release precision passes only if:

- full-window order-2 relative error against `rho_HK` is below `2e-6`;
- tail-window order-2 relative error is below `1e-6`;
- full-window order-3 relative error is below `1e-7`; and
- full- versus tail-window order-2 values differ by less than `1e-6`
  relative to `rho_HK`.

Order 1 is retained as a diagnostic and is not used to quote release digits.

### Dynamic solver sensitivity

Re-run Stage 3B for `r0 = 1.1, 1.5, 3.0` with the original amplitude grid and
domain but with `samples=4001`, `rtol=1e-12`, and `atol=1e-16`. Compare with
the frozen baseline (`samples=2001`, `rtol=1e-10`, `atol=1e-14`).

The dynamic control passes only if, for every registered shape:

- both runs classify the threshold as `TRANSIENT_CROSSING`;
- neither run classifies an attractor;
- the threshold-amplitude relative difference is below `1e-8`;
- the one-percent dwell-time change is no larger than `0.011` e-fold; and
- the tight run passes all of its internal validation checks.

## Registered commands

```powershell
conda run --no-capture-output -n itsm_env python -B Analysis/Casimir/CBR-001/cbr001_stage3b_ratio_test.py --stage2-csv Analysis/Casimir/CBR-001/stage2_outputs/cbr001_stage2_scan.csv --output-dir Analysis/Casimir/CBR-001/release_sensitivity_outputs/p2_release_sensitivity_attempt_01/stage3b_tight --r0 1.1 1.5 3.0 --epsilon-min 1e-6 --epsilon-max 10 --epsilon-points 49 --n-max 20 --samples 4001 --rtol 1e-12 --atol 1e-16

conda run --no-capture-output -n itsm_env python -B Analysis/Casimir/CBR-001/p2_release_sensitivity.py --tight-summary Analysis/Casimir/CBR-001/release_sensitivity_outputs/p2_release_sensitivity_attempt_01/stage3b_tight/cbr001_stage3b_summary.json --output Analysis/Casimir/CBR-001/release_sensitivity_outputs/p2_release_sensitivity_attempt_01/summary.json
```

## Decision rule

- `PASS_CONTROL_ONLY`: every registered check passes.
- `FAIL`: any registered check fails or any frozen input hash differs.

Irrespective of the local result, `physics_pass=false` and
`publication_ready=false` until the declared dynamical-QFT/state limitations
and deferred external review requirements are separately resolved.
