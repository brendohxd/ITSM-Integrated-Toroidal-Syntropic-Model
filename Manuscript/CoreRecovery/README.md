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

The complete multi-sector finite-`q` source `S2=partial_z L3[x,z1]`, generic
`L4[x,z1]` contact, and regular physical-scalar basis are verified. The
analytic cubic and reduced quartic functionals are now polarized into
factorized physical-basis kernels with exact external constraint resolvers.
The quartic result contains the complete physical pair-source kernel and all
three finite-channel Schur pairings. At exact zero internal momentum,
separate algebraic projectors remove `Sigma=-D^2 beta` and the homogeneous
`Xi` gauge orbit while retaining the lapse constraint and
`(Q_rho,Q_chi,Pi)` subspace. The corresponding finite-`q` physical inverse
quadratic kernel and exact projected `q=0` response are now constructed.
The fixed-comoving follow-on restores coefficient derivatives and Hubble
dilution and produces converged kinetic-normalized transfer matrices. It shows
that frozen-pole exponentiation is invalid in the nonadiabatic domain, while
the initial `q_phys/H=0.01` trajectory retains a maximum normalized
phase-space gain of `1.37708e27`. Because that gain has not yet been assigned
to a continuously tracked physical eigenmode, the result remains on HOLD and
is not classified as instability or gauge-continuation behavior. The
`q_phys/H=100` trajectory is a controlled adiabatic high-`q` subset. The
constrained `2-to-2` exchange-plus-reduced-contact amplitude, physical cutoff,
and local nonzero-gradient exact-`Y` reduction remain open. UVIR-003 is in
progress and MAT-001 remains blocked.
