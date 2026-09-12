# TOP-X4 `X4-S2F3` Plan-11 covariant scalar-matrix receipt

**Executed:** 2026-09-12  
**Checkpoint status:** `PASS_COVARIANT_SCALAR_CHI_MATRIX_OPERATOR_HOLD_STATES_GRAVITY_PARITY_AND_STRESS`  
**Scalar matrix operator:** `DERIVED_FIXED_METRIC_OFF_SHELL`  
**Matter counterterm structures:** `ENUMERATED_THROUGH_B2`  
**Physics pass:** `false`  
**Gate effect:** `NONE`

## 1. Binding result

The preregistered executable completed all `25/25` symbolic, symmetry,
dimensional, receipt, mutation and firewall checks. It derives the rank-three
fixed-metric fluctuation operator for the two canonical real components of
`Phi` coupled to `chi` before any homogeneous, winding or fixed-charge ansatz.
It then specializes the five-dimensional heat-kernel scaffold to this scalar
block and enumerates its local counterterm structures through `b_2`.

This is a bounded operator pass and a downstream HOLD:

```text
counterterm_normalizations=NOT_FIXED
scalar_matrix_hadamard_state=NOT_CONSTRUCTED
determinant=NOT_COMPUTED
renormalized_stress=NOT_COMPUTED
physics_pass=false
gate_effect=NONE
```

## 2. Execution receipt

```powershell
python Analysis\TOP\TOP-X4\topx4_s2f3_covariant_scalar_matrix_checkpoint.py
```

Recorded result:

```text
PASS_COVARIANT_SCALAR_CHI_MATRIX_OPERATOR_HOLD_STATES_GRAVITY_PARITY_AND_STRESS
checks=25/25
scalar_matrix_operator=DERIVED_FIXED_METRIC_OFF_SHELL
matter_counterterm_structures=ENUMERATED_THROUGH_B2
sha256=11125054bb284a4597587fbcb50e0d70358232ea8bd54f579b20a3948c202560
```

| Artifact | SHA-256 |
|---|---|
| `TOPX4_S2F3_COVARIANT_SCALAR_MATRIX_CONTRACT_2026-09-12.md` | `a6d1ffb25fb9445975a4ce72661fe734a98956e6537f0549ef8b88f96ca0ff14` |
| `topx4_s2f3_covariant_scalar_matrix_checkpoint.py` | `393584ccd00a4ea79ba1c2c8228cbca78bb925fade462b8b0740fe1c64e42f07` |
| `topx4_s2f3_covariant_scalar_matrix_summary.json` | `11125054bb284a4597587fbcb50e0d70358232ea8bd54f579b20a3948c202560` |

All seven registered authority/input sidecars matched. Three clean CLI
executions produced the same output hash.

## 3. Derived operator

With

\[
\Phi=\frac{\phi_1+i\phi_2}{\sqrt2},\qquad
s=\frac{\phi_1^2+\phi_2^2}{2},\qquad
\varphi^i=(\phi_1,\phi_2,\chi),
\]

direct differentiation of the frozen potential gives, off shell,

\[
S_{E,\mathrm{sc}}^{(2)}
=\frac12\int d^5x\sqrt G\,\eta^T(-\Box I_3+H)\eta,
\]

\[
H=\begin{pmatrix}
m_\Phi^2+\frac{\lambda_{\Phi5}}2r^2+\lambda_{\Phi5}\phi_1^2+\frac{g_5}2\chi^2
&\lambda_{\Phi5}\phi_1\phi_2&g_5\chi\phi_1\\
\lambda_{\Phi5}\phi_1\phi_2
&m_\Phi^2+\frac{\lambda_{\Phi5}}2r^2+\lambda_{\Phi5}\phi_2^2+\frac{g_5}2\chi^2
&g_5\chi\phi_2\\
g_5\chi\phi_1&g_5\chi\phi_2
&m_\chi^2+\frac{\lambda_{\chi5}}2\chi^2+\frac{g_5}2r^2
\end{pmatrix}.
\]

In the registered `P=-(D^2+E)` convention,

\[
{\cal D}_A=\nabla_A I_3,\qquad E=-H,\qquad\Omega_{AB}=0.
\]

