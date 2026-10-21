# First material compatibility of the canonical seeds: analytic feasibility

21 October 2026. Unchanged R4C1 / RES-001 / Stage2.
Owner: R9-MT1-MATERIAL-SEED-FEASIBILITY-V1.
Conditional first material identity, NOT a physical evolution/domain theorem.
All action parameters are held fixed under dynamical-field variations.

## 1. Initial admission: preserve what is already established

The18 October INITIAL-ADMISSION-V1 report, SHA
7237b9649f08fe16746660415f418dd93b0268b81edb0871e6105abdca7c47ef,
already supplies an EXACT IMPLICIT construction for the KNOWN planar initial
canonical constraints and both global charges, with certified positive dust
and a unique mean root in the declared bracket. Its coercive shift solution
is not defined by a rounded finite Galerkin table.

That result is inherited, not rerun, repaired, counted as new closure or
replaced by midpoint equality. It explicitly leaves additional/rank-changing
Dirac consistency, full data admission, persistence and the Cauchy problem
open. Conversely a small nonzero defect of a finite exported representative
is not evidence that no exact initial construction exists. Distinguish
known initial constraints, full initial admission, and an evolving solution.

## 2. Exact radial canonical identity with nonlocal restoration retained

Write rho for condensate amplitude, P for its canonical momentum, J=sqrt(det h),
s for the force-clock proper rate, and D for the fixed periodic coordinate
derivative. The original scalar kinetic/current identities give

    (du)^2+(dv)^2=(d rho)^2+rho^2(d theta)^2,
    v du-u dv=-rho^2 d theta.

Thus the alignment current contains no radial rate. The direct stationary
partial-Legendre derivative in the radial momentum direction is P/(J*s).

The FULL spatial-momentum constraint source contains P*D rho. The nonlinear
longitudinal momentum restoration, translation section, mean metric pairs
and lapse flux must still be varied. Their first momentum variation is a
linear functional of f*D rho. Denote its actual adjoint multiplier by W(X).
It includes the original primitive, inverse mean metric and translation
denominator; it is NOT set to a chosen shift or discarded. The complete
identity is therefore

    delta H/dP = P/(J*s)+W(X)*D rho.                    (1)

The required derivatives of W exist in this regular chart: positive J,s,
nonzero translation denominator and invertible original12-velocity map.
The velocity response/restoration and lapse-flux dependence are smooth here.
The C2 force/cusp sector has NO radial-momentum derivative and does not
enter W through such a derivative. No ordinary third force derivative at
alignment is used.

## 3. The changing-background term is not zero

For the original structural data P=0, D rho=0, the action-generated canonical
rate T_rho is zero by(1), hence D T_rho=0. For the fixed native seed u_f.P=f,
the s component of the full K=Hessian(H)-dOmega[*]T is

    Phi_s[u_f] = -P*f/(J*s^2)+(D_s W)^*(f*D rho).       (2)

The star denotes the FULL Frechet adjoint, not a local W_s approximation.
The two-form is independent of canonical momenta, so its drift term vanishes
for this seed. At the structural data both terms in(2) vanish identically.

Differentiate(2) along the complete background tangent, including its explicit
force clock tau_dot=1. Terms containing P, D rho or D T_rho vanish specifically
at this initial structure; they are not deleted from a general evolution.
The result, in average-L2 field covectors, is

    (D_t Phi)_s[u_f] = -T_P*f/p^2.                    (3)

For the Z row the direct kinetic term is Z-independent and the remaining
Frechet-adjoint term is (D_Z W)^*(f*D rho), whose initial material derivative
also vanishes.

The COMPLETE cross correction is Phi_Z=r_Z-B*r_P with B=s*D_Q g and
g=b*J*(V^T h V). Its amplitude column is identically zero. All other canonical
momentum/mean rows of K*u_f have the factor D rho, and their time derivatives
have the factors D rho or D T_rho. Thus neither B-dot nor the differentiated
other rows produces a missing term here. Consequently

    (D_t Phi)_Z[u_f]=0                                (4)

for the actual cross-corrected row. This argument retains the mean pairs and
nonlocal restoration; it does not assume the flat B formula at a changed
metric/s point.

## 4. Original-action radial force and the frozen next response

At the initial flat, constant-amplitude, zero-phase-gradient structure, let
j(z) be the restored LOCAL phase momentum density, not its spatial mean.
Before substituting rho=sqrt(eta), differentiate the original stationary
phase energy j^2/[2*rho^2*(1-zeta*rho^2*w^2)] and potential. This gives

    F_rho=V_rho-j(z)^2*(1-2*zeta*rho^2*w^2)
                          /[rho^3*(1-zeta*rho^2*w^2)^2],
    V_rho=m2*rho+lambda4*rho^3/2+lambda6*rho^5/(4*Lambda^2)
          +g_r*rho*r_reservoir^2/2.                   (5)

