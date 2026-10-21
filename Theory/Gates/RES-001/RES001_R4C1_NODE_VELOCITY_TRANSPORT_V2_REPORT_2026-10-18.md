# R4C1 node velocity: next necessary condition, actual frame input still open

18 October 2026. Unchanged-action Stage 2. Local 72/72 checks; complete fresh
read-only replay exact, exit zero. No initial state adopted or evolved.

## What this adds

The [coupled mean/node completion](RES001_R4C1_COUPLED_NODE_COMPLETION_V1_REPORT_2026-10-18.md),
read with its [endpoint addendum](RES001_R4C1_COUPLED_NODE_COMPLETION_V1_ENDPOINT_ADDENDUM_2026-10-18.md),
repairs a necessary condition on the initial FIELD. It leaves the selected
regulator VELOCITY unproved. This calculation derives the next time-consistency
condition and identifies the missing input precisely: the actual coupled
frame-acceleration gradient at a profile node.

The explicit metric-acceleration trace cancels after eliminating the scalar
third-time derivative. This cancellation does NOT authorize freezing gravity:
the missing frame acceleration must still come from the coupled metric/frame
equations. Substituting the old quadratic frequency would assume the result.

The selected velocity is therefore **UNRESOLVED**, neither accepted nor rejected
by this calculation. It is not a new action, a physical family GO, full initial
admission, a temporal solution, or a physical-window result.

## 1. Scope, gauge and regularity

Retain N=1 and the registered initial slice

    h=I, h_dot=2H I, V=(0,w,0), V_dot=(0,-Hbg*w,0),
    psi=0, psi_dot=p, Z=U*w^2, Z_dot=Ud*w^2.

At a simple node use w=s*x+O(x^3), R=r1*x+O(x^3),
R_dot=rt*x+O(x^3). Both signs of s are allowed. All six metric second-time
jets and their spatial variation, and all three frame second-time jets, are
allowed. Initial coordinate node velocity is zero; persistence is not proved.

Define

    F = partial_x(V_ddot_y)/s at the node,
    a = psi_ddot(node), j = psi_third_time(node),
    T = trace(h_ddot)(node).

F is a coordinate acceleration slope, with mass dimension two in the frozen
chart. It is not a characteristic frequency, a physical cutoff or an observed
acceleration. Ud is Z_dot/w^2, NOT U_dot. No U(t)*w(t,x)^2 evolution is adopted.

Require joint time/normal regularity sufficient to differentiate the regular-side
E_Z/w^2 quotient and take its node limit, and a finite scalar third-time jet.
This is a stronger classical compatibility question than the earlier continuous
scalar-acceleration test. No weak-solution or all-action no-go conclusion follows.

## 2. Complete geometry, including a preserved V1 error

For the original scalar regulator equation write c=V^2, gamma=sqrt(1+c),
v=V^z, l=log(sqrt(h)). With N=1 and planar dependence, the coefficient C of
psi_t in E_Z/b=Z+hp^{ab}partial_a partial_b psi+C*psi_t is

    C = c_t/2 + c*(l_t-R_z) - R*c_z/2 + gamma*v_z
        - K_ij V^i V^j + (gamma*v-c*R)*l_z.

The V1 executable's exported `C_general` string omitted the last term and was
therefore labeled too generally. Preserve that source and its 59/59 initial-only
receipts. The [V2 geometry addendum](RES001_R4C1_NODE_VELOCITY_TRANSPORT_V2_GEOMETRY_ADDENDUM_2026-10-18.md)
corrects the general identity; no historical bytes or hashes were edited.

On this initial slice l_z=l_zt=0 because h_z=h_dot_z=0. Thus the missing term
and its first-time derivative vanish HERE, not during arbitrary future evolution.
V2 explicitly checks the full product rule and four independent coordinate
connections with nonzero volume gradients. The omitted terms in those controls
range from approximately 0.02484 to 0.03869: their absence is actually exercised.
The original initial-only numerical controls and nine enclosure payloads
recompute byte-for-byte unchanged.

## 3. Next necessary scalar condition

On the initial slice the normal/time limit is

    lim (partial_t E_Z)/(b*w^2)
      = Ud + j + (5H-3Hbg-2r1)*a
        + p*[F+Hbg^2-8H*Hbg+T/2-2rt-4r1*(H-Hbg)].

Independently varying and differentiating the original psi density gives

    partial_t E_psi(node)
      = -K_Q*[j+(T/2-6H^2-rt)*p+(3H-r1)*a]
        + 2b*s^2*(Ud-2H*U) - beta*rho_dot.

These are equations before declaring any metric acceleration or scalar jerk
to be zero. The regulator spatial Hessian and its metric drift are retained.
The varied future-dust current, with pT=sqrt(h)*rho/C_matter and
partial_t pT=partial_i(S^i pT) on this homogeneous-clock initial slice, yields

    rho_dot = (-3H+r1+beta*p)*rho_node.

Eliminating j gives the next necessary condition

    0 = (1+2b*s^2/K_Q)*Ud + (2H-3Hbg-r1)*a
        + p*[F+Hbg^2-8H*Hbg+6H^2-rt-4r1*(H-Hbg)]
        - (4b*H*U*s^2+beta*rho_dot)/K_Q.

