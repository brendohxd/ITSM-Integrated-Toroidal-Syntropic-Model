# Initial compensated-scalar trace and momentum reconstruction

3 November 2026. Conditional planar initial-domain result. R-tau remains
an unadopted comparator; unchanged R4C1 and its earlier failures are preserved.
Review DEFERRED; physics_pass=false; gate_effect=NONE; G1-G6 incomplete.

## Result and coverage

The projected initial trace operator in physical compensated-scalar Sigma
coordinates has a bounded inverse throughout the registered certified root
ball. Its outward contraction bounds are below 0.357287 in L2->H2 and
0.370458 in H^-1->H1. Corresponding assembled-right-side inverse norms are
below 2.639787 and 2.695016. These estimates retain the coupled longitudinal
momentum completion and the physical-volume variation.

This resolves the specific question whether the compensated trace operator
can be inverted initially. It does not prove that arbitrary prescribed
sources meet the full momentum/charge range conditions. It also does not
provide the complete free-data-to-physical-state norm equivalence, a positive
physical energy, an evolving Green inverse or an actual background interval.
Those remain necessary for a physical evolution theorem.

Owners: [frozen contract](RES001_RTAU_COMPENSATED_STATIC_INVERSE_V1_SPEC_2026-11-03.md),
[compensated identity](RES001_RTAU_COMPENSATED_DENSITY_V1_REPORT_2026-11-03.md),
[complete initial rate](RES001_RTAU_COMPENSATED_RATE_V1_REPORT_2026-11-03.md),
and [original coupled inverse](RES001_R4C1_RTAU_COUPLED_PERIODIC_INVERSE_V1_REPORT_2026-11-01.md).
The unchanged [observable-norm bundle](RES001_RTAU_COUPLED_OBSERVABLE_NORM_V1_CONTRACT_2026-11-02.md)
remains incomplete.

## Canonical force-energy differential

Let M=N*mu, mu=sqrt(h), p=(psi_t-S^z*psi_z)/N, s=psi_z,
pi_psi=mu*f_p, and e=p*f_p-f. The full frame-dependent force f retains
its nonzero norm-cubed term. Taking its canonical differential gives

    delta e=(p/mu)*delta pi_psi-p*f_p*delta mu/mu
              -sum_q f_q*delta q-f_s*delta s,

    delta(M*e)=M*(e*delta N/N-f*delta mu/mu
                 -sum_q f_q*delta q-f_s*delta s)
                 +N*p*delta pi_psi.

The q partials in these formulas hold normal p and s fixed; q includes
the independent metric and plenum frame. Normal p itself is not held fixed
in the canonical differential. The cancellation follows from differentiating
pi_psi=mu*f_p and e, and is checked with an explicit nonquadratic,
frame-dependent force. The existing temporal inverse supplies the actual
prepared canonical chart. No new microscopic matching coefficient is inferred.

The defining scalar is

    Sigma=I/M+e+b*Z^2/2,

where I is the original improved canonical current density and Z=-Delta_h psi.
Thus scalar-volume variation is necessary even after forming the compensated
densitized combination. The compensated scalar is not a new conserved charge.

## Derive the actual trace operator

At the initial conformal metric h=a^2*I3, take the trace unknown u with

    delta hxx=delta hyy=a^2*u,

and retain the original h_xz,h_yz,h_zz unknown canonical momentum components
px,py,pz. Other fields, momenta, moduli and harmonic components are free
source data. This describes initial reconstruction; it imposes no conformal
future evolution. The secondary variation is exactly

    delta mu/mu=u, delta kappa=0, delta Z=-kappa*s*u_z,

where kappa=h^{zz}. For example, writing c=mu*kappa gives
delta Z=-u*Z-mu^-1*D_z(c*s*u)=-kappa*s*u_z.
This gradient term must be retained.

Let B2,B1,B0 be the exact old same-action current-density trace coefficients,
and RVi=q_t^i-Lie_S q^i. The compensated scalar row is

    C2*u_zz+C1*u_z+C0*u-sum_i Wi*pi_i=assembled_source,

    C2=B2/M=-a^-2,
    C1=B1/M-b*Z*kappa*s,
    C0=B0/M-f-a^2*(f_hxx+f_hyy)+b*Z^2/2-Sigma,
    Wi=RVi/M, i=(hxz,hyz,hzz).

These coefficients follow from the canonical differential above, the
secondary variation and the physical volume M. The executable reuses only
the preserved action-based construction of B2,B1,B0, rather than rerunning
its old experiment or inserting coefficients into a homogeneous matrix.
Background Sigma is independently evaluated from its other-action definition
including the full improvement. Direct full-action temporal inversion and
other-action differentiation check each of u,u_z,u_zz at three nonzero
profile locations, with nonzero unknown metric momenta and their completed
momentum slopes. All full raw current/momentum controls also pass there.

## Reference and continuum perturbation proof

