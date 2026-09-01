# UVIR-003 Stage B finite-q scalar-shift dressing sub-block

Date: 2026-07-29
Branch: `recovery/v12-core-architecture`
Scope: gravity/aether scalar shear with one soft curvature leg

## Decision

The exact gravity/aether extrinsic-curvature action has been expanded through
quartic order for a nonzero-momentum scalar shift,

```text
z = (delta_N, Sigma),
Sigma = -D^2 beta = q_phys^2 beta,
q_phys > 0,
```

with one spatially homogeneous curvature leg. This is a valid soft-leg
finite-`q` interaction channel and exposes the nonlinear lapse/shift dressing
that is absent from the origin-linear source.

The result is

```text
PASS_SOFT_CURVATURE_SHIFT_DRESSING_SUBBLOCK.
```

It is not the complete non-collinear three-momentum kernel.

## 1. Exact soft-channel block

Choose the shift momentum along the `x` direction. For a homogeneous
curvature leg, the mixed extrinsic-curvature eigenvalues are

```text
Kx_x =
  [H + R_dot + exp(-2R) Sigma]/N,

Ky_y = Kz_z =
  [H + R_dot]/N.
```

The exact gravity/aether coefficients obey

```text
A_K + B_K = -D_123,
A_K + 3 B_K = -2 M_cos^2,
```

so

```text
A_K = M_cos^2 - 3 D_123/2,
B_K = -M_cos^2 + D_123/2.
```

The resulting extrinsic-curvature density is

```text
L_K =
  exp(3R)/N [
    -3 M_cos^2 (H + R_dot)^2
    -2 M_cos^2 (H + R_dot) exp(-2R) Sigma
    -(D_123/2) exp(-4R) Sigma^2
  ].
```

Its quadratic constraint sub-matrix is exactly

```text
C_K =
  [ -6 H^2 M_cos^2    2 H M_cos^2 ]
  [  2 H M_cos^2         -D_123   ].
```

This regresses to the extrinsic-curvature portion of the verified finite-`q`
quadratic constraint matrix.

## 2. Origin-linear source

For this declared channel, the coefficient linear in constraints at the
origin is

```text
J2_N,origin =
  (3 M_cos^2/2) [
    9 H^2 R^2 + 12 H R R_dot + 2 R_dot^2
  ],

J2_Sigma,origin =
  -M_cos^2 R (H R + 2 R_dot).
```

These are verified components, but they are not the dressed source.

## 3. Nonlinear dressing

Let

```text
z1 = (delta_N1, Sigma1) = -C^(-1) J1.
```

The exact cubic action gives

```text
S2 = partial_z L3[x,z] evaluated at z=z1.
```

The lapse correction is

```text
Delta S2_N =
  1/2 [
    D_123 Sigma1^2
    -36 H^2 M_cos^2 R delta_N1
    +18 H^2 M_cos^2 delta_N1^2
    +4 H M_cos^2 R Sigma1
    -24 H M_cos^2 R_dot delta_N1
    -8 H M_cos^2 Sigma1 delta_N1
    +4 M_cos^2 R_dot Sigma1
  ].
```

The scalar-shift correction is

```text
Delta S2_Sigma =
  D_123 R Sigma1
  + D_123 Sigma1 delta_N1
  + 2 H M_cos^2 R delta_N1
  - 2 H M_cos^2 delta_N1^2
  + 2 M_cos^2 R_dot delta_N1.
```

Both corrections are generically nonzero.

## 4. Finite-q first-order solution

For

```text
C =
  [ C_14 q_phys^2 - 2V    2 H M_cos^2 ]
  [ 2 H M_cos^2               -D_123  ],
```

define

```text
Delta_C =
  C_14 D_123 q_phys^2
  - 2 D_123 V
  + 4 H^2 M_cos^4.
```

Then

```text
delta_N1 =
  [-D_123 J1_N - 2 H M_cos^2 J1_Sigma]/Delta_C,

Sigma1 =
  [-2 H M_cos^2 J1_N
   +(C_14 q_phys^2 - 2V) J1_Sigma]/Delta_C.
```

Direct substitution verifies `C z1 + J1 = 0`. The cubic and direct quartic
soft-channel blocks `L3[x,z1]` and `L4[x,z1]` are generated symbolically.

## 5. Boundary

This checkpoint derives:

- the exact gravity/aether scalar-shear block through quartic order;
- the nonlinear `delta_N1`/`Sigma1` correction to both components of `S2`;
- finite-`q` substitution of `z1=-C^(-1)J1`;
- `L3[x,z1]` and `L4[x,z1]` for the declared soft channel.

It does not derive:

- the generic non-collinear three-momentum gravity/aether kernel;
- `D_iR D_i beta` terms for arbitrary momentum triads;
- condensate or Track-A force shift-advection dressing for generic triads;
- the complete physical scalar projection or amplitude.

The homogeneous time-translation gauge result is unchanged because this
calculation is explicitly restricted to `q_phys>0`.

## 6. Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_scalar_shift_dressing.py
```

Expected footer:

```text
Exact soft-channel gravity+aether shift block: VERIFIED
Finite-q first-order z1 substitution: VERIFIED
Nonlinear lapse/shift correction to S2: VERIFIED
Soft-channel L3[x,z1] and L4[x,z1]: VERIFIED
Generic non-collinear finite-q S2: NOT_YET_DERIVED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_SOFT_CURVATURE_SHIFT_DRESSING_SUBBLOCK
```

Machine-readable output:

```text
Analysis/UVIR/UVIR-003/outputs/
  uvir003_scalar_shift_dressing_summary.json
```
