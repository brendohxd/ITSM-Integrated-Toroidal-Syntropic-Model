# A09.2 general planar coupled current-density operator

19 November 2026. Conditional linear-operator component COMPLETE_SCOPED.
Actual background/operator/energy persistence remains OPEN. R-tau UNADOPTED;
original R4C1 unchanged; review DEFERRED; Rule9_cleared=false;
physics_pass=false; gate_effect=NONE.

## Result and its limit

The coupled trace/current operator is now explicit in the general planar
spatial gauge, with the actual action's canonical coefficients, eliminated
momentum feedback, global translation compatibility and weighted means.
The Jacobian weights are essential: ordinary new-chart momentum means are
not the old-chart mean data. Retaining the weights identifies the initial
operator with its certified predecessor and gives an adapted Green bound
below 8. A conditional perturbation radius 1/16 then gives a bound below 16.

The new formulas were checked against the full raw action at a nonconformal
off-shell metric, with a newly validated temporal inverse. This test is not
an admitted background. The radius is a sufficient operator-invertibility
condition; no actual future coefficient tube, physical stability, cutoff or
frequency window is inferred. The next scientific task is to control the
actual background and coefficient drift entering this operator and its energy.

## Chart, canonical momentum means and global range

Use the preceding general-planar gauge owner and normalized 2*pi means.
Write h=[[H,m],[m^T,c]], G=H-mm^T/c, W=diag(1,1,2), R=W^-1,
B=W h, A=B^-T=R h^-1. The mixed/longitudinal metric components m,c are
constant in space. The trace configuration direction is

    delta G=G f, delta m=delta c=0,
    v=(Gxx,Gxy,0,Gyy,0,0,0,...,0), delta q=v f.

Other free metric/frame/scalar, momentum and modulus directions remain source
data. This is a linear background-based chart, not a nonlinear canonical
Darboux construction or a physical-time quotient.

Let e=(p_hxz,p_hyz,p_hzz), ell=-V^z(p_Vx,p_Vy,p_Vz)^T and
j=(0,0,sum_free p_A Dq_A)^T. The exact canonical momentum row is
C=D(B^T e+ell)-j. For fixed background weights Omega(z), the retained mean
data are eta=mean(Omega e). The previous unweighted formula is the special
case Omega=I. Define

    N=mean(Omega A),
    P_A,Omega v=A[v-N^-1 mean(Omega A v)].

For a general tangent source, linearizing the actual momentum equation gives

    delta e=A[P(delta j+delta C)-delta B^T e-delta ell+k],
    k=N^-1[delta eta-mean(Omega A(P(delta j+delta C)
                                      -delta B^T e-delta ell))],
    mean(delta j+delta C)=0.

Weights are held fixed for the tangent at the given background chart. Their
time dependence along a background is retained below. The mean/range condition
is not supplied automatically by the projected solve.

For the trace direction, hold the free canonical momentum slots fixed. Put

    t=p_hxx Gxx+p_hxy Gxy+p_hyy Gyy,
    u=p_hxx D Gxx+p_hxy D Gxy+p_hyy D Gyy,
    s=u-Dt, Q=[[G,0],[0,0]], kvec=Q W e,
    U=e_z t-kvec.

Then delta j=e_z(t Df+u f), delta ell=0, and the zero-mean-data trace map is

    T f=P_A,Omega[U f+e_z P(s f)].

Indeed P(t Df+u f)=t f-mean(t f)+P(s f), and P_A,Omega annihilates a constant
input vector. This cancellation retains the weighted normalization; it does
not discard a physical momentum mean. The global trace compatibility remains
mean(t Df+u f)=mean(s f), with the full free-source contribution included.
It must be imposed after solving the coupled projected current equation.

For smooth bounded coefficients T is order zero on L2. A sufficient generic
bound uses alpha=||A||infinity, w=||Omega||infinity, nu=||N^-1||:

    ||T|| <=alpha(1+nu*w*alpha)(||U||infinity+||s||infinity).

No lower-order feedback is deleted. The old auxiliary primary momentum remains
zero and no global phase or clock charge is fixed pointwise.

## All local current coefficients from the same action

Use q=(metric6,frame3,u,v,r,psi,Z), canonical p_i=Lbar_vi and the 13-rate
Legendre inverse, with the auxiliary primary excluded from that inverse.
The existing full action, its nonsingular local temporal Hessian and canonical
lapse-gradient identity specify the coefficient functions without new fitted
constants. Spatial rates, shift and all six metric slots are independent
during differentiation. With MP2 the declared Einstein coefficient,

    F=N*gamma*h^{iz} p_Vi-N*MP2*curvature_flux/2
                         -b*N*sqrt(h)*Z*h^{zz}*Dpsi,
    I=Ihat-D F, Ihat=Lbar-p*(qdot-Lie_S q).

