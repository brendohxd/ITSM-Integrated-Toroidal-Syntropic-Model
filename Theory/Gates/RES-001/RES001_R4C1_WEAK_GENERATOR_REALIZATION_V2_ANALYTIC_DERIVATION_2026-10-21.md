# Full weak-generator realization: analytic derivation

21 October 2026. Claim status: Conditional, within the unchanged frozen planar
R4C1 setup and the coefficient/domain assumptions stated below. Local analytic
argument; independent scientific review DEFERRED, not cleared. The numerical
verification and preservation record are supplied in the separate V2 owning
report. No physical state, positive energy or cosmological prediction is
admitted by this derivation.

## 1. Exactly what has advanced

The old two-form result did not, by itself, prove closedness of its composition
with the constrained Hamiltonian operator. Here the actual retained planar
operator has a continuous weak extension H -> H^-2. That extra structure gives
a CLOSED MAXIMAL MATHEMATICAL realization of Omega^-1 K by a direct graph-limit
argument. This is an operator-domain statement at frozen initial coefficients,
not a well-posedness, spectral-stability or physical-state theorem.

No dense physical domain, resolvent, semigroup, invariant time-dependent domain,
positive physical energy, healthy GR limit or physical frequency window is
established. In particular the negative scalar-rate energy restriction and the
finite-regulator weak-source linearization remain unchanged.

The graph-limit observation is a general structural fact once the weak
extension has been justified; its application here is not evidence of a new
cosmological prediction or an assessed publication-level novelty.

## 2. Space, coefficients and scope

Use the previous report's real canonical quotient space, including the
three mean metric coordinates and three conjugate momenta. Field components
have normalized periodic L2 norm on the planar circle; the finite mean pairs
have the declared reference-chart Euclidean norm. Phase/dust means and the
translation section remain removed by their original projections. These
projections are bounded on the periodic Sobolev spaces used below. They do
not discard the retained mean metric pairs.

Let H^2_sec denote the corresponding product periodic H2 test space plus means,
and let H^-2_sec be its dual. Embed H continuously and injectively in H^-2_sec.
Write D for the spatial derivative, I for its mean-zero inverse primitive,
and P0 for the periodic mean. For Fourier momentum m*k:

    I*D = Id-P0,
    ||I||_(H^r -> H^r) <= 1/k,
    ||I||_(H^(r-1) -> H^r) <= sqrt(1+k^-2).

These estimates include the zero Fourier component through P0, rather than
inverting it. For a smooth multiplication coefficient a,

    I(a*D f)=a*f-mean(a*f)-I((D a)*f).

The exact commutator and independent quadrature controls retain its mean term.
First variations of the spatial/global momentum restoration are consequently
order zero, although its second variation is not zero.

The frozen data have h=I, V=(0,w,0), w=e*cos(theta), theta=k*z,
s=p=eta/5, e=1/500, k=40, positive condensate amplitude Rc and eta>0.
The translation denominator is d=<sin(theta)*D w>=-e*k/2, not zero;
the mean inverse-metric matrix in the momentum restoration is I.
The original 12-velocity partial Legendre certificate applies on this slice.
No inverse at eta=0 is used.

The argument is for each supplied regular frozen coefficient set, with the
nine existing family/eta instances checked independently. It does not prove
a continuum of on-shell backgrounds or a bound uniform in eta->0.
The supplied registered rate T is retained. Its use does NOT establish that
the complete underlying background and physical auxiliary hierarchy are on
shell; that admission remains open.

## 3. Full Legendre Hessian: no frozen-velocity shortcut

Let calL=volume*L0, y the twelve complementary velocities, and P_y their
canonical covector, retaining the original factor two for the six metric
velocity components. Define

    E(X,y)=P_y(X).y-calL(X,y),
    calR=calL_yy,
    calL_y(X,y(X))=P_y(X),
    T_u=delta P_y[u]-delta(calL_y)[u] at FIXED base y.

The implicit derivative is calR*delta y[u]=T_u. At the base stationary
velocity, the exact local identity is

    E_true''[u,v]=E_envelope,fixed_y''[u,v]
                 + T_u^T calR^-1 T_v.

