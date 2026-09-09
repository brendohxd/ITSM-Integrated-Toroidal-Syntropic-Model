# ITSM research-route and selective-publication plan

**Date:** 2026-09-05  
**Last amended:** 2026-09-06 — recorded the local P2 portability/PDF repair and new downstream evidence constraints; no gate change  
**Branch:** `recovery/v12-core-architecture`  
**Document class:** proposed execution plan  
**Scientific standard:** hostile Tier-1 theoretical-physics review  
**Gate effect:** none  
**Publication authority:** none  

This plan is subordinate to `GEMINI.md`, the Core Identity Briefing,
`active_research.md`, signed gate decisions, the Tier-1 Route Test Programme,
and the current claim firewall. A work-package `PASS` is not a physics-gate
pass. No route may import an empirical normalization during derivation.

## 1. Objective

Pursue the routes with the greatest chance of resolving an upstream ITSM
obstruction, while extracting smaller publishable results that remain valid if
the full framework does not close.

The ordering principle is:

1. derive or reject a coherent relativistic finite-density parent;
2. publish independent mathematical or negative results when their evidence is
   already mature;
3. join topology, matter response and reservoir physics only through a declared
   common action;
4. defer observational fitting until the upstream observable is derived.

## 2. Binding starting state

| Item | Starting status | Consequence for this plan |
|---|---|---|
| `UVIR-003` | `IN_PROGRESS`; Tier-1 hold | No force or UV/IR closure claim |
| `MAT-001` | `BLOCKED` | No derived matter normalization |
| `V=C_m/sqrt(K_Q)` | `NOT_COMPUTED` | No downstream force normalization |
| `K_Q` | `NOT_DERIVED` | Bare chart coefficients are not observables |
| `a_0=cH_0/(2*pi)` | phenomenological present-epoch relation | Must not enter a blind derivation |
| `VOR-001` | open scaffold | Winding templates do not determine a force coefficient |
| `TOP-001` | open scaffold | No preferred physical modulus dynamics |
| `RES-001` | phenomenological/open-system control | No derived covariant `Q^mu` |
| `P2 / CBR-001` | scoped negative free-field result | Independent publication candidate |
| SPARC and other data routes | conditional/methods only | Cannot close a parent gate |

## 3. Prioritized route portfolio

| Priority | Route | Scientific leverage | Paper potential | Execution disposition |
|---|---|---:|---:|---|
| 1 | `M2/M3-U1` condensate portal within the relativistic complex-parent to phase-EFT classification | Very high | Very high | Main derivation lane |
| 2 | P2 rectangular-`T^3` Casimir/backreaction negative result | Independent | High, near-term | Parallel publication lane |
| 3 | Exact winding and phase-normalization audit | High for topology | Medium/high | Start as an audit; join only after parent selection |
| 4 | U5 covariant phase space plus M4 pole residue | High diagnostic value | Methods appendix or no-go paper | Embed in Priority 1 |
| 5 | Action/open-EFT reservoir derivation | High but difficult | High if successful | Open only after parent variables are fixed |
| 6 | Physical `T^3` spectrum from a surviving parent | High but dependent | High later | Dependency-locked |
| 7 | SPARC phenomenological comparator | Low upstream leverage | Methods only | Maintenance lane only |
| 8 | CMB, Hubble, clusters and PTA claims | Downstream | Premature | Defer |

Priority is scientific priority, not necessarily calendar order. P2 may reach
submission before Priority 1 closes because it does not depend on MAT-001.

## 4. Route 1 — relativistic complex parent and phase-EFT classification

### 4.1 Research question

Can one covariant finite-density complex-condensate action produce a healthy
low-energy mode, a nonzero static matter source, an invariant signed force
residue, and a controlled screening regime without inserting the desired
galactic law or normalization?

### 4.2 Literature control newly added

Use Berezhiani, Cintia, De Luca and Khoury, *Superfluid Dark Matter*,
`arXiv:2505.23900` / *Physics Reports* 1172 (2026), as a technical control,
especially its:

