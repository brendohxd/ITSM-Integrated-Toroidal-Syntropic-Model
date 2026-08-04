# UVIR-003 Stage B — Stage 4 permanent Conditional M3/M6 limit

**Date:** 2026-08-04  
**Branch:** `recovery/v12-core-architecture`  
**Serial stage:** **4**  
**Subgate:** `PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT`  
**Branch taken:** **B — permanent Conditional programme limit**  
**Stage 4 exit:** `PERMANENT_CONDITIONAL_M3_M6`  
**Claim status:** Conditional permanent programme limit  
**physics_pass:** **false**  
**Full UVIR-003 gate:** still **IN PROGRESS** (Stage 5)  
**MAT-001:** still **BLOCKED** for PASS  
**Numeric \(K_Q\):** **NOT_DERIVED**  
**\(V\):** **NOT_COMPUTED**

## Master Plan / serial alignment

Stage 4 goal (serial order):

> Substitute matched \(V\) (and \(\Cobs\)) into route maps → re-evaluate
> \(q_\times\), \(\Lambda_\parallel\).

Exit criterion (either branch):

| Branch | Criterion |
|--------|-----------|
| **A** | Derived path: M3 not OPEN/PARTIAL once matched \(V\) applied |
| **B** | Explicit **permanent Conditional** limit accepted by programme for M3/M6 |

Stage 3 left \(V=C_m/\sqrt{K_Q}\) **NOT_COMPUTED** and \(K_Q\) **NOT_DERIVED**.
Honest path is **branch B** — not inventing \(V\), not promoting R1 naive.

## Programme decision (branch B)

**Decision:** `PERMANENT_CONDITIONAL_M3_M6_LIMIT`

### M3 — causality

| Field | Value |
|-------|--------|
| Status | **`PERMANENT_CONDITIONAL_WITH_SCOPE`** |
| Meaning | Causality domain documented under Stage 2b floor (free \(P,C_{\mathrm{IR}}\)) + 2c diagnostics |
| Evidence | Conditional causality domain; matching floor; 2c scan (320 rows) |
| Not claimed | Derived matched \(Aq/K_Q\); naive \(q_\times/a_0=0.375\) as Derived |

### M6 — physical cutoff

| Field | Value |
|-------|--------|
| Status | **`PERMANENT_CONDITIONAL_NDA_DIAGNOSTIC`** |
| Meaning | Cutoff remains Conditional NDA diagnostic under floor \(P\); tree/NDA unitarity path still scoped |
| Evidence | Declared unitarity criterion + floor/2c \(\Lambda_\parallel\) structure |
| Not claimed | Derived matched strong-coupling scale; optical theorem |

### Rationale

1. Stage 3 scoped MAT did not compute \(V\).  
2. \(K_Q\) remains NOT_DERIVED (inventory; R3 Classification C).  
3. R2 structural theorem: static \(\Cobs\) alone cannot fix \(Aq/K_Q\) without \(V\).  
4. R1 naive \((P,C_{\mathrm{IR}})=(1,2/3)\) remains `NON_DERIVED_COMPARISON_ONLY`.

## Branch A scaffold (not applied)

If \(V\) is later Derived from \(S_{\mathrm{int}}\), re-open Stage 4 branch A and substitute:

\[
I_{a_0}=\frac{C_{\mathrm{IR}}^{1/3}\,V^{2}}{12\pi G\,\Cobs^{4/3}},
\qquad
K_Q=\frac{C_m^{2}}{V^{2}},
\qquad
\Lambda_\parallel \sim \frac{K_Q^{3/4}}{\sqrt{A}}.
\]

Machine scaffold recorded under `branch_A_scaffold_if_V_later` (status
`SCAFFOLD_ONLY_REQUIRES_DERIVED_V`).

## Explicit non-claims

- No UVIR-003 **full-gate PASS** (Stage **5** decides)  
- No **MAT-001 PASS**  
- No downstream Derived SCR/LEN/DISK/P3/P4 unlock  
- No Derived \(K_Q\), \(V\), or physical cutoff  
- No SPARC / \(H_0\) validation  

## Master Plan criteria after Stage 4

| ID | Status |
|----|--------|
| M1 | PASS_BOUNDED |
| M2 | PASS_BOUNDED |
| M3 | **PERMANENT_CONDITIONAL_WITH_SCOPE** |
| M4 | PASS_SCOPED |
| M5 | PASS_INVENTORY (\(K_Q\) NOT_DERIVED) |
| M6 | **PERMANENT_CONDITIONAL_NDA_DIAGNOSTIC** |
| M7 | OPEN — MAT blocked for PASS |

## Reproduce

```powershell
python Analysis\UVIR\UVIR-003\uvir003_conditional_matching_floor.py
python Analysis\UVIR\UVIR-003\uvir003_stage2c_floor_diagnostics.py
python Analysis\MAT\MAT-001\mat001_scoped_calculation.py
python Analysis\UVIR\UVIR-003\uvir003_stage4_m3m6_conditional_limit.py
# expect: PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT
# stage_4_exit: PERMANENT_CONDITIONAL_M3_M6
# physics_pass: False
```

## Next

- **Stage 5 — DONE (tier-1):** `PASS_BOUNDED_CONDITIONAL` (not Derived closed).  
- **Stage 6 next:** DISK/STAT claim-grade path; optional \(V\) for Stage 4A.  
- **Optional:** α.11 freeze recording Conditional bounded close.  
- Never promote R1 naive to Derived.
