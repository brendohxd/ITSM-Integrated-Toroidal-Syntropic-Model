# Quartic initial profile: a restricted four-condition root exists

27 October 2026. R9-MT1-QUARTIC-JOINT-COMPLETION-V1.
Conditional; review DEFERRED; Rule9_cleared=false; physics_pass=false;
gate_effect=NONE. Expanded G1 and the G1-G6 programme remain INCOMPLETE.

## Result and meaning

For new_B1_frame, eta=1/4, e=1/500 and k=40, the unchanged R4C1 action
admits a unique root of the FOUR REGISTERED NECESSARY initial conditions in
the frozen H/U/W box, with Ud eliminated by its original node-time equation.
The exact constrained shift, its parameter responses, local lapse-derived
dust and both fixed charges are retained. Initial dust is uniformly positive.

The chosen initial profiles are Z=U*w^2+W*w^4 and Zdot=Ud*w^2,
w=e*cos(kz). A separately assembled approximate four-equation solve gives:

| Quantity | Approximate value in reference units |
|---|---|
| H | 0.48232036713549974055 |
| U | 0.03071328630605657169 |
| Ud | 63.84213892953009017431 |
| W | 33.75222953001058464 |

These decimals are a numerical control, not certified narrow root intervals.
The existence/uniqueness claim concerns the full frozen box defined below.
It is conditional on the inherited exact equations and trusted interval
implementation, not proof-kernel verification or independent peer review.

The earlier quadratic continuation remains rejected in its stated regularity
class: its second trace lies in [222,231], away from zero. That result has
not been changed. The extra quartic INITIAL datum supplies a different
same-action continuation which passes this additional necessary condition.
It is not an observational coefficient, a new operator or an adopted state.

This is not full background admission, existence of a coupled time evolution,
physical perturbation clearance, stability or a physical EFT window. Those
remain separate substantive requirements. No cutoff or acceleration scale follows.

## Equations, original source and trace change

Use the original generic energy E and local lapse-flux divergence J before
substituting the new profiles. Define rho=-E-J. The periodic divergence has
zero mean; the exact energy cusp has mean -8*A*p^3*e^3/(3*pi).
Subtract the homogeneous energy analytically before interval evaluation.

The four necessary equations are mean energy F=mean(E)+rho0=0, scalar
node-field G=0, the inherited node-time equation T=0 and second regulator
trace Q=0. Here rho0=1/5, p=1/20 and the phase charge is held fixed by
D=Rc/(1-zeta*Rc^2*e^2/2), Rc=1/2. F=0 supplies the mean dust charge;
pointwise positivity is tested separately. The independent exact phase-charge
identity is unchanged by W.

The original longitudinal source contains b*p*(w*Z*wprime+w^2*Zprime).
Its quartic change is therefore exactly 5*b*p*W*w^5*wprime. The shift
operator is unchanged and coercive in the inherited odd periodic sector.
Its unique inverse depends on H,U,W; it is not frozen at the old root.

At fixed other node jets, hp00=w^2 in the initial gauge. The regulator
equation therefore changes aPsi by -W*w^2. With sigma^2=e^2*k^2=4/625,
the quadratic scalar-current coefficient gains +12*b*W*sigma^4. Consequently

    delta(aPsi[x^2]) = -W*sigma^2,
    delta(aZ|node) = -(K_Q/b+12*sigma^2)*W,
    delta Q = -(K_Q/b+14*sigma^2)*W = -4181*W/625.

The coupled metric/frame low normal orders and the shift's cubic-node
relation are unchanged at FIXED H/U/shift jets: the added Z term starts at
normal order four, its shift source at order five. The original node-time
condition is unchanged explicitly because the added Z term has zero value,
first and second normal derivatives at the node, and its added Zdot is zero.
Its implicit shift dependence and total H/U/W derivatives are retained.

The earlier exact polynomial Q0(H,Hbg,U,r1), r1=Rprime(node), can thus be
reused as Q=Q0-4181*W/625, while RECOMPUTING R and the root jointly. This
partial W coefficient is not the total derivative along the constraint surface.
The complete derivative, including r1(H,U,W), enters the certificate.

## Controlled shift and contraction argument

Write R_N=C*S*f(C^2), C=cos(kz), S=sin(kz), alpha=e^2. Add to the
previous three-term shift polynomial

    alpha^3 * [-5*b*p*W/(MU2*s0*k)]
            * (xi^2/36+5*xi/144+5/96),  s0=c1+c2+c3.

Recompute the exact residual and all three H/U/W residual derivatives.
The first three alpha orders cancel. The inherited Dirichlet half-cell
coercivity and flux-zero argument bound the inverse and gradient errors,
including parameter sensitivities. Uniform bounds over the fixed box are
|R-R_N|<3.802e-22 and |Rprime-R_Nprime|<3.042e-20 in reference units.
All error and sensitivity intervals are propagated into the nonlinear root
equations. No desired nodal or mean residual is manually set to zero.

