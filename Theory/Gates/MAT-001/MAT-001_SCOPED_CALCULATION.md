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
| $S_{\mathrm{int}}$ form $-\,C_m\rho_b\psi$ | **Declared** (architecture) |
| $C_{\mathrm{obs}}=C_m^{3/2}/\sqrt{C_{\mathrm{IR}}}$ | **Form Derived** under architecture premises |
| Special $C_m=C_{\mathrm{IR}}=C\RightarrowC_{\mathrm{obs}}=C$ | **Form Derived** |
| $I_{a_0}(C_{\mathrm{obs}},C_{\mathrm{IR}},V)$ map | **Form Derived** (matching-route identity) |
| $C_{\mathrm{obs}}\sim 1$ AQUAL baseline | **Conditional** hypothesis (Master Plan §6) — **not** micro Derived |
| $V=C_m/\sqrt{K_Q}$ from $S_{\mathrm{int}}$ | **NOT_COMPUTED** ($K_Q$ open) |
| Numeric $K_Q$ | **NOT_DERIVED** |

## Explicit non-claims

- No **MAT-001 PASS**  
- No Derived $C_{\mathrm{obs}}$ from micro $S_{\mathrm{int}}$ matching  
- No Derived $V$ or $K_Q$  
- No SPARC / $H_0$ validation  
- No dual RAR $(a_0=cH_0/2\pi,\,C=2/3)$  
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

- Compute $V=C_m/\sqrt{K_Q}$, or an equivalent matched invariant, from one declared action/field chart.  
- Reopen UVIR Stage **4A** for matched causality, relevant IR control, and physical-cutoff analysis.  
- Run a later independent Stage **5** closure review; current decision is `HOLD_TIER1_CLOSURE`.  
- MAT PASS still requires genuine UVIR closure, the MAT checklist, and claim-ledger update.
