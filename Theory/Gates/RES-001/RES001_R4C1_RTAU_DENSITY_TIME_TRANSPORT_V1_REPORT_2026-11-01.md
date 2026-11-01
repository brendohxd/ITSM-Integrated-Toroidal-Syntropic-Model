# Direct canonical-density time transport

1 November 2026. Conditional R-tau comparison; review DEFERRED.
physics_pass=false; gate_effect=NONE; R-tau unadopted; G1-G6 incomplete.

## Result and boundary

The direct time derivative of the canonical density map agrees with the
independently implemented action current, retaining the finite-centre
momentum defects and their general perturbations. This closes the local
density-map/current consistency check following the
[46-check current/transport result](RES001_R4C1_RTAU_CURRENT_TRANSPORT_V2_REPORT_2026-11-01.md).
It does not complete the prepared evolution contract: uniform operator
domain closure, physical mixed-norm estimates and controlled evolution
remain open. No new action is adopted and original R4C1 failures remain.

[Specification](RES001_R4C1_RTAU_DENSITY_TIME_TRANSPORT_V1_SPEC_2026-11-01.md)
was frozen first. [Executable](../../../Analysis/MasterTests/test_01_r4c1_rtau_density_time_transport_v1.py)
passes23/23; [receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_density_time_transport_v1_attempt_01/summary.json)
SHA256 5b6b8626985344b39ba97acd24d7435b684f50f9bb5ebf343decd12b69f36e2f.
Immutable replay COMPLETE, session30077 terminal exit0, byte-identical.
The current/transport46-check receipt also replayed exactly; no further
replay is needed for these unchanged sources.

## Density and direct time derivative

Let L be the actual clock-substituted density, with independent spatial
frame V and all six metric components. Split its regulator part from
L_nonreg. On the auxiliary secondary surface Z=-Delta_h psi,

    I=L_nonreg-p*(v-Lie_S q)-partial_z B0-b*N*sqrt(h)*Z^2/2,
    B0=N*gamma*sum_i(h^{iz}*p_Vi)-N*curvature_flux/2.

This is the same improved density as the raw lapse construction,
I=L-p*(v-Lie_S q)-partial_z(N*L_Nz). It is not a replacement energy
definition. Explicitly,

    L_reg=b*N*sqrt(h)*(Z^2/2-h^{zz}*Z_z*psi_z
                              +beta*Z*h^{zz}*psi_z^2),
    B_reg=-b*N*sqrt(h)*Z*h^{zz}*psi_z,
    L_reg-partial_z B_reg=b*N*sqrt(h)*(Z^2/2+Z*Delta_h psi).

The lapse-gradient contributions cancel. On the secondary surface the
last expression is -b*N*sqrt(h)*Z^2/2; its first variation is retained.
The negative sign here is an energy-density term, not a newly established
physical ghost classification or a chosen cutoff.

The regulator has no independent adapted-time velocity momentum.
Using the actual Legendre relation p=L_nonreg,v and the linearity of the
spatial Lie generator in q gives the local cancellation

    partial_t[L_nonreg-p*(v-Lie_S q)]
      =L_nonreg,q*v+L_nonreg,d*v_z
                 -pdot*(v-Lie_S q)+p*Lie_S v.

All acceleration terms cancel. Shift-time terms also cancel locally
between L_S*Sdot+L_Sz*Sdot_z and p*Lie_Sdot q. This is an identity;
it is not an imposed physical Sdot=0 prescription.

The implementation differentiates B0 in time and then in space using
metric/frame canonical rates, and differentiates the on-secondary
regulator density using the reconstructed Zdot. Mixed time/tangent
differentiation supplies the perturbation. The required action information
is the full Hessian, not a fresh full third variation. Only metric/frame
momentum-rate first spatial derivatives are needed for B0. The force-rate
second spatial derivative enters Zdot. Unsupported Zdot spatial derivatives
and scalar momentum-rate spatial derivatives are not manufactured.

