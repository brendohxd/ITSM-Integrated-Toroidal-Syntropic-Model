# P2 — Anisotropic Casimir on rectangular $T^3$ (instantaneous-closure control)

**Directory:** `papers/P2-Rectangular-T3-Casimir/`  
**VERSION:** see `VERSION` (currently `0.1.0-draft`)  
**Current locally verified PDF:** `Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Instantaneous-Closure-Control_v0.1.0-draft.pdf`
(written directly by the build script with a matching `.sha256` sidecar; see
`papers/PAPERS_NAMING.md`)

**Status:** `NO_GO_CURRENT_CANDIDATE`; locally repaired, independent Role-A/Role-B audits pending
**Branch:** `recovery/v12-core-architecture`  
**Science source:** `Analysis/Casimir/CBR-001/` (Stages 1–3B)  
**Claim firewall:** `papers/Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md`  
**Master plan:** `Theory/Core/ITSM_Master_Research_Plan.md`

## Core claim (allowed)

The implemented already-renormalized periodic-scalar stress is anisotropic on
rectangular flat $T^3$ and passes the recorded internal controls. When that
static stress is transported through the declared instantaneous $a^{-4}$
Bianchi-I closure, the bounded scan produces only *transient* passages near
$H_t/H_p=13/12$, with no quasi-plateau or attractor. This is not a general
dynamical-QFT no-go theorem.

## Must not claim

- Parameter-free $H_0=72.97$ or persistent free-field $13/12$ attractor  
- Geometric $a_0$ / MOND scale from this topology  
- Doughnut $T^2$ as flat $T^3$  
- Simulated box is Planck-safe cubic cosmology  
- Companion P1 as establishing geometric invariants  
- A general free-field result on evolving compact Bianchi-I spacetime
- Publication readiness before independent analytic, numerical and PDF audits

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
python cbr001_stage2_standalone.py --output-dir stage2_outputs
python cbr001_stage3_backreaction.py --stage2-csv stage2_outputs\cbr001_stage2_scan.csv --output-dir stage3_outputs
python cbr001_stage3b_ratio_test.py --stage2-csv stage2_outputs\cbr001_stage2_scan.csv --output-dir stage3b_outputs
```

Do not omit the Stage-2 output flag in a fresh chained run: the Stage-2 default
is the current directory, while the downstream defaults refer to
`stage2_outputs/`.

## Draft checklist

- [x] Skeleton `main.tex`  
- [x] Port CoreRecovery §06 + CBR STAGE docs  
- [x] Abstract ban-list review (B1–B16 packaging)  
- [x] Rectangular $T^3$ figure (not doughnut)  
- [x] Stage-1 / Stage-3B tables from validated outputs  
- [x] Stage-2 anisotropy + Stage-3B ratio/threshold figures  
- [x] Portable candidate hashes and explicit Stage-2 chain
- [x] Cover letter draft (`CoverLetter.txt`)  
- [x] Superseded hostile read retained with withdrawal warning
- [ ] Grok Role-A analytic normalization/closure audit
- [ ] Antigravity restricted Role-B execution witness
- [ ] Sensitivity suite and independent noncubic evaluator
- [x] Canonical named PDF rebuilt and all five pages visually inspected; source/PDF hashes frozen
- [ ] Explicit operator approval before any arXiv or journal action
