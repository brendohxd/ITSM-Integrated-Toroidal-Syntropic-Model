# ITSM recovery execution queue

**Branch:** `recovery/v12-core-architecture`
**Queue opened:** 2026-08-05
**Queue reconciled:** 2026-09-29
**Sprint goal:** execute the user-directed Master ITSM test programme in
dependency order, beginning with the Test 1 action-input completion gate;
preserve all existing fail-closed boundaries.

This is a short-lived execution queue for remote check-ins. The Master Research
Plan remains the scientific workflow authority; gate reports and deterministic
outputs remain the evidence authority.

The current active priority is Test 1 in
`Theory/Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md`. Its entry hold is
`ACTION_INPUT_INCOMPLETE_HOLD_BEFORE_VARIATION`; the hold is not a failed
variation or a physics result. TOP-X4 `X4-S4-C1` is a separate queued lane,
not the active programme priority.

**Rule-9 scheduling decision (25 September 2026):** all outstanding reviews
are `DEFERRED`. Follow `ITSM_RULE9_DEFERRED_REVIEW_POLICY.md` and the deferred
review register. Pending review alone does not block scoped provisional
research or parent documentation. Carry review dependencies forward; retain
scientific failures and missing-input holds for affected uses. The review
backlog is outside the active research critical path until the operator
resumes it; canonical closure and publication readiness still require review.

## Route priority after Rule-9 deferral — 26 September 2026

The deferred-review register separates a review-only dependency from a
substantive scientific hold. If Rule 9 is the only unmet requirement for an
exact bounded use, that use may proceed provisionally under its registered
scope. This does not change `physics_pass`, gate status, claim labels or
publication readiness.

The current work order, ranked by upstream dependency and Tier-1 importance,
is:

1. **P0 — Test 1 action/source-vector closure.** The conditional R4C1 action
   and variation are already recorded. Continue its viability and GR-limit
   work toward a defensible canonical action decision; do not repeat the
   completed candidate variation or presume canonical acceptance.
2. **P0 — R4C1 coupled evolution estimate.** Continue the permitted
   conditional diagnostics for the corrected `Mdot` term, defective zero
   branch and singular-domain controls. S4A rejects the fixed full graph
   differential bound; S4B rejects the specified one-extra-dust-derivative
   graph bound. S4C shows the proposed frame/dust pair is not closed at
   leading order. S4D finds an order-`p^2` phase-gradient-to-phase-kinetic
   term in the unweighted selected chart. S4E completes coordinate 9 and
   finds the leading phase pair is skew; graph-equivalent diagonal weighting
   cannot reduce its entries to order `p`. S4F completes all twelve columns
   and the sixteen-row graph: its only degree-two entries form that skew
   phase pair in a graph-equivalent norm, while the symmetric part still
   grows at order `p`. S4G constructs an exact positive graph-equivalent
   metric that cancels the order-`p` defect and has bounded formal
   high-p energy rate at the B1 initial event. S4H now verifies the
   moving regular-chart minor and reconstructs 24 sampled B1 symbols,
   but its exact moving leading coefficients and uniform interval bound
   remain unproved. Continue that single temporal-persistence gate;
   full IVP remains open.
3. **P0 — Test 2 weak-field and periodic-`T^3` closure.** Derive the force law
   and its domain from the frozen action, retaining the nonspherical rejection
   and harmonic-flux correction.
4. **P0 — Test 3 blind coefficient audit.** Only after an action-level force
   response exists, determine whether `C_chi` and `a0(z)` are identifiable
   without target insertion.
5. **P0 — MAT/UVIR matching.** Derive numeric `K_Q` or an equivalent
   action-level invariant, compute `V`, and then reassess Stage 4A and
   MAT-001.
6. **P1 — TOP-X4 bounded diagnostics.** Continue only as a separate
   conditional lane; local receipts do not replace the missing stress,
   determinant, gravity/ghost, parity/anomaly, counterterm, finite-charge and
   physical-Hessian sectors.
7. **P1 — BBN and observational fits.** Resume only after action-derived
   background and effective-gravity inputs exist; current missing inputs are
   not review-only holds.

