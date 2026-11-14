# Actual ordinary velocity remainder in the strong data norm

4 November 2026. Component of the acknowledged-High actual-rate bundle,
following the [free-velocity coefficient identification](RES001_RTAU_FREE_VELOCITY_IDENTIFICATION_V1_REPORT_2026-11-04.md).
R-tau UNADOPTED; review DEFERRED; physics_pass=false; gate_effect=NONE;
original R4C1 and G1-G6 remain unchanged and incomplete.

## Result and exact scope

The actual initial ordinary material-velocity rows now have an H1 remainder
bound relative to the identified leading operator. The eight configuration-
gradient state rows have a corresponding L2 remainder bound, including
coefficient derivatives and the material-advection commutator. This composes
the action's Legendre inverse, the strong reconstruction and the actual
paired spatial-gauge/coordinate correction instead of transferring the old
unreduced caller-shift estimate to the physical variables by assertion.

The bound is in the declared physical strong-DATA norm, including retained
global partners. It is not a proof of a full flat-20-component evolution
operator, preservation of the compatible domain or a finite-time theorem.
The nine ordinary momentum rows and the force/moving-map rows still need
their own analysis. All constants below are initial bounds on the registered
root domain, not time-uniform coefficients.

## Strong reconstruction used in the composition

Use the prior eight inputs D,Q,P,Z,Mchi,eta_x,eta_y,eta_z: corrected density
L2; free ordinary configuration H1 including physical moduli; ten free
canonical momenta L2; auxiliary force L2; the independent force mean; and
three eliminated-momentum means. Add H, the adapted harmonic coordinate
velocity vector norm. All means in bounds denote absolute values/norms.
Both global charges and the original weighted source range remain required.
No arbitrary tuple is declared an admissible initial perturbation.

The [momentum lift](RES001_RTAU_MOMENTUM_RATE_LIFT_V1_REPORT_2026-11-04.md)
gives the full canonical Qc=||delta q_13||H1 and Pc=||delta p_13||L2 bounds
and an H1 remainder Rp in its local momentum-leading lift. The metric trace
gradient remainder is the [strong reconstruction](RES001_RTAU_STRONG_RECONSTRUCTION_BUNDLE_V1_REPORT_2026-11-04.md)
result. The leading configuration-gradient lift includes all eight free
gradients and the trace term -(gamma/a)*delta p_Vz in both transverse metric
diagonal entries. The force gradient is H1 controlled by force H2 and belongs
to the remainder for these ordinary velocity rows, not to a removed mode.

Gauge-fixed original-coordinate metric entries have profiles J*c_x,J*c_y,
J^2*c_z. Their gradient H1 norm is bounded by Cm*Qc, where

    Cm=(4r+4r^2)*exp(8r), r=1/13000.

This follows from the exact initial J derivatives and the positive lower
profile bound, not from an unproved future gauge ansatz. Thus the full
configuration-gradient lift remainder Rq obeys

    ||Rq||H1 <=sqrt(2)*||metric_trace_gradient_remainder||H1
                                +Cm*Qc+||chi||H2.

The prior force-coordinate estimate supplies chi H2 with its mean retained.

## Canonical and moving-coordinate composition

Let A=L_vv, B=L_vd, C=L_vq, Pi the original-coordinate field gauge projector,
and S the background longitudinal shift. The affine zero-correction velocity
is v0=A^-1*(delta p-B*delta q_z-C*delta q). Put Bm=B+S*A.
After insertion of the local leading momentum/configuration-gradient lifts,
the canonical part of the material-velocity remainder is bounded by

    ||Pi||C1*||A^-1||C1*
       [||Rp||H1+||Bm||C1*||Rq||H1+||C||C1*Qc].

Here ||M||C1 denotes the sufficient multiplier bound
||M||infinity+||M_z||infinity. Derivatives of the temporal inverse are
retained using (A^-1)_z=-A^-1*A_z*A^-1. All full-action blocks and first
spatial derivatives come from the immutable whole-root export.

For the actual initial moving adapted chart, the background velocity w
satisfies w_z=lambda_dot-m-lambda_z*w. Its second derivative has bound

    ||w_zz||infinity <=2*epsilon/31+r*||w||infinity+r*||w_z||infinity,
    epsilon=1/1000.

