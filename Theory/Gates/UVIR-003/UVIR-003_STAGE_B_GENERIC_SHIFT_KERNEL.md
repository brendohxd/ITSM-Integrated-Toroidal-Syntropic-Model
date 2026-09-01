# UVIR-003 Stage B generic gravity/aether shift kernel

Date: 2026-07-29
Branch: `recovery/v12-core-architecture`
Scope: generic three-dimensional cubic constraint dressing at `q_phys>0`

## Decision

The generic real-space gravity/aether cubic constraint density and its
nonlinear lapse/scalar-shift dressing operators are assembled and verified.
The result is

```text
PASS_GENERIC_GRAVITY_AETHER_SHIFT_DRESSING_KERNEL.
```

This removes the soft-curvature restriction from the preceding scalar-shift
checkpoint. Complete finite-`q` `S2` still requires the condensate and Track-A
force shift-advection sectors.

## 1. Tensor conventions

Use

```text
N = 1 + delta_N,
N_i = D_i beta,
h_ij = a^2 exp(2R) delta_ij,
U^mu = n^mu.
```

All densities are divided by the unperturbed physical FRW volume `a^3`, and
`D_i` denotes the physical derivative on the unperturbed leaf.

Define

```text
B_ij = D_iD_j beta,
B = D^2 beta,
u = D_iR D_i beta,
W = B_ij D_iR D_j beta.
```

The conformal connection gives

```text
T_ij =
  B_ij
  -D_iR D_j beta
  -D_jR D_i beta
  +delta_ij u,

T = B + u,

T_ij T_ij =
  B_ij B_ij
  +2[-2W + B u]
```

through the order required by the cubic action.

## 2. Constraint-degree decomposition

Write

```text
L3 =
  L3[x,0]
  + L3,origin-linear
  + L3,nonlinear.
```

The origin-linear gravity/aether constraint density is

```text
L3,origin-linear =
  M_cos^2 {
    H R^2 B
    +2 R R_dot B
    +2 H R u
    +2 R_dot u
    +delta_N [
      (27/2) H^2 R^2
      +18 H R R_dot
      +3 R_dot^2
    ]
  }.
```

This is the part sampled by `J2_origin`.

## 3. Nonlinear constraint density

The previously missing gravity/aether dressing density is

```text
L3,nonlinear =
  (C_14/2)(R-delta_N)(D delta_N)^2

  +(2 M_cos^2-D_123)(R+delta_N) B^2/4
  +(3 D_123-2 M_cos^2)(R+delta_N) B_ij B_ij/4

  -D_123 B u
  +(3 D_123-2 M_cos^2) W

  -2 H M_cos^2 R delta_N B
  +2 H M_cos^2 delta_N^2 B
  -2 M_cos^2 R_dot delta_N B
  -2 H M_cos^2 delta_N u

  -9 H^2 M_cos^2 R delta_N^2
  +3 H^2 M_cos^2 delta_N^3
  -6 H M_cos^2 R_dot delta_N^2.
```

Every term has constraint degree two or three. Consequently it vanishes from
the derivative at the constraint origin but contributes to

```text
S2 = partial_z L3[x,z] evaluated at z=z1.
```

## 4. Lapse dressing operator

Let `n1=delta_N1`. Define the algebraic derivative of the nonlinear density
at the first-order solution:

```text
A_N =
  -C_14 (D n1)^2/2
  +(2 M_cos^2-D_123) B1^2/4
  +(3 D_123-2 M_cos^2) B1_ij B1_ij/4

  -2 H M_cos^2 R B1
  +4 H M_cos^2 n1 B1
  -2 M_cos^2 R_dot B1
  -2 H M_cos^2 u1

  -18 H^2 M_cos^2 R n1
  +9 H^2 M_cos^2 n1^2
  -12 H M_cos^2 R_dot n1.
```

The full gravity/aether lapse correction is

```text
Delta S2_N =
  A_N
  -D_i[C_14 (R-n1) D_i n1].
```

The second term is the functional derivative of the aether acceleration
operator and cannot be recovered from an algebraic origin-linear source.

## 5. Scalar-shift dressing operator

At `z1`, define

```text
f_B =
  (2 M_cos^2-D_123)(R+n1) B1/2
  -D_123 u1
  -2 H M_cos^2 R n1
  +2 H M_cos^2 n1^2
  -2 M_cos^2 R_dot n1,

f_B2 =
  (3 D_123-2 M_cos^2)(R+n1)/4,

f_u =
  -D_123 B1 - 2 H M_cos^2 n1,

f_W =
  3 D_123 - 2 M_cos^2.
```

The beta-source correction is the Euler derivative

```text
Delta S2_beta =
  D^2 f_B

  +D_iD_j [
    2 f_B2 B1_ij
    +f_W D_(i R D_j) beta1
  ]

  -D_i [
    f_u D_iR
    +f_W B1_ji D_jR
  ].
```

For the finite-`q` normalized shift,

```text
Sigma = -D^2 beta,
```

the source is

```text
Delta S2_Sigma =
  -(D^2)^(-1) Delta S2_beta.
```

The inverse Laplacian is defined only in the finite-`q` constraint sector.
This calculation does not alter the homogeneous time-translation gauge orbit.

## 6. Regressions

Under the soft-channel substitutions

```text
B = -Sigma,
B_ij B_ij = Sigma^2,
u = 0,
W = 0,
(D delta_N)^2 = 0,
```

the generic calculation reproduces exactly:

- the preceding quadratic soft-channel action;
- the complete cubic soft-channel action;
- the nonlinear `S2_N` correction;
- the nonlinear `S2_Sigma` correction.

## 7. Boundary

Derived:

- generic three-dimensional gravity/aether cubic constraint density;
- exact origin-linear/nonlinear constraint-degree decomposition;
- generic lapse functional dressing operator at `z1`;
- generic scalar-shift functional dressing operator at `z1`.

Still open:

- condensate temporal shift-advection dressing;
- Track-A force shift-advection dressing;
- combined complete finite-`q` `S2`;
- regular physical-scalar projection and amplitude.

## 8. Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_generic_shift_kernel.py
```

Expected footer:

```text
Generic 3D gravity/aether cubic constraint density: VERIFIED
Nonlinear lapse dressing operator at z1: VERIFIED
Nonlinear scalar-shift dressing operator at z1: VERIFIED
Regression to soft-curvature shift channel: VERIFIED
Matter/force shift advection: NOT_YET_DERIVED
Complete finite-q S2: NOT_YET_DERIVED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_GENERIC_GRAVITY_AETHER_SHIFT_DRESSING_KERNEL
```

Machine-readable output:

```text
Analysis/UVIR/UVIR-003/outputs/
  uvir003_generic_shift_kernel_summary.json
```
