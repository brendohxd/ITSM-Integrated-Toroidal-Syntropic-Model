# R4C1-G3V: coupled transverse constraint and vertex-regularity test

Date: 2026-10-08. Owner: Master Test 1 / conditional R4C1-v1 / G3.
Frozen after analytic planning, before executable covariance/constraint
checks and numerical sampling. Review DEFERRED, Rule9_cleared=false,
physics_pass=false, gate_effect=NONE.

## Purpose and decision boundary

G3I left metric/force/dust effects out of its frame-scattering probe.
Before constructing full ordinary cubic/quartic exchange diagrams on G3,
test that the constrained finite-density action has the necessary Taylor
vertices. The unchanged action and older Track-A report already warn that
Y^(3/2) is nonanalytic at Y=0. This task tests its physical, metric/dust
constrained pullback on the ACTUAL G3 backgrounds; it does not announce that
old property as a wholly new discovery or assume constraints remove it.

If a nonzero |epsilon|^3 term survives regular constraint reduction, ordinary
background-independent trilinear Taylor vertices are unavailable in that
direction. Report that substantive obstruction; do not smooth the operator,
invent a cubic vertex, omit it or transfer G3I's scattering amplitude to the
finite-density background. This is not a no-go for classical evolution,
a nonanalytic perturbative prescription, another background or all actions.

## Frozen calculation

1. Use full R4C1-v1, the unchanged six-member G3 family and pinned background
   arrays. Signature (-+++), spatially flat FRW, physical transverse frame
   tilt w_y(t,z), transverse physical shift B_y(t,z), gamma_ij=a^2 delta_ij.
   Keep the exact ADM unit parametrization with N retained:
   U^0=sqrt(1+w_y^2)/N,
   U^y=(w_y-B_y sqrt(1+w_y^2)/N)/a.
   Scalar/vector/tensor decomposition is around the isotropic on-shell
   homogeneous background. Do not freeze the transverse shift.
2. Contract all four frame invariants with the full metric connection through
   second order, including a_dot=a H. Add Einstein ADM/GHY bulk density and
   every relevant matter/condensate/reservoir/alignment/force/regulator block.
   Homogeneous scalar/dust gradients have no transverse shift source; prove
   that from their actions. Retain the force Q and current-alignment
   quadratic mass terms and verify the first regulator variation, not an
   imported vacuum force formula.
3. Impose the dust multiplier equation in the pure spin-1 direction:
   delta_tau=delta_psi=0 at first order, so delta_N=0. Derive and solve the
   nonzero-mode transverse shift equation. Check its rank denominator,
   lapse/shift time-derivative absence, kinetic coefficient and gradient
   coefficient. Compare the flat/zero-background control with G1 only as
   a control. Do not call the full interacting action equal to that vacuum
   control. Export any H w wdot and H^2 w^2 terms before integration by parts.
4. Derive the transverse linear equations, including the full G3 background
   flow when differentiating coefficients; export the resulting canonical
   quadratic mass/friction. Positive kinetic is not a full stability claim.
   The local physical kinetic normalization f^2 is expected to remain
   M_U^2(c1+c4)=eta M_P^2/6; retain any mismatch.
5. Compute Y and Delta psi from the exact covariant projector/connection,
   with psi_bar_dot retained. Show or reject
   Y=psi_bar_dot^2 w_y^2/N^2 for homogeneous psi in this chart.
   Derive Delta_0, Delta_1 and Delta_2. Eliminate the regulator auxiliary
   from its defining bulk equation, keeping its induced quartic direct term;
   do not pretend this is the complete quartic constrained action.
6. For w_y=epsilon W cos(kz), spatially average the leading exact force term
   using <|cos|^3>=4/(3 pi). Test the expected cubic-amplitude functional
   -a^3 A |psi_bar_dot|^3 |epsilon W|^3*4/(3 pi).
   Obtain its coefficient in both local V=f w and comoving X=a^(3/2) f w.
   Do not assign a multilinear vertex to this even degree-three functional.
7. Prove its leading cubic coefficient is independent of first-order
   lapse/shift/dust/regulator auxiliaries. Apply stationary elimination:
   regular second-order auxiliary corrections cannot change the cubic
   coefficient when the linear constraint equations hold. State the
   smoothness/rank assumptions and limits; no complete J2/J3 solution or
   full quartic Schur complement is claimed. If elimination instead cancels
   the cusp, retain that result and revise the scientific disposition.
8. Compute left/right third derivatives at epsilon=0. For a nonzero positive
   coefficient C, test F'''(0+)=-6C and F'''(0-)=+6C, and the evenness that
   makes a symmetric odd finite difference falsely suggest zero. Exact A=0
   and psi_dot=0 transverse controls remove this term. At psi_dot=0, test
   separately a retained finite-k force-gradient direction using S1's
   Y2=(grad(delta_psi)/a+psi_dot*w)^2. That prevents a zero transverse
   coefficient being mistaken for C3 regularity of the entire action.
9. Frozen numerical grid: eta=(1,1/4,1/16,1/64,1/256,1/1024), both archived
   methods, t=(0,.5,1,2,3,4), k=(20,40,80). Export every background event,
   ranks, kinetic/gradient/mass and cusp coefficients, including zero cases.
   Verify inherited on-shell Friedmann/dust/charge witnesses through pinned
   receipts; preserve G3's original failed 801-point derivative assertion.
   These are 216 chart events, not observed wavelengths or a continuum test.
10. Independently evaluate unexpanded ADM metric/projector contractions at
    epsilon=+/-h,+/-2h,+/-3h with h=(1e-3,5e-4,2.5e-4). Use fixed diagnostic
    jets a=7/5,H=2/5,w=3/10,B=-1/5, wdot=-2/7,w_z=1/4,Bdot=1/9,
    B_z=-1/6, psi_dot=1/8, psi_ddot=-1/11 and G3 eta=1/4.
    Require normalized second-order frame agreement <=1e-5 at the finest
    h and decreasing errors or all compared errors <=1e-8. Check projector
    identity/Y agreement <=1e-12. For cubic one-sided finite differences
    use the isolated exact force block, normalize by its nonzero coefficient
    and require <=1e-5 at finest h; retain errors/signs and all failures.

## Evidence and holds

Pin direct/transitive scientific sources, background arrays and this contract.
Never invoke an old receipt-writing main(). New numbered output directory
only, refuse existing paths, nonmutating byte-identity replay, immediate
artifact hashes. Preserve implementation failures and independent signs.

The full finite-density scattering/cutoff task is complete only when its
vertices and physical projection exist. A verified regularity obstruction
completes this bounded prerequisite test but leaves that dependent task
HOLD_SUBSTANTIVE. No blanket quantum inconsistency, instability, healthy GR,
full PDE theorem or empirical SPARC likelihood follows.

Register R9-MT1-G3V, with G3I/G3DF and all inherited variation, B1, G1, S1,
S2/S3, G2/G3/G3S/G3Z/G3E/G3A/G3F/G3D, PD1 and applicable Track-A review debt.
PROCEED_PROVISIONALLY within this test; claim Conditional; review DEFERRED.
Canonical Tests 1-3 HOLD_SUBSTANTIVE. MAT-001 BLOCKED, UVIR-003 IN_PROGRESS,
K_Q NOT_DERIVED, V NOT_COMPUTED, Stage4A CLOSED, TOP-X4 unchanged.
No model-provider dispatch, memory mutation, PDF edit, commit, push,
promotion, publication or parameter/action change.
