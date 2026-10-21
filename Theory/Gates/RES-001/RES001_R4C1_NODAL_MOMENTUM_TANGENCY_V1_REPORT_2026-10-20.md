# Initial coupled momentum flow calculated; numerical certification remains open

20 October 2026. Unchanged R4C1 Stage 2. Review DEFERRED.

## Result

The complete retained initial planar momentum flow has now been calculated,
including the metric/frame two-form cross terms. Its independent unreduced-
generator comparison agrees within the frozen tolerance on every registered
point/grid control. This is useful evidence for the reduction, not a passed
momentum/tangency milestone: **833/880 computational checks pass; 47 fail**.

The failures are preserved in the original V1 source, receipts and private logs.
No tolerance, equation, candidate coefficient or prior receipt was changed.
All 47 failed assertions were inspected. There is no physical no-go conclusion.

Stage 2 remains INCOMPLETE. The full physical descriptor spectrum, admissible
function space, persistence and physical frequency/interaction window remain
unresolved. Stage 3 is NOT_ENTERED; both identifying matching inputs are absent.

## Calculation and scope

Use the existing joint H/U/Ud candidate, not the earlier rejected selected Ud0.
The cases are archived G3, B1-frame and hierarchical continuation at
eta=1/4,1/64,1/1024, with e=1/500 and k=40 in the reference chart. Each uses
17,25,33 points and both shifted node orientations: 54 grid controls, each
evaluated at complex steps 1e-18 and 1e-22. These are pointwise numerical
controls, not interval enclosures over the complete amplitude/domain.

The fixed-charge finite polar chart keeps local phase/dust fluctuations,
the three mean metric pairs and the remaining global translation chart.
Spatial momenta are restored from the original constraints with p_Z=-g*s,
g=b*sqrt(h)*V^2, allowing exact g=0 without division by V^2. For each retained
canonical pair the momentum equation is

    Pdot = -H_Q - s*g_Q*Zdot.

The mean-coordinate cross terms have the canonical factors of two for
off-diagonal metric components. No physical mode or base state is projected
away; tangent directions respect the already declared quotient sections.
The nonzero cross force is between 1.74896e-12 and 1.17383e-7 across the grids;
the recorded relative binary64-floor test does not flag an unresolved cross.
This records an implementation effect, not a physical instability scale.

The comparison generator keeps the original local canonical momenta fixed
while varying configurations, including the multiplier term
N*(p_Z+g*s)*Z_hat before imposing its constraint. N and the original shift are
fixed at their initial values. This is an independent reduction/variation
route, but shares the frozen local partial-Legendre evaluator; it is not an
independently authored full action implementation or independent peer review.

For initial momentum first derivatives only, the exact flat, constant-lapse,
closed-torus identity delta integral(sqrt(h)*R3/s)=0 avoids cancellation of an
integrated curvature divergence. The code also derives the nonzero second
variation R3=-2*(a_prime)^2 for diag(exp(2a),exp(-2a),1). The full curvature is
retained in the directional node calculation. Curvature is NOT removed from
the future Hessian, mode problem or evolution away from this slice.

## Recorded numerical evidence

| Quantity | Largest recorded value | Frozen criterion / meaning |
|---|---:|---|
| Reduced versus original generator, normalized | 2.20438e-13 | <=1e-7; all pass |
| Full-period regulator row, reference-scaled | 2.31434e-16 | <=1e-4 sampled consistency |
| Explicit-clock energy chain-rule error | 1.53871e-9 | <=1e-7; all pass |
| G3 phase-current relative error | 2.05141e-3 | <=1e-4; unresolved |
| G3 dust-current relative error | 1.49425e-3 | <=1e-4; unresolved |
| Node-energy derivative, natural-scale ratio | 3.12221e-5 | <=1e-4, but step agreement fails |
| Node-energy two-step discrepancy | 4.09127e-5 | <=1e-7; unresolved |

The regulator row uses sdot from the original regulator equation and
gdot=g*(5H-2Hbg)/p, including metric-volume and frame-norm drift. The simple-node
limit Rshift*wprime/w=Rshiftprime is used, not a division by w at the node.

At the node, the differentiated compatibility is

    C_E = E0 + Edust + div(F) + sqrt(h)*K_Q*s^2,

where E0 already includes -sqrt(h)*K_Q*s^2/2. The node-energy derivative is
normalized by K_Q*p*max(|H|,max|sdot|); chi=Z+s*div(V) is also tested. The
initial coordinate node speed is zero for this jet, not imposed on general
perturbations. The time-dependent matter conformal factor is retained;
H_tau=beta*Qdust/p, so the Hamiltonian is not assumed time-independent.

