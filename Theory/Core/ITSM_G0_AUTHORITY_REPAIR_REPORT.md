# ITSM G0 authority and evidence repair report

**Date:** 2026-08-25  
**Branch:** `recovery/v12-core-architecture`  
**Result:** `PASS_G0_AUTHORITY_REPAIR_NO_PHYSICS_PROMOTION`  
**Commit/push/publication:** not performed

## Outcome

The repository now has one fail-closed scientific authority chain. The G0
repair does not endorse the theory or clear a physics gate; it prevents child
reports, exploratory code, manuscript packaging and web pages from overriding
the signed parent decisions.

Normalized boundary:

- UVIR-003: `IN_PROGRESS`, `HOLD_TIER1_CLOSURE`, `physics_pass=false`;
- MAT-001: `BLOCKED`, `V NOT_COMPUTED`, `K_Q NOT_DERIVED`;
- MAT R5: `HOLD_DECLARED_ACTION_UNDERDETERMINES_V`;
- R5-P1: `OPEN_RESEARCH_CANDIDATE`;
- STAT-001: `NOT_STARTED_AS_CLOSED_GATE`;
- CBR-002: `OPEN`;
- VOR-001 and RES-001: open scaffolds only.

## Frozen workspace evidence

The pre-repair state is sealed in:

- `ITSM_G0_WORKSPACE_EVIDENCE_MANIFEST.md`;
- manifest SHA-256 `B9794E9B2B9CA7ACAB02121B53D4E63990139A1A2FB6DD0BD4DDC571B5F6BDDE`.

At capture time:

- local HEAD: `4310a9ad7bc27b7e0f4169586210818761119936`;
- live remote branch tip, rechecked read-only on 2026-08-25:
  `c17a6dbe6efb53c0f92c08955f5306f5528bc054`;
- local branch is two commits ahead of that remote tip;
- staged changes: none;
- all listed pre-existing user/model changes were preserved before G0 edits.

No fetch, checkout, reset, move, deletion, commit, push or publication occurred.

## Rule-9 triangulation

Three read-only roles received the core identity and fail-closed status before
inspection. Exact prompt bytes and SHA-256 seals are recorded in the workspace
manifest:

| Role | Prompt SHA-256 | Independent conclusion |
|---|---|---|
| A — mathematical/physical hostile audit | `079B6422CDB09EE090E9FA3393D8AFBDAE2F0CC5A056BF1AF8847247E6EDDFAE` | No gate promotion is supported; identified coefficient, sign, branch, dimensional and PPN failures. |
| B — pipeline/provenance audit | `931D390D1F448C1E7459C4807D7115471194F0E076082D310ACED78D672E283C` | Found missing-sidecar acceptance, CRLF hash contamination, runtime drift and scoped evidence boundaries. |
| C — authority/claim audit | `DDE3375145B5723C2ADFC526017B8C1324E37564E0F681A52987B26DB81057BF` | Found duplicate-dashboard, manuscript, Pages and parent-child promotion conflicts. |

Consensus was complete on the canonical statuses and on the need to quarantine
the promoted MAT/UVIR/STAT/CBR chain. The only classification nuance was that
R5-P1 Task 2 may be retained as a negative toy note; it is still non-authority.
No disagreement required a derivation halt.

## Provenance repair and bounded recomputation

### UVIR full-gate closure audit

The producer now serializes canonical UTF-8/LF bytes and writes a mandatory
SHA-256 sidecar.

- producer SHA-256:
  `48930DE62062E39E80A753012E200EE62E8A849B49FE8FA0AD84F33E6F406383`;
- JSON SHA-256:
  `31FD6EF69D73F48563C144AA1C8426AB51D41599434B298E1CD064F13E8C59B1`;
- result: scoped checklist audit PASS while UVIR remains `IN_PROGRESS`.

### MAT UVIR-to-MAT handoff audit

Missing sidecars now fail closed. A temporary negative control omitted the
closure sidecar and correctly exited `1` with
`FAIL_MAT001_UVIR_HANDOFF_CONTRACT`. The repaired canonical chain then passed.

- producer SHA-256:
  `61246D4AE870D40D84E159F74D0988D8B442EF8F852813CD3A4EBE53C128BE89`;
- JSON SHA-256:
  `8E9ED21F25B6EFC122D56B1FB0EA0AAB5C1182E1A2202F80125F9529F62B5DE5`;
