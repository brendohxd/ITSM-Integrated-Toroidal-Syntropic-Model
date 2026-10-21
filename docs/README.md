# ITSM site (`docs/`)

Multi-page research site published at https://itsm-cosmology.com.

## Paper freshness and model-scope update - 21 October 2026

Following a comparison of the public main and recovery documentation:

- `papers.html` links P1 `0.2.0-rc7` and P2 `0.2.0-rc4`, with their current
  contributions, dates, source/revision records and outstanding release decisions.
  Thermodynamics `0.7.1-conditional-draft` and R4C1 `0.1.1-conditional-draft`
  remain current. Review candidates are not peer-reviewed releases. The immutable
  alpha.12 authority freeze remains separate from the mutable core build.
- `architecture.html` explains the separate wake, winding/mode and driven-stress
  hypotheses, then distinguishes legacy main-branch claims from the current
  recovery programme. R4C1 is one conditional route, not the whole ITSM model.
- `vision.html` connects the physical proposal to joint motion/lensing,
  expansion/structure/BBN and wave/early-universe tests. These are research
  objectives, not restored numerical predictions or completed validations.
- `claims.html` and `reproduce.html` now use the 21 October evidence map. The
  reproduction command names research revision `2587c3eb` explicitly; older
  checkpoints and their revision-specific integrity evidence remain valid.
- The service-worker cache is `itsm-pwa-v12-20261021`. The existing visual design
  and homepage progress note are retained. No scientific artifact or gate changes.

### Before deployment

```powershell
python -B -m unittest discover -s Scripts/site -p 'test_*.py'
python -B Scripts/site/check_public_site.py
```

The source checker now compares all four current paper cards with their tracked
`VERSION` files, canonical versioned PDFs and checksum sidecars. It rejects
stale labels/links even if an older PDF still exists, untracked/private artifacts
and quarantined versions. Historical links do not satisfy a current card.
Pinned GitHub evidence links are checked against their named Git objects.
The Pages workflow fetches only the linked snapshots into its ephemeral checkout
and runs these checks before uploading `docs/`; it does not fetch full history.

These are website checks, not a fresh physics replay or scientific clearance.
Deployment still requires the manual workflow and verification of the resulting
live pages. A local edit, passing checker or branch push is not a deployment.

Local verification: 19 offline regression tests pass; source checks cover seven
pages, 230 references, six public PDF targets, four current paper versions and
five pinned repository targets. Isolated local-browser checks cover all seven
pages at desktop and mobile widths without horizontal document/card overflow,
broken local images or JavaScript exceptions. External font loading was blocked
for that local check, so it verifies the fallback-font layout, not remote font
availability. Previews and execution logs remain ignored local artifacts.

## Public research-note source update - 21 October 2026

The homepage progress cards and Progress page now describe the first material
compatibility result, with links pinned to the owning report and evidence map
at research commit `2587c3eb`. They distinguish the changing-background
cancellation from the still-valid frozen result and retain the open evolution,
stability, physical-window, GR and matching requirements. The main concept,
vision, paper releases and canonical scientific statuses are unchanged.

The service-worker cache version advances to `itsm-pwa-v11-20261021` so offline
copies can refresh. The website checker follows that version without changing
its scientific-status, link, privacy or structural checks. Deployment uses the
existing manual Pages workflow on `recovery/v12-core-architecture`; a source
commit alone is not proof of deployment. The earlier navigation-only update
below did not deploy the site.

## Repository research checkpoint - 21 October 2026

The [latest checkpoint](../Theory/Verification/ITSM_RESEARCH_CHECKPOINT_2026-10-21.md)
records the coupled-domain, canonical-seed and first material compatibility
work since 18 October, including failed and unfinished calculations. Changing
background constraints cancel the earlier frozen seed forcing at first
material order in the declared class; no physical trajectory, stability,
validity window or numerical acceleration prediction is established.
Stage 2 remains incomplete, Stage 3 not entered and Rule-9 review deferred.

This is repository navigation only. Public HTML and the separate Pages
workflow are unchanged; this commit is not a website deployment.

### Preserved 17 October repository checkpoint

The [17 October checkpoint](../Theory/Verification/ITSM_RESEARCH_CHECKPOINT_2026-10-17.md)
records the three-family constraint and cubic-response work, the source-aware
summable-field bound and P1 rc6 / P2 rc4 review candidates. The bound is a
registered perturbative mathematical result, not a physical cutoff, complete
nonlinear solution or healthy-GR verdict. Stage 2 remains incomplete and
numerical Stage 3 has not been entered; coefficient matching is still missing.

This update changes repository documentation only. It does not change public
HTML, dispatch the Pages workflow or supersede the dated public-page audit below.

### Preserved 13 October repository checkpoint

The [13 October checkpoint](../Theory/Verification/ITSM_RESEARCH_CHECKPOINT_2026-10-13.md)
records bounded linear prepared-dust Stage-1 acceptance, the same-action
GR-family and coupled fixed-charge response work, the RM1/ST1/ST2 matching
screens, and versioned paper-preparation/review artifacts. Physical Stage-2
admission remains unresolved and numerical Stage 3 is not entered. The
fixed-charge preparation does not remove the registered timing warning;
the matching controls do not determine numerical ITSM coupling constants.

Its exact-byte evidence manifest and verifier distinguish artifact integrity
from scientific validation. Canonical Tests 1-3 remain `HOLD_SUBSTANTIVE`;
MAT-001 remains blocked; no physical cutoff, healthy full GR, new observational
prediction or publication clearance follows. Rule-9 remains `DEFERRED`.

This is repository documentation. The public-page audit below remains
its dated snapshot; a branch push does not dispatch the Pages workflow.

