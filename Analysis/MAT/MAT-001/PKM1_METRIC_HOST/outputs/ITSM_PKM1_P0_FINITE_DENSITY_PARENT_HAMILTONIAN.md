# PKM1-P0 finite-density parent Hamiltonian audit

**Calculation:** `PASS_BOUNDED_PARENT_AUDIT`
**Route disposition:** `HOLD_PKM1_P0_B_STABILITY_FIRST_CONTROL_ONLY_P0_A_REJECTED`
**Physics pass:** `false`
**MAT-001:** `BLOCKED` · **UVIR-003:** `IN_PROGRESS`

## Executive result

The parent action class survives one quadratic finite-density test, but the
specific interpolation inherited from the first PKM1 screen does not.

The inherited fast-transition control has

`J_Y+2Y J_YY=(2y^3+y^2-1)/(1+y+y^2+y^3)^2`.

It changes sign at

`y=0.657298106138`.

Static modified-Poisson ellipticity remains positive there, but the radial
khronon/lapse kinetic Hessian does not. P0-A is therefore rejected as a global
control. This corrects the narrower earlier route screen, which tested static
ellipticity but not the independent khronon kinetic Hessian.

The stability-first comparator

`mu_B=y/(1+y)`,

`J_B=-2 a0^2[y-ln(1+y)]`

has positive static and khronon transverse/radial eigenvalues for every finite
`y>0`, recovers the required deep `Y^(3/2)` term and has `mu_B->1` with
`J_B/Y->0`. It is retained only as fundamental EFT existence data. It was not
derived from the ITSM condensate, topology or observations.

## Same-action condensate result

The canonical phase kinetic term cannot be combined with an independently
free `K(Q)` without adding a new operator. At fixed amplitude,

`K_QQ=rho_0^2 mu^2/M_P^2`.

After consistently relaxing the stable radial mode,

`K_QQ=rho_0^2 mu^2/(M_P^2 c_s^2)`,

`m_K^2=K_QQ/2`,

where `c_s^2=M_rho^2/(M_rho^2+4mu^2)`. The response is strictly positive and
is enhanced, not cancelled, by amplitude relaxation. Exact AQUAL is therefore
not a same-action prediction of P0.

A local AQUAL approximation can still exist only in the simultaneous window

`m_K^2/(lambda_stat k^2)<<1`,

`k^2<<M_rho^2`.

Equivalently, the window requires

`m_K^2/(lambda_stat M_rho^2)<<1`.

No physical ITSM parameter point has yet established that overlap.

## Exact ADM and background findings

In uniform-phase gauge the parent contains spatial lapse derivatives but no
`dot(N)` or `dot(N^i)`. The generic count is four physical local degrees of
freedom: two tensor, one phase/khronon and one amplitude. The pair `(p_N,C_N)`
is second class. On the finite-charge `Y=0` branch, its homogeneous bracket
contains `-rho^2 mu^2`, so the fundamental-J parent does not suffer the
auxiliary control's zero-gradient constraint-rank loss.

Stationary finite-density Minkowski space is not an on-shell P0 background:
`rho+p=rho_0^2 mu^2>0`, which a cosmological constant cannot cancel. An
evolving flat-FRW branch is the retained background. The deterministic
existence integration closes the Friedmann, charge and continuity identities.

After eliminating lapse and scalar shift on that branch, the uniform-phase
scalar kinetic matrix is

`K=[[((rho_dot^2+rho^2 mu^2)+C_J q^2)/H^2,-rho_dot/H],`

`   [-rho_dot/H,1]]`,

with

`det(K)=(rho^2 mu^2+C_J q^2)/H^2>0`.

For P0-B at `Y=0`, `C_J=2M_P^2`. Positivity persists at strict `q=0`; the
numerical scan is a validation of this symbolic result, not its source.

## New action-class tradeoff

Let `delta=1-mu=-J_Y>0`. Radial khronon kinetic positivity requires

`(y delta)'>=0`.

Consequently a globally stable pure-`J` control cannot approach `mu=1` faster
than a `1/y` tail after any finite point where `delta>0`, and `J` cannot tend
to a finite constant. P0-B exhibits that slow tail. Whether any such tail
passes Solar-System/PPN bounds is a separate calculation; it is not assumed.
Published khronometric completions show that adding extrinsic-curvature
operators changes this issue, but P0 does not inherit their coefficients or
their phenomenology.

## Fail-closed decision

P0-A is rejected. P0-B remains a research control because its quadratic FRW
constraint and kinetic structure are regular, but PKM1 remains on global
hold. The microscopic origin and radiative stability of `J_B` and `a0`, the
locality window, nonlinear zero-gradient cutoff, stationary galactic
Hamiltonian, Jeans band, PPN/lensing/GW limits, topology and reservoir are all
open.

No canonical action or gate status changes.
