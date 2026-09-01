# ITSM post-G0 Tier-1 dependency-clearing execution plan

**Date:** 2026-08-25  
**Branch:** `recovery/v12-core-architecture`  
**Status:** `ACTIVE_EXECUTION_PLAN`  
**Authority:** subordinate to `GEMINI.md`, `active_research.md`, the Core Identity
Briefing, signed parent-gate decisions, and
`ITSM_Tier1_Route_Test_Programme.md`.

## 1. Objective

Execute the bounded Tier-1 sequence from the repaired G0 baseline through
Review Gate RG1. The programme must determine whether the current-action U1
quartet, R5-P1, any M1-M5 microscopic matching route, and any internally
derived acceleration coefficient deserve further expensive work.

An honest rejection, no-go result, or continued hold satisfies the scientific
objective. This plan cannot promote a physics gate by itself.

## 2. Binding baseline

The execution begins from the following fail-closed boundary:

| Item | Binding status |
|---|---|
| UVIR-003 | `IN_PROGRESS`; `HOLD_TIER1_CLOSURE`; `physics_pass=false` |
| MAT-001 | `BLOCKED`; `V NOT_COMPUTED`; `K_Q NOT_DERIVED` |
| MAT R5 | `HOLD_DECLARED_ACTION_UNDERDETERMINES_V` |
| R5-P1 | `OPEN_RESEARCH_CANDIDATE` |
| STAT-001 | `NOT_STARTED_AS_CLOSED_GATE` |
| CBR-002 | `OPEN` |
| VOR-001 and RES-001 | open scaffolds within their recorded sub-statuses |

Script-level, checklist, algebraic, provenance, or mutation-suite passes are
not physics passes. A child report cannot override a parent gate.

## 3. Execution packages

### E-1 — documentation and authority corpus audit

1. Enumerate and parse every repository documentation surface (`.md`,
   `.markdown`, `.rst`, README, changelog, licence, contribution, agent, and
   cover-letter files), including untracked recovery material.
2. Independently enumerate the local `main` tree and compare common files by
   normalized content without checking out or altering either branch.
3. Separate current canonical authority, gates, supporting documentation,
   manuscripts, immutable releases, historical archives, vendored solver
   documentation, local attachments, and private working notes.
4. Treat old `main`, archives, attachments, generated summaries, and local
   notes as provenance rather than present scientific authority.
5. Record contradictions that affect the Tier-1 route programme, especially
   old acceleration-coefficient, SPARC, Hubble, UVIR, and gate-closure claims.

This corpus pass establishes understanding and provenance only. Reading a
claim, finding it frequently, or finding it on `main` cannot validate it.

### E0 — freeze and verify G0

1. Verify the G0 workspace manifest and its SHA-256 seal.
2. Verify repaired canonical outputs and sidecars without silently replacing
   preserved work.
3. Record the live branch, HEAD, remote relation when available, and worktree
   state.
4. Confirm that canonical dashboards and claim surfaces retain the binding
   baseline above.
5. Stop if a G0 hash, status, or authority conflict cannot be reconciled.

### E1 — U1 controlled complex-quartet classification

1. Pre-register the parent action, background, parameter domain, field chart,
   Fourier/sign conventions, hypotheses, and kill criteria.
2. Reproduce the sampled quartet using a pinned numerical environment and
   deterministic output contract.
3. Derive the reduced physical scalar system after all constraints are applied.
4. Calculate gauge-invariant eigenmodes, dispersion, Hamiltonian energy and
   signed residues, characteristics/hyperbolicity, finite `k/a` support, growth
   timescale, and backreaction estimate.
5. Run dimension, sign, convention, branch, parameter-mutation, precision, and
   missing-evidence negative controls.
6. Classify the quartet as exactly one of:
   - controlled physical Jeans-like growth;
   - background pathology or vacuum runaway;
   - chart/domain/constrained-variable artifact;
   - unresolved because the declared evidence is insufficient.