## Preserved public-status audit - 26 September 2026

Audited 26 September 2026 against the v12.0-alpha.12 recovery authority and
the active Master Tests 1–3 disposition:

- **External evidence watch:** six unreviewed arXiv inputs were screened on 14
  September, with BBN and empirical-helium tests prioritized. This adds no
  gate closure or publication clearance. The [canonical evidence
  record](https://github.com/brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model/blob/recovery/v12-core-architecture/Theory/Core/ITSM_EXTERNAL_EVIDENCE_WATCH_2026-09-14.md)
  contains the source facts and bounded follow-up tasks.

- **BBN-001:** the local five-table CAMB schema/interpolation control passes,
  including the PRIMAT 2024 `Ombh2`/`ombh2` compatibility check and CAMB
  helium bridge. The upstream-interface preflight also confirms that the
  registered UVIR-003 branch is dimensionless and lacks the physical
  temperature, plenum, transfer and effective-gravity inputs needed for an
  ITSM BBN run. It remains `CONTROL_ONLY` with `physics_pass=false`; no
  action-derived ITSM early-time result or publication claim is established.

- **Master Tests 1–3 / R4C1:** the ordered programme remains incomplete. The
  conditional R4C1 candidate supplies bounded action/source, variation,
  interacting-background, GR-control and coefficient-identifiability receipts;
  S1/S2/S3 add scalar constraint, propagation and zero-branch diagnostics. The
  positive scalar kinetic result is restricted to its declared regular chart,
  the corrected propagation result retains a defective zero branch, and the
  full coupled well-posedness, physical matching and canonical parent remain
  open. These results retain `physics_pass=false`.

- **Rule 9:** outstanding review is `DEFERRED` with `Rule9_cleared=false`.
  Locally checked results can proceed provisionally when review is the only
  unmet requirement; substantive physics holds and final canonical/publication
  decisions remain binding. No reviewer dispatch is implied.

- **TOP-X4 / X4-S2F3:** `BOUNDED_LOCAL_AND_FINITE_ORDER_PLUS_THEOREM_BACKED_SCALAR_STATE_STRESS_HOLD`.
  Static determinant 12/12, entry gate 9/9, finite-charge operator 16/16,
  exact transport 18/18, D5 scaffold 20/20 and fixed-metric scalar-matrix
  operator 25/25 remain bounded. The local scalar-matrix Hadamard-parametrix
  checkpoint now passes 22/22 through `U_2`, and the finite-order Route-B
  adiabatic-symbol diagnostic passes 8/8 with stable orders 0--3, including
  full rank-three finite transport. The registered Route-A theorem-backed
  scalar-state construction passes 10/10 and records the formal all-order
  symbol, Borel/smoothing realization, positive low-mode patch and exact
  full-matrix evolution. This is not independent peer review or a numerical
  physics pass; normalization, gravity/parity completion, determinant, stress
  and physical Hessian remain held. The separate physical-Hessian readiness
  audit passes 8/8 bookkeeping checks but records
  `physical_hessian=NOT_CONSTRUCTED` and `radion_mass=NOT_COMPUTED`.
  `physics_pass=false` and
  `gate_effect=NONE`.
- **MAT-001:** `BLOCKED`; `K_Q` is `NOT_DERIVED` and `V` is
  `NOT_COMPUTED`.
- **UVIR-003:** `IN_PROGRESS`; no complete physical amplitude, unitarity
  result or EFT cutoff is promoted.
- **DISK-001 / STAT-001:** methods-only / closed gate not started. Historical
  optimizer and MCMC promotion claims are quarantined.
- **VOR-001, SCR-001, LEN-001, WAK-001, RES-001, ASTRO-001 and COS-001:**
  open scaffolds, controls or calibration-only work as specified on the site;
  none is a closed downstream physics gate.
- **Publication:** core and P1-P4 artifacts use their canonical descriptive
  names. P3 and P4 are quarantined drafts, and all current papers remain on
  publication hold.

Script `PASS_*` labels establish only the scope stated by their owning
receipt. They do not establish a physics pass, downstream promotion or
publication clearance.

| Page | Purpose |
|------|---------|
| `index.html` | Home and current snapshot |
| `vision.html` | Aims, positioning and evidence boundaries |
| `architecture.html` | Sectors and non-negotiable separations |
| `research.html` | Current gates and operator-priority route |
| `papers.html` | Current focused review drafts, core freeze and historical boundaries |
| `claims.html` | Status definitions and public claim matrix |
| `reproduce.html` | Bounded reproduction entry points |

The public pages summarize the verified scope only. The detailed Test-1–3 and
R4C1 reports remain the source documents for assumptions, hashes, domains and
failed/unknown-check handling.

## Deployment

- **Live domain:** https://itsm-cosmology.com
- **Workflow:** `.github/workflows/pages.yml`
- **Artifact:** the `docs/` directory from the ref selected when the
  `github-pages` workflow is manually dispatched
- **Canonical deployment ref:** `recovery/v12-core-architecture`

GitHub's Pages API currently retains `gh-pages:/` source metadata, but the
live artifact is uploaded by `actions/deploy-pages`. Pushing a branch does
not update the public site by itself; the workflow must be dispatched from the
intended ref and its deployment verified.

## Visual assets

The `assets/web/*_v2.png` figures are purpose-built conceptual illustrations
for the recovery-era site. They are not numerical outputs, observational
evidence, or replacements for executable gate reports. Earlier assets are
retained as provenance and fallback material.

The shared background adds a slow CSS-only toroidal field and star drift. This
motion is decorative rather than a numerical simulation, does not receive
pointer input, and remains static when the visitor requests reduced motion.

```powershell
cd docs
python -m http.server 8080
```
