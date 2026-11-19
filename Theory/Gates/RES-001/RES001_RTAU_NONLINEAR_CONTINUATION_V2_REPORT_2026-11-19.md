# A09.2 nonlinear continuation: norm obstruction and higher-energy component

19 November 2026. Conditional mathematical result. R-tau remains UNADOPTED.
Full background/operator/energy continuation remains OPEN; [0,0.05] is a
target, not a certified interval. Review DEFERRED; physics_pass=false;
gate_effect=NONE. No change to the original R4C1 action or its findings.

## What the calculation decides

The existing linear mixed-energy estimate does not, by itself, provide the
nonlinear continuity needed for a direct continuation argument on the
unreduced canonical product chart. The actual action contains a neutral
momentum square which is not controlled in L2 by an L2 momentum norm.
This also obstructs continuity of the current operator H2->L2 on that
product topology. Exact momentum-range correction does not remove it.

A stronger-topology estimate is available for that term. The calculation
also derives a conditional first-spatial-derivative energy for the actual
neutral-scalar canonical equations, with the metric/lapse/shift and
condensate sources retained. These are concrete continuation prerequisites,
not a complete coupled nonlinear theorem or a physical instability result.

The previously completed initial operator derivative <102.128 is preserved.
It is not integrated as if it were a future uniform bound.

## Actual scalar term and the full Schur trace

Let r be the neutral scalar, slot 11, and p its canonical momentum density.
Write v=sqrt(det h), S=S^z, and V_rpot for its potential contribution. The
full action's canonical scalar term, including its spatial gradient, is

    L_r=v(r_t-S r_z)^2/(2N)-N v[h^{zz} r_z^2/2+V_rpot],
    p=v(r_t-S r_z)/N,
    I_r=-N p^2/(2v)-N v[h^{zz} r_z^2/2+V_rpot].

The lapse-improvement flux F_lapse has no r or p_r dependence. All other
action sectors remain present in the full-action controls; no potential,
frame, force, curvature or regulator contribution is switched off there.

For h=[[H,m],[m^T,c]], G=H-mm^T/c and delta G=G f, retain

    delta v=v f, h^{zz}=1/c+chi,
    chi=m^T G^-1 m/c^2, delta h^{zz}=-chi f.

The complete scalar contribution to the trace's zero-order coefficient is

    a0_r=N p^2/(2v)-N v[r_z^2/(2c)+V_rpot].

At fixed configuration, the EXACT finite increments are

    Delta I_r=-(N/v)[p delta p+(delta p)^2/2],
    Delta a0_r=+(N/v)[p delta p+(delta p)^2/2].

The scalar temporal Hessian is v/N and has no cross-rate entries. This
separability lets the momentum increment be applied without changing any
other canonical momentum before the separate momentum-constraint repair.
On the prepared initial profiles N/v>0.9997425675813890. This is a positive
initial coefficient bound, not a future one or a full kinetic-signature test.

## An all-frequency concentration obstruction

Use normalized period-2*pi means and the smooth real trigonometric sequence

    S_N(z)=sum_{k=N}^{2N-1} cos(k z),
    mean(S_N^2)=N/2,
    mean(S_N^4)=(2N^3+N)/8.

For the fourth moment, the difference-frequency coefficients of S_N^2
are (N-d)/2, d=1,...,N-1, its mean is N/2, and the sum-frequency
coefficients are the triangular counts divided by 4. Their supports are
disjoint. Parseval and sum_{j=1}^{N-1}j^2 give the displayed identity for
EVERY positive integer N; the finite exact controls are supplementary.

Set N=m^8, f_m=m^-5 S_N for positive integer m. Then

    ||f_m||L2^2=1/(2m^2) ->0,
    ||f_m^2||L2^2=m^4/4+1/(8m^12) ->infinity.

Its input mean is zero. Removing the output mean subtracts only
1/(4m^4) from the second displayed squared norm, which still diverges.
For any fixed smooth background p0 and positive bounded c0=N/v,

    ||c0[p0 f_m+f_m^2/2]||L2
       >= (inf c0)/2 ||f_m^2||L2
          -||c0 p0||infinity ||f_m||L2 ->infinity.

Thus the canonical density map into L2 is not continuous at p0 on the
unreduced free-momentum L2 topology. There is no uniform quadratic L2
product bound to supply an ordinary Banach implicit-function argument on
that open product space. Fixed smooth spatial configurations do not fix it.

