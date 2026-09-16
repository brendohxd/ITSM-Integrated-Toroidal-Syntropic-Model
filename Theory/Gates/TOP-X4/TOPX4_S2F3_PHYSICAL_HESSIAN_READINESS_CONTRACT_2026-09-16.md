# TOP-X4 `X4-S2F3` physical-Hessian readiness contract

**Date:** 2026-09-16
**Status:** `FROZEN_READINESS_AUDIT`
**Scope:** readiness of the physical constrained Hessian only
**Gate effect:** none

## 1. Purpose and stop boundary

This contract freezes one single-gate audit: whether the registered
`X4-S2F3` artifacts contain the inputs needed to calculate the physical
scalar/radion Hessian after metric constraints are eliminated. It does not
calculate a Hessian, a radion mass, a determinant, a stress tensor or a new
background. It cannot change `physics_pass`, open A4 or Ultra, or promote any
downstream gate.

The audit must distinguish the fixed-metric scalar operator from the physical
constrained system. A positive eigenvalue of the former is not evidence for
the latter.

## 2. Required physical construction

The target object is the quadratic form obtained only after varying the
complete renormalized semiclassical action,

\[
 \Gamma=S_{I1C}+\Gamma_{\rm even}+\Gamma_{\rm odd}+\Gamma_{\rm ct},
\]

before imposing the homogeneous or fixed-charge ansatz. After the lapse,
shift, metric-scalar, radion, amplitude and phase blocks are declared, the
physical reduction must specify the auxiliary block and its singular domain.
Where the auxiliary block is invertible, the reduced Hessian has the Schur
form

\[
 H_{\rm phys}=H_{qq}-H_{qa}H_{aa}^{-1}H_{aq}.
\]

This formula is a construction requirement, not an input value or a license
to set a missing mixing block to zero.

## 3. Required inputs

The readiness audit records each item explicitly:

1. an on-shell finite-charge background from the complete varied action;
2. the state-dependent one-loop determinant and renormalized stress tensor;
3. scalar, Dirac, graviton, ghost and parity/anomaly sectors with their
   counterterm normalizations;
4. the pre-constraint kinetic, gradient and mass blocks for all retained
   scalar/metric variables;
5. the lapse, shift and other auxiliary constraint block, including its
   invertibility and singular-domain treatment;
6. the fixed-charge/phase constraint and the declared global-charge ensemble;
7. regulator, subtraction, state-order and resolution robustness over the
   registered domain; and
8. a deterministic reduced-Hessian output with negative controls.

## 4. Binding audit decision

The only admissible result while any required item is absent is

```text
HOLD_PHYSICAL_HESSIAN_INPUTS_NOT_CLOSED
physical_hessian=NOT_CONSTRUCTED
radion_mass=NOT_COMPUTED
physics_pass=false
gate_effect=NONE
```

The audit may pass its own bookkeeping checks while returning this hold. A
fixed-metric rank-three operator, local Hadamard data, a theorem-backed scalar
state, or exact finite-order transport does not satisfy the physical-Hessian
contract by itself.

## 5. Rejection tests

Reject the attempted construction if it:

- substitutes the static zero-density determinant for the finite-charge
  state-dependent effective action;
- identifies the fixed-metric scalar Hessian with the constrained physical
  Hessian;
- inserts zero metric/radion mixing without deriving it from the action;
- treats the scalar state construction as a renormalized stress result;
- evaluates a Schur complement outside the declared auxiliary-block domain;
- reports a radion mass without canonical normalization; or
- uses an observational target or desired scale to select a root.

## 6. Current expected boundary

The registered artifacts presently supply a bounded scalar operator and a
theorem-backed scalar-state construction, but do not supply the complete
semiclassical stress, gravity/ghost/parity sectors, counterterm normalizations,
finite-charge on-shell background or constraint blocks. The expected decision
is therefore the binding hold above. No value is inferred from the available
static or dimensionless controls.
