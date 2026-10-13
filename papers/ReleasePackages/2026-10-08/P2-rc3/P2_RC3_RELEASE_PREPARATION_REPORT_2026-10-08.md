# P2 rc3 release-preparation report — 8 October 2026

## Outcome

Paper 2 has a complete local negative-result release candidate. Version
`0.2.0-rc3` preserves the registered scientific result: the preregistered
release-sensitivity suite is `FAIL` at 18/19 checks because the `r0=1.5`
threshold-amplitude repeatability changed by `8.7384e-5`, above the frozen
`1e-8` bound. All registered trajectory classifications remained
`TRANSIENT_CROSSING`, no attractor appeared, and the bounded no-attractor
conclusion is unchanged.

This preparation changed version/date and release documentation only. It did
not alter equations, thresholds, numerical receipts, classifications, or
CBR-001 evidence inputs.

## Verification

- Canonical TeX project: three `pdflatex` passes and BibTeX completed; the
  helper process exited only during sidecar emission because the elevated host
  lacked `Get-FileHash`. The PDF was present and its sidecar was independently
  computed and verified.
- Canonical PDF: five pages, SHA-256
  `bbbfe121a3c91a47e29678b59aa43045b7d0e790bba3041adfa3fc6a6163a9e0`.
- Portable source build: five pages, SHA-256
  `2b9e9f0680e5918c38b5093688f4c56d92bccfc0347ebf0272b43a48133da998`.
- Canonical and portable PDFs have identical normalized extracted text.
- All five canonical pages were rendered at 120 dpi and visually inspected;
  no clipping, missing figures, overlap, or unresolved-reference text was
  observed. Normal RevTeX float and underfull-box warnings remain recorded in
  the build log and are not physics failures.
- Portable source archive contains the manuscript, bibliography, generated
  `main.bbl`, checksum ledger, and four figures. Archive SHA-256:
  `0e0c9b94290ea8d6ec53a4246bf8ae1d407f59b9819321e7c3c6c304e7edf93a`.

## Provenance

- Current manuscript SHA-256:
  `4f5e587c4882cc5a1937819c19c5eea85d4c0a29f3c59f932060f168e5467396`.
- Packaged manuscript SHA-256 (graphic path restricted to `figures/`):
  `cc66bfb243417741bd6f0c9c6444265ca91a6cd3871c756669af767fd60cbb3c`.
- Previous pre-rc3 manuscript snapshot:
  `5d287860c7bf8b449aa098ddb9668ace59948b9749c9d9d13ac353d62bb4bebc`.
- Retained rc2 PDF SHA-256:
  `70f4f8d7931c33bc224b4207d783b8c91cd57c7a876d4eb01d40584cc025b3a7`.
- P2 sensitivity report SHA-256:
  `c1398b26c1fd443f08f2873b07d28b3f648ed7170dc1892fc50ad7ba5e0b2c73`.
- P2 sensitivity contract SHA-256:
  `2dd240cd8d7890585aee259a4ad2c90c3600c3fb3428b1149eeaffbb083a8c04`.

The prior rc2 candidate and its sidecar, pre-rc3 source snapshot, older draft
PDFs, and existing CBR-001 evidence remain preserved. The portable package is
a separate clean source tree and does not replace the working manuscript.

## Status boundary

`local_preparation=COMPLETE`; `publication_ready=false`; review is `DEFERRED`;
`Rule9_cleared=false`; `research_execution=PROCEED_PROVISIONALLY`;
`gate_effect=NONE`.

Outstanding work is author proofread/metadata confirmation, applicable
independent review, explicit operator approval, and any future CBR-002,
dynamical-renormalization, zero-mode, or external-replication work. MAT-001,
UVIR-003, `K_Q`, `V`, and TOP-X4 parent statuses are unchanged.

No memory mutation, provider dispatch, commit, push, upload, DOI freeze,
promotion, or publication occurred.
