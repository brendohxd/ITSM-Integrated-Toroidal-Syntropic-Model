# Prepared evolution entry and auxiliary closure

1 November 2026. Conditional comparison; review DEFERRED.
physics_pass=false; gate_effect=NONE; R-tau unadopted; G1-G6 incomplete.

## Actual progress and remaining contract

The unreduced canonical field/momentum entry block and full-metric auxiliary
spatial/time reconstruction are implemented. The canonical rate inverse
now includes the second spatial derivative needed by the auxiliary time
row. The auxiliary is not left as an independent field-rate prescription.

This is NOT the complete prepared evolution operator. The actual
gauge-velocity solve, coordinate-rate composition, closed clock-current row,
constraint transport and physical norm remain incomplete under the
[owning evolution contract](RES001_R4C1_RTAU_PREPARED_EVOLUTION_V1_CONTRACT_2026-11-01.md).
No short-time stability, physical window or nonlinear admission is claimed.

## Canonical field and momentum rows

For prescribed canonical perturbation jets and caller-supplied shift
variation, the nonauxiliary thirteen rates solve

    M*dv=dp-L_vq*dq-L_vd*dq_z-L_vS*dS-L_vSz*dS_z,
    M*dv_z=rhs_z-M_z*dv,
    M*dv_zz=rhs_zz-2*M_z*dv_z-M_zz*dv.

The established validated temporal inverse supplies interval solve errors;
no auxiliary or gauge-null temporal block is inverted. The momentum rows
are the complete spatial Euler variations

    delta pdot_i=sum_k L_qi,yk*delta yk
                   -partial_z(sum_k L_di,yk*delta yk),

including all fourteen rows and coefficient derivatives. The Z row remains
the secondary-constraint tangent because p_Z=0. The unused auxiliary-rate
slot cannot affect these rows, by the inherited exact Hessian zeros; it is
not returned as a physical zero Zdot. The older entry block's zero second
rate slot was unused there and is not reused for auxiliary reconstruction.

[Entry V1](../../../Analysis/MasterTests/test_01_r4c1_rtau_canonical_flow_entry_v1.py):
15/15, exact replay COMPLETE, session40643 terminal exit0;
receipt5628cf0fb09844bc49005f727f8852bf81e96807b67a004848d803d703ba0075.
[Second-jet V2](../../../Analysis/MasterTests/test_01_r4c1_rtau_canonical_flow_second_jet_v2.py):
15/15, exact replay COMPLETE, session35009 terminal exit0;
receiptae30954122771bfd504f4b41396d70bc324dfd40702412ae192c5a8c13041786.
Both compare independent prescribed rate jets at the three prepared points,
retaining nonzero shift variations and rejecting omitted flux/drift.
Worst rate/momentum defects are below 7.374e-48/1.274e-47. These are local
controls, not a uniform physical evolution estimate.

## Full-metric auxiliary spatial/time closure

For a general positive planar spatial metric define

    C=hInv_zz*tr(hInv*h_z)/2-(hInv*h_z*hInv)_zz,
    Delta_h psi=hInv_zz*psi_zz+C*psi_z,
    Z=-Delta_h psi.

All six metric components remain independent. To supply Z and delta Z
through second spatial order, the module requires metric jets through
order3 and force jets through order4. The prepared background fourth force
derivative is the exact fixed-profile value

    psi_zzzz=epsilon*(cos(z)/29+16*cos(2z)/31).

Perturbation fourth derivatives are explicit independent inputs. They are
not fitted or filled with zero. Mixed time/field differentiation gives

    Zdot=-partial_t(Delta_h psi),
    delta Zdot=-delta partial_t(Delta_h psi).

The second-variation algebra receives both metric rates and field
perturbations, with mixed input equal to the perturbation rate. Thus the
mixed derivative retains the metric/time terms and psi_dot,zz. It returns
the time-row VALUE only; unsupported spatial derivatives of Zdot are not
fabricated. The auxiliary spatial jet is sufficient to retain the force
Euler row's fourth-spatial-order contribution.

The independent time check uses hInv_dot=-hInv*hdot*hInv and differentiates
C explicitly, then compares symmetric field perturbations. At the three
prepared centres, background Z through second order agrees below1.142e-53
and its actual first time tangent below6.624e-53. Independent finite
differences at steps1e-12/1e-16 have errors below3.810e-27/3.835e-35,
against frozen1e-20/1e-28. Metric-time and force-rate-second-derivative
omissions are rejected. These are caller-supplied rate controls; the gauge
and physical state-space transport have not been silently closed.

[Auxiliary executable V2](../../../Analysis/MasterTests/test_01_r4c1_rtau_auxiliary_rate_v2.py):
21/21, exact replay COMPLETE.
[Receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_auxiliary_rate_v2_attempt_01/summary.json)
SHA25657233b4614cc62519f53c7b9f706c6bdea85276334c55b9fb6d7cd930393068d.
V1's incomplete driver and failure record are preserved. Its mp/interval
step multiplication was corrected in [V2](RES001_R4C1_RTAU_AUXILIARY_RATE_V2_SPEC_2026-11-01.md),
with the same geometry, steps and tolerances. No physical input changes.

After substitution, delta Z=-delta Delta_h psi makes the secondary
tangent zero; its first time tangent follows from the mixed derivative.
The nonauxiliary rate reconstruction is independent of Z/Z_z by the
inherited exact Legendre cross-coefficient zeros. Composition therefore
does not introduce an extra auxiliary kinetic mode. This action identity
does not supply missing higher derivative bounds or nonlinear persistence.

## Next actual closure

Close the gauge-velocity solve in the existing adapted coordinates, keeping
its harmonic coordinate freedom and physical metric/momentum moduli. The
initial coordinate map must transform qdot, shift and momentum-density flow
together. Then close the density row with the explicit clock current and
compare full moving-map transport, preserving clock-time flow on the fixed
charge level. Do not substitute a formal similarity transform or another
initial-spectrum inventory for that calculation.

Older progress notes stating replay RUNNING are historical; both canonical
entry replays and the auxiliary replay are now terminal and exact. No
process remains running from these components. Goal ACTIVE; full evolution
and physical norm remain incomplete. Review DEFERRED; no canonical action
adoption, external dispatch, vault mutation, publication, commit or push.
