# UVIR-003 Stage B origin-linear finite-q J2 component

Date: 2026-07-29  
Branch: `recovery/v12-core-architecture`  
Scope: homogeneous zero-gradient force branch at finite scalar momentum

## Correction notice

The constraint-dressing completeness audit supersedes this report's original
interpretation. Every displayed origin-linear source formula and the algebraic
`-J2^T C^(-1)J2/2` identity remain verified, but they are components rather
than the complete second-order source and quartic constraint block.

The correct source after first-order constraint substitution is

```text
S2 = partial_z L3[x,z] evaluated at z=-C^(-1)J1.
```

See `UVIR-003_STAGE_B_CONSTRAINT_DRESSING_AUDIT.md`.

## Decision

The complete quadratic lapse/scalar-shift source has now been assembled from
the fixed

```text
gravity + Einstein-aether + condensate + alignment + Track-A force
```

action. In the same finite-wavenumber convention as the verified quadratic
ADM reduction,

```text
z = (delta_N, Sigma),
Sigma := -D^2 beta = q_phys^2 beta,
```

the result is

```text
HISTORICAL_STATUS_SUPERSEDED_BY_CONSTRAINT_DRESSING_AUDIT.
```

The exact `Y^(3/2)` term has no `J2` Taylor component at the homogeneous
zero-gradient origin. Its separate Track-A nonzero-gradient local analysis is
unchanged.

This checkpoint also evaluates the constraint-induced quartic functional

```text
-J2^T C^(-1) J2 / 2.
```

It does not yet derive the direct multi-sector quartic contact action, the
regular physical-scalar projection, a cosmological `2-to-2` amplitude or a
cutoff. UVIR-003 remains in progress and MAT-001 remains blocked.

## 1. Conventions

Use the aether-unitary scalar gauge

```text
U^mu = n^mu,
N = 1 + delta_N,
N_i = partial_i beta,
h_ij = a^2 exp(2R) delta_ij.
```

The dynamical scalar perturbations are

```text
(R, delta_rho, vartheta, pi).
```

`D_i` below is the physical derivative on the unperturbed FRW leaf. The force
background is homogeneous and spatially constant.

The fixed finite-`q` constraint matrix is

```text
C(q) =
  [ C_14 q_phys^2 - 2V       2 H M_cos^2 ]
  [ 2 H M_cos^2             -D_123       ].
```

## 2. Linear-source regression

Expanding the exact nonlinear parent action first reproduces the previous
linear source:

```text
J1_N =
  6 H M_cos^2 R_dot
  - 2 M_P^2 D^2 R
  - (V_rho + rho mu^2) delta_rho
  - rho_dot delta_rho_dot
  - rho^2 mu vartheta_dot,

J1_Sigma =
  -2 M_cos^2 R_dot
  - rho_dot delta_rho
  - rho^2 mu vartheta.
```

In Fourier space, `-D^2 R=q_phys^2 R`, so this is exactly the source used in
the verified finite-`q` quadratic reduction.

## 3. Complete lapse source J2

After using the Friedmann identity

```text
3 M_cos^2 H^2
  = (rho_dot^2 + rho^2 mu^2)/2 + V,
```

the quadratic lapse source per physical background volume is

```text
J2_N =
  3 M_cos^2 R_dot^2
  + 18 M_cos^2 H R R_dot
  - 2 M_P^2 R D^2 R
  - M_P^2 D_i R D_i R

  - delta_rho_dot^2/2
  - mu^2 delta_rho^2/2
  - 2 rho mu delta_rho vartheta_dot
  - rho^2 vartheta_dot^2/2

  - 3 R [
      rho_dot delta_rho_dot
      + rho mu^2 delta_rho
      + rho^2 mu vartheta_dot
      + V_rho delta_rho
    ]
  - V_rhorho delta_rho^2/2

  - [
      D_i(delta_rho) D_i(delta_rho)
      + rho^2 (1 + zeta_align rho^2)
        D_i(vartheta) D_i(vartheta)
    ]/2

  - K_Q pi_dot^2/2
  - gamma [D^2 pi]^2/(2 M_star^2).
```

The last line is exactly the previously verified Track-A force lapse source.

## 4. Complete scalar-shift source J2

Before spatial integration by parts, the quadratic term linear in `beta` is

