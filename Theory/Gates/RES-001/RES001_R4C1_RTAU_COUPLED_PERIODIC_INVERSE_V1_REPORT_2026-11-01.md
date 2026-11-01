# Prepared R-tau coupled periodic canonical inverse

1 November 2026. Conditional comparison; review DEFERRED.
physics_pass=false; gate_effect=NONE; R-tau unadopted; G1-G6 incomplete.

## Result and exact scope

The coupled INITIAL linear momentum/current-density graph now has a bounded
periodic inverse on its explicitly compatible source range, throughout the
certified initial-root ball. The momentum equations are solved first and
substituted into the complete density operator, including lower-order and
nonlocal terms. This is stronger than the previous principal trace check.
It is not a scalar trace inversion at fixed unrelated momenta.

The perturbation contraction bound is <0.534224, strictly below one.
The scalar trace inverse has L2-to-H2 norm <7.970 for its assembled right
side. Including the momentum sources and retained momentum means, a
conservative bound for trace H2 plus all three eliminated-momentum H1
norms is <41.662 in the declared control units and data norm below.

The remaining longitudinal compatibility is explicit; arbitrary source
data do not satisfy the full momentum system automatically. Its range
contains an infinite family of gauge-invariant cross-metric initial
perturbations, not merely coordinate directions. No parity or finite-band
restriction is imposed on general data. Torus moduli and momentum means
remain present. Clock and U(1) charge tangents remain global conditions.

This is NOT a physical evolution norm, transported symplectic quotient,
finite-time domain theorem or interaction window. The original unchanged
R4C1 action and its failures remain distinct from this R-tau comparison.

Owner: [prepared-Cauchy contract](RES001_R4C1_RTAU_PREPARED_CAUCHY_V1_CONTRACT_2026-10-31.md).
Immediate input: [canonical density graph](RES001_R4C1_RTAU_CANONICAL_DENSITY_GRAPH_V2_REPORT_2026-11-01.md),
using the [mixed operator](RES001_R4C1_RTAU_MIXED_OPERATOR_V4_REPORT_2026-11-01.md)
and [initial principal calculation](RES001_R4C1_RTAU_PREPARED_PRINCIPAL_V3_REPORT_2026-11-01.md).
The [coupled-inverse contract](RES001_R4C1_RTAU_COUPLED_PERIODIC_INVERSE_V1_CONTRACT_2026-11-01.md)
was frozen before execution.

## Coupled operator, range and Green proof

Use the fixed pullback of the existing compatible spatial gauge. At the
prepared conformal initial metric h=a^2 I, the free harmonic metric
variations in the mixed/longitudinal slots pull back as J*c_x,J*c_y,J^2*c_z.
They are source data. The unknown trace is dhxx=dhyy=a^2*f. The remaining
configuration fields, free momenta and moduli all enter the sources below.
No conformal ansatz is imposed on future evolution or all perturbations.

Let p_x,p_y,p_z denote the three unknown canonical momentum perturbations
in slots h_xz,h_yz,h_zz. Let P=p_hxx+p_hyy be the BACKGROUND trace
momentum density, and lambda_z=a_z/a. Substituting this trace variation
into the full canonical momentum tangent gives

    (a^2*p_x+a^2*p_hxz*f)_z=s_x,
    (a^2*p_y+a^2*p_hyz*f)_z=s_y,
    (2*a^2*p_z)_z-(a^2)_z*p_z-P*(a^2*f)_z=s_z.

These retain the variations of the spatial generators. The transverse
sources are exact periodic derivatives, so their means vanish for the
actual source construction. Dinv is the zero-mean periodic antiderivative
and P0 removes the mean. On L2, ||Dinv*P0||<=1 for the entire circle;
no Fourier band or parity condition is used in the bound.

For the trace-dependent part at zero retained momentum means,

    T_x f=-p_hxz*f+a^-2*average(p_hxz*f)/average(a^-2),
    T_y f=-p_hyz*f+a^-2*average(p_hyz*f)/average(a^-2).

