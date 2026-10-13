# P1/P2 local referee-style review and Grok reconciliation

Date: 9 October 2026. Review revision: 1. Scope: the current P1/P2
v0.2.0-rc3 artifacts, compared with the operator-supplied Grok review.

This is skeptical local author-assistance, not an independent journal referee
report, author proofreading, a Rule-9 clearance, or an acceptance recommendation
from a journal. The reviewing assistant previously contributed to this project;
an adversarial reread does not remove that limitation. No provider was dispatched.
The original manuscripts, PDFs, numerical outputs, and sidecars were not edited.

## Recommendation

Retain both narrowly scoped results, but make targeted revisions before a release
decision. Do not carry the Grok report's four alleged P2 transcription errors into
the current manuscript: they do not occur in the inspected rc3 PDF. Do not apply
its verdict on archived Thermodynamics v0.6.0 directly to the current v0.7.1 draft.
Neither model review establishes Tier-1 acceptance or independent review clearance.

P1 is a conditional scale/coefficient audit, not a geometric derivation of the
MOND scale. P2 is a static-stress control and a bounded negative result for a
declared instantaneous closure, not a complete semiclassical cosmology. These
standalone scopes need not solve every ITSM sector to be useful; their actual
claims do need sound mathematics, explicit assumptions, reproducible evidence,
and a defensible contribution beyond established literature.

## Exact reviewed artifacts

Paths below are relative to the ITSM repository. SHA-256 values were recomputed
after the review and agree with the starting artifacts.

| Artifact | SHA-256 |
| --- | --- |
| `papers/P1-Scale-Matching-Reconstruction/main.tex` | `4b0d0aefd22f81ea20057936ee7566f24eb12b9b49b2fb22bebdfdcc5a6f2510` |
| `papers/P1-Scale-Matching-Reconstruction/Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc3.pdf` | `d16a339e866358dbe448e7438b2e2e7e5e8fb1614cda7ed4ef1f1b4c380ca827` |
| `papers/P2-Rectangular-T3-Casimir/main.tex` | `4f5e587c4882cc5a1937819c19c5eea85d4c0a29f3c59f932060f168e5467396` |
| `papers/P2-Rectangular-T3-Casimir/Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Instantaneous-Closure-Control_v0.2.0-rc3.pdf` | `bbbfe121a3c91a47e29678b59aa43045b7d0e790bba3041adfa3fc6a6163a9e0` |

The supplied Grok attachment has SHA-256
`0a97d90c46eb5bc1c7b38647e99d4b2817539ff74502da8377ab74ade1c854e5`.
Its text was read through line 326. Its reported independent lattice extrapolation
has no accompanying executable/output artifact in the attachment and was not
treated as a separately verified replication.

## What was personally checked

- Complete P1/P2 TeX sources and bibliographies; every page of both PDFs,
  including rendered visual inspection (P1: six pages; P2: five).
- P2's disputed printed values and equations, against both PDF and source.
- The four P2 Appendix A artifact hashes, against the actual CSV/JSON files.
- The complete saved release-sensitivity receipt: 18/19, `FAIL`, including the
  exact failed threshold test. This receipt was inspected, not regenerated.
- Selected Stage-3B implementation sections governing the Hamiltonian branch,
  shear/shape evolution, Casimir fraction, and validation residuals; the complete
  threshold CSV. This was not a full fresh execution of CBR-001 or a complete
  code audit.
- Six fresh symbolic spot checks: field-rescaling invariance; the 13/12-to-3/38
  identity; fixed-de-Sitter required stress; and the small-source peak location,
  peak value, and required amplitude. All six returned true. These are algebraic
  checks, not a physics pass or an observational likelihood.
- Relevant primary sources: Planck 2015 topology, Edery's periodic-scalar
  benchmark, COMPACT 2024 and Negro et al. v2, and APS reviewer guidance.

No SPARC catalogue likelihood, full-domain lattice error analysis, curved-space
state evolution, external replication, or verified public immutable release
snapshot was produced by this review. The Zenodo page could not be inspected
through the web tool; that is a verification limitation, not evidence of absence.

## Grok objections reconciled with the current artifacts

