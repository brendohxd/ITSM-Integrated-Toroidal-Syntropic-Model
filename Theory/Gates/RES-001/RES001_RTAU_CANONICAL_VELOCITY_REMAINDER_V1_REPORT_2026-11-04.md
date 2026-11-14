# Actual unreduced canonical velocity rows and H1 remainder

4 November 2026. Component of the acknowledged-High actual-rate bundle,
following the [momentum lift](RES001_RTAU_MOMENTUM_RATE_LIFT_V1_REPORT_2026-11-04.md).
R-tau UNADOPTED; review DEFERRED; physics_pass=false; gate_effect=NONE;
original R4C1 and G1-G6 remain unchanged and incomplete.

## Exact row and bound

For all thirteen nonauxiliary canonical fields, reuse the full action
export with coefficient blocks

    A=L_vv, C=L_vq, B=L_vd, E=L_vS, F=L_vSz.

Here d=q_z. Configuration and velocity slots are those of the existing
clock-gauge action, including the force field and its lapse dependence.
The full Legendre variation is exactly

    delta v=A^-1*(delta p-C*delta q-B*D_z delta q
                             -E*delta S-F*D_z delta S).

The auxiliary velocity is absent; the Legendre columns for the auxiliary
field and its gradient are exactly zero by the inherited action identity.
The source checks that zero pattern. No nonauxiliary direction is removed.

Keep the unreduced leading row

    v_lead=A^-1*(delta p-B*D_z delta q-F*D_z delta S).

Its remainder is exactly

    Rv=-A^-1*C*delta q-A^-1*E*delta S.

This split still contains the actual shift and its gradient. It is not yet
the strong-state principal comparison or the compatible gauge generator.

Let a0 bound ||A^-1||infinity, a1 bound ||A_z||infinity, and c0,c1 bound
||C||infinity, ||C_z||infinity, using spectral norms conservatively enclosed
by the exported Frobenius bounds. The exact inverse derivative is

    (A^-1)_z=-A^-1*A_z*A^-1.

Consequently ||(A^-1)_z||infinity<=a0^2*a1. The ordinary H1 product rule
then bounds the C contribution by

    [a0*(c0+c1)+a0^2*a1*c0]*||delta q_13||H1.

The same expression with E's coefficient bounds gives the shift contribution.
This proves a continuum H1 multiplier bound, including coefficient gradients,
without differentiating an arbitrary L2 momentum or replacing the temporal
inverse by a midpoint inverse. The inherited temporal inverse and every
coefficient/first spatial derivative cover the certified initial root ball
and the whole original circle. No Hessian is recalculated.

In normalized original-coordinate control units, conservative outward bounds are

    ||A^-1||infinity <24.020615,
    ||(A^-1)_z||infinity <1.861383,
    ||Rv||H1 <=65.080769*||delta q_13||H1
                         +0.029339661*||delta S||H1.

The force coordinate is included in delta q_13. The established force H2
topology is stronger than the H1 input used here. This H1 output bound does
NOT supply an H2 force-velocity bound or control two derivatives of that
row in the auxiliary time equation. Its relevant cancellations and orders
must be established in the actual mixed system. These constants are not
growth rates, finite-time errors or physical scales.

## Controls and next required composition

[Versioned executable](../../../Analysis/MasterTests/test_rtau_canonical_velocity_remainder_v1.py),
[frozen criteria](RES001_RTAU_CANONICAL_VELOCITY_REMAINDER_V1_SPEC_2026-11-04.md),
[receipt](../../../Analysis/MasterTests/outputs/rtau_canonical_velocity_remainder_v1_20261104/receipt.json).
11/11 same-author controls pass, with byte-identical replay COMPLETE.
Independent exact variable-coefficient controls verify the Legendre split,
the inverse derivative and rejection of an omitted inverse derivative.
All inherited source bytes, existing sidecars and timestamps are preserved.
The controls are not independent Rule-9 clearance.

NEXT: close the paired spatial-gauge correction and coordinate drift, using
the existing actual gauge equations and retained harmonic/modulus partners.
Compose with the strong configuration-gradient and momentum lifts to compare
the ordinary velocity rows with the registered principal block. Keep the
force row's actual derivative order explicit; do not replace its missing
strong rate estimate by this H1 result. Then assemble momentum/force rates,
moving Green/range and physical-variable maps. Full actual-generator bound,
T_dot/H_dot, evolving compatible domain and background tube remain OPEN.
The present row split is an intermediate component, not acceptance of the
full actual-generator contract. The goal remains ACTIVE and the acknowledged
High calculation bundle is unfinished. No action adoption, matching input,
paper/site change, vault mutation, model dispatch or Git delivery occurred.
