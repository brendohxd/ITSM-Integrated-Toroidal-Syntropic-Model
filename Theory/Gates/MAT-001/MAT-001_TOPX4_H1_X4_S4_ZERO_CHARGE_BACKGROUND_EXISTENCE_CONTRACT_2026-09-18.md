# MAT-001 TOP-X4 H1 X4-S4 zero-charge background-existence contract

**Date:** 2026-09-18  
**Status:** FROZEN_NON_PROMOTING_BACKGROUND_EXISTENCE_TEST  
**Candidate:** X4-S4-GW2  
**Parent acceptance:** NOT_AUTHORIZED  
**Finite-charge continuation:** CLOSED  
**Gate effect:** NONE

## 1. Purpose and stop boundary

This gate tests one preregistered, dimensionless, zero-charge warped static
benchmark of the frozen X4-S4-GW2 candidate. It is a boundary-value and
consistency test, not a fit and not a proof that the candidate works over its
full parameter domain.

The test must solve the fully backreacted six-function classical system with
both scalar Robin conditions, both gravitational junction conditions and a
fixed gauge normalization. The Hamiltonian constraint and the integrated
static balance are independent residual audits; neither is supplied as a
solver boundary condition to force a result.

The gate stops immediately after this benchmark. A successful benchmark does
not authorize finite charge, determinant, stress, physical Hessian, H1,
MAT-001, Rule-9 or publication promotion. A failed benchmark rejects this
registered benchmark and returns X4-S4-GW2 to action selection; it may not be
repaired by changing parameters after seeing the numerical output.

## 2. Frozen zero-charge ansatz

Use a proper interval coordinate `z` and a dimensionless numerical coordinate
`x=z/L` with `x in [0,1]`, where `L>0` is solved as an internal modulus:

    ds^2 = exp(2 A(z)) eta_mu_nu dx^mu dx^nu + dz^2,
    Phi(z) = f(z) in R,
    varphi(z) = h(z) in R,
    Q = 0.

The constant phase is allowed because this gate has zero temporal charge. No
interval phase winding is used. The gauge normalization is `A(0)=0`; it is a
coordinate normalization and not an observational calibration.

The first-order variables in `x` are

    A_x = p,
    f_x = u,
    h_x = v.

The equations exported to the executable are

    A_x = p,
    p_x = -(2 u^2 + v^2)/(3 M5^3),

    f_x = u,
    u_x = -4 p u + L^2 [mPhi2 + lambdaPhi5 f^2
                         + (g5/2) h^2] f,

    h_x = v,
    v_x = -4 p v + L^2 [mvarphi2 h
                         + (lambdavarphi5/6) h^3 + g5 f^2 h].

These equations follow from the frozen action with `Phi=f` real. The
independent zero-charge Einstein constraint is

    C(x) = 6 M5^3 (p/L)^2 - (u/L)^2 - (v/L)^2/2
           + Lambda5 + U(f^2,h) = 0.

The test requires the maximum absolute constraint residual over the mesh to
be below the preregistered numerical tolerance.

## 3. Frozen boundary system

Let

    V_i(f,h) = tau_i + kappa_i (h^2-v_i^2)^2/4 + zeta_i f^2.

The outward-normal scalar conditions become

    u(0) - L zeta_0 f(0) = 0,
    u(1) + L zeta_pi f(1) = 0,

    v(0) - L kappa_0 h(0)[h(0)^2-v_0^2] = 0,
    v(1) + L kappa_pi h(1)[h(1)^2-v_pi^2] = 0.

The interval gravitational junction conditions with the frozen GHY sign are

    p(0) + L V_0(f(0),h(0))/(3 M5^3) = 0,
    p(1) - L V_pi(f(1),h(1))/(3 M5^3) = 0.

The seventh boundary residual is the gauge normalization `A(0)=0`. No
upstairs factor of two is inserted.

## 4. Preregistered internal benchmark

All quantities are expressed in powers of the internal unit `M5=1`. The
values are selected before execution, are not taken from observations, and do
not represent a physical parameter estimate:

| Parameter | Value |
|---|---:|
| `M5` | `1` |
| `Lambda5` | `-6` |
| `mPhi2` | `1/4` |
| `mvarphi2` | `1/4` |
| `lambdaPhi5` | `1/5` |
| `lambdavarphi5` | `1/5` |
| `g5` | `1/10` |
| `kappa_0`, `kappa_pi` | `10` |
| `v_0` | `1` |
| `v_pi` | `2/5` |
| `zeta_0`, `zeta_pi` | `1/20` |
| `tau_0` | `3` |
| `tau_pi` | `-16/5` |

The benchmark is a deliberately non-symmetric two-surface action point. Its
negative `tau_pi` is a preregistered internal action parameter required to let
the global static balance be tested; it is not inferred from a cosmological
or galactic observable.

## 5. Numerical acceptance and rejection tests

The executable must:

1. verify all authority receipts and sidecars;
2. solve the registered ODE/BVP without changing the benchmark;
3. report solver convergence, mesh size, `L`, finite fields and finite
   derivatives;
4. verify all seven boundary residuals independently;
5. verify the Einstein constraint over the complete mesh;
6. verify the static integrated balance with the complex-scalar weight two;
7. verify no observational target, finite charge or H1 quantity entered;
8. reject nonconverged, nonfinite, negative-`L`, boundary-failing or
   constraint-failing outputs; and
9. reject any downstream promotion flags.

The numerical tolerances are fixed before the solve:

    solve tolerance = 1e-7,
    boundary residual tolerance = 5e-5,
    constraint tolerance = 5e-5,
    sum-rule tolerance = 5e-5,
    minimum nonsingular modulus = 1e-4,
    regularity bound = 1e6.

These are numerical tolerances, not physics uncertainties.

## 6. Static sum-rule audit

For the zero-charge flat-four-slice seed, the executable evaluates

    B = V_0^ren + V_pi^ren
        + integral_0^L dz [ (d_z h)^2 + 2 (d_z f)^2 ].

The test requires `B=0` within the fixed sum-rule tolerance. The coefficient
two is independently derived from the stress combination
`T_mu^mu - 4 T_z^z`; it is not copied from a target or inserted as a label.

This static identity is not reused at finite temporal charge. A successful
zero-charge result therefore leaves finite-charge continuation closed.

## 7. Binding status

Before execution:

    candidate_action_contract_frozen=true
    X4-S4_parent_accepted=false
    finite_charge_background_solved=false
    physical_hessian_constructed=false
    MAT-001=BLOCKED
    K_Q=NOT_DERIVED
    V=NOT_COMPUTED
    Stage4A=CLOSED
    Rule9_cleared=false
    physics_pass=false
    gate_effect=NONE

The receipt status may be either `BENCHMARK_SOLUTION_FOUND_HOLD_FINITE_Q`
or `BENCHMARK_REJECTED_RETURN_TO_ACTION_SELECTION`. Neither status accepts
X4-S4-GW2 as the TOP-X4 parent.
