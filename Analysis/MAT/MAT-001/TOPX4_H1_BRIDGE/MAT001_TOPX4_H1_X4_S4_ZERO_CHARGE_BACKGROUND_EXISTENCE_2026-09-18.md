# MAT-001 TOP-X4 H1 X4-S4 zero-charge background-existence receipt

**Executed:** 2026-09-18  
**Status:** BENCHMARK_REJECTED_RETURN_TO_ACTION_SELECTION  
**Scope:** one preregistered internal zero-charge static benchmark  
**Checks:** 12/12  
**Physics pass:** false  
**Gate effect:** NONE

## 1. Result

The frozen X4-S4-GW2 action was tested with a fully backreacted warped
zero-charge ansatz. The numerical solver retained the two scalar equations,
the warp-factor equation, both scalar Robin systems, both gravitational
junction conditions and an independent Hamiltonian-constraint audit.

The benchmark is internal and dimensionless in units of `M5=1`; no observed
radius, Hubble value, BBN abundance, SPARC fit, `K_Q` or `V` value selected a
parameter. A successful benchmark is only a seed receipt and does not accept
X4-S4-GW2 or open finite charge.

## 2. Selected numerical result

{
  "L": 8.505356709014385e-13,
  "L_guess": 1.2,
  "V0": 3.424105252191412,
  "Vpi": -2.74027179435987,
  "boundary_max_abs": 2.6862062383514637e-12,
  "boundary_residuals": [
    2.117582368135751e-22,
    -3.654890357290082e-15,
    3.653108550073248e-15,
    -2.6862062383514637e-12,
    -8.268730538135763e-13,
    -3.6898385312258814e-13,
    5.6135730198634015e-14
  ],
  "constraint_max_abs": 10.972344011877714,
  "field_ranges": {
    "A": [
      -1.0044244664631912e-12,
      2.117582368135751e-22
    ],
    "f": [
      0.12139874128451576,
      0.12139874128451619
    ],
    "h": [
      0.7671255800582627,
      0.767125580062656
    ],
    "p": [
      -1.3397584057591754e-12,
      -7.207639061574195e-13
    ],
    "u": [
      -1.5095894431775406e-15,
      1.5078076359607119e-15
    ],
    "v": [
      -5.3712303913749774e-12,
      -3.6225773279257416e-12
    ]
  },
  "finite": true,
  "gradient_integral": 2.298795990729875e-11,
  "iterations": 3,
  "mesh_nodes": 385,
  "message": "The algorithm converged to the desired accuracy.",
  "regular": false,
  "solver_status": 0,
  "solver_success": true,
  "sum_rule": 0.6838334578545303,
  "variant": 2
}

## 3. Evidence checks

| Check | Satisfied |
|---|---|
| all_authority_and_input_files_exist | yes |
| all_required_sidecars_match_current_bytes | yes |
| frozen_action_and_route_handoff_are_authoritative | yes |
| benchmark_is_internal_dimensionless_and_not_observationally_selected | yes |
| human_contract_covers_the_registered_bvp_and_stop_boundary | yes |
| solver_attempts_use_fixed_action_and_bounded_initialization_variants | yes |
| solver_outcome_is_explicitly_classified_without_parameter_drift | yes |
| boundary_audit_is_executed_and_classified | yes |
| independent_Einstein_constraint_audit_is_executed_and_classified | yes |
| independent_static_sum_rule_audit_is_executed_and_classified | yes |
| positive_internal_modulus_and_no_finite_charge_or_H1_claim | yes |
| non_promoting_firewall_remains_closed | yes |

## 4. Mutation controls

- `benchmark_parameter_changed_after_registration`: rejected
- `observational_target_entered_scope`: rejected
- `finite_charge_promoted_from_static_seed`: rejected
- `parent_accepted_from_one_benchmark`: rejected
- `physical_hessian_promoted`: rejected
- `constraint_failure_accepted`: rejected
- `sum_rule_failure_accepted`: rejected
- `negative_modulus_accepted`: rejected
- `solver_claim_without_registered_solution`: rejected

All 9/9
registered mutations were rejected. This is local gate-integrity testing, not
independent Rule-9 review.

## 5. Boundary

The independent constraint and static integrated balance were not used as
solver boundary conditions. Finite-charge continuation remains closed, and no
physical Hessian, H1 residue, MAT coefficient, determinant, stress tensor or
publication status follows.

    candidate_action_contract_frozen=true
    X4-S4_parent_accepted=false
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

`TOPX4_H1_X4-S4_ACTION_SELECTION_AFTER_ZERO_CHARGE_TEST` — Return to X4-S4 action selection; finite charge remains closed.

## 7. Artifact record

- JSON: Analysis/MAT/MAT-001/TOPX4_H1_BRIDGE/outputs/mat001_topx4_h1_x4_s4_zero_charge_background_existence_summary.json
- JSON SHA-256: 312d6a205bf4988e22c75f36401ae71657b239e3091fa7c13cf593bd8c46e238
- contract: Theory/Gates/MAT-001/MAT-001_TOPX4_H1_X4_S4_ZERO_CHARGE_BACKGROUND_EXISTENCE_CONTRACT_2026-09-18.md
- executable: Analysis/MAT/MAT-001/TOPX4_H1_BRIDGE/mat001_topx4_h1_x4_s4_zero_charge_background_existence.py
