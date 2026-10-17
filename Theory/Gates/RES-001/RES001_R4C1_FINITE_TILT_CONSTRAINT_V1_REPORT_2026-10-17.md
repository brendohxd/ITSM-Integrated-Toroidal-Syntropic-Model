# R4C1 finite tilt: complete velocity map, physical constraints still open

17 October 2026. Master Test 1 / unchanged-action Stage 2.
Conditional calculation: 243/243 local checks; fresh exact read-only replay,
exit zero. Review DEFERRED; Rule9_cleared=false; physics_pass=false;
gate_effect=NONE. The FULL finite-amplitude physical reduction is NOT complete.

## Finding and meaning

The complete 22-field temporal Hessian has now been recomputed from the
original density at finite relative frame tilt. On its regular Legendre
patch, including the other metric, frame, scalar and dust velocities does
not create a hidden primary constraint that restores an algebraic Z.
The independent unit and dust multiplier equations do not supply that
missing Z relation either. This extends the earlier isolated psi/Z check;
it is NOT the final gravitationally constrained physical Hessian.

The local calculation cannot decide whether the extra velocity direction
belongs to admissible physical initial data/propagation, lies outside an
eventual controlled EFT window, or is removed by a remaining constraint.
In particular it does not establish a physical ghost, a viable family, a
physical cutoff, a full nonlinear initial-value theorem or healthy GR.

## Action, local chart and scope

The frozen [contract](RES001_R4C1_FINITE_TILT_CONSTRAINT_V1_CONTRACT_2026-10-17.md)
uses the original unspecialized G3N5 density, not substitutions into its
aligned quadratic kernel. All 22 fields are retained in its original order:

    alpha, Sx, Sy, Sz, Mxx, Mxy, Mxz, Myy, Myz, Mzz,
    Vx, Vy, Vz, du, dv, dr, Pi, T, Em, Z, nu, LambdaU.

At the evaluation point N=1, shift=0, spatial metric is orthonormal and
n=(gamma,w,0,0), gamma=sqrt(1+w^2). This is a local basis choice, NOT an
n-orthogonal slicing assumption or a newly admitted tilted solution.
The configuration w is finite before varying velocities; the perturbative
amplitude is not truncated first. The original independent extension
U=(1+nu)n is retained through variation.

All six metric velocities, three frame velocities, normal variation,
Cartesian scalars, dust and regulator enter. The acceleration term
-b Z acc(n).grad(psi), arbitrary Z, arbitrary spatial psi gradient and
the actual -A Y^(3/2) term are retained. The temporal kinetic remains
K_Q (n.grad psi)^2/2, not a replacement Lorentz-scalar kinetic.

The quadratic first-derivative sectors have Hessians independent of fixed
spatial first jets: for a quadratic form Q(A v+B), the v-Hessian is
2 A^T Q A, independent of B. This permits their temporal coefficients to
be computed without claiming those spatial jets vanish in the field equations.
Spatial Ricci and the full potential/portal have zero temporal Hessian;
they remain necessary inputs to the uncompleted lapse/momentum equations.

The three families retain the frozen generic maps, including b=5 eta/11,
K_Q=3 eta, MU2=2 eta/3, A=2 eta^(3/2)/7, zeta=eta/13 and beta=2 eta^2/5.
These are diagnostic inputs, not derived microscopic constants. Arithmetic
controls use eta=1/4,1/64,1/1024 and w=0,+/-1/10,+/-1/20,1/100.
Their scalar/control values are off-shell tests, NOT the registered exact
prepared finite-amplitude on-shell state or a replacement initialization.

## Why the complete Legendre calculation matters

Write p=psi_dot and q_i=partial_i psi in this point basis. Direct variation
of the FULL density gives

    p_Z = -b [w^2 p + gamma w q_x],
    H_Z,Pi = -b w^2; H_Z,Z=0; H_Z,j=0 for every j other than Pi.

