# UVIR-003 → MAT → papers — serial stage order

**Date:** 2026-08-04  
**Branch:** `recovery/v12-core-architecture`  
**Rule:** complete each stage before the next begins (no parallel shortcutting of blockers).  
**Authority:** Master Research Plan §5; full-gate checklist.

This is the **default critical path** when the goal is honest tier-1 closure,
not speed. Conditional lanes (DISK methods, phenom \(\Cobs\sim 1\)) may run
*alongside* for methods only; they never substitute a later stage.

---

## Why this order

| Constraint | Implication |
|------------|-------------|
| Master Plan: MAT gate PASS and downstream Derived use require UVIR-003 PASS | A scoped MAT calculation needs the explicit Conditional handoff recorded at Stage 2 |
| R2 matching *is* MAT (\(V=C_m/\sqrt{K_Q}\)) | Cannot finish Derived M3/M6 via R2 before MAT |
| R1 naive is Conditional only | Never promote \((k_Q,C_{\mathrm{IR}})=(1,2/3)\) to Derived |
| IR HOLD / complex-quartet modes are structural | Must **exclude or control** before claiming “stable domain” |

Chicken-and-egg is resolved by **Stage 1 domain freeze**, then **Stage 2
matching that does not require MAT (R3 attempt + Conditional scope)**, then
**Stage 3 MAT**, then **Stage 4 upgrade M3/M6 from matched \(V\)**.

---

## Serial stages (do not skip)

### Stage 0 — Already done (do not re-open as blockers)

| Tag | Evidence |
|-----|----------|
| M1 selected action | Stage A + Track A |
| M4 unitarity **path with scope** | `PASS_DECLARED_UNITARITY_EFT_CRITERION` |
| M5 invariant inventory | `PASS_KQ_MATCHING_INVENTORY_OPEN` |
| M3 documentation (Conditional) | `PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING` |
| Route maps | `PASS_MATCHING_ROUTE_PROGRAM_OPEN` |
| α.10 path package | multi-slice Green, nonzero-grad force, … |

### Stage 1 — **M2 bounded-domain evidence** ← **PARTIAL (high-q only)**

**Goal:** Master Plan “stable / weakly coupled **in declared domain**.”

**Must complete before Stage 2 claims:**

1. Permanent **include** list: high-\(q\) Green proxy, Track-A nonzero-gradient force, local packet norm (scoped).  
2. Permanent **exclude** list (out of weakly-coupled domain until separately solved):  
   - IR transfer HOLD / complex-quartet nonseparability  
   - homogeneous zero-gradient \(Y^{3/2}\) S-matrix  
   - full in-in nested integrals (Open, later gate)  
   - optical theorem (NOT_COMPUTED; out of UVIR scope or later gate)  
3. Machine audit: `PASS_DECLARED_WEAK_COUPLING_DOMAIN`  
4. M2 status → **PARTIAL_BOUNDED_HIGH_Q_ONLY** while the relevant IR response is held

**Recorded result:** bounded high-\(q\)+Track-A domain is written and audited, but excluding a relevant HOLD mode is not tier-1 stability closure.

### Stage 2 — **Matching without MAT first** (R3 attempt → Conditional floor)

**Goal:** best available \(Aq/K_Q\) / \(\Lambda_\parallel\) *before* MAT.

| Step | Action | Exit |
|------|--------|------|
| 2a | **DONE:** R3 audit of \(Z_\psi,r_\rho\) against declared UV / condensate sources | `INCOMPLETE_R3_UV_RESIDUE`; no value or rigorous bound → Conditional floor |
| 2b | **DONE:** freeze **Conditional** matching floor (R1/R3 structure + naive excluded as packaging) | `PASS_CONDITIONAL_MATCHING_FLOOR`; M3/M6 Conditional-with-scope |
| 2c | **DONE:** causality + NDA diagnostics under Conditional floor | `PASS_STAGE2C_FLOOR_DIAGNOSTICS`; domain tables remain Conditional documentation |

**Exit criterion (Stage 2):** written matching status for M3/M6 as **Conditional-with-scope** (met by 2b).  
**Do not** issue a MAT PASS tag or use MAT output for downstream Derived claims before UVIR closure and the MAT checklist. Stage 2 authorizes only a scoped Conditional calculation handoff.

