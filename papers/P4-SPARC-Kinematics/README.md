# P4 — SPARC Galactic Kinematics under 2D/3D AQUAL Picard Solutions

**Directory:** `papers/P4-SPARC-Kinematics/`  
**VERSION:** `0.1.0-draft`  
**Status:** **Draft complete & compiled** (`main.pdf`)  
**Current boundary:** DISK-001 Stage 5 passed ($\varepsilon = 6.06 \times 10^{-9}$); STAT-001 175-galaxy master catalog executed ($\widetilde{\chi}_\nu^2 = 1.84$ median unfloated; $\chi_\nu^2 = 7.38$ floated MCMC).  
**Authority:** `papers/Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md` §4.4  
**Branch:** `recovery/v12-core-architecture`

## What this is

A 2-page RevTeX 4.2 publication letter presenting the kinematic rotation curve evaluation of the 175 SPARC disk galaxies under the first-principles ITSM AQUAL Picard solver without dark matter halos.

## Build

```powershell
cd papers\P4-SPARC-Kinematics
python generate_rar_figure.py
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
```
