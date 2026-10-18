# ITSM initial-constraint and paper checkpoint - 18 October 2026

Operator-authorized documentation, commit and push on
`recovery/v12-core-architecture`, following `0585f359`. This supplements the
[17 October finite-tilt checkpoint](ITSM_FINITE_TILT_CHECKPOINT_2026-10-17.md).
No frozen scientific result is rewritten or promoted by this checkpoint.

## Findings and their limits

| Work | Owning evidence | Finding and boundary |
|---|---|---|
| Regulator nodes | [187-check report](../Gates/RES-001/RES001_R4C1_REGULATOR_NODE_V1_REPORT_2026-10-17.md) | The unreduced action supplies necessary alignment and transport conditions without extending the singular inverse. All 18 archived runs and 72 full-response events remain. The action's cusp momentum matters for a complete canonical lift; this is not an allegation that the velocity archive omitted it. Persistence and all-order admission remain open. |
| Exact initial system | [222-check report](../Gates/RES-001/RES001_R4C1_INITIAL_CONSTRAINT_V1_REPORT_2026-10-18.md) | Nonlinear transverse first integral, coercive longitudinal shift problem, complete lapse energy and local flux. It supplies the restricted initial system, not a temporal evolution theorem. Its original partial acceptance is preserved. |
| Certified known initial surface | [217-check report](../Gates/RES-001/RES001_R4C1_INITIAL_ADMISSION_V1_REPORT_2026-10-18.md) | All nine family/eta points, all angles and continuous `|e|<=1/500` on the specified planar initial slice: unique mean root in the frozen bracket, both global charges and pointwise positive dust, with a uniform density lower bound above 0.1683 in reference units. Higher/rank-changing and acceleration consistency, full admission and evolution remain open. |
| Replay evidence | [Preserved CLI failure](../Gates/RES-001/RES001_R4C1_INITIAL_ADMISSION_V1_REPLAY_HOLD_2026-10-18.md), [strict audit contract](../Gates/RES-001/RES001_R4C1_INITIAL_ADMISSION_REPLAY_AUDIT_V1_CONTRACT_2026-10-18.md), [audit receipt](../../Analysis/MasterTests/outputs/r4c1_initial_admission_replay_audit_attempt_01/audit.json) | The first replay failed a combined byte/metadata guard. Its cause remains unknown. A fresh unchanged execution reproduced all four JSONs; a separately frozen auditor freshly recomputed the calculation, matched all eight payload/sidecar files and recorded preservation of original bytes, sizes and mtimes. The successful run does not diagnose or erase the failure. |
| ET2-A0 | [Topology/signature/free-spectrum report](../Gates/TOP-001/TOP-001_ET2_A0_TOPOLOGY_SIGNATURE_SPECTRUM_REPORT_2026-10-17.md) | 22/22 exact controls distinguish compact Euclidean time, compact space and Lorentzian time. Abstract/free-spectrum equivalence does not establish physical equivalence, a condensate action or causal continuation. Canonical spatial T3 and TOP-X4 are unchanged. |
| P1 rc7 | [Revision report](../../papers/ReleasePackages/2026-10-17/P1-rc7/P1_RC7_REVISION_REPORT_2026-10-17.md), [manifest](../../papers/ReleasePackages/2026-10-17/P1-rc7/P1_RC7_MANIFEST.json) | Retains the versioned seven-page review PDF and portable source ZIP. It identifies the historical package being tested and shows the conditional Planck conversion explicitly. Scientific dispositions are unchanged; author verification and independent review remain pending. |

The owning reports record their computational runs and replays. The checks for
this Git checkpoint concern stored hashes, source pins, successful/failed check
rows, replay comparisons, portable archive contents and retained holds. They do
not rerun the full scientific pipelines or rebuild a PDF. Same-author checks
are not independent scientific review.

## What remains next

Test acceleration/higher rank-changing consistency and persistence of the
candidate initial data before any full admission claim. Physical constrained
reduction, temporal Cauchy/energy control, a nonlinear remainder, a demonstrated
nonempty physical momentum/frequency window and justified healthy GR remain
required. The unfinished node-acceleration executable and its draft contract
are not part of this verified checkpoint; no outcome from them is claimed.

Stage 1 is complete only in the original linear prepared-dust scope. Stage 2
is incomplete; no family receives physical GO. Stage 3 is `NOT_ENTERED` because
genuine information identifying both the matter residue and nonlinear-force
normalization remains absent. No numerical acceleration prediction is sealed.
Negative-energy, defective-mode and earlier failed-proof findings remain.

Tests 1-3 `HOLD_SUBSTANTIVE`; MAT-001 `BLOCKED`; UVIR-003 `IN_PROGRESS`;
`K_Q=NOT_DERIVED`; `V=NOT_COMPUTED`; Stage 4A `CLOSED`; TOP-X4 unchanged.
`physics_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false`, review
`DEFERRED`. Supported provisional research may continue within its scope.

## Preservation and scope

The exact-byte manifest retains the versioned sources, contracts, reports,
receipt attempts, original sidecars and declared source dependencies. The
execution queue and review register keep their existing append-only entries.
The pinned `active_research.md` dashboard and all old manifests stay unchanged;
historical manifests describe historical mutable-index bytes.

The register also cites the main-manuscript alpha.16 editorial revision. Its
[editorial report](../../Manuscript/ITSM_Main_Manuscript_Working_READER_REVISION_2026-10-17.md)
is retained as a record of that separate work, not a public release of its
working source/PDF. Those working builds, their separate bibliography edits,
older reconciliation drafts and associated figure-generation work remain
local. No manuscript content is silently removed or rewritten.

Private optimizer logs, scratch QA, raw critiques/recordings/chats, vault data,
credentials and incomplete calculations are excluded. No files are deleted.
Only mutable documentation digests are refreshed; frozen evidence hashes are
verified, not repaired. Commit/push does not authorize a website deployment,
paper submission, vault sync, action selection or provider/model change.

## Verify the checkpoint

The [manifest](ITSM_RESEARCH_CHECKPOINT_2026-10-18.manifest.json) uses the
existing exact-byte checkpoint schema. From the repository root:

```powershell
python -B Scripts/verify_research_checkpoint.py --manifest Theory/Verification/ITSM_RESEARCH_CHECKPOINT_2026-10-18.manifest.json
```

Add `--revision INDEX` to check staged blobs, or `--revision HEAD` to check
the committed snapshot. `PASS_CHECKPOINT_INTEGRITY_ONLY` is artifact/provenance
integrity, not physical closure or publication clearance.
