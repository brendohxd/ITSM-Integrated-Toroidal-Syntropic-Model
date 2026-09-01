# DISK-001 Stage 3 — Axisymmetric $(R,z)$ nonlinear AQUAL

Date: 2026-08-03  
Branch: `recovery/v12-core-architecture`  
Status: **PASS** (`PASS_DISK001_RZ_NONLINEAR_AQUAL`)  
Full DISK-001 gate: **IN PROGRESS**

## Equation

Axisymmetric cylindrical form (no $\varphi$ dependence):

\[
\frac{1}{R}\partial_R\Bigl(R\,\mu\frac{|\nabla\Phi|}{a_{0,\mathrm{eff}}}\partial_R\Phi\Bigr)
+\partial_z\Bigl(\mu\frac{|\nabla\Phi|}{a_{0,\mathrm{eff}}}\partial_z\Phi\Bigr)
=4\pi G\rho,
\]

$\mu(x)=x/\sqrt{1+x^2}$, $a_{0,\mathrm{eff}}=C_{\mathrm{obs}}^2 a_0$ (Conditional IR).

## Method (referee checklist)

| Item | Choice |
|------|--------|
| Density | $\rho\propto e^{-R/R_d}\mathrm{sech}^2(z/(2z_d))$, mass-normalised |
| Grid | Half-integer $R_j=(j+\tfrac12)\Delta R$ (no cell centre on axis); odd $n_z$ |
| Axis | Neumann regularity (no flux through $R=0$) |
| Outer BC | Dirichlet 3D soft Newtonian monopole |
| Nonlinear | Under-relaxed Picard + sparse direct solve |
| Residual | $\|A[\mu(\Phi)]\Phi-b\|_2/\|b\|_2$ interior, **same** $A$ as solve |
| Axis metric | $\mathrm{rms}_z[(\Phi_{j=1}-\Phi_{j=0})/\Delta R]/g_{\mathrm{char}}$ (should drop under refinement) |

## Convergence

| $n_R$ | $\varepsilon$ (discrete) | axis $d\Phi/dR$ metric | Picard iters |
|--------:|---------------------------:|------------------------:|-------------:|
| 33 | $9.2\times10^{-10}$ | 0.196 | 20 |
| 49 | $1.3\times10^{-9}$ | 0.142 | 20 |
| 65 | $1.4\times10^{-9}$ | 0.112 | 20 |

Residuals at solver floor; axis metric **improves** under refinement (as expected for $\Phi\sim a(z)R^2$ near the axis).

## Reproduction

```powershell
conda activate itsm_env
python Analysis\DISK\DISK-001\disk001_poisson_rz_aqual.py
# expect: PASS_DISK001_RZ_NONLINEAR_AQUAL
```

## Scientific boundary

- Conditional IR only; not Derived $C_{\mathrm{obs}}$.  
- Outer BC is soft monopole (disk multipoles not matched on $\partial\Omega$).  
- Not SPARC / STAT-001.  
- Full DISK-001 PASS still needs multipole-BC sensitivity, methods table polish, and explicit gate report criteria sign-off.

## Next toward full DISK-001

1. BC sensitivity (larger domain / multipole)  
2. Midplane $g(R)$ comparison to thin-disk limits  
3. `DISK-001_GATE_REPORT.md` when agreed full-pass criteria are met  