7. Reject or freeze U1 for a ghost, non-hyperbolicity, uncontrolled
   backreaction, vacuum runaway, or non-reproducibility.

No healing-length, contact-amplitude, screening, or cosmological claim may be
used to rescue a failed U1 result.

### E2 — hostile R5-P1 and M1-M5 A0-A2 comparison

1. Trace R5-P1 from its complete covariant parent action rather than a
   contact-only amplitude or pre-projection coefficient.
2. Audit its static-source provenance, constraint reduction, physical degrees
   of freedom, signed matter-to-physical-mode pole residue, stability, cutoff,
   GR/uncoupled limit, and parameter identifiability.
3. Apply the same A0-A2 cheap screens to M1-M5:
   - A0: declared action, dimensions, symmetries, limits, and parameter count;
   - A1: background existence and domain;
   - A2: constraints, physical modes, source projection, and first kill test.
4. Rank routes by core-identity fidelity, added freedom, calculability,
   stability risk, and falsifiability.
5. Advance at most two MAT routes. Advancing none is an admissible result.

No route passes MAT-001 unless it calculates invariant
`V = g_phys/sqrt(Z_phys)` from the declared action after diagonalisation.

### E3 — blind acceleration-coefficient audit

1. Use `a0_internal = C_chi c H0` with `C_chi` unknown.
2. Reconstruct the provenance of every historical multiplier/divisor form and
   separate written equations from quoted numerical values.
3. Attempt a dimensionally complete derivation of `C_chi` from the declared
   action, normalized physical modes, toroidal boundary conditions, winding,
   moduli, or compactification.
4. Prohibit observed MOND, SPARC, bTFR, weak-lensing, or desired `H0` values
   from entering the derivation.
5. Freeze the internal result before comparing it with `2*pi`, `1/(2*pi)`,
   `sqrt(1-q)/(2*pi)`, and observational constraints.
6. Retain the relation as phenomenological if the coefficient is not unique.

### E4 — RG1 decision and synchronization

1. Issue keep/repair/quarantine/reject dispositions for U1, R5-P1, M1-M5, and
   the acceleration coefficient.
2. Select at most two MAT routes, one UVIR alternative, and one screening route
   for expensive work.
3. Synchronize canonical dashboards and the claim ledger only after the
   dispositions are evidence-backed.
4. Register August 2026 source-vector, DESI interaction, El Gordo, LVK,
   early-universe, and competing-`a0` results as downstream tests, not current
   validation.
5. Preserve all blocked and in-progress parent statuses unless their complete
   signed checklists independently support a change.

## 4. Evidence contract

Each analytical package must provide:

1. a pre-registered specification and explicit assumptions;
2. executable source for every numerical operation;
3. deterministic raw outputs and machine-readable summary;
4. immediate SHA-256 seals for reports and generated evidence;
5. dimensional, sign, convention, branch, source-provenance, and mutation
   controls;
6. code-to-claim and parent/child-gate reconciliation;
7. a fail-closed disposition that distinguishes mathematical, pipeline, and
   physics conclusions.

Documentation-corpus indexes may contain paths or metadata for private or
untracked material and are therefore local audit evidence by default. They
must not be published without a separate sensitive-data review.

If independent three-role review is used, the exact prompts must be sealed and
the roles must remain read-only under `GEMINI.md` Rules 7-9.

## 5. Definition of done

The goal is complete when:

- G0 has been reverified or any discrepancy has been explicitly recorded;
- the working-tree and `main` documentation corpora have been read/indexed,
  compared, and assigned explicit authority classes;
- U1 has a reproducible, bounded classification;
- R5-P1 and M1-M5 have comparable A0-A2 dispositions;
- the acceleration coefficient has a blind provenance/derivation verdict;
- RG1 records a bounded route selection, including the possible empty set;
- canonical status surfaces do not exceed the evidence; and
- validation hashes and code-to-claim checks are recorded.

Commit, push, deployment, publication, Notion updates, deletion, and alteration
of immutable historical releases are outside this execution plan unless the
user separately authorizes them.
