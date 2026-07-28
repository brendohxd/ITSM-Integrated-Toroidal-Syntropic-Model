# Core Recovery manuscript changelog

This changelog applies only to the v12 core-recovery manuscript. The repository
root `CHANGELOG.md` records legacy project history.

## Unreleased

### Added

- Added the complete constraint-free direct cubic and quartic physical-field
  contact blocks `L3[x,0]` and `L4[x,0]` for the fixed
  `gravity+aether+condensate+alignment+Track-A force` action.
- Added symbolic regressions for the gravity, condensate/alignment and Track-A
  force components.
- Added the verified finite-`q` soft-curvature scalar-shift dressing sub-block
  and explicit nonlinear corrections to both components of `S2`.
- Added the condensate temporal lapse/shift-advection dressing, the Track-A
  affine-constraint audit, and the complete multi-sector finite-`q` `S2`
  functional.
- Added the corrected quartic Schur functional
  `-S2^T C^(-1)S2/2`.
- Added the complete generic `L4[x,z1]` contact functional and assembled the
  full reduced quartic functional before physical-mode projection.
- Added the regular finite-`q` physical-scalar basis and leg-wise interaction
  projection map.
- Added the generic three-dimensional gravity/aether lapse/shift dressing
  kernel and its functional source operators at `z1`.

### Corrected

- Reclassified the alpha.4 finite-`q` `J2` result as the verified
  origin-linear constraint component rather than the complete second-order
  source. The correct source is `S2=partial_z L3[x,z1]`.
- Reclassified `-J2^T C^(-1)J2/2` as a provisional origin-linear Schur
  component pending the complete finite-`q` constraint dressing.
- Updated and rebuilt the working manuscript with the corrected dressed
  source, complete quartic functional, and regular physical-basis boundary.

### Status boundary

- The complete finite-`q` `S2`, generic `L4[x,z1]`, reduced quartic
  functional and regular physical-scalar basis are verified at `q_phys>0`.
- Explicit projection of the momentum-space vertices, the
  exchange-plus-contact amplitude and cutoff remain open. This checkpoint
  does not create a new manuscript version.

## 12.0-alpha.4 - 2026-07-29

### Added

- Added the bounded force-completion option audit, including the covariant
  rest-space Laplacian identities and symbolic smoothing expansions.
- Added the Track-A force ADM expansion through direct quartic order and the
  verified force-sector lapse/shift `J2` component.
- Added the finite-`q` multi-sector origin-linear `J2` derivation, initially
  labelled as complete, including exact regression to the previous linear
  constraint source.
- Added the corresponding algebraic Schur component
  `-J2_origin^T C^(-1)J2_origin/2`.

### Changed

- Refined the force-sector hold into an explicit architecture choice between
  preserving the exact `Y^(3/2)` branch on a nonzero-gradient local background
  and adopting a smooth homogeneous completion with a new crossover scale.
- Selected Track A: adopted the rest-space Laplacian for derivation, retained
  exact `Y^(3/2)` and assigned its perturbative force test to a declared local
  nonzero-gradient background.
- Replaced the complete-`J2` hold with the next bounded requirement: derive
  the direct multi-sector cubic and quartic contact actions and project them
  onto the regular physical-scalar basis.

### Status boundary

- At release time, the finite-`q` source and Schur block were recorded as complete; this interpretation is corrected under `Unreleased`.
- The direct quartic contact action, physical `2-to-2` amplitude, cutoff,
  nonzero-gradient exact-`Y` reduction and MAT-001 remain open.

## 12.0-alpha.3 - 2026-07-26

### Added

- Added the aether-unitary scalar ADM principal-symbol reduction.
- Added the finite-wavenumber condensate kinetic determinant and the
  associated `q_ADM` validity scale.
- Added the complete time-dependent quadratic finite-`q` scalar constraint
  reduction and compact eigenvalue scan.
- Added the exact `q_phys^2` low-wavenumber kinetic-determinant factor and the
  resulting cubic-normalization hold point.
