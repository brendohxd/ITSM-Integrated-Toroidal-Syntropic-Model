# Sealed handoff for Grok — `G-A5` S6 ensemble and naturalness audit

**Agent role:** Role A — mathematical and dimensional auditor  
**Access:** read-only repository research and report-back  
**Package:** `G-A5` only  
**Required reasoning:** High  
**Gate effect:** none  
**Stop:** return one complete report and do not start coupled metric work  
**Execution isolation:** use a fresh Grok session; do not import any unlisted
external-agent answer

## Mandatory scientific frame

Before any derivation, read these repository files completely, in order:

1. `GEMINI.md`;
2. `Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md`;
3. `active_research.md`;
4. `Theory/Core/ITSM_RESEARCH_ROUTE_AND_SELECTIVE_PUBLICATION_PLAN_2026-09-05.md`;
5. `Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_RCP0_ACTION_LEDGER_2026-09-05.md`;
6. `Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_MAX_FIXED_BACKGROUND_REDUCTION_2026-09-05.md`;
7. `Theory/Verification/G-A4_A-B3_ROLE_C_ADJUDICATION_2026-09-05.md`;
8. this sealed handoff and `HANDOFF_SHA256.md`.

If any file is unavailable or the prompt hash differs from the manifest,
report the exact discrepancy and stop.

Core identity: the observable vacuum is an active finite-density condensate
whose low-energy excitations, global circulation sectors, compact boundary
conditions, and exchanges with matter and a reservoir may have gravitational
consequences. Do not replace it with Lambda-CDM, particle dark matter or an
assumed MOND interpolation.

Binding status:

- `MAT-001 BLOCKED`;
- `UVIR-003 IN_PROGRESS`;
- `K_Q NOT_DERIVED`;
- `V NOT_COMPUTED`;
- the `G-A4` result is a bounded timelike phase-EFT shape result only;
- no script or external-model agreement can promote a gate.

No repository write, commit, push, publication, Notion update or website edit
is authorized.

## Package `G-A5` — exact ensemble and lower-operator closure

### Central question

Does the bounded S6 result survive a consistent thermodynamic ensemble and the
most general symmetry-allowed quartic-plus-sextic potential over a nonempty,
controlled domain, or is the pure `3/2` phase-EFT shape an unprotected
fine-tuned limit?

Work in four dimensions with signature `(-,+,+,+)`, natural units,

\[
s=|\Phi|^2=\rho^2/2,\qquad
X_R=-g^{\mu\nu}\partial_\mu\Theta\partial_\nu\Theta,
\]

and audit the scalar action class

\[
S=\int d^4x\sqrt{-g}\left[
-|\partial\Phi|^2-U(s)
\right],
\qquad
U(s)=m^2s+\frac{\lambda_4}{2}s^2+\frac{\kappa_3}{3}s^3.
\]

The pure-S6 case is `lambda_4=0`. Do not insert a matter coupling, topology,
reservoir operator, PKM1 term or UVIR force operator into this calculation.

### A. Ensemble audit

1. Derive the Noether current and homogeneous equations from the displayed
   Lorentzian action.
2. Treat fixed chemical potential and fixed total charge as separate
   variational problems. Write the grand-potential/Routhian functional for the
   former and the Legendre-transformed fixed-charge energy for the latter.
3. State which spatial volume and boundary datum are held fixed. If an
   infinite-volume fixed-total-charge limit is ill-defined, say so and use a
   finite comoving or physical volume without smuggling topology into the
   coefficient.
4. Derive the background branches and second variations in both ensembles.
   Determine which local fluctuation spectra agree and where the homogeneous
   zero mode differs.
5. Do not declare ensemble equivalence without giving the exact Hessian or
   susceptibility condition that permits it.

### B. Mixed-potential reduction

1. Derive the exact algebraic stationary equation
   `X_R=U_s(s)` and every real `s>=0` branch.
2. Substitute each admissible branch to obtain the exact leading-derivative
   `P(X_R)` with its branch convention.
3. Derive `P_X`, `P_XX`, sound speed, radial gap and compressibility. State all
   positivity and hyperbolicity conditions.
4. Define a local effective exponent without using observations, for example

   \[
   p_{\rm eff}=\frac{d\ln|P-P_0|}{d\ln|X_R-X_0|},
   \]

   with `P_0` and `X_0` explicitly defined. Determine when, if ever,
   `p_eff` approaches `3/2` over a parametrically controlled interval.
