# PKM1-P0 finite-density parent Hamiltonian test specification

**Date frozen:** 2026-08-25
**Route:** PKM1 metric-hosted condensate foliation
**Status at entry:** `OPEN_RESEARCH_CANDIDATE`; no canonical-action change
**Permitted outcome:** bounded route evidence only; no gate promotion

## 1. Purpose

This calculation tests one explicit local parent for the PKM1 route. It asks
whether the same finite-density complex condensate can define the preferred
foliation and coexist with a metric-hosted low-acceleration operator without:

1. duplicating the condensate phase as an independent aether or force scalar;
2. tuning away the condensate's unavoidable lapse response;
3. changing the ADM constraint rank at zero spatial acceleration;
4. introducing a quadratic scalar ghost on an on-shell FRW background; or
5. claiming a microscopic derivation of a function that was selected as EFT
   data.

The test is deliberately upstream of local-gravity fits, lensing, SPARC,
cosmology, topology and publication.

## 2. Frozen parent action and domain

Use signature `(-,+,+,+)` and natural units. On the smooth timelike phase
chart

`Phi=(rho/sqrt(2)) exp(i Theta)`, `Z=-nabla_Theta^2>0`,

define

`U_mu=-nabla_mu Theta/sqrt(Z)`,

`a_mu=U^nu nabla_nu U_mu`, and `Y=a_mu a^mu>=0`.

The parent is

`S_P0=integral sqrt(-g) { (M_P^2/2)[R-2 J(Y)]`

`       - (nabla rho)^2/2 - rho^2(nabla Theta)^2/2 - V(rho) }`

`       + S_m[Psi_m,g]`,

with

`V=m^2 rho^2/2 + lambda4 rho^4/8`

`  + lambda6 rho^6/(24 Lambda^2)`.

`J(Y)` is fundamental controlled IR EFT data in this test. It is not derived
from `V`, circulation, topology, a reservoir or the observed acceleration
scale. The local matter action is minimally and universally coupled to the
single metric.

The following are expressly absent:

- an independent aether `U_mu`;
- an appended force scalar `psi` or direct `psi T` vertex;
- an independent `K(Q)` term;
- the engineered susceptibility `s` used in the earlier local auxiliary
  control;
- reservoir exchange and defect-core completion.

The phase chart ends where `Z<=0` or `rho=0`. No result may be extended across
those boundaries without a separate completion.

## 3. No-double-counting identity to test

In uniform-phase ADM gauge, `Theta=mu_Theta t`,

`Q=sqrt(Z)/mu_Theta=1/N`, `U^mu=n^mu`, and `Y=D_i ln(N) D^i ln(N)`.

The canonical phase term itself is

`rho^2 mu_Theta^2 Q^2/2`.

In the convention

`(M_P^2/2)[R-2J(Y)+2K(Q)]`,

this corresponds to

`K_cond(rho,Q)=rho^2 mu_Theta^2 Q^2/(2 M_P^2)`.

Thus an additional freely selected `K(Q)` would be a new operator, not a
rewriting of the canonical condensate. At fixed amplitude the prediction is

`K_QQ(1)=rho_0^2 mu_Theta^2/M_P^2>0`.

After controlled Thomas-Fermi relaxation of the amplitude, the test must
derive the complete positive susceptibility rather than assume this
fixed-amplitude value.

## 4. Two explicit J controls

### P0-A: inherited fast-transition control

Retest the interpolation used in the first PKM1 route screen,

`mu_A(y)=(y+y^2+y^3)/(1+y+y^2+y^3)`,

`J_A=a0^2[ln(1+y)-ln(1+y^2)/2-atan(y)]`,

where `y=sqrt(Y)/a0` and `1+J_Y=mu`.

It already passed static ellipticity. This test adds the independent khronon
kinetic-Hessian conditions

`J_Y<0`, `J_Y+2Y J_YY<0`.

Failure of either condition rejects this particular interpolation, not the
whole metric-hosted action class.

