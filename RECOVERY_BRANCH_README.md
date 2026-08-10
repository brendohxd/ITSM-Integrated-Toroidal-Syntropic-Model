# ITSM v12 core-recovery branch

This is the working guide for `recovery/v12-core-architecture`. The recovery
branch rebuilds the ITSM core from explicit actions, derivations, diagnostics,
and falsifiable gates. Legacy v11 documents remain historical inputs; they are
not the scientific status authority for this branch.

> **Forensic reconstruction checkpoint (2026-08-10):** the isolated repair
> branch `codex/recovery-forensic-rebuild` is rebuilt from reviewed anchor
> `4682a51`. Scientific changes from `c3386f0` through `4310a9a` are
> quarantined pending fresh review. This does not promote any gate. See the
> [repair record](Theory/Gates/RECOVERY_FORENSIC_REPAIR_2026-08-10.md) and
> [active status](Theory/Core/ITSM_Active_Research_Status.md).

## Start here

- **GitHub Pages (recovery site):** `docs/` — custom domain **itsm-cosmology.com**
  (see `docs/README.md` for DNS; fallback `https://brendohxd.github.io/ITSM-Integrated-Toroidal-Syntropic-Model/`)
- **Master research plan (workflow + identity + bans + timeline):**
  `Theory/Core/ITSM_Master_Research_Plan.md`
- Active research status: `Theory/Core/ITSM_Active_Research_Status.md`
- Core identity briefing: `Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md`
- Core architecture: `Theory/Core/ITSM_Core_Architecture.md`
- Recovery plan (gate detail): `Theory/Core/ITSM_Core_Recovery_Plan.md`
- Claim migration ledger: `Theory/Core/ITSM_Claim_Migration_Ledger.csv`
- Gate worklog: `Theory/Gates/RECOVERY_SESSION_WORKLOG.md`
- Selective publishing firewall: `papers/Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md`
- Manuscript workflow: `Manuscript/CoreRecovery/README.md`
- Manuscript changes: `Manuscript/CoreRecovery/CHANGELOG.md`
- Current bounded execution queue: `Theory/Core/ITSM_Recovery_Execution_Queue.md`

## Manuscript status

The newest frozen manuscript release is
[`12.0-alpha.12`](Manuscript/CoreRecovery/releases/v12.0-alpha.12/)
(06 August 2026). Every freeze is immutable under
`Manuscript/CoreRecovery/releases/v12.0-alpha.N/`. Working sources live in
`Manuscript/CoreRecovery/`; authoritative per-release detail is in
[`Manuscript/CoreRecovery/CHANGELOG.md`](Manuscript/CoreRecovery/CHANGELOG.md)
and each release’s `RELEASE_NOTES.md`.

Claim hygiene is unchanged across freezes: `13/12`, `H0=72.97`, automatic
Solar-System compliance, and historical SPARC `p=0.62` are **not** live
predictions. UVIR-003 remains **in progress**; MAT-001 is not unlocked.

### Frozen releases (`12.0-alpha.1` ... `12.0-alpha.12`)

#### [`12.0-alpha.1`](Manuscript/CoreRecovery/releases/v12.0-alpha.1/) — 2026-07-26

**Baseline architecture freeze** (Git commit `c836172`).

- Corrected v12 core architecture through zero-gradient scalar force-block
  factorization.
- Conditional weak-field limit retained; open-gate structure explicit.
- Research-stage reconstruction only — not a completed alternative cosmology.

#### [`12.0-alpha.2`](Manuscript/CoreRecovery/releases/v12.0-alpha.2/) — 2026-07-26

**Representative background-existence checkpoint.**

- Scalar-sector ADM-readiness audit and background-completion candidate screen.
- Homogeneous/isotropic FRW minisuperspace equations; representative on-shell
  expanding branch verified (Friedmann residual at the reported level).
- Frame-sector speed normalization corrected; UV/IR, exchange, cosmology,
  open-gates, and references updated.
