# WAK-001 Stage 2 - zero-background quadratic factorization

**Date:** 2026-08-04
**Gate status:** Open
**Result:** `PASS_WAK001_ZERO_BACKGROUND_QUADRATIC_FACTORIZATION_TEMPLATE`
**Physical wake law:** Not yet derived
**Hold:** `HOLD_MICROSCOPIC_MODE_IDENTITY_AND_CUBIC_CONSTRAINT_COMPLETION`

## Question

Does the local Route-II trial density itself justify a block-diagonal
quadratic `W` sector on the explicitly declared zero-wake background, or would
that still be an unsupported zero-mixing assumption?

The audited density is

```text
L_W = (Z_W/2) (U^mu nabla_mu W)^2
      - (Z_W c_W^2/2) h^{mu nu} nabla_mu W nabla_nu W
      - (M_W^2/2) W^2,

h^{mu nu} = g^{mu nu} + U^mu U^nu,
J_W = 0.
```

This density is a local calculation family, not an adopted ITSM wake action.
The unit-frame constraint belongs to the parent `U` sector once and is not
duplicated inside `S_W`.

## Declared expansion

On a local Minkowski patch, set

```text
g^{mu nu} = eta^{mu nu} + epsilon delta g^{mu nu},
U^mu       = Ubar^mu + epsilon delta U^mu,
Ubar^mu    = (1,0,0,0),
W          = epsilon w,
Wbar       = 0,
nabla Wbar = 0.
```

The exact expansion has no zeroth- or first-order `W` contribution. Its
quadratic coefficient is

```text
L_W^(2) = (Z_W/2) (partial_t w)^2
          - (Z_W c_W^2/2) |grad w|^2
          - (M_W^2/2) w^2.
```

It contains no `delta g` or `delta U`. The executable audit differentiates
`L_W^(2)` with respect to five `w`/derivative variables and fourteen
metric/frame perturbations. All 70 cross derivatives vanish.

Therefore zero quadratic mixing is **derived for this declared background and
trial density**. It is not assumed.

## Where coupling returns

Metric and frame perturbations enter `L_W^(3)`. Representative derivatives
are

```text
partial L_W^(3) / partial(delta U^0)
  = -Z_W (c_W^2 - 1) (partial_t w)^2,

partial L_W^(3) / partial(delta g^{00})
  = -(Z_W c_W^2/2) (partial_t w)^2,

partial L_W^(3) / partial(delta g^{0i})
  = -Z_W c_W^2 (partial_t w)(partial_i w).
```

Thus the free quadratic block does not imply nonlinear decoupling. The lapse,
shift and frame constraints must be expanded and eliminated again before any
cubic stability, strong-coupling or physical wake statement.

## Negative controls

The audit also verifies that the factorization is not generic:

1. A background with `nabla_0 Wbar = B_t != 0` produces quadratic
   fluctuation/frame mixing proportional to
   `-2 B_t Z_W (c_W^2 - 1)` in the selected probe.
2. Adding an explicit bilinear `g_mix W psi` produces the off-diagonal
   quadratic Hessian entry `g_mix`.

Any future nonzero background, source or interaction therefore requires a new
joined Hessian calculation. The present result cannot be carried over by
analogy.

## Reproducible result

Run:

```powershell
python Analysis\WAK\WAK-001\wak001_zero_background_factorization.py
```

The deterministic summary is
`Analysis/WAK/WAK-001/outputs/wak001_zero_background_factorization_summary.json`.
Its SHA-256 after two consecutive runs was
`D969D2BC8E8EC12E302B13F20AB15271BFCD70779A858074A5438AAF92B5DA62`.

## Scientific boundary and next action

This audit conditionally closes only the question of W-dependent quadratic
mixing for `Wbar=0`, `nabla Wbar=0`, `J_W=0`, and no explicit bilinear
cross-sector operator. It does not establish that `W` is microscopically
independent of `Phi`, `U` or `psi`, and it does not construct the complete
UVIR-plus-W parent Hessian.

Next derive or reject the microscopic identity of `W`. If the independent
mode survives, construct the cubic parent constraint system before proposing
a source, damping mechanism or nonlinear observable.
