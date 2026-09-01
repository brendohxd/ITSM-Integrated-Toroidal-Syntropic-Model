# UVIR-003 Stage B constraint-dressing completeness audit

Date: 2026-07-29
Branch: `recovery/v12-core-architecture`
Scope: second-order lapse/scalar-shift source used at quartic order

## Decision

The previously derived finite-`q` source is verified as the coefficient
linear in the constraints at the origin,

```text
J2_origin = partial_z L3[x,z] evaluated at z=0.
```

It is not, by itself, the complete second-order source after the first-order
constraint solution is inserted. The correct source is

```text
z1 = -C^(-1) J1,
S2 = partial_z L3[x,z] evaluated at z=z1.
```

The earlier algebraic Schur expression remains a verified
origin-linear component, but its interpretation as the complete quartic
constraint block is reclassified:

```text
PASS_CONSTRAINT_DRESSING_COMPLETENESS_AUDIT
PREVIOUS_SCHUR: PROVISIONAL_ORIGIN_LINEAR_COMPONENT
FULL_FINITE_Q_S2: NOT_YET_DERIVED
```

## 1. Why the distinction matters

Write the perturbative constraint solution as

```text
z = epsilon z1 + epsilon^2 z2 + ...
```

and the action as

```text
L = L2 + L3 + L4 + ...
```

The first-order equation is

```text
C z1 + J1 = 0.
```

At the next order, the source multiplying `z2` is not generally the
coefficient of `z` at the origin. It is

```text
S2 = partial_z L3[x,z1].
```

Eliminating `z2` therefore gives

```text
L3_red = L3[x,z1],

L4_red =
  L4[x,z1] - (1/2) S2^T C^(-1) S2.
```

The replacement `S2 -> J2_origin` is valid only if `L3` is affine in the
constraints. The exact ADM lapse action is not affine.

## 2. Exact homogeneous lapse counterexample

For the homogeneous gravity-plus-condensate block, define

```text
B(epsilon) =
  exp(3 epsilon R) [
    -3 M_cos^2 (H + epsilon R_dot)^2
    + (rho_dot + epsilon delta_rho_dot)^2/2
    + (rho + epsilon delta_rho)^2
      (mu + epsilon vartheta_dot)^2/2
  ],

P(epsilon) =
  exp(3 epsilon R) V(rho + epsilon delta_rho),

B = sum_n epsilon^n Bn,
P = sum_n epsilon^n Pn.
```

The exact lapse-dependent density is

```text
L = B(epsilon)/(1 + epsilon delta_N)
    - (1 + epsilon delta_N) P(epsilon).
```

Its cubic coefficient is

```text
L3 =
  B3 - P3
  - delta_N (B2 + P2)
  + delta_N^2 B1
  - delta_N^3 B0.
```

On the Friedmann background, `B0=-V`. Thus

```text
J2_N,origin = -(B2 + P2),

S2_N =
  J2_N,origin
  + 2 B1 delta_N1
  + 3 V delta_N1^2.
```

The last two terms are generically nonzero. This is an explicit exact
counterexample to treating the origin-linear coefficient as the full
second-order constraint source.

## 3. Quartic first-order lapse dressing

The quartic coefficient is

```text
L4 =
  B4 - P4
  - delta_N (B3 + P3)
  + delta_N^2 B2
  - delta_N^3 B1
  + delta_N^4 B0.
```

Therefore `L4[x,delta_N1]` contains additional terms beyond the previously
verified direct block `L4[x,0]`. On shell,

```text
L4[x,delta_N1] - L4[x,0] =
  -delta_N1 (B3 + P3)
  + delta_N1^2 B2
  - delta_N1^3 B1
  - V delta_N1^4.
```

The finite-`q` scalar-shift analogues must still be derived from the full ADM
action before the constrained quartic action can be called complete.

## 4. Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_constraint_dressing_audit.py
```

Expected footer:

```text
Exact homogeneous lapse L2/L3/L4 dressing: VERIFIED
Origin-linear J2 as a component: VERIFIED
Origin-linear J2 as complete S2: REJECTED
Correct source S2=partial_z L3[x,z1]: VERIFIED
Previous quartic Schur: RECLASSIFIED_PROVISIONAL_ORIGIN_LINEAR_COMPONENT
Complete finite-q S2: NOT_YET_DERIVED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_CONSTRAINT_DRESSING_COMPLETENESS_AUDIT
```

Machine-readable output:

```text
Analysis/UVIR/UVIR-003/outputs/
  uvir003_constraint_dressing_audit_summary.json
```

## Status

```text
Origin-linear J2 component: VERIFIED
Complete finite-q S2: NOT_YET_DERIVED
Direct L3[x,0] and L4[x,0]: VERIFIED
Constraint-dressed L3[x,z1]: NOT_YET_DERIVED
Constraint-dressed L4[x,z1]: NOT_YET_DERIVED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_CONSTRAINT_DRESSING_COMPLETENESS_AUDIT
```
