# Timestamp transport limitation and raw-integer preservation guards

21 October 2026. Provenance/checker correction only. No research equation,
numerical matrix, result, sidecar or original file timestamp was changed to
resolve the comparisons described here. No physical claim or gate is promoted.

## What happened

Before replay of CHECKPOINTED-QR-V2 tranche1, a private external guard compared
Python integer nanosecond timestamps with an earlier snapshot that had passed
through JavaScript JSON.parse/JSON.stringify. These epoch timestamps exceed
JavaScript's exact integer range. The transport rounded their values before
they were written back to the private snapshot.

All620 historical entries had identical SHA256 and file size; no entry was
missing.370 timestamps differed, by at most200ns. Every timestamp difference
disappeared when BOTH sides were compared at the earlier JavaScript floating-
number precision. This diagnoses the transport limitation, but does NOT
retrospectively prove nanosecond-exact timestamp preservation for every entry
covered only by that rounded historical snapshot. Earlier external timestamp
comparisons routed through JavaScript numbers have that resolution limitation.
Their exact SHA256/size comparisons are unaffected.

A separate diagnostic initially compared Python metadata tuples with JSON
metadata lists and consequently reported432 unequal records. Normalizing the
container representation through PYTHON JSON, without a floating-number
conversion, resolves that type-only discrepancy. Direct comparison against
the original CHECKPOINTED-QR-V2 run manifest proves ALL435 native source/runtime
metadata records match exactly, including their original integer timestamps.
The native executable's own before/after checks never used JavaScript numbers.

## Evidence and corrected forward method

The failed guard and diagnostic outputs are retained in ignored local artifacts;
they were not erased or relabelled as passes. The private rounded snapshot is
also retained. The corrected pre-replay guard:

1. Checks all620 historical hashes and sizes exactly, and explicitly bounds
   interpretation of their rounded timestamp comparison as described above.
2. Recomputes all435 native input/runtime metadata records and compares them
   exactly with the original manifest using Python integer arithmetic and
   container-normalized Python JSON.
3. Adds all76 completed-tranche output/sidecar files and saves a696-record raw
   snapshot directly into an ignored optimizer artifact. No timestamp values
   pass through JavaScript numbers. The artifact SHA256 is
   `4856330264421c968e90f820309f32a3a0ff8dcd7767e3152658ec0619de1272`.
4. Requires the post-replay comparison to load that original artifact in Python
   and compare hashes, sizes, exact integer timestamps and the file set. A
   compact count/digest may be returned to the assistant; integer records must
   not be parsed and reserialized through JavaScript numbers.

At this note's freeze, the fresh read-only quantum replay is RUNNING. A matching
baseline is not a completed replay. The first tranche has325/325 local checks,
status CHECKPOINTED_INCOMPLETE, and no completed full372-value spectrum. Its
precision-comparison, physical-mode, physical-window and parent-gate holds are
unchanged. Future replay success must be evidenced separately by the actual
terminal handle, byte comparisons and exact raw-integer post-replay guard.

No vault-management write, manuscript/site edit, publication, commit/push,
model/provider dispatch or package/global-runtime change. Rule9 DEFERRED;
Rule9_cleared=false; Stage2 INCOMPLETE; Stage3 NOT_ENTERED; physics_pass=false;
gate_effect=NONE. Preserve all original evidence and the historical diagnostics.