It requires invertibility, not positivity, of calR. No physical-energy sign
is inferred from this factorization. The frozen envelope still contains
the SECOND derivative of the entire nonlinear spatial/global/charge
constraint pullback. Dropping that derivative is a separate error which the
response term would not repair.

The full clock Hamiltonian is

    H(X)=< (E_true(X)+E_dust(X))/s - F(X)*D(1/s) >.

At the constant base s=p, its Hessian is the full frozen-envelope/clock/flux
Hessian PLUS <T_u^T calR^-1 T_v/p>. In particular, if h=E_true+E_dust,

    H''[u,v]=<
      h_uv/p-(h_u*v_s+h_v*u_s)/p^2+2*h0*u_s*v_s/p^3
      +(F_u*D v_s+F_v*D u_s)/p^2
      -2*F0*D(u_s*v_s)/p^3 >.

F0 is not zeroed merely because D(1/p)=0 at the base. The exact second-
variation check rejects that deletion. Full nonlinear spatial Ricci, the
dust contribution, the potential and the restored metric/frame/matter
components remain in the original functional.

The independent controls compare the ORIGINAL full-minus-frozen-velocity
Hessian with the explicit implicit-response contraction. Fresh original-
functional mixed values solve all twelve velocities again; they do not
reuse the factorized bilinear as their answer.

## 4. The apparent shift division is removable at both nodes

The original Galerkin shift contains exactly twelve even sine harmonics:

    R(theta)=sum_(j=1..12) c_j sin(2j theta).

The Laurent/Chebyshev identity
sin(2j theta)=2 sin(theta)cos(theta) U_(j-1)(cos(2theta))
gives the actual profile expression

    R*D w/w = -2*k*sin(theta)^2
                * sum_(j=1..12) c_j U_(j-1)(cos(2theta)).

It is a finite smooth trigonometric polynomial. At BOTH theta=pi/2 and
3*pi/2 its limit is 2*k*sum_j j*(-1)^j*c_j=D R at that node.
Moreover |U_(j-1)(x)|<=j on [-1,1], by its finite unit-circle sum, so

    |R*D w/w| <= 2*k*sum_j j*|c_j|.

Thus the registered scalar clock rate
T_s=-U/p-3H+HB+D R+R*D w/w has a finite smooth extension there.
This does not assign a point value to a generic unbounded L2 quotient in
the earlier graph domain. It concerns this SPECIFIC finite shift profile.
It neither changes the chosen background nor evolves it.

## 5. Actual weak-order argument, sector by sector

At the fixed slice the remaining coefficient denominators are finite:
p>0, Rc>0, d=-e*k/2, positive h and the invertible calR. The smooth
metric/frame coefficients and the Galerkin profile have bounded derivatives
on the compact circle. The initial dust coefficient contains at worst the
registered |w|^3 cusp; its derivatives through order two are bounded.

(a) Spatial/global/charge restoration. In the original restore routine,
S is a sum of canonical momenta times first spatial derivatives, a total
derivative, and the regulator pair. Its inverse primitive is followed by
the finite translation correction and the inverse mean-metric matrix.
Linearizing at the frozen data reduces I(a*D u) by the commutator above.
Its first derivative is therefore bounded L2->L2 and H2->H2, with the
finite mean and translation terms included. Second variations contain
bilinear terms with at most one spatial derivative. When paired against
the smooth base velocity/clock coefficients, move that derivative onto
the H2 test factor and coefficient, using periodic integration by parts
and the true adjoint of I. This yields an L2-by-H2 bound, including all
second pullback terms and the finite-rank denominator/mean derivatives.
There is no omitted zero-mode inverse.

(b) Complementary velocities. calR is an order-zero smooth matrix field.
T is first order plus the bounded restoration terms. It is bounded
H->H^-1 and H2->H1. Multiplication by calR^-1/p is bounded on H^-1,
by the W1,infinity coefficient multiplier bound. Consequently
T^*(calR^-1/p)T maps H continuously to H^-2. The available inverse bound
scales with inverse powers of eta; no uniform GR endpoint is supplied.