The mean m is spatially constant and the analytic initial lambda_dot profile
supplies its spatial derivative. No certification error radius is
differentiated. Let Rg be the paired-gauge field remainder, pulled back to
the original coordinate. Exact material/coordinate algebra gives

    v_material=Pi*(v0-S*delta q_z)+Rg
                -Pi*T(w_z)*delta q-(I-Pi)*(S-w)*delta q_z.

T is the field-index part of the longitudinal Lie derivative. In these
field coordinates its diagonal index weights have absolute values at most
two. The last term only selects the three gauge metric gradients, whose
additional derivative is controlled by their retained modulus profiles.
It is not estimated by assuming a second derivative of an arbitrary H1
configuration. The respective H1 multiplier bounds are

    2*||Pi||C1*(||w_z||infinity+||w_zz||infinity)*Qc,
    ||I-Pi||C1*||S-w||C1*Cm*Qc.

The adapted affine rate obeys

    ||Fadapt||L2 <=exp(5r)*[||A^-1||infinity*Pc
       +(||A^-1||infinity*(||C||infinity+||B||infinity)
                         +||w||infinity+2||w_z||infinity)*Qc].

The [paired gauge bound](RES001_RTAU_PAIRED_GAUGE_RATE_V2_REPORT_2026-11-04.md)
then controls Rg in H1. Its reverse field pullback has sufficient H1 norm
exp(r)*(exp(6r)+2r*exp(4r)), including Jacobian, component and derivative
factors. Harmonic coordinate velocities remain in that bound.

The pointwise leading free-velocity map is the registered same-action
Schur coefficient identified in the previous report. This completes the
ordinary velocity remainder composition in the stated strong-data topology.

## Eight strong configuration-gradient rows

Let R select the eight independent ordinary configurations and define
Ygrad=-i*D_z*R*delta q. R has norm at most one, R*E=I8 and annihilates the
unknown transverse metric trace and three gauge metric slots. If V(z) is
the identified pointwise velocity-leading matrix, then

    Ygrad_t-S*D_z Ygrad
      =-i*R*V*D_z Y20-i*R*V_z*Y20
                          -i*D_z*R*Rv-i*S_z*D_z*R*delta q.

Rv is the H1 velocity remainder just bounded. The first term is the
registered principal row. The next three terms are L2 controlled, including
the derivative of V and the derivative/advection commutator. The executable
bounds V_z by differentiating its factors Pi, A^-1, Bm and the local trace
lift gamma/a. It does not differentiate an interval uncertainty radius.

The elementary bound ||Y20||L2<=D+Q+P+Z controls this coefficient-gradient
term. All remaining configuration means/moduli, force mean and momentum
means stay in the declared data norm and reconstruction. This is not an
assertion that those global partners disappeared into Y20.

Both the ordinary velocity H1 remainder and eight gradient-row L2 remainder
are conservatively bounded by 72600 times the sum of the nine declared input
norms/absolute means. The receipt gives the sharper nine-column outward
coefficients. These large triangle/interval bounds do not certify useful
accuracy or a physical growth time, and must not be integrated using initial
constants as if a background time tube had already been proved.

## Evidence and continuation

[Executable](../../../Analysis/MasterTests/test_rtau_ordinary_velocity_remainder_v1.py),
[frozen criteria](RES001_RTAU_ORDINARY_VELOCITY_REMAINDER_V1_SPEC_2026-11-04.md),
[receipt](../../../Analysis/MasterTests/outputs/rtau_ordinary_velocity_remainder_v1_20261104/receipt.json).
11/11 component controls and byte-identical replay COMPLETE. Independent
exact controls verify the coordinate/material decomposition, drift derivative,
strong free chart, coefficient differentiation and advection commutator.
Source bytes, sidecars and timestamps remain preserved. Same-author controls
do not supply independent Rule-9 review.

NEXT: derive the nine ordinary canonical momentum-row remainders, including
the auxiliary-gradient coupling and the paired gauge/coordinate response.
Then assemble the force and density/moving-map sectors, full compatible
tangent generator and energy inequality. T_dot/H_dot, actual background
tube, physical interaction window and identifying matching remain OPEN.
The full actual-generator contract and original G1-G6 are INCOMPLETE.
Goal ACTIVE; High remains acknowledged for this unfinished rate bundle.
No action adoption, paper/site promotion, vault mutation, model dispatch,
Git delivery or publication occurred.
