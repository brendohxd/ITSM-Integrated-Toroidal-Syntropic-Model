# ITSM research and paper checkpoint - 17 October 2026

Operator-authorized documentation, commit and push on
`recovery/v12-core-architecture`, following branch tip `8f815b84` (14 October).
This preserves existing work and improves navigation. It does not perform a
new scientific derivation, independent review, paper submission or deployment.
The [13 October checkpoint](ITSM_RESEARCH_CHECKPOINT_2026-10-13.md) remains an
immutable earlier snapshot, not a manifest for the subsequently edited papers
or append-only navigation indexes.

## What advanced

| Route | Retained evidence | Meaning and limit |
|---|---|---|
| Compact T3 methods | [14 October report](../../Analysis/MasterTests/COMPACT_T3_CONTROL/REPORT_2026-10-14.md), 765/765 local checks and recorded exact replay | Reciprocal lattice, mode normalization and response interface; geometry/frequencies do not identify matter coupling or nonlinear force normalization |
| Three-family homogeneous comparison | [Fixed-charge report](../Gates/RES-001/RES001_R4C1_THREE_FAMILY_FIXED_CHARGE_KINETIC_V3_REPORT_2026-10-16.md), 1470/1470 and recorded exact replay | Positive homogeneous block in the separately fixed two-charge ensemble; not removal of the original ensemble's negative direction or full physical stability |
| Three-family nonzero modes | [Finite-k report](../Gates/RES-001/RES001_R4C1_THREE_FAMILY_FINITE_K_V3_REPORT_2026-10-16.md), 602/602 and recorded exact replay | Positive declared kinetic/principal-speed blocks coexist with a defective zero-speed branch and negative instantaneous dust-clock energy; no physical family GO |
| Prepared initial charges | [Initial-charge completion](../Gates/RES-001/RES001_R4C1_INITIAL_CHARGE_COMPLETION_V4_REPORT_2026-10-16.md), 392/392 and recorded exact replay | Higher-order initial corrections are identified separately; archived quadratic preparation is not reclassified as a complete nonlinear fixed-charge solution |
| Cubic coefficients and evolution | [Initial jets](../Gates/RES-001/RES001_R4C1_CUSP3_LOCAL_INITIAL_JET_V2_REPORT_2026-10-16.md) and [evolution](../Gates/RES-001/RES001_R4C1_CUSP3_EVOLUTION_V1_REPORT_2026-10-16.md) | Initial all-field jets and declared finite-mode evolution are distinct results, not the full finite-amplitude nonlinear solution |
| Full weighted evolution | [Corrected low-rank result](../Gates/RES-001/RES001_R4C1_LOW_RANK_WEIGHTED_EVOLUTION_V2_REPORT_2026-10-17.md), 671/671 and recorded exact replay | Complete 20-state mathematical evolution norm; not a physical Hamiltonian or cutoff |
| Infinite cubic tails | [Coupled V3 report](../Gates/RES-001/RES001_R4C1_CUSP3_COUPLED_TAIL_V3_REPORT_2026-10-17.md), 354/354 plus 45/45 companion checks | Earlier sufficient weak bound, including mean and retained low modes; preserved unchanged alongside its improvements |
| Source-aware estimate | [Owning report](../Gates/RES-001/RES001_R4C1_CUSP3_SOURCE_AWARE_WINDOW_V1_REPORT_2026-10-17.md), 336/336 and complete exact replay | Sufficient weighted O(|m|^-3) bound; all 22 field series absolutely summable at this cubic order in the registered cases; physical validity remains open |

Counts above identify local calculation receipts, not independent physical
tests or independent reviewers. Recorded replay refers to the owning report's
execution evidence, not a fresh execution of every pipeline during this Git
checkpoint. The checkpoint verifier checks bytes and declared source pins only.

## Latest bound, stated precisely

The source-aware construction retains the lower odd-mode initial transient,
the full fast particular response and complementary evolution, background/
basis/momentum drift, all reconstructed constraints and separate zero-mode
and retained-mode bounds. Its improvement from O(|m|^-1) to O(|m|^-3) is a
sufficient estimate, not a measured or sharp asymptotic equality.

Its domain is the unchanged-action prepared planar order-|e|^3 sector on the
coordinate 2*pi torus, leading w(t)cos(40z), t in [0, 1/20], at three families
times eta = 1/4, 1/64, 1/1024. It does not prove a continuous-eta result,
arbitrary initial data, useful finite-amplitude accuracy or healthy GR.
The actual LambdaU time derivative remains NOT_BOUNDED. Large inherited
sufficient amplification factors are not observed growth or an instability
proof; they still prevent certifying useful accuracy by these estimates.

The restartable local companion freshly recomputed all nine cases and the
complete original summary: ten original payloads match exactly. The replay
receipt records 909 source-metadata and 20 original-evidence metadata records
preserved. It reports `PASS_READ_ONLY_PARALLEL_REPLAY_EXACT`, exit zero.
The original serial CLI was not observed to finish; its interrupted attempts
are not retrospectively described as successful.

