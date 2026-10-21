# R4C1 joint mean/node/velocity completion: restricted root certified

19 October 2026. Unchanged-action Stage 2. Local177/177 controls, all nine
registered family/eta cases; complete fresh eight-worker replay exact, exit zero.
This certifies three NECESSARY initial-data conditions, not full initial
admission, an evolved state, physical stability or a physical validity window.

## Result in plain language

The [previous coupled-acceleration result](RES001_R4C1_COUPLED_NODE_ACCELERATION_V4_REPORT_2026-10-19.md)
rejected the old selected regulator velocity. That rejection is preserved.
A different, jointly adjusted H/U/velocity construction now satisfies the mean
constraint, scalar node field condition and next node time condition together.

The action, family coefficients, background prescription and observational
blindness are unchanged. No corrected state is adopted or evolved. This is
progress past a necessary-condition obstruction, not a healthy-GR or ITSM
validation claim. Stage2 remains INCOMPLETE and Stage3 NOT_ENTERED.

## 1. Scope and coupled equations

Retain the same three families at eta=1/4,1/64,1/1024, k=40,
0<|e|<=1/500 and the original initial profile ansatz

    h=I, h_dot=2H I, V=(0,w,0), V_dot=(0,-H0*w,0),
    psi=0, psi_dot=p, Z=U*w^2, Z_dot=Ud*w^2, w=e*cos(theta).

N=1 and rt=0 are the registered gauge; the parent action-derived transport
formula retained rt before its cancellation. Both node orientations are checked.
The strong classical joint time/normal regularity assumed in the transport
report remains required. No weak-solution or all-action theorem is inferred.

Let alpha=e^2, with r1=alpha*qnode from the controlled momentum-constraint
inverse. Write the three original necessary conditions as

    F = Ebase + alpha*<Edelta(H,U,Ud)> + rho0 = 0,
    G = (K_Q+2*b*k^2*alpha)*U-K_Q*H0*p-K_Q*p*r1-beta*rho_node = 0,
    T = Bv*Ud + R(H,U,qnode) = 0,
    Bv = 1+2*b*k^2*alpha/K_Q.

R retains the action-derived coupled metric/frame acceleration, the original
scalar condition and local dust-current evolution. It is not an old frequency.
The coefficient Bv is strictly positive on every registered box, so

    Ud_req(H,U) = -R/Bv.

This is an algebraic extension away from F=G=0; its physical node interpretation
requires the other equations at the root. The source checks equality with the
original exported undivided transport condition and exact elimination.

The momentum inverse, residual and both H/U sensitivities are explicitly checked
to be independent of Ud. Their inherited error theorem remains valid on the SAME
H/U domain. This permits reuse of that theorem, NOT reuse of the old root
certificate with a patched velocity.

## 2. New constraint bounds and uniqueness proof

Insert Ud_req into the original energy and local lapse equations and include

    total_i(Edelta) = partial_i(Edelta)|Ud
                     + partial_Ud(Edelta)*partial_i(Ud_req), i=H,U,

including node-inverse sensitivities in partial_i(Ud_req) and any applicable
flux derivatives. The normalized node flux is in fact independent of H/U/Ud.
Its full value is retained, not replaced by zero or mean density. Phase-charge
normalization, original regulator terms and exact cusp contribution remain.

Use B=G-beta*F=K_Q*(U-U0)+alpha*Dnode. The frozen H/U rectangle is
[49/50,51/50] times the registered positive H0/U0; it is not widened afterward.
For every alpha in [0,1/250000], interval enclosures establish:

- F>0 on the lower H face and F<0 on the upper face.
- B<0 on the lower U face and B>0 on the upper face.
- F_H<0 throughout the rectangle.
- B_U-B_H*F_U/F_H>0 throughout the rectangle.
- Positive future-dust lapse density, Bv>0 and finite nonsingular complements.

Thus F has a unique H(U), and the strictly increasing reduced B crosses zero
exactly once. Ud_req then fixes a unique third coefficient for this restricted
system. All nine cases resolve at the first frozen16-box angular partition.
This is an existence/uniqueness argument, not a small Newton residual.

A conservative global reference-chart density floor is rho>0.171, and the
reduced node derivative exceeds0.0029 across the nine tested cases. The density
record in the receipt is a LOWER-BOUND certificate, not a claim that density is
constant. This is not a proof for a continuum of eta or arbitrary initial data.

The alpha=0 equations are continued limiting controls only, not identification
of the aligned physical stratum with the finite-tilt constrained system.

## 3. Controlled coefficient and profile corrections

At the NEW joint root, use undivided identities to enclose

    h2=(H-H0)/alpha,
    u2=(U-U0)/alpha=-Dnode/K_Q,
    (Ud-Ud0)/alpha=-C_new/Bv.

h2 is enclosed via the mean equation's exact removable difference, not by
subtracting interval endpoints and dividing by alpha. The exact V4 normalized
time-defect polynomial is evaluated with the NEW root-correlation bounds.
No old fixed-velocity enclosure is substituted as a new proof.

Outward-coarsened bounds on (Ud-Ud0)/e^2 in the reference chart:

| Family | eta=1/4 | eta=1/64 | eta=1/1024 |
|---|---:|---:|---:|
| archived G3 | [-31383,-31319] | [-1936,-1932] | [-121,-120] |
| new B1-frame | [-30923,-30861] | [-1935,-1930] | [-121,-120] |
| new hierarchical | [-30953,-30891] | [-1935,-1930] | [-121,-120] |

