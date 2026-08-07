# P3 / P4 readiness map

**Date:** 2026-08-04  
**Branch:** `recovery/v12-core-architecture`  
**Authority:** Master Research Plan §8–9; Selective Publishing Plan §3–4

This is a **navigation document**, not a paper draft and not a gate PASS.

## Current signal lights

| Item | Light | Note |
|------|-------|------|
| P1 claim firewall | Green (draft) | Cite for hygiene only |
| P2 Casimir | Green (draft) | arXiv endorsement pending |
| UVIR-003 | Yellow | `PASS_STAGE5_DECISION_HOLD_TIER1`; physics gate IN_PROGRESS; M2/M3/M6/M7 open |
| \(K_Q\) matching | Yellow | Inventory PASS; numeric NOT_DERIVED |
| MAT-001 | Red | BLOCKED; scoped provisional forms are not a gate pass |
| DISK-001 | Yellow | Methods package PARTIAL PASS (Stages 0–4); full gate open |
| STAT-001 | Red | Readiness only |
| VOR-001 spectrum (units) | Red | Identity track; P3 alternate trigger |
| **Full P3 draft** | Red | Trigger not met |
| **Full P4 draft** | Red | DISK+STAT not met |
| **P3 outline-only** | Green | Allowed now — see `papers/P3-Observational-Program/` |

## Dependency sketch

```text
                    ┌── VOR-001 spectrum (units) ──┐
                    │   or ASTRO-001 / mapped limit │
                    └────────────┬─────────────────┘
                                 │
                                 ▼
                              FULL P3
                                 ▲
                                 │ (also helped by derived weak-field)
UVIR-003 ──► MAT-001 ──► SCR/LEN ──► DISK-001 ──► STAT-001 ──► FULL P4
   │              │                      │
   │              │                      └── Conditional AQUAL inputs
   │              │                          allowed for solver *dev*
   └── K_Q inventory (Open)                  but not Derived packaging
```

## Documents

| Path | Role |
|------|------|
| `Theory/Gates/MAT-001/MAT-001_READINESS.md` | R2 handoff + unblock criteria |
| `Theory/Gates/DISK-001/DISK-001_READINESS.md` | Solver + P4 physics gate |
| `Theory/Gates/STAT-001/STAT-001_READINESS.md` | Inference pipeline gate |
| `papers/P3-Observational-Program/` | Outline-only skeleton (no fixed predictions) |
| `papers/Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md` | Binding firewall |

## Commit policy for this workstream

- **Commit/push readiness + P3 outline** when content is self-contained (this package).  
- **Do not** open `papers/P4-...` or full P3 `main.tex` until the Selective Publishing **triggers** fire.  
- Prefer gate PASS reports over paper scaffolding when the science is still Open.

## Recommended order of work (capacity-aware)

1. Compute the matched \(V\) (or equivalent invariant) and reopen UVIR Stage 4A.  
2. Re-run the independent Stage 5 closure decision; keep MAT blocked until it genuinely passes.  
3. Continue VOR/TOP/WAK identity work and DISK tooling in parallel under Open/Conditional labels.  
4. Start STAT-001 only when DISK predictions with declared provenance exist.  
5. Keep P3 outline-only; open full P3/P4 drafts only when their green triggers fire.  

## Critical Open Risks (v12.0-alpha.14+)

> [!WARNING]
> **1. VOR-001 Topological Mapping Burden:** By accepting the Covariant Compensator in MAT-001, we mathematically proved that the coupling strength and kinetic normalization are dictated by a single scale $f$. Because ITSM is a fundamental topological theory (not a phenomenological MOND fit), we cannot tune $f$ by hand. VOR-001 is now strictly on the hook to organically derive the physical value of $f$ from the winding sector topology and toroidal moduli.

> [!WARNING]
> **2. CBR-002 Causality Tension:** In UVIR-003, we successfully regulated the $q=0$ divergence by expanding the fractional $|\nabla \pi|^3$ operator against the non-zero local adiabatic background gradient. However, this creates a major mathematical tension for highly dynamical, strong-field regimes where $\nabla \pi_0 \to 0$. CBR-002 (Hyperbolic Completion) must rigorously prove that these non-linear kinetic terms do not introduce superluminal phase velocities or acausal propagation in rapidly changing source environments.
