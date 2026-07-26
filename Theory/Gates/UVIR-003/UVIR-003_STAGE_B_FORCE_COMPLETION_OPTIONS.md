# UVIR-003 Stage B force-completion options

Date: 2026-07-26  
Branch: `recovery/v12-core-architecture`  
Scope: bounded operator comparison and recorded Track A selection

## Decision

The minimal evolving-frame completion recommended for explicit derivation is

```text
Delta_U psi := D_mu D^mu psi
             = h^{mu nu} nabla_mu nabla_nu psi + theta Q,
```

where

```text
D_mu := h_mu^nu nabla_nu,
theta := nabla_mu U^mu,
Q := U^mu nabla_mu psi.
```

It is a generally covariant rest-space scalar, reduces to the Stage-A spatial
Laplacian for constant `U`, has a spatial second-derivative principal part and
annihilates a force field homogeneous on the aether rest space. In
aether-unitary ADM on a hypersurface-orthogonal branch, it is the intrinsic
leaf Laplacian.

The comparison established that there is no option that simultaneously:

1. preserves the exact asymptotic `Y^(3/2)` law at `Y=0`;
2. is analytic at `Y=0`; and
3. supplies the ordinary zero-background vertices required by a standard
   cosmological scattering expansion.

Track A was subsequently selected. The rest-space Laplacian is adopted for
explicit derivation, the exact `Y^(3/2)` functional is retained, and its
ordinary perturbative force analysis is assigned to a declared local
nonzero-gradient background.

This is `TRACK_A_SELECTED`.

UVIR-003 remains in progress and MAT-001 remains blocked.

## 1. Regulator identities

Let

```text
h_mu^nu = delta_mu^nu + U_mu U^nu,
a^mu = U^nu nabla_nu U^mu.
```

For a scalar,

```text
D_mu D^mu psi
  = h^{mu nu} nabla_mu nabla_nu psi + theta Q.
```

The covariant divergence of the projected gradient is instead

```text
nabla_mu(h^{mu nu} nabla_nu psi)
  = D_mu D^mu psi + a^mu D_mu psi.
```

The acceleration term distinguishes two otherwise plausible completions.
Both reduce to the ordinary spatial Laplacian in the constant flat frame, but
they define different nonlinear lapse and aether vertices.

On flat FRW with a homogeneous `psi(t)`,

```text
h^{mu nu} nabla_mu nabla_nu psi = -3 H psidot,
theta Q = +3 H psidot.
```

The terms cancel in `D_mu D^mu psi`. The projected Hessian alone therefore
does not represent a purely spatial regulator on an evolving homogeneous
background.

## 2. Regulator comparison

### 2.1 Rest-space Laplacian

```text
Delta_U psi = D_mu D^mu psi.
```

Assessment:
`RECOMMENDED_FOR_EXPLICIT_DERIVATION_NOT_ADOPTED`.

Advantages:

- generally covariant under spacetime diffeomorphisms;
- invariant under the force-field shift;
- reduces exactly to the declared Stage-A operator;
- does not alter the homogeneous FRW force background;
- in unitary ADM, introduces no lapse-gradient term into `Delta_U` itself;
- retains a purely spatial second-derivative principal part.

The next calculation would insert

```text
L_reg = -gamma/(2 M_*^2) (D_mu D^mu psi)^2
```

into the nonlinear ADM action and derive its cubic lapse, shift, curvature and
force vertices. That calculation has not been performed here.

### 2.2 Projected spacetime Hessian

```text
Delta_H psi = h^{mu nu} nabla_mu nabla_nu psi
            = D_mu D^mu psi - theta Q.
```

Assessment: `NOT_RECOMMENDED`.

It is covariant and has the correct constant-frame limit, but on homogeneous
FRW it equals `-3 H psidot`. Squaring it adds a regulator contribution to the
homogeneous background and mixes the expansion directly with the force time
kinetic term. That is not the behavior declared for the Stage-A spatial
regulator.

### 2.3 Spacetime divergence of the projected gradient

```text
Delta_div psi = nabla_mu(h^{mu nu} nabla_nu psi)
              = D_mu D^mu psi + a^mu D_mu psi.
```

Assessment: `VIABLE_BUT_NONMINIMAL`.

This divergence-form choice is covariant and also annihilates a homogeneous
force field. However, it adds an acceleration coupling. In aether-unitary ADM,
`a_i=D_i ln N`, so it changes the nonlinear lapse-gradient vertices relative
to the minimal rest-space Laplacian. No present recovery requirement selects
that additional coupling.

