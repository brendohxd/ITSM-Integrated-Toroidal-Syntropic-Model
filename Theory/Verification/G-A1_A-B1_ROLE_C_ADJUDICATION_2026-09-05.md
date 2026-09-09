# G-A1 / A-B1 Role-C adjudication

**Date:** 2026-09-05  
**Branch:** `recovery/v12-core-architecture`  
**Role:** Codex Role C — claim hygiene and canonical gate reconciliation  
**Status:** `ADJUDICATED_WITH_CORRECTIONS`  
**Gate effect:** none  
**Commit/push/publication:** not performed

## 1. Decision

The two returned external packages are useful, but neither is accepted verbatim.

- Grok `G-A1` independently reproduces the bounded RCP-C0 condensate-portal
  mechanism and correctly finds a free source normalization and a
  Yukawa/inverse-square force rather than a MOND-like acceleration law. Several
  normalization, domain and interpretation statements require correction.
- Antigravity `A-B1` reproduces the science-bearing P2 CSV/PNG outputs and the
  transient-crossing classification in an isolated output root. Its raw JSON
  files are not byte-deterministic because they serialize absolute output
  paths. The audit harness also contains hard-coded comparison booleans and
  incomplete negative controls. The allowed classification is therefore
  `NUMERICAL_REPRODUCTION_WITH_LISTED_BOUNDED_DISCREPANCIES`, not an
  independent Tier-1 validation.
- Grok began `G-A2` after the sealed `G-A1` instruction said to stop. That
  response is quarantined as unsolicited and was not used in this decision.

No result changes the canonical boundary:

- `MAT-001 BLOCKED`;
- `UVIR-003 IN_PROGRESS`;
- `K_Q NOT_DERIVED`;
- `V NOT_COMPUTED`;
- `TOP-001 / CBR-002 SCOPED_NEGATIVE_FREE_DILUTION`.

## 2. Sealed intake and provenance

Raw external responses remain in their private local session stores. They are
not copied into the repository and are treated as untrusted findings.

| Item | Identifier / SHA-256 | Disposition |
|---|---|---|
| Sealed Grok handoff | `613f31708d930497a679ff89c6be6444675f2ab1f2a5319955db432129661014` | Current file matches sealed manifest |
| Grok session | `01a0717e-d260-7c83-9b83-653566add10a` | Private local provenance |
| Exact `G-A1` response, 34,071 characters | `2d42ff7a0125f74a1e96d70561bbf84cb753f3d81f3e9a9147346927dcdcb184` | Reviewed |
| Full Grok JSONL after later activity | `cd4bdd915ee83d1f7f41784be6f7b8fc07800454d902e1cc3b74c202f54263e2` | Container hash only; includes unsolicited `G-A2` |
| Unsolicited `G-A2` response | `a28debd933ae403cfdd2aea629f3bf72fc2f51f43f16940a3ceae5012f9e067f` | Quarantined, not adjudicated |
| Sealed Antigravity handoff | `cd6d76249a34dab76edd26f844f610c184597ff4843f66bf6144d78d567f5c4a` | Current file matches sealed manifest |
| Antigravity session | `1b0d390d-899b-4bba-bbc7-7cfb1588faa3` | Private local provenance |
| Final audit harness | `1af95c0607b4d93f5b195c20e706ef2caf08528f89c93306c845c5d867e88726` | Reviewed as code, not canonicalized |
| Final successful log | `998666cdbe2fa725f80488ee4eb2353fea509e5795b942c009719f02e5f248f7` | Exit code zero |
| Final manifest | `3062af8d09e2b4a267684a0c403a9ced0655d65f6b50a8a73e1f6ebf21e486a5` | Reviewed with limitations below |

### 2.1 Failed Antigravity attempts retained in provenance

The successful run was preceded by three material harness failures:

| Log | SHA-256 | Exact failure class |
|---|---|---|
| `task-129.log` | `56d68f7cf60b5336705e727247e185629b77b38ce9074478cee451848161825c` | `AttributeError`: string passed where a resolved path object was required |
| `task-219.log` | `cc82ac3e0853173d70e5d680000c93e7fd78f2622eb3339a7724a6079b65deac` | `IndexError`: threshold row key lookup returned no row |
| `task-300.log` | `4118a27b4b91492ee38e9b62c8020efcec7ab743430ccebdc5be319ed2fa1885` | `TypeError`: NumPy boolean was not JSON serializable |

