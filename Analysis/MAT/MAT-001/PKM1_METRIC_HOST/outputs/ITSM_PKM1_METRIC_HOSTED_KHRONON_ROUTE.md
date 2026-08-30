# PKM1 — metric-hosted condensate-khronon broad route

**Calculation:** `PASS_BOUNDED_SYMBOLIC_ROUTE_SCREEN`  
**Disposition:** `SELECT_PKM1_FOR_A2_A6_DERIVATION_NOT_GATE_PROMOTION`  
**Physics pass:** `false` · **MAT-001:** `BLOCKED` · **UVIR-003:** `IN_PROGRESS`

## Candidate action

Use the smooth condensate phase to define the preferred foliation,

`U_mu=-d_mu Theta/sqrt(-d Theta squared)`,

and put the low-acceleration operator in the gravitational sector:

`S=(M_P^2/2) integral sqrt(-g)[R-2 J(Y)+2 K(Q)] + S_m[Psi_m,g]`,

where `Y=(U.nabla U)^2` and ordinary matter is minimally coupled to the single
metric `g`. This is a new controlled route, not the live action.

## Conditional exact weak-field result

For

`mu(y)=(y+y^2+y^3)/(1+y+y^2+y^3)`, `y=|grad Phi_N|/a0`,

the interpolating function was selected first for this route screen, and an
explicit primitive was then constructed as

`J=a0^2[ln(1+y)-ln(1+y^2)/2-atan(y)]`.

It satisfies `1+J_Y=mu`, `mu~y` at low acceleration and `mu->1` at high
acceleration. For `K=K_0+(K_QQ(1)/2)(Q-1)^2+...`, the stationary weak-field
equation is

`div[mu(|grad Phi_N|/a0) grad Phi_N]+m_K^2 Phi_N=4 pi G rho_b`,

with `m_K^2=K_QQ(1)/2`. Exact AQUAL is the `m_K=0` subcase, or a declared
local regime in which the Helmholtz term is negligible.

This is an existence and normalization check, not a derivation of `J` from
ITSM microphysics. The source normalization comes from the minimally coupled
metric. There is no independent `C_m`, and no `C_m/sqrt(K_Q)` residue is
needed. In the exact-AQUAL subcase, spherical deep acceleration gives
`g=sqrt(a0*g_N)` with coefficient one. The scale `a0` is still an input and
has **not** been derived.

## Why this is broader than M2/U2

PKM1 changes the force host instead of adding another scalar portal. It unifies
the condensate rest frame and khronon foliation and makes the metric lapse the
force potential. The helical two-scalar control still leaves
`g_sigma*kappa/sqrt(Z_psi+Z_sigma*kappa^2)` free, so it does not repair M2.

## Fail-closed burden

PKM1 survives only the A0-A1/static-hosting screen. It still requires a
microscopic derivation of `J`, `K` and `a0`; the full amplitude-phase-metric
constraint count; zero-gradient, Jeans and strong-coupling control; and a
global treatment of winding and defect cores. Published khronon results are
precedent, not evidence that the ITSM embedding passes those tests.

**Recommendation:** advance PKM1 alone to a bounded A2-A6 derivation while
retaining the existing separate-phonon route as a frozen control. Do not change
any gate status.
