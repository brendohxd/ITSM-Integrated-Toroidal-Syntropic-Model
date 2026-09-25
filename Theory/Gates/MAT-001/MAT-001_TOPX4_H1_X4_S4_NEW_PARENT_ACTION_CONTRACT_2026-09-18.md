# MAT-001 TOP-X4 H1 X4-S4 new-parent action contract

**Date:** 2026-09-18  
**Status:** FROZEN_CANDIDATE_ACTION_CONTRACT_NON_PROMOTING  
**Candidate label:** X4-S4-GW2  
**Frozen control:** X4-S2F3 remains unchanged  
**Gate effect:** NONE

## 1. Decision and scope

This contract freezes one separately identified X4-S4 candidate strongly
enough to run a classical background-existence test. It does not accept the
candidate as the TOP-X4 parent and does not modify, repair or supersede the
frozen X4-S2F3 smooth-circle control.

The distinction is binding:

    candidate_action_contract_frozen=true
    classical_action_frozen_for_one_background_test=true
    parent_accepted=false

The action, geometry, variational signs and parameter domain below may not be
changed inside the background test. A failed background, junction, sum-rule,
regularity or stability check rejects this candidate or returns it to a new
action-selection gate; it may not be repaired after seeing an observational
target.

The construction is a Goldberger-Wise-class two-fixed-surface route with
full metric backreaction retained. The literature motivates the class of
operators and checks; it does not derive this ITSM candidate or confer a
physics pass.

## 2. Geometry and orbifold data

The candidate spacetime is

    M5 = R_t x T3_obs x I,
    I = S1/Z2,
    y in [0, pi].

`T3_obs` remains the observed spatial topology. The interval `I` is a new
extra-dimensional factor and is not a replacement for `T3_obs`. Its fixed
surfaces are

    Sigma_0  at y=0,
    Sigma_pi at y=pi.

The fundamental-interval action is used. Each surface has its own outward
unit normal `n_i^A`; all boundary equations below use that convention. A
covering-space jump equation is equivalent only after the corresponding
Z2 factor of two and normal orientation are derived from the same action.

Orbifold parities are frozen as follows:

- `G_{mu nu}`, `G_{yy}`, the complex condensate `Phi`, and the neutral
  stabilizer `varphi` are even;
- `G_{mu y}` is odd; and
- the normal shift is odd in a homogeneous ADM decomposition.

There is no protected winding sector along `I`. In particular, no phase
condition of the form `Theta(y+2 pi)-Theta(y)=2 pi n` is admitted as a source
of stabilization. The global charge is temporal and is defined in Section 7.

The signature is `(-,+,+,+,+)`. The extrinsic curvature convention is

    K_{mu nu} = (1/2) L_n gamma_{mu nu},
    K = gamma^{mu nu} K_{mu nu}.

## 3. Frozen field content

The candidate contains exactly:

1. the five-dimensional metric `G_AB`;
2. the existing complex finite-charge condensate `Phi`, with
   `s = Phi* Phi` and a global U(1);
3. one real, neutral, orbifold-even bulk stabilizer `varphi`, with the
   independent internal symmetry `varphi -> -varphi`; and
4. physical brane matter `Psi_m`, localized only on `Sigma_0` and minimally
   coupled to its induced metric.

The frozen internal symmetry is `U(1)_Phi x Z2_varphi`. It forbids
charge-breaking operators and odd powers of `varphi` in both the bulk and
localized actions. Orbifold parity and this internal `Z2_varphi` are distinct
statements.

The following X4-S2F3 control fields are not inherited: the real proxy field
`chi` and the three periodic massive five-dimensional Dirac spectators. No
bulk gauge field, hidden second matter sector, direct four-dimensional
portal, or observationally chosen compensator is present.

## 4. Candidate action

Write

    S_X4-S4-GW2 = S_bulk + S_GHY + S_0 + S_pi + S_ct.

At the frozen leading two-derivative classical order,

    S_bulk = integral_M5 sqrt(-G) [
        (M5^3/2) R5 - Lambda5
        - G^{AB} (nabla_A Phi)* nabla_B Phi
        - (1/2) G^{AB} partial_A varphi partial_B varphi
        - U(s,varphi)
    ],

with

    U(s,varphi) = mPhi2 s + (lambdaPhi5/2) s^2
                   + (mvarphi2/2) varphi^2
                   + (lambdavarphi5/4!) varphi^4
                   + (g5/2) s varphi^2.

The gravitational boundary term is

    S_GHY = M5^3 sum_i integral_Sigma_i sqrt(-gamma_i) K_i,
    i in {0,pi}.

The localized actions are

    S_i = integral_Sigma_i sqrt(-gamma_i) [
              (Mi2/2) R[gamma_i] - V_i(varphi,s)
          ] + delta_i0 S_m[Psi_m,gamma_0],

where

    V_i(varphi,s) = tau_i
                    + (kappa_i/4) (varphi^2-v_i^2)^2
                    + zeta_i s.

