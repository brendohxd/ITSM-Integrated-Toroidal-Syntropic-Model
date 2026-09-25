# MAT-001 TOP-X4 constraint/projection bookkeeping diagnostic

**Executed:** 2026-09-18  
**Status:** PASS_CONSTRAINT_PROJECTION_BOOKKEEPING_HOLD_PHYSICAL_HESSIAN  
**Checks:** 13/13  
**Scope:** synthetic exact rational algebra only  
**Physics pass:** false  
**Gate effect:** NONE

## 1. Result

This receipt tests the algebraic bookkeeping needed before a live constrained
source projection. It is motivated by the constraint-retention method in
arXiv:1901.03292v2, but it is not a reproduction of that paper and does not
claim a Dirac-bracket, action, background or physical-Hessian result.

The declared auxiliary block has determinant `14`. Exact
elimination gives the Schur pair `H_phys` and `c_phys`; the full quadratic
form agrees with the reduced form on all registered samples with residuals
`['0', '0', '0']`. The selected mode has norm squared
`445/14`, source numerator
`29/14`, and orientation-reversed numerator
`-29/14`.

## 2. Evidence checks

| Check | Satisfied |
|---|---|
| all_authority_inputs_exist | yes |
| all_required_sidecars_match_current_bytes | yes |
| prior_x4_s4_handoff_remains_non_promoting | yes |
| toy_matrix_dimensions_and_symmetry | yes |
| auxiliary_stationarity_is_satisfied | yes |
| schur_reduction_matches_completion_of_square | yes |
| full_and_reduced_quadratic_forms_agree | yes |
| reduced_pair_is_covariant_under_invertible_basis_changes | yes |
| selected_mode_has_positive_reduced_kinetic_norm | yes |
| orientation_reversal_changes_signed_source | yes |
| auxiliary_source_contribution_is_retained | yes |
| singular_auxiliary_domain_is_rejected_without_pseudoinverse | yes |
| non_promoting_firewall_remains_closed | yes |

## 3. Rejection controls

- physical_hessian_promoted: rejected
- x4_s4_action_frozen: rejected
- x4_s2f3_parent_changed: rejected
- singular_domain_pseudoinverse: rejected
- orientation_sign_erased: rejected
- auxiliary_source_dropped: rejected

All 6/6
registered mutations were rejected. This is local contract validation, not
independent Rule-9 review.

## 4. Scientific boundary

The diagnostic uses a declared three-variable/two-auxiliary toy quadratic
system. It validates stationarity, completion of the square, basis covariance,
positive-norm mode orientation, auxiliary-source retention and singular-domain
rejection. It does not construct the X4-S4 action or any live TOP-X4 physical
Hessian. In particular:

    parent_action_changed=false
    X4-S4_action_frozen=false
    physical_hessian_constructed=false
    MAT-001=BLOCKED
    K_Q=NOT_DERIVED
    V=NOT_COMPUTED
    Stage4A=CLOSED
    physics_pass=false
    gate_effect=NONE

## 5. Next single gate

`TOPX4_H1_X4-S4_NEW_PARENT_ACTION_CONTRACT` remains the next substantive gate.
The diagnostic does not authorize action variation or change to X4-S2F3.

## 6. Artifact record

- JSON: Analysis/MAT/MAT-001/TOPX4_H1_BRIDGE/outputs/mat001_topx4_h1_constraint_projection_diagnostic_summary.json
- JSON SHA-256: 79e842e11a7fb3ff695cf33c0e16c1f7d9d21742a6dbea1165d5f187f4ccbfc5
- contract: Theory/Gates/MAT-001/MAT-001_TOPX4_H1_CONSTRAINT_PROJECTION_DIAGNOSTIC_CONTRACT_2026-09-18.md
- executable: Analysis/MAT/MAT-001/TOPX4_H1_BRIDGE/mat001_topx4_h1_constraint_projection_diagnostic.py
- paper-method source: https://arxiv.org/html/1901.03292v2
