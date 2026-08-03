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
| **M2** | Stability / positivity in declared domain | **PARTIAL** | Finite-\(q\) kinetic positivity, many Stage B ADM/propagator passes; IR transfer HOLD retained for some modes |
| **M3** | Causality in declared domain | **PARTIAL (DOCUMENTED)** | Stage A + addendum; Conditional R1 domain mapped (`PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING`); naive \(q_\times/a_0=0.375\) parallel — **Derived** close still needs matched \(Aq/K_Q\) |
| **M4** | Weak coupling / unitarity **path stated with scope** | **PASS (scoped)** | `PASS_DECLARED_UNITARITY_EFT_CRITERION` — tree/NDA + Green health; **not** optical theorem |
| **M5** | Invariant ratios for force normalization | **PASS (inventory)** | `PASS_KQ_MATCHING_INVENTORY_OPEN` — \(Aq/K_Q\), \(A/K_Q^{3/2}\), …; **numeric \(K_Q\) NOT_DERIVED** |
| **M6** | Physical cutoff | **OPEN** | Blocked on matching (\(K_Q\), possibly \(C_{\mathrm{IR}}\)); NDA scale only |
| **M7** | Matter sector ready for MAT handoff | **OPEN** | Force sector methods exist; MAT still blocked for Derived vertex |

**Interpretation for MAT-001**

- Master Plan: MAT blocked until UVIR-003 **passes**.  
- Honest reading today: **M4–M5** support a *matching programme*; **M3/M6** still block a claim of “stable+causal+cutoff closed.”  
- Do **not** open MAT Derived claims until the programme either (i) closes M3/M6 under a named matching route, or (ii) **explicitly** accepts a Conditional UVIR domain for MAT (written amendment to this checklist—programme decision).

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
| Full-gate checklist audit | Evidence ledger | `PASS_UVIR003_CLOSURE_CHECKLIST_AUDIT` |

Machine audit:  
`python Analysis/UVIR/UVIR-003/uvir003_full_gate_closure_audit.py`

Conditional M3 domain:  
`python Analysis/UVIR/UVIR-003/uvir003_causality_domain_under_conditional_matching.py`

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

## 5. Next single critical-path action

**Done (v1.1):** Conditional causality domain under R1 premises — M3 **documented**.

**Now — toward Derived M3/M6 (full UVIR PASS):**

1. **Match** invariant \(Aq/K_Q\) (or \(A/K_Q^{3/2}\)) via a **named route**  
   - Prefer **R2** (MAT interface) once Conditional force domain is accepted for that step  
   - **R3** if UV/strong-coupling data fix the scale  
   - Do **not** promote naive R1 \((k_Q,C_{\mathrm{IR}})=(1,2/3)\) to Derived  
2. **Re-evaluate** \(q_\times(\theta)\) and \(R_c\le 1\) after matching  
3. **Physical cutoff** with matched normalization (M6)  
4. Only then: programme decision on MAT-001 unblock under Master Plan wording  

Parallel (not MAT-critical): DISK/STAT Conditional lane; TOP/VOR/WAK sketches.

---

## 6. Document control

| Version | Date | Note |
|---------|------|------|
| 1.0 | 2026-08-03 | Initial closure map + machine audit |
| 1.1 | 2026-08-03 | Ran audit + Conditional causality domain; M3 documented; next = matching |
