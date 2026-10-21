# R4C1 coupled node acceleration: selected regulator velocity rejected

19 October 2026. Unchanged-action Stage 2. The V4 calculation derives the missing
coupled metric/frame acceleration and tests the previous regulator velocity.
Local computational validation: **94/94**. Supplementary pre-chart dimensional
audit: **31/31**. Full immutable replay: exact, exit zero, with eight rather than sixteen workers.

## Result and scope

The previous [H/U field completion](RES001_R4C1_COUPLED_NODE_COMPLETION_V1_REPORT_2026-10-18.md),
with its endpoint addendum, remains a valid restricted necessary-field result
for its declared velocity. Its unresolved higher time condition is now tested.

For all three registered families and eta=1/4,1/64,1/1024, the selected
Z_dot=Ud0*w^2 fails the next necessary classical scalar time-consistency
condition throughout 0<|e|<=1/500. This is **REJECTED_SELECTED_SMOOTH_VELOCITY_CONTINUATION**,
not rejection of every initial state, every solution, a family, R4C1, or ITSM.
No repaired velocity or initial state is adopted or evolved. The exclusion assumes
the joint time/normal regularity needed to differentiate E_Z/w^2 and a finite
scalar third-time jet, as in the transport report. It is not a weak-solution no-go.

The earlier [transport report](RES001_R4C1_NODE_VELOCITY_TRANSPORT_V2_REPORT_2026-10-18.md)
derived the condition but did not know the actual frame acceleration. This
calculation supplies it from the original action. It does not infer it from an
old quadratic frequency or freeze the metric acceleration.

Stage2 INCOMPLETE; Stage3 NOT_ENTERED; physics_pass=false; gate_effect=NONE.
Review DEFERRED; Rule9_cleared=false. These local controls are not peer review.

## 1. Exact coupled acceleration calculation

Retain N=1, h=I, h_dot=2H I, V=(0,w,0), V_dot=(0,-H0*w,0),
psi=0, psi_dot=p, Z=U*w^2 and Z_dot=Ud0*w^2. At each simple node let
s=partial_z(w), s^2=k^2*alpha, alpha=e^2, k=40. Both signs of s are retained.
Keep the shift gradient r1 and its time derivative rt symbolically; rt=0 is
only the registered evaluation gauge. No temporal profile evolution is assumed.

Differentiate the original normalized-frame density before imposing flat
homogeneous metric values. The nodal metric equations have the exact form

    A*d + g = 0,
    A = a*I + b0*11^T,
    a = -(MP2-MU2*(c1+c3))/4,
    b0 = (MP2+MU2*c2)/4,
    a+3*b0 = M_cosmo/2,
    M_cosmo = MP2+MU2*(c1+3*c2+c3)/2,

where d contains the three diagonal metric second-time jets and g is the
original varied force vector. All nine matrix entries and original equation
residuals are checked. The exact solution is

    d = -g/a + b0*sum(g)/(a*(a+3*b0))*1.

The determinant is
(MP2-MU2*(c1+c3))^2*(2*MP2+MU2*(c1+3*c2+c3))/64.
It is nonzero on the registered boxes. The transverse frame coefficient is
-MU2*(c1+c4), also nonzero there. With E_frame the original normal Euler jet,

    F_actual = -E_frame(F=0, d=d_solution) / partial_F(E_frame),
    F = partial_z(V_ddot_y)/partial_z(V_y).

This is an exact action-derived affine solve, not a prescribed metric
acceleration. The exported equations.json contains every metric force and the
explicit rational F_actual. Other metric/frame accelerations and spatial jets
are allowed before their relevant nodal decoupling is checked. No inverse of
the singular psi/Z Hessian is taken.

Retain the exact transverse shift jets and the longitudinal constraint data.
Reduce the rational signed-slope dependence before replacing s^2 by k^2*alpha;
orientation symmetry and numerator/denominator reconstruction are checked.
The original cusp has vanishing first normal frame-Euler jet; no nonexistent
third cusp tensor is used. Regulator terms vanish in this specific metric/frame
node jet, not in the scalar equations or away from the node. Both terms remain
in the independent original-density controls. Intrinsic-curvature force vanishes
only on this initially flat slice; it is not dropped in future evolution.
Future dust has zero initial spatial pressure after variation, while its
density/current and local lapse flux remain in the constraints and transport.

## 2. Actual correlated velocity defect

