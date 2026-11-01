# R-tau: a physical mixed-regularity linear estimate through t=0.05

31 October 2026, Australia/Perth.
Result IDs: R9-MT1-RTAU-PHYSICAL-NORM-V2; R9-MT1-RTAU-NORM-EXTENSION-V1.
Claim Conditional; review DEFERRED; Rule9_cleared=false.
physics_pass=false; gate_effect=NONE. R-tau remains an unadopted comparator.

## Outcome and meaning

The repeated zero-speed branch in the preceding R-tau calculation does NOT
constitute a linear no-go in the physical norm constructed here. Keeping
the reconstructed matter density, canonical field momenta and their actual
derivative orders gives a momentum-uniform LINEAR energy estimate. Both
zero-speed degrees of freedom and the quartic force mode remain present.
No mode restriction, changed action or fitted cutoff cures the old test.

The complete coupled linear system is controlled on the OLD admitted
homogeneous B1 background for the registered planar modes |k|>=1, with k=0
treated separately. The estimate extends to t in [0,1/20]=[0,0.05]. It is
not a nonlinear physical-domain theorem or an interacting EFT window.

The estimate's constants are extremely conservative. They establish a
uniform mathematical bound, not useful finite-mode numerical accuracy.
Do not advertise a small numerical error or long physical lifetime from it.

F-tau's separate high-frequency gradient failure is unchanged. This new
result is for the explicitly different R-tau regulator action, not a repair
of the original unchanged R4C1 action or canonical gate promotion.

## Authority and equations reused

Follow the [physical-norm contract](RES001_R4C1_RTAU_PHYSICAL_NORM_V1_CONTRACT_2026-10-31.md),
[frozen variable/energy specification](RES001_R4C1_RTAU_PHYSICAL_NORM_V1_EXECUTION_SPEC_2026-10-31.md)
and [extension contract](RES001_R4C1_RTAU_NORM_EXTENSION_V1_CONTRACT_2026-10-31.md).
The parent [characteristics report](RES001_R4C1_TWO_REPAIR_CHARACTERISTICS_V3_REPORT_2026-10-31.md)
and its receipt own the FULL new quadratic action, lapse/density/shift/Z
reconstruction, changed clock and U(1) currents, and homogeneous mode.

No Hessian or old-action propagator is rerun as a substitute for that result.
Generic M,B,Q,M_dot,B_dot are reused and actual drift is checked. The local
scalar helicities are q=(Gamma,v_z,delta u,delta v,delta r,delta psi), with
Gamma=(gamma_xx+gamma_yy)/2 and kappa=k/a>0. Tensor/vector blocks decouple
exactly on the isotropic homogeneous background. Use negative k by conjugate
reality; the proof concerns the registered planar mode family. A general
nonlinear three-dimensional torus Cauchy theorem is not asserted.

All coefficients are the previously frozen OLD B1 control values, not the
later eta=1/4 vortical preparation and not microscopic matches. Frequencies,
momenta and times below are in those declared control units. There is no
conversion to an observed physical torus length or UV cutoff.

## Physical variable map and admitted data

Let p=psi_dot and beta=2/5. Reconstruct delta rho from the NEW full lapse
equation, including spatial Euler flux. On the conserved background
Friedmann constraint its coefficient on Gamma is exactly kappa^2.

Define

    sigma = delta rho + K_Q*p*(delta psi_dot+beta*p*delta psi),
    Pi = q_dot + M_scalar^{-1}*B_scalar*q,
    Y = (sigma,kappa*v_z,kappa*delta u,kappa*delta v,kappa*delta r,
         kappa^2*delta psi,Pi_Gamma,Pi_vz,Pi_u,Pi_v,Pi_r,delta psi_dot).

The added term in sigma is the variation of the timelike kinetic scalar
K_Q*(n.partial psi)^2/2 in the clock gauge. It is not identified with the
complete Hilbert/renormalized stress tensor. This is a bounded combination
of physical observables, not a new matter law or fixed-density condition.
For the force velocity use delta psi_dot rather than its shifted canonical
component, as explicitly frozen in the specification. The other five Pi
are normalized canonical momenta of the new action. In particular

    Pi_vz = v_z_dot - H*v_z/5 - (2*i*kappa/5)*delta psi.

Both the force contribution in sigma and the canonical momentum shift have
a physical source in the action and reconstruction. They are not k weights
selected to fit a finite list of eigenvalues.

Writing Y=T*(q,q_dot), the exact determinant is

    det T = kappa^6*(kappa^2+u_dot^2+v_dot^2+r_dot^2).

Thus the map is invertible for every nonzero registered momentum. Its
inverse reconstructs every scalar amplitude/velocity and delta rho. The
total state dimension is unchanged. Local nonzero-mode density fluctuations
are allowed; they are not set to zero by the fixed GLOBAL charge ensemble.

