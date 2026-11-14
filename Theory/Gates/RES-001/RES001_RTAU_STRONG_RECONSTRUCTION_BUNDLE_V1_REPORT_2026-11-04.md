# Strong initial constraint reconstruction and force-coordinate control

4 November 2026. Conditional component of the
[actual-generator remainder contract](RES001_RTAU_ACTUAL_GENERATOR_REMAINDER_V1_CONTRACT_2026-11-04.md)
and [prepared coupled-energy contract](RES001_RTAU_PREPARED_COUPLED_ENERGY_V1_CONTRACT_2026-11-04.md).
Operator acknowledged High for this calculation and returned to Medium
after its exact replays. R-tau remains UNADOPTED; original R4C1 unchanged.
Review DEFERRED; physics_pass=false; gate_effect=NONE; G1-G6 INCOMPLETE.

## Result and limits

The actual initial constraint reconstruction now has bounds from corrected
physical density and the free canonical data, rather than only from already
assembled rough sources. The physical density's metric-measure variation is
retained in the scalar operator. The difference between the metric trace
gradient and its local momentum-leading lift gains one derivative, with
explicit H1 bounds. The auxiliary force coordinate also has a two-way norm
estimate on the actual compatible image, with the force mean retained.

These results justify two reconstruction steps needed to interpret the
20-direction principal variables in the declared strong topology. They do
not assemble the full rate operator, prove a time-dependent energy inequality,
transport the compatible range or establish an actual background tube.
The full actual-minus-principal remainder acceptance is still OPEN.

## Data, ensemble and source assembly

Use the normalized original-coordinate circle Bessel norms of the
[weak graph](RES001_RTAU_WEAK_GRAPH_V1_REPORT_2026-11-03.md).
At the certified conformal initial slice, the unknown trace is
delta hxx=delta hyy=a^2*f. Write the remaining field variation as q_free,
with zero transverse trace; mixed/longitudinal metric moduli remain in it.
The force field is chi=delta psi. The ten free momenta occupy original slots
0,1,3,6,7,8,9,10,11,12; the eliminated metric momenta occupy 2,4,5.
Their independent original-coordinate means are eta_x,eta_y,eta_z.

The input norm columns below are

    D=||w||L2,
    Q=||q_free,ordinary||H1 (including metric moduli and field means),
    P=||p_free||L2 (including xi=delta pi_psi), F=||chi||H2,
    |eta_x|, |eta_y|, |eta_z|.

Here w is the existing two-step corrected physical density. All input tuples
must satisfy the original transverse source means, the longitudinal weighted
range after reconstruction, and the independent fixed-I/U1 charge tangents.
The projected Green inverse does not impose these conditions automatically.
No parity, Fourier band or physical mean is removed.

Reuse the exact [canonical density graph](RES001_R4C1_RTAU_CANONICAL_DENSITY_GRAPH_V2_REPORT_2026-11-01.md)
and its explicit canonical lapse improvement F_lapse. Its coefficients are

    C0=L_q+T(S_z)^T*p-(F_lapse,q)_z,
    C1=L_d+S^z*p-F_lapse,q-(F_lapse,d)_z,
    C2=-F_lapse,d,
    D0=-(qdot-Lie_S q)-(F_lapse,p)_z,
    D1=-F_lapse,p.

They act as delta I_density=C0*dq+C1*dq_z+C2*dq_zz+D0*dp+D1*dp_z.
The inherited action identity fixes C2 to the transverse metric trace and
force columns and D1 to the frame-z momentum column at this initial slice.
The auxiliary variation cancels on its exact secondary equation. These are
reused exact identities, not conclusions from an interval containing zero.
All remaining first-variation coefficients are newly enclosed, retaining
the full action and the original root uncertainty. A first-differential
version of the existing arithmetic evaluates these coefficients without
generating a new Hessian. Separate exact symbolic/spatial controls validate
that first-differential implementation.

For each momentum-source row, the full canonical identity gives

    s_i=-D_z(B_i^T*p_free+delta B_i^T*p_background)
         +delta_iz*(p_free.q_background,z+p_background.q_free,z).

The trace-dependent and eliminated-momentum pieces are those of the existing
coupled inverse. D_z:L2->H^-1 has norm at most one, so these formulas give
explicit H^-1 source bounds from Q,P,F. The force contribution in the last
term is bounded using ||chi_z||L2<=F/2. The field-dependent generator term
delta B is retained. The old periodic source maps then give L2 bounds for
the three source-momentum pieces, including every eta_i.

