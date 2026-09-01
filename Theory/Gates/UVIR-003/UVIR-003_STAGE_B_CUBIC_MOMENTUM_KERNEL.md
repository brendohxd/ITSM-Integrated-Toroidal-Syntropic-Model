# UVIR-003 Stage B factorized cubic momentum kernel

Date: 2026-07-29
Branch: `recovery/v12-core-architecture`
Scope: complete analytic cubic kernel at finite nonzero momentum

## Decision

The complete analytic cubic functional is now polarized over three Fourier
legs, resolved with the verified first-order constraints on each leg, and
mapped to the regular physical variables

```text
(Xi, Q_rho, Q_chi, Pi).
```

The result is

```text
PASS_FACTORIZED_FINITE_Q_PHYSICAL_CUBIC_KERNEL.
```

The representation is deliberately factorized: the symmetric trilinear
kernel retains named `delta_N_1_i` and `Sigma_1_i` entries, with exact
per-leg resolvers supplied alongside it. This is algebraically complete and
avoids flattening repeated rational constraint denominators into an
impractically large expression.

## Fourier construction

For `k1+k2+k3=0`,

```text
D_i -> i k_i,
k1.k2 = (q3^2-q1^2-q2^2)/2,
k1.k3 = (q2^2-q1^2-q3^2)/2,
k2.k3 = (q1^2-q2^2-q3^2)/2.
```

Each nonzero-momentum leg uses

```text
z1_i = -C(q_i)^(-1) J1_i,
Sigma_1_i = -D^2 beta_1_i,
beta_1_i = Sigma_1_i/q_i^2.
```

The script implements all derivative polarizations explicitly, including
the non-collinear Hessian contraction

```text
(D_iD_j beta)(D_i R)(D_j beta).
```

The coefficient is extracted by differentiating once with respect to each
of three auxiliary leg amplitudes and setting those amplitudes to zero. This
avoids a global polynomial expansion while returning the same symmetric
trilinear coefficient.

## Physical projection

The full time-dependent map is applied leg by leg:

```text
R_i = H Xi_i/q_i,
delta_rho_i = Q_rho_i + rho_dot Xi_i/q_i,
vartheta_i = Q_chi_i/rho + mu Xi_i/q_i.
```

Velocity substitutions include `dot(T)` and use

```text
q_dot_i = -H q_i
```

for fixed comoving momentum. The output supplies both the factorized physical
kernel and the lapse/shear resolvers already expressed in the physical basis.

## Boundaries

Two obstructions remain explicit.

1. The exact Track-A term

   ```text
   -A_IR |grad(pi)|^3
   ```

   is nonanalytic at the homogeneous zero-gradient background. It has no
   ordinary trilinear Taylor kernel there and remains assigned to a declared
   local nonzero-gradient analysis.

2. The exactly homogeneous `Xi` mode is the verified time-translation gauge
   orbit. The finite-`q` physical map cannot be continued by simply setting an
   internal spatial momentum to zero. In particular, this checkpoint does
   not supply a naive centre-of-mass `s`-channel exchange prescription.

Therefore no exchange-plus-contact amplitude, unitarity bound, strong-coupling
scale, or physical cutoff is claimed. UVIR-003 remains in progress and
MAT-001 remains blocked.

## Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_complete_l4_contact.py
python Analysis/UVIR/UVIR-003/uvir003_cubic_momentum_kernel.py
```

Expected second-command footer:

```text
Complete analytic cubic polarization: VERIFIED
Finite-q constraint resolvers: EXPLICIT_PER_LEG
Physical-basis cubic kernel: DERIVED_FACTORIZED
Exact |grad(pi)|^3 Taylor kernel: NONANALYTIC_AT_ZERO_GRADIENT
Homogeneous internal Xi channel: NOT_DEFINED_BY_FINITE_Q_MAP
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_FACTORIZED_FINITE_Q_PHYSICAL_CUBIC_KERNEL
```

Machine-readable output:

```text
Analysis/UVIR/UVIR-003/outputs/uvir003_cubic_momentum_kernel_summary.json
```
