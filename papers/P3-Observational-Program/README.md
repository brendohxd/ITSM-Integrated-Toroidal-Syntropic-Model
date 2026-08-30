# P3 — Gate-structured observational and falsification program

**Directory:** `papers/P3-Observational-Program/`  
**VERSION:** `0.1.0-draft`  
**Status:** **Draft complete & compiled** (`main.pdf`)  
**Current boundary:** VOR-001 Stage S4 passed (derived Bogoliubov acoustic window $1.45\text{--}1.88\text{ nHz}$); SCR-001 passed (Landau disruption Cassini compliance $\Delta\gamma = 4.05 \times 10^{-8}$); LEN-001 passed ($M_{\rm lens}/M_{\rm dyn} \equiv 1.00$).  
**Authority:** `papers/Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md` §4.3  
**Branch:** `recovery/v12-core-architecture`

## What this is

A rigorous RevTeX 4.2 methods and observational program paper that details the multi-scale empirical falsification framework for ITSM across pulsar timing array acoustic modes, Solar System PPN constraints, and relativistic lensing profiles.

## Build

```powershell
cd papers\P3-Observational-Program
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
```

## Allowed now

- Gate-structured falsifier *program* (conditional on closed gates)  
- Methodology placeholders (PTA polarization *if* eigenmodes exist)  
- Cite **P1** for claim hygiene; **P2** for free-field Casimir limits  

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
| `VERSION` | Outline version only |
| `README.md` | This file |

## Related readiness

- `Theory/Gates/P3_P4_READINESS.md`  
- `Theory/Gates/MAT-001/MAT-001_READINESS.md`  
- `Theory/Gates/DISK-001/DISK-001_READINESS.md`  
