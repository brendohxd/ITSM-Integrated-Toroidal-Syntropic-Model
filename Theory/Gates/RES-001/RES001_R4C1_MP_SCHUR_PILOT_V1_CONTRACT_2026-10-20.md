# Multiprecision Schur pilot V1: bounded execution, full retained dimension

20 October 2026. Continue unchanged R4C1 Stage2 from the sealed canonical-
conditioning V1 forms. This is a resource/precision pilot, not a physical gate.

## Scope

Use the COMPLETE 372-dimensional transformed n17 matrix for the B1-frame
eta=1/64, orientation0 case, which remains unresolved. Do not select a principal
submatrix, discard modes, change the action/clock or fit an acceleration target.
One declared pilot case cannot stand for all eighteen registered cases, the
small-eta limit, n25/n33 refinement, or an admitted physical perturbation space.

Use the existing installed mpmath1.3.0 Schur algorithm at35 and50 working digits.
At50 digits also apply the same independently fixed canonical rescaling used
by V3. Keep all eigenvalues, zero/negative/nonoscillatory information and the
complete Schur transformation; no physical sign reassignment from Schur vectors.
The supplied numerical form has100-digit working-format entries derived from
the original80-digit operator. Higher working precision is not a more accurate
action calculation or a certified physical/discretization error bound.

## Algorithm and checkpoints

Construct the same positive constant symplectic diagonal balancing from the
actual supplied diagonal entries, now at the declared working precision. Its
floor is numerical preconditioning only. Retain all signs and entries. Form the
complete Hamiltonian matrix A=J*S_balanced. Internal unitary transformations in
Hessenberg/Schur reduction are eigensolver operations, not canonical physical
coordinates; original-coordinate interpretation still requires back-transform.

First compute and seal Q,H with A*Q=Q*H and Q^dagger*Q=I. Then run the installed
Hessenberg QR routine and seal complete Q,R with A*Q=Q*R, R upper triangular.
Do not modify or monkeypatch the library. Pin its actual eigen.py source hash
and version in addition to all inherited inputs and new contract/executable.
Record every diagonal eigenvalue and retain full Q and R, so later left/right
mode or invariant-subspace reconstruction remains possible without discarding
the operator. Schur-vector columns are NOT individually normalized eigenmodes.

Require full-matrix backward/unitarity/triangularity diagnostics <=1e-8, complete
35/50 and fixed-rescaling spectrum agreement <=1e-6 if those stages finish.
Evaluate complete trace and trace-square identities as additional controls.
Numerical backward diagnostics may use the existing single-thread OpenBLAS
backend; precision comparisons retain the multiprecision eigenvalue values.
These checks are not certified eigenvalue enclosures and do not replace the
remaining left/right-mode, energy-domain, nonlinear or physical-window work.

## Execution budget and failure semantics

Each expensive phase runs in its own owned Windows-spawn child, with a180-second
pilot budget. The parent monitors that actual process and checkpoints completed
phases before proceeding. On expiry terminate ONLY that owned child and preserve
all existing evidence. A timeout is EXECUTION_LIMIT, not a theory rejection or
permission to lower precision/dimension/thresholds. Stop remaining pilot phases
after a timeout/error; do not autonomously multiply the cost across all cases.
Wall-time/PIDs and liveness heartbeats stay private/ignored, not scientific bytes.

Use exact known small-matrix controls, repeated/zero/Jordan and signed examples;
test the owned-child timeout path. Freeze source/contract after AST preflight
before execution, create fresh output, preserve failed attempts and use exact
read-only replay of completed phases plus external metadata guards. A run stopped
by its budget is not a completed scientific milestone; retain the precise stop
point and remaining work rather than claiming an eigensystem pass.

No installation, host/runtime/model/provider change or paid dispatch. The pilot
is dependency-bound and does not claim sixteen-way parallel speedup. Preserve
the six already numerically consistent cases and all twelve unresolved ones;
negative-action and nonoscillatory evidence is not removed by this pilot.
Stage2 INCOMPLETE; Stage3 NOT_ENTERED; Rule9 DEFERRED; physics_pass=false;
Rule9_cleared=false; gate_effect=NONE. No new action/parent, state adoption/
evolution, vault mutation, manuscript/site changes, publication, commit or push.
