# Prepared R-tau slice: compatible spatial gauge and velocity pullback

31 October 2026. Claim Conditional; review DEFERRED.
physics_pass=false; gate_effect=NONE. R-tau remains unadopted.

## Result and boundaries

The certified periodic initial data admit an explicit orientation-preserving
spatial coordinate change to a useful nonzero-mode gauge. Its time-dependent
velocity transformation preserves the extrinsic curvature, scalar normal
velocities, independent frame, auxiliary spatial operator, lapse constraint
and global charge measures. The certified root uncertainty is carried through
the map with an explicit bound, not discarded in favour of the displayed centre.

This completes the initial gauge/kinematic sub-bundle of the
[prepared-Cauchy contract](RES001_R4C1_RTAU_PREPARED_CAUCHY_V1_CONTRACT_2026-10-31.md),
under the [frozen gauge specification](RES001_R4C1_RTAU_SPATIAL_GAUGE_V1_CONTRACT_2026-10-31.md).
It does NOT derive the physical reduced kinetic/symplectic operator, actual
initial accelerations or future gauge/constraint tangency. No healthy
nonlinear time evolution or interaction/window claim follows.

## Periodic coordinate map on the actual initial metric

The prepared metric is h=exp(2*lambda(z))*I, lambda=a*cos(z),
a=epsilon/13=1/13000. Let

    Abar=average(exp(lambda)),
    zeta(z)=integral_0^z exp(lambda(s)) ds/Abar,
    J=d_z zeta=exp(lambda)/Abar.

J is strictly positive and zeta(z+2*pi)=zeta(z)+2*pi. This is a diffeomorphism
of the same torus cycle, not a change in topology, physical length or matter
clock. The initial metric in (x,y,zeta) is

    h_new=diag(exp(2*lambda(z)),exp(2*lambda(z)),Abar^2),
    d_zeta(h_i,zeta)=0.

The homogeneous metric components are retained. In particular Abar^2 is
not set to one, and the zero modes of the mixed components remain physical
moduli in the later variational problem, although zero for this preparation.

Use the ACTUAL initial lambda_dot=H+epsilon*cos(2z)/31. Define

    R2=average(exp(lambda)*cos(2z))/Abar,
    m=Abar_dot/Abar=H+epsilon*R2/31,
    w=zeta_t/J
      =exp(-lambda)*epsilon/31
          *integral_0^z exp(lambda(s))*(cos(2s)-R2) ds.

The uniform H term cancels from w exactly. The drift is periodic and odd;
w_z=lambda_dot-m-lambda_z*w. These relations depend only on the initial
metric and its first time jet. They do not assume that future equations
preserve the conformal metric ansatz or the prescribed velocity shapes.

## Values, velocities and shift must transform together

For a scalar f,

    f_new=f_old, d_zeta f_new=f_z/J,
    f_new_dot=f_old_dot-w*f_z.

The lapse is scalar, N_new=N, N_new,zeta=N_z/J. The ADM shifts obey

    S_new,zeta=J*(S_old,z-w), S_new,x,y=S_old,x,y,
    d_zeta S_new,zeta=S_old,z_z-w_z+lambda_z*(S_old,z-w).

Here S_old,z denotes the longitudinal shift VALUE; the final subscript _z
on S_old,z_z denotes its derivative. Reusing untransformed coordinate
velocities with this new shift is incorrect and fails the rejection control.

The spatial frame variables in the actual action are contravariant slice
components V^i. Their transformations include

    V_new,zeta=J*V_old,z, V_new,x,y=V_old,x,y,
    V_new,zeta_dot=J*(V_old,z_dot-w*V_old,z_z+w_z*V_old,z),
    V_new,x,y_dot=V_old,x,y_dot-w*V_old,x,y_z.

The last w_z term is required by the time-dependent vector transformation.
The full unit frame U=gamma*n_clock+V transforms as a vector; its slice norm
and gamma are unchanged. Independent frame components are not identified
with the matter-clock normal.

For the initial metric,

    h_new,xx_dot=2*h_xx*(lambda_dot-w*lambda_z),
    h_new,yy_dot=2*h_yy*(lambda_dot-w*lambda_z),
    h_new,zeta,zeta_dot=2*Abar^2*m.

Mixed metric values and velocities are zero on this prepared slice. Thus the
initial gauge and its velocity conditions hold. In subsequent variations
all physical metric amplitudes and homogeneous moduli must be retained;
neither transverse equality nor these initial shapes are a time-evolution
restriction. Auxiliary Z time tangency also remains to be derived from the
actual evolution, rather than inferred from an arbitrary unused velocity slot.

## Exact geometric and charge preservation

The identities w_z=lambda_dot-m-lambda_z*w and J_z=J*lambda_z give

    K_new,xx=K_old,xx, K_new,yy=K_old,yy,
    K_new,x,zeta=K_old,x,z/J,
    K_new,y,zeta=K_old,y,z/J,
    K_new,zeta,zeta=K_old,zz/J^2.