- **Boundary:** closes only representative background existence. Scalar
  perturbation stability, full cosmological viability, and observational
  acceptance remain open.

#### [`12.0-alpha.3`](Manuscript/CoreRecovery/releases/v12.0-alpha.3/) — 2026-07-26

**Nonlinear scalar-readiness checkpoint.**

- Aether-unitary scalar ADM principal-symbol reduction; finite-wavenumber
  condensate kinetic determinant and `q_ADM` validity scale.
- Complete time-dependent quadratic finite-`q` scalar constraint reduction and
  compact eigenvalue scan; exact `q_phys^2` low-wavenumber kinetic factor.
- Homogeneous time-translation null identity; gauge-invariant `q=0` scalar
  basis; representative positivity scan. Strict low-`q` rank loss identified
  as the homogeneous gauge orbit (not pure matter collapse).
- Longitudinal Stueckelberg quadratic/cubic aether vertex basis; complete
  3D flat-decoupling khronon cubic operator basis (collinear cross-check;
  constraint-order identity: first-order lapse/shift suffice at cubic order).
- On-shell three-point kinematics force collinearity; NDA diagnostic kept
  non-cutoff.
- Complete 3D flat-decoupling quartic khronon basis (96 expanded monomials);
  finite elastic contact; elastic `t/u` cubic exchange vanishes; `s` channel
  on homogeneous khronon gauge orbit; quartic Schur needs second-order
  constraint source.
- Nonlinear ADM provenance for exact
  `gravity+aether+condensate+alignment` parent block.
- Force-sector completion hold: evolving-frame `Delta_U` and non-analytic
  `Y^(3/2)` at `Y=0` required before full cosmological `J2`.
- Spin-0 superluminality recorded as multicone causality flag, not local
  instability verdict.
- **Boundary:** nonlinear scalar readiness advanced; full force-sector action,
  cosmological `J2`, physical `2-to-2`, unitarity cutoff, and MAT-001 open.

#### [`12.0-alpha.4`](Manuscript/CoreRecovery/releases/v12.0-alpha.4/) — 2026-07-29

**Label:** Complete finite-`q` `J2` and Schur checkpoint *(interpretation later corrected in alpha.5)*.

- Bounded force-completion option audit; covariant rest-space Laplacian
  identities and symbolic smoothing expansions.
- **Track A selected:** rest-space Laplacian
  `D_mu D^mu psi`; exact `Y^(3/2)` retained for a declared local
  nonzero-gradient perturbative force test (vs smooth homogeneous completion
  with a new crossover scale).
- Track-A force ADM expansion through direct quartic order; force-sector
  lapse/shift `J2` component.
- Finite-`q` multi-sector origin-linear `J2` (exact regression to prior linear
  constraint source) and algebraic Schur component
  `-J2_origin^T C^(-1)J2_origin/2`.
- **Boundary at freeze:** origin-linear source/Schur recorded as complete
  (reclassified in alpha.5). Direct quartic contact, physical `2-to-2`,
  cutoff, nonzero-gradient exact-`Y` reduction, and MAT-001 remain open.

#### [`12.0-alpha.5`](Manuscript/CoreRecovery/releases/v12.0-alpha.5/) — 2026-07-29

**Label:** Mode-resolved complex-quartet transfer checkpoint.

- **Correction of alpha.4:** finite-`q` `J2_origin` is the verified
  origin-linear constraint component, not the complete second-order source.
  Correct source: `S2 = partial_z L3[x,z1]` with `z1 = -C^(-1)J1`. Corrected
  quartic Schur: `-S2^T C^(-1)S2/2`.
- Complete constraint-free direct cubic/quartic physical contact blocks
  `L3[x,0]`, `L4[x,0]` for
  `gravity+aether+condensate+alignment+Track-A force`.