| Allegation | Current rc3 PDF | Disposition |
| --- | --- | --- |
| P2 Eq. (3) prints rho = -0.837557 | Page 2 prints -0.837537 | Not present in this artifact |
| P2 Eq. (8) prints r-dot = r delta-dot | Page 3 prints r-dot = r delta | Not present in this artifact |
| P2 Eq. (9) uses total pressure | Page 3 uses total energy density, rho_total | Not present in this artifact |
| P2 defines N = -ln a | Page 3 defines N = ln a | Not present in this artifact |

This establishes disagreement with the reviewed artifact, not the reason for
that disagreement. An older input, extraction error, or unsupported model claim
cannot be distinguished without Grok's exact input files and their hashes.

Grok's package summary also needs a distinction: P1 does derive the invariant
combination C_obs = C_m^(3/2)/sqrt(C_IR). It does not derive its numerical value
as 2/3. Grok's later ledger makes this distinction correctly.

The Thermodynamics README identifies v0.7.1 as current and v0.6.0 as preserved
history. It explicitly records withdrawal of topology-implies-inflow, exact
entropy cancellation, heat-death avoidance, and acceleration claims. This review
did not freshly referee the complete v0.7.1 paper or the other two legacy essays;
their individual Grok rejection recommendations therefore remain unverified here.

## P1 findings

### P1-A: clarify intrinsic geometry in the circulation argument

Page 3 / source lines 262-280 introduces R = L/(2 pi), then calls c^2/R a
centripetal acceleration. A closed geodesic in a flat three-torus does not acquire
nonzero intrinsic centripetal acceleration just because it closes. Treating the
cycle as a circular trajectory imports an embedding or a separate physical
confinement assumption.

The period/frequency inconsistency remains available without that assumption:
for uniform speed, Gamma = cL implies v = c, while a cycle clock with angular
frequency H0 implies v = H0 L/(2 pi) = c/(2 pi). Keep that conditional clock
argument. Either remove the centripetal bullet or explicitly label it as a
circular-embedding comparison, not an intrinsic acceleration on flat T3.

### P1-B: identify the construction being tested and justify the contribution

The text refers to geometric proposals without giving a precise attributed
source for the complete (L, Gamma, omega) package. Identify an exact historical
construction, or explicitly present it as an author-defined hypothesis being
tested. A reader must be able to distinguish a meaningful correction from an
argument against an unspecified proposal.

The MOND coincidence, flat-torus geometry, and projector trace are established
ingredients. Explain what the combined normalization audit adds. A correct short
calculation is not by itself evidence of the novelty/significance a particular
journal requires. No journal acceptance probability was estimated here.

### P1-C: sharpen observational and normalization language

The Planck source supports R_i > 0.97 chi_rec for the cubic torus, with distinct
likelihood-ratio and matched-circle confidence statements. Name the statistic
used rather than treating all bounds as an unspecified high-confidence result.
The conversion to roughly six Hubble lengths assumes the stated background
distance to recombination; do not export it unchanged to arbitrary ITSM histories
or twisted manifolds.

The invariant C_obs is field-normalization independent, but if a0 is free the
spherical response determines the product C_obs^2 a0, not both factors
separately. Preserve the independent-scale assumption whenever C_obs is called
an observable coefficient.

Fresh arithmetic at H0 = 70 km/s/Mpc gives a0 = 1.0824013602391998e-10 m/s^2,
a_eff = 4.8106727121742207e-11 m/s^2 for C_obs = 2/3, and velocity ratio
0.816496580927726. The last quantity is an analytic conditional shift, not a
completed empirical rejection. The paper already appropriately excludes a new
catalogue fit; retain that boundary.

## P2 findings

### P2-A: separate perturbative Stage 3A from finite-amplitude Stage 3B

Page 4's scope bullet describes Casimir as a small perturbation. Table III and
the preserved threshold CSV instead identify four nonperturbative candidates
and one marginal candidate. Their maximum absolute Casimir fractions, relative
to total density as defined in the code, are approximately 2.536, 0.632, 0.273,
0.133, and 0.082 for r0 = 1.1, 1.25, 1.5, 2, and 3.

The inspected integrator reconstructs H from rho_BG + epsilon rho_C and the
shear Hamiltonian constraint; it does not simply hold H fixed throughout those
finite-amplitude runs. That is not itself an algebraic error. Explain the
distinction: perturbative de-Sitter control versus finite-amplitude evolution
of an assumed instantaneous constitutive law. Large-amplitude results are not
thereby validated as a controlled semiclassical quantum approximation.

