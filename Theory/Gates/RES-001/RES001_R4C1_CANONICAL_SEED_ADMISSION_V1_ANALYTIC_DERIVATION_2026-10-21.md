# Canonical amplitude-momentum seeds: full K and frozen second-domain distinction

21 October 2026. Unchanged R4C1 / RES-001 / Stage2.
Conditional mathematical result for the registered smooth planar structural
background, not an on-shell-background, physical-mode or evolution theorem.
Owning contract: `RES001_R4C1_CANONICAL_SEED_ADMISSION_V1_CONTRACT_2026-10-21.md`.
The independent node prediction was recorded in the separate node-force
addendum after launch but before scientific-receipt inspection. It is not
misrepresented as a pre-launch prediction.

## 1. Full constrained first action, not a scalar-only substitution

Use the original polar condensate variables rho,theta, fixed total phase charge
and its retained local contrast, radial canonical momentum P_rho, constant
background rho=Rc, P_rho=0. For smooth periodic f set u_f.P_rho=f and every
other component zero. This respects the existing mean/translation quotients;
it does not assert the missing physical auxiliary hierarchy is satisfied.

Directly in the original Cartesian action,

    (du)^2+(dv)^2=(d rho)^2+rho^2(d theta)^2,
    v du-u dv=-rho^2 d theta.

Thus the radial temporal kinetic term is quadratic and the alignment current
contains no radial rate. Its full partial-Legendre response is delta y_rho=f
at the flat unit-volume background. Freezing velocities would erase the
nonzero f/p momentum-covector row and is not the same Hessian.

The NONLINEAR momentum restoration must still be differentiated twice.
The mixed radial source with a position variation a is S_mixed=f*D a. Write
I for the zero-mean inverse spatial derivative, w=e cos(kz), sigma=sin(kz),
d=<sigma*D w>, y_L=actual stationary Kzz velocity and y_V=actual stationary
Xy velocity. The original translation restoration gives

    lambda_mixed=-<f*D a>/d,
    delta P_Kzz=[I(f*D a+lambda_mixed*sigma*D w)]/2,
    delta P_Xy=lambda_mixed*sigma.

The longitudinal mean momentum remains fixed. Contraction of these ORIGINAL
restored momenta with the stationary velocities contributes

    <y_L*I(f*D a)>/p + lambda_mixed*C/p,
    C=<y_V*sigma>+<y_L*I(sigma*D w)>.

I*=-I on periodic average-L2, hence the actual coefficient is

    R_eff=-I(y_L)-C/d,
    mixed H variation = <R_eff*f*D a>/p.

The translation constant is not discarded or assumed zero; neither is R_eff
replaced by a desired prescribed shift. Integrating by parts and retaining the
full stationary response therefore gives the ENTIRE K action

    (K u_f)_P_rho=f/p,
    (K u_f)_Q_rho=-D(R_eff*f)/p,
    every other field/mean covector row=0.

The original two-form depends on metric/frame/auxiliary coordinates, not on
canonical momenta. Consequently dOmega[u_f]T=0 exactly for this particular
seed. This is not permission to omit drift for general perturbations. All
potential, matter, Ricci, fixed-charge and clock-flux terms remain present;
their mixed seed contributions vanish by the stated structural identities,
not by deleting their sectors.

## 2. A nontrivial part of the frozen maximal graph

Use the SAME bounded injective complete Omega and weak K from the predecessor.
For fixed regular coefficients, eta>0, p>0, Rc>0 and d !=0, the unique graph
image has

    (A u_f)_Q_rho=f/p,
    (A u_f)_P_rho=D(R_eff*f)/p,
    all other components=0.

Omega of this image is exactly the covector above. Both auxiliary forcings
r_s and r_Z-B*r_P vanish IDENTICALLY on the entire circle. They therefore
satisfy the value AND first spatial derivative conditions at BOTH nodes.
For smooth periodic f and smooth regular coefficients, u_f and its image
belong to the ambient H, and K u_f=Omega(Au_f) in H^-2. This supplies a genuine
nonzero (indeed infinite-dimensional smooth) subset of the frozen D(A_max).
It is not a proof that D(A_max) is dense, a complete physical initial-data
space, a physical normalization or a well-posed Cauchy problem.

