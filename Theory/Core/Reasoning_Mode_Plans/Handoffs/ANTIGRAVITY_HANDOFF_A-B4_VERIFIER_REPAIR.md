# Sealed handoff for Antigravity — `A-B4` verifier repair audit

**Agent role:** Role B — numerical and pipeline auditor  
**Access:** read-only repository research; temporary-copy execution only  
**Package:** `A-B4` only  
**Required reasoning:** High  
**Gate effect:** none  
**Stop:** return one complete report and do not edit the repository  
**Execution isolation:** use a fresh Antigravity session; do not import any
unlisted external-agent answer

## Mandatory scientific frame

Read these repository files completely, in order:

1. `GEMINI.md`;
2. `Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md`;
3. `active_research.md`;
4. `Theory/Core/Reasoning_Mode_Plans/README.md`;
5. `Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_RCP0_ACTION_LEDGER_2026-09-05.md`;
6. `Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_MAX_FIXED_BACKGROUND_REDUCTION_2026-09-05.md`;
7. `Theory/Verification/G-A4_A-B3_ROLE_C_ADJUDICATION_2026-09-05.md`;
8. `Analysis/MAT/MAT-001/M2M3_U1/m2m3_u1_fixed_background_checks.py`;
9. every file under `Analysis/MAT/MAT-001/M2M3_U1/outputs/`;
10. this sealed handoff and `HANDOFF_SHA256.md`.

If any required path is missing or the prompt hash differs from the manifest,
report the exact discrepancy and stop.

The binding boundary is `MAT-001 BLOCKED`, `UVIR-003 IN_PROGRESS`,
`K_Q NOT_DERIVED`, `V NOT_COMPUTED`. A repaired verifier remains an algebra
and provenance tool; it cannot decide a physics gate.

## Repository and environment protection

Do not edit, create, delete, rename or format any repository file. Work only
inside one unique operating-system temporary directory. Copy the minimum input
tree, record source and copy hashes, and prove equality before execution.

Use only:

```text
C:\Users\brend\anaconda3\envs\itsm_env\python.exe
```

Verify the interpreter and package versions. Do not install, upgrade or repair
Python or any dependency. If unavailable, return `ENVIRONMENT_BLOCKED`.

No commit, push, branch, publication, Notion or website action is authorized.

## Package `A-B4` — construct and audit a semantic version-2 verifier

### Central question

Can a temporary replacement verifier convert the weak literal/proxy checks
identified in `A-B3` into genuine semantic, arbitrary-precision and
end-to-end tests while reproducing every valid canonical identity?

The new verifier is a candidate patch only. Keep it outside the repository and
return its exact text or a unified diff for Codex review.

### Phase 1 — exact baseline reproduction

1. Inventory the complete set of code, Markdown and output files used to
   interpret the canonical checker.
2. Run the unmodified copied checker twice.
3. Save full command, working directory, environment, stdout, stderr, exit code,
   timestamps and complete output-tree hashes for both runs.
4. Compare trees symmetrically and distinguish raw-byte equality from
   normalized scientific-payload equality.

### Phase 2 — mandatory semantic replacements

Implement a temporary version-2 checker satisfying all of the following:

1. **Trace-sign check:** parse the actual frozen ledger expression and compare
   it with the action-derived convention. No literal-versus-literal boolean.
2. **Dimensions:** define base mass dimensions for symbols and propagate them
   through each tested product, quotient, power and sum. Fail on incompatible
   sums. No assertions such as `(4-2-2)==0` standing alone.
3. **Stability domains:** symbolically factor the relevant dispersion/root
   products and state the parameter and momentum intervals. Retain boundary
   samples only as regression tests.
4. **Independent roots:** build the first-order Hamiltonian evolution matrix
   directly from the quadratic Lagrangian and compare its eigenfrequencies
   with the analytic branches. Do not numerically solve the same characteristic
   polynomial used to construct the analytic answer.
5. **Low-`k` convergence:** use exact SymPy expressions or at least 80 decimal
   digits throughout. The sealed sequence is
   `k={1e-1,1e-2,1e-3,1e-4,1e-5,1e-6}`.
