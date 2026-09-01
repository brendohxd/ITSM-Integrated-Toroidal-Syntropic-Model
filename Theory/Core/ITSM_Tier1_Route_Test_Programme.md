# ITSM Tier-1 route-testing and recovery programme

**Version:** 1.1-proposed

**Date:** 2026-08-23

**Last evidence integration:** 2026-08-25

**Branch:** `recovery/v12-core-architecture`

**Status:** planning authority subordinate to `GEMINI.md`, the Core Identity
Briefing, the Master Research Plan, and gate decisions

**Scientific standard:** hostile Tier-1 theoretical-physics review

**Gate posture:** fail closed; this plan restores no claim

## 1. Objective

Test genuinely distinct routes for completing ITSM while preserving its
identity as a finite-density condensate with low-energy excitations, compact
`T^3` boundary conditions, circulation sectors, matter coupling, and a fully
accounted reservoir.

The programme must answer, in order:

1. Does a covariant, stable microscopic or controlled EFT action exist?
2. Does it contain the intended physical degrees of freedom without double
   counting the condensate current and independent frame field?
3. Does it derive a healthy weak-field response and normalized matter residue?
4. Can it pass local gravity, lensing, gravitational-wave, and compact-object
   constraints?
5. Can the same action generate a coherent background and perturbation
   cosmology?
6. Only then, does it improve observations relative to preregistered controls?

An honest no-go, bounded exclusion, or permanent hold is a successful research
outcome. Numerical agreement cannot repair an absent derivation.

## 2. Binding baseline

Until a later signed gate decision changes them:

| Item | Binding status |
|---|---|
| UVIR-003 | `IN_PROGRESS`; full Tier-1 closure held |
| MAT-001 | `BLOCKED` |
| `K_Q` | `NOT_DERIVED` |
| `V=C_m/sqrt(K_Q)` | `NOT_COMPUTED` |
| MAT R5 | `HOLD_DECLARED_ACTION_UNDERDETERMINES_V` |
| R5-P1 compensator | research candidate only; no gate pass |
| RES-001 | `OPEN_SCAFFOLD_ONLY`; no route selected |
| TOP-001, WAK-001 | open scaffolds |
| VOR-001 | partial scoped results; physical screening not established |
| DISK-001, STAT-001, SCR-001, LEN-001 | downstream; no physics pass |
| COS-001, PERT-001 | architecture only; no fiducial ITSM cosmology |
| `a_0=cH_0/(2*pi)` | present-epoch phenomenological relation, not derived |
| `C_obs=2/3`, `13/12`, `H0=72.97` | not live derived predictions |

`active_research.md` becomes a reliable dashboard only after Phase G0 removes
its duplicate status surfaces and reconciles it with signed gate decisions.

## 3. ADR-RT-001: staged route portfolio

**Status:** Proposed

**Decision:** Run bounded routes through the same admissibility and
falsification gates. Do not choose a mechanism because it reproduces `a_0`,
`C_obs`, `H_0`, or another desired number.

| Option | Advantage | Failure mode | Decision |
|---|---|---|---|
| Continue only Track-A/R5-P1 | Lowest setup cost | Locks programme to a contaminated route | Reject as sole strategy |
| Explore all historical ideas at once | Broad coverage | Unbounded cost and post-hoc switching | Reject |
| Staged portfolio with shared gates | Fair tests and cheap no-go screens | Needs strict route namespaces | Adopt |
| Fit closures first | Quick plots | Reverse engineers mechanisms | Control lane only |

Consequences:

- No route borrows a coefficient, stability result, or success from another
  route without an action-level map.
- Adding a field, symmetry, reservoir, metric coupling, or phase transition
  requires an architecture decision record.
- At most two expensive microscopic routes advance beyond cheap screens at
  one time.
- The null/current-action route remains in every comparison.

## 4. Universal route evidence contract

