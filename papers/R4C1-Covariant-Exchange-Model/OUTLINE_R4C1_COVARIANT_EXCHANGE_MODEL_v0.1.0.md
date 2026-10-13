# R4C1 theory-paper outline v0.1.0

## Working title

**A covariant finite-density exchange model: conservation, canonical density
dynamics, and limits of nonlinear force matching**

Alternative shorter title:

**Covariant finite-density exchange with a dynamical reservoir**

## Paper identity

This should initially be **one bounded R4C1 theory paper**, not two papers.
Coefficient non-identifiability, the compact-\(T^3\) curl condition, and the
periodic zero-mode condition belong together as limitations on what the model's
background or local force matching can establish. A separate no-go paper is
justified only if those results are later generalized into a theorem applying
to a clearly defined model class beyond R4C1.

The rectangular-\(T^3\) Casimir programme remains a separate P2 paper. R4C1
should cite its stress formula and the independent literature control, but not
merge P2's full scan, renormalization, or backreaction work into this paper.

## Public claim boundary

The paper presents a conditional action and derives what follows from it. It
does not claim that ITSM is established, that the weak-field square-root law is
derived, that all perturbations are stable, or that cosmological data prefer
the model.

The central public contribution is:

> A declared covariant action yields explicit, nonsingular exchange currents
> and total conservation; its canonical dust-density mode has the standard
> uncoupled normalization, while homogeneous matching and compact-domain
> integrability place sharp limits on any claimed nonlinear force
> normalization.

## Proposed abstract logic

1. State the problem: interacting cosmologies often postulate a transfer vector
   or infer local force normalizations from homogeneous expansion without a
   complete action-level derivation.
2. Introduce the conditional R4C1 action, including matter, plenum, finite-charge
   and reservoir sectors.
3. Derive the three sector exchange identities and total conservation.
4. Reduce the scalar dust-density mode and exhibit
   \(K_D=a^5\rho_m/k^2\) in the uncoupled limit.
5. Show the exact normalization agreement with the independent coupled-fluid
   EFT of Aoki et al., while explaining why this does not identify the
   interacting coefficients.
6. Prove the scoped non-identifiability and compact-domain compatibility
   results.
7. State the remaining stability, matching, state-selection, and observational
   obligations without promotion language.

## Section plan

### 1. Introduction

- Distinguish three questions:
  1. Is the exchange current derived from an action?
  2. Is the reduced system dynamically stable?
  3. Does it produce the proposed weak-field or cosmological phenomenology?
- Explain that satisfying the first question does not answer the other two.
- Position R4C1 as a conditional finite-density exchange construction, not a
  completed cosmology.
- Summarize the paper's positive results and its explicit obstructions.

### 2. Field content, frames, and action

- Declare metric signature, units, dimensions, and manifold assumptions.
- List the metric, amplitude/phase variables, auxiliary fields, finite-charge
  variable, reservoir field, and matter clock/fluid variables.
- Write the complete frozen R4C1 action in one place.
- Define the matter-frame metric \(\tilde g_{\mu\nu}=C^2g_{\mu\nu}\) and
  \(C=e^{\beta\psi}\).
- Separate fundamental terms, regulators, auxiliary constraints, and
  phenomenological ansatzes.
- State every domain restriction and singular surface.

### 3. Covariant variation and source-vector closure

- Vary each sector independently.
- Display \(T_m^{\mu\nu}\), \(T_P^{\mu\nu}\), and \(T_R^{\mu\nu}\).
- Derive
  \[
  \nabla_\mu T_m^{\mu\nu}=Q_{mp}^{\nu},\quad
  \nabla_\mu T_P^{\mu\nu}=-Q_{mp}^{\nu}+Q_{\rm syn}^{\nu},\quad
  \nabla_\mu T_R^{\mu\nu}=-Q_{\rm syn}^{\nu}.
  \]
- Verify total conservation algebraically.
- Demonstrate the uncoupled limit and identify which couplings must vanish.
- Explain that the frozen reservoir is reversible and does not yet constitute a
  microscopic irreversible heat bath.

### 4. Homogeneous finite-charge background

- Specify lapse, scale factor, homogeneous fields, and charge convention.
- Derive the background Euler-Lagrange and Hamiltonian/Friedmann equations.
- Eliminate auxiliaries only after their regularity domains are declared.
- Present the finite-charge on-shell branch and its existence conditions.
- Separate action-derived relations from any observational matching condition.
- Include a table of free initial data, conserved quantities, and conditional
  parameters.

### 5. Scalar constraints and canonical density reduction

- Introduce scalar metric, matter-density, amplitude, phase, and reservoir
  perturbations before constraints.
- Display the pre-constraint kinetic, gradient, and mass blocks.
- Solve lapse/shift and other auxiliary constraints, including singular-domain
  cases.
- Derive the physical density variable and its quadratic action.
- Present the formal result
  \[
  K_D=\frac{a^5\rho_m}{k^2}>0
  \]
  for uncoupled positive-density dust.
- Keep the known negative-mass/indefinite-Hamiltonian issue explicit; do not
  equate a positive kinetic coefficient with full stability.

### 6. Independent coupled-fluid EFT control

- Summarize the relevant convention in Aoki et al.:
  \(X^T=(\delta_c/k,\zeta,\delta_m/k)\) and no overall \(1/2\) in the
  quadratic action.
- Convert
  \[
  K_{11}=\frac{a^2M^2H^2}{2}
  (3\Omega_c+\alpha_{m2}-\bar\alpha_{m1}^{,2})
  \]
  to the standard \(\delta_c\) normalization.