### P2-B: retain the genuine convergence limitation without overstating it

The recorded failure is the r0 = 1.5 threshold changing from
0.6757299265902508 to 0.6756708783193345, relative difference
8.738442474237357e-5, versus the preregistered 1e-8 requirement. The recorded
classification remains transient and the tested no-attractor conclusion is
unchanged. Do not convert 18/19 to PASS or quote unsupported threshold precision.

Before treating threshold amplitudes as quantitative results, establish their
actual uncertainty. The inspected root objective uses maxima sampled on N_eval,
so peak-time/sample-grid convergence deserves attention alongside ODE tolerances
and source interpolation. This is a diagnostic recommendation, not a verified
cause of the present discrepancy. A qualitative negative-result note can
instead explicitly restrict its quantitative claims to the supported precision.

The Hamiltonian residual is evaluated after H is reconstructed from the same
constraint. It verifies algebraic consistency, not an independent integration
of the mean Einstein equation. Describe that boundary honestly; a separate
Raychaudhuri check would strengthen the reduced-system validation.

### P2-C: state the analytical obstruction with its exact assumptions

Constant q != 1 implies constant nonzero x and d ln r/dN = x. Consequently a
constant nonunit ratio cannot remain in a bounded shape domain indefinitely,
already at the kinematic level. The stress-decay argument is complementary,
but should not be presented as a general theorem over unbounded shape evolution.
The de-Sitter comparison also assumes continuing expansion with nonzero
asymptotic H; positivity of H alone is not the same assumption.

Preserve the tested finite-domain no-attractor result, the distinction between
static renormalized input and a dynamically renormalized state, and the missing
zero-mode/state and interacting sectors. None of those missing sectors is needed
to claim the limited numerical result actually demonstrated; they are needed
before extrapolating it into a general cosmological statement.

### P2-D: improve figure readability and literature positioning

All pages rendered without clipped equations or overlapping body text. Figure 3
on page 4 packs multiple trajectories into one column; its axis labels and panel
annotations are very small at final paper size. Reformat or enlarge it before
release. The plot issue is presentation, not a change in its data.

Edery's published periodic d = 3 benchmark is -0.837537, consistent with the
current rounded Eq. (3). Negro et al. v2 studies Casimir-induced anisotropic
expansion perturbatively and treats topology/scale phenomenologically. Explain
the distinct contribution of this work's closure/target audit relative to that
literature; do not claim discovery of anisotropic Casimir stress itself.

## Release and provenance boundaries

1. Make the targeted scientific and presentation corrections above; do not
   rewrite the preserved receipts or repair errors absent from the artifact.
2. For another model/human review, supply the exact current PDFs with the full
   hashes above, and keep legacy essays separate from current candidates.
3. Provide an immutable public source package matching the final artifact when
   publication is authorized. Local hash matches alone do not verify availability.
4. Author final proofreading remains pending: the operator explicitly answered
   that the final P1/P2 cold read has not been completed. This does not establish
   whether earlier scientific review occurred. Confirm the AI-use declarations
   are accurate; an assistant cannot perform the author's declaration for them.
5. Preserve deferred independent review and require separate submission authority.

All four inspected Appendix A hash prefixes match: `57847F382BAF`,
`FE648629545F`, `94B0AE4C6381`, and `9A5E80D2F713`. No original hash was changed.
This report does not change `physics_pass=false`, `gate_effect=NONE`,
`Rule9_cleared=false`, Tests 1-3 substantive holds, MAT-001, K_Q, V, Stage 4A,
or TOP-X4. The separate G3N5 executable was still live at the last poll;
this review does not claim any result from it.

## Primary references checked

- [APS reviewer guidance](https://journals.aps.org/referees): review must assess
  scientific contribution; AI assistance is not a substitute for referee judgment.
- [Planck 2015 XVIII](https://arxiv.org/abs/1502.01593): cubic-torus observational
  bound and its stated likelihood/confidence conventions.
- [Edery](https://arxiv.org/pdf/math-ph/0510056), Table 3: periodic-scalar cube
  benchmark.
- [COMPACT 2024](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.132.171501):
  topology non-exclusion is not a detection.
- [Negro et al. v2](https://arxiv.org/html/2603.12319v2): relevant comparator for
  perturbative Casimir backreaction and phenomenological topology inputs.