6. **Source and sphere controls:** retain the factor-two, enthalpy,
   uniform-sphere and monomial controls, but label each as identity, sample,
   asymptotic control or incomplete proxy.
7. **Source inventory:** hash every mandatory input named above, including the
   prompt and adjudication, rather than only the Python script subset.

### Predeclared stable root grid

Use the following exact rational triples `(M_sigma, mu, k)` and no replacements
after results are seen:

```text
(1,   1,   1/10)
(2,   1,   1/4)
(1/2, 3/2, 1/20)
(3,   2,   1/2)
(4,   1/2, 1)
```

Record absolute and relative differences at no less than 50 decimal digits.

### Required genuine mutations

Declare the mutation identifiers before running them. Each mutation must alter
the scientific object or filesystem behavior, not merely invert an expected
boolean:

1. change the kinetic mixing in the quadratic Lagrangian from `2*mu` to `mu`;
2. delete `sqrt(2)` from the canonical source expression;
3. replace `rho R^2/Lambda^2` with `rho R/Lambda^2` in the expression parsed by
   the dimension engine;
4. reverse the sign of the physical `k^2` gradient coefficient in the relevant
   dispersion expression;
5. change one coefficient in the uniform-sphere charge numerator;
6. write a real output file, mutate one byte on disk, then run sidecar
   verification on that file;
7. create a real extra file only in run 2 and prove symmetric tree comparison
   reports it;
8. alter one formula in a copied Markdown source and prove the parsed
   code-to-claim check detects the mismatch.

If any mutation survives, retain the failure and return
`VERIFIER_REPAIR_INCOMPLETE`. Do not add a post-hoc detector and erase the
original outcome.

### Phase 3 — sealing and self-audit

1. Run the candidate verifier twice from clean temporary subdirectories.
2. Seal the candidate script, source inventory, both complete execution
   records, raw results, mutation results and final report in one manifest.
3. Hash the exact final report after it is complete. Do not cite a hash that
   omits an arbitrary-precision follow-up.
4. Classify every test as one of:
   `INDEPENDENT_FORMULATION`, `SYMBOLIC_IDENTITY`, `ARBITRARY_PRECISION_LIMIT`,
   `NUMERICAL_REGRESSION`, `DIMENSION_ENGINE`, `PARSED_CODE_TO_CLAIM`,
   `END_TO_END_PROVENANCE`, or `INCOMPLETE_PROXY`.

### Allowed primary classifications

- `VERIFIER_V2_CANDIDATE_COMPLETE_ALL_PREDECLARED_MUTATIONS_DETECTED`;
- `VERIFIER_REPAIR_INCOMPLETE`;
- `BASELINE_NON_REPRODUCTION`;
- `ENVIRONMENT_BLOCKED`.

Even the strongest classification has `GATE_EFFECT: none`.

### Forbidden claims

Do not claim independent scientific validation, a derived force law, metric
constraint closure, screening, PPN/lensing closure, `K_Q`, `V`, `a_0`, or any
gate promotion. Do not call the sealed grid publicly preregistered; use
`predeclared in the sealed prompt`.

## Required return format

```text
AGENT: Antigravity
ROLE: B numerical/pipeline auditor
PACKAGE: A-B4
PROMPT_SHA256: ...
REPOSITORY_WRITE: none
TEMP_DIRECTORY: ...
SOURCE_AND_COPY_INVENTORY: ...
ENVIRONMENT: ...
BASELINE_RUNS: ...
CANDIDATE_SCRIPT_OR_DIFF: ...
SEMANTIC_REPLACEMENT_TABLE: ...
ROOT_GRID_RESULTS: ...
LOW_K_ARBITRARY_PRECISION_RESULTS: ...
MUTATION_DECLARATION: ...
MUTATION_RESULTS: ...
RUN_TREE_COMPARISON: ...
COMPLETE_MANIFEST: ...
CODE_TO_CLAIM_LIMITS: ...
VERIFIED_FACTS: ...
INFERENCES: ...
UNRESOLVED: ...
PRIMARY_CLASSIFICATION: ...
EXPLICIT_NON_CLAIMS: ...
GATE_EFFECT: none
OUTPUT_HASH: <hash of the exact complete report>
```

Return one report and stop after `A-B4`.