In particular, over the registered ansatz,

    0 <= H-H0 <= 5.049*e^2,
    |U-U0| <= 17.492*e^2,
    |Ud-Ud0| <= 31383*e^2,
    |Z-Zold| <= 17.492*e^4*cos(theta)^2,
    |Z_dot-Z_dot_old| <= 31383*e^4*cos(theta)^2.

At |e|<=1/500 the last global profile bound is <=5.02128e-7 in reference units.
The bounds are non-strict at nodes/e=0. They are INITIAL profile differences
within this declared construction, not temporal nonlinear error bounds.
Numerical chart coefficients do not identify K_Q or an absolute physical scale.

## 4. Independent controls and preserved implementation failure

The numerical control solves the three UNELIMINATED equations, using local
lapse-derived rho_node and the original scalar acceleration rather than
substituting the reduced node relations. Its worst point residual is below
7.825e-76 against frozen1e-50. Point roots lie inside the frozen H/U rectangles.

A separate numerical solve of the original metric equations and original frame
Euler jet checks both node orientations; the maximum normalized slope difference
is below2.661e-111 against1e-70. Original8/12-mode shift controls differ by less
than8.630e-54 against1e-30. These approximate controls are not the interval proof,
independent reviewers or a rigorous finite-time evolution calculation.

V1's interval certificates were successful, but all nine independent metric
controls failed: a SymPy-style callback was incorrectly passed to mpmath.matrix,
which silently produced a zero matrix. The installed-mpmath reproduction
confirmed the API error. V1's114/123 result, source, failures and receipts remain
preserved. It is not called a completed audit or a physical singularity.

V2 builds an explicit list of the same nine original matrix entries, checks each
entry and nonsingularity, and retains every tolerance and equation. AST comparison
confirms only the independent-control function changed. All nine V1 interval
certificates match V2 EXACTLY after excluding only the failed-control metadata
flag; no bound or mathematical result was rewritten to obtain a pass.

## 5. Replay, provenance and delivery

The successful V2 execution has177/177 local checks, zero failed/unknown checks.
Sources/contracts were frozen after AST preflight. Complete fresh replay with
eight rather than sixteen workers recomputes every payload and all controls:
READ_ONLY_REPLAY_EXACT, exit zero.

The native guard retains54 pinned inputs and108 source/sidecar metadata records,
plus all eight output/sidecar bytes, sizes and mtimes. An independent external
before/after guard over126 records also preserves V1's failed-attempt files and
the prior coupled-acceleration independent-control payload/sidecar.
Private operational logs remain ignored; no vault data or chat records are
copied into scientific artifacts.

    python -B Analysis/MasterTests/test_01_r4c1_joint_node_velocity_v2.py --replay Analysis/MasterTests/outputs/r4c1_joint_node_velocity_attempt_02 --workers 8

| Artifact | SHA-256 |
|---|---|
| Analysis/MasterTests/outputs/r4c1_joint_node_velocity_attempt_02/summary.json | f1d662d6d9a44eb03df285a541950b0886119c7fc02223408f73855725e7e6f9 |
| Analysis/MasterTests/outputs/r4c1_joint_node_velocity_attempt_02/formulas.json | 846dba62dc1b92ed541adec021805577d79f8898eb40977ce1454d7a775349e2 |
| Analysis/MasterTests/outputs/r4c1_joint_node_velocity_attempt_02/certificates.json | 76b4870fda66c9a85c85dcc282d4934a8ac09337a81c469d3a152f89511963cf |
| Analysis/MasterTests/outputs/r4c1_joint_node_velocity_attempt_02/independent.json | b399814e46e660b7ad52ef03f5c2e4ce262c5e3f815162ad3f9f35be47d0459e |
| Analysis/MasterTests/test_01_r4c1_joint_node_velocity_v2.py | e10bf2f7b20e871cd93fd10b00f1ed6f43f648f60b9282e15205e277d29e3d3d |
| Theory/Gates/RES-001/RES001_R4C1_JOINT_NODE_VELOCITY_V1_CONTRACT_2026-10-19.md | 1733f68993e70a4d73c365acdfaadf6d5df1c71f3541148987ea4c0fa6da7009 |
| Theory/Gates/RES-001/RES001_R4C1_JOINT_NODE_VELOCITY_V2_MATRIX_ADDENDUM_2026-10-19.md | 4c24eb869130aa8b13fbecaeb2c9799b525a10823708ffc3e78e58b743ccef97 |

## 6. Next route and unchanged programme holds

Next test the remaining rank-changing constrained acceleration/regularity
conditions and persistence of these necessary initial profiles using the FULL
coupled system. Do not continually project evolution onto this algebraic graph.
A joint root of these three conditions is not the full initial constraint
surface, a physical reduced Hessian, a hyperbolic Cauchy problem, a healthy-GR
theorem or an admitted frequency/momentum window.

R9-MT1-JOINT-NODE-VELOCITY-V2 is DEFERRED, inheriting COUPLED-NODE-ACCELERATION-V4,
NODE-VELOCITY-TRANSPORT-V2, coupled-completion, node-acceleration, initial-
admission/constraint, canonical/preparation/family and all transitive review debt.
Rule9_cleared=false. Provisional reuse is bounded to this necessary construction.

Stage1 original bounded linear prepared-dust acceptance only; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; K_Q NOT_DERIVED;
V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED; TOP-X4 unchanged;
physics_pass=false; gate_effect=NONE. Physical Hessian/Cauchy/energy domain,
nonlinear remainder/window, healthy GR and both identifying matter-residue/
nonlinear-force matching inputs remain open. No action/provider/model/global-
runtime change, state adoption/evolution, vault mutation, manuscript/PDF/site
edit, publication/submission, commit or push is included.