The new generator is exactly

    G_Y = (T_dot+T*G)*T^{-1},
    G_Y = kappa^2*A2 + kappa*A1 + R.

T_dot uses the actual background evolution and kappa_dot=-H*kappa. Dropping
it is explicitly rejected. This is a time-dependent change of variables,
not a projection of the evolution or an instantaneous isospectral claim.
The parent symplectic form transports by inverse congruence under this
invertible map; canonical momenta come from the full M/B action, not a
guessed kinetic metric.

## Principal estimate, including the formerly defective zero branch

Set F=kappa*v_z,

    D = Pi_Gamma-i*F/198,
    X = F+18*i*D.

The ordinary trace/frame principal equations become

    D_dot=0, X_dot=kappa*Pi_vz, Pi_vz_dot=-kappa*X/3.

Sigma supplies the other zero-speed coordinate. The full ordinary scalar
characteristic polynomial in GENERATOR eigenvalue lambda is

    lambda^2*(lambda^2+1/3)*(lambda^2+1)^2
        *(lambda^2+1+(u^2+v^2)/13).

Its two zero eigenvectors are independent throughout the real background
box. A nonzero rank-eight minor is -(13+u^2+v^2)/429. Hence the zero root
is semisimple in these variables, without imposing a smaller kernel.
The quartic force pair is retained separately in the same full generator:
A2 on (kappa^2*delta psi,delta psi_dot) is [[0,1],[-5/33,0]].

Use the positive energy

    E = |sigma|^2+|D|^2+|X|^2/3+|Pi_vz|^2
      + (kappa*delta phi)^dag C_phi (kappa*delta phi)
      + |Pi_u|^2+|Pi_v|^2
      + |kappa*delta r|^2+|Pi_r|^2
      + b*|kappa^2*delta psi|^2+K_Q*|delta psi_dot|^2,

where delta phi=(delta u,delta v), b=5/11, K_Q=3 and

    C_phi = I + (1/13)*(v,-u)^T*(v,-u).

The full exported H in E=Y^dag H Y satisfies EXACTLY

    H*A2+A2^dag*H=0, H*A1+A1^dag*H=0.

These are generic-background identities, not initial-event fits. On the
declared box, (1/330)*I <= H <= 110*I and ||H_dot||_2<=16/13. The
trace/frame two-dimensional block has determinant 1/3 and trace
4288789/39204<110; its separate unit Pi_vz coordinate is also below 110.
The condensate spatial form has eigenvalues 1 and 1+(u^2+v^2)/13.

## Explicit norm equivalence and remainder control

Define the natural observable norm

    N_phys = |delta rho|^2 + sum_j |q_dot_j|^2
           + kappa^2*(|Gamma|^2+|v_z|^2+|delta u|^2
                      +|delta v|^2+|delta r|^2)
           + kappa^4*|delta psi|^2.

Its field part combines positive temporal kinetic control with the stated
spatial derivatives of the fields. This is not a claim that the canonical
Hamiltonian is positive. Density has its actual reconstructed derivative
order. The exact maps between these observables and Y have bounds

    ||Y|| <= L*sqrt(N_phys), L=16792/165,
    sqrt(N_phys) <= N*||Y||, N=13654543/330,
    N_phys/(330*N^2) <= E <= 110*L^2*N_phys.

Thus the estimate is uniform relative to the specified physical data norm,
not merely in a diagonalizing basis with an unbounded condition number.
Bounds include kappa>=1/2 and all background values in the box below.
Higher curvature derivatives require correspondingly higher Sobolev
regularity, as usual; no same-order bound for every curvature observable
is inferred from a field-energy norm.

Entrywise exact rational majorants give

    ||R||_2 <= B_R=19215773602/96525,
    E_dot <= C*E,
    C=330*(16/13+220*B_R)=1690988124496/117,
    E(t) <= exp(C*t)*E(0).

For reproducibility, the numerator coefficients are bounded by absolute
polynomial coefficients on the box. Momentum denominators factor into
powers of kappa and kappa^2+u_dot^2+v_dot^2+r_dot^2. The latter is at least
kappa^2; remaining negative powers use kappa>=1/2. The receipt exports
every entry's bound. This proves a momentum-uniform estimate, not a
sampled-frequency extrapolation. C is about 1.4453e10: the exponential
bound is far too loose to certify useful numerical accuracy.

The algebraic Z and differentiated shift reconstructions have combined
coefficient bound 6398/165 in this norm. Lapse and dust multiplier follow
from their original reconstruction, with C(psi)>0. The frame, matter,
metric and regulator constraints have not been removed. The zero-speed
branch of the previous norm calculation is explained explicitly: its old
generalized vector has physical energy asymptotic to (121/36)*kappa^2,
while its zero vector has bounded energy. Its earlier apparent k*t growth
therefore did not establish a blow-up relative to fixed physical density
and field-energy initial data. Both vectors remain in the present system.

