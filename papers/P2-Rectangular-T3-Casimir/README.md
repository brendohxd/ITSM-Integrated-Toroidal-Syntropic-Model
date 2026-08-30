# P2 — Anisotropic Casimir on rectangular $T^3$ (free-field backreaction)

**Directory:** `papers/P2-Rectangular-T3-Casimir/`  
**VERSION:** see `VERSION` (currently `0.1.0-draft`)  
**Share PDF:** `Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Free-Field_Backreaction_v0.1.0-draft.pdf`  
(build script writes this from `main.pdf` + `VERSION`; see `papers/PAPERS_NAMING.md`)

**Status:** Draft scaffold (firewall-safe claims)  
**Branch:** `recovery/v12-core-architecture`  
**Science source:** `Analysis/Casimir/CBR-001/` (Stages 1–3B)  
**Claim firewall:** `papers/Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md`  
**Master plan:** `Theory/Core/ITSM_Master_Research_Plan.md`

## Core claim (allowed)

For a free massless scalar on rectangular flat $T^3$, renormalized lattice
Casimir stress is anisotropic and validated; free-field biaxial backreaction
produces only *transient* passages near $H_t/H_p=13/12$, with no
quasi-plateau or attractor.

## Must not claim

- Parameter-free $H_0=72.97$ or persistent free-field $13/12$ attractor  
- Geometric $a_0$ / MOND scale from this topology  
- Doughnut $T^2$ as flat $T^3$  
- Simulated box is Planck-safe cubic cosmology  
- Companion P1 as establishing geometric invariants  

## Build

```powershell
conda activate itsm_env
cd papers\P2-Rectangular-T3-Casimir
.\Build-P2-Rectangular-T3-Casimir.ps1
```

## Reproduce science

```powershell
conda activate itsm_env
cd Analysis\Casimir\CBR-001
python casimir_t3_lattice.py
python cbr001_stage2_standalone.py
python cbr001_stage3_backreaction.py
python cbr001_stage3b_ratio_test.py
```

## Draft checklist

- [x] Skeleton `main.tex`  
- [x] Port CoreRecovery §06 + CBR STAGE docs  
- [x] Abstract ban-list review (B1–B16 packaging)  
- [x] Rectangular $T^3$ figure (not doughnut)  
- [x] Stage-1 / Stage-3B tables from validated outputs  
- [x] Stage-2 anisotropy + Stage-3B ratio/threshold figures  
- [x] `CBR001_CHECKSUMS.md` + appendix anchors  
- [x] Cover letter draft (`CoverLetter.txt`)  
- [x] Hostile internal read (`HOSTILE_READ.md`) + minor tex fixes  
- [ ] Optional external co-read before journal submit  
- [ ] arXiv upload when author freezes CBR-001 digests + final PDF
