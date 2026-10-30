# Quartic initial construction: kinetic complement and a controlled node cusp

27 October 2026. Conditional; review DEFERRED; Rule9_cleared=false.
physics_pass=false; gate_effect=NONE. G1 and G1-G6 remain INCOMPLETE.

## Findings and their scope

For the registered new_B1_frame eta=1/4,e=1/500,k=40 quartic initial
construction, the complete fourteen-coordinate velocity operator has an exact
block form. Its twelve metric/frame/condensate/reservoir directions remain
uniformly invertible throughout the full profile, including both nodes.
The scalar/regulator coupling still vanishes quadratically at alignment.

The original initial scalar forcing has now been derived and checked away
from the nodes with the original full-coordinate Euler implementation. The
original cusp cannot be dropped: the regulator acceleration has a nonzero
leading |w| contribution. Including the coupled complement, its cusp part obeys

    aZ_cusp = c0*|w| + remainder,
    0.00398305 < c0 < 0.00409915,
    |remainder| < 3.623*|w|^3,   |w|<=1/1000,

in the declared reference units and over the ENTIRE frozen quartic root box.
These are outward interval/analytic bounds, not fitted angular limits.
The relative remainder is below0.000910 for this cusp contribution alone.
It is not an error bound on the total acceleration or future evolution.

The remaining forces are locally analytic on this initial slice under the
stated exact-shift and node-condition hypotheses. Thus their analytic part
does not cancel a nonzero |w| term. The initial aZ trace can be finite while
its normal derivative has a jump. Since |w|=|sigma*x|+O(|x|^3), sigma^2=4/625,
this excludes an extra C1 normal derivative of Ztt for this construction.
It does not, by itself, exclude continuous acceleration or C2 spacetime Z.
No claim of a weak solution, full initial admission or time evolution is made.

## 1. Full kinetic operator before physical constraint reduction

Use coordinate velocities ordered as six independent h components, three V
components, condensate u,v,reservoir r, then psi,Z. On h=I,N=1 the proper
metric velocity is half the coordinate metric velocity. The complete Hessian is

    M = [ B   C    0
          C.T d   -g
          0  -g    0 ],             g=b*w^2,

    C[hyy]=-b*Z*w^2, C[Vy]=-b*Z*w, other C entries zero,
    d=K_Q*(1+w^2)-6*A*p*|w|^3.

The exact B(w) and B(0)^-1 are stored in the kinetic receipt. They are derived
from the original density with all twelve proper velocities retained, then
transformed into coordinate velocities. The cusp has no derivatives in those
twelve velocity directions; its full scalar contribution is restored above.
It is not legitimate to set physical A=0 in the full operator or force.

With exact rational C0=B(0)^-1, outward interval arithmetic over sixteen
subintervals covering [-1/500,1/500] gives

    ||I-C0*B(w)||inf < 0.002403,
    ||B(w)^-1||inf < 24.058.

The Neumann inverse argument proves uniform nonsingularity. B(0) has eleven
positive and one negative eigenvalue; continuity preserves that UNREDUCED
signature. This is not a physical ghost or stability classification: lapse,
shift and physical constraint reduction have not supplied a physical mode map.
For nonzero w, det M=-g^2 det B. At a node M has rank thirteen and g=0;
no inversion of that singular operator is performed.

For the original acceleration forcing (fy,fpsi,fZ), the regular-side solve is

    aPsi=-fZ/g,
    ay=B^-1*(fy-C*aPsi),
    aZ=(d*aPsi-fpsi)/g+(C/g).T*ay.

The cross quotient is an exact polynomial for Z=U*w^2+W*w^4:
(C/g)[hyy]=-Z and (C/g)[Vy]=-w*(U+W*w^2). It vanishes at the node.
Force quotients, rather than a hidden singularity in B, remain the issue.

## 2. Original scalar force and compatibility

The regulator equation gives, for w!=0,

    aPsi=-U-W*w^2-p*(3H-Hbg-Rprime)+p*R*wprime/w.

R is the exact odd constrained shift. Near either node it is analytic by the
unchanged uniformly elliptic one-dimensional ODE with analytic coefficients.
R/w has a removable analytic limit; it is not replaced by a fitted constant.
The [quartic root report](RES001_R4C1_QUARTIC_JOINT_COMPLETION_V1_REPORT_2026-10-27.md)
supplies the exact joint conditions and energy/flux reflection controls; its
sealed SHA256 is 42091a7385e018af9fafefe6fd6ab1e1d7b6c61c165123a1eba61e71a1702c35.
The full scalar momentum and spatial flux, with volume drift retained, are
stored in the scalar receipt. Their Euler forcing includes local lapse-derived
dust, metric/frame drift and the original cusp. Coordinate accelerations are
set to zero ONLY to extract the forcing coefficient; the exact mixed kinetic
term C.T*ay remains in the solve above.