Their source parts include a^-2*Dinv(s_x/s_y), normalized to the prescribed
momentum means. Nonzero prescribed means are independent physical source
parameters; they are not set to zero by the inverse construction.

For the longitudinal equation put

    R=a/2*(lambda_z*P-P_z),
    W=Dinv*P0(R*f+s_z/(2*a)),
    p_z=P*f/2+W/a+C/a,
    C=[eta_z-average(P*f/2)-average(W/a)]/average(1/a).

Here eta_z is the retained original-coordinate mean of p_z. The remaining
EXACT compatibility condition is

    average(R*f+s_z/(2*a))=0.

The projected inverse does not make this condition automatic. Its solved
data satisfy the full longitudinal momentum equation if and only if the
displayed condition holds. This is the actual range condition, not an
additional physical prescription or a replacement by reflection symmetry.

Write T_z for the part of p_z depending on f at eta_z=s_z=0. The full
local canonical current-density row from its owning graph is

    A2*f_zz+A1*f_z+A0*f
       -Rvel_hxz*p_x-Rvel_hyz*p_y-Rvel_hzz*p_z=current_source.

The source includes all other fields/momenta, their actual derivatives,
auxiliary reconstruction and metric/momentum moduli. Thus the trace
operator to invert is the COUPLED operator

    L f=A2*f_zz+A1*f_z+A0*f
             -Rvel_hxz*T_x f-Rvel_hyz*T_y f-Rvel_hzz*T_z f.

It is not the scalar density row at unrelated fixed momenta. To compute
the coefficients directly, let F be the canonical lapse improvement from
the previous owner. On a trace variation,

    delta F=U0*f+U1*f_z,
    V0=a^2*(L_hxx+L_hyy)+(a^2)_z*(L_dhxx+L_dhyy)
         +P*S^z*(a^2)_z+a^2*(p_hxz*S^x_z+p_hyz*S^y_z),
    V1=a^2*(L_dhxx+L_dhyy+P*S^z),
    A0=V0-(U0)_z,
    A1=V1-U0-(U1)_z,
    A2=-U1=-N*a.

All derivatives of F here hold canonical momenta independent. Its
coefficient spatial derivatives include the actual background p_z and
the certified root's S_zz; no S_zzz estimate is needed by this operator.

## Reference inverse, including the mean block

At the zero-profile reference use the same action coefficients and
H0^2=3469/4620. The aether rest coefficient changes the metric trace
kinetic factor to cD=1+MU2*c2/MP2=16/15; c1+c3=0. Its inverse trace
factor is cD/(3*cD-1)=16/33. With pi=-11*H0/10,

    T_metric=2/volume*[tr((p*h)^2)-(16/33)*tr(p*h)^2],
    T_scalar=1/2*(1+1/16+3/25)=473/800.

The pinned potential gives rho0=1/5. For a nonzero trace mode the
momentum equation enforces delta p_hzz=pi*f. For the mean, its independent
momentum mean is retained, so the f-dependent part is pi*(f-average(f)).
Differentiating the same canonical Hamiltonian, not an old generator,
gives the reference density operator

    L0 f=-f_zz+(553/400)*P0(f)-(2263/8400)*average(f).

The negative mean eigenvalue is nonzero and must not be deleted or changed
to a positive mass. For normalized circle Fourier/Sobolev norms,

    ||f||_H2^2=sum_n (1+n^2)^2*|f_n|^2,
    ||L0^-1||_(L2 to H2)=8400/2263.

Indeed for every integer |n|>=1, (1+n^2)/(n^2+553/400)<=1; the mean
ratio is 8400/2263>1. This is an all-harmonic Green estimate, not a finite
matrix eigenvalue test. The nonzero reference mass differs from the
fixed-unrelated-momenta mass by 3469/2100.

## Actual-data perturbation bound

Let w0=1/a, w=w0/average(w0), and pi0=-11*H0/10. The exact longitudinal
map is (I-w*average)(P*f/2+w0*Dinv*P0(R*f)). Hence

    ||T_z-pi0*P0|| <= (1+||w||_infinity)
                        *(||P/2-pi0||_infinity
                           +||w0||_infinity*||R||_infinity)
                       +|pi0|*||w-1||_infinity.

