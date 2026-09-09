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
