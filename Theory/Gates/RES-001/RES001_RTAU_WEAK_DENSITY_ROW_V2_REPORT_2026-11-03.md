# R-tau initial weak current-density and physical-density time rows

3 November 2026. Conditional component of the confirmed-High observable-
norm bundle. R-tau unadopted; original R4C1 unchanged. Review DEFERRED;
physics_pass=false; gate_effect=NONE; G1-G6 incomplete.

## Result and scope

The initial forward density/gauge calculation now includes the action
current density I AND physical density rho=I/(N*sqrt(h)). Their static
variations are bounded in H^-1 and their time variations in H^-2 on the
registered compatible initial graph. The periodic gauge correction and
background coordinate drift are included. All metric/lapse measure terms
are retained; current density is not silently identified with rho.

The proof is for the registered PLANAR periodic perturbations, with all
six metric components and independent frame/matter fields retained. Its
one-dimensional Sobolev product argument does not extend automatically
to unrestricted three-dimensional perturbations. The result is an initial
weak forward rate map, not a physical energy estimate, bounded propagator,
strong density evolution theorem or controlled time interval.

Owners: [whole bundle](RES001_RTAU_COUPLED_OBSERVABLE_NORM_V1_CONTRACT_2026-11-02.md),
[gauge composition](RES001_RTAU_INITIAL_GAUGE_COMPOSITION_V2_REPORT_2026-11-03.md),
[weak canonical rows](RES001_RTAU_WEAK_CANONICAL_RATE_V2_REPORT_2026-11-03.md)
and [exact direct-density/current Ward identity](RES001_R4C1_RTAU_DENSITY_TIME_TRANSPORT_V1_REPORT_2026-11-01.md).
The [V1 contract](RES001_RTAU_WEAK_DENSITY_ROW_V1_SPEC_2026-11-03.md) and
[V2 dispatch correction](RES001_RTAU_WEAK_DENSITY_ROW_V2_SPEC_2026-11-03.md)
were frozen before their executions.

## Action current and weak derivative count

Use the owning current exactly:

    F=b*N^2*sqrt(h)*[Z*kappa*p_z+Z*T*psi_z-p*kappa*Z_z],
    kappa=h^{zz}, p=(psi_t-S^z*psi_z)/N,
    K=(h_t-Lie_S h)/(2N), T=tr(K)*kappa-2*K^{zz}.

The full first variation retains delta A,delta kappa,delta T,delta p,
delta Z and the force-field gradient, where A=b*N^2*sqrt(h). In particular

    delta A=A*(-2*beta*delta psi+tr(h^-1*delta h)/2),
    delta p=(delta psi_t-delta S^z*psi_z-S^z*delta psi_z)/N
                                                   +beta*p*delta psi,
    delta K=(delta h_t-Lie_S delta h-Lie_deltaS h)/(2N)
                                                   +beta*delta psi*K.

delta T includes both inverse metrics and the trace variation, so
off-diagonal metric/velocity and transverse shift variations are not
removed. The independent exact test differentiates the original current
with respect to all six metric entries, their velocities and nonzero
shift/force perturbations, then compares with this expanded variation.

All undifferentiated factors are controlled in L2 by the previously
bounded canonical rates and auxiliary observable. The only rough
derivatives are D_z(delta p) and D_z(delta Z). Multiplication by their
smooth background coefficients is handled with

    g*D_z f=D_z(g*f)-g_z*f,
    ||g*D_z f||H^-1 <= (||g||infinity+||g_z||infinity)*||f||L2.

The actual initial coefficients use the complete shift/root ball,
prepared metric and scalar profiles. No delta Z_t, unprovided scalar-rate
spatial jet or third shift-root derivative is required by this flux bound.

## Static density and its time row

On the auxiliary secondary surface the same improved density is

    I=L_nonreg-p_i*(q_t^i-Lie_S q^i)-D_z B0-b*N*sqrt(h)*Z^2/2,
    B0=N*gamma*h^{iz}*p_Vi-N*curvature_flux/2.

Legendre cancellation removes the unknown delta q_t and shift variation
from the static canonical first variation. The remaining local energy
variation is L2, delta B0 is L2, and the regulator-energy variation is
L2 when the force field is H2 and the metric H1. Thus delta I is H^-1.
The curvature/lapse improvement and negative regulator contribution to
this density are retained. This is not a new physical ghost diagnosis.

The exact current identity is

    I_t-D_z(S^z*I+F)=D_z(N^2*h^{iz}*C_i),
    delta defect=D_z[N^2*h^{iz}*delta C_i+delta(N^2*h^{iz})*C_i].

On the EXACT constrained background and admitted tangent the defect
vanishes. At a finite numerical centre it does not vanish by assumption;
the prior independent 23-control Ward audit and its nonzero centre/probe
defects remain authoritative and unchanged. This report does not repeat
those controls or relabel their residuals zero.

Consequently delta F in H^-1 and delta I in H^-1 give delta I_t in
H^-2, with I*delta S retained. Subtract D_z(w*delta I) and divide by J
for the adapted current-density rate. The scalar-density dual pullback
from the preceding gauge calculation supplies its H^-2 bound.

The actual background I is evaluated from the frozen action, including
all improvements. Conservative initial bounds include

    ||I||infinity <0.265915877,
    ||F||infinity <0.000026628150,
    ||I_t||H^-1 <= ||S^z||infinity*||I||infinity+||F||infinity
                     <0.000571384776,
    ||rho||infinity <0.265984350.

The weak time bound uses the exact constrained Ward identity; it is not
an assertion that all unconstrained points in an interval box solve it.
No reference density or observed target was substituted.

## Physical density and the measure terms

