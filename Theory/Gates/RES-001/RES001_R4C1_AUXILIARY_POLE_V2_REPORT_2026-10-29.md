# G1 auxiliary time-tangent pole: controlled local source balance

29 October 2026. **Conditional; Rule-9 DEFERRED; physics_pass=false;
gate_effect=NONE. G1-G6 INCOMPLETE.**

## Result and scope

For the unchanged R4C1 registered B1-frame preparation eta=1/4, e=1/500,
k=40, the previously observed auxiliary third-time cusp is now supported by
an explicit uniform remainder, rather than a fit to two offsets. Write
w=e cos(kz), jZ=partial_t^3 Z, and Delta for physical minus analytic-cubic
bookkeeping summand on the SAME initial fields, root and shift. This partition
does not adopt the A=0 summand as another physical background.

For 0<abs(w)<=1/1000, the initial original-action source balance gives

    abs(b*w^2*Delta(jZ) - K_Q*(9/560000)*abs(w)) <= B*abs(w)^3,
    B = 1927536082735036880015940019757805352398092566414841913058650736971841670703669
        / 68655800230791820854453946816333851426119512673825377484800000000000.

Thus B<28100000000 and

    abs(abs(w)*Delta(jZ) - 297/2800000) <= (B/b)*w^2.

The largest admissible dyadic radius selected by the frozen inequality
2*B*r^2<=K_Q*(9/560000) is r=2^-27=1/134217728. On that smaller range,

    Delta(jZ) >= (297/2800000)/(2*abs(w)).

The radius is a conservative mathematical proof neighborhood in the declared
dimensionless chart, not a physical length, momentum window or EFT cutoff.
Its small size reflects a loose complement-jerk bound, not a prediction of
where an observable effect begins. K_Q=3/4, b=5/44, A=1/28, beta=1/40 and
p=1/20 here are the already declared diagnostic values; this does not identify
microscopic K_Q, V, C_chi or a0.

## Original-current derivation

Differentiate the varied current before inserting the initial profiles:

    Pi_psi^mu = K_Q*n^mu*(n.grad psi)
                -3*A*sqrt(Y)*h_projected^(mu nu)*grad_nu psi
                -b*h_projected^(mu nu)*grad_nu Z - b*Z*a^mu,
    E_psi = -Dt(sqrt(h)*Pi_psi^0)-Dz(sqrt(h)*Pi_psi^z)
            -beta*sqrt(h)*rho.

The temporal regulator density is
-b*sqrt(h)*(c*Z_t-c*R*Z_z+Z*a0), c=h_yy*V_y^2,
a0=h_yy*V_y*(V_y,t-R*V_y,z)+V_y^2*(h_yy,t-R*h_yy,z).
Vary the generic metric/frame velocities and gradients first. On the initial
slice its acceleration coefficients are C_hyy=-b*Z*w^2, C_Vy=-b*Z*w,
C_Z=-b*w^2. The executable records the spatial current and every lower
coefficient AR_i, BR_i, retaining metric-volume and shift drift. In particular

    AR_Z=b*w^2*(-12*H+5*HB+Rprime+3*T*wprime),
    BR_Z=2*b*w^3*T, T=R/w.

The complete differentiated scalar balance is

    b*w^2*Delta(jZ) = Q - CUB + sum_i AR_i*Delta(a_i)
                     + sum_i BR_i*Delta(a_i,z)
                     + C_y^T*Delta(j_y) + beta*Delta(Dt(sqrt(h)*rho)),
    Q=K_Q*((1+w^2)*Delta(jPsi)
          +p*(w^2*Delta(a_hyy)+2*w*Delta(a_Vy))
          +(1+w^2)*p*trace(Delta(a_h))/2).

Here i runs over the four active metric/frame cusp channels and Z; all twelve
complementary third-time channels are retained in C_y^T*Delta(j_y). CUB is
the full physical cubic-current time derivative, including volume, projector,
scalar spatial derivative and frame/metric acceleration terms. Its normalized
expression CUB/abs(w)^3 is exported, not discarded by source counting.

The inherited exact complement response is Delta(a_y)=sign(w)*r(w), with
r_h=O(w^3), r_Vy=O(w^2), and

    Delta(jPsi)=sign(w)*jpos(w)=abs(w)*F(w), F(0)=9/560000.

The initial auxiliary response is Delta(aZ)=abs(w)*Qz, with Qz and its full
normal derivative exported. Consequently Delta(aZ,z) includes the bounded
sign(w)*wprime*Qz term; it is not assigned an extra vanishing order.
The dust quotient/current is retained:

    Delta(rho)=2*A*p^3*abs(w)^3,
    Delta(rho_t)=Delta(rho)*(3*T*wprime-3*H+Rprime+beta*p).

Its contribution includes the volume derivative 3*H*Delta(rho). The source
identity agrees independently with all ten sealed full-action time-tangent
datasets; this numerical control supports, but does not replace, the bound.

