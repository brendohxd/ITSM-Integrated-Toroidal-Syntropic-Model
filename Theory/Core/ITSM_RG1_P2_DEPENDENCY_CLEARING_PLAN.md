# ITSM RG1-to-P2 dependency-clearing plan

**Date:** 2026-08-25  
**Branch:** `recovery/v12-core-architecture`  
**Status:** `COMPLETED_FAIL_CLOSED_REVIEW_CHECKPOINT`

## Binding baseline

- UVIR-003: `IN_PROGRESS`, `HOLD_TIER1_CLOSURE`, `physics_pass=false`.
- MAT-001: `BLOCKED`; `V NOT_COMPUTED`; `K_Q NOT_DERIVED`.
- U1: frozen for uncontrolled linear response on the declared representative
  dimensionless background.
- M4: generic invariant projection control passes; the live same-chart residue
  remains blocked.
- No local-gravity, lensing, DISK, STAT, cosmology or publication gate opens
  from this plan alone.

## Package 1 — M2 radial/heavy-mode reduction

1. Freeze the actual condensate amplitude action and the currently declared
   matter interaction provenance.
2. Introduce no empirical target. If a candidate matter-amplitude interaction
   is tested, name it as a new controlled action class and retain every new
   coefficient.
3. Integrate out the radial/heavy mode before taking the soft limit.
4. Calculate the physical pole/contact structure, dimensions, sign, range,
   and `g_phys/sqrt(Z_phys)` after normalization.
5. Reject the tested route if the static source is absent, the long-range pole
   is absent, or the soft residue remains an independent Wilson combination.

## Package 2 — U2 exact nonzero-gradient A0-A2 screen

1. Use the exact `Y^(3/2)` operator on a declared nonzero-gradient background.
2. Freeze sign, Fourier, background-direction and field conventions.
3. Test A0 identity, A1 covariant action/domain and A2 symmetry/DOF without
   replacing the operator by a smoothing polynomial.
4. Derive the anisotropic spatial Hessian and identify its longitudinal and
   transverse eigenvalues; test the `|grad psi| -> 0` boundary separately.
5. Reject/freeze if the declared action/domain is incomplete, the operator has
   no domain overlapping the force regime, or a ghost/double count appears.

## Package 3 — S0 no-screening control

1. Propagate the unscreened force law, with coefficient left symbolic, to
   Solar-System, laboratory, pulsar and compact-object observables.
2. Separate exact algebraic scaling from PPN or strong-field calculations not
   present in the repository.
3. State the failure domain as inequalities in the unknown coupling; do not
   import a screening mechanism.
4. Treat failure as the null-control result, not as evidence for any S1-S4
   mechanism.

## Package 4 — VOR/TOP S2 winding and moduli

1. Reproduce the winding-modified amplitude extremum and energy from the
   declared finite-density action.
2. Complete the S2-T01--T06 controls and distinguish toy fixed-background
   results from the live evolving UVIR parent.
3. Derive the moduli dependence of winding energy and its Hessian on the
   fixed-volume shape slice; preserve modular/reindexing covariance.
4. Reject any inference of `2*pi`, `2/3`, `13/12`, `L=c/H`, a force coupling,
   or a cosmological attractor from the scoped calculation.

## Review checkpoint

For each package produce executable source, deterministic JSON/CSV where
applicable, a report, SHA-256 seals, negative controls and a fail-closed
disposition. The checkpoint may select, repair, freeze or reject routes. It
cannot promote a parent gate unless that gate's complete A0-A10 checklist is
independently satisfied.

Commit, push, deployment, publication, Notion synchronization, and changes to
immutable releases remain outside this plan.

## Review-checkpoint result (2026-08-25)

| Package | Reproducible disposition | Parent effect |
|---|---|---|
| M2 radial/heavy mode | `REJECT_MINIMAL_M2_CLASSES_SOFT_RESIDUE_NOT_DERIVED` | MAT-001 remains `BLOCKED`; `V NOT_COMPUTED` |
| U2 exact nonzero gradient | `FREEZE_U2_AT_A0_A2_INCOMPLETE_ACTION_DOMAIN_AND_DOF` | UVIR-003 remains `IN_PROGRESS`; `K_Q NOT_DERIVED` |
| S0 no screening | `REJECT_S0_AS_COMPLETE_LOCAL_GRAVITY_ROUTE` | SCR/local-gravity stages are not opened |
| VOR/TOP S2 | `REPAIR_VOR_S2_AND_REJECT_WINDING_ONLY_GENERIC_MODULI_STABILIZATION` | VOR-001 and TOP-001 remain `OPEN_SCAFFOLD_ONLY` |

The old VOR S2 runner used `lambda=100000` for T02, not the specified
`lambda=100, omega=1` point. The exact preregistered relative deviation is
`1/200 = 0.5%`, so T02 fails its `<0.1%` criterion. On the fixed-volume shape
slice, generic winding does not stabilize the cubic torus; a single-cycle
winding has a runaway toward zero winding energy.

**Checkpoint decision:** `NO_DOWNSTREAM_STAGE_OPENED`. Local gravity, lensing,
disks, SPARC, cosmology and publication remain behind their upstream gates.
