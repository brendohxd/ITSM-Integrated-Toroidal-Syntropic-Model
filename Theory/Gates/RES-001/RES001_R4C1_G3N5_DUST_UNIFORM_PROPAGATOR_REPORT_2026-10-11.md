# G3N5: uniform mixed-order propagator on the rotating B1 background

Date: 11 October 2026. Owner: Master Test 1 / conditional R4C1/B1, stage 1.
Disposition: CONDITIONAL_UNIFORM_MIXED_NORM_LINEAR_PROPAGATOR.
V2: 66/66 local checks, zero failed/unknown, exact read-only replay.
The prepared dust remainder and its actual convergence order remain OPEN.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.

## 1. Result and unchanged domain

For the complete registered 20-state linear system there is a positive,
time-dependent evolution norm with a bound independent of ell for ell>=4
on 0<=s<=t<=1/20. All 22 original fields and both complex scalar directions
are retained. This removes one obstruction in the previous absolute-value
majorant: large dispersive frequencies need not produce an exponentially
large momentum-dependent amplification estimate.

The exact B1 background is unchanged. Its initial data include v_dot=1,
r_dot=1/4 and angular charge a^3(u v_dot-v u_dot)=1, not a real nonrotating
scalar background. Coordinate periods are 2*pi and p=ell/a, p_dot=-H*p.
These are formal reference units, not measured galactic wavelengths or an
identified physical EFT cutoff. Zero modes, singular endpoints, arbitrary
backgrounds and all-direction nonlinear evolution are outside this proof.

## 2. Exact transformation, principal cancellation and bound

Starting with the existing balanced state z=B x, retain all 20 components.
Let C be the identity except C[13,13]=p, restoring the longitudinal frame
velocity derivative's mixed-order weight. With U^3=g U, g=-22 a^2/375,

```text
T_f = I+U/ell,
T_f_inverse = I-U/[ell(1-g/ell^2)]+U^2/[ell^2(1-g/ell^2)],
w = T_w T_f_inverse C z.
```

The inverse denominator is 1+22 a^2/(375 ell^2)>1. T_w has determinant 1;
C is invertible for a>0,ell>0. Every coordinate derivative is retained.
The full unspecialized transformed generator is rechecked symbolically:

```text
A_w = ell^2 F + ell L + T_w_dot T_w_inverse
      + (sum_{j=0}^5 V_j/ell^j)/(1+22 a^2/(375 ell^2)).
Q F+F^dagger Q = Q L+L^dagger Q = 0.
```

No order-zero/negative-order operator term, wave, slow or fast state is
discarded. The exact maps and residual matrices are linked and revalidated
in the [v2 formulas](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json).

Q is positive: its complex-scalar block is I+(v,-u)^T(v,-u)/13, with the other
entries specified in the receipt. Q>=D>0 for fixed diagonal D whose entries
are 1 except D00=1/3, D44=D55=4/5, D99=5/33. In particular Q>=5 I/33.
This is an evolution norm, not a positive physical Hamiltonian assertion.

Use the actual rotating background and rational ODE bootstrap bounds in
the [v2 controls](RES001_R4C1_G3N5_DUST_UNIFORM_PROPAGATOR_V2_CONTROLS_2026-10-11.md).
The Hermitian energy derivative is bounded with D^(-1/2), retaining the
off-diagonal Q and Q_dot. Exact rational outward interval/Gershgorin bounds
give E_dot<=mu E, E=w^dagger Q w, with the complete rational mu in formulas.
The displayed mu is 59.331802659385374 and the exact rational is less than 60.
Consequently,

```text
||w(t)||_Q(t) <= exp(mu*(t-s)/2) ||w(s)||_Q(s)
             <= exp(30*(t-s)) ||w(s)||_Q(s).
```