| Stage | Required evidence | Pass condition | Mandatory stop condition |
|---|---|---|---|
| A0 Identity | Question, five-pillar map, exact novelty | No silent identity replacement | Renames a rejected claim |
| A1 Action | Covariant off-shell action or explicitly phenomenological controlled law; fields, units, coefficients, stress-tensor split | Metric and field variations, provenance, and dimensions complete | Desired observable inserted as a relation or Bianchi identity used to invent a sector current |
| A2 Symmetry/DOF | Symmetries, breaking, constraints, gauge, DOF | Lagrangian/Hamiltonian counts agree | Ghost or double counting |
| A3 Background | On-shell Minkowski/FRW/galactic background | Every retained EOM solved | Off-shell poles/amplitudes |
| A4 Physical modes | Constraints eliminated before diagonalization | Healthy physical kinetic/gradient blocks | Ghost, uncontrolled instability, singular constraints |
| A5 Causality/EFT | Characteristics, front speeds, cutoff, coupling domain | Non-empty observational domain | Claim above cutoff/outside hyperbolicity |
| A6 Matter residue | Signed on-shell matter-to-mode pole residue | Field-redefinition invariant and reproduced | Bare/pre-projection coupling called observable |
| A7 Relativistic completion | Two potentials, PPN, lensing, GW propagation | One domain passes hard bounds | Local/lensing failure without derived screening |
| A8 Cosmology | Same action/declared closure for background and perturbations | Stable, continuous nested null limit and initial conditions | Mixed actions, dataset-specific backgrounds, or a singular zero-coupling limit |
| A9 Observation | Preregistered likelihood, controls, raw results | Gain survives nuisance and complexity penalties | Post-outcome selection/filtering |
| A10 Decision | Report, summary, hashes, hostile review | Scoped disposition | Generic `CLEARED` from script PASS |

Reproducibility minimum:

- deterministic command and environment record;
- raw output plus structured summary;
- units and conventions metadata;
- mutation and negative-control tests where meaningful;
- SHA-256 after the final run;
- no absolute private paths or synthetic replacement data;
- code-to-claim inspection, not merely successful execution;
- independent reproduction for gate-critical results.

## 5. Phase G0 — authority and evidence repair

No new route may receive a scientific status before this phase closes.

| ID | Task | Exit condition |
|---|---|---|
| G0.1 | Record branch, remote divergence, dirty/untracked files, and hashes without overwriting work | Signed workspace manifest |
| G0.2 | Normalize one gate dashboard and remove duplicates | One status per gate backed by a decision |
| G0.3 | Audit `CLEARED`, `DERIVED`, `zero-parameter`, `massive success`, `falsified` | Unsupported promotions quarantined/downgraded |
| G0.4 | Reconcile R5-P1 files with MAT R5 and UVIR Stage 5 | Child file cannot override parent gate |
| G0.5 | Recompute modified outputs/sidecars and compare code, output, prose | Evidence agrees or is invalidated |
| G0.6 | Classify untracked manuscripts/gate drafts: adopt, repair, quarantine, delete-later | Untracked work has no authority |
| G0.7 | Propagate corrected statuses to README, docs, Pages, manuscripts | Public surfaces do not exceed evidence |
| G0.8 | Protect immutable releases and historical records | No frozen release silently edited |

Known G0 targets from the 2026-08-23 audit:

- `STAT-001_GATE_REPORT.md` declares `CLEARED` despite open upstream gates and
  poor raw fit statistics.
- `UVIR-003_STAGE_B_R5_P1_AMPLITUDE.md` and
  `UVIR_003_T5_UNITARITY_CRITERION.md` claim full closure without the complete
  constrained physical amplitude.
- The R5-P1 contact amplitude comes from a background matter-density coupling
  and omits complete vacuum, derivative, gravity, and mixed sectors; it cannot
  establish arbitrary-energy unitarity.
- `CBR-002_SCALE_DERIVATION.md` calls a scale zero-parameter after imposing
  BTFR and RAR targets; that is matching, not blind derivation.
- `HEALING_LENGTH_TEST.md` compares an underived healing length with a
  target-derived length; it is not executable until microscopic parameters and
  the scale map are independently derived.
- Dynamic Scale Matching text obtains `a_0` only after postulating the required
  present-day torus circumference.
