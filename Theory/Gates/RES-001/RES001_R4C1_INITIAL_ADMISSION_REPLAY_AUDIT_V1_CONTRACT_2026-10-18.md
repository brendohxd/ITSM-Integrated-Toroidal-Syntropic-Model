# Initial-admission replay auditor V1: separate bytes from metadata

18 October 2026. Freeze before auditor execution. Preserve the V1 source,
both completed fresh executions, every receipt/sidecar and failed replay.
No V1 action, equation, computation, tolerance, serializer or file is changed.

The original execution passed217/217 and nine interval certificates.
Its CLI replay stopped on the combined byte/metadata comparison of proof.json.
A second unchanged-V1 execution completed217/217; its four JSON payloads are
byte-identical to the original. The failed replay's recomputed payload was
not saved, so this does not establish the historical failure's cause.

Auditor: Analysis/MasterTests/audit_01_r4c1_initial_admission_replay_v1.py.
Fresh output: Analysis/MasterTests/outputs/r4c1_initial_admission_replay_audit_attempt_01.

Required:

- Pin and verify the unchanged V1 source, this contract, the frozen failed-
  replay note, auditor source and their sidecars.
- Snapshot all eight original payload/sidecar bytes, sizes and mtimes.
- Call the unchanged V1 calculate function, without monkeypatches or model/
  runtime configuration changes. Recompute every mathematical/interval check.
- Save the recomputed candidate in the NEW audit directory before comparison,
  so a failure is diagnosable without overwriting the original.
- Separately record recomputed-byte equality, original-byte changes during
  execution and original metadata changes. Inspect ALL files, not only the
  first failure. Record field-level JSON differences when present.
- Strict audited replay PASS requires217/217 checks, every recomputed byte
  equal to the original, and every original byte/size/mtime unchanged. Do not
  relax any criterion or use this auditor to relabel the failed CLI run.
- A pass proves this independently instrumented run; it does not identify
  the earlier failure's cause or guarantee the CLI never fails intermittently.

The audit's observer receipt may contain before/after metadata; no claim is
made that observer timing itself is a replayable physical prediction.
No result is promoted from local validation into physical validity or review.
If comparison differs, preserve the complete candidate and exact distinctions.
Stage2/full admission remain OPEN; Stage3 not entered; physics_pass=false;
gate_effect=NONE; Rule9_cleared=false; review DEFERRED. No vault mutation,
commit/push, publication, provider dispatch, runtime or action change.
