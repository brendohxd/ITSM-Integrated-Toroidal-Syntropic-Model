# Retained legacy paper builds — 30 August 2026

These four PDFs were moved byte-for-byte on 30 September 2026 from the
corresponding `papers/P1`–`P4` directories, where each was named `main.pdf`.
The PDF creation dates are 30 August 2026 (Australia/Perth). Their original
manuscript `VERSION` at build time was not independently recorded. The
`v0.0.0-legacy-...` string is a **new administrative archive identifier**, not
a claim that the underlying research was version 0.0.0 or passed a gate.
The final filename token is the first eight hex characters of each PDF's
SHA-256 and distinguishes its exact bytes.

| Origin | Retained filename (in this directory) | SHA-256 | Source-level comparison |
|---|---|---|---|
| `P1-Scale-Matching-Reconstruction/main.pdf` | `Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.0.0-legacy-20260830-5374bd29.pdf` | `5374bd29dd35f9299a8e1c514b46b274915bf3a6311d25c2def06d0248e72e99` | Extracted text differs from the current named P1 draft only in its displayed build date; binary bytes differ. |
| `P2-Rectangular-T3-Casimir/main.pdf` | `Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Free-Field_Backreaction_v0.0.0-legacy-20260830-bbdd97ea.pdf` | `bbdd97ea37b2695795992c139fe3291e269e8c3533e977533dea0d0492cdc300` | Extracted text differs from the earlier named P2 free-field draft in its displayed date and one legacy P1 directory reference. |
| `P3-Observational-Program/main.pdf` | `Boyd_2026_Gate-Structured_Observational_Falsification_Program_ITSM_v0.0.0-legacy-quarantined-20260830-a4ea2bde.pdf` | `a4ea2bdebce8475d4079508878be6df5292a8e92af655944f04d24648d07b776` | Predates the current PDF's visible quarantine notice; not for citation or submission. |
| `P4-SPARC-Kinematics/main.pdf` | `Boyd_2026_SPARC_Galactic_Kinematics_AQUAL_Picard_Solutions_v0.0.0-legacy-quarantined-20260830-c169e3ae.pdf` | `c169e3aed9e592dbe7fcbf29ae1975daef8048c2320ab6651054ad641cf80f64` | Predates the current PDF's title and visible quarantine notice; not for citation or submission. |

Each PDF has a same-name `.sha256` sidecar. A checksum verifies bytes, not
scientific validity or original publisher provenance. The four binaries are
local and Git-ignored to prevent accidental public release; this manifest and
its sidecars may be versioned. Current named paper PDFs and their `VERSION`
files remain in their original directories, unchanged.
