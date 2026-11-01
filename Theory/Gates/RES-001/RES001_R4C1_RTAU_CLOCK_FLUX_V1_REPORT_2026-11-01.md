# R-tau explicit local clock current and matter transfer

1 November 2026. Conditional comparison calculation; review DEFERRED.
physics_pass=false; gate_effect=NONE. R-tau remains an unadopted action;
this is not a new current for canonical R4C1 or the separate F-tau repair.

## Result and remaining local check

The regulator's clock current is now explicit on a general clock-normal
foliation and bounded on the entire certified prepared slice. A separate
variation of the original regulator in a curved lapse/expanding metric
checks the expansion and lapse-gradient terms. The source is nonzero on
the prepared data, so bare local matter-current conservation is not valid.

The current has zero temporal component in adapted coordinates. It changes
the spatial flux without changing the already declared global charge density.
This explains why the earlier global charge checks were necessary but could
not by themselves verify the full local continuity equation.

The direct comparison with the time derivative of the independently
reconstructed lapse density is still NOT_COMPUTED. This report supplies
the missing explicit flux/source side, not a completed local evolution
certificate. Quantitative higher derivative control, physical reduction,
general transverse perturbations and finite-time persistence remain open.

Owner: [prepared-Cauchy contract](RES001_R4C1_RTAU_PREPARED_CAUCHY_V1_CONTRACT_2026-10-31.md).
Immediate owner: [initial construction](RES001_R4C1_RTAU_INITIAL_ACCELERATION_V1_REPORT_2026-11-01.md).
The [current contract](RES001_R4C1_RTAU_CLOCK_FLUX_V1_CONTRACT_2026-11-01.md)
was frozen before execution. This makes explicit the induced-current
notation in the [two-repair variation](RES001_R4C1_TWO_REPAIR_COMPARISON_V2_REPORT_2026-10-31.md).

## Derivation from the actual regulator

Use signature -+++, chi=sqrt(-grad(tau)^2)>0,
t=-grad(tau)/chi, h^{mu nu}=g^{mu nu}+t^mu*t^nu,
K_{mu nu}=h_mu^alpha*h_nu^beta*nabla_alpha(t_beta), K=div(t),
p=t.partial(psi), and D the projected spatial derivative. Keep Z independent.

The clock regulator is

    L_reg=b*Z^2/2-b*h^{mu nu}*Z_mu*psi_nu-b*Z*a_t^mu*psi_mu.

Integration by parts uses

    div(h.grad psi)=h^{mu nu}*nabla_mu*nabla_nu psi+K*p+a_t.grad psi.

Thus, modulo a divergence,

    L_reg=b*Z^2/2+b*Z*(h^{mu nu}*nabla_mu*nabla_nu psi+K*p).

Varying the independent normal before projecting its unit constraint gives

    E_t,mu=b*[2*Z*t^nu*nabla_mu*nabla_nu psi
               +Z*K*psi_mu-nabla_mu(Z*p)].

The normalized clock variation is delta t=-h.grad(delta tau)/chi. Hence

    F^alpha=(b/chi)*[Z*D^alpha p
          +Z*(K*h^{alpha beta}-2*K^{alpha beta})*D_beta psi
          -p*D^alpha Z],
    E_tau,reg=div(F).

All extrinsic-curvature components are retained. This is not an isotropic
substitution into a flat formula. The acceleration term in the original
regulator is essential to this result. Dimensions agree with the earlier
action convention: [F]=4 and [E_tau,reg]=5.

An independent original-density control uses
ds^2=-N(t,z)^2 dt^2+a(t,z)^2 dvec(x)^2 and normal rapidity theta. At theta=0,
the scalar normal Euler variation divided by sqrt(-g) is

    (b/a)*[Z*(psi_tz/N-psi_t*N_z/N^2)
              +Z*(a_t/(a*N))*psi_z-(psi_t/N)*Z_z].

It agrees exactly with the covariant projection. Omitting the expansion
piece fails the control. The general matrix projection separately retains
the full K tensor; the curved control checks its signs and normalization.

## Matter balance and global versus local conservation

The dust action gives E_tau,m=div(epsilon*C^2*grad tau). The total clock
equation is therefore

    div(epsilon*C^2*grad tau+F)=0.

On the multiplier branch rho=epsilon*C^4, chi=C, the matter Ward identity is

    div(T_m) = beta*T_m*grad psi-E_tau,reg*grad tau.