- Soft-curvature scalar-shift dressing, condensate temporal lapse/shift-
  advection dressing, Track-A affine-constraint audit; complete multi-sector
  finite-`q` `S2`; generic `L4[x,z1]`; full reduced quartic before physical-
  mode projection.
- Regular finite-`q` physical-scalar basis; analytic cubic Fourier
  polarization; factorized physical-basis cubic kernel; factorized reduced
  quartic momentum kernel (pair-source + three finite-channel Schur pairings).
- Exact homogeneous projectors remove scalar shift / `Xi` gauge coordinates
  while retaining the lapse constraint and `(Q_rho,Q_chi,Pi)` subspace.
- Finite-`q` physical inverse quadratic kernel, factorized force propagator,
  exact-`q=0` projected response; pole/residue/inverse-closure/kinetic-inertia
  diagnostics.
- Fixed-comoving pole tracking and kinetic-normalized transfer matrices with
  canonical-Hamiltonian equivalence check. Frozen-pole exponentiation fails in
  the nonadiabatic domain. Initial `q_phys/H=0.01` max phase-space gain
  `1.37708e27`.
- Five-case on-shell background/alignment audit: `Xi`-seeded dominant input
  every case, but every trajectory enters an off-axis complex quartet
  preventing unique continuous rank-two gauge/matter pole split. Record
  `HOLD_COMPLEX_QUARTET_IR_MODE_ATTRIBUTION`.
- **Boundary:** kernels verified on declared nonzero-momentum domains; exact
  zero-gradient `|grad(pi)|^3` Taylor kernel, source-projected retained-
  observable response, exchange-plus-contact amplitude, unitarity, and cutoff
  remain open.

#### [`12.0-alpha.6`](Manuscript/CoreRecovery/releases/v12.0-alpha.6/) — 2026-07-29

**Label:** Gauge-projected matter response checkpoint.

- Gauge-projected source-to-observable retarded-response audit in retained
  `(Q_rho,Q_chi)` only (no direct `Xi` or homogeneous time-translation source
  support).
- Source covectors annihilate the homogeneous time-translation orbit;
  source/readout support, impulse structure, orthonormality, and coarse/fine
  diagnostics across five reference / nearby on-shell-background / alignment
  cases.
- All five cases retain amplified through-quartet matter response, ranging
  from `2.67849e17` to `9.75967e19` (coarse/fine errors below the reported
  threshold). Record
  `PASS_GAUGE_PROJECTED_MATTER_RESPONSE_SURVIVES_WITH_SCOPE`.
- Clarified: Track-A force mode `Pi` remains in the complete finite-`q`
  physical basis; it factorizes at quadratic order and is outside the coupled
  complex-quartet block, not omitted from the framework.
- **Boundary:** resolves direct gauge-source attribution only for the tested
  finite-duration dimensionless neighborhood — not an all-background
  instability theorem, S-matrix, unitarity result, strong-coupling scale, or
  physical cutoff.

#### [`12.0-alpha.7`](Manuscript/CoreRecovery/releases/v12.0-alpha.7/) — 2026-07-29

**Label:** Controlled exchange-domain checkpoint.

- Controlled fixed-comoving exchange-domain map: real-pole, positive-kinetic,
  subhorizon, coupled-mode adiabaticity, and factorized-force adiabaticity
  criteria.
- High-momentum phase-space eigenspace projectors; every nonzero internal
  channel must independently pass the same domain gate.
- Removed infrared `Xi`-pure `gauge_continuation_Xi` initialization at high
  momentum; controlled domain tracks all three coupled finite-`q` physical
  pairs without that IR label.
- Sampled bracket on the representative branch: initial
  `q/H = 47.5, 50, 75, 100` pass; `45` fails the `0.1` adiabatic threshold.
  Sampled bracket only — not a continuous or all-background boundary.
- **Boundary:** physical vertex contraction, exchange-plus-contact amplitude,
  unitarity bound, strong-coupling scale, and physical cutoff remain unfinished.

