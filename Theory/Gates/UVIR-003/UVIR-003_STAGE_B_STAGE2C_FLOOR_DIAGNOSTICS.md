# UVIR-003 Stage B — Stage 2c floor diagnostics (causality + NDA)

**Date:** 2026-08-04  
**Serial stage:** **2c**  
**Subgate:** `PASS_STAGE2C_FLOOR_DIAGNOSTICS`  
**Claim status:** **Conditional**  
**physics_pass:** **false**  
**MAT-001:** **BLOCKED**  
**UVIR full gate:** **IN PROGRESS**  
**\(K_Q\):** **NOT_DERIVED**

## Purpose

Re-evaluate long-wavelength causality domain and NDA \(\Lambda_\parallel\)
diagnostics under the Stage **2b** Conditional matching floor parameter

\[
P \;:=\; k_Q \;\text{or}\; Z_\psi r_\rho,
\qquad
I_{a_0}=\frac{2}{3}\frac{C_{\mathrm{IR}}}{P}.
\]

## Results (Conditional)

- Analytic \(R_c = q/q_\times\) identity machine-checked on full \((P,C_{\mathrm{IR}},q/a_0)\) scan.  
- Naive comparison \((P,C_{\mathrm{IR}})=(1,2/3)\): \(q_\times^\parallel/a_0=0.375\), \(R_c=8/3\) — **NON_DERIVED_COMPARISON_ONLY**.  
- \(\Lambda_\parallel\) under floor expressed symbolically; numeric rows only in diagnostic \((G,a_0)=(1,1)\) units — **not** physical cutoff.

## Reproduce

```powershell
python Analysis\UVIR\UVIR-003\uvir003_stage2c_floor_diagnostics.py
# expect: PASS_STAGE2C_FLOOR_DIAGNOSTICS
```

## Non-claims

No Derived \(K_Q\), no physical cutoff, no MAT PASS, no UVIR full PASS, no observations.
