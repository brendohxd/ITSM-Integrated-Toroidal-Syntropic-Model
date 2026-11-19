# A09.2 general planar gauge and momentum-domain component

19 November 2026. Conditional mathematical component COMPLETE_SCOPED;
A09.2's actual evolving physical domain remains OPEN. R-tau is UNADOPTED.
The original R4C1 action and its failures remain separate. Review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Result and deciding limit

The initial conformal metric is not required for the planar coordinate-gauge
inverse or canonical momentum-constraint reconstruction. Both have explicit
general-metric formulas and conditional norm bounds. The actual prepared
initial metric and its first jet satisfy the stated geometric envelope.
The harmonic velocities still have no time-history law supplied by the spatial
gauge equations. This is residual coordinate freedom, not a missing physical
force or an instability finding. Two constant transverse translations act
trivially on the planar stratum; the longitudinal translation acts nontrivially
and is retained. No origin condition or physical-time/phase quotient is adopted.

This does not establish the actual background's continued existence or its
continued coupled density/current and energy charts. The next required
calculation is the actual coupled density/current operator on the permitted
nonconformal directions, followed by controlled background/coefficient and
energy persistence. The geometric and operator neighborhoods below are
conditional diagnostics, not a physical frequency/momentum validity window.

## General planar metric and coordinate inverse

Use the inherited normalized circle mean, D=partial_z and mean-free primitive
P=D^-1 P0, with period 2*pi. Fourier H1/H2 norms have squared weights
(1+n^2) and (1+n^2)^2. In the existing spatial gauge,

    h=[[Hxx(z),Hxy(z),mx],[Hxy(z),Hyy(z),my],[mx,my,mz]],
    W=diag(1,1,2), R=W^-1, K=h^-1, M=mean(K).

The three m_i are physical metric moduli, constant in space but not assumed
constant in time. No equality of Hxx,Hyy and no zero Hxy restriction is made.
For a planar coordinate velocity xi, its three mixed/longitudinal metric Lie
components are

    (Lie_xi h)_(xz,yz,zz)=B Dxi, B=W h.

The order W h matters. B need not be symmetric; R B=h is symmetric positive.
Let b be the ungauged metric-rate triple in this chart, with all already
required canonical and background-chart terms included. The gauge condition
is D(b+B Dxi)=0. Its unique mean-free solution and physical modulus rates are

    d=M^-1 mean(K R b), s=Dxi=K(d-R b),
    xi=P s+H(t), c=b+B s=W d.

All three components of H(t) remain explicit. M is positive definite for any
uniformly positive h. The original diagonal metric formula, including both
weighted transverse means and longitudinal mean, is an exact special case.
Deleting c generally destroys periodicity; it is not a harmless simplification.

Assume kappa I<=h<=Kmax I, ||h_z||_op<=L and ||h_t||_op<=T in this chart.
Then Kmax^-1 I<=M<=kappa^-1 I. Pairing h s=d-R b against mean-free s gives

    mean(s^T h s)=-mean(s^T R b),
    ||s||L2<=kappa^-1 ||R b||L2,
    ||xi-H||H1<=sqrt(2)/kappa ||R b||L2.

This coercive cancellation avoids a large triangle estimate on the separately
retained modulus constant. For b in H1, differentiating the equation gives

    ||s_z||L2<=kappa^-1 ||R b_z||L2+L/kappa^2 ||R b||L2,
    ||xi-H||H2<=(sqrt(3)/kappa+L/kappa^2)||R b||L2
                                      +kappa^-1 ||R b_z||L2.

For the mean-free gauge operator Axi=D(B Dxi), R A=D(h D).
Its negative has gap at least kappa. For a mean-free L2 source g,

    ||A^-1 g||H2<=sqrt(3+(1+L/kappa)^2)/kappa ||R g||L2.

These are coordinate-operator bounds, not positivity of a physical Hamiltonian.

## Drift and coordinate regularity

On a sufficiently differentiable supplied metric/rate history,

    K_t=-K h_t K,
    d_t=M^-1 mean[K(h_t s+R b_t)],
    s_t=K_t(d-R b)+K(d_t-R b_t), mean(s_t)=0.

Pairing the differentiated equation against s_t gives

    ||(xi-H)_t||H1<=sqrt(2)/kappa ||R b_t||L2
                                +sqrt(2)*T/kappa^2 ||R b||L2.