#### [`12.0-alpha.8`](Manuscript/CoreRecovery/releases/v12.0-alpha.8/) — 2026-07-29

**Label:** Mode-projected cubic pair-source checkpoint.

- Residue-normalized local coupled modes via positive-pole derivative of the
  finite-`q` inverse kernel.
- Physical cubic pair-source contraction: two on-shell external legs → one
  off-shell channel covector in `(Xi,Q_rho,Q_chi,Pi)`; sum- and
  difference-frequency channel prescriptions over 48 admitted equilateral
  mode/sign cases.
- Nonzero-channel inverse-kernel response, pole-separation, constraint margin,
  and external-leg permutation audits (residuals ~`1e-15`–`1e-16` class).
- Clarified: two coupled external legs produce no factorized `Pi` source in
  the verified analytic cubic kernel — does not remove `Pi` from the theory
  or resolve the held nonanalytic local-gradient vertex.
- Record `PASS_MODE_PROJECTED_CUBIC_PAIR_SOURCE`.
- **Boundary:** matched left/right source contraction, channel summation,
  reduced quartic contact assembly into a four-leg kernel, physical amplitude,
  and any unitarity scale remain unfinished.

#### [`12.0-alpha.9`](Manuscript/CoreRecovery/releases/v12.0-alpha.9/) — 2026-07-30

**Label:** Local four-leg kernel checkpoint.

- Completes the local analytic four-leg assembly requested by alpha.8.
- Four residue-normalized coupled modes on shell at the initial frozen-time
  snapshot (all-incoming elastic convention); equal-magnitude spatial momenta
  at regular-tetrahedron vertices so every `s`, `t`, `u` partition has
  strictly nonzero `q_K = 2q/sqrt(3)`.
- Each internal trajectory independently rerun through the fixed-comoving
  controlled-domain audit.
- Per partition: matched left/right physical cubic pair sources + complete
  finite-`q` physical propagator + polarized analytic quartic contact +
  constraint-induced quartic Schur pairing.
- Across 24 elastic mode-pair cases and 72 channel contractions: combined local
  kernels finite, nonzero, real within numerical tolerance, and permutation
  consistent.
- Record `PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL`.
- Representative audits: on-shell residual `3.41511e-15`; residue-norm error
  `3.33067e-16`; pair-source swap `5.98691e-16`; component permutation
  `1.70304e-14`; inverse-closure `4.74692e-16`; min pole distance `0.171148`;
  max imag fraction `1.92562e-16`; real-kernel range `[-62.1674, 1.78508]`;
  cancellation-ratio range `[0.00502092, 0.101546]` (kernel can be ~`0.5%` of
  the sum of absolute component magnitudes — resolved cancellation, not a
  derived suppression scale).
- Reproduce from repository root:

  ```powershell
  python Analysis\UVIR\UVIR-003\uvir003_local_four_leg_kernel.py
  ```

  Expected: `PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL`.

- **Boundary:** local frozen-time analytic four-leg kernel on the tested
  regular-tetrahedral slice only. Does **not** establish asymptotic
  cosmological in/out states; an S-matrix amplitude or cross section; optical-
  theorem or partial-wave unitarity normalization; a strong-coupling scale or
  physical EFT cutoff; robustness over general four-leg kinematics; the held
  nonanalytic `|grad(pi)|^3` contribution on a nonzero-gradient background;

## Current Status (2026-08-07)
*   **Target:** `v12.0-alpha.12`
*   **MAT-001 (Microscopic Matching):** BLOCKED (V=1/f NOT_COMPUTED, identifiability hold)
*   **UVIR-003 (Causality & Unitarity):** IN_PROGRESS (Blocked by MAT-001)
*   **VOR-001 (Topological Sector):** PASS_SCAFFOLD (S1 completed)
*   **Next Milestone:** UVIR-003 completion

