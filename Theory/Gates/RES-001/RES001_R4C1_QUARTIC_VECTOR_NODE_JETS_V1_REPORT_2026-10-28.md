# All-frame initial node jets and a controlled longitudinal quotient

28 October 2026, Australia/Perth. Conditional; Rule-9 DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE. G1-G6 INCOMPLETE.

## Result and meaning

For the unchanged R4C1 B1 eta=1/4,e=1/500,k=40 quartic initial
construction, the full coupled frame acceleration has the exact initial limits

    (Vx_tt,Vy_tt,Vz_tt)=(0,0,0)

at both simple alignment nodes. This result follows from the original Euler
forcing and the regular twelve-coordinate complement. The singular full14
velocity matrix is never inverted at a node. No stationary-node ansatz is
inserted.

The missing longitudinal acceleration has a removable analytic quotient.
Over the ENTIRE frozen H/U/Ud/W box, with either node slope and |w|<=1/1000,

    |fy[Vz]/w| < 0.010447,
    |Vz_tt/w| < 0.250715.

These are outward interval bounds in the declared reference units, not fits
to angular samples. Thus the longitudinal acceleration is O(w) and vanishes
at the nodes. Vx_tt is identically zero on this initial slice. The existing
Vy quotient/physical cusp result supplies the remaining transverse component.

If a C2 continuation of these data EXISTS with a simple Vy zero, the implicit
node position has z_dot=z_ddot=0 INITIALLY. All three vector components along
that putative moving node vanish through second time order. This is conditional
initial transport information, not a construction of the continuation or proof
of all-time alignment. G1 background admission remains open.

## 1. Vary before specializing the profile

Derive the h_yz and Vz Euler forcing from the original normalized-frame
density. Keep h_yz=m, m_t, m_z and Vz=v,v_t,v_z during variation. Only then
substitute h=I,V=(0,w,0), registered metric/frame velocities, the quartic
Z=U*w^2+W*w^4 and its declared initial velocity. Retain metric volume,
extrinsic terms, condensate, regulator and shift. Coordinate accelerations
are zero only while extracting forcing; the actual acceleration uses the
complete coupled kinetic operator.

The analytic partition omits precisely the previously isolated cubic cusp
for this derivation. Its physical contribution is then restored using its
known exact forcing and the following complete-sector identities. Physical
A is not changed in the theory.

The full exported B(w) has isolated sectors (h_xy,Vx) and (h_yz,Vz). Both
have identically zero scalar cross C. The original physical cusp forces
in all four selected rows are zero, and these sectors cannot receive the
cusp response from the other metric/Vy rows. Therefore their full physical
acceleration equals the analytic-sector acceleration on this initial slice.
This is an algebraically derived isolation, not a truncation of other fields.

The prior whole-profile original-force enclosures for h_xy and Vx are
exactly zero; the prior full Vy node-force identity is retained. The new
Vz source is varied explicitly. Substitute the unchanged shift ODE and its
regular R=w*T representation. The exact Vz source and full coupled Vz
acceleration divided by w have no node denominator. Their exact expressions,
including the metric cross response, are stored in the receipt.

At w=0 the frame rows of B(0)^-1 have no off-diagonal entries, and the
scalar cross vanishes. The resulting three frame accelerations are zero,
independent of the regulator's undetermined null direction at that node.
The already certified finite initial extension and its scalar compatibility
conditions remain required; this calculation does not replace them.

## 2. Conditional implicit-node equations

For a C2 function with a simple initial zero, differentiating Vy(t,z(t))=0
gives

    z_dot=-Vy_t/sigma,
    z_ddot=-(Vy_tt+2*Vy_tz*z_dot+Vy_zz*z_dot^2)/sigma,
    sigma=Vy_z=+/-2/25.

The registered initial velocity gives Vy_t=0 at a node. The newly completed
all-frame acceleration calculation gives Vy_tt=0 there. Consequently the
initial node velocity and acceleration vanish at either orientation. Initial
Vx,Vz and their first spatial/time derivatives are zero on the slice, so
their derivatives along this putative node also vanish through second order.
These statements require an existing continuation and do not prove one.

A verified rejection example is

    Vy=sigma*x+a*t^3,  Vz=b*t^3,
    x_node(t)=-a*t^3/sigma.

It has the same vanishing first/second node-motion and alignment jets, but
Vz on that node is nonzero for t!=0 when b!=0. This example is kinematic,
not an R4C1 solution. It shows why finitely many initial jets cannot certify
alignment persistence or identify an admissible evolved solution space.

## 3. Verification, provenance and limitations

48/48 exact/interval/reused-original-generator/rejection checks pass, with
no failed or unknown rows. A fresh recomputation gives READ_ONLY_REPLAY_EXACT.
159 pinned source artifacts and their digest values remain unchanged.
Same-author controls and replay do not constitute independent peer review.

The new raw h_yz/Vz sources, BEFORE substituting the shift ODE, agree with
all twelve retained original directional-AD controls on the SAME polynomial
shift representative. Largest normalized discrepancy is below2.40e-70.
The new coupled Vz acceleration agrees with all ten corrected charge-run
full14 accelerations on that run's NEW12-mode Fourier shift; largest
normalized discrepancy is below5.37e-57. The frozen criterion is1e-18.
Different shift representatives are not silently interchanged. Interval
bounds use the exact-shift root/quotient enclosures, with110 decimal point
and80 decimal interval precision, rather than the nominal-point residuals.

Executable: Analysis/MasterTests/test_01_r4c1_quartic_vector_node_jets_v1.py.
Source SHA256:
42d069e091c56c746b225167da2edbee737e25324c9ed9db0ca6984728e2a79a.
Contract: RES001_R4C1_QUARTIC_VECTOR_NODE_JETS_V1_CONTRACT_2026-10-28.md.
Receipt:
Analysis/MasterTests/outputs/r4c1_quartic_vector_node_jets_v1_attempt_01/summary.json.
Receipt SHA256:
8995885054f651a0d2d9d5344e98ac1a6345019d901ad3d65e0cd23b96122b97.
Use --output with a fresh directory or --replay with the retained directory.
No earlier scientific artifact, failed attempt, sidecar, manuscript or PDF changed.

Next derive normalized-frame Ward/ADM constraint transport with vector and
interface terms, and determine a meaningful evolved regularity class with
estimates. Initial node jets and sampled dust/phase tangency do not establish
full constraint propagation, uniqueness, a controlled time interval, physical
mode normalization or a physical validity window. The known weak scalar-jerk
interface term remains mandatory wherever it enters the actual equations.

PROCEED_PROVISIONALLY for the scoped initial identities, bounds and conditional
node jets. HOLD_SUBSTANTIVE for evolved alignment/constraints, actual background
admission, IVP, physical modes/window/GR, identifying matching and numerical
weak-field prediction. Stage2 INCOMPLETE; Stage3 NOT_ENTERED; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED.
No new parent/state adoption, vault mutation, dispatch, publication, commit/push
or deployment.
