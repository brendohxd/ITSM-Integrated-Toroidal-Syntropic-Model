# Quartic transport: scalar jerk has a controlled node cusp

27 October 2026. Conditional / scoped regularity exclusion; review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE. G1-G6 INCOMPLETE.

## Result and scope

For the registered unchanged-action B1 eta=1/4,e=1/500,k=40 quartic initial
data and initial gauge N=1, shift time jets0, the differentiated original
regulator requires a nonzero cusp in the scalar third-time jet j=psi_ttt.
Its cusp component satisfies, uniformly over the registered root box,

    j_cusp = (9/560000)*|w| + remainder,
    |remainder| < 0.00011395*|w|^3,  |w|<=1/1000,

in reference units. This is not an observational acceleration, a frequency,
a cutoff or a matched microscopic coefficient. No angular limit was fitted.

A scalar which is jointly C4 in this initial coordinate neighbourhood would
need a continuous normal derivative of psi_ttt. The nonzero |w| term is
incompatible with that requirement. This excludes THAT stronger regularity
class for THESE data/gauge. It does not exclude every initial state, gauge,
weaker classical or distributional solution, R4C1 or ITSM.

The [bounded continuous initial acceleration result](RES001_R4C1_QUARTIC_INITIAL_ACCELERATION_V1_REPORT_2026-10-27.md)
remains unchanged. Continuous initial second derivatives do not imply a
jointly C4 scalar or an evolved solution. C4 was one sufficient smoothness
class in earlier compatibility derivations; it is not automatically required
by the physical action. The new result does NOT bar provisional investigation
of a justified weaker graded regularity class.

The cusp component itself is locally Lipschitz, with different one-sided
normal derivatives. Establishing the regularity of the TOTAL j still requires
checking possible analytic quotients and other transport constraints; no
weaker solution or full third-time system is certified here.

## 1. Differentiate the actual regulator, keeping gravity and volume

Use E_Z/b=Z+div(hp*grad psi)-acc.grad psi, hp=g_inverse+n*n. The corrected
general coefficient of psi_t includes the volume-gradient term
(gamma*Vz-c*R)*partial_z(log sqrt(h)); it is retained in the independent
coordinate implementation. Its value and first-time variation vanish on this
initial homogeneous-metric-velocity slice only, not in general evolution.

Let ay denote all twelve coordinate metric/frame/condensate/reservoir
accelerations and R the actual initial shift. Off-node the initial equation
partial_t(E_Z/b)=0 gives

    j = -Ud-(5H-3Hbg-Rprime-R*wprime/w)*aPsi
        +2R*partial_z(aPsi)
        -p*[ay[Vy]/w+trace(ay[hdiag])/2+Hbg^2-8H*Hbg
             -2*(H-Hbg)*(Rprime+R*wprime/w)].

This is a necessary differentiated-regulator equation, not the complete
third-time evolution system. Ud is the declared initial Zdot/w^2; no future
polynomial Z or Zdot profile is imposed. No g=0 inversion is used.

For the cusp response at fixed initial fields/velocities, c_tt changes by
w^2*delta(hyy_tt)+2w*delta(Vy_tt), and l_tt changes by
trace(delta(h_tt))/2. The explicit K_ij V^i V^j derivative cancels the
first hyy contribution, leaving

    delta C_t = w*delta(ay[Vy])+w^2*trace(delta(ay[hdiag]))/2,
    delta j = -p*[delta(ay[Vy])/w+trace(delta(ay[hdiag]))/2].

The trace is not discarded and metric accelerations are not frozen. All
six metric and three frame second jets remain in the coordinate controls.
The full time-equation identity, not just this response, is independently
checked against the four-metric, normalized n, connection acceleration and
volume-weighted divergence.

## 2. Coupled coefficient and explicit remainder

