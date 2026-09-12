# TOP-X4 / KK-001 — higher-dimensional four-torus research fork

**Status:** original `X4-D2 HOLD_UNSTABILIZED`; `X4-S2F3` local scalar-matrix Hadamard parametrix passed 22/22, but global states/gravity/parity/stress remain held; A4 and Ultra entry closed
**Date:** 2026-09-12
**Gate effect:** none
**Rule-9 status:** no three-way clearance; the Plan 11 scalar-matrix checkpoints have no completed independent reviewer set

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
| `Theory/Gates/TOP-X4/TOPX4_S2F3_DYNAMIC_STATE_SUBTRACTION_CONTRACT_2026-09-12.md` | Preregistered evolving scalar-state scope, thresholds and stop rule |
| `Analysis/TOP/TOP-X4/topx4_s2f3_dynamic_state_subtraction_checkpoint.py` | Exact evolving scalar mode system and order-0/2/4 UV diagnostic |
| `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_dynamic_state_subtraction_summary.json` | Deterministic 11/12 failed result; `physics_pass=false` |
| `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT_2026-09-12.md` | Failure receipt, low-mode evidence and next admissible design boundary |
| `Theory/Gates/TOP-X4/TOPX4_S2F3_EXACT_TRANSPORT_RETRY_CONTRACT_2026-09-12.md` | Frozen scalar symplectic and Dirac finite-order transport retry |
| `Analysis/TOP/TOP-X4/topx4_s2f3_exact_transport_retry_checkpoint.py` | Exact charged/real-scalar and first-order Dirac transport executable |
| `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_exact_transport_retry_summary.json` | Deterministic 18/18 bounded pass; full Hadamard state remains false |
| `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_EXACT_TRANSPORT_RETRY_CHECKPOINT_2026-09-12.md` | Retry decision, hashes, measured residuals and hold boundary |
| `Theory/Gates/TOP-X4/TOPX4_S2F3_HADAMARD_SUBTRACTION_READINESS_CONTRACT_2026-09-12.md` | Frozen D5 local scaffold, inventory and fail-closed decision rule |
| `Analysis/TOP/TOP-X4/topx4_s2f3_hadamard_subtraction_readiness.py` | D5 Hadamard/heat-kernel scaffold and completion-inventory executable |
| `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_hadamard_subtraction_readiness_summary.json` | Deterministic 20/20 scaffold pass with binding readiness `HOLD` |
| `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_HADAMARD_SUBTRACTION_READINESS_2026-09-12.md` | Scaffold result, hashes, missing-operator inventory and next boundary |
| `Theory/Gates/TOP-X4/TOPX4_S2F3_COVARIANT_SCALAR_MATRIX_CONTRACT_2026-09-12.md` | Frozen off-shell fixed-metric scalar Hessian, bundle and counterterm contract |
| `Analysis/TOP/TOP-X4/topx4_s2f3_covariant_scalar_matrix_checkpoint.py` | Rank-three scalar Hessian, symmetry, heat-kernel and mutation executable |
| `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_covariant_scalar_matrix_summary.json` | Deterministic 25/25 operator pass with state/stress HOLD |
| `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_COVARIANT_SCALAR_MATRIX_CHECKPOINT_2026-09-12.md` | Operator derivation, hashes, counterterm map and next boundary |
| `Theory/Gates/TOP-X4/TOPX4_S2F3_SCALAR_MATRIX_HADAMARD_PARAMETRIX_CONTRACT_2026-09-12.md` | Frozen local D5 scalar-matrix Hadamard-parametrix/state-boundary contract |
| `Analysis/TOP/TOP-X4/topx4_s2f3_scalar_matrix_hadamard_parametrix_checkpoint.py` | Local `U_0`--`U_2` coincidence/transport, matrix and firewall executable |
| `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json` | Deterministic 22/22 local-parametrix result; global state/stress HOLD |
| `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_SCALAR_MATRIX_HADAMARD_PARAMETRIX_CHECKPOINT_2026-09-12.md` | Local-parametrix receipt, hashes, limitations and next boundary |

## Entry to Max

