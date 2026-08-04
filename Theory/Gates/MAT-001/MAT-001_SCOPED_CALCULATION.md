# MAT-001 — Scoped calculation (UVIR serial Stage 3)

**Date:** 2026-08-04  
**Branch:** `recovery/v12-core-architecture`  
**Subgate:** `PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL`  
**MAT-001 gate PASS:** **FORBIDDEN / false**  
**physics_pass:** **false**  
**Claim status:** Conditional provisional structure  
**UVIR-003:** still **IN PROGRESS**  
**Downstream Derived use:** **not authorized**

## Authority

UVIR-003 Stage 2b handoff (`PASS_CONDITIONAL_MATCHING_FLOOR`) authorizes
**calculation only**, not a MAT PASS tag (see serial Stage 3).

## What was computed

| Item | Status |
|------|--------|
| \(S_{\mathrm{int}}\) form \(-\,C_m\rho_b\psi\) | **Declared** (architecture) |
| \(\Cobs=C_m^{3/2}/\sqrt{C_{\mathrm{IR}}}\) | **Form Derived** under architecture premises |
| Special \(C_m=C_{\mathrm{IR}}=C\Rightarrow\Cobs=C\) | **Form Derived** |
| \(I_{a_0}(\Cobs,C_{\mathrm{IR}},V)\) map | **Form Derived** (matching-route identity) |
| \(\Cobs\sim 1\) AQUAL baseline | **Conditional** hypothesis (Master Plan §6) — **not** micro Derived |
| \(V=C_m/\sqrt{K_Q}\) from \(S_{\mathrm{int}}\) | **NOT_COMPUTED** (\(K_Q\) open) |
| Numeric \(K_Q\) | **NOT_DERIVED** |

## Explicit non-claims

- No **MAT-001 PASS**  
- No Derived \(\Cobs\) from micro \(S_{\mathrm{int}}\) matching  
- No Derived \(V\) or \(K_Q\)  
- No SPARC / \(H_0\) validation  
- No dual RAR \((a_0=cH_0/2\pi,\,C=2/3)\)  
- No UVIR full-gate PASS  
- No SCR/LEN/DISK Derived unlock from this package  

## Reproduce

```powershell
python Analysis\UVIR\UVIR-003\uvir003_conditional_matching_floor.py
python Analysis\UVIR\UVIR-003\uvir003_stage2c_floor_diagnostics.py
python Analysis\MAT\MAT-001\mat001_scoped_calculation.py
# expect: PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL
# mat001_pass: False
```

## Next

- Compute \(V\) when force kinetic / \(K_Q\) chart is available  
- UVIR Stages 4–5 before any MAT PASS or Derived downstream use  
