# UVIR-003 - Stage B time-dependent finite-q scalar ADM reduction

Date: 2026-07-26
Branch: `recovery/v12-core-architecture`
Status: **finite-q constraint elimination passed; low-q kinetic-rank hold**

## Executive result

The scalar calculation has advanced beyond the frozen-coefficient principal
symbol. For the declared two-derivative metric, independent aether and
canonical-condensate sectors, this subgate:

- expands the complete quadratic scalar action on the verified evolving
  flat-FRW branch;
- retains the background-dependent `q_phys^0`, `q_phys^2` and scalar-shift
  `q_phys^4` terms;
- retains the factorized force regulator at `q_phys^4`;
- eliminates the lapse and scalar momentum constraints at every
  `q_phys>0`;
- differentiates the reduced matrices along the background using
  `H_dot`, `rho_dot`, `rho_ddot`, `mu_dot` and
  `q_phys_dot=-H q_phys` for fixed comoving wavenumber;
- scans the kinetic inertia from `q_phys/H=10^3` down to `10^-3`.

The finite-wavenumber result is positive on the representative branch:
all 48,861 sampled reduced kinetic matrices have inertia
`3 positive, 0 negative`, and the constraint matrix remains nonsingular.

The strict low-wavenumber limit does not pass as a regular three-field
quadratic system. The exact on-shell reduced kinetic determinant is
proportional to `q_phys^2`, and one kinetic eigenvalue collapses as
`q_phys -> 0`. The representative scan fits the smallest eigenvalue to
`q_phys^2.00066`. At exactly zero wavenumber the reduced kinetic rank is two,
not three.

This is recorded as
`HOLD_KINETIC_RANK_LOSS_AT_Q_TO_ZERO`, not as a ghost. The variable
`Sigma=q_phys^2 beta` is a legitimate momentum-constraint variable for every
nonzero wavenumber but is not an independent exactly homogeneous
perturbation. A cubic action in the collapsing eigenbasis is required to
decide whether the approach to zero wavenumber is gauge-only or signals a
physical strong-coupling scale.

UVIR-003 remains in progress and MAT-001 remains blocked.

## 1. Scope and gauge

Use aether-unitary scalar gauge

```text
N = 1 + delta_N,
N_i = partial_i beta,
h_ij = a^2 exp(2 R) delta_ij,
U^mu = n^mu.
```

The condensate is

```text
Phi = [rho(t) + delta_rho]/sqrt(2)
      * exp{i[Theta(t) + vartheta]}.
```

Define

```text
q = q_phys = k/a,
Sigma = q^2 beta,
D_123 = M_U^2 c_123,
C_14 = M_U^2 c_14,
M = M_cos^2.
```

`Sigma` is used instead of `beta` because the scalar shift enters the
nonzero-wavenumber action through `q^2 beta`. The exactly homogeneous
`q=0` sector has different momentum-constraint and gauge content and must not
be obtained by declaring `Sigma` independent at `q=0`.

The background force field is constant. Its quadratic mode therefore remains
factorized:

```text
L_pi^(2) = K_Q pi_dot^2/2
           - gamma q^4 pi^2/(2 M_star^2).
```

The cubic `Y^(3/2)` force operator has no quadratic contribution at zero
background force gradient.

## 2. On-shell background identities

The calculation uses the verified background equations

```text
3 M H^2 = (rho_dot^2 + rho^2 mu^2)/2 + V,
H_dot = -(rho_dot^2 + rho^2 mu^2)/(2 M),
rho_ddot = -3 H rho_dot + rho mu^2 - V_rho,
mu_dot = mu(-3 H - 2 rho_dot/rho).
```

For a fixed comoving mode,

```text
q_dot = -H q.
```

No reservoir stress or charge-transfer perturbation is introduced. This is
consistent with the representative isolated-condensate branch, but it is not
a matter- or reservoir-coupled cosmological perturbation model.

## 3. Complete quadratic scalar constraint system

