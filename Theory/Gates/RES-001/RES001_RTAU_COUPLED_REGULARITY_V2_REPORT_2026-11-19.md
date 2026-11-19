# A09.2 coupled regularity: general planar quartic energy and weak geometry

19 November 2026. Conditional mathematical component. R-tau UNADOPTED;
review DEFERRED; physics_pass=false; gate_effect=NONE. Full nonlinear
background/operator/energy persistence remains OPEN. No positive time
interval, physical instability, validity window or action adoption follows.

## Result and deciding boundary

Three continuation prerequisites are now derived beyond the conformal
initial calculation:

1. The raw general-planar quartic self-block admits an explicit energy
   weight after spatial differentiation. The extra highest energy-adjoint
   derivative cancels; using the undifferentiated weight alone misses this.
2. The existing left-primitive cross-sector transformation has explicit H1
   commutator/inverse bounds with all means retained. Its composition
   remainder has a derived differentiated formula, not a frozen-symbol
   substitution. Actual nonconformal cross-block values remain required.
3. The preceding neutral-scalar energy needs only L2 second spatial
   coefficient derivatives. Its geometry/source bounds can therefore use
   an H2 spatial metric and appropriate scalar regularity, rather than
   unnecessarily assuming bounded pointwise second metric derivatives.

The residual closure problem is specific: derive the actual general-planar
ordinary Ward energy and both cross blocks from the unspecialized action,
then establish the full H1 remainder and common nonlinear constraint/charge
domain. Neither the old conformal ordinary matrices nor the new force
self-block proves those statements. The 487-input preceding result and
all original R4C1 results remain intact.

## General metric force/auxiliary rows

Use the original normalized circle and fixed coordinate derivative D.
Let v=sqrt(det h), kappa=h^{zz}>0, ell=D(v kappa)/v,
N=exp(-beta psi), s=D psi, d=b N v kappa. Use the FULL force Legendre
mass m=(v/N) f_pp>0 on its declared regular branch, aphi=1/m. No
clock-only kinetic substitute or new value of K_Q is introduced.

For the retained fast variables u=(delta Z,delta pi_psi), the self-block
at orders two and one is

    u_t=-A D^2 u+B D u+vadv D u+C u+f,
    A=[[0,kappa aphi],[-d,0]],
    B=[[0,-2 kappa D aphi-ell aphi],[D d-beta d s,0]],
    vadv=S^z-vphi.

C denotes local order-zero self terms. The source f includes the ordinary
coupling, actual other remainders and global/chart reconstruction; it is
not presumed independent, bounded in H1 or an externally prescribed force.
The source estimate remains part of the unclosed full system.

These are the raw self derivatives at fixed other canonical fields. They
are not an export of the final constraint-reduced nonconformal fast block.
Reconstructed metric responses in f may alter its derivative-order
identification; their order and bound must be proved in the full ordinary/
cross calculation. The conditional energy formulas below apply to the
displayed operator, not to an unverified identification of the complete
physical generator. No metric response is frozen or discarded from that
remaining task.

The first row follows directly by expanding -Delta_h(aphi delta pi_psi).
The second follows from the full clock-spatial regulator, including its
lapse-gradient term. Their exact geometric relation is

    (D d)/d=ell/kappa-beta s.

It holds on any positive planar metric, without future conformality.
Metric variation of the auxiliary and its paired gauge response still
contribute ordinary-to-force coupling; they are not set to zero here.

## Differentiated quartic weight and full local energy

H0=diag(d/kappa,aphi) is positive and H0 A is skew. Its energy-adjoint
first derivative vanishes:

    2 D(H0 A)+H0 B-B^T H0=0.

Commuting n spatial derivatives changes the first coefficient to B-n D A.
The correct highest-order weight is

    omega=sqrt(kappa d aphi), Hn=omega^n H0,
    2 D(Hn A)+Hn(B-n D A)-(B-n D A)^T Hn=0.

