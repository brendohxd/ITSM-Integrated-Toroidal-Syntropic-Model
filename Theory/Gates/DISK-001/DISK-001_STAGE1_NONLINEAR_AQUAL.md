# DISK-001 Stage 1 — Nonlinear AQUAL methods package

Date: 2026-08-03  
Branch: `recovery/v12-core-architecture`  
Status: **PASS** (`PASS_DISK001_STAGE1_NONLINEAR_AQUAL`)  
Full DISK-001 gate: **IN PROGRESS**

## Peer-review posture

This stage is written so a methods referee can audit:

1. the **equation solved**,  
2. the **discretisation**,  
3. **quantitative residuals**,  
4. **convergence under refinement**,  
5. **explicit non-claims**.

Conditional IR only (`C_{\mathrm{obs}}\sim 1`, phenomenological \(a_0\)). Not Derived \(\Cobs\).

## Results

### A. Spherical identity (theorem, not a fake 1D PDE win)

Under spherical symmetry, AQUAL integrates to the algebraic map

\[
|g|\,\mu(|g|/a_{0,\mathrm{eff}})=|g_N|.
\]

| \(n_r\) | max rel mass error | identity residual |
|--------:|-------------------:|------------------:|
| 64 | \(4.7\times10^{-3}\) | \(\sim10^{-16}\) |
| 128 | \(1.2\times10^{-3}\) | \(\sim10^{-16}\) |
| 256 | \(2.9\times10^{-4}\) | \(\sim10^{-16}\) |
| 512 | \(7.1\times10^{-5}\) | \(\sim10^{-16}\) |

Subgate: `PASS_DISK001_SPHERE_AQUAL_IDENTITY_CONVERGENCE`

### B. 2D nonlinear AQUAL Poisson (Picard + sparse FD)

\[
\nabla\cdot\bigl(\mu(|\nabla\Phi|/a_{0,\mathrm{eff}})\,\nabla\Phi\bigr)=4\pi G\,\Sigma
\]

on an elliptical Gaussian surface density; Dirichlet soft Newtonian BC.

| \(n\) | rel PDE residual | curl of \(-\nabla\Phi\) (rel) | curl of algebraic map (rel) |
|------:|-----------------:|-----------------------------:|----------------------------:|
| 33 | \(8.9\times10^{-2}\) | \(\sim10^{-17}\) | \(3.1\times10^{-3}\) |
| 49 | \(5.2\times10^{-2}\) | \(\sim10^{-17}\) | \(1.4\times10^{-3}\) |
| 65 | \(3.5\times10^{-2}\) | \(\sim10^{-17}\) | \(7.9\times10^{-4}\) |

Potential field is curl-free at FD noise; residual improves under refinement.  
Algebraic \(g=f(|g_N|)g_N\) is **not** substituted for the potential solution.

Subgate: `PASS_DISK001_2D_NONLINEAR_AQUAL_PICARD`

## Reproduction

```powershell
conda activate itsm_env
python Analysis\DISK\DISK-001\disk001_stage1_run_all.py
```

## Scientific boundary (must appear in any citation)

- Midplane **2D** model, not full 3D disk / \(R\)–\(z\).  
- PDE residual \(\sim\) few percent on \(n=65\): methods progress, **not** production astronomy.  
- BC is soft Newtonian monopole (known limitation).  
- No SPARC fits, no STAT-001, no Derived matching.  
- Full DISK-001 PASS still requires tighter residuals, geometry upgrades, and a gate report.

## Next

1. Larger domain / better multipole BC  
2. Axisymmetric \(R\)–\(z\) or 3D  
3. Convergence tables at production residual targets (\(\lesssim10^{-3}\)–\(10^{-4}\))  
4. `DISK-001_GATE_REPORT.md` only when full pass criteria met  
