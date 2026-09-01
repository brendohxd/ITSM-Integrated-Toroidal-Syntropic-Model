# UVIR-003 Stage B regular physical-scalar basis

Date: 2026-07-29
Branch: `recovery/v12-core-architecture`
Scope: finite-`q` physical basis and vertex-projection map

## Decision

Define

```text
Xi     = (q_phys/H) R,
Q_rho  = delta_rho - (rho_dot/H) R,
Q_chi  = rho [vartheta - (mu/H) R].
```

The transformed kinetic matrix has a finite, nonzero `q_phys -> 0` limit and
positive inertia throughout the validated representative finite-`q` domain.
The result is

```text
PASS_REGULAR_FINITE_Q_PHYSICAL_SCALAR_BASIS.
```

This does not reinstate an exactly homogeneous `Xi` mode. At `q_phys=0`,
`Xi` is absent and `(Q_rho,Q_chi)` reduce to the previously verified
two-dimensional physical homogeneous block.

## Inverse map

For every external leg with `q_phys>0`,

```text
R         = (H/q_phys) Xi,
delta_rho = Q_rho + (rho_dot/q_phys) Xi,
vartheta  = Q_chi/rho + (mu/q_phys) Xi.
```

The first column is the homogeneous time-translation vector
`(H,rho_dot,mu)` divided by `q_phys`. This converts the verified `q_phys^2`
kinetic collapse into a finite gradient-mode normalization without
canonically normalizing the homogeneous gauge orbit.

## Time-dependent map

For fixed comoving momentum, `q_phys_dot=-H q_phys`. Therefore interaction
projection must use

```text
dot(y) = T dot(p) + dot(T) p,
```

including `H_dot`, `rho_ddot`, `mu_dot`, and `q_phys_dot`. The machine-readable
summary records the complete field and velocity substitution.

## Vertex projection

The leg-wise maps are

```text
V_phys,abc =
  T^i_a(k1) T^j_b(k2) T^k_c(k3) V_ijk,

W_phys,abcd =
  T^i_a(k1) T^j_b(k2) T^k_c(k3) T^l_d(k4) W_ijkl.
```

Each leg carries its own nonzero physical momentum. A homogeneous internal
channel must be treated through the gauge-regular projected kernel; it may not
be inverted as an `Xi` propagator.

## Verification

The audit verifies:

- the exact transformation and inverse;
- a finite symbolic `q_phys -> 0` kinetic matrix;
- the transformed determinant obtained from the on-shell finite-`q`
  determinant;
- positive transformed inertia across 39,249 representative matrices over
  `10^-3 <= q_phys/H <= 10^3`;
- bounded convergence of the smallest transformed eigenvalue over the
  low-`q` scan.

## Boundary

Still open:

- explicit momentum-space cubic kernels;
- leg-wise projection of the complete cubic and quartic interactions;
- the gauge-regular exchange-plus-contact amplitude;
- a declared unitarity criterion and physical cutoff;
- the nonzero-gradient exact-`Y` local reduction.

UVIR-003 remains in progress and MAT-001 remains blocked.

## Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_physical_scalar_basis.py
```

Expected footer:

```text
Finite-q physical scalar basis: VERIFIED
Physical-basis q->0 kinetic limit: FINITE
Representative physical-basis inertia: 3_POSITIVE_0_NEGATIVE
Exactly homogeneous Xi mode: EXCLUDED_AS_GAUGE
Leg-wise cubic/quartic projection map: DEFINED
Projected physical vertices: NOT_YET_EVALUATED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_REGULAR_FINITE_Q_PHYSICAL_SCALAR_BASIS
```

Machine-readable outputs:

```text
Analysis/UVIR/UVIR-003/outputs/uvir003_physical_scalar_basis_summary.json
Analysis/UVIR/UVIR-003/outputs/uvir003_physical_scalar_basis_scan.csv
```
