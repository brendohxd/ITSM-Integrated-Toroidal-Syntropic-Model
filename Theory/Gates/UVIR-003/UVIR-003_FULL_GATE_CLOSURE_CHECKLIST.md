# UVIR-003 — Full gate closure checklist (Master Plan critical path)

**Date:** 2026-08-03  
**Branch:** `recovery/v12-core-architecture`  
**Authority:** Master Research Plan §5.1  
**Full gate status:** **IN_PROGRESS**  
**MAT-001:** **BLOCKED** until this gate’s pass condition is met under declared scope  

This document is the **single map** from Master Plan wording to evidence on disk.
It does **not** close UVIR-003 by itself. Closing requires every **must** row below
to be PASS (or explicitly Conditional with a referee-grade domain statement that
the programme accepts as sufficient for MAT handoff—that is a **programme
decision**, not automatic).

---

## 1. Master Plan pass condition (quote)

> UVIR-003 | Selected action stable/causal/weakly coupled in declared domain;
> invariant ratios; physical cutoff/unitarity path stated with scope.

Break into **must** criteria (M1–M5) and **supporting** evidence (S*).

| ID | Criterion | Status | Evidence / notes |
|----|-----------|--------|------------------|
| **M1** | Selected two-sector preferred-frame action declared | **PASS (bounded)** | Stage A + UVIR-002 route; Track A force retention of exact \(Y^{3/2}\) |
| **M2** | Stability / positivity in declared domain | **PASS_BOUNDED** | Stage 1 domain freeze: high-\(q\)+Track-A in; IR HOLD / complex-quartet **out** (`PASS_DECLARED_WEAK_COUPLING_DOMAIN`) |
| **M3** | Causality in declared domain | **PERMANENT_CONDITIONAL_WITH_SCOPE** | Stage 4 branch B: Conditional floor + 2c diagnostics are the programme limit until matched \(Aq/K_Q\) (`PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT`); naive \(q_\times/a_0=0.375\) still **not** Derived |
| **M4** | Weak coupling / unitarity **path stated with scope** | **PASS (scoped)** | `PASS_DECLARED_UNITARITY_EFT_CRITERION` — tree/NDA + Green health; **not** optical theorem |
| **M5** | Invariant ratios for force normalization | **PASS (inventory)** | `PASS_KQ_MATCHING_INVENTORY_OPEN` — \(Aq/K_Q\), \(A/K_Q^{3/2}\), …; **numeric \(K_Q\) NOT_DERIVED** |
| **M6** | Physical cutoff | **PERMANENT_CONDITIONAL_NDA_DIAGNOSTIC** | Stage 4 branch B: NDA \(\Lambda_\parallel\) diagnostic under floor \(P\); **not** Derived matched cutoff |
| **M7** | Matter sector ready for MAT handoff | **OPEN** | Force sector methods + scoped MAT structure exist; MAT still blocked for Derived vertex / PASS |

**Interpretation for MAT-001**

- MAT gate PASS and downstream Derived use remain blocked until UVIR-003 **passes**.
- Honest reading today: **M1–M2, M4–M5** support a declared domain + matching inventory; **M3/M6** are **permanent Conditional** (Stage 4 branch B), not Derived “stable+causal+cutoff closed.”  
- Stage 4 recorded the **programme Conditional limit** for M3/M6. Stage **5** must still decide whether that is sufficient for `full_gate_status=PASS`.  
- Do **not** open MAT Derived claims or MAT PASS until UVIR Stage 5 (or a later Derived reopen of Stage 4 branch A after \(V\) is computed).
- Serial Stage 3 remains a **scoped Conditional calculation handoff**, not a MAT PASS.

---

## 2. Supporting subgate ledger (post–α.9 / α.10)

| Tag | Role | Status |
|-----|------|--------|
| Stage A | Architecture + flat decoupling checks | PASS (Stage A) |
| Local four-leg kernel (tetra) | α.9 freeze | `PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL` |
| Four-leg kinematic deformation | Off-tetra robustness | `PASS_FOUR_LEG_KINEMATIC_DEFORMATION_AUDIT` (if present on branch) |
| Local adiabatic packet norm | Observable proxy, not S-matrix | `PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION` |
| FRW in-in path declared | Path only | `PASS_FRW_IN_IN_OBSERVABLE_PATH_DECLARED` |
| Multi-slice + \(G_{\mathrm{mp}}\) | High-\(q\) Green proxy | `PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN` |
| Nonzero-gradient \(\lvert\nabla\pi\rvert^3\) | Track A local | `PASS_NONZERO_GRADIENT_FORCE_LOCAL` |
| Declared unitarity/EFT criterion | Scoped | `PASS_DECLARED_UNITARITY_EFT_CRITERION` |
| \(K_Q\) matching inventory | Invariants + routes | `PASS_KQ_MATCHING_INVENTORY_OPEN` |
| Causality domain (Conditional R1) | M3 documentation | `PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING` |
| Matching-route program (R2/R3 maps) | Toward M3/M6 | `PASS_MATCHING_ROUTE_PROGRAM_OPEN` |
| Declared weakly-coupled domain | Stage 1 / M2 | `PASS_DECLARED_WEAK_COUPLING_DOMAIN` |
| Conditional matching floor | Stage 2b | `PASS_CONDITIONAL_MATCHING_FLOOR` |
| Floor diagnostics | Stage 2c | `PASS_STAGE2C_FLOOR_DIAGNOSTICS` |
| MAT scoped calc (provisional) | Stage 3 | `PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL` (no MAT PASS) |
| Permanent Conditional M3/M6 | Stage 4 branch B | `PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT` |
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

