# ITSM reasoning-mode execution plans

**Date:** 2026-09-09  
**Status:** execution index; no gate effect  
**Parent plan:** `../ITSM_RESEARCH_ROUTE_AND_SELECTIVE_PUBLICATION_PLAN_2026-09-05.md`  

These plans separate work by the minimum reasoning level appropriate to the
scientific risk. Their purpose is to avoid spending Ultra reasoning on routine
work and, equally importantly, to stop a lower-reasoning run before it makes a
gate-critical inference.

## Plans

| Order | Mode | Plan | Purpose | May start when |
|---:|---|---|---|---|
| 1 | High | [`02_HIGH_SPECIFICATION_AND_AUDITS/PLAN.md`](02_HIGH_SPECIFICATION_AND_AUDITS/PLAN.md) | Freeze actions, definitions, literature deltas and referee questions | Now |
| 2 | Medium | [`01_MEDIUM_REPRODUCIBILITY_AND_PACKAGING/PLAN.md`](01_MEDIUM_REPRODUCIBILITY_AND_PACKAGING/PLAN.md) | Deterministic reruns, hashes and mechanical evidence maps | Now; run around the High work as convenient |
| 3 | Max | [`03_MAX_BOUNDED_EXACT_REDUCTIONS/PLAN.md`](03_MAX_BOUNDED_EXACT_REDUCTIONS/PLAN.md) | Exact parent-to-EFT, static-source, winding and independent P2 calculations | Relevant High specification frozen |
| 4 | Ultra | [`04_ULTRA_COUPLED_CONSTRAINT_AND_RESIDUE/PLAN.md`](04_ULTRA_COUPLED_CONSTRAINT_AND_RESIDUE/PLAN.md) | Full amplitude-phase-metric constraints, U5 and M4 physical residue | Max parent reduction survives |
| 5 | Ultra | [`05_ULTRA_RESERVOIR_DERIVATION/PLAN.md`](05_ULTRA_RESERVOIR_DERIVATION/PLAN.md) | Microscopic/open-EFT reservoir and covariant transfer current | Physical parent variables and stress tensor fixed |
| 6 | Ultra | [`06_ULTRA_PHYSICAL_T3_SPECTRUM/PLAN.md`](06_ULTRA_PHYSICAL_T3_SPECTRUM/PLAN.md) | Joined winding background and physical compact spectrum | Parent and winding join survive |
| 7 | High | [`07_HIGH_TOPX4_ACTION_FREEZE/PLAN.md`](07_HIGH_TOPX4_ACTION_FREEZE/PLAN.md) | Freeze the TOP-X4 five-dimensional action and on-shell background | **Complete, control-only**; X4-D1 recorded |
| 8 | Max | [`08_MAX_TOPX4_REDUCTION_AND_RADION/PLAN.md`](08_MAX_TOPX4_REDUCTION_AND_RADION/PLAN.md) | Derive the KK reduction, EFT hierarchy and radion stability | **Complete: X4-D2 hold, unstabilized** |
| 9 | Ultra | [`09_ULTRA_TOPX4_COUPLED_CONSTRAINTS/PLAN.md`](09_ULTRA_TOPX4_COUPLED_CONSTRAINTS/PLAN.md) | Full metric-radion-condensate physical constraints | **Closed**; A2/A3 did not survive |
| 10 | High | [`10_HIGH_TOPX4_STABILIZATION_RETRY_SELECTION/PLAN.md`](10_HIGH_TOPX4_STABILIZATION_RETRY_SELECTION/PLAN.md) | Compare and freeze one non-ad-hoc stabilization retry, or close TOP-X4 | **Complete**; `X4-S2F3` frozen |
| 11 | Max | [`11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION/PLAN.md`](11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION/PLAN.md) | Derive the S2F3 determinant and test the finite-charge compactification | **Static checkpoint complete; entry held before finite-charge completion** |

Plans 5, 6 and 9 are independent future Ultra goals. Do not combine them into
one run merely because they use the same reasoning setting. The operator has
redirected new derivation work to TOP-X4; plans 1--6 are preserved but paused
until an X4 decision boundary. Plan 11's static checkpoint is complete, but its
finite-charge entry gate remains held and no A4 or Ultra work is open.

## External workload split

Read-only Antigravity/Grok delegation and the Codex integration protocol are
defined in [`Handoffs/WORKLOAD_DISTRIBUTION.md`](Handoffs/WORKLOAD_DISTRIBUTION.md).
Use the sealed handoffs there one package at a time; external-agent agreement
cannot change a gate.

## Mode-switch rule

1. Run only the selected `PLAN.md`.
2. Stop at its explicit handoff boundary.
3. Package the result at Medium/High before opening another expensive goal.
4. Change mode only when the next plan's entry conditions have been checked.
5. A failed entry condition is a result; do not spend a higher mode trying to
   reason around it without changing the action or plan explicitly.

## Suggested task prompts

Use one task at a time:

```text
/goal Execute Theory/Core/Reasoning_Mode_Plans/02_HIGH_SPECIFICATION_AND_AUDITS/PLAN.md exactly. Stop at its handoff boundary and do not begin Max or Ultra calculations.
```

Then, only after its completion record:

```text
/goal Execute Theory/Core/Reasoning_Mode_Plans/03_MAX_BOUNDED_EXACT_REDUCTIONS/PLAN.md exactly, starting only the work packages whose entry conditions are satisfied. Stop before the coupled amplitude-phase-metric constraint calculation.
```

Use the equivalent path for each other plan. These prompts authorize execution
of the plan only; they do not authorize commit, push, publication, external
updates or gate promotion.

## Shared scientific firewall

- `MAT-001` remains `BLOCKED` and `UVIR-003` remains `IN_PROGRESS` unless a
  later signed gate decision says otherwise.
- `K_Q` alone is chart-dependent. Prefer the physical pole residue and other
  field-redefinition invariants.
- Do not use observed `a_0`, SPARC, `H_0`, `2*pi`, `2/3`, a target healing
  length or another desired output during a derivation.
- A script `PASS_*` is bounded execution evidence, not a physics pass.
- Preserve negative and incomplete results.
