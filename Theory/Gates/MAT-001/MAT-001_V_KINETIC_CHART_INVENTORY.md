# MAT-001 — (V) kinetic-chart blocker inventory

**Date:** 2026-08-04<br>
**Branch:** `recovery/v12-core-architecture`<br>
**Subgate:** `PASS_MAT001_V_KINETIC_CHART_INVENTORY_OPEN`<br>
**Inventory status:** `COMPLETE_BLOCKER_MAP_V_OPEN`<br>
**MAT-001 PASS:** **forbidden / false**<br>
**(V) status:** **NOT_COMPUTED**<br>
**physics_pass:** **false**

## Result

This is a fail-closed evidence inventory, not the matched calculation. It
verifies that the existing MAT/UVIR packages consistently define

\[
V=\frac{C_m}{\sqrt{K_Q}}
\]

as a field-redefinition invariant while leaving its numerical value open.
A machine PASS means only that the blocker map matches the exact upstream
Open/Partial evidence.

## Exact upstream contracts

| Source | Required status | Use |
|--------|-----------------|-----|
| MAT scoped calculation | `PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL`; (V) NOT_COMPUTED; MAT/physics false | Static interface and present hold |
| (K_Q) inventory | `PASS_KQ_MATCHING_INVENTORY_OPEN`; numeric (K_Q) NOT_DERIVED | Confirms (C_m/\sqrt{K_Q}) is invariant |
| Matching-route programme | `PASS_MATCHING_ROUTE_PROGRAM_OPEN`; R2 Open/MAT-blocked | Confirms static \(C_{\rm obs}\) alone cannot determine (V) |
| Nonzero-gradient force package | `PASS_NONZERO_GRADIENT_FORCE_LOCAL`; UVIR IN_PROGRESS; MAT blocked | Declared force-sector slice only |

## What is actually required to compute (V)

1. Choose one declared dynamical action and one (psi) field-normalization chart.
2. Derive (C_m) and the time-kinetic coefficient (K_Q) in that same chart; **or** compute the invariant on-shell vertex residual (V) directly.
3. Preserve the field-rescaling/gauge convention connecting those quantities.
4. Reopen UVIR Stage 4A only after that matched result exists.

(C_{\rm IR}) is needed later for \(C_{\rm obs}\)/\(I_{a_0}\) maps, but it is
not required merely to define (V); it is therefore recorded separately from
the direct (V) blockers.

## Reproduce

```powershell
python Analysis\MAT\MAT-001\mat001_v_kinetic_chart_inventory.py
# expect: PASS_MAT001_V_KINETIC_CHART_INVENTORY_OPEN
# V_status: NOT_COMPUTED
# physics_pass: False
```

## Explicit non-claims

- No computed (V) or numeric (K_Q)
- No MAT-001 or UVIR-003 PASS
- No Stage 4A unlock
- No downstream Derived use
- No SPARC, (H_0), dual-RAR, or manuscript-freeze claim