- Added the exact homogeneous time-translation null identity, gauge-invariant
  `q=0` scalar basis and representative positivity scan.
- Added the bounded longitudinal Stueckelberg quadratic and cubic aether
  vertex basis with an explicit no-cutoff claim boundary.
- Added the complete three-dimensional flat-decoupling khronon cubic operator
  basis, its collinear cross-check and the cubic constraint-order identity.
- Added an operator-basis NDA diagnostic and the on-shell three-point
  kinematic obstruction, without promoting either to a physical cutoff.
- Added the complete three-dimensional flat-decoupling quartic khronon basis,
  with 96 expanded monomials and an independent longitudinal reduction.
- Added the exact elastic contact angular form, exact vanishing of the elastic
  `t/u` cubic exchange vertices and the homogeneous `s`-channel gauge hold.
- Added the quartic constraint-order identity: the second-order constraint
  source enters through a Schur complement, while third-order solutions cancel.
- Added nonlinear ADM action provenance for the exact
  `gravity+aether+condensate+alignment` parent block.
- Added the force-sector completion hold: the evolving-frame `Delta_U`
  completion and a perturbative rule for non-analytic `Y^(3/2)` at `Y=0`
  are required before the full cosmological `J2` can be claimed.

### Changed

- Advanced UVIR-003 from “scalar ADM ready to begin” to “subhorizon principal
  block reduced,” while keeping the full time-dependent low-wavenumber system
  open.
- Recorded the representative spin-0 superluminality as a multicone causality
  flag rather than classifying it as either a local instability or a completed
  causal theory.
- Advanced the working manuscript from a principal-only scalar result to
  finite-`q` constraint elimination with positive representative kinetic
  inertia.
- Resolved the strict `q=0` rank-loss hold as a homogeneous gauge orbit while
  keeping nonlinear weak coupling and the physical interaction scale open.
- Replaced the planned canonical normalization of the collapsing eigenvector
  with the correct gauge-invariant nonlinear task.
- Corrected the cubic constraint workflow: first-order lapse and shift
  solutions suffice because explicit second-order corrections cancel at cubic
  order.
- Replaced a cubic three-point cutoff target with the invariant constrained
  `2-to-2` exchange-plus-quartic-contact amplitude required next.
- Refined that target after the flat quartic audit: the contact term is finite,
  elastic `t/u` exchange vanishes, and the `s` channel requires the full
  gauge-regular constrained cosmological scalar system.
- Replaced immediate full-`J2` expansion with the prior action-completion
  subgate required to make that source and its quartic Schur complement
  well-defined.

### Status boundary

- This release advances nonlinear scalar readiness but does not close
  UVIR-003.
- The full force-sector action, cosmological `J2`, physical `2-to-2` amplitude,
  unitarity cutoff and MAT-001 remain open.

## 12.0-alpha.2 - 2026-07-26

### Added

- Added the scalar-sector ADM-readiness audit.
- Added the background-completion candidate screen.
- Derived the homogeneous/isotropic FRW minisuperspace equations and verified
  a representative on-shell expanding branch.
- Added the new UVIR-003 reports, diagnostics, and manuscript references needed
  to trace those results.

### Changed

- Corrected the frame-sector speed normalization and regenerated its summary.
- Updated the UV/IR hierarchy, exchange law, cosmological status, open gates,
  and reference sections to reflect the new results.
- Separated the background-existence result from the still-open scalar
  perturbation ADM reduction.

### Status boundary

- This release closes only the representative background-existence subproblem.
- Scalar perturbation stability, full cosmological viability, and observational
  acceptance remain open.

## 12.0-alpha.1 - 2026-07-26

### Baseline

- Froze the corrected v12 core architecture at Git commit `c836172`.
- Included the zero-gradient scalar force-block factorization.
- Retained the conditional weak-field limit and explicit open-gate structure.

### Status boundary

- The manuscript remains a research-stage reconstruction, not a completed
  alternative cosmology.