### Mission Brief
The recovery branch is attempting to remediate the MAT-001 physics wall. The declared action underdetermines $V$. The R5-P1 scale-compensator fork is currently being evaluated to see if it can algebraically derive $V=1/f$. UVIR-003 remains on a Tier-1 closure hold until the matched invariant is verified.

#### [`12.0-alpha.10`](Manuscript/CoreRecovery/releases/v12.0-alpha.10/) — 2026-08-03

**Label:** Post-alpha.9 UVIR-003 path package.

- Records the FRW in-in observable path declaration and multi-slice
  mode-projected Green proxy.
- Records the local Track-A nonzero-gradient `|grad(pi)|^3` expansion and
  scoped tree/NDA criterion.
- Records the matching-invariant inventory while leaving numeric `K_Q` and
  the physical cutoff unmatched.
- **Boundary:** no cosmological S-matrix or optical theorem, no matched
  physical cutoff, no full UVIR-003 PASS, and no MAT-001 unlock.

#### [`12.0-alpha.11`](Manuscript/CoreRecovery/releases/v12.0-alpha.11/) - 2026-08-04

**Label:** Tier-1 closure hold and identity decision checkpoint. **Prior freeze**

- Integrates the post-alpha.10 Stage 1--5 record through
  `PASS_STAGE5_DECISION_HOLD_TIER1`; UVIR-003 remains `IN_PROGRESS`.
- Records the fail-closed MAT blocker map with $V=C_m/\sqrt{K_Q}$ still
  `NOT_COMPUTED`; MAT-001 remains `BLOCKED`.
- Integrates TOP/VOR scaffold-only templates and WAK/RES `NOT_SELECTED`
  decision packets, all with `physics_pass: false` where applicable.
- Synchronizes P3 as `0.0.2-outline`; the full paper trigger remains unmet.
- **Boundary:** no tier-1 UVIR closure, matched cutoff, MAT PASS, selected
  wake/reservoir route, derived observable, or full P3 manuscript.

#### [`12.0-alpha.12`](Manuscript/CoreRecovery/releases/v12.0-alpha.12/) - 2026-08-06

**Label:** Dual-status MAT interface and Tier-1 hold checkpoint. **Current freeze**

- Retains `HOLD_TIER1_CLOSURE`; UVIR-003 remains `IN_PROGRESS`.
- Records the Track-A Conditional matter channel and parent-matching incompleteness without promoting them to Derived matching.
- Keeps `V` `NOT_COMPUTED`, `K_Q` `NOT_DERIVED`, MAT-001 `BLOCKED`, and Stage 4A `CLOSED`.
- **Boundary:** no MAT/UVIR physics PASS, numeric residue, physical cutoff, downstream observable, or full cosmology follows.

### Current open boundary (after alpha.12)

These bounded results do **not** establish full perturbative stability,
observational viability, or a completed cosmology.

**Manuscript freeze voice (alpha.12, authoritative for citations):** UVIR-003
remains **in progress**; MAT-001 is **not unlocked**. Claim hygiene above is
unchanged.

**Programme / gate ledger (post–α.10 serial Stages 1–5 — not a manuscript
freeze):**

| Stage | Subgate / exit | Boundary |
|-------|----------------|----------|
| 1 | `PASS_DECLARED_WEAK_COUPLING_DOMAIN` | Evidence-package pass only; M2 remains partial because the relevant IR response is uncontrolled |
| 2a | `INCOMPLETE_R3_UV_RESIDUE` | No action-level \(Z_\psi r_\rho\) |
| 2b | `PASS_CONDITIONAL_MATCHING_FLOOR` | Conditional-with-scope floor; scoped MAT handoff text only |
| 2c | `PASS_STAGE2C_FLOOR_DIAGNOSTICS` | Causality/NDA under floor; Conditional only |
| 3 | `PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL` | **PARTIAL** provisional forms; \(V\) NOT_COMPUTED; no MAT PASS |
| 4 | `PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT` | Conditional record preserved; insufficient for tier-1 closure; reopen Stage 4A after matching |
| 5 | `PASS_STAGE5_DECISION_HOLD_TIER1` | Decision audit complete; physics gate **`IN_PROGRESS`**; M2/M3/M6/M7 block closure |