Lapse/shift velocities cancel in all 16 covariant n-derivative entries.
The six rows alpha, Sx, Sy, Sz, Em and LambdaU of the 22-field temporal
Hessian vanish. The remaining 16-velocity block includes nu and dust time.

Order its COMPLETE remaining complement R before Pi and Z. It has structure

    H_dyn = [[R, h, 0], [h^T, a, -b w^2], [0, -b w^2, 0]].

For det R != 0 the exact Schur pair is

    [[a-h^T R^-1 h, -b w^2], [-b w^2, 0]],
    det(pair) = -b^2 w^4,
    det(H_dyn) = -b^2 w^4 det R.

The determinant identity also follows directly by expansion along the Z
row/column. It does not freeze the metric/frame velocities, assume h=0,
or assume the complement is positive. The same structure holds after the
unit-tangent restriction removes nu_dot, wherever that complement is regular.
The exported formulas retain the complete metric/frame/normal determinants
and their zero sets; no inverse at a zero determinant is licensed.

Thus, for b w != 0 on this regular Legendre patch, p_Z determines p rather
than constraining phase-space data by a Z-primary relation. This is a
Legendre statement, not a physical count of propagating degrees of freedom.
At w=0 the Z velocity relation changes rank; no uniform inverse across
alignment or the eta=0 endpoint has been established or used.

## What the auxiliary equations actually remove

Variation of LambdaU gives -(nu+nu^2/2)=0. The future/unit branch 1+nu>0
selects nu=0, with differentiated condition nu_dot=0. The coefficient of
LambdaU in the nu equation is -(1+nu), nonzero on this branch; this normal
equation must determine its multiplier, not be discarded before variation.

For positive density and future comoving dust, retain volume=sqrt(det h),
lapse N, C>0 and the spatial dust gradient before any clock gauge. Its
Hamiltonian density at zero shift is

    H_dust = N [p_T^2/(2 volume epsilon C^2)
                 + volume epsilon (C^2 |D T|^2+C^4)/2].

The epsilon equation has nonzero density Jacobian
p_T^2/(volume epsilon^3 C^2) on the stated branch. It solves epsilon as

    epsilon = p_T/[volume C^2 sqrt(|D T|^2+C^2)],  p_T>0.

It is not an extra algebraic constraint on the psi/Z momenta. For zero
spatial dust gradient, N=T_dot/C, not C*T_dot; at N=1 the original
background convention remains T_dot=C. No lapse/momentum equation has
been deleted by imposing T=t before variation.

## Verification, including limitations of the controls

- Every one of the 484 symbolic temporal entries is derived and symmetric.
  The aligned limit matches every entry of the independently stored original
  kernel. The actual C2 cusp has zero second derivative on Y=0; a nonexistent
  ordinary third derivative is not inserted.
- All ten density-sector dimensions and all nonzero Hessian-entry dimensions
  match. Direct nonzero-term controls retain metric/frame mixing, normal
  variation, temporal-not-Lorentz kinetics and the Z acceleration coupling.
  Omitting those terms is also tested by the independent density comparisons.
  These are mathematical rejection controls, not separately mutated-code runs.
- 54 full-matrix arithmetic cases retain all three families and all tilt
  strata. The complete determinant factorization is compared with direct
  full-matrix determinants at all 45 nonzero-tilt points. Numerical ranks
  and inertias are controls, not interval or physical-domain proofs.
- At each of two finite-tilt parameter controls, 22 individual velocity
  directions and four dense all-field directions are independently evaluated
  from the original ADM metric/vector definitions. Both unrotated and rotated
  spatial bases are tested: 52 directions, 104 original-density comparisons.
  Nonzero Z and finite spatial psi gradients are retained. At 80 digits the
  largest normalized discrepancy is 1.0542197943230523e-81, below the frozen
  1e-40 tolerance.
- Full dynamic raw inertia at w=0 is 13 positive / 2 negative / 1 zero;
  at the 45 nonzero controls it is 13 / 3 / 0. After the unit-tangent
  restriction these become 13 / 1 / 1 and 13 / 2 / 0. These are NOT physical
  reduced-mode inertias. The metric conformal sector already illustrates
  why an unreduced negative direction alone is not a ghost diagnosis.