All sampled node/regulator residuals lie within their individual thresholds.
The receipt's `sampled_first_node_tangency=true` is therefore NOT sufficient
for reuse as a certified first-tangent result: the independent step-stability
requirement fails. The overall validation correctly remains FAIL/UNRESOLVED.

## Exact failure classification and necessary repair

1. **One symbolic checker failure:** the polar one-form difference remains
   (dR*pR+dtheta*ptheta)*(sin(theta)^2+cos(theta)^2-1) in the checker output.
   A separate read-only SymPy trigonometric reduction returns exactly zero.
   The V1 failed assertion is not rewritten as a pass.
2. **Fourteen phase and fourteen dust current failures:** only the archived
   G3 family fails these relative checks. The smallest G3 phase-current
   amplitude is 6.69296e-13; differentiating the much larger terms leaves
   absolute errors at approximately the binary64 roundoff level. Both new
   families' current comparisons are below 2e-10 relative. These observations
   support a conditioning diagnosis, not a demonstrated repair or relaxed
   criterion. All original current discrepancies remain recorded.
3. **Eighteen node-derivative step failures:** all three families at eta=1/1024,
   all six grids/orientations. Absolute node-energy derivatives are around
   1e-11 reference units, and the smallest declared normalization is about
   5.21e-7. Agreement of the individual residual with 1e-4 does not resolve its
   much tighter step-stability test. Do not infer exact tangency or a physical
   violation from these numerically unresolved derivatives.

The next version must derive better-conditioned first variations of the SAME
constrained functional, separating exact homogeneous/charge cancellations
before floating evaluation, and independently check the small-current and
node-energy derivatives at higher precision. Keep the original generator,
both step sizes, domain and tolerances; do not replace computed forces with
the expected current or set a near-zero residual to zero. Fixing only the
trigonometric checker would leave the substantive numerical hold in place.

Only after that first-tangent milestone is verified proceed to the complete
descriptor Hessian AND background drift, with a justified nodal space and
both traces. Neither a node-free grid nor an isolated raw kinetic sign can
replace the physical mode/domain calculation.

## Preservation, replay and files

Source and contract sidecars were frozen after AST preflight, before the first
run. Nine independent cases use bounded Windows-spawn processes; only the
parent writes scientific receipts. Worker count is not a physical input.
The first run returned exit 1 and is preserved as a failed validation attempt.

Fresh read-only eight-worker replay recomputed the complete calculation and
returned READ_ONLY_REPLAY_EXACT: all six payload/sidecar files are byte-for-byte
identical, including the SAME 47 failed assertions. The CLI correctly returns
exit 1 again because reproducible failure is not successful validation.
The source guard covers 89 pins/178 metadata records. A separate external
232-record before/after guard passed, retaining prior sources, failures,
successes and the new receipts with unchanged hashes, sizes and mtimes.

| Artifact | SHA-256 |
|---|---|
| test_01_r4c1_nodal_momentum_tangency_v1.py | 77b8b7d45ca9ea6b16fbea175c162ca98355382bf72b1ee26026b97437181a08 |
| V1 contract | ff588ca6e50798fd25242d2976d71ed58e562a37a8558be03266c18a986ede2b |
| attempt_01/summary.json | 69270f59143ef1a381074c1851aaef0d99836ac3a459ff61af2ac3145d63f4b3 |
| attempt_01/formulas.json | d19cb3e5e19f50f30a840302b5b3a6e346857b6446fc216a9df27e6be7395bdf |
| attempt_01/independent.json | 15330fbfe01c1ef4aefe953282390373a04b18cad5017b20e408675c37d42a09 |

Executable: Analysis/MasterTests/test_01_r4c1_nodal_momentum_tangency_v1.py.
Receipts: Analysis/MasterTests/outputs/r4c1_nodal_momentum_tangency_attempt_01/.
Private runtime journals/diagnostic outputs stay ignored; they are not committed.

Review DEFERRED, Rule9_cleared=false; inherit GLOBAL-NODAL-LIFT-V2,
NODAL-DESCRIPTOR-V2, PLANAR-REDUCED-HAMILTONIAN-V1, joint-root, regularity,
canonical and transitive debt. Pending review alone does not block provisional
research, but the unresolved current/derivative validation blocks physical
admission or a certified tangent claim. Stage1 remains complete only in the
registered bounded linear prepared-dust scope; Stage2 INCOMPLETE; Stage3
NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; K_Q NOT_DERIVED;
V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED; TOP-X4 unchanged;
physics_pass=false; gate_effect=NONE. No state adoption/evolution,
action/provider/model/global-runtime change, vault mutation, manuscript/site
edit, publication, commit or push is included.
