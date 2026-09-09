# Max plan — TOP-X4 `X4-S2F3` semiclassical stabilization

**Mode:** Max  
**Entry:** `X4-S2F3 FROZEN_FOR_ONE_MAX_RETRY`  
**Exit:** `X4-D2_RETRY PASS_STABLE_DOMAIN`, `HOLD`, or `CLOSED_NEGATIVE`  
**Gate effect:** none

## Objective

Determine whether the frozen three-periodic-Dirac completion produces a
self-consistent finite-charge compactification with a positive physical
radion mass and a nonempty five-dimensional EFT domain.

## Current checkpoint — 2026-09-09

The zero-density static parity-even determinant checkpoint completed `12/12`
bounded calculation checks. The finite-charge entry gate then completed `9/9`
provenance and policy checks and returned
`HOLD_TOPX4_S2F3_BEFORE_FINITE_CHARGE_QUANTUM_COMPLETION`. Items 3--9 below
remain open: finite-charge state-dependent variation, evolving-state control,
physical Hessian, continuous robustness and parity/anomaly/counterterm audit.
The static solver is not a substitute for those calculations. No A4 or Ultra
work is opened, and Rule-9 three-way clearance is not met because Roles B and C
returned usage-limit errors without reports.

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
