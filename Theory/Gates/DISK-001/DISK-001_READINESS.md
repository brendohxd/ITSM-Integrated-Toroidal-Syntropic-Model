# DISK-001 — Readiness checklist (disk / morphology solver)

**Status:** **IN PROGRESS** — Stages 0–3 **PASS** (Stage 3: axisymmetric \(R\)–\(z\) nonlinear AQUAL, residual \({\sim}10^{-9}\)); full gate open until multipole-BC + report  



**Branch:** `recovery/v12-core-architecture`  
**Date:** 2026-08-03  
**Authority:** Master Research Plan §5.1; Selective Publishing Plan §4.4 (P4)

## What DISK-001 is

A **periodic nonlinear** weak-field / force-sector solver for:

- sphere and disk geometries,  
- quantified **curl / non-potential** residuals on compact domains if relevant,  
- controlled morphology dependence before any “coupling is morphology-independent” claim.

**Pass when (Master Plan):** periodic nonlinear solver; sphere + disk; curl quantified.

## Why it is not open for Derived packaging yet

| Dependency | Role for DISK |
|------------|----------------|
| IR force law | Need either **matched** \(\Cobs\) (MAT-001) or **explicit Conditional** AQUAL-class inputs |
| UVIR-003 | Upstream of derived force; Conditional IR still allowed for solver *development* |
| Matter sector | Baryonic \(\rho_b\) as external source; no halo fields as free functions |
| Compact \(T^3\) hygiene | Compensated sources / curl caution (P1) if domain is compact |

**Allowed early work:** implement solvers under **declared** \((a_0,\Cobs)\) without claiming geometry-derived coefficients.  
**Forbidden early packaging:** “DISK proves topology \(\Rightarrow a_0\)” or dual RAR (**B9**).

## P4 hard gate

Selective Publishing Plan: **DISK-001 before claiming morphology-independent coupling.**  
Full P4 draft also needs **STAT-001**.

## Open checklist

### Physics / numerics

- [x] Declare IR law used (matched MAT vs Conditional AQUAL \(\Cobs\sim 1\)) — Stage 0 Conditional  
- [x] Sphere test: Plummer deep-MOND / AQUAL benchmark (Stage 0)  
- [x] Thin disk: midplane exponential + AQUAL (Stage 0; not full 2D/3D Poisson)  
- [x] Quantify curl residual of algebraic AQUAL map (Stage 0 diagnostic)  
- [x] Nonlinear AQUAL/Poisson potential solver (2D Picard FD — Stages 1–2)  
- [x] Discrete residual = same operator as solve; 2D log free-space BC (Stage 2)  
- [x] Axisymmetric \(R\)–\(z\) nonlinear AQUAL (Stage 3)  
- [ ] 3D thin-disk solver (optional upgrade)  

- [ ] Compact-domain option: compensated source protocol (P1 hygiene)  
- [x] Convergence: multi-resolution table with \(\varepsilon\sim10^{-9}\) (Stage 2)  



### Claim hygiene

- [ ] Inputs table: \(a_0\), \(\Cobs\), distance scale, \(\Upsilon_\star\) policy  
- [ ] **Never** default dual \(a_0=cH_0/2\pi\) + \(\Cobs=2/3\) as RAR (**B9**)  
- [ ] No SPARC global \(H_0\) claim from fits (**B15**)  
- [ ] Ledger update when PASS  

### Deliverables for PASS report

- [ ] `Theory/Gates/DISK-001/DISK-001_GATE_REPORT.md`  
- [ ] Reproducible scripts under `Analysis/` (or `Scripts/`) with seed + env  
- [ ] Figures suitable for P4 methods (not science claims beyond the gate)  

## Minimal path to P4 (two lanes)

| Lane | IR inputs | When legitimate |
|------|-----------|-----------------|
| **A — Derived path** | MAT-001 \(\Cobs\) | After UVIR-003 + MAT |
| **B — Conditional path** | Declared \(\Cobs\sim 1\), phenomenological \(a_0\) | Master Plan §6; still need DISK+STAT; never call Derived |

## Related

- P1: \(\Cobs\) invariant + no-gos  
- P4: Selective Publishing §4.4  
- STAT-001: `Theory/Gates/STAT-001/STAT-001_READINESS.md`  
