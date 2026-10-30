# Joint-background acceleration V1: full initial Euler diagnostic

27 October 2026. Expanded goal G1, INCOMPLETE.
Result ID R9-MT1-JOINT-BACKGROUND-ACCELERATION-V1. Claim Conditional.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## What advanced

The original action now supplies a full fourteen-coordinate initial acceleration
diagnostic on the corrected joint H/U/Ud representative, rather than only the
three necessary node/root equations. Both sides of both alignment nodes and
two regular control points were tested. All 176 internal numerical checks pass;
the complete fresh two-worker replay is byte-exact after the four-worker run.

This is an instantaneous approximate-representative calculation. It does NOT
establish a continuum node extension, exact-root/shift error control, full initial
admission, persistence or healthy physical modes. G1-G6 remain unfinished.

## Original action and coupled Euler system

Use the pinned normalized-frame list-contraction density from nodal momentum
tangency V3. Restore its regulator temporal term when constructing the full
Lagrangian; it was intentionally outside the old partial temporal complement:

    L = sqrt(h)*L_partial
        -b*sqrt(h)*(Zdot-R*Z_z)*(c*s+gamma*V^z*psi_z),
    c=V^T*h*V, gamma=sqrt(1+c), s=psidot-R*psi_z.

The fourteen coordinates are six symmetric metric components, three frame
components, condensate u/v, reservoir r, psi and Z. Use
K=(hdot-Lie_S h)/2, X=Vdot-R*partial_z V+V^z*partial_z S and normal scalar rates.
All shift first/second spatial derivatives, all metric/frame crosses and the
regulator pair remain. Initial shift time derivatives are zero as a declared
coordinate gauge; future quotient/gauge preservation is not inferred.

For the initial-slice density L(q,v,d,S,Sz), d=partial_z q, the equations are

    M*a = L_q - (Hessian(L)*W_t)_v
                 - (Hessian(L)*W_z)_d + source,
    W_t=(v,0,partial_z v,0,0),
    W_z=(d,partial_z v,partial_z^2 q,Sz,Szz),
    source_psi=-beta*sqrt(h)*rho.

The full proper Legendre energy and LOCAL flux derivative determine rho. No mean
density substitution or local-flux deletion is used. The spatial Ricci Euler force
vanishes on this flat periodic initial metric at N=1; its full future variation
is not discarded. The varied comoving dust has zero spatial pressure initially,
while its density and scalar source remain. This is not a generic nonflat solver.

The temporal matrix has the structure

    M = [R12  C    0;
         C^T  d   -g;
          0  -g    0],  g=b*sqrt(h)*V^T*h*V.

The existing partial Legendre certificate controls R12 after the invertible
coordinate/proper-velocity map. Away from g=0 it is legitimate to solve this
coupled matrix. No inverse is evaluated at either exact alignment node.
An invertible matrix in this reference chart is not a physical kinetic verdict.

## Inputs and computation

Reference: new_B1_frame, eta=1/4, e=1/500, k=40. Use the stored independent joint
point H/U/Ud and a recomputed twelve-mode shift as APPROXIMATE representatives.
Their high printed precision does not certify exact-background accuracy. The
exact joint construction remains defined by its certified implicit equations.

Fourteen angles: theta=0,pi/4 and node +/- delta at both pi/2,3pi/2 for
delta=0.1,0.01,0.001. Ninety-digit working arithmetic, complex steps 1e-20 and
1e-26. Reverse AD supplies the original-density gradient; Hessian-vector actions
retain every coordinate and spatial-jet contribution. No third cusp tensor or
smoothing is used at a zero: the sampled points have nonzero frame.

At both regular controls, h_xx, V_y, psi and Z Euler equations are independently
checked by nested real differentiation of the spacetime Taylor-jet density,
without AD gradients. All fourteen linear Euler rows are checked internally.
The frozen normalized criterion is 1e-18; the largest recorded error is about
7.736e-29, for two-step acceleration agreement near a node. Independent real
Euler checks are a numerical method control, not independent peer review.

## Observed responses: no extrapolated node theorem

At distance 0.001 from either node, on either side, the diagnostic gives

    psi_ddot approximately -0.0789464869431,
    Z_ddot approximately 225.787890944.

The frame acceleration changes signs with the appropriate orientations. The
local dust density remains approximately 0.199736 near these samples. Values
are reference-chart quantities, not observed accelerations or physical cutoffs.

The Z acceleration does not follow a w^2 profile over the sampled slice:

| Representative point | Z_ddot |
|---|---:|
| theta=0 | 225.787525008 |
| theta=pi/4 | 225.787709643 |
| node distance 0.1 | 225.787888015 |
| node distance 0.01 | 225.787890980 |
| node distance 0.001 | 225.787890944 |

The last small nonmonotonic change is preserved, not fitted away. These samples
do not certify a bounded node limit or justify keeping the initial regulator
profile as a dynamical ansatz. The next actual test is the differentiated original
regulator equation with the full coupled acceleration and its spatial jets.
Apparent node behavior cannot be classified physically before exact-root/shift
errors are propagated through the singular reduction or eliminated analytically.

## Provenance and next step

Executable: Analysis/MasterTests/test_01_r4c1_joint_background_acceleration_v1.py,
SHA256 2cbb055c8a4172ef9e75daa7b80a92c5f979aadc817e29d7cace6115adb47ec5.
Contract SHA256 3b1d7093ab44fe21d688521c58eba10fb0ac1fec25d398e247b7a3fba3bc657e.
Computational addendum SHA256 fd87f4ae2c54893af0409d3a2ce4fb136a0f00d17024f3ccf3634d51317df101.
Receipt: Analysis/MasterTests/outputs/r4c1_joint_background_acceleration_v1_attempt_01/summary.json,
SHA256 ae70906b2fbe22e88afb087a7efd00245f8b49409953349d03061c8d7188c746.
Its 102 source pins, all point payloads and checks remain. Zero failed/unknown
rows in this receipt. Complete fresh replay with two rather than four workers:
READ_ONLY_REPLAY_EXACT, exit zero. Private logs remain ignored.

Continue G1 with exact/controlled both-node acceleration consistency and, where
needed, genuinely free higher initial-profile data determined by the same action.
Do not patch those data and reuse an old constraint/root certificate unchanged.
Do not mark G1 or the expanded goal complete for this diagnostic checkpoint.

Inherit joint-node-velocity V2, coupled-node-acceleration V4, transport V2,
initial/partial-Legendre, normalized-frame density and their transitive review
dependencies. All remain deferred. Stage2 INCOMPLETE; Stage3 NOT_ENTERED;
MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS;
Stage4A CLOSED. No new parent, physical state adoption, manuscript/site change,
publication, vault mutation, commit/push or provider/global runtime change.
