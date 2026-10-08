# External evidence watch: reconciliation of the 6 October note

Assessment date: 7 October 2026, Australia/Perth.
Result ID: `R9-EW-20261007`. Status: **Conditional source assessment**.
`review_status=DEFERRED`, `Rule9_cleared=false`, `physics_pass=false`,
`gate_effect=NONE`. External reports are not ITSM gate authority.

## Disposition

Add the three papers to the external benchmark inventory. They supplement
[the SPARC identifiability assessment](../Verification/ITSM_SPARC_IDENTIFIABILITY_LITERATURE_ASSESSMENT_2026-10-07.md),
whose source bytes remain unchanged. They do not displace the live Master
Tests 1–3/R4C1 programme or establish the physical inputs for ITSM fitting.

The attachment was read in full. Titles, authors, arXiv versions and abstracts
were checked against primary sources. Selected SPARC methods/results and
Lambda-LTB likelihood/conclusion sections were inspected. The cluster item
is an abstract-level screen. No new posterior, cluster solution, cosmological
likelihood or source-code reproduction is claimed.

## EWO-20261007-SPARC: full-sample NFW/MOND comparator

[Da Silva, arXiv:2610.05871v1](https://arxiv.org/html/2610.05871v1),
submitted 5 October, reports 175 galaxies with nuisance-parameter MCMC.
The quoted BIC tallies (96/79, then 86/89 with the concentration prior),
concentration offset and population acceleration/scatter agree with the
abstract. The 0.14 dex is observed scatter, not an intrinsic-scatter detection.
The author explicitly attributes much apparent per-galaxy acceleration
variation to nuisance degeneracy. This does not establish physical variation.

Methods use 0.1-dex stellar-mass priors, truncated distance/inclination priors,
an algebraic MOND law and MAP-based BIC. Bayesian evidence is not computed.
Reported chain-length checks on a subset are not per-fit convergence diagnostics.
The public Zenodo record currently lists one PDF, rather than executable
reproduction materials; code/results are described as available by request.
Its publication-date metadata and manuscript date are 5 September, while
the arXiv submission is 5 October: a new arXiv listing does not prove that
the work first became public on that date.

**Assessment and permitted next work:** retain this as a candidate benchmark,
then audit its likelihood coordinates, priors, chain diagnostics, parameter
counts and tables before numerical comparison. Separate reproduction of its
empirical comparator from an independently designed hierarchical universality
test. The same SPARC observations cannot become a new independent validation
sample through reanalysis. Keep gas-rich dwarfs and massive, bright/bulged
galaxies as prespecified diagnostic populations, with outcome-independent
quality reporting and common nuisance treatment.

The present ITSM coefficient is not established by this external paper.
`a0=cH0/(2 pi)` is a historical candidate requiring the blind coefficient
audit; the `2/3` projection and saturation law also require their owning
derivations. A residual correlation does not derive them. Determine the
coefficient independently before exposing it to the target fit.

## EWO-20261007-RG: cluster population comparator

[Primignani et al., arXiv:2610.06841v1](https://arxiv.org/abs/2610.06841),
submitted 5 October, reports 74 CIRS clusters combined into three
velocity-dispersion stacks. It uses MG-MAMPOSSt and jointly inferred baryonic
profiles; the quoted vacuum-permittivity range of 0.04–0.37 and gas-model/
disturbance dependence agree with the abstract. This is not 74 independent
per-cluster demonstrations of one fixed gravity parameter.

**Assessment and permitted next work:** add RG as a competitor to the existing
population programme. Prepare a data/selection manifest including original
member velocities, membership criteria, gas/stellar profiles, stack scaling,
anisotropy prescriptions and equilibrium cuts. Reproduce stack construction
before comparing gravity models. A stacked fit and per-cluster posterior fit
are different experiments; include object/stack covariance and the same
selection for all competitors. Disturbed mergers need a separate dynamical
model rather than automatic reuse of an equilibrium likelihood.

The requested ITSM solution needs a specified admissible field equation,
matter coupling, boundary conditions and velocity-dispersion forward model.
Those cannot be supplied by renaming RG permittivity as plenum response.

## EWO-20261007-LTB: expansion/inhomogeneity degeneracy control

[Zhang and Zhang, arXiv:2610.05729v1](https://arxiv.org/html/2610.05729v1),
submitted 5 October, finds comparable distance fits for Lambda-LTB and
`w0waCDM`; kSZ restricts the permitted profiles. The quoted roughly
300 Mpc/h, 10-percent overdensity is an allowed configuration, not a detected
structure. The likelihood uses compressed Planck constraints, not a full
Planck spectrum fit. "No preference" concerns comparison with dynamical
dark energy; it must not be paraphrased as no preference relative to
Lambda-CDM. The reported comparison with Lambda-CDM depends on the SN sample.

**Assessment and permitted next work:** add Lambda-LTB to the cosmological
control inventory, retaining its radial profile, observer placement,
perturbative validity and compressed-CMB assumptions. Freeze which SN
compilation, kSZ constraint, covariance, selection and evidence priors enter
each comparison. Distinguish a kSZ upper-bound exclusion from a full kSZ
likelihood. A background-distance fit alone does not determine growth,
Weyl-potential correlations or a galaxy-selection-aware lensing observable.

The attachment's `G_cosmo`-glitch comparator needs a specified published model,
parameterization and likelihood contract before inclusion. An undefined label
is not an executable competitor. ITSM growth/lensing/kSZ prediction remains
dependent on its background, exchange perturbations and metric equations.

## EWO-20261007-EUCLID: release-date correction

The live [Euclid NASA Science Center DR1 page](https://euclid.caltech.edu/page/euclid-dr1)
lists **12 November 2026: DR1 Foundation**, and **mid-2027: complete DR1**.
Older [ESA timeline material](https://www.cosmos.esa.int/web/euclid/timeline)
still has 21 October 2026, explicitly tentative. Direct browser access to that
ESA page returned HTTP 451, so its current revision was not confirmed.
The attachment's October deadline should not be retained as a confirmed
current schedule, and a foundation release must not be equated with complete
cosmological likelihood availability.

**Permitted preparation:** freeze hypotheses, selection, analysis procedures
and rejection conditions before consulting the relevant target products.
Numeric ITSM predictions require an independently supplied physical model;
an approaching release date does not justify inventing them. No Euclid DR1
cosmological result was analysed here and no future monitoring was scheduled.

## Reconciled work order and boundaries

1. Preserve the owning upstream action, well-posedness/stability, weak-field
   and blind-coefficient/matching programme. `MAT-001=BLOCKED`,
   `UVIR-003=IN_PROGRESS`, `K_Q=NOT_DERIVED`, `V=NOT_COMPUTED`.
2. In the separately permitted methods lane, use the new full-sample paper
   as a benchmark candidate and extend the existing overlap/kinematic manifest
   to independently measured distances and stellar masses. Catalogue coverage
   and pressure-support measurements are still needed for the dwarf test.
3. Prepare the cluster-stack and cosmological competitor contracts, with
   explicit inputs and excluded uses. Preserve `DISK-001=METHODS_ONLY`,
   `STAT-001=NOT_STARTED_AS_CLOSED_GATE` and `LEN-001=OPEN`.
4. Run action-derived ITSM prediction comparisons only when their required
   equations and controlled domain exist. A deliberately assumed empirical
   coefficient may support a separately named conditional control, never a
   claim of independent coefficient derivation or an ITSM gate pass.

`TR-001-v3`, `SPARC-001`, `Cluster-001` and `DESI-001` in the attachment are
proposed labels, not newly admitted canonical gates. The external note's
priority list is reconciled with the live programme rather than used to
bypass its substantive prerequisites. `PROCEED_PROVISIONALLY` applies to
this completed source assessment and evidence preparation. Dependent ITSM
observational fits remain `HOLD_SUBSTANTIVE` until the missing physics is
supplied; no review panel is required merely to continue methods research.

No new provisional R4C1 numerical result was reused. Any later use of the
earlier parent SPARC reconstruction inherits `R9-SPARC-LIT-20261007` review
debt. This document adds source dispositions and proposed tasks, not fitted
parameter values or source-confirmed physical results.

## Source snapshots and verification

The ignored manifest
`.local/itsm-context/evidence-watch-reconciliation-20261007/sources.json`
records URLs, retrieval timestamps and SHA-256 values. It includes five
retrieved public sources plus the attachment digest. Source pages were
downloaded for provenance; download success does not validate their science.

| Source snapshot | SHA-256 |
|---|---|
| Da Silva arXiv HTML | `7923740aaa481d58b712221eabf6ae4fc977f59671759c53fb8aff6affa1d0c8` |
| RG arXiv HTML | `692ca018953dfe535fd3499236ca28753417704fdd6f5b83df3a4284d3883a1b` |
| Lambda-LTB arXiv HTML | `946520a9bfcfe6181548b9c1d0ae62f3e057c1185078928411bfa346282fef1f` |
| NASA Euclid page | `6449e803d9156e1e5b3d108e8d7d28db3d9c9468847f640e3cfea0d594763732` |
| SPARC Zenodo metadata | `291a09cb3491779ae2d17cc8a65b6088fa23670c16507d7d57d967eb29d773ef` |
| User attachment | `2ab2a04f255645dacf76c05704cb53e5400f4b29bc1b88e08cdd967f9703d4ad` |

The mandatory governance files remain hash-identical to their previous full
reads. No fits, model-provider dispatch, runtime reconfiguration, manuscript
change, commit, push or publication occurred. No model change is indicated
for this source reconciliation.
