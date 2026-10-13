# G3N5: finite-mode full-state energy bound, version 1

Date: 12 October 2026. Owner: Stage 1 / RES-001 / Master Test 1.
This is a bound calculation on the existing rotating B1 prepared family,
not an action change, new physical domain or projected dust evolution.

## Frozen calculation

Reuse the verified full w propagator and corrected-reference identities.
For each original ell=4,8,16,32,64 on 0<=t<=1/20:

1. Reconstruct the complete corrected lift Hc, its drift, Mc=M+N2/ell^2,
   the normalization J=Oc Hc and original exact prepared columns. Retain the
   original initial mismatch; never evolve only on the corrected graph.
2. Reconstruct every corrected source coefficient R3..R6 from the complete
   Laurent generator and prior R2..R5. Normalize by exact rational cancellation
   only, with identity checks before interval bounding. Do not discard high
   coefficients, imaginary fields, metric constraints or basis/momentum drift.
3. Use w=Tw(I+U/ell)^-1 x_c, Q>=D>0 and the inherited full propagator
   ||Gamma_w(t,s)||_Q <= exp(30(t-s)). Q is an evolution norm, not a physical
   Hamiltonian or ghost criterion. Prove the actual observable's Q-to-infinity
   bound using D and Cauchy-Schwarz. Bound the COMPLETE original initial
   mismatch in Q(0), including both original prepared columns. Bound the full
   w-source on the existing proven background box. Include Q's time dependence
   through the inherited propagator; no new off-shell background is substituted.
4. Derive explicit finite-mode bounds for W_full-W_ref and W_full-Phi_M W0.
   Include the reference normalization and Phi_Mc-Phi_M difference. Every
   constant is exact rational or enclosed algebraic with outward rational
   square-root rounding. Numerical displays do not define proof constants.

## Verification and interpretation

Keep the full positive Duhamel forcing sign. Reject omission of drift,
initial mismatch, source coefficients, principal curvature data or input pins.
Check coefficient identities, normalization, full-source identity at independent
70-digit algebraic shell points, and the original five-mode archive, all four
columns/22 reconstructed fields and nonmonotonic complementary data. These
identity points are NOT trajectory projection or new trajectory solutions.
Use the same numerical control threshold 1e-30; check all bound violations
with a declared binary64 roundoff allowance, not a fitted accuracy threshold.

Freeze a new executable and use fresh finite_energy_attempt_01. Refuse
overwrite; reproduce all artifacts and sidecars by read-only replay. Preserve
every old source, failure, receipt, report and sidecar, and all inherited
hash/size/mtime metadata. Do not rerun the completed asymptotic-order audits.

Report actual bound sizes and limitations. A passing derivation need not
yield useful finite-band accuracy; do not call a loose bound physical
instability or manufacture usefulness by selecting a tolerance after results.
Full Stage 1 remains open unless its complete requested error-control scope
is met. The V3 asymptotic theorem remains a separate unchanged result.

physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Stage 2 STOP_AND_ASSESS_DOMAIN_UNRESOLVED; no action selected. Stage 3 NOT
ENTERED: identifying matter-residue/nonlinear-force inputs absent. No new
parent, TOP-X4 pivot, provider/model dispatch, vault/runtime change, commit,
push or publication is included.