The raw lapse variation gives this F; it is not an optional boundary choice.
Canonical derivatives of F hold p independent. Let Lie_S(delta q)
=S^z D(delta q)+T_S delta q. The complete local operator is

    delta I=C0 delta q+C1 D(delta q)+C2 D^2(delta q)
                                  +D0 delta p+D1 D(delta p),
    C0=Lbar_q+T_S^T p-D(F_q),
    C1=Lbar_d+S^z p-F_q-D(F_d), C2=-F_d,
    D0=-(qdot-Lie_S q)-D(F_p), D1=-F_p.

The implementation's canonical_coefficients function evaluates every row of
these arrays from the full action and explicit full-metric F. It does not use
the old specialized B1 matrices. Shift variations cancel in this canonical
representation; shift, lapse and chart effects in the coefficients remain.

Since F contains no eliminated metric momentum, D1_e=0 and D0_e=-Rvel_e.
Thus the complete projected trace operator, with free sources moved to its
right-hand side, is

    L f=a2 D^2 f+a1 Df+a0 f-Rvel_e dot T f,
    a2=C2 dot v,
    a1=C1 dot v+2 C2 dot Dv,
    a0=C0 dot v+C1 dot Dv+C2 dot D^2 v.

All free-source rows use the same C/D arrays and the general tangent momentum
formula above. Frame momentum derivatives remain: D1_Vi=-N*gamma*h^{iz}.
Physical density rho=I/(N sqrt(h)) also retains its algebraic measure variation;
I and rho are not identified as coordinates or time-rate norms.

## Exact general principal coefficient

For a planar metric the actual spatial curvature flux satisfies

    curvature_flux=-sqrt(h)*(h^{zz}h^{ij}-h^{zi}h^{zj}) D h_ij.

Contracting its derivative with the Schur trace direction gives

    a2=-N*MP2*sqrt(h)/2 * [2/c+(m^T G^-1 m)/c^2].

For positive lapse, MP2>0 and positive h, this is strictly negative. It is a
constraint/current trace-ellipticity statement, not a propagation speed or a
positive physical kinetic-energy result. With kappa I<=h<=Kmax I,

    |a2|>=N_min*MP2*kappa^(3/2)/Kmax.

The mixed-modulus contribution must not be dropped. At the initial adapted
metric m=0, c=Abar^2, G=a^2 I, the coefficient is -N*MP2*a^2/Abar. It equals
the old coefficient -N*MP2*a multiplied by the initial Jacobian J=a/Abar,
as required for a density and a second derivative.

The regulator's complete improvement gives
I_reg=b*N*sqrt(h)*(Z^2/2+Z Delta_h psi). On the auxiliary secondary relation
it is -b*N*sqrt(h)*(Delta_h psi)^2/2. Metric variation of Delta_h psi has at
most one metric derivative. Independent Z/Z_z contributions cancel as in the
owning canonical-density derivation. No extra second-metric-derivative term is
inserted by substituting the auxiliary secondary relation into one term only.

## Correct initial chart identification and inverse margin

At the initial background zeta_z=J, fields pull back by U f=f(z(zeta)) and
current densities by I_new=U(I_old/J). Canonical mixed momenta transform as
p_xz,new=p_xz,old, p_yz,new=p_yz,old, p_zz,new=J p_zz,old. Therefore the
OLD mean data, expressed in the new chart, use

    Omega=diag(1/J,1/J,1/J^2).

Replacing these by ordinary new means changes the trace operator by a
normalization/finite-rank term. No such replacement is made here. With all
free sources, means and the compatible range transformed consistently,

    L_new(0)=J^-1 U L_old(0) U^-1,
    G_new(0)=U G_old(0) U^-1 J.

The last J denotes source multiplication before the old-coordinate solve.
The fixed-charge source measure and original data definitions are preserved.
The old reference's negative nonzero mean coefficient is retained.

For r=1/13000 the certified initial map obeys exp(-2r)<=J<=exp(2r) and
||J_z||<=r exp(2r). Direct chain rule and change of variable give

    ||U||_(H2_old to H2_new)<=exp(3r)+(r/2)exp(7r),
    ||U^-1 J||_(L2_new to L2_old)<=exp(r).

Here D_zeta^2(Uf)=U[J^-2 f_zz-J_z J^-3 f_z], and the sharp bound
||f_z||L2<=||f||H2/2 is included. Hence

    ||G_new(0)||<7.970*(exp(4r)+(r/2)exp(8r))
                  <7.972759413<8.

On the same identified chart/range, an ACTUAL future operator difference
||L_new(t)-L_new(0)||_(H2 to L2)<=1/16 would give ||G_new(t)||<16.
This difference has not been established. It is not inferred from metric
positivity or from initial coefficient values. The Green drift identity is
G_t=-G L_t G, with the conditional bound ||G_t||<256||L_t||.

