# G3N5 corrected remainder v3: expression-preserving interval evaluation

Date: 12 October 2026. Version 3. Inherit the complete
[v2 contract](RES001_R4C1_G3N5_CORRECTED_DUST_REMAINDER_V2_CONTRACT_2026-10-12.md),
including its positive forcing and independent scalar/matrix sign regressions.
No action, parameter, physical initial data, state, equation, rejection rule,
paired coupled-solver tolerance or scientific acceptance requirement changes.

The only evaluation change is in interval absolute values. Decompose each
expression exactly with as_real_imag(deep=True), preserving its rational
factorization, instead of first expanding the entire complex expression.
For q=re+i im, retain the bound |q|<=max|re|+max|im|. Use the SAME exact rational
interval arithmetic, denominator-exclusion rule and outward square-root
enclosures. No approximate floating interval, sampled maximum or deleted term.
Factored versus expanded enclosure constants may differ; both represent the
same coefficient. Do not assert that a tighter constant is a physics result.

Before first v3 execution add exact real, imaginary and mixed scalar
decomposition/regression checks, nonnegative enclosures and explicit zero-
denominator rejection. Keep the original full coefficient/sample/remainder
controls. No sample check replaces the whole-interval arithmetic proof.

V2 remains byte-identical. Its incomplete run is superseded for this validated
representation optimization, not declared failed, physically invalid or stopped
merely because an observation timed out. Preserve source/contract/sidecars,
partial private log and a truthful interruption record. V1's distinct forcing
sign defect remains INVALID and preserved. Use fresh attempt_03 for v3; no
existing source or attempt directory is overwritten.

The full corrected reference, all original wave/fast mismatch response and
positive forced remainder remain. Full dust closure, useful accuracy and
sharp/actual convergence order are not accepted by an enclosure optimization.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Stage 2 stop and stage 3 matching gap unchanged. No publication, provider/model
dispatch, vault mutation, commit or push.