The operator reference is derived from the same declared Hamiltonian and
canonical ensemble. At a=1,N=1, the force kinetic energy contribution is
K_Q/50; it scales as inverse volume at fixed pi_psi. Dividing the compensated
densitized expression by the varied volume yields

    Sigma_ref=13/50,
    Lref=-D_z^2+(17/16)*P0-(4951/8400)*mean,

with P0=1-mean. The zero-mode coefficient remains negative and nonzero;
it is not replaced by the positive nonzero-mode coefficient. Its sign in
this static constraint operator is not a kinetic-sign or ghost verdict.
Omitting the scalar-volume variation changes both reference masses by
13/50, and is explicitly rejected. Omitting longitudinal momentum completion
also changes the operator and is rejected.

For every nonzero Fourier mode n, (1+n^2)/(n^2+17/16)<1. The mean inverse
has magnitude R0=8400/4951>1. Therefore R0 bounds both reference inverse
norms L2->H2 and H^-1->H1 on the entire periodic circle, without imposing
a Fourier cutoff or parity restriction.

The old exact momentum completion is unchanged. Use its trace operators
Tx,Ty,Tz, bounds tx,ty and longitudinal difference E_T, with

    Tz_ref*u=pi_ref*P0*u,
    pi_ref=-(11/10)*sqrt(3469/4620), Wz_ref=2*sqrt(3469/4620).

Define d2=||C2+1||infinity, d1=||C1||infinity,
d0=||C0+4951/8400||infinity. A bound for the nonlocal difference is

    E_nonlocal=||Wx||infinity*tx+||Wy||infinity*ty
       +||Wz||infinity*E_T+||Wz-Wz_ref||infinity*abs(pi_ref).

All coefficients are evaluated over the entire certified initial root
enclosure. The strong perturbation bound is

    E_strong=d2+d1/2+d0+E_nonlocal.

Here ||D_z u||L2<=||u||H2/2. For the weak estimate, integrate the variable
leading coefficient by parts. Its derivative satisfies

    ||C2_z||infinity<=2*r*exp(2*r), r=1/13000.

Thus

    E_weak=d2+d1+d0+E_nonlocal+2*r*exp(2*r).

The last term must not be omitted. It needs only the known conformal-profile
derivative, not a third derivative of the shift root. The Neumann estimates
R0*E_strong<0.357287 and R0*E_weak<0.370458 are strict. Consequently

    ||u||H2<=2.639787*||assembled_source||L2,
    ||u||H1<=2.695016*||assembled_source||H^-1.

The assembled source includes the completed momentum-source contributions
with the actual Wi coefficients. These are assembled-source constants;
they must not be advertised as bounds for arbitrary unassembled free data
or as time-evolution growth rates.

## Full range and conserved ensemble remain necessary

Transverse momentum sources require their existing zero means, while all
three retained momentum means remain physical data. The longitudinal
condition remains

    mean(R*u+s_z/(2*a))=0,
    R=a*(lambda_z*P-P_z)/2, P=p_hxx+p_hyy.

The projected trace inverse does not impose this condition. The fixed-I
condition is also retained in its actual form

    integral delta I=0,
    delta I=M*delta Sigma+Sigma*delta M
                -delta(M*e)-delta(M*b*Z^2/2).

It is not replaced by integral delta Sigma=0. Original phase-charge
conditions, spatial moduli, harmonic data and cross terms remain present.
No mode is deleted to make these estimates work.

## Evidence, preservation and next work

[Executable](../../../Analysis/MasterTests/test_rtau_compensated_static_inverse_v1.py):
35/35 checks passed, no failed/unknown controls. Fresh
[receipt](../../../Analysis/MasterTests/outputs/rtau_compensated_static_inverse_v1_20261103/receipt.json)
SHA256 9f07bf684f644f70d16bfb299f8e7c5f2b13e3017ff91b51af24cd012fc0598d.
Read-only recomputation matched the receipt byte for byte, with all 35
controls again passing. The continuum proof is the operator estimate above;
agreement at the point controls alone
would be insufficient. Controls are same-author, not independent review.
All 219 inherited source hashes and snapshotted source/sidecar bytes and
timestamps were preserved. Earlier failures remain intact.

NEXT: quantify the complete compensated free-source map and its physical
norm equivalence, then test the action-based coupled kinetic/symplectic
energy including zero-speed and quartic modes. Retain coordinate/gauge
drift, evolving Green terms and the actual coupled background domain.
The new static inverse does not by itself close any of those requirements.
The nonlinear validity window, GR/local compatibility and identifying
matching remain incomplete. No C_chi or a0 prediction follows.

No concrete defect in existing P1/P2/Thermodynamics/original-R4C1 manuscripts
is established here. No paper/site promotion, action adoption, vault mutation,
external review dispatch, publication, commit/push or deployment is included.
Goal ACTIVE.
