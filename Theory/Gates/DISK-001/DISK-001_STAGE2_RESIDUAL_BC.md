# DISK-001 Stage 2 — Residual definition, 2D BC, referee-grade residuals

Date: 2026-08-03  
Branch: `recovery/v12-core-architecture`  
Status: **PASS** (`PASS_DISK001_2D_AQUAL_STAGE2_RESIDUAL_BC`)  
Full DISK-001 gate: **IN PROGRESS**

## Why Stage 2 existed

Stage 1 used (i) a residual estimated with `np.gradient` (not the discrete
operator) and (ii) a **3D soft monopole** Dirichlet BC for a **2D** midplane
Poisson problem. Both limit peer-review credibility of the residual numbers.

Stage 2 fixes those methods issues under the same Conditional IR policy.

## Equation and BC

\[
\nabla\cdot\bigl(\mu(|\nabla\Phi|/a_{0,\mathrm{eff}})\,\nabla\Phi\bigr)
= 4\pi G\,\Sigma,
\qquad
\mu(x)=\frac{x}{\sqrt{1+x^2}},
\quad
a_{0,\mathrm{eff}}=C_{\mathrm{obs}}^2 a_0.
\]

- Density: elliptical Gaussian surface density $\Sigma$ (declared mass, $\sigma_x,\sigma_y$).  
- **BC:** Dirichlet outer data from the **2D free-space monopole**
  $\Phi_{\partial\Omega}=2GM\log(R_{\mathrm{soft}}/R_{\mathrm{ref}})$.  
- Start: linear Newtonian solve with the same BC; under-relaxed Picard thereafter.

## Residual definition (audit-critical)

\[
\varepsilon
=
\frac{\|A[\mu(\Phi)]\,\Phi - b\|_2}{\|b\|_2}
\quad\text{(interior DOFs only)},
\]

where $A[\mu]$ is the **same** face-centred 5-point operator used in the
linear solve. This is the residual a referee should demand.

## Convergence table (half-box $=24\,\mathrm{kpc}$)

| $n$ | $\Delta x$ | discrete $\varepsilon$ | curl of $-\nabla\Phi$ (rel) | algebraic-map curl (rel) |
|------:|-------------:|-------------------------:|-----------------------------:|-------------------------:|
| 49 | 1.00 | $8.7\times10^{-10}$ | $\sim10^{-18}$ | $2.3\times10^{-3}$ |
| 73 | 0.67 | $2.2\times10^{-9}$ | $\sim10^{-17}$ | $1.9\times10^{-3}$ |
| 97 | 0.50 | $1.7\times10^{-9}$ | $\sim10^{-18}$ | $1.7\times10^{-3}$ |
| 129 | 0.38 | $1.2\times10^{-9}$ | $\sim10^{-17}$ | $1.4\times10^{-3}$ |

All grids meet $\varepsilon<10^{-3}$ (by many orders). Residuals sit at the
direct-solver / floor regime; mild non-monotonicity at $10^{-9}$ is not
interpreted as a physics failure.

Potential structure: curl of $-\nabla\Phi$ at FD noise.  
Algebraic map $g=f(|g_N|)g_N$ retains larger relative curl (contrast only).

## Reproduction

```powershell
conda activate itsm_env
python Analysis\DISK\DISK-001\disk001_poisson_2d_aqual_stage2.py
# expect: PASS_DISK001_2D_AQUAL_STAGE2_RESIDUAL_BC
```

Outputs:

- `outputs/disk001_poisson_2d_aqual_stage2_summary.json`
- `outputs/disk001_stage2_convergence.csv`

## Scientific boundary

- Still **2D midplane**, Conditional IR, not SPARC, not Derived $C_{\mathrm{obs}}$.  
- Outer BC is **monopole only** (elliptical multipoles not matched on $\partial\Omega$).  
- Full DISK-001 PASS still needs $R$–$z$/3D geometry and a final gate report.

## Next

1. Axisymmetric $R$–$z$ nonlinear AQUAL  
2. Multipole BC beyond monopole  
3. `DISK-001_GATE_REPORT.md` only when geometry+criteria for full PASS are met  