For the trace operator, test its increment on the constant trace function
1, whose H2 norm is 1. The same growing zero-order term occurs. This test
does not delete the constant mode or treat it as a physical eigenmode.

## Momentum constraints, charges and limits of the counterexample

This is more than an arbitrary nonperiodic source. On a fixed smooth
general-planar configuration, orthogonally project f_m away from the finite
span of 1 and r_z, discarding redundant basis elements. Call the result g_m.
Then mean(g_m)=mean(g_m r_z)=0, ||g_m||L2<=||f_m||L2, and

    ||g_m-f_m||infinity<=C_span ||f_m||L2,
    ||g_m^2-f_m^2||L2<= (2 C_span+C_span^2)||f_m||L2^2 ->0.

These follow from the finite smooth Gram inverse and Holder; the divergent
square survives the correction. The source delta j=e_z g_m r_z has exactly
zero mean. With the same weighted momentum means eta, the existing exact
momentum solve gives

    delta e=A[P(delta j)-Nmean^-1 mean(Omega A P(delta j))],
    A=Bmetric^-T, Nmean=mean(Omega A).

Here P is the mean-free primitive and Bmetric=W h, distinct from the scalar
energy coefficient B below. Using P:L2->H1 with norm <=sqrt(2) and the
explicit H1 embedding below,

    ||delta e||infinity
       <=alpha[sqrt(10)+nu omega alpha] ||r_z||infinity ||g_m||L2 ->0,

where alpha=||A||infinity, nu=||Nmean^-1||, omega=||Omega||infinity.
The momentum constraints and their weighted means are therefore repaired
without an unbounded compensating eliminated momentum. The auxiliary
relation is unchanged because all configurations are fixed. The other
local Legendre/current terms vary continuously with this small eliminated
momentum on the regular background branch; F_lapse has no eliminated
metric-momentum dependence. In the trace map, t and s use the fixed free
metric momenta; the remaining eliminated-momentum feedback is order zero
and small. It cannot cancel the growing scalar square.

This family is NOT asserted to satisfy the full fixed-I/U1 nonlinear
admission problem or to be solutions of the time equations. In particular,
the nonlinear density is itself one possible reduced coordinate: its large
change is not a small perturbation in every possible nonlinear reduced
chart. Removing an output mean is not a construction of fixed-charge data.
The obstruction concerns the direct unreduced product-space argument;
it does not disprove a better reduced chart, a stronger regularity theorem,
or the existing linear estimates on compatible tangent data.

## A sufficient stronger term estimate

For the normalized Fourier H1 convention, Cauchy-Schwarz gives

    ||f||infinity<=sqrt(sum_n 1/(1+n^2)) ||f||H1 <sqrt(5)||f||H1.

Indeed sum_{n>=1}1/n^2<=1+integral_1^infinity x^-2 dx=2. Consequently

    ||c(p^2-q^2)||L2
       <=sqrt(5)||c||infinity (||p||H1+||q||H1)||p-q||L2.

A uniform H1 momentum bound is sufficient for this term's Lipschitz control.
If c also changes, add
sqrt(5)||c-c0||infinity ||p0||H1 ||p0||L2 to the corresponding finite-increment
bound. This is a sufficient component estimate, not a claim that H1 is the
minimal space or that the rest of the full system closes there. Frequency-
band counting also excludes a generic Hsigma-to-L2 square bound for
0<=sigma<1/4; no endpoint theorem is assumed.

## Actual neutral-scalar higher-energy calculation

To pursue the stronger requirement rather than only name it, put

    A=N/v, B=N v h^{zz}, C=N v, u=D r, F=C partial_r V_rpot.
    r_t=S u+A p,
    p_t=D(S p+B u)-F,
    u_t=D(S u+A p).

Here u means D r, not the condensate field bearing the same letter.
The actual potential derivative retains the condensate U,V fields:

    partial_r V_rpot=mr2 r+lambda_r r^3+(g_r/2)(U^2+V^2)r.

For positive A,B define the controlling component energy

    E_r=mean[A(p^2+p_z^2)+B(u^2+u_z^2)]/2.

