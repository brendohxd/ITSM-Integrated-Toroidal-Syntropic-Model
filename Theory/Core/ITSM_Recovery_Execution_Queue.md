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
| P0 | Same-chart free-sector quadratic export | **completed (partial)** | Original-chart \(K,C\) exported; constraint source split into \(M_x,M_v\); physical-chart free \(K\) transformed; pure static J2 \(B\) and matter \(d,h,u\) still absent |
| P0 | Declared \(S_{\rm int}\) + IR \(d,h\) form / live placement | **completed (form only; live blocked)** | Architecture/J1 form declared; IR \(d=(-C_m)\), \(h=\emptyset\) recover \(\lvert V\rvert\); live free-sector chart lacks \(\psi\), so UVIR \(d,h\) stay `NOT_EXPORTED` |
| P0 | Force-field hosting readiness inventory | **completed (no host ready)** | Five host routes compared; only Track-A has a force phonon and it lacks matter; full ADM force completion blocked; no live \(d,h\) host selected |
| P0 | Track-A Conditional \(S_{\rm int}\) embed + \(d,h\) export | **completed (Conditional host)** | Track-A selected; \(S_{\rm int}=-C_m\rho_b\psi\) embedded with \(\psi=\psi_{\rm bar}+\pi\); \(d=(-C_m)\), \(h=(0,0)\) exported; free-sector still not identified; \(V\) not computed |
| P0 | Track-A host \(K_Q\) readiness | **completed (symbolic only)** | Host \(K=K_Q\) exported symbolically; on-host \(V\) form + rescaling identity hold; numeric \(K_Q\) still `NOT_DERIVED`; Conditional estimate rejected as Derived |
| P0 | \(K_Q\) microscopic derivation dig | **completed (incomplete)** | P1–P4 paths checked; none ready for numeric \(K_Q\); R3 remains incomplete; R1 not a derivation |
| P0 | Conditional matching branch (dual status) | **completed (open Conditional)** | Branch open with labeled Conditional samples; Derived \(V\)/`K_Q` stay closed; Stage 4A closed |
| P0 | Track-A matter/free-force join readiness | **completed (partial)** | Matter-only static channel form-ready; free-force J2 is velocity-quadratic residual; full multi-sector J2 not assembled |
| P0 | Tier-1 peer-review readiness (hold retained) | **completed** | Stage 5 HOLD re-verified; M2/M3/M6/M7 unmet; Stage 4A reopen contract all false; MAT dual-status surface consistent; claim ledger deny-list executable |
| P0 | Tier-1 forward plan (H0–H7) | **active** | Plan at `Theory/Core/ITSM_Tier1_Forward_Plan.md`; Lane A Derived critical path H1→H5; Lane B Conditional parallel only |
| P0 | H1.1–H1.2 parent-action matching declare + inventory | **completed (incomplete)** | Derived route declared (Z_φ,g_φ→Track-A); repo inventory finds no numeric micro coefficients |
| P0 | H1.3 parent-action source derivation audit | **completed (incomplete)** | All named declared sources audited; no \(Z_\phi/g_\phi\); RR1–RR5 frozen; H1 not complete |
| P0 | H1.4 research requirements published | **completed** | RR1–RR5 in plan + H1.3 JSON; governance firewall RR5 active |
| P0 | RR1 parent-action skeleton declaration | **completed (unmatched coeffs)** | Minimal \(Z_\phi\) kinetic + \(g_\phi\) vertex + Track-A map declared; all micro coeffs still NOT_DERIVED |
| P0 | RR2–H7 bounded completion package | **completed (bounded)** | RR2 incompleteness freeze; RR3 chart convention; H2 symbolic invariance; H3–H6 holds/firewalls; H7 hygiene |
| P0 | RR2 residue pathway attempt | **completed (incomplete)** | Symbolic \(|g_{\rm can}|=V\) on Track-A; no live bare-\(K_Q\)-free export; diagnostics rejected |
| P0 | MAT remediation R5 action identifiability | **completed (HOLD)** | Exact audit proves independent `C_m`,`K_Q` underdetermine signed `V`; shortcut closures and UVIR-route namespace collision rejected; new microscopic relation or live residue required |
| P0 | R5-P1 scale-compensator parent fork | **open (research candidate)** | Minimal shift-symmetric density portal lacks a direct static `rho_b*pi` source; test one-scale compensator/superfluid action, physical-mode residue, stability, cutoff and local-gravity constraints |
| P0 | RR2 true Derived micro/residue | **open (physics wall; R5 no-go proven)** | Declared action underdetermines `V`; needs microscopic \(g_\phi/\sqrt{Z_\phi}\) or live normalized signed residue — **no further inventory substitutes** |
| P0 | H3–H5 true reopen/PASS | **blocked on RR2** | Stage 4A/M2/MAT PASS remain correctly closed |
| P0 | Lane B Conditional dual-status methods | **open (parallel only)** | Probes allowed; never substitute H1–H5 |
| P1 | WAK C1/C2/C3 identity-route evidence rubric | **completed** | All routes are compared under eight hard requirements; none is selectable; C2 calculation priority is not identity selection |
| P1 | RES R1/R2/R3 constitutive-route evidence rubric | **completed** | All routes are compared under eight hard requirements; none is selectable; R0 remains control and R1 is not activated |
| P1 | VOR-to-UVIR parent-identity interface inventory | **completed** | Shared polar convention noted; action identification held undeclared; no resonance/force packaging; `physics_pass: false` |

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