- All 243 checks pass with no failed/unknown check rows. The five missing
  physical obligations remain explicit in the summary; zero unknown CHECK
  rows does not mean zero unknown PHYSICS. All 11 sources and 22 source/
  sidecar metadata records are unchanged. Exact replay freshly recomputes
  all three JSON payloads and preserves all six payload/sidecar bytes and
  modification times. Both original run and replay terminate exit zero.

The existing environment is Python 3.13.9, SymPy 1.14.0, mpmath 1.3.0;
no library, model/provider or runtime reconfiguration is performed.

Methodological comparison only: [Garfinkle, Isenberg and Martin-Garcia](https://arxiv.org/abs/1207.6530)
explain why fixed-metric vector constraints do not replace the coupled
gravity calculation. Their theory does not supply this action's constraints
or an ITSM verdict; all equations/results above are repository calculations.

## Remaining acceptance and next calculation

The contract's FULL physical reduction is OPEN. Still missing:

1. Derive the complete finite-tilt canonical lapse and shift constraints,
   restoring spatial curvature, potential, all spatial first jets and the
   coupled momenta; establish their actual preservation/closure and reduction.
2. Construct admissible finite-amplitude prepared initial data with the torus
   mean/harmonic sector and fixed global charges. Off-shell test points do
   not prove such a state exists or belongs to the archived preparation.
3. Determine an admissible Cauchy/characteristic and physical energy domain,
   and whether the regulator direction survives in its physical reduction.
   Do not infer an extra propagating mode or ghost from the Legendre rank.
4. Control the nonlinear remainder and establish a nonempty physical window
   and justified GR recovery. A regular kinetic patch is NOT that window.
5. Supply genuine matter-residue and nonlinear-force matching inputs before
   entering numerical Stage 3. No assumed coefficient or target fit fills them.

Next work is the actual canonical lapse/shift Hamiltonian and constraint
algebra, not more raw eigenvalue samples or another completed dust/tail audit.
No family receives GO. R9-MT1-FINITE-TILT-CONSTRAINT-V1 is DEFERRED and may
support only the stated Legendre/auxiliary observations. Inherit G3N5's
off-shell kernel, G3N2, the generic family-map and source-aware review debt.

Stage1 complete only in registered linear prepared-dust scope; Stage2
INCOMPLETE; Stage3 NOT_ENTERED. Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 unchanged. No physical pass, publication readiness or Rule-9 clearance.

## Frozen artifacts and replay

| Artifact | SHA-256 |
|---|---|
| Contract | 5bc0f9b3f81869f576bc8e7373cb4770727a1e64abef7cad1974263f4bca205d |
| Executable | 199d2ae85d059eaf5861570e03b44f31b739e1c48e396f1579bf3dc547b55579 |
| summary.json | 43b28344b62ba35b1a5b2e1adbef9d8dc76d924bc2fb41f1451c6c12dc6cf7ef |
| formulas.json | 69ada62a0bf17ddaeb1240ad94f2fb9f911b9daf795c17f1fff04ea12b8e3839 |
| numerics.json | 1b7d3592f3507a2c41fac9230ca55058ec48a85ccade151f53c59309c4054096 |

Executable: `Analysis/MasterTests/test_01_r4c1_finite_tilt_constraint_v1.py`.
Receipt directory: `Analysis/MasterTests/outputs/r4c1_finite_tilt_constraint_attempt_01`.

    python -B Analysis/MasterTests/test_01_r4c1_finite_tilt_constraint_v1.py --replay Analysis/MasterTests/outputs/r4c1_finite_tilt_constraint_attempt_01

New calculations require --output with a NEW nonexistent directory. No source,
old evidence, sidecar or failed attempt is replaced. Only the mutable research
queue/review indexes receive a guarded append and new index digests. No vault,
manuscript/PDF/site, commit/push, publication/submission or action change.
