# Sealed handoff for Antigravity — `A-P2A0` execution witness

**Agent role:** Role B0 — mechanical execution witness  
**Access:** read-only repository; the supplied harness writes only to an operating-system temporary directory  
**Package:** `A-P2A0` only  
**Required reasoning:** High is unnecessary; use the lowest reliable tool-using mode  
**Gate effect:** none  
**Stop:** return after one harness execution or the first error  
**Execution isolation:** use a fresh Antigravity session; do not use a task manager, background agent, subagent or another model

## Why this package is deliberately narrow

Previous Antigravity work mixed derivation, implementation, verification and
scientific classification. That process produced polished but invalid results.
For this package Antigravity must make no scientific decision and write no
code. Codex owns the harness and will independently inspect every returned
byte.

## Mandatory scientific frame

Read, without editing:

1. `GEMINI.md`;
2. `Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md`;
3. `active_research.md`;
4. `Theory/Gates/TOP-001/P2_CBR001_TIER1_HOSTILE_REAUDIT_2026-09-05.md`;
5. this handoff and `HANDOFF_SHA256.md`.

Core identity: the observable vacuum is an active finite-density condensate
whose low-energy excitations, global circulation sectors, compact boundary
conditions, and exchanges with matter and a reservoir may have gravitational
consequences. P2 is only a rectangular-`T^3` free-scalar control.

Binding status: `TOP-001 / CBR-002` is
`SCOPED_NEGATIVE_FREE_DILUTION`; `MAT-001 BLOCKED`; `UVIR-003 IN_PROGRESS`;
`K_Q NOT_DERIVED`; `V NOT_COMPUTED`. A harness `PASS` cannot change a gate.

If a required file is missing or the handoff digest differs from
`HANDOFF_SHA256.md`, return the mismatch and stop.

## Prohibited operations

Do not:

- install, locate, repair or choose Python;
- edit or generate source code;
- run commands other than the two exact commands below;
- overwrite tracked outputs;
- interpret `STATUS: PASS` as a scientific result;
- summarize missing output from memory;
- retry an error with altered flags;
- use `ManageTask`, a scheduler, a background job or a subagent;
- commit, push, publish or update Notion/websites.

## Exact execution

Run from the repository root:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath Analysis\Casimir\CBR-001\p2_reproduction_a0_harness.py
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\Casimir\CBR-001\p2_reproduction_a0_harness.py
```

Do not activate Conda and do not call bare `python`. The harness creates two
clean temporary copies, executes the fixed baseline, compares output trees and
prints the absolute path and SHA-256 of one audit manifest.

On success, return:

1. the complete unedited stdout and stderr;
2. the process exit code;
3. the harness SHA-256 shown by the first command;
4. the manifest absolute path and SHA-256 printed by the harness;
5. the complete manifest text, unedited.

On any error, return immediately with:

```text
PRIMARY_CLASSIFICATION: EXECUTION_BLOCKED
COMMAND: <exact command>
EXIT_CODE: <exact value or NOT_STARTED>
STDOUT: <complete raw text>
STDERR: <complete raw text>
RETRY_ATTEMPTED: no
REPOSITORY_WRITE: none
GATE_EFFECT: none
```

Do not diagnose or repair the error. Codex will do that.

## Successful return header

```text
AGENT: Antigravity
ROLE: B0 mechanical execution witness
PACKAGE: A-P2A0
PROMPT_SHA256: ...
REPOSITORY_WRITE: none
HARNESS_SHA256: ...
COMMAND: ...
EXIT_CODE: ...
STDOUT: <complete raw text>
STDERR: <complete raw text>
MANIFEST_PATH: ...
MANIFEST_SHA256: ...
MANIFEST_TEXT: <complete unedited JSON>
PRIMARY_CLASSIFICATION: EXECUTION_EVIDENCE_RETURNED_UNADJUDICATED
EXPLICIT_NON_CLAIMS: no independent derivation; no physics pass; no gate change
GATE_EFFECT: none
```

Return once and stop. Do not begin sensitivity testing; Codex must validate
this baseline before a separate `A-P2A1` package can exist.