This is an exact all-integer identity for the displayed highest terms.
For n>1, the lower commutators must still be estimated; no nonlinear Hn
theorem follows merely from this identity. omega is the local quartic
principal frequency coefficient, not a physical cutoff or matched scale.

At one derivative put q=D u, B1=B-D A and
C1=C+D B+(D vadv)I. Then the exact differentiated equation is

    q_t=-A D^2 q+(B1+vadv I)D q+C1 q+(D C)u+D f.

Let Qj=D^2(Hj A)-D(Bj^T Hj)+Hj Cj+Cj^T Hj, with B0=B,C0=C.
The controlling energy Efast=mean(u^dagger H0 u+q^dagger H1 q)/2 obeys

    Efast'=mean[u^dagger W0 u+q^dagger W1 q]/2
            +Re mean[u^dagger H0 f+q^dagger H1((D C)u+D f)],
    Wj=(Hj)_t+Qj-D(vadv Hj).

The exact local spatial divergence is checked separately in the audit.
It retains the zero-order energy form as well as highest cancellation.
If the displayed coefficient norms are finite, a sufficient bound is

    Efast' <=(Kfast+1)Efast
              +mean(f^dagger H0 f+(D f)^dagger H1 D f)/2,
    Kfast=max_j ||Hj^-1/2 Wj Hj^-1/2||infinity
                 +||H1^1/2 (D C) H0^-1/2||infinity.

Time-weight drift and physical advection remain. This bound is conditional
on an actual admissible background and the full coupled source; it neither
constructs them nor proves the source is controlled by the energy.

## The full periodic cross-sector change at H1

Write X for the existing cross matrix S1, P=D^-1(I-mean), T=I+i P X.
For any matrix dimension, including the retained twenty directions,

    [D,T]=i P(D X), mean(TY)=mean(Y).

If ||T^-1||L2<=c and ||D X||infinity<=x1, then

    ||T^-1||H1<=c(1+c x1),
    ||T||H1<=1+||X||infinity+x1.

With the prior INITIAL bounds these are <2.880487 and <1.660305,
respectively. They are not future estimates. The inverse changes no
physical degrees of freedom and removes no mode, mean or zero-speed row.

For the owning principal convention G=-A2 D^2-i Bfull D, set
F=X A2, Q=X Bfull, Bd=blockdiag(Bordinary,Bfast),
Rmul=i D F+i A2 D X+Q-Bd X. The existing exact Rpre has commutator

    [D,Rpre]=multiplication(D Rmul)
              -2i mean(D^2 F .)-i P(D^3 F .)
              -mean(D Q .)-P(D^2 Q .)
              +(D Bd)mean(X .)+Bd mean(D X .).

In particular [D,mean(C .)]=mean(D C .), not zero. No finite-rank term
is discarded. If r0 bounds ||Rpre||L2 and r1 bounds this commutator, then

    ||Rpre T^-1||H1<=(r0+r1)c(1+c x1).

The commutator explicitly needs another coefficient derivative, e.g. D^3 F,
in this sufficient estimate. The old initial D^2 F certificate alone does
not supply it on a future nonlinear background. This is a remaining
estimate requirement, not proof of unavoidable physical derivative loss.
T_t, its commutators, physical advection and global-source derivatives must
also be controlled. The algebra does not export the actual nonconformal
ordinary/cross matrices or transport the fixed-I/U1 domain automatically.

## Weak-coefficient r energy: a sharper coupled estimate

