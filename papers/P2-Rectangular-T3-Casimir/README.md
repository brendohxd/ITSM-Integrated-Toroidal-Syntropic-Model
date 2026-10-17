# P2 — Anisotropic Casimir on rectangular $T^3$ (instantaneous-closure control)

**Directory:** `papers/P2-Rectangular-T3-Casimir/`  
**VERSION:** see `VERSION` (currently `0.2.0-rc4`)
**Current PDF candidate:** `Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Instantaneous-Closure-Control_v0.2.0-rc4.pdf`
(written directly by the build script with a matching `.sha256` sidecar; see
`papers/PAPERS_NAMING.md`)

**Status:** Local release candidate for external review; `NO_GO_CURRENT_CANDIDATE` remains the physics result
**Branch:** `recovery/v12-core-architecture`  
**Science source:** `Analysis/Casimir/CBR-001/` (Stages 1–3B)  
**Claim firewall:** `papers/Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md`  
**Master plan:** `Theory/Core/ITSM_Master_Research_Plan.md`

## v0.2.0-rc2 editorial revision

- Places the analytic persistence condition before the finite-domain scan, so
  the numerical experiment follows directly from the required-stress result.
- Replaces the standalone historical-defence section with one neutral null-target
  statement in the introduction.
- Expands the conclusion to identify the bounded closure-level exclusion and
  the independently derived driven/memory-stress test required next (CBR-002).
- Preserves the 18/19 sensitivity result, publication hold, and all scientific
  scope limitations; no numerical receipt or physics classification was altered.

## v0.2.0-rc3 release-preparation revision

This candidate freezes the corrected manuscript date and packages the already
recorded negative result without changing equations, thresholds, classifications,
or receipts. The preregistered sensitivity suite remains `FAIL` at 18/19: one
threshold-amplitude stability check exceeded its deliberately stringent bound,
while all bounded no-attractor classifications remained unchanged.

The local preparation record will carry the exact source/PDF/package hashes,
portable-build evidence, and the remaining author, independent-review, and
operator-approval steps. This is a release candidate for review, not a public
submission or a Rule-9 clearance.

The completed [rc3 preparation record](../ReleasePackages/2026-10-08/P2-rc3/P2_RC3_RELEASE_PREPARATION_REPORT_2026-10-08.md)
and manifest preserve the 18/19 result, exact hashes, PDF inspection, and
portable-source verification.

## Core claim (allowed)

Version `0.2.0-rc4` addresses the 9 October local referee reconciliation.
Stage 3A's perturbative de Sitter control is distinguished from Stage 3B's
finite-amplitude, constraint-reconstructed expansion. Four threshold cases
are nonperturbative and one marginal. The persistence argument states its
unbounded-expansion, compact-shape, and nonzero-asymptotic-H assumptions.
The 18/19 failure remains unchanged; sampled thresholds have no certified
precision error bars. Figure 3 is full-width using unchanged image data.
The contribution is positioned against Edery and Negro et al.; final author
verification is not pre-certified. See the
[rc4 revision report](../ReleasePackages/2026-10-17/P1_P2_rc4/P1_P2_RC4_REVISION_REPORT_2026-10-17.md).

The implemented already-renormalized periodic-scalar stress is anisotropic on
rectangular flat $T^3$ and passes the recorded internal controls. When that
static stress is transported through the declared instantaneous $a^{-4}$
Bianchi-I closure, the bounded scan produces only *transient* passages near
$H_t/H_p=13/12$, with no quasi-plateau or attractor. This is not a general
dynamical-QFT no-go theorem.

## Must not claim

- Parameter-free $H_0=72.97$ or persistent free-field $13/12$ attractor  
- Geometric $a_0$ / MOND scale from this topology  
- Doughnut $T^2$ as flat $T^3$  
- Simulated box is Planck-safe cubic cosmology  
- Companion P1 as establishing geometric invariants  
- A general free-field result on evolving compact Bianchi-I spacetime
- Publication readiness before deferred external review and explicit operator approval

## Build

```powershell
conda activate itsm_env
cd papers\P2-Rectangular-T3-Casimir
.\Build-P2-Rectangular-T3-Casimir.ps1
```

## Reproduce science

```powershell
conda activate itsm_env
cd Analysis\Casimir\CBR-001
python casimir_t3_lattice.py
python cbr001_stage2_standalone.py --output-dir stage2_outputs
python cbr001_stage3_backreaction.py --stage2-csv stage2_outputs\cbr001_stage2_scan.csv --output-dir stage3_outputs
python cbr001_stage3b_ratio_test.py --stage2-csv stage2_outputs\cbr001_stage2_scan.csv --output-dir stage3b_outputs
```

Do not omit the Stage-2 output flag in a fresh chained run: the Stage-2 default
is the current directory, while the downstream defaults refer to
`stage2_outputs/`.

## Draft checklist

- [x] Skeleton `main.tex`  
- [x] Port CoreRecovery §06 + CBR STAGE docs  
- [x] Abstract ban-list review (B1–B16 packaging)  
- [x] Rectangular $T^3$ figure (not doughnut)  
- [x] Stage-1 / Stage-3B tables from validated outputs  
- [x] Stage-2 anisotropy + Stage-3B ratio/threshold figures  
- [x] Portable candidate hashes and explicit Stage-2 chain
- [x] Cover letter draft (`CoverLetter.txt`)  
- [x] Superseded hostile read retained with withdrawal warning
- [ ] Deferred Role-A analytic normalization/closure audit
- [ ] Deferred restricted Role-B execution witness
- [x] Independent heat-kernel/Mellin noncubic evaluator (four points)
- [x] Preregistered release-sensitivity suite completed (18/19; one stringent
  threshold-amplitude stability check failed, classifications unchanged)
- [x] Canonical v0.2.0-rc2 PDF rebuilt; all five pages visually inspected and
  PDF metadata/checksum sidecar verified (historical rc2 check only)
- [ ] Author's final cold read and confirmation of the rc4 declaration
- [ ] Explicit operator approval before any arXiv or journal action
