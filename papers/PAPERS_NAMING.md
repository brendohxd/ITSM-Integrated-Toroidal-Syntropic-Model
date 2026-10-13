# Retained document and paper PDF naming (recovery era)

Every **retained document/manuscript PDF** must have an explicit version string
in its filename. This includes current papers, historical paper builds, cover
letters and supplementary documents. Canonical names match paper identity,
content title and version; the canonical PDF is the share, Zenodo and
collaborator artifact. Figure assets referenced by source code and the mutable
`ITSM_Core_working.pdf` build are outside this retained-document rule; neither
is a versioned manuscript deliverable. Do not share a working build as a
frozen release.

## Required PDF filename scheme

```text
Boyd_<YYYY>_<ContentTitleSlug>_v<SEMVER>[-status].pdf
```

| Part | Rule | Example |
|------|------|---------|
| Author | `Boyd` | `Boyd` |
| Year | manuscript calendar year | `2026` |
| Content title slug | short, readable, no spaces; underscores between words; no hype slogans | `Present-Epoch_Scale_Matching_Cobs_Hygiene` |
| Version | from that paper's `VERSION` file | `v0.1.0-draft` |

### Status tags

| Tag | When |
|-----|------|
| `draft` | pre-arXiv / internal (default now) |
| `rcN` | locally compiled and packaged release candidate; external review or submission clearance may remain open |
| `conditional-draft` | complete bounded manuscript whose declared ansatz or unresolved physics gates prohibit a Derived/publication-ready claim |
| `quarantined-draft` | internal provenance artifact containing claims that are not cleared; never submit or cite |
| `preprint` | after public preprint DOI/arXiv |
| `submitted` | under review |
| `accepted` / `published` | post-acceptance; prefer the journal version of record |

Bump `VERSION` when claims, tables, or figures change materially. Do not put
“Geometric-Invariants” or “parameter-free” in filenames.

For an orphan historical PDF whose build-time manuscript version cannot be
verified, use `v0.0.0-legacy-<YYYYMMDD>-<sha8>` (or
`v0.0.0-legacy-quarantined-<YYYYMMDD>-<sha8>` where required). This is a
content-addressed **administrative archive ID**, not an invented manuscript
version or a scientific endorsement. If a version is printed in the PDF, retain
that version and append a quarantine/date/hash suffix when necessary. Preserve
the original bytes, prior path, full SHA-256 and status in a manifest; never
silently assign an old PDF the current `VERSION` file's value. A checksum
establishes byte identity, not scientific clearance.

## Current canonical paper PDFs

| ID | Directory | `VERSION` | Canonical PDF | Build helper |
|----|-----------|-----------|---------------|--------------|
| **P1** | `papers/P1-Scale-Matching-Reconstruction/` | `0.2.0-rc3` | `Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc3.pdf` | `Build-P1-Scale-Matching-Reconstruction.ps1` |
| **P2** | `papers/P2-Rectangular-T3-Casimir/` | `0.2.0-rc3` | `Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Instantaneous-Closure-Control_v0.2.0-rc3.pdf` | `Build-P2-Rectangular-T3-Casimir.ps1` |
| **P3** | `papers/P3-Observational-Program/` | `0.1.1-quarantined-draft` | `Boyd_2026_Gate-Structured_Observational_Falsification_Program_ITSM_v0.1.1-quarantined-draft.pdf` | `Build-P3-Observational-Program.ps1` |
| **P4** | `papers/P4-SPARC-Kinematics/` | `0.1.1-quarantined-draft` | `Boyd_2026_SPARC_Galactic_Kinematics_AQUAL_Picard_Solutions_v0.1.1-quarantined-draft.pdf` | `Build-P4-SPARC-Kinematics.ps1` |
| **Thermodynamics** | `papers/Syntropic-Thermodynamics/` | `0.7.1-conditional-draft` | `Boyd_2026_Covariant_Entropy_Accounting_Interacting_Sectors_v0.7.1-conditional-draft.pdf` | `Build-Syntropic-Thermodynamics.ps1` |
| **R4C1** | `papers/R4C1-Covariant-Exchange-Model/` | `0.1.1-conditional-draft` | `Boyd_2026_Covariant_Finite-Density_Exchange_Model_v0.1.1-conditional-draft.pdf` | `Build-R4C1-Covariant-Exchange-Model.ps1` |

