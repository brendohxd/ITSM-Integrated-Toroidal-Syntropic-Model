# Constraint-restored scalar-rate energy: negative restriction, physical domain open

21 October2026. Unchanged R4C1 Stage2; version1. Local823/823, complete fresh
read-only replay exact. This verifies an energy-Hessian RESTRICTION and a
conditional continuum estimate, not a physical-mode or instability theorem.

## Finding first

The entire scalar-rate Hessian restriction is numerically negative in all54
registered finite-grid controls. The five normalized probe curvatures are near
-15 in the registered reference normalization. The conditional continuum
calculation explains the leading value -K_Q/p, rather than inferring it from
a fitted slope or diagonal-only numerical approximation.

Consequently this restriction of the clock Hamiltonian Hessian cannot simply
be used as a POSITIVE energy norm on those directions. A spatial weight does
not change the sign of the same quadratic form. This does NOT reject weighted/
mixed-order formulations or an independently justified positive symmetrizer.
The complete auxiliary constraints may exclude the tested directions; their
physical admission and coupled evolution have NOT been established.

The earlier uniform partial Legendre inverse certificate is unchanged. An
invertible partial temporal complement and a positive physical perturbation
energy are different requirements. Neither result supplies the latter.

## Full scalar-rate second variation

Use the undivided nodal pullback and full planar constraint restoration, with
the force clock varied before elimination. Fix all configurations, independent
reduced momenta, both charges and the three mean metric pairs, and vary only
the independent scalar-rate field s=p+t*f, p>0. Dependent momenta are NOT fixed.

For this direction geometry is fixed. The full Ricci contribution is retained
and is constant (zero on the registered flat metric), not deleted from a
general physical Hessian. Dust, potential, background frame terms and lapse
flux remain in the baseline energy and inverse-clock derivatives.

At fixed configuration write the original proper-velocity density as

    L0 = y^T R y/2 + ell(s)^T y + f0(s),
    E0 = (P-ell)^T R^-1(P-ell)/2 - f0,
    y = R^-1(P-ell).

Volume is1 in this registered family. R is independent of s, ell is affine in
s, and the restored P is affine along the path. Let

    deltaP = full restored momentum response,
    d = deltaP-ell_s*f,
    E1 = y.d-f0_s*f,
    E2 = d^T R^-1 d-f0_ss*f^2,
    C0 = E0+Edust+F0'.

