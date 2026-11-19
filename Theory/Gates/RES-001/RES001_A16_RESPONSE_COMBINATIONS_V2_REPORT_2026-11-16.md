# A16.2 bounded response-state extension: dust rates and accelerations

16 November 2026. High confirmed for this bounded derivation. Conditional
initial-point result for the original R4C1/B1 linear export. No new action,
state, degree of freedom, reservoir or physical domain is adopted.

## Identified combinations

Start with the reconstructed map A4 x=(D,Vx,Pi,P_n), where
P_n=Pi_dot-psi_dot alpha in the parent's fixed gauge and normalized frame.
For every map A use T(A)=A_dot+A L along the actual background, xdot=L x.

Exact row selection in increasing index order identifies rows 0 and 1 of
T(A4) as the two independent additions modulo A4. Their physical definitions
in the existing chart are the dust density-contrast rate D_dot and longitudinal
velocity rate Vx_dot. These are response observables, not newly added fields.

    A6 x=(D,Vx,Pi,P_n,D_dot,Vx_dot).

The rate test for A6 again fails closure. Its two independent added rows are
indices 4 and 5 of T(A6), hence the actual dust accelerations:

    A8 x=(D,Vx,Pi,P_n,D_dot,Vx_dot,D_ddot,Vx_ddot).

Every derivative here acts on the coefficient-dependent observation map and
on the full original generator before initial evaluation. The proper-force
and lapse map drift, momentum/field coefficients and background rates are
retained. No constant evaluated row basis is promoted to a time-independent
physical definition.

## Exact result at all five registered modes

| Retained map | Rank A | Rank stacked A,T(A) | Pointwise closed? |
| --- | ---: | ---: | --- |
| A4: dust and force pair | 4 | 6 | No; inherited result reproduced |
| A6: add dust rates | 6 | 8 | No |
| A8: add dust accelerations | 8 | 10 | No |

The same ranks and selections hold at ell=4,8,16,32,64 on the registered
initial background. The executable supplies exact null vectors d for which
A d=0 and T(A)d is nonzero, independently checking the rank criterion by
substitution. All maps and witnesses are retained in the receipt.

For ell=4 the A6 witness has support in original slots 0 and 6: the first
metric coordinate and Cartesian condensate du. The A8 witness has support
in slots 6,8,10: condensate du, reservoir dr and the first metric coordinate's
rate. These are coupled chart directions, not invariant independent sector
interventions. Other modes have their exact witnesses in the receipt; no
physical attribution is inferred from a chosen basis or normalization.

The result says these particular retained response values do not determine
their next initial rates. It does not imply new physical degrees of freedom,
failure of the full system's deterministic evolution, or irreducible memory.
The complete twenty-state description remains the parent of this reduction.
It is not proved that ten selected values would close their own dynamics.

## Verification, scope and preserved failure

[Frozen contract](RES001_A16_RESPONSE_COMBINATIONS_V1_CONTRACT_2026-11-16.md),
[V2 input pins](RES001_A16_RESPONSE_COMBINATIONS_V2_INPUTS_2026-11-16.json),
[V2 executable](../../../Analysis/MasterTests/test_a16_response_combinations_v2.py),
and [receipt](../../../Analysis/MasterTests/outputs/a16_response_combinations_v2_20261116/receipt.json).
30/30 recorded controls pass; fresh-directory replay is byte-identical.

Exact Taylor jets through degree three use the algebraic field containing
the initial H, sqrt(2) and i. This computes only the required initial time
derivatives; it is not a finite-time Taylor approximation. Independent direct
SymPy differentiation checks two nontrivial observation coefficients through
second derivative, including a genuinely time-dependent proper-rate coefficient.
Rational reciprocal/zero-denominator controls, inherited ranks, the initial
Friedmann shell, force reconstruction and coefficient-drift retention are
checked. Exact rank and nullspace witnesses provide complementary tests.
These are same-assistant computational controls, not an independent review panel.

[V1 implementation failure](RES001_A16_RESPONSE_COMBINATIONS_V1_FAILURE_2026-11-16.md)
is preserved with its source and pins: a zero symbolic derivative returned a
Python integer. V2 repairs that representation and selects a nonconstant
proper-rate coefficient for the derivative control. No equation, acceptance
criterion, coupling, state or physical scope was changed.

Only the specified initial event and nonzero modes are tested. Gauge/source
interpretation, original global/constraint restrictions and physical admission
remain inherited obligations. The witnesses are not covered by a new finite-time
error certificate. Zero modes, nonlinear dynamics, kernel normalization and
evolving-domain persistence are not established.

## Handoff: stop the derivative hierarchy here

The authorized six/eight-row calculation is complete in its declared scope.
Do not continue to ten or more response derivatives automatically. Next map
the remaining row-space information to the reconstructed metric, condensate
and reservoir variables and their actual constraints, seeking a physically
interpretable retained-state choice or source experiment. A mere change of
row basis is not a mechanism or an isolated reservoir intervention.

Preserve the distinction between deterministic information hidden by reduction,
a useful effective history law, and a microscopic irreversible reservoir.
The founding organizing question remains Open. No entropy production, selected
structure, acceleration coefficient, matched observable or causal physical
window follows. R-tau remains a separate unadopted comparator. Review DEFERRED;
physics_pass=false; gate_effect=NONE; G1–G6 and MAT matching remain incomplete.
