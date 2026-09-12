# ITSM Tier-1 route-testing and recovery programme

**Version:** 1.2-proposed

**Date:** 2026-08-23

**Last evidence integration:** 2026-09-06 (six downstream benchmarks; no gate change)

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
| U5 | Covariant phase-space rewrite of frozen PKM1-P0 | Presymplectic current and DOF vs existing ADM count | Rank comparison written; no new kinetic term | Split-artefact “fixed” by inserting operators |
| U6 | Cartan/teleparallel host of PKM1 identity | A0–A2 tetrad/Weitzenböck action or named incompleteness | Healthy GR+condensate DOF without extra force | Slogan torsion; second expensive parent without a decision |
| U7 | Truncated \(T^3\) Fourier/difference of P0-B | Mode-truncation rank table, two \(N\) values | Rank visible without \(L=c/H\) or winding-as-coupling | \(2\pi\) or cavity size imported to hit \(a_0\) |

U1 is the highest-value immediate Tier-1 physics task because the quartet lies
on the present action's viability path.

Cheap-screen activation (2026-09-04): U3 and M4 are authorized as P1
adversarial screens, not as a second expensive parent. U5–U7 are method or
host screens on the frozen PKM1-P0 control. Specs, kill criteria and lane
discipline are in
`Theory/Core/ITSM_CHEAP_SCREEN_ROUTE_ACTIVATION_2026-09-04.md`.
PKM1 A0–A6 remains the only expensive microscopic lane.

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

M4 is activated as a 2026-09-04 cheap screen on the live Track-A chart and
the PKM1-P0-B control. It is not a second expensive parent.

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

### 8.2 Evidence-watch benchmarks integrated on 2026-09-06

Primary arXiv records were checked on 2026-09-06. A duplicate six-record
source packet was reconciled against the same current records on 2026-09-12;
the existing rows were enriched in place and no duplicate tranche was added.
These additions change test requirements only; they do not supply an ITSM
derivation or change a gate.