The bounds a=exp(lambda), |lambda|<=1/13000 give explicit bounds for
w0,w,w-1 and a^-2/average(a^-2). Together with outward actual action
coefficient intervals, these bound every local and nonlocal term of L-L0.
For the first derivative, ||f_z||_L2<=||f||_H2/2. The second derivative,
zeroth derivative and mean projection have norm <=1 in these conventions.

If e bounds ||L-L0||_(H2 to L2) and q=(8400/2263)*e<1, the Neumann
argument gives an actual inverse with

    ||L^-1||_(L2 to H2) <= (8400/2263)/(1-q).

This is an initial-data linear inverse. It does not transport a physical
symplectic form or establish any time interval, characteristic symmetrizer
or nonlinear energy estimate. If q>=1, this particular estimate is
inconclusive and cannot be presented as a physical failure or clearance.

## Charges, physical density, range and nontrivial data

The U(1) tangent is

    average(u*dp_v-v*dp_u+p_v*du-p_u*dv)=0.

Resolve the constant part of dp_v from this condition; average(u)=1
on the fixed prepared profile. This operation is independent of the unknown
trace and eliminated metric momenta. It is a charge-level coordinate
choice, not pointwise charge fixation. Retain all other phase/mean data.

For a fixed clock charge, the target delta I_density has zero integral.
Its scalar physical-density relation remains

    delta I_density=N*sqrt(h)*delta rho
                         +I_density*delta log(N*sqrt(h)).

Thus current density is an action-derived weighted physical density, not
an imposed new matter law or a claim that rho alone is the same coordinate.
The algebraic measure term is retained. The density inverse reconstructs
the metric mean where constrained by this ensemble; it does not set a
homogeneous metric or momentum mode to zero.

The actual full inverse is on the source subspace satisfying the weighted
longitudinal compatibility after the projected solve. This range is not
empty or solely gauge. For each n>=1, choose an even tensor-cross
configuration dhxy=cos(nz), with zero independent momentum means and even
current source of zero mean. The prepared data and coefficient functions
have their certified reflection parity. Uniqueness of the projected inverse
then makes f even, while R*f+s_z/(2a) is odd, so its integral vanishes.
The auxiliary secondary perturbation is reconstructed afterwards. This is
an admitted infinite family of INITIAL linear tangents. No parity rule is
adopted for general data; both parities remain in the range problem.

These hxy directions are not planar coordinate gauge: at the prepared
hxy=0 background, Lie_xi hxy=0 for every planar xi. Residual translations
are still gauge equivalences of the full graph and require treatment in
the eventual physical symplectic quotient, not deletion as a mode.

## Actual interval bounds and complete momentum control

All coefficients use the full initial-root C2 uncertainty. Only values
and first spatial coefficients are needed; the unused highest shift jet
in the Taylor engine does not impose a vanishing third derivative on the
root. No future conformal, constant-rate or finite-Fourier restriction is
assumed. The exact initial root and its previous smoothness certificates
remain the source of admissible background data.

The outward operator bounds in the preceding proof give

    ||A2+1||_infinity <0.001952,
    ||A1||_infinity <0.015215,
    ||A0-(-2263/8400)||_infinity <0.082302,
    ||T_z-pi0*P0||_(L2 to L2) <0.025983,
    ||L-L0||_(H2 to L2) <0.143923,
    ||L0^-1*(L-L0)||_(H2 to H2) <0.534224,
    ||L^-1||_(L2 to H2) <7.970.

The negative reference mean coefficient is an initial constraint-operator
coefficient. It is not a negative squared frequency, a kinetic signature
or a physical ghost diagnosis. Its nonzero value permits inversion.

For all three momentum unknowns, the audit differentiates their actual
momentum equations and bounds their H1 norms, not merely their values.
Let the assembled source/data norm be

    D=||r||_L2+sum_i(||s_i||_L2+|eta_i|).

