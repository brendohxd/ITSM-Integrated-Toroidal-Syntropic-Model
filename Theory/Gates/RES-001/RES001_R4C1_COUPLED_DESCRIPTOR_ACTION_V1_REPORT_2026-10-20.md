# Coupled planar operator action verified locally; large reference-chart response

20 October 2026. Unchanged R4C1 Stage 2. Review DEFERRED.

## New findings

The retained coupled planar Hessian-vector and dynamic-descriptor actions are
implemented and pass **955/955 local computational checks**. Unlike the prior
first-variation evaluator, this calculation includes the response of the solved
temporal velocities and the FULL nonlinear spatial Ricci scalar. No action,
candidate coefficient, initial-state recipe or acceptance threshold was changed.

Both node auxiliary columns are computed with their responses in every retained
canonical/mean variable. All 108 sampled two-row blocks are nonsingular on the
declared reference-chart criterion, permitting their finite-grid linear Schur
elimination. Their canonical couplings are NOT dropped.

There is also an important conditioning issue: for the fixed unscaled dense
probes, some resulting canonical-row Schur corrections are as large as
1.1394e20 in reference-chart units. Invertibility is therefore not evidence
for a well-controlled physical domain. These coordinate-dependent numbers do
not establish a physical instability, strong-coupling scale, cutoff or no-go;
physical energy/clock normalization and admissible perturbations are still
required. Do not hide this response behind the passing check count.

No physical spectrum has been calculated and no state adopted or evolved.
Stage 2 remains INCOMPLETE; Stage 3 NOT_ENTERED; physics_pass=false.

## Calculation actually performed

All nine inherited family/eta cases, e=1/500,k=40, n=17,25,33 and both shifted
node orientations give 54 controls. Each is evaluated at 100 decimal digits,
with fixed complex steps1e-18 and1e-22. The two dense directions contain every
retained sector and mean pair. Both actual node auxiliary basis columns are
also calculated. The operator accepts arbitrary directions, but these tests
do NOT materialize its complete matrix or classify every eigenmode.

All metric/frame/scalar/reservoir/phase/dust/regulator variables, both fixed
charges and their local fluctuations, three mean metric pairs, global
translation section, nonlinear spatial constraint solution, potential, cusp
and lapse flux remain. Only already prescribed redundant quotient tangent
directions are projected; the base state and physical modes are not removed.
The existing candidate auxiliary rates remain diagnostic inputs, not a newly
admitted exact global solution.

For Lcal=volume*L0 and the complete quadratic temporal complement, the true
first implicit response is

    dy=Lcal_yy(base)^(-1)*(dP_y-d(Lcal_y)|fixed_y0).

This response is included when differentiating the first gradient. Freezing
y would omit the Legendre correction and give an incorrect Hessian. A separate
kinetic rejection control detects that omission. Independent mixed finite
differences rebuild and solve the FULL complement at every displaced point,
using fixed real steps1e-12 and1e-16 on n=17 controls. These are not differences
of the old frozen-y envelope.

The Ricci scalar includes the full metric inverse, connection derivatives and
connection products. It is compared with the pinned general spatial-geometry
implementation and a nonflat analytic control. Its nonzero second variation is
retained. No integrated first-divergence shortcut is used for this Hessian.

## Dynamic descriptor and node constraints

Use the complete two-form from

    Theta=<P*dQ-g*s*dZ>+PM*dM, g=b*sqrt(h)*V^2.

With the inherited complete initial tangent Xdot, the linearized operator is

    Omega*deltaXdot=K*deltaX,
    K*v=Hessian(H)*v-dOmega[v]*Xdot.

The metric/frame crosses and background/two-form drift remain. K is not a
symmetric static Hessian. The code tests Hessian symmetry, two-form
antisymmetry and v*(K-K^T+Omega_dot)*w=0. The recorded drift action is nonzero;
dropping it is not an equivalent simplification.

At the exact node g=dg=0 the s,Z two-form rows are null. The full descriptor
columns supply the corresponding 2x2 auxiliary block A. For a registered dense
direction v the code solves A*u=-(K*v)_aux and retains K*v+K_aux*u in ALL rows.
The Schur residual is an algebraic assembly check using those full columns,
not an independent continuum-existence or physical-admissibility proof.

The stored `retained_canonical_momentum_effect` names a norm of canonical
P/PM COVECTOR rows, not a measured momentum acceleration. The larger
canonical-row norms below were separately read from all canonical Q/P/M/PM
rows of the stored full correction. They are reference-chart diagnostics.

## Recorded numerical results

