# Prepared gauge-velocity inverse and paired coordinate rates

1 November 2026. Conditional comparison; review DEFERRED.
physics_pass=false; gate_effect=NONE; R-tau unadopted; G1-G6 incomplete.

## Result and scope

The coordinate gauge-velocity row has an explicit bounded periodic
functional inverse on the actual initial adapted metric. Its integration
constants retain physical metric-modulus rates; independent harmonic
coordinate velocities remain inputs. Canonical point controls verify the
matching field and momentum-density response, including the density
Jacobian and paired original/adapted rate change.

This is coordinate gauge fixing, not positivity of the physical indefinite
shift constraint or a physical zero-shift prescription. The full action
current-density row and transported physical norm remain incomplete under
the [evolution contract](RES001_R4C1_RTAU_PREPARED_EVOLUTION_V1_CONTRACT_2026-11-01.md).
The [specification](RES001_R4C1_RTAU_GAUGE_VELOCITY_V1_SPEC_2026-11-01.md)
was frozen first. Reuse the [canonical/auxiliary entry](RES001_R4C1_RTAU_EVOLUTION_ENTRY_AUXILIARY_V2_REPORT_2026-11-01.md)
and [compatible gauge](RES001_R4C1_RTAU_SPATIAL_GAUGE_V1_REPORT_2026-10-31.md).

## Actual periodic inverse

In adapted zeta coordinates h=diag(a^2,a^2,Abar^2), let b_i be the metric
velocity from the canonical inverse before its unknown shift correction.

    partial_zeta(b_x+hxx*xi_x')=0, similarly y,
    partial_zeta(b_z+2*Abar^2*xi_z')=0.

For the adapted-circle mean and mean-free antiderivative Dinv,

    c_x=mean(b_x/hxx)/mean(1/hxx),
    xi_x'=(c_x-b_x)/hxx, xi_x=Dinv(xi_x')+harmonic_x,

and similarly y. Longitudinally,

    c_z=mean(b_z), xi_z'=(c_z-b_z)/(2*Abar^2),
    xi_z=Dinv(xi_z')+harmonic_z.

Corrected metric rates are the retained constants c_i. Omitting them
destroys periodicity in general. Every other field and momentum receives
the same shift response; the metric is not independently projected.
The old-coordinate corrective shift is (xi_x,xi_y,xi_z/J), J=a/Abar.

With ell=1/13000, all certified initial roots have the same metric-profile
bounds. For the MEAN-FREE coordinate velocities,

    ||xi_x/y||_H1 <2.829298*||b_x/y||_L2,
    ||xi_z||_H1 <0.707216*||b_z||_L2.

Independent harmonics add their finite norm; they are not erased by these
estimates. The mean-free FP inverse L2-to-H2 bounds are <5.830375
transversely and <1.000154 longitudinally, in actual adapted-circle norms.

Proof: put hInvMax=exp(2ell), ratio=exp(4ell). The transverse slope bound
is (1+ratio)*hInvMax. Poincare bounds the primitive by its slope and gives
the H1 factor sqrt(2)*(1+ratio)*hInvMax. For a general FP source g,
xi'=(Dinv g+C)/h; retain C and use
||(1/h)'||_infinity<=2ell*exp(4ell). The resulting H2 bound is
(1+sqrt(2))*(1+ratio)*hInvMax+hInvMax+(1+ratio)*2ell*exp(4ell).
For z, the exact multiplier 1/(2*Abar^2*n^2) has H2 bound
1/Abar^2<=exp(2ell). These hold for every nonzero harmonic, without a
finite band/parity restriction or a physical stability inference.

## Full canonical and coordinate consistency

For all six metric, three frame and five scalar/auxiliary fields write
Lie_w q=w^z*q_z+T(w_z)*q. The canonical dual is

    Lie_w^dual p=(w^z*p)_z-T(w_z)^T*p,
    p*Lie_w(dq)+(Lie_w^dual p)*dq=partial_z(w^z*p*dq).

The actual prepared-point field-rate response to a shift equals Lie_xi q
through second spatial order, and the momentum Euler response equals
Lie_xi^dual p. The density Jacobian is required. Canonical pairing is
preserved after periodic integration, not by discarding its divergence.

Old-to-adapted field factors are 1/J on hxz/hyz, 1/J^2 on hzz, J on Vz,
and 1 elsewhere. Momentum-density factors are 1/(J*field_factor). With
the already-established background coordinate velocity w,

    qdot_new=Tq*(qdot_old-Lie_w q),
    pdot_new=Tp*(pdot_old-Lie_w^dual p).

For current density, Inew=I/J and
Inew_dot=(Idot-partial_z(w*I))/J. The new longitudinal shift is
J*(S_old^z-w). This kinematic helper does not close the action current.
The caller must supply whichever spatial jets of J,w are needed;
point-value covariance tests do not manufacture absent derivatives.

For actual perturbations first transform the canonical zero-correction
field and momentum rates consistently. Form b_i from the adapted metric
rates. Compute xi, convert it to the original corrective shift, reevaluate
the canonical rows and transform both rows back together. Physical moduli
and independent harmonic/mean data remain.

## Verification and remaining work

[Executable](../../../Analysis/MasterTests/test_01_r4c1_rtau_gauge_velocity_v1.py):18/18.
Immutable replay COMPLETE, session43577 terminal exit0; receipt SHA256
b04c13cdc5a26673e5f91291c43e50edfb5f4a03bf4a0f68c2a317c95d53e92b.
[Receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_gauge_velocity_v1_attempt_01/summary.json).
Actual-profile integral/primitive controls include both parities, nonzero
harmonic coordinate inputs and nonzero modulus rates. Errors are below
9e-102 against1e-40; the coordinate-series tail used by quadrature is
bounded by2.918e-91. Universal inverse claims use the functional proof,
not these samples or collocation eigenvalues.

At z=0.3 the actual Legendre/field defect is <7.105e-49 and the canonical
momentum-density defect <1.080e-48 against1e-28. Omitting periodic
constants, density Jacobian or paired coordinate-rate correction rejects.
All local canonical coordinate factors and the initial longitudinal gauge
rate are checked. Same-author controls are not external peer review.

NEXT: close the actual clock-current row with the full-metric current,
auxiliary reconstruction and corrected canonical rates; verify compatible
momentum/charge transport and the moving-map relation. Complete prepared
generator, physical norm, nonlinear persistence, transverse modes and
interactions/window remain open. No new identifying matching or manuscript
defect arose. Goal ACTIVE; review DEFERRED; physics_pass=false;
gate_effect=NONE. No action adoption, external dispatch, vault mutation,
publication, commit, push or deployment.
