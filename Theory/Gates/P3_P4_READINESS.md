# P3 / P4 readiness map

**Date:** 2026-09-09

**Branch:** `recovery/v12-core-architecture`

**Status:** `FAIL_CLOSED_RECONCILED`

**Authority:** `active_research.md`, signed parent-gate decisions, Master
Research Plan §8–9, then Selective Publishing Plan §3–4

This is a **navigation document**, not a paper draft or gate PASS. A compiled PDF
establishes buildability only. It does not establish scientific readiness,
publication clearance or a parent-gate result.

## Current signal lights

| Item | Current light | Boundary |
|---|---|---|
| **P1 claim firewall** | Amber — local draft compiled | Claim-hygiene candidate; author freeze and external submission are not verified here |
| **P2 Casimir** | Amber — repaired local draft compiled | Bounded free-field result; publication remains on independent-review and sensitivity hold |
| **UVIR-003** | Red — `IN_PROGRESS` | Complete constrained amplitude, matched invariant and physical EFT cutoff remain open |
| **MAT-001** | Red — `BLOCKED` | `K_Q NOT_DERIVED`; `V=C_m/sqrt(K_Q) NOT_COMPUTED` |
| **DISK-001** | Amber — `METHODS_ONLY` | Conditional numerical tooling is not a morphology-independent ITSM prediction |
| **STAT-001** | Red — `NOT_STARTED_AS_CLOSED_GATE` | Earlier optimizer/MCMC claims are quarantined; repaired comparator is optimization-only |
| **VOR-001** | Amber — `OPEN_SCAFFOLD` | Chosen cavity/mode examples do not establish an ITSM PTA prediction |
| **SCR-001** | Red — `OPEN` | Landau disruption remains an unverified heuristic downstream of the matter coupling |
| **LEN-001** | Red — `OPEN` | Lensing potentials and wave propagation remain unclosed downstream of `V` |
| **Full P3 draft** | Red — quarantined scaffold | The claim-bearing `main.tex` and PDF are provenance artifacts, not citable results |
| **Full P4 draft** | Red — quarantined scaffold | The claim-bearing `main.tex` and PDF are provenance artifacts, not citable results |

TOP-X4 / KK-001 does not change this table. Its Plan 11 static parity-even
determinant checkpoint is bounded, the finite-charge entry is held,
`physics_pass=false`, and `gate_effect=NONE`.

## Dependency sketch

```text
UVIR-003 ──► MAT-001 ──► SCR/LEN ──► DISK-001 ──► STAT-001 ──► P4 review
                         │
VOR / ASTRO / mapped observable ─────────────────────────────► P3 review

TOP-X4 Plan 11: separate bounded fork; no publication inheritance
```

Conditional solvers and example spectra may be developed before these gates
close, but they must retain their assumptions and cannot be packaged as
Derived ITSM predictions.

## Documents

| Path | Role |
|---|---|
| `active_research.md` | Current gate and operator-priority dashboard |
| `Theory/Gates/MAT-001/MAT-001_READINESS.md` | MAT handoff and unblock criteria |
| `Theory/Gates/DISK-001/DISK-001_READINESS.md` | Solver and P4 physics boundary |
| `Theory/Gates/STAT-001/STAT-001_READINESS.md` | Inference-pipeline boundary |
| `papers/P3-Observational-Program/OUTLINE.md` | Current P3 planning authority |
| `papers/Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md` | Binding publication firewall |

## Current commit and publication policy

- P1/P2 may be built and reviewed within their stated scopes; neither is
  promoted here.
- P3 stays outline-led. Its current full source/PDF is retained only as a
  visibly quarantined legacy scaffold.
- P4 stays gated behind MAT, DISK and STAT. Its current full source/PDF is
  retained only as a visibly quarantined legacy scaffold.
- Do not submit, archive or cite P3/P4 as results until a new signed readiness
  decision replaces this hold.
- Prefer parent-gate decisions over child scripts, dashboards, paper scaffolds
  or matching checksum sidecars.

## Recommended order of work

1. Complete the currently authorized TOP-X4 Plan 11 finite-charge quantum
   requirements or record a closed-negative outcome at its decision boundary.
2. Preserve MAT-001 as blocked and UVIR-003 as in progress unless their own
   parent checklists close.
3. Continue VOR, SCR, LEN, DISK and STAT only within their current Open,
   Conditional or methods-only boundaries.
4. Reassess P3 only after a derived observable maps cleanly to a test.
5. Reassess P4 only after MAT, DISK and STAT prerequisites are independently
   satisfied and the RAR-normalization firewall is obeyed.

## Quarantined prior status map

The 2026-08-30 revision displayed green lights for MAT, UVIR, VOR, SCR, LEN,
DISK, STAT and the full P3/P4 drafts. The 1 September parent-gate audit rejected
those promotions. Git history preserves the exact prior wording; it is not
current authority.