Per background volume `a^3`, write the quadratic Lagrangian as

```text
L^(2) = L_0 + z^T J + z^T C z/2,
z = (delta_N, Sigma)^T.
```

The exact constraint matrix is

```text
C = [[C_14 q^2 - 2 V,  2 M H],
     [2 M H,             -D_123]].
```

The source vector is

```text
J_N =
  6 M H R_dot + 2 M_P^2 q^2 R
  - (V_rho + rho mu^2) delta_rho
  - rho_dot delta_rho_dot
  - rho^2 mu vartheta_dot,

J_Sigma =
  -2 M R_dot - rho_dot delta_rho - rho^2 mu vartheta.
```

All lapse, shift and background-mixing terms are therefore retained through

```text
z = -C^(-1) J,
L_red^(2) = L_0 - J^T C^(-1) J/2.
```

The unconstrained part is

```text
L_0 =
  -3 M R_dot^2 - 18 M H R R_dot
  + (M_P^2 q^2 - 9 V) R^2
  + 3(rho mu^2 - V_rho) R delta_rho
  + 3 rho_dot R delta_rho_dot
  + 3 rho^2 mu R vartheta_dot
  + 2 rho mu delta_rho vartheta_dot
  + delta_rho_dot^2/2
  + rho^2 vartheta_dot^2/2
  + (mu^2 - V_rhorho - q^2) delta_rho^2/2
  - rho^2(1 + zeta_align rho^2)q^2 vartheta^2/2.
```

This expression uses the background Friedmann equation to simplify terms
that otherwise appear separately as `H^2`, enthalpy and potential
contributions.

## 4. Exact kinetic determinant

Let `K_red` be the velocity Hessian of `L_red^(2)` for

```text
v = (R_dot, delta_rho_dot, vartheta_dot).
```

The symbolic reduction gives

```text
det K_red =
  [2 M rho^2 (2 M - 3 D_123) C_14 q^2]
  /[C_14 D_123 q^2 - 2 D_123 V + 4 M^2 H^2].
```

The denominator is minus the determinant of the constraint matrix. A
sufficient finite-wavenumber no-ghost domain is

```text
M > 0,
rho > 0,
C_14 > 0,
D_123 > 0,
2 M - 3 D_123 > 0,
C_14 D_123 q^2 - 2 D_123 V + 4 M^2 H^2 > 0,
```

together with positivity of the remaining principal minors. The
representative scan checks the full matrix eigenvalues rather than relying on
the determinant alone.

Using

```text
M = M_P^2 + M_U^2(c_13 + 3 c_2)/2,
D_123 = M_U^2(c_13 + c_2),
```

the combination in the numerator obeys

```text
2 M - 3 D_123 = 2(M_P^2 - M_U^2 c_13).
```

The large-`q` curvature Hessian is twice the principal-report Lagrangian
coefficient, as required:

```text
K_RR(q -> infinity)
  = 4 M(M_P^2 - M_U^2 c_13)/(M_U^2 c_123).
```

The amplitude and phase Hessians tend to `1` and `rho^2`, respectively. This
recovers the previous principal-symbol result from the complete finite-`q`
system.

## 5. Low-q endpoint

The determinant contains the exact factor

```text
det K_red proportional to q^2.
```

Consequently,

```text
det K_red -> 0,
rank K_red -> 2,
```

as `q -> 0`. This occurs while the lapse-momentum constraint matrix remains
invertible on the representative branch. It is therefore not caused by a
finite-`q` constraint pole.

The result has two possible interpretations that the quadratic action alone
cannot distinguish:

1. the collapsing direction is the expected loss of an independent
   homogeneous scalar momentum perturbation; or
2. canonical normalization causes interactions to grow and introduces a
   physical low-momentum strong-coupling scale.

The cubic action and its canonically normalized interaction coefficients are
required to decide between them.

## 6. Representative trajectory scan

The scan uses the existing dimensionless branch and no physical fit:

```text
t in [0,8],
801 background samples,
q/H in [10^-3,10^3],
61 logarithmic wavenumber samples,
48,861 finite-q matrix evaluations.
```

The phase variable is instantaneously normalized by `chi=rho*vartheta` before
reporting numerical kinetic eigenvalues. This removes the trivial shrinking
of the raw phase coefficient as the background amplitude decreases. The
inertia is unchanged by this regular transformation.

Results:

| Diagnostic | Result |
|---|---:|
| Negative finite-`q` kinetic eigenvalues | 0 |
| Finite-`q` inertia at every sample | 3 positive, 0 negative |
| Smallest constraint singular value | 0.0501148 |
| Smallest normalized eigenvalue at `q/H=10^-3` | `5.86989e-9` |
| Largest normalized condition number at `q/H=10^-3` | `1.01110e9` |
| Fitted low-`q` eigenvalue power | 2.00066271 |
| Strict `q=0` kinetic rank | 2 of 3 |
| Directional coefficient-derivative error | `3.47e-9` |

At `t=0`, the normalized `q=0` kinetic eigenvalues are

```text
(0, 1, 4.11668713)
```

within numerical precision. At `t=8` they are

```text
(0, 1, 3.97553082)
```

within the declared `1e-9` rank tolerance.

The local first-order equation generator includes derivatives of the
time-dependent reduced matrices. Its instantaneous eigenvalues are stored as
diagnostics. Their real parts are not promoted to invariant growth rates
because time-dependent field normalization and the evolving background
change those local values. A physical stability statement requires either a
canonical cubic analysis or an initial-value transfer calculation with
declared observables.

The diagnostic-only choice `zeta_align=1` affects the phase-gradient
stiffness but not the constraint matrix, kinetic inertia or low-`q` rank
result.

## 7. Gate decision

### Derived and verified

- the full quadratic scalar metric-aether-condensate action for the declared
  two-derivative sectors on the verified FRW branch;
- finite-`q` lapse and momentum-constraint elimination;
- the exact on-shell reduced kinetic determinant;
- recovery of the previous high-`q` principal limit;
- positive finite-`q` kinetic inertia over the representative scan;
- nonsingular finite-`q` constraint matrices over that scan;
- exact `q^2` kinetic-determinant collapse and rank two at `q=0`;
- coefficient time derivatives including `mu_dot` and fixed-comoving-mode
  redshifting.

### Not derived

- the cubic action in the collapsing low-`q` eigenbasis;
- an invariant strong-coupling scale for that mode;
- a proof that the rank loss is purely gauge;
- a physical alignment coefficient or selected aether parameter point;
- matter and reservoir perturbation response;
- vector and tensor Hamiltonians on the evolving branch;
- global multicone causality or a physical EFT cutoff.

### Consequence

The scalar programme advances from a principal subhorizon pass to
**finite-q constraint elimination passed with a strict low-q hold**.

UVIR-003 is not closed. The next calculation is the cubic low-`q` scalar
action and canonical interaction-scale audit. MAT-001 remains blocked.

## 8. Reproduction

Run from the repository root:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_scalar_adm_finite_q.py
```

Outputs:

- `Analysis/UVIR/UVIR-003/outputs/uvir003_scalar_adm_finite_q_summary.json`
- `Analysis/UVIR/UVIR-003/outputs/uvir003_scalar_adm_finite_q_scan.csv`

Expected footer:

```text
UVIR-003 finite-q scalar ADM identities: VERIFIED
Finite-q lapse and momentum constraints: ELIMINATED
Finite-q kinetic inertia over representative scan: 3_POSITIVE_0_NEGATIVE
Low-q smallest-eigenvalue power: 2.00066271
Strict q->0 reduced kinetic rank: 2_OF_3
Low-q decision: HOLD_KINETIC_RANK_LOSS_AT_Q_TO_ZERO
Full UVIR-003 gate: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_FINITE_Q_REDUCTION_WITH_LOW_Q_HOLD
```
