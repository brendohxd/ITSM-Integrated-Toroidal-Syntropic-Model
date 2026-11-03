# R-tau weighted-range drift and weak constraint transport

3 November 2026. Confirmed-High observable-norm bundle, still incomplete.
R-tau remains an unadopted comparator; original R4C1 unchanged. Review
DEFERRED; physics_pass=false; gate_effect=NONE; G1-G6 incomplete.

## Result and exact scope

The weighted longitudinal compatibility condition now has an explicit
initial time-variation bound that retains the moving metric weight and
canonical momentum rate. Its coefficient functional can be controlled
without inventing an unavailable spatial derivative of that momentum rate.
The three-component spatial constraint's Ward transport also has a
conditional H^-1 norm estimate with the full covector-density index terms.

These are necessary pieces of moving-domain control. They do not prove a
coupled solution exists, reconstruct the full source-rate map, establish
that physical perturbations stay bounded, or provide an actual time tube.
The numerical coefficients below are INITIAL values, not time-uniform ones.

Owners: [bundle contract](RES001_RTAU_COUPLED_OBSERVABLE_NORM_V1_CONTRACT_2026-11-02.md),
[initial weak graph](RES001_RTAU_WEAK_GRAPH_V1_REPORT_2026-11-03.md),
[coupled inverse](RES001_R4C1_RTAU_COUPLED_PERIODIC_INVERSE_V1_REPORT_2026-11-01.md)
and [full constraint Ward identity](RES001_R4C1_RTAU_CURRENT_TRANSPORT_V2_REPORT_2026-11-01.md).
The [specific contract](RES001_RTAU_MOVING_RANGE_V1_SPEC_2026-11-03.md) was
frozen before execution. Bessel norms and normalized periodic averages
are those of the weak-graph report.

## Initial moving compatibility functional

At the prepared conformal initial slice let

    a=exp(lambda), L=a_t/a, P=p_hxx+p_hyy,
    R=(a_z*P-a*P_z)/2,
    c=mean(R*f+s/(2a)).

s denotes the longitudinal momentum SOURCE, not a shift component.
c=0 is the retained range condition. Differentiation gives

    c_t=mean(R*f_t)+<R_t,f>
                       +<s_t,1/(2a)>-<s,L/(2a)>.

The brackets allow distributional sources. The last term is required;
the metric weight is evolving. For the coefficient functional, periodic
integration by parts gives the exact identity

    <R_t,f>=mean[(a_t*P+a*P_t)*(lambda_z*f+f_z/2)
                                      +a*P*L_z*f].

The strong formula would contain P_t,z. The displayed weak formula only
needs P_t in L2 against f in H1. The two integrands differ by
-D_z[(a_t*P+a*P_t)*f]/2, whose periodic average vanishes. No uncomputed
momentum jet is set to zero.

This is the actual background FIRST JET at the initial slice. The
prescribed initial metric rate is h_t=2Lh, which justifies the time
derivative there. It does not impose a future conformal metric. All
free-field, harmonic, gauge and chart changes belong in the true source
rate s_t and trace-coordinate rate f_t; they have not been replaced by
arbitrary independent rates or solved by setting c_t to a desired value.

## Action-derived initial momentum-rate coefficient

The preserved full mixed-action export has affine Euler forcing

    F_i=L_qi-D_z L_di-sum_j(L_vi,qj*v_j+L_vi,dj*v_j,z).

Thus the canonical Euler rate itself is

    (p_i)_t=F_i+sum_j(L_vi,qj*v_j+L_vi,dj*v_j,z).

The sum retains every one of the thirteen nonauxiliary fields. The
exported exact zero pattern is checked before excluding the unavailable
auxiliary rate. No shift-rate prescription is required: the shift-rate
terms cancel between the Euler acceleration equation and the time
derivative of canonical momentum. Actual lapse, shift and scalar/frame
effects remain in F, the Hessian and the prepared rates.

Reusing the whole-circle/root-ball intervals gives

    ||P_t||L2 <0.662360,
    ||P||infinity <1.932337,
    ||R||infinity <0.007314224.

Direct raw action Euler evaluations at z=0.3,1.1,2.4 are independently
enclosed by the reconstructed P_t bound. They are controls of the bound,
not a three-point proof of its uniformity; that proof uses the exported
whole-circle intervals and exact identities above.

Let r=1/13000, M bound |L|, B=2/(31000) bound |L_z|. The weak coefficient
estimate is

    ||R_t||H^-1
      <=exp(r)*[(M*P_bound+Pt_bound)*(r+1/2)+P_bound*B]
      <1.168826.

