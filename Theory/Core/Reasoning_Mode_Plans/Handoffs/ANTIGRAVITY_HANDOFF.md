# Sealed handoff for Antigravity — Role B numerical/pipeline auditor

**Use:** provide this complete file to Antigravity  
**Access:** read-only repository research  
**Start package:** `A-B1` only  
**Do not begin later packages without a new instruction**  

## Mandatory rules before any task action

Read these files completely, in order:

1. `GEMINI.md`;
2. `Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md`;
3. `Theory/Core/Reasoning_Mode_Plans/README.md`;
4. `Theory/Core/Reasoning_Mode_Plans/01_MEDIUM_REPRODUCIBILITY_AND_PACKAGING/PLAN.md`;
5. `Theory/Core/ITSM_RESEARCH_ROUTE_AND_SELECTIVE_PUBLICATION_PLAN_2026-09-05.md`;
6. every task-specific source named below.

Core identity: the observable vacuum is an active finite-density condensate
with low-energy excitations, global circulation sectors, compact boundary
conditions, and possible exchanges with matter and a reservoir.

Method: identity first, derive mechanisms second, restore predictions only
afterward. `MAT-001` is blocked; `UVIR-003` is in progress; `K_Q`, `V` and
`a_0` are not derived by the live parent.

You are Role B only. Do not make a scientific gate decision.

## Repository protection

Do not edit, create, delete, rename or format any repository file. Do not run a
script if it will write canonical repository outputs. Instead:

1. hash every source/input file;
2. create a unique directory under the operating system temporary directory;
3. copy the minimum scripts and inputs into it;
4. run there;
5. record copied-file hashes and prove they match the source hashes;
6. return the report in chat/plain text.

No commit, push, branch, release, Notion, website or external publication
action is authorized.

## Package `A-B1` — P2 isolated numerical reproduction

### Question

Do the frozen CBR-001 calculations reproducibly establish the scoped negative
claim stated in `papers/P2-Rectangular-T3-Casimir/README.md`?

### Read completely

- `papers/P2-Rectangular-T3-Casimir/README.md`;
- `papers/P2-Rectangular-T3-Casimir/HOSTILE_READ.md`;
- `papers/P2-Rectangular-T3-Casimir/main.tex`;
- `Analysis/Casimir/CBR-001/README.md`;
- `Analysis/Casimir/CBR-001/STAGE2.md`;
- `Analysis/Casimir/CBR-001/STAGE3.md`;
- `Analysis/Casimir/CBR-001/STAGE3B.md`;
- all scripts and declared input/output schemas used by those stages.

### Perform

1. Inventory and hash exact source scripts and inputs.
2. Copy only required files to a unique temporary audit directory.
3. Reproduce Stages 1, 2, 3 and 3B without changing constants or tolerances.
4. Run twice and compare deterministic outputs byte-for-byte.
5. Record exit code, stdout/stderr and SHA-256 for every output.
6. Test documented convergence controls without selecting results post hoc.
7. Independently calculate the Stage-3B residence/plateau classification from
   raw trajectories, keeping crossing, residence, plateau and attractor
   distinct.
8. Map each P2 number/table/figure to the reproduced raw artifact.
9. Report every mismatch. Do not repair it.

### Required negative controls

- permutation/reflection of rectangular axes where the equations require it;
- at least one stricter and one looser numerical-resolution setting declared
  before inspecting the classification;
- altered initial conditions from a preregistered small set;
- mutation showing the classifier would detect a synthetic genuine plateau;
- checksum failure when one copied artifact byte is changed.

### Permitted conclusion

Only one of:

- exact isolated reproduction;
- numerical reproduction with listed bounded discrepancies;
- non-reproduction with exact failure evidence;
- task blocked because a necessary input or environment is unavailable.

Do not decide that P2 is publishable or change the CBR/P2 status.

## Later package `A-B2` — winding S2 numerical audit

Do not start until instructed. Reproduce the current S2 audit at the exact
preregistered `lambda=100`, `omega=1` point, preserve the known `0.5%` failure,
and test symmetry/limit mutations in an isolated copy. This package cannot
identify the VOR template with the live UVIR parent.

## Later package `A-B3` — `M2/M3-U1` equation checks

Do not start until Codex supplies a frozen action and equations. Implement:

- dimensional and symbolic identity tests;
- kinetic/gradient eigenvalues;
- field-rescaling invariance of the physical residue;
- static Green-function and limiting-case checks;
- nonlinear spherical matching and effective charge;
- deliberate sign and coefficient mutations.

Never infer the action or missing coefficient yourself. A script cannot repair
an incomplete parent.

## Required report format

```text
AGENT: Antigravity
ROLE: B numerical/pipeline auditor
PACKAGE: A-B1
PROMPT_SHA256: <supplied manifest value>
REPOSITORY_WRITE: none
TEMP_DIRECTORY: <path>
SOURCE_HASHES: ...
ENVIRONMENT: ...
COMMANDS: ...
RAW_RESULTS: ...
DETERMINISM: ...
NEGATIVE_CONTROLS: ...
MISMATCHES: ...
FACTS: ...
INFERENCES: ...
UNRESOLVED: ...
GATE_EFFECT: none
OUTPUT_HASH: <hash if available, otherwise HASH_NOT_AVAILABLE>
```

Stop after returning `A-B1`.

