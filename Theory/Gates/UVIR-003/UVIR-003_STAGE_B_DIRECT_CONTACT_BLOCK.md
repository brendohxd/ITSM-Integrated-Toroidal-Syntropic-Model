# UVIR-003 Stage B direct physical-field contact block

Date: 2026-07-29
Branch: `recovery/v12-core-architecture`
Scope: constraint-free component of the cosmological cubic/quartic action

## Decision

The complete direct physical-field contact blocks

```text
L3[x,0], L4[x,0],
x = (R, delta_rho, vartheta, pi),
```

have been derived from the fixed nonlinear

```text
gravity + Einstein-aether + condensate + alignment + Track-A force
```

action. The result is

```text
PASS_X_ONLY_DIRECT_CONTACT_BLOCK.
```

This is a component of the constrained vertices, not the completed
cosmological interaction action. The latter requires

```text
z1 = -C^(-1)J1,
S2 = partial_z L3[x,z1],

L3[x,z1],
L4[x,z1] - S2^T C^(-1) S2/2.
```

Only the origin-linear Schur component is verified at the preceding
checkpoint. The complete dressed source and constraint-dressed blocks remain

## 1. Conventions

Use aether-unitary scalar gauge and set the constraints to their background
values only for this component:

```text
delta_N = 0,
beta = 0.
```

All displayed densities are divided by the unperturbed physical FRW volume
`a^3`. `D_i` is the physical derivative on the unperturbed leaf.

Up to a spatial boundary term, the conformal-curvature identity is

```text
integral sqrt(h) M_P^2 R3/2
  = integral a^3 M_P^2 exp(R) D_i R D_i R.
```

## 2. Condensate building blocks

Define

```text
B0 = (rho_dot^2 + rho^2 mu^2)/2 - V,

B1 = rho_dot delta_rho_dot
   + rho mu^2 delta_rho
   + rho^2 mu vartheta_dot
   - V_rho delta_rho,

B2 = delta_rho_dot^2/2
   + mu^2 delta_rho^2/2
   + 2 rho mu delta_rho vartheta_dot
   + rho^2 vartheta_dot^2/2
   - V_rhorho delta_rho^2/2,

B3 = rho delta_rho vartheta_dot^2
   + mu delta_rho^2 vartheta_dot
   - V_rhorhorho delta_rho^3/6,

B4 = delta_rho^2 vartheta_dot^2/2
   - V_rhorhorhorho delta_rho^4/24.
```

For the phase-gradient stiffness

```text
F(rho) = rho^2 (1 + zeta_align rho^2),
```

the required background derivatives are

```text
F0 = rho^2 (1 + zeta_align rho^2),
F1 = 2 rho + 4 zeta_align rho^3,
F2 = 2 + 12 zeta_align rho^2.
```

## 3. Gravity contact terms

The direct gravity/aether physical-field blocks are

```text
L3_g[x,0] =
  M_P^2 R (D R)^2
  - 3 M_cos^2 [
      3 R R_dot^2
      + 9 H R^2 R_dot
      + (9/2) H^2 R^3
    ],

L4_g[x,0] =
  M_P^2 R^2 (D R)^2/2
  - 3 M_cos^2 [
      (9/2) R^2 R_dot^2
      + 9 H R^3 R_dot
      + (27/8) H^2 R^4
    ].
```

The aether acceleration operator begins quadratically in the lapse and
therefore has no contribution to the `x-only` block. It remains present in the
constraint-dressed calculation.

## 4. Condensate and alignment contact terms

The direct cubic block is

```text
L3_Phi[x,0] =
  B3 + 3 R B2 + (9/2) R^2 B1 + (9/2) R^3 B0
  - 1/2 [
      R {(D delta_rho)^2 + F0 (D vartheta)^2}
      + F1 delta_rho (D vartheta)^2
    ].
```

The direct quartic block is

```text
L4_Phi[x,0] =
  B4 + 3 R B3 + (9/2) R^2 B2
  + (9/2) R^3 B1 + (27/8) R^4 B0
  - 1/2 [
      (R^2/2) {(D delta_rho)^2 + F0 (D vartheta)^2}
      + R F1 delta_rho (D vartheta)^2
      + (F2/2) delta_rho^2 (D vartheta)^2
    ].
```

## 5. Track-A force contact terms

Let

```text
L = D^2 pi,
G = D_i R D_i pi.
```

The analytic part of the direct cubic force block is

```text
L3_force,analytic[x,0] =
  (3/2) K_Q R pi_dot^2
  + gamma R L^2/(2 M_star^2)
  - gamma L G/M_star^2.
```

The exact IR functional is retained alongside it:

```text
L3_force,exactIR[x,0] =
  -A_IR [(D pi)^2]^(3/2).
```

As before, this is a classical `|epsilon|^3` functional and not an ordinary
homogeneous analytic cubic Taylor vertex.

The direct quartic force block is

```text
L4_force[x,0] =
  (9/4) K_Q R^2 pi_dot^2
  - gamma R^2 L^2/(4 M_star^2)
  + gamma R L G/M_star^2
  - gamma G^2/(2 M_star^2).
```

These expressions regress exactly to the constraint-free terms in the
previous Track-A ADM expansion.

## 6. Complete x-only component

The verified component is

```text
L3[x,0] =
  L3_g[x,0] + L3_Phi[x,0] + L3_force[x,0],

L4[x,0] =
  L4_g[x,0] + L4_Phi[x,0] + L4_force[x,0].
```

No interaction scale is inferred from these expressions in isolation.

## 7. What remains

The first-order constraints are

```text
z1 = -C^(-1) J1.
```

The next calculation must retain every cubic and quartic term involving
first-order `delta_N` and `beta`, then form

```text
L3_reduced = L3[x,z1],

L4_reduced =
  L4[x,z1] - S2^T C^(-1) S2/2.
```

Only after these vertices are projected onto the regular physical-scalar basis
can the gauge-regular exchange-plus-contact amplitude be evaluated.

## 8. Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_direct_contact_block.py
```

Expected footer:

```text
Direct gravity cubic/quartic contact block: VERIFIED
Direct condensate/alignment contact block: VERIFIED
Direct Track-A force contact block: VERIFIED
Complete L3[x,0] and L4[x,0]: VERIFIED
Constraint-dressed L4[x,z1]: NOT_YET_DERIVED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_X_ONLY_DIRECT_CONTACT_BLOCK
```

Machine-readable output:

```text
Analysis/UVIR/UVIR-003/outputs/uvir003_direct_contact_block_summary.json
```

## Status

```text
Direct L3[x,0]: VERIFIED
Direct L4[x,0]: VERIFIED
Constraint-dressed L3[x,z1]: NOT_YET_DERIVED
Constraint-dressed L4[x,z1]: NOT_YET_DERIVED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_X_ONLY_DIRECT_CONTACT_BLOCK
```