The opposite sign is rejected by the free-scalar control
`b_1=-m^2+R/6`. In a smooth phase-aligned frame,
`A_A=J*d_A(Theta)` is pure gauge and still has `Omega_AB=0`; its
`A_t=mu J` projection recovers first-derivative mixing of magnitude `2*mu`.
The Cartesian chart remains regular at `rho=0`.

## 4. Trace and counterterm result

\[
\operatorname{tr}H
=2m_\Phi^2+m_\chi^2+(4\lambda_{\Phi5}+g_5)s
+\left(g_5+\frac12\lambda_{\chi5}\right)\chi^2,
\]

\[
\begin{aligned}
\operatorname{tr}H^2={}&2m_\Phi^4+m_\chi^4
+(8\lambda_{\Phi5}m_\Phi^2+2g_5m_\chi^2)s\\
&+(2g_5m_\Phi^2+\lambda_{\chi5}m_\chi^2)\chi^2
+(10\lambda_{\Phi5}^2+g_5^2)s^2\\
&+g_5(4g_5+4\lambda_{\Phi5}+\lambda_{\chi5})s\chi^2
+\left(\frac12g_5^2+\frac14\lambda_{\chi5}^2\right)\chi^4.
\end{aligned}
\]

The direct Cartesian trace agrees with an independent phase-aligned
calculation. Omitting portal mixing loses `2*g_5^2*r^2*chi^2` from
`tr(H^2)` and is rejected.

For rank three,

\[
\operatorname{tr}b_0=3,\quad
\operatorname{tr}b_1=-\operatorname{tr}H+\frac12R,
\]

\[
\begin{aligned}
\operatorname{tr}b_2={}&\frac12\operatorname{tr}H^2
-\frac16R\operatorname{tr}H-\frac16\Box\operatorname{tr}H\\
&+3\left(\frac1{72}R^2-\frac1{180}R_{AB}R^{AB}
+\frac1{180}R_{ABCD}R^{ABCD}\right)+\frac1{10}\Box R.
\end{aligned}
\]

The generic integrated scalar divergence through `b_2` requires
`1, s, chi^2, s^2, s*chi^2, chi^4, R, R*s, R*chi^2, R^2,
R_AB R^AB, R_ABCD R^ABCD`. The local coefficient retains `Box(s)`,
`Box(chi^2)` and `Box(R)` until boundary/falloff assumptions are applied.
Every `Lambda^5*b_0`, `Lambda^3*b_1` and `Lambda*b_2` monomial has
five-dimensional Lagrangian dimension.

The `R*s` and `R*chi^2` terms are new relative to the minimally coupled tree
scalar action. Their finite renormalized coefficients remain unfixed. This is
not the complete higher-order, higher-loop, spinor, graviton or Wilsonian
five-dimensional EFT basis.

## 5. Controls, remaining work and next gate

The calculation verifies `U(1)/O(2)` and `chi -> -chi` covariance, the
off-shell Ward identity, zero-portal/zero-field/free limits, two independent
trace derivations, and all mass dimensions. Seven mutations are rejected:
wrong `E` sign, missing portal mixing, nonzero Cartesian curvature, missing
phase-frame connection, missing `R*s`, missing `R*chi^2`, and an equation of
motion inserted into the off-shell Hessian.

Only the fixed-metric scalar-operator inventory line is completed. Scalar and
Dirac Hadamard states, curved graviton/ghost operators, parity-odd phase,
counterterm normalization, determinant, stress and the physical Hessian remain
open. The next admissible single checkpoint is a scalar matrix Hadamard
parametrix/state construction using this operator.

Rule-9 status remains `THREE_WAY_CLEARANCE_NOT_MET` with zero completed
independent reports. No background solve, A4, Ultra, gate promotion or
publication change is authorized.

## 6. Primary-source audit

The quadratic background-field boundary, unique Laplace-type data and matrix
`a_0,a_2,a_4` coefficients follow Vassilevich,
[*Heat kernel expansion: user's manual*](https://arxiv.org/abs/hep-th/0306138).
That source controls the universal formalism; it is not an independent Rule-9
review of this repository-specific result.
