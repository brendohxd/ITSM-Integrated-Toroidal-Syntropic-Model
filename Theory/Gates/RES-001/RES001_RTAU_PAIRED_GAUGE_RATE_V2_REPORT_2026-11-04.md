# Paired initial gauge-rate map and controlled remainder

4 November 2026. Component of the acknowledged-High actual-rate bundle,
following the [canonical velocity rows](RES001_RTAU_CANONICAL_VELOCITY_REMAINDER_V1_REPORT_2026-11-04.md).
R-tau UNADOPTED; original R4C1 unchanged; review DEFERRED;
physics_pass=false; gate_effect=NONE; G1-G6 INCOMPLETE.

## Result and remaining boundary

The actual periodic spatial-gauge correction now has a local field-rate
projector plus an H1-bounded finite-rank/primitive remainder. It is paired
with the canonical covector-density momentum correction and an independently
verified scalar response for the auxiliary force variable. Metric-modulus
rates and independent harmonic coordinate velocities remain explicit.

The input is the affine field rate in the existing adapted coordinate.
Its strong-state principal comparison is still required. This result does
not assemble the full generator, transport the physical-variable map, or
prove a time-dependent energy inequality or compatible background tube.

## Exact field map

Use the existing initial adapted coordinate zeta with normalized period
2*pi, J=d zeta/dz=a/Abar and Abar=mean(a). It gives background metric
diag(a^2,a^2,Abar^2). No future conformal metric is imposed. The affine
field rate F is the existing pulled-back zero-correction rate with its
background coordinate drift retained. It has thirteen nonauxiliary rows.

Let W select metric slots hxz,hyz,hzz and let B be the actual spatial field
generator. Its metric entries in these rows are

    g=(a^2,a^2,2*Abar^2), B[metric_i,i]=g_i,
    B[V_i,i]=-Vbar_z.

Other B entries vanish on this initial planar background. Put u_i=1/g_i,
N=B*diag(u), Pi=I13-N*W. Then W*N=I3, W*Pi=0 and Pi^2=Pi. Pi has rank
ten: it enforces three spatial gauge conditions. Matrix shape does not
prove that thirteen independent physical directions survived. The original
physical constraint chart and its mode requirements remain authoritative.

With b=W*F, the actual periodic equations and constants are

    b_i+g_i*D_zeta xi_i=c_i,
    c_i=mean(u_i*b_i)/mean(u_i),
    xi_i=H_i+P[u_i*(c_i-b_i)].

P is the mean-free periodic primitive in zeta; H_i are independent harmonic
coordinate velocities. The c_i are the physical metric-modulus rates.
Their means are not set to zero. The exact corrected field rate is

    F_corrected=Pi*F+N*c+qbar_zeta*xi_z.

Since the three gauge-fixed background metric entries have zero spatial
derivative, W*F_corrected=c. The finite-rank term restores those physical
modulus rates. This is the actual coordinate correction, not a repeated
projection onto a desired physical slow graph.

## Continuum estimates

Set L=||F||L2 and H=|harmonic coordinate velocity vector|. Let
rho=max_i ||u_i||infinity/mean(u_i), u0=max_i||u_i||infinity and
Q1=||qbar_zeta||infinity+||qbar_zeta,zeta||infinity. Then

    |c|<=rho*L,
    ||xi_zeta||L2<=u0*(rho+1)*L,
    ||xi||H1<=H+sqrt(2)*u0*(rho+1)*L,
    ||F_corrected-Pi*F||H1
       <=[(||N||infinity+||N_zeta||infinity)*rho
                       +Q1*sqrt(2)*u0*(rho+1)]*L+Q1*H.

The all-integer-mode inequality ||P||L2->H1<=sqrt(2), coefficient product
rule and norm-one averaging prove these estimates. Certified profiles give
Abar in [exp(-r),exp(r)], r=1/13000, and rho<=exp(4r). All coefficient
derivatives are converted to zeta with the actual J. Conservative bounds are

    ||Pi||L2->L2 <2.732050808,
    ||F_corrected-Pi*F||H1 <=1.734987787*L+0.000837323*H,
    ||xi||H1 <=2.829297578*L+H,
    |c|<=1.000307740*L.

Norms here are normalized adapted-coordinate Bessel norms. These constants
are initial coefficient controls, not physical growth rates or cutoffs.

## Paired momentum and auxiliary response

The adapted canonical background momentum is pbar_j=p_j/(J*Tq_j), using
the existing field pullback Tq. This Jacobian is retained for every row.
With K_i,j=partial(B[:,i])/partial(q_j) dotted with pbar, its exact response is

    correction_pj=xi_z*D_zeta pbar_j
                  +sum_i(delta_iz*pbar_j-K_i,j)*D_zeta xi_i.

The second term includes the canonical field-index response. For example a
contravariant frame component's dual response has a second xi_zeta*p term;
scalar-density transport alone would miss it. Cached momenta/spatial
derivatives and the actual Jacobian give

    ||correction_p||L2 <=6.861426203*L+0.015441238*H.

For the auxiliary scalar Z=-Delta_h psi, the full metric AND clock variation
gives exactly correction_Z=xi_z*D_zeta Zbar. This identity is checked for
arbitrary longitudinal displacement and variable diagonal metric
diag(a^2,a^2,b^2); the planar transverse corrections vanish. Thus it does
not follow by taking two unproved derivatives of a clock velocity estimate.
Actual initial Z derivatives give

    ||correction_Z||H1 <=0.002387197*L+0.000843742*H.

These statements concern the gauge contribution. They do not supply the
remaining affine force row, its mixed-order cancellations or a full rate
bound for the physical force sector. The density normal-form and original
global range/charge requirements are inherited, not silently replaced.

## Evidence, preservation and next work

[Executable V2](../../../Analysis/MasterTests/test_rtau_paired_gauge_rate_v2.py),
[V1 criteria](RES001_RTAU_PAIRED_GAUGE_RATE_V1_SPEC_2026-11-04.md),
[V2 clarification](RES001_RTAU_PAIRED_GAUGE_RATE_V2_SPEC_2026-11-04.md),
[receipt](../../../Analysis/MasterTests/outputs/rtau_paired_gauge_rate_v2_20261104/receipt.json).
15/15 component controls and byte-identical replay COMPLETE. Exact controls
include the projector/rank identities, nonconstant periodic correction with
nonzero means, scalar Laplacian covariance, the dual frame-index response
and all-harmonic primitive inequality. Bounds use cached whole-root
background momenta and certified initial profile jets; no Hessian is rerun.
Source bytes, sidecars and timestamps remain preserved. These are same-author
controls; independent Rule-9 review remains DEFERRED.

V1's 14/14 source/specification/receipt remain. Its projector-shape check
was labelled as retaining thirteen directions, which shape alone cannot
establish. V2 corrects that label and explicitly checks rank ten alongside
the restored modulus rates. No equation, estimate or acceptance threshold
changed. No removal of physical modes is inferred from this gauge matrix.

NEXT: compose the affine canonical velocity, coordinate drift and strong
configuration/momentum lifts with this paired map. Compare against the
registered principal operator in the same variables. Assemble remaining
momentum/force rates and moving Green/range/physical-variable maps before
claiming a full actual-generator remainder. Then T_dot/H_dot and a genuine
background tube are still required for finite-time evolution.
Goal ACTIVE; High remains acknowledged for the unfinished rate bundle.
No action adoption, matching input, publication, paper/site promotion,
vault mutation, model dispatch or Git delivery occurred.
