# UVIR-003 — Full gate closure checklist (Master Plan critical path)

**Date:** 2026-08-04  
**Branch:** `recovery/v12-core-architecture`  
**Authority:** Master Research Plan §5.1  
**Full gate status:** **`IN_PROGRESS`** — Stage 5 decision is `HOLD_TIER1_CLOSURE`  
**Frozen manuscript (α.10):** UVIR-003 still **in progress** until a reviewed freeze upgrades wording  
**MAT-001:** **BLOCKED** for PASS tag; scoped calculation handoff already authorized  


This document is the **single map** from Master Plan wording to evidence on disk.
It does **not** close UVIR-003 by itself. Tier-1 closure requires the applicable
must rows to be physically satisfied in the declared claim domain. A scoped
exclusion, Conditional diagnostic, or programme decision cannot substitute for
matching, relevant IR control, causality, or a physical cutoff.

---

## 1. Master Plan pass condition (quote)

> UVIR-003 | Selected action stable/causal/weakly coupled in declared domain;
> invariant ratios; physical cutoff/unitarity path stated with scope.

Break into **must** criteria (M1–M5) and **supporting** evidence (S*).

| ID | Criterion | Status | Evidence / notes |
|----|-----------|--------|------------------|
| **M1** | Selected two-sector preferred-frame action declared | **PASS (bounded)** | Stage A + UVIR-002 route; Track A force retention of exact $Y^{3/2}$ |
| **M2** | Stability / positivity in declared domain | **PARTIAL_BOUNDED_HIGH_Q_ONLY** | Stage 1 verifies a bounded high-$q$+Track-A slice; the relevant IR complex-quartet response remains uncontrolled |
| **M3** | Causality in declared domain | **HOLD_MATCHED_INVARIANT_REQUIRED** | Stage 4 preserves Conditional diagnostics, but matched $Aq/K_Q$ (or an equivalent invariant) is still required |
| **M4** | Weak coupling / unitarity **path stated with scope** | **PASS (scoped)** | `PASS_DECLARED_UNITARITY_EFT_CRITERION` — tree/NDA + Green health; **not** optical theorem |
| **M5** | Invariant ratios for force normalization | **PASS (inventory)** | `PASS_KQ_MATCHING_INVENTORY_OPEN` — $Aq/K_Q$, $A/K_Q^{3/2}$, …; **numeric $K_Q$ NOT_DERIVED** |
| **M6** | Physical cutoff | **HOLD_PHYSICAL_CUTOFF_REQUIRED** | The Conditional NDA $\Lambda_\parallel$ diagnostic is not a gauge-invariant matched physical cutoff |
| **M7** | Matter sector ready for MAT handoff | **PARTIAL_SCOPED_HANDOFF_ONLY** | Provisional MAT engineering is allowed; MAT PASS and downstream Derived use remain blocked |

**Interpretation for MAT-001**

- UVIR-003 remains **`IN_PROGRESS`**; Stage 5 records `HOLD_TIER1_CLOSURE`.
- M2, M3, M6 and M7 remain incomplete at tier 1; $K_Q$ is NOT_DERIVED and $V$ is NOT_COMPUTED.
- Serial Stage 3 is a **partial scoped calculation handoff**, not a MAT PASS.
- Compute the matched invariant, reopen Stage 4A, and run a later independent Stage 5 review before any UVIR or MAT PASS.

---

## 2. Supporting subgate ledger (post–α.9 / α.10)

| Tag | Role | Status |
|-----|------|--------|
| Stage A | Architecture + flat decoupling checks | PASS (Stage A) |
| Local four-leg kernel (tetra) | α.9 freeze | `PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL` |
| Four-leg kinematic deformation | Off-tetra robustness | `PASS_FOUR_LEG_KINEMATIC_DEFORMATION_AUDIT` (if present on branch) |
| Local adiabatic packet norm | Observable proxy, not S-matrix | `PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION` |
| FRW in-in path declared | Path only | `PASS_FRW_IN_IN_OBSERVABLE_PATH_DECLARED` |
| Multi-slice + $G_{\mathrm{mp}}$ | High-$q$ Green proxy | `PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN` |
| Nonzero-gradient $\lvert\nabla\pi\rvert^3$ | Track A local | `PASS_NONZERO_GRADIENT_FORCE_LOCAL` |
| Declared unitarity/EFT criterion | Scoped | `PASS_DECLARED_UNITARITY_EFT_CRITERION` |
| $K_Q$ matching inventory | Invariants + routes | `PASS_KQ_MATCHING_INVENTORY_OPEN` |
| Causality domain (Conditional R1) | M3 documentation | `PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING` |
| Matching-route program (R2/R3 maps) | Toward M3/M6 | `PASS_MATCHING_ROUTE_PROGRAM_OPEN` |
| Declared weakly-coupled domain | Stage 1 / M2 | `PASS_DECLARED_WEAK_COUPLING_DOMAIN` |
| Conditional matching floor | Stage 2b | `PASS_CONDITIONAL_MATCHING_FLOOR` |
| Floor diagnostics | Stage 2c | `PASS_STAGE2C_FLOOR_DIAGNOSTICS` |
| MAT scoped calc (provisional) | Stage 3 | `PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL` (no MAT PASS) |
| Conditional M3/M6 record | Stage 4 | `PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT` — insufficient for tier-1 closure |
| Full-gate decision audit | Stage 5 | `PASS_STAGE5_DECISION_HOLD_TIER1` → `IN_PROGRESS` / `HOLD_TIER1_CLOSURE` |
| Full-gate checklist audit | Evidence ledger | `PASS_UVIR003_CLOSURE_CHECKLIST_AUDIT` |
| Serial stage order | Process control | `UVIR-003_SERIAL_STAGE_ORDER.md` |