1. **Matching of invariant \(Aq/K_Q\) (or \(A/K_Q^{3/2}\))** via a named route  
   - Prefer R2 (MAT) once force domain is accepted, or R3 if UV data exist  
   - R1 dimensional analogy remains **Conditional candidate only** (not Derived)  
2. **Causality statement with matched invariants**  
   - Re-evaluate \(q_\times(\theta)\) and domain of \(v_{\mathrm{ph}}\le 1\) after matching  
3. **Physical cutoff / strong-coupling scale** with matched normalization  
   - Upgrade NDA \(\Lambda_\parallel\) from diagnostic to matched scale or declare permanent Conditional limit  

### P1 — strongly recommended before MAT Derived claims

4. Optical theorem / multi-channel unitarity **or** explicit permanent exclusion from UVIR scope  
5. IR transfer HOLD modes: either control them or permanently exclude from “weakly coupled domain”  
6. Full in-in integrals: keep as Open **or** schedule under a later gate (do not smuggle as PASS)

### P2 — parallel (not on critical path for MAT)

7. Identity tracks TOP/VOR/WAK/\(Q_{\mathrm{syn}}\)  
8. DISK/STAT Conditional lane (fits without Derived \(\Cobs\))

---

## 4. What is already enough for *honest* programme progress

| Activity | OK now? |
|----------|---------|
| Manuscript freezes recording path package (α.10) | Yes |
| Conditional AQUAL disk methods (DISK methods package) | Yes |
| Declaring MAT interface (readiness) without Derived vertex | Yes |
| Claiming UVIR-003 closed / MAT open | **No** |
| P3/P4 full drafts | **No** |

---

## 5. Serial order (each stage complete before next)

Authoritative process doc: **`UVIR-003_SERIAL_STAGE_ORDER.md`**.

| Stage | Content | Status |
|-------|---------|--------|
| 0 | Path package, inventory, M3 doc, route maps | **DONE** |
| **1** | M2 domain freeze (exclude IR HOLD) | **DONE** (`PASS_DECLARED_WEAK_COUPLING_DOMAIN`) |
| **2** | Matching floor without MAT (R3 → Conditional floor + 2c) | **DONE** Conditional-with-scope |
| **3** | Scoped MAT calculation (\(V\), \(\Cobs\)) | **DONE** provisional structure — **no MAT PASS**; \(V\) still NOT_COMPUTED |
| **4** | Upgrade M3/M6 with matched \(V\) *or* permanent Conditional | **DONE (branch B)** — `PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT` |
| **5** | UVIR-003 full-gate PASS | **NEXT** — programme decision under declared policy |
| 6 | DISK full + STAT | after Stage 5 for claim-grade obs |
| 7 | P3/P4 full drafts | after Stage 5–6 triggers |

**Next single action:** Stage **5** — decide whether permanent Conditional M3/M6 + M1–M5 are sufficient for `full_gate_status=PASS` (or keep IN_PROGRESS / reopen Stage 4 branch A if \(V\) is computed).  
**Never** promote R1 naive to Derived. **Never** MAT PASS before UVIR Stage 5.

Parallel methods only: DISK Conditional lane; TOP/VOR/WAK sketches.

---

## 6. Document control

| Version | Date | Note |
|---------|------|------|
| 1.0 | 2026-08-03 | Initial closure map + machine audit |
| 1.1 | 2026-08-03 | Ran audit + Conditional causality domain; M3 documented; next = matching |
| 1.2 | 2026-08-03 | Matching-route program PASS; R2 \(V\) target explicit; next = A/B/C decision |
| 1.3 | 2026-08-03 | Serial order adopted; Stage 1 M2 domain freeze PASS_BOUNDED |
| 1.4 | 2026-08-04 | Stage 2a R3 audit exits Classification C; Stage 2b Conditional floor next |
| 1.5 | 2026-08-04 | Stage 2b Conditional matching floor PASS; Stage 2 exit CONDITIONAL_WITH_SCOPE; next Stage 3 scoped MAT calc |
| 1.6 | 2026-08-04 | Stages 2c + 3: floor diagnostics PASS; MAT scoped calc provisional (no PASS); next Stage 4 |
| 1.7 | 2026-08-04 | Stage 4 branch B: permanent Conditional M3/M6 limit PASS; next Stage 5 full-gate decision |
