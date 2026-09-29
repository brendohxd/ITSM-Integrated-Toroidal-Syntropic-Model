# R4C1-T2P1: action-derived periodic-force contrast contract

Date: 2026-09-29. Owner: Master Test 2 / conditional R4C1-v1.
This is a fixed-background, aligned-frame `T^3` necessary-condition and
numerical-method audit. It does **not** select R4C1 as the canonical parent,
solve its perturbed Einstein/frame/dust constraints, prove a quasistatic
error bound, derive the projection factor, or close Tests 1–3.

## Frozen sources and interpretation

Pin the unchanged R4C1 action, first variation, C1 force derivation, B1
parameter literal, Test-2 topology addendum, Tests-1–3 disposition, and master
test programme by SHA-256 before calculation. The source hashes, in that order,
are:

```
81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3
4834ea7517fd0393015e1d94fa1c130d84e2796b0ae1667712c2b5cf4653692c
c4af4084ae83f7ed70d63f44700a0ebfc2c394ed7d79cd0061e3efe279b7dc0a
1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f
a4f251ff3d751a60ff4130d61a060f199c825604f877e1aeb5dd5515db8f317c
b999dff43b81f1dc73a9f584bd1c6a1856c559fe15b896719aa82300c8327883
81c7138568d44fd3197b88cb21efe67b17c406ada941f7ff778c2f8821ae074b
```

Do not import or execute an old receipt-producing `main()` to obtain B1
parameters. Existing receipts remain immutable. The earlier conditional
`b=0`/unregulated Test-2 result is not silently substituted for R4C1's
`b>0` action.

## Analytic obligations

Use flat FRW `ds^2=-dt^2+a(t)^2 d\mathbf x^2` on a cubic comoving torus,
period `2*pi` per coordinate, with aligned fixed `n=partial_t`. Keep
`K_Q,A,b,beta` constant and positive, impose the dust constraint so
`T_m=-rho`, and eliminate `z=-Delta psi` only with its frozen boundary
convention. Derive from the first-order current, without guessing a source,

```
E_psi = -K_Q*a^-3*d_t(a^3*d_t psi)
        +3*A*a^-3*div_x(|grad_x psi| grad_x psi)
        -b*a^-4*Delta_x^2 psi -beta*rho = 0.
```

Check the homogeneous limit against B1's equation. Integrate over `T^3`:
the two spatial terms vanish and the exact mean equation is
`K_Q*a^-3*d_t(a^3*d_t mean(psi))=-beta*mean(rho)`. Hence a fully static,
fixed-frame solution with positive mean dust is impossible. This is a
scoped zero-mode obstruction, not an all-formulation no-go. Subtract the
mean equation before forming a density-contrast equation; do not insert
positive total mass into periodic Poisson/force equations.

At the declared snapshot `a=1`, neglect the **contrast** time derivative
and freeze metric/frame responses only for the numerical method control:

```
3*A*div(|grad psi| grad psi)-b*Delta^2 psi=beta*delta_rho,
mean(psi)=mean(delta_rho)=0.
```

Record those omitted terms as unbounded errors. The spatial functional is
`J=sum[A|grad psi|^3+b(Delta psi)^2/2+beta delta_rho psi]` up to a positive
cell-volume factor. Verify its gradient against an independent directional
finite difference and its weak Euler form; retain `b`, its sign, and the
harmonic/mean mode. Do not claim a continuum existence theorem or a physical
periodic galaxy solution from a grid minimizer.

## Frozen numerical probe and acceptance rules

- Use B1 `A=2/7`, `b=5/11`, `beta=2/5`, `K_Q=3`, at reference `a=1` and
  homogeneous dust density `rho_bar=1/5`. On the cubic `2*pi` torus prescribe
  **before solution** `delta_rho=(cos x+2 cos y+3 cos z)/50`.
  Thus `rho_bar+delta_rho>=2/25>0`, while `mean(delta_rho)=0`.
- Use odd cubic pseudospectral grids `N=17,25,33`, a zero-mean gauge, a
  convex-energy minimization with analytic gradient, and the exact `A=0`
  linear solution as a control. Preserve the grid values and source; no
  coefficient, source, tolerance or topology retuning after seeing output.
- For each grid require finite solution, positive `b`, mean `psi` below
  `1e-12`, and normalized strong collocation Euler residual below `1e-5`
  relative to `beta*||delta_rho||_2`.
- Require each independent weak residual against `cos x,cos y,cos z` and
  `sin x,sin y,sin z` below `1e-5` relative to the global source scale
  `beta*rms(delta_rho)*rms(test_function)+1e-12`.
- Require the three normalized fundamental cosine coefficients at `N=25`
  and `N=33` to agree relatively within `5e-3` (floor `1e-12`). This is a
  convergence diagnostic, **not** a continuum error bound.
- The analytic `A=0` spectral solution must have a normalized residual below
  `1e-10`. At the nonlinear solution, deliberately omitting the `b` term
  must leave normalized residual above `1e-2`. A nonzero full-density mean
  must fail the static zero-mode compatibility test exactly.
- On the `N=17` grid, verify a central directional finite difference of the
  discrete energy against the analytic gradient with relative discrepancy
  below `1e-5`, using the off-shell probe
  `psi_probe=0.03*(cos x+sin(2y)+cos(3z))`, one seeded zero-mean direction
  (seed `311`), and step `1e-6` in a direction of Euclidean norm one.

Any failed check is retained as a failed attempt and diagnosed; never loosen
thresholds to force a PASS. A successful local receipt remains
`physics_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false`, and
`review_status=DEFERRED`. Canonical Test 2 additionally needs the full
metric/Euler response, controlled quasistatic/domain errors, a physical
periodic solution, Test 4's projection factor and Test 5's admissibility.
