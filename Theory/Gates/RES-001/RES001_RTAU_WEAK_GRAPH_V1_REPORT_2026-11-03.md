# Prepared R-tau weak initial graph and auxiliary observable

3 November 2026. Conditional mathematical component of the confirmed-High
coupled observable-norm bundle. R-tau remains an unadopted comparator.
Original R4C1 is unchanged. Review DEFERRED; physics_pass=false;
gate_effect=NONE; original G1-G6 incomplete.

## What changed

The existing coupled periodic momentum/density inverse extends to rough
assembled sources in H^-1, reconstructing the metric trace in H1 and all
three eliminated metric momenta in L2. This accommodates a derivative of
an L2 frame momentum without claiming that derivative is itself L2.
It does not supply two extra derivatives to the trace from physical-density
control alone. Both momentum parities, torus means and the weighted source
compatibility remain present.

The actual initial auxiliary observable also has a full six-metric-entry
bound from metric H1 and force-field H2 into L2. This is a justified mixed
regularity component, not a positive physical Hamiltonian, complete norm,
compatible evolution generator or time-uniform background estimate.

Owners: [whole bundle](RES001_RTAU_COUPLED_OBSERVABLE_NORM_V1_CONTRACT_2026-11-02.md),
[coupled inverse](RES001_R4C1_RTAU_COUPLED_PERIODIC_INVERSE_V1_REPORT_2026-11-01.md),
[canonical density graph](RES001_R4C1_RTAU_CANONICAL_DENSITY_GRAPH_V2_REPORT_2026-11-01.md),
[weak symplectic chart](RES001_R4C1_RTAU_SYMPLECTIC_CHARGE_FRAME_V1_REPORT_2026-11-01.md),
and [previous coupled auxiliary component](RES001_RTAU_COUPLED_AUXILIARY_BUNDLE_PROGRESS_2026-11-02.md).
The [specific contract](RES001_RTAU_WEAK_GRAPH_V1_SPEC_2026-11-03.md) was frozen
before execution; no old acceptance requirement was changed.

## Continuum weak inverse

Use normalized circle Bessel norms

    ||u||Hs^2=sum_n(1+n^2)^s |u_n|^2.

The old actual initial scalar operator, after elimination of the three
metric momentum unknowns, is

    L f=A2 f''+A1 f'+A0 f-sum_i Rvel_i*T_i f.

Its reference is

    L0=-D^2+(553/400)P0-(2263/8400)mean.

For n!=0 the ratio defining ||L0^-1||H^-1->H1 is
(1+n^2)/(n^2+553/400)<=1. The mean ratio is 8400/2263. Therefore the same
reference bound 8400/2263 holds, including its negative, nonzero mean.
No mean positivity or kinetic interpretation follows from this inversion.

For test g in H1, integrate the leading term by parts:

    <A2 f'',g>=-<A2 f',g'>-<A2' f',g>.

The norm of D:L2->H^-1 is <=1. All old multiplication and nonlocal
L2->L2 terms remain bounded H1->H^-1 by the norm-one embeddings. The
old first-derivative factor 1/2, appropriate for H2 input, becomes 1 for
H1 input. Thus, if e_old is the old H2->L2 perturbation estimate,

    ||L-L0||H1->H^-1 <= e_old+||A1||infinity/2+||A2'||infinity.

This is an upper bound, not equality of the two operator norms. Here
A2=-N*a, a=exp(lambda), N=exp(-beta*psi), beta=2/5, r=1/13000 and

    psi_max=(1/1000)(1/29+1/31),
    psi_z_max=(1/1000)(1/29+2/31),
    |A2'|<=exp(r+beta*psi_max)*(r+beta*psi_z_max).

It uses the exact prepared profiles, rather than a numerical grid maximum.
Together with the old whole-root coefficients, outward arithmetic gives

    |A2'| <0.000116535,
    ||L-L0||H1->H^-1 <0.151647,
    ||L0^-1(L-L0)||H1->H1 <0.562894,
    ||L^-1||H^-1->H1 <8.491947.

