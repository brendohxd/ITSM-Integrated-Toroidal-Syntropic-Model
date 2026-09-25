# MAT-001 TOP-X4 H1 X4-S4 action selection after zero-charge test

**Date:** 2026-09-19  
**Status:** SELECT_CURVED_SLICE_OUTPUT_ROUTE_HOLD_EXECUTION  
**Candidate:** X4-S4-GW2 remains unaccepted  
**Supersedes:** no prior receipt; the rejected flat benchmark remains immutable  
**Gate effect:** NONE

## 1. Decision

The failed zero-charge benchmark is not rerun and none of its parameters are
changed. Its result remains

    BENCHMARK_REJECTED_RETURN_TO_ACTION_SELECTION.

The failure is adjudicated as a flatness-closure failure at the registered
action point, not as evidence that every X4-S4 action is impossible and not as
an equation-sign defect. The next selected route is a maximally symmetric
four-slice calculation in which the signed four-dimensional curvature
`kappa4` is an output of the same frozen bulk and localized action.

The selected route is

    X4-S4-C1 = CURVED_SLICE_BACKGROUND_OUTPUT_TEST.

It preserves all previously frozen action parameters. It does not choose
`kappa4` from an observed Hubble value or require it to vanish.

## 2. Why the flat benchmark was overclosed

For the flat static ansatz, the three second-order functions `A`, `f` and `h`
supply six integration constants. The proper interval length `L` is one
additional unknown. The registered BVP used exactly seven conditions:

1. one warp normalization `A(0)=0`;
2. four scalar Robin conditions; and
3. two gravitational junction conditions.

The independent Einstein/Hamiltonian constraint is an eighth condition. Once
all action parameters and flatness are fixed, it is therefore a codimension-one
compatibility condition. Equivalently, flat branes require one relation among
the bulk vacuum data and localized vacuum terms.

For

    C0 = 6 M5^3 A_z^2 - f_z^2 - h_z^2/2 + Lambda5 + U(f^2,h),

the frozen bulk equations give

    dC0/dz = 4 A_z [3 M5^3 A_zz + 2 f_z^2 + h_z^2] = 0.

Thus the constraint is propagated by the evolution equations but its constant
value must be fixed once. The failed solver found branches satisfying the
evolution and boundary equations while carrying the wrong nonzero value of
`C0`; the near-zero `L` branches do not cure that incompatibility.

This is the standard flat-brane tuning structure described by
DeWolfe-Freedman-Gubser-Karch and by the compact-space sum rules:

    https://arxiv.org/abs/hep-th/9909134
    https://arxiv.org/abs/hep-th/0011225

## 3. Selected maximally symmetric extension

Retain the same fields and action, but use

    ds^2 = exp(2 A(z)) ghat_mu_nu dx^mu dx^nu + dz^2,
    Rhat_mu_nu = 3 kappa4 ghat_mu_nu,
    Phi=f(z) in R,
    varphi=h(z),
    Q=0.

`kappa4>0`, `kappa4=0`, and `kappa4<0` denote de Sitter, flat and anti-de
Sitter four-slices in this convention. Its sign and magnitude are solver
outputs. Curved branes from non-fine-tuned localized vacuum data are a known
possibility; the route class is independently exemplified by

    https://arxiv.org/abs/hep-th/0011156

In the dimensionless coordinate `x=z/L`, with `p=A_x`, `u=f_x`, and `v=h_x`,
the modified warp equation is

    p_x = -L^2 kappa4 exp(-2A)
          -(2u^2+v^2)/(3 M5^3).

The scalar equations and Robin conditions are unchanged. The independent
constraint is

    Ck = 6 M5^3 [(p/L)^2-kappa4 exp(-2A)]
         -(u/L)^2-(v/L)^2/2+Lambda5+U(f^2,h) = 0.

`kappa4` is an eighth unknown. The next solver must impose `Ck(0)=0` in
addition to the previous seven conditions, and then verify `Ck` over the full
mesh rather than treating it as a fitted residual.

## 4. Induced-curvature terms and junctions

