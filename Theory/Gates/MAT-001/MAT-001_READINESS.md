# MAT-001 — Readiness checklist (R2 force–matter matching)

**Status:** gate PASS and downstream Derived use **BLOCKED**; scoped calculation **run** (`PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL`) — **not** MAT PASS  
**Branch:** `recovery/v12-core-architecture`  
**Date:** 2026-08-04  
**Authority:** Master Research Plan §5; UVIR-003 force sector; Selective Publishing Plan (P3/P4 downstream)  
**Scoped package:** `MAT-001_SCOPED_CALCULATION.md`  
**UVIR Stage 5:** `PASS_BOUNDED_CONDITIONAL` — authorizes continued MAT *engineering* under Conditional policy; **still not MAT PASS**

## What MAT-001 is

Compute the **matter–force (phonon) vertex** from one declared interaction so that

\[
\Cobs = \frac{C_m^{3/2}}{\sqrt{C_{\mathrm{IR}}}}
\]

is a **matched** combination (not assumed \(2/3\)). This is the Master Plan pass
condition for MAT-001 and the long-term **R2** route for \(K_Q\)-class
invariants (`UVIR-003_STAGE_B_KQ_MATCHING_INVENTORY`).

## Why it is blocked now

| Dependency | Current status | Why MAT needs it |
|------------|----------------|------------------|
| UVIR-003 force sector | **IN PROGRESS** | Vertex lives in the same IR force + preferred-frame action |
| Stable/causal domain | Partial (Stage A + many Stage B subgates) | Matching without a declared domain is packaging |
| \(K_Q\) absolute value | **NOT_DERIVED** (inventory Open) | Absolute norm entangled with \(C_m\), \(A\); invariants ready |
| Declared unitarity/EFT criterion | PASS (scoped, not theory closed) | Bounds the domain where a vertex is meaningful |
| Full UVIR-003 gate close | **`PASS_BOUNDED_CONDITIONAL`** (not Derived closed) | Unblocks programme permission for MAT engineering; still blocks MAT PASS until MAT checklist; \(V\) still NOT_COMPUTED |

**Do not** open MAT-001 Derived claims or a MAT “pass report” while the table above remains red on UVIR-003 full gate + matching domain.

A Stage-2 handoff may authorize calculation of provisional matched quantities under named Conditional premises. It does **not** authorize a MAT PASS tag or downstream Derived claims before UVIR Stage 5.

## Handoff interface (what UVIR must deliver to MAT)

When starting MAT, import these as *inputs*, not re-derive casually:

1. **Force sector action slice**  
   Track-A exact \(Y^{3/2}\) on nonzero-gradient backgrounds + regulator structure  
   (`PASS_NONZERO_GRADIENT_FORCE_LOCAL`, Track-A ADM notes).

2. **Redefinition invariants** (must match, not bare \(K_Q\))  
   - \(A q / K_Q\) (causality)  
   - \(A / K_Q^{3/2}\) (NDA \(\Lambda_\parallel\))  
   - \(C_m / \sqrt{K_Q}\) (vertex residual \(V\))  
   See `UVIR-003_STAGE_B_KQ_MATCHING_INVENTORY.md` and  
   `UVIR-003_STAGE_B_MATCHING_ROUTE_PROGRAM.md`.

3. **Scoped EFT window**  
   Declared criterion package  
   `PASS_DECLARED_UNITARITY_EFT_CRITERION` — tree/NDA only; optical theorem still open.

4. **Scientific boundary language**  
   No homogeneous FRW S-matrix from exact \(Y^{3/2}\) at zero gradient; no dual RAR packaging.

### R2 structural result (2026-08-03 matching-route program)

**Static \(\Cobs\) alone cannot fix \(Aq/K_Q\).** MAT must deliver the invariant
vertex residual

\[
V := \frac{C_m}{\sqrt{K_Q}}
\]

(from one \(S_{\mathrm{int}}\)). With Conditional or Derived \((\Cobs,C_{\mathrm{IR}},V)\),

\[
I_{a_0}=\frac{A a_0}{K_Q}
=\frac{C_{\mathrm{IR}}^{1/3}\,V^{2}}{12\pi G\,\Cobs^{4/3}}.
\]

Subgate: `PASS_MATCHING_ROUTE_PROGRAM_OPEN`  
Script: `Analysis/UVIR/UVIR-003/uvir003_matching_route_program.py`  
This does **not** unblock MAT; it makes the MAT target quantity explicit.

## MAT-001 open checklist (when unblocked)

- [x] For calculation start: Stage-2 exit plus explicit Conditional MAT-only handoff  
- [ ] For MAT gate PASS/downstream Derived use: UVIR-003 full-gate status upgraded from IN_PROGRESS  
- [x] Declare interaction \(S_{\mathrm{int}}\) **form** (\(-\,C_m\rho_b\psi\); architecture)  
- [x] Static weak-field reduction **form** → \(\Cobs=C_m^{3/2}/\sqrt{C_{\mathrm{IR}}}\)  
- [ ] Report \(\Cobs\) as **Derived from micro \(S_{\mathrm{int}}\)** (still Conditional baseline only)  
- [ ] **Compute \(V=C_m/\sqrt{K_Q}\)** from dynamics (\(K_Q\) still NOT_DERIVED)  
- [x] Map \(I_{a_0}\) formula in \((\Cobs,C_{\mathrm{IR}},V)\) (form only)  
- [ ] Map numeric result onto full invariant list  
- [ ] Update claim ledger + Selective Publishing ban-list on real MAT PASS  
- [x] **Not** claim SPARC / cosmic \(H_0\) validation from this gate alone  

## What MAT unlocks

| Downstream | Use |
|------------|-----|
| SCR-001 / LEN-001 | Screening / lensing once force+matter exist |
| DISK-001 | Disk solver under matched or **declared** \(\Cobs\) |
| P4 | Declared \((a_0,\Cobs)\) with honest provenance |
| P3 | One possible “derived observable” path (weak-field), not automatic |

## Parallel (not a substitute)

- **Conditional AQUAL IR** (\(\Cobs\sim 1\)) may be used for **honest fits** under Master Plan §6 without MAT — still **not** Derived matching, still **not** P4 without DISK+STAT.  
- **R3** condensate-microscopic \(K_Q\) sketch remains Open (identity dig-harder).

## Reproduction / related scripts

```text
Theory/Gates/UVIR-003/UVIR-003_STAGE_B_KQ_MATCHING_INVENTORY.md
Theory/Gates/UVIR-003/UVIR-003_STAGE_B_MATCHING_ROUTE_PROGRAM.md
Analysis/UVIR/UVIR-003/uvir003_kq_matching_inventory.py
Analysis/UVIR/UVIR-003/uvir003_matching_route_program.py
Analysis/UVIR/UVIR-003/uvir003_declared_unitarity_eft_criterion.py
Analysis/UVIR/UVIR-003/uvir003_nonzero_gradient_force_local.py
```