## Failures and provenance remain visible

The [rejected weighted inverse](../Gates/RES-001/RES001_R4C1_WEIGHTED_EVOLUTION_CUBIC_REJECTION_REPORT_2026-10-17.md)
retains its 37/38 failed construction and exact failed replay. Coupled-tail
V1 (13/17) and V2 (23/26) remain separate from V3: complex conjugation and
zero-mode chart implementation errors are explained by frozen addenda, not
relabelled as action failures or silently replaced receipts. Earlier syntax,
binding, numerical and solver attempts are likewise retained as distinct files.

Existing frozen source/report hashes are not refreshed. The queue and deferred
review register remain append-only; their new source-aware entries preserve
the complete prior byte prefix. Only deliberately mutable documentation gets
new sidecars. Three inherited missing UVIR sidecars remain explicit in the
source-aware evidence; their source bytes are pinned, and no sidecars are
fabricated to hide that historical state.

The preserved P1 rc3 `main.tex` / sidecar pair has a pre-existing mismatch:
the retained source is SHA256 `4b0d0aefd22f81ea20057936ee7566f24eb12b9b49b2fb22bebdfdcc5a6f2510`,
while its old sidecar claims `5597cb6eeeb5b70c6264eb606c78f95319ace9c31dd2ea4fd58cc1a27228b1d4`.
The same source bytes and old sidecar are already present at parent tip
`8f815b84`; this checkpoint did not introduce their disagreement.
Neither is rewritten. This concerns the preserved historical pair, not the
matching current P1 rc6 or P2 rc4 source/PDF hashes. The checkpoint manifest
pins both historical files and explicitly records their disagreement.
The frozen compact-T3 control also pins `active_research.md`, so that dated
dashboard remains unchanged; README, this checkpoint and the execution queue
provide the latest navigation without invalidating the frozen control input.

## Paper preparation retained, not new publication clearance

- P1 rc4 through rc6 and P2 rc4: versioned PDFs, current sources, portable
  source members, preparation/revision reports and preserved previous versions.
  [P1 rc6](../../papers/ReleasePackages/2026-10-17/P1-rc6/P1_RC6_REVISION_REPORT_2026-10-17.md)
  improves motivation, argument order and placement of reconstruction criteria;
  its 21 displayed equations, bibliography and figure are preserved.
- [P1/P2 rc4](../../papers/ReleasePackages/2026-10-17/P1_P2_rc4/P1_P2_RC4_REVISION_REPORT_2026-10-17.md)
  clarifies normalization, topology/statistical comparisons and P2 closure/
  threshold scope. P2's sensitivity receipt remains 18/19 FAIL, not a repaired
  pass. Author final verification and applicable independent review are pending.
- Source ZIPs stay local under the existing exclusion. Their sidecars/manifests
  document local provenance; portable sources are retained directly in Git.
  No existing PDF or scientific receipt is rebuilt for this checkpoint.

## Remaining walls and next route

Stage 1 remains complete only in its original bounded linear prepared-dust
scope. Stage 2 is incomplete: a finite-amplitude metric/frame/matter/regulator
constraint reduction, physical kinetic/energy and characteristic assessment,
controlled nonlinear remainder, nonempty physical domain and justified GR
recovery remain unresolved. A raw velocity-block signature is not already a
physical ghost classification; an aligned quadratic operator cannot substitute
for the finite-amplitude calculation. No automatic TOP-X4 pivot is authorized.

Numerical Stage 3 remains NOT_ENTERED. Independently identifying matter-residue
and nonlinear-force matching inputs are still missing. A residue calculated
from assumed coefficients does not identify those coefficients. No numerical
C_chi or a0 prediction is sealed and no target fitting is introduced.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage 4A CLOSED; TOP-X4 unchanged.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Integrity, scope and privacy

The companion `ITSM_RESEARCH_CHECKPOINT_2026-10-17.manifest.json` records the
selected exact-byte files, current scientific source pins, retained receipt
dispositions and exclusions. Use `Scripts/verify_research_checkpoint.py` with
its explicit `--manifest` and optional `--revision INDEX` or commit reference
to inspect the worktree, staged or committed bytes. The unchanged generic
checker is expected to return FAIL for exactly the preserved historical P1
sidecar mismatch above. It is not advertised as an all-sidecars PASS. All
manifest byte/hash and current scientific source-pin comparisons must match;
any additional failure is unexpected and blocks this checkpoint's push.
This is artifact integrity, not new scientific validation or a programme rerun.

All `.local/` logs, vault databases/backups, raw audio/transcripts, credentials,
local ZIPs, scratch QA and the separate unreviewed core-manuscript working
files remain outside this commit and untouched. The root-level
`qa_and_append_cusp3_evolution_20261016.py` is excluded as a private scratch
helper, not used to append anything again. No files are deleted. This branch
push does not dispatch Pages, submit a paper or mutate the memory vault.