- Modified and untracked evidence needs code/output/hash reconciliation before
  commit.

Preserve these files as evidence until disposition is logged. Do not silently
delete them or use them as current theory.

## 6. Dependency graph and lanes

```text
G0 authority repair
 |
 +-- F0 current-action null/control
 +-- UVIR physical viability --------+
 +-- MAT microscopic matching -------+--> SCR + LEN --> DISK + STAT
 +-- TOP + VOR + WAK ----------------+
 +-- RES action/constitutive law -----+--> COS + PERT --> cosmological data
 +-- coefficient/provenance audits (parallel; cannot unlock gates alone)
```

- **Lane A — derivation:** can change gate status.
- **Lane B — methods/phenomenology:** can test solvers and discriminators but
  cannot supply a missing action, coefficient, or pass.

## 7. Route portfolio

### 7.1 UVIR and force routes

| ID | Route | First decisive test | Advance only if | Reject/freeze if |
|---|---|---|---|---|
| U0 | Current Track-A action/control | Reproduce Stage-5 ledger and transfer | Clean rerun survives claim audit | Provenance/equations fail |
| U1 | Controlled complex-quartet interpretation | Gauge-invariant dispersion, Hamiltonian energy, finite `k/a` band, growth and backreaction | Finite controlled episode returns healthy | Vacuum runaway, nonhyperbolicity, uncontrolled backreaction |
| U2 | Exact nonzero-gradient `Y^(3/2)` | Physical modes and full constrained amplitude on declared gradient | Domain covers galaxy regime below cutoff | No overlap with force regime |
| U3 | Analytic completion/Track-B | Declare altered operator and UV origin; rerun A1-A6 | Derives rather than smooths IR term | Smoothing only manufactures vertices |
| U4 | Unified condensate-force parent | Integrate out heavy/amplitude modes and match EFT | Same parent yields density, force, normalization | Repeats UVIR-001 no-go/unstable modes |

U1 is the highest-value immediate Tier-1 physics task because the quartet lies
on the present action's viability path.

### 7.2 MAT-001 normalized-residue routes

| ID | Route | Required calculation | Kill/control criterion |
|---|---|---|---|
| M0 | Current independent `C_m,K_Q` action | Preserve identifiability family | Control remains underdetermined |
| M1 | Compensator + finite-density condensate | Full mixed reduction and signed matter pole residue | Reject if `f` only renames `V`, scalar is unscreened, or only pre-projection `1/f` appears |
| M2 | Radial/heavy-mode microscopic matching | Integrate out heavy sector with explicit matter interaction and calculate `g_phys/sqrt(Z_phys)` | Reject if static source absent or soft coefficient independent |
| M3 | Two-sector mixing/portal | Derive mixing from one parent and project matter onto eigenmodes | Reject appended free coupling/double counting |
| M4 | Direct on-shell residue | Compute invariant source-pole residue without assigning bare `K_Q` | Reject chart dependence or phenomenological normalization |
| M5 | Topology/modulus-locked matching | Derive coupling from normalized moduli/winding fluctuations | Reject inserted `L=c/H`, `2*pi`, `2/3`, or cycle count |
| M6 | Conditional AQUAL `C_obs≈1` | Blind methods/observational control | Never a MAT derivation |

After A0-A2, rank M1-M5 by identity fidelity, added parameters,
calculability, stability risk, and falsifiability. Advance at most two.

### 7.3 Screening and high-acceleration routes

| ID | Route | Decisive work |
|---|---|---|
| S0 | No-screening control | Direct Solar-System, laboratory, pulsar, compact-object failure domain |
| S1 | Kinetic/interpolating screening | Complete-action characteristics and front velocities; distinguish phase/group/front speed |
| S2 | Condensate disruption/Landau criterion | Excitation spectrum, critical gradient, healing length, nucleation, recovery/hysteresis, metric in disrupted region |
| S3 | Environmental mass/coupling | Named symmetry/action, radiative stability, equivalence-principle bounds |
| S4 | Retarded/wake relaxation | Causal relaxation suppressing high-gradient quasi-static response while preserving galaxy limit |

