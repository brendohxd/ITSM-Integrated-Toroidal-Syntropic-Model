# P1 rc6 revision report

**Date:** 2026-10-17  
**Manuscript:** `Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc6.pdf`  
**Version:** `0.2.0-rc6`

## Scope

This local revision applies the editorial and structural recommendations extracted from the supplied recording. It does not claim that those recommendations validate the model, close any scientific gate, or authorize submission.

## Changes made

1. The introduction now states the intended appeal of the construction: the Hubble-scale coincidence supplies a dimensional acceleration scale, while the projector ratio supplies a dimensionless response coefficient. The text immediately states that this remains a consistency question because the phase dynamics and matter coupling are not supplied.
2. The main argument is ordered by scale and dependency: microphysical circulation and the \(a_0\) identification; local weak-field/action and projector analysis; global expansion and compact-topology constraints; then the conditional spherical RAR normalization check.
3. The reconstruction requirements are placed before the corresponding tests. The manuscript now introduces the M, S, and E requirements at the relevant points and retains the full checklist in Section VIII.
4. The conditional status of the \(4/9\) normalization and the approximately 18% same-input velocity comparator remains explicit. Neither is presented as a completed data rejection or galaxy likelihood fit.

No displayed equation, reconstruction criterion, bibliography entry, figure, physical input, observational catalogue, or P2 artifact was intentionally changed. The source, portable source bundle, and PDF are sealed separately from the working tree.

## Validation

- Canonical source build: passed with the installed Tectonic runtime.
- Portable source build: passed with the installed Tectonic runtime.
- Canonical and portable extracted PDF text: identical.
- PDF length: 7 pages.
- Rendered-page inspection: all 7 pages inspected at 110 dpi; no clipped text, missing figure, or visible layout defect was found.
- Displayed equations preserved: 21.
- Reconstruction criteria preserved: yes.
- Preserved artifact count checked by the seal: 220.
- Unresolved references, missing characters, and LaTeX errors: none.
- Build diagnostics retained in the manifest: 6 underfull-box warnings, 2 bibliography overfull-vbox warnings, and the existing deferred-float warning in each identical build log. The bibliography warning does not visibly clip content in the rendered pages.

## Scientific and governance status

```text
local_validation_pass = true
physics_pass = false
gate_effect = NONE
publication_ready = false
author_final_verification = PENDING
review_status = DEFERRED
Rule9_cleared = false
```

The manuscript remains a scoped present-epoch consistency and reconstruction note. The conditional Planck/topology comparator, \(C_{\rm obs}=2/3\) normalization, \(a_{0,\rm eff}=4a_0/9\), and velocity comparators remain analytic or background/statistic-specific results. They are not a global \(T^3\) solution, an independent MOND derivation, or an observational fit. No publication or external submission was performed.

## Sealed artifact hashes

The machine-readable values below are authoritative for this package and are duplicated in `P1_RC6_MANIFEST.json`.

| Artifact | SHA-256 |
|---|---|
| `main.tex` | `17d5a6feb2729497fc46e69b1b14a25a4b6559d58b0462bb32595989c79751df` |
| `Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc6.pdf` | `51dbece22cf601bf016f9f967e2f711e9abbebdfe5f85342d2b4adbaac24c6bf` |
| `ITSM_P1_source_v0.2.0-rc6_2026-10-17.zip` | `ca1709024a4d0c51767a82f5b953a9de1a38f10556695a4a9e1d56763116a9b8` |