The sharper endpoint amplification display is 4.407444603338979. The simple
rigorous endpoint expression is exp(3/2), approximately 4.482. Neither is a
measured growth rate or proof of physical stability. The proof comes from
the exact identities and interval enclosure, not the sampled checks.

## 3. Failed first attempt is not erased or relabelled

V1 and attempt 01 failed 67/72. I incorrectly assumed zero v_dot and r_dot
when tightening the background enclosure. The five independent archive-domain
checks each rejected it, with violation 1. Its displayed 2.798753391173326
bound and affirmative proof flag are NOT valid for our registered background.
Do not reuse that flag or bound as an admitted result.

V1's original source, controls, receipt, hashes, sidecars and private log are
preserved. V2 does not modify initial data or omit rotation to obtain a pass.
It reuses only general unspecialized maps, rechecks their exact generator and
inverse identities, and calculates a new energy enclosure with the full Q.
The corrections are substantive domain corrections, not merely bookkeeping.

## 4. Controls, evidence and preservation

- All five modes ell=4,8,16,32,64, 257 times, two prepared columns and two
  complementary columns remain. The old nonmonotonic responses are unchanged.
- Worst normalized direct/factored generator disagreement: 1.9696180874039399e-16.
- Worst full inverse reconstruction disagreement: 5.700926707640965e-16.
- Worst all-22-field archive disagreement: 9.615893912656803e-15.
- Every sampled new background enclosure violation is zero. Every column's
  Q-norm amplification satisfies the analytic bound, including t=0; these are
  controls rather than a continuous-time proof.
- V2 preserves 451 input/source/available-sidecar files in hash, size and mtime.
  Exact scientific JSON and sidecar replay passed without receipt writes.

[Executable v2](../../../Analysis/MasterTests/test_01_r4c1_g3n5_dust_uniform_propagator_v2.py):
bda5fcb42e6fec850093075d681c712972b951fc08107f3f70eed52420898ca3.
[Summary](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_uniform_propagator_attempt_02/summary.json):
ba2c19f2ee923816ca4ae0bf2de6a2cf4d898975c468cd0529d6cbc9f2dc1356.
Formula artifact: 8373e57ab213e8f342fe026500c712a974b522f9c15a074ef7a4225475676e9f.
Diagnostics: 96b2cf9e064c5801ea7d1bb9a16416ed0a638989cb6709001d91ca32dc155053.

Use the known itsm_env Python with -B and executable v2; --replay followed by
Analysis/MasterTests/outputs/r4c1_g3n5_dust_uniform_propagator_attempt_02.

## 5. Remaining acceptance requirements and next work

The [earlier exact split](RES001_R4C1_G3N5_DUST_REMAINDER_REPORT_2026-10-11.md),
its nonzero R r and S W terms and first inverse-p^2 graph correction remain.
Uniform full-state amplification does not by itself bound the dust-observable
error or prove an inverse-square rate. The prepared graph is not an invariant
subspace; the generated fast response and any corrected-lift initial mismatch
must be retained and controlled in the actual observable.

Next: use this uniform propagator to bound an action-derived corrected lift,
its residual forcing and prepared initial mismatch. Prove the observable
remainder's order and constants, or record the precise remaining obstruction.
Do not infer a sharp order from the five-mode sample or continually project
evolution onto the slow graph. Stage 1 is not complete.

The original -11/6 slow velocity coefficient, indefinite Hamiltonian and
ordinary-wave Jordan defect remain; this frequency-dependent mixed norm does
not replace the rejected equal-regularity ordinary-wave formulation. No ghost,
physical cutoff, healthy GR or canonical clearance follows. Stage 2 still
needs full coupled interactions and a physical validity window; the operator
may reassess its action choice later. Stage 3 has not been entered.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
The memory skill kept local validation distinct from physical closure; current
repository equations/receipts supplied the evidence. Standalone optimizer used;
no provider billing savings claimed. No vault mutation, provider/model change,
manuscript/PDF, publication, submission, commit, push or deployment change.
