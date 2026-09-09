# TOP-X4 / X4-S2F3 — finite-charge entry-gate receipt

Date: 2026-09-09  
Scope: Plan 11 transition from the static determinant checkpoint toward finite charge

## Decision

The executable entry gate completed `9/9` provenance and policy checks:

```text
HOLD_TOPX4_S2F3_BEFORE_FINITE_CHARGE_QUANTUM_COMPLETION
physics_pass=false
gate_effect=NONE
advance_to_finite_charge=false
advance_to_a4=false
```

This is a safe hold, not a failed numerical calculation. It confirms that the prerequisite controls are available while preserving the missing finite-charge quantum work as an explicit blocker.

## Revalidated inputs

- A1 action/metric variation: `9/9`, status `PASS_TOPX4_A1_INDEPENDENT_SYMBOLIC_AUDIT`.
- A1 classical finite-charge background: `7/7`, status `PASS_TOPX4_A1_CONTROL_BACKGROUND_ONLY`.
  - Hamiltonian residual: `9.4102503567228268e-13`.
  - Relative global-charge drift: `1.7201795543542175e-12`.
  - Stress-continuity residual: `4.9960036108132044e-16`.
- A2/A3 classical boundary: `15/15`, status `HOLD_TOPX4_A2A3_UNSTABILIZED_CONTROL` and `HOLD_UNSTABILIZED_RADION`.
- S2F3 static parity-even determinant: `12/12`, status `PASS_STATIC_PARITY_EVEN_DETERMINANT_HOLD_PARITY_ODD_AND_FINITE_CHARGE`.

## Explicit quantum boundary

The static determinant declares only a positive-frequency Minkowski vacuum on static `Minkowski4 x S1`, with decompactified Poisson image subtraction. The entry gate confirms that the following finite-charge inputs are not yet present:

- a finite-density spectrum and state-dependent one-loop stress tensor;
- a Hadamard/adiabatic state with order-convergence evidence;
- the parity-odd determinant phase, global-anomaly data and quantized counterterms;
- the coupled metric-radion-amplitude-phase constraint reduction and physical Hessian.

The gate contains no import or reuse of the static determinant solver as a dynamic background solver. This prevents the static vacuum formula from being silently inserted into the evolving A1 background.

## Receipts

Executable gate:

`topx4_s2f3_finite_charge_entry_gate.py`  
SHA-256: `da804ba76958277bf31b7b4d4e3dff8752aa9fcf610d01ed515cab5b63ef83fd`

Gate output:

`outputs/topx4_s2f3_finite_charge_entry_gate_summary.json`  
SHA-256: `aaa582e9d0391b641910b7efe3193c234674bfd245d35ce8454a31f228a72c6a`

No A4, Ultra, phenomenology, publication, or canonical-model revision is opened by this receipt.