At the certified restricted mean/node root,

    a = -U-(3H-Hbg-2r1)*p.

The new condition has mass dimension three term by term. Its undivided form
is retained at p=0; solving for F is only used for the registered p>0 cases.
T cancels after eliminating j. No metric equation has thereby been solved.
The original C2 cusp has vanishing required nodal composite derivatives when
V=V_dot=0 and grad(psi)=grad(psi_dot)=0; no ordinary third cusp tensor is used.

As a limiting control, with s=r1=rt=0 and H=Hbg, the previous quadratic recipe

    U0=Hbg*p+beta*rho/K_Q,
    Ud0=Hdot_bg*p+Hbg*pdot_bg+beta*rhodot_bg/K_Q-wave_ddot*p,
    F_bg=wave_ddot-Hdot_bg+Hbg^2

satisfies the condition exactly. This checks the old bridge only; F_bg is not
the finite-amplitude interacting frame acceleration.

## 4. Nine reference-unit enclosures and independent checks

For all three families at eta=1/4,1/64,1/1024, the whole inherited
|e|<=1/500 range and the frozen H/U rectangles, cases.json encloses the F
REQUIRED by the selected Ud with rt=0. It uses the controlled exact-inverse
gradient remainder, charge prescription and local lapse flux, not just mean
density. A conservative outward global enclosure is

    -1301.572 <= F_required <= -1279.790.

These wide reference-unit necessary ranges are not predictions of F. The
continued e=0 equations do not divide by a physically zero wave. The coupled
frame/metric Euler system has not yet supplied F_actual, so there is no finite-
amplitude comparison establishing or rejecting velocity compatibility.

At mp.dps=100, independent original-density four-coordinate variations keep
nonzero off-diagonal/spatially varying metric second-time jets, arbitrary three
frame second-time jets, shift time gradients and a nonzero arbitrary Z_ddot.
The maximum normalized differentiated-psi discrepancy is below 7.900e-103
against 1e-45. Symmetric normal probes at 1e-12 and 1e-18 have maximum errors
below 9.547e-27 and 9.547e-39, respectively, against frozen 1e-20 and 1e-30.
These probes are limiting controls, not certified finite-x remainders.
The complete-general-geometry coordinate discrepancy is below 1.952e-102
against 1e-60. These are same-author independent implementations, not Rule-9
clearance or formal verification of SymPy/mpmath.

## 5. Preservation, delivery and next calculation

All 72 local checks pass with zero failed/unknown checks. Source and contract
final-byte digests were frozen after AST preflight and before scientific runs.
The complete fresh read-only V2 replay recomputes all four JSON payloads and
checks all eight output/sidecar bytes, sizes and mtimes separately. All 36
source pins and 72 source/sidecar metadata records remain unchanged. V1 and
all earlier results, failed attempts and sidecars are preserved.

Next derive F_actual from the ORIGINAL coupled frame/metric acceleration
equations, including the necessary spatial jets and constraints, and compare
with the condition above. Do not impose the old frequency, freeze gravity,
continually project onto a preferred graph, or infer persistence from this test.

Frozen executable: Analysis/MasterTests/test_01_r4c1_node_velocity_transport_v2.py.
Fresh receipts: Analysis/MasterTests/outputs/r4c1_node_velocity_transport_attempt_02.

| Artifact | SHA-256 |
|---|---|
| V1 contract | 6213246535807f2c8486373c0e976a510ee504a3f884617b8c96a49d21772e1f |
| V2 geometry addendum | 8fd754f649fb34829018745bb933347035b4c73f7c6b43112140e0b1eeb471e9 |
| V2 executable | e19a7f44584b92a6677cfe985092c0319207a1dfa910c3a1ec69047105fe8de4 |
| summary.json | 0bf9482f7addd5fa1a1d66d4aff19b3562fd5cecc19e96f1b099040e5a658c2e |
| equations.json | 01b75e280f4d23340d7e5fe87854b00981e0a5443ed45113270bfc594b47a18b |
| independent.json | a300ff14093b3e9fb02d7f2ade5459867596a2230070714324a276064de18ece |
| cases.json | 9fbc226db2b9bdd983bad2b2e4f3a6b64c28469700d944a04e73a5f44c626c39 |

    python -B Analysis/MasterTests/test_01_r4c1_node_velocity_transport_v2.py --replay Analysis/MasterTests/outputs/r4c1_node_velocity_transport_attempt_02

R9-MT1-NODE-VELOCITY-TRANSPORT-V2 is DEFERRED, not cleared, inheriting the
coupled-completion, node-acceleration, initial-admission and all transitive
review dependencies. Stage1 original bounded linear prepared-dust acceptance
only; Stage2 INCOMPLETE; Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE;
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; TOP-X4 unchanged; physics_pass=false; gate_effect=NONE;
Rule9_cleared=false. Full admission/persistence, physical Hessian/Cauchy/energy
domain, nonlinear remainder, physical window, healthy GR and both identifying
matter-residue/nonlinear-force matching inputs remain open. No vault mutation,
manuscript/PDF/site edit, commit/push, publication/submission, new action,
provider dispatch or model/runtime change was included.