Let Hbg be the original certified background value and
U0=Hbg*p+beta*rho0/K_Q. U0 is a bracket centre, not an assigned solution.
The frozen variables are

    H=Hbg+(Hbg/50)*yH, U=U0+(U0/50)*yU, W=34+4*yW,
    each y in [-1,1].

Eliminate Ud using T=0; its coefficient 1+2*b*k^2*alpha/K_Q is positive.
Set B=G-beta*F, and use preconditioners

    dF=-6*Mcosmo*Hbg*(Hbg/50),
    dB=K_Q*(U0/50), dQ=-4*4181/625.

For f=(F/dF,B/dB,Q/dQ), define Tmap(y)=y-f(y). The exact inverse is
continuously differentiable in these parameters by the unchanged coercive
linear shift problem. The scalar elimination is nonsingular. The cusp mean
is included exactly and does not introduce a parameter singularity here.

Outward 80-digit interval bounds give row sums of DTmap below
(0.020001,0.001941,0.147177), and centre-plus-row self-map bounds below
(0.021987,0.113613,0.192753). Thus Tmap maps the closed box into itself
and is a strict contraction in the maximum norm. Banach's theorem gives
one unique restricted root. These are uniform box bounds, not sampled slopes.

The first registered angular partition, 16 subintervals per quarter cell,
already certifies this result. Exact energy/flux reflection checks justify
the quarter-cell mean; the unique shift inherits the source/operator
symmetries. Both node orientations are thereby retained. No box widening,
tolerance change or post-result domain selection was used.

Across the full frozen box the lapse-derived dust satisfies rho>0.1713.
The phase charge identity is exact; the mean dust charge follows from F.
The unchanged shift inverse and scalar elimination are nonsingular in this
scope. This does not prove positivity or hyperbolicity of physical coupled modes.

## Verification and preservation

- Joint executable: 16/16 checks. Independently assembled 8/12-mode Fourier
  shift solutions agree to normalized 1.86e-53 at the registered controls.
  Their differences from R_N lie inside the recomputed inverse bounds.
- The uneliminated approximate four-equation solve has maximum absolute
  residual 6.04e-76 in reference units; it lies inside the frozen box.
  Numerical quadrature in this control is not the interval existence proof.
- Separate nonzero-W full-coordinate scalar-current controls: 4/4, both
  slope signs, normalized tolerance 1e-30.
- Separate exact algebra controls: 13/13, including the generic shift source,
  both energy/flux reflection symmetries, trace gain and omitted-term rejections.
- All three executables freshly recomputed with READ_ONLY_REPLAY_EXACT.
  The joint receipt pins 114 sources; hashes were verified before and after.
  All primary sources, receipts and sidecars remain unchanged. Same-author
  independent methods and byte-exact replay are not independent peer review.

| Receipt under Analysis/MasterTests/outputs/ | SHA256 |
|---|---|
| r4c1_quartic_joint_completion_v1_attempt_01/summary.json | 2df2eb08f06243ca1ef60152a17921d17c7755bbca18fbd59bc33ab27f45acb0 |
| r4c1_quartic_scalar_trace_independent_v1_attempt_01/independent.json | 7853be9f208fd985dbeff8492f200f3f6fc296849c97210a6a0e521d4a484995 |
| r4c1_quartic_algebra_independent_v1_attempt_01/independent.json | 2a23a9a346115680e984def0f373b0a58ed816b318bf0e5666bcb90c57d6c5a4 |

Contracts: QUARTIC_JOINT_COMPLETION_V1_CONTRACT, its COMPUTATIONAL_ADDENDUM,
and QUARTIC_ALGEBRA_CONTROL_V1_CONTRACT, all dated 2026-10-27 in this directory.
The new executables are test_01_r4c1_quartic_joint_completion_v1.py,
verify_01_r4c1_quartic_scalar_trace_v1.py and
verify_01_r4c1_quartic_algebra_v1.py under Analysis/MasterTests/.

## Remaining work and review dependencies

Next establish the actual coupled acceleration/node extension on this new
implicit initial construction, with controlled root/shift uncertainty and
the required regularity, then the remaining background consistency and
constraint/charge persistence. Do not constrain future evolution to either
initial polynomial profile. Proceed to physical perturbations only when
their background prerequisites are justified. No full IVP follows from a
finite list of necessary nodal conditions.

Inherit review debt from the joint node-velocity construction, original generic
constraint/density derivation, coupled acceleration and second-node results.
Local result reuse is PROCEED_PROVISIONALLY under the deferred Rule-9 policy;
full background admission, physical modes/domain and dependent predictions
remain HOLD_SUBSTANTIVE. Stage2 INCOMPLETE; Stage3 NOT_ENTERED;
MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED;
UVIR-003 IN_PROGRESS; Stage4A CLOSED. No canonical promotion, new action,
state adoption, vault write, publication, commit/push or provider change.
