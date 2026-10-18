# R4C1 regulator-node V1: frozen bounded calculation

17 October 2026. Unchanged-action Stage 2, following FINITE-TILT-CANONICAL-V2.
Freeze this contract before executing the new calculation. No action change,
new parent, reinitialization, fresh observational fit, or physical GO is allowed.

## Question and required derivation

The canonical inverse divides by the relative frame norm V^2. The registered
transverse wave has zeros of cos(40z); those points cannot be admitted using
that regular inverse. Derive the regulator's unreduced Euler equation directly
from the original first-order regulator density, then its alignment constraint
and necessary transport condition, retaining evolving geometry and frame jets.

Keep the original normalized n=U/sqrt(-U^2), independent unit variation,
positive future dust branch, all spatial directions and the actual C2 cusp.
Do not replace the regulator operator by its generally different formal adjoint.
Do not infer a global Dirac classification from a stratum-local constraint.

Required outputs:

1. Covariant regulator Euler equation; general ADM Hessian projection; exact
   aligned constraint with nonzero spatial frame divergence retained. Check
   the aligned scalar momentum from the original force density.
2. Necessary transport on an alignment worldsheet. Retain metric/Laplacian
   drift, nonuniform lapse, divergence of frame-velocity drift and motion of
   the worldsheet. A field's value vanishing at a node does not set its jets
   to zero. Do not assume a normal-transport-invariant worldsheet exists.
3. Precise local compatibility conditions for extending the canonical inverse
   across a simple profile zero. Give explicit finite-regularity assumptions,
   a controlled quotient bound and exclusions for joint/degenerate zeros.
   Do not use an ordinary third cusp derivative or infer uniform eta/e limits.
4. Derive the action-specific effect of omitting the cusp's temporal momentum
   when lifting velocity data to canonical data. Determine its actual amplitude
   order and regularity. Velocity archives are not accused of a missing term:
   they are not truncated canonical-momentum archives. Any momentum completion
   must be fixed by the unchanged action, not a fitted target.
5. Test the alignment constraint and its transport against every stored full
   response event in the existing 18-run archive: all three diagnostic families,
   eta=1/4,1/64,1/1024, both Radau/DOP853 methods, k=40, and all four retained
   events per run. The archive's 21-point time grid does not supply 21 complete
   22-field response events. Preserve mean, second harmonic, auxiliary fields,
   shifts and their velocities. Check, rather than assume, the reconstructed
   nodal frame and normal shift. These are second-order sampled controls on
   [0,1/20], not a full-time or finite-amplitude theorem.

## Frozen numerical and rejection controls

Exact identities use symbolic expansion/cancellation. Independent direct
finite-tilt regulator-density controls use 80-digit mpmath arithmetic and a
normalized 1e-50 tolerance. Stored binary64 full-response and transport controls
use the inherited normalized 1e-10 tolerance. Retain every run and event,
including failures; do not tune tolerances or select families after evaluation.

Reject omission of acceleration, expansion/divergence, geometric Laplacian
drift, lapse derivatives, divergence of a vanishing frame's time derivative,
moving-node transport, either inverse numerator's normal-jet condition, and
the cusp contribution to temporal momentum. Include a finite-regularity
counterexample to an unwarranted smooth quotient. A failed control is a
preserved failed attempt, not an invitation to rewrite previous evidence.

## Sources and preservation

Use the original full/first-variation reports (25 September), the original
G3N5 off-shell action builder, the interacting background equations, the frozen
three-family map, INITIAL-CHARGE-COMPLETION-V4, FINITE-TILT-CANONICAL-V2 and its
source/receipt, and FIXED-CHARGE-RETARDED-V3 trajectories/formulas. Pin exact
source bytes and required sidecars, and verify their hashes and metadata before
and after the run. Do not re-run or revise their completed pipelines.

Executable: `Analysis/MasterTests/test_01_r4c1_regulator_node_v1.py`.
Fresh directory: `Analysis/MasterTests/outputs/r4c1_regulator_node_attempt_01`.
Output symbolic formulas/proofs, independent controls, all archived nodal
records, and a summary separating check status, physics and deferred review.
Recompute all outputs for exact read-only replay and preserve bytes/mtimes.
Never overwrite an existing output directory or frozen source/sidecar.

## Acceptance and unchanged holds

Acceptance is the stated unreduced node/transport calculation and necessary
compatibility result with explicit assumptions and rejection controls. It is
not sufficient admission of nonlinear initial data or closure of Stage 2.
Any unresolved mathematical step or failed archived control must be recorded
as such; leave the relevant obligation open.

General 3D constraint algebra/reduction, complete finite-amplitude data,
physical Hessian/Cauchy/energy domain, nonlinear remainder, nonempty physical
validity window and healthy GR remain required. Stage 1 retains its original
linear prepared-dust acceptance; Stage 2 INCOMPLETE; Stage 3 NOT_ENTERED.
Identifying matter-residue and nonlinear-force matching inputs remain absent.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.

R9-MT1-REGULATOR-NODE-V1 inherits canonical/constraint/G3N5/generic-family and
all transitive review debt. Pending review alone does not stop supported
provisional reuse. No vault mutation, manuscript/PDF/site change, commit/push,
publication, submission, model/provider dispatch or runtime change is included.
