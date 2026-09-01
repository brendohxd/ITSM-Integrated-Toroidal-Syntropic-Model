# UVIR-003 Stage B complete finite-q S2 operator

Date: 2026-07-29
Branch: `recovery/v12-core-architecture`
Scope: complete second-order constraint source at `q_phys>0`

## Decision

The complete multi-sector functional source

```text
S2 = partial_z L3[x,z] evaluated at z=z1,
z1 = -C^(-1)J1,
```

is assembled and verified on the homogeneous zero-gradient Track-A force
branch. The result is

```text
PASS_COMPLETE_FINITE_Q_S2_FUNCTIONAL.
```

The corresponding corrected quartic constraint functional is

```text
-1/2 integral d^3k S2(-k)^T C(k)^(-1) S2(k).
```

This does not yet supply the complete generic `L4[x,z1]` contact functional,
physical scalar projection, cosmological amplitude, or cutoff.

## 1. Dependencies

This checkpoint combines:

- the verified multi-sector coefficient linear in constraints at the origin,
  `J2_origin`;
- the generic gravity/aether nonlinear lapse and shift operators;
- the condensate temporal lapse/shift-advection dressing derived below;
- the Track-A affine-constraint audit derived below.

The finite-`q` constraint matrix remains

```text
C =
  [ C_14 q_phys^2 - 2V    2 H M_cos^2 ]
  [ 2 H M_cos^2               -D_123  ],
```

with `q_phys>0` and `det(C)!=0`.

## 2. Condensate nonlinear constraint density

Define

```text
T0 = (rho_dot^2 + rho^2 mu^2)/2,

T1 =
  rho_dot delta_rho_dot
  +rho mu^2 delta_rho
  +rho^2 mu vartheta_dot,

A_beta =
  rho_dot D_i beta D_i delta_rho
  +rho^2 mu D_i beta D_i vartheta.
```

The complete nonlinear condensate cubic constraint density is

```text
L3_Phi,nonlinear =
  delta_N A_beta
  +delta_N^2 T1
  +(3 R delta_N^2-delta_N^3) T0.
```

The result follows from the exact temporal ADM block

```text
exp(3R)/(2N) [
  (rho_dot+delta_rho_dot-N^iD_i delta_rho)^2
  +(rho+delta_rho)^2
   (mu+vartheta_dot-N^iD_i vartheta)^2
].
```

## 3. Condensate source dressing

At `z1`, the lapse correction is

```text
Delta S2_N,Phi =
  rho_dot D_i beta1 D_i delta_rho
  +rho^2 mu D_i beta1 D_i vartheta

  +2 delta_N1 T1
  +(6 R delta_N1-3 delta_N1^2) T0.
```

The beta-source correction is

```text
Delta S2_beta,Phi =
  -D_i {
    delta_N1 [
      rho_dot D_i delta_rho
      +rho^2 mu D_i vartheta
    ]
  }.
```

For the normalized finite-`q` shift,

```text
Delta S2_Sigma,Phi =
  -(D^2)^(-1) Delta S2_beta,Phi.
```

## 4. Track-A force audit

The Track-A cubic force density is

```text
L3_force =
  (K_Q/2)(3R-delta_N) pi_dot^2
  -K_Q pi_dot D_i beta D_i pi

  -gamma/(2M_star^2) [
    (delta_N-R)(D^2 pi)^2
    +2(D^2 pi) D_iR D_i pi
  ]

  -A_IR [(D pi)^2]^(3/2).
```

Its lapse and beta dependence is affine. Constraint-degree decomposition gives

```text
L3_force,nonlinear-constraint = 0.
```

Therefore

```text
Delta S2_force beyond J2_origin = 0.
```

The exact `Y^(3/2)` functional remains constraint independent at cubic
amplitude order on the declared homogeneous zero-gradient branch.

## 5. Complete source

The assembled source is

```text
S2_N =
  J2_N,origin
  +Delta S2_N,gravity+aether
  +Delta S2_N,Phi,

S2_beta =
  J2_beta,origin
  +Delta S2_beta,gravity+aether
  +Delta S2_beta,Phi,

S2_Sigma =
  -(D^2)^(-1) S2_beta.
```

Sector coverage:

- gravity;
- Einstein-aether;
- canonical condensate amplitude and phase;
- current alignment;
- Track-A `Q^2`;
- Track-A rest-space regulator;
- exact `Y^(3/2)` under the declared zero-gradient rule.

## 6. Corrected Schur functional

The second-order solution is

```text
z2 = -C^(-1)S2.
```

Eliminating it gives

```text
L4_constraint =
  -1/2 integral d^3k
  S2(-k)^T C(k)^(-1) S2(k).
```

This supersedes the provisional origin-linear expression using
`J2_origin`. It is still only the constraint-elimination part of the reduced
quartic action:

```text
L4_red =
  L4[x,z1]
  -1/2 S2^T C^(-1)S2.
```

## 7. Boundary

Derived:

- condensate nonlinear lapse/shift-advection dressing;
- Track-A cubic affine-constraint audit;
- complete multi-sector finite-`q` `S2` functional;
- corrected quartic Schur functional in terms of `S2`.

Still open:

- complete generic `L4[x,z1]`;
- physical scalar eigenmode projection;
- cosmological exchange-plus-contact amplitude;
- physical strong-coupling scale and cutoff;
- nonzero-gradient exact-`Y` local reduction.

The inverse Laplacian remains restricted to `q_phys>0`; the homogeneous
time-translation gauge result is unchanged.

## 8. Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_complete_s2_operator.py
```

Expected footer:

```text
Condensate shift-advection dressing at z1: VERIFIED
Track-A cubic nonlinear constraint correction: ZERO_VERIFIED
Generic gravity/aether dressing dependency: VERIFIED
Multi-sector origin-linear source dependency: VERIFIED
Complete finite-q S2 functional: VERIFIED
Corrected quartic Schur functional: ASSEMBLED
Complete L4[x,z1]: NOT_YET_DERIVED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_COMPLETE_FINITE_Q_S2_FUNCTIONAL
```

Machine-readable output:

```text
Analysis/UVIR/UVIR-003/outputs/
  uvir003_complete_s2_operator_summary.json
```
