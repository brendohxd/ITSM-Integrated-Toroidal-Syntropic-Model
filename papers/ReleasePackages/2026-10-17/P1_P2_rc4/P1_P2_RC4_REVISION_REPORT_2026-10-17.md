# P1/P2 rc4 — targeted referee-response revision

Date: 17 October 2026. Version: `0.2.0-rc4` for both manuscripts.

## Outcome and scope

The targeted manuscript revision and local review-package preparation are
complete. Both six-page PDFs compile, their isolated source packages compile,
and extracted text agrees between canonical and isolated builds. All 12 final
pages have been visually checked. This is not independent peer review,
publication clearance, an ITSM physics promotion, or author proofread approval.
Nothing was submitted, published, committed, pushed, or synchronized to the vault.

Owning review:
[9 October local referee/Grok reconciliation](../../2026-10-09/P1_P2_LOCAL_REFEREE_REVIEW_AND_GROK_RECONCILIATION_2026-10-09.md).
That report, the original rc3 PDFs, and the scientific evidence remain unchanged.

## Scientific corrections

| Review issue | rc4 response |
|---|---|
| P1-A: flat-torus geodesic versus circular acceleration | Removed the centripetal-acceleration premise. The inconsistency uses the explicitly defined cycle clock `omega = 2 pi v/L`; a closed flat geodesic has zero intrinsic covariant acceleration. |
| P1-B: unspecified proposal and novelty | The full construction is explicitly author-defined, not attributed to unnamed published proponents. Established MOND, AQUAL, projector and topology ingredients are separated from this note's joint consistency audit. |
| P1-C: coefficient identifiability | Field rescaling leaves `C_obs` invariant, but a free `a0` introduces another reparameterization: the spherical response identifies only `C_obs^2 a0`. Neither coefficient is independently fixed by computing it from assumed inputs. |
| P1-C: topology statistics and background | Distinguished the Planck likelihood threshold from the numerically equivalent 99%-confidence matched-circle result. The conversion to roughly six Hubble lengths is conditional on the benchmark background and distance, not an all-cosmology exclusion of `T^3`. |
| P1: conventions and numerical comparison | Separated superfluid density from integer winding, stated the nonrelativistic circulation formula's domain, and withdrew a relativistic-flow/particle-mass interpretation of the formal mass assignment. At illustrative `H0=70`, the conditional effective scale is about `4.8e-11 m/s^2`; the 18% velocity shift compares the same input `a0`, not a completed galaxy likelihood. |
| P2-A: perturbative versus finite-amplitude stages | Stage 3A is a small-source de Sitter control. Stage 3B evolves shape/shear with Hamiltonian-reconstructed mean expansion. Four threshold cases are nonperturbative and one marginal by the registered source-fraction convention. No controlled dynamical-QFT accuracy is asserted for them. |
| P2-A: independent dynamics check | A Hamiltonian residual computed after reconstructing `H` from that same constraint is labelled an algebraic control, not an independent mean Einstein equation. A separately evolved Raychaudhuri check remains undemonstrated. |
| P2-B: threshold repeatability | Kept the original `FAIL`, 18/19. Printed the discrepant threshold pair; the relative shift uses the original baseline denominator. Sampled-time maxima and missing certified peak-time/grid error control are explicit. Qualitative stability refers to the three re-tested shapes; no certified threshold uncertainty is invented. |
| P2-C: asymptotic scope | Constant nonunit directional ratio forces exponential shape drift and cannot remain in a compact positive shape interval over unbounded expansion. The complementary stress argument explicitly assumes `a -> infinity`, bounded shape factor, `H -> H_infinity > 0`, and the stated regular derivative limits. Positive `H` alone is insufficient. The numerical scan ends at `N=20`, not infinity. |
| P2-D: contribution and presentation | Positioned the closure/target-persistence audit relative to established static Casimir results and Negro et al.'s state-based calculation. Figure 3 is full-width with the exact original image/data. Keywords are visible, and the availability link is readable. |
| Both: author and release statements | Replaced unconfirmed assertions of completed author verification with an accurate pending declaration. README, submission checklist and cover-letter drafts identify rc4 without certifying independent review or author approval. |

The four alleged P2 transcription errors rejected by the owning review were
not applied: the cubic density, `rdot = r delta`, total-density Hamiltonian
constraint, and `N = +ln a` retain their correct conventions.

Primary literature checked for these revisions:

- [Planck 2015 XVIII, v2](https://arxiv.org/abs/1502.01593v2): source for the
  distinct likelihood and matched-circle statistics, not a new ITSM likelihood.
- [Negro et al., v2](https://arxiv.org/html/2603.12319v2): context for static
  topology stress, quantum-state/zero-mode dependence and anisotropic
  backreaction; not validation of the present finite-amplitude closure.

## Verification

- `validate_rc4.py` checks 31 bounded algebra/provenance statements. Final
  receipt: `validation_attempt_04.json`, **31/31**, with `physics_pass=false`
  and `publication_ready=false`. These flags are deliberately separate from
  local computational validation.
- The receipt retains the P2 sensitivity source's exact **FAIL, 18/19**,
  `physics_pass=false`, and its sole failed threshold-repeatability check.
  No CBR scientific calculation, criterion, threshold CSV, or old receipt was
  regenerated or overwritten for this revision.
- Checked the cycle-clock inconsistency, field and scale reparameterizations,
  `q <-> x` target, required-stress identity, shape drift, small-source maximum,
  required amplitude, threshold classifications, source fractions and frozen
  evidence hashes. This does not certify physical closure or numerical ODE
  error bounds.
- Canonical and isolated builds use bundled Tectonic 0.17.0 in untrusted mode.
  Final TeX logs have no undefined citations/references, overfull boxes,
  missing-character warnings, or LaTeX errors. Benign underfull warnings remain.
  P1 also reports a RevTeX deferred-float warning; Figure 1 is nevertheless
  present and correctly placed on page 3 in both builds, checked visually.
- All final pages were rendered with Poppler at 110 dpi. P1 pages 1–5 are
  byte-identical renders of already inspected pages; its changed page 6 was
  re-inspected. All six final P2 pages were inspected after the last revision.
- Source ZIP CRCs and members were checked. The only canonical-to-portable
  TeX transformation is restricting `graphicspath` to the included `figures/`.
  Generated `main.bbl`, bibliography and original figure assets are included.
  Canonical/portable PDF text and page counts agree exactly.
- `P1_P2_RC4_MANIFEST.json` identifies sources, PDFs, source ZIPs, member
  hashes and build-log hashes. Its sidecar seals the manifest; it is not a
  scientific clearance certificate.

### Preserved attempts and environment failures

The initial native MiKTeX attempts were blocked by registry/launch failures;
a direct version probe returned `-1058471934`. No firewall, security rule,
registry setting, compiler configuration or installed TeX distribution was
changed. The built-in standalone preview could not access the project's
external figure. Tectonic initially could not retrieve its resource bundle
inside the sandbox; the permissioned bundled-compiler route succeeded.
An optional cached-only bundle experiment failed and was not used for the
delivered PDFs. Raw local command output remains under ignored `.local/`
artifacts, not in the source archives.

Validation attempts 01 and 02 are preserved. They used the tightened threshold
as the relative-error denominator instead of the registered baseline and
therefore failed that new audit assertion (30/31); attempt 01 additionally
failed while formatting a relative output path after saving its receipt.
The audit was corrected against the original sensitivity implementation,
not by altering the threshold data or tolerance. Attempt 03 passed the
intermediate sources; attempt 04 passes the final sources. A packaging
attempt with the research interpreter lacked `pypdf`; the supplied document
runtime was used without installing anything.

## Preservation and the pre-existing P1 source-sidecar discrepancy

Before any manuscript edit, the canonical source, bibliography, version,
README, submission checklist, cover letter and any source sidecar were
copied into `preserved_rc3/`. Older rc3 release packages and scientific
sidecars were left in place.

At the start, P1's working `main.tex.sha256` claimed
`5597cb6eeeb5b70c6264eb606c78f95319ace9c31dd2ea4fd58cc1a27228b1d4`,
while the actual pre-edit source was
`4b0d0aefd22f81ea20057936ee7566f24eb12b9b49b2fb22bebdfdcc5a6f2510`.
The latter agrees with the preserved 8 October rc3 preparation report.
This is an observed pre-existing stale working sidecar; its cause/timing
has not been established here. The original mismatch is not rewritten or
certified as a historical match.

The exact old sidecar and source remain together in `preserved_rc3/`. The
mutable canonical P1 source sidecar now identifies the intentionally revised
rc4 TeX (`2dddcba884df60dd8f990ee03a65e219b831540817569927af1164f9e099f8f8`).
No old PDF sidecar, scientific output hash, or historical freeze was updated.

## Still outstanding

1. Author's final cold read, metadata confirmation and AI-declaration approval.
2. Applicable independent review; the automated revision is not an unbiased
   external referee or Tier-1 acceptance guarantee.
3. P2 certified threshold precision and independent mean-equation controls
   remain open; the present claim is expressly qualitative and closure-bounded.
   Full evolving-state renormalization is outside this paper's narrower scope,
   not a calculation silently claimed complete by this revision.
4. Explicit submission/publication authority and a verified immutable public
   snapshot for the exact selected version.

No additional ITSM derivation, observational fit, or stronger-model session
was required or initiated for this editorial/scientific-scope revision.
