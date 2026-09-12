# TOP-X4 / X4-S2F3 — Plan 11 finite-charge operator checkpoint

Date started: 2026-09-09
Date completed: 2026-09-12
Scope: constant-background charged-scalar operator and fixed-global-charge variation contract

## Decision

The executable checkpoint completed `16/16` exact calculation and mutation
checks:

```text
PASS_FINITE_CHARGE_OPERATOR_HOLD_DYNAMIC_STATE_STRESS_AND_HESSIAN
physics_pass=false
gate_effect=NONE
advance_to_dynamic_determinant=false
advance_to_a4=false
advance_to_ultra=false
```

This is a bounded operator/variation result. It is not the finite-charge
determinant, a renormalized state-dependent stress tensor, a coupled physical
Hessian, a stabilized radion result or a parent-level physics pass.

## Result established

For canonical fluctuations
`rho=rho_0+sigma` and `theta=mu*t+pi/rho_0`, the independently expanded
constant-background quadratic action contains the required
`2*mu*sigma*pi_dot` mixing. Its frequency polynomial is

```text
(omega^2-k_n^2-M_sigma^2)(omega^2-k_n^2)-4*mu^2*omega^2=0
```

with `k_n^2=k_obs^2+n^2/b^2`. At zero momentum it has one Goldstone branch
and one amplitude branch with
`omega_+^2=M_sigma^2+4*mu^2`; the low-momentum Goldstone speed is
`M_sigma^2/(M_sigma^2+4*mu^2)` in the declared stable domain.

The fixed-charge Routhian

```text
L_Q=-N*Q^2/(2*a^3*b*rho^2)
```

reproduces the registered radial centrifugal term and positive phase-kinetic
energy and pressures. This seals the ensemble boundary: the conserved global
charge is not replaced by an externally inserted chemical potential.

The checkpoint also rejects deliberate omitted-mixing and wrong-sign-Routhian
mutations. The zero-charge operator factorizes correctly, and the neutral
spectator fermions have no direct `mu` shift.

## Open hold

The following remain required before any finite-charge completion:

- the coupled time-dependent mode system on the A1 background;
- a declared Hadamard/adiabatic state and subtraction terms;
- adiabatic-order convergence and a renormalized state-dependent stress tensor;
- metric-radion-amplitude-phase constraint reduction and physical Hessian;
- parity-odd determinant phase, anomaly and quantized-counterterm audit;
- continuous mass-ratio, cutoff, state and regulator robustness.

A4, Ultra, phenomenology, publication and canonical-model revision remain
closed.

## Reproducibility

- Source: `topx4_s2f3_finite_charge_operator_checkpoint.py`
- Source SHA-256: `ed06de54970da29adf191dbb0ca2185ebaad8e0753d60894f5a8a26b29d18845`
- Output: `outputs/topx4_s2f3_finite_charge_operator_summary.json`
- Output SHA-256: `53d9e3673224b68c4ebeedf861fbb88d7b830d48bbe2bc6a53180cb5db79885b`
- Variation contract: `Theory/Gates/TOP-X4/TOPX4_S2F3_FINITE_CHARGE_VARIATION_CONTRACT_2026-09-09.md`
- Contract SHA-256: `916e4beb4c295845e684c32da2bb921cde8942e7d48ea69f05eba92c1bb1a2fa`
- Two consecutive executions produced byte-identical output.

## Rule-9 status

Three auxiliary review jobs were requested during the original run. One
returned an account usage-limit error and no review; the other two produced no
report before the resumed bounded wait ended. They were stopped on 12
September rather than treated as successful reviewers. Rule-9 three-way
clearance is therefore **not met**, and no model-consensus claim is made.
