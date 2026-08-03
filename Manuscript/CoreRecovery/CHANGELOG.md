# Core Recovery manuscript changelog

This changelog applies only to the v12 core-recovery manuscript. The repository
root `CHANGELOG.md` records legacy project history.

## Unreleased

### Parallel identity-gate checkpoint

- Added bounded post-alpha.10 gate records for TOP-001 full-triaxial
  fixed-volume geometry, VOR-001 finite-density/smooth-winding energy, and
  WAK-001 constrained Route-II preparation.
- All results remain mathematical-template or Conditional inputs with
  `physics_pass: false`; TOP/VOR remain `OPEN_SCAFFOLD_ONLY` and WAK remains
  Open under microscopic-identity and cubic-constraint holds.
- No working manuscript equations or frozen release were changed by this
  checkpoint. A future alpha.11 may incorporate the results only after a
  dedicated manuscript integration and review.

### Corrected

- Hardened the post-alpha.10 M2 audit so missing IR-HOLD evidence or missing
  quantitative-domain support fails rather than silently passing.
- Limited M2 `PASS_BOUNDED` to the recorded analytic and discrete sampled
  support; no continuous-neighbourhood or dynamical no-leakage theorem is
  claimed.
- Clarified the serial dependency: Stage 3 may become a scoped Conditional MAT
  calculation only after a written Stage-2 handoff. MAT gate PASS and
  downstream Derived use remain blocked until UVIR Stage 5.

These changes are **not yet a frozen manuscript release**. The next freeze is alpha.11.

## 12.0-alpha.10 - 2026-08-03

### Added

- Recorded the post--alpha.9 UVIR-003 working subgate chain in the open-gates
  narrative: FRW in-in path declaration, multi-slice mode-projected Green,
  Track-A nonzero-gradient $|\nabla\pi|^3$ local expansion, declared scoped
  unitarity/EFT criterion, and $K_Q$ matching inventory (invariants + routes).
- Clarified that these subgates do not establish an S-matrix, optical theorem,
  matched physical cutoff, or numeric $K_Q$, and that MAT-001 remains blocked.

### Status boundary

- Checkpoint label: post--alpha.9 UVIR-003 path package (not full UVIR-003 PASS).
- Subgate tags include (non-exhaustive):
  `PASS_FRW_IN_IN_OBSERVABLE_PATH_DECLARED`,
  `PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN`,
  `PASS_NONZERO_GRADIENT_FORCE_LOCAL`,
  `PASS_DECLARED_UNITARITY_EFT_CRITERION`,
  `PASS_KQ_MATCHING_INVENTORY_OPEN`.
- Full UVIR-003 gate and MAT-001 remain open / blocked respectively.

## 12.0-alpha.9 - 2026-07-30

### Added

- Added a regular-tetrahedral elastic four-leg slice with strictly nonzero
  and independently admitted `s`, `t`, and `u` internal trajectories.
- Added matched left/right cubic pair-source contractions through the full
  physical finite-`q` propagator.
- Added the analytic quartic contact and all three constraint-induced Schur
  pairings in the same polarization and residue-normalization convention.
- Added component-level permutation, pole-separation, inverse-closure and
  cancellation diagnostics over 24 mode-pair cases and 72 channels.

### Status boundary

- Record
  `PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL`.
- The local frozen-time analytic four-leg kernel is assembled on the tested
  slice. A cosmological S-matrix normalization, unitarity bound,
  strong-coupling scale and physical cutoff are not established.
- The combined kernel can be as small as `0.502%` of the sum of absolute
  component magnitudes. This resolved cancellation remains a sensitivity,
  not a derived suppression scale.

## 12.0-alpha.8 - 2026-07-29

### Added

- Added residue-normalized local coupled modes using the positive-pole
  derivative of the finite-`q` inverse kernel.
- Added the physical cubic pair-source contraction with two on-shell external
  legs and one off-shell channel covector.
- Added sum- and difference-frequency channel prescriptions over 48 admitted
  equilateral mode/sign cases.
- Added nonzero-channel inverse-kernel response, pole-separation, constraint
  margin and external-leg permutation audits.

### Clarified

- Clarified that two coupled external legs produce no factorized `Pi` source
  in the verified analytic cubic kernel. This does not remove `Pi` from the
  theory or resolve the held nonanalytic local-gradient vertex.

### Status boundary

- Record `PASS_MODE_PROJECTED_CUBIC_PAIR_SOURCE`.
- Matched left/right source contraction, channel summation, reduced quartic
  contact, the physical amplitude and any unitarity scale remain unfinished.

## 12.0-alpha.7 - 2026-07-29

### Added

- Added the controlled fixed-comoving exchange-domain map with explicit
  real-pole, positive-kinetic, subhorizon, coupled-mode adiabaticity and
  factorized-force adiabaticity criteria.
- Added tracked high-momentum phase-space eigenspace projectors and the rule
  that every nonzero internal channel must independently pass the same domain
  gate.

### Corrected

- Removed the attempted use of the infrared `Xi`-pure
  `gauge_continuation_Xi` initialization rule at high momentum. The controlled
  domain tracks all three coupled finite-`q` physical pairs without assigning
  that infrared label.

