# UVIR-003 Stage B nonlinear ADM action provenance

Date: 2026-07-26  
Branch: `recovery/v12-core-architecture`  
Scope: nonlinear action provenance before the cosmological quartic reduction

## Decision

The exact nonlinear aether-unitary ADM parent action for the
gravity--aether--condensate--alignment block is fixed and reproduces both the
verified FRW minisuperspace action and the complete finite-wavenumber
quadratic lapse/shift constraint data.

This is
`PASS_G_U_PHI_ALIGNMENT_ACTION_PROVENANCE`.

The full cosmological quadratic constraint source `J2` is not yet derivable
from the complete declared Stage-A theory. The force regulator `Delta_U` was
defined only in the constant hypersurface-orthogonal frame and still lacks a
generally covariant completion on the evolving foliation. In addition, the
`Y^(3/2)` force operator is non-analytic about the selected zero-gradient
background and does not define an ordinary cubic Taylor vertex there.

This is
`HOLD_FORCE_SECTOR_NONLINEAR_COMPLETION_REQUIRED`.

UVIR-003 remains in progress and MAT-001 remains blocked.

## 1. Exact parent block

In aether-unitary gauge,

```text
U^mu = n^mu,
N = 1 + delta_N,
N_i = partial_i beta,
h_ij = a^2 exp(2R) delta_ij.
```

The exact gravity-plus-aether ADM density is

```text
N sqrt(h)/2 [
  M_P^2 R^(3)
  + (M_P^2-M_U^2 c13) K_ij K^ij
  - (M_P^2+M_U^2 c2) K^2
  + M_U^2 c14 a_i a^i
].
```

For the condensate amplitude `varrho` and phase `theta`,

```text
L_Phi = N sqrt(h) [
  {n(varrho)^2 + varrho^2 n(theta)^2}/2
  - h^ij{D_i varrho D_j varrho
          + varrho^2 D_i theta D_j theta}/2
  - V(varrho)
].
```

The exact current projection is

```text
J_Phi^mu = -varrho^2 grad^mu(theta),
h_mn J_Phi^m J_Phi^n
  = varrho^4 h^ij D_i(theta) D_j(theta).
```

Hence

```text
L_align =
  -N sqrt(h) zeta_align varrho^4
   h^ij D_i(theta)D_j(theta)/2.
```

This establishes a nonlinear parent action for the
`g+U+Phi+alignment` block without inferring higher-order terms from the
quadratic reduced action.

## 2. FRW provenance

Define

```text
c13 = c1+c3,
c14 = c1+c4,
c123 = c1+c2+c3,
M_cos^2 = M_P^2 + M_U^2(c1+3c2+c3)/2.
```

The ADM coefficients obey

```text
(M_P^2-M_U^2 c13)
+ 3(-M_P^2-M_U^2 c2)
= -2 M_cos^2.
```

The exact homogeneous action therefore reduces to

```text
L_bg =
  -3 M_cos^2 a adot^2/N
  + a^3(rho_dot^2+rho^2 Theta_dot^2)/(2N)
  - N a^3 V(rho),
```

which is the previously verified FRW minisuperspace action.

Expanding the homogeneous lapse and using

```text
3 M_cos^2 H^2
= (rho_dot^2+rho^2 mu^2)/2 + V
```

gives the quadratic Lagrangian coefficient `-V delta_N^2`, or constraint
matrix entry `C_NN=-2V` before adding the acceleration term.

## 3. Finite-wavenumber quadratic provenance

With `Sigma=q_phys^2 beta`, the exact parent block gives

```text
C = [[M_U^2 c14 q_phys^2 - 2V,  2 M_cos^2 H],
     [2 M_cos^2 H,              -M_U^2 c123]].
```

It also gives

```text
J_N =
  6 M_cos^2 H R_dot
  + 2 M_P^2 q_phys^2 R
  - (V_rho+rho mu^2) delta_rho
  - rho_dot delta_rho_dot
  - rho^2 mu vartheta_dot,

J_Sigma =
  -2 M_cos^2 R_dot
  - rho_dot delta_rho
  - rho^2 mu vartheta.
```

These expressions exactly match the independent finite-`q` quadratic
reduction. The alignment term likewise reproduces the phase-gradient
stiffness

```text
rho^2(1+zeta_align rho^2).
```

The quadratic calculation therefore has a verified nonlinear parent action
within this block.

## 4. Why the full `J2` is on hold

The physical scalar `2-to-2` calculation cannot silently omit the force
sector. Although the constant force background makes its quadratic mode
factorize, nonlinear metric and constraint couplings begin at higher order.

Two declarations are missing:

1. `Delta_U` needs a generally covariant nonlinear completion on the evolving
   aether foliation. Stage A explicitly deferred acceleration, curvature and
   commutator terms.
2. At the zero-gradient background, write `Y=epsilon^2 Y2`. Then

   ```text
   Y^(3/2) = |epsilon|^3 Y2^(3/2).
   ```

   This is even under `epsilon -> -epsilon`, whereas a nonzero homogeneous
   cubic Taylor polynomial is odd. It therefore does not supply an ordinary
   analytic cubic vertex about that background. A non-analytic perturbative
   prescription or a smooth microscopic completion must be declared.

Without those choices, a purported full `J2`, quartic Schur complement or
physical cutoff would depend on an action that has not been specified.

## 5. Next calculation

The bounded sequence is now:

1. choose and derive the nonlinear covariant completion of `Delta_U`;
2. declare a controlled treatment or smooth completion of `Y^(3/2)` at
   `Y=0`;
3. expand the completed scalar ADM action through cubic order and extract
   the quadratic lapse/shift source `J2`;
4. form `-J2^T C^(-1)J2/2`, add the direct quartic contact block and project
   onto the regular physical scalar basis;
5. only then construct the gauge-regular `2-to-2` amplitude and state a
   unitarity criterion.

## 6. Reproduction

Run from the repository root:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_nonlinear_adm_action_provenance.py
```

Generated record:

```text
Analysis/UVIR/UVIR-003/outputs/
  uvir003_nonlinear_adm_action_provenance_summary.json
```

The calculation reports:

```text
Nonlinear g+U+Phi+alignment ADM parent action: VERIFIED
FRW minisuperspace provenance: VERIFIED
Finite-q quadratic C and J1 provenance: VERIFIED
Full cosmological J2:
  HOLD_FORCE_SECTOR_NONLINEAR_COMPLETION_REQUIRED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_G_U_PHI_ALIGNMENT_ACTION_PROVENANCE
```