Still **not** claimed: Derived numeric \(K_Q\), computed \(V\), optical theorem,
matched physical cutoff, MAT PASS, or downstream Derived packaging.

**Next scientific actions (ordered):** (1) compute \(V\), or an equivalent
matched invariant, from one declared action/field chart; (2) reopen Stage 4A
for matched causality, relevant IR control, and a physical cutoff/unitarity
result; (3) run a later independent Stage 5 closure review; (4) complete MAT,
then DISK/STAT, before full P3/P4 claim packaging. Alpha.12 freezes this
honest checkpoint without upgrading those claims.

### Post-alpha.12 MAT Tier-1 R1-R5 remediation - 2026-08-07

The post-freeze evidence chain was scrutinized and repaired without changing any global gate:

- R1 corrects the ADM-to-J2 convention bridge to `B=-M_x^T`, `C_J2=-C_ADM` and retains the nonzero velocity-mixing obstruction.
- R2 replaces circular source-absence assertions with source-backed provenance and fail-closed mutation cases.
- R3 selects the covariant conformal matter action `S_m[Psi_m,A(psi)^2 g]` and derives exact lapse/shift variation. The Track-A `d=(-C_m)`, `h=(0,0)` result is only the normalized comoving linear limit; mixed lapse and moving-matter shift vertices remain.
- R4 carries the signed coupling through canonical normalization and mode projection: for the anchored `u_psi=+1` convention, `g_can=-C_m/sqrt(K_Q)=-V_signed`. Magnitude-only diagnostics cannot satisfy the matching contract.
- R5 proves the declared effective action leaves `C_m` and `K_Q` independent and therefore underdetermines `V`; normalization choices, `C_m=C_IR`, fixed `C_obs`, and the Conditional UVIR route-R5 anchor do not close matching.
- The consolidated 22-output runner executes available mutation suites and verifies every JSON/SHA-256 pair.

Scoped remediation passes do not supply microscopic `C_m`, numeric `K_Q`, a live normalized residue, a UV completion, lensing closure or a physical cutoff. R5 records `HOLD_DECLARED_ACTION_UNDERDETERMINES_V`; Tier-1 remains `NOT_MET`, MAT-001 remains `BLOCKED`, and Stage 4A remains `CLOSED`. See `Theory/Gates/MAT-001/MAT-001_R5_MICROSCOPIC_MATCHING_DECISION.md`, `Theory/Gates/MAT-001/MAT-001_R5_PATHWAY_SURVEY_2026-08-07.md`, and `Theory/Gates/MAT-001/MAT-001_TIER1_REMEDIATION_ADDENDUM_2026-08-07.md`.

### Post-alpha.11 MAT normalization preparation - 2026-08-05

Three post-freeze structural audits now make the matching target unambiguous:

- J1 derives the same-action identity
  \(V=C_m/\sqrt{K_Q}=g_\phi/\sqrt{Z_\phi}\) without supplying either
  microscopic coefficient.
- R2 distinguishes the canonical source vertex \(V\), the mixed response
  coefficient \(V/P\), and the source-source exchange coefficient
  proportional to \(V^2/P\).
- The unit-chart contract separates the covariant \(x^0=ct\) coefficient from
  the coordinate-time coefficient,
  \(K_Q^{(t)}=K_Q^{(x^0)}/c^2\), and rejects a universal extra \(c^{-2}\).

These are evidence-integrity and dimensional-contract passes only. Numerical
\(K_Q\) remains `NOT_DERIVED`, \(V\) remains `NOT_COMPUTED`, MAT-001 remains
`BLOCKED`, UVIR-003 remains `IN_PROGRESS`, and Stage 4A remains closed. See
`Theory/Gates/MAT-001/MAT-001_J1_JOINT_ACTION_NORMALIZATION.md`,
`MAT-001_R2_DIRECT_RESIDUE_AUDIT.md`, and
`MAT-001_UNIT_CHART_CONTRACT.md`. No frozen manuscript release is modified.