## Relation to the action current and moving map

With mathcalF from the full-metric clock-current owner and C_i the
canonical spatial momentum constraint, the inherited time Ward identity
on the full canonical Euler/auxiliary equations gives

    I_dot-partial_z(S^z*I+mathcalF^z)
      =partial_z(N^2*h^{iz}*C_i),
    delta R=partial_z(N^2*h^{iz}*delta C_i
                             +delta(N^2*h^{iz})*C_i).

The direct density derivative and current are calculated independently.
Their agreement does not arise by setting their residual to zero or
solving for a desired coefficient. At an exact constrained smooth
background with an admitted tangent C=delta C=0, the right side vanishes.
The point controls deliberately do not make those assumptions.

For the old/adapted coordinate change with J=partial_z zeta and its
background coordinate velocity w,

    I_new=I/J,
    I_dot_new=(I_dot-partial_z(w*I))/J,
    S_new^zeta=J*(S_old^z-w), mathcalF_new^zeta=mathcalF_old^z.

The same paired map applies to perturbations when its background J,w are
held fixed. The current-row test retains both the density Jacobian and
moving-coordinate divergence. These are the density component of
G_Y=(T_dot+T*A_can)*T^{-1}, not an instantaneous similarity transform.
For a field-dependent constrained chart, T_dot also contains its background
and gauge/constraint drift. The local check does not bound every such
operator term or prove an evolving inverse exists on a fixed Banach domain.

## Controls and what they show

At z=0.3,1.1,2.4 the improved density and tangent agree with the raw lapse
map through their first spatial coefficients at the frozen1e-28 tolerance.
Direct background/time-tangent Ward discrepancies are below
1.172e-47/1.046e-46. These are arithmetic consistency bounds at the stated
points, not physical error bars or a uniform prepared-root estimate.

The actual background residuals are approximately -6.0524e-13,
5.8574e-13 and2.8665e-13, matching their finite-centre momentum defects.
The arbitrary test perturbation is not constrained: its residual is about
0.339 at each point, also matching the independently calculated linearized
Ward defect. Its nonzero value is retained. This is an off-constraint
identity test, not the admission of that probe as a physical perturbation.

Checks reject omitted regulator-density time variation, lapse improvement
and moving-density drift. The run/replay preserve384 inherited/current
source and sidecar byte/mtime pairs. The earlier current V1 implementation
failure remains preserved and is not counted as scientific evidence.
No new failure was encountered in this direct-density implementation.

For any sufficiently regular periodic solution of the constrained equations,
the divergence law preserves the global I integral, and the U(1) transport
law preserves Q. Physical clock flow X_H0=-X_I remains on the fixed-charge
level; it is not quotiented away as coordinate gauge. These conditional
identities do not prove solution existence, weighted longitudinal range
preservation in an evolving function space, or absence of caustics.

## Next deciding calculation

The local field/momentum, auxiliary, gauge and current pieces are now
mutually consistent in their registered controls. The next task is the
actual variable-coefficient physical evolution estimate: assemble the
compatible periodic chart with its moving inverse, specify the physical
mixed regularity/domain, and test its zero-speed/quartic coupling without
invented positive norm weights or dropping forced harmonics. Establish
uniform coefficient and constraint/weighted-range bounds, or preserve the
precise obstruction. The completed homogeneous t=0.05 control is a
different background and cannot supply this theorem.

Principal Jordan/cone warnings, nonlinear persistence, transverse modes,
interactions/window, GR/local compatibility and identifying matter/force
matching remain open. No new K_Q, V, C_chi or a0 is obtained. No concrete
change to P1/P2, Thermodynamics or original R4C1 claims follows from this
unadopted-candidate check. All inherited review debt remains deferred;
same-author controls are not external review. Goal ACTIVE and incomplete.
No publication, external dispatch, action adoption, vault mutation or
commit/push/deployment.