H_t is not inferred from these equations. Its spatial gradient is zero even
when H depends arbitrarily on time. At fixed planar canonical data the constant
transverse generators act trivially on both fields and their momentum-density
duals. The longitudinal generator transports their actual spatial profiles.
The clock evolution X_H0=-X_I remains physical and is not that translation.

For a supplied background with the uniform bounds and b in L1(time;H1), the
mean-free coordinate velocity is integrably spatially Lipschitz. An H in L1
time supplies an absolutely continuous residual translation. A resulting
coordinate flow, when constructed, has positive Jacobian bounded below by
exp(-integral ||Dxi||infinity dt). L2 time control of H suffices on a finite
interval and is also a natural sufficient condition for an energy forcing term
bounded by a constant times |H|^2. These are conditional regularity requirements,
not a choice of H or a proof of a coupled background flow.

## Full canonical momentum reconstruction and range

The inherited action-derived spatial generator has the sign convention

    C_i=D(B_full,i(q)^T p)-delta_iz p*q_z.

In this gauge let e=(p_hxz,p_hyz,p_hzz), eta=mean(e). Let

    ell=-V^z (p_Vx,p_Vy,p_Vz)^T,
    j=(0,0,sum_free p_A Dq_A)^T.

The sum includes the free metric, frame and scalar sectors, with auxiliary
primary momentum zero. The eliminated contribution to p*q_z vanishes because
D h_iz=0, not because its momentum or modulus is zero. The exact equation is

    C=D(B^T e+ell)-j.

For a specified residual/source r, solving C=r requires mean(j+r)=0. Define

    v=P(j+r)-ell, A=B^-T=R K, N=mean(A)=R M,
    k=N^-1 [eta-mean(A v)], e=A(v+k).

This retains all canonical means and the residual longitudinal translation
compatibility. The transverse conditions reduce to mean(r_x)=mean(r_y)=0.
For exact constraints r=0, mean(j_z)=0 is still required. The projected solve
alone does not make it automatic. At this chart, eta labels instantaneous
canonical momentum means; it is not an invented conserved charge and is not
silently identified with means in the older original coordinate.

For L2 v, putting y=W(e-eta) and using mean(y)=0 yields

    ||e||L2<=(1+2*Kmax/kappa)|eta|+kappa^-1||v||L2.

If j+r is L2 and ell is H1, then

    ||De||L2<=kappa^-1||j+r-Dell||L2+(2L/kappa)||e||L2.

These solve the momentum part at fixed configuration/free data. The coupled
clock-current scalar inverse and auxiliary reconstruction must still be
composed on a justified common domain; this is not their nonlinear solution.

## Moving Ward pairing without a conformal metric assumption

The full action's conditional Ward law is C_t=Lie_S C. With a perturbation,
delta C_t=Lie_S delta C+Lie_deltaS C_background. For any smooth periodic
vector weight rho, the exact weak identity is

    d[-mean(rho^T delta C)]/dt
      =-mean[(rho_t-S^z D rho+rho_zcomp D S)^T delta C]
       -mean[rho^T Lie_deltaS C_background].

Here rho_zcomp is the longitudinal component, not D rho. The local integration-
by-parts difference is exactly D[S^z rho^T delta C]. No conformal identity is
needed for this formula. A weight that defines an actual range functional
must still be derived from the chosen chart, rather than chosen to make its
rate vanish. The earlier conformal weight (0,0,1/(2a)) and its derivative give
the owning scalar formula, with all transverse index/source terms retained.
The finite numerical centre is not treated as an exact constrained background.

For an already existing regular background/shift, the full constraint transport
also obeys the conditional L2 bound

    d||C||L2^2/dt <= (||D S^z||infinity+2||D S||infinity)||C||L2^2.

This follows by the same periodic divergence and Cauchy-Schwarz. Integrable
shift-gradient control therefore propagates zero constraints for a solution
that exists. It does not supply that solution, its shift-gradient bound, or
the coupled density/range chart. Inhomogeneous finite-centre terms stay explicit.

## Initial envelope and conditional Green margin