### Stage 3 — **MAT-001** (R2 vertex) ← **PARTIAL (scoped forms only)**

**Goal:** compute \(\Cobs\) and \(V=C_m/\sqrt{K_Q}\) from one \(S_{\mathrm{int}}\).

Prerequisites: Stage 1 PASS_BOUNDED; Stage 2 exit plus explicit Conditional handoff amendment; force-sector slice frozen as MAT input.

**Exit criterion (met as provisional structure):** scoped package
`PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL` freezes static-reduction forms and
Conditional \(\Cobs\sim 1\) baseline; \(V\) remains **NOT_COMPUTED** (\(K_Q\)
NOT_DERIVED). Stage 3 is therefore partial. No MAT PASS tag and no downstream Derived use before UVIR closure plus the MAT checklist.

### Stage 4 — **UVIR M3/M6 matched upgrade** ← **HOLD; REOPEN 4A**

**Goal:** substitute matched \(V\) (or an equivalent invariant) into the route
maps, then re-evaluate causality, the relevant IR response, and the physical
cutoff/unitarity result in the intended claim domain.

**Current record:** `PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT` preserves
useful Conditional diagnostics, but is **not sufficient for tier-1 closure**.
Stage 3 left \(V\) NOT_COMPUTED, so Stage 4A must reopen after matching.

### Stage 5 — **UVIR-003 full-gate decision** ← **AUDIT DONE; PHYSICS HOLD**

**Goal:** independently decide whether every tier-1 closure requirement is
physically satisfied, without converting scope exclusions into positive results.

**Current decision:**

```text
decision = HOLD_TIER1_CLOSURE
full_gate_status = IN_PROGRESS
```

M2, M3, M6 and M7 remain incomplete. The audit tag
`PASS_STAGE5_DECISION_HOLD_TIER1` means the decision machinery passed and failed
closed; it is not a physics PASS. MAT PASS and downstream Derived packaging
remain forbidden.

### Stage 6 — **DISK-001 full + STAT-001** (observational pipeline) ← **CONDITIONAL METHODS ONLY**

Methods package already partial PASS. Full multipole/BC/STAT after force+matter story is frozen for claims that need them.

### Stage 7 — **P3 / P4 full drafts** (Selective Publishing Plan)

Only after UVIR-003 and the relevant MAT/DISK/STAT triggers are genuinely closed.

---

## Explicitly not serial-critical (may parallel *methods only*)

- DISK Conditional AQUAL methods (already on branch)  
- TOP / VOR / WAK / \(Q_{\mathrm{syn}}\) identity sketches  
- Manuscript freezes recording *path*, not claim upgrades  

---

## Forbidden reordering

| Forbidden | Why |
|-----------|-----|
| MAT Derived before Stage 1 domain freeze | Matching without declared domain is packaging |
| Promote R1 naive to Derived | Speculative stack; checklist ban |
| P3/P4 full paper before Stage 5–6 triggers | Master Plan + Selective Publishing Plan |
| Call UVIR full PASS while IR HOLD modes are *in* weakly-coupled domain | M2 lie |

---

## Progress log

| Stage | Status | Commit / note |
|-------|--------|----------------|
| 0 | **DONE** | α.10 + inventory + causality Conditional + matching maps |
| 1 | **PARTIAL** | bounded high-\(q\)+Track-A evidence; relevant IR response held |
| 2 | **DONE (Conditional record)** | 2a C; 2b floor; 2c `PASS_STAGE2C_FLOOR_DIAGNOSTICS` |
| 3 | **PARTIAL** | provisional forms only; no MAT PASS; \(V\) NOT_COMPUTED |
| 4 | **HOLD / reopen 4A** | Conditional M3/M6 record is insufficient for tier-1 closure |
| 5 | **HOLD** | `PASS_STAGE5_DECISION_HOLD_TIER1`; full gate `IN_PROGRESS` |
| 6 | conditional methods only | Derived observational path waits for UVIR/MAT |
| 7 | outline only | Full P3/P4 awaits the documented triggers |