The Max A2/A3 task is complete for the exact `X4-I1C` control. Its bounded
fixed-background scalar spectrum survives, but its radion is not stabilized
and no EFT hierarchy is established. The High freeze is complete under
`X4-S2F3`; Plan 11 completed the 12/12 static parity-even determinant and the
9/9 finite-charge entry gate, then completed a 16/16 constant-background
charged-scalar operator and fixed-charge variation checkpoint. This does not
open the evolving-state determinant. The preregistered dynamic
state/subtraction run then failed 11/12: its exact evolving scalar operator and
UV hierarchy passed, but three low-mode fourth-order WKB iterates became
non-positive near the initial boundary. This froze the requirements for the
separate exact-transport retry recorded below. Do not begin A4 or Ultra work.
No gate effect follows.

The separately frozen retry preserves that WKB failure and uses a different
low-mode prescription: positive-Hamiltonian data at `t=0` followed by exact
symplectic transport. It also constructs and exactly evolves a first-order
Dirac superadiabatic projector. All 18/18 bounded checks pass, including
normalization, static and resolution controls and decreasing registered UV
endpoint mixing. This establishes exact transport only. The scalar state is
not an infinite-order matrix adiabatic state, the Dirac projector is only first
order, and the covariant 5D subtraction/counterterm map remains uncomputed.
No stress, Hessian, A4, Ultra or gate promotion follows.

The next frozen readiness checkpoint passes 20/20 checks on the universal
five-dimensional local scaffold: scalar Hadamard singular terms through
`U_2`, matrix Laplace-type coefficients through `b_2`, proper-time divergence
powers and the independent pure-gravity counterterm basis. This is a scaffold
pass, not stress readiness. The audit records `hadamard_stress_ready=false`
because the model-specific off-shell scalar/`chi` matrix operator, scalar and
Dirac Hadamard states, curved graviton/ghost operators, parity-odd phase and
counterterm normalization conditions remain incomplete. The next single gate
is the covariant scalar/`chi` matrix second variation before any homogeneous
or fixed-charge reduction. No downstream promotion follows.

That scalar-matrix checkpoint now passes 25/25 checks. It derives the
fixed-metric off-shell rank-three operator, `E=-H`, zero Cartesian
`Omega_AB`, the pure-gauge phase-aligned connection and the induced scalar
counterterm structures through `b_2`. The result does not construct a
Hadamard state, fix counterterm normalizations, calculate a determinant or
stress, or include the graviton/ghost and parity sectors. The next single gate
is the scalar matrix Hadamard parametrix/state; no A4, Ultra or gate promotion
follows.

## Plan 11 — scalar-matrix Hadamard parametrix

Run the frozen local scalar-matrix checkpoint with:

```powershell
python Analysis\TOP\TOP-X4\topx4_s2f3_scalar_matrix_hadamard_parametrix_checkpoint.py
```

The recorded bounded status is:

```text
PASS_SCALAR_MATRIX_HADAMARD_PARAMETRIX_HOLD_GLOBAL_STATE_AND_STRESS
```

All 22/22 checks pass. The executable registers the five-dimensional
Hadamard singular power and prefactor, verifies the Cartesian `U_0` parallel
transport and the `U_1`/`U_2` coincidence data in the frozen
`P=-(D^2+E)`, `E=-H` convention, and exercises a flat constant-matrix
transport realization. It also retains the phase-aligned pure-gauge
connection and its `2 mu` derivative mixing.

This is a local coincidence/transport checkpoint, not a global state. The
arbitrary-background off-diagonal biscalars, smooth state term `W`, positivity,
wavefront condition, counterterm normalizations, determinant, stress, physical
Hessian, gravity/ghost and parity sectors remain open. The binding fields are
`scalar_matrix_hadamard_parametrix=DERIVED_LOCAL_U0_U2`,
`scalar_matrix_hadamard_state=NOT_CONSTRUCTED`, `physics_pass=false`, and
`gate_effect=NONE`; no A4, Ultra or downstream promotion follows. The next
single gate is a globally admissible infinite-order scalar-matrix state
construction.
