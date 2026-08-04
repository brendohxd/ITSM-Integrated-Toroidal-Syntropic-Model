# UVIR-003 Stage B — Conditional matching floor (Stage 2b)

**Date:** 2026-08-04  
**Branch:** `recovery/v12-core-architecture`  
**Serial stage:** **2b**  
**Subgate:** `PASS_CONDITIONAL_MATCHING_FLOOR`  
**Claim status:** **Conditional-with-scope**  
**physics_pass:** **false**  
**Full UVIR-003 gate:** **IN PROGRESS**  
**MAT-001:** **BLOCKED** (scoped calculation handoff text only — **not** MAT PASS)  
**Numeric \(K_Q\):** **NOT_DERIVED**

## Context

Stage **2a** R3 UV residue audit terminated as  
**`INCOMPLETE_R3_UV_RESIDUE`** (Classification C): no action-level \(Z_\psi\),
\(r_\rho\). Serial order then requires a **Conditional matching floor** with
explicit scope so M3/M6 are documented without fake Derived packaging.

## Floor structure (Conditional)

Introduce free product parameter

\[
P \;:=\; k_Q \quad\text{(R1)} \quad\text{or}\quad Z_\psi r_\rho \quad\text{(R3 residual rename)}.
\]

Algebra (same as matching-route program):

\[
I_{a_0}=\frac{2}{3}\,\frac{C_{\mathrm{IR}}}{P},\qquad
\frac{q_\times(\theta)}{a_0}=\frac{P}{2\,C_{\mathrm{IR}}\,(1+\cos^2\theta)}.
\]

\(P>0\) and \(C_{\mathrm{IR}}>0\) remain **free Conditional** parameters.
Domain tables under R1 structure are already on disk  
(`PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING`).

### Naive point — comparison only

\((P,C_{\mathrm{IR}})=(1,2/3)\) ⇒ \(I_{a_0}=4/9\), \(q_\times^\parallel/a_0=0.375\),
\(R_c(\parallel,q=a_0)=8/3\).

**Label:** `NON_DERIVED_COMPARISON_ONLY` — priority flag, **not** Derived.

## Scope after 2b

| In scope (Conditional) | Forbidden |
|------------------------|-----------|
| Referee M3 documentation under free \((P,C_{\mathrm{IR}})\) | Derived numeric \(K_Q\) / \(Z_\psi,r_\rho\) from this floor |
| NDA \(\Lambda_\parallel\) as diagnostic once \(P,C_{\mathrm{IR}}\) chosen Conditional | MAT-001 **PASS** |
| Stage 3 **scoped** MAT calculation of \(V,\Cobs\) under handoff text | UVIR full-gate PASS |
| | Physical cutoff as Derived |
| | SPARC / \(H_0\) / cosmology |

### Master Plan criteria after floor

| ID | Status |
|----|--------|
| M3 | PARTIAL — **documented Conditional-with-scope** |
| M6 | OPEN — Conditional NDA diagnostic only |
| M7 | OPEN — MAT blocked for PASS |

## MAT scoped handoff amendment (text only)

**Authorizes:** declare \(S_{\mathrm{int}}\); compute *provisional* \(V=C_m/\sqrt{K_Q}\)
and \(\Cobs\) under named premises; map invariants.

**Does not authorize:** MAT PASS report; downstream Derived use before UVIR
Stage 5; SPARC/\(H_0\) validation; UVIR full PASS.

## Stage 2 exit

```text
status: CONDITIONAL_WITH_SCOPE
allows_stage3_scoped_MAT_calculation: true
allows_MAT_PASS: false
allows_UVIR_full_PASS: false
```

## Reproduce

```powershell
conda activate itsm_env
python Analysis\UVIR\UVIR-003\uvir003_r3_uv_residue_audit.py
python Analysis\UVIR\UVIR-003\uvir003_conditional_matching_floor.py
# expect: PASS_CONDITIONAL_MATCHING_FLOOR
# physics_pass: False
```

## Next

- **2c — DONE:** `PASS_STAGE2C_FLOOR_DIAGNOSTICS` (causality + NDA under this floor).  
- **Stage 3 — DONE (scoped):** `PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL` — still no MAT PASS; \(V\) NOT_COMPUTED.  
- **Stage 4 — DONE (branch B):** `PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT`.  
- **Stage 5 next:** full-gate programme decision (or reopen Stage 4A if \(V\) computed).  
- Never promote R1/R3 naive \(O(1)\) to Derived.
