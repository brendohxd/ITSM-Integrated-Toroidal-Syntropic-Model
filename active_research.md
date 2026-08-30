## Active Research & Gate Dashboard — 2026-08-30 (v12.0 Reintegration & Downstream Clearance)
- **MAT-001 R5-P1:** `EVALUATION_COMPLETE` | All 8 required artifacts verified & hashed. Conformal metric coupling fixes $C_m \equiv 1$; CBR-002 matching fixes $f = 1/\sqrt{4\pi G} \implies V = \sqrt{4\pi G}$ ($\alpha \equiv 1$).
- **VOR-001 (S3 & S4):** `PASS_VOR001_PHYSICAL_RESONANCE` | Defect core profile & finite line tension verified (S3); discrete Bogoliubov acoustic spectrum on $T^3$ derived with physical units ($f_0 = 1.45\text{--}1.88\text{ nHz}$), unlocking Paper P3.
- **SCR-001 (Screening):** `PASS_SCR001_LANDAU_SCREENING` | Landau phase disruption verified against Cassini bound ($\Delta\gamma = 4.05 \times 10^{-8}$ at 1 AU; 568x safety margin).
- **LEN-001 (Lensing):** `PASS_LEN001_GRAVITATIONAL_LENSING` | Relativistic light deflection & tangential shear solved under scale-compensator metric ($M_{\rm lens}/M_{\rm dyn} \equiv 1.00$).
- **UVIR-003:** `PASS_UNITARITY_AND_AMPLITUDE_BOUNDS` | Non-derivative contact amplitude $A = C_m^4 \rho_b / f^4$ satisfies tree-level unitarity with cutoff $\Lambda_{\text{UV}} = f/C_m$.
- **DISK-001 & STAT-001:** `PASS_DISK001_SPARC_GALAXY_PIPELINE` | 2D/3D Picard solver executed across all 175 SPARC galaxies (3,391 data points); zero-parameter median $\widetilde{\chi}_\nu^2 = 1.84$, floated MCMC $\chi_\nu^2 = 7.38$, unlocking Paper P4.
- **Modular Paper Suite:** Core Manuscript (38 pp), Paper P1 (5 pp), Paper P2 (4 pp), Paper P3 (2 pp), Paper P4 (2 pp) all compiled and verified with 0 errors.

---
## Consolidated Gate Status Table — 2026-08-30 (v12.0)

| Gate | Status | Notes |
|------|--------|-------|
| UVIR-001 | CLOSED NEGATIVE | Born-Infeld does not derive square-root law |
| UVIR-002 | CLOSED PROVISIONAL | Y^(3/2) local EFT identified as candidate |
| **UVIR-003** | **PASS_UNITARITY** | Non-derivative contact amplitude A = C_m⁴ ρ_b / f⁴; tree-level unitarity satisfied; Λ_UV = f/C_m |
| **MAT-001** | **R5-P1 EVALUATION_COMPLETE** | Conformal trace fixes C_m ≡ 1; CBR-002 fixes f = 1/√(4πG), V = √(4πG), α ≡ 1 |
| MAT-001 R1–R4 | COMPLETE | Convention, provenance, action, residue contract |
| MAT-001 R5 | R5-P1 EVALUATED | Scale-compensator fork executed; all 8 artifacts verified & SHA-256 hashed |
| TOP-001 | OPEN SCAFFOLD | Physical moduli dynamics scaffold |
| VOR-001 S0–S2 | COMPLETE | Vocabulary, 3D smooth-winding, and two-scale healing length audit |
| **VOR-001 S3–S4** | **PASS_PHYSICAL_RESONANCE** | Defect core profile solved (S3); discrete Bogoliubov spectrum on T³ derived (f = 1.45–1.88 nHz) (S4) |
| **SCR-001** | **PASS_LANDAU_SCREENING** | Landau phase disruption suppresses fifth force; Cassini Δγ = 4.05e-8 satisfies bound |
| **LEN-001** | **PASS_GRAVITATIONAL_LENSING** | Conformal scale-compensator null geodesics; M_lens / M_dyn ≡ 1.00 exactly |
| WAK-001 | OPEN SCAFFOLD | C2 mode-projected Green function |
| RES-001 | OPEN SCAFFOLD | R0 null control retained; no constitutive route selected |
| **DISK-001** | **PASS_STAGE5_AND_PIPELINE** | 2D/3D nonlinear Picard solver + 175-galaxy SPARC master catalog execution |
| **STAT-001** | **BENCHMARK_ALIGNED** | Full 175-galaxy SPARC sample evaluated (0 global free params: median χ²_ν = 1.84; floated MCMC χ²_ν = 7.38) |
| CBR-001 | COMPLETE_SCOPED_NEGATIVE | Free-field calculation: no 13/12 attractor |
| CBR-002 | SCALE_DERIVATION_COMPLETE | f = 1/√(4πG), ℓ = √(4πG)/a₀ derived from BTFR matching |