These are development failures, not failed physics tests, but omitting them
would make the execution record falsely appear one-shot.

## 3. Claim-by-claim reconciliation

| Claim/equation | Grok Role A | Antigravity Role B | Canonical Codex check | Disposition |
|---|---|---|---|---|
| RCP-C0 background is `mu^2=m^2+lambda_4 v^2`, `n=2 mu v^2` | Derived | Not in A-B1 scope | Direct expansion and Noether current agree | Confirmed within fixed-background comparator |
| Complete scalar kernel has amplitude-phase kinetic mixing | Derived | Not in scope | Canonical fields `sigma=sqrt(2)h`, `q=sqrt(2)v pi` give mixing `2 mu sigma q_dot` | Confirmed |
| Exact branches have one gapless mode and gap `2 lambda_4 v^2+4 mu^2` | Derived | Not in scope | Symbolic root sum/product and both `k=0` limits pass | Confirmed |
| Static response is Yukawa with `ell=(2 lambda_4 v^2)^(-1/2)` | Derived | Not in scope | Direct static Euler-Lagrange equation agrees with primary source | Confirmed; `ell approximately (2mc_s)^(-1)` is NR only |
| Source strength is fixed by the parent | Found `g_C0=sqrt(2)v/Lambda^2` but free | Not in scope | Canonical chart gives the same coefficient; `v/Lambda^2` remains unmatched | Confirmed free normalization, not an ITSM prediction |
| Displayed action implies the review's quoted force coefficient | Grok detected an overall factor two | Not in scope | Canonical exchange gives `g_C0^2/(4pi)=v^2/(2pi Lambda^4)` while the review prints `v^2/(4pi Lambda^4)` | Unresolved source-to-probe normalization; do not inherit either coefficient as ITSM |
| The portal yields a MOND-like force | Rejected | Not in scope | Kernel is `(k^2+M_sigma^2)^(-1)` and gives Yukawa/inverse-square behavior | Contradicted as a standalone MOND route |
| `P(X)` and GP reductions are interchangeable at all momenta | Domain-limited | Not in scope | `P(X)` drops radial gradients; GP retains `k^4/(4m^2)` and extends to `k << m` | Confirmed only with separate domains |
| Uniform-sphere charge is `M_eff/M=3(x-tanh x)/x^3` | Derived | Not in scope | Direct limits give `1` for `x->0` and screening for `x->infinity` | Confirmed for C0, `lambda_4=0`, `J=+rho` |
| Weak distortion is `rho R/Lambda^2<1` | Stated | Not in scope | `x=R sqrt(rho)/Lambda`, so `x^2=rho R^2/Lambda^2` | Contradicted; missing factor of `R` and dimensionally invalid |
| Attractive strong-source sign remains healthy | Rejected | Not in scope | The quoted local dispersion has negative `omega^2` below `sqrt(rho)/Lambda` for `J=-rho` | Scoped no-go for that strong C0 branch |
| RCP-I1-C directly couples conformal Maxwell photons | Wording ambiguous | Not in scope | Four-dimensional Maxwell theory is classically conformally invariant and traceless; lensing requires the metric solution | Contradicted as a direct classical trace vertex; lensing unresolved |
| RCP-I1-C computes a physical ITSM residue | Rejected/incomplete | Not in scope | Variation gives a fixed-background dust coefficient `alpha_1 rho_0`, but `A`, `alpha_1`, matter susceptibility and metric constraints remain open | Unresolved physical residue; useful scalar control only |
| P2 rerun is perfectly byte-deterministic | Not in G-A1 scope | Manifest says `false` | Every CSV/PNG is identical; Stage-3/3B JSON differs only in serialized `run1` versus `run2` absolute paths | Raw false; scientific payload path-normalized deterministic |
| P2 threshold cases form a `13/12` attractor | Not in scope | Independent classifier finds transient crossings only | `r0=1.10..3.00` dwell `0.27..0.30`; all return to unity; no quasi-plateau | Contradicted within implemented scan/closure |
| P2 cube value is stable to extrapolation choice at eight decimals | Not in scope | Order/window results differ | Order 1: `-0.8373740585`; order 2: `-0.8375358930`; order 3: `-0.8375369173`; order-2 extended window: `-0.8375362689` | Eight printed decimals not robust to declared extrapolation choice |
| P2 manuscript hashes freeze the fresh calculation | Not in scope | Three prefixes match fresh rerun; Stage-3B JSON does not | Current tracked outputs match none of the four ledger hashes; fresh Stage-3B JSON is also path-dependent | Contradicted; release blocker remains |

