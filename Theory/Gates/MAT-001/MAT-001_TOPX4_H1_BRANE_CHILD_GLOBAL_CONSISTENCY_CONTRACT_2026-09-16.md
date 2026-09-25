# MAT-001 TOP-X4 brane-child global-consistency preflight contract

**Date:** 2026-09-16  
**Status:** FROZEN_NON_PROMOTING_GLOBAL_CONSISTENCY_PREFLIGHT  
**Parent:** unchanged X4-S2F3  
**Candidate:** a separately versioned brane-induced-metric child only  
**Allowed effect:** conditional route disposition  
**Gate effect:** none

## 1. Purpose and stop boundary

This is a preflight for the recommended brane matter architecture. It asks
whether a future four-dimensional matter hypersurface can be added to a
periodic five-dimensional circle consistently enough to justify a separately
frozen child action.

It does not add a brane to X4-S2F3, vary a final child action, solve the
junction equations, calculate K_Q or V, construct the physical Hessian, or
reopen MAT-001/Stage 4A. A bookkeeping pass is not a physics pass.

The preflight must keep three statements separate:

1. the induced-metric radion coefficient is a kinematic source component;
2. a localized action is a new codimension-one theory ingredient; and
3. global compact-space consistency is an independent condition on the full
   bulk, defect, boundary and counterterm system.

## 2. Candidate localized action and covariant delta

The candidate child must begin from a declared action of the form

    S_child = S_X4-S2F3 + S_brane
    S_brane = - integral d4x sqrt(-gamma)
               [lambda_b + L_matter(gamma, Psi)]

with the brane at a declared position y = y_b on the periodic circle.
The induced metric is

    gamma_mn = r^(-1) g_mn = A_b(sigma)^2 g_mn
    A_b(sigma) = exp[-sigma/(sqrt(6) M_Pl)]

If the localized term is represented in a five-dimensional covariant
equation, use

    delta_perp(y) = delta_2pi(y - y_b) / (R_ref r)
    integral_0^(2pi) dy R_ref r delta_perp(y) = 1

for the registered metric chart. The delta is a density with respect to the
proper transverse measure; it is not an open boundary or an inserted
four-dimensional portal.

In natural units, lambda_b and the four-dimensional matter Lagrangian have
mass dimension four, delta_perp has mass dimension one, and the covariant
five-dimensional integrand has dimension five. The normalization and
dimension checks are necessary, not sufficient.

## 3. Localized variation obligations

Varying the induced metric produces both the tangential brane stress and its
radion response. The response contains the declared tension and the
matter-trace contribution; it cannot be replaced by alpha_b alone.

An actual codimension-one defect also requires the normal/embedding variation
and the appropriate two-sided junction or fixed-point/orbifold conditions. A
smooth periodic circle has no external endpoint at which the source can be
discarded. The child contract must state:

- whether the hypersurface is an internal two-sided defect or a fixed point of
  an orbifold;
- the induced metric and brane stress convention;
- the normal orientation and both-sided jump condition;
- the brane-bending/embedding degree of freedom and its constraints;
- the localized gravitational and scalar boundary data; and
- the gauge, matter and counterterm variations supported on the defect.

Setting the opposite-side data, brane bending, or a localized variation to
zero without deriving it is a rejection.

## 4. Periodic compact-space consistency

Before a child action is frozen, its background must satisfy a global
integrated compact-space condition. For a static periodic circle with flat
four-dimensional slices and the canonical-sign bulk sector, the relevant
weighted Einstein/scalar sum rule has the schematic form

    0 = weighted_sum(renormalized localized tensions)
        + integral_circle dy [canonical nonnegative gradient terms
                               + declared bulk potential/flux terms]

The exact weights and signs must be derived from the child action and metric
ansatz; this preflight does not invent them. It does establish the following
conditional rejection: a single uncompensated positive renormalized brane
tension cannot be accepted as a static periodic flat-circle background when
all remaining registered contributions are nonnegative and no compensating
negative/flux/curvature term is present.

Therefore a tensionless background term is not an automatic solution either.
The child must explicitly derive one of:

- a renormalized zero-tension condition;
- a compensating bulk/defect contribution with its sign and origin; or
- a different curved/warped background and its complete equations.

The compact-space condition is a background consistency prerequisite, not a
claim that a brane route is impossible in every extended theory.

## 5. Localized renormalization

Four-dimensional matter loops on a hypersurface generate localized
counterterm structures, at minimum a tension/cosmological term and an
induced-curvature term, with further operators determined by the field
content and symmetries. The child must specify a regulator, subtraction
scheme, renormalized conditions and scale dependence. "Set the tension to
zero" without a renormalization condition and loop calculation is incomplete.

The localized counterterms modify the same background, determinant, stress
and physical-Hessian problem that the child is meant to solve. They are not
post-processing corrections.

## 6. Decision rule

The preflight may return the following conditional disposition:

    BRANE_ROUTE=CONDITIONAL_SURVIVOR_TENSIONLESS_BACKGROUND_ONLY
    single_uncompensated_positive_tension=REJECTED_GLOBAL_SUM_RULE
    child_freeze=HOLD_PENDING_GLOBAL_SUM_RULE_AND_RENORMALIZATION

This means the induced-metric route remains worth a child-action
investigation only if the background tension is renormalized to zero or
globally compensated and the full localized variation is supplied. It does
not mean a consistent child has been constructed.

## 7. Rejection tests

Reject an attempted preflight if it:

- normalizes the localized delta with coordinate measure instead of proper
  transverse measure;
- treats the internal brane as an external boundary or drops the opposite
  side of a smooth periodic circle;
- identifies alpha_b with the constrained H1 residue, V or K_Q;
- accepts a lone positive tension on a static periodic flat circle without a
  derived compensator;
- sets brane-bending, junction, localized curvature or counterterm data to
  zero by omission;
- adds the brane directly to the frozen X4-S2F3 parent;
- uses a desired a0, H0, SPARC result or MAT status to select a tension,
  radius or root; or
- claims Rule-9 clearance or a physics pass from local consistency checks.

## 8. Primary-source boundary

The preflight is informed by Gibbons, Kallosh and Linde, Brane world
sum rules, https://arxiv.org/abs/hep-th/0011225, which derives integrated
consistency conditions for compact internal spaces. That source constrains
the type of global check required; it does not supply the ITSM child
equations, renormalized coefficients or a MAT solution.

## 9. Binding boundary

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
