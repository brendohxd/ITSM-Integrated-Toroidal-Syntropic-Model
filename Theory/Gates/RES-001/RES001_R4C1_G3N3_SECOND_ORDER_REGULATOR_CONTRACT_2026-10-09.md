# R4C1-G3N3: complete second-order regulator response equation

Date: 9 October 2026. Version 1. Owning Test-1 continuation after G3N2.
Conditional; PROCEED_PROVISIONALLY; review DEFERRED.
physics_pass=false; Rule9_cleared=false; gate_effect=NONE.

## Calculation to perform

Derive the complete order-epsilon^2 regulator equation around the aligned
G3 homogeneous background with the retained first-order G3V transverse
direction. Do not replace the induced scalar/frame/metric response by zero.
Also derive the dust multiplier equation at that order, prior to imposing
its constraint. This supplies coupled response equations for the forthcoming
nonlinear system, not a solved J2, physical Hessian or Cauchy theorem.

Frozen action: RES001_R4C1_ACTION_FREEZE_2026-09-25.md, SHA-256
81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3.
G3N2 report SHA-256 e0f066347d13bbd00566cf8f9af5857e424e4c8ce1102f1eebd457b419c9da19;
G3N2 summary SHA-256 7f0fee4b79104cb43dab3b712b851c1de253d683fe870e920bb2d80e18789252.
S1 scalar-constraint report SHA-256
0b5f06aa3ca91876895c0f1ab521093fa44034f04ce62d605d676f9190824b1b.
Carry their complete source pins, original failures and three absent sidecars.

## Fields and coordinate domain

Use the cosmic-time background N=1, tau_dot=C=exp(beta psi_0), not tau=t.
Coordinates (t,x,y,z), dependence on (t,z), physical first-order transverse
boost w_y=epsilon W(t,z) and shift B_y=epsilon B(t,z). Retain independent
second-order response:

```text
N=1+epsilon^2 alpha
h_ij=a^2[delta_ij+epsilon^2 M_ij], arbitrary symmetric M_ij(t,z)
N^i=(epsilon B delta_iy+epsilon^2 S_i)/a
v^i=(epsilon W delta_iy+epsilon^2 V_i)/a
gamma=sqrt(1+h_ij v^i v^j)
U^t=gamma/N, U^i=v^i-N^i gamma/N
psi=psi_0+epsilon^2 Pi
tau=tau_0+epsilon^2 T, tau_0_dot=C
z_aux=epsilon^2 Z.
```

All six M_ij, three S_i, three V_i, alpha, Pi and T and their required
derivatives remain independent in the derivation. Restriction to (t,z)
is the inherited plane-wave geometry, not a full three-dimensional result.
Use the exact unit normalization for numerical controls and its consistent
order-two expansion for symbolic work. Keep B arbitrary through derivation;
the G3 first-order constraint B=-eta W/(8-eta) is a later check, not a gauge.

No second-order matter density or scalar potential variation is discarded
from the full theory: their effects on the unsolved response variables are
not calculated in this regulator equation. There is no all-equations solve
or on-shell finite-amplitude background claim.

## Required derivation and controls

1. Build the ADM metric, inverse, connection, frame derivative, h^mn and
   Delta=h^mn nabla_m nabla_n psi+theta U^m partial_m psi directly. Verify
   metric inverse and U^2=-1 through order two; derive every Delta coefficient.
2. Compare Delta2 with the inherited linear operator acting on (Pi,V_z)
   plus the direct quadratic transverse source. Test whether alpha, M_ij,
   S_i, V_x and V_y cancel at this order; do not assume that cancellation.
   Reject omissions of either induced Pi curvature or longitudinal frame
   divergence. Explicitly distinguish this equation from its solution.
3. Derive the order-two dust constraint from
   C(psi)^2 g^mn partial_m tau partial_n tau+C(psi)^4=0. Solve its alpha
   relation only after expansion. Retain beta Pi and T_dot. Do not set the
   dust action to zero before its variation or identify dust with U.
4. Vary the order-four regulator density b Z^2/2+b Z Delta2. Verify its
   Z equation and eliminated bulk density exactly, retaining the induced
   fields and fixed/periodic boundary convention. This is the regulator
   contribution only, not the complete quartic Schur action.
5. Export all Fourier coefficients for the parent's profiles
   W=cos(chi)+(1/3)cos(3chi), W_dot=(1/4)cos(chi)-(1/8)cos(3chi), chi=kz.
   Pi=sum Pi_m cos(m chi), V_z=sum V_m sin(m chi), m=0,2,4,6. Leave Pi_m,V_m
   symbolic. Isolate the mean without inverting a Laplacian or dropping m=0.
   Reference-profile rates carry their reference-chart units; they are not
   newly integrated on-shell waves or an observational prediction.
6. Use every archived G3V chart and G3N2 direct-source coefficient as a
   consistency control. Do not change the inherited sample k into an asserted
   physical torus mode or fit amplitude/force coefficients.

Independent unexpanded covariant controls: two generic nonzero arbitrary
second-order metric/frame/lapse/shift/force/dust jets; exact unit frame;
50-digit mpmath. Evaluate the even second-difference coefficient using
epsilon=(1e-3,5e-4,2.5e-4). The final normalized discrepancy with the symbolic
coefficient must be <=1e-5; successive errors must decrease or remain <=1e-12
at a numerical floor. Compare Hessian-trace/theta and divergence/acceleration
implementations of Delta to <=1e-30. All scales are declared reference units.
Keep the acceleration term. Numerical controls are independent code paths,
not independent reviewers or an upgrade of archived trajectory precision.

## Boundaries, output and disposition

Write new versioned formula/response/control receipts and their SHA-256
sidecars, with every failed/unknown assertion and exact read-only replay.
Existing outputs must not be overwritten. Freeze a new version for a genuine
implementation repair; no post-result tolerance, field or action change.
All generated harmonics remain visible. A finite set of modes is not claimed
invariant under nonlinear evolution.

Successful algebra establishes the full second-order regulator and dust
constraint equations in this declared perturbative plane-wave chart, not
the full solved metric/frame/condensate/reservoir/matter response. Those
remaining equations and their compatible initial data, time-domain/DAE,
physical cutoff, stability and continuous GR obligations remain substantive.
No physical ghost verdict, all-classical no-go or canonical adoption follows.

Review DEFERRED; Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 unchanged. No action change, manuscript/PDF edit, vault mutation,
provider dispatch, commit, push, promotion or publication.
