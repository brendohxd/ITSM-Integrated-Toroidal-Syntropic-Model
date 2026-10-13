# G3N5: retained fast-component transfer bound

Date: 11 October 2026. Owner: Master Test 1 / conditional R4C1/B1, stage 1.
Result: CONDITIONAL_FAST_COMPONENT_TRANSFER_LEMMA, 33/33 local checks,
zero failed/unknown, exact read-only replay. Complete prepared dust error
and sharp convergence order remain OPEN. physics_pass=false; gate_effect=NONE;
Rule9_cleared=false; review DEFERRED. No physical family admission.

## 1. What is newly established

Starting from the [uniform rotating-B1 propagator](RES001_R4C1_G3N5_DUST_UNIFORM_PROPAGATOR_REPORT_2026-10-11.md),
an exact second change of variables controls transfer from a fast coordinate
component into the other coordinates. It applies to a COMPONENT of the
original prepared-data mismatch, not a newly chosen physical initial state.
The old complementary probes are not asserted to be pure fast eigenstates.

All 20 first-order states, angular charge J=1 and both complex scalar
directions remain. The 22-field reconstruction, unchanged B1 action,
coordinate/momentum drift and complete off-block coupling are retained.
Time domain: 0<=s<=t<=1/20, positive a,C,rho_m, fixed positive ell and p=ell/a.

## 2. Exact normal form and mathematical domain

In the existing w coordinates, let P_f select indices 9,19 and P_o=I-P_f.
The positive evolution metric Q and both principal operators respect the split.
Write A_w=ell^2 F+ell L+B0+B_rem. Solve

```text
[F,V_map]+off_f(B0)=0,
y=(I+V_map/ell^2)^(-1) w,
A_y=ell^2 F+ell L+diag_f(B0)
    +(I+V_map/ell^2)^(-1) [ [L,V_map]/ell
      +(B0 V_map-V_map diag_f(B0)-V_map_dot)/ell^2
      +B_rem (I+V_map/ell^2) ].
```

V_map is a coordinate matrix, NOT the missing MAT-001 matter-residue invariant V.
The complete generator identity and V_map_dot are checked exactly.

Rational interval matrix norms bound ||V_map||_2 by an exact number displayed
as 33.34779902385899. With Q>=5 I/33 and Q<=9 I/8, norm conversion is <=3.
The Neumann requirement ell^2>=6||V_map||_2 therefore gives the derived
integer domain ell>=15. No observational discrepancy chose that threshold.
It is not a measured momentum, physical cutoff or EFT validity window.

On this domain, T2=I+V_map/ell^2 has Q-operator norm <=3/2 and its inverse
<=2. The previous uniform full propagator then gives

```text
||Phi_y(t,s)||_Q(t)<-Q(s) <= 3 exp(30*(t-s)).
||off_f(A_y)||_Q <= kappa/ell.
```

All constants are exact rational interval expressions in the
[formulas](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_fast_transfer_attempt_01/formulas.json).
Their displays are kappa=515.2084412844515 and
gamma=30+3*kappa/15=133.0416882568903. A bounded-perturbation Volterra estimate
gives the block-diagonal COMPARISON propagator <=3 exp(gamma*(t-s)). This is
only a tool for bounding the full coupled solution; actual off-block evolution
is never suppressed, and no repeated slow projection is performed.

For an initial component with y_other(0)=0, variation of constants using the
FULL retained fast response yields

```text
||y_other(t)||_Q(t)
    <= 9*kappa*t*exp(gamma*t)*||y_fast(0)||_Q(0)/ell.
```

This is a conservative upper bound, not an observed response or instability
rate. By linearity an actual initial mismatch can be split into its two
components without replacing that initial mismatch. The bound must still be
combined with the actual observable map, corrected-lift forcing and data.

## 3. Independent controls and retained low modes

All five archived modes and all four original columns remain. All 22 fields
were checked at t=0,1/40,1/20. Worst field disagreement: 5.926090835233935e-15.
Above the new inverse domain (ell=16,32,64), worst normalized generator
disagreement is 2.220542154403707e-16; worst inverse disagreement is
2.794973307947217e-17. Coupling times ell is at most 17.0514099385131 at these
control points, below the independently derived interval constant 515.20844.
Those samples do not supply the constant or continuous-domain proof.

Ell=4 and 8 are explicitly OUTSIDE this new lemma. Their original archive
results are unchanged. Zero inverse/generator/coupling placeholders in their
new diagnostic rows mean NOT EVALUATED for T2, not measured zero errors.
The earlier ell>=4 full-propagator certificate remains separate and valid.
Nonmonotonic complementary responses and all adverse signs remain intact.

The main calculation preserves 463 input/source/available-sidecar files in
hash, size and mtime. Read-only replay matches all three JSON outputs and
their sidecars exactly. Earlier failed sources, including the rejected
nonrotating-background uniform bound, are retained rather than overwritten.

[Executable](../../../Analysis/MasterTests/test_01_r4c1_g3n5_dust_fast_transfer_v1.py):
7a982ff1c100b35aee057030f818efd7024af491cd537fc0baf88cf486eac2cf.
[Summary](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_fast_transfer_attempt_01/summary.json):
c05d0237a34a4ac35771dc24da9ad961df3ed8c1fd947c10c1ca24c9d6c0d5d9.
Formula hash: 4da424c227df07c723419c0633a3d7cc13b2e8e23632b1d1bfb5513d3561861b.
Diagnostics hash: 33dd1eb20189cebfc67ee71d9a25d9a3763cb3b6b7eb8d892a8d499ccc5130b6.

## 4. Remaining work; no weaker completion claim

The original prepared graph is not invariant. Its corrected lift, whole-
interval residual forcing, original initial mismatch and ACTUAL dust
observable error must be combined before claiming a remainder or its order.
The symbolic lift recurrence has no accepted scientific receipt yet. An
interrupted private exploratory source remains preserved without a mathematical
pass/fail verdict; no formal expansion or additional samples close this gate.
The new lemma does not change or narrow the approved acceptance requirements.

Stage 1 remains OPEN. Stage 2 still lacks full physical interactions/window
and healthy GR admission; the operator can reassess its action choice later.
Stage 3 remains NOT ENTERED. Original -11/6 coefficient, ordinary-wave Jordan
defect and indefinite physical Hamiltonian are not removed by this norm.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Review dependencies: rotating uniform propagator, dust remainder/finite-mode,
weighted/nonzero G3N5, B1G and inherited action/operator review, all DEFERRED.
Memory skill supplied continuity boundaries; current equations and receipts
supplied evidence. Standalone optimizer used; no billed savings are claimed.
No commit/push, publication, submission, provider/model dispatch, vault mutation,
action replacement, manuscript/PDF or deployment change.
