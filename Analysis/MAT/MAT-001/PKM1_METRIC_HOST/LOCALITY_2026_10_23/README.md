# PKM1 P0-B bounded locality diagnostic (23 October 2026)

This package compares a conditional local force reduction with frozen primary
Solar-System benchmarks. It is not an ITSM physical pass, ephemeris fit, full
PPN calculation, numerical a0 prediction or demonstrated cutoff window.

## Evidence and versions

- Contract V1 and frozen_inputs_v1.json were sealed in the authorized task
  workspace before scientific execution. The canonical Core copy is byte-identical.
- pkm1_p0b_locality_v1.py and receipts/primary_v1_attempt_01 are preserved:
  98/99; SymPy could not infer positivity before factorization.
- V2 repairs only that predicate. Its receipt has 99/99 computational checks.
- verify_pkm1_p0b_locality_v1.py implements Binet angle evolution independently
  of the primary Cartesian time evolution; 19/19 local checks.
- Both successful computations were freshly replayed byte-exactly. These are
  same-author controls, not independent peer review.
- Existing source and dirty-file bytes/native-integer metadata are recorded
  in preservation.json. No old sidecar was refreshed by the calculation.

The owning comparison report lives at:
../../../../../Theory/Core/ITSM_FORCE_ARCHITECTURE_COMPARISON_V1_REPORT_2026-10-23.md

## Reproduction from repository root

Use the existing itsm_env interpreter; no installation or provider is required.
The source archive is deliberately excluded from version control. Obtain
https://arxiv.org/pdf/1601.00947v1 as
sources/Fienga_2016_INPOP15a_arxiv1601.00947v1.pdf before replay, and verify SHA256
e555f32afc6e93b2cf26842c126a2c1191dd0ec538206a76efd4de7d3480d1b4.
The archived table was checked visually. Rendering PNGs are not calculation inputs.

The following variable is only a relative package path:

    $locality = 'Analysis/MAT/MAT-001/PKM1_METRIC_HOST/LOCALITY_2026_10_23'
    conda run --no-capture-output -n itsm_env python -B "$locality/pkm1_p0b_locality_v2.py" --repo . --replay "$locality/receipts/primary_v2_attempt_01"
    conda run --no-capture-output -n itsm_env python -B "$locality/verify_pkm1_p0b_locality_v1.py" --primary "$locality/receipts/primary_v2_attempt_01/summary.json" --primary-script "$locality/pkm1_p0b_locality_v2.py" --replay "$locality/receipts/independent_v1_attempt_01"

For a fresh calculation use --out-dir with a NEW subdirectory of this package.
Existing receipts are write-once. Do not replace them or relax a failed assertion.

The strict source pins intentionally reject changed inputs. Future mutable-index
changes require a preserved source snapshot/replay design, not refreshed hashes
silently substituted into these artifacts. The historical repository_integration
field records the original secondary-workspace run, not the final integration
state; the owning report and integration evidence record that later step.

## Scope limits

The inward force has a0-scale high-acceleration correction in the declared
local/aligned/spherical, regulator-negligible reduction. INPOP15a C1/C2 are
postfit-residual acceptance thresholds, not Gaussian confidence intervals.
The exact algebraic force remainder does not certify the omitted background,
preferred-frame, global boundary, nonlinear orbit or quasistatic errors.

The physical cutoff, complete PPN/radio observables, actual coupled validity
window and identifying microscopic inputs remain open. Hypothetical partial-band
examples are arithmetic controls only.

Rule-9 DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.
No commit, push, publication, model/provider dispatch or vault mutation occurs.