## Physical density changes the lower-order trace operator

Let M=N*sqrt(h) and j=I_density on the background. The exact relation is

    delta j=M*delta Sigma+j*delta log(M),
    delta Sigma=w+c*P0primitive(xi)+alpha*chi_z.

The primitive and c,alpha are the existing normal-form owners' quantities.
It retains xi's independent mean. For the unknown trace, delta log(M)=f;
the free-field part also retains the lapse variation -beta*chi.
Consequently the trace operator for fixed physical-density coordinate is

    L_Sigma=L_current-M_j,  M_j:f -> j*f.

This is a coordinate reconstruction of the same action, not an action
change. The old current-density inverse remains valid in its own variables.
It must not simply be relabelled as the physical-density inverse.

At the pinned coefficient reference, j0=1/5. Thus

    L_Sigma,0=-D_z^2+(473/400)*P0-(3943/8400)*mean,
    ||L_Sigma,0^-1||H^-1->H1=8400/3943.

For every integer |n|>=1, the inverse ratio is
(1+n^2)/(n^2+473/400)<=1. The negative, nonzero mean has ratio 8400/3943
and remains in the inverse. With e_weak the old certified H1->H^-1
perturbation bound,

    ||L_Sigma-L_Sigma,0||H1->H^-1
        <= e_weak+||j-1/5||infinity.

Sixteen equal circle cells, each carrying the full certified root ball,
give j in [0.18283372035299...,0.21791970403472...]. The contraction is
below 0.361235851 and the physical-density Green norm is below 3.335124.
This is an entire-circle initial operator proof; cells are enclosure
subdivisions, not selected physical modes or a time-domain certificate.

## One-derivative remainder in the metric-gradient lift

Put A2=-N*a, C=N*gamma/a^2 and ell=C/A2=-gamma/a^3. After the exact
momentum reconstruction and physical-density measure adjustment, write

    A2*f_zz+A1*f_z+K*f=D_z(C*p_Vz)+r0.

K includes the full local and nonlocal zeroth-order trace operator.
The regular source r0 is L2 on the stated input space. In particular the
canonical momentum-improvement derivative cancels its coefficient gradient
in r0, leaving the material free-momentum rates. It is not discarded from
the differential equation. The source also retains M*w, M*c*primitive(xi),
M*alpha*chi_z, all free-field density coefficients, the free lapse/measure
term and the three source-momentum maps.

Define g=f_z-ell*p_Vz. Direct differentiation gives the exact identity

    A2*g_z=r0-A1*g-K*f+(A2_z-A1)*ell*p_Vz.

The leading momentum derivative has cancelled. The physical Green bound
first controls f in H1. Then ||g||L2<=||f||H1+||ell||infinity*P, and the
displayed equation bounds g_z in L2 using the positive lower bound on |A2|.
Thus g is H1 without requiring a derivative of an arbitrary L2 momentum.

The actual metric-gradient remainder is

    (a^2*f)_z+(gamma/a)*p_Vz=a^2*g+(a^2)_z*f.

Its H1 bound includes both first and second derivatives of a^2. In the
principal convention k=-i*D_z, this proves the corresponding lower-order
remainder relative to X_trace=i*(gamma/a)*p_Vz. Both metric trace entries
and all nine ordinary momenta remain.

Upward-rounded coefficients in the declared column order are:

| Output norm | D | Q | P | F | eta_x | eta_y | eta_z |
|---|---:|---:|---:|---:|---:|---:|---:|
| f H1 | 3.334893 | 41.461820 | 12.230720 | 2.505894 | 0.000037998 | 0.000037998 | 5.795153 |
| g H1 | 11.958379 | 148.675310 | 43.887872 | 8.985726 | 0.000136252 | 0.000136252 | 20.780471 |
| metric-gradient remainder H1 | 11.963086 | 148.733822 | 43.905141 | 8.989262 | 0.000136306 | 0.000136306 | 20.788649 |

Each bound is the sum of column coefficient times the named norm/absolute
mean. All eliminated-momentum coefficients and authoritative binary outward
endpoints are in the receipt. Constants are in existing dimensionless
control units; they are not measured rates, physical cutoffs or precision
claims for t=0.05.

## Closing the force-coordinate estimate on the compatible image

