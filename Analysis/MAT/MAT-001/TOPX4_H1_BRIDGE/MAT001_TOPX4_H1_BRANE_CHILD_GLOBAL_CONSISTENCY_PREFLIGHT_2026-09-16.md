# MAT-001 TOP-X4 brane-child global-consistency preflight

**Executed:** 2026-09-16  
**Status:** HOLD_TOPX4_H1_BRANE_CHILD_GLOBAL_SUM_RULE_AND_RENORMALIZATION  
**Checks:** 11/11  
**Parent action changed:** false  
**Physics pass:** false  
**Gate effect:** NONE

## 1. Bounded result

The brane-induced-metric route remains a conditional research candidate, but
the preflight does not authorize a child action. Under the declared static,
flat-four-dimensional, periodic-circle assumptions, a single uncompensated
positive renormalized brane tension is rejected by the required global
compact-space balance. A tensionless or compensated background remains
possible only after the child action derives the compensator and all localized
variation data.

The result is therefore:

    BRANE_ROUTE=CONDITIONAL_SURVIVOR_TENSIONLESS_BACKGROUND_ONLY
    single_uncompensated_positive_tension=REJECTED_GLOBAL_SUM_RULE
    child_freeze=HOLD_PENDING_GLOBAL_SUM_RULE_AND_RENORMALIZATION

This is a consistency boundary, not a constructed brane theory and not a
MAT-001 result.

## 2. Exact local controls

The proper transverse measure is R_ref*r dy. The covariant localized source
uses delta_perp = delta_2pi(y-y_b)/(R_ref*r), whose integral against that
measure is exactly one. The localized Lagrangian has mass dimension four,
delta_perp has mass dimension one, and the five-dimensional source integrand
has mass dimension five.

These controls do not solve the defect equations. The brane response includes
the induced-metric stress trace and radion variation, while a two-sided
junction/embedding treatment is still required on a smooth periodic circle.

## 3. Global compact-space boundary

The relevant integrated Einstein/scalar condition must be derived from the
child action with exact weights and signs. This preflight records the
conditional kill criterion: with a canonical-sign bulk contribution, flat
four-dimensional slices, periodic internal space, and no negative/flux/
curvature compensator, a lone positive renormalized localized tension cannot
be accepted as a static solution.

The preflight does not claim that every brane model is impossible. It narrows
the admissible child start to a derived zero-tension condition, a derived
global compensator, or a different complete curved/warped background.

## 4. Localized variation and renormalization

The future child must specify whether the source is a two-sided defect or an
orbifold fixed point, the normal orientation, junction equations, brane
bending, induced metric, bulk/scalar boundary data and all localized matter
variations. Matter loops require localized tension and induced-curvature
counterterms with a declared regulator, subtraction scheme and renormalized
conditions. These terms feed the same stress, determinant and physical
Hessian problem; they cannot be added after the fact.

## 5. Evidence checks

| Check | Satisfied |
|---|---|
| all_authority_and_input_files_exist | yes |
| all_required_sidecars_match_current_bytes | yes |
| architecture_recommendation_is_the_frozen_brane_candidate | yes |
| proper_transverse_delta_is_exactly_normalized | yes |
| localized_covariant_dimension_closes | yes |
| localized_variation_and_radion_response_are_required | yes |
| two_sided_junction_and_embedding_data_are_required | yes |
| periodic_global_sum_rule_and_conditional_rejection_are_frozen | yes |
| localized_counterterm_obligation_is_frozen | yes |
| source_anchor_and_parent_firewall_are_present | yes |
| upstream_holds_remain_binding | yes |

## 6. Rejection controls

- coordinate_delta_used_without_proper_measure: rejected
- periodic_defect_treated_as_external_boundary: rejected
- lone_positive_tension_accepted: rejected
- junction_data_set_to_zero_by_omission: rejected
- kinematic_alpha_promoted_to_h1_residue: rejected
- brane_added_to_frozen_parent: rejected
- localized_counterterms_omitted: rejected
- observational_target_selected_tension_or_root: rejected

All 8/8
registered mutations were rejected. This is local contract validation, not
independent Rule-9 review.

## 7. Source boundary

The compact-space consistency requirement is informed by Gibbons, Kallosh and
Linde, Brane world sum rules:
https://arxiv.org/abs/hep-th/0011225

That source constrains the kind of integrated check required; it does not
supply ITSM child equations, renormalized coefficients or a MAT solution.

## 8. Next single gate

TOPX4_H1_BRANE_CHILD_ACTION_FREEZE_OR_REJECT: derive the exact child global balance
and localized renormalization conditions, then decide whether a separate
brane child action can be frozen. Stop before changing X4-S2F3.

## 9. Artifact record

- JSON: Analysis/MAT/MAT-001/TOPX4_H1_BRIDGE/outputs/mat001_topx4_h1_brane_child_global_consistency_summary.json
- JSON SHA-256: 524c59483430e4efcb5520c65a73e7f2236c0d11dbc53bd4423e2448dc4af8f8
- contract: Theory/Gates/MAT-001/MAT-001_TOPX4_H1_BRANE_CHILD_GLOBAL_CONSISTENCY_CONTRACT_2026-09-16.md
- executable: Analysis/MAT/MAT-001/TOPX4_H1_BRIDGE/mat001_topx4_h1_brane_child_global_consistency_preflight.py

## 10. Binding boundary

    preflight_status=FROZEN_NON_PROMOTING
    parent_action_changed=false
    brane_child_action=NOT_FROZEN
    global_sum_rule=NOT_DERIVED
    localized_variation=REQUIRES_CHILD_ACTION
    junction_data=NOT_DERIVED
    localized_counterterms=NOT_NORMALIZED
    single_uncompensated_positive_tension=REJECTED_CONDITIONALLY
    route_disposition=CONDITIONAL_SURVIVOR_TENSIONLESS_BACKGROUND_ONLY
    MAT-001=BLOCKED
    K_Q=NOT_DERIVED
    V=NOT_COMPUTED
    Stage4A=CLOSED
    physics_pass=false
    gate_effect=NONE