5. Give exact inequalities for quartic-dominated, crossover and
   sextic-dominated domains. A single sample point is insufficient.
6. Derive the first radial-gradient correction and compare it with the leading
   algebraic term across those domains.

### C. Wilsonian naturalness and cutoff

1. List every local `U(1)`-invariant operator through mass dimension six that
   the declared symmetries permit, separating potential and derivative
   operators.
2. Explain whether any declared symmetry forbids `s^2`. Do not invent one.
3. Audit quartic generation from the sextic interaction. If giving a
   coefficient, identify the 1PI diagram, loop order, regulator, subtraction
   convention and combinatorial factor. Otherwise report only regulator-aware
   power counting.
4. State the counterterms needed for closure of the EFT at the declared order.
5. Distinguish the dimensional scale `|kappa_3|^(-1/2)`, a Wilsonian cutoff,
   the radial gap and the phonon strong-coupling scale; do not identify them by
   dimensional resemblance.
6. Determine whether a nonempty hierarchy can simultaneously satisfy:
   sextic dominance, radial-mode decoupling, stable positive density and
   energies below the EFT cutoff.

### D. Decision

Give one primary disposition:

- `PURE_S6_ACTION_CLASS_READY_FOR_SEPARATE_METRIC_FREEZE`;
- `MIXED_QUARTIC_SEXTIC_ACTION_CLASS_READY_WITH_EXPLICIT_HIERARCHY`;
- `S6_SHAPE_CONDITIONAL_ON_UNPROTECTED_TUNING`;
- `S6_ACTION_CLASS_KILLED_BY_EMPTY_CONTROLLED_DOMAIN`;
- `INCOMPLETE_DUE_TO_UNSPECIFIED_ENSEMBLE_OR_RENORMALIZATION`.

Advancing means only that Codex may consider a separate action freeze. It does
not authorize the coupled metric calculation and cannot change a gate.

### Required adversarial checks

- Take `lambda_4 -> 0`, `kappa_3 -> 0`, `s_0 -> 0` and the branch/crossover
  limits separately; do not exchange nonuniform limits silently.
- Check boundedness of `U(s)` on the physical half-line `s>=0`.
- Check susceptibility and radial-gap signs in both ensembles.
- Identify where `P_XX` or the derivative expansion becomes singular.
- Test whether the claimed sextic window remains below all declared cutoffs.
- State explicitly whether any result determines a static spatial force,
  nonlinear screened charge, matter residue, `K_Q`, `V` or `a_0`.

### Forbidden inputs and operations

Do not use observed `a_0`, `H_0`, SPARC, `2*pi`, `2/3`, a desired force law,
target healing length, target coefficient or target cutoff. Do not repair a
failed hierarchy by importing topology, reservoir exchange, a nonanalytic
absolute value or an undeclared matter operator. Do not perform lapse/shift or
metric constraint elimination.

## Required return format

```text
AGENT: Grok
ROLE: A mathematical/dimensional auditor
PACKAGE: G-A5
PROMPT_SHA256: ...
REPOSITORY_WRITE: none
SOURCES_READ: ...
CONVENTIONS_AND_DIMENSIONS: ...
FIXED_MU_VARIATIONAL_PROBLEM: equation-by-equation
FIXED_CHARGE_VARIATIONAL_PROBLEM: equation-by-equation
ENSEMBLE_COMPARISON: ...
MIXED_POTENTIAL_BRANCHES: ...
PHASE_EFT_AND_EFFECTIVE_EXPONENT: ...
GAP_SOUND_AND_SUSCEPTIBILITY: ...
GRADIENT_EXPANSION_DOMAIN: ...
OPERATOR_INVENTORY: ...
RENORMALIZATION_AND_NATURALNESS: ...
NONEMPTY_WINDOW_TEST: ...
COUNTEREXAMPLES_OR_FAILURES: ...
VERIFIED_FACTS: ...
INFERENCES: ...
UNRESOLVED: ...
PRIMARY_DISPOSITION: ...
EXPLICIT_NON_CLAIMS: ...
GATE_EFFECT: none
OUTPUT_HASH: <hash of the exact complete report, or HASH_NOT_AVAILABLE>
```

Return one report and stop after `G-A5`.

