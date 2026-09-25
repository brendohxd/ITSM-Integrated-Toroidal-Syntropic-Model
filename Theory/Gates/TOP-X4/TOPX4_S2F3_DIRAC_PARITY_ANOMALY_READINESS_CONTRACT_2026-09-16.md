# TOP-X4 `X4-S2F3` Dirac/parity/anomaly readiness contract

**Date:** 2026-09-16  
**Status:** `FROZEN_READINESS_AUDIT`  
**Scope:** Dirac completion, parity-odd determinant phase, anomaly data and
quantized-counterterm readiness only  
**Gate effect:** none

## 1. Purpose and stop boundary

This contract freezes one single-gate audit of the fermionic and parity-odd
inputs required before a five-dimensional finite-charge determinant or
semiclassical stress calculation can be considered. It does not derive a new
Dirac operator, construct a spinor Hadamard state, evaluate a determinant,
cancel an anomaly, fix a counterterm level or promote `X4-S2F3`.

The audit distinguishes the existing bounded first-order Dirac transport
control from the dimension-appropriate infinite-order state and the complete
curved finite-charge fermion effective action. It also distinguishes the
parity-even determinant magnitude from the parity-odd phase, which is not
recovered by squaring a Dirac operator.

## 2. Required closure inputs

| Required input | Minimum evidence | Current boundary |
|---|---|---|
| Full curved five-dimensional Dirac operator | Vielbein, spin connection, Clifford convention, mass/charge normalization and domain on the registered finite-charge background | `NOT_CLOSED`; the repository has a frozen static spectator action and a finite-order transport control, not this completed input set |
| Dimension-appropriate Dirac state | Infinite-order Hadamard/pseudodifferential two-point construction, positivity and wavefront condition | `NOT_CONSTRUCTED`; the existing projector is first order |
| Evolving finite-charge fermion determinant | State, background, regulator and mode/spectral prescription on the coupled solution | `NOT_COMPUTED`; the static Casimir result is not reused |
| Parity-odd determinant phase | Regulator/reference phase, spin structure, spectral-flow or equivalent global definition and its domain | `NOT_DERIVED` |
| Anomaly data | Explicit local/global anomaly calculation for the frozen field content, geometry and allowed transformations | `NOT_DERIVED` |
| Quantized local counterterms | Complete parity-odd counterterm basis, normalization and quantization/cancellation test | `NOT_FIXED` |
| Gravity/ghost and constraint coupling | Curved gauge-fixed metric sector and its coupling to the fermion determinant before physical-Hessian reduction | `NOT_AVAILABLE` |
| Independent review | Role-separated mathematical, numerical and claim-hygiene reports with explicit comparison | `NOT_MET`; Rule-9 remains `THREE_WAY_CLEARANCE_NOT_MET` |

The static periodic-spin-structure determinant and the exact first-order
transport receipt are valid controls at their declared scopes. Neither one
supplies the missing curved, state-dependent, parity-odd or anomaly data.

## 3. Binding decision

While any required input is absent, the only admissible result is:

```text
HOLD_TOPX4_DIRAC_PARITY_ANOMALY_INPUTS_NOT_CLOSED
dirac_completion=NOT_DERIVED
dirac_hadamard_state=NOT_CONSTRUCTED
parity_odd_determinant_phase=NOT_DERIVED
anomaly_cancellation=NOT_DERIVED
counterterm_quantization=NOT_FIXED
physics_pass=false
gate_effect=NONE
```

The executable may pass its own bookkeeping and rejection checks while
returning this hold. A `PASS` from those checks is not a physics pass.

## 4. Deterministic rejection tests

The readiness executable must reject each of the following attempted
shortcuts:

1. identify the zero-density static parity-even determinant with the complete
   finite-charge fermion effective action;
2. treat a first-order Dirac projector and exact unitary transport as an
   infinite-order five-dimensional Hadamard state;
3. infer the parity-odd phase or anomaly cancellation from a squared Dirac
   operator or from the parity-even Casimir magnitude;
4. import a four-dimensional/even-dimensional structural result as the
   repository-specific five-dimensional spinor construction without a stated
   extension and proof obligations;
5. set a missing anomaly, counterterm, spin-structure or ghost contribution to
   zero without deriving that value from the frozen action; and
6. use an observational target, desired scale or downstream gate status to
   select a root or declare fermionic closure.

## 5. Current expected boundary

The registered artifacts establish a frozen periodic spectator field content,
a static parity-even determinant control and a bounded first-order Dirac
transport control. They do not establish a full curved Dirac state, a
state-dependent determinant, a parity-odd phase, an anomaly result or
quantized counterterms. The readiness audit must therefore leave
`physics_pass=false`, `gate_effect=NONE`, A4/Ultra closed, and all MAT, UVIR,
cosmology, BBN, Rule-9 and publication statuses unchanged.
