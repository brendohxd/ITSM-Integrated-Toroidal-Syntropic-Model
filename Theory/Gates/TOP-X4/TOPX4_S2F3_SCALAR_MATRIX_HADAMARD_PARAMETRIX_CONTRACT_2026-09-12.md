# TOP-X4 `X4-S2F3` scalar-matrix Hadamard-parametrix contract

**Frozen:** 2026-09-12  
**Reasoning mode:** Max  
**Checkpoint class:** bounded local rank-three `D=5` Hadamard parametrix and
state-boundary audit  
**Authority effect:** none unless a later, separately reviewed gate says otherwise

## 1. Purpose and stop boundary

This contract freezes the next single TOP-X4 calculation after the completed
fixed-metric scalar-matrix operator checkpoint. It constructs the local
rank-three scalar Hadamard parametrix through `U_2`, verifies its transport and
coincidence controls against the corrected off-shell operator, and records the
exact boundary between a local parametrix and a globally admissible quantum
state.

The calculation uses an arbitrary smooth fixed five-dimensional metric and an
arbitrary smooth scalar background. It does not impose a homogeneous,
fixed-charge or winding ansatz. It does **not** construct a global positive
state, evaluate a determinant or mode sum, perform a stress-tensor point split,
normalize counterterms, vary the metric, solve a semiclassical background, or
calculate the physical Hessian.

The binding state result of this checkpoint is therefore
`scalar_matrix_hadamard_state=NOT_CONSTRUCTED`. A local Hadamard parametrix is
necessary subtraction data; it is not by itself a state because the smooth
state-dependent bisolution, positivity and global wavefront construction remain
separate requirements.

## 2. Owning authorities

The executable must verify the checked-in SHA-256 sidecars for:

1. `TOPX4_S2F3_COVARIANT_SCALAR_MATRIX_CONTRACT_2026-09-12.md`;
2. the covariant scalar-matrix output;
3. the covariant scalar-matrix executable;
4. `TOPX4_S2F3_HADAMARD_SUBTRACTION_READINESS_CONTRACT_2026-09-12.md`;
5. the Hadamard/subtraction readiness output;
6. the exact scalar/Dirac transport output;
7. the Plan-11 `PLAN.md`; and
8. this contract.

The preceding scalar operator must remain
`PASS_COVARIANT_SCALAR_CHI_MATRIX_OPERATOR_HOLD_STATES_GRAVITY_PARITY_AND_STRESS`
with `counterterm_normalizations=NOT_FIXED`,
`scalar_matrix_hadamard_state=NOT_CONSTRUCTED`,
`renormalized_stress=NOT_COMPUTED`, `physics_pass=false` and `gate_effect=NONE`.
The exact transport predecessor must retain its finite-order-only and
non-Hadamard declarations.

## 3. Canonical operator and local parametrix

The Euclidean quadratic operator is

\[
 P_E=-\Box I_3+H=-(\mathcal D^2+E),\qquad E=-H.
\]

In the Cartesian scalar bundle,

\[
 \mathcal D_A=\nabla_A I_3,\qquad \Omega_{AB}=[\mathcal D_A,\mathcal D_B]=0.
\]

For the local Lorentzian Hadamard transport control, use the corresponding
hyperbolic operator

\[
 \mathscr P=\mathcal D^A\mathcal D_A-H.
\]

Let `sigma` be Synge's world function, with
`sigma_A sigma^A=2 sigma`, and let square brackets denote coincidence
evaluation. In five dimensions the singular Feynman control is

\[
 G_{\mathrm{sing}}^F(x,x')=
 \frac{i}{16\sqrt{2}\,\pi^2}
 \frac{U(x,x')}{[\sigma(x,x')+i\epsilon]^{3/2}},
\qquad
 U=U_0+U_1\sigma+U_2\sigma^2+O(\sigma^3).
\]

The leading coefficient is the Van Vleck factor times bundle parallel
transport:

\[
 U_0=\Delta^{1/2}\,\mathcal P_{x\leftarrow x'},
 \qquad [U_0]=I_3.
\]

In Cartesian variables `mathcal P=I_3`. In a smooth phase-aligned patch it is
the parallel transporter of the pure-gauge connection
`A_A=J partial_A(Theta)`. The aligned representation must retain that
connection even though its curvature is zero.

For `n=1,2`, the local transport recursion is

\[
 \left[2\sigma^{;A}\mathcal D_A+\Box\sigma+2n-5\right]U_n
 =\frac{2}{3-2n}\,\mathscr P U_{n-1}.
\]

The `n=0` equation is

\[
 \left[2\sigma^{;A}\mathcal D_A+\Box\sigma-5\right]U_0=0.
\]

The executable must verify the coincidence controls

\[
 [U_1]=E+\frac16 R I_3=-H+\frac16 R I_3,
\]

and

\[
 [U_2]=-b_2,
\]

where

\[
\begin{aligned}
 b_2={}&\frac12E^2+\frac16RE+rac1{12}\Omega_{AB}\Omega^{AB}\\
 &+I_3\left(\frac1{72}R^2-rac1{180}R_{AB}R^{AB}
 +\frac1{180}R_{ABCD}R^{ABCD}\right)\\
 &+\frac16\Box E+\frac1{30}(\Box R)I_3.
\end{aligned}
\]

For the present Cartesian scalar block this becomes

\[
 [U_2]=-
 \left[\frac12H^2-\frac16RH-\frac16\Box H
 +I_3\left(\frac1{72}R^2-\frac1{180}R_{AB}R^{AB}
 +\frac1{180}R_{ABCD}R^{ABCD}+\frac1{30}\Box R\right)\right].
\]

The `U_2=-b_2` relation is a coincidence control for the stated convention;
it does not replace the off-diagonal transport construction needed for a
complete state.

## 4. Required bounded controls

The executable must independently test:

1. every authority/input sidecar and both predecessor hold boundaries;
2. the five-dimensional singular exponent `3/2` and propagator prefactor;
3. the `U_0` transport equation, coincidence identity and Cartesian parallel
   transport;
4. the `U_1,U_2` recursion coefficients at coincidence;
5. the corrected `E=-H` mapping and the rank-three `b_1,b_2` coincidence map;
6. a flat constant-matrix control with arbitrary symmetric `H`, including
   `U_1=-H` and `U_2=-H^2/2`;
7. the free scalar nested control and agreement with the registered scalar
   `u_1,u_2` formulas;
8. covariance of the local coefficients under a constant orthogonal bundle
   basis change;
9. the phase-aligned pure-gauge connection and zero curvature, while retaining
   its first-derivative `2*mu` projection;
10. the distinction between the local parametrix and a global state-dependent
    smooth bisolution;
11. the distinction between static Poisson `q=0` subtraction and evolving
    state-dependent stress subtraction;
12. dimensions of the singular prefactor, `U_n`, `H`, `E` and the local terms;
13. the current completion inventory and Rule-9 boundary; and
14. the observational-target and downstream-action firewalls.

At least eight rejecting mutations must be included:

1. use `E=+H`;
2. use the wrong sign for `U_2`;
3. omit the matrix `Omega^2` term from the generic `b_2` control;
4. omit phase-frame parallel transport or its `2*mu` derivative mixing;
5. copy the free scalar `U_1,U_2` component by component into the interacting
   matrix without `H^2` and portal terms;
6. promote finite-order exact transport to a global Hadamard state;
7. treat static `q=0` Poisson removal as renormalized evolving stress; and
8. claim a stress, determinant, positivity, semiclassical background or
   physical-Hessian result from the local parametrix alone.

## 5. Decision rule

The bounded status may be

`PASS_SCALAR_MATRIX_HADAMARD_PARAMETRIX_HOLD_GLOBAL_STATE_AND_STRESS`

only if every algebraic, dimensional, receipt, mutation and firewall check
passes. The output must contain:

- `calculation_status=PASS`;
- `scalar_matrix_hadamard_parametrix=DERIVED_LOCAL_U0_U2`;
- `scalar_matrix_hadamard_state=NOT_CONSTRUCTED`;
- `renormalized_stress=NOT_COMPUTED`;
- `determinant=NOT_COMPUTED`;
- `counterterm_normalizations=NOT_FIXED`;
- `physics_pass=false`;
- `gate_effect=NONE`;
- no homogeneous/fixed-charge reduction, background solve, physical Hessian,
  A4, Ultra, claim promotion or publication change; and
- `THREE_WAY_CLEARANCE_NOT_MET` until genuinely independent reports exist.

Any failed check produces
`FAIL_SCALAR_MATRIX_HADAMARD_PARAMETRIX_CHECKPOINT`. Even a pass completes
only local scalar subtraction data and the associated state-boundary inventory.

## 6. Required next boundary

After this checkpoint, the next separate scalar task is a globally admissible
infinite-order Hadamard state construction, or a justified
pseudodifferential/adiabatic construction with positivity and wavefront
conditions. The existing exact scalar transport is retained as finite-order
evidence only.

The Dirac Hadamard state, parity-odd phase/global anomaly, curved
graviton/ghost/Jacobian operators, counterterm normalization, renormalized
stress, coupled semiclassical background and physical Hessian remain separate
receipted prerequisites. No downstream gate follows from this local pass.

## 7. Primary-source controls

- Decanini and Folacci, *Hadamard renormalization of the stress-energy tensor
  for a quantized scalar field in a general spacetime of arbitrary dimension*,
  arXiv:gr-qc/0512118.
- Vassilevich, *Heat kernel expansion: user's manual*,
  arXiv:hep-th/0306138.
- Hollands, *The Hadamard Condition for Dirac Fields and Adiabatic States on
  Robertson-Walker Spacetimes*, arXiv:gr-qc/9906076.
- Junker and Schrohe, *Adiabatic vacuum states on general spacetime
  manifolds*, arXiv:math-ph/0109010.
- Gerard and Wrochna, *Construction of Hadamard states by pseudodifferential
  calculus*, arXiv:1209.2604.

These sources constrain the local and microlocal formalism. They are not
independent Rule-9 reviews of this repository-specific matrix calculation.
