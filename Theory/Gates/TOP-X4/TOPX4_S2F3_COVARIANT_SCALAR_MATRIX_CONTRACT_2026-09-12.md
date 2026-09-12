# TOP-X4 `X4-S2F3` covariant scalar-matrix contract

**Frozen:** 2026-09-12  
**Reasoning mode:** Max  
**Checkpoint class:** bounded off-shell fixed-metric scalar second variation  
**Authority effect:** none unless a later, separately reviewed gate says otherwise

## 1. Purpose and stop boundary

This contract freezes the next single TOP-X4 checkpoint after the
five-dimensional Hadamard/subtraction readiness audit. The checkpoint must
derive the covariant quadratic operator for the two canonical real components
of `Phi` coupled to `chi`, before any homogeneous, fixed-charge or winding
ansatz. It must expose the matrix endomorphism, bundle connection and curvature,
and expand the scalar one-loop heat-kernel structures through `b_2` far enough
to enumerate the induced local matter counterterms.

The metric is an arbitrary fixed five-dimensional background during this
checkpoint. Metric fluctuations, scalar-graviton mixing, gauge fixing,
Faddeev-Popov/Jacobian operators and the physical constrained Hessian remain
outside this scalar block. The checkpoint also does **not** construct a scalar
Hadamard state, evaluate a determinant or mode sum, normalize renormalized
couplings, compute a stress tensor, impose a background ansatz, or solve a
semiclassical equation.

## 2. Owning authorities

The executable must verify checked-in SHA-256 sidecars for:

1. `TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md`;
2. `TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md`;
3. `TOPX4_S2F3_FINITE_CHARGE_VARIATION_CONTRACT_2026-09-09.md`;
4. the Plan-11 `PLAN.md`;
5. `TOPX4_S2F3_HADAMARD_SUBTRACTION_READINESS_CONTRACT_2026-09-12.md`;
6. the Hadamard/subtraction readiness output; and
7. this contract.

The prior readiness result must remain
`PASS_5D_HADAMARD_COUNTERTERM_SCAFFOLD_HOLD_FULL_OPERATORS_STATE_AND_STRESS`
with `readiness_decision=HOLD`, `hadamard_stress_ready=false`,
`physics_pass=false` and `gate_effect=NONE`.

## 3. Canonical Cartesian fields and potential

Use canonical real fields

\[
 \Phi=\frac{\phi_1+i\phi_2}{\sqrt2},\qquad
 s=\Phi^*\Phi=\frac{r^2}{2},\qquad
 r^2=\phi_1^2+\phi_2^2,
\]

and the rank-three field vector

\[
 \varphi^i=(\phi_1,\phi_2,\chi).
\]

The scalar part of the frozen action has canonical kinetic metric
`delta_ij` and potential

\[
\begin{aligned}
 {\cal V}(\varphi)={}&U_0+\frac{m_\Phi^2}{2}r^2
 +\frac{\lambda_{\Phi5}}{8}r^4
 +\frac{m_\chi^2}{2}\chi^2
 +\frac{\lambda_{\chi5}}{24}\chi^4
 +\frac{g_5}{4}r^2\chi^2.
\end{aligned}
\]

This is an exact Cartesian rewriting of the frozen `X4-I1C` scalar action.
No chemical potential, gauge field, brane term or fermion-scalar coupling is
introduced.

## 4. Off-shell Euclidean second variation

After Wick rotation, expand an arbitrary smooth background as
`varphi -> bar(varphi)+eta`. Before imposing any background equation,

\[
 S_{E,\mathrm{sc}}^{(2)}=
 \frac12\int d^5x\sqrt{G}\,\eta^T P_{\mathrm{sc}}\eta,
 \qquad
 P_{\mathrm{sc}}=-\Box I_3+H,
\]

where

\[
 H_{ij}=\frac{\partial^2{\cal V}}
 {\partial\varphi^i\partial\varphi^j}.
\]

The first variation generally remains nonzero; that is not grounds for
discarding it or using an equation of motion inside the Hessian. In the
readiness convention

\[
 P=-\left(G^{AB}{\cal D}_A{\cal D}_B+E\right),
\]

the Cartesian data are

\[
 {\cal D}_A=\nabla_A I_3,\qquad E=-H,\qquad
 \Omega_{AB}=[{\cal D}_A,{\cal D}_B]=0.
\]

The explicit Hessian is

\[
H=\begin{pmatrix}
m_\Phi^2+\frac{\lambda_{\Phi5}}2r^2
+\lambda_{\Phi5}\phi_1^2+\frac{g_5}2\chi^2
&\lambda_{\Phi5}\phi_1\phi_2&g_5\chi\phi_1\\
\lambda_{\Phi5}\phi_1\phi_2
&m_\Phi^2+\frac{\lambda_{\Phi5}}2r^2
+\lambda_{\Phi5}\phi_2^2+\frac{g_5}2\chi^2
&g_5\chi\phi_2\\
g_5\chi\phi_1&g_5\chi\phi_2
&m_\chi^2+\frac{\lambda_{\chi5}}2\chi^2+\frac{g_5}2r^2
\end{pmatrix}.
\]