The accepted exact complement gives ay_cusp=B(w)^-1*fy_cusp. Its original
cusp sources are the previously derived three diagonal metric forces
proportional to |w|^3 and the frame force -3*A*p^3*w*|w|.
Exact kinetic conjugation under w->-w proves inverse-entry parity. At w=0,
B0inv[Vy,Vy]=24 and its metric/Vy crosses vanish. Therefore

    leading(j_cusp) = 3*A*p^4*24*|w|
                   = 72*A*p^4*|w| = (9/560000)*|w|.

The trace and off-diagonal coupled effects enter the controlled remainder.
With I>=sup||B^-1||, interval matrix bounds give

    sup||Bprime|| < 0.050134, sup||Bsecond|| < 0.091717,
    J1=I^2*sup||Bprime|| < 29.016118,
    J2=2I^3*sup||Bprime||^2+I^2*sup||Bsecond|| < 123.076414.

Inverse-entry parity and Taylor's theorem bound the cubic jerk remainder by

    A*p^4*(3*J2/2+15*J1/2+9*I/2)*|w|^3
      < 0.00011395*|w|^3.

The remainder consists of explicit analytic inverse coefficients multiplying
cubic absolute powers; it is not an arbitrary oscillatory error. Its normal
first derivative vanishes at the node. The leading |w| coefficient is
strictly positive in outward interval arithmetic. Both node orientations
are retained; |w|=|sigma*x|+O(|x|^3), |sigma|=2/25.

The remaining analytic-part forcing is analytic before its removable or
meromorphic node quotients. Such an analytic/Laurent contribution cannot
cancel a nonzero two-sided |w| term. A jointly C4 candidate would first have
to eliminate any analytic pole, and would still encounter this cusp. We do
not assume those possible poles are already eliminated in a weaker class.

## 3. Verification and preservation

- Jerk transport V2 passes38/38 exact/interval/coordinate controls. Eight
  independent Taylor-geometry controls cover signed w/e=-1,-1/2,1/2,1 and
  both normal slopes, with arbitrary metric/frame second jets and gradients.
  Full time-equation, actual coupled cusp response and compensating jerk
  discrepancies are below7.00e-106 normalized, against1e-30 acceptance.
  The uncompensated change exceeds the frozen1e-25 rejection threshold.
- Coupled numerical responses in the stated node domain lie within the proved
  cubic bound; those controls do not replace the interval argument.
- A fresh READ_ONLY_REPLAY_EXACT recomputes the receipt.144 source artifacts
  are pinned. Same-author independent methods are not independent peer review.
- V1 stopped before a receipt because exact-zero matrix derivative entries
  were Python integers rather than interval scalars. V2 embeds every entry
  into the same interval type before norm accumulation. V1 source, sidecar
  and full ignored failure log are preserved; no equation or criterion changed.

Receipt: Analysis/MasterTests/outputs/r4c1_quartic_jerk_transport_v2_attempt_01/summary.json,
SHA256 426c6e781f7f113771d9afd92a9fc83aa968409246360a7f367ab8f1ab252e63.
Its exact formulas, coefficients, outward binary endpoints and all controls
remain available. The earlier TRANSPORT_WORKING_ALGEBRA note is untouched;
this report supplies the accepted evidence for its tested response/coefficient.

## Next supported route

Continue same-action G1 with the weaker mixed-regularity assessment: establish
the analytic part of j and ay[Vy]/w at the node, identify the actual admissible
graded spaces, and formulate constraint/charge transport there without illegal
trace differentiation. Derive any distributional interface terms explicitly.
Do not force C4 smoothness, continually project onto a graph, or infer weak
existence/uniqueness or persistence from these initial jets. G2 only proceeds
when its actual background prerequisites are justified.

Inherit all initial-root, acceleration, cusp, full-geometry/action and scalar
review dependencies. PROCEED_PROVISIONALLY for these scoped results and the
weaker-space investigation. HOLD_SUBSTANTIVE for a jointly C4 continuation of
these registered data/gauge and for claims needing actual admission/IVP.
Stage2 INCOMPLETE; Stage3 NOT_ENTERED; MAT-001 BLOCKED; K_Q NOT_DERIVED;
V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED. No parent/state
adoption, vault mutation, dispatch, publication, commit/push or deployment.
