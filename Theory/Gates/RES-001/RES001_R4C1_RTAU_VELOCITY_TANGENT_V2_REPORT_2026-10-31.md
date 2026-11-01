# Prepared R-tau slice: constraint-tangent velocity form

31 October 2026. Conditional comparison calculation; review DEFERRED.
physics_pass=false; gate_effect=NONE. R-tau remains unadopted.

## Result and exact scope

The temporal Hessian form is uniformly positive on the fixed-field velocity
tangents satisfying the actual projected momentum equations and the declared
two fixed global charges. The bound covers every root of the certified
initial-data ball and every planar circle harmonic, with both real parities.
No finite perturbation band or evolving conformal ansatz is imposed.

In the normal-rate convention defined below, the Hessian form obeys

    E(W) > 0.024 * average(|W|^2)

on this kernel. The quadratic temporal Lagrangian contribution is E/2.
This is a normalization-dependent control constant, not an observable or a
physical Hamiltonian bound. The extra global longitudinal momentum equation
is retained: imposing it further restricts this positive subspace.

This explains why the preceding raw negative conformal direction does not
by itself prove a physical ghost. It does NOT establish the full physical
symplectic form, principal evolution, initial accelerations, constraint
persistence, general three-dimensional perturbations, interactions or a
physical validity window. The result is an instantaneous, fixed-spatial-field
velocity-tangent statement in the registered planar problem.

Owner: [prepared-Cauchy contract](RES001_R4C1_RTAU_PREPARED_CAUCHY_V1_CONTRACT_2026-10-31.md).
Inputs: [temporal V2](RES001_R4C1_RTAU_PREPARED_TEMPORAL_V2_REPORT_2026-10-31.md),
[initial-root existence](RES001_R4C1_RTAU_PERIODIC_INVERSE_V1_REPORT_2026-10-31.md),
and [prepared spatial gauge](RES001_R4C1_RTAU_SPATIAL_GAUGE_V1_REPORT_2026-10-31.md).
The [tangent contract](RES001_R4C1_RTAU_VELOCITY_TANGENT_V1_CONTRACT_2026-10-31.md)
was frozen before execution. The calculation does not change the action,
fixed clock charge 1/5, U(1) charge 1, microscopic inputs or earlier failures.

## Actual variable-coefficient momentum operator

Work in the original periodic z coordinate of the prepared initial slice,
h=a(z)^2 I, ell=lambda_z, a=exp(lambda). This is solely the evaluation
slice; all six metric rates remain independent. Let W denote variations
of the thirteen normal rates in the order K6/frame3/u/v/r/psi, with
Frobenius-normalized K entries as in the temporal owner. Auxiliary Z has
zero momentum and its secondary relation Z=-Delta psi remains required;
no independent kinetic norm for Z is asserted.

For a planar coordinate generator xi(z), the rate variation it produces
is (B*xi_z+A*xi)/N. The nonzero entries of B are

    B[K_xz, x]=1/sqrt(2), B[K_yz, y]=1/sqrt(2), B[K_zz, z]=1,
    B[frame_i, i]=-V_z.

Only A's z column is nonzero:

    A[K_xx,z]=A[K_yy,z]=A[K_zz,z]=ell,
    A[frame_i,z]=V_i,z-ell*V_i,
    A[u/v/r/psi,z]=u_z/v_z/r_z/psi_z.

Here V denotes orthonormal components of the independent spatial frame.
The ell terms in its Lie rate are essential. With M the full normal-rate
temporal Hessian and P=a^3*M*W, the fixed-field momentum tangent is

    (B^T*P)_z-A^T*P=0.

Let P0 subtract the circle mean and Dinv be the zero-mean antiderivative,
whose L2 norm is at most one by its Fourier multipliers 1/(ik), |k|>=1.
The equivalent split conditions are

    P0(B^T*P)-Dinv*P0(A^T*P)=0,
    average(A^T*P)=0.

The second condition is NOT solved by the first. Its transverse components
vanish identically in this planar geometry; its longitudinal component
remains an additional global condition. Positivity below is first proved
on the larger projected kernel, so it remains true on any further subset
satisfying the mean equation. The global condition is not discarded or
replaced by a reflection restriction on perturbations.

## Clock and phase tangents retain the lapse flux

The reconstructed clock charge is integral(E_N/C). Because N=1/C and
N_z/N=-beta*psi_z, integration by parts gives its integrand

    N*(L_N+(N_z/N)*L_Nz).

It equals L-p.(v-Lie_S q) for the nonmatter density. This uses simultaneous
lapse/gradient scaling; the Euler flux has not been omitted. Let Wbar be
the normal-rate image of v-Lie_S q at the actual prepared root. In its frame
components it excludes the lapse-acceleration offset already affine in the
full rate. The fixed-field global charge tangents are

    delta I = -average(N*a^3*(M*Wbar).W),
    delta Q =  average(a^3*(M*j).W),  j[u]=-v, j[v]=u.

Their zero values implement the declared ensemble. They are not a new
assumption of pointwise charge constancy. Density perturbations remain
reconstructed from the lapse Euler equation. Fixed-field tangents are
only one part of the later full field/momentum constraint graph.

## Reference kernel and continuum perturbation proof

