# ITSM recovery execution queue

**Branch:** `recovery/v12-core-architecture`
**Queue opened:** 2026-08-05
**Sprint goal:** advance the UVIR-to-MAT critical-path interface without
overstating matching, then harden the independent TOP basis audit.

This is a short-lived execution queue for remote check-ins. The Master Research
Plan remains the scientific workflow authority; gate reports and deterministic
outputs remain the evidence authority.

## Active queue

| Priority | Task | Status | Definition of done |
|---|---|---|---|
| P0 | UVIR-to-MAT fail-closed handoff audit | **completed** | Eight exact upstream contracts pass; corrupted/mismatched input fails; docs and checkpoint pushed |
| P0 | MAT basis-covariant physical-mode vertex projection | **queued** | Projection identity, field-basis covariance, kinetic normalization and negative controls pass without computing \(V\) |
| P1 | TOP S1M physical-eigenvalue cutoff invariance | **queued** | Modularly reindexed spectra agree under a physical cutoff; raw coordinate-box cutoff hazard reproduced |

## Capacity and sequencing

The queue is intentionally scoped to three bounded checkpoints. Validation,
documentation and Git publication are included in each task rather than left
as end-of-sprint cleanup. Work proceeds serially so an upstream correction can
change the next task before additional claims are built on it.

## Definition of done for every checkpoint

- executable result passes twice with byte-identical JSON;
- malformed or mismatched input exits nonzero where applicable;
- claim-firewall fields remain fail closed;
- no absolute workstation paths enter tracked outputs;
- relevant README, gate note, worklog and changelog are updated;
- frozen manuscript releases remain unchanged;
- scoped files only are committed and pushed to the recovery branch.

## Risks and controls

| Risk | Control |
|---|---|
| A structural identity is mistaken for numerical matching | Keep \(V\) `NOT_COMPUTED`, MAT blocked and Stage 4A closed in executable outputs |
| A field-coordinate coefficient is mistaken for an invariant | Test simultaneous source and kinetic transformations under invertible basis changes |
| A label cutoff creates a false torus-spectrum difference | Compare a physical eigenvalue cutoff and separately reproduce the raw-label-box hazard |
| Documentation drifts from executable status | Update canonical gate notes and changelog in the same checkpoint |

## Out of scope for this queue

- numerical \(V\), \(K_Q\) or \(C_{\rm obs}\);
- reopening UVIR Stage 4A;
- full UVIR/MAT physics PASS;
- alpha.12 manuscript freeze;
- cosmological, SPARC, lensing or (H_0) packaging.