## 3. Why the exact zero-gradient branch is not a Taylor vertex

At the selected background,

```text
Y = epsilon^2 Y2
```

and therefore

```text
Y^(3/2) = |epsilon|^3 Y2^(3/2).
```

The functional is a well-defined classical nonlinear operator. It is twice
differentiable with respect to the spatial gradient at the origin, but its
third derivative is not a background-independent trilinear form. The exact
branch can be retained in nonlinear boundary-value calculations; it cannot be
silently substituted for an ordinary analytic cubic Feynman vertex about
`Y=0`.

## 4. Controlled options for `Y^(3/2)`

### Track A: preserve the exact IR branch

Keep the exact operator and expand around a nonzero local spatial gradient.
For a background magnitude `v>0`, with a parallel fluctuation `x` and squared
transverse fluctuation `p_perp^2`,

```text
|v + epsilon grad(pi)|^3
 = v^3
 + 3 v^2 epsilon x
 + (3/2) v epsilon^2 (2 x^2 + p_perp^2)
 + epsilon^3 (x^3 + (3/2) x p_perp^2)
 + (3/8) epsilon^4 p_perp^4/v
 + O(epsilon^5).
```

This is an ordinary local expansion and preserves the exact force operator.
Its quartic coefficient is singular as `v -> 0`, and the background selects a
spatial direction. It is therefore suitable for a local weak-field response
calculation, not for an isotropic zero-gradient FRW scattering amplitude.

Track A means:

- preserve the intended asymptotic low-acceleration law;
- perform force-sector perturbation theory on a declared nonzero-gradient
  local background;
- do not label that result the homogeneous cosmological `2-to-2` amplitude.

### Track B1: smooth completion with a generated linear term

For a dimensionless crossover `sigma>0`, define

```text
F_B1(Y) = (Y+sigma^2)^(3/2) - sigma^3.
```

Near the origin,

```text
F_B1(Y)
 = (3/2) sigma Y
 + (3/8) Y^2/sigma
 - (1/16) Y^3/sigma^3
 + O(Y^4).
```

This is analytic and supplies quadratic spatial stiffness. The generated
linear `Y` term dominates as `Y -> 0`, so it changes the exact asymptotic
square-root branch and reverses the explicit Stage-A decision not to insert a
canonical spatial term.

### Track B2: smooth completion with the linear term subtracted

Define

```text
F_B2(Y)
 = (Y+sigma^2)^(3/2) - sigma^3 - (3/2) sigma Y.
```

Then

```text
F_B2(Y)
 = (3/8) Y^2/sigma
 - (1/16) Y^3/sigma^3
 + O(Y^4).
```

This is analytic and does not generate a canonical `Y` term. Its leading
zero-background force interaction is quartic in spatial gradients, so it can
enter a standard `2-to-2` calculation. It still introduces a new crossover
scale and replaces the exact deep-IR `Y^(3/2)` law by `Y^2`.

## 5. Required architecture choice

The two scientifically coherent paths are:

```text
Track A
  preserve exact Y^(3/2)
  -> nonzero-gradient local force calculation
  -> no homogeneous force-sector S-matrix claim

Track B
  preserve homogeneous analytic perturbation theory
  -> select B1 or B2 and sigma
  -> re-test the modified deep-IR force law
```

The present audit recommends the rest-space Laplacian for the regulator, but
does not choose between these `Y` tracks. Selecting one changes what the
theory asserts in the deep IR and must be an explicit architecture decision.

No full force-inclusive `J2`, quartic Schur complement, physical `2-to-2`
amplitude or cutoff is claimed.

## 6. Next bounded calculation

After the architecture choice:

1. derive `(D_mu D^mu psi)^2` in aether-unitary ADM through cubic order;
2. insert the selected `Y` prescription;
3. reproduce the existing flat and FRW limits;
4. extract the force-inclusive quadratic lapse/shift source `J2`;
5. form the quartic Schur complement and physical scalar projection.

## 7. Reproduction

Run from the repository root:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_force_completion_options.py
```

Generated record:

```text
Analysis/UVIR/UVIR-003/outputs/
  uvir003_force_completion_options_summary.json
```

Expected terminal status:

```text
Rest-space Laplacian identities: VERIFIED
Smooth-completion series: VERIFIED
Nonzero-gradient singular limit: VERIFIED
Rest-space regulator: TRACK_A_ADOPTED
Y^(3/2) treatment: EXACT_NONZERO_GRADIENT_LOCAL_TRACK
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: TRACK_A_SELECTED
```
