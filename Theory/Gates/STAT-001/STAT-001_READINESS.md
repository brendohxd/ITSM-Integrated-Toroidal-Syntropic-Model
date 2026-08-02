# STAT-001 — Readiness checklist (matched statistical pipeline)

**Status:** **Not started as a closed gate** (readiness only)  
**Branch:** `recovery/v12-core-architecture`  
**Date:** 2026-08-03  
**Authority:** Selective Publishing Plan §4.4 (P4); Master Plan claim hygiene

## What STAT-001 is

A **matched** inference pipeline for rotation-curve / SPARC-style comparisons under
**declared** model inputs, so that:

- likelihood / BIC / residual stats are defined once,  
- nuisance parameters (\(\Upsilon_\star\), distances, inclination policy) are explicit,  
- global \(p\)-values are not quoted without a fixed analysis plan.

**P4 rule:** STAT-001 matched pipeline **before any global \(p\)-value**.

## Prerequisites

| Item | Requirement |
|------|-------------|
| DISK-001 (or controlled disk approximation) | Model prediction \(v_{\mathrm{mod}}(R)\) under declared IR |
| Data interface | SPARC (or successor) loaders; quality cuts documented |
| Declared \((a_0,\Cobs)\) | Inputs, not “derived from topology” |

## Open checklist

- [ ] Analysis plan written **before** unblinding global metrics (or explicitly exploratory)  
- [ ] Likelihood: Gaussian / Student-t / reported SPARC errors — pick one and stick  
- [ ] \(\Upsilon_\star\): fixed grid vs free per galaxy — declare  
- [ ] BIC / AIC definition fixed (parameter count rules)  
- [ ] Cross-validation or holdout policy if claiming generality  
- [ ] **Ban B15:** no \(p=0.62\) packaging; no “SPARC measures cosmic \(H_0\)”  
- [ ] **Ban B9:** no dual RAR normalization  
- [ ] Reproduce script + seed + env pin  
- [ ] `STAT-001_GATE_REPORT.md` on PASS  

## Relation to P3/P4

- **P4** requires DISK-001 + STAT-001.  
- **P3** does **not** require STAT-001; P3 needs a *derived observable* or clean mapped limit, not SPARC significance theater.

## Related

- `Theory/Gates/DISK-001/DISK-001_READINESS.md`  
- `papers/Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md` §4.4  
