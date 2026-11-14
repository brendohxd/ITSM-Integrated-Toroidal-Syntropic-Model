# Nine ordinary momentum-row L2 remainders

4 November 2026. Component of the acknowledged-High actual-rate bundle,
following the [strong ordinary velocity remainder](RES001_RTAU_ORDINARY_VELOCITY_REMAINDER_V1_REPORT_2026-11-04.md).
R-tau UNADOPTED; original R4C1 unchanged; review DEFERRED;
physics_pass=false; gate_effect=NONE; G1-G6 INCOMPLETE.

## Result and precise scope

All nine ordinary canonical momentum rows now have explicit initial L2
remainder bounds relative to the same-action material principal flux and
the retained auxiliary-gradient coupling. Local reaction, zeroth-order
flux, coefficient gradients and the paired gauge momentum response remain.
This is a strong remainder estimate, not a relabelled H^-1 momentum bound.

Together with the preceding eight configuration-gradient rows, it controls
the initial ordinary-row remainders in the declared physical strong-data
norm. It does not complete the force/density/moving-map sectors, prove that
the output remains in the evolving compatible domain, or provide a full
generator/energy inequality or an actual background time tube.

## Exact canonical material flux

Use the full thirteen-field action coefficients

    A=L_vv, B=L_vd, G=L_dd, C=L_vq, Dq=L_dq,
    Bm=B+S*A, Gm=G+S*(B+B^T)+S^2*A,
    Fq=Dq+S*C.

S is the background longitudinal shift in the original coordinate. Let
v0 be the zero-corrective-shift canonical velocity and vm=v0-S*delta q_z.
The exact Legendre identity is delta p=A*vm+Bm*delta q_z+C*delta q.
For the ordinary row selection (0,1,3,6,7,8,9,10,11), the material Euler
equation can therefore be written

    delta p_t-S*delta p_z
        =local+S_z*delta p
             -D_z[Bm^T*vm+Gm*delta q_z+Fq*delta q]
             +a_q*D_z(delta Z)+paired_gauge.

Here local contains L_qq*delta q+L_qv*v0+L_qd*delta q_z and the local
auxiliary-value column. The ordinary auxiliary value/gradient FLUX columns
are exactly zero by the inherited action identities and exported zero
pattern. The local auxiliary-gradient term is not zero: in the two
transverse metric diagonal rows it is

    a_q=-d*psi_z/(2*a^2), d=b*N*a, b=5/11,

and it vanishes in the other seven ordinary rows. It stays in the registered
principal operator. Interval overlap checks consistency of this known exact
coefficient identity; overlap is not its proof. Spatial force-field terms
remain in the regular flux/remainder and are controlled by force H2.

Fq is essential: the canonical momentum relation contributes S*C in addition
to L_dq. Omitting this zeroth-order flux or its spatial coefficient derivative
would not give the actual momentum equation. Similarly S_z*delta p comes
from -D_z(flux)-S*D_z(delta p)=-D_z(flux+S*delta p)+S_z*delta p.

## Identification of the leading reduced flux

Let E and Bg be the free-slot embedding and spatial field generator of the
[free-velocity identification](RES001_RTAU_FREE_VELOCITY_IDENTIFICATION_V1_REPORT_2026-11-04.md),
with K=Bg^T*A*Bg. At leading order write vm=E*v+Bg*nu and delta q_z=E*X.
The momentum constraint gives

    nu=-K^-1*Bg^T*(A*E*v+Bm*E*X).

Substituting into E^T*(Bm^T*vm+Gm*E*X) yields exactly

    Ceff^T*v+Geff*X,
    Ceff=E^T*(Bm-A*Bg*K^-1*Bg^T*Bm)*E,
    Geff=E^T*(Gm-Bm^T*Bg*K^-1*Bg^T*Bm)*E.

These are the same material Schur coefficients used by the registered
principal calculation. The ordinary nine-slot selection retains the force
field in the full source/remainder while respecting its stronger regularity.
No kinetic signature or physical mode is selected by this algebra. The
previous strong lifts provide the actual lower-order corrections to this
pointwise leading reconstruction.