| Control | Largest value / minimum margin | Meaning |
|---|---:|---|
| Dense all-sector Hessian symmetry error | 1.385e-32 normalized | criterion1e-8 |
| Independent full-Legendre mixed difference | 8.432e-20 normalized | criterion1e-7 |
| Two-form/background balance | 1.849e-23 raw | normalized criterion1e-8 passes |
| Nonflat analytic Ricci discrepancy | 1.889e-50 | criterion1e-30 |
| Auxiliary determinant margin | minimum0.9999999999999788 | criterion>1e-8 |
| Absolute auxiliary determinant | minimum34.0909 | reference units only |
| Schur assembly constraint residual | 3.579e-106 normalized | criterion1e-8 |

The background-drift action norm ranges from1.0733e-8 to3.8959e-7 in these
reference coordinates. It is neither set to zero nor interpreted as a
physical frequency. All two-step operator comparisons pass the frozen1e-8
criterion. Both full auxiliary columns and full Schur corrections are retained
in independent.json; failed and unknown check lists are empty.

Maximum responses for the SAME fixed unscaled probes, over families/grids:

| eta | Auxiliary-coordinate correction | Canonical-row Schur correction |
|---|---:|---:|
| 1/4 | 3.9867e4 | 2.6536e10 |
| 1/64 | 1.0204e7 | 1.7386e15 |
| 1/1024 | 2.6120e9 | 1.1394e20 |

The observed growth is not an asymptotic theorem as eta tends to zero. The
coordinates have not been converted into an invariant physical-energy norm,
and the force-clock normalization also changes with eta. Do not identify this
table with a physical strong-coupling scale or a rejection of GR recovery.
Conversely, no uniform physical control follows from the nonsingular block.

## What remains necessary

The next calculation must complete the admissible constraint/perturbation
space and physically normalized reduced operator, retaining the full Schur
coupling and background drift, then obtain the actual mode/characteristic and
frequency-domain evidence. A reduced operator that discards the large mixed
response is not the same theory.

These shifted odd grids each contain one exact node, with the opposite node
tested separately. Both simultaneous continuum traces, the full auxiliary
hierarchy, appropriate mixed-order/weighted regularity, nonlinear persistence,
and arbitrary-direction completion remain open. The earlier obstruction to a
uniform unweighted inverse is not revoked. The new result is not a complete
physical Hessian on an admitted continuum domain, a ghost classification,
stability theorem, propagating mode count or physical validity window.

Both identifying matter-residue/nonlinear-force matching inputs are still
missing. No numerical C_chi or acceleration target has been inserted. No
potential parameter or vacuum-probe scale is adopted as a physical cutoff.

## Preservation and replay

Source/contract were frozen after AST preflight before execution. At most16
Windows-spawn workers handled independent grid tasks; only the parent wrote
receipts. The first run returned exit zero. All previous successes, failures,
sidecars and unrelated dirty work are preserved.

A complete fresh eight-worker read-only replay recomputed all955 checks and
returned exit zero and READ_ONLY_REPLAY_EXACT. All six scientific JSON/sidecar
files, sizes and mtimes are unchanged. The source guard covers104 pins/208
metadata records. The independent266-record before/after guard passed;
the original260 pre-run records were also independently verified unchanged.
This preserves earlier successes and failures, not only the new outputs.

| Artifact | SHA-256 |
|---|---|
| Contract | c990146583f55e58e605943ea36224b8c631678159a3746ee133f659f85f7cf8 |
| test_01_r4c1_coupled_descriptor_action_v1.py | 99a71aa721140a59c0e27af4632e4c52c9ae30138a8ae9af53b690b5c2cee157 |
| attempt_01/summary.json | 458c7eb31b747aad761288486afc2f5da650a2f852083b51c9aaa8331fb079de |
| attempt_01/independent.json | 25f8495dd3f08f476962712339f19db390011994aab72529272922d03f0e46d4 |
| attempt_01/formulas.json | b50153e16239b0cce616802f1850e4ce394f8f23e9632e3b3bb6b481bfc9587b |

Executable: Analysis/MasterTests/test_01_r4c1_coupled_descriptor_action_v1.py.
Receipts: Analysis/MasterTests/outputs/r4c1_coupled_descriptor_action_attempt_01/.
Private ignored runtime journals are not committed or publication evidence.
Worker counts do not imply a speedup or billed-token saving.

Review DEFERRED; Rule9_cleared=false; inherit NODAL-MOMENTUM-TANGENCY-V3,
GLOBAL-NODAL-LIFT-V2, NODAL-DESCRIPTOR-V2, planar-reduction/joint-root/
regularity/canonical and transitive debt. The operator-action checks allow
bounded provisional research, not family GO or canonical promotion. Stage1
registered bounded linear scope only; Stage2 INCOMPLETE; Stage3 NOT_ENTERED;
Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED;
UVIR-003 IN_PROGRESS; Stage4A CLOSED; TOP-X4 unchanged; physics_pass=false;
gate_effect=NONE. No state adoption/evolution, action/parent change, smoothing,
provider/model/global-runtime change, vault mutation, manuscript/site edit,
publication, commit or push.
