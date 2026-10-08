# ITSM site (`docs/`)

Multi-page research site published at https://itsm-cosmology.com.

## Repository research checkpoint - 8 October 2026

The recovery branch now contains the
[conditional G3 checkpoint](../Theory/Verification/ITSM_RESEARCH_CHECKPOINT_2026-10-08.md),
covering density reconstruction, interaction/regularity limits, tilted
homogeneous candidates and their coupled finite-k scalar operator.
Its exact-byte evidence manifest and verifier distinguish research
reproducibility from physical validation. Canonical Tests 1-3 remain
HOLD_SUBSTANTIVE; physical stability/cutoff, healthy full GR and SPARC
predictions remain open. Rule-9 review remains DEFERRED, not cleared.

This is repository documentation. The public-page audit below remains
its dated snapshot; a branch push does not dispatch the Pages workflow.

## Current public status

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
| `papers.html` | Canonically named core and P1-P4 artifacts |
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
