# Checkpointed QR V2: complete retained problem, resumable numerical work

21 October 2026. V1 passes115/115 execution/algebra controls but its startup
metadata probe fails because this Python build exposes zlib as a built-in
module without __file__. No research quantum was launched. Preserve V1 and
its failure receipt. V2 records built-in origin and zlib versions and pins the
host Python executable when no separate zlib file exists. The local QR driver,
scientific inputs, precision, thresholds and resource budgets are unchanged.

Continue unchanged R4C1 Stage2 from BLOCK-SCHUR-V3's
terminal600-second QR limit. Do not restart that terminal attempt, repeat the
accepted Hessenberg reductions, or substitute the easier70-coordinate block
for the full372-coordinate problem.

## Fixed inputs and scope

Use all three sealed302-coordinate Hessenberg factors from V3:35 digits,
50 digits and50 digits with the fixed original-index canonical rescaling.
Keep Q AND H, every coupling, zero direction and sign. Retain the corresponding
complete70-coordinate Schur factors as frozen inputs. Only the union of both
complete spectra can satisfy the declared372-mode precision comparisons.
This one B1-frame eta=1/64, n17, orientation0 case is not an all-family result.
Pin the V3 executable, report, contracts, all retained factor files, aggregate
files, original inputs and their sidecars. Preserve all earlier failed versions.

## Transparent local iteration driver

The installed mpmath1.3.0 `hessenberg_qr` monolithic call does not expose
intermediate state. Implement a readable, versioned LOCAL iteration driver
mirroring its pinned outer loop, calling the UNCHANGED installed `qr_step`.
Retain the library copyright/license. Do not monkeypatch the installed library,
change packages/runtime, or change any shift, deflation criterion, precision
or convergence limit. In particular retain eps=ctx.eps/(100*n), the original
norm definition, exceptional shifts, maxits=4*dps and the reset rules.

Checkpoint only between completed outer iterations. Retain n0,n1,its,totalits,
norm,eps,maxits,precision and completion flag, plus the ENTIRE Q,H arrays.
Resume from the actual previous numerical state, not a reinitialized norm or
iteration counter. Encode multiprecision values with enough digits for an
exact working-precision round trip. A dimension-one factor is exact; no mode
is deleted. Internal unitary transformations are not physical canonical modes.

## Controls and complete acceptance

Compare uninterrupted and repeatedly serialized stop/resume execution with
the installed unmodified routine on small signed, real/complex, nonnormal,
zero/repeated/Jordan and dense controls. Require identical serialized complete
Q,R values, not only matching eigenvalues. Reject omitted or inconsistent
resume fields/precision and test owned-child timeout/cleanup. Controls are
execution/algebra evidence only, not independent scientific peer review.

At every accepted checkpoint verify the COMPLETE302-dimensional factorization
backward error, unitarity and Hessenberg structure <=1e-8, independent
multiprecision full-coordinate matvec probes <=1e-8, full trace and trace-square
identities, monotone iteration progress and provenance-chain consistency.
On completion require triangularity. Retain full final Q,R and every eigenvalue.
Then reconstruct all372 eigenvalues using both blocks; require35/50 and the
fixed independent-rescaling comparisons <=1e-6. These are not certified
forward eigenvalue enclosures, left/right physical normalization, or stability.

## Bounded execution, storage and replay

Use up to three owned Windows-spawn workers, one per independent precision/
rescaling branch. Each quantum executes at most FOUR completed outer
iterations, with a180-second hard child budget. The parent monitors actual
process handles, emits private liveness messages, and terminates/joins only its
owned children on failure/expiry. A child timeout is terminal for that attempt;
preserve all completed checkpoints. Never label it a physics failure.

One advance tranche permits at most TWELVE quanta per unfinished branch.
An unfinished but successful tranche is a saved continuation, not an accepted
full spectrum or terminal failure. A subsequent authorized goal turn may
advance that SAME unfinished attempt from its last exact checkpoint. Freeze
tranche receipts append-only; do not overwrite an earlier summary or checkpoint.
Use deterministic gzip for the full numerical checkpoints, pinning Python's
compression implementation/version. Limit the attempt to2GiB of retained
outputs and require at least3GiB free before advancing; stop without deleting
research evidence if either storage condition fails. No speedup is promised.

Require source/sidecar and external earlier-output metadata guards. A fresh
read-only replay must recompute every saved quantum from its declared predecessor
and reproduce numerical/check bytes exactly. This does not claim a fresh replay
of upstream action/Hessian/Hessenberg calculations. Runtime/PIDs/wall time stay
in ignored logs and outside deterministic scientific receipts.

## Unchanged physical and authority boundaries

The prior six numerically consistent cases, twelve unresolved cases and all
negative-action/nonoscillatory evidence remain unchanged until the applicable
full controls actually finish. Retain physical perturbation/energy/clock,
continuum/node and25/33 refinement, nonlinear persistence, full coupled
interactions/cutoff, healthy-GR recovery and both identifying matching inputs
as substantive requirements. Stage1 complete only in the registered bounded
linear prepared-dust scope; Stage2 INCOMPLETE; Stage3 NOT_ENTERED;
Tests1--3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED;
UVIR-003 IN_PROGRESS; Stage4A CLOSED; TOP-X4 unchanged. Rule9 DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE. No new action/parent,
state adoption/evolution, vault-management mutation, manuscript/site edits,
publication, commit/push, paid dispatch or model/global-runtime changes.
