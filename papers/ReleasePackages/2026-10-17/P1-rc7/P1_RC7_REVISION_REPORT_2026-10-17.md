# P1 rc7 revision report

**Date:** 2026-10-17
**Manuscript:** `Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc7.pdf`
**Version:** `0.2.0-rc7`
**Predecessor:** `v0.2.0-rc6`, PDF SHA-256 `51dbece22cf601bf016f9f967e2f711e9abbebdfe5f85342d2b4adbaac24c6bf`

## Scope

This local revision records the rc7 presentation and seals a portable source bundle. It does not change a disposition, a numbered physical equation, a numerical conclusion, a gate, or the sealed rc6 artifacts.

## Changes made

1. The introduction names the package under test. The historical `main` line states that macroscopic circulation quantization derives \(a_0=cH_0/2\pi\) and that the projector trace is the geometric coefficient \(C_{\mathrm{obs}}=2/3\). Zenodo `10.5281/zenodo.18808348` is identified as the legacy public archive of that package. The note does not attribute the package to an independent published model, and the Zenodo record is not treated as a derivation authority.
2. The Planck length conversion now shows the cited Planck 2018 TT,TE,EE+lowE+lensing central values: \(r_*=144.43\,\mathrm{Mpc}\), \(100\theta_*=1.04110\), and \(H_0=67.36\,\mathrm{km\,s^{-1}\,Mpc^{-1}}\). With \(c=299792.458\,\mathrm{km\,s^{-1}}\) and a flat background, \(\chi_{\mathrm{rec}}=r_*/\theta_*=13872.8\,\mathrm{Mpc}\), \(c/H_0=4450.60\,\mathrm{Mpc}\), and \(\chi_{\mathrm{rec}}/(c/H_0)=3.117\). Then \(1.94\times 3.117=6.05\). The retained displayed bound remains \(L\gtrsim 6\,c/H_0\), the one-figure form of that product. The coarser round number \(3.15\) is not this central-value ratio. The factor-of-six comparison and the suppressed-scale expression are unchanged.
3. The full GitHub address `github.com/brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model` is printed on two lines. The REVTeX class option `showkeys` remains because, in this class, it prints the keyword line rather than citation keys.

## Validation

- Canonical source build: `pdflatex`/`bibtex`/`pdflatex`/`pdflatex` through `Build-P1-Scale-Matching-Reconstruction.ps1`, exit 0.
- Portable source build: the same four-pass sequence from the sealed rc7 portable bundle, exit 0.
- The build shell reported conda environment `base`, not `itsm_env`. The TeX run itself completed.
- PDF length: 7 pages for both canonical and portable builds.
- Canonical and portable PDFs have identical extracted text and identical 110-dpi rendered page images for all seven pages.
- Log scan: no LaTeX errors, undefined references, overfull boxes, or missing characters in either final log. Six underfull-box warnings and the existing deferred-float warning remain in each log; rendered-page inspection found no clipping or missing content.
- Rendered-page inspection: all seven canonical pages inspected at approximately 110 dpi; portable output matched every page image byte-for-byte at that render scale.
- Portable archive: `ITSM_P1_source_v0.2.0-rc7_2026-10-17.zip` passed `ZipFile.testzip()` and contains only `VERSION`, `main.bbl`, `main.tex`, `references.bib`, and `figures/itsm_t3_fundamental_domain.pdf`.
- rc6 PDF hash rechecked and unchanged.
- No commit or push was performed.

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

The manuscript remains a scoped present-epoch consistency note. The conditional Planck comparison, the underived \(C_{\mathrm{obs}}=2/3\) comparator, \(a_{0,\mathrm{eff}}=4a_0/9\), and the velocity comparators are unchanged. This revision does not clear a gate or authorize submission.

## Sealed artifact hashes

| Artifact | SHA-256 |
|---|---|
| `main.tex` | `455521639bd9e10923ba5add70f4733a838b2778128272fc6a61b73445cfd5bd` |
| `Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc7.pdf` | `762180a79eb88dbe01afc504c9a8cad305ee7668f1d854fb15b699f3827580b0` |
| `ITSM_P1_source_v0.2.0-rc7_2026-10-17.zip` | `ecafe4b55320a8744e26c35c979446ab5acbbb7bc4c050c39a5f3dfd7c43a266` |
| rc6 PDF, unchanged | `51dbece22cf601bf016f9f967e2f711e9abbebdfe5f85342d2b4adbaac24c6bf` |
