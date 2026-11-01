# Full-metric clock current and canonical transport

1 November 2026. Conditional R-tau comparison; review DEFERRED.
physics_pass=false; gate_effect=NONE; R-tau unadopted; G1-G6 incomplete.

## Result

The action-derived clock-current row is implemented with the full planar
metric, reconstructed auxiliary spatial jets and actual canonical field
and momentum rates. Local U(1) and spatial momentum Noether transport
checks pass at all three registered finite centres. This advances the
[prepared evolution contract](RES001_R4C1_RTAU_PREPARED_EVOLUTION_V1_CONTRACT_2026-11-01.md),
but is not a physical norm, a finite-time existence theorem or action adoption.

[V2 executable](../../../Analysis/MasterTests/test_01_r4c1_rtau_current_transport_v2.py):
46/46 checks; [receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_current_transport_v2_attempt_01/summary.json)
SHA256 8ff36131f3058e32200ab8f7b3c8247d2a2ea66d8ea272ee1ebc8215dd22a322.
Immutable replay COMPLETE, native session90270 terminal exit0, byte-identical.
No repeat replay is needed for these unchanged sources.

## Current row

Use the covariant current derived by the
[clock-flux owner](RES001_R4C1_RTAU_CLOCK_FLUX_V1_REPORT_2026-11-01.md).
With positive FLRW K_ij=(hdot_ij-Lie_S h_ij)/(2N), p=(psi_dot-S^z psi_z)/N,

    mathcalF^i=b*N^2*sqrt(h)*[Z*h^{iz}*p_z
                  +Z*(K*h^{iz}-2*K^{iz})*psi_z-p*h^{iz}*Z_z],
    I_dot=partial_z(S^z*I+mathcalF^z),
    delta I_dot=partial_z(S^z*delta I+I*delta S^z+delta mathcalF^z).

All six metric components remain independent in differentiation. The
transverse current is retained even though only the longitudinal derivative
enters a planar density divergence. The module returns current value/first
spatial coefficient and the density-rate value only; no higher time-spatial
rate is fabricated. The auxiliary Z and delta Z spatial jets come from the
[full-metric secondary reconstruction](RES001_R4C1_RTAU_EVOLUTION_ENTRY_AUXILIARY_V2_REPORT_2026-11-01.md),
including explicit force fourth derivatives.

At fixed canonical q,p a pure shift variation produces Lie_deltaS q in
the field rate. Normal K and p, and hence mathcalF, are unchanged. The
density rate changes by partial_z(I*delta S^z), as required for a density.
This checks composition with the
[gauge-velocity owner](RES001_R4C1_RTAU_GAUGE_VELOCITY_V1_REPORT_2026-11-01.md);
it does not prescribe zero physical shift or erase harmonic/modulus data.

## Actual charge and constraint transport

For Q_density=u*p_v-v*p_u and Q_flux=-v*L_u_z+u*L_v_z, the canonical Euler
rows obey Q_density_dot+partial_z Q_flux=0. Its linearization is evaluated
with all canonical field/momentum directions and reconstructed delta Z.
The periodic integral preserves Q whenever a sufficiently regular solution
exists. It does not establish that solution's existence or boundedness.

For the canonical momentum constraint, write

    C_i=partial_z(B_i(q)^T*p)-delta_iz*p*q_z,
    C_dot=Lie_S C,
    delta C_dot=Lie_S delta C+Lie_deltaS C.

Here B is the full metric/frame local shift generator, not a scalar-only
translation. C is a covector density:

    (Lie_S C)_i=S^z*C_i,z+S^z_z*C_i+delta_iz*sum_j C_j*S^j_z.

The formula follows from the spatial Ward identity when the full canonical
Euler and auxiliary equations hold. The direct checks differentiate the
actual canonical constraint and use actual momentum-rate spatial derivatives
for the metric/frame rows. Scalar momentum-rate spatial derivatives are
unneeded and are not returned as physical zero values.

Finite-centre C is retained. In particular Lie_deltaS C is nonzero and
cannot be dropped by pretending that a numerical centre is the exact root.
On an exact smooth constrained solution the identity gives homogeneous
constraint transport. A conditional propagation identity is not a uniform
prepared-background evolution estimate, nor a proof of the weighted
compatibility map's finite-time invertibility.

## Controls and scope

At z=0.3,1.1,2.4 the generic current agrees with the independently frozen
prepared-profile current through first spatial order below4.242e-54.
All-field current tangents agree with symmetric finite differences below
3.307e-27/3.308e-35 at steps1e-12/1e-16, against the frozen1e-20/1e-28
tolerances. Pure-shift normal-current defects are below5.355e-53.
Actual background/tangent constraint-transport defects are below
2.005e-50/4.171e-47 against1e-28. These are local arithmetic controls;
their small errors do not quantify physical prediction accuracy.

Omitting regulator flux, auxiliary tangent or finite-centre constraint drift
is rejected. The run checks376 inherited/current source and sidecar byte/
mtime pairs. V1 failed at unsupported interval-left Jet multiplication
before completing the experiment; its source and failure remain sealed.
[V2 specification](RES001_R4C1_RTAU_CURRENT_TRANSPORT_V2_SPEC_2026-11-01.md)
corrects operand ordering only, retaining the scientific specification.

The next deciding check is the direct time derivative of the canonical
density map, including the lapse improvement and moving-map term. Full
prepared operator-domain closure, physical mixed-norm control, nonlinear
persistence, transverse modes, coupled interactions/window, GR/local
compatibility and identifying matching remain incomplete. The prior
principal Jordan/cone warnings remain. No new manuscript correction or
matching information follows from these controls. All inherited review
dependencies remain deferred; same-author replay is not external review.
Goal ACTIVE. No publication, action adoption, vault mutation or commit/push.
