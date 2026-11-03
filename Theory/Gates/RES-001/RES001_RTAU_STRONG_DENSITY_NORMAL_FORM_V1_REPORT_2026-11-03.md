# Strong-density periodic normal form: exact row and initial coefficients

3 November 2026. Conditional initial planar component of the continuing
coupled-energy calculation. R-tau unadopted; original R4C1 unchanged.
Review DEFERRED; physics_pass=false; gate_effect=NONE; G1-G6 incomplete.
Goal ACTIVE; full normal-form/energy contract INCOMPLETE.

## Result and its boundary

An action-current-derived periodic change of the linear density observable
cancels the surviving fast delta Z_z term. It retains L2 density strength
and has a bounded triangular inverse with canonical scalar momentum L2.
The complete transformed row includes coefficient time drift, weighted
means, primitive commutators and all original source sectors. Initial
whole-root coefficient and background-gradient bounds are finite.

This addresses the fast Z_z term without weakening density to H^-1 or
assuming an extra derivative of the force perturbation. It is not a full
energy theorem. Force-momentum gradients and ordinary coupled derivatives
remain in the explicit remainder; they have not been declared bounded L2
forcing or removed. No physical time interval or positive coupled energy
is established by this component.

Owners: [full normal-form contract](RES001_RTAU_STRONG_DENSITY_NORMAL_FORM_V1_CONTRACT_2026-11-03.md),
[execution criteria](RES001_RTAU_STRONG_DENSITY_NORMAL_FORM_V1_EXECUTION_SPEC_2026-11-03.md),
[weak-density adequacy screen](RES001_RTAU_WEAK_DENSITY_ENERGY_SCREEN_V1_REPORT_2026-11-03.md),
[exact compensated row](RES001_RTAU_COMPENSATED_DENSITY_V1_REPORT_2026-11-03.md),
and [complete initial rate](RES001_RTAU_COMPENSATED_RATE_V1_REPORT_2026-11-03.md).

## Derive the momentum current before choosing the correction

Use M=N*mu, mu=sqrt(h), kappa=h^{zz}, s=psi_z,
p=(psi_t-S^z*s)/N, e=p*f_p-f and

    T=kappa*trK-2*Kupzz, d=b*M*kappa.

Here kappa is an inverse-metric component, not a Fourier wave number.
The full frame-dependent force f and its nonzero norm-cubed term are
retained. The clock-spatial regulator density is

    L_reg=b*M*Z^2/2-d*s*Z_z+beta*d*Z*s^2.

The exact scalar Euler equation can be written

    pi_psi,t=D_z J+R,
    J=S^z*pi_psi-M*f_s-L_other,psi_z+d*Z_z-2*beta*d*Z*s,
    R=L_other,psi+beta*M*e-beta*L_reg.

Its linear local source has the fast term r*delta Z_z with
r=beta*d*s. This split follows from the complete force, other-action and
regulator Euler rows, including the lapse terms. It is checked symbolically
against those rows, rather than guessed from a frozen high-frequency fit.

The density row's fast coefficient is a=b*N*T*s. Therefore

    c=a/d=T*s/(mu*kappa).

The denominator is strictly positive across the registered initial root
ball. No microscopic coefficient, state, cutoff or action is selected here.

## Complete linear transformed row on the fixed original circle

Write sigma=delta Sigma, xi=delta pi_psi and zeta=delta Z. Let

    P=Dinv*P0, P0 f=f-mean(f),
    u=Sigma_sharp=sigma-c*P(xi), C=N*(beta*p-trK), S=S^z.

Coefficients in this transformation are background coefficients. It is a
time-dependent LINEAR combination of physical perturbation observables,
not an asserted nonlinear replacement matter law. Momentum xi is retained
as an independent state component. Its mean is not fixed to zero and is
not substituted for the original total clock charge I.

Define exact remainders

    J0=delta J-S*xi-d*zeta_z,
    R0=delta R-r*zeta_z,
    sigma_t=S*sigma_z+C*sigma+a*zeta_z+F0.

F0 contains the complete remaining density linearization: delta S times
the background Sigma gradient, delta C times background Sigma, force/frame/
metric/matter/lapse work and the local regulator variations. The Ward
defect is retained by its owner; it vanishes only on the exact constrained
background and compatible tangent, not by assuming a numerical centre is
exact. J0 includes delta d times background Z_z and delta S times the
background scalar momentum. No nonzero background auxiliary field is set
to zero.

Using P*D=P0 and

    P(r*zeta_z)=P0(r*zeta)-P(r_z*zeta),
    mean(d*zeta_z)=-mean(d_z*zeta),

the COMPLETE transformed row is

    u_t-S*u_z=C*u+(C*c-c_t+S*c_z)*P(xi)+F0
       +c*[mean(S*xi)-S*mean(xi)]-c*mean(d_z*zeta)
       -c*P0(J0)-c*P0(r*zeta)+c*P(r_z*zeta)-c*P(R0).

