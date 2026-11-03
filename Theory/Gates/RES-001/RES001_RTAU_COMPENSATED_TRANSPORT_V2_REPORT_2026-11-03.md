# Initial compensated-density transport in its weak chart norm

3 November 2026. Conditional initial planar density-sector result.
R-tau remains an unadopted comparator; original R4C1 unchanged.
Review DEFERRED; physics_pass=false; gate_effect=NONE; G1-G6 incomplete.

## Result and limitation

The compensated density sector has an initial H^-1 logarithmic-norm
estimate using the new compatible source/state chart. It does not require
an additional Sigma_L2 bound. Advection is retained as part of the operator,
rather than estimated by treating a derivative of Sigma as external forcing.
Reaction, full material remainder, corrective gauge shift and both scalar
coordinate pullback directions are included.

The estimate is finite but conservative, with a large composed density
coefficient. It does not certify a useful finite-time accuracy or the target
interval [0,0.05]. There is still no actual coupled background tube or full
coupled physical-energy inequality. This is an INITIAL density-sector bound
conditional on the exact compatible prepared background/tangent; it is not
a theorem of nonlinear existence or positive physical energy.

Owners: [V1 contract](RES001_RTAU_COMPENSATED_TRANSPORT_V1_SPEC_2026-11-03.md),
[V2 implementation correction](RES001_RTAU_COMPENSATED_TRANSPORT_V2_SPEC_2026-11-03.md),
[complete source/state chart](RES001_RTAU_COMPENSATED_SOURCE_CHART_V1_REPORT_2026-11-03.md),
[complete material row](RES001_RTAU_COMPENSATED_RATE_V1_REPORT_2026-11-03.md),
and [action identity](RES001_RTAU_COMPENSATED_DENSITY_V1_REPORT_2026-11-03.md).

## Transport and reaction in the actual adapted coordinate

Let u=delta Sigma in the adapted coordinate zeta, J=zeta_z and w the
background coordinate drift. The principal scalar row is

    u_t=B*u_zeta+C*u+F,
    B=J*(S^z-w), C=N*(beta*p-trK).

The source F contains the full linearized material remainder, including
delta C times the background Sigma, force/frame/other-action terms and
surviving metric/regulator work. Corrective shift times background Sigma_z
is also retained. The momentum-constraint Ward defect vanishes only on
the exact constrained background and compatible tangent. A numerical
centre is not declared an exact constrained state.

Writing lambda_z=J_z/J gives

    B_zeta=lambda_z*(S^z-w)+S^z_z-w_z,
    B_zetazeta=[lambda_zz*(S^z-w)+lambda_z*(S^z_z-w_z)
                                         +S^z_zz-w_zz]/J.

Use the original gauge relation
w_zz=L_z-lambda_zz*w-lambda_z*w_z. The known initial profile and certified
root C2 bounds suffice. No third shift-root derivative is introduced.
Whole-root outward bounds are

    ||B_zeta||infinity<0.003477985,
    ||B_zetazeta||infinity<0.006316896.

The reaction multiplier satisfies

    ||C*u||H^-1<=(||C||infinity+||C_zeta||infinity)*||u||H^-1,
    ||C||infinity<2.525672, ||C_zeta||infinity<0.009091965.

Its conservative multiplier bound is below 2.534764. No pointwise
positivity or damping inference is made from this absolute bound.

## Exact H^-1 transport energy identity

Let v=(1-D_zeta^2)^-1*u, so ||u||H^-1=||v||H1. Periodic integration by
parts gives the exact real transport pairing

    <v,B*D_zeta(u)>
      =-integral[B_zeta*v^2/2+3*B_zeta*v_zeta^2/2
                                  +B_zetazeta*v*v_zeta].

Complex perturbations use the real Hermitian pairing and the same bound.
Consequently the scalar transport logarithmic bound is

    gamma_B=(3/2)*||B_zeta||infinity+(1/2)*||B_zetazeta||infinity
             <0.008375424.

The B_zetazeta term is necessary; an independent periodic nonconstant
profile gives a nonzero omitted contribution. This estimate does not
bound B*u_zeta as a forcing term in H^-1. It controls its energy pairing.
The reaction term is handled through its H^-1 multiplier estimate above.

## Complete source and coordinate composition