`U_0` has zero field Hessian, but the scalar determinant still induces a bulk
vacuum counterterm through `b_0` and mass-dependent terms in `b_1,b_2`.

## 5. Symmetry and phase-aligned bundle gauges

The Cartesian connection vanishes because all three fluctuations are neutral
spacetime scalars with a flat target-space kinetic metric. The Hessian must be
covariant under the frozen global `U(1)`, represented as `O(2)` rotations of
`(phi_1,phi_2)`, and under `chi -> -chi`. The off-shell `U(1)` differential
identity is

\[
 HJ\varphi=J\,\partial{\cal V},
\qquad
J=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&0\end{pmatrix}.
\]

On a patch with `rho=sqrt(r^2)>0`, an orthonormal frame aligned with the local
background phase `Theta` is a bundle gauge transformation `eta=S(Theta) xi`.
It gives

\[
 {\cal A}_A=S^T\partial_A S=J\,\partial_A\Theta,
 \qquad
 \Omega_{AB}=\partial_A{\cal A}_B-\partial_B{\cal A}_A
 +[{\cal A}_A,{\cal A}_B]=0,
\]

and

\[
 P'=-\left(\nabla+{\cal A}\right)^2+S^THS,
 \qquad E'=-S^THS.
\]

The aligned Hessian is

\[
H_{\rm al}=\begin{pmatrix}
m_\Phi^2+\frac32\lambda_{\Phi5}\rho^2+\frac{g_5}2\chi^2
&0&g_5\rho\chi\\
0&m_\Phi^2+\frac12\lambda_{\Phi5}\rho^2+\frac{g_5}2\chi^2&0\\
g_5\rho\chi&0&m_\chi^2+\frac12\lambda_{\chi5}\chi^2
+\frac{g_5}2\rho^2
\end{pmatrix}.
\]

Thus a later homogeneous phase with `partial_t Theta=mu` obtains its
amplitude-phase first-derivative mixing from the flat connection. This is only
a nested consistency projection after the covariant derivation, not the input
to it. The aligned chart is singular at `rho=0`; the Cartesian operator is not.

## 6. Trace invariants

The required field invariants are

\[
\begin{aligned}
 \operatorname{tr}H={}&2m_\Phi^2+m_\chi^2
 +(4\lambda_{\Phi5}+g_5)s
 +\left(g_5+\frac12\lambda_{\chi5}\right)\chi^2,
\end{aligned}
\]

and

\[
\begin{aligned}
\operatorname{tr}H^2={}&2m_\Phi^4+m_\chi^4\\
&+(8\lambda_{\Phi5}m_\Phi^2+2g_5m_\chi^2)s\\
&+(2g_5m_\Phi^2+\lambda_{\chi5}m_\chi^2)\chi^2\\
&+(10\lambda_{\Phi5}^2+g_5^2)s^2\\
&+g_5(4g_5+4\lambda_{\Phi5}+\lambda_{\chi5})s\chi^2\\
&+\left(\frac12g_5^2+\frac14\lambda_{\chi5}^2\right)\chi^4.
\end{aligned}
\]

Here `m_Phi^4` means `(m_Phi^2)^2`, and similarly for `m_chi^4`.
The portal off-diagonal entries contribute the indispensable term
`2*g_5^2*r^2*chi^2` to `tr(H^2)` before conversion to `s`.

For rank three and `E=-H`, the traced local coefficients are

\[
 \operatorname{tr}b_0=3,
 \qquad
 \operatorname{tr}b_1=-\operatorname{tr}H+\frac12R,
\]

and

\[
\begin{aligned}
\operatorname{tr}b_2={}&\frac12\operatorname{tr}H^2
-\frac16R\operatorname{tr}H-\frac16\Box\operatorname{tr}H\\
&+3\left(\frac1{72}R^2-\frac1{180}R_{AB}R^{AB}
+\frac1{180}R_{ABCD}R^{ABCD}\right)+\frac1{10}\Box R.
\end{aligned}
\]

The `tr(Omega_AB Omega^AB)/12` term vanishes in both the Cartesian and smooth
phase-aligned gauges, but it must be tested rather than omitted by assumption.

## 7. Induced scalar counterterm structures through `b_2`

For the three real bosonic fluctuations,

\[
 \Gamma^{(1)}_{\rm sc}=\frac12\operatorname{Tr}\log P_{\rm sc}
 =-\frac12\int_{\Lambda^{-2}}^\infty\frac{d\tau}{\tau}
 \operatorname{Tr}e^{-\tau P_{\rm sc}}.
\]

