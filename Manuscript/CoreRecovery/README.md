# ITSM Core Recovery manuscript

This directory is the manuscript workspace for the
`recovery/v12-core-architecture` branch. It does not replace the legacy
`Manuscript/ITSM_Core_Cosmology_v11.4.1.tex`.

## Current files

- `ITSM_Core_working.tex` and `sections/` are the mutable manuscript sources.
- `ITSM_Core_working.pdf` is a convenience build and may change at any time.
- `VERSION` records the newest frozen manuscript release.
- `CHANGELOG.md` records scientific and editorial changes between releases.
- `releases/v<version>/` contains immutable source and PDF snapshots.

The current frozen release is
[`v12.0-alpha.3`](releases/v12.0-alpha.3/). The previous release is
[`v12.0-alpha.2`](releases/v12.0-alpha.2/); all versioned source and PDF trees
are immutable snapshots.

## Versioning rule

A filename containing a version is a frozen release, not a working filename.
Never rebuild or edit an existing directory under `releases/`.

Use `12.0-alpha.N` while the v12 architecture remains research-stage. Increment
`N` whenever the manuscript changes its equations, evidence, claim status,
gate status, or scientific conclusions. Small corrections also receive a new
alpha number; this keeps every cited PDF unambiguous.

## Working and release workflow

1. Edit `ITSM_Core_working.tex` and the shared `sections/`.
2. Build and inspect `ITSM_Core_working.pdf`.
3. Record pending changes under `Unreleased` in `CHANGELOG.md`.
4. When the manuscript is ready to freeze, run:

   ```powershell
   .\New-ManuscriptRelease.ps1 -Version 12.0-alpha.4 -Label "Next verified checkpoint"
   ```

5. Inspect the new PDF, add `RELEASE_NOTES.md`, move the `Unreleased` entries
   to the new version, update `VERSION`, and commit all source, PDF, notes, and
   checksums together.

The release script refuses to overwrite an existing version directory.

## Scientific status

The manuscript intentionally distinguishes derived, conditional, open, and
rejected claims. `13/12`, `H0=72.97`, automatic Solar-System compliance, and
the historical SPARC `p=0.62` are not live predictions in this draft.

Release `12.0-alpha.3` records the low-`q` gauge-orbit audit, the complete
three-dimensional flat-decoupling khronon cubic and quartic operator bases,
the cubic and quartic constraint-order identities, and nonlinear ADM action
provenance for the exact `g+U+Phi+alignment` block. The full cosmological `J2`
is not yet assembled. Track A now adopts `D_mu D^mu psi`, retains exact
`Y^(3/2)` and assigns its perturbative force test to a declared local
nonzero-gradient background. The homogeneous zero-gradient force action is
verified through direct quartic order and its lapse/shift `J2` component is
derived. The physical interaction scale remains open pending the complete
multi-sector source and gauge-regular constrained `2-to-2` amplitude.