# Prepared R-tau full canonical constraint and density graph

1 November 2026. Conditional action comparison; review DEFERRED.
physics_pass=false; gate_effect=NONE; R-tau unadopted; G1-G6 incomplete.

## Result and exact limitation

The actual field-dependent momentum tangent and local reconstructed density
are now expressed in canonical fields/momenta. This includes the derivative
of the independent frame momentum, the spatial lapse improvement, both
charge tangents, the extra mean momentum equation and the auxiliary
secondary relation. It is not merely the earlier fixed-field velocity map.

The metric-trace principal density coefficient is strictly nonzero on the
whole certified initial-root ball. Direct action controls at all three
registered centres validate the local canonical graph and its highest
spatial coefficients. This supplies the physical density map needed for
mixed-regularity work. It DOES NOT establish the full periodic inverse,
physical symplectic quotient, variable-coefficient norm or finite-time
admission. The zero-speed warning from the principal owner remains open.

Owner: [prepared-Cauchy contract](RES001_R4C1_RTAU_PREPARED_CAUCHY_V1_CONTRACT_2026-10-31.md).
Immediate inputs: [prepared principal](RES001_R4C1_RTAU_PREPARED_PRINCIPAL_V3_REPORT_2026-11-01.md),
[mixed operator](RES001_R4C1_RTAU_MIXED_OPERATOR_V4_REPORT_2026-11-01.md),
[initial clock identity](RES001_R4C1_RTAU_CLOCK_IDENTITY_V2_REPORT_2026-11-01.md)
and [initial acceleration](RES001_R4C1_RTAU_INITIAL_ACCELERATION_V1_REPORT_2026-11-01.md).
The [canonical graph contract](RES001_R4C1_RTAU_CANONICAL_DENSITY_GRAPH_V1_CONTRACT_2026-11-01.md)
was frozen before execution. No action, ensemble, physical restriction,
mode deletion, cutoff or matching input is introduced.

## Derivation and complete coefficient functions

Use the coordinate canonical densities p_i=Lbar_vi and the exact clock
branch, with q=(metric6,frame3,u,v,r,psi,Z). The auxiliary primary
momentum is zero; the other thirteen rates have the previously certified
nonsingular temporal Hessian. This is not yet a physical gauge quotient.

For a planar spatial displacement xi(z), write

    Lie_xi q=A(q,q_z)*xi+B(q)*xi_z.

Only A's longitudinal column is nonzero: A[:,z]=q_z. For metric h_ab,
B[h_ab,i]=h_ai*delta_bz+h_bi*delta_az; for frame V_j,
B[V_j,i]=-V_z*delta_ji. Scalar/Z rows of B vanish. Since shift enters
the rates through qdot-Lie_S q, the actual momentum equation is

    E_S=(B^T*p)_z-A^T*p=0.

Its complete canonical tangent is

    delta E_Si=(B[:,i].delta p+delta B[:,i].p)_z
                 -delta_iz*(delta p.q_z+p.delta q_z).

Both field variations are required; a fixed-field velocity tangent is
only the subcase delta q=0. The torus mean equation is

    average(delta E_Si)
       =-delta_iz*average(delta p.q_z+p.delta q_z)=0.

It cannot be inferred from the projected nonzero-mode equation. The two
global charge conditions remain, independently,

    delta Q=integral(u*delta p_v-v*delta p_u+p_v*delta u-p_u*delta v)=0,
    delta I=integral(delta I_density)=0.

Neither fixes density or charge pointwise. Homogeneous metric/matter
degrees and all harmonics remain present. Solving this graph together
with the actual gauge and charge conditions is still required.

The original weak density contains

    X^i=(Vdot^i-S^z*V^i_z+V^z*S^i_z+gamma*h^{iz}*Nz)/N.

Its frame-rate derivative is p_Vi, so the X contribution to L_Nz is
gamma*h^{iz}*p_Vi. The independent spatial-curvature and regulator terms
then give the full identity

    L_Nz=gamma*h^{iz}*p_Vi-MP2*curvature_flux/2
            -b*sqrt(h)*Z*h^{zz}*psi_z.