The extra term is parallel to the clock normal. It changes the matter energy
balance, not the previously derived orthogonal dust force. This is classical
reversible action exchange, not derived irreversible entropy production or
a microscopic matter-creation mechanism. It does not identify b, beta, K_Q
or the nonlinear-force normalization. Setting b and beta to zero removes
this matter exchange; it is not by itself GR recovery of the entire action.

In tau=t ADM coordinates, h^{0mu}=0 even for nonzero shift, so F^0=0.
The matter clock current has components J_m^0=-rho and J_m^i=rho*S^i.
With W=N*sqrt(h), the exact planar continuity equation is

    partial_t(W*rho)-partial_z(W*rho*S^z+W*F^z)=0.

The positive clock charge density remains W*rho=sqrt(h)*rho/C. The extra
flux integrates to zero on the periodic circle but need not vanish locally.
The equivalent normal matter-energy balance is

    t.partial rho+K*rho=beta*rho*p+chi*E_tau,reg.

The executable checks these forms agree, including every lapse, volume,
shift-divergence and conformal coupling term. In the existing flat probe,
Z=k^2*amp*cos(kz), p=constant, it recovers
E_tau,reg=b*p*k^4*amp*cos(kz). Flat space is a variational control, not an
asserted admitted finite-density background or a physical cutoff estimate.

The earlier homogeneous characteristic calculation already includes this
linear source: its R-tau extra row is b*p*k^2*delta Z/a^2, matching
chi*E_tau,reg in that limit. Its total clock Ward test subtracts that row
and explicitly rejects bare dust continuity. Inspection of the unchanged
[V3 executable](../../../Analysis/MasterTests/test_01_r4c1_two_repair_characteristics_v3.py)
confirms this; those old calculations are not reopened or relabeled by the
present nonlinear/curved current result. This inspection is not a fresh
replay of their complete experiment.

## Actual prepared-data current and bounds

At the initial conformal metric h_ij=a^2 delta_ij, write h=a^2,
p=(psi_dot-S^z*psi_z)/N and Kzz_phys=K_zz/h. Then

    F^x=b*Z*Sx_z*psi_z/h, F^y=b*Z*Sy_z*psi_z/h,
    F^z=(b*N/h)*[Z*p_z+Z*(K-2*Kzz_phys)*psi_z-p*Z_z].

The transverse components are retained, although their divergence vanishes
in this planar geometry. The shift, its first/second derivatives, metric
rate, clock lapse and all uncertain H/omega/root data enter the calculation.
The prepared initial metric is not imposed as a future evolving shape.

Thirty-two outward coefficient cells cover every z and every root in the
certified C2 ball. All 224 current/derivative/source endpoint pairs are
finite and ordered. The bounds include

    |F^x|, |F^y| < 5.019e-14,
    |F^z| < 2.607e-5,
    |E_tau,reg| < 5.003e-5.

These numbers use the registered diagnostic units/coefficients and are not
observational predictions. Centre source values at z=0.3,1.1,2.4 are about
4.170e-5, -2.618e-5 and 1.798e-6. Their intervals exclude zero; removing the
local regulator source is rejected. The current has no singular clock
normalization on this slice: chi>0.9999. No null-clock or caustic extension
is inferred.

## Verification and next calculation

[Executable](../../../Analysis/MasterTests/test_01_r4c1_rtau_clock_flux_v1.py):
14/14, no failed/unknown checks; exact recomputing read-only replay.
[Receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_clock_flux_v1_attempt_01/summary.json)
SHA256 471748908020df864be786a073a29b5e5dd94a187456ed6686b9d0a5996ead4a.
Controls include the independent curved original-action variation, full
curvature projection, ADM charge/energy equivalence, existing flat operator
and nonzero prepared source. These same-author controls are not independent
external scientific review. All source/sidecar bytes and mtimes are preserved.

Next obtain the higher root/acceleration derivative control needed to compare
the reconstructed density time derivative directly with this LOCAL current
equation. Keep the full lapse Euler flux and actual gauge drift; do not
substitute the global charge identity for the local test. Sharp final gauge
quadrature, the full physical symplectic/characteristic problem, transverse
spatial wavevectors, finite-time evolution, interactions/window and matching
remain open. No new paper or canonical claim is established by this sub-bundle.

P1/P2, Thermodynamics, original R4C1 and the site are unchanged. G1-G6 remain
incomplete. No action adoption, external dispatch, vault mutation, publication
or commit/push.
