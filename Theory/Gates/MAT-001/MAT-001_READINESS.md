# MAT-001 — Readiness checklist (R2 force–matter matching)

**Status:** gate PASS and downstream Derived use **BLOCKED**; scoped calculation **run** (`PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL`) — **not** MAT PASS  
**Branch:** `recovery/v12-core-architecture`  
**Date:** 2026-08-04  
**Authority:** Master Research Plan §5; UVIR-003 force sector; Selective Publishing Plan (P3/P4 downstream)  
**Scoped package:** `MAT-001_SCOPED_CALCULATION.md`  
**UVIR Stage 5:** `PASS_STAGE5_DECISION_HOLD_TIER1` — decision audit passed fail-closed; UVIR physics remains **IN_PROGRESS**

## What MAT-001 is

Compute the **matter–force (phonon) vertex** from one declared interaction so that

\[
C_{\mathrm{obs}} = \frac{C_m^{3/2}}{\sqrt{C_{\mathrm{IR}}}}
\]

is a **matched** combination (not assumed $2/3$). This is the Master Plan pass
condition for MAT-001 and the long-term **R2** route for $K_Q$-class
invariants (`UVIR-003_STAGE_B_KQ_MATCHING_INVENTORY`).

## Why it is blocked now

| Dependency | Current status | Why MAT needs it |
|------------|----------------|------------------|
| UVIR-003 force sector | **IN PROGRESS** | Vertex lives in the same IR force + preferred-frame action |
| Stable/causal domain | Partial (Stage A + many Stage B subgates) | Matching without a declared domain is packaging |
| $K_Q$ absolute value | **NOT_DERIVED** (inventory Open) | Absolute norm entangled with $C_m$, $A$; invariants ready |
| Declared unitarity/EFT criterion | PASS (scoped, not theory closed) | Bounds the domain where a vertex is meaningful |
| Full UVIR-003 gate close | **IN_PROGRESS / HOLD_TIER1_CLOSURE** | M2/M3/M6/M7 remain incomplete; $V$ NOT_COMPUTED; MAT PASS blocked |

**Do not** open MAT-001 Derived claims or a MAT “pass report” while the table above remains red on UVIR-003 full gate + matching domain.

A Stage-2 handoff authorizes only provisional engineering under named Conditional premises. It does **not** authorize a MAT PASS tag or downstream Derived claims before genuine UVIR closure plus the MAT checklist.

## Handoff interface (what UVIR must deliver to MAT)

When starting MAT, import these as *inputs*, not re-derive casually:

1. **Force sector action slice**  
   Track-A exact $Y^{3/2}$ on nonzero-gradient backgrounds + regulator structure  
   (`PASS_NONZERO_GRADIENT_FORCE_LOCAL`, Track-A ADM notes).

2. **Redefinition invariants** (must match, not bare $K_Q$)  
   - $A q / K_Q$ (causality)  
   - $A / K_Q^{3/2}$ (NDA $\Lambda_\parallel$)  
   - $C_m / \sqrt{K_Q}$ (vertex residual $V$)  
   See `UVIR-003_STAGE_B_KQ_MATCHING_INVENTORY.md` and  
   `UVIR-003_STAGE_B_MATCHING_ROUTE_PROGRAM.md`.

3. **Scoped EFT window**  
   Declared criterion package  
   `PASS_DECLARED_UNITARITY_EFT_CRITERION` — tree/NDA only; optical theorem still open.

4. **Scientific boundary language**  
   No homogeneous FRW S-matrix from exact $Y^{3/2}$ at zero gradient; no dual RAR packaging.

### R2 structural result (2026-08-03 matching-route program)

**Static $C_{\mathrm{obs}}$ alone cannot fix $Aq/K_Q$.** MAT must deliver the invariant
vertex residual

\[
V := \frac{C_m}{\sqrt{K_Q}}
\]

(from one $S_{\mathrm{int}}$). With Conditional or Derived $(C_{\mathrm{obs}},C_{\mathrm{IR}},V)$,

\[
I_{a_0}=\frac{A a_0}{K_Q}
=\frac{C_{\mathrm{IR}}^{1/3}\,V^{2}}{12\pi G\,C_{\mathrm{obs}}^{4/3}}.
\]

Subgate: `PASS_MATCHING_ROUTE_PROGRAM_OPEN`  
Script: `Analysis/UVIR/UVIR-003/uvir003_matching_route_program.py`  
This does **not** unblock MAT; it makes the MAT target quantity explicit.
### Post-alpha.11 normalization preparation (2026-08-05)