The finite collocation counterpart uses the original skew D/I and original
constraint restoration; both entire payloads, not only their auxiliary rows,
were compared against this independent formula.

## 3. Independent second-action node prediction

Let v=A u_f. Its radial-momentum part contributes zero auxiliary rows by the
first-action identity. Its position part is a=f/p. At either node w=0,
g=b*w^2 and Dg vanish. The clock-affine velocity coefficient vanishes there.
For the auxiliary s pullback the restoration source coefficient is
G=g*D Z=2*b*U*w^3*D w: both its value and first derivative vanish at the node.
The corresponding adjoint nonlocal/translation terms consequently have zero
VALUE there. This does not delete their nonzero effects away from alignment.
For this amplitude/radial-momentum image dOmega[v]T is also zero because g
has no dependence on either variable.

The remaining s-amplitude variation is the derivative of the local stationary
energy at FIXED LOCAL phase momentum j. At alignment its radial force is

    F_rho=V_rho-j_node^2/rho^3,
    V_rho=m2*rho+lambda4*rho^3/2
          +lambda6*rho^5/(4*Lambda^2)+g_r*rho*r_reservoir^2/2.

Since H contains E/s, the node mixed derivative is -F_rho/p^2. Therefore

    (K v)_s(node)=-F_rho*f(node)/p^3,
    (K v)_Z(node)=0.

The local phase density MUST NOT be replaced by its fixed total mean. The
original initialized phase velocity is Rc/(1-zeta*eta*e^2/2) and its momentum
coefficient is 1-zeta*eta*w^2. Thus at the node

    j_node=eta/(1-zeta*eta*e^2/2), not eta.

With rho=r_reservoir=sqrt(eta), e=1/500 and the ORIGINAL scalar parameter maps,

    x=eta^2/6500000,
    F_rho=sqrt(eta)*[eta/6+127*eta^2/560-((1-x)^(-2)-1)] >0.

Indeed 3*x-[(1-x)^(-2)-1]=x*(1-5*x+3*x^2)/(1-x)^2>0 on the registered domain,
and127/560>3/6500000. No microscopic matching or desired acceleration is used.
For f=1 or sin(kz), f(node)=+/-1, so the continuous s forcing is nonzero.
Since g has a quadratic zero, its quotient cannot be L2. Hence

    u_f is in frozen D(A), but A u_f is NOT in frozen D(A);
    equivalently u_f is not in frozen D(A^2).

This is an analytic conditional node argument with independent numerical
controls, not an inference of continuum traces from finite-grid convergence.
The computed positive force belongs to the chosen diagnostic coefficient
family, not an identified numerical ITSM prediction.

## 4. What this does NOT decide about evolution

D(A^2) is a stronger regularity requirement than D(A). The result is NOT a
proof of failure of a C0 semigroup, lack of its D(A) invariance, physical
instability, a ghost, a cutoff or an all-action no-go. A general strong solution
need not have its time derivative in D(A). No projection is applied to make
the next forcing vanish.

For a nonautonomous constraint F(t)u(t)=0 the material condition also contains
partial_t F, changing Omega/K and node motion; frozen F*A*u is insufficient.
A simple exact rejection example is F(t)=(-t,1), u(t)=(c,t*c),
M=((0,0),(1,0)). Then u'=M*u and F(t)u(t)=0 identically, whereas F(0)M*u(0)=c.
The missing explicit-time contribution is -c. This is a mathematical
counterexample to the invalid inference, not a proposed R4C1 trajectory.

The stored R4C1 background/rate has small NONZERO sampled chart residuals;
there is no certified exact on-shell evolving state. Finite precision alone
neither proves an exact solution nor rejects every nearby one. The new seeds
therefore remain mathematical candidates, not physically cleared initial data.
Completing the actual evolving auxiliary hierarchy/background and its physical
energy/domain is still necessary. No ordinary third force derivative at the
C2 alignment point, new physical state, or trajectory is assumed.

## Status

Stage2 INCOMPLETE; Stage3 NOT_ENTERED; physics_pass=false; gate_effect=NONE.
Review DEFERRED, Rule9_cleared=false; inherit the weak-generator/two-node,
scalar-energy, Legendre/descriptor and transitive dependencies. Existing
negative energy and finite-regulator weak-source results remain binding.

