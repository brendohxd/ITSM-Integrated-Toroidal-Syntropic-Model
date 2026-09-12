# TOP-X4 `X4-S2F3` Plan-11 scalar-matrix Hadamard-parametrix receipt

**Executed:** 2026-09-12  
**Checkpoint status:** `PASS_SCALAR_MATRIX_HADAMARD_PARAMETRIX_HOLD_GLOBAL_STATE_AND_STRESS`  
**Local scalar parametrix:** `DERIVED_LOCAL_U0_U2`  
**Global scalar Hadamard state:** `NOT_CONSTRUCTED`  
**Physics pass:** `false`  
**Gate effect:** `NONE`

## 1. Binding result

The separately frozen executable completed `22/22` symbolic, dimensional,
receipt, mutation and firewall checks. It uses the completed fixed-metric
rank-three scalar operator with the registered convention `E=-H`, Cartesian
`Omega_AB=0`, and the phase-aligned pure-gauge connection.

This is a bounded local parametrix and state-boundary pass. It verifies the
five-dimensional singular power and normalization, the `U_0,U_1,U_2`
coincidence controls, the local transport recursion, the generic matrix
heat-kernel map and the flat constant-matrix realization. It does not claim a
globally admissible state.

The binding output remains:

```text
scalar_matrix_hadamard_parametrix=DERIVED_LOCAL_U0_U2
scalar_matrix_hadamard_state=NOT_CONSTRUCTED
determinant=NOT_COMPUTED
renormalized_stress=NOT_COMPUTED
counterterm_normalizations=NOT_FIXED
physics_pass=false
gate_effect=NONE
```

## 2. Execution receipt

Command:

```powershell
python Analysis\TOP\TOP-X4\topx4_s2f3_scalar_matrix_hadamard_parametrix_checkpoint.py
```

Recorded result:

```text
PASS_SCALAR_MATRIX_HADAMARD_PARAMETRIX_HOLD_GLOBAL_STATE_AND_STRESS
checks=22/22
scalar_matrix_hadamard_parametrix=DERIVED_LOCAL_U0_U2
scalar_matrix_hadamard_state=NOT_CONSTRUCTED
determinant=NOT_COMPUTED
renormalized_stress=NOT_COMPUTED
counterterm_normalizations=NOT_FIXED
physics_pass=false
gate_effect=NONE
sha256=db3ad816b25fe0a2a4227f7bc070842959bf8791937f65507041d374764e596e
```

Artifact hashes:

| Artifact | SHA-256 |
|---|---|
| `TOPX4_S2F3_SCALAR_MATRIX_HADAMARD_PARAMETRIX_CONTRACT_2026-09-12.md` | `4f036104de14ac2e05f2a0edadf7aaf8da85a1209d6852e6ef5a13513d9ffc56` |
| `topx4_s2f3_scalar_matrix_hadamard_parametrix_checkpoint.py` | `5a9d17c94a73d69caa87afd34b47617bbd18765ffb10f00dfac3e88af20a201c` |
| `topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json` | `db3ad816b25fe0a2a4227f7bc070842959bf8791937f65507041d374764e596e` |

The authority/input sidecars matched before calculation. Two clean CLI runs
produced the same output hash. The output contains no absolute workstation
paths or observational target tokens.

## 3. Local parametrix controls

The executable registers the five-dimensional local Feynman singular control

\[
 G^F_{\mathrm{sing}}(x,x')=
 \frac{i}{16\sqrt{2}\,\pi^2}
 \frac{U_0+U_1\sigma+U_2\sigma^2+O(\sigma^3)}
      {[\sigma+i\epsilon]^{3/2}}.
\]

For the fixed-metric scalar matrix it verifies

\[
 [U_0]=I_3,\qquad [U_1]=E+\frac16RI_3=-H+\frac16RI_3,
 \qquad [U_2]=-b_2.
\]

The generic matrix coefficient retains `tr(Omega_AB Omega^AB)/12`, while the
Cartesian scalar bundle sets `Omega_AB=0`. A flat constant symmetric matrix
control independently reproduces `U_1=-H` and `U_2=-H^2/2` through the `n=1,2`
transport recurrences. The free scalar nested control agrees with the
registered `D=5` `u_1,u_2` formulas.

The phase-aligned connection is retained as
`A_A=J*d_A(Theta)` with zero local curvature; its `A_t=mu*J` projection gives
the invariant derivative-mixing magnitude `2*mu`.

## 4. Rejection and state boundary

The executable rejects all eight registered mutations:

1. `E=+H` through the free `U_1` control;
2. the opposite `U_2` sign;
3. omission of the generic `Omega^2` contribution;
4. omission of phase-frame transport or its `2*mu` mixing;
5. componentwise free-scalar substitution for matrix `U_2`;
6. promotion of finite-order exact transport to a global Hadamard state;
7. promotion of static Poisson `q=0` subtraction to evolving stress
   renormalization; and
8. any determinant, stress, positivity, semiclassical-background or physical-
   Hessian claim from the local parametrix alone.

The present result constructs local coincidence/transport data and a flat
matrix realization. It does not construct the arbitrary-background
off-diagonal coefficient biscalars, the smooth state-dependent bisolution, a
positive global state, or a wavefront-condition proof. Those are deliberately
not hidden behind the local `U_0,U_1,U_2` result.

## 5. Decision boundary

The preceding scalar operator, Hadamard scaffold and exact-transport holds
remain preserved. This checkpoint does not change `MAT-001=BLOCKED`,
`UVIR-003=IN_PROGRESS`, `K_Q=NOT_DERIVED` or `V=NOT_COMPUTED`.

The following remain open:

- globally admissible infinite-order scalar matrix Hadamard state or justified
  pseudodifferential/adiabatic equivalent;
- Dirac Hadamard two-point function and parity-odd/global-anomaly audit;
- curved finite-charge graviton, ghost, Jacobian and zero-mode operators;
- gravitational and matter counterterm normalization;
- determinant, state-dependent renormalized stress and self-consistent
  semiclassical background; and
- coupled physical Hessian and radion mass.

No homogeneous or fixed-charge reduction, A4, Ultra, phenomenology,
publication or canonical-model revision follows. `Rule-9` remains
`THREE_WAY_CLEARANCE_NOT_MET` with zero independent reports for this
checkpoint.

## 6. Primary-source boundary

The local five-dimensional scalar Hadamard coefficients and their relation to
the state-dependent smooth part are controlled by Decanini and Folacci,
arXiv:gr-qc/0512118. The Laplace-type matrix connection, endomorphism and
heat-kernel map are controlled by Vassilevich, arXiv:hep-th/0306138. These
sources constrain the formalism; they are not independent Rule-9 reviews of
the repository-specific calculation.
