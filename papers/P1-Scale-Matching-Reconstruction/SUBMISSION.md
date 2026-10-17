# Paper 1 — Submission readiness

## What this paper is (honest product)

A **short technical note**: scoped consistency constraints for an author-defined geometric packaging of
$a_0\sim cH_0/(2\pi)$ on cubic $T^3$, plus the derived weak-field invariant
$C_{\mathrm{obs}}=C_m^{3/2}/\sqrt{C_{\rm IR}}$.

It is **not** a derivation of MOND from topology and **not** a multi-tension
cosmology paper. Its narrow claims remain subject to author and independent review.

## Files to submit

| File | Role |
|------|------|
| `main.tex` + `references.bib` | Source |
| `Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc6.pdf` | Current local review PDF |
| `CoverLetter.txt` | arXiv comment / journal cover letter |
| Figure via `\graphicspath` | Bundle `itsm_t3_fundamental_domain.pdf` in `figures/`; the projection illustration is not included in rc6 |

For arXiv/journal upload, bundle the retained fundamental-domain figure and
use `\graphicspath{{figures/}}` in the packaged source. Include `main.tex`,
`references.bib`, and the generated `main.bbl`. Author/review/venue decisions
are distinct from a successful source-package build.

## Build (env already active)

```powershell
conda activate itsm_env
cd papers\P1-Scale-Matching-Reconstruction
.\Build-P1-Scale-Matching-Reconstruction.ps1
```

## Pre-flight checklist

### Scientific (firewall)

- [x] No circulation-quantization derivation of $a_0$
- [x] No $(L,\Gamma=cL,\omega=H_0)$ consistency claim as physics
- [x] Cubic $E_1$ at $L=c/H_0$ marked incompatible with the cited Planck bound
- [x] Fixed-moduli $L_{\rm phys}(t)=c/H(t)$ marked incompatible except for $q=0$ (or an added modulus sector)
- [x] Trace $2/3$ does not determine $C_{\mathrm{obs}}$
- [x] Dual $a_0=cH_0/2\pi$ + $C_{\mathrm{obs}}=2/3$ result bounded to the conditional spherical baseline
- [x] Doughnut not used as $T^3$
- [x] $C_{\mathrm{obs}}$ invariant derived via field rescaling
- [x] Reconstruction checklist for future geometric claims

### Presentation

- [x] Keywords
- [x] PDF bookmarks safe (`\texorpdfstring` on math section titles)
- [x] `hidelinks` (no colored boxes)
- [x] Table I full-width + row rules + text after table
- [x] Code/data availability
- [x] Focused bibliography (cited works only)
- [x] AI-tool use disclosed; final author verification and responsibility confirmation explicitly pending
- [x] Unsupported attribution to unspecified "recent proposals" removed
- [x] Reviewer-neutral disposition language replaces prosecutorial wording
- [x] (M), (S), and (E) evaluation criteria previewed before application
- [x] Each sector states its relevant requirements before testing the construction
- [x] Body follows circulation, local field theory, cosmology, then conditional normalization
- [x] Introduction explains the construction's intended physical appeal
- [x] $4/9$ and 18% shifts identified as conditional normalization checks, not a completed data rejection

### Human steps before upload

Current candidate: `0.2.0-rc6`, 17 October 2026. The
[rc6 revision report](../ReleasePackages/2026-10-17/P1-rc6/P1_RC6_REVISION_REPORT_2026-10-17.md)
records the audio-feedback response, preserved equations and scientific scope,
build and visual checks, and retained prior artifacts. The recording is an
editorial input, not independent scientific validation. Final author verification
and applicable review remain outstanding.

The preceding
[rc5 revision report](../ReleasePackages/2026-10-17/P1-rc5/P1_RC5_REVISION_REPORT_2026-10-17.md)
records the three targeted feedback responses, explicit velocity reference
conventions, local verification and preservation. There is no new data fit,
model preference, publication approval or completed author verification.

The preserved rc4
[revision report](../ReleasePackages/2026-10-17/P1_P2_rc4/P1_P2_RC4_REVISION_REPORT_2026-10-17.md)
maps the 9 October referee issues to corrections and records the rc4 build,
algebra, preservation, and visual checks. Those are local checks, not external
peer review. The author's final read and applicable independent review remain
outstanding; no submission is authorized.

### Preserved rc3 preparation record

Local rc3 preparation completed on 8 October 2026:

- [x] Saved manuscript corrections applied and version/date frozen
- [x] Canonical PDF compiled using the installed MiKTeX
- [x] Portable source package built with local figure paths
- [x] All six PDF pages visually inspected
- [x] Earlier retained PDFs/sidecars and pre-edit source snapshots preserved

The [rc3 preparation record](../ReleasePackages/2026-10-08/P1-rc3/P1_RC3_RELEASE_PREPARATION_REPORT_2026-10-08.md)
contains hashes and verification. The in-app preview compile timed out; the
native project and isolated-package builds passed. The human steps below
remain outstanding.

- [ ] Final author proofread (cold read of abstract + Secs. a0, bounds, rar)
- [ ] Confirm ORCID and email in footer
- [ ] Choose arXiv categories: **gr-qc** primary; **astro-ph.CO** cross-list
- [ ] Applicable independent review and author confirmation of the AI-use declaration
- [ ] Journal decision after arXiv feedback (CQG Note or PRD)

## Realistic venue expectation

| Venue | Fit |
|-------|-----|
| arXiv | **Recommended first** |
| CQG (Note / Comment) | Good fit for no-go + EFT hygiene |
| PRD | Possible as Brief Report; may ask for more positive results |
| ApJ / MNRAS | Weak fit (little new data analysis) |

## What would still block “derivation paper” status

The local rc3 preparation record is maintained separately from these human
steps. Applying the saved corrections and compiling a source package does
not complete the author proofread or independent review.

The sector reconstruction checklist in “Evaluation criteria, retained results,
and a reconstruction path” is
**future work**, not a defect of *this* note.