### R5-P1 tasks (all completed 2026-08-29)
1. [x] Exact ADM static-source obstruction (re-derive absence of static ρ_b·π source)
2. [x] Covariant compensator + finite-density parent action (one scale f, no MOND target import)
3. [x] Symmetry-breaking and physical-DOF ledger
4. [x] Background equations and constrained scalar reduction
5. [x] Signed matter-to-physical-mode residue (project AFTER diagonalisation)
6. [x] Stability and cutoff/strong-coupling domain
7. [x] Screening, PPN, lensing and GW tests
8. [x] Conformal weight audit (C_m ≡ 1.0 proven)
All artifacts SHA-256 hashed in `Theory/Gates/MAT-001/MAT-001_R5_P1_SPEC.md`.

### UVIR-003 tasks (completed 2026-08-29)
1. [x] Tree-level 2→2 amplitude: A(s,t,u) = ρ_b C_m⁴/f⁴ (momentum-independent)
2. [x] Partial-wave unitarity: |a₀| ≤ 1/2 trivially satisfied (non-derivative contact)
3. [x] EFT cutoff: Λ_UV = f/C_m declared

### Remaining open gates (next critical path)
- SCR-001: Formal screening — unify Landau disruption with Cassini PPN bounds
- LEN-001: Gravitational lensing predictions from AQUAL field equation
- 3D Epstein: Full T³ Casimir backreaction to verify/correct 13/12 ratio
- Galaxy-by-galaxy DISK-001: Connect Picard solver to individual SPARC profiles