The earlier exact six-metric auxiliary variation gives

    delta Z=-kappa*chi_zz-kappa*lambda_z*chi_z+metric_terms,
    ||metric_terms||L2 <= Ck*||delta h||H1,Frobenius.

Use the inherited Ck<0.000369079, kappa^-1<=exp(2r),
|kappa*lambda_z|<=exp(2r)*r and r=1/13000. The exact all-harmonic inequalities
are F<=|mean(chi)|+2||chi_zz||L2 and ||chi_z||L2<=F/2.
Coordinate-to-Frobenius conversion and the trace lift give

    ||delta h||H1,Frobenius
        <= sqrt(2)*Q+sqrt(2)*exp(2r)*(1+2r)*||f||H1.

Substitute the complete f bound above. The resulting coefficient multiplying
F on the right is below 0.002694087, strictly below one. Moving that term
to the left proves an inverse ESTIMATE for already compatible data. Together
with the existing forward auxiliary estimate this gives two-way initial norm
control; it does not prove surjectivity for arbitrary auxiliary source tuples.
Weighted-range and charge conditions are still required.

For example, the reconstructed force field obeys the conservative bound

    F <= 0.003492350*D+0.044466339*Q+0.012808195*P
         +2.005711277*||delta Z||L2+1.002701365*|mean chi|
         +0.000000039792*(|eta_x|+|eta_y|)+0.006068772*|eta_z|.

The force mean cannot be reconstructed from a spatial Laplacian. It is an
explicit retained input. No zero mode has been absorbed into a cutoff or
deleted from the norm. The full initial physical/symplectic interpretation
and subsequent rate estimates retain their own outstanding requirements.

## Evidence, failed attempts and continuation

- [Strong lift V2 executable](../../../Analysis/MasterTests/test_rtau_strong_constraint_lift_v2.py)
  and [receipt](../../../Analysis/MasterTests/outputs/rtau_strong_constraint_lift_v2_20261104/receipt.json):
  79/79 component controls; byte-identical replay COMPLETE.
- [Independent control executable](../../../Analysis/MasterTests/audit_rtau_strong_constraint_lift_v1.py)
  and [receipt](../../../Analysis/MasterTests/outputs/rtau_strong_constraint_lift_audit_v1_20261104/receipt.json):
  28/28; byte-identical replay COMPLETE. Exact variable-coefficient/nonlocal
  and nonzero-mean fixtures, all-frequency remainder bounds and rejection of
  an omitted or wrong-sign leading momentum lift are included. Green upper
  endpoints receive independent exact-rational checks.
- [Coupled force-coordinate V2 executable](../../../Analysis/MasterTests/test_rtau_strong_force_coordinate_v2.py)
  and [receipt](../../../Analysis/MasterTests/outputs/rtau_strong_force_coordinate_v2_20261104/receipt.json):
  20/20; byte-identical replay COMPLETE. Exact-rational Machin bounds also
  validate the entire-circle enclosure coverage.

V1 strong lift stopped on interval-scalar/derivative-object multiplication
dispatch. V2 reorders the identical scalar product. V1 force-coordinate
receipt retains its 18/19 outcome: an expanded polynomial was compared
structurally with an equivalent factored form. V2 checks their exact
difference and adds separate integer controls. Neither correction changes
an equation, branch, norm, tolerance or acceptance criterion. All V1 files,
receipts/failure and hashes remain preserved. These are same-author controls,
not independent Rule-9 peer review.

The final package inherits 315 source pins, including the original 219 and
all 292 starting pins. Scientific sources and existing sidecars/timestamps
are checked unchanged. Original R4C1 failures, the rejected density-only
weakening and all independent paper evidence remain distinct.

NEXT: compose the actual canonical and gauge-closed rate rows with this
strong reconstruction. The ordinary and force rows still need their full
actual-minus-principal operator bound, including the moving physical-variable
map, global partners and applicable Green/range connection. Then restore
physical-time advection and bound T_dot/H_dot, with a genuine compatible
background tube before any finite-time integration. Do not repeat the
completed reconstruction as a new milestone or infer a full bound from it.

No new identifying K_Q/V or nonlinear-force input is supplied. There is no
new concrete P1/P2/Thermodynamics/original-R4C1 manuscript defect from these
coordinate estimates. No paper, website, gate or publication promotion is
warranted. Goal ACTIVE; full actual-generator contract and original G1-G6
remain INCOMPLETE. No action adoption, vault mutation/sync, model dispatch,
Git delivery, deployment or publication occurred in this calculation.