Tensor and vector helicities use their own canonical momenta and positive
wave energies. Their squared speeds remain 1 and 4/5, with respective
energy rates 33992/75 and 37732/65. No new tensor/local-gravity observation
or healthy GR limit is inferred from those numbers.

## Background lifespan, mean mode and scope

The same background box is

    1/2<=a<=2, 1/20<=rho<=2,
    |H,u,v,r,u_dot,v_dot,r_dot,p,psi|<=2.

The original on-shell initial data are strictly inside it. All non-density
coordinates obey their exact individual absolute-flow exit bounds through
t=1/20; the tightest tested velocity margin remains strictly positive.
For density use the actual equation rho_dot=(-3H+beta*p)*rho, giving
|rho_dot/rho|<=34/5. With x=(34/5)*(1/20)=17/50,

    33/250 <= rho(t) <= 10/33,

from exp(-x)>=1-x and exp(x)<=1/(1-x). These bounds are strictly inside the
same box. Standard first-exit/local-ODE continuation therefore supplies the
background through 0.05; the Friedmann constraint is preserved exactly.
The initial V2 absolute-exit proof only claimed 0.005 and remains frozen;
the distinct extension receipt supplies the longer interval. No numerical
background fit or changed initial state is used.

For |k|>=1, a<=2 implies kappa>=1/2. This is a mathematical infrared
restriction in the declared control units, NOT a physical UV cutoff.
Smaller nonzero momenta require their own constants. The exact k=0 mode
uses all six metric amplitudes and the separately reconstructed equations.
Its Euclidean generator norm is bounded by 34310503/53625, with energy
rate twice that value. Its two independent transported global charges give
a fixed-charge level of dimension 24. This is not a completed global
symplectic quotient or quantum-ghost diagnosis of the raw conformal sign.

The Fourier estimates give controlled full linear evolution on this mode
family without continually projecting onto a slow graph. The same estimate
can be summed with fixed Sobolev weights. It does not prove nonlinear
constraint/domain persistence, finite-amplitude positivity, caustic avoidance,
general three-dimensional nonlinear well-posedness or a physical interaction
window. Those are the next requirements, not consequences of a check count.

## Verification, preserved failure and next task

- [Norm executable V2](../../../Analysis/MasterTests/test_01_r4c1_rtau_physical_norm_v2.py),
  [receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_physical_norm_v2_attempt_01/summary.json):
  58/58, no failures/unknowns; SHA256
  2a4e72ceef0a7681c8ee3fc38028d9dcb86b2ebd9999af6b0bdb58b0a3e80533.
- [Extension/additional controls](../../../Analysis/MasterTests/audit_01_r4c1_rtau_norm_extension_v1.py),
  [receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_norm_extension_v1_attempt_01/summary.json):
  25/25, no failures/unknowns; SHA256
  0b2c3d34b6cb19da0701ab10497b554f4fcdf6e8c494b1b5bbf8da611fc2f1ad.
- BOTH complete recomputing read-only replays are byte-identical. The source
  pins and sidecars retain their bytes and modification times.
- Independent actual-map drift differences at k=1,7,40 and 120 digits have
  normalized errors below 1.502e-28 and 1.502e-44 for steps 1e-14 and 1e-22.
  Exact complex-state reconstruction and the complete energy derivative
  are checked with nonzero frame/matter data at those modes.
- V1 57/58 is retained. Its sole failure checked the full three-dimensional
  trace instead of the intended two-dimensional certificate block. The
  [V2 addendum](RES001_R4C1_RTAU_PHYSICAL_NORM_V2_EXECUTION_ADDENDUM_2026-10-31.md)
  corrects that slice; all 22 compared scientific export fields, energies,
  constants, equations and tolerances remain exactly identical.
- These are same-author provisional controls and exact replay, not an
  independent review panel. Rule-9 remains DEFERRED.

The bounded R-tau linear physical-norm question now has a supported positive
answer in this scope. The next deciding work is finite-amplitude coupled
constraint/principal robustness and actual nonlinear interactions, retaining
the norm-cubed force's nonanalytic third-order behaviour. Do not substitute
a vacuum/frame-only scattering threshold for a physical cutoff.

Neither candidate is adopted. No concrete defect in existing unchanged-action
papers is established by this new comparison result; no manuscript/PDF/site
was edited. Full physical interacting domain/window, microscopic clock choice,
realistic matter, GR/local compatibility and identifying matching remain OPEN.
Original G1-G6 INCOMPLETE; MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED;
UVIR-003 IN_PROGRESS; Stage4A CLOSED; TOP-X4 unchanged. The native goal is
ACTIVE following app/user resume. No commit/push, deployment, publication,
external provider/reviewer dispatch or vault mutation in this bundle.
