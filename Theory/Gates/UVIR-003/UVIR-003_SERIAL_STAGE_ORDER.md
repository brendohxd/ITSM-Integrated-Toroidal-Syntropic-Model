# UVIR-003 → MAT → papers — serial stage order

**Date:** 2026-08-03  
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
| Master Plan: MAT blocked until UVIR-003 passes | No Derived MAT before UVIR domain is declared |
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

### Stage 1 — **M2 domain freeze** ← **CURRENT**

**Goal:** Master Plan “stable / weakly coupled **in declared domain**.”

**Must complete before Stage 2 claims:**

1. Permanent **include** list: high-\(q\) Green proxy, Track-A nonzero-gradient force, local packet norm (scoped).  
2. Permanent **exclude** list (out of weakly-coupled domain until separately solved):  
   - IR transfer HOLD / complex-quartet nonseparability  
   - homogeneous zero-gradient \(Y^{3/2}\) S-matrix  
   - full in-in nested integrals (Open, later gate)  
   - optical theorem (NOT_COMPUTED; out of UVIR scope or later gate)  
3. Machine audit: `PASS_DECLARED_WEAK_COUPLING_DOMAIN`  
4. M2 status → **PASS_BOUNDED** (not “all modes healthy”)

**Exit criterion:** weakly-coupled domain written + audited; no smuggling of HOLD modes as PASS.

### Stage 2 — **Matching without MAT first** (R3 attempt → Conditional floor)

**Goal:** best available \(Aq/K_Q\) / \(\Lambda_\parallel\) *before* MAT.

| Step | Action | Exit |
|------|--------|------|
| 2a | Dig-harder **R3**: bound or derive \(Z_\psi,r_\rho\) from declared UV / condensate structure | Either Derived-under-premises or **explicit fail → Conditional floor** |
| 2b | If 2a incomplete: freeze **Conditional** matched floor (R1 structure + excluded naive packaging) with referee domain tables already on disk | M3/M6 remain Conditional/OPEN with **scope**, not fake Derived |
| 2c | Re-run causality + NDA diagnostics under that floor | Domain tables updated |

**Exit criterion:** written matching status for M3/M6 (Derived *or* Conditional-with-scope).  
**Do not** open MAT Derived until Stage 1 + Stage 2 exit are recorded.

### Stage 3 — **MAT-001** (R2 vertex)

**Goal:** compute \(\Cobs\) and \(V=C_m/\sqrt{K_Q}\) from one \(S_{\mathrm{int}}\).

Prerequisites: Stage 1 PASS_BOUNDED; Stage 2 exit recorded; force sector slice frozen as MAT input.

**Exit criterion:** \(\Cobs\) and \(V\) reported under named premises; claim ledger updated; still no SPARC/\(H_0\) validation from this gate alone.

### Stage 4 — **UVIR M3/M6 upgrade** (post-MAT)

**Goal:** substitute matched \(V\) (and \(\Cobs\)) into route maps → re-evaluate \(q_\times\), \(\Lambda_\parallel\).

**Exit criterion:** M3 not OPEN/PARTIAL on Derived path *or* explicit permanent Conditional limit accepted by programme; M6 physical cutoff stated with matched norm or permanent Conditional scope.

### Stage 5 — **UVIR-003 full-gate PASS**

**Goal:** checklist M1–M6 all non-blocking under declared policy; M7 ready for MAT handoff *after* Stage 3–4 if not already sequential-complete.

**Exit criterion:** `full_gate_status = PASS` in audit; MAT unblocked for downstream Derived use.

### Stage 6 — **DISK-001 full + STAT-001** (observational pipeline)

Methods package already partial PASS. Full multipole/BC/STAT after force+matter story is frozen for claims that need them.

### Stage 7 — **P3 / P4 full drafts** (Selective Publishing Plan)

Only after Stage 5 (and Stage 6 for P4 SPARC claims).

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
| 1 | **DONE** | `PASS_DECLARED_WEAK_COUPLING_DOMAIN` — M2 PASS_BOUNDED |
| 2 | **NEXT** | Matching floor without MAT (R3 → Conditional floor) |
| 3–7 | pending | — |