Put M=N*sqrt(h), ell=delta log M and alpha=M_t/M. Retain the full quotient:

    delta rho=M^-1*delta I-rho*ell,
    delta rho_t=M^-1*delta I_t-M^-1*I_t*ell
                                           -alpha*delta rho-rho*delta alpha.

At the initial conformal background, with L=a_t/a,

    ell=tr(h^-1*delta h)/2-beta*delta psi,
    alpha=3L-beta*psi_t,
    delta alpha=tr(h^-1*delta h_t)/2
                          -L*tr(h^-1*delta h)-beta*delta psi_t.

The last equation is only the actual initial first jet, not a future
conformal ansatz. Its metric and scalar velocities are those of the
corrected canonical map.

The product I_t*ell must not demand an unprovided pointwise I_t bound.
On the normalized periodic circle, Cauchy-Schwarz in Fourier space gives
||f||infinity<=sqrt(5)||f||H1: the reciprocal weight sum is bounded by
1+2*sum_(n>=1)n^-2<=5, using the telescoping tail bound
1/n^2<=1/[n(n-1)] for n>=2. The product rule then gives the sufficient
algebra constant

    ||f*g||H1 <=3*sqrt(5)*||f||H1*||g||H1.

By duality this controls H1 times H^-1 into H^-1. Thus I_t in H^-1 and
ell in H1 suffice. This avoids assuming an unavailable pointwise I_z/I_t
or a third spatial derivative of the C2-certified shift root. All remaining
measure multipliers have explicit W1/W2 bounds from the prescribed
lambda and psi profiles.

Physical rho is a scalar field, whereas I is a scalar density. Their
pullbacks therefore use different dual test weights, J and one. For
rho_t also retain -w*delta rho_z. The needed w_zz estimate follows from
the actual initial gauge identity

    w_z=L-mean_rate-lambda_z*w,
    w_zz=L_z-lambda_zz*w-lambda_z*w_z,
    ||w_zz||infinity <0.000064536687.

No extra root jet is inferred. The scalar H^-2 pullback and this drift
give the physical-density rate below.

## Explicit compatible-input estimates

Inputs are the same Dminus,Qfree,Pfree,F2,Hharm as the gauge-composition
owner. Dminus is the ASSEMBLED H^-1 source norm with its weighted range,
means, retained momentum means and separate global I/Q conditions. It
is not just rho. Inputs use the original coordinate; density outputs use
the adapted coordinate, except the flux row labelled original.

Each output norm is at most the sum of the five controls times the
following conservative upward-rounded constants:

| Output | Dminus | Qfree | Pfree | F2 | Hharm |
| --- | ---: | ---: | ---: | ---: | ---: |
| current density H^-1 | 200.953460 | 3.646286 | 4.185541 | 0.000074401960 | 0 |
| current-density rate H^-2 | 1815.617109 | 47.323291 | 18.702010 | 0.091180329 | 0.274606513 |
| physical density H^-1 | 213.895467 | 4.081510 | 4.188717 | 0.000074458419 | 0 |
| physical-density rate H^-2 | 74628.026997 | 1941.635105 | 773.385723 | 0.091506254 | 11.056891117 |
| original current flux H^-1 | 56.863153 | 1.482452 | 0.585279 | 0.091139884 | 0.008488279 |

The large composed estimates are not a time-growth inequality, fit
result, numerical error bar or physical cutoff. They control only the
stated initial maps into weaker spaces. Local I/Q conservation and the
physical clock flow are retained; no charge-level time quotient or
physical density fixation is introduced.

## Verification and preservation

[Executable V2](../../../Analysis/MasterTests/test_rtau_weak_density_row_v2.py):
13/13 controls, exact read-only replay COMPLETE. Fresh
[receipt](../../../Analysis/MasterTests/outputs/rtau_weak_density_row_v2_20261103/receipt.json)
SHA256 d3d2146f33b8a744aaf4b02b673f2f27b13592f7b371ea82670165c80d454e63.
All 219 inherited source hashes, original sidecar bytes and input timestamps
were preserved. Exact controls cover the full-metric current variation,
weak products, time quotient, Sobolev tail bound and gauge-drift derivative.
They reject omitted measure variation and auxiliary-gradient flux.
Same-author controls are not independent scientific review.

V1's [source](../../../Analysis/MasterTests/test_rtau_weak_density_row_v1.py),
specification, sidecars and
[failure](../../../Analysis/MasterTests/outputs/rtau_weak_density_row_v1_20261103/failure.json)
are unchanged. It failed on interval-left multiplication of a Taylor jet.
V2 changes that scalar multiplication order only, with added provenance
pins. No equation, domain, coefficient, threshold or rejection is relaxed.

## Scientific boundary and next calculation

The initial forward canonical/gauge/current/physical-density rows are
now controlled in their stated weak spaces. The evolving inverse,
strong physical norm, density L2 propagation, coupled background tube
and finite-time estimate remain unproved. No strong symplectic inverse
of the order-minus-two density block is assumed. The initial forward
current identity incorporates density-map drift; it does not justify
omitting inverse-map drift in the later physical energy calculation.

The next useful test is the action-derived kinetic/regulator contribution
to a compensated density observable. Derive its exact normalization from
the SAME action, then test whether its time variation cancels the highest
quartic-density terms. This is a calculation to perform, not an adopted
new density law or a claimed cancellation. Retain metric/frame stress,
zero-speed and quartic branches and all lower-order coupling. A useful
energy must close the actual coupled estimate, not merely change its labels.

No new microscopic matching relation or concrete manuscript defect arose.
No numerical acceleration prediction or publication/site change follows.
Goal ACTIVE; whole bundle and original G1-G6 incomplete; review DEFERRED.
No action adoption, vault sync/mutation, external dispatch, publication,
commit, push or deployment.