`S_ct` is the symmetry-complete counterterm functional at the declared loop
and derivative order. It starts at order `hbar` and is not used to tune the
tree-level background-existence test. Its required operator classes are
frozen in Section 10; its finite coefficients are not yet normalized.
Consequently this contract is not a complete renormalized semiclassical
effective action.

## 5. Mass-dimension ledger

Natural units are used and the five-dimensional action is dimensionless.

| Object | Mass dimension |
|---|---:|
| `Phi`, `varphi`, `v_i` | `3/2` |
| `s` | `3` |
| `M5` | `1` |
| `Lambda5` | `5` |
| `mPhi2`, `mvarphi2` | `2` |
| `lambdaPhi5`, `lambdavarphi5`, `g5` | `-1` |
| `tau_i` | `4` |
| `kappa_i` | `-2` |
| `zeta_i` | `1` |
| `Mi2` | `2` |
| brane matter Lagrangian density | `4` |

These dimensions are part of the contract and are not labels standing in for
a derivation.

## 6. Variational equations and boundary signs

Define the bulk scalar stress tensor by varying all scalar kinetic and
potential terms with respect to `G^{AB}`. The bulk equations are

    M5^3 G_AB = T_AB^(Phi,varphi) - Lambda5 G_AB,

    Box5 Phi
      - [mPhi2 + lambdaPhi5 s + (g5/2) varphi^2] Phi = 0,

    Box5 varphi - mvarphi2 varphi
      - (lambdavarphi5/6) varphi^3 - g5 s varphi = 0.

Variation on the fundamental interval, with each normal pointing outward,
gives the scalar boundary equations

    n_i^A nabla_A varphi
      = - partial V_i/partial varphi
      = - kappa_i varphi (varphi^2-v_i^2),

    n_i^A nabla_A Phi
      = - partial V_i/partial Phi*
      = - zeta_i Phi.

Define the localized surface stress tensor by

    S_mu_nu^(i) = -(2/sqrt(-gamma_i)) delta S_i/delta gamma_i^{mu nu}
                = -V_i gamma_mu_nu
                  + T_mu_nu^(m,i)
                  - Mi2 G_mu_nu[gamma_i],

where `T_mu_nu^(m,pi)=0`. With the GHY and extrinsic-curvature conventions
above, the interval boundary equation is

    M5^3 (K_mu_nu - K gamma_mu_nu) = S_mu_nu^(i).

No Israel sign or factor of two may be imported from an upstairs convention
without explicitly translating the normal and jump definitions.

For covariance bookkeeping, the induced metric is defined before gauge
fixing by embeddings `X_i^A(x)`:

    gamma_mu_nu^(i) = G_AB(X_i) partial_mu X_i^A partial_nu X_i^B.

Because the surfaces are orbifold fixed points, an odd normal displacement is
not an independent propagating brane coordinate after the Z2 condition is
imposed. Nevertheless, metric-scalar perturbations and compensating brane
bending must be varied and combined before a Gaussian-normal or fixed-brane
gauge is chosen. The physical radion is the gauge-invariant proper separation
of the two fixed surfaces and remains in the scalar constraint/Hessian system.

## 7. Fixed-charge ensemble

The conserved U(1) current and charge are

    j^A = i [Phi* nabla^A Phi - Phi nabla^A Phi*],

    Q = integral_Sigma_t d^4x sqrt(h) n_A j^A != 0.

No chemical potential is inserted into the covariant action. Fixed `Q` is
implemented only after variation, through the constrained Hamiltonian or
equivalent Routhian with the charge normalization and boundary terms kept.
Charge conservation requires vanishing net U(1) flux through both fixed
surfaces, which is compatible with the real Robin coefficient `zeta_i`.

## 8. Exact static-seed balance and its limitation

For a zero-charge, static, flat-four-slice seed written in an upstairs proper
coordinate `z`, the integrated Einstein equations require

    0 = sum_i V_i^ren(varphi_i,s_i)
        + integral_S1 dz [
              (partial_z varphi)^2 + 2 |partial_z Phi|^2
          ].

The full covering-space measure is used in the integral and each fixed-point
localized term is counted once. On the flat seed, the induced-curvature terms
vanish; localized matter vacuum energy is part of the renormalized `tau_i`.

Therefore a nonconstant scalar profile is incompatible with both net
localized vacuum contributions being strictly positive. This is a necessary
global condition, not a sufficient solution.

The displayed identity is not licensed at finite temporal charge. Finite
density breaks four-dimensional Lorentz symmetry, so the finite-`Q`
integrated Einstein identity must be rederived from the full lapse, shift,
spatial and interval equations. Reusing the static sum rule unchanged is a
rejection condition.

## 9. Background programme and kill criteria

The next calculation must proceed in this order:

1. solve a zero-charge warped static seed with full scalar backreaction,
   both scalar boundary equations, both gravitational junction equations and
   the integrated balance;
