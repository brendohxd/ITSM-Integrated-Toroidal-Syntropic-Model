# Complete initial strong-density L2 transport/source estimate

4 November 2026. Conditional initial planar density-sector result.
R-tau remains an unadopted comparator; original R4C1 unchanged.
Review DEFERRED; physics_pass=false; gate_effect=NONE; G1-G6 incomplete.
Goal ACTIVE; full coupled physical energy and actual time tube remain open.

## Result

The COMPLETE corrected-density row now has an initial L2 source and
logarithmic-norm estimate on the exact compatible prepared domain. Density
L2, canonical momentum L2, ordinary configuration H1 and force H2 orders
are retained. The calculation includes the full force/current/regulator
remainders, all weighted mean/primitive terms, both coefficient time jets,
actual gauge-velocity closure and scalar coordinate transport.

This is stronger than the earlier H^-1 density-sector component. It does
not promote the rejected density-only weak mixed norm. It is still only
the density sector: no positive full field/zero-speed/quartic energy,
moving symplectic/Green estimate or controlled interval follows from it.

Owners: [contract](RES001_RTAU_STRONG_DENSITY_L2_SOURCE_V1_CONTRACT_2026-11-04.md),
[execution criteria](RES001_RTAU_STRONG_DENSITY_L2_SOURCE_V1_EXECUTION_SPEC_2026-11-04.md),
[local lapse identity](RES001_RTAU_OTHER_SECTOR_LAPSE_IDENTITY_V1_REPORT_2026-11-03.md),
[first normal form](RES001_RTAU_STRONG_DENSITY_NORMAL_FORM_V1_REPORT_2026-11-03.md),
and [second normal form](RES001_RTAU_STRONG_DENSITY_NORMAL_FORM_V2_REPORT_2026-11-03.md).

## Complete row and input space

Use the established original-coordinate normal form

    w=delta Sigma-c*P(xi)-alpha*chi_z,
    xi=delta pi_psi, chi=delta psi, P=Dinv*P0,
    c=T*psi_z/(mu*kappa), alpha=-(p*f_ps+f_s).

The primitive has zero mean; xi's mean is retained, not fixed to zero.
The canonical mean is not substituted for global clock charge I. Let
zeta=delta Z, s=psi_z, M=N*mu, d=b*M*kappa, r=beta*d*s and C=-N*trK.
The exact reorganized current and local source are

    J=S*pi_psi-M*f_s+d*Z_z-2*beta*d*Z*s,
    R=beta*M*(p*f_p-f-Sigma)-beta*L_reg.

Define J0=delta J-S*xi-d*zeta_z and R0=delta R-r*zeta_z. The full two-step
row, with the identified fast derivatives cancelled, is

    w_t-S*w_z=C*w+K_alpha*chi_z+K_c*P(xi)+F0
      +c*[mean(S*xi)-S*mean(xi)]-c*mean(d_z*zeta)
      -c*P0(J0)-c*P0(r*zeta)+c*P(r_z*zeta)-c*P(R0)
      -alpha*N_z*delta p-alpha*D_z Gchi,

    K_alpha=C*alpha-alpha_t+S*alpha_z-alpha*S_z,
    K_c=C*c-c_t+S*c_z,
    Gchi=-beta*N*p*chi+s*delta S.

F0 contains the complete remaining density variation after separating
C*delta Sigma, a*zeta_z and N*alpha*delta p_z. In particular it retains
Sigma_bg*delta C, delta S*Sigma_bg,z, all force/frame work, coefficient
variations against background Z_z and p_z, and the local regulator terms.
The exact constrained background/tangent condition still controls the
Ward defect; no numerical centre is declared exactly constrained.

Norms below are normalized periodic Sobolev norms in the declared control
units. Write Q=||delta q_13||H1, Pcan=||delta p_13||L2, F=||chi||H2 and
U=||delta S||H1. These are the full original-coordinate canonical vectors,
not truncated modes. They include retained physical means and the allowed
metric/frame/matter/clock data on the original compatible range.

## Bound every local and nonlocal source

The actual full frame-dependent force is used. Its explicit f_s expression
and Hessian supply the necessary third force partials on the certified
positive Y patch. They are checked independently against symbolic third
derivatives at a rational tilted coefficient control. That off-shell
control is not adopted as a physical state. No clock-only force is inserted.

In particular the full gradient decomposition is

    -(p/mu)*D_z(M*f_s)-f_s*D_z(N*p)-f_s*S_z*s
      =N*alpha*p_z-(p/mu)*M_z*f_s
       -N*p*sum_q f_sq*q_z-N*p*f_ss*s_z-f_s*N_z*p-f_s*S_z*s.

Only the PERTURBATION fast derivative is cancelled; delta(N*alpha)*p_bg,z
is retained. The regulator likewise keeps delta a*Z_bg,z after cancelling
a*zeta_z. Nine component bounds are exported: reaction-coefficient work,
local force, regular force gradient, its background-gradient coefficient,
full metric/frame work, regulator coefficient, local regulator, complete
current remainder and complete local momentum remainder.

The canonical force relation gives

    delta p=[xi-f_p*delta mu-mu*sum_q f_pq*delta q
                                  -mu*f_ps*chi_z]/(mu*f_pp).