- relativistic complex-scalar to Gross-Pitaevskii reduction;
- `P(X)` classification and range of validity;
- amplitude-phase mixing beyond leading derivative order;
- `U(1)`-invariant source portal `-|Phi|^2 J/Lambda^2`;
- source-dependent nonlinear screening and healing-length force range.

The earlier underlying force construction is Berezhiani and Khoury,
*Phys. Rev. D* 99, 076003 (2019). These sources supply precedents, not ITSM
gate evidence.

### 4.3 Registered bounded control — `M2/M3-U1`

**Route ID:** `M2/M3-U1_CONDENSATE_PORTAL_CONTROL`  
**Status:** `ACTIVE_BOUNDED_RESEARCH`; `physics_pass=false`; RCP-0/1 fixed-background work completed with holds; S6 is conditional on unprotected tuning; the semantic verifier is locally repaired but independent Role-B confirmation is incomplete  
**Parent gates:** `MAT-001 BLOCKED`; `UVIR-003 IN_PROGRESS`  
**Architecture effect:** none unless a later signed decision adopts a survivor  
**Observational inputs during derivation:** prohibited  

#### Exact route question

Can a single covariant ITSM-compatible finite-density complex parent, with a
`U(1)`-invariant schematic matter portal

\[
    S_{\rm portal}=\int d^4x\,\sqrt{-g}\,
    F(|\Phi|^2)\,T_m,
\]

produce a stable physical mode with a nonzero, signed and normalized matter
residue after the full amplitude-phase-metric constraint reduction?

Here `T_m` is schematic at route registration. RCP-0 must define it off shell:
for example, as the trace derived from a specified covariant matter action or
as another declared scalar matter operator. It must not be introduced through
a circular definition in which the stress tensor already includes the portal
whose variation is being calculated.

The literature comparator is the special class
`F(|Phi|^2)=-|Phi|^2/Lambda^2` with a declared source convention. An
ITSM-compatible parent must derive or openly parameterize its own `F`; it may
not inherit the comparator's coefficient or dark-matter interpretation.

#### Mandatory bounded calculation

1. Write the covariant ITSM-compatible parent with
   `F(|Phi|^2) T_m`, including the off-shell matter definition, metric
   variation, dimensions and source-sign convention.
2. Solve the finite-density background without observational inputs.
3. Retain amplitude, phase and metric perturbations; do not set the phase or
   metric sector to zero before identifying the physical modes.
4. Perform the complete constraint reduction and diagonalization.
5. Calculate the signed, field-redefinition-invariant matter pole residue and
   reproduce it from the static source-to-source response where applicable.
6. Derive the healing length and nonlinear screened charge from the same
   parent, including interior/exterior matching.
7. Test ghosts, gradient stability, the zero-density and zero-coupling limits,
   equivalence principle, PPN and lensing. Record cutoff and domain conditions.
8. Only afterward ask whether topology or condensate microphysics fixes
   `v/Lambda^2` and produces the required acceleration dependence.

#### Why this control is genuinely new for the live programme

The previously tested minimal M2 radial/heavy classes did not contain a live
static radial source or left an independent soft coefficient. Expansion of a
finite-density invariant portal can supply a term linear in the amplitude
fluctuation, while the finite-density state mixes amplitude and phase modes.
This defeats only the restricted **no-static-source** obstruction. It does not
overturn the remaining M2/M3/M4 requirements or retroactively pass a rejected
route.

#### Findings that must remain visible during the test

| Issue exposed by the comparator | Consequence for ITSM |
|---|---|
| The linear force is inverse-square below a healing length | It is not automatically the required deep-regime/MOND-like acceleration law |
| Its strength contains a combination such as `v^2/Lambda^4` | Removing the static-source obstruction does not derive the normalization |
| The healing length depends on condensate density and self-interaction | It must be derived and evaluated in a valid condensate domain, not matched to a target scale |
| Dense objects acquire screened, size-dependent effective charge | Equivalence-principle, compact-object and source-universality tests are mandatory |
| One source-interaction sign can develop an infrared gradient instability when strongly distorted | The sign of the physical source-to-source force and the condensate response must be audited separately |
| The construction is a fifth-force calculation in a condensate | Lensing and both metric potentials do not follow automatically |
| The source model treats the condensate as particle dark matter | ITSM may use the mathematics as a control but must preserve its active-vacuum identity |
| No compact topology, winding or reservoir appears in the comparator | Those sectors cannot be claimed as derived or used to normalize this route |

