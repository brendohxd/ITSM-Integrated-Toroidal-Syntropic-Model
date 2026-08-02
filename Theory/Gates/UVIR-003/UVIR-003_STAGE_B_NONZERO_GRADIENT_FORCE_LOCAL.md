# UVIR-003 Stage B — Nonzero-gradient force local expansion (Track A)

Date: 2026-08-03

Branch: `recovery/v12-core-architecture`

Calculation status: **PASS** (local Track-A sector; not homogeneous S-matrix)

Subgate:
`PASS_NONZERO_GRADIENT_FORCE_LOCAL`

Full UVIR-003 gate: **IN PROGRESS**

MAT-001: **BLOCKED**

## Purpose

Close the held exact Track-A obstruction

\[
-A_{\mathrm{IR}}\,|\nabla\pi|^3
\]

by performing the **declared local nonzero-gradient expansion** (Force Completion
Options §4, Track A), instead of forcing a zero-gradient Taylor kernel that
does not exist.

## Declared background

\[
\overline{\nabla\pi} = v\,\mathbf{e}_x,\qquad v>0.
\]

Fluctuations: \(\nabla\delta\pi = \varepsilon\,(x,y,z)\) with parallel \(x\) and
transverse \(p_\perp^2=y^2+z^2\).

## Verified expansion

\[
\begin{aligned}
|v\mathbf{e}_x+\varepsilon\nabla\delta\pi|^3
&= v^3
+ 3v^2\varepsilon x
+ \tfrac32 v\,\varepsilon^2(2x^2+p_\perp^2) \\
&\quad
+ \varepsilon^3\!\left(x^3+\tfrac32 x\,p_\perp^2\right)
+ \tfrac38\varepsilon^4\frac{p_\perp^4}{v}
+ O(\varepsilon^5).
\end{aligned}
\]

Symbolic match: **PASS**.

## Local force dynamics (from \(L=-A_{\mathrm{IR}}|\nabla\pi|^3\))

- Quadratic potential Hessian eigenvalues \(\{6A_{\mathrm{IR}}v,\,3A_{\mathrm{IR}}v\}\)
  — **positive** for \(A_{\mathrm{IR}}>0\), \(v>0\) (Stage-A cubic Hessian claim).
- Local cubic Fourier vertex for three force legs constructed and checked on
  pure-parallel kinematics: \(6\mathrm{i}A_{\mathrm{IR}}q^3\).
- Quartic coefficient \(\propto 1/v\) — **singular as** \(v\to 0\); zero-gradient
  homogeneous limit is **not** taken.

## Non-claims

- Not an isotropic FRW / homogeneous \(2\to 2\) amplitude.  
- Not nested in-in integrals.  
- Not unitarity / strong-coupling scale.  
- Not MAT-001.

## Reproduction

```powershell
conda activate itsm_env
python Analysis\UVIR\UVIR-003\uvir003_nonzero_gradient_force_local.py
# expect: PASS_NONZERO_GRADIENT_FORCE_LOCAL
```

Outputs:

- `outputs/uvir003_nonzero_gradient_force_local_summary.json`
- `outputs/uvir003_nonzero_gradient_force_local_samples.csv`

## Next (remaining alpha.10)

1. **Declared** perturbative-unitarity / EFT-validity criterion with explicit
   scope (high-\(q\) Green proxy + this local force sector) — **not** “theory closed”.  
2. Optional: feed the local anisotropic force vertex as a source into the
   multi-slice FRW Green proxy.