The diagnostic geometric envelope kappa=1/2, Kmax=2, L=1/10, T=2 contains the
actual prepared initial metric and its first jet, uniformly over the inherited
root ball. Outward interval checks use the certified H interval, r=1/13000,
the initial adapted profile and its drift; conservative rounded bounds are

    h >=0.99984616 I, h <=1.00015386 I,
    ||h_z||op<0.000153894, ||h_t||op<1.733405.

In that conditional envelope the coordinate H1 and gauge-operator H2 constants
are 2*sqrt(2) and 2*sqrt(111/25); drift constants are 2*sqrt(2) per ||R b_t||
and 8*sqrt(2) per ||R b||. Momentum L2 constants are 9 per |eta| and 2 per
||v||; its derivative estimate has constants 2 and 2/5 respectively.

The separately certified initial coupled scalar Green bound is G0<797/100,
including its nonzero negative mean eigenvalue. If the actual continued
operator is identified on that same normed chart/range and obeys

    ||L(t)-L(0)||_(H2 to L2)<=50/797,

the Neumann argument gives ||G(t)||_(L2 to H2)<797/50=15.94. If L_t is also
bounded in that operator norm, G_t=-G L_t G gives
||G_t||<254.0836 ||L_t||. This does not extend the initial conformal operator
formula by substitution. The actual general-metric reduced operator, its chart
identification and its time-variation bound remain to be calculated. Exceeding
this sufficient radius makes this estimate inconclusive, not a singularity or
an all-action no-go. No actual future interval, cutoff or positive physical
energy follows from these conditional neighborhoods.

## Evidence, failures and continuation

The [frozen contract](RES001_RTAU_PLANAR_GAUGE_DOMAIN_V1_CONTRACT_2026-11-19.md)
and approved preparation precede execution. The
[V3 executable](../../../Analysis/MasterTests/test_rtau_planar_gauge_domain_v3.py)
passes 31/31 checks and exactly replays its
[receipt](../../../Analysis/MasterTests/outputs/rtau_planar_gauge_domain_v3_20261119/receipt.json),
SHA-256 `185e3765ed9c2a3564fa0a704f84ed9dde1e62fb1332124a97e42764489b8d8a`.
It verifies 450 scientific source pins, including all inherited 439 inputs.
Exact lossless Laurent controls have variable nonconformal transverse metrics,
nonzero mixed moduli, time drift, nonzero momenta, both parities and full frame/
scalar terms. They test the actual registered Lie module, not an assumed scalar
block. Manufactured profiles are algebra controls, not new on-shell solutions.

The [separate audit](../../../Analysis/MasterTests/audit_rtau_planar_gauge_domain_v1.py)
passes 17/17 checks and exactly replays its
[receipt](../../../Analysis/MasterTests/outputs/rtau_planar_gauge_domain_audit_v1_20261119/receipt.json),
SHA-256 `a5e775d483940b76341ccd04a85766320eb4beb54f5b092e021409fe8f455218`.
Its 452 pins include the primary evidence. It independently derives the tensor
block and weak Ward total-divergence identity and checks exact norm/Green
arithmetic. This is same-assistant mathematical verification, not external
peer review or Rule-9 clearance. Source bytes, sidecars and mtimes are preserved.

V1 stopped before algebra by asking for sidecars of eight already-pinned
sidecars. V2 corrected that leaf handling, then stopped on an mpmath scalar/
interval adapter. V3 corrects operand conversion only. Both original sources
and failure artifacts remain pinned; no equation, domain or tolerance changed.

Provisional use: general planar coordinate/momentum inversion and the stated
conditional Ward/Green estimates. Inherit the initial forced-energy, planar
gauge, coupled inverse, canonical action/transport and symplectic/charge-frame
owners and all their unresolved review debt. Review asks include the canonical
slot factors, matrix ordering, global range, coordinate/physical distinction,
regularity, and hypothetical versus demonstrated tube.

Next derive the actual continued coupled current-density operator and its
range in this chart, with background/coordinate and source drift. Then test
whether the actual canonical evolution admits a controlled coefficient/energy
tube and a supported interval. The initial Ward/conformal formulas cannot be
reused unmodified at later times. A09.3 interactions/window, G1-G6 and both
identifying matching inputs remain open; K_Q NOT_DERIVED; V NOT_COMPUTED;
MAT-001 BLOCKED. No A16 refinement, new parent, physical-time quotient,
manuscript/site edit, vault mutation, provider dispatch, commit, push,
deployment or publication is implied or performed by this calculation.
