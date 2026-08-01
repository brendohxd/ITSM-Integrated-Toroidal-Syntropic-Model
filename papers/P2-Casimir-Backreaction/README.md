# P2 — Rectangular \(T^3\) Casimir stress and free-field backreaction

**Status:** Draft scaffold (firewall-safe claims)  
**Branch:** `recovery/v12-core-architecture`  
**Science source:** `Analysis/Casimir/CBR-001/` (Stages 1–3B)  
**Claim firewall:** `papers/Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md`  
**Master plan:** `Theory/Core/ITSM_Master_Research_Plan.md`

## Core claim (allowed)

For a free massless scalar on rectangular flat \(T^3\), renormalized lattice
Casimir stress is anisotropic and validated; free-field biaxial backreaction
produces only *transient* passages near \(H_t/H_p=13/12\), with no
quasi-plateau or attractor.

## Must not claim

- Parameter-free \(H_0=72.97\) or persistent free-field \(13/12\) attractor  
- Geometric \(a_0\) / MOND scale from this topology  
- Doughnut \(T^2\) as flat \(T^3\)  
- Simulated box is Planck-safe cubic cosmology  
- Companion P1 as establishing geometric invariants  

## Build

```powershell
conda activate itsm_env
cd papers\P2-Casimir-Backreaction
.\Build-P2.ps1
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
- [x] Rectangular \(T^3\) figure (not doughnut)  
- [x] Stage-1 / Stage-3B tables from validated outputs  
- [ ] Optional: embed Stage-2 stress panel + threshold \(\epsilon\) figure  
- [ ] Final abstract freeze + cover letter  
- [ ] arXiv / venue pass after internal hostile read  