- scientific boundary: symbolic projection work is authorized, but numeric
  matching, Stage 4A reopening, MAT PASS, UVIR PASS and downstream Derived use
  remain forbidden.

### MAT R5 identifiability audit

The mutation suite passed. A temporary production run was byte-identical to the
canonical JSON, and the sidecar producer was changed from platform text mode to
canonical bytes.

- producer SHA-256:
  `1202E447BE39127CACBF4E9C1AC08D1449795A18C24F65C20416EF97904686A3`;
- JSON SHA-256:
  `20B6A0BD506755DCFB8933668C8F2DC99B90C8BC4917DF8982BB9F59C0C50F24`;
- result: `PASS_MAT001_R5_IDENTIFIABILITY_AUDIT_HOLD` — a scoped audit PASS
  whose physical conclusion is HOLD.

### UVIR local four-leg outputs

The apparent CSV/JSON modifications are CRLF-only; Git-normalized blobs equal
HEAD and there is no numerical content change. They were not presented as a
fresh exact reproduction because the current runtime differs from the pinned
NumPy/SciPy environment, SymPy was previously omitted, sidecars are absent and
the transitive numerical provenance is under-specified. They remain scoped
historical local-kernel evidence only.

## Applied dispositions

The full 25-item map is in `ITSM_G0_CONTRADICTION_LEDGER.md`.

- **Kept:** signed MAT R5, R5-P1 specification, signed UVIR Stage-5 HOLD,
  fail-closed RES artifacts, scoped VOR templates and alpha.12 authority.
- **Repaired:** canonical dashboard, claim ledger, Master Plan comparator
  language, architecture claim boundaries, Solar-System diagnostic, VOR gate,
  STAT gate specification, provenance producers, README and Pages sources.
- **Quarantined without deletion:** duplicate dashboard, MAT R6, R5-P1 T1-T7,
  promoted UVIR chains, STAT report, CBR designed/scale closures, healing-length
  test, alpha.13/v11.4.1 manuscript package and current submission cover letter.
- **Rejected as live claims:** MAT/UVIR clearance, exact physical cutoff,
  Bayesian-MCMC STAT completion, derived `C=1` or `2/3`, derived inverse-`2pi`
  coefficient, solved Solar-System screening and downstream cosmology success.

## Downstream status verification

Local Pages source now says alpha.12, UVIR in progress, MAT blocked and STAT not
closed. A separate read-only request to `https://itsm-cosmology.com/` and
`/research.html` returned HTTP 200. The deployed HTML is not byte-identical to
the local working source, but its live status cards were already fail-closed:

- alpha.12 frozen;
- UVIR-003 in progress;
- MAT-001 blocked with `V NOT_COMPUTED`, `K_Q NOT_DERIVED`, Stage 4A closed;
- downstream gates gated.

Therefore this turn makes no deployment claim and performs no publication.

## Validation summary

- Three independent role audits converged.
- Closure and handoff scripts passed after repair.
- Missing-sidecar negative control failed as required.
- JSON-sidecar digests match and use the canonical sidecar format.
- MAT R5 mutation suite passed and temporary/canonical JSON hashes matched.
- Live Pages requests returned HTTP 200 and fail-closed status text.
- Bounded live-surface scan found no remaining alpha.13 freeze, STAT COMPLETE,
  UVIR complete/cleared or R5-P1 complete language in `docs/`, the live README
  header or `active_research.md`.
- `git diff --check` reports only the pre-existing extra final blank line in
  `GEMINI.md`; no G0-created whitespace error remains.

## Remaining non-G0 limitations

- The worktree is intentionally dirty and includes preserved pre-existing work.
- The live site and local Pages source differ byte-for-byte; publication review
  and commit/push/deploy remain separate user-approved operations.
- Exact UVIR numerical reproduction requires a fully pinned numerical stack,
  BLAS/thread contract, transitive hashes and canonical output sidecars.
- No external Notion or publication surface was updated in this G0 repair.

## Next Tier-1 physics task

Proceed to **U1 controlled complex-quartet interpretation** under High/Tier-1
reasoning. Freeze the background and declared parameter domain; reproduce the
sampled quartet under a pinned environment; derive gauge-invariant eigenmode,
residue and characteristic diagnostics; and predeclare outcomes that classify
the effect as physical Jeans-like growth, a background pathology or a chart /
domain artifact. Do not promote healing-length, contact-amplitude, screening or
cosmological-likelihood work ahead of U1.

