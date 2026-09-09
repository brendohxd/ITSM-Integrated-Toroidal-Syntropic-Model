# Max plan — bounded exact reductions and independent calculations

**Required reasoning:** Max  
**Gate effect:** none without later Ultra physical-mode completion and signed review  
**Entry condition:** corresponding High specification is frozen  
**Hard boundary:** stop before the full amplitude-phase-metric constraint/pole calculation  

## Purpose

Perform exact but bounded calculations that are too subtle for High and do not
yet require the complete gravitational constraint system. Each work package is
independent; run only those marked `READY_FOR_MAX_DERIVATION` by the High plan.

## X-1 — literature comparator parent-to-EFT reduction

From the frozen `RCP-C0` action:

1. solve the finite-density background;
2. expand `Phi=(rho_0+h) exp[i(mu t+pi)]/sqrt(2)` consistently;
3. derive the complete amplitude-phase quadratic kernel on the declared fixed
   background;
4. derive the physical dispersion branches before eliminating a field;
5. integrate out the heavy/amplitude mode only within its valid derivative
   expansion;
6. derive both the phase `P(X)` and Gross-Pitaevskii descriptions;
7. retain the `k^4/(4m^2)` term and mark the `P(X)` breakdown scale;
8. compare both reductions term by term.

Deliverable: symbolic derivation, assumptions ledger and deterministic checks.

## X-2 — ITSM-compatible parent scalar-sector reduction

Repeat X-1 for the frozen `RCP-I1` action without importing comparator
coefficients or its particle-dark-matter interpretation. Derive:

- finite-density solution and conserved charge;
- scalar amplitude-phase kernel;
- static source produced by the invariant portal;
- low-energy operators and their coefficients;
- field-chart map to any provisional ITSM IR variables;
- which coefficient combinations remain free.

If an on-shell gravitational background cannot be declared, stop with a named
background obstruction. Do not freeze metric perturbations and then call the
result a full ITSM physical mode.

## X-3 — nonlinear static source and screening control

On a background already validated for this restricted calculation:

- derive linear Green functions and healing length;
- solve at least one spherical extended source in linear and nonlinear regimes;
- match interior and exterior solutions;
- calculate effective charge versus source radius and density;
- audit both portal signs and all gradient eigenvalues;
- test zero-density, zero-coupling and weak-distortion limits;
- identify equivalence-principle/composition dependence;
- state whether the result is inverse-square, MOND-like or neither.

This package may classify a mechanism. It cannot derive the final physical
residue while metric constraints remain omitted.

## X-4 — independent P2 mathematical reproduction

Implement an independent route for representative rectangular-`T^3` Casimir
stress and the Stage-3B negative diagnostic:

- use an independent summation/regulator or analytic cross-check where
  available;
- reproduce representative lattice points and permutation symmetries;
- verify energy/pressure derivative conventions;
- test convergence and precision sensitivity;
- independently distinguish crossing from plateau/attractor;
- compare results without tuning tolerances to agreement.

Deliverable: independent code/output/hash set and discrepancy report. Do not
overwrite canonical evidence.

## X-5 — exact winding-template calculation

Only from the High-frozen convention and parent template:

- derive Noether current and circulation normalization;
- solve amplitude relaxation in fixed winding sectors;
- reproduce the S2 tests at preregistered parameter points;
- derive energy and stress versus rectangular moduli;
- test reflection, permutation, zero-winding and decompactification limits;
- keep the result a template until it is joined to the surviving physical
  parent.

## Max-level kill conditions

- the background is off shell;
- the reduction mixes equations from different actions;
- a heavy mode is eliminated outside its gap/derivative domain;
- the required force sign is unstable;
- a numerical target enters a coefficient;
- the result requires the omitted metric constraints to have physical meaning.

## Stop and switch to Ultra when

The next step requires any of:

- lapse/shift and metric constraint elimination;
- full ADM/Dirac or covariant presymplectic rank;
- diagonalization of the coupled amplitude-phase-metric system;
- invariant signed source-pole residue;
- PPN, lensing or gravitational-wave characteristics.

## Completion record

Report exact surviving action/domain, equations, code, raw outputs, hashes and
kill/hold decisions. Package at Medium/High before starting Ultra.