Let Da=A_t-S A_z, Db=B_t-S B_z. Exact differentiation and periodic
integration by parts give

    E_r'=mean[(Da+A S_z)p^2/2+(Db+B S_z)u^2/2
              +(Da+3A S_z)p_z^2/2+(Db+3B S_z)u_z^2/2
              +(AB)_z p_z u_z
              +A p_z(S_zz p+B_zz u)+B u_z(S_zz u+A_zz p)
              -A(p F+p_z F_z)].

The local difference before integration is exactly the derivative of

    S[A(p^2+p_z^2)+B(u^2+u_z^2)]/2+AB(p u+p_z u_z).

No coefficient time derivative, second spatial derivative, shift term or
condensate source is suppressed. A sufficient conditional scalar bound is

    E_r' <=(K_r+1)E_r+(||A||infinity/2)||F||H1^2,
    K_r=max(||Da/A||infinity,||Db/B||infinity)+3||S_z||infinity
        +||(AB)_z/sqrt(AB)||infinity+||S_zz||infinity
        +||A_zz sqrt(B/A)||infinity+||B_zz sqrt(A/B)||infinity.

Weighted Cauchy/Young inequalities give each term. If A,B>=mu>0,
E_r>=mu(||p||H1^2+||u||H1^2)/2. The retained mean obeys

    |mean(r)_t|<=sqrt(2/mu)(||S||infinity+||A||infinity)sqrt(E_r),
    ||r||H2<=|mean(r)|+sqrt(2)||u||H1.

This supplies conditional control of the precise neutral momentum/gradient
regularity exposed by the obstruction. It does NOT close the coupled
background: A,B,S and F are actual metric/lapse/shift/condensate quantities,
and their displayed uniform norms must be produced by the other equations,
the constraints and their common domain. No such future bounds, autonomous
solution or positive time interval are supplied here.

## Evidence, correction and next task

[Contract](RES001_RTAU_NONLINEAR_CONTINUATION_V1_CONTRACT_2026-11-19.md),
[Schur correction](RES001_RTAU_NONLINEAR_CONTINUATION_V2_SPEC_2026-11-19.md),
[energy specification](RES001_RTAU_NONLINEAR_CONTINUATION_ENERGY_V1_SPEC_2026-11-19.md).
[Main V2](../../../Analysis/MasterTests/test_rtau_nonlinear_continuation_v2.py):
45/45 controls, 482 pinned sources; receipt SHA-256
`62b41a6c8e3bd494c27fa28c8acaa5ad2a03d4f50ac5d80c54d8b6e2bd577434`;
byte-identical replay. Full-action current/trace defects are below 2.262e-48
against the unchanged 1e-28 tolerance. This is numerical identity verification,
supplementing the exact derivation, not a background solution.

[Separate audit V2](../../../Analysis/MasterTests/audit_rtau_nonlinear_continuation_v2.py):
47/47, 487 pinned sources. It independently extracts the original scalar
kinetic term, derives the full Schur geometry, counts ordered Fourier
quadruples, checks nonorthogonal range projections, and verifies the exact
variable-coefficient higher-energy divergence and omission controls.
It is same-assistant mathematical verification, not external peer review or
a second full nonlinear background solve. Its predecessor V1 (36/36) is
preserved. Original source bytes, sidecars and mtimes are unchanged.
Audit receipt SHA-256:
`6daec0d9cc82c7386891dd2045d8abfaa84a8234100f953f9c234a907d1e9000`;
byte-identical replay.

Primary V1 (45/45) is preserved too: its volume-only exact fixture was valid
only in the block-diagonal case. V2 includes the missing h^{zz} Schur drift.
Every full-action numerical control and concentration example is identical
between V1 and V2. Positive check counts did not establish that geometric
generalization; the independent derivation exposed and corrected it.

Next derive a coupled higher-regularity continuation estimate with the
actual metric/frame/condensate/quartic-force equations and constrained trace
reconstruction, using this r-component estimate as a prerequisite. First
test whether their differentiated equations control the coefficient/source
norms in K_r and ||F||H1 without derivative loss. Retain moving weighted
means, residual profile, charges, gauge and physical moduli. If that fails,
identify the precise commutator/domain obstruction rather than assume a
coefficient history. Do not repeat the completed initial-drift calculation.

G1-G6 INCOMPLETE; MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED.
Physical interactions/window, healthy GR and identifying matching remain
open. No action adoption, manuscript/site edit, vault mutation, provider
dispatch, publication, commit or push occurred.
