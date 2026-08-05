# WAK-001 Stage 2 - identity-route evidence rubric

**Subgate:** `PASS_WAK001_IDENTITY_ROUTE_EVIDENCE_RUBRIC_NO_SELECTION`
**Research gate:** `OPEN_SCAFFOLD_ONLY`
**Decision:** `NO_ROUTE_SELECTABLE_ON_CURRENT_EVIDENCE`
**Selected candidate:** `null`
**Identity:** `UNRESOLVED`
**physics_pass:** `false`

## Purpose

The route catalog requires one eventual choice among:

- C1: identify (W) with an existing UVIR mode;
- C2: derive an independent wake sector from a parent action; or
- C3: treat (W) as an internal constitutive variable of the plenum.

This checkpoint compares all three under one hard-requirement rubric. It does
not select a route merely because one candidate has received more template
work.

## Hard requirements

Every route must supply:

1. a microscopic identity or constitutive origin;
2. a complete parent action or controlled constitutive closure;
3. stress-energy or entropy accounting;
4. exact conservation/exchange bookkeeping;
5. coupled-mode independence, or a proof that no kinetic rank is added;
6. a controlled static limit without duplicating the AQUAL response;
7. an interaction-derived source and observable; and
8. covariant completion in a declared domain.

## Comparison result

| Route | Current evidence | Primary blocker | Selectable? |
|---|---|---|---|
| C1 existing UVIR mode | Existing modes are inventoried | No gauge-regular (W=F[\Xi,Q_\rho,Q_\chi,\Pi]) map or single stress allocation | **No** |
| C2 independent sector | Free positive/hyperbolic parent template and bounded local audits | Microscopic independence, (T_W^{\mu\nu}), (I_W^\nu), covariant completion and joined constrained Hessian are absent | **No** |
| C3 internal variable | Route-I bookkeeping is defined | No plenum free-energy/constitutive closure or entropy-production law | **No** |

C2 is the **most developed calculation scaffold**. This is not an identity
selection, preferred physical route or wake-law claim.

The zero-background quadratic factorization does not establish nonlinear
decoupling: the existing audit explicitly restores metric/frame couplings at
cubic order.

## Decision boundary

- keep C1/C2/C3 open;
- do not activate a source or damping term;
- do not identify (W) with a UVIR mode;
- do not create a separate (T_W^{\mu\nu}) until the independent route is
  derived;
- do not package galaxy or cluster observables.

## Reproduction

```text
python Analysis/WAK/WAK-001/ROUTE_DECISION/wak001_identity_route_evidence_rubric.py
```

Expected status:

```text
PASS_WAK001_IDENTITY_ROUTE_EVIDENCE_RUBRIC_NO_SELECTION
```

## Next admissible work

For C2 calculation work, derive (T_W^{\mu\nu}) and (I_W^\nu) from one
covariant (S_W+S_{\rm int}), then construct the joined constrained Hessian.
Alternatively, supply the missing C1 identification map or C3 constitutive
closure and rerun this rubric. No route can be selected before its hard
requirements are evidenced.