Reuse the actual r equations and E_r of nonlinear-continuation V2. Here
A_r=N/v, B_r=N v kappa, F_r=N v partial_r V_rpot, u_r=D r.
Let mu=min(inf A_r,inf B_r)>0, Hmax=max(||A_r||infinity,||B_r||infinity).
The exact previous energy identity and ||f||infinity<=sqrt(5)||f||H1 give

    E_r' <=(Kr_weak+1)E_r+(||A_r||infinity/2)||F_r||H1^2,
    Kr_weak=max(||((A_r)_t-S D A_r)/A_r||infinity,
                ||((B_r)_t-S D B_r)/B_r||infinity)
             +3||D S||infinity
             +||D(A_r B_r)/sqrt(A_r B_r)||infinity
             +(2 sqrt(5)Hmax/mu)||D^2 S||L2
             +(sqrt(5)/mu)(||A_r||infinity ||D^2 B_r||L2
                              +||B_r||infinity ||D^2 A_r||L2).

For example, the troublesome term is bounded as
|mean(A_r p_z B_r,zz u_r)|<=sqrt(5)||A_r||infinity
||B_r,zz||L2 ||p_z||L2 ||u_r||H1. The other second-coefficient terms use
the same Holder/Young step. The r mean remains separately retained.
This improves a sufficient estimate; no equation or norm is silently changed.

### Actual metric and lapse coefficients

Assume k0 I<=h<=K0 I and use H1=||D h||infinity, H2=||D^2 h||L2,
Ht=||h_t||infinity, Pj=||D^j psi|| for j=0,1,2, with P0,P1 in
Linfinity and P2 in L2; Pt=||psi_t||infinity. Matrix Sobolev norms can
use the Frobenius norm. Put beta0=|beta|, Nmax=exp(beta0 P0),

    LA=beta0 P1+3 H1/(2 k0), LB=beta0 P1+5 H1/(2 k0).

Inverse/log-volume identities give the explicit sufficient bounds

    ||D^2 A_r||L2 <=Amax[LA^2+beta0 P2
                              +3 H2/(2 k0)+3 H1^2/(2 k0^2)],
    ||D^2 B_r||L2 <=Bmax[LB^2+beta0 P2
                              +5 H2/(2 k0)+9 H1^2/(2 k0^2)],
    max relative material time rate
        <=beta0 Pt+5 Ht/(2 k0)+||S||infinity LB,
    ||D(A_r B_r)/sqrt(A_r B_r)||infinity
        <=Nmax/sqrt(k0)[2 beta0 P1+H1/k0].

Here Amax=Nmax/k0^(3/2), Bmax=Nmax*K0^(3/2)/k0 are sufficient;
positive lower bounds use Nmin=exp(-beta0 P0),
Amin=Nmin/K0^(3/2), Bmin=Nmin*k0^(3/2)/K0.
The cancellation A_r B_r=N^2 kappa removes volume from the cross bound.

The relative inverse estimates follow from K=h^-1, kappa=e_z^T K e_z:

    |D kappa|/kappa<=H1/k0,
    |D^2 kappa|/kappa<=2 H1^2/k0^2+|D^2 h|/k0.

They use ||K e_z||^2<=kappa/k0. No initial conformality is used.
Thus spatial coefficient requirements can be supplied by h in H2 and
psi in H2 on a positive metric domain; the actual time-rate bounds must
still come from the full canonical Legendre equations on a uniform regular
branch. The new r energy alone does not control h, psi or their momenta.

The general-planar gauge inverse also supplies, conditionally on its
actual raw metric-rate triple bvec in H1,

    ||D^2 Svec||L2<=k0^-1||R D bvec||L2+(H1/k0^2)||R bvec||L2.

Here R=diag(1,1,1/2) and the full three-component shift gradient is retained.
The harmonic velocities have zero spatial derivative; their actual time
history still enters ||S||infinity and is not set to zero. Obtaining bvec
in H1 uses the full coupled canonical velocity map, not a prescribed shift.

### Condensate source

