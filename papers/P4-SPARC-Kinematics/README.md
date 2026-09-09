# P4 — SPARC Galactic Kinematics under 2D/3D AQUAL Picard Solutions

**Directory:** `papers/P4-SPARC-Kinematics/`  
**VERSION:** see `VERSION` (currently `0.1.1-quarantined-draft`)

**Canonical quarantine PDF:** `Boyd_2026_SPARC_Galactic_Kinematics_AQUAL_Picard_Solutions_v0.1.1-quarantined-draft.pdf`

**Status:** **Quarantined claim-bearing legacy scaffold; not for citation or submission**

**Current boundary:** DISK-001 is `METHODS_ONLY`; STAT-001 is `NOT_STARTED_AS_CLOSED_GATE`; MAT-001 is `BLOCKED`. The earlier 175-galaxy zero-parameter/MCMC claims are quarantined. The repaired 152-galaxy comparator is optimization-only and is not an ITSM prediction.

**Authority:** `papers/Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md` §4.4  
**Branch:** `recovery/v12-core-architecture`

## What this is

A RevTeX 4.2 legacy scaffold retained to preserve the provenance of a proposed
SPARC paper. Its first page and filename are deliberately quarantined because
the body overstates the parent-action coupling, solver scope and statistical
evidence.

## Build

```powershell
cd papers\P4-SPARC-Kinematics
.\Build-P4-SPARC-Kinematics.ps1
```

## Allowed now

- Maintain conditional AQUAL/Picard tooling and explicit comparator tests.
- Declare acceleration and nuisance inputs; separate raw likelihood from
  priors and optimization from posterior sampling.
- Rebuild this PDF for internal integrity review only; compilation is not
  publication clearance.

## Forbidden until new signed gate decisions

- First-principles or zero-global-parameter ITSM SPARC claims.
- The quarantined 175-galaxy MCMC statistics as a current result.
- Publication, citation or archive deposit of this scaffold as a result.

## Files

| File | Role |
|------|------|
| `VERSION` | Manuscript version |
| `Build-P4-SPARC-Kinematics.ps1` | Canonical named-PDF build helper |
| `main.tex` | Internal LaTeX source entry point |
| `Boyd_2026_SPARC_Galactic_Kinematics_AQUAL_Picard_Solutions_v0.1.1-quarantined-draft.pdf` | Canonical local quarantine PDF; not citable |
