# R4C1-G3E: evolving high-momentum zero-sector reduction

Date: 2026-09-30. Master Test 1 / conditional R4C1-v1 / G3.
Frozen before calculation. Review DEFERRED, physics_pass=false, gate effect NONE.

## Scope and owning evidence

Resolve the distinction identified by the [G3Z report](RES001_R4C1_G3_ZERO_INNER_REPORT_2026-09-30.md):
its fixed-event lambda pencil is not the evolving reduced equation. Use
G3S's full canonical G,W,R and background flow, keeping time derivatives
at fixed comoving k. The action, G3 coefficients, background initial data,
earlier receipts and all substantive parent holds remain unchanged.

Derive the leading large-k *low-frequency* sector, not a uniform theorem
for arbitrary fast-wave initial data. Eliminating propagating modes selects
a formal well-prepared slow branch; omitted fast initial data are not claimed
absent physically. Require 0<eta<=1,a,C,H,rho_m>0,k!=0 and S1's auxiliary rank
domain. No inverse through eta=0. Formal k->infinity is not EFT validity.

## Calculation

1. Expand the full differential equations xddot+G xdot+W x=0 at fixed k.
   Let x_W=X(t); four propagating coordinates start at Y_i(t)/k, and
   x_psi=F1/k+F2/k^2+F3/k^3. Retain dummy next-order propagating amplitudes
   Z_i/k^2 so their cancellation, rather than their deletion, must establish
   closure of the leading W equation.
2. Solve the force equations in descending k powers and the leading
   propagating equations algebraically. Check all higher-power residuals.
   Differentiate the resulting coefficients with the **new G3 background
   flow**, including a(t), before extracting the W equation at O(1).
   Require the leading equation not to depend on the dummy Z_i. Record
   its derivative order, normalization and rank restrictions; report any
   failed closure instead of forcing an ODE.
3. As an independent control, freeze elimination coefficients before
   differentiation. Its frequency polynomial must recover G3Z's inner
   pencil. Reject omission of the coefficient derivatives if the evolving
   result differs. Do not replace lambda with d/dt as the derivation.
4. Reconstruct q=R x and qdot, then use S1's **generic** auxiliary solutions
   with G3 coefficients. Check dust normalization, z=-delta Delta and
   density delta rho=C^4 delta epsilon+4 beta rho_m delta psi. For the
   leading low-frequency density/velocity response use X=Z/k and derive
   finite large-k maps, reporting any divergence or degeneracy. The
   reconstructed density is not defined by an inserted Poisson/source law.
5. Integrate the derived two-dimensional slow fundamental matrix together
   with its background for all six frozen G3 eta values on [0,4], with
   DOP853/Radau, rtol=1e-11,atol=1e-13 and 101 sample times. Verify normalized
   background agreement with pinned G3 trajectories (<1e-8), two-method
   slow-transfer agreement (<1e-7), and the determinant/Liouville identity
   (<1e-7). These are finite-time accuracy checks of the reduced branch,
   not convergence of the full PDE or an all-sector stability pass.

## Integrity and exclusions

Pin all direct and inherited sources before computation. Preserve each
failure and its scope. New numbered outputs only; refuse existing targets;
pure replay and byte-identity check, no earlier receipt-producing main().
Do not alter parameter values, modes, tolerances or graph norms to pass.
No observer fit, PDF work, provider dispatch, commit, push or publication.

Inherit R9-MT1-VARIATION/B1/G1/S1/S2/S3/G2/G3/G3S/G3Z and their restrictions.
Review deferred, Rule9_cleared=false. Canonical Tests 1–3 HOLD_SUBSTANTIVE;
MAT-001 BLOCKED,UVIR-003 IN_PROGRESS,K_Q NOT_DERIVED,V NOT_COMPUTED,
Stage4A CLOSED,TOP-X4 unchanged. Full mixed-regularity IVP, singular modes,
physical EFT cutoff, healthy GR, nonlinear force and blind matching remain
required independently of any locally passing reduced calculation.