Here r is the current-density right side after known free-field and U(1)
source assembly; eta_i are the retained original-coordinate momentum
means. The actual transverse source construction has zero means. For
arbitrary independent r/s data, these mean conditions and the solved
longitudinal compatibility are required range conditions.

Conservative complete bounds are

    ||f||_H2 <13.872*D,
    ||p_x||_H1 <3.002*D,
    ||p_y||_H1 <3.002*D,
    ||p_z||_H1 <21.788*D,
    ||f||_H2+sum_i||p_i||_H1 <41.662*D.

These are bounds on the assembled initial inverse, not observational
numbers, numerical error estimates or a claim about an optimal norm.
The scalar physical rho is recovered with its complete algebraic measure
variation; I_density and rho are not silently identified. Source assembly
must retain the frame-momentum derivative and force/metric second
spatial derivatives from the canonical graph.

## Direct controls, audit and immutable replay

[Scientific executable](../../../Analysis/MasterTests/test_01_r4c1_rtau_coupled_periodic_inverse_v1.py):
31/31, exact immutable replay COMPLETE; session 41654 terminal exit 0.
[Receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_coupled_periodic_inverse_v1_attempt_01/summary.json)
SHA256 b97ac2036d5e3ae02776443caaf2ece057268fdfdab04f885c5eb24cc1507157.

Three independent local trace jets at each registered centre are completed
with nonzero momentum values and derivatives satisfying the actual coupled
momentum equations. The direct raw-action density comparison differs by
less than 5.079e-46, against frozen 1e-28. The original canonical-rate and
full-field graph controls pass on these completed probes. The integrating
factor identity is independently checked symbolically. The action's exact
reference density, both mean/nonzero coefficients and the all-harmonic
Green bound are verified; omitting longitudinal momentum changes the
operator by 3469/2100 at the reference.

[Interpretation/Sobolev audit](../../../Analysis/MasterTests/audit_01_r4c1_rtau_coupled_periodic_inverse_v1.py):
12/12, exact replay COMPLETE.
[Audit receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_coupled_periodic_inverse_audit_v1_attempt_01/summary.json)
SHA256 25d6da6f28a4e0f5601825999bb8fb891e3fe486087e3e61eb63adbab136895e.
It independently reads binary endpoints, verifies the Neumann inequality,
derives all three H1 momentum estimates from the exact equations using
exported action Hessians/actual profile jets, and retains the weighted
compatibility. Same-author controls are not independent external review.

This bundle has no failed scientific attempt or relaxed tolerance. All
inherited earlier failures, sources and sidecars remain preserved. No
lapse, force, mean or constraint coefficient was adjusted to obtain the
bound. The prior unresolved-inverse report remains historically correct;
this new proof is a separate versioned result with an explicit range.

## Disposition and next deciding task

Initial projected canonical inversion and its full compatible range are
now established in the registered planar linear scope. Residual coordinate
symmetries and charge-level degeneracies still require the actual physical
symplectic quotient. Nontrivial initial tangents do not prove a preserved
nonlinear physical sector or a healthy evolving background.

NEXT: pull back/quotient the actual canonical two-form through this inverse,
retain both global charges and all physical means, and derive the prepared
physical evolution operator with time-dependent basis/projector drift.
Use the existing initial accelerations and clock/current identities. The
zero-speed sector, indefinite principal gradient energy and actual mixed
spatial derivative counts must be handled, not removed by an arbitrary
positive weight or by reusing the old homogeneous t=0.05 theorem.

Transverse modes, nonlinear persistence, interactions/validity window,
GR/local compatibility and genuine identifying matching remain incomplete.
No new identifying input or concrete P1/P2/Thermodynamics/original-R4C1
manuscript defect arose here. No paper/site change is warranted. Inherit
prior action/root/gauge/temporal/mixed/principal/canonical/clock review debt.
Goal ACTIVE and incomplete; review DEFERRED; physics_pass=false;
gate_effect=NONE. No action adoption, provider dispatch, vault mutation,
publication, commit, push or deployment.