| Record | Verified scope | Programme consequence |
|---|---|---|
| [LUX-ZEPLIN Collaboration, arXiv:2609.02823](https://arxiv.org/abs/2609.02823); [HEPData 182472 v1](https://doi.org/10.17182/hepdata.182472.v1) | Official collaboration preprint with a linked public data release: one event consistent with a `248 +/- 23_stat +/- 23_sys keV` nuclear recoil in `2.84 tonne-year`, with `2.6 sigma` global and `3.4 sigma` maximum local background tension; explicitly not a dark-matter detection | Add a falsification clause for the **pure particle-dark-matter replacement** version only. Derive any plenum-excitation recoil spectrum and target scaling, or predeclare that a statistically secure cross-experiment particle spectrum falsifies that pure version; one event does not do so |
| [Wang, Yu & Wu, arXiv:2609.03062](https://arxiv.org/abs/2609.03062) | For `Q=beta H rho_de`, using Planck/ACT CMB, DESI DR2 and DES-Dovekie with perturbations and a PPF treatment through `w=-1`, the interacting CPL result has `beta=-0.35^{+0.77}_{-0.62}` and improves the matched noninteracting CPL best fit by only `Delta chi2_int=-0.03`; its AIC is higher than the noninteracting CPL result. Restricted trajectories give model-dependent signs and growth | Strengthen the COS/PERT nested-null contract: derive `Q^mu` and `w_p(z)` from one action, evolve perturbations, and compare distances, `f sigma8(z)`, lensing and clustering. Report `Delta chi2`, AIC/BIC and Bayesian evidence against `Q^mu=0`. DESI cannot presently be cited as evidence for the Syntropic Source Vector |
| [Lagos & Wolf, arXiv:2609.04112](https://arxiv.org/abs/2609.04112) | A particular nonminimally coupled scalar-tensor model predicts `c_M=-0.5+/-0.2`, `Xi_0=0.88+/-0.05`, `n=3.2+/-0.3`, consistent with current GWTC-5 siren constraints within about `1 sigma`. Common `c_M` and CPL fits place the same physical model in `2.2 sigma` and `3.6 sigma` tension respectively, partly because stability cuts impose strong implicit priors | Add a distinct **GW-FRICTION** contract: derive `alpha_M(z)` and `D_L^GW/D_L^EM` from the surviving action before mapping to phenomenological parameters. Do not identify its fitted `n` with an ITSM exchange exponent or merge this test with GW speed/dispersion |
| [Lagos et al., arXiv:2609.03537](https://arxiv.org/abs/2609.03537) | The `z=0`-calibrated Shark semi-analytic model reports UV-luminosity-function agreement through `z=17`, stellar-mass-function agreement through `z=10`, and star-formation-rate-density agreement through `z=15`, attributing high-redshift burstiness to violent disk instabilities | Remove any uniqueness inference from bright JWST galaxies. A later ITSM test must beat a bursty-LambdaCDM comparator jointly in luminosity, stellar mass, star-formation rate and scatter, using a preregistered residual observable |
| [Euclid Collaboration, arXiv:2609.04192](https://arxiv.org/abs/2609.04192) | Simulation preparation paper compares density, mass, velocity-dispersion and excess-surface-density profiles to `5 r_500c`; low-mass `f(R)` cases differ by order `10%`, while other cases are often a few percent. Under simplified assumptions, detecting those comparator differences requires roughly `10^5` stacked haloes at `z=1.1` but a few thousand at `z<=0.5` | Add a dependency-locked halo-profile suite `rho(r), M(<r), sigma_v(r), DeltaSigma(R)` after a viable force/lensing action exists. Freeze ITSM's outskirts sign and estimate its own required stack; the quoted stack sizes are comparator-specific forecasts, not ITSM predictions |
| [TDCOSMO XXIX, arXiv:2609.03089](https://arxiv.org/abs/2609.03089) | JWST/NIRSpec resolved kinematics for three time-delay lenses have `6--11%` per-bin uncertainty, about `1.2%` average correlation, and reduce integrated-dispersion uncertainty from `3.7%` to `2.4%`; no new `H_0` result is reported | Keep time-delay-lens `H_0` separate in the coefficient audit. Do not insert it into `a_0=cH_0/(2*pi)` until the ITSM lens potential, kinematic maps, time delays and line-of-sight convergence are fitted self-consistently |

Immediate ordering remains upstream-first. The LZ and DESI records require
claim-firewall checks now; GW friction, JWST formation, Euclid halo profiles
and time-delay cosmography remain dependency-locked behind a surviving
matter/metric action. None is a reason to divert Max/Ultra work from
`MAT-001`, `UVIR-003`, the physical pole/residue, or the independent P2 audit.

### 8.3 Evidence-watch benchmarks integrated on 2026-09-08

Primary arXiv records first posted on 2026-09-04 were rechecked on
2026-09-12. The two Unite papers were revised on 2026-09-09, after the source
packet was prepared. The current v2 values below supersede the packet's
earlier significance figures. These additions change test requirements only;
they do not supply an ITSM derivation, change a gate, or displace TOP-X4 Plan
11.

| Record | Verified scope | Programme consequence |
|---|---|---|
| [Camilleri et al., arXiv:2609.05053v2](https://arxiv.org/abs/2609.05053) and [Lee et al., arXiv:2609.05321v2](https://arxiv.org/abs/2609.05321) | Unite combines Pantheon+ and DES-SN5YR into 2,884 likely Type-Ia supernovae with one analysis framework. With CMB and DESI DR2 it reports `(Omega_m,w0,wa)=(0.305+/-0.004,-0.861^{+0.044}_{-0.042},-0.60^{+0.17}_{-0.19})`, a roughly 30% smaller `w0-wa` confidence area, `3.3 sigma` MAP and `3.1 sigma` maximum-likelihood preference over flat LambdaCDM, but only weak Bayesian preference. The companion v2 host-mass audit moves the Unite-Pantheon+ subset from `3.4 sigma` to `4.0 sigma` MAP when its remeasured masses replace release masses, while the DES-SN5YR/DES-Dovekie subset is virtually unchanged. The Hubble diagram, likelihood, photometry and masses are promised upon journal acceptance, not yet public. | Prepare a versioned Unite likelihood adapter, but do not claim or run the fit until the public likelihood and covariance are available. Then refit action-derived `Q(z)`, `w_p(z)` and any defensible exchange exponent with `H0` and `r_d`, branching released versus remeasured host masses. Keep MAP/maximum-likelihood significance separate from Bayesian evidence. |
| [Zapata, Carrion & Garcia-Arroyo, arXiv:2609.05410](https://arxiv.org/abs/2609.05410) | Unreviewed three-author comparison using DESI DR2, Pantheon+ and Planck 2018. With CMB it reports `ln B_(LambdaCDM,EDE)=12.44+/-0.05` and `ln B_(LambdaCDM,CPL)=2.33+/-0.06`, favouring LambdaCDM even though two-dimensional contours show multi-sigma displacement. Its learned harmonic-mean evidence estimator was checked against UltraNest only for cheaper background-level fits. | For any surviving early-only, late-only or complete ITSM cosmology, require independently reproducible nested-sampling evidence with all priors and convergence diagnostics frozen. Report posterior displacement, `Delta chi2`, AIC/BIC and `ln B` together; never translate contour exclusion into model preference without prior-volume accounting. |
| [Zhang et al., arXiv:2609.04990](https://arxiv.org/abs/2609.04990) | Phys. Rev. D-accepted phenomenological study of `Q=3 H xi rho_DE`. In its continuity convention, `xi<0` means DE-to-DM transfer and is displaced from zero beyond 95% credibility in combined fits, but neither interacting model is favoured over LambdaCDM or CPL by `Delta chi2_min` and Bayesian evidence. For IPEDE, `H0` falls from `69.52+/-0.95` with CMB+DESI to `67.88^{+0.52}_{-0.53} km/s/Mpc` with DES-Dovekie added; representative `S8` values are about `0.63--0.69`. | Implement this model only as a sign-mapped control beside an action-derived ITSM exchange law. On identical data compare `H0`, `S8`, `f sigma8(z)`, `Delta chi2` and Bayesian evidence, and test the joint failure mode of losing high `H0` while over-suppressing structure. Do not transfer the sign of `xi` without mapping both continuity equations. |
| [Gray, Williams & Papadopoulos, arXiv:2609.04991](https://arxiv.org/abs/2609.04991) | Unreviewed methods paper using `gwcosmo`, not an official LVK result. A sampled redshift prior permits joint inference of cosmology, GW population and host-galaxy weighting while accounting for incomplete catalogues. Its partial GWTC-5 reproduction gives `H0=71.9^{+9.1}_{-7.5} km/s/Mpc` at 68% credibility, too broad for sharp discrimination. | Replace fixed host-luminosity weighting in the coefficient audit with sampled host-population hyperparameters and catalogue incompleteness. Propagate the full non-Gaussian `H0` posterior into any `a0=cH0/(2 pi)` calibration, independently of GW friction, stochastic production and GW170817-type propagation tests. |
| [Dent & Newstead, arXiv:2609.04673](https://arxiv.org/abs/2609.04673) | Short, highly provisional phenomenology fit to the single LZ high-energy event already registered in Section 8.2. An exothermic inelastic-DM spectrum can peak near 250 keV while avoiding the low-energy null; normalized to one event it forecasts about 4.5 signals in LZ's projected 1,000-live-day exposure. The empty high-energy sideband disfavors broad peaks, and extended-window XENONnT/PandaX-4T analyses provide multi-target tests. | Extend the pure-particle-DM-replacement falsification table with the 4.5-event forecast, high-energy sideband and cross-xenon spectrum. A consistent confirmed spectrum would challenge that pure replacement claim. Failure of this particular exothermic forecast rejects the competitor only and is not evidence for ITSM. |

No new SPARC rotation-curve result, merging-cluster constraint, direct JWST
high-redshift release, official DESI cosmological-parameter release, or
GW170817 propagation bound was identified in this tranche. The cosmology,
dark-siren and recoil tasks remain downstream and dependency-locked; they do
not outrank the active derivation route or the Section 8.4 SPARC audit.

### 8.4 Evidence-watch benchmarks integrated on 2026-09-10

Primary arXiv records posted on 2026-09-08--09 were checked against their
abstracts and, where needed, the full text. They change test requirements only.
They do not derive an ITSM mechanism, promote a gate, or displace the active
TOP-X4 Plan 11 calculation.

| Record | Verified scope | Programme consequence |
|---|---|---|
| [Bian et al., arXiv:2609.08536](https://arxiv.org/abs/2609.08536) | Unreviewed four-author symbolic-regression methods preprint. From 175 SPARC galaxies it retains 163 and 3,269 points, reports BIC preference for `K=3`, and identifies near-Newtonian, square-root and constant-floor relations. It reports `a0` near `1.2e-10 m/s^2` for gas-poor galaxies and `0.55e-10 m/s^2` for gas-rich dwarfs, with leave-one-galaxy-out RMSE gains of 2.8% overall and 7.3% for gas-rich dwarfs. Its `p<1e-34` is attached to the residual--gas-fraction correlation (`r=-0.42`), not a direct likelihood-ratio rejection significance for universal `a0`; the paper does not demonstrate the ITSM-required nuisance marginalization or within-galaxy covariance treatment. | Make this the highest-priority **observational SPARC/coefficient audit**, dependency-locked behind MAT/DISK rather than a current refutation. Reproduce the exact sample and `K=1,2,3` analysis using galaxy-level nested cross-validation; marginalize distance, inclination, stellar mass-to-light ratio, gas uncertainties and within-galaxy covariance. Compare the fixed-`a0` Plenum Shear hypothesis with the three-law mixture using held-out likelihood, AIC/BIC and Bayesian evidence. Report residual-correlation significance separately from model-rejection significance. |
| [Ballard et al., arXiv:2609.08573](https://arxiv.org/abs/2609.08573) | Unreviewed nine-author analysis of the double-source-plane lens SDSS J0946+1006, submitted to MNRAS. HST imaging plus VLT-MUSE kinematics help constrain the internal multi-plane mass-sheet degeneracy. Combined with DESI BAO, the fiducial model gives `(w0,wa)=(-0.87^{+0.10}_{-0.11},-0.22^{+0.28}_{-0.25})`, less than one standard deviation from LambdaCDM. External convergence remains unconstrained, and the third-source-plane reconstruction is explicitly incomplete. | Add J0946 as a supernova-independent expansion and lensing test after LEN/COS prerequisites. Jointly fit the ITSM lens potential, stellar Jeans kinematics, HST images, MUSE dispersion, external convergence and source-plane distance ratios; test rather than assume whether an ITSM effective history requires phantom crossing. |
| [Argudo-Panes, Gonzalez-Fuentes & Gomez-Valent, arXiv:2609.10133](https://arxiv.org/abs/2609.10133) | Unreviewed 51-page covariant scalar-tensor analysis. The tested positive-coupling branch of `F(phi)=1+alpha phi^2` realizes phantom crossing while satisfying the paper's BBN and local-gravity tests; past `G_eff` deviations remain below about 0.3%, and the likelihood propagates varying `G` into supernova luminosity. The reported preference over LambdaCDM is about `2.14 sigma`, or `1.77 sigma` when the initial field is counted as an additional degree of freedom; some fine-tuning is acknowledged. | Crossing alone is not an ITSM discriminator. Derive `G_eff(k,z)`, `dot(G)/G`, PPN parameters and BBN limits from a surviving plenum action; include any action-derived `G` dependence of supernova luminosity; require simultaneous crossing, perturbative stability, Solar-System compliance and acceptable low-redshift growth. |
| [Adil et al., arXiv:2609.09261](https://arxiv.org/abs/2609.09261) | Unreviewed formal-theory preprint with no new observational fit. Of three reconstructed sign-switching histories, one has a smooth finite-redshift realization, one reaches a `C1` but non-`C2`, non-Lipschitz endpoint with nonunique evolution, and the exact ladder history requires distributional kinetic stress in the adopted one-field action. Its unretuned closure test has a maximum absolute `Delta Omega_phi` mismatch of about `0.16`. | Treat a fitted `Q(z)` or `w_eff(z)` as phenomenology until generated by a regular action. For any ITSM exchange history, test field-map existence, invertibility, differentiability, uniqueness, hyperbolicity and ghost/gradient stability, then forward-integrate from independently fixed initial data and publish the unretuned closure residual. |
| [Kihara et al., arXiv:2609.09729](https://arxiv.org/abs/2609.09729) | Unreviewed controlled N-body methods/test-case preprint submitted to ApJ, not an observational detection. For matched satellite-host simulations, increasing the velocity-dependent SIDM cross-section retains less dark matter from an initially cuspy NFW satellite but more from an initially cored Burkert satellite. The reversal is attributed to the direction of heat conduction and tidally accelerated gravothermal contraction. | Strengthen the downstream WAK/cluster comparator: freeze the same satellite mass, host, orbit and pericentric sequence, and test both cuspy and cored initial structures. Predict stellar structure, bound dynamical/lensing mass and plenum morphology after each passage; do not infer dark-matter-deficiency or ITSM uniqueness without initial-structure and tidal-history controls. |
| [Leonard et al. / DESI Collaboration, arXiv:2609.09340](https://arxiv.org/abs/2609.09340) | Collaboration-scale 49-author DESI Y1 measurement preprint, not yet a cosmological-parameter fit. The connected even-parity LRG four-point correlation function is detected at about `12--17 sigma` in full-sky analyses and about `15 sigma` with a cross-patch estimator designed to reduce mock--data covariance mismatch. Hemisphere, redshift and completeness selections were tested. | Add a dependency-locked nonlinear-structure acceptance test after COS/PERT exists: generate ITSM mock catalogues under the same LRG selection and survey mask, calculate the finely binned connected 4PCF and covariance, and require one parameter set to fit DESI two-point clustering, BAO and four-point structure simultaneously. |

The Bian et al. reproduction is first among the new observational-method tasks
because it directly probes whether one acceleration law is adequate. It remains
a preregistered comparator and coefficient audit, not permission to fit before
the ITSM matter vertex and disk field solution exist. The other five records
are dependency-locked acceptance tests. No new Bullet Cluster observation,
direct JWST release, GW170817 propagation limit, or official DESI cosmological-
parameter release was identified in this evidence-watch tranche.

## 9. Execution phases and review gates

### G0 — repair authority

Completed on 2026-08-25 with
`PASS_G0_AUTHORITY_REPAIR_NO_PHYSICS_PROMOTION`; authority is
`Theory/Core/ITSM_G0_AUTHORITY_REPAIR_REPORT.md`. This froze a truthful
baseline without changing a physics gate.

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
| P0 | G0 authority/evidence repair — completed 2026-08-25 | Truthful baseline frozen without physics promotion |
| P1 | U1 quartet classification | Current-action viability blocker |
| P1 | R5-P1 hostile audit plus M1-M5 A0-A2 comparison | MAT critical path/contamination source |
| P1 | Blind `a0_internal`/`C_obs` audit | Prevent target-derived geometry |
| P1 | Cheap screens U3/M4/U5 (then U7/U6 if named) | Parallel; cannot unlock PKM1 or MAT |
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

G0 is complete. The current operator-selected route is TOP-X4 `X4-S2F3` Plan
11. The static parity-even determinant and constant-background finite-charge
operator checkpoints are bounded completions only; both retain
`physics_pass=false` and `gate_effect=NONE`.

Execute one bounded **dynamic-state and subtraction checkpoint**:

1. construct the coupled time-dependent amplitude/phase mode system on the A1
   background without importing the static vacuum solver;
2. declare the Hadamard/adiabatic state and all subtraction terms;
3. test adiabatic-order convergence and the diffeomorphism/global-`U(1)` Ward
   identities;
4. report the renormalized state-dependent stress only if those checks close;
5. stop on failure or at the resulting hold/continuation decision.

Do not begin the coupled physical Hessian, parity/anomaly completion, A4,
Ultra, phenomenology, manuscript revision or publication in this checkpoint.
The binding scope is
`Theory/Core/Reasoning_Mode_Plans/11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION/PLAN.md`
and
`Theory/Gates/TOP-X4/TOPX4_S2F3_FINITE_CHARGE_VARIATION_CONTRACT_2026-09-09.md`.