| Package | Established | Still open |
|---|---|---|
| J1 joint-action identity | $V=g_\phi/\sqrt{Z_\phi}$ when both coefficients come from one parent action | Microscopic $g_\phi,Z_\phi$ |
| R2 canonical response | Vertex $V$, mixed response $V/P$, exchange coefficient $V^2/P$ are distinct | Live constraint reduction and physical-mode projection |
| Unit-chart contract | $K_Q^{(t)}=K_Q^{(x^0)}/c^2$; current natural/covariant ratios are dimensionally closed | Selected SI observable/action chart |
| UVIR handoff contract | Eight UVIR/MAT records form a consistent fail-closed interface for a scoped projection audit | Action-level source vector, kinetic metric and numerical matching |
| J2 mode projection | $g_{\rm can}=c_{\rm eff}^Tu/\sqrt{u^TKu}$ after constraint elimination is basis invariant | Live same-action $K,C,B,d,h,u$ export and numerical matching |
| Live UVIR export inventory | Partial live $K,C$ and constraint-source evidence is identified without substitution | Same-chart bundle remains absent: $d,h$ are not exported, $B$ is not isolated, and $u$ is not selected |
| Same-chart free-sector export | Original-chart free $K,C$ plus exact $M_x,M_v$ source decomposition; physical free $K$ transformed | Pure static J2 $B$ blocked by nonzero $M_v$; matter $d,h$ and mode $u$ still absent |
| $S_{\rm int}$ + $d,h$ placement | Conditional form $-C_m\rho_b\psi$ declared; IR $d=(-C_m)$, $h=\emptyset$ recover $\lvert V\rvert$ | Live free-sector chart lacks force field $\psi$; live UVIR $d,h$ remain `NOT_EXPORTED` |
| Force hosting readiness | Five host routes inventoried; Track-A has force without matter; full ADM force completion blocked | Inventory stage: no host selected until the Track-A embed checkpoint |
| Track-A $S_{\rm int}$ embed | Track-A selected Conditional; $d=(-C_m)$, $h=(0,0)$ exported on host; $\lvert V\rvert$ form recovered with symbolic $K_Q$ | Numeric $K_Q$/`V` not derived; free-sector join not declared; MAT still blocked |
| Track-A $K_Q$ readiness | Host time-kinetic $K_Q$ exported symbolically; on-host $V$ form + rescaling identity hold | Numeric $K_Q$ still `NOT_DERIVED`; Conditional dimensional estimate rejected as Derived |
| $K_Q$ derivation dig | Four paths audited; none ready for numeric $K_Q$ | Microscopic matching still incomplete |
| Conditional matching branch | Dual-status branch open; Conditional samples labeled only | Derived $V$/`K_Q` closed; Stage 4A closed |
| Track-A join readiness | Matter-only static channel form-ready; free-force J2 residual; full multi-sector not assembled | Numeric matching still blocked on $K_Q$ |

Subgates include
`PASS_MAT001_CONDITIONAL_MATCHING_BRANCH_OPEN_DUAL_STATUS` and
`PASS_MAT001_TRACK_A_JOIN_READINESS_PARTIAL_MATTER_CHANNEL_ONLY`. All preserve
Derived $V$ as `NOT_COMPUTED`, `mat001_pass: false`, Stage 4A closed.

## MAT-001 open checklist (when unblocked)

- [x] For calculation start: Stage-2 exit plus explicit Conditional MAT-only handoff  
- [ ] For MAT gate PASS/downstream Derived use: UVIR-003 tier-1 gate genuinely closed after matched Stage 4A + independent Stage 5 review  
- [x] Declare interaction $S_{\mathrm{int}}$ **form** ($-\,C_m\rho_b\psi$; architecture)  
- [x] Static weak-field reduction **form** → $C_{\mathrm{obs}}=C_m^{3/2}/\sqrt{C_{\mathrm{IR}}}$  
- [ ] Report $C_{\mathrm{obs}}$ as **Derived from micro $S_{\mathrm{int}}$** (still Conditional baseline only)  
- [ ] **Compute $V=C_m/\sqrt{K_Q}$** from dynamics ($K_Q$ still NOT_DERIVED)  
- [x] Map $I_{a_0}$ formula in $(C_{\mathrm{obs}},C_{\mathrm{IR}},V)$ (form only)  
- [ ] Map numeric result onto full invariant list  
- [ ] Update claim ledger + Selective Publishing ban-list on real MAT PASS  
- [x] **Not** claim SPARC / cosmic $H_0$ validation from this gate alone  

## What MAT unlocks

| Downstream | Use |
|------------|-----|
| SCR-001 / LEN-001 | Screening / lensing once force+matter exist |
| DISK-001 | Disk solver under matched or **declared** $C_{\mathrm{obs}}$ |
| P4 | Declared $(a_0,C_{\mathrm{obs}})$ with honest provenance |
| P3 | One possible “derived observable” path (weak-field), not automatic |

## Parallel (not a substitute)

- **Conditional AQUAL IR** ($C_{\mathrm{obs}}\sim 1$) may be used for **honest fits** under Master Plan §6 without MAT — still **not** Derived matching, still **not** P4 without DISK+STAT.  
- **R3** condensate-microscopic $K_Q$ sketch remains Open (identity dig-harder).

## Reproduction / related scripts

```text
Theory/Gates/UVIR-003/UVIR-003_STAGE_B_KQ_MATCHING_INVENTORY.md
Theory/Gates/UVIR-003/UVIR-003_STAGE_B_MATCHING_ROUTE_PROGRAM.md
Analysis/UVIR/UVIR-003/uvir003_kq_matching_inventory.py
Analysis/UVIR/UVIR-003/uvir003_matching_route_program.py
Analysis/UVIR/UVIR-003/uvir003_declared_unitarity_eft_criterion.py
Analysis/UVIR/UVIR-003/uvir003_nonzero_gradient_force_local.py
Analysis/MAT/MAT-001/J1_JOINT_ACTION/mat001_j1_joint_action_normalization.py
Analysis/MAT/MAT-001/R2_DIRECT_RESIDUE/mat001_r2_direct_residue_audit.py
Analysis/MAT/MAT-001/UNIT_CHART/mat001_unit_chart_contract.py
Analysis/MAT/MAT-001/HANDOFF/mat001_uvir_handoff_contract_audit.py
Analysis/MAT/MAT-001/J2_MODE_PROJECTION/mat001_j2_basis_covariant_mode_projection.py
Analysis/MAT/MAT-001/LIVE_EXPORT_INVENTORY/mat001_live_uvir_export_inventory.py
```
