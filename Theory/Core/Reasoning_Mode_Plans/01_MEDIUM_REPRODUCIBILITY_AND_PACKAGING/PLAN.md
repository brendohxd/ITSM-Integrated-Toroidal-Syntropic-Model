# Medium plan — reproducibility, evidence mapping and packaging

**Required reasoning:** Medium  
**Gate effect:** none  
**Scientific inference authority:** none beyond exact execution facts  
**Can start:** immediately  

## Purpose

Perform deterministic and mechanical work without spending High/Max/Ultra
reasoning. This plan may establish that commands ran, hashes agree and prose
points to an artifact. It may not decide whether an equation or theory is
physically correct.

## M-0 — preflight

1. Read the Core Identity Briefing and the parent plan.
2. Record branch, `git status --short`, Python/environment versions and current
   input hashes.
3. Preserve the dirty worktree. Do not rewrite or delete prior evidence.
4. Identify which outputs are generated and which are historical/frozen.

Deliverable: read-only preflight manifest.

## M-1 — P2 canonical rerun

Run only the declared CBR-001/P2 commands from the P2 README in a recorded
environment:

- lattice/Casimir calculation;
- Stage-2 stress calculation;
- Stage-3 backreaction;
- Stage-3B ratio/plateau diagnostic.

Requirements:

- retain stdout/stderr and exit codes;
- run twice and compare structured outputs byte-for-byte where deterministic;
- compute final SHA-256 values;
- do not alter tolerances after seeing results;
- do not interpret a transient crossing as an attractor.

If a command fails or output differs, stop and hand the exact evidence to the
High plan. Do not debug the physics at Medium.

## M-2 — code/output/manuscript evidence map

Build a mechanical table for every P2 abstract/conclusion number, table and
figure:

| Manuscript item | Generating script | Raw output | Hash | Current match |
|---|---|---|---|---|

Flag mismatches without repairing scientific prose. Verify repository-relative
paths and the absence of private absolute paths in public artifacts.

## M-3 — artifact hygiene

- run `git diff --check` on task files;
- confirm JSON parses and required fields exist;
- confirm checksum sidecars match their targets;
- confirm figures exist at the stated dimensions and filenames;
- confirm two consecutive deterministic runs agree;
- list missing dependencies or untracked outputs.

## M-4 — conditional release packaging

Open this package only after the High/Max scientific checks approve the frozen
evidence and the user explicitly requests release preparation:

- compile the paper from frozen source;
- verify the PDF opens and contains the expected figures/tables;
- assemble versioned code/output/checksum inventory;
- prepare, but do not submit, the Zenodo/arXiv bundle;
- do not commit, push or upload without explicit authorization.

## M-5 — SPARC maintenance-only lane

Run only if specifically requested. Permitted work is data provenance,
deterministic parsing, frozen exclusions, raw-output checks and comparator
reproduction. No physical interpretation, parameter selection or theory
normalization is authorized here.

## Stop and switch to High when

- an equation, sign, dimension, regulator or physical interpretation is in
  doubt;
- a rerun disagrees with frozen evidence;
- prose exceeds what a raw artifact establishes;
- a choice between repairing, quarantining or superseding evidence is needed.

## Completion record

Report exact commands, environment, output paths, mismatches and hashes. End
the task. Do not proceed into the High or Max plan automatically.