Machine audit:  
`python Analysis/UVIR/UVIR-003/uvir003_full_gate_closure_audit.py`

Conditional M3 domain:  
`python Analysis/UVIR/UVIR-003/uvir003_causality_domain_under_conditional_matching.py`

Matching-route program:  
`python Analysis/UVIR/UVIR-003/uvir003_matching_route_program.py`

---

## 3. Remaining work (ordered for critical path)

### P0 — required for full UVIR-003 PASS (as written in Master Plan)

1. **Matching of invariant $Aq/K_Q$ (or $A/K_Q^{3/2}$)** via a named route  
   - Prefer R2 (MAT) once force domain is accepted, or R3 if UV data exist  
   - R1 dimensional analogy remains **Conditional candidate only** (not Derived)  
2. **Causality statement with matched invariants**  
   - Re-evaluate $q_\times(\theta)$ and domain of $v_{\mathrm{ph}}\le 1$ after matching  
3. **Physical cutoff / strong-coupling scale** with matched normalization  
   - Upgrade NDA $\Lambda_\parallel$ from diagnostic to a matched physical scale in the claim domain  

### P1 — strongly recommended before MAT Derived claims

4. Optical theorem / multi-channel unitarity **or** explicit permanent exclusion from UVIR scope  
5. Control the relevant IR transfer / complex-quartet response in the intended claim domain  
6. Full in-in integrals: keep as Open **or** schedule under a later gate (do not smuggle as PASS)

### P2 — parallel (not on critical path for MAT)

7. Identity tracks TOP/VOR/WAK/$Q_{\mathrm{syn}}$  
8. DISK/STAT Conditional lane (fits without Derived $C_{\mathrm{obs}}$)

---

## 4. What is already enough for *honest* programme progress

| Activity | OK now? |
|----------|---------|
| Manuscript freezes recording path package (α.10) | Yes |
| Conditional AQUAL disk methods (DISK methods package) | Yes |
| Declaring MAT interface (readiness) without Derived vertex | Yes |
| Claiming UVIR-003 **Derived** closed / MAT PASS | **No** |
| Citing UVIR-003 as physically closed under `PASS_BOUNDED_CONDITIONAL` | **No** — superseded by Stage 5 hold |
| MAT engineering under scoped handoff | **Yes** (no MAT PASS tag) |
| P3/P4 full drafts with Derived packaging | **No** (Conditional language only until further work) |

---

## 5. Serial order (each stage complete before next)

Authoritative process doc: **`UVIR-003_SERIAL_STAGE_ORDER.md`**.

| Stage | Content | Status |
|-------|---------|--------|
| 0 | Path package, inventory, M3 doc, route maps | **DONE** |
| **1** | M2 domain freeze (exclude IR HOLD) | **DONE** (`PASS_DECLARED_WEAK_COUPLING_DOMAIN`) |
| **2** | Matching floor without MAT (R3 → Conditional floor + 2c) | **DONE** Conditional-with-scope |
| **3** | Scoped MAT calculation ($V$, $C_{\mathrm{obs}}$) | **PARTIAL** provisional structure — no MAT PASS; $V$ NOT_COMPUTED |
| **4** | Upgrade M3/M6 with matched $V$ | **HOLD** — Conditional record exists; Stage 4A must reopen after matching |
| **5** | UVIR-003 full-gate decision | **HOLD** — `PASS_STAGE5_DECISION_HOLD_TIER1`; full gate `IN_PROGRESS` |
| **6** | DISK full + STAT | Conditional methods may continue; Derived claim path waits for UVIR/MAT |
| 7 | P3/P4 full drafts | Conditional language only until further Derived work |

**Next single action:** compute $V$, or an equivalent matched invariant, then reopen Stage 4A.  
**Never** promote R1 naive to Derived. **Never** MAT PASS without MAT checklist.

Parallel methods only: DISK Conditional lane; TOP/VOR/WAK sketches.

---

## 6. Document control

| Version | Date | Note |
|---------|------|------|
| 1.0 | 2026-08-03 | Initial closure map + machine audit |
| 1.1 | 2026-08-03 | Ran audit + Conditional causality domain; M3 documented; next = matching |
| 1.2 | 2026-08-03 | Matching-route program PASS; R2 $V$ target explicit; next = A/B/C decision |
| 1.3 | 2026-08-03 | Serial order adopted; Stage 1 M2 domain freeze PASS_BOUNDED |
| 1.4 | 2026-08-04 | Stage 2a R3 audit exits Classification C; Stage 2b Conditional floor next |
| 1.5 | 2026-08-04 | Stage 2b Conditional matching floor PASS; Stage 2 exit CONDITIONAL_WITH_SCOPE; next Stage 3 scoped MAT calc |
| 1.6 | 2026-08-04 | Stages 2c + 3: floor diagnostics PASS; MAT scoped calc provisional (no PASS); next Stage 4 |
| 1.7 | 2026-08-04 | Stage 4 branch B: permanent Conditional M3/M6 limit PASS; next Stage 5 full-gate decision |
| 1.8 | 2026-08-04 | Stage 5 tier-1: PASS_BOUNDED_CONDITIONAL; not Derived closed; MAT PASS still forbidden; next Stage 6 |
| 1.9 | 2026-08-04 | Corrected policy-defined Stage 5 pass to fail-closed HOLD_TIER1_CLOSURE; restored UVIR IN_PROGRESS and Stage 4A matched-invariant critical path |