The Neumann series converges on the entire initial circle/root ball.
This extends the actual nonlocal operator, not a specialized homogeneous
matrix or a finite Fourier truncation. No finite-time Neumann margin has
been inferred: L_dot and the future background are separate work.

## Rough momentum sources and retained range

For nonzero integer harmonics,

    ||Dinv P0||H^-1->L2=sup_n!=0 sqrt(1+n^2)/|n|=sqrt(2).

A smooth multiplier g obeys

    ||M_g||H^-1->H^-1 <= ||g||infinity+||g'||infinity

by duality from the H1 product rule. These facts extend the exact momentum
source formulas in the old owner. Let

    Dminus=||r_source||H^-1+sum_i(||s_i||H^-1+|eta_i|).

r_source is the density right side after known free-field/charge source
assembly, before adding the three source-momentum rate terms to the scalar
solve. It is not just the physical density perturbation. eta_i are the
retained original-coordinate momentum means.

For r=1/13000 put w2=exp(2r), ratio2=exp(4r), ratio1=exp(2r). The
transverse source maps have coefficient
(1+ratio2)*w2*sqrt(2) for ||s_x/s_y||H^-1 and ratio2 for |eta_x/y|.
The longitudinal source coefficient is
(1+ratio1)*w2*(1+r)/sqrt(2), with ratio1 for |eta_z|. The additional
factor 1+r comes from multiplying the rough source by 1/(2a) before the
antiderivative. Omitting this multiplier derivative is not justified.

Combining these source bounds with the actual all-root Rvel_i coefficients,
the new weak Green bound and the already bounded T_i gives

    ||f||H1 <20.905620 Dminus,
    ||p_x||L2 <2.829676 Dminus,
    ||p_y||L2 <2.829873 Dminus,
    ||p_z||L2 <21.884608 Dminus,
    ||f||H1+sum_i||p_i||L2 <48.449775 Dminus.

These are conservative normalized coordinate/source bounds. Physical scalar
density retains delta I_density=N*sqrt(h)*delta rho+
I_density*delta log(N*sqrt(h)); it is not replaced by r_source.

All source formulas are continuous extensions of the smooth ones. The full
longitudinal equation is solved only on

    mean(s_x)=mean(s_y)=0,
    mean(R*f+s_z/(2a))=0,
    R=a*(lambda_z*P_b-P_b,z)/2.

The last mean is the dual pairing of an H^-1 source with a smooth weight,
so it is defined in this rough-source domain. It is not automatic after
the projected solve. For example f=0 and s_z=2a violate it with value one.
Global I/Q tangents remain independent restrictions. No parity condition
or physical clock quotient is adopted. Harmonic means are explicitly in
Dminus and in the reconstructed solution.

## Actual auxiliary derivative count

Use the earlier verified six-entry first variation with k=delta h,
chi=delta psi, mu=sqrt(det h), H=h^-1, c=mu Hzz:

    delta Z=-(H:k/2)*Z-mu^-1 D_z[c*chi_z+(D:k)*psi_z],
    D=mu*(-H[:,z]*H[z,:]+Hzz*H/2).

At the actual initial conformal metric,

    mu^-1<=exp(3r), c<=exp(r), |c_z|<=r*exp(r),
    ||H/2||F<=sqrt(3)*exp(2r)/2=E0,
    ||D||F<=sqrt(3)*exp(r)/2=D0, ||D_z||F<=r*D0,
    |Z|<=exp(2r)*(psi_zz_max+r*psi_z_max)=Z0.

Apply the ordinary product rule before taking L2 norms. With
psi_zz_max=(1/1000)(1/29+4/31), the separate metric coefficients are

    Ck0=E0*Z0+exp(3r)*D0*(r*psi_z_max+psi_zz_max),
    Ck1=exp(3r)*D0*psi_z_max.