S2 is admissible but only a hypothesis. Predict healing length from microscopic
parameters before comparing it with a galactic transition scale.

### 7.4 Relativistic and lensing routes

| ID | Route | Required test |
|---|---|---|
| L0 | Pure conformal metric | Control expected to fail independent lensing |
| L1 | Disformal/universal metric | Both potentials, matter/light geodesics, PPN, GW speed |
| L2 | Aether/vector contribution | Reduced scalar/vector potentials and preferred-frame PPN |
| L3 | Emergent condensate metric | One covariant metric for matter/light; no birefringence or EP failure |

No lensing route advances if appended only to repair a post-fit deficit.

### 7.5 Topology, winding, moduli, and acceleration scale

| ID | Route | Decisive work |
|---|---|---|
| T0 | Passive `T^3` stress | Retain CBR-001 control; no persistent `13/12` |
| T1 | Dynamical shape/volume moduli | Kinetic terms, potential, normalized modes, stability, stress coupling |
| T2 | Smooth winding/circulation | Complete energy from declared action with amplitude relaxation/zero modes |
| T3 | Defects/vortices | Finite-core solutions, energy, nucleation, network evolution, gravitational stress |
| T4 | Dynamic scale attractor | Starting without `L=c/H`, test whether evolution drives a modulus toward `H` |
| T5 | Blind acceleration-coefficient audit | Derive `C_chi(H,q,moduli)` before comparing `cH`, `cH/2pi`, `sqrt(1-q)cH/2pi`, alternatives |

For observations keep `a0_obs=C_obs^2 a0_internal`; bare `a0_internal` cannot
be compared directly while `C_obs` is unresolved.

### 7.6 Wake routes

| ID | Route | Decisive work |
|---|---|---|
| W0 | Static control | State what time-independent response cannot explain |
| W1 | Hyperbolic wake | Positive Hamiltonian, retarded Green function, cone, source, damping, static limit |
| W2 | Relaxation/memory | Entropy-compatible kernel and causality/Kramers-Kronig checks |
| W3 | Defect-carried wake | Link to derived vortex/defect stress, not illustrative offset halo |

Cluster-offset claims remain downstream until a route predicts a time-resolved
lensing mass map.

### 7.7 Reservoir and syntropic throughput

| ID | Route | Decisive work |
|---|---|---|
| R0 | Regular no-throughput control | Set the coupling/current exactly to zero at the action/closure level and also take the interacting-branch limit; require agreement and conserved matter+plenum with `Q_syn=0` |
| R1 | Irreversible constitutive vector | Explicitly phenomenological covariant closure; entropy production, coefficients, frame, all transfer four-vectors, pressure/entropy closure, and causal perturbations |
| R2 | Action-coupled reservoir | Vary one off-shell `S[g,psi_m,Psi_p,Psi_R]` to obtain all field equations, `T_m`, `T_p`, `T_R`, `Q_mp`, `Q_syn`, and total conservation |
| R3 | Topology-locked throughput | Modulus/winding-to-current mechanism without `H0`, creation rate, `13/12` |
| R4 | Early phase/decoupling | Parent-action transition, products, momentum transfer, BBN, perturbation matching |

Keep `Q_mp`, `Q_syn`, and condensate-number source `S_N` distinct unless one
action derives their relationship.

For every nonzero-current route, the Bianchi/Noether identity is only the
total-conservation check. It does not select the constituent exchange currents.
The route must additionally demonstrate a nonsingular zero-coupling limit,
the physical positivity domain of all backgrounds, absence of ghost/gradient
instabilities after constraint reduction, finite transfer coefficients, and
stable background and perturbation eigenmodes. A background-only kernel such
as `Q propto (1+z)^(-n)` remains phenomenological until this contract closes.
Do not divide by an interaction coefficient before comparing the exact-zero
branch with the limit from nonzero coupling, and test whether a reshuffling of
the sector stress split changes the claimed current.

### 7.8 Cosmology and competitor tests

