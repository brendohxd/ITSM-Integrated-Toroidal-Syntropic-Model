# Paper directory and PDF naming (recovery era)

Canonical names match paper identity, content title, and version. The
canonical PDF is the share, Zenodo, and collaborator artifact.

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
| `quarantined-draft` | internal provenance artifact containing claims that are not cleared; never submit or cite |
| `preprint` | after public preprint DOI/arXiv |
| `submitted` | under review |
| `accepted` / `published` | post-acceptance; prefer the journal version of record |

Bump `VERSION` when claims, tables, or figures change materially. Do not put
“Geometric-Invariants” or “parameter-free” in filenames.

## Current canonical paper PDFs

| ID | Directory | `VERSION` | Canonical PDF | Build helper |
|----|-----------|-----------|---------------|--------------|
| **P1** | `papers/P1-Scale-Matching-Reconstruction/` | `0.1.0-draft` | `Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.1.0-draft.pdf` | `Build-P1-Scale-Matching-Reconstruction.ps1` |
| **P2** | `papers/P2-Rectangular-T3-Casimir/` | `0.1.0-draft` | `Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Instantaneous-Closure-Control_v0.1.0-draft.pdf` | `Build-P2-Rectangular-T3-Casimir.ps1` |
| **P3** | `papers/P3-Observational-Program/` | `0.1.1-quarantined-draft` | `Boyd_2026_Gate-Structured_Observational_Falsification_Program_ITSM_v0.1.1-quarantined-draft.pdf` | `Build-P3-Observational-Program.ps1` |
| **P4** | `papers/P4-SPARC-Kinematics/` | `0.1.1-quarantined-draft` | `Boyd_2026_SPARC_Galactic_Kinematics_AQUAL_Picard_Solutions_v0.1.1-quarantined-draft.pdf` | `Build-P4-SPARC-Kinematics.ps1` |

The older P2 file
`Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Free-Field_Backreaction_v0.1.0-draft.pdf`
is retained as a descriptive, superseded historical candidate. It is not the
current P2 deliverable.

P3 and P4 are canonical **quarantine artifacts**, not current publication
deliverables. Their descriptive filenames, first-page notices and README
boundaries prevent a successful build from being mistaken for gate clearance.

Full titles are kept in the manuscript metadata and README files; filenames
use short identity slugs so they remain readable.

## Core manuscript and recovery artifacts

Core and recovery PDFs already use descriptive authority names:

- Mutable working build: `Manuscript/CoreRecovery/ITSM_Core_working.pdf`.
- Current immutable recovery freeze: `Manuscript/CoreRecovery/releases/v12.0-alpha.12/ITSM_Core_v12.0-alpha.12.pdf`.
- Quarantined historical root manuscripts retain their versioned names, for
  example `Manuscript/ITSM_Core_Cosmology_v12.0-alpha.13.pdf`.
- Recovery, gate, and verification records use their document ID plus date or
  version; no active record uses a generic PDF deliverable name.

Historical changelogs and deposit manifests may retain old paths exactly as
provenance. They are not current build or publication instructions.

## Build behaviour

- An active P1-P4 build writes the canonical versioned PDF directly and emits
  its matching `<canonical-name>.pdf.sha256` sidecar.
- `main.pdf` is not a canonical or supported deliverable name. Build helpers
  remove a leftover generic PDF after the named output has been verified.
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