- Show the exact uncoupled equality with R4C1.
- Give a side-by-side operator table and mark every unmapped coefficient as
  `NOT_DERIVED`.
- Explain the difference between a normalization control and an interacting
  theory equivalence.

### 7. What homogeneous matching cannot identify

- State the exact R4C1 action and branch to which the result applies.
- Identify the combinations of coefficients visible to homogeneous background
  equations.
- Exhibit the degeneracy/reparameterization family that leaves those equations
  unchanged.
- Conclude only that the nonlinear force normalization is not identifiable from
  that homogeneous data within the stated branch.
- Do not advertise a broad model-class theorem unless a separate proof supplies
  the class assumptions and counterexample exclusions.

### 8. Compact-\(T^3\) compatibility conditions

#### 8.1 Local curl/integrability condition

- A force prescribed as the gradient of a scalar must be curl free.
- Apply this to the proposed pointwise square-root relation.
- State the conditions under which the relation is locally integrable and give
  explicit counterexamples when it is not.
- Distinguish failure of a universal pointwise prescription from failure of
  every nonlocal or projected torus solution.

#### 8.2 Periodic zero-mode condition

- Integrate the periodic Poisson-type equation over the compact domain.
- Show that its source must have zero spatial mean.
- Explain why a strictly positive mean density requires subtraction of the
  homogeneous mode, a compensating sector, or a different equation.
- Keep this compatibility result separate from observational claims.

#### 8.3 Topology-sector control

- Cite the rectangular-\(T^3\) conformal-scalar stress from P2/CBR-001.
- Record the independent heat-kernel and Negro et al. agreement.
- State that the state-dependent isotropic zero mode and dynamical backreaction
  remain outside the R4C1 result.

### 9. Stability and well-posedness ledger

- Tabulate what is checked and what remains open:
  - uncoupled density kinetic normalization;
  - interacting kinetic matrix;
  - gradient matrix and characteristic speeds;
  - fourth-spatial-derivative regulator;
  - constraint singularities;
  - mass matrix and Hamiltonian boundedness;
  - hyperbolicity and domain robustness.
- State failure criteria before presenting parameter examples.
- Do not use check counts as a physics-closure claim.

### 10. Phenomenological interface and falsifiers

- Explain which observables require the still-missing stable interacting branch.
- List the eventual outputs: \(H(z)\), \(Q^\mu\), \(G_{\rm eff}\), slip,
  weak-field force law, BBN inputs, and perturbation transfer functions.
- State that no fit should be interpreted as an ITSM prediction until the
  action-to-observable dictionary is fixed.
- Provide a falsification table for the conditional branch.

### 11. Discussion and conclusion

- Lead with the action-derived conservation result and density normalization.
- Treat the non-identifiability and compact-domain results as scientific
  constraints, not disappointments.
- Explain precisely which further derivation would turn the conditional model
  into a predictive theory.
- Reiterate that external review remains deferred, not waived.

## Appendices

- **A.** Full variations and boundary terms.
- **B.** Dimensions, signs, and convention translations.
- **C.** Background equations and finite-charge branch algebra.
- **D.** Constraint elimination and canonical transformations.
- **E.** Aoki-EFT convention conversion and coefficient dictionary.
- **F.** Non-identifiability proof and scope assumptions.
- **G.** Curl and compact zero-mode proofs with counterexamples.
- **H.** Reproducibility manifests, hashes, and executable receipts.

## Claim ledger for drafting

| Proposed statement | Current status | Permitted wording |
|---|---|---|
| R4C1 is a declared covariant action | Conditional action frozen | “We study the following conditional action.” |
| Sector exchange currents follow from variation | Locally derived | “Variation yields…” with equations and assumptions |
| Total stress is conserved | Locally derived | “The summed sectors obey total conservation on shell.” |
| Uncoupled density kinetic coefficient is standard | Exact local derivation plus independent control | “The uncoupled dust normalization agrees exactly with coupled-fluid EFT.” |
| Interacting density sector is stable | Not derived over the full domain | Must not be claimed |
| Homogeneous cosmology fixes the nonlinear force coefficient | Rejected for the scoped R4C1 branch | “The coefficient is not identifiable from these homogeneous equations alone.” |
| Universal pointwise square-root law works on \(T^3\) | Fails without local integrability and zero-mode conditions | State the conditional obstruction, not a universal theory rejection |
| Casimir stress closes R4C1 or TOP-X4 | Not established | Cite only as a separate topology-sector control |
| ITSM fits cosmological or galaxy data from this action | Not yet demonstrated | Prospective only |
| Paper is publication ready | Deferred independent review remains | Must not be claimed |

## Minimum submission package

Before public preprint submission, require:

1. one internally consistent LaTeX manuscript with no stale equations;
2. a source-to-claim table linking each equation to its derivation or declared
   ansatz;
3. executable symbolic/numerical controls with immutable receipts;
4. a limitations and falsification section in the main text;
5. independent technical review of variations, constraints, and theorem scope;
6. a clean bibliography using the exact paper versions cited; and
7. a final public-data and sensitive-content audit.

## Immediate drafting order

1. Sections 2–3: action and source-vector closure.
2. Section 5: canonical density reduction, including the Hamiltonian caveat.
3. Sections 7–8: scoped limitations and compact-domain proofs.
4. Section 6: external EFT control.
5. Sections 4 and 9: background and stability ledger.
6. Introduction, discussion, and abstract only after the technical body is
   internally consistent.
