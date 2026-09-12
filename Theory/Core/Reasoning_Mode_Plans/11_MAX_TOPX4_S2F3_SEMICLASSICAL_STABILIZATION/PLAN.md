# Max plan — TOP-X4 `X4-S2F3` semiclassical stabilization

**Mode:** Max  
**Entry:** `X4-S2F3 FROZEN_FOR_ONE_MAX_RETRY`  
**Exit:** `X4-D2_RETRY PASS_STABLE_DOMAIN`, `HOLD`, or `CLOSED_NEGATIVE`  
**Gate effect:** none

## Objective

Determine whether the frozen three-periodic-Dirac completion produces a
self-consistent finite-charge compactification with a positive physical
radion mass and a nonempty five-dimensional EFT domain.

## Current checkpoint — 2026-09-12

The zero-density static parity-even determinant checkpoint completed `12/12`
bounded calculation checks. The finite-charge entry gate then completed `9/9`
provenance and policy checks and returned
`HOLD_TOPX4_S2F3_BEFORE_FINITE_CHARGE_QUANTUM_COMPLETION`. Items 3--9 below
remain open. A subsequent 16/16 checkpoint derived the constant-background
charged amplitude-phase operator, its Goldstone/amplitude branches and the
fixed-global-charge Routhian/variation identities. It rejected omitted-mixing
and wrong-sign-Routhian mutations, but did not construct an evolving quantum
state or renormalized stress tensor. Item 3 is therefore only partially
advanced; evolving-state control, physical Hessian, continuous robustness and
parity/anomaly/counterterm audit remain open. The preregistered dynamic
state/subtraction checkpoint subsequently constructed the exact evolving
scalar mode system and passed its UV order hierarchy, but returned `11/12`:
three low-mode fourth-order WKB iterates became non-positive near the initial
hypersurface. Its binding status is
`FAIL_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT`. Item 2 is therefore only
partially specified and Item 3 remains incomplete. No A4 or Ultra work is
opened, and Rule-9 three-way clearance is not met.

A separately frozen exact-transport retry preserves the failed WKB result and
passes `18/18` bounded checks. It supplies positive-Hamiltonian scalar Cauchy
data with exact symplectic transport and a first-order Dirac superadiabatic
projector with exact unitary transport. The prior low modes remain finite under
this different prescription. This does not complete Item 2: neither state is
an infinite-order Hadamard construction, and the covariant 5D subtraction and
counterterm map remain uncomputed. Item 3 and all later items remain open.

The subsequent five-dimensional Hadamard/subtraction readiness checkpoint
passes `20/20` bounded checks on the universal local scaffold and returns
`PASS_5D_HADAMARD_COUNTERTERM_SCAFFOLD_HOLD_FULL_OPERATORS_STATE_AND_STRESS`.
It recovers the scalar singular structure through `U_2`, the general matrix
Laplace-type coefficients through `b_2`, the proper-time power divergences and
the independent pure-gravity counterterm basis. Its binding readiness decision
is nevertheless `HOLD`: the off-shell covariant scalar/`chi` matrix second
variation, scalar and Dirac Hadamard states, curved graviton/ghost operators,
parity-odd phase and counterterm normalizations are incomplete. Item 2 remains
partial, Item 3 remains incomplete, and all downstream items remain closed.

The next covariant scalar-matrix checkpoint passes `25/25` exact symbolic,
symmetry, dimensional, receipt, mutation and firewall checks. It derives the
rank-three fixed-metric off-shell operator for
`(sqrt(2) Re Phi, sqrt(2) Im Phi, chi)` before any homogeneous or fixed-charge
ansatz. In the registered convention its data are `E=-H` and `Omega_AB=0`;
the phase-aligned connection is pure gauge and reproduces the local
finite-charge derivative mixing. The scalar-induced bulk counterterm
structures are enumerated through `b_2`, including `R*s` and `R*chi^2`.
Counterterm normalizations, scalar and Dirac Hadamard states, curved
graviton/ghost operators, parity-odd data, determinant, stress and the
physical Hessian remain incomplete. Items 2 and 3 therefore remain partial,
`physics_pass=false`, `gate_effect=NONE`, and all downstream items stay
closed.

The next local scalar-matrix Hadamard-parametrix checkpoint passes `22/22`
bounded checks with status
`PASS_SCALAR_MATRIX_HADAMARD_PARAMETRIX_HOLD_GLOBAL_STATE_AND_STRESS`. It
verifies the five-dimensional singular power and prefactor, Cartesian
`U_0`, the matrix `U_1`/`U_2` coincidence controls in the registered
`E=-H` convention, the generic bundle-curvature term, and the
phase-aligned pure-gauge connection with its derivative mixing. A flat
constant-matrix recurrence supplies the executable matrix transport
realization. This derives local parametrix data through `U_2` only: the
arbitrary-background off-diagonal biscalars, smooth state term `W`, positivity,
wavefront condition, counterterm normalizations, determinant, stress and
physical Hessian remain open. Thus
`scalar_matrix_hadamard_parametrix=DERIVED_LOCAL_U0_U2`,
`scalar_matrix_hadamard_state=NOT_CONSTRUCTED`, `physics_pass=false`, and
`gate_effect=NONE` remain binding, and all downstream items stay closed. The
next single gate is a globally admissible infinite-order scalar-matrix state
construction.

## Required calculation

1. Re-derive the smooth-circle scalar, fermion and gravitational determinants
   from the frozen action; reproduce the High witness independently.
2. Declare the regulator, decompactification subtraction, renormalization
   scale, local counterterms and quantum state in executable metadata.
3. Vary the complete semiclassical effective action before applying the
   ansatz. Derive metric, radion, condensate-amplitude and phase equations.
4. Solve the finite-charge background with the Hamiltonian and global-charge
   constraints enforced, including the zero-charge nested control.
5. Perform the coupled scalar/radion/metric constraint reduction far enough to
   identify the canonical static Hessian and physical radion mass. Do not claim
   the later full A5 physical pole calculation.
6. Scan the frozen mass-ratio/cutoff domain. Report every exclusion and all
   unsuccessful roots, not only survivors.
7. Test regulator, subtraction-scale, state-order, resolution and initial-root
   robustness; require deterministic JSON and SHA-256 sidecars.
8. Apply every kill criterion in
   `TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md` fail closed.
9. Audit the parity-odd phase/anomaly content of the 5D fermion determinant and
   show that all required local counterterms obey their quantization rules.

## Required controls

- equal-mass analytic benchmark;
- `N_F=2` marginal/negative control;
- zero-charge, zero-portal and zero-winding controls;
- decompactification and small-circle limits;
- deliberate wrong fermion-sign mutation;
- deliberate omitted-mode mutation;
- finite-density Goldstone count versus the zero-density five-graviton
  long-distance count;
- cutoff-boundary and mass-ratio-boundary cases.

## Stop boundary

Stop at the new `X4-D2_RETRY` decision. Do not begin A4 exchange, A5 Ultra
constraints, local gravity, phenomenology, manuscript revision or publication.

## Reasoning transition

Switch to Max for this plan. Ultra remains closed even if the radion survives;
the A4 exchange/source calculation must be separately frozen and completed
before any A5 entry decision.