The corresponding Rule-9 rows remain `DEFERRED` and `Rule9_cleared=false`.
No active item in this queue waits for independent review when review is its
only remaining requirement; substantive missing inputs and failed physics
checks continue to hold dependent uses.

## Active queue

| Priority | Task | Status | Definition of done |
|---|---|---|---|
| P0 | Master programme Test 1 — covariant action and source vector | **active priority; action-input hold** | Complete and freeze the full off-shell matter/plenum/reservoir action and interaction-stress split before variation; then derive currents and verify regular zero-coupling and declared GR limits. Contract: `Theory/Gates/ITSM_MASTER_TEST_01_SOURCE_VECTOR_CLOSURE_CONTRACT_2026-09-24.md` |
| P0 | Master Tests 1–3 bounded derivation audit | **local calculations complete; provisional reuse allowed; review DEFERRED** | Conditional source/witness 29/29; weak-field 11/11; coefficient 9/9; periodic T3 addendum 19/19; v7.2 transcription-chain rejection 10/10. Full disposition and deferred register retain scope and substantive programme requirements. No parent promotion or complete blind coefficient audit |
| P0 | Approved R4C1 four-dimensional reservoir candidate | **provisional research continues; full coupled well-posedness/stability/GR/matching holds retained** | Current 119/119; variation/Ward 162/162; B1 48/48; G1 56/56; C1 63/63; S1 71/71; S2 56/56; S3 57/57. S4A 99/99 and S4B 169/169 reject two specified fixed-graph instantaneous differential bounds. S4C 117/117 finds the frame/dust pair leaks at order p. S4D 125/125 stops the unweighted order-p recursion at an order-p^2 phase coupling. S4E 147/147 finds a skew leading phase pair and rejects graph-equivalent diagonal weighting as an entrywise order-p repair. S4F 208/208 completes the full B1 symbol: its degree-two pair is skew but the candidate norm has order-p symmetric growth. S4G attempt 02 passes 194/194, constructs an exact positive graph-equivalent correction and bounded formal high-p energy rate at the B1 initial event. S4H attempt 02 passes 189/189 **local reconstruction** checks, but remains `INCOMPLETE_TEMPORAL_PERSISTENCE`: exact moving leading coefficients, uniform energy constants and the physical p-domain are not derived. The failed double-precision S4H attempt 01 is preserved. Full IVP, wider phase cone, quartic dispersion, homogeneous/singular sectors, GR and matching remain open. Failed S2/S3 and both S4D attempts remain preserved. Review deferred; no parent promotion. See `Theory/Gates/RES-001/RES001_R4C1_TEMPORAL_PERSISTENCE_REPORT_2026-09-29.md` |
| Deferred | Tests 1-3 independent review | **DEFERRED_BY_OPERATOR; outside research critical path** | Preserve existing partial reports and sealed snapshots. `docs/ITSM_MASTER_TEST_REVIEW.md` prepares current mandates and ten receipts when needed. Resume reviewers only when directed; Rule 9 remains NOT_CLEARED. Review-only delay does not prevent eligible provisional work |
| P0 | UVIR-to-MAT fail-closed handoff audit | **completed** | Eight exact upstream contracts pass; corrupted/mismatched input fails; docs and checkpoint pushed |
| P0 | MAT basis-covariant physical-mode vertex projection | **completed** | Projection identity, field-basis covariance, kinetic normalization and negative controls pass without computing $V$ |
| P1 | TOP S1M physical-eigenvalue cutoff invariance | **completed** | Modularly reindexed spectra agree under a physical cutoff; raw coordinate-box cutoff hazard reproduced |
| P0 | Live UVIR quadratic-export inventory | **completed** | Required $K,C,B,d,h,u$ roles are mapped from current outputs; chart/role gaps fail closed; $V$ remains `NOT_COMPUTED` |
| P0 | Same-chart free-sector quadratic export | **completed (partial)** | Original-chart $K,C$ exported; constraint source split into $M_x,M_v$; physical-chart free $K$ transformed; pure static J2 $B$ and matter $d,h,u$ still absent |
| P0 | Declared $S_{\rm int}$ + IR $d,h$ form / live placement | **completed (form only; live blocked)** | Architecture/J1 form declared; IR $d=(-C_m)$, $h=\emptyset$ recover $\lvert V\rvert$; live free-sector chart lacks $\psi$, so UVIR $d,h$ stay `NOT_EXPORTED` |
| P0 | Force-field hosting readiness inventory | **completed (no host ready)** | Five host routes compared; only Track-A has a force phonon and it lacks matter; full ADM force completion blocked; no live $d,h$ host selected |
| P0 | Track-A Conditional $S_{\rm int}$ embed + $d,h$ export | **completed (Conditional host)** | Track-A selected; $S_{\rm int}=-C_m\rho_b\psi$ embedded with $\psi=\psi_{\rm bar}+\pi$; $d=(-C_m)$, $h=(0,0)$ exported; free-sector still not identified; $V$ not computed |
| P0 | Track-A host $K_Q$ readiness | **completed (symbolic only)** | Host $K=K_Q$ exported symbolically; on-host $V$ form + rescaling identity hold; numeric $K_Q$ still `NOT_DERIVED`; Conditional estimate rejected as Derived |
| P0 | $K_Q$ microscopic derivation dig | **completed (incomplete)** | P1–P4 paths checked; none ready for numeric $K_Q$; R3 remains incomplete; R1 not a derivation |
| P0 | Conditional matching branch (dual status) | **completed (open Conditional)** | Branch open with labeled Conditional samples; Derived $V$/`K_Q` stay closed; Stage 4A closed |
| P0 | Track-A matter/free-force join readiness | **completed (partial)** | Matter-only static channel form-ready; free-force J2 is velocity-quadratic residual; full multi-sector J2 not assembled |
| P0 | Tier-1 peer-review readiness (hold retained) | **completed** | Stage 5 HOLD re-verified; M2/M3/M6/M7 unmet; Stage 4A reopen contract all false; MAT dual-status surface consistent; claim ledger deny-list executable |
| P0 | Tier-1 forward plan (H0–H7) | **suspended by operator priority** | Plan remains preserved at `Theory/Core/ITSM_Tier1_Forward_Plan.md`; it is not the active September route |
| P0 | H1.1–H1.2 parent-action matching declare + inventory | **completed (incomplete)** | Derived route declared (Z_φ,g_φ→Track-A); repo inventory finds no numeric micro coefficients |
| P0 | H1.3 parent-action source derivation audit | **completed (incomplete)** | All named declared sources audited; no $Z_\phi/g_\phi$; RR1–RR5 frozen; H1 not complete |
| P0 | H1.4 research requirements published | **completed** | RR1–RR5 in plan + H1.3 JSON; governance firewall RR5 active |
| P0 | RR1 parent-action skeleton declaration | **completed (unmatched coeffs)** | Minimal $Z_\phi$ kinetic + $g_\phi$ vertex + Track-A map declared; all micro coeffs still NOT_DERIVED |
| P0 | RR2–H7 bounded completion package | **completed (bounded)** | RR2 incompleteness freeze; RR3 chart convention; H2 symbolic invariance; H3–H6 holds/firewalls; H7 hygiene |
| P0 | RR2 residue pathway attempt | **completed (incomplete)** | Symbolic $|g_{\rm can}|=V$ on Track-A; no live bare-$K_Q$-free export; diagnostics rejected |
| P0 | TOP-X4 original `X4-I1C` parent | **hold — unstabilized** | A2/A3 controls expose a radion runaway and no EFT hierarchy; A4 and Ultra remain closed |
| P0 | TOP-X4 `X4-S2F3` static parity-even determinant | **completed (bounded 12/12)** | Reproduces the frozen stationary witness at zero density; `physics_pass=false`, parity-odd and finite-charge work excluded |
| P0 | TOP-X4 `X4-S2F3` finite-charge entry | **hold (9/9 entry checks)** | `HOLD_TOPX4_S2F3_BEFORE_FINITE_CHARGE_QUANTUM_COMPLETION`; no A4 or Ultra entry |
| P0 | TOP-X4 `X4-S2F3` finite-charge operator | **completed (bounded 16/16)** | Charged amplitude-phase operator and fixed-charge variation identities pass with two negative mutations; dynamic state/stress/Hessian and Rule-9 clearance remain open |
| P0 | TOP-X4 `X4-S2F3` dynamic state/subtraction | **failed (bounded 11/12); preserved** | Exact evolving scalar operator and UV hierarchy pass, but three low-mode fourth-order WKB iterates become non-positive near the initial boundary; the failed branchwise state remains rejected and is not superseded by the separate transport retry |
| P0 | TOP-X4 `X4-S2F3` exact scalar/Dirac transport retry | **completed (bounded 18/18); Hadamard hold** | Prior WKB failure preserved; exact scalar symplectic and first-order Dirac unitary transport pass, but infinite-order state and covariant 5D subtraction remain open; no stress, Hessian, A4 or Ultra |
| P0 | TOP-X4 `X4-S2F3` D5 Hadamard/subtraction readiness | **scaffold completed (bounded 20/20); readiness hold** | Universal D5 local coefficients and counterterm basis pass; model-specific scalar matrix operator, Hadamard states, graviton/ghosts, parity phase and normalization remain incomplete; no stress or downstream entry |
| P0 | TOP-X4 `X4-S2F3` covariant scalar matrix operator | **completed (bounded 25/25); state/stress hold** | Fixed-metric off-shell rank-three Hessian, `E`/`Omega` data and scalar counterterm structures through `b_2` pass; Hadamard states, normalization, gravity/parity, determinant, stress and physical Hessian remain open |
| P0 | TOP-X4 `X4-S2F3` scalar-matrix Hadamard parametrix | **completed (bounded 22/22); global-state hold** | Local D5 `U_0`--`U_2` coincidence/transport controls pass with `E=-H`, matrix `Omega` and phase-mixing controls; global state, stress, determinant, physical Hessian and Rule-9 remain open |
| P0 | TOP-X4 `X4-S2F3` global scalar-matrix state construction | **completed (theorem-backed 10/10); Dirac/stress/Hessian hold** | Route-A pseudodifferential construction records the arbitrary-order formal symbol, Borel/smoothing realization, positive low-mode patch, exact full-matrix transport and basis covariance; `physics_pass=false`, Rule-9 clearance is unmet, and Dirac/gravity/parity, determinant, stress and physical Hessian remain open |
| P0 | TOP-X4 `X4-S2F3` finite-order adiabatic-symbol diagnostic | **completed (bounded 8/8); global-state hold** | Route-B Riccati witness is finite and transpose-symmetric through orders 0–6; stable orders 0–3 show decreasing high-frequency residuals, positive normalized data and exact finite-mode CCR transport for the full rank-three matrix; no Borel sum or global state is claimed |
| P0 | TOP-X4 `X4-S2F3` physical-Hessian readiness audit | **completed (readiness 8/8); physical Hessian hold** | Confirms the complete varied action, state-dependent stress, gravity/ghost/parity sectors, finite-charge background and metric/radion constraint blocks are not exported; `physical_hessian=NOT_CONSTRUCTED`, `radion_mass=NOT_COMPUTED`, `physics_pass=false` |
| P0 | TOP-X4 `X4-S2F3` Dirac/parity/anomaly readiness audit | **completed (readiness 10/10); fermion/parity hold** | Static determinant remains parity-even and first-order Dirac transport remains finite-order; `dirac_completion=NOT_DERIVED`, `parity_odd_determinant_phase=NOT_DERIVED`, `anomaly_cancellation=NOT_DERIVED`, `counterterm_quantization=NOT_FIXED`, `physics_pass=false` |
| P0 | TOP-X4 `X4-S2F3` scoped curved Dirac operator | **completed (bounded 13/13); quantum closure hold** | Hamiltonian-form operator, homogeneous spin connection, periodic KK spectrum and three negative mutations pass; 2/2 contract checks are separated from 11/11 operator checks; Hadamard state, determinant, parity/anomaly, stress and Hessian remain open |
| P1 | Paper-suite artifact naming | **completed locally** | P1–P4 use descriptive versioned PDF names; P3/P4 remain quarantined claim-bearing scaffolds, not publication-ready papers |
| P1 | TOP-001 3D Epstein Casimir tensor | **bounded controls complete; research scaffold remains open** | Static finite-cutoff Epstein stress, passive dilution and inserted-source sensitivity controls pass twice byte-identically; action-derived modulus/reservoir stress, independent dynamical stress and research-gate closure remain open |
| P1 | WAK C1/C2/C3 identity-route evidence rubric | **completed** | All routes compared under eight hard requirements; C2 retained as calculation scaffold |
| P1 | RES R1/R2/R3 constitutive-route evidence rubric | **completed** | All routes compared under eight hard requirements; R0 retained as control |
| P1 | 14 September external evidence watch | **recorded; no gate change** | Six unreviewed arXiv inputs recorded; BBN/helium, JWST clustering, siren, LVK-curvature and intrinsic-alignment follow-ups are dependency-locked in `Theory/Core/ITSM_EXTERNAL_EVIDENCE_WATCH_2026-09-14.md` |
| P1 | BBN-001 bundled-table/CAMB and external-network controls | **completed and published** | Six focused regression checks, five table schemas, PRIMAT 2024 compatibility, CAMB bridge and isolated AlterAlterBBN baseline/expansion controls pass; remains `CONTROL_ONLY`, `physics_pass=false`, `gate_effect=NONE` |
| P1 | BBN-001 ITSM upstream-background interface preflight | **completed; upstream physics blocked** | Registered UVIR-003 export is checked for the external six-column history and ITSM closing inputs; missing physical temperature, units, plenum, transfer, charge-source and $G_{\rm eff}$ fields fail closed; no quantity is inferred |
| P1 | BBN-001 action-derived input contract | **completed (validated 12/12); upstream physics blocked** | Machine-readable network/ITSM field contract is frozen; preflight records a precise 12-field missing-input receipt; values/provenance remain unvalidated and no BBN prediction is claimed |
| P1 | MAT-001/TOP-X4 H1 signed-source bridge readiness | **completed locally; bridge hold** | Schur-reduced source/kinetic target and 10-item closure inventory are frozen; foundation 11/11 and mutations 6/6 pass; signed residue, physical mode, stabilized background and K_Q/V remain closed |
| P1 | MAT-001/TOP-X4 bulk-versus-brane architecture comparison | **completed locally; route recommendation only** | Exact radion source scaling and Track-A derivative mismatch are checked; brane-induced-metric child is the lead candidate; no child action is frozen and X4-S2F3 is unchanged |
| P1 | MAT-001/TOP-X4 brane-child global-consistency preflight | **completed locally; conditional hold** | Proper delta normalization, dimensions, localized variation, junction obligations, compact-space tension rejection and counterterm requirements pass 11/11 with 8/8 mutations; child freeze remains held |
| P1 | MAT-001/TOP-X4 minimal brane-child freeze decision | **completed locally; minimal candidate rejected** | Flat-product distributional control requires lambda_b^ren=0 for a lone tension; 10/10 checks and 7/7 mutations pass; compensated/warped child remains a separate route and X4-S2F3 is unchanged |
| P1 | MAT-001/TOP-X4 compensated/warped route handoff | **completed locally; new-parent design only** | Existing S0 audit defers X4-S4 orbifold/brane as a different parent and finds no distinct minimal smooth-S1 flux repair; 10/10 checks and 7/7 mutations pass; no compensator or new action selected |
| P1 | MAT-001/TOP-X4 constraint/projection bookkeeping diagnostic | **completed locally; synthetic method hold** | Exact rational Schur/source projection, basis covariance, orientation-sign retention and singular-domain rejection pass 13/13; 6/6 mutations pass; no live Hessian or gate promotion |
| P1 | MAT-001/TOP-X4 X4-S4-GW2 candidate-action contract | **completed locally; candidate frozen, parent not accepted** | Orbifold geometry, two fixed surfaces, full leading classical bulk/localized action, variational signs, derived static sum-rule weights and counterterm classes pass 21/21 checks with 15/15 mutations rejected; zero-charge background existence is next and all downstream physics holds remain closed |
| P1 | MAT-001/TOP-X4 X4-S4-GW2 zero-charge background existence | **completed locally; registered benchmark rejected, new-parent action selection required** | Two bounded BVP attempts converged numerically but the best branch collapsed to `L=8.505e-13`; independent constraint residual `10.9723` and static-balance residual `0.683833` fail; no finite-charge or downstream promotion follows |
| P1 | MAT-001/TOP-X4 post-zero-charge action selection | **completed locally; separate queued lane; curved-slice output not computed** | The failed flat benchmark remains immutable and is classified as a codimension-one flatness compatibility failure; exact curved Einstein/constraint/balance signs pass 13/13 checks with 14/14 mutations rejected. If resumed, the next output is signed `kappa4` under `TOPX4_H1_X4-S4_CURVED_SLICE_BACKGROUND_OUTPUT_TEST`; parent acceptance, finite charge, H1 and MAT remain closed |
| Deferred | Rule-9 TOP-X4/BBN evidence packet | **DEFERRED_BY_OPERATOR; historical packet preserved** | Existing packet contains 11 authority documents, 24 hashed receipts, unresolved questions and role-separated prompts. Historical clearance remains `THREE_WAY_CLEARANCE_NOT_MET`; review alone does not stop eligible work. Reassess the exact substantive dependencies when that queued lane resumes |

