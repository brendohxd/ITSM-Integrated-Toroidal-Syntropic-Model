# MAT-001 TOP-X4 H1 physical-matter architecture comparison

**Executed:** 2026-09-16  
**Status:** `HOLD_TOPX4_H1_MATTER_ARCHITECTURE_CHILD_ACTION_NOT_FROZEN`  
**Checks:** `10/10`  
**Parent action changed:** `false`  
**Physics pass:** `false`  
**Gate effect:** `NONE`

## 1. Bounded result

The lead source-projection candidate is a **new brane-induced-metric child
route**, not because it solves MAT-001, but because it exposes one universal
physical metric for four-dimensional matter without introducing a full
physical-matter KK tower. This is a route recommendation only; no child action
is frozen or authorized.

Bulk physical matter remains the smooth-circle control. A realistic bulk
matter theory would require the complete gauge/Higgs/Yukawa/chiral spectrum,
its KK tower, anomaly data and its loop contribution to stabilization.

## 2. Exact kinematic result

For the verified Einstein-frame chart,

\[
A_b(\sigma)=r^{-1/2}
=\exp\!\left[-\frac{\sigma}{\sqrt{6}M_{\rm Pl}}\right],
\qquad
\alpha_b=\frac{d\ln A_b}{d\sigma}
=-\frac{1}{\sqrt{6}M_{\rm Pl}}.
\]

A minimally coupled massive bulk-scalar zero mode has an `r`-independent
four-dimensional kinetic coefficient and
`m_0(sigma)=m_5 exp[-sigma/(sqrt(6) M_Pl)]`, giving the same logarithmic
mass derivative in that limited control.

This common coefficient is **not** `V`: it is an unreduced radion source
component before metric/radion/condensate mixing and auxiliary constraints.

## 3. Direct-map no-go

The Einstein--Hilbert radion kinetic operator is homogeneous of degree two in
first derivatives. Track A requires degree three through `Y^(3/2)`. A regular
point-field redefinition preserves derivative degree, so

```text
DIRECT_RADION_EQUALS_TRACK_A_PSI = REJECTED
```

Only a newly derived mixed radion--condensate physical mode or other nonlinear
dynamics can keep the TOP-X4 H1 route open.

## 4. Structural comparison

| Requirement | Bulk physical matter | Brane-localized physical matter |
|---|---|---|
| `preserves_smooth_circle_classically` | `YES` | `NO_LOCALIZED_DEFECT_ADDED` |
| `avoids_physical_matter_KK_towers` | `NO` | `YES_BY_CONSTRUCTION` |
| `chiral_4d_matter_without_new_bulk_mechanism` | `NO_ON_CURRENT_SMOOTH_S1_SPECIFICATION` | `POSSIBLE_IN_DECLARED_4D_MATTER_ACTION` |
| `universal_source_metric_is_explicit` | `REQUIRES_COMPLETE_REDUCED_MATTER_THEORY` | `YES_AT_INDUCED_METRIC_KINEMATIC_LEVEL` |
| `junction_and_localized_counterterms` | `ABSENT` | `COMPULSORY` |
| `changes_S2F3_quantum_stabilization_problem` | `YES_FULL_PHYSICAL_MATTER_SPECTRUM` | `YES_LOCALIZED_STRESS_BOUNDARY_DATA_COUNTERTERMS` |
| `directly_derives_track_a_Y_three_halves` | `NO` | `NO` |

No numerical weights were assigned.

## 5. Evidence checks

| Check | Satisfied |
|---|---|
| `all_authority_and_input_files_exist` | yes |
| `all_required_sidecars_match_current_bytes` | yes |
| `comparison_does_not_relabel_the_existing_chi_proxy` | yes |
| `brane_induced_metric_radion_scaling_is_exact` | yes |
| `bulk_scalar_zero_mode_is_canonical_and_has_same_mass_scaling` | yes |
| `kinematic_source_coupling_has_mat_mass_dimension` | yes |
| `direct_radion_to_track_a_map_is_rejected` | yes |
| `comparison_is_structural_and_contains_no_weighted_score` | yes |
| `primary_source_anchors_are_registered` | yes |
| `parent_survival_and_physical_hessian_holds_remain_binding` | yes |

## 6. Rejection controls

- `quadratic_radion_promoted_to_track_a`: rejected
- `parent_modified_during_comparison`: rejected
- `child_freeze_without_global_preflight`: rejected
- `kinematic_alpha_promoted_to_physical_residue`: rejected
- `bulk_brane_hybrid`: rejected
- `operator_homogeneity_mismatch_erased`: rejected

All `6/6`
registered mutations were rejected. This is local contract validation, not
independent Rule-9 review.

## 7. Literature boundary

- Appelquist, Cheng and Dobrescu:
  <https://arxiv.org/abs/hep-ph/0012100>.
- Papavassiliou and Santamaria:
  <https://arxiv.org/abs/hep-ph/0102019>.
- Kofman, Martin and Peloso:
  <https://arxiv.org/abs/hep-ph/0401189>.
- Maeda and Wands:
  <https://arxiv.org/abs/hep-th/0008188>.

These sources support the architecture cautions; they do not validate ITSM.

## 8. Next single gate

`TOPX4_H1_BRANE_CHILD_GLOBAL_CONSISTENCY_PREFLIGHT`: test compact-circle consistency,
localized variation, junction data and counterterm requirements before any
brane child action can be frozen. Stop before changing `X4-S2F3`.

## 9. Artifact record

- JSON: `Analysis/MAT/MAT-001/TOPX4_H1_BRIDGE/outputs/mat001_topx4_h1_matter_architecture_comparison_summary.json`
- JSON SHA-256: `9119fd4a26d102a463acaef324adb1b8c4c5a1850c653fe03727d5fbe97eefca`
- contract: `Theory/Gates/MAT-001/MAT-001_TOPX4_H1_MATTER_ARCHITECTURE_COMPARISON_CONTRACT_2026-09-16.md`
- executable: `Analysis/MAT/MAT-001/TOPX4_H1_BRIDGE/mat001_topx4_h1_matter_architecture_comparison.py`

## 10. Binding boundary

```text
lead_source_projection_candidate=BRANE_INDUCED_METRIC_CHILD_ROUTE
lead_meaning=ROUTE_RECOMMENDATION_ONLY
child_action_freeze=NOT_AUTHORIZED
direct_radion_track_a_map=REJECTED_DERIVATIVE_HOMOGENEITY_MISMATCH
mixed_radion_condensate_mode=OPEN_DEPENDENCY_LOCKED
physical_hessian=NOT_CONSTRUCTED
signed_residue=NOT_COMPUTED
K_Q=NOT_DERIVED
V=NOT_COMPUTED
MAT-001=BLOCKED
Stage4A=CLOSED
physics_pass=false
gate_effect=NONE
```