2. continue from a regular seed into a fixed nonzero-`Q` homogeneous sector,
   retaining lapse and the odd interval shift before constraint reduction;
3. solve all background constraints and verify regularity, finite action,
   charge normalization and agreement of local equations with the generalized
   integrated identity; and only then
4. build the pre-constraint kinetic, gradient and mass blocks.

A suitable finite-charge homogeneous ansatz may be parameterized as

    ds^2 = -N(t,y)^2 dt^2
           + a(t,y)^2 d x_T3^2
           + b(t,y)^2 [dy + N^y(t,y) dt]^2,

with amplitude, phase and `varphi` retained. Setting `N`, `N^y`, a scalar
constraint, or a surface displacement before variation is forbidden.

The candidate is rejected or returned to action selection if any of the
following occurs over the registered domain: no regular static seed, failed
junction or integrated balance, singular compact interval, nonconserved
charge, no finite-charge continuation, a negative-norm physical scalar, an
uncontrolled singular auxiliary block, or dependence on fitting an observed
radius/coupling to make the equations close.

## 10. Renormalization and counterterm contract

The eventual semiclassical calculation must use a covariant background-field
regulator compatible with the orbifold/Robin problem, with dimensional
regularization and heat-kernel bookkeeping where applicable. Renormalized
parameters are quoted in `MSbar` at a named scale `mu_R`.

At the chosen loop and derivative order, `S_ct` must include every divergent
operator allowed by the symmetries, including as required:

- bulk vacuum, Einstein, scalar wave-function, mass, self-coupling and portal
  counterterms;
- bulk curvature-squared and curvature-scalar operators;
- localized vacuum/tension and induced-curvature counterterms;
- localized scalar kinetic, Robin/pinning, curvature-scalar and mixed scalar
  counterterms; and
- boundary geometric operators, including the renormalization of GHY and the
  extrinsic-curvature structures required by the selected boundary problem.

The independent renormalized inputs include `Lambda5`, `M5`, both bulk scalar
masses and couplings, and each `tau_i`, `Mi2`, `kappa_i`, `v_i`, and `zeta_i`.
No `tau_i=0`, `Mi2=0`, finite determinant remainder, or subtraction constant
is obtained by omission. The actual one-loop determinant, state-dependent
stress tensor, finite counterterm conditions and anomaly/parity sectors remain
open. Any additional localized kinetic, curvature-scalar or extrinsic
coefficient required by the selected loop/derivative order is likewise an
independent renormalized input until a stated renormalization condition fixes
it.

## 11. Source-independent primary domain

The primary action-level domain is

    M5 > 0,
    Lambda5 < 0,
    mPhi2 >= 0,
    mvarphi2 >= 0,
    lambdaPhi5 > 0,
    lambdavarphi5 > 0,
    g5 >= 0,
    kappa_i > 0 and finite,
    v_i >= 0,
    zeta_i >= 0,
    Mi2 >= 0.

The renormalized `tau_i` are independent signed parameters whose admissible
combinations are selected by the local junction equations and global balance,
not by observational matching. No Hubble value, SPARC fit, BBN abundance,
MOND scale, desired compactification radius, `K_Q`, or `V` value selects an
action parameter, root or branch.

## 12. H1 and MAT firewall

If and only if a renormalized finite-charge background later survives may the
full scalar system be reduced. With dynamical variables `q` and auxiliary
variables `a`, the required objects remain

    H_phys = H_qq - H_qa H_aa^-1 H_aq,
    c_phys = c_q - H_qa H_aa^-1 c_a,

on a registered nonsingular auxiliary domain. H1 requires a positive-norm,
oriented physical mode and its signed source residue. An induced-metric
coefficient, a bare radion entry, or an absolute coupling magnitude is not H1.

The canonical radion cannot be identified directly with the Track-A
`Y^(3/2)` law because their derivative homogeneities differ. Only a derived
mixed radion/condensate physical mode remains eligible for later testing.

Binding status after this contract is:

    candidate_action_contract_frozen=true
    X4-S4-GW2_classical_action_frozen_for_one_background_test=true
    X4-S4_parent_accepted=false
    X4-S2F3_parent_changed=false
    finite_charge_background_solved=false
    semiclassical_action_complete=false
    counterterms_finitely_normalized=false
    physical_hessian_constructed=false
    signed_H1_residue_computed=false
    Rule9_cleared=false
    MAT-001=BLOCKED
    K_Q=NOT_DERIVED
    V=NOT_COMPUTED
    Stage4A=CLOSED
    physics_pass=false
    gate_effect=NONE

## 13. Next single gate

The next admissible gate is
`TOPX4_H1_X4-S4_ZERO_CHARGE_BACKGROUND_EXISTENCE`. It may test only the
frozen candidate above. It must stop before finite-charge continuation if the
static seed, either boundary system, or the exact static sum rule fails.
