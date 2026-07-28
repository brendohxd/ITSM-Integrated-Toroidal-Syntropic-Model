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
[`v12.0-alpha.4`](releases/v12.0-alpha.4/). The previous release is
[`v12.0-alpha.3`](releases/v12.0-alpha.3/); all versioned source and PDF trees
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
   .\New-ManuscriptRelease.ps1 -Version 12.0-alpha.5 -Label "Next verified checkpoint"
   ```

5. Inspect the new PDF, add `RELEASE_NOTES.md`, move the `Unreleased` entries
   to the new version, update `VERSION`, and commit all source, PDF, notes, and
   checksums together.

The release script refuses to overwrite an existing version directory.

## Scientific status

The manuscript intentionally distinguishes derived, conditional, open, and
rejected claims. `13/12`, `H0=72.97`, automatic Solar-System compliance, and
the historical SPARC `p=0.62` are not live predictions in this draft.

Release `12.0-alpha.4` records the Track-A regulator selection, the complete
homogeneous zero-gradient force action through direct quartic order, and the
assembled finite-`q` multi-sector `J2`. The source regresses exactly to the
previous linear constraint system and yields the verified
`-J2^T C^(-1)J2/2` quartic Schur functional. The inverse-Laplacian shift
representation is restricted to `q_phys>0`; the homogeneous gauge-orbit
result is unchanged.

The direct multi-sector cubic and quartic contact actions, regular
physical-scalar projection, gauge-regular constrained `2-to-2` amplitude,
physical cutoff and local nonzero-gradient exact-`Y` reduction remain open.
UVIR-003 is in progress and MAT-001 remains blocked.
