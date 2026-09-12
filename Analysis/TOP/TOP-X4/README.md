# TOP-X4 A0 analysis

Deterministic mathematical controls for the higher-dimensional
`R_t x T3_obs x S1_y` research fork.

Run from the repository root:

```powershell
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\TOP\TOP-X4\topx4_a0_kinematic_control.py
```

Expected execution status:

```text
PASS_TOPX4_A0_KINEMATIC_AND_DIMENSIONAL_CONTROL
```

This means only that the registered topology, Fourier/KK decomposition and
mass-dimension ledger are mutually consistent. The JSON must retain
`physics_pass: false`, `gate_effect: NONE`, and an empty `derived_claims` list.

## A1 finite-charge background control

After reading the frozen A1 action ledger, run:

```powershell
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\TOP\TOP-X4\topx4_a1_background_control.py
```

This integrates one dimensionless on-shell background of the `X4-I1C` bulk
scalar control. A pass is only an action/background consistency result. It is
not a perturbation, radion, physical-matter, transfer-current or phenomenology
pass.

Run the independent symbolic action/metric audit with:

```powershell
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\TOP\TOP-X4\topx4_a1_symbolic_audit.py
```

## A2/A3 reduction and radion control

Run the fixed-action Max audit with:

```powershell
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\TOP\TOP-X4\topx4_a2a3_reduction_radion_control.py
```

The Einstein-frame radion normalization used there is independently checked by
constructing the five-dimensional Ricci scalar directly:

```powershell
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\TOP\TOP-X4\topx4_a2_radion_symbolic_audit.py
```

This audit distinguishes healthy fixed-background KK identities from the
separate requirement that the fourth radius be a stationary, stable solution.
It must not report a physics pass merely because the bounded algebra executes.

## S0 stabilization-candidate prescreen

Run the completed High-only selection control with:

```powershell
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\TOP\TOP-X4\topx4_s0_stabilization_prescreen.py
```

Expected status:

```text
SELECT_TOPX4_S2F3_FOR_MAX_RETRY_ONLY
```

This verifies eight algebraic, field-count, stationary-witness and cutoff-
domain checks. It deliberately does not evaluate a determinant or solve the
new finite-density background, and its JSON must retain `physics_pass: false`.

## Plan 11 — static determinant checkpoint

Run the frozen `X4-S2F3` parity-even determinant checkpoint with:

```powershell
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\TOP\TOP-X4\topx4_s2f3_static_determinant_checkpoint.py
```

The recorded bounded status is:

```text
PASS_STATIC_PARITY_EVEN_DETERMINANT_HOLD_PARITY_ODD_AND_FINITE_CHARGE
```

The checkpoint passes 12/12 calculation checks for the zero-density static
`Minkowski4 x S1` parity-even determinant, including proper-time/Poisson and
Bessel/polylog cross-checks, the equal-mass `N_F=3` stationary witness and
negative controls. It keeps `physics_pass: false` and does not establish a
finite-charge background, physical radion mass, parity/anomaly clearance or
publication result.

## Plan 11 — finite-charge entry gate

Run the fail-closed transition gate with:

```powershell
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\TOP\TOP-X4\topx4_s2f3_finite_charge_entry_gate.py
```

The current status is:

```text
HOLD_TOPX4_S2F3_BEFORE_FINITE_CHARGE_QUANTUM_COMPLETION
```

All 9/9 provenance and policy checks pass, but the gate correctly refuses to
reuse the static determinant as a time-dependent finite-charge calculation.
The missing state-dependent spectrum/stress, anomaly data, evolving-state
convergence and coupled physical Hessian keep finite-charge completion closed.
No A4 or Ultra work is authorized. Rule-9 three-way independent clearance is
also not met: Role A completed, while Roles B and C returned usage-limit
errors without reports.

## Plan 11 — finite-charge operator checkpoint

Run the constant-background charged-scalar operator and fixed-charge
variation checkpoint with:

```powershell
python Analysis\TOP\TOP-X4\topx4_s2f3_finite_charge_operator_checkpoint.py
```

The recorded bounded status is:

```text
PASS_FINITE_CHARGE_OPERATOR_HOLD_DYNAMIC_STATE_STRESS_AND_HESSIAN
```

The checkpoint passes 16/16 exact algebra, provenance and mutation checks. It
derives the amplitude-phase mixing, Goldstone/amplitude branches and
fixed-global-charge Routhian identities, while rejecting omitted-mixing and
wrong-sign-Routhian mutations. It retains `physics_pass: false`, has no gate
effect and does not advance to the evolving-state determinant. The then-next
calculation—the coupled time-dependent mode system, declared scalar adiabatic
state ingredients and order-convergence test—is recorded below.

## Plan 11 — dynamic state/subtraction checkpoint

Run the preregistered evolving scalar-mode and finite-order adiabatic test with:

```powershell
python Analysis\TOP\TOP-X4\topx4_s2f3_dynamic_state_subtraction_checkpoint.py
```

The recorded status is:

```text
FAIL_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT
```

The run clears 11/12 checks. The exact time-dependent charged-scalar mode
system, charge-law regression, mutation controls and preregistered UV
order-0/2/4 hierarchy pass. The all-mode positivity check fails because the
fourth-order WKB iterate becomes negative for three low-momentum branch/mode
combinations near the initial hypersurface. Base frequencies remain positive,
so this is not recorded as a physical tachyon; it rejects the tested
branchwise fourth-order candidate over the complete registered grid.

