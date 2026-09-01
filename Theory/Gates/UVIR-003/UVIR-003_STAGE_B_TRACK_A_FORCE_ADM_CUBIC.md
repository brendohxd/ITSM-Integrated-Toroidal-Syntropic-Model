# UVIR-003 Stage B Track A force ADM expansion

Date: 2026-07-26  
Branch: `recovery/v12-core-architecture`  
Scope: adopted rest-space regulator and force-sector constraint source

## Decision

Track A is selected.

The force action used for the next derivation is

```text
L_psi =
  K_Q Q^2/2
  - A Y^(3/2)
  - gamma (D_mu D^mu psi)^2/(2 M_*^2).
```

The evolving-frame regulator is now defined by

```text
Delta_U psi := D_mu D^mu psi.
```

The exact `Y^(3/2)` operator is retained. Its ordinary perturbative force
analysis is assigned to a declared local nonzero-gradient background rather
than replaced by a smoothing at the homogeneous origin.

The homogeneous zero-gradient force action has now been expanded through
direct quartic order. Its quadratic lapse/shift source is derived.

This is
`PASS_FORCE_SECTOR_J2_COMPONENT`.

The complete `g+U+Phi+alignment+psi` source has not yet been assembled, and no
physical `2-to-2` amplitude or cutoff is claimed. UVIR-003 remains in progress
and MAT-001 remains blocked.

## 1. ADM setup

On the flat-FRW, aether-unitary scalar branch, use

```text
U^mu = n^mu,
N = 1 + delta_N,
N_i = partial_i beta,
h_ij = a^2 exp(2R) delta_ij,
psi = psi_bar + pi,
partial_i psi_bar = 0.
```

The exact force building blocks are

```text
Q =
  [pi_dot
   - a^-2 exp(-2R) partial_i beta partial_i pi]/N,

Y =
  a^-2 exp(-2R) partial_i pi partial_i pi,

D_mu D^mu psi =
  a^-2 exp(-2R)
  [partial^2 pi + partial_i R partial_i pi].
```

The rest-space Laplacian contains no lapse or shift. Its principal derivative
remains spatial. The lapse enters the regulator only through the volume
factor `N sqrt(h)`.

## 2. Quadratic force action

Per unit comoving coordinate volume,

```text
L_psi^(2) =
  a^3 K_Q pi_dot^2/2
  - gamma (partial^2 pi)^2/(2 M_*^2 a).
```

This reproduces the previous factorized `z=2` force branch:

```text
omega^2 = gamma k_phys^4/(K_Q M_*^2).
```

The earlier zero-gradient quadratic result is therefore preserved by the
nonlinear completion.

## 3. Cubic force action

Define

```text
L := partial^2 pi,
G := partial_i R partial_i pi,
B := partial_i beta partial_i pi.
```

The `Q^2` contribution is

```text
L_Q^(3) =
  (a^3 K_Q/2)(3R-delta_N) pi_dot^2
  - a K_Q pi_dot B.
```

The adopted regulator contributes

```text
L_reg^(3) =
  - gamma/(2 M_*^2 a)
    [(delta_N-R)L^2 + 2LG].
```

The exact IR operator contributes

```text
L_Y^(3) = -A (partial_i pi partial_i pi)^(3/2).
```

At the homogeneous zero-gradient origin this last expression is a classical
homogeneous nonlinear functional, not a background-independent trilinear
Taylor vertex. It contains no lapse, shift or curvature perturbation at cubic
amplitude order.

## 4. Force contribution to `J2`

Before converting the scalar shift to a finite-wavenumber normalized
constraint variable, the lapse component is

```text
J2_deltaN,force =
  -a^3 K_Q pi_dot^2/2
  -gamma (partial^2 pi)^2/(2 M_*^2 a).
```

Dividing by `a^3` and using the physical leaf Laplacian gives

```text
J2_deltaN,force / a^3 =
  -K_Q pi_dot^2/2
  -gamma [D_phys^2 pi]^2/(2 M_*^2).
```

The scalar-shift term is

```text
-a K_Q pi_dot partial_i beta partial_i pi.
```

After spatial integration by parts, its source is

```text
J2_beta,force =
  a K_Q partial_i(pi_dot partial_i pi).
```

The regulator has no scalar-shift source:

```text
J2_beta,reg = 0.
```

At the zero-gradient origin,

```text
J2_Y = 0.
```

This last zero means only that the leading exact `Y^(3/2)` functional is
constraint independent at cubic amplitude order. It does not turn that
functional into an analytic three-point vertex.

## 5. Direct quartic force block

The symbolic audit also retains the direct fourth-order action because it is
required alongside the future constraint Schur complement.

For `Q^2`,

```text
L_Q^(4) =
  (a^3 K_Q/2)
  [(9R^2/2 - 3R delta_N + delta_N^2) pi_dot^2
   + 2(delta_N-R)a^-2 pi_dot B
   + a^-4 B^2].
```

For the regulator,

```text
L_reg^(4) =
  -gamma/(2 M_*^2 a)
  [(R^2/2-delta_N R)L^2
   +2(delta_N-R)LG
   +G^2].
```

The exact IR operator gives

```text
L_Y^(4) =
  -A delta_N (partial_i pi partial_i pi)^(3/2).
```

These are direct ADM terms only. The reduced quartic action additionally
requires

```text
-J2^T C^(-1) J2/2
```

after the complete constraint source is assembled.

## 6. What has and has not advanced

Derived:

- a nonlinear covariant definition of the Stage-A regulator;
- its exact aether-unitary ADM form on the conformally flat scalar branch;
- the complete homogeneous zero-gradient force action through direct quartic
  order;
- the force-sector lapse and scalar-shift components of `J2`;
- preservation of the previous zero-gradient `z=2` quadratic limit.

Still open:

- assembly of these components with the cubic
  `g+U+Phi+alignment` constraint source;
- conversion of the quadratic shift source into the existing finite-`q`
  convolution convention;
- the complete quartic Schur complement and regular physical scalar
  projection;
- the separate nonzero-gradient local reduction of exact `Y^(3/2)`;
- the physical `2-to-2` amplitude, unitarity criterion and cutoff.

## 7. Next bounded calculation

The next calculation is to expand the already fixed nonlinear
`g+U+Phi+alignment` ADM parent action to cubic order, combine its lapse/shift
source with the force result above and form the complete finite-`q` `J2`
vector. Only then can the quartic Schur complement be evaluated.

The exact `Y^(3/2)` nonzero-gradient calculation remains a separate local
Track-A branch and must not be mislabeled as homogeneous FRW scattering.

## 8. Reproduction

Run from the repository root:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_track_a_force_adm_cubic.py
```

Generated record:

```text
Analysis/UVIR/UVIR-003/outputs/
  uvir003_track_a_force_adm_cubic_summary.json
```

Expected terminal status:

```text
Track A rest-space regulator: ADOPTED_FOR_DERIVATION
Force ADM expansion through quartic order: VERIFIED
Force-sector lapse/shift J2 component: VERIFIED
Exact Y^(3/2): RETAINED_NONANALYTIC_LOCAL_TRACK
Complete cosmological J2: NOT_YET_ASSEMBLED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_FORCE_SECTOR_J2_COMPONENT
```
