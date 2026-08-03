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
[`v12.0-alpha.10`](releases/v12.0-alpha.10/). The previous release is
[`v12.0-alpha.9`](releases/v12.0-alpha.9/); all versioned source and PDF trees
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
   .\New-ManuscriptRelease.ps1 -Version 12.0-alpha.11 -Label "Next verified checkpoint"
   ```

5. Inspect the new PDF, add `RELEASE_NOTES.md`, move the `Unreleased` entries
   to the new version, update `VERSION`, and commit all source, PDF, notes, and
   checksums together.

The release script refuses to overwrite an existing version directory.

## Scientific status

The manuscript intentionally distinguishes derived, conditional, open, and
rejected claims. `13/12`, `H0=72.97`, automatic Solar-System compliance, and
the historical SPARC `p=0.62` are not live predictions in this draft.
UVIR-003 remains in progress; MAT-001 is not unlocked.

Authoritative per-release bullets live in `CHANGELOG.md` and each freeze’s
`RELEASE_NOTES.md`. Branch-level inventory (alpha.1–alpha.10) is also kept in
the repository root
[`RECOVERY_BRANCH_README.md`](../../RECOVERY_BRANCH_README.md). Summary of
what each frozen release added:

| Release | Date | Label / content |
|---------|------|-----------------|
| [`12.0-alpha.1`](releases/v12.0-alpha.1/) | 2026-07-26 | Baseline architecture freeze (`c836172`); zero-gradient force-block factorization; conditional weak-field; open-gate structure. Research-stage only. |
| [`12.0-alpha.2`](releases/v12.0-alpha.2/) | 2026-07-26 | Scalar ADM-readiness; FRW minisuperspace + representative on-shell expanding branch. Closes background existence only. |
| [`12.0-alpha.3`](releases/v12.0-alpha.3/) | 2026-07-26 | Finite-`q` scalar constraint reduction; gauge-orbit `q=0` resolution; 3D flat khronon cubic/quartic bases (96 monomials); elastic contact; vanishing elastic `t/u` exchange; parent-block nonlinear ADM provenance; force-sector completion hold. |
| [`12.0-alpha.4`](releases/v12.0-alpha.4/) | 2026-07-29 | Track A (`D_mu D^mu psi`, exact `Y^(3/2)` on local nonzero-gradient); force ADM through direct quartic; origin-linear finite-`q` `J2` + Schur *(reclassified incomplete in alpha.5)*. |
| [`12.0-alpha.5`](releases/v12.0-alpha.5/) | 2026-07-29 | Correct source `S2=partial_z L3[x,z1]`; full multi-sector `S2` / `L4[x,z1]`; factorized cubic and reduced-quartic kernels; physical inverse kernel; fixed-comoving transfer; complex-quartet IR HOLD (`HOLD_COMPLEX_QUARTET_IR_MODE_ATTRIBUTION`). |
| [`12.0-alpha.6`](releases/v12.0-alpha.6/) | 2026-07-29 | Gauge-projected `(Q_rho,Q_chi)` response; amplified through-quartet matter survival (`PASS_GAUGE_PROJECTED_MATTER_RESPONSE_SURVIVES_WITH_SCOPE`); `Pi` clarified as factorized, not omitted. |
| [`12.0-alpha.7`](releases/v12.0-alpha.7/) | 2026-07-29 | Controlled high-`q` exchange domain (`q/H=47.5–100` pass, `45` fail adiabatic); no IR `Xi`-pure init at high momentum. |
| [`12.0-alpha.8`](releases/v12.0-alpha.8/) | 2026-07-29 | Residue-normalized modes; cubic pair sources over 48 equilateral cases (`PASS_MODE_PROJECTED_CUBIC_PAIR_SOURCE`). |
| [`12.0-alpha.9`](releases/v12.0-alpha.9/) | 2026-07-30 | Regular-tetrahedral elastic four-leg kernel: 24 mode-pairs × 72 channels; exchange + quartic contact + Schur (`PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL`). Cancellation ratio down to ~0.5% is a sensitivity, not a suppression scale. |
| [`12.0-alpha.10`](releases/v12.0-alpha.10/) | 2026-08-03 | **Current freeze.** Post-alpha.9 UVIR path package: FRW path and multi-slice Green proxy, Track-A nonzero-gradient force expansion, scoped tree/NDA criterion, and open matching-invariant inventory. Full UVIR-003 remains in progress. |

### Current freeze boundary (`12.0-alpha.10`)

Alpha.10 records the post-alpha.9 UVIR working path. It includes the FRW
observable-path declaration, multi-slice mode-projected Green proxy, local
Track-A nonzero-gradient expansion, scoped tree/NDA criterion, and matching
invariant inventory. It does **not** establish an S-matrix or optical theorem,
a matched physical cutoff, numeric Derived `K_Q`, full UVIR-003 PASS, or
MAT-001.

Post-alpha.10 gate work, including the Conditional causality map, matching-route
program, and bounded M2 declaration, belongs in a future alpha.11 only after
the working manuscript is updated and reviewed. Never overwrite alpha.10.
