# Local multicore execution for the coupled-node calculation

The versioned coupled-node executable supports `--workers N` (default 16).
It uses local Python processes, not external model providers or CPU-bound
Python threads. The present Ryzen 7 reports 8 physical cores / 16 logical
processors. Sixteen workers target the logical processors, not sixteen
independent physical cores; no 16-fold speedup is promised.

Python's [ProcessPoolExecutor documentation](https://docs.python.org/3.13/library/concurrent.futures.html#processpoolexecutor)
describes its separate-process execution and pickling/import requirements.
The implementation explicitly uses the Windows-compatible spawn context.

## What runs in parallel

- The 77 required symbolic derivative jobs, with differentiation BEFORE the
  same exact atomic nodal assignment. Up to 16 processes may participate.
- The two independent coordinate-control seeds: at most two processes.
- The nine registered family/eta cases: at most nine processes, each with its
  own mpmath context (`mp.dps=100`, `iv.dps=80`).

Dependency-bound algebra stays serial. There are no nested pools. The script
caps workers at usable logical processors (and Windows process-pool limits),
collects results in canonical order, propagates worker failures, and lets only
the parent write scientific receipts. Worker count, PIDs, timings and completion
order are not physical inputs and are excluded from scientific payloads.

## Commands

Use the existing `itsm_env` interpreter through the standalone context optimizer.
Every new output directory AND operational progress filename must be unused.
Replace `NEW` below with a fresh identifier; do not overwrite old attempts.

```powershell
python -B Scripts/itsm_context.py run -- python -B Analysis/MasterTests/test_01_r4c1_coupled_node_acceleration_v4.py --workers 16 --output Analysis/MasterTests/outputs/r4c1_coupled_node_acceleration_NEW --progress-log .local/itsm-context/coupled-node-NEW.jsonl
```

Use `--workers 8` or `--workers 1` when less parallelism is wanted. This does
not change equations, precision, domain or acceptance criteria. Sixteen workers
can increase RAM use; do not infer a speed improvement solely from worker count.

A bounded execution-only test compares the same task values serially and in
the process pool. It creates no scientific receipts:

```powershell
python -B Scripts/itsm_context.py run -- python -B Analysis/MasterTests/test_01_r4c1_coupled_node_acceleration_v4.py --parallel-smoke --workers 16
```

After a successful full receipt exists, `--replay <existing-directory>`
recomputes it read-only. Changing worker count must not change scientific bytes,
sidecars, sizes or mtimes. The smoke test is not a substitute for full replay
or the original independent physical controls.

V4 also has `--algebra-smoke --workers 16`: execution-only checks for exact
atomic replacement, signed even-rational reduction, coefficientwise amplitude
normalization, invalid-input rejection and serial/parallel equivalence.
Its 21/21 smoke result is not the full scientific result.

## Progress and preservation

Optional `--progress-log` writes a fresh ignored journal under
`.local/itsm-context/`. It records stage names, completed derivative/case counts
and actual worker PIDs. A sibling `.stacks` directory holds fatal diagnostics.
There are no periodic asynchronous stack dumps in V3. These operational logs
are private/ignored and must not be committed or treated as scientific receipts.

V1's interrupted run and V2's native-crash attempt remain preserved; neither
is a physics rejection. V3 subsequently reached interval evaluation and exited
with `KeyError: 'slope'`, without final scientific receipts. It remains preserved
too. The V3 execution addendum records the checked structured metric solve and
its original-matrix/residual requirements. V4 retains these and replaces global
multivariate normalization with independently simplified amplitude coefficients,
with exact reconstruction and cancellation checks. Unresolved slope symbols
must fail, not receive invented values. The V4 algebra addendum owns that scope.
No source or hash is
silently updated in place: further substantive changes need a new version and
fresh output directory.

Execution success does not clear initial admission, physical-domain, matching,
publication or review gates. Consult the live RES-001 owning report for the
actual scientific disposition. No automatic model dispatch, package installation,
global runtime reconfiguration, commit, push or publication is part of this mode.

## Verified checkpoint: 19 October 2026

