# P2 / CBR-001 Tier-1 hostile re-audit

**Date:** 2026-09-05  
**Role:** Codex Role C — canonical claim and gate audit  
**Branch:** `recovery/v12-core-architecture`  
**Status:** `LOCAL_REPAIR_CANDIDATE_COMPLETE; HOLD_FOR_INDEPENDENT_ROLE_A/B_AND_SENSITIVITY`  
**Gate effect:** none; `TOP-001 / CBR-002` remains
`SCOPED_NEGATIVE_FREE_DILUTION`

## 1. Decision

The stored Stage-3B output supports the bounded numerical statement that, in
the implemented closure and scanned domain, five threshold trajectories touch
the historical ratio `13/12` transiently, none remains within one per cent for
one e-fold, and the valid threshold trajectories return to unity by `N=20`.

P2 is **not Tier-1 release-ready**. The earlier 2026-08-01 internal `GO` is
withdrawn because it did not verify the artifact hashes, the Stage-2 scale
convention, the physical meaning of `epsilon`, or the distinction between an
instantaneous Casimir-stress closure and a quantum field solved on evolving
Bianchi-I spacetime.

**2026-09-06 amendment.** A local repair candidate now narrows the manuscript,
fixes the Stage-2 chaining instructions and scale convention, removes absolute
paths from structured outputs, fixes CSV line endings, and reproduces the full
pipeline in two isolated roots. This closes no physics or publication gate.
The earlier claim below that LF normalization did not explain the stored CSV
hash mismatch was itself incorrect and is corrected explicitly in P0.1.

The current defensible result is narrower:

> A static rectangular-`T^3` periodic-scalar Casimir tensor, transported by the
> declared thermodynamically consistent `a^-4` closure on a positive-de-Sitter
> biaxial background, does not yield a maintained `H_t/H_p=13/12` state in the
> reported bounded scan. The target-reaching cases are marginal or
> nonperturbative threshold touches and subsequently isotropize.

This is a useful negative control. It is not yet a general no-go theorem for a
free quantum field on dynamical compact Bianchi-I spacetime.

## 2. Evidence actually checked

- `casimir_t3_lattice.py` evaluates
  `rho=-(2*pi^2)^(-1) sum_(n!=0) R_n^(-4)` and obtains pressures by analytic
  length derivatives.
- Its cutoff model is `y(N)=y_inf+a1/N+a2/N^2` by default. Thus the manuscript's
  phrase "an O(1/N^2) cutoff fit" means a polynomial retained through
  `1/N^2`; it must not be read as evidence that the leading tail is
  `O(1/N^2)`.
- Stage 2 fixes `L_p=1` and sets `L_t=r L_p`; it does not keep volume or mean
  scale fixed.
- Stage 3 converts the raw Stage-2 scan to fixed mean scale by multiplying the
  raw stress by `r^(8/3)`, then reconstructs a conservation-consistent source
  from `du/dln(r)=-(2/3) Delta p`.
- Stage-3A stored validation reports a maximum source-reconstruction relative
  error `5.10e-6`, Hamiltonian and continuity residuals near machine
  precision, and small-source agreement at `2.21e-7` relative error.
- Stage-3B stored output contains 463 recorded integrations, 377 valid runs,
  and, over all valid stored runs, zero `QUASI_PLATEAU` labels. Its threshold
  summary contains five transient threshold touches, two no-crossings and one
  invalid initial boundary case.
- Four threshold cases are labelled nonperturbative and one marginal. No
  target-reaching threshold is perturbative under the package's own Casimir
  fraction criterion.
- The Stage-3B scan is `epsilon=1e-6` to `10`, a ratio of `10^7` (seven
  decades), not six decades as stated in `main.tex`.
- The `r0=4` case is not initially outside the tabulated domain. It is rejected
  because it begins at the upper interpolation boundary with an outward drive.

A fresh local two-run audit is now recorded by
`Analysis/Casimir/CBR-001/p2_reproduction_a0_harness.py`. Both isolated runs
completed Stages 1--3B, their complete repaired output trees were byte
identical, and they matched the repaired tracked output tree. This is Codex
Role-C/local tooling, not independent Role-B evidence. Antigravity's restricted
execution-witness packet and Grok's independent analytic packet remain to be
returned and adjudicated.

## 3. Severity-ranked findings

### P0 — release blockers

#### P0.1 The old checksum freeze was nonportable, not numerically false

The 2026-09-05 audit correctly observed that the four old raw digests did not
match the checkout, but its statement that LF normalization could not restore
the CSV matches was false. A fresh pre-repair Windows run reproduced all three
old CSV digests exactly:

| Artifact | Old ledger prefix | Fresh CRLF prefix | LF checkout prefix |
|---|---:|---:|---:|
| `cbr001_stage1.csv` | `9E6874226FAA` | `9E6874226FAA` | `57847F382BAF` |
| `cbr001_stage2_scan.csv` | `9257F3A67CB5` | `9257F3A67CB5` | `FE648629545F` |
| `cbr001_stage3b_thresholds.csv` | `370B02480FF0` | `370B02480FF0` | `94B0AE4C6381` |

The size differences were exactly one carriage-return byte per CSV record,
and canonical parsing showed identical cells. The old Stage-3B JSON digest was
separately nonportable because the file serialized absolute workstation paths;
after known-root normalization its scientific payload matched the fresh run.
Thus the mismatch did not demonstrate numerical drift.

The portability defect was still real. The repaired candidate now fixes LF
record terminators in all CSV writers and records output filenames relative to
the summary directory. Two isolated post-repair runs produced byte-identical
complete output trees and matched the regenerated checkout. Source and output
digests are recorded in
`papers/P2-Rectangular-T3-Casimir/CBR001_CHECKSUMS.md`.

**Disposition:** locally repaired; manuscript/source/PDF hashes are aligned and
all five PDF pages were visually checked. Independent Role-B execution remains
pending. A hash match remains artifact identity, not a physics pass.

#### P0.2 The evolved source is a closure, not a full dynamical free-field stress

Stage 1 evaluates an already-renormalized static flat-`T^3` expression. Stages
3A/3B then impose its shape dependence with an `a^-4` dilution law while the
background and anisotropy evolve. The code does not solve scalar mode
functions on the time-dependent Bianchi-I geometry and does not calculate the
renormalized curved-spacetime expectation value `<T_mn>` for a declared vacuum,
curvature coupling and subtraction prescription. Particle production,
curvature counterterms, trace anomaly and non-adiabatic/memory terms are not
computed.

Consequently, the title/abstract/conclusion language "free-field
backreaction" and "free Casimir stress alone" is broader than the executed
operation. The numerical result is a no-attractor result for the implemented
instantaneous-stress closure, not for every free field on dynamical compact
Bianchi I.

**Repair options:**

1. narrow the paper throughout to an adiabatic/instantaneous constitutive
   control and state that it does not exclude the omitted dynamical terms; or
2. derive and renormalize `<T_mn>` on the evolving compact spacetime, bound the
   closure error, and rerun the backreaction.

Option 1 is the realistic near-term paper route.

### P1 — major scientific corrections

#### P1.1 Stage-2 scale convention in the paper is wrong

`main.tex` says the Stage-2 scan uses fixed mean scale, but the code holds
`L_p=1` while varying `L_t=r`. At `r=2^(1/3)` the paper quotes the raw value
`rho=-0.47015`; the fixed-mean-scale value after the Stage-3 `r^(8/3)`
conversion is about `-0.87061`.

**Repair:** describe Stage 2 as a fixed-`L_p` rectangular scan, then explicitly
derive the homogeneous rescaling used to obtain the fixed-mean-scale Stage-3
source. Do not mix raw and rescaled numbers in one convention.

**2026-09-06 local disposition:** repaired in the manuscript candidate and run
instructions; independent hostile confirmation remains pending.

#### P1.2 `epsilon` is not a free vacuum-field amplitude

For one field, fixed topology and fixed physical lengths, the Casimir vacuum
normalization is fixed. The scan parameter represents a ratio of the Casimir
scale to the de-Sitter density scale (or, conditionally, a change in compact
length, species/multiplicity or coupling); calling it simply a free-field
"amplitude" hides the physical scale problem.

The manuscript must give the unit-restored map, including all `c` factors and
the number/species/boundary-condition factor, and evaluate it for every
cosmological interpretation it discusses. In particular, a Hubble-scale
compact length gives the Planck-suppressed fraction already recorded in the
canonical dashboard, of order `10^-121` for one conventional massless field.
The threshold values `epsilon ~ 0.089` to `2.55` therefore are reachability
controls, not physically established ITSM amplitudes.

**Repair:** rename the parameter a dimensionless source-scale ratio, derive
its physical map, and state that no ITSM mechanism presently supplies the
required scale or multiplicity.

#### P1.3 The renormalization is assumed rather than independently validated

The direct sum is an absolutely convergent dual Epstein sum after the
renormalized formula has been supplied. Trace, permutation, scaling and
thermodynamic derivative checks are valuable implementation tests, but most
are identities of the same formula. The only external numerical benchmark is
the cubic value; noncubic anisotropy lacks an independent evaluator.