The coefficient of the unbounded fast zeta_z term cancels exactly because
a=c*d. All spatially varying coefficients and mean corrections remain.
An independent nonconstant periodic control uses nonzero mean xi and a
nonzero weighted fast mean; it verifies the entire identity. Omitting c_t
or the weighted mean changes that equation.

The remaining F0 is not purely an ordinary-sector source. In particular
the force-gradient terms involving D_z(M*f_s) still contain derivatives
of the force momentum/normal velocity. These must be treated in the next
coupled calculation. The receipt's remaining_ordinary_derivatives field
records that ordinary derivatives are retained; it is not a claim that all
other fast coupling has disappeared.

## Coordinate/gauge primitive commutator and means

For a coordinate velocity w, the scalar momentum is a density and obeys
Lie_w xi=D_z(w*xi), while P(xi) is a primitive. Their exact commutator is

    P(D_z(w*xi))-w*D_z(P(xi))
       =w*mean(xi)-mean(w*xi).

It is generally nonzero. This is retained when converting to a moving
coordinate chart; treating P as a scalar pullback that commutes with
density transport would lose harmonic terms. The independent periodic
control rejects that shortcut. The report above gives the exact original-
coordinate row; it does not declare all moving symplectic/gauge/Green
terms solved. Original fixed-I/U1, range and modulus/harmonic conditions
remain unchanged.

## Initial coefficient bounds and retained density strength

The correction and its inverse are triangular:

    sigma=u+c*P(xi), xi unchanged.

On the original periodic circle ||P||L2->L2<=1. Thus both transformations
on the (density,scalar-momentum) L2 product have operator norm at most
1+||c||infinity. They do not change the density's derivative order. All
ordinary-field, other-momentum and force H2 controls are carried unchanged.
The earlier exact relation Sigma=rho+e+b*Z^2/2 is still the physical-density
reconstruction; the full force Legendre and auxiliary variations remain
part of its comparison with rho.

Whole-root outward bounds are

    ||c||infinity <0.000087645129,
    ||c_z||infinity <0.000147490900,
    ||c_t||infinity <0.011455828,
    ||map||, ||inverse map|| <1.000087646,
    |Sigma_background| <0.325969,
    |Sigma_background,z| <0.095210280,
    d >0.454079013.

These are INITIAL bounds in declared diagnostic units. No future time
uniformity is inferred.

The higher shift jet is REUSED from the immutable
[1 November clock-density V3 owner](RES001_R4C1_RTAU_CLOCK_DENSITY_V3_REPORT_2026-11-01.md).
That owner derived ||S_zzz||_2<0.155352 across the whole circle from the
differentiated momentum ODE and its exact-root C2 certificate. The numerical
bound is an all-position Euclidean component bound. It is inserted as an
enclosure of the second Taylor coefficient of S_z, with its factor 1/2,
before evaluating the new background Sigma gradient. A dummy zero jet or
the Fourier centre's third derivative is not used as evidence. The old
owner's wide local-clock residual is not imported as a continuum closure.

The coefficient time derivative uses the actual initial canonical Euler
momentum derivative and the established temporal inverse. If L depends
on velocity and shift through RV=v-S^z*q_z-B(q)*S_z, then

    L_vS=-M13*q_z for S^z, L_vS^x=L_vS^y=0,
    L_vSz=-M13*B(q).

For c=c(q,d,RV), c_S=-c_v*q_z and c_Sz=-c_v*B(q). Thus S_t and S_tz
cancel from its canonical time derivative. The particular acceleration

    a0=M13^-1*(p_t-L_vq*v-L_vd*v_z)

can be used in c_t=c_q*v+c_d*v_z+c_v*a0 without imposing a physical
S_t=0 prescription. Structural identities and independent actual action/
coefficient matrix checks at three nonzero prepared locations verify that
cancellation. No auxiliary acceleration or time-uniform background flow is
invented. All inherited phase/clock/gauge conditions remain necessary.

## Verification and next calculation

[Executable](../../../Analysis/MasterTests/test_rtau_strong_density_normal_form_v1.py):
34/34 controls passed with no failed/unknown controls. Fresh
[receipt](../../../Analysis/MasterTests/outputs/rtau_strong_density_normal_form_v1_20261103/receipt.json)
SHA256 0978896c5dd51fad8540d41ad952b7921330ecde6e674f51f42ef5ed02255568.
Read-only recomputation matched the receipt byte for byte, with all 34
controls again passing. All 219 original source
hashes and snapshotted source/sidecar bytes/timestamps are preserved.
No failed attempt occurred in this version; earlier failures remain intact.
Controls are same-author and do not clear independent review.

NEXT: resolve the remaining force-momentum derivative coupling and then
the full ordinary/zero-speed/quartic principal energy, including all
symplectic cross terms and moving constraint/gauge/Green maps. A bounded
normal form and fast-term cancellation are components, not full energy
or goal completion. The prepared physical norm, actual time tube, nonlinear
preservation, interactions/window, GR/local compatibility and identifying
matching remain incomplete. No C_chi or a0 follows. No concrete existing
paper correction or public claim change is established. No action adoption,
vault mutation/sync, dispatch, publication, commit/push or deployment.
