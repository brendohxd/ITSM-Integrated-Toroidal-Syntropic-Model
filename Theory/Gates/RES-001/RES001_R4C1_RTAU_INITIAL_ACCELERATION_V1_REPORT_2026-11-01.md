# Prepared R-tau initial acceleration and gauge construction

1 November 2026. Conditional comparison result; review DEFERRED.
physics_pass=false; gate_effect=NONE. R-tau remains unadopted; the original
R4C1 action, its failed domains and canonical G1-G6 status are unchanged.

## Result and limits

The thirteen nonauxiliary initial accelerations now have an explicit
functional construction: the actual pointwise temporal inverse applied to
the full Euler forcing, followed by a periodic spatial-gauge correction.
The correction retains shift drift, all metric components and mean metric
accelerations, and preserves the original-coordinate zero shift-mean
convention. Uniform, coarse initial bounds cover every certified root.
The auxiliary first time tangent Zdot is also fixed by its spatial relation.

This is not a sharp numerical evaluation of the final continuum gauge
integrals. The displayed centre samples are particular-inverse diagnostics,
not the final exact-root gauge-fixed accelerations. Quantitative auxiliary
second-rate/higher-derivative bounds, local clock-evolution checks, the full
physical symplectic quotient and finite-time evolution remain open.

Owner: [prepared-Cauchy contract](RES001_R4C1_RTAU_PREPARED_CAUCHY_V1_CONTRACT_2026-10-31.md).
Inputs: [mixed operator](RES001_R4C1_RTAU_MIXED_OPERATOR_V4_REPORT_2026-11-01.md),
[prepared gauge](RES001_R4C1_RTAU_SPATIAL_GAUGE_V1_REPORT_2026-10-31.md),
[temporal inverse](RES001_R4C1_RTAU_PREPARED_TEMPORAL_V2_REPORT_2026-10-31.md),
[initial-root certificate](RES001_R4C1_RTAU_PERIODIC_INVERSE_V1_REPORT_2026-10-31.md).
The [construction contract](RES001_R4C1_RTAU_INITIAL_ACCELERATION_V1_CONTRACT_2026-11-01.md)
was frozen before execution. The actual action coefficients remain declared
diagnostic choices, not new identifying matching information.

## Shift drift is the coordinate generator, not a chosen physical forcing

In the original ADM variables the shift enters the time-rate part through
v-Lie_S(q). The lapse is the already declared clock branch and is fixed
when taking a velocity/shift variation at fixed spatial fields. Consequently

    C=L_vS=-M*D0, D=L_vSz=-M*D1,
    Lie_T(q)=D0*T+D1*T_z.

For M=L_vv restricted to the thirteen nonauxiliary coordinates, the full
initial Euler system therefore gives

    a=a0+Lie_T(q), a0=M^-1*R, T=Sdot,
    R=L_q-(L_d)_z-L_vq*v-L_vd*v_z.

All metric, independent frame, canonical scalar and force entries remain.
The source R is the full mixed-owner forcing, not a homogeneous propagator.
The particular inverse a0 parametrizes the affine family; it does not
assign the physical shift drift to zero. The actual T is chosen below by
the existing spatial gauge and original shift-mean convention.

The actual centre inverse is interval-residual controlled at z=0.3,1.1,2.4.
The shift/Lie coupling residual is below 1.52e-49 there. A nonzero shift-rate
jet substituted into the full affine Euler system has residual below
3.32e-48. These point controls supplement the all-root inverse bounds;
they do not replace the exact-root continuum construction.

## Differentiate the existing gauge without preserving conformal evolution

Retain the frozen initial map zeta0(z), J=zeta0_z=exp(lambda)/Abar,
w=zeta_t/J, m=H+epsilon*R2/31 and r=lambda_dot-m=w_z+lambda_z*w.
To specify its second coordinate jet, choose only the coordinate extension

    zeta(t,z)=zeta0(z)+t*zeta1(z), zeta1=J*w.

This preserves the existing first jet and has zeta_tt=0. It is not a
physical time-evolution ansatz. The inverse coordinate has

    z_t=-w, z_tt=2*w*w_z+lambda_z*w^2.

At the initial slice h_new,xz=h_new,yz=0, h_new,zz=Abar^2, with compatible
first velocities already certified. Transforming the particular metric
acceleration gives the three quantities

    b_x=a0_xz/J, b_y=a0_yz/J,
    b_z=a0_zz/J^2+Abar^2*(-8*r*lambda_dot+6*r^2).

The last term is a real coordinate two-jet contribution, not an assumption
about future conformality. The independent inverse-coordinate audit uses
a deliberately nonconformal second metric jet anchored to an actual a0
sample and confirms this term. No initial conformal/velocity shape is
projected onto subsequent evolution.

Let xi be the pushforward of T, xi=(T_x,T_y,J*T_z). Gauge acceleration
tangency requires

    b_x+h_xx*xi_x,zeta=c_x,
    b_y+h_yy*xi_y,zeta=c_y,
    b_z+2*Abar^2*xi_z,zeta=c_z,

where the right-hand sides are spatial constants. Periodicity FIXES them:

    c_x=<b_x/h_xx>_zeta/<1/h_xx>_zeta,
    c_y=<b_y/h_yy>_zeta/<1/h_yy>_zeta,
    c_z=<b_z>_zeta.

These are the actual mean metric accelerations, not parameters set to zero.
The derivative right-hand sides have zero zeta means. Integrate them with
the periodic antiderivative Pi, initially normalized to zero zeta mean.
Fix the remaining additive coordinate translations by

    xi_x=Pi(g_x)-<Pi(g_x)>_z, and similarly y,
    xi_z=Pi(g_z)-<Pi(g_z)/J>_z/<1/J>_z.