**Repair:** add the functional-equation derivation from the periodic-mode
vacuum energy, declare zero-mode and vacuum treatment, and cross-check several
noncubic shapes with an independent Ewald/Chowla-Selberg or equivalent
zeta-function implementation. Report cutoff-order/window sensitivity rather
than only the least-squares residual.

#### P1.4 Numerical search is underqualified in the manuscript

The target maximum and dwell times are taken from the sampled `N` grid
(`Delta N=0.01` in the stored run). Stage 3B has no documented sample-density,
fit-order, Stage-2-grid, interpolation, `epsilon`-range or initial-shape
sensitivity suite. The search is finite, and two near-cubic no-crossings are
bounded by its valid amplitude range.

**Repair:** use dense output or scalar peak optimization; interpolate band
entry/exit times; rerun at multiple `N` resolutions, Stage-2 resolutions,
cutoff sets and interpolation choices; state the exact scanned domain in every
no-crossing claim. An analytic asymptotic argument may establish late-time
isotropization only after its assumptions (`H` bounded positive, `r` bounded,
and the declared `a^-4` source closure) are stated.

### P2 — precise wording and reporting defects

- Change "six decades" to "seven decades" for `1e-6 <= epsilon <= 10`.
- Change the `r0=4` description from an out-of-domain initial shape to an
  at-boundary trajectory whose initial drive leaves interpolation support.
- Make clear that the five quoted threshold solutions are touches of the
  sampled maximum by construction; "touch or crossing" is correct, but
  "crossing" alone would not be.
- Distinguish `STATUS: PASS` of numerical self-checks from a physics-gate pass
  everywhere the JSON or README is cited.
- Clarify that convergence of nearby trajectories at `N=20` is convergence to
  the de-Sitter isotropic state, not attraction to `13/12`.

## 4. What remains valid and useful

- The periodic rectangular-`T^3` static stress formula has the expected cube
  sign, magnitude, scaling, pressure identity and symmetry behavior.
- The thermodynamic fixed-mean reconstruction is explicit and agrees closely
  with the Stage-2 tabulation.
- The Bianchi-I shear equation, ratio identity and target conversion
  `13/12 <=> delta/H=3/38` are implemented consistently.
- The analytic small-source profile correctly shows that merely reaching the
  target requires a source outside the strict small-perturbation regime.
- The stored numerical results do not smuggle the historical target in as an
  attractor: the target-reaching cases are tuned threshold touches and decay
  to unity.
- The paper explicitly rejects a Hubble-tension solution, galactic
  acceleration derivation and parameter-free cubic-cosmology claim.

These points justify continuing the bounded negative-paper route after repair;
they do not justify the previous release `GO`.

## 5. Independent calculations required before release

### Medium numerical reproduction — Antigravity packet

1. Recreate Stage 1 through Stage 3B in a fresh output root with the repository
   `itsm_env` interpreter.
2. Recompute headline values, checks, plots and stable hashes without copying
   tracked outputs.
3. Run cutoff-window/order, Stage-2-grid, interpolation and `N`-resolution
   sensitivity checks.
4. Cross-check noncubic stress values with an independently implemented
   convergent representation.
5. Report mismatches; do not edit gates or the manuscript.

### Max bounded analytic work

1. Derive the periodic-scalar normalization from the spectral sum through the
   Epstein functional equation, with units, zero-mode treatment and pressure
   variation explicit.
2. Derive a conditional no-late-attractor statement for the exact closure
   actually integrated and list every assumption needed for the proof.
3. Decide, using an adiabatic expansion of the dynamical compact-space modes,
   which terms are omitted by the instantaneous `a^-4` closure and whether an
   error bound can be given in the perturbative regime.

The third item is the point at which switching from High to Max is warranted.
A full renormalized dynamical `<T_mn>` calculation would be a separate Ultra
task, not a condition for the narrower near-term control paper if the claims
are repaired.

## 6. Publication gate

`NO_GO_CURRENT_CANDIDATE` until the restricted Role-B reproduction is
independently adjudicated, the Role-A normalization/omission audit is returned,
the `epsilon` physical map is completed, and the sensitivity/noncubic checks
are resolved. The rebuilt PDF now matches its frozen source and has passed
local five-page visual inspection. P0.1 and P1.1 have local repair candidates;
P0.2 is locally narrowed to the instantaneous closure. P1.3--P1.4 must either
be completed or converted into explicit limitations with corresponding claim
narrowing acceptable to a target journal.