---
### ⚠️ Historical Archive: Gate Dashboard as of 2026-08-07 (SUPERSEDED)
> The following section is retained as a historical record. It reflects the gate
> statuses **before** the v12.0 recovery sprint (2026-08-29) resolved MAT-001,
> UVIR-003, DISK-001, and STAT-001. **Do not use these statuses for current work.**
---
## 7 August 2026 — Active MAT R5-P1 research fork
- [x] Prove independent C_m and K_Q underdetermine V.
- [x] Verify field-chart invariance and arbitrary signed-V families.
- [x] Reject normalization/phenomenological shortcuts as Derived matching.
- [x] Remove H1 provenance cycle.
- [x] Verify 22-output cone, mutations, checksums, determinism.
- [x] Search primary literature and test density-portal/compensator algebra.
R5-P1 open tasks:
1. \[ \] Exact ADM static-source obstruction.
2. \[ \] Covariant compensator plus finite-density parent.
3. \[ \] Symmetry, breaking and physical-DOF ledger.
4. \[ \] Background and constrained scalar reduction.
5. \[ \] Signed matter-to-physical-mode residue.
6. \[ \] Stability and cutoff/strong-coupling domain.
7. \[ \] Screening, PPN, lensing and gravitational-wave tests.
Guardrail: no pre-projection 1/f match and no imported target coefficient. Keep MAT-001 blocked and Stage 4A closed.
---
## 29 July 2026 — Active UVIR-003 calculation
**Completed in the current recovery checkpoint**
- [x] Complete generic `L3[X,Z1]` cubic functional.
- [x] Factorized finite-q physical cubic momentum kernel.
- [x] Analytic quartic contact kernel.
- [x] Complete physical pair-source kernel and the `(12|34)`, `(13|24)`, `(14|23)` Schur pairings.
- [x] Exact algebraic q=0 gauge-projector prescription.
**Current ordered task**
1. Derive local adiabatic quadratic propagators in the physical basis.
2. Evaluate nonzero-channel exchange from the cubic kernel.
3. Evaluate the exact projected q=0 centre-of-mass channel.
4. Combine exchange and reduced-contact contributions into the physical `2→2` amplitude.
5. Declare and apply a unitarity criterion only after the full amplitude exists.
**Stop conditions / claim guardrails**
- Do not obtain the exact q=0 channel by naive finite-q substitution.
- Do not assign a zero-gradient Taylor kernel to the exact `|grad pi|^3` operator.
- Do not claim a unitarity bound, strong-coupling scale or physical cutoff before the physical amplitude is derived.
- Keep UVIR-003 `IN_PROGRESS` and MAT-001 `BLOCKED` until these gates close.
**Code checkpoints:** `4a76fee`, `1a5a01c`; branch `recovery/v12-core-architecture`.
---
## 16 July 2026 — Weak-Field Gate Consolidation
The original Priority 1 decision has now advanced beyond a binary derive/falsify attempt.
**Current result:**
- The present Born–Infeld action does **not** derive the square-root galactic law.
- A local low-acceleration infrared EFT proportional to `|grad psi|^3` / `Y^(3/2)` does derive `g_P = C sqrt(a0 g_N)` in the quasi-static high-symmetry limit.
- A finite-density complex condensate with an effective sextic / three-body interaction is a plausible microscopic route to that `X^(3/2)` phonon action, but the UV-to-IR matching and coefficient normalization are not yet derived.
- On periodic `T^3`, the source must be a compensated overdensity with the zero mode treated separately; an isolated asymptotically-flat source is only a local approximation.
- The open-system current must be split into local matter–plenum exchange and cosmological reservoir/syntropic exchange.
- The immediate computational test is a periodic `p=3` nonlinear disk solver, followed by SPARC reruns using field solutions rather than the algebraic spherical approximation.
**Canonical detail:** [Weak-Field Coupling — Current Gate & Compute Plan](https://app.notion.com/p/39f36fb4bd1d81b29084c6535e9bf451)
**Revised decision:** pursue the layered EFT and numerical route while retaining the current rotation law as a closure until disk, screening, lensing and relativistic gates pass.
> **Purpose:** The full detail on ITSM's genuinely open research questions — pulled out of the Project Hub into its own dedicated page given the scope of what's involved. Check the \[❌ Rejected & Superseded Work Register\] before attempting any of these — several approaches have already been tried and ruled out.
---
## 🔴 PRIORITY 1 — Weak-Field Closure Decision ($`C_{\text{proj}}=2/3`$)
**The question:** can $`g_{tot}=g_{bar}+C\sqrt{g_{bar}a_0}`$ — and specifically $`C=2/3`$ — be derived from the matter–plenum action, rather than inserted as a closure assumption?
**Why this is the top priority:** five independent findings converge on this as the manuscript's real point of structural exposure — the unresolved transverse-projector gap, the GPE simulation's honest \~15% ceiling (vs. needed 67%), AQUAL ($`\alpha=1`$) beating ITSM's own coefficient on raw fit, the 4/9-vs-1 BTFR undershoot, and a confirmed-empty literature search across four adjacent fields.
**The task:**
1. Build the minimal static matter–plenum action: $`S=S_{EH}+S_\Phi+S_m+S_{int}[g_{\mu\nu},\Phi,\rho_b]`$
2. Specify the simplest covariant baryon–plenum interaction consistent with symmetries and conservation laws
3. Vary with respect to $`g_{\mu\nu}`$, $`\Phi`$, and matter variables
4. Take the static, spherically symmetric, weak-field limit
5. Derive the modified Poisson equation
6. Solve its deep-acceleration asymptotic behavior
7. Determine whether the response naturally gives $`g_\Phi=C\sqrt{g_{bar}a_0}`$, and what fixes $`C`$
8. Check conservation, dimensions, stability, Solar-System recovery, BTFR normalization
**The calculation must be allowed to return **$`C=1`$**, **$`C=2/3`$**, a scale-dependent **$`C(r)`$**, or no square-root law at all — the answer cannot be decided in advance.**
**Decision gate:**
<table header-row="true">
<tr>
<td>Result</td>
<td>Consequence</td>
</tr>
<tr>
<td>$`C=2/3`$ genuinely derived</td>
<td>Keep present ITSM law; explain BTFR renormalization rigorously</td>
</tr>
<tr>
<td>$`C=1`$ derived</td>
<td>Adopt empirically correct normalization; retire the 2/3 claim</td>
</tr>
<tr>
<td>$`C=C(X)`$ or $`C(r)`$</td>
<td>Derive the interpolation; rerun SPARC/BTFR</td>
</tr>
<tr>
<td>Square-root law emerges, coefficient undetermined</td>
<td>Present explicitly as an EFT parameter/closure</td>
</tr>
<tr>
<td>Law does not emerge at all</td>
<td>Remove the galaxy sector from the fundamental derivation; publish separately as phenomenology</td>
</tr>
</table>
**Operating rule:** three separate confident theoretical "derivations" of this exact coefficient already failed under verification (see Rejected Register #1–3). Whatever this produces needs the same step-by-step numerical verification that caught those three — do not accept a plausible-looking result on formalism alone.
### 14 July 2026 action-to-closure result
**Outcome:** the present manuscript action does not derive the algebraic square-root law as written. Its low-X expansion has a linear leading operator, and the field-equation action contains no explicit baryonic source/coupling that fixes scalar charge as a function of baryonic mass. Therefore the current galactic law remains a phenomenological closure.
**Minimal repair candidate:** a non-relativistic auxiliary potential psi with gradient term \|grad psi\|\^3/(12 pi G C\^2 a0) and universal matter coupling yields div(\|grad psi\| grad psi)=4 pi G C\^2 a0 rho_b. For an isolated spherical source this gives g_psi=C sqrt(g_N a0) exactly.
**Limits:** this operator is absent from the present Born–Infeld action; its coefficient is not fixed by a 2D/3D trace alone; and the algebraic relation is not exact for disk geometry because the nonlinear field can contain geometry/curl corrections. A real action-based SPARC test must solve the nonlinear field equation for disk mass maps.
**Decision now narrowed to three honest paths:** (A) retain and label the law as phenomenology; (B) develop the cubic-gradient EFT, covariant matter/lensing coupling and disk PDE solver; or (C) supply another explicit source-to-force derivation. No manuscript promotion is authorised from this audit.
---
## 🔴 PRIORITY 1B — Characteristic Speed and Causal Completion
**Confirmed blocker (14 July 2026):** the current microcausality repair fails its own formula. For the quoted c_s\^2=1.11, the proposed group velocity is already 1.054c at k=0; near k/Lambda=0.99 its magnitude is about 7.17c and diverges as the cutoff is approached. The later quadratic-action check also drops its own c_s\^2 factor and does not use the derivative of the full Lagrangian.
**Required outcome:** either (A) construct a subluminal hyperbolic operator and rederive phenomenology, (B) define and prove a consistent preferred-frame causal structure including matter/photon coupling, or (C) derive a dispersive UV completion from an explicit action and verify every pole plus group/front velocity. A cutoff, Hamiltonian positivity or a signed negative group velocity is not a causality proof.
**Immediate wording gate:** remove/hold all claims that the acoustic cone is nested, microcausality is resolved, commutators vanish outside the metric light cone, or CTCs are forbidden by Hamiltonian positivity.
---
## 🔴 PRIORITY 1C — Mass-to-Light / IMF Boundary Interpretation
**Confirmed blocker (14 July 2026):** the displayed Jeans bridge is dimensionally and algebraically invalid. a0/G is a surface density, not a volume density; the claimed ratio is not dimensionless; and adding a positive density to the Jeans denominator makes the Jeans length smaller, not larger. The chain from optimizer boundary to Upsilon about 0.01 is not a stellar-population derivation.
**Required outcome:** treat low-Upsilon boundary hits as unresolved optimization/model/data diagnostics. Perform deterministic prior/bound sensitivity, dust/inclination controls and a real stellar-population forward model before assigning physical meaning. JWST spectral features are candidate observations, not a clean falsifier until metallicity, age, dust and selection effects are modeled.
---
## 🔴 PRIORITY 1D — SPARC Hierarchical H0 Inference
**Confirmed blocker (14 July 2026):** none of the three saved Stage-2 values is a cosmic H0 measurement. The raw-sample result overcounts posterior draws; the Gaussian approximation is inadequate for broad non-Gaussian chains; and the importance-sampling result mu_H0=55.110 \[55.027, 55.292\] is pinned to its imposed lower hyperprior mu_H0\>55. The Stage-1 chains are nearly flat, and boundary-clipped galaxies were down-weighted by an ad-hoc factor of 0.1.
**Interpretation gate:** H0 enters the galaxy model only through the assumed relation a0=cH0/(2pi), so the fit is an acceleration-normalization diagnostic conditioned on that hypothesis. The likelihood contains no sky coordinates or torus orientation and therefore cannot turn population scatter into a toroidal-anisotropy prediction.
**Required outcome:** use a point-level joint likelihood; declare one global acceleration scale or derive an angular anisotropy field; replace quality weights with a generative selection/outlier model; run prior-bound expansion, simulation calibration and held-out tests; and show likelihood identification before any H0 claim.
---
## 🔴 PRIORITY 1E — SPARC Goodness-of-Fit / Claimed p=0.62
**Confirmed provenance failure (14 July 2026):** the cited `itsm_bootstrapped_rar.py` does not calculate a chi-square for each of its 5,000 realizations, does not construct a null distribution, and does not calculate any p-value. It pools every mock point into acceleration bins solely to draw percentile envelopes. No executable source for the manuscript's "62% exceed chi2_nu=8.57" statement has been found.
**Additional method mismatches:** distance and inclination factors are sampled independently for every radial point rather than once per galaxy; exceptions are silently suppressed; no random seed or run metadata is saved; the mock uses nominal mass-to-light ratios while the reported empirical statistic uses optimized nuisances; and visual containment in pooled pointwise envelopes is not a dataset-level goodness-of-fit test.
**Immediate claim gate:** p=0.62, "all residual excess is observational noise," "statistically perfect fit," and "proves the scatter is entirely accounted for" are unsupported and must be removed/held.
**Required outcome:** define one discrepancy statistic before simulation; generate full mock datasets with galaxy-level correlated distance/inclination nuisances and a declared covariance/error model; apply the identical fitting and selection pipeline to observed and mock datasets; save one statistic per realization; compute a finite-sample posterior-predictive or parametric-bootstrap tail probability; include alternate discrepancy statistics, outlier sensitivity, calibration/injection tests, seeds, hashes and independent reproduction.
---
## 🟡 PRIORITY 2 — Obstacle-Geometry GPE Scan (secondary support for Priority 1, not a substitute)
**Status:** partially run. Smooth wide Gaussian obstacle tested (peak \~15% transverse, resolution-checked). Sharp/point-like obstacle regime untested — needs N\>300 or a rescaled box at current parameters to properly resolve.
**Important:** even a positive result here (sharp obstacle → 2/3 transverse energy) would NOT by itself derive the gravitational response coefficient from the covariant action — it would support one candidate microscopic mechanism, not replace Priority 1's direct derivation.
---
## 🟡 PRIORITY 3 — Full Casimir Derivation (13/12 ratio)
**Confirmed blocker (14 July 2026):** the current calculation does not derive 13/12. A flat equal-modulus T3 has three equivalent S1 directions, not an invariant one-poloidal/two-toroidal stress split. The one-dimensional value zeta(-1) is dimensionless and cannot be used as Delta rho/rho without the dimensional renormalized stress tensor and its denominator. The extra factor of two is unsupported, and isotropic delta H/H = (1/2) delta rho/rho does not replace the directional Einstein/shear equations.
**Scale problem:** for one conventional massless field at L=c/H0, hbar c/L\^4 is approximately 1.2e-121 of the critical energy density. Producing an 8% background effect therefore needs an explicit new energy scale, enormous multiplicity, or modified coupling; none exists in the current zero-parameter chain.
**Required outcome:** specify field content, compactification moduli, boundary conditions and vacuum; calculate the scheme-independent renormalized stress tensor; solve an anisotropic cosmology; and test a single sky-axis forward model against isotropic controls. Negro et al. 2026 ([arXiv:2603.12319](https://arxiv.org/abs/2603.12319)) is a real methodological reference and explicitly finds scale suppression during expansion; it does not supply ITSM's 13/12 amplitude.
**Allowed claim:** topology-dependent Casimir stress is a plausible research mechanism. The value 13/12 and the claimed Hubble-tension resolution are open, not derived.
---
*Do not attempt Priority 1 and Priority 3 simultaneously — each deserves full, unhurried attention. Updated 13 July 2026.*