### P0-B: stability-first comparator

If P0-A fails, test the analytic control in `y>0`

`mu_B(y)=y/(1+y)`,

`J_B(Y)=-2 a0^2[y-ln(1+y)]`.

It must independently satisfy:

- `1+J_Y=mu_B`;
- `mu_B~y` and `J_B=-Y+(2/(3a0))Y^(3/2)+...` as `y->0+`;
- positive transverse and radial static ellipticity;
- positive transverse and radial khronon kinetic Hessians;
- `mu_B->1` and `J_B/Y->0` at high acceleration.

`J_B` is only a stability-first existence control. It is not licensed as an
observational interpolation or as the ITSM function.

## 5. ADM and Dirac calculation

The exact unitary-gauge action to Legendre transform is

`S_P0=integral dt d^3x N sqrt(h) {`

` (M_P^2/2)[R3+K_ij K^ij-K^2-2J(Y)]`

` +(dot rho-N^i D_i rho)^2/(2N^2)`

` -D_i rho D^i rho/2 +rho^2 mu_Theta^2/(2N^2)-V }+S_m`.

The test must derive the momenta, Hamiltonian and lapse equation. It must
classify `p_N,C_N` and count physical degrees of freedom in both:

- a generic smooth `Y>0` patch; and
- the homogeneous `Y=0` finite-charge branch.

The principal lapse operator is to be checked in directions transverse and
parallel to the background acceleration. A lower-order phase term must not be
used to conceal a loss of principal differential order.

## 6. Background and quadratic scalar tests

The retained local parent must be checked on:

1. stationary finite-density Minkowski space, allowing only a cosmological
   constant counterterm within P0;
2. an evolving spatially flat FRW solution of the complete P0 background
   equations; and
3. a declared stationary nonzero-gradient patch at the level justified by the
   local derivative expansion.

On FRW, use uniform-phase scalar gauge and retain the amplitude perturbation.
The lapse and scalar shift must be eliminated from the same quadratic ADM
action. Report the exact reduced kinetic determinant at finite `q` and at
`q=0`; a numerical scan is validation only.

The calculation may report a local/frozen equation generator and principal
front-speed limits. It may not convert time-dependent FRW eigenvalues into a
global conserved-energy claim.

## 7. Helmholtz/locality test

After radial elimination, derive

`K_eff(Q)=P(mu^2 Q^2)/M_P^2`

from the same condensate. Define `m_K^2=K_eff,QQ(1)/2`. For a local static
mode of wavenumber `k` and static ellipticity eigenvalue `lambda_stat`, the
declared AQUAL-locality condition is

`m_K^2/(lambda_stat k^2) << 1`.

The Thomas-Fermi condition must also be shown. An exact AQUAL equation is not
to be claimed if `m_K^2` is nonzero.

## 8. Kill and hold criteria

Reject P0 or the affected control if any of the following is derived:

- a negative reduced kinetic eigenvalue in its declared domain;
- a vanishing or sign-changing principal constraint/kinetic eigenvalue at a
  finite claimed background;
- a change in physical degree-of-freedom count at `Y=0`;
- no overlap between the local-AQUAL and amplitude-elimination windows;
- no on-shell background supporting the claimed calculation;
- a coefficient inferred from the desired galaxy law rather than the parent.

Hold, without rejection, if the quadratic parent is regular but any of these
remain underived:

- the nonlinear/cubic zero-gradient cutoff;
- a stationary galactic background and its complete physical Hamiltonian;
- radiative stability of `J`;
- topology, winding and defect-core compatibility;
- PPN, Shapiro, lensing, GW and compact-object limits.

## 9. Gate firewall

Regardless of a script-level pass:

- MAT-001 remains `BLOCKED`;
- UVIR-003 remains `IN_PROGRESS`;
- live-route `V` remains `NOT_COMPUTED`;
- live-route `K_Q` remains `NOT_DERIVED`;
- `a0` and its coefficient remain underived;
- no downstream physics or publication gate opens.
