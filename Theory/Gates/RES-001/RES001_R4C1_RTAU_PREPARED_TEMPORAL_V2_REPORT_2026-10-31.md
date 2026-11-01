# Prepared R-tau slice: unreduced temporal operator

31 October 2026. Conditional comparison result; review DEFERRED.
physics_pass=false; gate_effect=NONE. R-tau is not an adopted parent action.

## What has been established

The full prepared-data temporal Hessian has been derived before spatial
constraint/charge reduction. On the registered initial slice, including
every root in the preceding existence certificate, its fourteen retained
rate coordinates have inertia **12 positive, one negative, one zero**.
The zero coordinate is the auxiliary Z rate; the negative direction belongs
to the unreduced gravitational/conformal block. This is not a physical ghost
verdict: the actual gauge, momentum and global-charge reduction is still open.

The thirteen nonauxiliary temporal rates have a nonsingular Legendre map
with an explicit uniform normal-rate gap. This is a useful prerequisite
for constructing the actual evolution operator; it does not prove that
the spatially constrained operator is positive or that evolution is well posed.

Owner: [prepared-Cauchy contract](RES001_R4C1_RTAU_PREPARED_CAUCHY_V1_CONTRACT_2026-10-31.md).
Immediate input: [prepared spatial gauge](RES001_R4C1_RTAU_SPATIAL_GAUGE_V1_REPORT_2026-10-31.md),
which retains the [continuum initial-constraint certificate](RES001_R4C1_RTAU_PERIODIC_INVERSE_V1_REPORT_2026-10-31.md).
The [temporal contract](RES001_R4C1_RTAU_PREPARED_TEMPORAL_V1_CONTRACT_2026-10-31.md)
was frozen before execution. All six metric rates and three independent
frame rates are retained. Neither perturbation parity nor any homogeneous
metric component has been removed. Initial reflection symmetry concerns the
prepared background only, not the admissible perturbation space.

## Rate coordinates and the full metric/frame block

At a point choose an orthonormal spatial basis. Let K be the symmetric
extrinsic-curvature rate and X the orthonormal components of the independent
normal frame rate entering the original density. The latter is the
normal/Lie coordinate rate in that density, not the time derivative of
components in a moving orthonormal basis; the covariant frame acceleration
also contains K*V. Use Frobenius-normalized K coordinates: off-diagonal
entries of K are their corresponding coordinates divided by sqrt(2).

These are invertible changes of instantaneous rate coordinates, with
positive lapse and spatial metric. The nine-dimensional Hessian comes
directly from the unspecialized candidate density, not a B1 matrix with
new coefficients substituted. Spatial derivatives and background rates
enter affine/lower-order pieces but do not change this metric/frame
temporal Hessian. Spatial rotations act orthogonally on symmetric tensors
and vectors in these normalized coordinates.

Align V locally with the third axis, V=(0,0,w), solely to describe the
pointwise matrix. This is not a restriction on physical frame components,
a global spatial coordinate change, or permission to omit the derivatives
of this basis in the later spatial/evolution operator. The exported matrix
has one singleton K_xy eigenvalue 1; two identical blocks on (K_xz,X_x)
and (K_yz,X_y); and a scalar block on (K_xx,K_yy,K_zz,X_z).

The two-dimensional vector block is

    [(w^4+5*w^2+15)/15, sqrt(2)*w*(w^2+5)/30]
    [sqrt(2)*w*(w^2+5)/30, (w^2+5)/30].

Its determinant is (w^2+5)/30>0. The scalar determinant is

    -11*(2*w^2+3)/(90*(1+w^2)).

The full nine-dimensional determinant is

    -11*(w^2+5)^2*(2*w^2+3)/(81000*(1+w^2)).

These exact algebraic identities also have no finite real-tilt zero. This
observation concerns this unreduced temporal block only. At w=0 its
eigenvalues are 1 (five), -11/5 (one), 1/6 (three).

For |V|<=1e-4 an outward interval row-norm bound on M(V)-M(0), combined
with symmetry, gives minimum absolute eigenvalue greater than

    0.16662666599 > 0.16.

The inertia is therefore eight positive and one negative throughout this
domain. Rotation preserves this statement for arbitrary frame orientation.
The raw endpoint enclosures and the complete exact matrix are in the receipt.

## Condensate/reservoir and full force contribution

Write c=|V|^2, gamma=sqrt(1+c), s=n_clock.partial(psi), and
g=orthonormal longitudinal spatial derivative of psi. With
j=(v,-u,0), the canonical u/v/r temporal block is

    I_3-zeta*c*j*j^T.

Its least eigenvalue is at least 1-zeta*c*(u^2+v^2). The full force term,
including the norm-cubed contribution, has temporal coefficient

    K_Q*(1+c)-3*A*(c*q+b^2/q),
    q^2=c*s^2+2*gamma*Vz*s*g+(1+Vz^2)*g^2,
    b=c*s+gamma*Vz*g.

