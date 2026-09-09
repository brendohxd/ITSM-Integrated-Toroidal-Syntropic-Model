# Sealed handoff for Antigravity — `A-B3` fixed-background audit

**Agent role:** Role B — numerical and pipeline auditor  
**Access:** read-only repository research; temporary-copy execution only  
**Package:** `A-B3` only  
**Gate effect:** none  
**Stop:** return the requested report and do not start another package  
**Execution isolation:** start a fresh Antigravity session; do not import or
reveal any prior Grok, Antigravity or Codex answer beyond the canonical files
named here  

## Mandatory rules before any task action

Read these repository files completely, in order:

1. `GEMINI.md`;
2. `Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md`;
3. `active_research.md`;
4. `Theory/Core/Reasoning_Mode_Plans/README.md`;
5. `Theory/Core/Reasoning_Mode_Plans/03_MAX_BOUNDED_EXACT_REDUCTIONS/PLAN.md`;
6. `Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_RCP0_ACTION_LEDGER_2026-09-05.md`;
7. `Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_MAX_FIXED_BACKGROUND_REDUCTION_2026-09-05.md`;
8. `Theory/Verification/G-A1_A-B1_ROLE_C_ADJUDICATION_2026-09-05.md`;
9. `Analysis/MAT/MAT-001/M2M3_U1/m2m3_u1_fixed_background_checks.py`;
10. the JSON and SHA-256 sidecar under
    `Analysis/MAT/MAT-001/M2M3_U1/outputs/`.

If any required file is unavailable, report the exact missing path and stop.
Do not guess or reconstruct it.

Core identity: the observable vacuum is an active finite-density condensate
with low-energy excitations, global circulation sectors, compact boundary
conditions, and possible exchanges with matter and a reservoir. Method:
identity first, derive mechanisms second, restore predictions afterward.

The binding boundary remains `MAT-001 BLOCKED`, `UVIR-003 IN_PROGRESS`,
`K_Q NOT_DERIVED`, `V NOT_COMPUTED`; the fixed-background script cannot alter
those statuses.

## Repository and environment protection

Do not edit, create, delete, rename or format any repository file. Do not run
the canonical script in place because it writes canonical outputs.

1. Hash all source files before copying.
2. Create a unique operating-system temporary directory.
3. Recreate the minimum repository-relative directory structure there so that
   the unmodified script's `parents[4]` root discovery remains valid.
4. Copy the script and every hashed input it reads.
5. Prove copied-file hashes equal source hashes.
6. Run and write audit artifacts only in the temporary directory.
7. Return results in chat/plain text. Do not copy results into the repository.

The verified interpreter for this machine is:

```text
C:\Users\brend\anaconda3\envs\itsm_env\python.exe
```

It previously reported Python `3.13.9` and SymPy `1.14.0`. Verify those values
before use. **Do not install, upgrade or repair Python or any package.** If that
exact interpreter is unavailable, report `ENVIRONMENT_BLOCKED` and stop.

No commit, push, branch, release, Notion, website or external publication is
authorized.

## Package `A-B3` — isolated reproduction and adversarial verifier audit

### Central question

Does the frozen 30-check RCP-C0/RCP-I1-C script reproducibly test the identities
claimed in its report, and which checks are independent calculations versus
tautologies, hard-coded assumptions or incomplete proxies?

This is a code-to-claim and numerical/symbolic audit. Do not infer a new action,
repair an equation, or decide a gate.

### Phase 1 — exact isolated reproduction

1. Inventory SHA-256, size and relative path for every file read by the script
   and for the report, output JSON and sidecars.
2. Copy the minimum complete structure into a unique temporary audit root.
3. Run the unmodified copied script twice with the exact interpreter above.
4. Record command, working directory, start/end time, exit code, full stdout,
   full stderr, environment versions and every produced-file SHA-256.
5. Compare the two output trees symmetrically: detect missing, added and
   changed files on either side. Report raw byte identity separately from
   normalized scientific-payload identity.
6. Verify each repository sidecar against its current file. A matching hash is
   provenance evidence only, not a physics pass.

### Phase 2 — check-by-check audit

For all 30 named checks in the JSON and source:

1. classify it as `INDEPENDENT_SYMBOLIC_IDENTITY`, `NUMERICAL_SAMPLE`,
   `DIMENSIONAL_ASSERTION`, `TAUTOLOGY_OR_LITERAL`, `DOMAIN_ASSUMPTION`, or
   `INCOMPLETE_PROXY`;
2. identify the exact code expression and the exact report claim it supports;
3. state whether the check would fail if its target equation were wrong;
4. identify hidden positivity, branch, limit or normalization assumptions;
5. flag any check whose name is stronger than its implementation.

Do not accept `all(checks.values())` as independent evidence that the inputs or
expected expressions are physically correct.

### Phase 3 — independent controls outside the repository

Create fresh audit code only inside the temporary directory. It must not import
the canonical checker as a module. Using independently entered equations:

1. calculate the two roots of the amplitude-phase determinant at a declared
   preregistered grid of at least five stable parameter points and compare with
   direct numerical eigenvalue/root calculations;
2. test the low-`k` sound speed and lower-pole overlap limit with explicit
   convergence as `k` decreases;
3. independently series-expand the uniform-sphere charge ratio near zero and
   evaluate its strong-`x` behavior;
4. verify that `rho R^2/Lambda^2` is dimensionless and `rho R/Lambda^2` is not;
5. derive the displayed-action source-exchange coefficient and independently
   test the reported factor-two discrepancy;
6. verify that finite-density enthalpy remains nonzero after adding a single
   cosmological-constant counterterm;
7. verify the algebraic monomial relation
   `n/(n-1)=3/2 -> n=3`, while explicitly classifying it as a shape screen, not
   a complete sextic-parent validation.

### Required mutations

Declare mutations before inspecting their results. At minimum test that the
audit detects:

- replacing the kinetic mixing `2*mu` by `mu`;
- deleting the `sqrt(2)` in the canonical source normalization;
- replacing `rho R^2/Lambda^2` by `rho R/Lambda^2`;
- reversing the strong-source gradient sign;
- altering the uniform-sphere charge numerator by one coefficient;
- changing one byte of an output before checksum verification;
- adding one extra output only to run 2, to prove the comparison is symmetric.

If a mutation survives unexpectedly, report it as an audit-harness weakness;
do not silently add another test after seeing the result.

### Scope boundaries

The audit does not eliminate lapse, shift or metric constraints; establish a
self-consistent gravitating background; calculate PPN, lensing or GW
observables; derive a MOND/AQUAL law; or compute `K_Q` or `V`. Do not use
observed `a_0`, `H_0`, SPARC, `2*pi`, `2/3`, a target healing length or force
normalization.

### Permitted conclusion

Use exactly one primary classification:

- `EXACT_ISOLATED_REPRODUCTION_CHECK_SUITE_AUDIT_COMPLETE`;
- `REPRODUCTION_WITH_BOUNDED_CHECK_OR_HARNESS_DISCREPANCIES`;
- `NON_REPRODUCTION_WITH_EXACT_FAILURE_EVIDENCE`;
- `ENVIRONMENT_OR_INPUT_BLOCKED`.

List all limitations separately. None is a gate decision.

## Required return format

```text
AGENT: Antigravity
ROLE: B numerical/pipeline auditor
PACKAGE: A-B3
PROMPT_SHA256: <read from HANDOFF_SHA256.md for this exact file>
REPOSITORY_WRITE: none
TEMP_DIRECTORY: ...
SOURCE_INVENTORY_AND_HASHES: ...
ENVIRONMENT: ...
COMMANDS: ...
RAW_RUN_RESULTS: ...
DETERMINISM: ...
SIDECAR_VERIFICATION: ...
CHECK_CLASSIFICATION_TABLE: all 30 checks
INDEPENDENT_CONTROLS: ...
MUTATION_RESULTS: ...
CODE_TO_CLAIM_MISMATCHES: ...
FACTS: ...
INFERENCES: ...
UNRESOLVED: ...
PRIMARY_CLASSIFICATION: ...
EXPLICIT_NON_CLAIMS: ...
GATE_EFFECT: none
OUTPUT_HASH: <hash if available, otherwise HASH_NOT_AVAILABLE>
```

Return one complete report. Stop after `A-B3`.
