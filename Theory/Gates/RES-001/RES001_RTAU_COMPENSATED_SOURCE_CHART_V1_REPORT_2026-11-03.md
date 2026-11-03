# Complete initial compensated-source and canonical-state chart

3 November 2026. Conditional initial planar result. R-tau remains an
unadopted comparator; original R4C1 unchanged. Review DEFERRED;
physics_pass=false; gate_effect=NONE; G1-G6 incomplete; goal ACTIVE.

## Result and precise limit

The full initial source map is now bounded in both directions between the
canonical configuration H1/momentum L2 state and the compensated-scalar
H^-1/free-data chart, on the declared exact compatible range. This supplies
the free-source estimate missing from the preceding projected static inverse.
The improvement flux, its variable outer multiplier, all three momentum
sources and all three independent retained momentum means are included.

This is a bounded INITIAL linear chart and norm equivalence. It is not an
action-energy positivity theorem, a strong symplectic inverse, an evolution
symmetrizer or a controlled background interval. In particular Sigma_L2 is
not inferred from canonical H1/L2. The stronger Sigma_L2 domain used in the
earlier rate estimate remains an explicit additional observable restriction.

Owners: [frozen contract](RES001_RTAU_COMPENSATED_SOURCE_CHART_V1_SPEC_2026-11-03.md),
[static inverse](RES001_RTAU_COMPENSATED_STATIC_INVERSE_V1_REPORT_2026-11-03.md),
[compensated identity](RES001_RTAU_COMPENSATED_DENSITY_V1_REPORT_2026-11-03.md),
[initial rate](RES001_RTAU_COMPENSATED_RATE_V1_REPORT_2026-11-03.md), and
[original momentum completion](RES001_R4C1_RTAU_COUPLED_PERIODIC_INVERSE_V1_REPORT_2026-11-01.md).
The [coupled observable-norm bundle](RES001_RTAU_COUPLED_OBSERVABLE_NORM_V1_CONTRACT_2026-11-02.md)
remains incomplete.

## Derive the complete static canonical variation

Let x=delta q for the 13 nonauxiliary fields, pi=delta p for their canonical
momenta, and M=N*sqrt(h). Let RV=q_t-Lie_S q and p_o be the background
canonical momentum with its force-scalar component set to zero ONLY in the
other-sector Legendre expression. The actual identity is

    Sigma=(L_other-sum_other p_i*RV_i-D_z B0)/M,
    B0=N*(gamma*h^{iz}*p_Vi-curvature_flux/2).

Here L_other is the same action after removing the full frame-dependent
force and clock-spatial regulator. Its first canonical variation is

    delta Sigma=M^-1*(sum_i[L_other,qi*x_i+L_other,di*x_i,z
                             +p_o,i*Lie_S(x)_i]
                    -sum_other RV_i*pi_i-D_z delta B0)
                    -Sigma*delta M/M.

The time-velocity variation cancels by the actual Legendre relation.
Shift variation cancels between L_other and the retained Lie term; direct
raw-action controls include nonzero delta S and delta S_z. Scalar lapse and
volume variation remain in delta M. The force scalar momentum cancels from
this compensated static row by the exact force Legendre identity. It is not
deleted from the state or the original constraints.

Write the local field terms as sum(a_i*x_i+b_i*x_i,z) and

    delta B0=sum(Bq_i*x_i+Bd_i*x_i,z+Bp_i*pi_i).

All coefficient vectors are evaluated across the certified initial-root
ball. The coefficient outside the divergence is variable. With m=1/M,

    m*D_z F=D_z(m*F)-m_z*F,
    ||m*D_z F||H^-1<=(||m||infinity+||m_z||infinity)*||F||L2.

This identity retains the derivative of the outer multiplier. It requires
no pointwise derivative of a rough x_z or pi. Thus

    ||delta Sigma||H^-1<=Cq*||x||H1+Cp*||pi||L2,
    Cq<3.704022, Cp<4.180250.

The vectors Bq,Bd and Bp contain the full frame/curvature improvement.
Auxiliary-column exclusions use exact other-sector independence, not small
interval-subtraction remainders. Only known initial root derivatives enter.
The full norm-cubed force remains in the action used to construct this
identity and the raw temporal inverse; it is not replaced by clock-only
kinetic energy.

## All momentum sources remain present

The canonical momentum constraint has the full form

    C_i=D_z(B(q)^T*p)_i-delta_iz*p.q_z.

For free data x_f,pi_f, its source is the negative of

    D_z(B(q)^T*pi_f+K(p)*x_f)_i
       -delta_iz*(pi_f.q_z+p.x_f,z),

where K(p)*x=B(x)^T*p. Both field-generator variation and the longitudinal
nondivergence term are retained. The force scalar has a zero row in B(q),
but its momentum contributes through p.x_f,z and pi_f.q_z. Direct controls
specifically reject deleting that contribution just because it cancels in
the compensated density row.

The whole-root H^-1 source bounds are

    ||s_i||H^-1<=sQ_i*Qfree+sP_i*Pfree,
    sQ_i=||K_i(p)||+delta_iz*||p||,
    sP_i=||B_column_i(q)||+delta_iz*||q_z||.