Writing N=d*aPsi-fpsi, its constant node numerator is exactly minus the
registered scalar node condition G. The certified joint root has G=0. The
analytic numerator has the required node reflection parity, so no simple
normal pole is inserted. This structural removal is distinct from computing
uniform numerical error bounds for every remaining analytic force.

The cusp quotient is exactly

    N_cusp/(b*w^2) = (A/b)*|w|*
      [F0+6*p*W*w^2+3*p^2*(R*wprime/w-Rprime)],
    F0=6*p*U+3*Hbg*p^2+2*beta*p^3.

The strictly positive coefficient interval for c0=(A/b)*F0 retains the full
H/U box and the original certified Hbg enclosure. No observed acceleration
target, changed action or microscopic matching coefficient enters it.

## 3. Controlled coupled cusp remainder

Differentiate the original -A*sqrt(det h)*(p^2*V.h.V)^(3/2) before the initial
substitution. Its only nonzero complement forces are

    fy_cusp[hxx]=fy_cusp[hzz]=-A*p^3*|w|^3/2,
    fy_cusp[hyy]=-2*A*p^3*|w|^3,
    fy_cusp[Vy]=-3*A*p^3*w*|w|.

It has no complement velocity or spatial-gradient momenta; these are its
complete complement Euler contributions. In particular
||fy_cusp||inf<=3*A*p^3*w^2 on the registered range. Applying the actual
coupled inverse bound and cross quotient makes its additional aZ contribution
at most 1.019e-5*|w|^3. It cannot cancel the leading |w| term.

The exact shift ODE and its derivative give, uniformly on |w|<=e/2,
|Rprime|<8.248e-6 and |Rthird|<0.021994. Taylor's theorem with
|w|>=|sigma*x|/2 and |kx|<=pi/6 then gives

    |R*wprime/w-Rprime| <= D*w^2, D<16.954.

All inverse/gradient errors from the quartic root certificate are included
when bounding Rprime. The ODE bounds include every H/U/W response and its
new quartic source. The scalar remainder constant is below3.622819;
adding the coupled complement gives below3.623. The exact outward binary
endpoints, coefficient/derivative expressions and intermediate constants are
in the remainder receipt. The estimates are deliberately conservative.

## 4. Verification, preserved failure and limitations

- Kinetic V1: 24/28. Four endpoint numerical controls failed because Python
  division rounded +/-1/500 outside the exact range before acos. Existing
  imaginary baseline components then invalidated complex-step differentiation.
  Its source, sidecar, receipt and failure output are preserved.
- Kinetic V2: 33/33 with exact rational endpoint construction and five added
  real/in-domain baseline guards. No equation, domain or tolerance changed.
  Both signed controls, exact alignment and both complex steps remain.
- Scalar quotient V1: 42/42. Original full-coordinate AD/Euler controls at
  nine registered angles and two complex steps have worst normalized error
  below1.84e-38. These are method controls on a polynomial-shift representative,
  not a continuum exact-background error certificate.
- Cusp remainder V1: 6/6 exact/interval controls, with explicit constants and
  both-node domain. All three accepted executables freshly recomputed with
  READ_ONLY_REPLAY_EXACT. The remainder receipt pins 126 source artifacts.
  Same-author controls/replays are not independent scientific peer review.

| Receipt under Analysis/MasterTests/outputs/ | SHA256 |
|---|---|
| r4c1_quartic_kinetic_extension_v1_attempt_01/summary.json (failed) | 4b68c9ae0cf43350caad2b94f70e557a795aacd7eaa61fc5f258eb05f8b4d689 |
| r4c1_quartic_kinetic_extension_v2_attempt_01/summary.json | 18d56b68030c19c7c48bf27c670deed597a57c1d2f2432b5e459156af3a06765 |
| r4c1_quartic_scalar_quotient_v1_attempt_01/summary.json | 0f8f49732d09fe5e2095c120ef7d2d6e479888ba157863eef156d5dd2a0b11dd |
| r4c1_quartic_cusp_remainder_v1_attempt_01/summary.json | c662c4261cd6496b053979ab6927b7be7fec87520556d7cbffadf453a883879f |

## Next G1 work and inherited holds

Compute uniform controlled bounds/remainders for the remaining analytic
complement and scalar forcing, and determine the actual admissible nodal
function space and constraint transport with this cusp retained. Verify
background consistency and short-time persistence; do not infer an IVP from
the initial kinetic complement or a finite compatibility hierarchy. An extra
smoothness requirement must be justified, not silently imposed or discarded.
No evolved polynomial profile is imposed and the quadratic failure is preserved.

Inherit quartic-root, second-node, original action/density, scalar-coordinate
and coupled-operator review dependencies. PROCEED_PROVISIONALLY for these
scoped identities, bounds and regularity information; HOLD_SUBSTANTIVE for
full admission, physical modes, evolution, interaction/window/GR and matching.
Stage2 INCOMPLETE; Stage3 NOT_ENTERED; MAT-001 BLOCKED; K_Q NOT_DERIVED;
V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED. No state adoption,
new parent, vault mutation, dispatch, publication, commit/push or deployment.