Define its canonical lapse improvement

    F(q,q_z,p)=N*gamma*h^{iz}*p_Vi-N*MP2*curvature_flux/2
                -b*N*sqrt(h)*Z*h^{zz}*psi_z.

This is the actual lapse-gradient derivative, not an added boundary choice.
The local reconstructed clock density is

    I_density=Ihat-partial_z F,
    Ihat=Lbar-p*(qdot-Lie_S q).

Its complete canonical first variation is

    delta I_density=-(qdot-Lie_S q).delta p
      +Lbar_q.delta q+Lbar_d.delta q_z
      +p.Lie_S(delta q)-partial_z(delta F).

The explicit shift-variation terms cancel algebraically. This is a change
of canonical representation, not a restriction Sdot=0 or delta S=0.
Let Lie_S(delta q)=S^z*delta q_z+T(S_z)*delta q. Derivatives of F below
are canonical derivatives, holding p independent. The density operator is

    delta I_density=C0*delta q+C1*delta q_z+C2*delta q_zz
                      +D0*delta p+D1*delta p_z,
    C0=Lbar_q+T^T*p-partial_z(F_q),
    C1=Lbar_d+S^z*p-F_q-partial_z(F_d),
    C2=-F_d,
    D0=-(qdot-Lie_S q)-partial_z(F_p),
    D1=-F_p.

Every coefficient is supplied by the pinned action, its actual prepared
profiles, canonical Legendre inverse and the displayed explicit F. No
norm weights, parent action or matching constants have been selected.

The regulator cancellation is especially useful. Before eliminating Z,

    I_reg=b*N*sqrt(h)*(Z^2/2+Z*Delta_h psi).

The raw Z_z and Nz terms cancel only with the complete local improvement.
On Z=-Delta_h psi,

    I_reg=-b*N*sqrt(h)*(Delta_h psi)^2/2.

The first density variation with respect to independent Z is proportional
to b*N*sqrt(h)*(Z+Delta_h psi); its Z_z coefficient vanishes identically.
Thus both auxiliary variation coefficients vanish on the secondary
equation, although Z and its secondary relation remain in the system.

At the actual conformal initial h=a^2 I, the highest derivative terms are

    delta I_density=
      -N*MP2/(2*a)*(delta hxx_zz+delta hyy_zz)
      -N*gamma/a^2*delta p_Vz,z
      +b*N*a*Z*delta psi_zz
      +terms with at most one spatial derivative of fields
       or no spatial derivative of momenta.

All off-diagonal field variations are retained in the lower-order terms;
this is not an evolving conformal restriction. Physical density is
rho=I_density/(N*sqrt(h)). Its first variation also includes the algebraic
background-measure term -rho*delta log(N*sqrt(h)). Its highest metric
coefficient is therefore -MP2/(2*a^4), and its frame-momentum coefficient
is -gamma/a^5. The trace coordinate f with delta hxx=delta hyy=f has
strictly nonzero second-derivative coefficient -N*MP2/a in I_density.

On every certified initial root, the fixed profiles obey

    exp(-beta*psi_max-lambda_max)<=N/a<=exp(beta*psi_max+lambda_max),
    psi_max=(1/1000)*(1/29+1/31), lambda_max=1/13000.

This establishes principal trace ellipticity and the actual derivative
counts. It does not establish an inverse of the full variable-coefficient
periodic operator. In particular it does not permit deleting the frame
momentum derivative or declaring its subtraction a bounded norm change.
The physical density map must retain these terms and its mean/charge
conditions in the eventual mixed-regularity estimate.

Still required: the full periodic trace/constraint inverse including
lower-order coefficients, spatial gauge and residual symmetries, both
charge/mean conditions, the transported physical symplectic form,
time/basis drift and the actual variable-coefficient evolution estimate.
This derivation does not transfer the old homogeneous t=0.05 theorem.

## Action controls and quantitative results

