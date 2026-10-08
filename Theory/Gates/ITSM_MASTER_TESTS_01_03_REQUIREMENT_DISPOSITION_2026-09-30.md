# Master Tests 1–3: requirement-level, fail-closed disposition

Date: 2026-09-30. Branch: `recovery/v12-core-architecture`.
Authority: [master test programme](../Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md),
not a new parent action or gate decision. This record assesses the evidence
available now against the **full** Test 1–3 requirements. It does not turn a
local script `PASS` into a physics pass, call a conditional candidate
canonical, complete an independently blind coefficient derivation, or
claim publication readiness. `review_status=DEFERRED`,
`Rule9_cleared=false`, `physics_pass=false`, `gate_effect=NONE`.

## Requirement-by-requirement decision

| Programme requirement | Evidence that is actually established | Disposition and missing condition |
|---|---|---|
| **1: Complete off-shell action and action-derived sector currents.** | The canonical [Test-1 entry contract](ITSM_MASTER_TEST_01_SOURCE_VECTOR_CLOSURE_CONTRACT_2026-09-24.md) records missing complete reservoir/interaction action in the v12 parent. The separately frozen [R4C1-v1](RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md) is a complete *classical, reversible candidate* with dust and a real reservoir field. Its [full variation/Ward ledger](RES-001/RES001_R4C1_FULL_VARIATION_REPORT_2026-09-25.md) derives, in its declared stress split, `Q_mp^nu=beta T_m grad^nu psi` and `Q_syn^nu=-g_r (u^2+v^2) r grad^nu r/2`; the three on-shell sector identities sum to zero. Its U(1) charge source remains separate. | `CONDITIONAL` candidate-level classical closure; **canonical Test 1 `HOLD_SUBSTANTIVE`**. R4C1 does not derive an irreversible reservoir, a nonzero condensate-number source, Standard-Model/BBN matter, or canonical adoption. Its named reservoir exchange changes under an allowed interaction-stress reassignment, so the fixed split must travel with any use. |
| **1: Finite currents, physical domain and uncoupled GR control.** | The R4C1 first/full variation checks cover regular current zero-coupling controls on the declared smooth timelike chart. [G1](RES-001/RES001_R4C1_GR_LIMIT_REPORT_2026-09-25.md) rejects `zero exchange => GR` for B1 (`G_cos/G_static=5/6`) and finds vanishing transverse kinetic coefficient along its registered Einstein-dust approach. [G2](RES-001/RES001_R4C1_GR_EQUALITY_SCALAR_KINETIC_OBSTRUCTION_2026-09-30.md) excludes repairing equal Newton couplings inside the `alpha_13=0`, positive-transverse/regular-S1-no-ghost subfamily. | The algebraic Einstein-dust endpoint is not a demonstrated **healthy continuous** GR limit. G2 is a conditional necessary-condition obstruction, not an all-action or all-parameter no-go. A viable, constraint-regular, stable GR-connected domain or a different frozen action is still required, together with all-sector/EFT checks. |
| **2: Metric, Euler and controlled periodic weak-field law.** | A conditional spherical, regulator-subleading reduction gives an `a_dyn` dependent on free action coefficient `A`, not the programme's full matter-frame law. The [T3 addendum](ITSM_TEST_02_T3_TOPOLOGY_ADDENDUM_2026-09-25.md) rejects a universal *pointwise* gradient assignment by a nonzero-curl counterexample. The finite-`b` [weak-source report](RES-001/RES001_R4C1_WEAK_SOURCE_REPORT_2026-09-29.md) and complete fixed-mode [coupled linear report](RES-001/RES001_R4C1_COUPLED_LINEAR_LIMIT_REPORT_2026-09-29.md) reject a fixed positive square-root term as the arbitrarily weak-source asymptote in their stated R4C1 reductions. | The universal pointwise shortcut and a square-root derivation from those linear/weak-source branches are `REJECTED` **within their tested scopes**. Canonical Test 2 remains `HOLD_SUBSTANTIVE`: no coupled nonlinear periodic metric/frame/dust/Euler solution, controlled quasistatic remainder, common physical EFT window or independently derived `C_proj=2/3`. The displayed law must remain a conditional/empirical EFT ansatz, not a Derived ITSM prediction. A different nonlinear regime or action is not excluded. |
| **3: Historical chain, blind `C_chi` and `a0(z)`.** | The [early](ITSM_TEST_03_EARLY_COEFFICIENT_LINEAGE_AUDIT_2026-09-30.md), [later](ITSM_TEST_03_LATER_LINEAGE_AND_V12_GAP_AUDIT_2026-09-30.md), [original-PDF](ITSM_TEST_03_ORIGINAL_PDF_CIRCULATION_CROSSCHECK_2026-09-30.md) and [dimensional-repair](ITSM_TEST_03_DIMENSIONAL_REPAIR_DISPOSITION_2026-09-30.md) audits expose historical assignments, inconsistent multiplier/divisor and speed/acceleration steps, and a v12 gap equality missing a `2*pi` factor as printed. They do not authenticate every historical equation. The [R4C1-C1](RES-001/RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_REPORT_2026-09-25.md) action test holds the homogeneous/linear data and topology fixed while varying `A`, changing the conditional nonlinear force scale. | Historical claims of a *derived* `1/(2*pi)` from those inspected chains are `REJECTED`; the physical coefficient is `NOT_DERIVED`. Canonical Test 3 is `HOLD_SUBSTANTIVE`, not a completed blind audit. The analyst knows the historical target; no target-free unique `C_chi`, matter-frame `a0(z)`, Test-4 projection, independently blind derivation, or subsequent held-out SPARC/bTFR/lensing comparison exists. Assigning `A` to hit a comparator is not a prediction. |