### Post-inventory free-sector same-chart export - 2026-08-06

After the live-export inventory blocker map, a free-sector export checkpoint
published original-chart free \(K\) and \(C\), decomposed the constraint source
exactly into field map \(M_x\) and velocity map \(M_v\), recorded the convention-correct static
J2 candidate \(B=-M_x^{T}\), \(C_{\rm J2}=-C_{\rm ADM}\), while retaining the nonzero \(M_v\) residual, and
transformed free \(K\) into the physical scalar chart.

This does **not** complete the live same-action bundle: matter covectors
\(d,h\) are still not exported, pure static J2 \(B\) is not ready, and mode
\(u\) is not selected. Subgate:
`PASS_MAT001_SAME_CHART_FREE_QUADRATIC_EXPORT_PARTIAL`. See
`Theory/Gates/MAT-001/MAT-001_SAME_CHART_FREE_QUADRATIC_EXPORT.md` and
`Theory/Gates/MAT-001/MAT-001_LIVE_UVIR_EXPORT_INVENTORY.md`.

### Declared \(S_{\rm int}\) and IR \(d,h\) form - 2026-08-06

A follow-on audit declares Conditional
\(S_{\rm int}\supset -C_m\rho_b\psi\), derives IR J2 covectors
\(d=(-C_m)\), \(h=\emptyset\) that recover signed \(g_{\rm can}=-V\) in the anchored field orientation, and proves the
live free-sector chart cannot host those covectors because it lacks the force
field \(\psi\). Live UVIR \(d,h\) remain `NOT_EXPORTED`. Subgate:
`PASS_MAT001_S_INT_DH_DECLARATION_LIVE_CHART_BLOCKED`. See
`Theory/Gates/MAT-001/MAT-001_S_INT_DH_DECLARATION.md`.

### Force-field hosting readiness - 2026-08-06

A five-route inventory shows no live host is ready for matter coupling:
free-sector ADM is not a force host; Track-A hosts \(\pi\) without \(S_{\rm int}\);
full ADM force completion remains blocked on \(\Delta_U\) and \(Y^{3/2}\).
Subgate: `PASS_MAT001_FORCE_HOSTING_READINESS_BLOCKED`. See
`Theory/Gates/MAT-001/MAT-001_FORCE_HOSTING_READINESS.md`.

### Track-A Conditional \(S_{\rm int}\) embed - 2026-08-06

Track-A is selected as the Conditional force host. With
\(\psi=\psi_{\rm bar}+\pi\), \(S_{\rm int}=-C_m\rho_b\psi\) is embedded and
matter-channel \(d=(-C_m)\), \(h=(0,0)\) are exported on that host. The signed relation
\(g_{\rm can}=-V\) recovers with symbolic \(K_Q\) only in the anchored orientation. Free-sector ADM is
not identified with Track-A. Subgate:
`PASS_MAT001_TRACK_A_S_INT_EMBED_DH_EXPORTED_CONDITIONAL`. See
`Theory/Gates/MAT-001/MAT-001_TRACK_A_S_INT_EMBED.md`.

### Track-A host \(K_Q\) readiness - 2026-08-06

Host time-kinetic \(K_Q\) is exported symbolically and the on-host \(V\) form
holds with rescaling covariance. Numeric \(K_Q\) remains `NOT_DERIVED`; the
Conditional dimensional estimate stays non-Derived. Subgate:
`PASS_MAT001_TRACK_A_KQ_SYMBOLIC_HOST_NUMERIC_BLOCKED`. See
`Theory/Gates/MAT-001/MAT-001_TRACK_A_KQ_READINESS.md`.

### \(K_Q\) dig and Conditional dual-status branch - 2026-08-06