Let R0=||r||infinity, Q0=||(U,V)||infinity for the actual condensate fields,
Cmax=Nmax K0^(3/2), Lc=beta0 P1+3H1/(2k0). Then

    ||F_r||H1<=Cmax[(1+Lc)Lpot||r||L2+Jpot||D r||L2
                         +|g_r|R0 Q0||D(U,V)||L2],
    Lpot=|mr2|+|lambda_r|R0^2+|g_r|Q0^2/2,
    Jpot=|mr2|+3|lambda_r|R0^2+|g_r|Q0^2/2.

This retains both condensates and their gradients. H1 fields supply their
Linfinity bounds, but their actual evolution estimates remain required.
No thermal reservoir or external constitutive input is invented.

## Exact nonlinear curvature trace identity

In the existing gauge h=[[H,m],[m^T,c]], D m=D c=0, with G=H-mm^T/c,
the original weak-action Christoffel flux is exactly

    flux_curvature=-v kappa D log(det H).

Indeed its transverse coefficient matrix is
G^-1 m m^T G^-1/c^2-kappa G^-1=-kappa H^-1.
Replacing det H by det G is incorrect at nonzero mixed moduli. The raw
canonical lapse improvement contains -N MP2 flux_curvature/2, so its
current principal term in tau=log(det H) is

    -N MP2 v kappa D^2 tau/2.

This isolates the curvature trace geometrically without imposing equality
of the transverse eigenvalues. Frame-momentum derivative terms, nonlinear
lower terms and all current/momentum means still remain in the actual
inverse problem. This identity does not adopt a replacement physical or
Darboux chart, change the residual profile, fix a charge or divide out time.

## Evidence and next equation-level task

[Frozen contract](RES001_RTAU_COUPLED_REGULARITY_V1_CONTRACT_2026-11-19.md);
[weak-geometry specification](RES001_RTAU_COUPLED_REGULARITY_WEAK_GEOMETRY_V1_SPEC_2026-11-19.md).
[Main executable](../../../Analysis/MasterTests/test_rtau_coupled_regularity_v1.py):
23/23, 492 source pins; receipt SHA-256
`6bf27cb5d4f5caa584b64d73fde2f50721da2d5921378eb2017803e072c83d3c`;
byte-identical replay.
[Separate extended audit](../../../Analysis/MasterTests/audit_rtau_coupled_regularity_v2.py):
28/28, 497 pins; receipt SHA-256
`6b432a8781afe3bb9773b017c03be4a98f76c63acbbe549558bb8b1ae3886790`;
byte-identical replay. Its earlier successful 19-check version is preserved.

The audit independently derives the differentiated-weight ODE, verifies the
full spatial energy divergence, and checks the inverse geometry and direct
Christoffel flux. Exact noncommuting Fourier fixtures retain convolution
tails and finite-rank mean terms. These are same-assistant mathematical
controls, not independent external review, a numerical nonlinear background
solution or a second full general-metric Hessian export. Norm inequalities
are analytic conditional estimates; no future constants were measured.
Original source bytes, sidecars and mtimes are preserved.

Next derive the general-planar ORDINARY Ward/Schur principal system and its
two cross blocks from the full action, checking the actual physical
constraints rather than substituting into old conformal matrices. Then
test the positive controlling complement and zero-speed partners, and the
full H1 actual remainder with moving Green/range/charge/gauge reconstruction.
The new fast weight, periodic commutators, weak r estimate and curvature
identity are reusable prerequisites; they should not be recalculated as
another initial-constant sweep. A genuine nonlinear compatible background
and energy tube, G1-G6 and physical interactions/window remain incomplete.
MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED. No manuscript/site edit,
vault mutation, dispatch, publication, commit, push or deployment occurred.


## Scope clarification and preserved draft

The [V1 mathematical draft](RES001_RTAU_COUPLED_REGULARITY_V1_REPORT_2026-11-19.md)
is preserved with its original sidecar. V2 makes the raw-self versus final
constraint-reduced operator distinction explicit. All equations, receipts,
checks and numerical bounds are unchanged; no additional physical clearance
is asserted. Scientific acceptance remains with the live gate owners.
