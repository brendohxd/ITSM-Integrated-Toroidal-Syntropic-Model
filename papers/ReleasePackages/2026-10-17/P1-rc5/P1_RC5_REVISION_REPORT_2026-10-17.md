# P1 rc5 revision and validation report

Date: 17 October 2026  
Manuscript: `Present-epoch scale matching, the weak-field invariant C_obs, and constraints on a cubic T^3 geometric construction`  
Version: `0.2.0-rc5`

## Scope

This package records three targeted refinements to P1 following the local
referee/Grok critique. P2 was not edited. The preceding rc4 package and all
files protected by the rc5 preservation baseline remain unchanged.

## Changes made

1. The introduction now states the transferable value narrowly: this is a
   joint consistency and normalization audit, with a reusable procedure for
   distinguishing field conventions from matched couplings, stating the
   independent acceleration input, and retaining compact-source integrability.
   It does not claim a new microscopic theory, a new universal law, or priority
   for the coefficient identity.
2. The velocity comparison is disambiguated. The approximately 18% reduction
   is the same-input comparison
   \(v(C_{\rm obs}=2/3)/v(C_{\rm obs}=1)=\sqrt{2/3}\), namely 18.3503%.
   The separate illustrative comparison to
   \(1.2\times10^{-10}\,\mathrm{m\,s^{-2}}\), using \(H_0=70\), gives a
   ratio of 0.7957 and a 20.4288% reduction. Neither number is presented as
   an observed discrepancy or a completed data rejection.
3. The endpoint now states explicitly that the note stops at analytic
   normalization. It contains no rotation-curve likelihood, nuisance
   marginalization, intrinsic-scatter test, or model-evidence comparison.
   Those require a separately specified response, matching inputs, data
   selection, and nuisance model.

The action block, bibliography, figure, physical inputs, and scientific scope
were not changed by this revision.

## Validation

- Canonical and portable source builds completed with the bundled Tectonic
  compiler.
- Canonical and portable PDFs were six pages and had identical extracted text
  and page counts.
- The final six rendered pages were inspected individually for clipping,
  overlap, missing figures, and unreadable equations. No such defect was
  found.
- Build logs contained no undefined references, missing characters, overfull
  boxes, or LaTeX errors. They retain five pre-existing underfull-box warnings
  and the pre-existing deferred-float warning; these are recorded in the
  manifest and are not treated as silent failures.
- The sealed manifest reports `local_validation_pass: true`,
  `physics_pass: false`, and `publication_ready: false`.
- The numerical audit records
  \(a_0=1.0824013602391998\times10^{-10}\,\mathrm{m\,s^{-2}}\) for the
  illustrative \(H_0=70\) input and
  \(a_{0,\mathrm{eff}}=4.810672712174221\times10^{-11}\,\mathrm{m\,s^{-2}}\).
  These are analytic checks, not a fitted observational result.

The built-in editor preview compiler could not run because the current
restricted desktop environment refused its required writable-root policy.
The independent native Tectonic builds and the external rendered-page
inspection succeeded. An earlier direct optimizer invocation also failed at
the shell-parser boundary; the corrected invocation was the one used for the
accepted builds. No security, firewall, or compiler configuration was changed.

## Preservation and review status

The rc5 baseline protects 76 prior artifacts, including the rc4 package and
the unchanged P2 source/PDF set. The canonical source sidecar was updated to
the final rc5 source hash. The sealed manifest and sidecars record the final
artifact hashes.

Author final verification remains `PENDING`, and independent review remains
`PENDING`. This package is therefore a review copy, not a publication-ready or
physics-cleared release.

