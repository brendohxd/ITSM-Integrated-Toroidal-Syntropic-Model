# Canonical spectrum V3: checkpointed algebra and isolated numerical backend

20 October 2026. Execution-only addendum to the frozen canonical-spectrum V1
contract and V2 smoke addendum. The action, initial data, cached Hessian,
constraint reduction, evolving canonical embedding, all retained directions,
80-decimal matrix construction and acceptance tolerances are unchanged.

## Preserved failed execution

V2 terminated with `BrokenProcessPool` after four complete n17 cases were sealed.
Windows Application events 1000/1001 at 15:17:32--15:17:38 local time identify
`python.exe` access violations (`0xc0000005`) in the environment's
`mkl_def.2.dll` 2025.0.1.0. Matched worker PIDs include 15592, 9616, 29088 and
5012. This establishes a native-library crash, not its underlying implementation
cause, memory exhaustion, interference or a scientific rejection.

The four surviving cases each passed their fifteen matrix/algebra controls but
failed both numerical spectrum controls. Preserve their complete original
receipts, sidecars, inputs, executable and raw failed execution. Do not promote
their spectra. Their checks must not be rewritten into success.

## Bounded execution repair

Use NumPy's already installed OpenBLAS eigensolver instead of calling the
crashing SciPy/MKL eigensolver. No installation, dependency replacement,
environment-variable modification, host configuration or provider change.
Record the loaded numerical backend identities. The local BLAS thread limit
applies to this calculation only. Native crash diagnostics may write to the
existing ignored command-output stream; do not enable periodic stack dumps.

Seal full matrices, auxiliary blocks, labels and all matrix checks in parent-only
append-only stage receipts BEFORE any eigensolver call. Release the algebra
worker pool before the separate spectrum stage. A spectrum failure must not
lose a completed matrix. Use at most sixteen Windows-spawn algebra workers;
the spectrum stage is serial with one BLAS thread. Garbage collection may
release completed automatic-differentiation graphs; it changes no equations.

The four surviving V2 matrices may be imported with their pinned source hashes,
unchanged matrix contents and explicit attribution. Import only their matrix
data and fifteen matrix checks, while separately retaining both old spectrum
failures verbatim. Recompute their spectra with the new backend. This import
is reuse of checked finite algebra, not an independent replay.

Compute right eigenvectors from A and left eigenvectors from its transpose;
match the latter to the conjugate eigenvalues with complete one-to-one matching.
Retain and check left eigenpair residuals and matching as additional diagnostics.
Never substitute another mode when matching is unresolved. Preserve the V1
right-residual tolerance 1e-8 and canonical-rescaling tolerance 1e-6. The original
symplectic congruence, action/energy formulae and all unresolved-mode handling
remain unchanged. Backend success alone does not establish accurate eigenvalues.

## Replay and scope

The executable may select a declared subset of the registered family/grid/node
keys for bounded preflight. Only coverage of all eighteen n17 keys is a complete
coarse-grid calculation. Neither subset nor n17 coverage replaces n25/n33
refinement or the continuum and interaction requirements.

Resume validates manifest, complete stage-receipt hashes and matching keys;
never overwrite a sealed stage, including failed spectra. Read-only replay
recomputes ALL selected matrices from the frozen action, including imported
ones, and compares exact matrix, spectrum and aggregate bytes. Preserve earlier
attempts even if replay fails. Partial manifests are not evidence of live work.

Keep computational validation and substantive interpretation separate:
`physics_pass=false`, `gate_effect=NONE`, `review_status=DEFERRED`,
`Rule9_cleared=false`, Stage2 INCOMPLETE, Stage3 NOT_ENTERED. Near-zero,
complex, degenerate, poorly conditioned and failed rescaling cases remain
explicit. No physical stability, cutoff, healthy-GR, continuum-admission,
state-evolution, microscopic matching or numerical weak-field claim follows.

No action change, new state, vault mutation, manuscript/site edits, publication,
commit or push is included.
