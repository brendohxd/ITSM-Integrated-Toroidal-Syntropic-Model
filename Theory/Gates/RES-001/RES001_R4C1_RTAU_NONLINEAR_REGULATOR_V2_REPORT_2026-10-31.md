# R-tau first nonlinear summands: exact regulator and controlled force cusp

31 October 2026. Conditional comparison work; review DEFERRED.
physics_pass=false; gate_effect=NONE; R-tau is not adopted as a parent.
This is the FIRST sub-bundle of the coupled-interactions contract, not its
completion. The full nonlinear lapse/shift/matter solve, reduced physical
interactions, domain persistence and interacting window remain INCOMPLETE.

## Established result

The nonlinear auxiliary constraint is regular on a positive-metric, positive-
lapse clock patch and stays purely spatial. There are explicit metric/clock
cubic and quartic regulator interactions. The norm-cubed force survives as
a nonanalytic homogeneous cubic with a controlled fourth-order remainder.
Neither is an on-shell solution or a complete canonical scattering amplitude.

Follow the [owning interaction contract](RES001_R4C1_RTAU_COUPLED_INTERACTIONS_V1_CONTRACT_2026-10-31.md)
and [sub-bundle contract](RES001_R4C1_RTAU_NONLINEAR_REGULATOR_V1_CONTRACT_2026-10-31.md).
Reuse the completed linear physical-norm estimate; no quadratic audit is
repeated. These are the same old-B1 control coefficients and the unadopted
R-tau action, not the separate vortical preparation or microscopic matching.

## Exact auxiliary reduction and torus mean

In the planar clock gauge write V=sqrt(h), K=V*h^zz, with independent N>0:

    L_reg=b*(N*V*Z^2/2-N*K*Z_z*psi_z-K*N_z*Z*psi_z).
    E_Z=b*N*V*(Z+Delta_h psi),
    Delta_h psi=(K*psi_z)_z/V.

The derivative of N in the spatial Euler flux cancels the explicit
acceleration term. Omitting that term fails the exact rejection check.
Up to the boundary flux -b*N*K*Z*psi_z,

    L_reg=b*N*V*(Z^2/2+Z*Delta_h psi),
    Z=-Delta_h psi,
    L_reg,eliminated=-b*N*V*(Delta_h psi)^2/2.

The pivot b*N*V is nonzero on the stated patch. This proves only the Z
part of constraint regularity, not the nonlinear shift/lapse operator.
Periodicity gives integral(V*Z)=0; it does not authorize setting every
unweighted nonlinear mean or the mean interaction energy to zero.

## Coupled metric/clock interaction coefficients and remainder

For h=exp(2*e*f)*I, psi=psi_bg+e*g, N=exp(-beta*e*g), define

    U=f+beta*g, L=g_zz, W=f_z*g_z.
    L_reg,eliminated=-b*e^2*exp(-e*U)*(L+e*W)^2/2.

The cubic and quartic coefficients (coefficients of e^3 and e^4, without
factorials) are exactly

    C3=-b*(2*L*W-U*L^2)/2,
    C4=-b*(W^2-2*U*L*W+U^2*L^2/2)/2.

For |e|<=e0=1/100, the remainder after the quadratic and cubic terms obeys

    |R_reg| <= (b/2)*|e|^4*exp(e0*|U|)
               *(U^2*L^2/2+2*|U*L*W|+W^2).

This follows from the exponential Taylor remainder and triangle inequality;
finite-amplitude agreement is an additional control, not the proof.
For the frozen packet f=1/7+cos(theta)/5,
g=-1/11+2*cos(theta+pi/3)/9, theta=k*z, the coordinate-averaged cubic
coefficient is 41*k^4/68607, NONZERO. Products also generate harmonics;
they are not projected back to the input mode. This coefficient alone is
not the fully constraint-reduced homogeneous physical energy.

## Force cusp retained, with explicit error bound

Use physical tilt V_frame=e*w and clock-normal force velocity
psi_normal=exp(beta*e*g)*(p+e*delta p). In an orthonormal spatial frame,
gamma=sqrt(1+e^2*|w|^2). The exact rest-space gradient divided by e is

    q_e=exp(-e*f)*grad(g)+w*psi_normal
          +e^2*w*(w.dot(grad(g)))*exp(-e*f)/(gamma+1).
    L_force,cusp=-A*|e|^3*exp(e*(3*f-beta*g))*|q_e|^3.

Thus its leading interaction is -A*|e|^3*|grad(g)+p*w|^3, not an analytic
cubic polynomial. A generic nonzero ray has unequal one-sided third
derivatives at zero; an analytic third Frechet derivative is not supplied.
The vanishing C2 contribution in the earlier quadratic calculation was
correct but never meant this force term was absent at finite amplitude.

For |f|<=F, |g|<=G, |grad(g)|<=G1, |w|<=W0, |delta p|<=P1 define

    B=F*exp(e0*F)*G1
       +W0*exp(beta*G*e0)*(P1+beta*G*|p|)
       +(e0/2)*W0^3*exp(e0*F)*G1,
    M=G1+|p|*W0, J=3*F+beta*G.

The boost formula gives |q_e-q_0|<=|e|*B. The norm-power inequality then
gives the explicit bound

    |R_force| <= A*|e|^4*exp(e0*J)
                   *(J*M^3+3*(M+e0*B)^2*B).

The controls use F=12/35, G=31/99, G1=2*k/9, W0=1, P1=1/23 and the
registered p=1/5. Both signs of e and k=1,7,40 are retained. The finite
constants are in the declared control units, not physical EFT cutoffs.
A separate zero-leading ray has a nonzero order-|e|^9 residue; zero cubic
order is not treated as disappearance of the nonlinear force.

The full-density comparison subtracts an A=0 decomposition to extract the
force summand; A=0 is not an adopted action. Metric, frame, condensate,
reservoir and dust entries are present in independent local off-shell jets.
They are not claimed to solve the nonlinear periodic constraints. The
separate regulator packet above is genuinely periodic. No whole-system
on-shell cubic Hamiltonian follows from this summand comparison.

## Verification, failure preservation and continuation

[V2 executable](../../../Analysis/MasterTests/test_01_r4c1_rtau_nonlinear_regulator_v2.py),
[receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_nonlinear_regulator_v2_attempt_01/summary.json):
123/123, no failed/unknown checks; exact recomputing read-only replay.
SHA256 ebf0bb4708ca1167bbbf4f3049ee8d418bfb76b0e992686ed6b85bca923f3d46.
The 57 input pins and sidecars retain bytes and modification times.
Physical-density decomposition errors at 100 digits are below 5.370e-101,
within the frozen 1e-60 bound. All sampled remainder inequalities passed;
the largest force-remainder/bound ratio was below 0.02168.

V1's general-purpose integration failed with MemoryError before a receipt.
Its source and private traceback are preserved. The [V2 addendum](RES001_R4C1_RTAU_NONLINEAR_REGULATOR_V2_ADDENDUM_2026-10-31.md)
uses the exact endpoint value of an already-known periodic flux instead;
no action, coefficient or tolerance was changed. These same-author checks
do not supply independent external scientific review.

Next continue the owning contract's nonlinear lapse/shift/density equations
and full reduced interaction functional. Carry these exact summands,
nonanalytic remainder bounds, mean fluxes and generated harmonics into that
calculation. Do not certify full constraint/principal persistence, a physical
window, GR/local compatibility, realistic matter or identifying matching.
Original G1-G6 remain INCOMPLETE; no canonical parent adoption, publication,
vault mutation, commit/push or provider dispatch. Native goal ACTIVE.
