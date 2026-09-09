# ITSM external-agent workload distribution

**Date:** 2026-09-05  
**Status:** proposed read-only delegation plan  
**Gate effect:** none  
**Commit/push/publication authority:** none  

## 1. Purpose

Use Antigravity and Grok to reduce duplicated expensive Codex work while
preserving one canonical integration owner. This implements the repository's
three-role audit model:

| Role | Agent | Responsibility | Repository access |
|---|---|---|---|
| A — mathematical/dimensional audit | Grok | Independent algebra, variation, dimensions, counterexamples and literature comparison | Read-only |
| B — numerical/pipeline audit | Antigravity | Reproduction, convergence, mutations, output/hash verification and independent numerical controls | Read-only; copied scripts may run outside the repository |
| C — claim/gate audit and integration | Codex | Canonical-source checks, reconcile disagreements, write reviewed results and decide whether a gate review is warranted | Parent-only writer |

Agreement between agents is not proof. Disagreement, a free coefficient or a
missing assumption is a mandatory stop for canonical integration.

## 2. Core identity shared with every agent

The observable vacuum is an active finite-density condensate whose low-energy
excitations, global circulation sectors, compact boundary conditions, and
exchanges with matter and a reservoir may have gravitational consequences.

Method:

```text
Identity first -> derive mechanisms second -> restore predictions afterward.
```

Starting gate boundary:

- `MAT-001` is `BLOCKED`;
- `UVIR-003` is `IN_PROGRESS`;
- `K_Q` is `NOT_DERIVED`;
- `V=C_m/sqrt(K_Q)` is `NOT_COMPUTED`;
- `a_0=cH_0/(2*pi)` is phenomenological, not derived;
- VOR/TOP/RES remain scoped or open;
- a script-level `PASS_*` cannot promote a physics gate.

## 3. Work allocation by scientific route

### 3.1 `M2/M3-U1` condensate portal

| Agent | Bounded task | Expected product | Mode/cost class |
|---|---|---|---|
| Grok | Derive and attack the fixed-background comparator; dimensions, signs, amplitude-phase modes, invariant source response and no-go risks | Independent equation-by-equation mathematical report | Max-equivalent external reasoning |
| Antigravity | After equations are frozen, implement symbolic/numerical checks, field-rescaling mutations, eigenvalues, static Green functions and limiting cases in an isolated copy | Reproducibility bundle and exact raw results | Max-equivalent numerical work |
| Codex | Freeze ITSM action namespaces, include metric constraints, run U5/M4, determine physical pole residue, enforce gate firewall | Canonical integrated calculation and disposition | High specification, then Ultra only at the coupled stage |

### 3.2 P2 rectangular-`T^3` Casimir negative result

| Agent | Bounded task | Expected product | Mode/cost class |
|---|---|---|---|
| Grok | Independent analytic/regulator and claim-domain audit | Mathematical referee report | High/Max-equivalent |
| Antigravity | Fresh isolated rerun, convergence, byte identity, hashes and independent no-plateau diagnostic | Numerical audit report and artifact manifest | Medium/Max-equivalent |
| Codex | Verify code-to-claim alignment, resolve discrepancies, update manuscript only after review | Canonical hostile read/release decision | High; Medium for packaging |

### 3.3 Winding and phase normalization

| Agent | Bounded task | Expected product | Mode/cost class |
|---|---|---|---|
| Grok | Derive Noether current, phase normalization, velocity/circulation map and compact-length convention | Mathematical convention audit | High/Max-equivalent |
| Antigravity | Reproduce S2 at preregistered points and test reflection/permutation/limit mutations in isolation | Numerical S2 audit | Medium/Max-equivalent |
| Codex | Check parent-interface compatibility and preserve the corrected failure/status boundary | Canonical VOR/TOP decision | High |

### 3.4 Reservoir and physical `T^3` spectrum

Do not delegate these yet. Their inputs depend on a surviving physical parent.
Create new sealed handoffs only after the relevant Ultra entry conditions are
met. Early work here would cause action mixing and wasted reasoning.

## 4. First dispatch sequence

1. Send Grok only package `G-A1` from `GROK_HANDOFF.md`.
2. Send Antigravity only package `A-B1` from `ANTIGRAVITY_HANDOFF.md`.
3. Keep the prompts independent; do not show either agent the other's result.
4. Return both complete responses to Codex unchanged.
5. Codex performs Role-C comparison and identifies discrepancies.
6. Dispatch second packages only after the first comparison is recorded.

This order obtains one upstream mathematical analysis and one independent
near-term numerical/publication audit without running two agents on the same
unfrozen calculation.

## 5. Universal read-only boundary

Antigravity and Grok must not:

- edit any repository file, including formatting or typo fixes;
- change `active_research.md`, a gate report, README, manuscript or plan;
- create commits, branches, tags, pushes, releases or external updates;
- overwrite canonical outputs or checksum sidecars;
- choose a gate status or call a route `CLEARED`;
- combine equations from different action namespaces;
- infer a coefficient from observed `a_0`, SPARC, `H_0`, `2*pi`, `2/3`, PTA
  bands or a target healing length;
- hide failed tests, divergent runs or inconvenient signs.

Antigravity may copy exact inputs into a new temporary directory outside the
repository and write only there. Its report must include source and copied-file
hashes so Codex can verify identity.

### 5.1 Antigravity probationary reliability protocol

Repeated Antigravity runs have expanded their mandate, attempted environment
repair, mixed implementation with verification, or returned polished summaries
without the required raw evidence. Until reliability is re-established:

1. Antigravity receives **mechanical B0 witness packages only**: prewritten
   commands against Codex-authored, frozen harnesses.
2. Each package must use a fresh foreground session, name the exact interpreter,
   prohibit package installation and environment discovery, and stop on the
   first error without retrying or changing flags.
3. `ManageTask`, background work, subagents, autonomous coding and scientific
   dispositions are prohibited. A sandbox or Windows-Temp error is returned as
   `EXECUTION_BLOCKED`; it is not permission to install or repair Python.
4. A return is admissible only if it contains the unedited command, exit code,
   stdout, stderr, source hash, manifest path/hash and complete manifest text.
   Missing fields invalidate the witness even if its prose says `PASS`.
5. Codex independently verifies every returned hash and reruns any decisive
   calculation. Antigravity output remains unadjudicated until that comparison.
6. Only after **two consecutive clean B0 packages** may Antigravity receive one
   bounded numerical-sensitivity package. Derivation, gate language and direct
   repository edits remain permanently outside its role.

Any deviation resets the clean-run count. The work is then reassigned to Codex
or another independent numerical implementation rather than repaired inside
the failed Antigravity session.

## 6. Required return format

Every report must contain:

1. agent/role and exact task package;
2. prompt SHA-256 supplied at dispatch;
3. sources read and versions/hashes where available;
4. assumptions and conventions;
5. exact derivation or commands;
6. dimensions and signs;
7. raw results, failures and negative controls;
8. verified facts versus inference versus unresolved items;
9. explicit non-claims and gate status unchanged;
10. exact response/artifact SHA-256 if the environment permits it.

If response hashing is unavailable, return plain text without later editing;
Codex will preserve and hash the imported response before using it.

## 7. Reconciliation rule

Codex must compare Role A, Role B and canonical Role C at the equation/claim
level. A majority vote cannot override a failed derivation. Canonical writing
is permitted only after discrepancies are either resolved or explicitly logged
as open.
