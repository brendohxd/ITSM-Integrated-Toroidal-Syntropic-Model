# G3N5 finite-wavenumber correction in actual dust variables

Date: 11 October 2026. Version 1. Stage 1 / Master Test 1 / conditional B1.
Result: CONDITIONAL_FORMAL_OBSERVABLE_CORRECTION. Local checks 29/29; exact
read-only replay PASS. Corrected-system remainder and sharp order NOT_PROVED.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.

## What is new

The first formal inverse-coordinate-wavenumber-squared correction has been
computed from the full generator in the ACTUAL dust-observable coordinates.
It is not just the instantaneous graph block from the earlier exact split.
It includes the normalization drift needed when converting the comparison
lift's dust variables to the measured dust variables. No acceleration target,
new action, fitted coefficient, new initial data or projected evolution is used.

Let R_H=A_c H-H_dot-H M, with H0-H3 from the unchanged prepared-error
certificate. Select the two principal-kernel rows 3,13 after Tw, using S.
Then

```text
G = S Tw H0 = [[0,1],[-6 rho_m,-13 H-2 psi_dot/5]], det G=6 rho_m.
N2 = G^-1 S Tw R2,
O_c H = I + ell^-2 J2 + ...,
N_obs = N2 + J2_dot + [J2,M].
```

The formal normalized chart therefore has M+ell^-2 N_obs as its first
correction. This is ONLY a principal-kernel solvability result. The fast/wave
residual, original initial mismatch and full coupled response remain to be
controlled; this is not a closed finite-mode dust evolution equation.

At the original dimensionless B1 initial background, the exact coefficient is

```text
N_obs(0) = [[372/1375, 706493/330000],
            [130249/1512500 + 144 sqrt(4006695)/529375,
             -444/1375 + 6 sqrt(4006695)/21175]].
```

The complete time-dependent N2,J2,N_obs are exported in
[formulas.json](../../../Analysis/MasterTests/outputs/r4c1_g3n5_observable_correction_attempt_01/formulas.json).
Coordinate periods remain 2*pi, p=ell/a and p_dot=-H*p. A coefficient written
with p^-2 instead of ell^-2 must be N_obs/a^2. These are the declared benchmark
units and assumed parent coefficients, not microscopic identification or an
SI acceleration prediction.

## Chart and derivative controls

For any auxiliary two-state chart Z(t), H -> H(I+ell^-2 Z) gives

```text
N2 -> N2+[M,Z]-Z_dot,
J2 -> J2+Z,
N_obs -> N_obs.
```

This cancellation was checked exactly on the stated preserved shell, together
with principal-kernel conditions, projected solvability and normalized actual
observation through order two. It checks auxiliary-chart invariance, not
arbitrary physical field or unit invariance of the complete action. Omitting
J2_dot or the observation normalization changes the coefficient and is rejected.

Independent finite differences of J2 along the unchanged background series
give discrepancies 7.895357423404192e-9, 3.5712961199418913e-9 and
5.6722922192609104e-9 at t=0,1/40,1/20. The frozen step was 1e-5, with centered
interior and three-point one-sided endpoint derivatives. All are below the
pre-execution 1e-6 relative plus 1e-7 absolute allowance. These controls are
implementation checks, not estimates of the evolution remainder.

The inverse uses rho_m>=17/100 in the registered [0,1/20] boxes. No rho_m=0
endpoint or division by a scalar velocity is admitted. All evolving background,
constraint and momentum terms are kept; J=1, v_dot(0)=1,r_dot(0)=1/4. No old
trajectory, five-mode/four-column probe or 22-field reconstruction was replaced.

## What remains open

1. Extend the corrected lift through the complete non-kernel residual and
   derive a controlled remainder for the corrected full system, preserving
   fast/wave forcing and the ORIGINAL prepared-data mismatch.
2. Prove or reject the sharp/actual uniform convergence order. A nonzero
   formal N_obs is not that proof. The private leading fast-time candidate
   cancels exactly, so it cannot be used as a sharp-order witness. Its failed
   uncancelled 0/0 limit and the corrected private diagnostic remain intact.
3. Establish useful finite-mode accuracy. The prior upper-rate theorem remains
   valid but its 1.68549e8 coefficient is too conservative. A separate frozen
   compressed-energy/exact-source calculation is still live at this checkpoint;
   no PASS or sharpened constant from that job has been adopted here.

The ordinary-wave Jordan defect and indefinite physical Hamiltonian are not
removed or promoted by this chart calculation. A transfer-norm estimate is not
physical positivity, a Cauchy-domain theorem or a physical EFT cutoff.

## Evidence and preservation

[Contract](RES001_R4C1_G3N5_OBSERVABLE_CORRECTION_CONTRACT_2026-10-11.md):
7c244ad93eba92d09781efb20a216d6b64982dfcb2abe1a6403e0b540f64dd78.
[Executable](../../../Analysis/MasterTests/test_01_r4c1_g3n5_observable_correction_v1.py):
51608f615e85103d792ddda255f4cfddd1929b4c1faf23e85de854c153e31805.
[Summary](../../../Analysis/MasterTests/outputs/r4c1_g3n5_observable_correction_attempt_01/summary.json):
105fb82583080699e300027737e2e6c117827ba4b273b2d03494f099d0491cbc.
Formula hash: e60447325960c8e795b4bbb6d8771af2c42b06c60cfdc187d92be2dd4e86f667.
Diagnostics hash: 34200c1c0d83c5461f8b2b5d860b78e81e4a7803ae4c60678b5a39deee226ba8.
All 483 pinned input/source/available-sidecar files preserved hash/size/mtime.
All 29 checks passed; replay independently recomputed and matched every
scientific JSON and sidecar byte without modifying the receipt directory.
Failures, missing inherited sidecars and private exploratory sources remain.

The ITSM memory skill keeps conditional local coefficients separate from
canonical or physical clearance. Current source equations and pinned receipts,
not old memory or model agreement, are evidence. No vault mutation occurred.
The standalone optimizer was used; no billing-savings guarantee is claimed.

Stage 1 remains OPEN. Stage 2 STOP_AND_ASSESS_DOMAIN_UNRESOLVED with no
new action-selection authority; full coupled physical interactions/window and
healthy GR remain missing. Stage 3 NOT ENTERED; identifying residue/nonlinear
force matching is absent. Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 UNCHANGED. Inherited reviews remain DEFERRED, not cleared. No publication,
submission, model/provider dispatch, commit/push, manuscript/PDF or deployment change.