Use the undivided condition from the transport report:

    D = (1+2*b*k^2*alpha/K_Q)*Ud0 + (2*H-3*H0-r1)*a_psi
        + p*(F_actual+H0^2-8*H*H0+6*H^2-rt-4*r1*(H-H0))
        - (4*b*H*U*k^2*alpha+beta*rho_dot_node)/K_Q,
    a_psi = -U-(3*H-H0-2*r1)*p,
    beta*rho_node = (K_Q+2*b*k^2*alpha)*U-K_Q*H0*p-K_Q*p*r1,
    beta*rho_dot_node = (-3*H+r1+beta*p)*(beta*rho_node).

The arbitrary shift-time jet cancels from the final test after inserting the
coupled acceleration. Do not replace local density by mean density.

Before normalization, substitute the certified root correlations

    H=H0+alpha*h2, U=U0+alpha*u2, r1=alpha*r2.

The exact constant term vanishes. Polynomial reconstruction proves
D=alpha*C, with no division by a physically zero amplitude and no absolute
roundoff error divided by alpha. The phase charge, local flux and controlled
shift inverse/gradient remainder are retained. The whole frozen root rectangles
and continuous amplitude interval are enclosed, not just point estimates.

The following are deliberately outward-coarsened reference-chart bounds for C:

| Family | eta=1/4 | eta=1/64 | eta=1/1024 |
|---|---:|---:|---:|
| archived G3 | [31380,31383] | [1935,1936] | [120,121] |
| new B1-frame | [30920,30923] | [1934,1935] | [120,121] |
| new hierarchical | [30951,30953] | [1934,1935] | [120,121] |

Every lower bound is strictly positive. Each case resolves at the first frozen
16-box angular partition; no domain, tolerance or family is selected afterward.
cases.json preserves full outward binary endpoints and all dispositions.

The action-derived F_actual has global reference-chart enclosure
[-1298.872,-1279.839]. These are coordinate acceleration-slope values, not a
physical cutoff, observed acceleration or C_chi. They overlap earlier broad
F_required enclosures; overlap of marginal intervals does NOT establish
compatibility. The correlated, normalized D above supplies the exclusion.

At alpha=0 the continued equation has D=0. That is a limiting control, not a
claim that the finite-amplitude velocity passes or that the aligned stratum is
a physically identical constrained state.

## 3. Independent controls and dimensions

Original four-coordinate normalized-frame density variations at mp.dps=100
retain all six metric and three frame second-time jets, spatial metric
variation, shift time jets, and the original regulator/cusp.

- Maximum normalized metric-Euler discrepancy: below 7.318e-103, against 1e-40.
- Symmetric frame normal probes at |x|=1e-12: below 1.608e-24, against 1e-20.
- At |x|=1e-18: below 1.608e-36, against 1e-30.

These are limiting numerical controls, not certified finite-x remainder bounds
or independent reviewers.

The separate pinned dimensional audit verifies the pre-chart density and metric/
frame equations have mass degree four, metric coefficients degree two, their
determinant degree six, accelerations degree two, appropriate shift jets, and
undivided scalar transport degree three. It includes invalid-input rejection
and independent exact unit rescaling. Its 31/31 result replays exactly.

The already nondimensionalized charge recipe shares reference numbers between
different physical quantities. This audit does not assign a single physical
dimension to that shared numerical Rc or invent an absolute physical scale.
Reference-chart arithmetic is not microscopic matching or a physical-unit map.

## 4. Execution, replay and preservation

V4 source and contracts were frozen after AST preflight. The original frame
density, independent coordinate variations, 39 registered physical assignments,
domains, precisions and scientific tests were retained. Independent derivatives
and coefficient simplifications use process pools; dependent algebra stays
serial. Operational PIDs/timings are excluded from scientific payloads.

The completed attempt returned in about 637.49 seconds by its private monotonic
journal. This is not a controlled speedup comparison: earlier versions did not
finish successfully. No sixteenfold speedup or billing saving is claimed.
All 21 execution-only algebra smoke checks also pass.

The complete fresh eight-worker replay recomputes all four payloads and all
original checks. Every output/sidecar byte, size and mtime is unchanged. Its
READ_ONLY_REPLAY_EXACT result is confirmed by a separate external before/after
guard over all 96 original records: 44 pinned sources and their sidecars (88),
plus all eight scientific output/sidecar files. No worker-count-dependent
scientific payload or overwritten receipt was found.

Preserved history:

- V1 interrupted on the operator's multicore request; not a physics failure.
- V2 native Windows access violation; exact cause remains UNKNOWN.
- V3 completed symbolic/control tasks, then exited with KeyError: 'slope';
  task completion alone was not a passed scientific audit.
- Supplementary dimensional V1 stopped before mathematics because of a copied
  expected-digest typo. Original bytes and sidecar matched the external snapshot.
  V2 corrects that reference only; all functions are AST-identical.

No historical source, sidecar, failure or receipt was rewritten. Private progress/
terminal logs remain ignored and are not publication evidence.

Frozen executable:
Analysis/MasterTests/test_01_r4c1_coupled_node_acceleration_v4.py
Fresh receipts:
Analysis/MasterTests/outputs/r4c1_coupled_node_acceleration_attempt_04
Supplement:
Analysis/MasterTests/test_01_r4c1_coupled_node_dimensional_audit_v2.py
with outputs/r4c1_coupled_node_dimensional_audit_attempt_02.

    python -B Analysis/MasterTests/test_01_r4c1_coupled_node_acceleration_v4.py --replay Analysis/MasterTests/outputs/r4c1_coupled_node_acceleration_attempt_04 --workers 8

| Artifact | SHA-256 |
|---|---|
| Analysis/MasterTests/outputs/r4c1_coupled_node_acceleration_attempt_04/summary.json | 9f8d5fce14a4fadf3052eafdf4ec5d0e4adbe3937be991d344ff126fa49f6019 |
| Analysis/MasterTests/outputs/r4c1_coupled_node_acceleration_attempt_04/equations.json | 4aa8b6ff0abea3840a4aaededd6a4a713a89a9c29477d23f1585ee8042723857 |
| Analysis/MasterTests/outputs/r4c1_coupled_node_acceleration_attempt_04/independent.json | 4f53942c7066b1be9416bf463c95e9d35899ffbce28b27f5c290888d66dd7176 |
| Analysis/MasterTests/outputs/r4c1_coupled_node_acceleration_attempt_04/cases.json | bcaa4b484426ca37eb6d63900e977071bf0ecd3f8fc1f29e48e7ae42c2a8d125 |
| Analysis/MasterTests/outputs/r4c1_coupled_node_dimensional_audit_attempt_02/audit.json | 273f50caceb1f8181c42f012b5e4b16a68f45b5f037f6a14915c78471365b64d |
| Analysis/MasterTests/test_01_r4c1_coupled_node_acceleration_v4.py | c6a7e31c2f63d8e6481d2e5a4b4f2725ce376f3de05ab639594a7b9e991f1ae7 |
| Analysis/MasterTests/test_01_r4c1_coupled_node_dimensional_audit_v2.py | 75b74f737e4b4910058c8ab50c3ef6d96c3d5a318a5fcca784bbfb9edfcd78de |

## 5. Next same-action calculation and remaining programme

The defect is affine in the regulator velocity coefficient, with positive
Bv=1+2*b*k^2*alpha/K_Q on these boxes. At FIXED old H/U root values, the next
necessary coefficient would be Ud_req=Ud0-alpha*C/Bv. The positive bounds imply
a downward O(alpha) correction. This algebraic implication is not an adopted
velocity or an admitted initial state.

Do not change Ud in isolation and reuse the old mean/root certificate: the
original finite-amplitude lapse energy contains zdc (the regulator velocity
coefficient). A legitimate continuation must recheck the mean equation, node
field condition and time condition TOGETHER, including exact constraint inverse
sensitivities and the resulting lapse density/charges. Whether this joint
necessary completion exists remains OPEN. Higher rank-changing consistency and
persistence would still remain afterward.

R9-MT1-COUPLED-NODE-ACCELERATION-V4 is DEFERRED, inheriting NODE-VELOCITY-
TRANSPORT-V2, coupled-completion, node-acceleration, initial-admission, initial-
constraint/canonical/preparation/family and transitive review dependencies.
Supplementary dimensional checks inherit this same review debt.

Stage1 original bounded linear prepared-dust acceptance only; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; K_Q NOT_DERIVED;
V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED; TOP-X4 unchanged.
Full initial admission/persistence, physical reduced Hessian/Cauchy/energy
domain, nonlinear evolution remainder, physical window, healthy GR and both
identifying matter-residue/nonlinear-force matching inputs remain open.
No action/provider/model/global-runtime change, vault mutation, manuscript/PDF/
site edit, publication/submission, commit or push is included.