V4 completed all 94 local controls and its complete eight-worker read-only replay
reproduced every scientific byte. The supplementary pre-chart dimensional audit
passed 31/31 and replayed exactly. These are different scoped checks, not a
combined physical clearance. All nine registered cases reject the old selected
regulator velocity; they do not reject every family or the unchanged action.
See the [owning report](../Theory/Gates/RES-001/RES001_R4C1_COUPLED_NODE_ACCELERATION_V4_REPORT_2026-10-19.md)
for bounds, preservation and the next joint H/U/velocity route. Review remains
deferred and the physical-domain and matching gates remain open.

The subsequent [joint H/U/velocity checkpoint](../Theory/Gates/RES-001/RES001_R4C1_JOINT_NODE_VELOCITY_V2_REPORT_2026-10-19.md)
has 177/177 local checks and exact eight-worker replay. All nine cases have a
unique restricted root of the mean, node-field and node-time conditions. It
preserves the old velocity rejection and does not admit/evolve an initial state.
Its executable is `Analysis/MasterTests/test_01_r4c1_joint_node_velocity_v2.py`;
it also supports `--workers`, fresh `--output`, read-only `--replay` and ignored
`--progress-log`. All physical-domain, matching and review holds remain.

The subsequent [regulator-acceleration regularity checkpoint](../Theory/Gates/RES-001/RES001_R4C1_REGULATOR_ACCELERATION_REGULARITY_V1_REPORT_2026-10-19.md)
has 200/200 local checks and exact eight-worker replay. Coupled feedback does
not cancel the leading finite absolute-value cusp in the regulator acceleration.
It obstructs C3 regulator continuation in the registered profile class; it does
not reject the earlier joint root or rule out C2/weak solutions. No new C3
physical gate is imposed. Full Cauchy/energy-domain and persistence work remains.

The [fixed-charge patch momentum checkpoint](../Theory/Gates/RES-001/RES001_R4C1_FIXED_CHARGE_PATCH_MOMENTUM_V2_REPORT_2026-10-19.md)
has 104/104 local checks and full exact eight-worker replay. Its nine independent
case tasks use at most nine workers with the same bounded spawn mode; sixteen
is the configured ceiling, not a speedup claim. V1's integer/interval helper
exception remains preserved. V2 changes only input conversion and pins, not
equations or tolerances. Opposite signs survive the known constraints and
fixed charges on regular planar patches; complete physical modes, frequency
window and ghost classification remain open. No billing savings are measured.

The [regular-planar Hamiltonian reduction](../Theory/Gates/RES-001/RES001_R4C1_PLANAR_REDUCED_HAMILTONIAN_V1_REPORT_2026-10-19.md)
has 493/493 checks and complete exact eight-worker replay, using the same
bounded spawn/parent-write mode. All nine cases retain metric means, both
fixed charges, the remaining global constraint and the weighted lapse flux.
Its nodeless numerical method controls do not admit the actual nodal profiles
or establish physical modes, a cutoff or a frequency window. The standalone
executable supports fresh --output, read-only --replay and --workers.

The [undivided nodal descriptor](../Theory/Gates/RES-001/RES001_R4C1_NODAL_DESCRIPTOR_V2_REPORT_2026-10-19.md)
has 704/704 checks and full exact eight-worker replay. Nine case tasks retain
the same bounded spawn/parent-write execution. The missing-helper V1 failure
is preserved; V2 changes only original helper aliases/pins, with all function
ASTs and scientific formulas identical. The node partial block avoids V^2
division, but global nodal DAE/spectrum integration and a physical window
remain open. No inverse, cutoff or speedup/billing claim follows from counts.

## Global nodal initial-flow checkpoint: 20 October 2026

The [global nodal lift](../Theory/Gates/RES-001/RES001_R4C1_GLOBAL_NODAL_LIFT_V2_REPORT_2026-10-20.md)
passes 1072/1072 with complete exact eight-worker replay. All nine cases retain
the joint candidate inputs, original shifts, local density, fixed charges and
mean metric pairs at exact nodes. V1's successful1018/1018 and replay remain
preserved. V2's equivalent periodic by-parts flux evaluation improves its narrow
rate margin without changing targets/equations/tolerances; all other numerical
functions and initial recipes are identical. The full momentum/DAE hierarchy,
physical spectrum/window and matching remain open. Runtime journals stay ignored;
no automatic provider/model dispatch or billed-token savings are claimed.