#### Outcomes and route disposition

| Outcome | Disposition |
|---|---|
| Healthy physical pole, derived normalization and viable relativistic domain | Candidate may advance to a signed architecture review; no automatic gate pass |
| Healthy pole but residue retains free `F`, `v/Lambda^2` or equivalent data | Retain as a calculable comparator and potential classification paper; `MAT-001` stays blocked |
| Stable inverse-square force but no required acceleration dependence | Publishable mechanism/control result only; not an ITSM galactic completion |
| Required sign is unstable, screened charge violates hard bounds, or no overlapping EFT domain exists | Freeze/reject the tested action class and preserve the no-go evidence |
| Constraint reduction cannot be completed from the declared action | Hold with the missing operator or off-shell definition named explicitly |

#### Explicit non-claims

This control does not derive `a_0`, `1/(2*pi)`, `C_obs`, `H_0`, a winding-force
map, a physical `T^3` spectrum, a reservoir current, SPARC success, lensing,
Bullet Cluster behavior or a cosmological solution. A literature result is
precedent, not an ITSM result.

### 4.4 Compared action classes

Keep three namespaces separate:

| Class | Purpose | Non-inheritance rule |
|---|---|---|
| RCP-C0 | Minimal quartic complex-scalar plus invariant source portal | Literature comparator only; dark-matter ontology is not ITSM identity |
| RCP-I1 | ITSM-compatible finite-density vacuum-condensate parent | Must declare its own matter and metric coupling |
| RCP-PKM1 | Metric-hosted condensate-foliation candidate | Cannot borrow a fifth-force residue from RCP-C0 or RCP-I1 |

No Gross-Pitaevskii equation may be appended to an unrelated relativistic
action. It must be obtained through an explicit slowly-varying-field expansion
with the omitted fast modes and error order recorded.

### 4.5 Work packages

#### RCP-0 — preregistration and action ledger

Deliver:

- exact fields, dimensions, signs, symmetries and source convention;
- definition of the finite-density ensemble and chemical potential;
- distinction between vacuum condensate, particle dark matter and an external
  matter source;
- parameter-provenance table;
- predeclared success, hold and kill outcomes;
- explicit ban on using observed `a_0`, SPARC, `H_0`, `2*pi`, `2/3` or a target
  healing length.

Exit: one frozen action per namespace. If an action is incomplete, record the
missing operator rather than continuing with equations from another action.

#### RCP-1 — background and relativistic-to-nonrelativistic reduction

For each surviving action:

1. solve all retained background equations;
2. expand `Phi=(rho_0+h) exp[i(mu t+pi)]/sqrt(2)` in one fixed convention;
3. derive the quadratic amplitude-phase kernel before integrating out `h`;
4. derive the controlled low-energy phase theory;
5. independently derive the nonrelativistic Gross-Pitaevskii form;
6. show where the two reductions agree and state their cutoff/error terms;
7. retain the `k^4/(4m^2)` correction when the leading `P(X)` theory is no
   longer valid.

Exit: a mode-by-mode equivalence/classification table, not merely matching
notation.

Kill: an off-shell background, ghost, wrong-sign gradient, singular reduction,
or hybrid equations not derived from the frozen action.

#### RCP-2 — invariant matter portal and physical pole

Use the invariant portal as a control and test any ITSM replacement from its
own action:

1. expand the matter source about the finite-density background;
2. include amplitude, phase, metric and all relevant constraints;
3. eliminate nondynamical variables before diagonalizing;
4. compute the full source-to-source amplitude;
5. identify every physical pole, dispersion relation, sign and residue;
6. verify the residue under nonsingular field redefinitions;
7. compare with the static Green-function calculation;
8. state whether the force normalization is derived or still contains a free
   combination such as `rho_0/Lambda^2`.

