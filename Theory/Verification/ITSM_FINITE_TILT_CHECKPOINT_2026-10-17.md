# ITSM finite-tilt checkpoint - 17 October 2026

Operator-authorized documentation, commit and push on
`recovery/v12-core-architecture`, following `d00acd43`. This supplements the
[earlier checkpoint](ITSM_RESEARCH_CHECKPOINT_2026-10-17.md); it does not revise
that frozen evidence, perform new scientific work, or clear a physical gate.

## What advanced, and what it means

| Calculation | Owning evidence | Result and boundary |
|---|---|---|
| Complete finite-tilt velocity map | [Constraint V1 report](../Gates/RES-001/RES001_R4C1_FINITE_TILT_CONSTRAINT_V1_REPORT_2026-10-17.md) | 243/243 local checks; complete 22-field temporal Hessian and independently varied unit/dust auxiliaries. No hidden primary constraint restores an algebraic regulator on the regular Legendre patch. This is not the physical constrained Hessian or a propagating-mode count. |
| Canonical lapse and shift | [Canonical V2 report](../Gates/RES-001/RES001_R4C1_FINITE_TILT_CANONICAL_V2_REPORT_2026-10-17.md) | 204/204 local checks; full coupled inverse, lapse/shift functionals and local lapse-gradient flux. Planar periodic bracket controls do not prove general 3D closure or admit the prepared initial state. |
| Independent implementation bridge | [Backend addendum](../Gates/RES-001/RES001_R4C1_FINITE_TILT_CANONICAL_BACKEND_V1_ADDENDUM_2026-10-17.md) and [receipt](../../Analysis/MasterTests/outputs/r4c1_finite_tilt_canonical_backend_attempt_01/verification.json) | 397/397 checks comparing the fast implementation with the original density at 18 general first-jet controls. Same-author implementation independence is not independent peer review. |
| Preserved failed attempt | [Original V1 summary](../../Analysis/MasterTests/outputs/r4c1_finite_tilt_canonical_attempt_01/summary.json), [normal-form addendum](../Gates/RES-001/RES001_R4C1_FINITE_TILT_CANONICAL_V2_NORMAL_FORM_ADDENDUM_2026-10-17.md) | V1 remains 203/204 FAIL. V2 corrects a symbolic exact-zero assertion after substitution. Its numerical/action functions and tolerances are unchanged; all 16 non-summary payloads match the original attempt byte-for-byte. |

The three successful calculations have complete fresh read-only replays
recorded in their owning reports. This checkpoint independently verifies
stored bytes, sidecars, declared source hashes and receipt dispositions; it
does not claim to rerun those scientific pipelines. No full replay of the
failed V1 attempt is asserted.

## Consequences for the live programme

The missing canonical-formula dependency is resolved only on the declared
regular future-unit/positive-dust branch: positive lapse and spatial metric,
nonzero regulator coupling and frame tilt, and nonsingular complete Legendre
complement. Its inverse must not be extended by division through zero tilt.
The registered transverse wave has alignment/profile-zero points; no new
node calculation, constraint-admissible finite-amplitude preparation, or
arbitrary-3D closure proof is supplied by these receipts.

The remaining physical requirements are the full constraint reduction,
admissible data and Cauchy/energy domain, physical reduced Hessian, nonlinear
remainder, a demonstrated nonempty physical validity window and justified GR
recovery. No physical family GO or ghost/healthy classification follows from
the unreduced rank or finite controls. Earlier negative energy and defective
zero-speed findings remain unchanged.

Stage 1 is complete only in its registered linear prepared-dust scope.
Stage 2 remains incomplete. Stage 3 is `NOT_ENTERED`: genuine information
identifying both the matter residue and nonlinear-force normalization remains
absent. No numerical acceleration coefficient is sealed.

Tests 1-3 `HOLD_SUBSTANTIVE`; MAT-001 `BLOCKED`; UVIR-003 `IN_PROGRESS`;
`K_Q=NOT_DERIVED`; `V=NOT_COMPUTED`; Stage 4A `CLOSED`; TOP-X4 unchanged.
`physics_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false` and review
`DEFERRED`. The two new review-register entries retain inherited dependencies;
deferred review alone does not stop supported provisional research.

## Preservation and publication scope

Retain the four finite-tilt receipt directories, four versioned executables,
contracts, addenda, owning reports, failures and original sidecars. The
execution queue and deferred-review register contain the already-recorded
append-only continuations; this checkpoint does not append another scientific
result or rewrite their earlier entries. The pinned `active_research.md`
dashboard remains unchanged. Only the edited mutable README's digest is
refreshed; frozen artifact digests are checked, not repaired.

The exact-byte manifest also includes the inherited source pins needed to
verify this boundary. Old manifests remain historical snapshots of then-current
mutable indexes, not manifests for their subsequent approved appends.

Separate P1 rc7/bibliography work and unreviewed core-manuscript working files
remain local and untouched. Private optimizer logs, scratch QA, raw chats,
recordings, vault databases and credentials are excluded. This is a research
checkpoint, not paper publication, submission, website deployment, vault sync,
action selection or model/provider dispatch.

## Integrity verification

The [manifest](ITSM_FINITE_TILT_CHECKPOINT_2026-10-17.manifest.json) records
byte lengths, SHA-256 digests, scientific source pins and unchanged holds.
Run the existing checker from the repository root:

```powershell
python -B Scripts/verify_research_checkpoint.py --manifest Theory/Verification/ITSM_FINITE_TILT_CHECKPOINT_2026-10-17.manifest.json
```

For staged blobs add `--revision INDEX`; for the committed snapshot add
`--revision HEAD`. A `PASS_CHECKPOINT_INTEGRITY_ONLY` result verifies this
artifact boundary, not physical validity or review clearance.