## Initial momentum/tangency checkpoint: 20 October 2026

The [coupled momentum report](../Theory/Gates/RES-001/RES001_R4C1_NODAL_MOMENTUM_TANGENCY_V1_REPORT_2026-10-20.md)
records 833/880 computational checks, NOT a passed milestone. All nine cases
were calculated with nine Windows-spawn workers; the complete eight-worker
read-only replay reproduced every byte and the same 47 failed assertions.
Exit 1 remains correct even when READ_ONLY_REPLAY_EXACT is printed. The
232-record external preservation guard passed. Currents and node-derivative
step agreement require better conditioning/higher precision; do not loosen
the acceptance criteria or interpret sampled node flags as physical clearance.
Full nodal hierarchy, descriptor Hessian/drift, physical window and matching
remain open. Original source, failures and private ignored journals are retained.

## High-precision first-variation checkpoint: 20 October 2026

The [V3 first-variation report](../Theory/Gates/RES-001/RES001_R4C1_NODAL_MOMENTUM_TANGENCY_V3_REPORT_2026-10-20.md)
records 2923/2923 and complete exact eight-worker read-only replay after an
initial run with at most16 spawn workers. The54 grid tasks each recompute at
80/100 decimals with both original complex steps; only the parent writes
receipts. A254-record external guard preserves all earlier attempts and outputs.
V1's47 failures remain intact. V2's2922/2922 first run remains preserved with
its subsequently identified constant-reciprocal precision limitation; V3 fixes
only that adjoint operation and adds its test, retaining all scientific tolerances.
The registered numerical hold is resolved, not Stage2 admission: the evaluator
is FIRST-DIFFERENTIAL ONLY, not a physical Hessian/evolution Hamiltonian. Full
auxiliary/nodal conditions, descriptor/background drift, physical window and
matching remain open. Runtime logs stay ignored; no provider or model change,
installation or measured billed-token saving is part of this mode.

## Coupled descriptor-action checkpoint: 20 October 2026

The [coupled descriptor report](../Theory/Gates/RES-001/RES001_R4C1_COUPLED_DESCRIPTOR_ACTION_V1_REPORT_2026-10-20.md)
records 955/955 and complete exact eight-worker replay after the bounded16-worker
first run. All54 tasks retain the true implicit velocity response, nonlinear
Ricci, constraints and background/two-form drift; independent full-Legendre
mixed controls prevent reuse of a frozen-y Hessian. The266-record preservation
guard passed. Sampled node Schur blocks are nonsingular, but their unscaled
canonical-row corrections can reach about1.14e20 in reference units. This is
not a physical cutoff or instability claim; physical normalization, admissible
space, full modes and the validity window remain open. The full matrix/spectrum
is not materialized by these operator-action controls. All old evidence remains
intact; logs are private/ignored and no provider/model or publication change occurs.

## Checkpointed canonical matrices: 20 October 2026

`Analysis/MasterTests/test_01_r4c1_canonical_spectrum_v3.py` separates the complete
finite-grid matrix calculation from the numerical spectrum stage. The parent
seals `matrix_*.json` and matching sidecars before any eigensolver call. Algebra
uses at most16 Windows-spawn processes; that pool exits before serial spectrum
evaluation with one local BLAS thread. All equations, constraints, drift terms,
80-decimal matrix construction and scientific tolerances remain frozen.

The earlier canonical-spectrum V2 run suffered native access violations in
`mkl_def.2.dll`; its four completed cases and failed numerical checks are
preserved. V3 uses the already installed NumPy/OpenBLAS eigensolver instead of
the SciPy/MKL eigensolver. There is no package installation, global environment
change or model/provider dispatch. Its15/15 execution smoke checks are not a
cosmological receipt. Spectrum matching and conditioning may still fail and
must remain explicit, even when matrix construction and eigenpair residuals pass.

Use the same fresh `--output`, bounded `--workers`, ignored `--progress-log` and
read-only `--replay` pattern above. `--grids` accepts registered17,25,33 grids.
`--keys 3:17:0,4:17:0,5:17:1,7:17:0` selects only those declared diagnostic keys;
it cannot establish full family/grid/node coverage. A partial output may use
`--resume` with the identical grids/keys and frozen inputs. Resume validates and
reuses sealed stages, including failed spectra; it never silently replaces them.
After `summary.json` exists, use replay or a fresh version/attempt, not resume.

