# ITSM post-G0 documentation and authority audit

**Date:** 2026-08-25  
**Branch:** `recovery/v12-core-architecture`  
**HEAD:** `4310a9ad7bc27b7e0f4169586210818761119936`  
**Reference:** local `main` at `8183db8feb97fe0aa59c9ce8e99d37ac5559128a`  
**Disposition:** `PASS_CORPUS_ENUMERATION`; `HOLD_CLAIM_AUTHORITY_TO_G0`

## Scope and method

`Analysis/Documentation/docs_corpus_audit.py` read and indexed every working
tree and local-`main` documentation surface matching `.md`, `.markdown`,
`.rst`, README, changelog, licence, contribution, agent, Gemini, and cover
letter names. It extracted full-file hashes, headings, status terms, claim
terms, tracking state, and authority categories. High-risk authority files,
the current and `main` README/changelog, core plans, gate reports, history
indexes/timelines, and the six `main`-only documents were then inspected
directly in context.

The machine index is local audit material. It includes metadata from
untracked/private files and attachments and is `PRIVATE_LOCAL_AUDIT_DO_NOT_PUBLISH`
until a separate sensitive-data review is completed.

## Corpus result

| Surface | Count/result |
|---|---:|
| Working-tree documents read/indexed | 643 |
| Tracked working-tree documents | 247 |
| Untracked working-tree documents | 396 |
| Local `main` documents read/indexed | 48 |
| Common, normalized-identical | 39 |
| Common, different | 3 |
| `main` only | 6 |
| Working tree only | 601 |

The three changed common files are `README.md`, `CHANGELOG.md`, and
`Manuscript/Submission_Materials/CoverLetter_JCAP.tex`. The six `main`-only
files are comparative mythology/pseudohistory material under
`papers/Al-Jabr-Reunification/Research_Archive/`; they are not Tier-1 physics
evidence and have no current authority.

## Authority classification

1. Current authority begins with `GEMINI.md`, the Core Identity Briefing,
   signed parent-gate decisions, `active_research.md`, the G0 repair record,
   and the Tier-1 route programme.
2. Current recovery core/gate documents are live only to the extent that they
   agree with the G0 normalized status and parent-gate hierarchy.
3. `main`, `Theory/History`, old manuscripts, releases, Zenodo packages, and
   archived webpages are provenance. Their presence proves historical usage,
   not correctness.
4. `.codex-remote-attachments`, duplicate `*-ITSM-Cosmologist` files, generated
   summaries, vendored CAMB documentation, and local notes are non-authority.
5. `.local_build_notes.md` contains private/metaphysical material and is neither
   scientific evidence nor publication material.

## Material contradictions recovered

- Historical drafts alternate between `2*pi*c*H0` and `c*H0/(2*pi)` while
  sometimes retaining a numerical value compatible only with the divisor.
  No recovered derivation uniquely moves the factor between numerator and
  denominator.
- Old `main` presents zero-parameter SPARC, Hubble-tension, CMB/JWST, cluster,
  PPN, stochastic-background, and exact acceleration-coefficient claims as
  established. The recovery evidence does not support those promotions.
- Historical records document synthetic/provenance-defective galaxy inputs,
  inconsistent `H0` packaging, a failed `2/3` coefficient route, and a
  superluminal-sound-speed concern. These are negative controls, not results
  to rehabilitate silently.
- The current changelog's alpha.14/alpha.13 entries record contaminated Grok
  claims that UVIR-003 closed and that later statistical/route results were
  achieved. G0 quarantines those claims. The entries must be superseded by a
  correction, not used as gate authority.

## G0 re-verification

The sealed G0 workspace manifest and all five entries in
`ITSM_G0_REPAIR_ARTIFACTS.sha256` match their live files. Canonical status
surfaces retain:

- UVIR-003: `IN_PROGRESS`, `HOLD_TIER1_CLOSURE`, `physics_pass=false`;
- MAT-001: `BLOCKED`, `V NOT_COMPUTED`, `K_Q NOT_DERIVED`;
- MAT R5: `HOLD_DECLARED_ACTION_UNDERDETERMINES_V`;
- R5-P1: `OPEN_RESEARCH_CANDIDATE`;
- STAT-001: `NOT_STARTED_AS_CLOSED_GATE`.

The worktree is intentionally dirty and contains preserved user/model work.
No checkout, reset, deletion, commit, push, or publication was performed.

## Scientific boundary

This audit establishes corpus coverage, provenance, contradictions, and the
authority hierarchy. It does not validate any equation, numerical claim, or
gate. All subsequent route decisions remain fail-closed and must cite
executable evidence rather than document frequency or branch age.