All coefficient norms here are uniform Euclidean coefficient-vector bounds.
The original integrating-factor solution gives

    ||p_source,i||L2<=cs_i*||s_i||H^-1+ce_i*abs(eta_i),

with r=1/13000,

    cs_x=cs_y=(1+exp(4r))*exp(2r)*sqrt(2),
    cs_z=(1+exp(2r))*exp(2r)*(1+r)/sqrt(2),
    ce_x=ce_y=exp(4r), ce_z=exp(2r).

These include the weighted longitudinal source and all retained original
momentum means eta_i. The sqrt(2) factor comes from the all-mode periodic
H^-1->L2 antiderivative bound. No band or parity restriction is adopted.

## Assemble and invert the complete source

Use input order

    (Sigma_Hminus1_original, Qfree_H1_original, Pfree_L2_original,
     abs(eta_x)+abs(eta_y)+abs(eta_z)).

The assembled compensated source is delta Sigma minus the free-field
static row plus the completed momentum-source terms with the actual
coefficients Wi=RVi/M. A conservative outward bound is

    ||assembled_source||H^-1
       <=Sigma_Hminus1+13.474477*Qfree+9.106811*Pfree+1.740949*eta_sum.

Apply the established whole-root weak inverse norm below 2.695016. Restore
the trace configuration using x_trace=(a^2*u,0,0,a^2*u,0,...), with

    ||x_trace||H1<=sqrt(2)*exp(2r)*(1+2r)*||u||H1.

Restore the three eliminated momenta using their actual trace operators
and source/mean pieces. This yields the complete initial canonical bound

    ||x||H1+||pi||L2
       <=6.451354*Sigma_Hminus1+97.449103*Qfree
                          +64.652772*Pfree+12.231780*eta_sum.

These rounded-up constants enclose the binary receipt endpoints. They are
spatial reconstruction bounds, not time-growth rates or physical lifetime
claims. The free trace-free metric projection in slots hxx/hyy and the free
momentum projection are orthogonal constant projections in these canonical
component norms. Therefore Qfree<=||x||H1 and Pfree<=||pi||L2; also
eta_sum<=sqrt(3)*||pi||L2. The forward data norm obeys

    Sigma_Hminus1+Qfree+Pfree+eta_sum
       <=4.704022*||x||H1+6.912300*||pi||L2.

Together these estimates give a bounded linear chart in both directions
ON THE ORIGINAL COMPATIBLE RANGE. Its inverse is unique by the previously
established projected trace inverse and the momentum mean normalization.
This is not a claim of surjectivity onto arbitrary free source tuples.

An additional force configuration H2 control is the identical free clock
configuration datum in both charts, and can be carried along unchanged.
It remains necessary for the earlier L2 auxiliary observable estimate.
The initial weak chart alone does not imply that stronger force control
or Sigma_L2. Adding those as explicit stronger domain conditions does not
turn the chart estimate into a physical energy theorem.

## Compatibility, evidence and next decision

The original spatial gauge, moduli/harmonic fields, transverse source means,
weighted longitudinal range and fixed-I/U1 charge tangents remain required.
In particular

    mean(R*u+s_z/(2*a))=0,
    integral delta I=0,
    delta I=M*delta Sigma+Sigma*delta M
                  -delta(M*(p*f_p-f))-delta(M*b*Z^2/2).

The Sigma mean is not fixed in place of the original charge. Physical clock
flow is retained. The vault continuity pointer chk_c3034d6f578f2f6525a0306c
identifies the older symplectic/charge-frame contract; the current local
bundle and static owners control this calculation. No stored historical
homogeneous theorem is transferred to the prepared background.

[Producer](../../../Analysis/MasterTests/test_rtau_compensated_source_chart_v1.py):
34/34 checks passed; no failed or unknown controls. Fresh
[receipt](../../../Analysis/MasterTests/outputs/rtau_compensated_source_chart_v1_20261103/receipt.json)
SHA256 4600a4b8a4237dee324b28490a896dbcd6776fbd3b1a88f89114ed74363429f7.
Read-only recomputation matched the receipt byte for byte, with all 34
controls again passing. Controls include
the complete raw canonical temporal inverse, all fields/momenta and nonzero
shift variation at three nonzero prepared locations, an independent weak
multiplier pairing, force-momentum cancellation/retention and source/mean
bounds. These are same-author checks; independent review remains deferred.
All 219 inherited source pins and snapshotted sidecar bytes/timestamps are
preserved. Earlier failed versions remain intact.

NEXT: test a compatible action-based coupled energy and generator in this
chart, including density transport, zero-speed/quartic coupling, moving
inverse/ranges, all symplectic cross terms and actual background bounds.
Do not infer a strong symplectic inverse or positivity from norm equivalence.
Controlled time evolution, nonlinear preservation, physical interactions,
validity window, GR/local compatibility and identifying matching remain
incomplete. No C_chi or a0 follows. No concrete paper defect or public
claim change is established. No action adoption, vault mutation/sync,
dispatch, publication, commit/push or deployment is included.