[Executable V2](../../../Analysis/MasterTests/test_01_r4c1_rtau_canonical_density_graph_v2.py):
90/90, with no failed/unknown checks.
[Receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_canonical_density_graph_v2_attempt_01/summary.json)
SHA256 0cb96db2f86ead50721f7e0bb87aacfa262c189b905f0fbd46677ed47acfcf1c.
Immutable replay COMPLETE: session 73828 terminal exit 0, byte-identical
receipt SHA256 above. No duplicate replay is needed.

At z=0.3,1.1,2.4, compare the independent raw N/Nz variation with the
explicit canonical flux. The maximum value/first-spatial-derivative defect
is below 4.144e-53. Seven canonical probes per point include every field
and nonauxiliary momentum, nonzero shift variations, all three frame
momentum derivatives, metric/force second derivatives and an independent
auxiliary perturbation. These are local off-shell tangent controls, not
new physical initial data or a projection to seven allowed perturbations.

For prescribed canonical momentum jets, the existing validated 13-rate
inverse and its differentiated equation reconstruct the rate jets. The
maximum residual/enclosure error is below 1.234e-47, against frozen
1e-35. No inversion of the zero auxiliary momentum block is attempted.
Direct density versus the canonical expression differs by less than
6.776e-47; the full momentum tangent differs by less than 9.514e-48,
against frozen 1e-28. Field variations of the spatial generators are
retained throughout.

For delta hxx=delta hyy=f, the coefficient magnitude of f_zz is bounded
on every certified initial root by

    0.99989638596212 < N/a < 1.00010362477486.

The three direct trace probes give density coefficients approximately
-0.99990269, -0.99996645 and -1.00006577. Omitting the lapse improvement
incorrectly makes every one zero. The field-dependent momentum-generator
omission gives errors about 0.1295 on the full probes, not a small label
or tolerance mismatch. Auxiliary first density variations cancel to below
1.028e-53 on the secondary equation. The frame-momentum and force
second-derivative coefficients pass their direct raw-action controls.

V1 failed syntax preflight before any scientific execution. Its sealed
[source](../../../Analysis/MasterTests/test_01_r4c1_rtau_canonical_density_graph_v1.py)
and [NOT_RUN failure](../../../Analysis/MasterTests/outputs/r4c1_rtau_canonical_density_graph_v1_attempt_01/failure.json)
are preserved. The [V2 specification](RES001_R4C1_RTAU_CANONICAL_DENSITY_GRAPH_V2_SPEC_2026-11-01.md)
expands one omitted-geometry control into explicit statements, correcting
an unclosed parenthesis. No mathematical acceptance requirement changes.

## Physical meaning and next deciding calculation

The density variable controls a COMBINATION of metric-trace second
derivatives and frame-momentum first derivatives, as well as the force
second derivative. For nonzero Fourier modes its inverse principal map
contains both an inverse-k-squared density term and an inverse-k frame
momentum term. It therefore does not independently give two extra Sobolev
derivatives to the metric trace from density control alone. Deleting the
frame derivative or declaring its subtraction a bounded change of norm
would conceal this physical regularity issue.

The next calculation must establish the full periodic canonical
configuration/momentum/density inverse with the actual lower-order
coefficients, gauge and residual-symmetry conditions, extra mean momentum
and both global charge conditions. It must then transport the symplectic
form and retain projector/time drift in the actual variable-coefficient
operator. Principal trace ellipticity is a necessary input, not the
completed inverse or evolution theorem. Reuse the mixed/principal/current
operators; another rest spectrum or independent interval bound that loses
these cancellations is not a substitute.

The original unchanged R4C1 remains distinct from this unadopted R-tau
candidate. General transverse perturbations, finite-time persistence,
interactions/window, GR/local compatibility and identifying matching remain
incomplete. No new matching relation or concrete defect in P1/P2,
Thermodynamics or the original R4C1 manuscript was found by this graph.
No manuscript/website change is warranted. Inherit prior action/root/gauge/
temporal/mixed/principal/clock review debt. Same-author algebra and action
controls are not independent external review. Goal ACTIVE and incomplete;
review DEFERRED; physics_pass=false; gate_effect=NONE. No action adoption,
provider dispatch, vault mutation, publication, commit, push or deployment.