```text
L3_beta/a^3 =
  2 M_cos^2 [
    (R R_dot + H R^2/2) D^2 beta
    + (R_dot + H R) D_i R D_i beta
  ]

  - D_i beta [
      delta_rho_dot D_i(delta_rho)
      + R rho_dot D_i(delta_rho)
      + rho^2 vartheta_dot D_i(vartheta)
      + 2 rho mu delta_rho D_i(vartheta)
      + R rho^2 mu D_i(vartheta)
      + K_Q pi_dot D_i(pi)
    ].
```

Define

```text
W_i =
  2 M_cos^2 (R_dot + H R) D_i R
  - delta_rho_dot D_i(delta_rho)
  - R rho_dot D_i(delta_rho)
  - rho^2 vartheta_dot D_i(vartheta)
  - 2 rho mu delta_rho D_i(vartheta)
  - R rho^2 mu D_i(vartheta)
  - K_Q pi_dot D_i(pi).
```

Then the finite-`q` normalized shift source is

```text
J2_Sigma =
  -2 M_cos^2 (R R_dot + H R^2/2)
  + (D^2)^(-1) D_i W_i.
```

The inverse Laplacian is defined mode by mode only for `q_phys>0`. This is the
same domain on which `Sigma=q_phys^2 beta` is an independent constraint
variable. The exactly homogeneous time-translation orbit remains governed by
the existing low-`q` gauge audit and is not reclassified here.

## 5. Constraint-induced quartic block

Define

```text
Den =
  C_14 D_123 q_phys^2
  - 2 D_123 V
  + 4 H^2 M_cos^4.
```

For `Den != 0`,

```text
C^(-1) =
  1/Den [
    D_123                    2 H M_cos^2
    2 H M_cos^2             -C_14 q_phys^2 + 2V
  ].
```

The second-order constraint solution is

```text
z2 = -C^(-1) J2.
```

Substitution into the quartic action gives

```text
L4_constraint =
  -J2^T C^(-1) J2/2

  = [
      (C_14 q_phys^2 - 2V) J2_Sigma^2
      - D_123 J2_N^2
      - 4 H M_cos^2 J2_N J2_Sigma
    ]/(2 Den).
```

The symbolic audit verifies this result both by matrix inversion and by direct
completion of the square.

For the field-theory functional, products in `J2` are convolutions:

```text
S4_constraint =
  -1/2 integral d^3k
  J2(-k)^T C(k)^(-1) J2(k).
```

## 6. What has advanced

Verified:

- exact regression to the previous finite-`q` `J1`;
- origin-linear multi-sector `J2_N`;
- origin-linear multi-sector `J2_Sigma` for `q_phys>0`;
- Track-A force-source regression;
- the exact finite-`q` constraint inverse;
- the origin-linear algebraic quartic Schur component.

Not yet derived:

- the direct multi-sector cubic and quartic contact actions;
- the regular physical-scalar eigenmode projection;
- the cosmological `2-to-2` exchange-plus-contact amplitude;
- a unitarity criterion or physical cutoff;
- the separate nonzero-gradient local reduction of exact `Y^(3/2)`.

## 7. Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_full_j2_schur.py
```

Expected footer:

```text
Finite-q J1 regression: VERIFIED
Complete multi-sector finite-q J2: VERIFIED
Origin-linear quartic Schur component: VERIFIED
Direct multi-sector quartic contact: NOT_YET_DERIVED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_ORIGIN_LINEAR_J2_COMPONENT
```

Machine-readable output:

```text
Analysis/UVIR/UVIR-003/outputs/uvir003_full_j2_schur_summary.json
```

## 8. Next bounded calculation

Derive the direct

```text
gravity + aether + condensate + alignment
```

cubic and quartic contact actions in the same conventions. Combine the direct
quartic block with the corrected dressed-source Schur functional, then project
quartic interactions onto the regular physical-scalar basis. Only that
combined result can support the gauge-regular cosmological `2-to-2` amplitude
and a physical unitarity criterion.

## Status

```text
Origin-linear finite-q J2: ASSEMBLED_AND_VERIFIED
Constraint-induced quartic block: ASSEMBLED_AND_VERIFIED
Direct multi-sector quartic contact: NOT_YET_DERIVED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_ORIGIN_LINEAR_J2_COMPONENT
```