(c) Spatial curvature. The ORIGINAL Ricci expression contains the full
connection derivatives and connection products. Its second variation
has order at most two: first-derivative bilinears and terms containing
one second derivative, including their clock cross terms. At the flat,
constant-clock base, periodic integration by parts places up to two
derivatives on the H2 test field. It is bounded H->H^-2. Replacing Ricci
by only its first variation would miss these terms; the original
nonlinear Ricci controls are retained.

(d) Force cusp and other local densities. In a smooth local spatial
orthonormal frame write the force cubic as |xi|^3, with base xi proportional
to w. Its REAL second differential has matrix
3|xi| I+3 xi xi^T/|xi| off zero and extends by zero at xi=0.
Along the base it is Lipschitz (W1,infinity), not assumed C3.
Its first-derivative bilinear form is bounded H->H^-2 by duality:
D u is H^-1 and a*D v is H1 for v in H2 and a in W1,infinity.
The lower derivative terms have the same or a better bound.
Canonical matter, alignment, the algebraic potential and the dust term
give ordinary local first-order or zeroth-order terms with the above
bounded coefficient multipliers. No analytic third force vertex is used.

(e) Clock and flux. The complete mixed formula in section3 contains only
the retained first derivatives and the finite clock weights. Its remaining
terms, including F0*D(u_s*v_s), obey the same L2-by-H2 estimate.
The second derivative of 1/s at the base cannot be discarded.

(f) Background two-form drift. Omega depends algebraically on canonical
configurations, s and mean coordinates, not spatial field derivatives.
Its derivative against u, contracted with the supplied configuration/
auxiliary rate T, is a bounded order-zero operator on H. The shift identity
above removes the apparent rate division at both nodes. Background
canonical momentum rates do not create a higher derivative term here,
since Omega has no momentum dependence. No drift term is suppressed.

In coefficient-norm notation, let C_env be the finite norm of (a),(c)--(e),
t0 and t2 the norms of T:H->H^-1 and T:H2->H1, m1 the multiplier norm of
calR^-1/p on H^-1, and C_drift the order-zero norm in (f). Then

    ||K u||_(H^-2) <= (C_env+t2*m1*t0+C_drift)*||u||_H,
    K u=Hessian(H)u-dOmega[u]T.

All constants refer to the fixed coefficients and declared reference units.
This is a finite coefficient-norm estimate, NOT a numerically certified
propagator constant, nonlinear error bound or physical cutoff. The analytic
sector argument, not the finite Fourier diagnostics, supplies continuity.
It initially holds for smooth sections and extends uniquely by their
density in H.

## 6. Closed maximal realization: what the theorem really says

The previous complete two-form is bounded and injective on H. For fixed
eta>0, g=b*w^2>0 almost everywhere; its two zero points have measure zero.
Define

    D(Amax)={u in H: exists v in H with K u=Omega v in H^-2},
    Amax u=v.

Injectivity makes v unique. If u_j->u and Amax*u_j->v in H, continuity of K
into H^-2 and boundedness of Omega give

    K u = lim K u_j = lim Omega*Amax*u_j = Omega v in H^-2.

Thus u is in D(Amax) and Amax*u=v: the graph is CLOSED.
The argument does not invoke an invalid general product-of-closed-operators
rule. It uses the actual weak extension established above.

Equivalently, K u must first belong to H and then to the previous forcing
domain Yg:

    (K u)_s/g in L2,
    ((K u)_Z-B*(K u)_P)/g in L2.

For auxiliary residuals actually in H2, the previous BOTH-node value and
first-derivative criterion applies. It must NOT be imposed on raw (K u)_Z
without the B*(K u)_P subtraction. No unproved H2 regularity is assigned to
general residuals in the maximal distributional domain.

Closedness alone does not prove that D(Amax) is dense or that it contains
the required physical initial-data class. It supplies no resolvent estimate,
semigroup, time-dependent persistence, uniqueness of the nonlinear IVP or
positive physical energy. Those facts are not consequences of defining
a graph norm. No generic method direction is promoted to a physical state.
