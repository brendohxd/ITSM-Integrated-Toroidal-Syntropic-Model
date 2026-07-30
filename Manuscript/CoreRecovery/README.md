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
[`v12.0-alpha.9`](releases/v12.0-alpha.9/). The previous release is
[`v12.0-alpha.8`](releases/v12.0-alpha.8/); all versioned source and PDF trees
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
   .\New-ManuscriptRelease.ps1 -Version 12.0-alpha.10 -Label "Next verified checkpoint"
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
phase-space gain of `1.37708e27`. The subsequent five-case mode-resolved audit
finds that the dominant singular input is `Xi` seeded in every tested case.
However, each trajectory enters an off-axis complex quartet whose real
invariant subspace has rank four, preventing a unique continuous rank-two
split between the gauge-continuation and retained-matter pole pairs.

The source-to-observable follow-on removes direct `Xi` and homogeneous
time-translation source support and reads only retained `(Q_rho,Q_chi)`.
Every tested case retains amplified through-quartet response, ranging from
`2.67849e17` to `9.75967e19`. Record
`PASS_GAUGE_PROJECTED_MATTER_RESPONSE_SURVIVES_WITH_SCOPE`. This resolves the
direct gauge-source attribution question for the tested finite-duration
dimensionless neighborhood, not an all-background instability theorem. The
Track-A force mode `Pi` remains factorized at quadratic order and is outside
this coupled quartet audit rather than omitted from the full framework.

A controlled sampled high-momentum exchange domain is now established on the
representative branch. Initial `q_phys/H=47.5,50,75,100` passes the real-pole,
subhorizon and `max |omega_dot/omega^2|<0.1` criteria; the `45` sample fails
only the adiabatic threshold. This is a sampled bracket, not a continuous or
all-background boundary. Every nonzero internal exchange momentum must pass
the same gate independently, while exact `q_K=0` uses the separate homogeneous
projector.

The analytic cubic kernel is now contracted with two residue-normalized
on-shell coupled modes in 48 admitted equilateral momentum/sign cases. Every
case produces a finite nonzero off-shell pair-source covector and finite
inverse-kernel response; permutation and inverse closure are below `6.2e-16`.
The `Pi` source vanishes for two coupled external legs at this analytic cubic
order.

A subsequent regular-tetrahedral elastic slice keeps every `s`, `t`, and `u`
internal momentum nonzero and reruns each internal trajectory through the
controlled-domain audit. Across 24 mode-pair cases and 72 channels, matched
physical exchange contractions are combined with the analytic quartic contact
and all three constraint-Schur pairings. The local frozen-time four-leg kernel
is finite, real within numerical tolerance, nonzero, and permutation
consistent. Component cancellations reach the `0.502%` level and remain an
explicit sensitivity. A cosmological S-matrix normalization, physical cutoff,
and local nonzero-gradient exact-`Y` reduction remain open.
