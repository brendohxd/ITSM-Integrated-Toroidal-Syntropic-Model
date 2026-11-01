# R-tau constraint-consistent local clock identity V2

1 November 2026. Conditional action-comparison result; review DEFERRED.
physics_pass=false; gate_effect=NONE; R-tau unadopted; G1-G6 incomplete.

## Result

The local clock residual has an exact constraint-consistent identity after
lapse/multiplier reconstruction. It vanishes on the exact initial root when
the complete initial field Euler equations are imposed. This supplies an
INITIAL classical consistency argument that independent interval boxing
could not resolve. It does not establish finite-time conservation or
physical admission. The original R4C1 action and its failures are unchanged.

The [frozen contract](RES001_R4C1_RTAU_CLOCK_IDENTITY_V1_CONTRACT_2026-11-01.md)
is implemented by [V2](../../../Analysis/MasterTests/test_01_r4c1_rtau_clock_identity_v2.py).
The [receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_clock_identity_v2_attempt_01/summary.json)
passes 18/18 checks. Receipt SHA256:
fa72a504e953901fb132483638a33cf97dc2c81ba9e87664bc208012046b8559.
Immutable replay COMPLETE: session 63771 terminal exit 0, byte-identical
SHA256 above. No duplicate replay is needed.

The [density V3 owner](RES001_R4C1_RTAU_CLOCK_DENSITY_V3_REPORT_2026-11-01.md)
remains correct: its independent whole-root box [-572.4583,555.7021] is too
wide to certify local closure. That receipt is not edited or retrospectively
promoted. The new result uses a structural identity and exact equations,
rather than asserting that an uncertain numerical box has become small.
The [prepared-Cauchy contract](RES001_R4C1_RTAU_PREPARED_CAUCHY_V1_CONTRACT_2026-10-31.md)
remains the owning physical-admission task.

## Derivation

Use coordinate Euler densities E, not Euler scalars. The convention is
E_q=L_q-partial_t L_qdot-partial_j L_qj. Write V for the independent
contravariant slice frame, U^0=gamma/N, U^i=V^i-gamma*S^i/N, and
gamma^2=1+h_ij V^i V^j. All metric off-diagonal variations are independent
symmetric-metric variations with their existing multiplicities.

For an active local time diffeomorphism xi=(f,0), the coefficients of
f_t and f_j in the ADM/frame variations, after separating f times the
actual time derivative, are

    delta N = f*Ndot + N*f_t-N*S^j*f_j,
    delta S^i = f*Sdot^i+S^i*f_t
                -(N^2*h^{ij}+S^i*S^j)*f_j,
    delta h_ij = f*hdot_ij+S_i*f_j+S_j*f_i,
    delta V^i = f*Vdot^i-(gamma*N*h^{ij}+S^i*V^j)*f_j,
    delta scalar = f*scalar_dot, delta tau=f.

The frame formula follows from transforming U as a vector and the metric
as a tensor; its normalization variation is delta gamma-f*gammadot
=-N*V^j*f_j. It is not a Lie derivative of V as a purely spatial vector
under this time deformation. Let P_q^j denote the displayed f_j
coefficient of q=(h6,V3,u,v,r,psi,Z).

Variation of the full covariant action and integration by parts in f gives

    0=E_tau+E_q*qdot+E_N*Ndot+E_Si*Sdot^i+E_epsilon*epsilon_dot
      -partial_t(N*E_N+S^i*E_Si)
      -partial_j(E_q*P_q^j-N*S^j*E_N
                 -(N^2*h^{ij}+S^i*S^j)*E_Si).

Impose the dust multiplier and full lapse equations as reconstruction
identities: N=exp(-beta psi), rho from the full lapse Euler derivative.
Their spacetime derivatives vanish as well. The q Euler densities then
equal those of the clock-substituted nonmatter density: the extra matter
psi term is reproduced by the lapse chain rule after reconstruction.
The independently derived clock current gives E_tau=-R_clock, where

    I_density=N*E_N,nonmatter=Ihat-partial_j(N*L_Nj),
    Ihat=Lbar-pi*(qdot-Lie_S q),
    R_clock=partial_t I_density
             -partial_j(I_density*S^j+N*sqrt(h)*F^j).

Thus the time Ward identity becomes

    R_clock=E_q*qdot-S^i*partial_t E_Si
            -partial_j(E_q*P_q^j)
            +partial_j((N^2*h^{ij}+S^i*S^j)*E_Si).

For an arbitrary spatial displacement xi, write
Lie_xi q=D0(q)*xi+D1^j(q)*partial_j xi. The spatial Ward identity,
using delta S=xi_dot+[xi,S], is

    partial_t E_Si=(D_q^* E_q)_i
                   +partial_j(S^j*E_Si)+E_Sj*partial_i S^j.

The quadratic shift contributions cancel exactly:

    partial_j(S^i*S^j*E_Si)
      -S^i*partial_j(S^j*E_Si)-S^i*E_Sj*partial_i S^j=0.

The remaining adjoint identity is

    E_q*qdot-S*(D_q^* E_q)-partial_j(E_q*P_q^j)
      =E_q*(qdot-Lie_S q)
         +partial_j(E_q*(D1^j*S-P_q^j)).

