# P1 — Present-epoch scale matching and $C_{\mathrm{obs}}$ hygiene

**Directory:** `papers/P1-Scale-Matching-Reconstruction/`  
**VERSION:** see `VERSION` (currently `0.2.0-rc4`)
**Canonical PDF:** `Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc4.pdf`

(the build script writes this named PDF directly and emits its `.sha256`
sidecar; see `papers/PAPERS_NAMING.md`)

**Genre:** Technical note (scoped consistency constraints + one derived EFT identity)
**Status:** Local release candidate for author/external review; not submitted

**Title:** *Present-epoch scale matching, the weak-field invariant $C_{\mathrm{obs}}$, and constraints on a cubic $T^3$ geometric construction*

## Claims (allowed)

| Claim | Status |
|-------|--------|
| $2\pi a_0\sim cH_0$ coincidence | Empirical fact |
| $a_0\equiv cH_0/2\pi$ at $t_0$ | **Phenomenological** postulate only |
| Circulation quantization $\Rightarrow a_0$ | **Not derived** in the tested construction |
| Cubic $E_1$, $L=c/H_0$ vs Planck | **Incompatible** in the cited background/statistical benchmark, not an all-cosmology topology exclusion |
| Fixed-moduli $L_{\mathrm{phys}}(t)=c/H(t)$ | **Incompatible** except the coasting branch |
| $\mathrm{Tr}(h)/\mathrm{Tr}(\gamma)=2/3$ | Derived identity (generic) |
| $C_{\mathrm{obs}}=C_m^{3/2}/\sqrt{C_{\mathrm{IR}}}$ | **Derived** field-rescaling invariant; spherical force identifies only $C_{\mathrm{obs}}^2a_0$ if $a_0$ is free |
| $C_{\mathrm{obs}}=2/3$ from geometry | **Not derived** |
| Dual $a_0=cH_0/2\pi$ + $C_{\mathrm{obs}}=2/3$ | Conditional $4/9$ normalization conflict in the spherical baseline; not a global $T^3$ prediction or completed data fit |

## Release-candidate revision

Version `0.2.0-rc4` addresses the 9 October local referee reconciliation:
the construction is explicitly author-defined; the cycle-frequency test does
not infer centripetal acceleration from a flat torus geodesic; the circulation
formula's nonrelativistic domain is stated; Planck likelihood and matched-circle
statistics are distinguished; and the additional acceleration-scale degeneracy
is explicit. The author-verification declaration is pending, not pre-certified.
Original rc3 sources, PDFs, sidecars, and review records remain preserved.
See the [rc4 revision report](../ReleasePackages/2026-10-17/P1_P2_rc4/P1_P2_RC4_REVISION_REPORT_2026-10-17.md).

### Preserved rc3 history

Version `0.2.0-rc3` implements the saved 8 October cold-read corrections:
explicit metric traces, positive-coefficient branch and SI dimensions,
consistent scalar notation, and a conditional normalization statement in
Table I. The speculative projection illustration is omitted from this
candidate; its original asset and earlier PDFs are preserved. Keywords are
displayed, archive links use compact labels, and the version date is fixed.
The $C_{\mathrm{obs}}$ invariant and scoped $4/9$ result remain unchanged.
Author confirmation and applicable independent review remain outstanding.

See the [8 October rc3 preparation record](../ReleasePackages/2026-10-08/P1-rc3/P1_RC3_RELEASE_PREPARATION_REPORT_2026-10-08.md)
for compiler/PDF/package checks, exact hashes, and the remaining release steps.

## Build

Activate the project env **once** in the terminal, then leave it active:

```powershell
conda activate itsm_env
cd papers\P1-Scale-Matching-Reconstruction
.\Build-P1-Scale-Matching-Reconstruction.ps1
```

See `SUBMISSION.md` for the full readiness checklist and `CoverLetter.txt` for
arXiv/journal text.

## Files

| File | Role |
|------|------|
| `main.tex` | Manuscript |
| `references.bib` | Bibliography |
| `Build-P1-Scale-Matching-Reconstruction.ps1` | Build helper |
| `SUBMISSION.md` | Pre-flight / venue notes |
| `CoverLetter.txt` | Cover letter draft |
| `Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc4.pdf` | Current review PDF |

## Firewall for later papers

Do not re-inflate unsupported geometric claims in Papers 2–4. See
`../Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md` (ban list B1–B16).