Exit: signed invariant residue or a precise no-go/incompleteness statement.

Kill: a bare source coefficient called the physical coupling; a static profile
without the dynamical-mode audit; or a coefficient fixed by the desired force.

#### RCP-3 — nonlinear source and screening audit

Derive rather than assume:

- the weak-distortion condition;
- the nonlinear interior and exterior profiles for at least one spherical
  source;
- effective source charge as a function of size and density;
- healing length and its microscopic parameter dependence;
- stability for both interaction signs;
- matching between screened and unscreened regimes;
- test-body universality and equivalence-principle risk;
- Landau/condensate-disruption conditions, if retained, from the same parent.

Exit: a non-empty stable force domain with a physical cutoff and controlled
source matching.

Kill: the attractive or required sign is unstable in the intended regime;
screening introduces unacceptable composition dependence; or the force domain
does not overlap the claimed physical scale.

#### RCP-4 — relativistic completion screen

Only after RCP-0 through RCP-3 survive:

- compute both metric potentials;
- determine whether photons, matter and gravitational waves couple to the same
  or distinct effective metrics;
- derive PPN, Shapiro-delay, lensing and GW-propagation limits;
- establish the high-acceleration/zero-coupling GR limit;
- identify strong-coupling and radiative-stability scales.

Exit: either an allowed relativistic domain or a scoped exclusion.

#### RCP-5 — coefficient and phenomenology decision

Ask only after the blind derivation:

1. Does the parent determine the force strength?
2. Is the force inverse-square, MOND-like, scale-dependent or absent?
3. Does a transition scale emerge without importing `a_0`?
4. Can topology or winding enter through a normalized physical mode rather
   than a cycle-count slogan?
5. Is the result suitable for an observational test?

No observational lane opens merely because the source obstruction has been
removed.

### 4.6 Route-1 publication branches

| Result | Honest paper |
|---|---|
| Complete healthy response | Relativistic finite-density condensate with derived matter response |
| Portal works but normalization is free | Classification of long-range source responses in complex condensates |
| Restricted action classes fail | No-go/obstruction paper on static matter forces from finite-density condensates |
| Relativistic and GP reductions disagree outside a domain | Domain-of-validity/matching paper |

The paper should stand without claims about SPARC, the Hubble tension, Bullet
Cluster, PTA data or a topological origin of `a_0`.

## 5. Route 2 — P2 Casimir/backreaction negative-result paper

### 5.1 Scientific scope

The permitted result is narrow and independent:

> A free massless scalar on rectangular flat `T^3` has a validated anisotropic
> renormalized Casimir stress, while the tested free-field biaxial
> backreaction produces transient passages but no persistent `13/12` plateau
> or attractor.

It is not evidence for `a_0`, `H_0=72.97`, a driven condensate attractor or a
complete ITSM cosmology.

### 5.2 Submission-readiness packages

#### P2-A — fresh reproducibility freeze

- rerun Stages 1-3B from a recorded environment;
- require two byte-identical structured outputs;
- regenerate SHA-256 manifests after the final run;
- verify that every manuscript number and figure is generated by the frozen
  code/output pair;
- retain raw regulator, timestep and initial-condition sweeps.

#### P2-B — independent mathematical checks

- independently evaluate representative rectangular-lattice stress points;
- verify regulator/extrapolation convergence and permutation symmetries;
- check the stress tensor, energy derivative and pressure conventions;
- audit dimensions and sign conventions line by line;
- reproduce the absence of a plateau with an independently coded diagnostic.

#### P2-C — hostile manuscript audit

- audit abstract, title, figures and conclusion against the current canonical
  claim firewall, not contaminated historical summaries;
- make negative-result selection criteria explicit;
- state the domain of the free-field and biaxial model;
- distinguish a transient crossing from a plateau or attractor;
- verify code/data availability and exact artifact hashes.

#### P2-D — release decision

After P2-A to P2-C:

- optional external expert read;
- freeze versioned source and PDF;
- prepare repository/Zenodo reproducibility bundle;
- submit only after explicit operator approval.