The frozen action contains independent localized induced-curvature
coefficients `Mi2`. They vanish from the previous flat benchmark, so their
absence there did not select a value. For the next tree-level diagnostic the
following explicit reference-scale condition is preregistered:

    M0^2(mu0)=0,
    Mpi^2(mu0)=0,

with `S_ct=O(hbar)`. This is a stated tree-level benchmark condition, not an
omission and not a claim that matter loops leave these coefficients zero.

For nonzero `Mi2`, the outward-normal junction equations would be

    p(0) + L V0/(3 M5^3)
         - L M0^2 kappa4 exp[-2A(0)]/M5^3 = 0,

    p(1) - L Vpi/(3 M5^3)
         + L Mpi^2 kappa4 exp[-2A(1)]/M5^3 = 0.

The next executable must retain these terms symbolically even though the
preregistered tree-level numerical values are zero.

## 5. Generalized integrated balance

On the covering circle, with each fixed-point term counted once, the curved
static balance is

    0 = V0 + Vpi
        + integral_S1 dz [h_z^2+2 f_z^2]
        + 3 kappa4 [
              M5^3 integral_S1 dz exp(-2A)
              - M0^2 exp[-2A(0)]
              - Mpi^2 exp[-2A(L)]
          ].

At `kappa4=0` this reduces to the previously frozen flat sum rule. The next
test must compute this identity independently from the solved fields and must
not infer it from the imposed pointwise constraint.

## 6. Route comparison

### Selected primary route: C1 curved-slice output

- Keeps every previously registered bulk and localized benchmark parameter.
- Adds only the curvature integration parameter required by the general
  maximally symmetric ansatz.
- Determines whether the failed flat benchmark has a regular de Sitter or
  anti-de Sitter continuation.
- Does not solve the cosmological-constant problem and does not compare
  `kappa4` to observation at this gate.

### Retained secondary diagnostic: F1 flat-tension eigenvalue

Keep `kappa4=0`, promote one localized vacuum coefficient such as `tau_pi` to
an eigenparameter, impose the pointwise constraint, and solve for the exact
flatness tuning relation. This route may quantify the required tuning but
cannot count as a prediction or natural explanation. It is not selected for
the next execution.

### Deferred action-changing route: W1 superpotential-correlated action

A bulk potential and brane potentials generated from a common superpotential
can satisfy flatness relations by construction. That would change the frozen
X4-S4-GW2 action and requires a new parent-action contract. It is not silently
introduced here.

### Rejected route: R0 unchanged rerun

Rerunning the same flat benchmark with the same equations and parameters is
rejected. Changing an initialization is allowed only inside the existing
bounded solver protocol; changing a physical parameter after seeing the
failure would be post-result tuning.

## 7. Next gate and rejection conditions

The next single gate is

    TOPX4_H1_X4-S4_CURVED_SLICE_BACKGROUND_OUTPUT_TEST.

It must use the already registered benchmark parameters, add only
`M0^2=Mpi^2=0` at the named tree-level reference scale, and solve `kappa4` as
an unconstrained signed output. It must reject or return inconclusive if:

- no regular finite-`L` branch converges under bounded initializations;
- the pointwise constraint fails away from the imposed endpoint;
- either scalar or gravitational boundary system fails;
- the generalized integrated balance fails;
- the solution depends on an observational target or a sign restriction on
  `kappa4`; or
- a finite-charge or downstream quantity is inferred.

## 8. Binding firewall

    failed_flat_benchmark_preserved=true
    unchanged_flat_rerun_authorized=false
    selected_route=CURVED_SLICE_BACKGROUND_OUTPUT_TEST
    kappa4_selected_from_observation=false
    flat_tension_eigenvalue_route=SECONDARY_DIAGNOSTIC_ONLY
    action_changed=false
    X4-S4_parent_accepted=false
    finite_charge_background_solved=false
    physical_hessian_constructed=false
    signed_H1_residue_computed=false
    MAT-001=BLOCKED
    K_Q=NOT_DERIVED
    V=NOT_COMPUTED
    Stage4A=CLOSED
    Rule9_cleared=false
    physics_pass=false
    gate_effect=NONE

