# TOP-X4 / KK-001 — higher-dimensional four-torus research fork

**Status:** original `X4-D2 HOLD_UNSTABILIZED`; `X4-S2F3` finite-charge operator checkpoint complete, evolving-state determinant held; A4 and Ultra entry closed
**Date:** 2026-09-12
**Gate effect:** none
**Rule-9 status:** static-checkpoint Role A completed, but no three-way clearance; the finite-charge operator checkpoint has no completed independent reviewer set

## Scope

Test the higher-dimensional manifold

\[
 \mathbb R_t\times\mathbb T^3_{\rm obs}\times S^1_y
\]

as a possible parent extension of ITSM. The fourth cycle is spatial/internal,
not periodic Lorentzian time. The canonical ITSM `T^3` identity remains in
force unless a later architecture decision adopts a successfully reduced
parent.

## Immediate question

What separately frozen stabilization sector, if any, can generate an on-shell
positive-mass radion minimum without selecting the radius or coefficients from
an observational target?

## Required boundaries

- Do not call this `Route T4`; that name already belongs to TOP-001's twisted
  `E2/E3` route.
- Do not use the extra circle to manufacture `2*pi`, `a0`, `K_Q`, `V`, `H0` or
  a reservoir current.
- Do not treat periodic identification as an open physical boundary.
- Do not mix bulk matter, brane matter and inserted four-dimensional portals.
- A kinematic script pass is not a physics or architecture pass.

## Files

| File | Purpose |
|---|---|
| `Theory/Core/ITSM_TOPX4_KK001_ROUTE_PLAN_2026-09-06.md` | Authoritative staged route and decision criteria |
| `Analysis/TOP/TOP-X4/topx4_a0_kinematic_control.py` | Exact A0 spectrum/dimension checks |
| `Analysis/TOP/TOP-X4/outputs/topx4_a0_kinematic_summary.json` | Deterministic A0 result |
| `Theory/Gates/TOP-X4/TOPX4_A0_KINEMATIC_RESULT_2026-09-06.md` | Role-C scope and decision record |
| `Theory/Gates/TOP-X4/TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md` | Frozen X4-I1C action, ensemble and background equations |
| `Analysis/TOP/TOP-X4/topx4_a1_symbolic_audit.py` | Independent metric/action variation audit |
| `Analysis/TOP/TOP-X4/topx4_a1_background_control.py` | Finite-charge on-shell background integration |
| `Theory/Gates/TOP-X4/TOPX4_A1_CONTROL_BACKGROUND_RESULT_2026-09-06.md` | A1 evidence, scope and decision record |
| `Analysis/TOP/TOP-X4/topx4_a2_radion_symbolic_audit.py` | Independent Einstein-frame radion and mode normalization |
| `Analysis/TOP/TOP-X4/topx4_a2a3_reduction_radion_control.py` | Fixed-action KK, scalar and stabilization/no-go audit |
| `Theory/Gates/TOP-X4/TOPX4_A2A3_REDUCTION_RADION_RESULT_2026-09-06.md` | Max result, limitations and hold decision |
| `Analysis/TOP/TOP-X4/topx4_s0_stabilization_prescreen.py` | High-only candidate algebra/sign prescreen |
| `Analysis/TOP/TOP-X4/outputs/topx4_s0_stabilization_prescreen_summary.json` | Deterministic 8/8 selection result; not a physics pass |
| `Theory/Gates/TOP-X4/TOPX4_S0_STABILIZATION_CANDIDATE_AUDIT_2026-09-06.md` | Literature, simultaneous-stationarity and candidate adjudication |
| `Theory/Gates/TOP-X4/TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md` | Exact retry action, quantum definition, domains and Max kill criteria |
| `Analysis/TOP/TOP-X4/topx4_s2f3_static_determinant_checkpoint.py` | Plan 11 zero-density parity-even determinant checkpoint |
| `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_static_determinant_summary.json` | 12/12 bounded static result; `physics_pass=false` |
| `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_STATIC_CHECKPOINT_RECEIPT_2026-09-09.md` | Static checkpoint decision, witness and open quantum boundaries |
| `Analysis/TOP/TOP-X4/topx4_s2f3_finite_charge_entry_gate.py` | Fail-closed finite-charge transition gate |
| `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_finite_charge_entry_gate_summary.json` | 9/9 entry checks; finite-charge completion held |
| `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_FINITE_CHARGE_ENTRY_GATE_RECEIPT_2026-09-09.md` | Entry-gate receipt and no-static-loop substitution boundary |
| `Theory/Gates/TOP-X4/TOPX4_S2F3_FINITE_CHARGE_VARIATION_CONTRACT_2026-09-09.md` | Covariant variation, fixed-charge ensemble and charged-scalar operator contract |
| `Analysis/TOP/TOP-X4/topx4_s2f3_finite_charge_operator_checkpoint.py` | Exact finite-charge operator and fixed-charge variation checkpoint |
| `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_finite_charge_operator_summary.json` | Deterministic 16/16 bounded result; dynamic state/stress/Hessian held |
| `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_FINITE_CHARGE_OPERATOR_CHECKPOINT_2026-09-12.md` | Operator-checkpoint decision, hashes and open quantum boundary |

## Entry to Max

The Max A2/A3 task is complete for the exact `X4-I1C` control. Its bounded
fixed-background scalar spectrum survives, but its radion is not stabilized
and no EFT hierarchy is established. The High freeze is complete under
`X4-S2F3`; Plan 11 completed the 12/12 static parity-even determinant and the
9/9 finite-charge entry gate, then completed a 16/16 constant-background
charged-scalar operator and fixed-charge variation checkpoint. This does not
open the evolving-state determinant. The next required work is the coupled
time-dependent mode system, Hadamard/adiabatic state and subtraction scheme,
state-order convergence and renormalized stress, followed by the physical
constraint/Hessian and parity/anomaly audits. Do not begin A4 or Ultra work.
No gate effect follows from the checkpoint.
