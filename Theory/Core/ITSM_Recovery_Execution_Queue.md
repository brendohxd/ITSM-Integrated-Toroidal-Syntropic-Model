# ITSM recovery execution queue

**Branch:** `recovery/v12-core-architecture`
**Queue opened:** 2026-08-05
**Sprint goal:** advance the UVIR-to-MAT critical-path interface without
overstating matching, then route the next bounded task from executable
evidence.

This is a short-lived execution queue for remote check-ins. The Master Research
Plan remains the scientific workflow authority; gate reports and deterministic
outputs remain the evidence authority.

## Active queue

| Priority | Task | Status | Definition of done |
|---|---|---|---|
| P0 | UVIR-to-MAT fail-closed handoff audit | **completed** | Eight exact upstream contracts pass; corrupted/mismatched input fails; docs and checkpoint pushed |
| P0 | MAT basis-covariant physical-mode vertex projection | **completed** | Projection identity, field-basis covariance, kinetic normalization and negative controls pass without computing \(V\) |
| P1 | TOP S1M physical-eigenvalue cutoff invariance | **completed** | Modularly reindexed spectra agree under a physical cutoff; raw coordinate-box cutoff hazard reproduced |
| P0 | Live UVIR quadratic-export inventory | **completed** | Required \(K,C,B,d,h,u\) roles are mapped from current outputs; chart/role gaps fail closed; \(V\) remains `NOT_COMPUTED` |
| P0 | Same-chart MAT action export | **blocked by inventory** | Requires derived action-level \(d,h\), isolated \(B\), explicit dimensions and selected \(u\); no placeholder wiring allowed |
| P1 | WAK C1/C2/C3 identity-route evidence rubric | **completed** | All routes are compared under eight hard requirements; none is selectable; C2 calculation priority is not identity selection |
| P1 | RES R1/R2/R3 constitutive-route evidence rubric | **completed** | All routes are compared under eight hard requirements; none is selectable; R0 remains control and R1 is not activated |
| P1 | VOR-to-UVIR parent-identity interface inventory | **queued** | Compare the VOR toy parent and live UVIR condensate conventions without identifying them or packaging resonance numbers |

## Capacity and sequencing

The queue began with three bounded checkpoints and now continues through the
live-export inventory. Validation, documentation and Git publication are
included in each task rather than left as end-of-sprint cleanup. Work proceeds
serially so an upstream correction can change the next task before additional
claims are built on it.

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
| Diagnostic response probes are mistaken for matter vertices | Reject \(Q_\rho,Q_\chi\) impulses as substitutes for action-derived \(d,h\) |
| Partial matrices from different charts are silently combined | Require one explicit chart, normalization and dimension contract before wiring J2 |

## Out of scope for this queue

- numerical \(V\), \(K_Q\) or \(C_{\rm obs}\);
- reopening UVIR Stage 4A;
- full UVIR/MAT physics PASS;
- alpha.12 manuscript freeze;
- cosmological, SPARC, lensing or \(H_0\) packaging.