Since ||chi_z||L2<=||chi||H2/2 and ||chi_zz||L2<=||chi||H2,

    ||delta Z||L2
      <=exp(4r)*(1+r/2)*||chi||H2+(Ck0+Ck1)*||k||H1,F
      <1.000347*||chi||H2+0.000369079*||k||H1,F.

No metric derivative above one is needed for this initial observable.
This does not by itself bound a force gradient, every stress component or
the time derivative in the same strong norm. The previous corrected
canonical/gauge estimate gives the distinct initial rate control

    ||delta Z_t||H^-2
      <24.084505*P0+64.463524*QH1+0.000554257*Hc,

where P0 is the full nonauxiliary canonical L2 momentum norm, QH1 the
full canonical H1 configuration norm in the original coordinate and Hc
the retained harmonic coordinate velocity. Using H1 for every coordinate
is a sufficient control topology here, not a choice of physical energy.
The independent force H2 requirement is stronger for the force coordinate.

## Symplectic implications and the remaining obstacle

The physical density/trace pairing still comes from f=G*r+other sources
and Omega contains mean(a^2 f wedge P), the momentum/momentum cross
terms and every modulus/conjugate pair. The new bounded reconstruction
makes this initial pairing continuous for r in H^-1 and canonical P in L2.
It does not make the order-minus-two density block K=G^*M_a^2 a strong
symplectic inverse on a flat L2 product. No cross block has been discarded
and no arbitrary positive weight has been introduced.

This result controls assembled sources. Quantitative assembly constants
from all genuinely free physical data, the transported constraint domain,
compatible generator and its norm estimate are still incomplete. It does
not show that arbitrary independent H1/L2 coordinates satisfy the density,
range and charge graph. In particular the density and frame-momentum
derivative can cancel as distributions; treating each as separately L2
would impose an additional, unproved regularity restriction.

NEXT: assemble the free-data graph and time-dependent range in the same
mixed topology, retaining physical clock flow, chart/gauge drift,
G_dot=-G*L_dot*G and the actual quartic/zero-speed/subleading couplings.
Initial bounds do not furnish a background tube or a [0,.05] theorem.
The zero-speed Jordan warning and indefinite principal gradient energy
remain substantive. No physical stability conclusion follows from these
new kinematic estimates.

## Verification, preservation and programme disposition

[Executable](../../../Analysis/MasterTests/test_rtau_weak_graph_v1.py):
19/19 exact/interval controls; fresh receipt and byte-identical read-only
replay completed with exit zero.
[Receipt](../../../Analysis/MasterTests/outputs/rtau_weak_graph_v1_20261103/receipt.json)
SHA256 f3e66a8ed8ef12ca69cff37c0d13df95f2c330e59381a35e07592088c636fbee.

The controls verify the continuum reference inequalities for every integer
mode, the exact weak leading-coefficient identity, the integrating factor
and rough-source scaling. A separate exact periodic probe rejects omission
of A2' with normalized defect 1/40. The reference Fourier sequence with
s_n=i*n*exp(i*n*z) has bounded H^-1 source and H1 trace but unbounded
H2 trace, so a stronger uniform derivative claim cannot be substituted.
This is a reference-principal regularity control, not a new physical
mode family or a proof of failure on the actual varying background.
The full six-entry auxiliary expansion agrees with the earlier independently
differentiated exact formula. Same-author checks are not external review.

All 219 inherited input hashes match. Source and existing sidecar bytes
and timestamps were unchanged before/after each run. New source/specification
pins and receipt sidecar were added; old sources, failed attempts and their
sidecars were not rewritten. No new failed attempt occurred in this step.
The unrelated Manuscript/references.bib edit remains untouched.

No new microscopic matching relation or concrete defect in P1/P2,
Thermodynamics or original R4C1 is established here. No paper/site update
is warranted by this component. G1-G6 and the whole observable-norm bundle
remain incomplete; Stage 3 is not entered. Goal ACTIVE. No new action,
external dispatch, vault mutation, commit, push, deployment or publication.