P2 can proceed while Route 1 remains open.

## 6. Route 3 — exact winding and phase-normalization audit

### 6.1 Immediate audit

1. Fix whether the phase is dimensionless and record all `hbar`/`c`
   conventions.
2. Derive the Noether current and canonical charge from the parent action.
3. Derive circulation from the single-valued order parameter:
   `oint grad(theta).dl = 2*pi*n`, with the physical velocity map separately
   derived.
4. Define every compact length as edge, geodesic cycle, circumference or
   physical modulus; never interchange them.
5. Recompute the winding energy with amplitude relaxation.
6. Preserve the corrected S2 preregistered failure at `lambda=100`,
   `omega=1`; do not restore the superseded pass.

### 6.2 Parent join

Only after Route 1 selects a survivor:

- put the winding background on the same finite-density solution;
- derive its covariant stress tensor and backreaction;
- calculate amplitude-phase-metric modes about nonzero winding;
- differentiate the effective action with respect to rectangular moduli;
- test zero-winding, decompactification and isotropic limits;
- determine whether topology changes a normalized residue without importing a
  numerical target.

### 6.3 Publication condition

A standalone topology paper is allowed if it derives a clean, parent-specific
winding/moduli result. It must not claim a geometric acceleration scale unless
the complete invariant map is actually closed.

## 7. Route 4 — U5 covariant phase space and M4 pole residue

These are diagnostics inside Route 1, with two reusable outputs.

### U5 deliverable

- derive the presymplectic potential and current from the frozen action;
- identify gauge degeneracies and boundary/compact zero modes;
- compare the on-shell degree-of-freedom count with the ADM/Dirac count;
- repeat at the zero-gradient and nonzero-gradient backgrounds;
- state whether any rank change is physical, a chart boundary or a split
  artefact.

### M4 deliverable

- construct the constrained quadratic kernel with the matter-source vector;
- invert only on the physical subspace;
- compute signed source-pole residues;
- verify field-redefinition invariance and static/dynamic agreement;
- report a number only if its normalization is derived from the action.

Publication use: methods appendix to the parent paper, or a short no-go paper
if the covariant and ADM analyses expose a general obstruction.

## 8. Route 5 — action/open-EFT reservoir derivation

### 8.1 Entry condition

Do not open the expensive reservoir derivation until Route 1 fixes the system
degrees of freedom and stress tensor. The current finite-dimensional GKSL
calculation remains a phenomenological comparator, not a derivation of the
cosmological exchange current.

### 8.2 Work packages

1. **RES-R0 control audit:** reproduce positivity, trace preservation and
   steady-state results; separate mathematical consistency from physical
   identification.
2. **RES-R1 microscopic declaration:** specify system, reservoir, state,
   coupling operators, spectrum and covariance assumptions.
3. **RES-R2 reduction:** derive the influence functional or justified open-EFT
   generator and state every Markov, secular and coarse-graining assumption.
4. **RES-R3 stress transfer:** derive `T_m^munu`, `T_p^munu` and `Q^nu` from the
   declared dynamics; Bianchi conservation alone does not determine separate
   currents.
5. **RES-R4 limits and stability:** demonstrate zero-coupling recovery,
   positivity, no singular transfer coefficients, entropy accounting and
   stable background/perturbation eigenmodes.
6. **RES-R5 cosmological interface:** only a survivor may define background
   and perturbation transfer terms for later likelihood work.

Paper condition: publish only a controlled open-EFT derivation or a useful
closure/no-go theorem. A fitted `Q proportional (1+z)^(-n)` is phenomenology,
not the microscopic paper.

## 9. Route 6 — physical `T^3` spectrum from the surviving parent

### Entry condition

Route 1 must supply the physical constrained modes and Route 3 must supply the
consistent compact/winding background.

### Deliverables

- quantize the surviving physical modes on rectangular `T^3`;
- include amplitude-phase-metric mixing and zero modes;
- derive eigenfrequencies, degeneracies and moduli dependence;
- demonstrate regulator and truncation convergence;
- calculate which observables actually couple to each mode;
- test isotropic, decompactification and zero-winding limits;
- keep a spectral frequency distinct from a detectable PTA or GW signal.

