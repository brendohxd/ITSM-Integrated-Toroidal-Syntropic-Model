# ITSM G0 contradiction and disposition ledger

**Date:** 2026-08-25  
**Branch:** `recovery/v12-core-architecture`  
**Scope:** authority, source-to-claim alignment, reproducibility and downstream status propagation  
**Scientific effect:** governance repair only; no physics gate is promoted

## Authority rule

The signed parent decisions and `active_research.md` override child reports,
duplicate dashboards, manuscript packaging, public pages and historical
artifacts. A script-level `PASS_*` is scoped to the checks that the script
actually performs and is never, by itself, a physics PASS.

## Ledger

| ID | Contradiction or defect | Controlling evidence | Disposition |
|---|---|---|---|
| G0-C01 | `active_research_updated.md` promotes alpha.13 and calls STAT a completed Bayesian MCMC analysis. | `active_research.md`; `STAT-001_READINESS.md`; optimizer source uses L-BFGS-B. | **QUARANTINE** duplicate dashboard; use `active_research.md` only. |
| G0-C02 | `MAT-001_R6_GATE_CLEARANCE.md` clears MAT and locks `V=C_m/f`. | Signed MAT R5 decision retains HOLD, `V NOT_COMPUTED`, `K_Q NOT_DERIVED`. | **QUARANTINE** invalid child decision. |
| G0-C03 | R5-P1 Task 1 claims a static-source obstruction while deriving a linear source. | Its own ADM expansion; R5-P1 parent specification. | **QUARANTINE** as a failed derivation. |
| G0-C04 | R5-P1 Task 2 substitutes a real-scalar compensator for the required finite-density parent and leaves scales free. | Task 2 conclusion; R5-P1 parent specification. | **QUARANTINE** as a negative toy route. |
| G0-C05 | R5-P1 Task 3 infers ghost freedom from a spatial Hessian without the constrained temporal kinetic system. | Missing lapse/shift, finite-density and reservoir reduction. | **QUARANTINE** incomplete audit. |
| G0-C06 | R5-P1 Task 4 contains a coefficient mismatch: its equations yield `sqrt(G M a0)/r`, not the claimed extra `sqrt(2)`. | Direct algebra from its displayed equations. | **QUARANTINE** mathematical draft. |
| G0-C07 | R5-P1 Task 5 changes the action sign and does not diagonalize the full constrained physical basis. | Task 4/5 comparison and missing kinetic eigenbasis. | **QUARANTINE** sign/projection draft. |
| G0-C08 | R5-P1 Task 6 changes the invariant convention on a static branch and promotes scaling power counting as a physical cutoff. | Its definition of `Y` and fractional-power use. | **QUARANTINE** convention/cutoff draft. |
| G0-C09 | R5-P1 Task 7 fails its own Cassini coupling inequality and asserts uncomputed PPN, lensing, GW and cluster results. | Its displayed bound and value. | **QUARANTINE** failed compliance claim. |
| G0-C10 | R5-P1 UVIR propagator and zero-mode artifacts hardcode the desired diagonal/well-posed structure. | Producer code appends positive diagonal blocks and Boolean conclusions. | **QUARANTINE** documents, code and outputs as toy checks. |
| G0-C11 | R5-P1 cubic exchange expands an assumed matter exponential and calls the excursion scale a UV cutoff. | Producer operations do not perform constraint elimination or signed mode projection. | **QUARANTINE** algebraic proxy. |
| G0-C12 | R5-P1 amplitude differentiates a background-density contact term but claims the full physical amplitude and arbitrary-energy unitarity. | Producer omits vacuum, derivative, gravity, mixed, exchange and constrained sectors. | **QUARANTINE** contact-only toy. |
| G0-C13 | Alternative UVIR T1/T2-T4/T5 chain uses a wrong static-gradient branch, an unspecified amplitude coefficient and an assumed cutoff. | Direct sign, coefficient and partial-wave audit. | **QUARANTINE** all three drafts. |
| G0-C14 | STAT gate report calls poor optimizer results a massive success and assumes the upstream coefficient. | Raw summary; L-BFGS-B source; MAT remains blocked. | **QUARANTINE** report and outputs as gate evidence; retain exploratory provenance. |
| G0-C15 | STAT's stored `chi2` includes prior penalties, while AIC/BIC and reduced chi-square use that name; no posterior sampler or output sidecar exists. | `stat001_inference_pipeline.py`. | **REPAIR BEFORE REUSE**; rewritten gate spec now requires separate raw likelihood and penalties. |
| G0-C16 | `CBR-002_SCALE_DERIVATION.md` imposes BTFR/RAR targets, confuses `ell` with `ell^2`, and infers a causality theorem from a static spatial function. | Direct algebra and dimensions. | **QUARANTINE** target-conditioned draft. |
| G0-C17 | `SOLAR_SYSTEM_BOUND.md` compared a fifth-force ratio directly with PPN `gamma`, misstated orders of magnitude and declared Landau disruption as the solution. | Observable mismatch and absent parent-action screening solution. | **REPAIR** diagnostic scope; disruption remains an open candidate. |
| G0-C18 | `HEALING_LENGTH_TEST.md` equates a target-conditioned scale with a healing length without a derived map or microscopic inputs. | Missing mass, number density, scattering length and relativistic condensate map. | **QUARANTINE** future test. |
| G0-C19 | Claim ledger and Master Plan promoted `C=1` and called `C=2/3` falsified without a closed matched statistical gate. | MAT, DISK and STAT are not closed. | **REPAIR** both as preregistered comparators; reject only the trace-ratio derivation. |
| G0-C20 | Pages advertised alpha.13, UVIR complete, R5-P1 complete and STAT complete. | `VERSION=12.0-alpha.12`; signed parent decisions. | **REPAIR** `docs/index.html` and `docs/research.html`. |
| G0-C21 | Root alpha.13 manuscript, JCAP cover letter and v11.4.1 extraction exceed every current gate. | Current alpha.12 recovery manuscript and parent decisions. | **QUARANTINE** source and companion PDFs; preserve only for provenance. |
| G0-C22 | Root README's live header pointed to alpha.13 and its archived block remained searchable as if current. | `Manuscript/CoreRecovery/VERSION`; current dashboard. | **REPAIR** live pointer and add an explicit invalidated-history banner. |
| G0-C23 | MAT handoff accepted a missing input sidecar and documented a stale output digest. | Producer/report audit and canonical-LF hash comparison. | **REPAIR AND RECOMPUTE** with mandatory sidecars and final-byte hashing. |
| G0-C24 | R5 sidecar producer used platform text mode, leaving a line-ending-only dirty artifact. | Raw/filtered hash comparison. | **REPAIR AND RECOMPUTE** with byte-exact LF output. |
| G0-C25 | UVIR local four-leg CSV/JSON appear dirty only because of CRLF and lack complete environment/provenance capture. | Git-normalized blobs equal HEAD; runtime differs from `environment.yml`. | **KEEP** scoped historical evidence; do not claim fresh exact reproduction until environment/provenance are controlled. |

## Preserved authority

- `Theory/Gates/MAT-001/MAT-001_R5_MICROSCOPIC_MATCHING_DECISION.md`
- `Theory/Gates/MAT-001/MAT-001_R5_P1_SPEC.md`
- `Theory/Gates/UVIR-003/UVIR-003_STAGE_B_STAGE5_FULL_GATE_DECISION.md`
- `Theory/Gates/UVIR-003/UVIR-003_FULL_GATE_CLOSURE_CHECKLIST.md`
- `Theory/Gates/RES-001/` fail-closed route artifacts
- `Manuscript/CoreRecovery/` working source and immutable alpha.1 through alpha.12 releases

## Quarantine meaning

Quarantine is non-destructive. The artifact remains in place to preserve
provenance, but it may not be cited as live gate evidence, imported into a
manuscript, used to unblock a child gate or presented on a public status
surface. PDF companions inherit the quarantine of their same-version source.

