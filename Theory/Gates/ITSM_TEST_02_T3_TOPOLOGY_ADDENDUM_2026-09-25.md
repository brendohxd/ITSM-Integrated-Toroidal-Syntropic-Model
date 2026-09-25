# Test 2: explicit periodic T3 addendum

Date: 2026-09-25. Scope: conditional static weak-field mathematics.
Gate effect: NONE. Independent Rule-9 review: NOT_COMPLETED.

This follow-up was prompted by the user's topology question. Its examples
were worked out analytically before execution; it is not an independently
blinded test. Preserve the original 11/11 receipt and its narrower local
scope. Neither that receipt nor this one completes canonical Test 2.

## Registered calculations

Use a flat cubic T3 snapshot with dimensionless angular coordinates of
period 2*pi, physical positions r=L*x, and S_Q=0. This is a special case
within flat rectangular T3, not a derivation of the actual cosmological
metric from topology alone. A nonzero curl in this allowed case is sufficient
to reject a universal pointwise formula.

1. Take Phi_N=epsilon*(cos x+2 cos y), epsilon>0. Its Laplacian is
   -epsilon*(cos x+2 cos y), periodic and zero mean. It describes a density
   contrast. A sufficiently positive homogeneous density makes total density
   nonnegative. Do not substitute that homogeneous mode into the periodic
   Poisson equation.
2. On a patch where grad Phi_N is nonzero, test the proposed gradient
   v=k*grad Phi_N/|grad Phi_N|^(1/2), k>0. Verify |v|v=k^2 grad Phi_N and
   the associated sourced divergence. Calculate curl v, including the exact
   point x=y=pi/4, epsilon=k=1. Nonzero curl means this vector cannot be the
   gradient of any scalar even locally; periodicity cannot repair it.
3. For phi=sin x+(b/2)sin(2x), verify mean grad phi=0, but the derivative
   at b=0 of mean(|grad phi| grad phi) is nonzero. Split the elementary
   integral at the zeros of cos x, retaining the absolute-value sign.
4. Verify the nonzero-mode Fourier decomposition for a transverse vector.
   For wavevector n!=0, H_n=i*n cross F_n/|n|^2 has i*n cross H_n=F_n.
   Separately retain the constant mode. A periodic curl has zero mean by
   integration of derivatives over a period; a nonzero constant field cannot
   be represented by that curl.

## Required interpretation

For the conditional source equations, equality of divergences implies

```
F = |grad phi| grad phi/a0 - (Cm/CIR) grad Phi_N
  = curl H + h0,        h0 = <F>.
```

On a flat torus h0 is the harmonic constant vector. It is a nonlinear flux
mode determined by the solution, not permission to add a nonperiodic linear
scalar potential or freely fit a constant acceleration. Zero-mean scalar
gradient does not force zero-mean nonlinear flux. A curved T3 requires the
metric-dependent Hodge formulation; topology alone does not supply a flat
metric or the constant-vector formula.

For S_Q!=0, the simple difference F is not divergence-free. A separately
derived zero-mean exchange-source contribution must first be subtracted;
the current-to-scalar map is still absent.

A locally compensated, approximately spherical overdensity can retain the
spherical control in an appropriately small patch. No global spherical
symmetry of T3, quantitative error bound, physical periodic galaxy solution,
or universal algebraic force law follows from that control. Even in exact
spherical symmetry C_obs=Cm^(3/2)/sqrt(CIR) is conditional; neither topology
nor these checks derives C_obs=2/3.

## Stop and publication boundary

Any failed identity must be reported and investigated without changing its
meaning to obtain PASS. Keep the primary 11/11 receipt unchanged. Correct
the working compact-source manuscript equations if the harmonic-mode
omission is confirmed; leave frozen historical and released artifacts intact.
The source-only correction does not rebuild or validate existing PDFs.

All canonical statuses remain: physics_pass=false, gate_effect=NONE,
MAT-001 BLOCKED, UVIR-003 IN_PROGRESS, K_Q NOT_DERIVED, V NOT_COMPUTED,
Stage4A CLOSED. The parent action, full weak-field metric, exchange map and
periodic physical solution remain open.