| ID | Route | Use |
|---|---|---|
| C0 | GR/ΛCDM plus inactive ITSM | Nested null control |
| C1 | Late reservoir exchange | Only after RES selects a stable covariant route |
| C2 | Pre-recombination transition | Only after R2/R4 action and matching |
| C3 | Dynamical topology/moduli | Only after T1/T4 stable homogeneous branch |
| C4 | Combined early+late ITSM | Last; same action/shared parameters, not stitched likelihood |

COS-001/PERT-001 must require:

- `H(a)` and all sector densities/pressures;
- `Q^0` and `Q^i` with transfer frame;
- density, velocity, entropy, and anisotropic-stress perturbations;
- initial and transition-matching conditions;
- `r_s(z*)`, baryon-drag `r_drag`, photon-diffusion `r_damp` separately;
- BBN and recombination `Delta N_eff`;
- CMB TT/TE/EE+lensing, BAO, SNe, matter power, full-shape, growth;
- baseline without SH0ES, then a separate local-calibration test;
- `Delta chi^2`, AIC/BIC, Bayesian evidence, residual tension.

For interacting-sector comparisons define, with the ITSM matter-sector sign
convention fixed before inference,

`delta_eff^m(z) = [dot(rho_m)+3 H rho_m]/[H rho_m] = Q_m/[H rho_m]`.

Do not identify a dark-matter--dark-energy fit parameter with `Q_mp` or
`Q_syn` until the action and component map justify it. Forward-model the
derived `delta_eff^m(z)` through the observables and compare at minimum against
`Q=0`, constant-`w`, CPL, and sign-changing controls. Record the momentum
transfer frame and test whether the inferred sign survives the extra
dark-energy freedom and Bayesian complexity penalty.

Use a nested control ladder rather than treating `delta=0` as LambdaCDM:
`delta=0` gives the corresponding noninteracting dark-energy model;
`w_a=0` then gives constant-`w`; and only `w_0=-1` supplies LambdaCDM within
that family. The underlying gravitational theory and its separate GR limit
must be stated independently.

DRMD/Hot-NEDE is a comparator for the microphysics-to-perturbations chain, not
an ITSM component.

## 8. Downstream observational programme

Observations constrain/reject routes after predictions are frozen; they do not
promote upstream gates.

| Gate | Preregistered minimum |
|---|---|
| DISK-001 | Manufactured, spherical, exponential-disk tests; periodic compensation; curl field; convergence; no SPARC first |
| STAT-001 | All usable SPARC; exclusions frozen; raw/nuisance controls; halo, Newtonian, AQUAL, `C=1`, `C=2/3`; held-out checks |
| SPARC X-Y | Reproduce signs, smoothing, sample accounting; target `g_trans/a0_eff`, not `X_trans(a0)` |
| SCR-001 | Cassini/PPN, ephemerides, lab fifth-force, pulsars, compact objects; like-for-like observables |
| LEN-001 | Galaxy/cluster lensing, Shapiro delay, slip, preferred-frame limits, and the separate `GW-PROP` and `GW-SGWB` contracts below |
| WAK/cluster | Time-dependent gas, galaxy, X-ray/SZ, temperature, shock, shear/lensing-profile, and centroid maps; freeze masses, impact parameter, encounter speed, viewing angle, gas profile/fraction, and time since pericentre before comparison |
| COS/PERT | Joint likelihood and posterior predictive checks from one frozen action/dataset manifest |

The gravitational-wave contracts are not interchangeable:

- **GW-PROP:** derive the reduced tensor/vector/scalar quadratic action,
  canonical modes, characteristics, speed, dispersion, damping, birefringence,
  polarization content, and source/detector coupling. Compare speed and
  arrival-time predictions with GW170817-type multimessenger bounds.
- **GW-SGWB:** only when a named ITSM mechanism produces a background, derive
  its source stress correlator or event population, production efficiency,
  canonical normalization, transfer functions, present-day
  `Omega_GW^p(f)`, spectral shape, and detector overlap response. A free-wave
  propagation equation alone predicts no stochastic amplitude. Map each
  physical mode through the action-derived matter vertex and detector metric;
  an acoustic condensate scalar is not automatically LVK's scalar metric
  polarization. Narrowband or anisotropic predictions require their matched
  searches rather than a power-law isotropic limit.