This expression uses Cauchy-Schwarz and the actual prepared initial
profiles. For the two source weights, H1 product bounds give

    ||1/(2a)||H1 <=exp(r)*(1+r)/2 <0.500076928,
    ||L/(2a)||H1 <=exp(r)*[(1+r)*M+B]/2 <0.433383316.

Consequently this sufficient first-jet domain obeys

    |c_t| <=0.007314224*||f_t||L2+1.168826*||f||H1
              +0.500076928*||s_t||H^-1+0.433383316*||s||H^-1.

This does NOT establish that the actual coupled source rate is H^-1.
That regularity must follow from the assembled evolution, or the dual
weight estimate must be extended to its actual weaker domain. In
particular derivatives of canonical force distributions cannot be
declared H^-1 merely because the initial source was in that space.
The present bound must not become an unproved physical restriction.

## Full covector-density constraint estimate

Write the three constraint residuals as vector C. On a sufficiently
regular exact Euler/auxiliary solution, the previously derived Ward
identity is

    C_t=Lie_S C,
    (Lie_S C)_i=S^z*C_i,z+S^z_z*C_i+delta_iz*sum_j S^j_z*C_j.

On the exact constrained background the linearized equation is
delta C_t=Lie_S delta C. At a finite numerical centre there is also
Lie_deltaS C; that inhomogeneous term is not dropped in interpretation.

For a periodic H1 test vector phi, put u=S^z and b=partial_z S. The
adjoint of the complete Lie operator is

    A*phi=-u*phi_z+b*phi^z.

The extra vector term comes from the covector index, rather than scalar
density transport. With E=||phi||L2^2+||phi_z||L2^2, periodic integration
by parts gives the exact quadratic identity

    (1/2)E_t=mean[u_z*(|phi|^2-|phi_z|^2)/2
            +(phi.b)*phi^z+(phi_z.b)*phi_z^z+(phi_z.b_z)*phi^z].

Therefore the norm growth coefficient is bounded by

    gamma=(1/2)||S^z_z||infinity
                +||partial_z S||infinity,2
                +(1/2)||partial_z^2 S||infinity,2.

Here infinity,2 denotes the spatial supremum of the Euclidean vector
norm, conservatively bounded by component suprema. The same absolute
bound applies to the backward adjoint. Duality then gives the conditional
residual estimate

    ||C(t)||H^-1 <=exp(integral_0^t gamma(s) ds)*||C(0)||H^-1.

For an existing regular exact background this propagates zero residual
and bounds small homogeneous residuals. It is a constraint estimate,
not a positive physical perturbation energy. The certified initial shift
ball supplies

    ||partial_z S||infinity,2 <0.003413318,
    ||partial_z^2 S||infinity,2 <0.006250967,
    gamma(0)<0.008245441.

No third shift derivative is required here. A future time integral is
not evaluated with gamma(0): no actual coupled background tube has yet
been established. General harmonic shift transport is retained by the
formula; a constant advection does not contribute to this norm bound.

## Verification and remaining work

[Versioned executable](../../../Analysis/MasterTests/test_rtau_moving_range_v1.py):
17/17 exact/interval/direct-action controls. Fresh
[receipt](../../../Analysis/MasterTests/outputs/rtau_moving_range_v1_20261103/receipt.json)
SHA256 219f4d9dcc83348150f7d9f42c129b19f41b43adf5ee85d134c4d7f0fe3072aa.
Read-only replay recalculated the point controls and returned byte-identical
receipt bytes. All 219 inherited source hashes, original sidecars and
input timestamps were preserved. No new failed attempt occurred.

Exact controls reject freezing the time weight on a positive nonconstant
periodic profile, with defect -1/2 in the stated fixture. They verify
the full dual Lie identity and energy identity; a transverse-shift probe
produces a nonzero longitudinal residual from the index term. Same-author
checks are not independent peer review or a replacement for the continuum
arguments and their hypotheses.

The deciding next work is the full FREE-DATA SOURCE/RATE assembly in the
actual mixed topology, and the compatible generator with moving gauge,
Green inverse, source range and symplectic form. The source-rate regularity
issue above must be resolved rather than assumed. Retain the physical
clock flow, both charges, mean/modulus partners, quartic force branch,
zero-speed sector and subleading mixing. A conditional Ward estimate
cannot supply the missing full physical norm or coupled background tube.

No [0,.05] theorem, interaction window, microscopic match or theory-fixed
acceleration follows. No concrete P1/P2/Thermodynamics/original-R4C1 defect
or new matching relation is found here. No paper/site update is warranted.
Goal ACTIVE; whole bundle and G1-G6 incomplete. No action adoption,
dispatch, vault mutation, publication, commit, push or deployment.