The whole-root f_pp is strictly positive. This bounds delta p by Q and
Pcan, retaining metric/frame/volume changes. The existing full canonical
velocity estimate bounds every required ordinary raw velocity variation;
the complete auxiliary map bounds zeta in L2 from F and all six metric
variations in H1. No force H3, momentum H1 or hidden auxiliary acceleration
is assumed.

Local coefficient first-variation bounds use the uniform Euclidean norms
of their partial vectors. A first-variation lift of a force partial uses
its actual Hessian; unused higher lift entries are not asserted physical
derivatives. Background density coefficients use certified absolute boxes
or separate triangle bounds, never an assumed favourable sign.

The periodic operators satisfy ||P0||L2<=1 and ||P||L2->L2<=1. Therefore
all primitive terms have L2 bounds. The weighted fast mean uses
|mean(d_z*zeta)|<=||d_z||infinity*||zeta||L2; the two scalar momentum
transport means are retained separately. Both normal-form time jets,
spatial coefficients, reaction and all Gchi_z terms are included. Finally

    ||delta Sigma||L2<=||w||L2+||c||infinity*Pcan
                                      +||alpha||infinity*Q

closes the density input at the SAME L2 order. No source is made finite by
dropping a mean or Fourier tail.

## Caller-shift, gauge closure and original-coordinate bound

Before closing the caller's gauge velocity, the complete material-source
estimate is, with coefficients rounded outward,

    ||w_t-S*w_z||L2
       <=2.605699*||w||L2+23.306539*Q+8.570573*Pcan
                          +0.000895085*F+8.818979*U.

This includes reaction C*w. It is not yet the norm derivative because
scalar advection is retained on the left. Actual gauge-velocity closure
comes from the preserved coupled canonical/gauge owner, including the
independent harmonic coordinate-velocity input Hharm. After composing it,
and using the exact periodic scalar L2 transport pairing, the initial
original-coordinate logarithmic estimate is

    d||w||L2/dt <=2.607405*||w||L2+1542.215492*Q+608.336352*Pcan
                                  +0.000895085*F+8.821693*Hharm.

At zero norm use the upper right norm derivative, or the equivalent
regularized squared-norm inequality. The larger Q/Pcan coefficients arise
from conservative separate gauge/velocity estimates. They are not measured
instability rates and are not optimized for a desired time interval.

## Adapted coordinate and full normal-form pullback

Define w_ad as the scalar pullback of the ENTIRE original normal form,
including its original primitive conjugated with the scalar/momentum-density
pullbacks. Do not rebuild P as a fresh zero-mean primitive in zeta. The
nonzero coordinate commutator remains

    P(D_z(w_coord*xi))-w_coord*D_z(P(xi))
       =w_coord*mean(xi)-mean(w_coord*xi).

V1's mean/commutator and V2's gradient vector-weight identities are retained.
Taking the scalar pullback of the whole original equation gives exactly

    (w_ad)_t-B*(w_ad)_zeta=source_ad,
    B=J*(S-w_coord).

This chain includes the time derivative of the conjugated normal-form
operator. It does not assert that its individual primitive commutes with
the moving coordinates. With j<=J<=j_upper, scalar L2 source pullback has
norm <=sqrt(j_upper), and the inverse density norm pullback <=1/sqrt(j).
The actual B_zeta bound is reused from the unchanged initial gauge map.
The exact pairing integral u*B*u_zeta=-integral B_zeta*u^2/2 supplies its
L2 logarithmic constant.

Thus the complete INITIAL adapted-density bound is

    d||w_ad||L2/dt <=2.607839*||w_ad||L2
                      +1542.334128*Q+608.383149*Pcan
                      +0.000895154*F+8.822371*Hharm.

Q,Pcan,F remain explicitly in ORIGINAL coordinates; Hharm is the retained
adapted harmonic coordinate velocity. This is an identified mixed-coordinate
estimate with certified initial pullback factors, not an unproved
time-uniform norm equivalence for the full state.

## Evidence and remaining physics

[Executable](../../../Analysis/MasterTests/test_rtau_strong_density_l2_source_v1.py):
20/20 controls and byte-identical read-only replay COMPLETE; no failed or
unknown controls. Fresh
[receipt](../../../Analysis/MasterTests/outputs/rtau_strong_density_l2_source_v1_20261104/receipt.json)
SHA256 5dabd5cf8d13ccd84ab09fd0aad928e4e7f59035808128a20c6d6a5271c54a15.
Binary outward bounds for every component, caller source, original rate
and adapted rate are retained. All parent source pins as well as the 219
original pins are checked; snapshotted sources/sidecars preserve bytes and
timestamps. Earlier failures remain intact; this version has no failed run.

Exact gradient/transport/coordinate identities, independent third-force
partials, the nonzero primitive mean commutator and complete finite row
bounds support the stated continuum inequalities. Counts alone do not
prove them. These are same-author controls; scientific review is deferred.

The bound concerns the initial operator throughout the exact-root domain.
There is NO certified time-uniform background tube, so the estimate cannot
be integrated over [0,0.05] as a physical theorem. The full ordinary-field/
other-zero-speed/quartic action energy, all moving symplectic/Green terms,
nonlinear domain preservation, physical interactions/window, GR/local
compatibility and identifying matching remain open. No C_chi/a0 or
canonical Derived promotion follows. Existing papers acquire no concrete
defect here. No action adoption, vault mutation/sync, dispatch, publication,
commit/push or deployment is included.