The older P2 file
`Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Free-Field_Backreaction_v0.1.0-draft.pdf`
is retained as a descriptive, superseded historical candidate. It is not the
current P2 deliverable.

P3 and P4 are canonical **quarantine artifacts**, not current publication
deliverables. Their descriptive filenames, first-page notices and README
boundaries prevent a successful build from being mistaken for gate clearance.

Four generic `main.pdf` builds from 30 August 2026 have been preserved locally
with versioned archive IDs under
[`papers/LegacyBuilds/2026-08-30/`](LegacyBuilds/2026-08-30/README.md).
Their original manuscript versions are unverified; the P3/P4 binaries predate
the visible quarantine notices and must not be cited or submitted. The PDF
binaries are Git-ignored against accidental publication, while the manifest
and individual `.sha256` sidecars remain available for provenance.

Full titles are kept in the manuscript metadata and README files; filenames
use short identity slugs so they remain readable.

Check current retained-document filenames with the read-only
`Scripts/Check-RetainedPdfNames.ps1`. It includes local legacy PDFs, but does
not infer scientific validity from a well-formed filename.

## Core manuscript and recovery artifacts

Core and recovery PDFs already use descriptive authority names:

- Mutable working build: `Manuscript/CoreRecovery/ITSM_Core_working.pdf`.
- Current immutable recovery freeze: `Manuscript/CoreRecovery/releases/v12.0-alpha.12/ITSM_Core_v12.0-alpha.12.pdf`.
- Quarantined historical root manuscripts retain their versioned names, for
  example `Manuscript/ITSM_Core_Cosmology_v12.0-alpha.13.pdf`.
- The retained historical JCAP cover letter is
  `Manuscript/Submission_Materials/ITSM_JCAP_Cover_Letter_v0.0.0-legacy-quarantined-20260621-f1e5b509.pdf`;
  its build-time version is unverified and its scientific claims are withdrawn.
- The retained historical SPARC supplement is
  `Manuscript/Supplementary/ITSM_SPARC_MCMC_Parameter_Ledger_v11.4.1-quarantined-20260706-7700346a.pdf`;
  `11.4.1` is printed in that PDF, but the MCMC claims are not current results.
- Recovery, gate, and verification records use their document ID plus date or
  version; no active record uses a generic PDF deliverable name.

Historical changelogs and deposit manifests may retain old paths exactly as
provenance. They are not current build or publication instructions.

## Build behaviour

- An active P1-P4 build writes the canonical versioned PDF directly and emits
  its matching `<canonical-name>.pdf.sha256` sidecar.
- `main.pdf` is not a canonical or supported deliverable name. Paper build
  helpers **refuse to run** if an unversioned generic PDF or sidecar is still
  present. Hash and archive it first; helpers must not silently delete it.
- P1-P4 currently retain `main.tex` as an internal LaTeX source entry point;
  source compatibility does not make `main.pdf` an acceptable share name.
- Generated auxiliary files remain local build products and are ignored.

## Versioning advice

1. Start at `0.1.0-draft` for recovery-era drafts.
2. Use `0.x.y` while claims or figures move; use `1.0.0-preprint` at first
   public archive and `1.0.0` only for a frozen citable preprint record.
3. Keep one `VERSION` file per paper directory (single line, no quotes).
4. After each intentional bump, rebuild so the PDF filename and sidecar match
   `VERSION`.
5. Zenodo, email, and collaborators receive the canonical named PDF.

## Renamed directories (do not reintroduce)

| Old path | Why wrong |
|----------|-----------|
| `papers/P1-Geometric-Invariants/` | Implies geometric invariants established |
| `papers/P2-Casimir-Backreaction/` | Less specific than rectangular $T^3$ free-field scope |

## Related

- Selective publishing: `papers/Selective-Publishing-Plan/`
- P2 arXiv: deferred pending endorsement