No PTA comparison opens until the source, propagation and observable amplitude
are all derived.

## 10. Routes 7 and 8 — maintenance and deferment

### SPARC

Maintain only:

- data provenance and exclusion ledger;
- deterministic comparator execution;
- raw likelihood separated from priors;
- Newtonian, nuisance-refitted and shuffled controls;
- explicit `Conditional` labels for any assumed force law.

Do not optimize the parent theory through SPARC or infer a cosmological `H_0`
from an underived galactic normalization.

### CMB, Hubble, clusters and PTA

Defer likelihood or headline claims until their respective action, background,
perturbation, lensing/hydrodynamic and propagation dependencies close. Evidence
watch may continue, but it changes test requirements rather than validating
ITSM.

## 11. Execution sequence

### Phase A — immediate, independent actions

1. Freeze this plan without changing gate status.
2. Start RCP-0 and RCP-1 for the complex-parent classification.
3. In parallel at project level, run P2-A reproducibility and P2-B independent
   checks; no scientific dependency exists between them.
4. Run the Route-3 convention/provenance audit, but do not join it to the force
   action yet.

#### Current checkpoint — 2026-09-06

- Plan and RCP-0 action namespaces are frozen without gate promotion.
- The bounded RCP-C0/RCP-I1-C fixed-background reduction is complete. It found
  a healthy scalar domain and a nonzero source coefficient but only a
  Yukawa/inverse-square response, free normalization and an off-shell
  finite-density Minkowski background.
- Grok `G-A4` and Antigravity `A-B3` were adjudicated with corrections in
  `Theory/Verification/G-A4_A-B3_ROLE_C_ADJUDICATION_2026-09-05.md`.
- The pure-sextic `RCP-I2-S6` route retains a bounded timelike
  `(X_R-m^2)^(3/2)` phase-EFT shape. It does not derive the spatial force
  operator or any normalization.
- Codex's independent mixed-potential precheck finds that any nonzero positive
  quartic restores quadratic behavior near `X_R=m^2`; a `3/2` interval
  requires sextic dominance and a still-unproved Wilsonian hierarchy.
- Grok `G-A5` was accepted with corrections as a narrowing result:
  `S6_SHAPE_CONDITIONAL_ON_UNPROTECTED_TUNING`. It does not naturalness-close
  the pure-S6 parent.
- The completed old-session Antigravity `A-B4` verifier was rejected for a
  wrong low-`k` `k^4` sign and non-semantic pass logic. A fresh external run
  terminated before a valid final report. Codex's replacement verifier passes
  all 32 local semantic checks and detects all 9 registered mutations, but it
  is local tooling and does not satisfy independent-review Rule 9.
- Full coupled metric work remains unopened. The present S6 result does not
  satisfy the RCP-2 entry conditions.

#### Current checkpoint — 2026-09-09

- Operator priority remains redirected to `TOP-X4 / KK-001`, so the RCP-2,
  publication and external-dispatch queues remain paused.
- Plan 11 completed the `X4-S2F3` static parity-even determinant checkpoint
  (`12/12`) and held at the finite-charge entry gate (`9/9`). This does not
  satisfy the RCP-2 entry conditions, reopen Ultra work or change any MAT,
  UVIR, RES, VOR or publication status.
- The Plan 11 Rule-9 review is incomplete: Role A completed, while Roles B and
  C returned usage-limit errors with no reports.

### Phase B — decisive upstream calculation

1. Complete RCP-2 physical pole/residue with U5 and M4 integrated.
2. If it survives, run RCP-3 screening and stability.
3. If it fails, freeze the failed class and write the classification/no-go
   result before designing another parent.

### Phase C — relativistic and publication decisions

1. Run RCP-4 only for a survivor.
2. Decide the Route-1 paper branch from the actual outcome.
3. Complete P2 hostile review and release freeze independently.
4. Join winding to the surviving parent or retain it as a scoped template.

### Phase D — dependent theory

