# Paper 1 — Submission readiness

## What this paper is (honest product)

A **short technical note**: no-go results for a common geometric packaging of
\(a_0\sim cH_0/(2\pi)\) on cubic \(T^3\), plus the derived weak-field invariant
\(\Cobs=C_m^{3/2}/\sqrt{C_{\rm IR}}\).

It is **not** a derivation of MOND from topology and **not** a multi-tension
cosmology paper. That is a feature: it is what can currently survive peer review.

## Files to submit

| File | Role |
|------|------|
| `main.tex` + `references.bib` | Source |
| `main.pdf` | Built PDF |
| `CoverLetter.txt` | arXiv comment / journal cover letter |
| Figures via `\graphicspath` to `Assets/Figures/` | Bundle `itsm_t3_fundamental_domain.pdf` and `itsm_23_factor_schematic.pdf` with the source zip |

For arXiv/journal upload, copy the two figure PDFs into this directory (or a
`figures/` subfolder) and set `\graphicspath{{./}{figures/}}` if required by
the upload layout.

## Build (env already active)

```powershell
conda activate itsm_env
cd papers\P1-Geometric-Invariants
.\Build-P1.ps1
```

## Pre-flight checklist

### Scientific (firewall)

- [x] No circulation-quantization derivation of \(a_0\)
- [x] No \((L,\Gamma=cL,\omega=H_0)\) consistency claim as physics
- [x] Cubic \(E_1\) at \(L=c/H_0\) marked excluded vs Planck
- [x] Fixed-moduli \(L_{\rm phys}(t)=c/H(t)\) excluded (needs \(q=0\) or moduli)
- [x] Trace \(2/3\) does not determine \(\Cobs\)
- [x] Dual \(a_0=cH_0/2\pi\) + \(\Cobs=2/3\) RAR no-go stated
- [x] Doughnut not used as \(T^3\)
- [x] \(\Cobs\) invariant derived via field rescaling
- [x] Reconstruction checklist for future geometric claims

### Presentation

- [x] Keywords
- [x] PDF bookmarks safe (`\texorpdfstring` on math section titles)
- [x] `hidelinks` (no colored boxes)
- [x] Table I full-width + row rules + text after table
- [x] Code/data availability
- [x] Focused bibliography (cited works only)

### Human steps before upload

- [ ] Final author proofread (cold read of abstract + Secs. a0, bounds, rar)
- [ ] Confirm ORCID and email in footer
- [ ] Bundle figures for arXiv (paths relative to upload root)
- [ ] Choose arXiv categories: **gr-qc** primary; **astro-ph.CO** cross-list
- [ ] Optional: ask one external physicist for a 48h hostile read
- [ ] Journal decision after arXiv feedback (CQG Note or PRD)

## Realistic venue expectation

| Venue | Fit |
|-------|-----|
| arXiv | **Recommended first** |
| CQG (Note / Comment) | Good fit for no-go + EFT hygiene |
| PRD | Possible as Brief Report; may ask for more positive results |
| ApJ / MNRAS | Weak fit (little new data analysis) |

## What would still block “derivation paper” status

The ten-step reconstruction checklist in Sec.~“What remains…” — that is
**future work**, not a defect of *this* note.
