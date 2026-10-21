# Coupled node acceleration V2: operator-requested multicore implementation

18 October 2026. Supplement the unchanged V1 scientific contract. The operator
requested use of all 16 available logical processors. This computer reports
8 physical cores and 16 logical processors; these are not 16 physical cores.

The original V1 run was deliberately interrupted for this execution rewrite,
not because of a failed physical equation. It returned no scientific receipts.
Keep its frozen source, contract, empty attempt01 directory and ignored terminal
log. Do not label the interrupted calculation a physics failure or a completed audit.

## Execution changes only

- Add --workers N, default 16, bounded by usable logical processors and Windows
  process-pool limits. Workers use the standard-library spawn process context,
  not CPU-bound Python threads. No new packages, providers, paid sessions,
  global settings, physical parameters or model/runtime changes are adopted.
- Prefetch the exact required symbolic derivative table across worker processes.
  Every task differentiates the same original density BEFORE imposing the same
  nodal symbol values. Use exact atom replacement for this symbol-only map;
  do not replace the original field variation with already-specialized matrices.
  Reject missing derivative keys. Gather results in a fixed canonical key order.
- Run independent coordinate-control seeds and the nine registered family/eta
  cases as separate jobs where useful. Never create nested pools or share the
  mutable mpmath precision/context across processes. Each numerical worker
  explicitly sets mp.dps=100 and iv.dps=80.
- Only the parent writes scientific receipts, after all required jobs return.
  A failed worker must propagate an error, not disappear from the result set.
  Sort/gather jobs by original case/seed order. Worker count, process IDs and
  wall-clock timings must not alter the scientific JSON payloads.
- Add an ignored, fresh, local progress journal and periodic diagnostic stack
  log. They are operational diagnostics, not scientific evidence or public files.
  Report actual completed tasks/worker use, not a promised 16-fold speedup.
  Dependency-bound serial algebra remains serial. Do not duplicate independent
  work merely to display all CPUs busy.

## Verification

Freeze final source/contract hashes after AST preflight, before execution.
First verify serial/process-pool deterministic task results in a bounded
non-scientific smoke mode. Then run the unchanged full calculation in a fresh
attempt02 directory. Inspect every failed/unknown check and every inconclusive
physical disposition. No new physical result exists until those jobs return.

Validate exact read-only replay. Where feasible replay with a different worker
count and require identical scientific bytes, sidecars, sizes and mtimes.
The original full-action coordinate controls, precision, domain, rejection
criteria, amplitude normalization and physical acceptance requirements remain
unchanged. The optimization does not supply a missing physical input.

All inherited gate and review holds remain: Stage2 INCOMPLETE; Stage3 NOT_ENTERED;
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED;
full admission/persistence, physical window, healthy GR and both identifying
matching inputs remain open. No previous hashes/results are overwritten, no
state is adopted/evolved, and no commit, push, publication, submission, vault
mutation, manuscript/site edit, new action or provider dispatch is included.
