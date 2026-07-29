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

Release `12.0-alpha.4` records the Track-A regulator selection, the
homogeneous zero-gradient force action through direct quartic order, and the
finite-`q` coefficient linear in lapse/scalar shift at the constraint origin.
A subsequent dressing audit corrected the interpretation: this `J2_origin`
and `-J2_origin^T C^(-1)J2_origin/2` are verified components, not the complete
second-order source and quartic constraint correction.

The correct source is `S2=partial_z L3[x,z1]`, with
`z1=-C^(-1)J1`. The inverse-Laplacian shift representation remains restricted
to `q_phys>0`; the homogeneous gauge-orbit result is unchanged.

The complete multi-sector finite-`q` source `S2=partial_z L3[x,z1]` and the
complete generic `L4[x,z1]` contact functional are now verified. Their
combination assembles the reduced quartic functional. A regular finite-`q`
physical-scalar basis and leg-wise projection map are also verified without
restoring the homogeneous gauge mode. The complete analytic cubic functional
is now polarized into a factorized finite-`q` physical-basis kernel with
exact per-leg lapse/shear resolvers. The reduced quartic momentum kernel, a
gauge-regular homogeneous internal-channel prescription, the constrained
`2-to-2` amplitude, physical cutoff and local nonzero-gradient exact-`Y`
reduction remain open. UVIR-003 is in progress and MAT-001 remains blocked.
