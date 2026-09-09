# TOP-X4 `X4-S2F3` semiclassical parent freeze

**Date:** 2026-09-06  
**Status:** `FROZEN_FOR_ONE_MAX_RETRY`  
**Parent:** `X4-I1C + three periodic massive 5D Dirac spectators`  
**Gate effect:** none

## 1. Frozen action

The retry action is

\[
 S_{S2F3}=S_{I1C}+\sum_{I=1}^{3}\int d^5x\sqrt{-G}
 \left[\frac{i}{2}\bar\Psi_I\Gamma^A
 \overleftrightarrow D_A\Psi_I-m_{F,I}\bar\Psi_I\Psi_I\right].
\]

`S_I1C` is exactly the action in
`TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md`. No scalar coupling,
matter portal, brane term or gauge charge is added to the spectator fermions.
Their only compulsory interaction is through the five-dimensional metric.

The fermion stress tensor is defined off shell by metric/vielbein variation;
in symmetric form,

\[
 T^{(F)}_{AB}=\frac{i}{4}\sum_I\left(
 \bar\Psi_I\Gamma_A\overleftrightarrow D_B\Psi_I+
 \bar\Psi_I\Gamma_B\overleftrightarrow D_A\Psi_I\right).
\]

Conventions remain signature `(-,+,+,+,+)` and
`y equivalent y+2*pi` with physical radius `R` and circumference `ell=2*pi R`.

## 2. Dimensions and boundary data

In five-dimensional natural units,

\[
 [\Psi_I]=2,\qquad [m_{F,I}]=1,
 \qquad [\bar\Psi i\Gamma^A D_A\Psi]=5.
\]

All three fermions obey the same periodic spin structure,

\[
 \Psi_I(x,y+2\pi)=+\Psi_I(x,y).
\]

All pre-existing bosons remain periodic. The fermions are dark bulk
spectators; no claim is made that their four-dimensional zero modes reproduce
chiral Standard-Model matter. Their massive four-dimensional zero modes are
real added degrees of freedom and must be retained in later cosmological and
local-gravity inventories if the parent survives.

## 3. Quantum definition

The Max retry must use the background-field one-loop effective action with:

1. the positive-frequency Minkowski vacuum on the static
   `Minkowski4 x S1` control;
2. covariant proper-time/heat-kernel evaluation and Poisson resummation, with
   zeta-function evaluation allowed only as an independently equivalent
   representation;
3. subtraction of the decompactified contribution;
4. the complete periodic KK tower, including the correct fermion sign and four
   physical components per 5D Dirac field;
5. no hard-coded Casimir coefficient or imported radius.

For the time-dependent finite-charge continuation, Max must specify a
Hadamard/adiabatic state and demonstrate state-order convergence. The static
vacuum formula may not simply be inserted into an evolving background.

## 4. Counterterms and normalization

The unorbifolded smooth-circle control has no fixed-point counterterms. The
local covariant counterterm basis must include the renormalized bulk vacuum
term and, on curved backgrounds, the gravitational and matter operators
required at the working loop/EFT order. On the flat zero-density potential,
only the renormalized bulk vacuum term affects the radius dependence.

The zero-vacuum-energy benchmark may determine that one renormalized
coefficient through

\[
 V_{\rm eff}(R_*)=0,
 \qquad \partial_RV_{\rm eff}(R_*)=0.
\]

This is a declared fine-tuned normalization condition, not a solution of the
cosmological-constant problem and not a prediction of the low-energy theory.
Max must also report the untuned nonzero-vacuum-energy domain.

## 5. Frozen parameter domains

- `N_F=3` exactly; changing multiplicity is a new candidate.
- `m_{F,I}=m_F>0` in the primary benchmark.
- Primary equal-mass control:
  `m_Phi=m_chi=m_F=m_*` at zero density.
- Robustness domain after the benchmark:
  `m_Phi/m_F` and `m_chi/m_F` each in `[0.5,2]`.
- Cutoff condition:
  `0 < m_F/Lambda_5 <= 0.04` and, at every accepted minimum,
  `Delta_KK/Lambda_5 <= 0.1`.
- The condensate charge, portal and quartics remain those of the frozen
  `X4-I1C` control when the finite-density continuation is run.

The ratios define a bounded stress test; they are not observational priors.
The absolute `m_F`, `Lambda_5` and `R` remain unpredicted.

## 6. Max calculation order

1. Independently reproduce the periodic scalar and Dirac determinants and
   their decompactification subtraction.
2. Recover the High equal-mass witness without using its saved numerical root
   as solver input.
3. Vary the complete renormalized effective action with respect to the metric,
   radion, condensate amplitude and phase before imposing a background.
4. Solve the finite-charge semiclassical background and enforce every
   Hamiltonian/continuity constraint.
5. Calculate the full canonical Hessian, radion mass and mixing with amplitude,
   phase and metric scalar modes.
6. Scan the frozen mass-ratio and cutoff domains and test regulator,
   subtraction-scale and adiabatic-state stability.
7. Test zero-charge, zero-portal, decompactification and small-circle limits.
8. Audit the parity-odd phase of the 5D fermion determinant and every required
   quantized local counterterm; the Casimir energy alone is not the complete
   fermion effective action.

## 7. Max kill criteria

Freeze or reject `X4-S2F3` if any of the following occurs:

- the independent determinant has a different sign or degree count;
- the finite-density Goldstone/amplitude spectrum changes the long-distance
  count so that the stationary minimum is lost;
- the minimum disappears after simultaneous field/gravity variation;
- the finite-charge background is off shell or lacks conserved total stress;
- the physical scalar/radion Hessian has a ghost or negative eigenvalue not
  identified as the intended condensate instability;
- no accepted point satisfies `Delta_KK/Lambda_5 <= 0.1`;
- the result is materially regulator, subtraction-scale or state dependent
  after the declared counterterms and normalization conditions;
- stabilization exists only at the equal-mass point and disappears throughout
  the registered robustness domain;
- the periodic-spin-structure or nonperturbative circle stability conditions
  are inconsistent;
- a parity/global anomaly or parity-odd determinant term cannot be cancelled
  consistently within the frozen field content;
- a desired phenomenological scale is used to select a parameter.

Survival permits only a new `X4-D2_RETRY` decision. It does not open A4,
derive exchange, derive `K_Q` or `V`, or revise the canonical model.
