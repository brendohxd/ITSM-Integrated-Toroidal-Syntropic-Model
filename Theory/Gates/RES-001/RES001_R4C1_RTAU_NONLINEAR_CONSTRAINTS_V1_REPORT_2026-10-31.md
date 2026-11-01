# Nonlinear R-tau constraints: exact density and all-direction local shift pivot

31 October 2026. Conditional comparator result; review DEFERRED.
physics_pass=false; gate_effect=NONE. R-tau remains unadopted.

## Outcome

The dust multiplier/lapse sector has an exact nonsingular reconstruction on
its positive clock branch. The independently derived nonlinear shift
principal matrix is uniformly invertible for physical |V_frame|<=1/500,
including arbitrary tilt directions. This advances the owning
[coupled-interactions contract](RES001_R4C1_RTAU_COUPLED_INTERACTIONS_V1_CONTRACT_2026-10-31.md)
and follows the [frozen sub-contract](RES001_R4C1_RTAU_NONLINEAR_CONSTRAINTS_V1_CONTRACT_2026-10-31.md).

This is NOT the full nonlinear periodic constraint solution. Nonzero
principal determinant does not solve global compatibility, constant modes,
fixed charges or prove nonlinear domain persistence. No fully reduced
physical interaction functional or interacting window is yet supplied.

## Exact nonlinear multiplier/lapse reconstruction

Before imposing its multiplier equation, the clock-gauge dust density is

    L_m=epsilon*sqrt(h)/2*(C^2*tau_dot^2/N-N*C^4), C=exp(beta*psi)>0.

On the future positive branch with tau_dot>0 its multiplier equation gives
N=tau_dot/C. The matter lapse equation then has coefficient

    partial(E_N,m)/partial epsilon=-sqrt(h)*C^4.

With E_N,nonmatter=L_N,nonmatter-d_z(L_Nz,nonmatter) in the full new ADM
action, the full lapse constraint reconstructs

    epsilon=E_N,nonmatter/(sqrt(h)*C^4),
    rho=E_N,nonmatter/sqrt(h).

All spatial Euler fluxes are retained. These are exact identities, not a
perturbation series or use of the old bare-dust continuity equation. Actual
positive physical density additionally requires E_N,nonmatter>0; algebraic
reconstruction alone does NOT prove that inequality for trial data.
Degenerate metric, null clock, vanishing C or tau_dot and caustic boundaries
are excluded. Independent metric/frame equations remain part of the full
system; the reconstruction does not replace them.

The total induced clock current from the earlier candidate variation is
still required. On clock-normal slices its extra current has no normal
component, so the global clock charge density is sqrt(h)*rho/C, with the
modified spatial flux. This does not make the bare local dust current
separately conserved. The nonlinear condensate U(1) charge and both global
charge values remain constraints of the forthcoming periodic preparation.

## Fresh full shift principal block

At a point use an orthonormal spatial frame, N=1, and orient the derivative
covector along z. Let V_frame=(x,y,zeta) and t=x^2+y^2. The Hessian of the
full candidate density in (Sx_z,Sy_z,Sz_z) is

    K = (1/30)*[
      [15+5*x^2+x^2*t, x*y*(t+5), x*zeta*(t+5)],
      [x*y*(t+5), 15+5*y^2+y^2*t, y*zeta*(t+5)],
      [x*zeta*(t+5), y*zeta*(t+5), t*zeta^2-2*t+3*zeta^2-2]
    ].

This is recomputed from the action at arbitrary tilt, not inferred from
the earlier one-axis continuation. At alignment K0=diag(1/2,1/2,-1/15).

Only Einstein/frame kinetic terms contain spatial shift derivatives. In
the declared ADM density K_ij and the frame normal-velocity variables
depend linearly on them; those action terms are quadratic in these
derivatives. The scalar normal velocities depend on shift values, not
their derivatives. The norm-cubed force therefore does not enter this
principal Hessian. Nor do the clock-spatial regulator or potentials.
They DO affect lower-order terms and the nonlinear shift equation, and
are not removed from that remaining problem.

The exact calculation may consequently set the other local jets to simple
values to extract K, without declaring those values an admitted background.
Independent full-physical-density controls restore nonzero force, scalar,
metric-velocity, reservoir and gradient data and reproduce the same block.
No A=0 action or old specialized shift matrix is adopted.

For |V_frame|<=1/500 each component is bounded by 1/500. Absolute polynomial
coefficient bounds give

    ||K-K0||_2 <= 5875009/937500000000,
    sigma_min(K) >= 20831374997/312500000000 > 0.

The proof uses the sum of all entry bounds as an operator-norm majorant
and the singular-value perturbation inequality, not a finite tilt scan.
The bound applies for every derivative direction after local orthonormal
rotation. It does not require a global rotation of the compact torus.

Positive lapse and metric introduce positive volume/lapse factors and
coordinate congruence. Uniform Euclidean-coordinate bounds additionally
require bounds on those factors. The stated lower bound is the normalized
orthonormal N=1 one, not a constant valid through degenerate metrics.

The inertia stays (2 positive,1 negative,0 zero) by continuity along the
tilt ball. This is an invertible constraint symbol, NOT a positive coercive
operator or a propagating ghost verdict. In particular it supplies neither
a positive variational minimization principle nor automatic global
periodic invertibility. The k=0 shift still needs its own gauge and momentum
compatibility treatment, not inversion of a nonzero-mode symbol.

## Verification and next deciding task

[Executable](../../../Analysis/MasterTests/test_01_r4c1_rtau_nonlinear_constraints_v1.py),
[fresh receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_nonlinear_constraints_v1_attempt_01/summary.json):
15/15, no failed/unknown checks; exact recomputing read-only replay.
SHA256 202ead4f7fd5d26d3eae4ec1ccc05798f2b8ef646eb7468a1a09103e3c13a987.
Independent real second differences of the full physical density at 100
digits and steps 1e-12/1e-18 have normalized errors below 1.867e-77 and
1.015e-65, within the frozen 1e-30 bound. All pinned source/sidecar bytes
and modification times remain unchanged. Same-author controls are not an
independent external review panel.

Next construct the full periodic nonlinear shift/lapse/density preparation
with fixed global charges and actual momentum solvability. Retain generated
harmonics, weighted torus means, frame/matter couplings and the force cusp.
An elliptic principal symbol plus a finite numerical residual is insufficient:
the zero modes, inverse/domain bound and controlled remainder must be supplied.

The earlier linear norm estimate and regulator/force summands remain valid
within their scopes. Full nonlinear constraint solution, reduced canonical
interactions, physical window, realistic matter, GR/local tests and identifying
matching remain INCOMPLETE. Original G1-G6 incomplete; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED. No action adoption, manuscript/site change,
commit/push, publication, provider dispatch or vault mutation. Goal ACTIVE.