## Continuum bound and gauge transport

Let Rp and Rq be the full momentum-leading and configuration-gradient lift
remainders in H1, with Qc=||delta q_13||H1 and Pc=||delta p_13||L2. The raw
material velocity remainder obeys

    ||Rvm||H1 <=||A^-1||C1*
                      [||Rp||H1+||Bm||C1*||Rq||H1+||C||C1*Qc].

The ordinary regular flux remainder is bounded in H1 by

    ||Bm||C1*||Rvm||H1+||Gm||C1*||Rq||H1+||Fq||C1*Qc.

Its derivative is L2 controlled. All C1 matrix bounds use the cached full
action coefficients and first spatial derivatives, including S_z and
(A^-1)_z=-A^-1*A_z*A^-1. The local velocity has the sufficient L2 estimate
||v0||L2<=||A^-1||infinity*[Pc+(||C||infinity+||B||infinity)*Qc].
This controls the full ordinary local reaction and S_z*delta p; the local
auxiliary column is bounded by ||delta Z||L2.

Differentiation of the leading flux also produces its coefficient derivative
times Y20. That derivative is explicitly bounded using Bm_z,Gm_z and the
local momentum/trace-gradient lifts, and ||Y20||L2<=D+Q+P+Z. No derivative
of an arbitrary L2 momentum or of an interval error radius is assumed.

For the paired gauge contribution, use the prior adapted canonical response.
The exact rate identities are p_rate,new=Tp*(p_rate,corrected-Lie_w^dual dp)
and p_rate,affine,new=Tp*(p_rate,zero-Lie_w^dual dp). Restoring the original
canonical rate cancels the two identical background-coordinate Lie terms,
leaving Tp^-1 times the actual paired gauge response. Its L2 pullback has
bound exp(5r), retaining the canonical Jacobian. The corrective gauge depends
on the affine field rate including w; that dependence is retained using
the preceding explicit affine-rate bound. Harmonic velocities remain inputs.

All nine ordinary L2 remainders are conservatively bounded by 47749 times
the sum of the same nine physical input norms/absolute means as the velocity
owner. The receipt supplies sharper nine-column binary outward bounds.
These large initial triangle/interval constants are not measured growth
rates, useful accuracy estimates or time-uniform coefficients. A background
tube is still required before any finite-time conclusion.

## Evidence, failure preservation and next work

[Executable V2](../../../Analysis/MasterTests/test_rtau_ordinary_momentum_remainder_v2.py),
[V1 criteria](RES001_RTAU_ORDINARY_MOMENTUM_REMAINDER_V1_SPEC_2026-11-04.md),
[V2 correction](RES001_RTAU_ORDINARY_MOMENTUM_REMAINDER_V2_SPEC_2026-11-04.md),
[receipt](../../../Analysis/MasterTests/outputs/rtau_ordinary_momentum_remainder_v2_20261104/receipt.json).
13/13 component controls and byte-identical replay COMPLETE. Independent
exact noncommuting block controls verify the Schur flux and canonical
constraint; other exact controls retain material flux, zeroth flux and the
paired moving-coordinate cancellation. Source bytes, sidecars and timestamps
are preserved. These remain same-author controls, not Rule-9 clearance.

V1 stopped before receipt generation on a missing spatial-Jet exp method.
Its source, specification, failure record and hashed failed-run log remain.
V2 evaluates the identical exponential using the factory's j.exp function.
No equation, branch, norm, tolerance or acceptance threshold changed.

NEXT: derive the actual force-pair remainder, with all mixed-order
cancellations, auxiliary metric-gradient mixing and coefficient drift.
Then assemble the density/physical-variable and moving Green/range maps,
the full compatible tangent generator and energy inequality. Ordinary-row
control alone does not complete those tasks. T_dot/H_dot, actual background
tube, physical window and identifying matching remain OPEN. Goal ACTIVE;
High remains acknowledged for the unfinished rate bundle. No action adoption,
paper/site promotion, vault mutation, dispatch or Git/publication occurred.
