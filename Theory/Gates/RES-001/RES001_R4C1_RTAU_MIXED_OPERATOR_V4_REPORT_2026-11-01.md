# Prepared R-tau mixed quadratic and canonical operator

Completed 1 November 2026, Australia/Perth. Contracts and executable
versions retain their frozen 31 October filenames and hashes.
Conditional comparison result; review DEFERRED; physics_pass=false;
gate_effect=NONE. R-tau remains unadopted; original R4C1 is unchanged.

## Result and boundary

The actual prepared-data clock-constrained density now has a complete
48-slot local second variation, including its first spatial derivative,
outward whole-circle coefficient bounds carrying the certified initial-root
uncertainty, and independent original-density controls. This supplies the
unreduced canonical Legendre two-form and the initial Euler equations in
affine acceleration/shift-drift form. Those unknown accelerations and shift
rates have NOT been solved.

The result is more than a velocity-only kinetic test. It retains mixed
metric/frame/matter/force/auxiliary variations, the lapse-map curvature and
variable-coefficient formal-adjoint terms. It is still NOT the fully
constrained physical symplectic quotient, characteristic/evolution theorem,
interaction calculation or a physical validity window. Dependence is planar;
general transverse spatial wavevectors on this inhomogeneous slice remain open.

Owner: [prepared-Cauchy contract](RES001_R4C1_RTAU_PREPARED_CAUCHY_V1_CONTRACT_2026-10-31.md).
Inputs: [velocity-tangent report](RES001_R4C1_RTAU_VELOCITY_TANGENT_V2_REPORT_2026-10-31.md),
[temporal owner](RES001_R4C1_RTAU_PREPARED_TEMPORAL_V2_REPORT_2026-10-31.md),
[certified initial root](RES001_R4C1_RTAU_PERIODIC_INVERSE_V1_REPORT_2026-10-31.md).
The [mixed contract](RES001_R4C1_RTAU_MIXED_OPERATOR_V1_CONTRACT_2026-10-31.md)
was frozen before execution. No new matched parameter or parent action is supplied.

## Clock branch and the density being varied

Use y=(q14,v14,d14,S3,Sz3), where q contains metric6, independent frame3,
u/v/r/psi and auxiliary Z; v and d are their time and z derivatives. The
dust clock is tau=t on its positive branch,

    N=exp(-beta*psi), Nz=-beta*N*psi_z.

The dust multiplier term vanishes identically after this substitution.
This does not remove its original equations. The lapse equation still
reconstructs epsilon=E_N,nonmatter/(sqrt(h)*C^4), with its full spatial
Euler flux, and rho=E_N,nonmatter/sqrt(h). Its coefficient -sqrt(h)*C^4
is nonsingular on the declared branch. If the multiplier and lapse equations
are imposed, variation of the substituted action agrees with the remaining
original field equations: the extra variations multiply those eliminated
Euler equations. The reconstructed density, clock-current consistency and
future positivity/persistence remain requirements for an evolving solution.
They are not established by an initial Hessian.

The direct density combines the old temporal-regulator cancellation exactly
before interval evaluation. It retains the clock-regulator expression

    b*N*sqrt(h)*Z^2/2
      -b*N*sqrt(h)*hzz*Z_z*psi_z
      -b*sqrt(h)*Z*hzz*Nz*psi_z.

No Z time derivative remains. All metric variations remain independent;
the initial conformal metric is not imposed as a future restriction.

## Full second-order lapse pullback

Let Phi(y) map the 48 slots into the original 56 ADM slots. With J=Phi_y,
the mixed Hessian is

    Hbar=J^T*H_original*J+sum_a (L_original)_a*(Phi_a)_yy.

The nonzero extra map derivatives include

    N_psi=-beta*N, N_psipsi=beta^2*N,
    Nz_psi=-beta*Nz, Nz_dpsi=-beta*N,
    Nz_psipsi=beta^2*Nz, Nz_psi,dpsi=beta^2*N.

A Jacobian-only pullback misses real coefficients. At the three registered
control points, the omitted curvature correction has maximum size between
0.03114 and 0.03240 in these coordinates. These are diagnostic coefficients,
not observational predictions. Independent controls use the original
uncombined candidate density with N and Nz independently varied. The fixed
tau_z slot is excluded from that backend's differentiation, since every
48-slot Jacobian direction has tau_z=0; no covariant tau_z derivative is claimed.

## Full force norm and outward mixed coefficients

The force term retains its norm-cubed contribution. For arbitrary positive
spatial metric, spatial covector g and independent frame V, write

    gamma=sqrt(1+V^T*h*V),
    rest=h^-1*g+V*(s+(V.g)/(gamma+1)),
    Y=rest^T*h*rest.

This equals the original projected norm for general metric variations,
not just conformal ones. Explicit diagonal squares and metric cross terms
retain all off-diagonal variations without losing square nonnegativity in
interval arithmetic. The original-density controls include all six metric
directions and their mixed derivatives.

On the ENTIRE prepared circle and every certified root,

    Y > 7.300e-12, hence sqrt(Y)>2.70e-6.

This justifies the third derivatives needed for spatially differentiating
the Hessian on this particular prepared domain. It does not assert that
the norm-cubed action is C3 at a vanishing rest gradient elsewhere.

The receipt exports 692 nonzero upper-triangle coefficient intervals and
their first spatial derivatives; all remaining entries are exactly zero
or fixed by symmetry. Together with the 14 forcing intervals and rest-norm
bound, 1,399 binary interval pairs are finite and ordered. One whole-circle
enclosure bounds coefficients; it does not truncate perturbation harmonics.
Both real parities, metric polarizations and homogeneous components remain.