Action parameters (including eta in their maps) are fixed in this derivative.
The original force/cusp, frame and regulator terms are retained but have
no direct rho dependence in this variation. The restored source's first
rho variation is P*D(delta rho), hence vanishes at P=0. Full spatial scalar
gradient terms have zero first variation because the initial gradients vanish.
Thus the entire initial radial force and canonical rate are

    delta H/d rho=F_rho/p,    T_P=-F_rho/p.             (6)

The full seed image from the preceding proof is

    v=A*u_f, v_rho=f/p, v_P=D(R_eff*f)/p.

Its momentum part has zero auxiliary rows by the original seed identity.
Varying(6) with respect to s gives the complete bulk s-amplitude row
-F_rho/p^2. F_rho is independent of s,Z and of metric/frame canonical momenta
on this structural slice. The corresponding Z row and its B correction vanish.
The two-form has no rho or P dependence, so the image drift is also zero.
The ACTUAL full frozen next forcing is therefore

    Phi_s[A*u_f]=-F_rho*f/p^3,    Phi_Z[A*u_f]=0.       (7)

It remains separately NONZERO at both nodes for the registered profiles.
The preceding frozen D(A^2) result is not retracted or overwritten.

## 5. First material balance and moving nodes

Combining(3),(6),(7),

    (D_t Phi)[u_f]+Phi[A*u_f]=(0,0).                   (8)

Both opposite s terms are retained: +F_rho*f/p^3 and -F_rho*f/p^3.
Their cancellation is derived from the action, not imposed by projection.

The identity is on the full circle under the stated smooth structural
hypotheses. Therefore its spatial derivative is also zero. At a moving node
z_*(t), transport adds z_*dot*D Phi[u_f] to the value and
z_*dot*D^2 Phi[u_f] to the first-jet expression. Those terms vanish here
because Phi[u_f] is initially IDENTICALLY zero, not because nodes are generally
stationary. The full frame's transverse nodal rates and original background
defects must still be checked; no persistent nodal trajectory is constructed.

This establishes a CONDITIONAL FIRST DIRECTIONAL MATERIAL compatibility identity
for this seed class. It is not the complete higher hierarchy, a proof that
every admissible perturbation persists, an invariant positive energy or a
well-posed/nonlinear short-time evolution theorem. It does not assume the
finite exported background is exactly on shell. In particular, a directional
curve X+h*T is a derivative control, NOT a solved physical trajectory.

The original temporal formulation includes tau_dot=1 for the global force
clock, while perturbations have fixed tau. Omega does not depend on tau.
Including explicit time dependence here is not a modification of the older
frozen operator or of its perturbation chart.

## 6. Dust-contrast defect bridge: no shortcut around the mean equation

On the homogeneous dust-time slice with s=p,

    H_dust=<exp(beta*tau)*p_dust/s>,
    R_s=n*(Omega*T-dH)_s.

A mean-zero canonical dust-momentum contrast d changes no scalar/frame
positions or their canonical coordinate rates at this slice. It is absent
from the12-velocity stationary equations and its spatial constraint source is
d*D T_dust=0. Thus, from the ORIGINAL full functional,

    Delta R_s=exp(beta*tau)*d/p^2,    Delta R_Z=0.       (9)

Its mean is zero. A constant contrast is removed by the fixed-charge chart
and changes nothing. Formally cancelling the zero-mean part of R_s leaves
the mean residual, not a solved global admission condition. The existing
certified mean construction remains necessary; its satisfaction is not by
itself a proof of the entire new background/Dirac hierarchy.

The finite1e-9 contrast used in the executable is only a temporary algebra
control. It neither rewrites the stored dust data nor adopts a new physical
initialization. Equation(9) is a bridge distinguishing representation defects
from full physical admission, not a second claim to have completed the old
initial-data construction.

## 7. Verification scope and remaining decision

The symbolic proof applies conditionally to smooth structural data in the
declared regular chart at fixed positive eta; no bound uniform at eta=0 follows.
The new numerical controls use ONLY six representative n17 cases: all three
families at eta=1/4, both node orientations, f=1 and sin(theta). They do not
become all-eta, all-domain or continuum interval certification. The entire
original functional, full Ricci, constraints, means and12-velocity responses
are used. Changed temporal matrices are rebuilt from the original local
density at every X+/-h*T point, not inherited from a specialized base matrix.

Positive first feasibility means the frozen next-response warning alone
does not stop this seed class at first material order. To proceed physically,
one still needs the exact evolving background/higher rank-changing consistency,
a controlled admitted perturbation space, persistence and Cauchy/energy/error
control, then the physical interaction/gravity window. Matching is independent.

Stage2 INCOMPLETE; Stage3 NOT_ENTERED; physics_pass=false; gate_effect=NONE.
Review DEFERRED; Rule9_cleared=false. No state adoption/evolution, new action,
publication, commit/push, vault mutation, paid dispatch or model/runtime change.