The merger-cluster control suite must contain collisionless CDM, elastic SIDM,
and a two-state inelastic SIDM comparator, with cross-system checks on El Gordo,
the Bullet Cluster, and the Sausage Cluster. El Gordo thresholds from a
competitor model constrain that model, not ITSM directly; an ITSM route must
freeze its own mass/separation/offset prediction before the data are unblinded.

### 8.1 Evidence-watch benchmarks integrated on 2026-08-25

These records sharpen tests but change no gate status:

| Record | Verified scope | Programme consequence |
|---|---|---|
| [Akarsu, Bulduk & Katirci, arXiv:2608.23447](https://arxiv.org/abs/2608.23447) | Formal two-fluid EMSG case study: Bianchi fixes total conservation, while constituent currents require an off-shell action or declared closure; its chosen nonzero-coupling closure has a singular GR limit | Strengthen A1/A8 and R1/R2; use as a closure-artifact adversarial test, not as an ITSM no-go theorem |
| [Yang et al., arXiv:2608.21938](https://arxiv.org/abs/2608.21938) | Phenomenological `rho_dm propto a^(-3+delta_0)` fit using DESI DR2 BAO, not full-shape data: a small negative `delta_0` is about `2.2 sigma` for constant `w`, falls below about `1.3 sigma` with CPL freedom, and Bayesian evidence favours LambdaCDM | Add convention-locked `delta_eff^m(z)`, nested constant-`w`/CPL/null controls, and full perturbation/complexity comparison; do not equate its dark-sector current or perturbation prescription with an ITSM current |
| [Valdarnini, arXiv:2608.21844](https://arxiv.org/abs/2608.21844) | The arXiv comment says accepted for ApJ; its HTML abstract quotes elastic `4--5 cm^2/g`, while the PDF abstract/conclusions use `4--6 cm^2/g`, plus inelastic `2--4 cm^2/g` and `V_th=1200--1600 km/s`; Eq. 10 activates up-scattering only for pair speed `v>2 V_th`; results are sensitive to weak-lensing mass, profile, centroid, and geometry uncertainties | Add a preregistered El Gordo comparator suite downstream of WAK/LEN; do not import its cross-sections or threshold as ITSM parameters or treat `740 kpc` as a universal ITSM threshold |
| [LVK, arXiv:2608.23477; LIGO-P2600217](https://arxiv.org/abs/2608.23477) | Official collaboration preprint, O1--O4c1 no isotropic detection through 2025-04-01; for a log-uniform amplitude prior, `Omega_GW(25 Hz) <= 2.0e-9`, `2.8e-9`, and `2.6e-10` for indices `2/3`, `0`, and `3`; updated mixed/pure tensor/vector/scalar limits are also prior/template dependent | Split propagation from stochastic production; compare only a derived spectrum using the same polarization, spectral, detector-response, and prior assumptions |

For the El Gordo comparator, preserve both levels of the paper's proposed
future discriminator: the abstract's approximate low-primary-mass and
`d_DM >= 740 kpc` warning, and the fuller combined conditions (including
centroid/offset uncertainties) used for particular fiducial simulations. Do
not collapse them into a theory-independent single-number falsifier.

For the LVK benchmark, store both log-uniform and uniform-amplitude-prior
limits and the exact search band/template. The quoted `1.4` gain is relative to
O1--O4a reprocessed with the new frequency cuts and varies from `1.3--1.5`
across templates/priors; it is not a universal sensitivity multiplier. Treat
GW170817 speed/arrival, transient dispersion/damping, stochastic amplitude,
and stochastic polarization as separate likelihood blocks.

## 9. Execution phases and review gates

### G0 — repair authority

Complete G0.1-G0.8 and freeze a truthful baseline. No route status changes.

### P1 — cheap adversarial screens

1. Reproduce the current null/control action.
2. Audit R5-P1 from its parent action; invalidate contact-only amplitude and
   pre-projection residue claims where unsupported.
3. Reclassify CBR-002 scale and Landau/healing claims.
4. Complete dimensional, sign, convention, source-provenance mutations.
5. Register hypotheses and kill criteria before calculation.

**RG1:** select at most two MAT routes, one UVIR alternative, and one screening
route for expensive work.

### P2 — microscopic and physical-mode derivations

Run A1-A6. Current-action priority is U1; new-action priority is a fair
M1-M5 comparison followed by at most two full reductions.

**RG2:** reject any route lacking a stable EFT domain or invariant signed
matter residue. Do not fit it.

### P3 — local gravity and relativistic completion

Run S0, selected screening, and L0-L3 before galaxy fitting.

**RG3:** only SCR/LEN-passing routes enter predictive galaxy/cosmology lanes.

### P4 — topology, wake, reservoir

Run T1-T5, W1-W3, R1-R4 with null controls. They may proceed in parallel but
cannot rescue a failed local force route by assertion.

**RG4:** select mechanisms only from action-level evidence.

### P5 — controlled observations

Run DISK, preregistered SPARC/X-Y, lensing, and wake/cluster tests. Unblind
coefficients only after predictions and exclusions freeze.

### P6 — coherent cosmology

Build COS/PERT equations and controls; implement a Boltzmann solver only after
one route passes analytic background/perturbation/stability requirements.

### P7 — publication decision

Hostile review, code-to-claim audit, independent reproduction, sensitive-data
audit, manuscript freeze, and public-surface synchronization. Negative/no-go
papers may publish independently.

## 10. Priority queue

| Priority | Work package | Reason |
|---|---|---|
| P0 | G0 authority/evidence repair | Truthful baseline required |
| P1 | U1 quartet classification | Current-action viability blocker |
| P1 | R5-P1 hostile audit plus M1-M5 A0-A2 comparison | MAT critical path/contamination source |
| P1 | Blind `a0_internal`/`C_obs` audit | Prevent target-derived geometry |
| P2 | Screening controls and S2 admissibility | Solar-System survival mandatory |
| P2 | Lensing/relativistic admissibility | Conformal force insufficient |
| P2 | T1/T2 moduli/winding | Core identity and independent falsification |
| P2 | RES R1/R2 development | Required for syntropic cosmology |
| P3 | DISK and SPARC/X-Y methods | Useful Lane B; cannot unlock MAT |
| P3 | COS/PERT acceptance contract | Defines burden without inventing sector |
| P4 | Full likelihoods/public claims | Only after upstream gates |

## 11. Resource discipline

- Highest/Tier-1: bounded action, constraint, mode, amplitude, stability, and
  gate-decision work.
- High: architecture, hostile review, route comparison, solver design,
  release-critical audits.
- Medium: deterministic reruns, hashes, status propagation, formatting.
- Prefer analytic no-go screens before scans/MCMC.
- Stop on a hard kill criterion and write the negative result.
- Do not mix scientific and governance changes in one commit.

## 12. Definition of done

### Successful-theory outcome

One action passes A0-A10: healthy physical modes, invariant residue, local
gravity, lensing/GW, coherent cosmology, preregistered observations.

### Scientific no-go outcome

Every admissible route fails a named hard criterion, with reproducible failure
domains, without making the identity unfalsifiable.

### Bounded partial outcome

Surviving pillars, retired mechanisms, and publishable negative/methodological
results are clearly separated from unresolved ITSM claims.

No script `PASS_*`, fit gain, or attractive narrative is completion by itself.

## 13. Immediate next checkpoint

Execute **G0 only**:

1. non-destructive workspace/evidence manifest;
2. contradiction ledger for promoted claims;
3. recompute modified evidence/sidecars from corresponding code;
4. exact keep/repair/quarantine dispositions;
5. normalize `active_research.md` and queue only after review.

Do not begin a new physics derivation or commit the dirty tree until this
checkpoint establishes which artifacts are trustworthy.