Four numeric-\(K_Q\) derivation paths are incomplete. A dual-status Conditional
matching branch is open for labeled probes only; Derived \(V\) and \(K_Q\) stay
closed. Subgates: `PASS_MAT001_KQ_DERIVATION_DIG_INCOMPLETE`,
`PASS_MAT001_CONDITIONAL_MATCHING_BRANCH_OPEN_DUAL_STATUS`.

### Track-A join readiness - 2026-08-06

Matter-only static channel form-ready; free-force constraint J2 is
velocity-quadratic (not pure static \(B\)); full multi-sector J2 not assembled.
Subgate: `PASS_MAT001_TRACK_A_JOIN_READINESS_PARTIAL_MATTER_CHANNEL_ONLY`.

### Tier-1 peer-review readiness - 2026-08-06

Executable hold-retention audit after the Track-A Conditional MAT kit: Stage 5
`HOLD_TIER1_CLOSURE` retained; Stage 4A reopen contract all false; MAT dual-status
surface consistent; peer-review allow/deny ledger published. Subgate:
`PASS_TIER1_PEER_REVIEW_READINESS_HOLD_RETAINED`. See
`Theory/Gates/UVIR-003/UVIR-003_TIER1_PEER_REVIEW_READINESS.md`.

Authoritative process detail:
`Theory/Gates/UVIR-003/UVIR-003_SERIAL_STAGE_ORDER.md` and
`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_STAGE5_FULL_GATE_DECISION.md`.

## Parallel identity-gate checkpoint - 2026-08-04

TOP-001, VOR-001 and WAK-001 advanced as parallel Open/Conditional research
lanes. The detailed bounded record is
[`Theory/Gates/IDENTITY_GATE_CHECKPOINT_2026-08-04.md`](Theory/Gates/IDENTITY_GATE_CHECKPOINT_2026-08-04.md).

- TOP-001: the full-triaxial fixed-volume log-shape template passes nine
  geometry, covariance, refinement and firewall checks.
- VOR-001: the finite-density minimum and smooth integer-winding template pass
  after separating the exact discrete energy from continuum convergence.
- WAK-001: constrained variation, mode-counting, readiness,
  zero-background factorization and identity-inventory audits pass within
  their declared mathematical scope.

All three gates remain Open. No modulus action, parent condensate validation,
defect/resonance mechanism, microscopic wake identity, source, exchange
current or physical observable is derived. Alpha.11 integrates this status
boundary without promoting the underlying gates.

### Identity continuation (same day)

Further scaffold-only executables and decision records:

- TOP-001 S2 CBR bridge template (`physics_pass: false`)
- VOR-001 S2b toy parent-action template (`physics_pass: false`)
- WAK-001 C2 decision packet: `NOT_SELECTED`; C1/C2/C3 remain Open
- RES-001 R1 decision packet: `NOT_SELECTED`; R1/R2/R3 remain Open
- MAT-001 kinetic-chart blocker inventory: $V$ remains `NOT_COMPUTED`
- MAT-001 J1/R2/unit-chart preparation: structural identities and coefficient
  charts pass; microscopic matching remains open

See `Theory/Gates/IDENTITY_GATE_CHECKPOINT_2026-08-04.md` and
`Theory/Gates/RES-001/`.

## Repository rules for recovery work

1. Treat the claim migration ledger and gate reports as the status record.
2. Keep derived, conditional, open, and rejected claims visibly distinct.
3. Put ongoing manuscript edits in `ITSM_Core_working.tex` and `sections/`.
4. Never overwrite a versioned manuscript PDF or its source tree.
5. Freeze every manuscript version under
   `Manuscript/CoreRecovery/releases/v<version>/`.
6. Update the manuscript changelog and `VERSION` in the same commit as a new
   release.

The root `README.md` is now a recovery-native landing page. The root
`CHANGELOG.md` retains substantial legacy v11 history for provenance and must
not be read as the current v12 recovery claim set.
