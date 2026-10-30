# G1 coupled nodal budget: a partial surface cancellation is not a solution

29 October 2026. **Conditional; Rule-9 DEFERRED; physics_pass=false;
gate_effect=NONE; G1-G6 INCOMPLETE.**

## Finding and scope

The original registered normal-frame equation couples to the auxiliary
gradient with coefficient -1/176 at the node. Retaining its metric-trace,
lapse-gradient and shift terms gives additional necessary conditions on a
putative concentrated auxiliary field. Solving just the auxiliary/frame
surface balances leaves a scalar double-layer residual and conflicts with
the leading zero-data normal-frame Cauchy equation.

This excludes the SPECIFIED partial linearized defect budget. It does not
exclude all finite-measure-current classes: this budget has no independent
concentrated metric/frame current and permits only order-zero remainder
currents in the scalar equation. Additional nonlinear frame/metric current
defects have not been derived or bounded. The executable's flag
finite_measure_current_closure_rejected has exactly this restricted meaning.
No full nonlinear layer or full R4C1 weak-solution no-go is established.

## 1. Coefficients from the original normalized-frame action

Vary the original 56-slot action before nodal restriction. At the registered
aligned node, let Vz denote the contravariant normal frame component, N the
lapse and Sz the normal shift. With b=5/44 and p=1/20, the derivative part
of its unreduced local row is

    E_Vz = -(1/24)*(Vz_tt+N_zt)
           +(1/60)*(Vz_zz+trace(h)_tz/2-Sz_zz)
           -(1/176)*Z_z + lower terms.

Thus m=1/24, d=1/60 and b*p=1/176. The coefficient is NOT obtained by
freezing a metric equation or removing a shift. The lapse-gradient and
metric/shift contributions above remain available in the budget.
This is an original local row, not a completed physical normalization,
propagator or characteristic-speed calculation on an admitted background.

The exact symbolic mixed Hessians are

| Original derivative | Value |
|---|---:|
| L_Vz_t,Vz_t | 1/24 |
| L_Vz_z,Vz_z | -1/60 |
| L_Vz_t,N_z | 1/24 |
| L_Vz_z,hii_t, each diagonal | -1/120 |
| L_Vz_z,Sz_z | 1/60 |
| L_Vz,Z_z | -1/176 |

The two mixed drift channels that could change the direct Z_z coefficient
vanish, as does the frame spatial-current derivative with respect to Z at
the node. The physical norm-cubed term has zero real Hessian at zero
projected gradient: its radial/tangential eigenvalues tend to zero. Using
that C2 fact for these nodal second derivatives does not adopt A=0 as a
physical parent. The physical cubic is retained in the independent original
action controls.

Both node slopes and complex steps1e-20/1e-26 agree below4.80e-117 normalized
error. The exact coefficients do not depend on the control H/density values;
those controls are not new admitted backgrounds. Independently, every stored
full initial Jacobi export agrees with the finite-w coefficient

    J_space[Vz,Z]=-b*p*sqrt(1+w^2).

## 2. Conditional highest-order surface budget

Work in the inherited inner normal X chart with sigma=+/-2/25, a=sigma^2,
and c=c3>0 from corrected INNER_CAUCHY_V2. Formally write an auxiliary
surface coefficient M(T)*delta(X) and a normal-frame value jump J(T).
These are unknowns in a diagnostic balance, not fields adopted into R4C1.

Assume the metric/lapse/shift limit is continuous with piecewise regular
derivatives. Their terms retained in the row then produce no highest
delta_prime coefficient. An independent concentrated frame current is not
included in this partial budget. The auxiliary delta and frame delta_prime
balances are

    M+2*a*c*T^3+p*sigma*J=0,
    d*sigma^2*J-b*p*sigma*M=0.

They have the unique formal solution

    M=-2*a*c*T^3/(1+b*p^2/d),
    J=b*p*M/(d*sigma), b*p^2/d=3/176.

Both equations and both orientations are checked exactly. The inherited
source box gives

    M/T^3 in [-0.000495784,-0.000481909],
    abs(J/T^3) in [0.002053590,0.002112713].

The J sign reverses between the two node orientations; M does not. The
metric/lapse/shift regularity hypothesis is essential. A singular limit in
those sectors or a concentrated frame current would require a new balance
derived from their equations; it cannot be inferred absent from finite action.

## 3. Two remaining failures

First, the normalized scalar residual is

    R_psi=K*Psi_TT-b*L(Z)-source+div(J_remainder).

The auxiliary surface produces -b*a*M*delta_second(X). A finite Radon
remainder current gives at most a delta_prime under one divergence, and a
dust Radon density contributes no second derivative. Thus this partial
scalar budget requires M=0, which the formal solution above contradicts.
Together the three equations have no solution for c,T>0.

If a derivative-valued scalar current D(T)*delta_prime(X) were available,
it would have to satisfy D=b*a*M. The required coefficient is

    D/T^3 in [-3.60569586692836e-7,-3.50479459706384e-7].

That current is NOT supplied or selected here. Nonlinear current products
would have to generate and conserve it from the original fields, or a
different full balance would have to avoid M altogether.

Second, the necessary leading normal-frame equation is Vz_TT=0 with zero
initial value and velocity. The formal jump J proportional to T^3 does not
satisfy it. For Vz=J(T)*H(X), it also leaves a leading bulk term

    -m*J''(T)*H(X).

Its coefficient per T has magnitude in [0.000513397,0.000528179], with sign
reversing between node orientations. Cancelling only a surface distribution
cannot cancel that bulk residual. An additional leading coupled response,
or failure of the assumed inner limit, would have to be established.

## 4. What is still possible, and what has not been done

The earlier finite-action example showed that unscaled action bounds do not
provide all rescaled compactness needed here. This result does not restore
that missing estimate. It says precisely why an auxiliary shell and a chosen
frame jump are insufficient by themselves.
The frozen dust Lagrangian depends on psi, metric, clock and multiplier,
not directly on the frame. A dust shell cannot be inserted as an arbitrary
direct normal-frame force; its metric/scalar effects must obey those equations.

A nonlinear metric/frame CURRENT defect could change the partial frame
balance, even if it is an ordinary measure current. Such a possibility is
not excluded by the scalar current-order argument. It still must satisfy
the leading time equation, other constraints, positivity/conservation of
matter and the full scalar equation. A metric/frame discontinuity or a
noncanonical product of distributions is not automatically authorized by
writing a formal jump equation.

No actual on-shell concentration, new weak-product rule, shell source,
initial state, action or boundary prescription has been constructed/adopted.
The full original evolving limit and all full-action weak conclusions remain
OPEN. The next target is the leading nonlinear current/concentration budget
with metric/frame and constraint equations included, not another free choice
of M,J or another initial trace calculation.

## 5. Evidence

Contract: [coupled defect V1](RES001_R4C1_COUPLED_DEFECT_V1_CONTRACT_2026-10-29.md).
Executable: Analysis/MasterTests/test_01_r4c1_coupled_defect_v1.py.
Receipt: Analysis/MasterTests/outputs/r4c1_coupled_defect_v1_attempt_01/summary.json.
SHA256: 2cc59e83ea9e206c49b162fe86f1a7255983120520b3dae70ada1f062942943b.
40/40 computational checks, no failed/unknown rows;258 pins; exact replay.
G1-G6, physical normalization/window, identifying matching and numerical
prediction remain incomplete. Earlier evidence and publication states stand.