## Evidence integrity and limits of this check

On this date, read-only `itsm_context.py receipt` checks found matching
sidecars and zero failed/unknown **local** checks in four decisive receipts:
R4C1 full variation `a91ad85caa748b77b888f69aede80c2dce5322dcdef4f1b77cf61f5a93a4e156`
(162/162), G1 `9b55e0a54dfaef0e1e44eca62ee765b89a53a399f84e8c3b3ffa371edfd079a8`
(56/56), coupled T2P3 `28a76334ca9af87658ccf4c8a3b8a18174b706a7bc327d08eaa3f5a84f2e1596`
(34/34), and C1 `49b10df599d6158f02ae6e55febe054f5b6fe2e3a2b53ee70daf7196f44d2fcf`
(63/63). Separately recomputing every declared direct/transitive dependency
in these four receipts checked **39 entries, zero missing or mismatched**;
entries may repeat paths. Neither count proves the full mathematics, all
configuration coverage, independent review, or physical admissibility.

## Stop conditions and next discriminating calculation

Canonical downstream promotion is blocked by **substantive physics**, not
Rule 9 alone. The next Test-1 action decision is to test a separately frozen
candidate GR-connected route outside G2's excluded subfamily (or supply a
different complete parent), including the tensor/frame/scalar constraint
domain, an on-shell finite-charge background beyond the existing bounded B1
control, characteristic/energy estimates and EFT
scale. The algebraic `alpha_13!=0` example in G2 only shows that G2 is not
an all-parameter theorem; it is **not** a viable parent. If no admissible
parent emerges, keep R4C1 conditional and reject it for canonical use rather
than borrowing its fitted force law. Only after a parent/domain survives
should Test 2 seek an error-controlled coupled nonlinear periodic solution
and Test 4's projection. Only then can Test 3 freeze a target-independent
coefficient/background prediction for an independent blinded audit and
held-out comparison.

Until those conditions are met: `canonical_Test1_pass=false`,
`canonical_Test2_pass=false`, `canonical_Test3_pass=false`,
`C_chi=NOT_DERIVED`, `a0(z)=NOT_PREDICTED`,
`MAT-001=BLOCKED`, `UVIR-003=IN_PROGRESS`, `K_Q=NOT_DERIVED`,
`V=NOT_COMPUTED`, `Stage4A=CLOSED`. TOP-X4 and its own gate are unchanged.
This is a requirement-level disposition of the *current evidence*, not a
claim that the full Tests 1–3 research objective has been achieved.