1. Open the reservoir action/open-EFT route.
2. Derive the physical compact spectrum.
3. Only then reassess galaxy, cosmology, cluster and GW/PTA programmes.

## 12. Decision matrix

| Checkpoint | Advance | Hold | Reject/freeze |
|---|---|---|---|
| Parent action | Complete, covariant, on-shell background | Missing declared UV data that can be isolated | Hybrid/inconsistent action |
| Physical modes | Healthy constrained spectrum | Controlled narrow domain | Ghost, singular rank or no cutoff overlap |
| Matter response | Invariant signed residue | Form derived but normalization free | No source or chart-dependent residue |
| Screening | Stable matched regimes and acceptable universality | Domain too narrow to claim | Required sign unstable or equivalence-principle failure |
| Relativistic limit | GR/PPN/lensing/GW-compatible domain | Additional explicit completion required | No viable high-acceleration limit |
| Topology | Parent-specific stress and modes | Mathematical template only | Target coefficient inserted through cycle conventions |
| Reservoir | Derived current with nested null limit | Phenomenological control | Bianchi identity used as a closure |
| Observation | Derived observable and preregistered controls | Methods-only comparator | Post-hoc filtering or reverse engineering |

## 13. Reasoning-mode and cost discipline

The executable work has been split into mode-specific plans under
[`Theory/Core/Reasoning_Mode_Plans/`](Reasoning_Mode_Plans/README.md). Use that
index to start one bounded task and stop at the recorded handoff boundary.

| Work | Recommended mode |
|---|---|
| Repository inventory, reruns, hash/manuscript checks | Medium/High |
| P2 hostile review and route architecture | High |
| Frozen parent-to-EFT and nonlinear static reductions | Max |
| Coupled amplitude-phase-metric constraints, U5 and M4 | Ultra |
| Reservoir influence-functional/current derivation | Ultra |
| Physical parent-specific `T^3` spectrum | Ultra |
| Packaging after equations and claims are frozen | Medium |

Switch down after each bounded derivation. Do not spend Ultra reasoning on
SPARC fitting, formatting, routine reruns or release packaging. The reservoir
and physical-`T^3` plans are separate future Ultra goals and must not be bundled
with the immediate pole-residue calculation.

## 14. First three bounded tasks

1. **`M2/M3-U1` registration plus RCP-0/1 specification:** freeze the
   off-shell portal definition, create the three action namespaces, reproduce
   the literature comparator reduction and identify the exact delta required
   for ITSM identity.
2. **P2-A/B release audit:** independently reproduce the negative result and
   freeze code-output-manuscript hashes.
3. **RCP-2 with U5/M4:** compute the full constrained source response and decide
   whether the invariant portal is a viable ITSM research parent, a useful
   comparator or a no-go.

Task 3 is the first point at which Ultra is justified. None of these tasks
authorizes a commit, push, publication submission, gate promotion or external
workspace update.

### Current disposition of the first three tasks

| Task | Status on 2026-09-06 | Next evidence required |
|---|---|---|
| `M2/M3-U1` RCP-0/1 | `BOUNDED_REDUCTION_COMPLETE_WITH_HOLDS`; Role-C adjudicated | The local verifier is repaired and S6 remains conditional. A new symmetry/UV protection mechanism or a different frozen parent is required before RCP-2; external Role-B rerun remains useful for triangulation but cannot substitute for that physics input. |
| P2-A/B | `LOCAL_REPAIRED_CANDIDATE`; not release-ready | Independent Role-A normalization/closure audit, restricted Role-B execution witness, sensitivity suite and independent noncubic evaluator |
| RCP-2 with U5/M4 | `NOT_OPENED` | One action class, ensemble, on-shell gravitating background, matter interface and EFT domain must first be frozen |

Use High for the independent P2 hostile audit and for designing any new
symmetry/UV-completed action class. Use Max only after one replacement action
and its ensemble are explicitly frozen. Switch to Ultra only if that parent
satisfies every stated RCP-2 entry condition; the present conditional S6 route
does not justify Ultra coupled-calculation spend.
