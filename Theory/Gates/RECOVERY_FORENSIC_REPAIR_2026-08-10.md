# Recovery forensic repair - 2026-08-10

**Repair branch:** `codex/recovery-forensic-rebuild`
**Reconstruction anchor:** `4682a51`
**Scientific disposition:** fail closed; no physics gate promoted

## Decision

The repair branch is reconstructed from `4682a51`, the last reviewed tree whose
executable and documentary status surfaces consistently retain:

`UVIR-003 IN_PROGRESS | Tier-1 NOT_MET | MAT-001 BLOCKED | V NOT_COMPUTED |
K_Q NOT_DERIVED | Stage 4A CLOSED`.

The original working checkout and its uncommitted files were not modified.

## Quarantine boundary

Scientific changes introduced from `c3386f0` through `4310a9a` are quarantined
from this reconstruction. This is a content decision, not an assertion that
every line in the range is unusable. A later change may recover a bounded item
only after a fresh derivation-level review and independent validation.

The quarantined claim families include:

- R5-P1 scripts that replaced the eight TODO artifacts with assumed diagonal
  systems, fixed source vectors, or preselected positive matrices;
- UVIR scripts that treated symbolic form, absence of an energy variable, or
  hard-coded booleans as propagator, unitarity, cutoff, or gate closure evidence;
- STAT packaging that fixed an upstream coefficient at `2/3`, ran an optimizer,
  and labelled the result a cleared inference gate despite MAT remaining blocked;
- post-alpha.12 manuscript/publication material that promoted blocked matching
  and observational claims;
- the proposed CBR scale/Landau-disruption chain, whose dimensional algebra and
  inference did not support the claimed scale or Solar-System resolution;
- inconsistent Solar-System bounds and downstream manuscript conclusions.

## Recovery rule

Benign documentation or implementation work in the quarantined range is not
automatically lost. It must be reintroduced as a scoped change with its own
evidence, dependency audit, and claim classification. Git chronology, a script
name containing `PASS`, or a successful optimizer is not scientific evidence.

## Machine enforcement

`Analysis/Integrity/recovery_claim_firewall.py` checks the authoritative JSON
states, the R5-P1 TODO contract, the alpha.12 release boundary, and absence of
known pseudo-closure artifacts. It writes deterministic JSON and SHA-256
evidence. This check is a repository-integrity gate only; its own PASS cannot
close UVIR-003, MAT-001, or any physics gate.
