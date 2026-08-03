# WAK-001 Stage 2 - Route-II free-field screen

**Date:** 2026-08-03
**Calculation status:** `PASS_WAK001_ROUTE2_FREE_TEMPLATE`
**Gate status:** Open
**Physical wake law:** Not yet derived

## Scope

This screen implements the source-free local preferred-frame quadratic family
selected for calculation in `WAK-001_STAGE2_BOOKKEEPING_ROUTE.md`.

It checks only:

- positive free dispersion at a declared representative toy point;
- non-negative quadratic Hamiltonian samples;
- characteristic speed inside the declared matter cone;
- finite positive static susceptibility for a massive free template; and
- negative controls for zero/negative kinetic coefficient, negative gradient
  coefficient, superluminal declared characteristic and tachyonic mass.

## Reproduction

```powershell
conda run -n itsm_env python Analysis\WAK\WAK-001\wak001_route2_free_field.py
```

Expected status:

```text
PASS_WAK001_ROUTE2_FREE_TEMPLATE
WAK-001 gate: OPEN
Physical wake law: NOT_YET_DERIVED
```

## Verified representative output

For the dimensionless toy point `Z_W=1.2`, `c_W^2=0.36` and `M_W^2=0.8`:

```text
omega_sq(k=0)  = 0.6666666666666667
omega_sq(k=10) = 36.666666666666664
chi_static(k=0)  = 1.25
chi_static(k=10) = 0.022727272727272728
```

All ten checks pass. Five mandatory negative controls reject zero kinetic
coefficient, ghost kinetic sign, negative gradient coefficient, a
characteristic outside the declared matter cone and tachyonic mass.
`physics_pass` remains `false` in the deterministic JSON summary.

## Claim boundary

A pass validates a free mathematical template only. It does not establish:

- the existence of an independent physical wake degree of freedom;
- metric or preferred-frame stress variation;
- a non-duplicated mode relative to `Phi`, `U` and `psi`;
- an interaction-derived source or exchange current;
- a dissipative completion or derivation of `tau_W`;
- any correction to the Conditional AQUAL static baseline; or
- any galaxy, cluster, lensing or anisotropy result.

The calculation must remain source-free until its mode inventory is compared
against the already declared sectors.
