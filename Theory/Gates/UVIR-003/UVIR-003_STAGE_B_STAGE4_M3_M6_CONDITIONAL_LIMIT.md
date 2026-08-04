# UVIR-003 Stage B — Stage 4 Conditional M3/M6 record

**Date:** 2026-08-04  
**Branch:** `recovery/v12-core-architecture`  
**Serial stage:** **4**  
**Subgate:** `PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT`  
**Record:** **Conditional programme limit pending matched Stage 4A reopen**  
**Stage 4 status:** `HOLD_MATCHED_STAGE4A_REQUIRED`  
**Claim status:** Conditional diagnostic record; insufficient for tier-1 closure  
**physics_pass:** **false**  
**Full UVIR-003 gate:** **IN PROGRESS**; Stage 5 decision is `HOLD_TIER1_CLOSURE`  
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
| **B record** | Preserve Conditional diagnostics when matching is unavailable; this does not satisfy tier-1 closure |

Stage 3 left \(V=C_m/\sqrt{K_Q}\) **NOT_COMPUTED** and \(K_Q\) **NOT_DERIVED**.
The honest record is a **Conditional branch-B diagnostic**, not an accepted physics close. Stage 4A must reopen once \(V\), or an equivalent invariant, is matched.

## Programme record (branch B)

**Record:** `CONDITIONAL_M3_M6_LIMIT_REOPEN_REQUIRED`  
The historical “permanent” label means only that the Conditional diagnostic remains on record until replaced; it is not a physics pass and not a ban on a later Derived upgrade.

### M3 — causality

| Field | Value |
|-------|--------|
| Status | **`HOLD_MATCHED_INVARIANT_REQUIRED`** |
| Meaning | Causality domain documented under Stage 2b floor (free \(P,C_{\mathrm{IR}}\)) + 2c diagnostics |
| Evidence | Conditional causality domain; matching floor; 2c scan (320 rows) |
| Not claimed | Derived matched \(Aq/K_Q\); naive \(q_\times/a_0=0.375\) as Derived |

### M6 — physical cutoff

| Field | Value |
|-------|--------|
| Status | **`HOLD_PHYSICAL_CUTOFF_REQUIRED`** |
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
| M2 | PARTIAL_BOUNDED_HIGH_Q_ONLY |
| M3 | **HOLD_MATCHED_INVARIANT_REQUIRED** |
| M4 | PASS_SCOPED |
| M5 | PASS_INVENTORY (\(K_Q\) NOT_DERIVED) |
| M6 | **HOLD_PHYSICAL_CUTOFF_REQUIRED** |
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

- Compute \(V\), or an equivalent matched invariant, from one declared action/field chart.  
- Reopen **Stage 4A** for matched causality, relevant IR control, and a physical cutoff/unitarity result.  
- Run a later independent Stage 5 closure review; current decision is `HOLD_TIER1_CLOSURE`.  
- Alpha.11 may record this open checkpoint after review, but must not describe a bounded Conditional close.  
- Never promote R1 naive to Derived.
