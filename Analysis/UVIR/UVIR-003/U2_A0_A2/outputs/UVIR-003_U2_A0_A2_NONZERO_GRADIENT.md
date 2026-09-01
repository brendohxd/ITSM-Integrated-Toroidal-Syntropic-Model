# UVIR-003 U2 exact nonzero-gradient A0-A2 screen

**Calculation:** `PASS_AUDIT_PIPELINE`  
**Disposition:** `FREEZE_U2_AT_A0_A2_INCOMPLETE_ACTION_DOMAIN_AND_DOF`  
**UVIR-003:** `IN_PROGRESS` · **MAT-001:** `BLOCKED` · **physics pass:** `false`

## Exact result

For `grad(psi_bar)=v e_x`, `v>0`, the exact `Y^(3/2)` expansion independently
reproduces the prior local result. The spatial potential Hessian is

- longitudinal: `6*A_IR*v`;
- transverse: `3*A_IR*v` (twice).

Both are positive for `A_IR>0` and `v>0`. The quartic coefficient is
`3*(y**2 + z**2)**2/(8*v)` and diverges at the zero-gradient boundary.

## A0-A2 disposition

- **A0 — `PASS_BOUNDED_IDENTITY_FIDELITY`:** the route preserves the declared
  separate force sector and does not replace the finite-density condensate.
- **A1 — `HOLD_RESTRICTED_BACKGROUND_ACTION_NOT_FULL_DOMAIN`:** the exact local
  patch exists, but the regulator's general covariant completion, zero-gradient
  join, matched `K_Q`, and physical cutoff do not.
- **A2 — `HOLD_LOCAL_HESSIAN_ONLY_FULL_CONSTRAINT_DOF_UNRESOLVED`:** a positive
  spatial Hessian is not the full coupled constraint/Hamiltonian count.

U2 therefore freezes at A0-A2. The repository has not established that this
patch overlaps the galaxy-force regime below the physical cutoff, and no
parent-gate promotion follows.