## Canonical two-form with spatial drift

Define A=L_vq, M=L_vv, B=L_vd, C=L_vS, D=L_vSz. Then

    delta pi=A*delta q+M*delta v+B*partial_z(delta q)
                +C*delta S+D*partial_z(delta S).

Choose Omega(delta1,delta2)=integral(delta1 q.delta2 pi-
delta1 pi.delta2 q). Its unreduced Legendre pullback in (q,v,S) has blocks

    Omega_qq=A-A^T+(B^T)_z+(B+B^T)*partial_z,
    Omega_qv=M,
    Omega_qS=C+D*partial_z,

with opposite blocks the negative formal adjoints. The other diagonal
blocks vanish. Periodic integration by parts gives Omega_qq^*=-Omega_qq;
the derivative of B^T is essential. The explicit boundary divergence is
zero only after the periodic integral, not pointwise. Actual B_z+B_z^T
is nonzero at all three control points, with maximum magnitudes roughly
0.01708, 0.007924 and 0.001199. Replacing it by a constant-coefficient
formula therefore discards real terms.

Auxiliary Z has zero momentum and zero temporal/momentum cross coefficients
with its field and gradient. The resulting presymplectic degeneracy is
retained with the secondary relation Z=-Delta psi; it is not a new physical
mode or a completed Dirac reduction. Moving physical/gauge bases and their
time drift still require the actual reduced operator and background flow.

## Actual initial Euler system, not an assumed acceleration

The initial field equations take the form

    M*qddot+C*Sdot+D*partial_z(Sdot)
       =L_q-partial_z(L_d)-A*v-B*partial_z(v).

All quantities on the right come from the full prepared profiles and
uncertain root, including the spatial Euler flux. Its exported component
intervals have absolute endpoints below 3.03 in the declared coordinates.
This is a finite FORCING bound, not an acceleration or time-error bound.
The matrix on the left remains to be solved together with gauge, momentum,
charge and auxiliary tangency conditions. No shift drift is set to zero.

The auxiliary Euler equation reduces exactly to

    E_Z=b*N*sqrt(h)*(Z+Delta psi).

The lapse-gradient terms cancel only with the complete spatial flux. It is
satisfied by the prepared auxiliary relation. The temporary unused Z-rate
slot cannot affect the other momentum derivatives because those coefficients
are exactly zero; its physical time tangency must still be reconstructed.

## Verification and preserved implementation failures

[Executable V4](../../../Analysis/MasterTests/test_01_r4c1_rtau_mixed_operator_v4.py):
29/29, no failed/unknown checks, exact recomputing read-only replay.
[Receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_mixed_operator_v4_attempt_01/summary.json)
SHA256 d916402a0751fa4a0409d2048ed4e38ea18dd9b5629836f6a3517fdd44e0b577.
The complete mixed Hessian is checked against original-density reverse AD
at z=0.3,1.1,2.4 and two complex steps at 100 digits. Maximum distances from
the outward coefficient enclosures are below 1.56e-35 and 1.55e-47; frozen
tolerances are 1e-24 and 1e-32. Lapse-curvature and spatial-drift omission
controls reject the shortened formulae.

[Variational/endpoint audit](../../../Analysis/MasterTests/audit_01_r4c1_rtau_mixed_operator_v1.py):
16/16, exact replay.
[Audit receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_mixed_operator_audit_v1_attempt_01/summary.json)
SHA256 38dd70c6da41c7f917658220c0e82181c6be164923efbe9992bb28d31369ea3b.
It independently derives the lapse-map curvature, two-form boundary identity
and auxiliary Euler flux cancellation, and checks every exported endpoint.
Same-author controls do not constitute independent external scientific review.

V1, V2 and V3 remain preserved as NOT_COMPLETED failure records:

- [V2 namespace specification](RES001_R4C1_RTAU_MIXED_OPERATOR_V2_SPEC_2026-10-31.md):
  V1's extracted weak density lacked its original HM slot tuple.
- [V3 square specification](RES001_R4C1_RTAU_MIXED_OPERATOR_V3_SPEC_2026-10-31.md):
  V2's generic interval norm multiplication lost square nonnegativity.
- [V4 control specification](RES001_R4C1_RTAU_MIXED_OPERATOR_V4_SPEC_2026-10-31.md):
  V3 differentiated a clock-gradient slot fixed by the declared backend gauge.

No scientific equation, allowed 48-slot variation, threshold or parent result
was changed to obtain the completed V4 checks. Original sources, hashes,
sidecars, local traces and unrelated files remain preserved.

## Next dependency and publication implications

Use these actual mixed coefficients to construct the FULL field-dependent
momentum/charge/gauge tangent graph and solve the coupled initial acceleration
and shift-drift equations. Retain the global mean momentum equation, all
means, auxiliary time tangency, clock/lapse reconstruction, gauge-projector
drift and root uncertainty. Do not import the old homogeneous propagator or
project future fields onto the conformal preparation. Characteristics,
general transverse wavevectors, finite-time persistence, interactions/window
and identifying matching remain open.

No concrete correction to P1/P2, Thermodynamics or the original R4C1 paper
follows from this unadopted comparison prerequisite. Those papers and the
website are unchanged. G1-G6 remain incomplete; no canonical gate promotion,
action adoption, external dispatch, vault mutation, publication or commit/push.