The FULL restricted Hessian of Hpsi=<(E0+Edust+F')/s> is

    Hss[f,f] = < E2/p - 2*(E1+deltaF')*f/p^2 + 2*C0*f^2/p^3 >.

The velocity response d^T R^-1 d is essential. The stationary first-differential
evaluator from the earlier momentum report was not reused as a Hessian.
Original density values with re-solved velocities independently test this
second-variation formula. All off-diagonal temporal couplings remain in R^-1.

## Exact nonlocal momentum restoration on the registered family

Let theta=k*z with the registered origin offset, w=e*cos(theta), e=1/500,
Z=U*w^2, g=b*w^2, h=I. With I_z the zero-mean periodic primitive:

    G = g*Z' = 2*b*U*w^3*w',
    d_translation = <sin(theta)*w'> = -e*k/2,
    delta_lambda = <G*f>/d_translation,
    deltaS = -G*f + delta_lambda*sin(theta)*w',
    deltaP_Kzz = I_z(deltaS),
    deltaP_Xy = delta_lambda*sin(theta),
    all other deltaP components = 0.

The global source has zero mean exactly; no arbitrary source mean is discarded.
Fixed mean metric momenta are retained. The factor2 relating p_hzz to proper
Kzz momentum is included. Also F=gamma*pVz, so deltaF=0 on THIS direction
because delta pVz=0. This does NOT set F0' to zero.

Original-density derivatives give

    ell_s,Kyy = -2*b*Z*w^2; ell_s,Xy = -b*Z*w;
    f0_s = K_Q*(1+w^2)*p - 3*A*abs(w)^3*p^2;
    f0_ss = K_Q*(1+w^2) - 6*A*abs(w)^3*p.

No third derivative of the C2 spatial cusp is required. Preserve the actual
initial compatibility residual, with the inherited shift and regulator rate:

    Zhat = Ud*w^2 - shift*Z',
    J = C0 + p*(ell_s.y + f0_s - g*Zhat).

This is NOT declared exactly zero for the stored initial data. Substitution
into the complete Hessian cancels the local ell_s.y terms and yields

    Hss[f,f] = < d^T R^-1 d/p - 2*y.deltaP*f/p^2
                  + (-f0_ss/p + 2*g*Zhat/p^2 + 2*J/p^3)*f^2 >.

The K_Q/p=15 value follows only from the already declared diagnostic recipes
K_Q=3*eta and p=eta/5. It is NOT a microscopic matching, physical acceleration
coefficient, universal ITSM prediction or new determination of K_Q.

## Conditional continuum localization bound with explicit constants

Fix the reference coordinate/field units used by the diagnostic recipes; the
following norms and epsilon are numerical reference-chart quantities, not SI
energy normalization or a physical cutoff. Let L=2*pi/k and x measure distance
from EITHER alignment node. Choose smooth f supported at epsilon<x<2*epsilon,
with normalized-average norm <f^2>=1, 0<epsilon<=min(1,L/16).

Assume finite bounds

    Rmax >= sup |shift|,
    Y >= sup sqrt(y_Kzz^2+y_Xy^2),
    sigma >= sup_support |J|.

These continuum background/residual bounds are HYPOTHESES; point sampling below
does not certify them. Set c=e*k, d_abs=e*k/2, and use the independently
certified partial inverse bound ||R^-1||_2<=C_R/eta, C_R=200/33. Symmetry makes
the column/row maximum norms equal, so the earlier infinity-norm certificate
also supplies this Euclidean bound in the fixed reference chart. Define

    M = 16*abs(b*U)*c^4,
    P = 2*M*sqrt(L)+M/(d_abs*sqrt(L)),
    E = 8*abs(b*U)*(1+2*e)*c^3.

On the support |w|<=2*c*epsilon and |w'|<=c, hence |G|<=M*epsilon^3.
Cauchy-Schwarz gives |<G*f>|<=M*epsilon^(7/2)/sqrt(L). Because
<abs(sin(theta)*w')>=d_abs, the restored source satisfies
<abs(deltaS)><=2*M*epsilon^(7/2)/sqrt(L). A mean-zero periodic primitive has
sup norm at most L*<abs(deltaS)>, as follows by integrating once and subtracting
its mean. Thus

    ||deltaP||_L2 <= P*epsilon^(7/2),
    ||ell_s*f||_L2 <= E*epsilon^3.

The resulting EXPLICIT bound is

    |Hss[f,f]+K_Q/p| <= Delta(epsilon)+2*sigma/p^3,

    Delta(epsilon) = 4*(K_Q/p)*c^2*epsilon^2
        +48*abs(A)*c^3*epsilon^3
        +32*abs(b)*c^4/p^2*(abs(Ud)*epsilon^4
                            +abs(U)*Rmax*epsilon^3)
        +2*Y*P/p^2*epsilon^(7/2)
        +C_R/(eta*p)*(P*epsilon^(7/2)+E*epsilon^3)^2.

Every contribution, including nonlocal translation/metric-momentum restoration,
vanishes as epsilon tends to zero at FIXED eta>0. This is not eta-uniform GR
control. For0<epsilon<=1, Delta<=Cstar*epsilon^2, where

    Cstar = 4*(K_Q/p)*c^2 +48*abs(A)*c^3
        +32*abs(b)*c^4/p^2*(abs(Ud)+abs(U)*Rmax)
        +2*Y*P/p^2 +C_R/(eta*p)*(P+E)^2.

Cstar>0 for the stated K_Q,p,e,k>0. The executable checks the nonnegative
coefficient/power majorization exactly after setting rho=sqrt(epsilon).
If sigma<=K_Q*p^2/8 and

    0<epsilon<=min(1,L/16,sqrt(K_Q/(4*p*Cstar))),

then Hss[f,f]<=-K_Q/(2*p). This is an explicit CONDITIONAL continuum theorem,
not an unconditional theorem about the stored on-shell candidate or physical
tangent space. The same uniform estimate applies to normalized combinations
of disjoint smooth bumps satisfying any finite set of real homogeneous linear
conditions defined on that probe space, using the prior finite-node kernel
argument. This does not replace an unknown pointwise auxiliary hierarchy with
finitely many conditions or assume localized probes are physically admitted.

## Numerical controls, not physical eigenmodes

All9 unchanged family/eta inputs use the existing H/U/Ud and shift, n=17,25,33
and both node offsets:54 controls. Every complete n-by-n restriction is retained
with all off-diagonal entries. Constant, cos(theta), cos(theta)^2, sin(2theta)
and sin(3theta)+2*cos(2theta)/7 probes are normalized in grid-average L2.
Direct ORIGINAL-density second differences use separately re-solved velocities
at steps1e-20 and1e-24,100-digit working arithmetic and frozen normalized1e-28.

| Recorded control | Value |
| --- | --- |
| Largest normalized direct second-difference discrepancy |2.46640952324e-33 |
| Largest sampled abs(J)/(K_Q*p^2) |2.37639068123e-16, retained nonzero |
| Normalized probe curvatures, all families |about -15.0000499323 to -15.0000299635 |
| Numerical average-L2 Gershgorin row estimates, all controls |about -15.0000597717 to -14.9999999999943 |
| Largest off-diagonal average-L2 entry |1.55375543844e-12 |
| Largest change if the lapse-flux term were omitted |149130.808768 |
| Largest change if the solved-velocity response were omitted |2.78916467843e-19 |

Gershgorin estimates here are finite high-precision DIAGNOSTICS, not outward
interval eigenvalue enclosures. Neither grid refinement nor tiny sampled J
certifies the required continuum bound sigma or complete physical admission.
The large flux-deletion effect demonstrates that the near--15 curvature is not
obtained by discarding a seemingly small boundary term. The much smaller but
nonzero temporal-response term is also preserved and resolved by the controls.

All823 local checks pass. A full fresh8-worker replay repeats the16-worker
calculation, reproduces the three JSONs/sidecars byte-for-byte and returns exit0
with READ_ONLY_REPLAY_EXACT. The complete replay log's54 keys and all per-grid
checks were inspected programmatically. Sources cover115 pins and319 native
source/runtime metadata records. A separate734-record raw-integer guard and38
output-directory file sets are unchanged across replay. Historical timestamp
transport limitations and all older failures remain preserved, not rewritten.

| Artifact | SHA256 |
| --- | --- |
| Contract |abdc2005b326ecf23c2e20a77be18332727bad42221afdb1992a1ab17ff2d7c1 |
| Executable |a159ac186b11fd823f5d8daf33af6a189606e9d80cabe141f97f4feda4bda95e |
| summary.json |066bddf8701db87794fd35c49e9832bc4f7e0ccdfc57dd0e9ff0eb04f212ba8a |
| independent.json |c79b10470b890ef973b7ac630d1a749d824500da089c9c73f9c8c65e0f2a992f |
| formulas.json |38196c8400c244673846010ba470a2ad9c8a30a9dce24a49f663adaf04bfbbdd |
| Fresh replay log |379bb938c4458e8abfa1d7fcc8cd2635b0b17443976b186c0d7403c2201f04ef |
| Raw post-replay guard log |e236e380199a1347cafed143649fd79c16f370cedb479e679a0cbaf801b77ddd |

Executable: Analysis/MasterTests/test_01_r4c1_scalar_rate_energy_v1.py.
Receipts: Analysis/MasterTests/outputs/r4c1_scalar_rate_energy_v1_attempt_01/.
The parent alone writes new receipts; replay writes none. Private runtime logs
remain ignored. An optional CIM process-inspection query lacked local access
after the primary handle had already completed; no elevation or system change
was needed or attempted. No speedup or billed-token savings are inferred.

## Physical interpretation and next required calculation

The displayed Hessian is restricted to scalar-rate variations at fixed other
INDEPENDENT variables with full DEPENDENT momentum/velocity restoration. It is
not the entire coupled physical Hessian or a normalized mode computation.
Background two-form drift still belongs in the coupled generator and was not
discarded by calling this curvature a spectrum. At a nonstationary constrained
candidate, a negative energy direction is not, by itself, proof of exponential
growth. Even a canonical oscillator with H=-(q^2+p^2)/2 has rotational classical
flow; physical ghost classification additionally requires actual physical-mode
and normalization evidence. No instability or quantum health is decided here.

The next necessary question is whether the complete auxiliary constraints and
their persistence admit or remove these localized scalar-rate directions, and
what positive control norm, if any, is justified on the remaining coupled space.
Do not silently replace H by its absolute value or claim that an arbitrary
weight cures the issue. A separately derived symmetrizer/graph norm remains an
open option. The full372 QR continuation remains preserved and unfinished.

Stage1 complete only in its bounded linear prepared-dust scope; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1--3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED;
TOP-X4 unchanged. Rule9 DEFERRED; Rule9_cleared=false; inherit Legendre-domain,
finite-node, nodal/global-reduction/tangency/descriptor and transitive review debt.
Same-author verification is not independent scientific review. Physical domain,
full auxiliary admission/persistence, coupled modes/interactions/cutoff, healthy
GR and both identifying matching inputs remain substantive. physics_pass=false;
gate_effect=NONE. Root goal ACTIVE/incomplete. No new action/parent, state adoption/
evolution, vault mutation, manuscript/site/publication, commit/push, paid dispatch
or model/package/global-runtime change.