## Weighted normalization and full drift obligations

For the diagnostic geometric envelope kappa=1/2,Kmax=2, the unweighted mean
matrix N0=R mean(h^-1) has ||N0^-1||<=4. If epsilon=||Omega-I||infinity,

    ||N0^-1(N-N0)||<=8 epsilon.

Thus 8 epsilon<1 suffices for weighted normalization. The actual initial
epsilon<=exp(4r)-1<0.000307740 gives contraction <0.002461918. The independent
one-percent weight envelope has ||N^-1||<=100/23. The earlier unweighted
momentum estimate and mean(e)=-mean((Omega-I)e) also imply, for zero weighted
mean and epsilon<=1/100,

    ||T||<=(200/91)(||U||infinity+||s||infinity).

This is a sufficient conditional bound. Neither arbitrary positive weights
nor the unweighted momentum bound alone justify a weighted inverse.

Let v_f=U f+e_z P(s f), k_f=-N^-1 mean(Omega A v_f), with f fixed for an
operator derivative. Then

    A_t=-R h^-1 h_t h^-1,
    N_t=mean(Omega_t A+Omega A_t),
    k_f,t=-N^-1 mean[(Omega_t A+Omega A_t)(v_f+k_f)
                                             +Omega A v_f,t],
    T_t f=A_t(v_f+k_f)+A(v_f,t+k_f,t).

For a=||A||, at=||A_t||, w=||Omega||, wt=||Omega_t||, nu=||N^-1||,
d=||U||+||s|| and dt=||U_t||+||s_t||, a sufficient bound is

    ||T_t|| <=(1+nu*w*a)*[(at+a*nu*(wt*a+w*at))*d+a*dt].

The complete coefficient drift consequently obeys the conditional estimate

    ||L_t||_(H2 to L2)<=||a2_t||+||a1_t||/2+||a0_t||
                         +||Rvel_e,t||*||T||+||Rvel_e||*||T_t||.

These are explicit inputs to be bounded from actual canonical evolution,
not free parameters to set to zero. All time derivatives are in the declared
background chart; its coordinate drift is included. For the inherited initial
map zeta_t=J w, J_t at fixed zeta is J w_z. Hence the initial transported
weights have rates -w_z/J and -2 w_z/J^2. This does not prescribe their future
history or show the coupled flow stays in either diagnostic envelope.

## Evidence and next task

[Contract](RES001_RTAU_PLANAR_CURRENT_OPERATOR_V1_CONTRACT_2026-11-19.md);
[executable](../../../Analysis/MasterTests/test_rtau_planar_current_operator_v1.py);
[receipt](../../../Analysis/MasterTests/outputs/rtau_planar_current_operator_v1_20261119/receipt.json).
Main 29/29; SHA-256
`146c6c78e682a2bfc1cbf56f2f8312ac9adf662420b08c8fc21a5a00476c7305`;
456 source pins, with byte-identical replay. The full raw action is reevaluated
at the declared nonconformal positive metric; its temporal Hessian is rebuilt
and its inverse validated with contraction <3.106e-49. Full canonical-density
and raw-lapse identities agree below 4.770e-48 against the frozen 1e-28
tolerance, including a trace-second-derivative and an all-slot canonical probe.
These local controls neither fit new coefficients nor admit a new background.

[Separate audit](../../../Analysis/MasterTests/audit_rtau_planar_current_operator_v1.py);
[audit receipt](../../../Analysis/MasterTests/outputs/rtau_planar_current_operator_audit_v1_20261119/receipt.json).
17/17; SHA-256 `4b4be0a8582c2ff73704b3560a7c9097157f6d3fdcc458d2970bc977883f9b3b`;
458 pins and byte-identical replay. It independently derives the generic Schur
contraction, coordinate/mean factors and norm arithmetic. It audits the primary
raw-action receipt; it is not a second independent action implementation or
external peer review. No failed attempt occurred in this component. Earlier
failed versions remain pinned and untouched.

Provisional reuse is supported for this full operator, its weighted range and
conditional inverse estimates. Inherit general-planar gauge/momentum,
canonical-density, coupled-inverse, action/transport, initial-energy and
symplectic/charge-frame review dependencies. Later review must examine the
weighted means, canonical slot factors, current improvement, chart drift,+operator domains and conditional-versus-actual time estimates.

Next obtain the actual nonconformal background/current-coefficient time
control for a2_t,a1_t,a0_t,Rvel_e,t,U_t,s_t and the moving weights, and test the
operator margin with continued constraints and energy. A uniform bound or
existence argument remains required; a prescribed coefficient path or isolated
finite-centre residual cannot supply it. Harmonic coordinate history remains
explicit. G1-G6, physical interactions/window and identifying matching remain
open; MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED. No action adoption,
manuscript/site edit, vault mutation, provider dispatch, commit, push,
deployment or publication.