The result retains `physics_pass: false`, `gate_effect: NONE`, and no advance
to renormalized stress, A4 or Ultra. Coupled eigenvector transport, the Dirac
adiabatic state, covariant five-dimensional subtraction/counterterms,
renormalized stress, physical Hessian and Rule-9 clearance remain open.

## Plan 11 — exact scalar/Dirac transport retry

Run the separately frozen exact-transport retry with:

```powershell
python Analysis\TOP\TOP-X4\topx4_s2f3_exact_transport_retry_checkpoint.py
```

The recorded bounded status is:

```text
PASS_EXACT_SCALAR_DIRAC_TRANSPORT_HOLD_HADAMARD_STRESS_AND_HESSIAN
```

The retry passes 18/18 checks. It preserves the failed WKB output as an input,
then initializes the coupled scalar modes from the positive Hamiltonian on the
original `t=0` surface and evolves them exactly. It separately constructs a
first-order, exactly retracted rank-two Dirac projector and evolves its range
unitarily. The three prior low-mode failures remain finite under this different
transport prescription; they are not relabeled as WKB passes.

The result verifies canonical normalization, static controls, rejecting
mutations, decreasing registered UV endpoint mixing and a 801/401-point
resolution witness. It remains a finite-order state candidate:
`full_Hadamard_state: false`, `physics_pass: false`, `gate_effect: NONE`, and
no advance to a stress tensor, semiclassical background, Hessian, A4 or Ultra.

## Plan 11 — five-dimensional Hadamard/subtraction readiness

Run the separately frozen local-scaffold and completion-inventory audit with:

```powershell
python Analysis\TOP\TOP-X4\topx4_s2f3_hadamard_subtraction_readiness.py
```

The recorded bounded status is:

```text
PASS_5D_HADAMARD_COUNTERTERM_SCAFFOLD_HOLD_FULL_OPERATORS_STATE_AND_STRESS
```

All 20/20 checks pass. The executable recovers the scalar `D=5` Hadamard
singularity through `U_2`, the general matrix Laplace-type `b_0,b_1,b_2` map,
the `Lambda^5`, `Lambda^3`, `Lambda` proper-time structure, and the five
independent pure-gravity counterterms. It rejects six scope mutations and
keeps the static Poisson `q=0` subtraction separate from evolving
state-dependent stress renormalization.

The binding readiness decision is `HOLD`: the off-shell covariant
charged-scalar/`chi` matrix second variation, scalar and Dirac Hadamard states,
curved graviton/ghost operators, parity-odd phase and counterterm
normalizations are not completed. Accordingly `hadamard_stress_ready: false`,
`physics_pass: false`, `gate_effect: NONE`; no stress, background, Hessian, A4
or Ultra follows.

## Plan 11 — covariant scalar-matrix checkpoint

Run the frozen fixed-metric off-shell scalar-operator checkpoint with:

```powershell
python Analysis\TOP\TOP-X4\topx4_s2f3_covariant_scalar_matrix_checkpoint.py
```

The recorded bounded status is:

```text
PASS_COVARIANT_SCALAR_CHI_MATRIX_OPERATOR_HOLD_STATES_GRAVITY_PARITY_AND_STRESS
```

All 25/25 checks pass. The executable derives the rank-three Hessian for
`(sqrt(2) Re Phi, sqrt(2) Im Phi, chi)` on an arbitrary fixed
five-dimensional background before any homogeneous or fixed-charge ansatz.
It verifies `E=-H`, zero Cartesian bundle curvature, the pure-gauge
phase-aligned connection, `U(1)` and `chi -> -chi` covariance, and the
scalar-induced counterterm structures through `b_2`. Seven bad mutations are
rejected and three clean runs produce byte-identical JSON.

The result completes only the fixed-metric scalar-operator inventory line.
`counterterm_normalizations: NOT_FIXED`,
`scalar_matrix_hadamard_state: NOT_CONSTRUCTED`,
`determinant: NOT_COMPUTED`, `renormalized_stress: NOT_COMPUTED`,
`physics_pass: false` and `gate_effect: NONE` remain binding. The next
single gate is a scalar matrix Hadamard parametrix/state construction; gravity,
spinor, parity, physical-Hessian, A4 and Ultra work remain closed or separate.

## Plan 11 — scalar-matrix Hadamard parametrix

Run the frozen local checkpoint with:

```powershell
python Analysis\TOP\TOP-X4\topx4_s2f3_scalar_matrix_hadamard_parametrix_checkpoint.py
```

The recorded bounded status is:

```text
PASS_SCALAR_MATRIX_HADAMARD_PARAMETRIX_HOLD_GLOBAL_STATE_AND_STRESS
```

All 22/22 checks pass. The result verifies the D5 local singular structure,
Cartesian `U_0`, the matrix `U_1`/`U_2` coincidence controls, the registered
`E=-H` sign, the generic `Omega` contribution, and the phase-aligned
pure-gauge connection with derivative mixing. A flat constant-matrix
transport realization is included as the executable matrix recurrence check.

The result derives only local parametrix data through `U_2`; it does not
construct the arbitrary-background off-diagonal biscalars or the smooth,
positive, globally admissible state term `W`. Therefore
`scalar_matrix_hadamard_parametrix=DERIVED_LOCAL_U0_U2`,
`scalar_matrix_hadamard_state=NOT_CONSTRUCTED`, `determinant=NOT_COMPUTED`,
`renormalized_stress=NOT_COMPUTED`, `physics_pass=false`, and
`gate_effect=NONE` remain binding. Counterterm normalizations, Dirac and
graviton/ghost states, parity/anomaly, physical Hessian, A4 and Ultra remain
closed or separate; no downstream promotion follows.
