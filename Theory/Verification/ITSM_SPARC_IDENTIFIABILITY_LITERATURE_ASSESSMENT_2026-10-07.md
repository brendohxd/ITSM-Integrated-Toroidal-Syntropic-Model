# SPARC identifiability: literature assessment and independent-test plan

Date: 7 October 2026 (Australia/Perth). Result ID: `R9-SPARC-LIT-20261007`.
Claim status: **Conditional methods control**. `review_status=DEFERRED`,
`Rule9_cleared=false`, `physics_pass=false`, `gate_effect=NONE`.

## Decision

Retain the gas-rich dwarf residual as a question worth testing. Do not adopt
compactness as a physical coupling, interpret the result as a MOND rejection,
or use it to justify an ITSM observational fit. The next discriminating work
is a resolved-kinematics and catalogue-provenance control, followed by a
prospective test on galaxies not used to select the hypothesis. MIGHTEE and
lensing are later tests with distinct selection and forward-model requirements.

The present task is locally complete as a source assessment, partial raw-table
replay and implementation-ready research plan. The independent external test
has **not** been performed.

## External evidence and what was actually checked

[Sosna, arXiv:2608.08945v1](https://arxiv.org/html/2608.08945v1), submitted
9 August 2026, audits structural corrections under a fixed empirical RAR.
Its main conclusion is non-identifiability in the full sample. Its secondary
gas-rich, low-acceleration residual has an unresolved physical interpretation.
Quality dependence, conservative rank controls and uncertain pressure support
limit the inference. The claimed observational floor is protocol-specific;
it is not a universal detection limit. The paper's hierarchical fits use
maximum likelihood, rather than Bayesian posterior sampling.

The paper's main text, methods, conclusions and appendices were read. Its
[v20 Zenodo archive](https://zenodo.org/records/21856110) was retrieved through
the API after browser retrieval failed. The downloaded ZIP matches Zenodo's
published MD5. Its two MRT-table hashes match its README. Selected scripts and
plain-text results were inspected; no downloaded Python was executed and no
pickled arrays were loaded.

An independently authored parser and numerical control rebuilt galaxy
quantities from the archived ASCII MRT tables. This establishes a partial
reconstruction from that archive, not an independent confirmation of the raw
observations or a replay of every statistic in the paper.

### Locally measured anchors

Script: `Analysis/LiteratureControls/sparc_identifiability_anchor_audit_20261007.py`.
Receipt: `.local/itsm-context/sparc-identifiability-20261007/parent_anchor_replay_v2/summary.json`.
The process exited zero. The optimizer recognizes 11 passed checks, zero failed
checks and zero unknown checks. These checks concern parsing, anchor agreement,
a structural identity and multiplicity-adjustment arithmetic; they do not
close a physics gate. NumPy 2.3.5 and SciPy 1.16.3 were already installed.

| Quantity | Parent reconstruction |
|---|---:|
| Catalogue galaxies / selected galaxies / retained points | 175 / 126 / 2,709 |
| Low-acceleration subgroup | 63 galaxies |
| Raw low-group compactness correlation | `r=0.4638824574934208`, `p=0.00012856660241515513` |
| Low-group partial correlation after uniform 8 km/s device and Q, point count, mass, inclination-error controls | `r=0.299210474955674`, `p=0.021328342926227425`, 57 degrees of freedom |
| Full-sample structural-proxy MSPE / mass-only MSPE | `0.9861699712782175` |
| Full-sample structural-proxy MSPE / quality-only MSPE | `1.2200517334434742` |
| Low-group structural-proxy MSPE / mass-only MSPE | `0.942004710441965` |
| Low-group structural-proxy MSPE / quality-only MSPE | `1.0238493686077836` |
| Canonical BH-adjusted p from the archived 27-test table | `0.03594375` |

MSPE ratios below one favour the structural proxy. The small low-group gain
against mass does not establish a gain against data quality: its error is
approximately 2.4 percent higher than the quality baseline. No uncertainty on
these predictive differences was estimated here. The uniform-dispersion
addition is a sensitivity device, not a measured per-galaxy correction.
The BH computation reuses the author's p-values and checks their adjustment
arithmetic only; it does not independently validate all 27 tests.

### Limits exposed by inspection and reconstruction

1. The archived `cv.py` predicts mean residuals with a straight line in
   log compactness. It does not fit the nonlinear multiplicative M2 law inside
   every training fold. The replay explicitly labels this **linear-proxy
   leave-one-galaxy-out cross-validation**. A prospective experiment must
   specify which of these two models it tests.
2. `MASTER_RESULTS_FROZEN.json` and `MASTER_RESULTS_AUDIT.json` are byte-identical.
   Identical bytes do not establish independent generation. The parent replay
   supplies fresh computation for selected anchors only.
3. The primary controlled effect is small and sensitive to the error model.
   Proxies for kinematic difficulty are not measurements of pressure support.
4. The source median split was reconstructed using all 126 galaxies. It is a
   descriptive subgroup definition, not an untouched external validation set.
5. A fixed empirical acceleration scale enters the reconstruction. It is
   neither an independently derived ITSM coefficient nor evidence for a
   particular `a0(z)` history.

## A structural degeneracy that can be proved directly

Use logarithms of dimensionless quantities relative to fixed reference units:
`m=log(M/M_ref)` and `r=log(R_eff/R_ref)`. Define
`lambda=GM/(R_eff c^2)` and
`s=log[(M/(pi R_eff^2))/Sigma_ref]`. Then

```text
ell = log(lambda) = m - r + constant
s = m - 2r + constant = 2 ell - m + constant.
```

Let `P` remove the intercept and mass by linear least-squares projection on
the same galaxies and with the same weights. Since `P m=P 1=0`,
`P s=2 P ell`. Their Pearson partial correlations with any nondegenerate
residual are therefore identical, regardless of the underlying mechanism.
This equality requires the same mass and radius definitions; it need not hold
for independently measured definitions, nonlinear controls or rank transforms.

The parent reconstruction gives partial `r=0.30128755858436934` for compactness
and `r=0.3012875585843686` for surface density, a difference of
`-7.216449660063518e-16`. This numerical agreement checks an algebraic
degeneracy. It cannot select compactness over surface density, or distinguish
potential-depth physics from another dependence on the same mass-size axis.

Dimensions are explicit: `[G]=L^3 M^-1 T^-2`, so
`[GM/(R c^2)]=1`, `[M/(pi R^2)]=M L^-2` and `[V^2/R]=L T^-2`.
The reconstruction converts km/s squared to m/s squared with `1e6` and kpc to
metres with `3.0856775814913673e19`. Its gas-velocity column already contains
helium; applying another 1.33 factor there would double count it. The 1.33
factor is used separately for catalogue H I mass.

## Data combinations and their readiness

| Input | Verified availability or result | Use and present limit |
|---|---|---|
| LITTLE THINGS | Oh et al. publish resolved rotation curves for 26 dwarfs; CDS exposes catalogue and rotation-curve tables. | First pressure-support/pipeline comparison. Determine object and observation overlap before calling anything independent. Direct CDS text download failed TLS verification; no TLS checks were disabled. |
| MIGHTEE RAR, 2025 | Published analysis uses NUTS/Hamiltonian Monte Carlo; public spectral cubes are linked, while other underlying products are available by author request. | Independent survey selection and resolved stellar masses. It assumes pressure support negligible for its relatively fast rotators, so it does not directly settle the slow-dwarf systematic. |
| MIGHTEE mass models, 2026 | Published/accepted analysis presents 20 galaxies and examines fixed versus spatially varying mass-to-light ratios. | Useful nuisance-model comparison. Do not add its sample size to the 19-object RAR sample without matching object IDs. |
| Joint kinematic/weak-lensing RAR, 2024 | Published study extends the acceleration range using consistently estimated stellar masses and isolation cuts. | Later cross-scale test. Different selected populations and projected observables prevent treating it as a direct dwarf-residual replication. |
| WALLABY pilot DR2 | Official public release provides H I products and a resolved kinematic subset. | Candidate source of new galaxies; audit resolution, dispersion modelling, distances and completeness before inference. |

Primary sources: [LITTLE THINGS paper](https://arxiv.org/abs/1502.01281),
[CDS catalogue](https://tapvizier.u-strasbg.fr/viz-bin/VizieR-3?-source=J%2FAJ%2F149%2F180),
[MIGHTEE RAR](https://academic.oup.com/mnras/article/541/3/2366/8182195),
[MIGHTEE 2026 mass models](https://arxiv.org/abs/2603.16992),
[joint lensing RAR](https://arxiv.org/abs/2310.15248),
[official WALLABY release](https://wallaby-survey.org/data/data-pilot-survey-dr2/).

Two additional 2026 preprints provide conveniently unified catalogues:
[438 survey entries](https://arxiv.org/abs/2604.13489) and
[129 dwarf/irregular entries](https://arxiv.org/abs/2605.22163).
They are discovery indexes requiring verification against original releases.
The second explicitly distinguishes only 26 full multi-point curves from
103 single-ring/profile-width estimates. A larger row count does not supply
the resolved information needed here; duplicate objects and metadata-only
entries must be removed from any purported validation sample.

For posterior methodology retain [Desmond's joint SPARC HMC analysis](https://arxiv.org/abs/2303.11314).
It is older, but directly treats correlated galaxy nuisance parameters.
A simple algebraic RAR is also not every implementation of MOND:
[the MOND/Solar-System analysis](https://academic.oup.com/mnras/article/530/2/1781/7641422)
explains its limits in modified-gravity settings. Rejection of an exact local
empirical relation must not be broadened into rejection of all MOND theories.

## Prospective experiment contract

This is a proposed methods experiment; it has not been run or externally
preregistered. Freeze the final data manifest and choices before seeing its
target residuals.

1. **Build a provenance and overlap table.** Resolve aliases using coordinates,
   source observation IDs and original references. Record beam, ring count,
   velocity/dispersion profiles, surface-density profiles, distance posterior,
   inclination posterior, stellar-mass model and existing drift treatment.
   Identify raw rotation, corrected circular speed and model-derived halo
   quantities separately. An overlap object tests measurement reproducibility;
   it cannot serve as an independent galaxy-level validation object.
2. **Test measurement effects first.** Compare common galaxies at a common
   distance, inclination and radius convention. Use measured dispersion and
   the declared dynamical approximation; retain its geometry and equilibrium
   limitations. Never apply drift a second time to corrected circular speeds.
   If only a constant dispersion is available, report a sensitivity envelope
   and keep the physical interpretation open.
3. **Freeze the hypothesis and population.** Choose linear residual–structure
   prediction or nonlinear M2 explicitly. Use the existing SPARC threshold
   as a fixed descriptive transfer threshold, or derive a new threshold on
   training data alone. Freeze gas-fraction and resolution criteria from
   inputs, independently of fit outcomes. Check whether external objects
   occupy the relevant mass, surface-brightness and acceleration range.
   If coverage is inadequate, return `INCONCLUSIVE_COVERAGE`.
4. **Infer jointly.** A suitable hierarchical model has global empirical RAR
   parameters and structural effect, galaxy-specific distance/inclination/
   stellar-mass uncertainties, measured dispersion uncertainty, within-galaxy
   covariance and a declared intrinsic-scatter component. Fit baseline and
   structural models with the same nuisance priors. HMC/NUTS is a candidate
   sampler once likelihood differentiability and diagnostics are verified;
   no sampler installation or run is part of this assessment.
5. **Predict without leakage.** Hold out complete galaxies and, where useful,
   whole surveys. Select transformations and hyperparameters inside training
   folds. Compare to RAR-only, mass-only, quality-only and hierarchical
   nuisance controls. Score held-out predictive density and calibrated
   coverage; use galaxy-level uncertainty on predictive differences. A
   correlation p-value or in-sample BIC is not that predictive comparison.
6. **Freeze rejection and inconclusive outcomes.** If the effect disappears
   under resolved pressure support, record a kinematic explanation. If it
   fails the strongest predictive baseline, record no demonstrated structural
   predictive gain. If it survives on genuinely new, appropriately selected
   galaxies, record an empirical secondary dependence with its uncertainty;
   assigning it to a particular physical theory requires that theory's
   independent prediction. Insufficient power, unresolved covariance or
   incomplete dispersion data produce an inconclusive result.
7. **Advance to lensing only with a forward model.** Model the actual projected
   lensing observable, baryonic gas, isolation, satellite contamination and
   sample selection. A rotation-curve acceleration substitution does not
   supply a relativistic metric or a lensing prediction.

## ITSM authority and inherited holds

The live dashboard retains `DISK-001=METHODS_ONLY`,
`STAT-001=NOT_STARTED_AS_CLOSED_GATE`, `LEN-001=OPEN`, `MAT-001=BLOCKED`,
`UVIR-003=IN_PROGRESS`, `K_Q=NOT_DERIVED` and `V=NOT_COMPUTED`.
Master Tests 1–3 and the conditional R4C1 continuation remain the owning
upstream programme. Its observational prediction tests require action-derived
weak-field, background, stability and matching inputs. This work neither
supplies nor numerically reuses a provisional R4C1 prediction.

`PROCEED_PROVISIONALLY` applies to the completed literature/methods assessment
and later scoped measurement diagnostics. An action-derived ITSM MCMC or
lensing fit remains `HOLD_SUBSTANTIVE`; absent force/metric inputs are a
scientific prerequisite, not merely deferred review. No gate, manuscript,
public website, provider setting or model session is changed by this report.

Sources of authority read in full: `GEMINI.md`,
`Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md`,
`Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md`,
`Theory/Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md` and
`docs/ITSM_CONTEXT_OPTIMIZER.md`. Relevant dashboard/register sections were
read, rather than claiming a full read of those longer records.

## Provenance and reproducibility limits

| Artifact | SHA-256 |
|---|---|
| Downloaded v20 ZIP | `c6a48a834d61c8fab8c2cd6a3539be03af5ffd84a0b611c1ec0fb43a63ca582c` |
| Retrieved arXiv HTML | `6d32937fd687767c9962e9f3231894a2ec5f72cbc56cf29918c2552fd6383ecf` |
| Archived galaxy MRT | `5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243` |
| Archived mass-model MRT | `9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c` |
| Parent audit script | `e6d3b201b03558a09b6ffd06aeeac18878fc227d6cc58f534b0f9705f0a68945` |
| Parent v2 receipt | `5d6fb9e173dd92ca48a8106ad55c4f8c8c72ec2f5a8c0be6291bbe61d0d6f1e4` |
| Both archived master-results files | `9977ca787aed7d9314ef128c7b240d869290e3bfc50963489c619dcda0500292` |

Public source downloads, extracted material, command logs and numerical
receipts stay in ignored `.local/itsm-context/sparc-identifiability-20261007/`.
The script refuses to overwrite an existing final receipt. To replay it, copy
the script to an isolated working version and declare a new output directory.
Preserve the source hashes and record the new script hash.

History retained: sandboxed downloads failed before a permitted network retry;
CDS subsequently failed certificate verification. The first parser attempt
used advertised byte positions and failed on archival whitespace; the final
parser validates whitespace column counts. The first successful receipt used
string check statuses, which the optimizer correctly treated as unknown.
The v2 boolean-check receipt fixes that schema and reproduces the numerical
results exactly; the earlier receipt and script snapshot remain preserved.

No full nonlinear-M2 replay, Bayesian sampling, resolved dwarf correction,
external-data fit, survey power estimate, or ITSM dynamical solution is claimed.
The next useful work is the overlap/measurement-data manifest in step 1.
No model change is indicated for this bounded assessment; more compute or a
different model cannot replace the missing observational or physical inputs.
