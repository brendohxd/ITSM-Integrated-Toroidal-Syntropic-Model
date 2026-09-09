# P3 — Gate-structured observational and falsification program

**Directory:** `papers/P3-Observational-Program/`  
**VERSION:** see `VERSION` (currently `0.1.1-quarantined-draft`)

**Canonical quarantine PDF:** `Boyd_2026_Gate-Structured_Observational_Falsification_Program_ITSM_v0.1.1-quarantined-draft.pdf`

**Status:** **Quarantined claim-bearing legacy scaffold; not for citation or submission**

**Current boundary:** VOR-001 is `OPEN_SCAFFOLD`; SCR-001 and LEN-001 are `OPEN`; MAT-001 is `BLOCKED`; UVIR-003 is `IN_PROGRESS`. No derived PTA window, screening prediction or lensing equivalence is currently cleared.

**Authority:** `papers/Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md` §4.3  
**Branch:** `recovery/v12-core-architecture`

## What this is

A RevTeX 4.2 legacy scaffold retained to preserve the provenance of a proposed
multi-scale falsification paper. Its first page and filename are deliberately
quarantined because the body contains claims that exceed current parent-gate
status. `OUTLINE.md` is the current planning surface.

## Build

```powershell
cd papers\P3-Observational-Program
.\Build-P3-Observational-Program.ps1
```

## Allowed now

- Gate-structured falsifier *program* (conditional on closed gates)  
- Methodology placeholders (PTA polarization *if* eigenmodes exist)  
- Cite **P1** for claim hygiene; **P2** for free-field Casimir limits  
- Rebuild the PDF for internal integrity review only; compilation is not
  publication clearance

## Forbidden (ban list — non-exhaustive)

| Forbidden | Ban / note |
|-----------|------------|
| Fixed NANOGrav $[1.08,\pi]$ nHz as prediction | B13 |
| Scalar PTA as guaranteed near-term result | B13 |
| JWST CO/Na I as model-level falsifier from Jeans/IMF | B14 |
| Withdrawn geometric $a_0$ as positive input | B1 |
| Bullet Cluster quantitative “solution” | ledger |
| Dual $C_{\mathrm{obs}}=2/3$ + $a_0=cH_0/2\pi$ as RAR | B9 (if kinematics appear) |

## Files

| File | Role |
|------|------|
| `OUTLINE.md` | Section map + claim tags |
| `VERSION` | Manuscript version |
| `Build-P3-Observational-Program.ps1` | Canonical named-PDF build helper |
| `main.tex` | Internal LaTeX source entry point |
| `Boyd_2026_Gate-Structured_Observational_Falsification_Program_ITSM_v0.1.1-quarantined-draft.pdf` | Canonical local quarantine PDF; not citable |
| `README.md` | This file |

## Related readiness

- `Theory/Gates/P3_P4_READINESS.md`  
- `Theory/Gates/MAT-001/MAT-001_READINESS.md`  
- `Theory/Gates/DISK-001/DISK-001_READINESS.md`  