Therefore its local divergent part has the inherited five-dimensional powers
`Lambda^5`, `Lambda^3`, and `Lambda`, with overall sign fixed by the displayed
proper-time convention. Counterterms canceling those divergences require the
following symmetry-preserving structures through `b_2`:

\[
\begin{gathered}
1,\quad s,\quad\chi^2,\quad s^2,\quad s\chi^2,\quad\chi^4,\\
R,\quad Rs,\quad R\chi^2,\quad
R^2,\quad R_{AB}R^{AB},\quad R_{ABCD}R^{ABCD}.
\end{gathered}
\]

The local coefficient also contains `Box(s)`, `Box(chi^2)` and `Box(R)`.
They may be removed from the integrated action only after the smooth
no-boundary/noncompact-falloff assumptions are declared. They remain explicit
in a local point-split subtraction. No independent scalar wave-function
counterterm is generated by the integrated `b_0,b_1,b_2` divergence in this
minimal fixed-metric scalar block; this is not a statement about higher heat-
kernel orders, higher loops, or the full nonrenormalizable five-dimensional
EFT basis.

The appearance of `R*s` and `R*chi^2` means the minimally coupled tree action
is not by itself the complete renormalized scalar action. Their renormalized
finite coefficients and every other normalization condition remain open.

## 8. Dimensional audit

In five-dimensional natural units,

\[
[\phi_1]=[\phi_2]=[\chi]=\frac32,\quad [s]=[\chi^2]=3,
\quad [H]=[E]=2,
\]

\[
[b_0]=0,\quad[b_1]=2,\quad[b_2]=4,
\]

so `Lambda^5*b_0`, `Lambda^3*b_1` and `Lambda*b_2` each have Lagrangian
dimension five. The executable must also verify every monomial in `tr(H)` and
`tr(H^2)`, and the complete counterterm list, against these dimensions.

## 9. Preregistered executable checks and rejecting mutations

The script must independently test:

1. every authority/input sidecar and the prior readiness HOLD;
2. the exact Cartesian rewrite of the frozen potential;
3. the direct symbolic Hessian and its symmetry;
4. the minimal identity principal symbol and off-shell boundary;
5. `E=-H` in the registered Laplace-type convention;
6. Cartesian `Omega_AB=0`;
7. global-`U(1)` covariance and the off-shell Ward identity;
8. `chi -> -chi` covariance;
9. the aligned Hessian, pure-gauge phase connection and zero curvature;
10. the local finite-charge derivative-mixing projection;
11. `tr(H)` and `tr(H^2)` in invariant form;
12. the rank-three `b_0,b_1,b_2` trace map;
13. every induced counterterm structure and mass dimension;
14. zero-portal, `Phi=0`, `chi=0` and free nested controls; and
15. the observational-target and downstream-action firewalls.

At least six bad mutations must be rejected: use `E=+H`, omit portal mixing,
declare nonzero Cartesian bundle curvature, omit the phase-frame connection,
omit either nonminimal curvature-scalar structure, or use a background equation
to delete an off-shell Hessian term.

## 10. Decision rule

The bounded status may be

`PASS_COVARIANT_SCALAR_CHI_MATRIX_OPERATOR_HOLD_STATES_GRAVITY_PARITY_AND_STRESS`

only if every symbolic, symmetry, dimensional, receipt, mutation and firewall
check passes. It must be accompanied by:

- `calculation_status=PASS`;
- `scalar_matrix_operator=DERIVED_FIXED_METRIC_OFF_SHELL`;
- `matter_counterterm_structures=ENUMERATED_THROUGH_B2`;
- `counterterm_normalizations=NOT_FIXED`;
- `scalar_matrix_hadamard_state=NOT_CONSTRUCTED`;
- `determinant=NOT_COMPUTED`;
- `renormalized_stress=NOT_COMPUTED`;
- `physics_pass=false`;
- `gate_effect=NONE`;
- no homogeneous/fixed-charge reduction, background solve, physical Hessian,
  A4, Ultra, claim promotion or publication change; and
- `THREE_WAY_CLEARANCE_NOT_MET` until genuinely independent reports exist.

Any failed check produces
`FAIL_COVARIANT_SCALAR_CHI_MATRIX_OPERATOR_CHECKPOINT`. Even a pass completes
only the fixed-metric scalar-operator line in the readiness inventory.

## 11. Primary-source control

The quadratic-background-field boundary, unique Laplace-type connection and
endomorphism, and matrix heat-kernel coefficients follow Vassilevich,
*Heat kernel expansion: user's manual*, arXiv:hep-th/0306138, especially
Eqs. (1.2), (2.1)--(2.4), and (4.26)--(4.28).

That source constrains the universal formalism. It is not an independent
Rule-9 review of this repository-specific Hessian or counterterm expansion.