## Uniform remainder and omissions audit

All rational normalized source functions are exactly cancelled before their
node denominators are tested. Outward 80-digit interval evaluation retains
the parent root/initialization enclosures and all signs. No root residual is
manually set to zero. The exact generic mixed derivative coupling aZ,z to a
complement row vanishes: derivatives of Z pair only with derivatives of psi.
This structural identity is also checked against all twelve complement
channels in each of six original full-Hessian exports.

The analytic physical density is quadratic in the first derivatives. Its
coefficient bounds use complex first-jet polydiscs of radius delta=1/1000
around every registered initial point. The common exact disk enclosure has
metric centers h=I, amplitude/radion centers 1/2, V_y and Z radii 2/1000,
velocity radii 2+delta, and spatial/shift radii 1+delta. The corrected phase
velocity lies in that velocity enclosure; it is not an amplitude displacement.
All 112 inverse and four square-root operations remain in their analytic
domains. The exact rational absolute action bound is below 53, giving

    H2=2*53/delta^2=106000000,
    H3=6*53/delta^3=318000000000.

With initial coordinate-velocity l1 bound 32 and spatial/shift-derivative
bound 20, use Acoef=2*H2+84*H3 and Bcoef=2*H2. The parent complement inverse
norm is below 25. The receipt exports Ma,Md,Mz,Mzz,CF,JF and the resulting
Mj<246806944172267, so abs(Delta(j_y))<=Mj*abs(w). Initial curvature's
first time derivative has zero partition difference: the two partitions
share initial h, h_z, h_t and h_tz. Initial dust spatial stress and its first
time derivative vanish upon imposing its clock constraint and its time
derivative; density and multiplier changes are not omitted in the scalar row.
These are initial-slice statements, not future flatness or pressure assumptions.

Rounded values below are explanatory; the receipt retains exact outward
rational bounds used in the proof.

| Source in B | Bound, approximately |
|---|---:|
| Quadratic remainder | 0.000006484114 |
| Full cubic current | 2.574139512 |
| Regulator acceleration and spatial derivative | 0.035997829 |
| Physical matter/volume current | 2.922768e-10 |
| All complement third-time jets | 28075356722.61153 |

## Physical jet, gauge and regularity interpretation

The analytic bookkeeping summand is a single meromorphic initial expression
near each simple node: its coefficients and prepared profiles are analytic,
the complement inverse is regular, and the remaining inverse has only finite
powers of w. Higher meromorphic poles cannot cancel a 1/abs(w) cusp; a
simple residue a/w would require both a+C=0 and a-C=0, with C=297/2800000>0.
Thus both sides of a node cannot become locally integrable by adding that
analytic summand. Since abs(wprime) at either node is 2/25, the conclusion
holds in the spatial coordinate as well.

Free second-time shift jets and their spatial derivatives remain available.
The original auxiliary row has zero direct shift source. Their scalar
response divided by b*w^2 is regular; its relevant quotient is
w*(3*U+5*W*w^2)*wprime. Bounded gauge jets therefore cannot cancel this pole.
No singular gauge is selected.

This excludes a continuation with a locally integrable third-time Z trace,
enough off-node regularity to differentiate the Euler equations once, unit
lapse and bounded second-time shift jets, for this preparation. It does NOT
exclude every C2 or distributional weak continuation. In particular the
singular derivative enters the scalar time-mass row multiplied by w^2;
weighted weak admission requires a separate analysis. No actual evolution,
node/domain persistence, physical normalization/window or matching follows.

## Reproducibility, failed guard and next route

Contract: [frozen V1 contract](RES001_R4C1_AUXILIARY_POLE_V1_CONTRACT_2026-10-29.md).
Executable: Analysis/MasterTests/test_01_r4c1_auxiliary_pole_v2.py.
Receipt: Analysis/MasterTests/outputs/r4c1_auxiliary_pole_v2_attempt_01/summary.json.
Receipt SHA256: 048c5a18417cc6abead66bb80cc3999e697dc67a001a5d2287349e1cb2a66e0e.
79/79 checks, no failed/unknown rows, 231 source pins; READ_ONLY_REPLAY_EXACT.

V1 and its 77/78 failed receipt remain unchanged. Its denominator guard
inspected a rational expression before exact cancellation. V2 adds an exact
identity check and applies the same guard after cancellation; equations,
domain and tolerances are unchanged. See the [implementation note](RES001_R4C1_AUXILIARY_POLE_V2_IMPLEMENTATION_NOTE_2026-10-29.md).
The older time-tangent candidate flags and NOT VALIDATED working note retain
their historical meanings; this new proof does not rewrite them.

Next inspect the original kinetic weighting and nodal distribution kernel
before treating the unweighted regularity obstruction as a weak-solution
failure. Do not choose a finite-part prescription, new state, cutoff, parent
or future boundary condition automatically. G1-G6 and substantive upstream
holds remain; provisional use is permitted under deferred Rule-9 policy.
