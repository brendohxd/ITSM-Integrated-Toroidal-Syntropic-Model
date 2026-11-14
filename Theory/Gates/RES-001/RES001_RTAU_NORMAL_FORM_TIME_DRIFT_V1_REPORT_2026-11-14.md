# Actual initial time drift of the cross normal form

The [frozen contract](RES001_RTAU_NORMAL_FORM_TIME_DRIFT_V1_CONTRACT_2026-11-14.md)
now has a conditional whole-initial-root numerical estimate:

    ||C_t||infinity <2.787274,
    ||T_t||L2->L2 <2.787274,
    ||T_t T^-1||L2->L2 <7.001777.

These constants use the registered benchmark time and coordinate norm;
they are not rates measured in physical seconds or observed growth rates.
The upper endpoints before rounding are approximately 2.787273566455799
and 7.001776432940290. This completes the initial time-drift component,
not the coupled energy inequality or an actual evolution interval.

## Derivative being bounded

Use the original-coordinate periodic primitive P and the registered
left-primitive cross change

    T=I+i P C(z,t), T_t=i P C_t.

The primitive is fixed in this coordinate. This does not set the separate
physical constraint Green/range maps or their time derivatives to zero.
The scalar corrected-density normal form already belongs to the earlier
actual row calculation; C is the later matrix cross change and must not
be confused with that scalar coefficient.

The actual time-dependent transformed equation contains T_t T^-1 Z.
It is separate from the already bounded physical-advection commutator.
Neither contribution is substituted for the other.

## Generic action coefficients and required rates

The [material-block specification](RES001_RTAU_MATERIAL_BLOCK_TIME_EXPORT_V1_SPEC_2026-11-14.md)
gives the action-level structural argument. ADM, frame, canonical and
alignment derivative sectors are quadratic forms with field-dependent
coefficients. The weak spatial curvature is also quadratic in derivatives.
The nonlinear force and combined R-tau regulator have no ordinary-velocity,
ordinary-gradient or shift-gradient argument. Thus the selected ordinary
principal Hessians depend on q alone after converting to material form.

For a general longitudinal shift S, the raw blocks satisfy

    A(S)=A0, B(S)=B0-S A0,
    Cshift(S)=C0, Dshift(S)=D0-S C0, Kshift(S)=K0.

Schur reduction therefore cancels S and S_t from B_R and Dshift+S Cshift.
This is an algebraic material identity, not the choice S_t=0. The export
takes generic second variations in nine ordinary velocities, nine ordinary
gradients and three shift gradients. Its outer first-time jet retains the
actual q_t. Only those required subblocks are evaluated; the full action
Hessian is not recomputed. Their values are checked against the preserved
action export with its material correction.

The initial force coefficients retain independent proper velocity p and
gradient s, together with their actual rates. The certified p_t enclosure
comes from the full canonical clock Euler current and Legendre identity.
It is not inferred by fixing p or differentiating the root uncertainty.
The actual s_t, lapse, volume, metric, frame and scalar rates remain.

In the ordinary slots, generic differentiation gives

    pi_psi=mu f_p,
    Tq_i=mu_i f_p+mu f_pqi,
    Qaux_i=-s[kappa (log mu)_i+kappa_i],
    aq_i=b N mu Qaux_i, kappa=h^zz.

These expressions use the full nonlinear force and generic metric/frame
variables before the conformal initial slice is evaluated. The registered
conformal first metric tangent is used at that instant only; it is not a
future conformal evolution ansatz. Inverse derivatives are retained:

    (Kshift^-1)_t=-Kshift^-1 Kshift_t Kshift^-1,
    (Mordinary^-1)_t=-Mordinary^-1 Mordinary_t Mordinary^-1.

## Both cross directions and operator bound

For the preserved leading gradient map L, ordinary velocity V and full
shift-gradient response W, the generic reverse coefficient is

    Bfo,first=-kappa aphi Tq L+i Qaux V-i kappa s W_long
              -vphi Qaux L,
    Bfo,second=0.

W_long denotes the longitudinal row of the shift-gradient response.
This is the full auxiliary/clock variation, including raw/projected
velocity and gauge cancellation, expressed without discarding generic
metric variation. Its values agree with the registered conformal formula.
The forward block retains i aq in the nine ordinary momentum rows. The
time export differentiates

    Cof=-Bof Afast^-1, Cfo=Afast^-1 Bfo,

including every inverse and product factor. The density row and column of
C_t remain exactly zero; both ordinary/force cross directions remain.
The independent generic forward formula is

    Cof_(P_i,xi)=-i s[(log mu)_i+kappa_i/kappa].

The numerical estimate uses the Frobenius enclosure of the complete
twenty-by-twenty C_t, hence bounds its operator norm. Since ||P||=1 and
the existing original-coordinate inverse has norm below 2.512052107,
the two displayed operator bounds follow on the transported registered
domain. No arbitrary physical-domain extension or frequency cutoff is used.

## Checks and limits

The [executable](../../../Analysis/MasterTests/test_rtau_normal_form_time_drift_v1.py)
verified 431 pinned inputs and seventeen controls, including exact
noncommuting material/inverse identities, retained proper-clock-rate
dependence and generic metric rates. Its
[receipt](../../../Analysis/MasterTests/outputs/rtau_normal_form_time_drift_v1_20261114/receipt.json)
replayed byte for byte.

The [separate audit](../../../Analysis/MasterTests/audit_rtau_normal_form_time_drift_v1.py)
passed seven controls and replayed exactly. Closed scalar and frame kinetic
Hessians independently check value and time-rate enclosures; the generic
forward formula checks its metric time dependence. Exact rational endpoint
arithmetic checks the Frobenius bound and inverse composition. Enclosure
overlap is a consistency check; the generic action identities supply the
coefficient formulas. These are same-assistant checks, not an independent
review panel or Rule-9 clearance. All original sources/sidecars remain.

Next: derive the controlling energy's actual initial H_t, then assemble
the full supported energy/global-partner estimate and investigate actual
compatible-domain/background persistence. Initial constants do not supply
a time tube and must not be integrated as time-uniform bounds. Positive
controlling energy is not a claim of a positive physical Hamiltonian.

R-tau UNADOPTED; review DEFERRED; physics_pass=false; gate_effect=NONE.
Interactions, matching, numerical weak-field normalization and canonical
promotion remain outside this result's clearance.