Full replay recomputes every selected matrix from the action, including those
initially imported from the four preserved V2 cases. Compare exact bytes and
metadata; a successful replay of an unresolved spectrum remains unresolved.
The [canonical-spectrum report](../Theory/Gates/RES-001/RES001_R4C1_CANONICAL_SPECTRUM_V3_REPORT_2026-10-20.md)
owns the resulting evidence and limitations. Neither a full finite matrix nor
backend success establishes a continuum physical mode, cutoff or validity window.

Verified n17 checkpoint: all18 matrices and270/270 matrix controls; overall
305/347 UNRESOLVED with42 numerical spectrum failures. Complete fresh eight-worker
replay reproduced every byte and the same failures, with80 output files and a
400-record external preservation guard unchanged. Exit1 remains intentional;
READ_ONLY_REPLAY_EXACT is not a physics or spectrum pass.

## Canonical cancellation diagnostic: 20 October 2026

`Analysis/MasterTests/test_01_r4c1_canonical_conditioning_v1.py` operates on the
sealed full n17 matrices. It does not rebuild or modify the action. A constant
canonical momentum shear retains all mixed remainders, means, constraints,
drift and signs; block algebra is repeated at 80/100 working digits before
the unchanged binary64 spectrum evaluator. Singular momentum blocks are rejected,
not regularized or projected away. `--smoke` has 51 execution/algebra controls.

Use fresh `--output`, bounded `--workers`, ignored `--progress-log`, immutable
partial `--resume` and complete read-only `--replay` as above. Optional `--keys`
selects registered case:grid:orientation triples for a declared preflight only.
Only the parent seals full shear stages before the separate serial spectrum
stage. The maximum is16 spawn workers with a local one-thread BLAS context;
no installation or host/model/provider change is involved.

The complete first run has162/162 transformation controls and303/361 overall,
UNRESOLVED. All six eta=1/4 cases pass the finite-spectrum consistency checks;
twelve smaller-eta cases remain unresolved. The58 failures are29 numerical issues
checked at both working precisions, not58 distinct physical failures. Negative
action signs and nonoscillatory directions remain stored, not suppressed.
The [owning conditioning report](../Theory/Gates/RES-001/RES001_R4C1_CANONICAL_CONDITIONING_V1_REPORT_2026-10-20.md)
records replay, preservation and substantive limitations. Finite numerical
consistency is not physical stability, a ghost-free branch or a validity window.

The complete fresh eight-worker conditioning replay reproduces every byte and
the same failures. All80 output files and the502-record preservation guard remain
unchanged. Exit1 correctly retains UNRESOLVED; no physical gate is promoted.

## Bounded multiprecision pilot and exact blocks: 20 October 2026

`test_01_r4c1_mp_schur_pilot_v1.py` uses owned spawn children and180-second
phase limits, with live-process heartbeats and parent-only checkpoints. Its
24/24 smoke controls test the timeout path. The first full372-dimensional
35-digit Hessenberg phase reached that limit with no accepted factorization;
no remaining phases or full-family expansion were launched. This is a bounded
execution result, not a numerical spectrum pass or physics rejection.

`test_01_r4c1_exact_canonical_blocks_v1.py` subsequently verified all eighteen
complete numerical operators as exact302+70 canonical blocks, with no tolerance
pruning or omitted direction. Structural173/173, complete byte-exact read-only
replay,44 unchanged output files and a564-record preservation guard. The full
operator is retained: a later solver must process BOTH blocks and reconstruct
all372 coordinates. Blockwise factorization and any speed improvement are not
yet established. Use fresh --output or exact read-only --replay; this lightweight
structural audit is not a physical-mode calculation.

The [combined owning report](../Theory/Gates/RES-001/RES001_R4C1_MP_SCHUR_PILOT_V1_REPORT_2026-10-20.md)
keeps the timed-out attempt, successful structural audit and unchanged physical
holds separate. All prior negative/nonoscillatory evidence remains preserved.
