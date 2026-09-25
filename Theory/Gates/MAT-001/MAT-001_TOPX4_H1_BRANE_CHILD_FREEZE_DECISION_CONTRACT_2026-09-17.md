# MAT-001 TOP-X4 brane-child action freeze decision contract

**Date:** 2026-09-17  
**Status:** FROZEN_NON_PROMOTING_CHILD_FREEZE_DECISION  
**Candidate tested:** minimal unwarped single-tension brane child  
**Parent:** unchanged X4-S2F3  
**Allowed effect:** scoped candidate rejection or route continuation  
**Gate effect:** none

## 1. Purpose and scope

This contract makes the next decision after the brane-child
global-consistency preflight. It tests whether the simplest proposed child
can be frozen:

    S_minimal = S_X4-S2F3 + S_brane
    S_brane = - integral d4x sqrt(-gamma)
               [lambda_b + L_matter(gamma, Psi)]

The tested minimal candidate retains the registered unwarped static
four-dimensional-slice chart, uses one internal two-sided localized
hypersurface, supplies no negative/flux/curvature compensator, and does not
alter the frozen X4-S2F3 action.

The decision is deliberately narrower than "brane route impossible." It may
reject the minimal child while preserving a separately designed compensated
or warped child route.

No MAT-001 quantity, K_Q, V, physical Hessian, parent action, Rule-9 status or
publication status may change in this gate.

## 2. Minimal-product distributional control

For the constant-radius flat-product control, the registered metric has no
distributional curvature at an internal hypersurface unless a warp/junction
profile or equivalent localized gravitational term is introduced. In the
minimal candidate:

    bulk distributional Einstein tensor = 0
    brane tangential stress = -lambda_b gamma_mn delta_perp

Consequently, with no other localized contribution or compensator, the
distributional tangential equation requires the renormalized background
tension to vanish:

    lambda_b^ren = 0

This is an exact statement for the declared minimal flat-product control. It
is not an exact sum rule for a future warped, flux-supported or otherwise
extended child. Such a child must derive its own weighted integrated
equations.

Matter vacuum energy and loop counterterms contribute to lambda_b^ren. A
bare statement that lambda_b is zero is not a renormalization condition.

## 3. Freeze prerequisites

A separate child action may be frozen only when all of the following are
present:

1. a new versioned action and matter field content, without mutating X4-S2F3;
2. an exact bulk/defect variation with the induced stress and radion source;
3. an internal-defect or orbifold choice with normal orientation and
   two-sided/fixed-point junction equations;
4. a derived global balance for the selected curved or flat background;
5. a regulator, subtraction scheme and renormalized localized tension and
   induced-curvature conditions;
6. the brane-bending/embedding degree of freedom and its constraints;
7. a controlled finite-charge on-shell background and EFT domain; and
8. an explicit decision that the child is a new research theory, not the
   canonical parent or a hidden four-dimensional portal.

The current evidence does not supply these prerequisites. The existing
X4-S2F3 parent is a smooth-circle bulk control with no brane term.

## 4. Decision rule

Under the minimal-product assumptions, return:

    minimal_child=REJECTED_ZERO_TENSION_DISTRIBUTIONAL_CONTROL
    brane_route=OPEN_ONLY_COMPENSATED_OR_WARPED_CHILD
    child_action_freeze=NOT_AUTHORIZED

The route remains open only for a new child that derives a zero-renormalized
background tension, an explicit global compensator, or a different
warped/curved background with complete field equations and junction data.

The decision does not compute the H1 residue. Even a future accepted child
would still require the complete renormalized action, state-dependent stress,
constraint reduction, positive-norm mode and signed source projection.

## 5. Deterministic rejection tests

Reject an attempted freeze if it:

- promotes the minimal product result to a complete brane solution;
- treats lambda_b^ren = 0 as automatic without localized renormalization;
- hides a negative/flux/curvature compensator outside the declared action;
- drops the internal two-sided junction or brane-bending variation;
- adds the brane directly to X4-S2F3;
- promotes alpha_b to the constrained H1 residue or to V/K_Q;
- freezes a child without a derived global balance and counterterm conditions;
- chooses a tension, radius, warp profile or root from a0, H0, SPARC or MAT;
  or
- claims a physics pass, gate opening or Rule-9 clearance from this decision.

## 6. Binding boundary

    decision_status=REJECT_MINIMAL_BRANE_CHILD_FREEZE_CONDITIONALLY
    minimal_child=REJECTED_ZERO_TENSION_DISTRIBUTIONAL_CONTROL
    brane_route=OPEN_ONLY_COMPENSATED_OR_WARPED_CHILD
    child_action_freeze=NOT_AUTHORIZED
    parent_action_changed=false
    global_sum_rule=NOT_DERIVED_FOR_FUTURE_CHILD
    localized_variation=NOT_CLOSED
    junction_data=NOT_DERIVED
    localized_counterterms=NOT_NORMALIZED
    MAT-001=BLOCKED
    K_Q=NOT_DERIVED
    V=NOT_COMPUTED
    Stage4A=CLOSED
    physics_pass=false
    gate_effect=NONE
