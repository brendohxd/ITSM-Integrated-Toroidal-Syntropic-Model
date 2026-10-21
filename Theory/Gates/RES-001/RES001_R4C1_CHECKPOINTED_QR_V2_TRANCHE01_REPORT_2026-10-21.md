# Checkpointed QR V2, tranche1: exact continuation verified; spectrum unfinished

21 October 2026. Unchanged R4C1 Stage2. One registered B1-frame eta=1/64,
n17, orientation0 case; no new action, physical state or mode admission.

## Result

The first tranche retains36 complete numerical checkpoints:12 per35-digit,
50-digit and independently canonically rescaled50-digit branch. All325 local
factor/state/source checks pass. A fresh read-only replay recomputed every
quantum from its pinned predecessor, reproduced every saved numerical/check
byte and the tranche receipt, returned exit0 and printed READ_ONLY_REPLAY_EXACT.
The separate696-record raw-integer guard found no changed, added or missing
record and no hash, size or exact integer-mtime difference.

The disposition is **CHECKPOINTED_INCOMPLETE**, not a completed Schur spectrum
or physical pass. All three large blocks remain unfinished:

| Branch | Saved quanta | Outer iterations | Actual QR steps | Active Schur end index |
| --- | ---: | ---: | ---: | ---: |
|35 digits |12 |48 |39 |293 |
|50 digits |12 |48 |40 |294 |
|50 digits, fixed rescaling |12 |48 |40 |294 |

These are internal algorithm counters, not physical dimensions or mode counts.
Every checkpoint retains the ENTIRE302-coordinate Q,H arrays, including already
deflated portions, all couplings, zero directions and signs. The complete
70-coordinate factors also remain required frozen inputs. The full372-value
precision/rescaling comparisons cannot run before all large-block QR branches
finish. No intermediate Schur column is treated as a normalized physical mode.

## What changed in implementation

The monolithic BLOCK-SCHUR-V3 QR phase reached its600-second budget. Its accepted
Hessenberg factors are reused without rerunning them or restarting that terminal
attempt. A readable local driver mirrors the pinned mpmath1.3.0 outer loop and
calls the unchanged installed qr_step. Norm, eps, shifts, deflation/reset rules,
maxits=4*dps and working precision are retained. All loop state is serialized
between completed iterations; the original norm is not reinitialized on resume.

The installed-versus-local, repeated serialized stop/resume, complete Q,R array,
signed/complex/nonnormal/zero/Jordan, malformed-state and owned-timeout controls
pass115/115. They are same-author execution/algebra controls, not independent
scientific review. V1's built-in-zlib startup metadata failure launched no
research quantum and remains preserved. V2 records built-in origin/versions and
the host executable when no separate zlib file exists; no package was changed.

At most three owned workers execute four outer iterations per quantum with a
180-second child budget. This tranche ended normally after the registered12
quanta per branch, not through a timeout. Deterministic gzip checkpoints are
append-only and preserve predecessor hashes. No speedup or billed-token saving
is inferred from this progress. The attempt's2GiB output cap and3GiB free-space
floor remain in force; retained tranche1 output is330113570 bytes across76 files.

## Provenance and the timestamp transport correction

There are216 frozen source pins and435 native source/runtime metadata records.
The native integer metadata comparison matches the original manifest exactly.
The earlier external snapshot's620 hashes/sizes also match. Its timestamps had
passed through JavaScript numbers, so those older external timestamp checks
have a submicrosecond resolution limitation; this is documented, not erased,
in [the transport note](../../Verification/ITSM_PROVENANCE_TIMESTAMP_TRANSPORT_NOTE_2026-10-21.md).
The retained failed diagnostics include a separate tuple/list comparison error.
No scientific file, sidecar or original timestamp was rewritten to resolve them.

The corrected696-record raw snapshot is stored directly by the optimizer,
without JavaScript integer conversion. The post-replay guard loads that original
snapshot in Python and compares every record and the file set exactly. The new
exact result does not retrospectively strengthen rounded historical timestamps.
Private runtime logs/snapshots remain ignored; they are not publication artifacts.

| Artifact | SHA256 |
| --- | --- |
| V2 contract |567e466dd6b5a056619ba5db10c6b3a874f91a6db4073e359ddf9bf03399ba1f |
| V2 executable |00d3031b5280880bf4e31f80dba9ef16f5757b570b55dad121ed431a145337af |
| run_inputs.json |8f46e0f0802e21dcbbd5ec40d724540b4849325e3e8816ffea1f7963638cbe90 |
| tranche_0001_summary.json |e3ad821ef6a03e18fb56a7b5ac48df675f547167972997566a14a5a63068aaba |
| raw pre-replay snapshot |4856330264421c968e90f820309f32a3a0ff8dcd7767e3152658ec0619de1272 |
| post-replay guard output |435911a7f1a356ee20d92666a21f70185e95fe006e5606ad043959cd1bd9d527 |

Executable: Analysis/MasterTests/test_01_r4c1_checkpointed_qr_v2.py.
Receipts: Analysis/MasterTests/outputs/r4c1_checkpointed_qr_v2_attempt_01/.
This is a replay from the declared frozen Hessenberg inputs, not a fresh
upstream action/Hessian/Hessenberg replay or independent peer review.

## Next work and unchanged physical disposition

The saved attempt may advance from quantum12; never overwrite tranche1 or its
checkpoints, restart accepted reductions, loosen thresholds or substitute the
easier70-coordinate spectrum. Finish this one pilot and its full comparisons
before multiplying expensive QR work across other registered cases.

Numerical precision alone cannot supply the admitted physical perturbation/
energy/clock space. Both simultaneous continuum-node traces, weighted regularity,
full auxiliary hierarchy/persistence,25/33 refinement, nonlinear interactions/
cutoff and justified healthy-GR recovery remain substantive. The descriptor
owning report retains these requirements explicitly. Both matter-residue and
nonlinear-force identifying matching inputs remain missing. No numerical C_chi,
a0, physical cutoff, ghost-free branch or observational fit is derived here.

Earlier six numerically consistent cases, twelve unresolved cases and all
negative-action/nonoscillatory evidence remain unchanged. Stage1 complete only
in its registered bounded linear prepared-dust scope; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1--3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED;
TOP-X4 unchanged. Rule9 DEFERRED; Rule9_cleared=false; inherit BLOCK-SCHUR-V3
and all transitive review debt. physics_pass=false; gate_effect=NONE.
No new action/parent, state adoption/evolution, vault-management write,
manuscript/site edit, publication, commit/push, paid provider dispatch or
model/package/global-runtime change.
