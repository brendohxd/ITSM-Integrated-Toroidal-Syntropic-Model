# ITSM site (`docs/`)

Multi-page research site published at https://itsm-cosmology.com.

## Current public status

Audited 12 September 2026 against the v12.0-alpha.12 recovery authority:

- **TOP-X4 / X4-S2F3:** `LOCAL_PARAMETRIX_PASS_GLOBAL_STATE_STRESS_HOLD`.
  Static determinant 12/12, entry gate 9/9, finite-charge operator 16/16,
  exact transport 18/18, D5 scaffold 20/20 and fixed-metric scalar-matrix
  operator 25/25 remain bounded. The local scalar-matrix Hadamard-parametrix
  checkpoint now passes 22/22 through `U_2`. A global/infinite-order state,
  normalization, gravity/parity completion, determinant, stress and physical
  Hessian remain held. `physics_pass=false` and `gate_effect=NONE`.
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
