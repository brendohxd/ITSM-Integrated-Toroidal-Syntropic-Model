# Paper 1 — Present-epoch scale matching and \(C_{\mathrm{obs}}\) hygiene

**Genre:** Technical note (no-go results + one derived EFT identity)  
**Status:** Submission-ready draft for arXiv / CQG-style note  

**Title:** *Present-epoch scale matching, the weak-field invariant \(C_{\mathrm{obs}}\), and no-go results for a cubic \(T^3\) geometric story*

## Claims (allowed)

| Claim | Status |
|-------|--------|
| \(2\pi a_0\sim cH_0\) coincidence | Empirical fact |
| \(a_0\equiv cH_0/2\pi\) at \(t_0\) | **Phenomenological** postulate only |
| Circulation quantization \(\Rightarrow a_0\) | **Withdrawn** |
| Cubic \(E_1\), \(L=c/H_0\) vs Planck | **Excluded** |
| Fixed-moduli \(L_{\mathrm{phys}}(t)=c/H(t)\) | **Excluded** |
| \(\mathrm{Tr}(h)/\mathrm{Tr}(\gamma)=2/3\) | Derived identity (generic) |
| \(C_{\mathrm{obs}}=C_m^{3/2}/\sqrt{C_{\mathrm{IR}}}\) | **Derived** (field rescaling) |
| \(C_{\mathrm{obs}}=2/3\) from geometry | **Withdrawn** |
| Dual \(a_0=cH_0/2\pi\) + \(C_{\mathrm{obs}}=2/3\) as RAR | **Excluded** |

## Build

Activate the project env **once** in the terminal, then leave it active:

```powershell
conda activate itsm_env
cd papers\P1-Geometric-Invariants
.\Build-P1.ps1
```

See `SUBMISSION.md` for the full readiness checklist and `CoverLetter.txt` for
arXiv/journal text.

## Files

| File | Role |
|------|------|
| `main.tex` | Manuscript |
| `references.bib` | Bibliography |
| `Build-P1.ps1` | Build helper |
| `SUBMISSION.md` | Pre-flight / venue notes |
| `CoverLetter.txt` | Cover letter draft |
| `main.pdf` | Built PDF |

## Firewall for later papers

Do not re-inflate withdrawn geometric claims in Papers 2–4. See  
`../Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md` (ban list B1–B16).
