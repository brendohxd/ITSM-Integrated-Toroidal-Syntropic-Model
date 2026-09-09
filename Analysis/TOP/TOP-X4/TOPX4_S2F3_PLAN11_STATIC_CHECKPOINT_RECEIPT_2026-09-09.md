# TOP-X4 / X4-S2F3 — Plan 11 static checkpoint receipt

Date: 2026-09-09  
Route: `TOP-X4_KK-001`  
Candidate: `X4-S2F3`  
Scope: zero-density, static `Minkowski4 x S1`, parity-even determinant only

## Decision

The sealed checkpoint completed with `12/12` calculation checks passing:

```text
PASS_STATIC_PARITY_EVEN_DETERMINANT_HOLD_PARITY_ODD_AND_FINITE_CHARGE
checkpoint_decision=HOLD_BEFORE_FINITE_CHARGE
physics_pass=false
gate_effect=NONE
advance_to_finite_charge=false
advance_to_a4=false
```

This is a bounded mathematical checkpoint. It is not a parent-level stabilization result, a physical radion-mass result, a finite-charge background, an anomaly clearance, or a publication gate.

## Reproduced witness

For the frozen equal-mass `N_F=3` control, the independently scanned stationary zero-vacuum root is

```text
x = 2.53067902130963261758981684772
alpha = 0.0105888717092240159635357605738
f_second = 4.1680216387683411009576707474
Delta_KK/Lambda5 at mF/Lambda5=0.04 = 0.0993122439356694493372858780888
```

The checkpoint also reproduces the scalar/Dirac parity-even ratio `-4`, the five-dimensional graviton degree count `5`, the `N_F=2` equal-mass no-root control, deliberate fermion-sign rejection, omitted-Poisson-image rejection, and the registered coarse `0.5..2.0` mass-ratio grid.

The `N_F=2` control is recorded narrowly: leading small-radius balance is marginal, while the next equal-mass term is attractive; this is not a finite-charge or unequal-mass theorem.

## Quantum definition and limitations

The calculation uses the decompactification-subtracted finite Casimir term, proper-time/Poisson and modified-Bessel/polylog representations, periodic spectator fermions, and the positive-frequency Minkowski vacuum. The local renormalized bulk vacuum term remains separate. The following remain open holds:

- parity-odd determinant phase, regulator/counterterm data, and global/nonperturbative spin-structure audit;
- complete finite-charge semiclassical variation and the charge-dependent spectrum;
- Hadamard/adiabatic state and state-order convergence for an evolving background;
- coupled metric-radion-amplitude-phase constraints and physical radion pole/mass;
- continuous finite-charge robustness and complete EFT-domain scan.

## Reproducibility receipts

The calculation output is:

`outputs/topx4_s2f3_static_determinant_summary.json`  
SHA-256: `04d7d96758285dc5e1133a95f6a1a9b1c2f6732dde38f21ecc9771668a36c419`

The sealed source is:

`topx4_s2f3_static_determinant_checkpoint.py`  
SHA-256: `ded1c191dc220ef8bc8ace922b9bf888357fb5a7bf8e6b2ac94b8c10b441ee5a`

## Rule-9 reviewer receipt

The sealed prompts were dispatched with these hashes:

| Role | Agent | Prompt SHA-256 | Outcome |
|---|---|---|---|
| A | `01a0852c-0f75-7970-b2be-6e8fc39190b7` | `43ea7a33a6e70502fe944504a685b72e00b31bd5b5ba681aa423577f4c0d4f92` | Completed; bounded review agrees with the parity-even result and qualifies the `N_F=2` wording |
| B | `01a0852c-1093-7af3-a9c0-2ea72b5ef93b` | `f88c7c9ebdfc26bbd04beab71e93e6276338675c58eb8aebaac848343f20a6e3` | No output; agent returned usage-limit error |
| C | `01a0852c-2252-7291-8cdf-78720646d048` | `47074647a291a7d13f5c18c12e679a0e717451c5e1ea6fad7e187087544a4f46` | No output; agent returned usage-limit error |

Therefore Rule-9 three-way independent clearance is **not met**. No claim of three-way agreement is made, and the Plan 11 route remains held before finite charge.
