# MAT-001 TOP-X4 H1 X4-S4 new-parent action-contract receipt

**Executed:** 2026-09-18  
**Status:** PASS_X4_S4_GW2_CANDIDATE_ACTION_CONTRACT_HOLD_PARENT_ACCEPTANCE  
**Candidate:** X4-S4-GW2  
**Checks:** 21/21  
**Physics pass:** false  
**Gate effect:** NONE

## 1. Result

The X4-S4-GW2 geometry, field inventory, leading classical bulk/localized
action, variational signs, fixed-charge definition, zero-charge sum rule,
counterterm classes and source-independent primary domain are now frozen for
one background-existence test.

This is not acceptance of X4-S4-GW2. It closes action-selection ambiguity for
the next calculation while leaving the finite-charge background,
semiclassical action, physical Hessian, H1 residue, MAT coefficient and Rule-9
review open.

## 2. Evidence checks

| Check | Satisfied |
|---|---|
| all_authority_and_input_files_exist | yes |
| all_required_sidecars_match_current_bytes | yes |
| prior_route_handoff_authorizes_only_a_separate_new_parent_design | yes |
| orbifold_geometry_fixed_points_parities_and_observed_T3_are_explicit | yes |
| field_content_is_complete_without_silent_X4_S2F3_inheritance | yes |
| bulk_boundary_GHY_induced_gravity_and_localized_actions_are_declared | yes |
| every_frozen_operator_has_the_required_bulk_or_boundary_mass_dimension | yes |
| bulk_and_boundary_scalar_variations_match_the_frozen_potentials | yes |
| GHY_junction_stress_and_upstairs_factor_conventions_are_closed | yes |
| embedding_bending_and_radion_are_retained_until_after_variation | yes |
| fixed_charge_is_temporal_variational_and_has_no_protected_y_winding | yes |
| zero_charge_static_seed_sum_rule_has_correct_complex_scalar_weight | yes |
| static_sum_rule_gradient_weights_follow_from_stress_trace_combination | yes |
| sum_rule_sign_obstruction_and_finite_charge_limit_are_fail_closed | yes |
| background_programme_orders_static_seed_before_finite_charge_and_Hessian | yes |
| renormalization_scheme_and_bulk_boundary_counterterm_classes_are_registered | yes |
| semiclassical_and_finite_counterterm_claims_remain_open | yes |
| primary_parameter_domain_is_bounded_and_source_independent | yes |
| human_contract_covers_the_structured_variational_boundary | yes |
| candidate_freeze_is_separated_from_parent_acceptance | yes |
| downstream_physics_and_publication_firewall_remains_closed | yes |

The mass-dimension test evaluates every frozen bulk operator to dimension 5
and every localized operator to dimension 4. Symbolic differentiation of the
bulk and boundary potentials returned zero residual for all four registered
derivatives.

## 3. Rejection controls

- `second_fixed_surface_removed`: rejected
- `orbifold_replaced_by_smooth_circle`: rejected
- `GHY_omitted`: rejected
- `X4_S2F3_spectators_silently_inherited`: rejected
- `stabilizer_internal_Z2_removed`: rejected
- `protected_interval_winding_inserted`: rejected
- `localized_induced_curvature_omitted`: rejected
- `static_sum_rule_sign_obstruction_ignored`: rejected
- `zero_charge_sum_rule_reused_at_finite_charge`: rejected
- `finite_charge_background_claimed_solved`: rejected
- `candidate_promoted_to_accepted_parent`: rejected
- `physical_Hessian_and_H1_promoted`: rejected
- `action_parameter_selected_from_observational_target`: rejected
- `boundary_scalar_counterterm_class_omitted`: rejected
- `semiclassical_completion_claimed_without_calculation`: rejected

All 15/15
registered mutations were rejected. These are contract-integrity controls,
not independent peer review or evidence that a background exists.

## 4. Scientific boundary

The frozen split is:

    candidate_action_contract_frozen=true
    X4-S4-GW2_classical_action_frozen_for_one_background_test=true
    X4-S4_parent_accepted=false
    X4-S2F3_parent_changed=false
    finite_charge_background_solved=false
    semiclassical_action_complete=false
    counterterms_finitely_normalized=false
    physical_hessian_constructed=false
    signed_H1_residue_computed=false
    Rule9_cleared=false
    MAT-001=BLOCKED
    K_Q=NOT_DERIVED
    V=NOT_COMPUTED
    Stage4A=CLOSED
    physics_pass=false
    gate_effect=NONE

The zero-charge static sum rule is registered only for the Lorentz-invariant
flat-slice seed. It is explicitly not reused unchanged at finite temporal
charge.

## 5. Next single gate

`TOPX4_H1_X4-S4_ZERO_CHARGE_BACKGROUND_EXISTENCE` must test the frozen candidate for a
regular fully backreacted zero-charge solution satisfying both scalar boundary
conditions, both gravitational junction systems and the integrated balance.
It must stop before finite-charge continuation if that seed fails.

## 6. Artifact record

- JSON: Analysis/MAT/MAT-001/TOPX4_H1_BRIDGE/outputs/mat001_topx4_h1_x4_s4_new_parent_action_contract_summary.json
- JSON SHA-256: 0e7d18811ec40f1a2966b6a6010b2dd3be6651427527ec541eb5cc6ce1875c66
- contract: Theory/Gates/MAT-001/MAT-001_TOPX4_H1_X4_S4_NEW_PARENT_ACTION_CONTRACT_2026-09-18.md
- executable: Analysis/MAT/MAT-001/TOPX4_H1_BRIDGE/mat001_topx4_h1_x4_s4_new_parent_action_contract.py
- Goldberger-Wise class: https://arxiv.org/abs/hep-ph/9907447
- backreacted scalar-gravity-brane system: https://arxiv.org/abs/hep-th/9909134
- compact-space sum rules: https://arxiv.org/abs/hep-th/0011225
- physical radion mixing: https://arxiv.org/abs/hep-ph/0401189
- induced brane curvature: https://arxiv.org/abs/hep-th/0005016
