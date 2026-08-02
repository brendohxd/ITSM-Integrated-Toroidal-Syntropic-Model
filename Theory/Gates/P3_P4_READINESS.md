# P3 / P4 readiness map

**Date:** 2026-08-03  
**Branch:** `recovery/v12-core-architecture`  
**Authority:** Master Research Plan §8–9; Selective Publishing Plan §3–4

This is a **navigation document**, not a paper draft and not a gate PASS.

## Current signal lights

| Item | Light | Note |
|------|-------|------|
| P1 claim firewall | Green (draft) | Cite for hygiene only |
| P2 Casimir | Green (draft) | arXiv endorsement pending |
| UVIR-003 | Yellow | IN PROGRESS; many Stage-B subgates; full gate open |
| \(K_Q\) matching | Yellow | Inventory PASS; numeric NOT_DERIVED |
| MAT-001 | Red | BLOCKED until UVIR-003 passes (Derived) |
| DISK-001 | Red | Readiness only |
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

1. Keep UVIR-003 critical path until MAT can open (or freeze alpha.10).  
2. Optional parallel: VOR-001 dimensionful spectrum sketch → **P3 trigger**.  
3. DISK-001 under Conditional IR for tooling (no Derived packaging).  
4. STAT-001 after DISK predictions exist.  
5. Full P3/P4 only on green triggers.  