For q>0, the exact identity

    c*q^2-b^2=(c-Vz^2)*g^2 >= 0

gives 0<=3*A*(c*q+b^2/q)<=6*A*c*q. The upper bound tends to
zero at q=0, giving the continuous C2 Hessian there. No C3 expansion or
adopted A=0 action is used. A stable boosted-rest-vector norm is used in
the numerical control rather than subtracting nearly equal temporal terms.

The registered diagnostic parameters remain K_Q=3, A=2/7, zeta=1/13.
They are assumed coefficients, not new microscopic matching information.
On c<=1e-8, |g|<=1e-4, |s|<=0.3, u^2+v^2<=1.001,

    q <= sqrt(1+c)*|g|+sqrt(c)*|s|,
    force coefficient > 2.99999999999777,
    least canonical eigenvalue >= 0.99999999923.

The exact fixed profiles and the certified shift ball satisfy these bounds
on the whole circle. The force normal rate uses the actual uncertain shift
through s=(psi_dot-S^z*psi_z)/N; it is not replaced by the centre value.
The prepared normal/frame profiles themselves are fixed in the certificate,
and its lapse is positive. Thus the bounds cover every certified root,
not merely a few sampled points. The auxiliary clock-regulator has no Z_dot
term after exact cancellation, so its conjugate momentum is zero.

The conformal initial metric is only used to evaluate the actual prepared
slice and its rate conversion. All six rate variations remain independent;
future solutions are not projected onto a conformal metric or prescribed
velocity profile. The previously justified spatial gauge and these local
orthonormal rate coordinates describe the same slice. Neither replaces the
as-yet uncomputed gauge-projector derivatives for general metric variations.

## Controls, failed versions and reproducibility

[Temporal executable V2](../../../Analysis/MasterTests/test_01_r4c1_rtau_prepared_temporal_v2.py):
**26/26**, no failed/unknown checks, exact recomputing read-only replay.
[Receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_prepared_temporal_v2_attempt_01/summary.json)
SHA256 aba30848eed3be2d4cb3f0122899ea0394aafcf93b6ebd4d91ecfb3b63f6ac93.

An independent calculation of the full original-density velocity Hessian
uses reverse AD with two complex-step sizes, 1e-18 and 1e-24, at prepared
z=0.3,1.1,2.4 and 100-digit precision. After the explicit coordinate-rate
congruence, errors are below 3.882e-50 and 3.882e-62. Full Z momentum/null
tests and rejection of omitted force Hessians pass. These point controls
supplement the analytic and interval proof; they do not replace its domain.

[Block/endpoint audit V2](../../../Analysis/MasterTests/audit_01_r4c1_rtau_prepared_temporal_v2.py):
**15/15**, exact recomputing read-only replay.
[Audit receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_prepared_temporal_audit_v2_attempt_01/summary.json)
SHA256 a7e029cdcc3d5d3ffc8f1b9e27d97ada9a8366580af5f54193795fbc7854c309.
It checks the different block determinant calculation, all 81 binary
interval pairs, the inverse-gap bound and the force Cauchy identity.
It is a same-author control audit, not independent external peer review.

Preserved failures:

- Temporal V1 was 24/26. Python division introduced Float(1.0) into the
  exact symbolic rotation basis. The [V2 repair specification](RES001_R4C1_RTAU_PREPARED_TEMPORAL_V2_SPEC_2026-10-31.md)
  replaces that test constant with an exact integer and directly encloses
  [-1,1]/10000. Equations, variables and thresholds are unchanged.
- Audit V1 was 11/15. Three structural expression comparisons needed exact
  simplification; one coefficient list omitted zero odd-power coefficients.
  The [audit V2 specification](RES001_R4C1_RTAU_PREPARED_TEMPORAL_AUDIT_V2_SPEC_2026-10-31.md)
  documents those repairs. Both failing sources/receipts remain pinned.

## Consequence and next work

The initial-data continuation has a controlled, invertible nonauxiliary
temporal block. The candidate has not acquired a new temporal singularity
on this certified slice. This is progress toward the prepared Cauchy
operator; it is not an extension of the old homogeneous evolution estimate.

Next derive the full spatial momentum/gauge/charge tangent reduction and
actual initial accelerations, including all homogeneous modes, both
perturbation parities, the lapse and auxiliary Euler fluxes, changed clock
exchange, uncertain root and time-dependent basis/projector drift. The
negative raw conformal direction must be assessed only in that reduction.
Physical signatures, characteristics, nonlinear constraint persistence,
coupled interactions and a physical validity window remain unresolved.

No concrete correction to P1/P2, Thermodynamics or the original R4C1 paper
follows from this unadopted-action temporal prerequisite. No manuscript
sweep, external dispatch, vault mutation, publication or commit/push was
performed. Original G1-G6 remain incomplete; matching inputs remain missing.
