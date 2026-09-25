# MAT-001 TOP-X4 H1 X4-S4 post-zero-charge action selection

**Executed:** 2026-09-19  
**Status:** SELECT_CURVED_SLICE_OUTPUT_ROUTE_HOLD_EXECUTION  
**Checks:** 13/13  
**Physics pass:** false  
**Gate effect:** NONE

## 1. Decision

The rejected flat benchmark remains immutable. Its failure is classified as a
codimension-one flatness compatibility failure: seven flat-BVP unknowns are
already consumed by seven gauge/boundary/junction conditions, leaving the
Hamiltonian constraint as one additional action-parameter relation.

The selected next route is `X4-S4-C1`: retain the same action and solve the
signed maximally symmetric four-dimensional curvature `kappa4` as an internal
output. No observational value or sign is supplied.

## 2. Symbolic audit

The registered residuals are:

{
  "Einstein_difference_residual": "0",
  "curved_constraint_derivative_residual": "0",
  "flat_constraint_derivative_residual": "0",
  "generalized_balance_residual": "0"
}

All residuals vanish exactly. The audit checks the curved Einstein-tensor
difference, propagation of the flat and curved constraints, and the
generalized integrated balance.

## 3. Evidence checks

| Check | Satisfied |
|---|---|
| all_authority_and_input_files_exist | yes |
| all_required_sidecars_match_current_bytes | yes |
| failed_flat_benchmark_is_preserved_as_authority | yes |
| frozen_candidate_action_remains_unaccepted_and_unchanged | yes |
| flat_BVP_equation_count_exposes_one_compatibility_condition | yes |
| curved_Einstein_signs_and_constraint_propagation_are_symbolically_closed | yes |
| curvature_output_restores_unknown_condition_count_without_tension_retuning | yes |
| induced_curvature_junction_terms_are_retained_with_explicit_tree_values | yes |
| generalized_balance_reduces_to_flat_rule_and_remains_postsolve | yes |
| route_order_separates_generic_curvature_tuning_diagnostic_and_action_change | yes |
| human_contract_covers_the_failure_diagnosis_and_selected_route | yes |
| no_observational_target_or_downstream_quantity_selects_the_route | yes |
| non_promoting_firewall_remains_closed | yes |

## 4. Mutation controls

- `failed_benchmark_erased`: rejected
- `unchanged_flat_rerun_authorized`: rejected
- `flat_tension_tuning_promoted_to_primary`: rejected
- `curvature_selected_from_observation`: rejected
- `curvature_sign_reversed`: rejected
- `constraint_curvature_sign_reversed`: rejected
- `endpoint_constraint_omitted`: rejected
- `induced_curvature_terms_omitted`: rejected
- `left_induced_curvature_junction_sign_reversed`: rejected
- `integrated_balance_boundary_sign_reversed`: rejected
- `superpotential_action_silently_inserted`: rejected
- `parent_accepted_from_route_selection`: rejected
- `finite_charge_opened`: rejected
- `physical_hessian_promoted`: rejected

All 14/14
mutations were rejected. This validates the route-selection contract only; it
does not demonstrate that a regular curved background exists.

## 5. Scientific boundary

The flat-tension eigenvalue route remains a secondary fine-tuning diagnostic.
A superpotential-correlated bulk/brane action remains deferred because it
would change the candidate action. The unchanged flat benchmark is not rerun.

    action_changed=false
    X4-S4_parent_accepted=false
    curved_background_solved=false
    finite_charge_background_solved=false
    physical_hessian_constructed=false
    MAT-001=BLOCKED
    K_Q=NOT_DERIVED
    V=NOT_COMPUTED
    Stage4A=CLOSED
    Rule9_cleared=false
    physics_pass=false
    gate_effect=NONE

## 6. Next single gate

`TOPX4_H1_X4-S4_CURVED_SLICE_BACKGROUND_OUTPUT_TEST` — Solve signed kappa4 as an internal output of the unchanged zero-charge action while imposing the endpoint constraint and independently checking the full-mesh constraint and generalized integrated balance.

## 7. Artifact record

- JSON: Analysis/MAT/MAT-001/TOPX4_H1_BRIDGE/outputs/mat001_topx4_h1_x4_s4_action_selection_after_zero_charge_test_summary.json
- JSON SHA-256: 1d418bf9cf8fc015002c13a63ae09aece88c56f8e9f00b57d963f16fcacfe3c7
- contract: Theory/Gates/MAT-001/MAT-001_TOPX4_H1_X4_S4_ACTION_SELECTION_AFTER_ZERO_CHARGE_TEST_CONTRACT_2026-09-19.md
- executable: Analysis/MAT/MAT-001/TOPX4_H1_BRIDGE/mat001_topx4_h1_x4_s4_action_selection_after_zero_charge_test.py
- primary flatness/curvature source: https://arxiv.org/abs/hep-th/9909134
- compact-space sum-rule source: https://arxiv.org/abs/hep-th/0011225
- non-fine-tuned curved-brane example: https://arxiv.org/abs/hep-th/0011156