The earlier material-rate producer first closed its canonical/gauge row,
then lifted it to its old density-source coordinates. Its frozen lift
formula explicitly stores the pre-graph canonical P,Q,force,H coefficients
in columns 2,1,3,4 of full_material_rate. The executable verifies this
selection symbolically against that actual immutable function. No matrix
inversion or subtraction of rounded display constants is used.

The old material Sigma column contains only C*u, which is now treated as
the reaction multiplier; it is not discarded. In the frozen source,
unit(4) appears in the material row only through coefficient_times_Sigma.
The separate Eulerian derivative column is replaced by the retained
transport operator, not dropped. All other material contributions remain.

For the corrective shift, use the weak identity

    delta S*Sigma_background,z
       =D_z(delta S*Sigma_background)-delta S_z*Sigma_background.

Its H^-1 bound needs only the bounded background Sigma and the full
corrective shift H1 bound. It does not assume a pointwise background
Sigma_z. The gauge receipt supplies the shift's canonical-data constants,
including the harmonic coordinate-velocity input.

For j<=J<=j_upper and |J_z/J|<=r, scalar distribution pullbacks obey the
conservative bounds

    original -> adapted: j_upper*(max(1,j_upper)+r)/sqrt(j),
    adapted -> original: (1+r)*j^(-3/2),

with j<=1. The first follows from testing against J*phi(zeta(z)); the
second from testing against phi(z(zeta))/J. First derivatives of these
weights are retained. Both factors are below 1.000462 and 1.000308,
respectively. These are scalar pullbacks, not canonical-density weights.

Compose the material/gauge source with the full canonical reconstruction
from the source chart, using the inverse scalar pullback for its original-
coordinate Sigma input. Define s=||u||H^-1_adapted. The resulting initial
norm inequality, with outward rounded constants, is

    d(s)/dt <=47255*s+682801*Qfree_H1_original
                    +452851*Pfree_L2_original+86081*eta_sum
                    +0.000301*force_H2_original+55.726*harmonic_velocity.

At s=0 use the upper right norm derivative; equivalently apply the energy
inequality to s^2/2 and pass to a regularized norm. The constants apply to
the initial operator throughout the certified root ball, not to an
unproved time-uniform background family. The large composed coefficient
is a conservative estimate, not evidence of an actual growth rate or an
instability, and gives no useful physical lifetime.

The natural H^-1 density input is justified by the completed initial
canonical/compensated chart. Force H2 remains an explicit configuration
control for the quartic/auxiliary terms. The original momentum means,
harmonic data, weighted range, fixed-I/U1 charges and physical clock flow
are retained. There is no stronger Sigma_L2 input in this estimate.

## Verification, failure preservation and remaining work

[V2 executable](../../../Analysis/MasterTests/test_rtau_compensated_transport_v2.py):
15/15 controls and byte-identical read-only replay COMPLETE. Fresh
[receipt](../../../Analysis/MasterTests/outputs/rtau_compensated_transport_v2_20261103/receipt.json)
SHA256 f98ced812b3e47d6a2877f13e44ca2b7078362f7a04f4b52882b0bfa18831dcb.
The generic transport identity, independent periodic pairing, adapted
derivative identities, canonical coefficient extraction, reaction product
and coordinate bounds are checked. Same-author controls do not replace
independent scientific review.

V1 failed before receipt creation when a point-mpf left operand attempted
to coerce a nonzero-width interval. Its source, contract, sidecars and
[failure](../../../Analysis/MasterTests/outputs/rtau_compensated_transport_v1_20261103/failure.json)
remain unchanged. V2 adds the explicit interval cast and provenance paths;
equations, inputs and acceptance tests are unchanged. No V1 pass is claimed.
All 219 inherited source pins and snapshotted source/sidecar bytes and
timestamps remain preserved.

NEXT: the coupled metric/frame/matter/force energy, including the other
zero-speed partner, quartic mode, all symplectic cross terms and evolving
constraint/gauge/Green maps. The scalar density estimate does not control
those sectors or prove strong symplectic invertibility. A full background
tube, nonlinear preservation, physical interactions/window, GR/local
compatibility and identifying matching remain incomplete. No C_chi/a0
prediction or concrete paper/public-claim revision follows. Goal ACTIVE.
No action adoption, vault mutation/sync, dispatch, publication or Git delivery.