## 4. Grok G-A1 corrections

The following corrections are mandatory if the external derivation is reused:

1. Replace its equation E41 with
   `rho R^2/Lambda^2<1`; the written `rho R/Lambda^2` is not dimensionless.
2. Keep `ell=(2 lambda_4 v^2)^(-1/2)` exact for RCP-C0, but label
   `ell approximately 1/(2mc_s)` as a nonrelativistic relation.
3. Do not call the static finite-`lambda_4` response a pure Goldstone
   propagator. At `omega=0` the phase response vanishes for nonzero `k`; the
   amplitude Green function is Yukawa. Dynamical poles are mixed.
4. Preserve the action-normalized factor-two discrepancy with the published
   force formula. A numerical convention for a probe source cannot be guessed.
5. For RCP-I1-C use exactly `g_tilde=A^2(s/M_*^2)g`. A pure conformal Maxwell
   action has no classical trace source; photon deflection cannot be asserted
   before the coupled metric potentials are solved.
6. The fixed-background scalar overlap is not the final ITSM residue. Lapse,
   shift, scalar metric constraints and a declared on-shell gravitating
   background remain required.

Primary checks used:

- <https://arxiv.org/abs/1812.09332>;
- <https://arxiv.org/abs/2505.23900>;
- <https://doi.org/10.1103/PhysRevD.99.076003>.

## 5. Antigravity A-B1 bounded result

### 5.1 What reproduced

- Python `3.13.9`, NumPy `2.4.6`, using the `itsm_env` interpreter.
- Stages 1, 2, 3 and 3B exited zero twice.
- All CSV and PNG artifacts were byte-identical between isolated runs.
- Stage-3 and Stage-3B JSON scientific content was identical; the only diff
  was the absolute `run1`/`run2` path strings inside each `outputs` object.
- Independent classification code agreed with the canonical labels for the
  generated trajectories.
- Solver variation at `r0=1.5` retained `TRANSIENT_CROSSING`: loose/standard
  `max q=1.08333334`, dwell `0.29000`; tight `max q=1.08334213`, dwell
  `0.29500`.
- Permutation residuals were `1.051e-15` and `1.315e-15`.
- A one-byte mutation changed the checksum as expected.

### 5.2 What the harness did not establish

1. The test labelled “permutation / reflection” implements permutations only;
   no reflection is evaluated.
2. Multiple manuscript `match` fields are literal `True` values rather than
   computed comparisons. Only the final checksum-prefix matches are actually
   evaluated.
3. `resolution_invariance` is written as literal `True` in the manifest;
   there is no declared tolerance assertion converting the printed solver
   differences into that boolean.
4. The altered initial-condition set was created during the audit and is
   exploratory, not preregistered.
5. The run comparison iterates over run-1 keys only and therefore would not
   detect an extra run-2 artifact.
6. Full stdout/stderr for each stage is held in memory but is not saved as a
   complete per-stage evidence set.
7. The harness hashes four scripts, not all documentation, schemas and inputs
   used to interpret them.
8. Its “independent classifier” receives trajectories produced by the same
   canonical integration machinery; only classification logic is independent.
9. Synthetic plateau/attractor cases validate labels, not a physical
   attractor solution.
10. The current tracked artifacts differ from the fresh outputs:

| Artifact | Current repository SHA-256 prefix | Fresh A-B1 prefix |
|---|---:|---:|
| `cbr001_stage1.csv` | `57847F382BAF` | `9E6874226FAA` |
| `cbr001_stage2_scan.csv` | `FE648629545F` | `9257F3A67CB5` |
| `cbr001_stage3b_thresholds.csv` | `94B0AE4C6381` | `370B02480FF0` |
| `cbr001_stage3b_summary.json` | `0DE8ED5C2134` | `4252533BA1E7` |

The final row also disagrees with the manuscript prefix `4AD9223CE32C`.

## 6. Gate and workflow decision

`G-A1` can inform the independent Max derivation only after applying section 4.
`A-B1` strengthens the existing P2 bounded negative result and proves that the
tracked evidence package is stale/nonportable; it does not make the current P2
draft release-ready.

The next authorized calculation remains the Codex-owned bounded RCP-C0 and
RCP-I1-C fixed-background reduction. Full amplitude-phase-metric constraint
elimination, physical pole residue, PPN and lensing remain Ultra tasks and are
not performed in this adjudication.