### Status boundary

- Initial `q/H=47.5,50,75,100` passes on the representative branch; `45`
  fails the `0.1` adiabatic threshold. This sampled bracket is not a continuous
  or all-background boundary.
- Physical vertex contraction, exchange-plus-contact amplitude, unitarity
  bound, strong-coupling scale and physical cutoff remain unfinished.

## 12.0-alpha.6 - 2026-07-29

### Added

- Added the gauge-projected source-to-observable retarded-response audit in
  retained `(Q_rho,Q_chi)`.
- Added exact checks that the original-field source covectors annihilate the
  homogeneous time-translation orbit.
- Added source/readout support, impulse/readout structure, orthonormality, and
  coarse/fine response diagnostics.
- Added every-source-time response summaries and the maximizing response
  traces across five reference, nearby on-shell-background, and alignment
  cases.

### Clarified

- Clarified that the complete finite-`q` physical basis still includes the
  Track-A force mode `Pi`. It factorizes exactly at quadratic order and is
  outside the coupled complex-quartet mixing block rather than omitted from
  the ITSM framework.
- Replaced the pending source-projected-response wording in the recovery
  records and manuscript with the completed bounded result.

### Status boundary

- All five tested cases retain amplified through-quartet response in
  `(Q_rho,Q_chi)` after direct `Xi` and homogeneous time-translation source
  support are removed. Record
  `PASS_GAUGE_PROJECTED_MATTER_RESPONSE_SURVIVES_WITH_SCOPE`.
- This resolves the direct gauge-source attribution question only for the
  tested finite-duration dimensionless neighborhood. It is not an
  all-background instability theorem, physical fit, S-matrix amplitude,
  unitarity result, strong-coupling scale, or physical cutoff.
- A controlled real-pole adiabatic exchange domain, physical interaction

## 12.0-alpha.5 - 2026-07-29

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
- Added the complete analytic cubic Fourier polarization, exact per-leg
  finite-`q` constraint resolvers, and factorized physical-basis kernel.
- Added the factorized reduced quartic momentum kernel, complete physical
  pair-source kernel, three finite-channel Schur pairings, and exact
  homogeneous constraint/physical projectors.
- Added the finite-`q` physical inverse quadratic kernel, factorized force
  propagator, and separate exact-`q=0` projected response kernel, together
  with pole, residue, inverse-closure, and kinetic-inertia diagnostics.
- Added the generic three-dimensional gravity/aether lapse/shift dressing
  kernel and its functional source operators at `z1`.
- Added fixed-comoving pole tracking, adiabaticity measures, and converged
  kinetic-normalized time-domain transfer matrices with an independent
  canonical-Hamiltonian equivalence check.
- Added kinetic-normalized pole-pair frames, principal-angle assignment,
  Procrustes parallel transport, and a five-case on-shell
  background/alignment robustness audit.

### Corrected

- Reclassified the alpha.4 finite-`q` `J2` result as the verified
  origin-linear constraint component rather than the complete second-order
  source. The correct source is `S2=partial_z L3[x,z1]`.
- Reclassified `-J2^T C^(-1)J2/2` as a provisional origin-linear Schur
  component pending the complete finite-`q` constraint dressing.
- Updated and rebuilt the working manuscript with the corrected dressed source,
  cubic and reduced-quartic momentum kernels, the exact homogeneous
  internal-channel projector boundary, local propagator HOLD, and the
  follow-on fixed-comoving and complex-quartet mode-attribution HOLDs from
  the converged time-domain transfer.

### Status boundary

- The complete finite-`q` `S2`, generic `L4[x,z1]`, regular physical-scalar
  basis, factorized analytic cubic kernel, and factorized reduced quartic
  momentum kernel are verified for their declared nonzero-momentum domains.
- Exact homogeneous constraint and physical projectors are defined and
  algebraically audited; they are not a naive finite-`q` substitution.
- Local physical quadratic propagators are constructed. The high-`q`
  representative subset has real positive-frequency poles with positive
  residues. The required fixed-comoving transfer audit is now numerically
  converged and shows that frozen-pole exponentiation is invalid in the
  nonadiabatic domain.
- The initial `q_phys/H=0.01` trajectory retains a converged maximum
  kinetic-normalized phase-space gain of `1.37708e27`. The five-case
  follow-on finds an `Xi`-seeded dominant input in every case, but every
  trajectory enters an off-axis complex quartet that prevents a unique real
  rank-two gauge/matter pole split. Matter-seeded subspaces also amplify. The
  result is `HOLD_COMPLEX_QUARTET_IR_MODE_ATTRIBUTION`, not an instability
  finding or pure gauge-artifact dismissal.
- The exact `|grad(pi)|^3` Taylor kernel at zero gradient, local adiabatic
  source-projected retained-observable response, exchange-plus-reduced-contact
  amplitude, unitarity criterion, and cutoff remain open. This checkpoint
  is frozen as manuscript release `v12.0-alpha.5`.

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

- At release time, the finite-`q` source and Schur block were recorded as complete; this interpretation is corrected in `v12.0-alpha.5`.
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