The reference temporal matrix M0 has norm 3. Its metric block is I minus
(16/15) times the trace outer product; its frame block is I/6 and its
u/v/r/psi block is diag(1,1,1,3). This is the exact zero-tilt limit of the
fresh unspecialized operator, not an imported evolution generator.

Normalize the three nonzero-mode momentum rows to

    W_xz, W_yz, (W_zz+16*(W_xx+W_yy))/sqrt(513).

For the means use the Q row and (I+Q)/L, where

    H0=sqrt(3469/4620),
    L^2=3*(11*H0/5)^2+1/16+9/25.

These global rows are orthonormal; the projected rows act on mean-zero
functions and are orthogonal to them in the Hilbert direct sum. Thus the
reference map C0 satisfies C0*C0^*=I and its orthogonal kernel projection
is P_ref=I-C0^*C0. Mean metric modes have not been deleted.

For a nonzero-mode transverse trace/difference (a,d), the allowed metric
rate vector has squared norm 513*a^2+d^2 and metric form 33*a^2+d^2.
The remaining directions are positive. For the means, Q fixes the mean
phase rate; I+Q determines the conformal rate from reservoir/force rates.
A Cauchy bound gives mean scalar/metric ratio at least 139623/158551;
including the frame, the mean gap is at least 1/6. Hence on ker C0 a
conservative all-harmonic gap is lambda0=1/20, less than 11/171 and 1/6.

For the ACTUAL variable-coefficient map C, outward/analytic bounds give

    ||C-C0|| <= delta < 0.004179,
    ||N*a^3*M-M0|| <= e < 0.000813,
    constraint right-inverse norm < 1.004197.

Specifically C*C0^* differs from I by at most delta<1, so
C0^*(C*C0^*)^-1 is a bounded right inverse. This is a continuum L2
statement, not a finite-grid inverse. For C*W=0,

    ||(I-P_ref)W|| <= delta*||W||.

Using ||M0||=3, the actual Hessian form is bounded below by

    [lambda0*(1-delta^2)-6*delta-3*delta^2-e]*||W||^2
      > 0.02406104302456*||W||^2.

The 32 interval cells enclose coefficient functions and the uncertain
prepared rates over the entire circle. They do not restrict W's Fourier
support or parity. The known background departure from the homogeneous
rates is bounded by 0.003375; it is fully included in the clock-row bound.
The much smaller certified root uncertainty contributes less than
0.000032219 to the normal-rate vector. These are different quantities.

This establishes a controlled positive velocity form on the projected
constraint/charge kernel. The remaining mean momentum equation may
restrict it further. Higher spatial regularity, the full field-dependent
constraint graph and the symplectic/gauge quotient still require work.

## Checks, preserved failure and interpretation

[Executable V2](../../../Analysis/MasterTests/test_01_r4c1_rtau_velocity_tangent_v2.py):
22/22, no failed/unknown checks, exact recomputing read-only replay.
[Receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_velocity_tangent_v2_attempt_01/summary.json)
SHA256 f4efb6bc588528aa6287fa2cca2a8020f581fddc0564e0336b9e8bf52906a814.
Full-density lapse/phase and shift/shift-gradient mixed derivatives at
three prepared points and two complex-step sizes agree with the derived
maps. The clock Noether integrand agrees to better than 1.108e-100 at
100 digits. The Hessian serialization limits derivative comparison to
roughly 50 digits; the actual frozen tolerances remain 1e-28 and 1e-40.

[Audit](../../../Analysis/MasterTests/audit_01_r4c1_rtau_velocity_tangent_v1.py):
16/16, exact replay.
[Audit receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_velocity_tangent_audit_v1_attempt_01/summary.json)
SHA256 f12a29d0cc5e9e13218ffa38c97a43ddca035fc83fb70e5af99a7e2907e5e115.
It independently reconstructs the norm/coercivity inequalities from raw
binary endpoints, retains a nonzero mean metric/reservoir tangent, and
exhibits negative reference directions when either the mean clock charge
or nonzero momentum condition is omitted. Same-author controls are not
independent external scientific review.

V1 is preserved at 20/21. I added an unjustified precheck that the TOTAL
departure from the homogeneous reference be <0.001. The prepared shift
already exceeds that scale. The [V2 specification](RES001_R4C1_RTAU_VELOCITY_TANGENT_V2_SPEC_2026-10-31.md)
separates the full background departure from the actual root uncertainty.
The total departure used in all operator inequalities is unchanged. The
scientific acceptance thresholds, action, ensemble and equations are
unchanged; V1's incorrect precheck is not retrospectively certified.

Next derive the mixed field/velocity quadratic and symplectic operators,
full constraint/gauge tangents and actual initial accelerations, with the
mean momentum equation, projector/basis drift, auxiliary relation, lapse
flux, root uncertainty and generated harmonics retained. General transverse
spatial wavevectors on this inhomogeneous background remain uncomputed.
No nonlinear persistence or physical window follows from this result.

No concrete manuscript correction follows from this unadopted-action
prerequisite. P1/P2, Thermodynamics and the original R4C1 paper are unchanged.
G1-G6 remain incomplete; matching coefficients remain unidentifed. No
action adoption, external dispatch, vault mutation, publication or commit/push.
