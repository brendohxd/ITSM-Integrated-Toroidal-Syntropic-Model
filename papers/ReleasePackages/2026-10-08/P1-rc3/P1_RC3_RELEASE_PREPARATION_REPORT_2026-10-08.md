# P1 rc3 local release preparation - 8 October 2026

Result ID: `P1-RC3-PREP-20261008`. Manuscript: `0.2.0-rc3`.
Local manuscript correction and source-package preparation are complete.
This is a local release candidate for author and independent review; no
external submission, publication, gate closure or review clearance is claimed.

## Changes and scope

The saved correction patch (`918e61fac03abbdf8adc549aee8ea45556c899c1c37076d178bb2491d7c19891`)
was applied to the recorded rc2 source. The current manuscript explicitly
defines metric traces, positive-coefficient branch and SI dimensions; uses
`psi` consistently in the compact-source flux; states the Table-I coefficient
comparison as a conditional normalization shift; and displays keywords.
The speculative projection illustration is omitted. Its original asset and
all earlier retained PDFs remain available. The numerical scale-matching
postulate, normalization invariant, and conditional spherical `4/9` result
are unchanged. No new fit or first-principles coefficient is asserted.

The version/date, README, submission notes, draft cover letter and P1 naming
row are updated. Code-availability links are labelled and the paragraph uses
ragged-right alignment to avoid stretched spacing. The manuscript date is
fixed to 8 October 2026 for this candidate.

## Verification

- The complete native MiKTeX project build passed: three TeX passes and BibTeX.
- The portable source build passed with package installation and shell escape
  disabled. Its recorder lists `252` inputs and zero repository dependencies.
- Canonical and isolated PDFs each have six pages, with equal extracted text
  after whitespace normalization. Every page was inspected; the affected last
  two pages were rendered and reinspected after the final paragraph correction.
- Thirteen distinct citation keys match thirteen bibliography entries.
- The upload archive contains `main.tex`, `references.bib`, generated
  `main.bbl`, and `figures/itsm_t3_fundamental_domain.pdf`. The packaged
  manuscript differs only by the local figure search path and terminal newline.
- The native final log has no TeX error, undefined citation/reference or
  overfull box. Nameref/underfull-box and BibTeX style diagnostics remain
  recorded in ignored local logs; no compiler warning is a physics verdict.
- The built-in document compiler returned `compile-failed: Compilation timed
  out` with `sandbox error: command timed out`. No preview-check success is
  claimed. The final native project/source builds and PDF inspection are the
  successful verification path.

| Artifact | SHA-256 |
|---|---|
| Current `main.tex` | `4b0d0aefd22f81ea20057936ee7566f24eb12b9b49b2fb22bebdfdcc5a6f2510` |
| Canonical rc3 PDF | `d16a339e866358dbe448e7438b2e2e7e5e8fb1614cda7ed4ef1f1b4c380ca827` |
| Packaged `main.tex` | `63f854eeaed62bde4da13fd6b370c0943112e1efe5b059bd140bc9f8fe385ea3` |
| Source ZIP | `e2c37792462e9bae1cc390ba2a8f237ed6e4b971829c94e70ffd83d2839563a1` |
| Isolated verification PDF | `75c96631976979383f7a5dc8c81c77311b9dd950a96b78b28560584c26309d98` |

## Provenance and review dependency

The exact seven pre-edit P1 source/document files were copied and hash-checked
before corrections. The previous rc3 layout proof and its sidecar were also
preserved before the final proof iteration. These private snapshots and build
logs remain local. The earlier rc1/rc2 retained PDFs, original illustration
assets, rc2 preparation report/manifest, and saved correction patch are not
rewritten by this record. Current-source changes are intentional and versioned.

`review_status=DEFERRED`, `Rule9_cleared=false`,
`research_execution=PROCEED_PROVISIONALLY`, `gate_effect=NONE`, and
`publication_ready=false`. This is a parent-authored local preparation record;
it does not constitute independent Role-A/B/C assessment. No provisional
R4C1/TOP-X4 observational prediction is imported. Existing scoped P1 identities
and source assumptions remain the inputs. Any later reuse inherits the
uncompleted review of this candidate.

`MAT-001=BLOCKED`, `UVIR-003=IN_PROGRESS`, `K_Q=NOT_DERIVED`, and
`V=NOT_COMPUTED` remain unchanged. They do not prevent local preparation of
this bounded consistency note and do prevent stronger dependent claims.

## Remaining author and external-release work

- Author cold proofread and confirmation of email, ORCID, affiliation,
  acknowledgement and the manuscript's author-review declaration.
- Applicable independent assessment when the operator resumes reviews.
- Final venue/categories/endorsement and public-release decision.

These human steps remain unchecked. No paid reviewer was dispatched, no
repository commit/push was made, and no account, deposit or website was changed.
The next planned paper is P2's bounded Casimir/closure result.