For metric and scalar variables D1^j*S-P_q^j=0. For the independent frame
it equals gamma*N*h^{ij}. Therefore

    R_clock=partial_j(N^2*h^{ij}*E_Si)
            +E_q*(qdot-Lie_S q)
            +partial_j(gamma*N*h^{ij}*E_Vi).

The last term must be retained off shell. The auxiliary Euler work E_Z
must also remain in E_q*(qdot-Lie_S q). Removing either is not justified
by the equations of a different probe or by the vanishing global integral.

Initial implication, conditional on this proof and its action controls:
the certified exact periodic root has E_S=0 as a spatial function; its
smoothness follows from its nonsingular momentum ODE. The complete
initial acceleration/gauge construction makes E_q=0 as a spatial function,
including the independent auxiliary equation and its actual first tangent.
The required spatial derivatives of these zero functions vanish. Hence
R_clock=0 at the initial instant on that exact constructed jet. A finite
Fourier centre instead has nonzero E_S; its small local residual should
be the derivative of N^2*h^{-1}*E_S. Neither implication is a future
constraint-persistence, symplectic-positivity or well-posedness theorem.

This proof is restricted to the stated classical action and lapse/multiplier
reconstruction. It does not remove independent clock dynamics off that
reconstruction, resolve quantum anomalies, or supply missing matching data.

## Independent controls and limitations

The exact symbolic controls use a general non-diagonal 3x3 metric. They
verify the ADM metric and unit-frame local time transformations, spatial
adjoint flux and quadratic-shift cancellation. The action-level proof uses
the covariant action's time and spatial Ward identities and its independently
derived explicit regulator current. A global Bianchi assertion alone is not
the calculation. Numerical controls below use the declared planar data;
no general transverse perturbation test is claimed.

At z=0.3,1.1,2.4, the preserved density V3 residual equals the freshly
calculated derivative of N^2*h^{-1}*E_S to within 6.71e-46. The previous
~6e-13 centre residual is therefore a finite-centre momentum defect; it is
not an independently failing clock equation. This does not replace the
previous certified exact-root existence proof with centre agreement.

At z=0.3, the direct density time derivative/current and complete identity
agree within 1.342e-45, below the frozen 1e-28 tolerance, both for the
constructed acceleration and two deliberately off-shell controls:

- Add 1/7 to the Vz acceleration, with its spatial derivative unchanged.
  Omitting the frame Euler flux then causes a nonzero discrepancy of
  approximately 1.62411849e-6.
- Add a spatially constant 1/1000 to the independent auxiliary Z value,
  retaining all other data and the previous acceleration. Omitting E_Z
  work then causes a nonzero discrepancy of approximately 5.56747325e-8.

All other nonzero off-shell Euler terms are retained. The tests compare
independently evaluated density/current derivatives with the Ward expression;
they do not force a desired residual by solving for a missing coefficient.
Neither off-shell control is adopted as physical data. Nonzero shift drift
is handled by covariance and the prior paired drift controls, not by a
physical prescription Sdot=0.

V1 stopped before producing numerical controls at an input-path KeyError.
Its [failure record](../../../Analysis/MasterTests/outputs/r4c1_rtau_clock_identity_v1_attempt_01/failure.json)
and sealed source are preserved. The [V2 implementation specification](RES001_R4C1_RTAU_CLOCK_IDENTITY_V2_SPEC_2026-11-01.md)
corrects that lookup, the Jet sqrt API and interval-left multiplication.
No equation, input, threshold or physical scope changes. The first V1 run
is not counted as a scientific result. V2 checks preservation of 250
inherited/current source and sidecar byte/mtime pairs.

## Disposition and next deciding task

Initial clock consistency on the exact constructed R-tau jet is established
conditionally on the stated reconstructed equations and classical action.
The initial data remain a candidate, not a physically admitted evolving
background. Do not relabel this as a [0,0.05] prepared-background theorem.
The old homogeneous physical-norm theorem is a different background.

Proceed to the actual prepared-data physical symplectic/characteristic
problem: spatial gauge and momentum constraints with both charge/mean
conditions, the auxiliary secondary equation, coefficient drift and mixed
quartic/background-gradient terms. Establish a physical quotient and its
principal evolution, or preserve a concrete failure. Additional initial
identity inventories alone do not meet this admission requirement.

Quantitative higher auxiliary bounds, sharp final gauge quadrature, full
transverse wavevectors, nonlinear evolution, interactions/window, GR/local
compatibility and genuine identifying matching remain incomplete. No new
matching information arose here. MAT-001/K_Q/V/UVIR-003/Stage 4A and TOP-X4
retain their live statuses. No concrete change to P1/P2, Thermodynamics or
original R4C1 manuscript claims is justified by this unadopted-candidate
identity. Author and independent-review decisions remain outstanding.

Review debt includes action comparison, root/gauge, temporal, velocity,
mixed, initial-jet, current and density owners. These same-author controls
are not independent external review. Review DEFERRED; physics_pass=false;
gate_effect=NONE. No action adoption, provider dispatch, vault mutation,
publication, commit, push or deployment. The larger scientific goal is
ACTIVE and incomplete.