Then T=(xi_x,xi_y,xi_z/J) has zero original z means, preserving the original
shift normalization. Only coordinate translations are fixed. Physical
homogeneous metric modes and the global momentum equation are retained.

The prepared-coordinate shift drift also has a baseline coordinate term:

    Sdot_new=(-w*Sx_z,-w*Sy_z,
               J*(w_z*Sz-w*Sz_z+w*r))+xi.

It must not be replaced by xi alone. The independent inverse-map test
checks this formula using the actual prepared centre shift. All coordinate
transformations are of the same torus and clock; no topology or scale is
selected to obtain a desired force coefficient.

## Controlled initial bounds and their practical weakness

The prior normal-rate gap and positive metric/lapse factors imply
||M^-1||_2<24.021 in the original coordinate rate convention. Combining it
with the full mixed forcing gives ||a0||_2<118.740 uniformly in z and over
all certified roots. Periodic antiderivatives have L-infinity norm at most
pi/2; imposing the old shift-mean convention can double that bound.

The resulting deliberately coarse estimates include

    max |xi_x,y| < 746.291,
    max |xi_z| < 373.205,
    max |T_z| < 373.262,
    ||a||_2 < 530.385.

These are initial coordinate control constants. They are not measured
accelerations, physical cutoffs, a useful evolution error estimate, or
evidence that a large shift drift is actually present. Actual centre a0
samples are much smaller; the loose norm bounds lose cancellations and
use worst-case component forcing. A sharp final gauge quadrature is still
NOT_COMPUTED. No time interval of domain preservation follows from these
initial constants alone.

## Auxiliary first tangent and action consistency

The auxiliary relation is Z=-Delta_h psi. With the actual first metric jet
on this initial conformal slice, differentiation gives

    Zdot=-2*lambda_dot*Z-exp(-2lambda)*
      (psi_dot_zz+lambda_z*psi_dot_z+lambda_dot_z*psi_z).

This fixes the previously unused auxiliary velocity slot. Its value did
not affect the preceding momentum equations: the mixed owner proves
those momentum derivatives independent of Z, Z_z and Zdot. In prepared
coordinates Zdot_new=Zdot-w*Z_z. The all-root bound is

    |Zdot_new|<0.000475041.

An independent direct derivative of the geometric auxiliary relation agrees
to better than 1.75e-105 at the control point. This is first time tangency;
quantitative Zddot and higher spatial/acceleration derivative bounds are open.

For the original EL convention E_q=L_q-pi_t-(L_d)_z, action spatial
covariance gives

    E_Sdot=Dq^* E_q-ad_S^* E_S.

This identity follows by varying q with Lie_xi(q) and the shift with
xi_t+[xi,S] and integrating by parts. It includes constant parameters and
therefore the mean momentum equation; it is not merely its mean-free
projection. Together with the exact-root initial E_S=0 and the constructed
initial Euler equations, it supplies initial momentum consistency in the
corresponding variational/weak sense. The phase and clock/global energy
identities are

    Qdot=-<Jphase.E_q>,
    I=-H-<S.E_S>, Idot=<E_q.v-S.E_Sdot>.

Thus the declared global charges are consistent with this initial jet.
The audit derives the generic parameter/boundary identity independently.
This is an action-identity argument, not a newly measured local clock Ward
residual or a finite-time conservation certificate. The local reconstructed
clock/density evolution still needs its explicit check.

## Reproducibility, review and next dependency

[Executable](../../../Analysis/MasterTests/test_01_r4c1_rtau_initial_acceleration_v1.py):
23/23, no failed/unknown checks; exact recomputing read-only replay.
[Receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_initial_acceleration_v1_attempt_01/summary.json)
SHA256 dbcdacf8954e1cc59a2ebc42b91cd77f7a8e3473c2c54906b1f94e506455154d.

[Coordinate/variational audit V2](../../../Analysis/MasterTests/audit_01_r4c1_rtau_initial_acceleration_v2.py):
11/11, exact replay.
[Audit receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_initial_acceleration_audit_v2_attempt_01/summary.json)
SHA256 a0e30b7444c0831ecb76fd985122ff9dd6be045a14b112ced9fd9e2ceda86208.
Independent inverse-coordinate second differences use two steps and a
manufactured second jet, not a claimed evolved solution. Audit V1 remains
preserved at 10/11: its extra bound-count assertion expected 13 rather than
the actual 12 named bounds. The [V2 schema specification](RES001_R4C1_RTAU_INITIAL_ACCELERATION_AUDIT_V2_SPEC_2026-11-01.md)
replaces that number with the explicit required key set. No physics or
geometric acceptance threshold changes. Same-author controls are not
independent external scientific review.

Next obtain sharp certified final gauge/acceleration values and higher
auxiliary/gauge derivative controls, check local clock reconstruction,
and complete the field-dependent physical symplectic/characteristic
problem before any finite-time admission claim. Retain both parities,
all planar harmonics, means, moving projectors and root uncertainty.
General transverse spatial wavevectors, nonlinear evolution, interactions/
window and identifying matching remain open. Do not substitute old homogeneous
propagation or repeated projection for those missing calculations.

There is no concrete correction to P1/P2, Thermodynamics or the original
R4C1 paper from this unadopted initial construction. Papers and site remain
unchanged. G1-G6 incomplete; no canonical promotion, action adoption,
external dispatch, vault mutation, publication or commit/push.
