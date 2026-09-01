# UVIR-003 Stage B complete generic L4 contact functional

Date: 2026-07-29
Branch: `recovery/v12-core-architecture`
Scope: generic quartic contact at first-order finite-`q` constraints

## Decision

The complete generic contact functional

```text
L4[x,z1],  z1=-C^(-1)J1,
```

is assembled and verified on the homogeneous zero-gradient Track-A branch.
The result is

```text
PASS_COMPLETE_GENERIC_L4_X_Z1_CONTACT.
```

Together with the verified complete source `S2`, the reduced quartic
functional is now

```text
L4_red =
  L4[x,z1]
  -1/2 integral d^3k S2(-k)^T C(k)^(-1)S2(k).
```

This is a complete functional before physical-mode projection; it is not yet
a physical scattering amplitude or cutoff.

## Sector coverage

The fourth-order expansion retains:

- the generic conformal-ADM gravity/aether shift contractions;
- the aether lapse-gradient operator;
- the lapse-dependent spatial-curvature block;
- condensate temporal shift advection, potential, spatial gradients and
  alignment;
- Track-A `Q^2`, rest-space regulator and the declared zero-gradient
  exact-`Y^(3/2)` rule.

For

```text
T_ij =
  D_iD_j beta-D_iR D_jbeta-D_jR D_ibeta
  +delta_ij D_kR D_kbeta,
```

the quartic contraction includes

```text
T_ij T_ij =
  (D_iD_j beta)^2
  +2[-2(D_iD_j beta)D_iR D_jbeta
     +(D^2 beta)D_iR D_i beta]
  +2(DR)^2(D beta)^2
  +(D_iR D_i beta)^2.
```

## Regressions

The calculation verifies:

- exact regression to the separately derived direct `L4[x,0]`;
- exact regression of the gravity/aether block to the soft-curvature
  `L4[x,z1]`;
- the complete finite-`q` `S2` dependency.

## Boundary

Still open:

- a regular finite-`q` physical scalar eigenmode basis;
- projection of the complete cubic and quartic vertices;
- the gauge-regular exchange-plus-contact `2-to-2` amplitude;
- a declared unitarity criterion and physical cutoff;
- the separate nonzero-gradient exact-`Y` local reduction.

The inverse-Laplacian shift representation remains restricted to
`q_phys>0`; the homogeneous time-translation gauge result is unchanged.
UVIR-003 remains in progress and MAT-001 remains blocked.

## Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_complete_l4_contact.py
```

Expected footer:

```text
Generic gravity/aether L4[x,z1]: VERIFIED
Condensate/alignment L4[x,z1]: VERIFIED
Track-A zero-gradient L4[x,z1]: VERIFIED
Direct and soft-channel regressions: VERIFIED
Complete reduced quartic functional: ASSEMBLED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_COMPLETE_GENERIC_L4_X_Z1_CONTACT
```

Machine-readable output:

```text
Analysis/UVIR/UVIR-003/outputs/uvir003_complete_l4_contact_summary.json
```