## Quarantined 29 August queue assertions

The prior queue placed the following items in the active table as completed or
passed. The 1 September parent-gate audit rejected those promotions. They are
retained here as disagreement provenance and **must not** be used as current
status:

| Prior assertion | Current adjudication |
|---|---|
| MAT R5 hold resolved by conformal trace and BTFR scale matching | **Quarantined:** the declared action underdetermines the normalized response; MAT-001 remains `BLOCKED` |
| R5-P1 fixed $C_m=1$, $f=1/\sqrt{4\pi G}$, $V=\sqrt{4\pi G}$ and $\alpha=1$ | **Quarantined:** these are not parent-action-derived ITSM constants |
| UVIR-003 tree-level unitarity passed with $\Lambda_{\rm UV}=f/C_m$ | **Quarantined:** the complete constrained amplitude and matched physical cutoff remain open |
| DISK-001 and the 175-galaxy STAT-001 package passed | **Quarantined:** DISK is `METHODS_ONLY`; STAT is `NOT_STARTED_AS_CLOSED_GATE` |
| VOR spectrum, SCR screening and LEN lensing passed | **Quarantined:** VOR remains an open scaffold; SCR and LEN remain open downstream of MAT/UVIR |
| P3 and P4 were complete publication drafts | **Quarantined:** their claim-bearing sources are retained only as visibly marked legacy scaffolds |

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
| A structural identity is mistaken for numerical matching | Keep $V$ `NOT_COMPUTED`, MAT blocked and Stage 4A closed in executable outputs |
| A field-coordinate coefficient is mistaken for an invariant | Test simultaneous source and kinetic transformations under invertible basis changes |
| A label cutoff creates a false torus-spectrum difference | Compare a physical eigenvalue cutoff and separately reproduce the raw-label-box hazard |
| Documentation drifts from executable status | Update canonical gate notes and changelog in the same checkpoint |
| Diagnostic response probes are mistaken for matter vertices | Reject $Q_\rho,Q_\chi$ impulses as substitutes for action-derived $d,h$ |
| Partial matrices from different charts are silently combined | Require one explicit chart, normalization and dimension contract before wiring J2 |

## Out of scope for this queue

- numerical $V$, $K_Q$ or $C_{\rm obs}$;
- reopening UVIR Stage 4A;
- full UVIR/MAT physics PASS;
- alpha.12 manuscript freeze;
- cosmological, SPARC, lensing or $H_0$ packaging.