Scalar normal velocities (f_dot-S^z*f_z)/N are unchanged. The frame norm
and contraction n.partial(psi) are unchanged, so a coordinate choice does
not remove a physical force or an instability.

For the new metric,

    Delta_new psi=1/(exp(2lambda)*Abar)
       *d_zeta(exp(2lambda)/Abar*d_zeta psi)
       =exp(-2lambda)*(psi_zz+lambda_z*psi_z)=Delta_old psi.

The exact auxiliary Z=-Delta psi is therefore preserved. The volume relation
sqrt(h_new)*J=sqrt(h_old) preserves the clock charge measure. For scalar
condensate momenta pi_new=pi_old/J, hence the U(1) charge integral is also
preserved. The lapse Euler density transforms as E_N,new=E_N,old/J and
rho remains a scalar. These are coordinate statements for the complete
constraint data, not a new solution fit. The initial-constraint existence
result and its positive density are transported to the new coordinates.

Boundary-dependent ADM curvature densities are not required to agree
pointwise: their spatial integration-by-parts terms differ by a divergence.
The actual lapse Euler flux is retained in the covariance test. This is
why a density-only comparison with that flux dropped would be insufficient.

## Gauge operator and uniform root-uncertainty bounds

At this initial metric, infinitesimal planar coordinate generators have

    delta G_x=d_zeta(h_xx*d_zeta xi_x),
    delta G_y=d_zeta(h_yy*d_zeta xi_y),
    delta G_z=2*Abar^2*d_zeta^2 xi_z,
    G_i=d_zeta(h_i,zeta).

After quotienting constant translations, the negative of this operator
has quadratic form integral(h_xx*|xi_x'|^2+h_yy*|xi_y'|^2+
2*Abar^2*|xi_z'|^2). The mean-free 2*pi-circle Poincare inequality gives
positive spectral gaps at least exp(-2a), exp(-2a), 2*exp(-2a).
This establishes a nonsingular infinitesimal coordinate gauge at the slice.
It is not the indefinite physical shift constraint matrix and does not
claim a positive physical Hamiltonian or a future nonlinear gauge theorem.

Since exp(-a)<=Abar<=exp(a),

    exp(-2a)<=J<=exp(2a),
    |w|<=2*pi*(epsilon/31)*exp(2a),
    |w_z|<=2*epsilon/31+a*sup|w|.

The stored bounds give J>0.9998461, J<1.0001539,
|w|<0.000202715 and |w_z|<0.000064532.
They are control-coordinate bounds, not observed cosmological quantities.

The map and w are independent of the uncertain H/omega/root shift. For a
shift difference, transverse pullback gives derivatives delta S_z/J and
(delta S_zz-lambda_z*delta S_z)/J^2. Longitudinal pullback J*delta S gives
derivatives delta S_z+lambda_z*delta S and
(delta S_zz+lambda_z*delta S_z+lambda_zz*delta S)/J.
Thus a sufficient transformed C2 norm factor is

    M=exp(4a)*(1+2a)<1.000462.

The certified root displacement <1.139e-5 becomes <1.140e-5 in these
coordinates. H and omega are unchanged as continuation parameters; all
velocity changes shown above are carried with them. Physical scalar density
and charges retain their certified values/bounds. This applies to every
root in the preceding certificate, not only the numerical centre.
These root variations leave the prescribed metric profiles fixed. General
physical metric perturbations require the actual gauge-projector and
Jacobian variations; this M is not a universal perturbation/symplectic bound.

## Verification and next requirement

[Executable](../../../Analysis/MasterTests/test_01_r4c1_rtau_spatial_gauge_v1.py),
[fresh receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_spatial_gauge_v1_attempt_01/summary.json):
30/30, no failed/unknown checks; exact recomputing read-only replay.
SHA256 449ce6a63c04a479fb8fc79cee62806ba5072d8dacac99f8614e9ab96e9ce014.
Exact symbolic identities are supplemented by original full-action lapse
Euler and condensate momentum covariance controls at 100 digits; normalized
errors are below 1.100e-100 and 1.429e-101 respectively. Arc normalization,
weighted mean and periodic drift are checked with independent quadrature.
Interval endpoint tuples retain the uniform uncertainty/gauge-gap bounds.
All source and sidecar bytes/mtimes are preserved. These controls do not
constitute independent external peer review.

Next derive the actual unreduced and gauge-reduced quadratic/symplectic
and initial-acceleration operators on the prepared inhomogeneous data.
Include both perturbation parities, all homogeneous metric modes, global
momentum/charge tangents, root uncertainty and lapse/shift/auxiliary drift.
Do not import the old homogeneous propagator or assume initial conformal
shapes remain invariant. Physical signatures, characteristic evolution,
nonlinear persistence, interactions/window and matching remain unresolved.
Original G1-G6 incomplete; no canonical action adoption, manuscript/site edit,
publication, dispatch, vault mutation or commit/push. Goal ACTIVE.
