# Homogeneous B1: positive kinetic block and coupled quadratic drift

29 October 2026. Conditional independent G2/G4 control. Review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## What is newly established

The [instantaneous B1 reduction](RES001_R4C1_B1_REDUCED_KINETIC_V1_REPORT_2026-10-29.md)
extends to a general point of the same, already registered homogeneous B1
background. The full original action gives

$$M(t)=a(t)^3M_0,$$

where M_0 is the positive ten-field matrix in the parent report. Thus its
kinetic inertia remains (10 positive, 0 negative, 0 zero) along this exact
homogeneous solution. The existing B1 background theorem supplies a>0 for
all finite forward times and explicit bounds on every finite interval; this
calculation does not repeat that theorem. In the declared amplitude convention
M(t) >= a(t)^3 I/6. This is an interval statement about the **kinetic block**,
not interval-wide stability or controlled perturbation evolution.

The background-dependent q/velocity and field/field coefficients are now
exported from the original quadratic density. Their actual time derivative
gives the coupled linear generator. At the initial event its symplectic
transport identity is checked exactly, including volume and momentum drift.
This advances an independent homogeneous G2/G4 control without replacing,
admitting, or altering the registered vortical G1 preparation.

## Derivation and domain

The [frozen contract](RES001_R4C1_B1_KINETIC_DRIFT_V1_CONTRACT_2026-10-29.md)
retains the original old B1 coefficients and future positive-dust branch.
For generic a,H,u,v,r and their homogeneous scalar velocities, the complete
second variation is recalculated from the original weak-action density.
Metric amplitudes are delta h=a^2 gamma and frame amplitudes delta V=v/a;
their 2H gamma and -H v time terms are retained. Shift amplitudes are physical
spatial amplitudes with coordinate shift S/a. The Fourier number k is
**comoving and held fixed in time**; physical momentum is k/a.

The multiplier is varied before the clock/lapse elimination described in
the parent report. The background has tau_dot=C and epsilon=rho_m/C^4;
delta tau=0 fixes N=exp(-beta delta psi). N_z is retained. Spatial curvature,
canonical scalars, portal, alignment, force and regulator are retained in the
second variation. The physical norm-cubed term has zero C2 coefficient at
aligned projected gradient, not zero nonlinear response.

For each nonzero planar mode, the actual algebraic block is

$$D(t,k)=\operatorname{diag}(5a^3/11,ak^2/2,ak^2/2,-ak^2/15),
\qquad\det D=-a^6k^6/132.$$

Therefore the same Z and three-shift elimination remains regular for a>0,
k != 0. Its complete reconstruction matrix is exported. The eliminated
variables are solved from this matrix, not fixed by a projection during
evolution. The remaining lapse equation reconstructs the dust multiplier,
including the original flux terms. The zero mode needs separate gauge and
constraint treatment. No continuation of the finite-tilt inverse through
V=0, no finite-amplitude neighbourhood theorem and no nodal interface law
is inferred here.

The generic matrices M,B,Q reproduce **all three** parent initial matrices
exactly. Their functional dependence is derived before initial substitution;
it is not obtained by extending a frozen numerical matrix. They are smooth
functions of the finite homogeneous fields for a>0 and fixed k != 0.
This supplies a defined nonzero-mode linear coefficient problem along the
known homogeneous solution. No explicit propagator/error bound or estimate
uniform over arbitrarily large k has yet been established.

## Actual background time derivative and generator

The old B1 flow is reused with M_cos^2=11/10, K_Q=3, beta=2/5 and the
original scalar potential. In particular

$$\dot a=aH,\quad
\dot H=-\frac{\dot u^2+\dot v^2+\dot r^2+3\dot\psi^2+\rho_m}{2(11/10)},
\quad\ddot\psi=-3H\dot\psi-\frac{2\rho_m}{15},$$

$$\dot\rho_m=(-3H+(2/5)\dot\psi)\rho_m.$$

The condensate and radion accelerations retain their original polynomial
potential and portal. Exact differentiation checks the same energy-loss
identity and preservation of the Friedmann constraint as the background
owner. H is evolved by its equation, not projected onto a root.

Write the reduced mode Lagrangian as

$$L_2=\tfrac12\dot q^\dagger M\dot q+
\operatorname{Re}(\dot q^\dagger Bq)+\tfrac12q^\dagger Qq.$$

Derivatives of the exported coefficient functions along this actual flow
give dot M=3HM and dot B. The field equation is

$$M\ddot q+(\dot M+B-B^\dagger)\dot q+(\dot B-Q)q=0.$$

Thus, for x=(q,q_dot), the actual coupled generator is

$$G=\begin{pmatrix}0&I\\
-M^{-1}(\dot B-Q)&-M^{-1}(\dot M+B-B^\dagger)
\end{pmatrix}.$$

The initial-event G is exported explicitly. For the parent convention
Omega=[[B-B^dagger,M],[-M,0]], the exact initial calculation verifies

$$\dot\Omega+G^\dagger\Omega+\Omega G=0.$$

It also checks the time derivative of the canonical pullback through
pi=M q_dot+Bq. Omitting dot M and dot B from G leaves 46 nonzero entries
in the transport residual. Thus freezing the momentum map would change this
problem. The general Lagrangian identity explains the required transport;
the explicit matrix check is performed at the registered initial event.
It is not a numerical proof of propagation or conserved perturbation energy.

## Verification, preservation and remaining work

The [versioned executable](../../../Analysis/MasterTests/test_01_r4c1_b1_kinetic_drift_v1.py)
passes 27/27 checks. The [fresh receipt and coefficient functions](../../../Analysis/MasterTests/outputs/r4c1_b1_kinetic_drift_v1_attempt_01/summary.json)
has SHA-256 `e66aaa83814afb726ace2bbaf1543591ba6502c37440be4430aca2ad7375c3cb`.
A complete recomputing read-only replay is byte-identical, exit 0. Eleven
direct input files and their eleven sidecars retain bytes and modification
times during calculation and replay. Original inputs and parent receipts
are not overwritten.

Exact checks cover the generic constraint block, kinetic identity, parent
recovery, background flow, initial generator and time-dependent canonical
map. Numerical central differences of the generated general B matrix along
the actual background tangent, at fixed k=1,7,40 and steps 1e-12 and 1e-18,
give maximum normalized derivative error 2.664e-36 at the smaller step and
the expected second-order convergence. This independently checks the
differentiation method on the generated coefficients; it is not an external
review of the action or a separate physical implementation.

The next useful homogeneous-control calculation is controlled propagation
on [0,0.05], with the reconstructed constraints, evolving coefficients and
physical kinetic normalization retained. A frozen-spectrum scan, an energy
fit, or positive kinetic inertia alone is insufficient. Nonlinear interaction
bounds and an actual frequency/momentum window remain necessary, as do the
separate GR and matching requirements. The old B1 normalization discrepancy
and the registered G1 nonlinear nodal/current obstruction are not removed.

G1-G6 INCOMPLETE; Stage 2 INCOMPLETE; Stage 3 NOT_ENTERED; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage 4A CLOSED.
Inherited review remains DEFERRED. No action/state adoption, new matching
input, manuscript/PDF/site change, vault mutation, commit or push.
