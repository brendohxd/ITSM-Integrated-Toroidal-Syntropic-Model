# Full planar implicit weak action: curvature, dust and local constraints

28 October 2026, Australia/Perth. Conditional; Rule-9 DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE. G1-G6 INCOMPLETE.

## What changed

There is now an executable, unspecialized PLANAR variational backend for the
original R4C1 action, retaining nonlinear spatial curvature, all six metric
and three frame components, u,v,r,psi,Z, the dust clock and its multiplier.
It also retains lapse/gradient and shift/gradient variations. It implements
the implicit equations rather than inverting the singular matrix at a node.

The preceding initial-acceleration evaluator explicitly set R3=0. That is
appropriate for its initial flat slice, but it could not be reused unchanged
as a future nonlinear evolution engine. The new backend supplies this missing
action-level implementation. It does not invalidate or overwrite that earlier
initial calculation.

127/127 curvature, full-coordinate-action, first-variation, exact alignment,
constraint-weight, interface and countersequence controls pass. A fresh run
reproduces the scientific receipt exactly.171 pinned sources and digest
values remain unchanged. No failed or unknown rows were found. These are
same-author implementation/analytic checks, not peer review or an evolved
background certificate.

## 1. Nonlinear curvature and the local lapse constraint

For the planar metric h(z), with ALL h entries retained, define

    L_GammaGamma=sqrt(h)*h^(ij)*
        [Gamma^k_(i,l)*Gamma^l_(j,k)-Gamma^k_(ij)*Gamma^l_(k,l)],
    B=sqrt(h)*[h^(ij)*Gamma^z_(ij)-h^(iz)*Gamma^j_(ij)].

Direct nonlinear Ricci differentiation gives

    sqrt(h)*R3=L_GammaGamma+partial_z(B),
    N*sqrt(h)*R3=N*L_GammaGamma-N_z*B+partial_z(N*B).

The periodic action therefore uses MP2*(N*L_GammaGamma-N_z*B)/2, but
the local lapse constraint MUST retain the resulting curvature divergence.
At N=1,N_z=0, the independently varied lapse gradient is

    L_Nz=J-MP2*B/2,  J=gamma*h^(zj)*Pi_Vj,
    Hperp=E_weak+partial_z(J-MP2*B/2).

E_weak includes the full dust Legendre energy and is a weight-one density.
The torus integral of a divergence being zero does not delete this local term.
The original Einstein/GHY convention is preserved; there is no flat-curvature
or omitted-lapse-gradient shortcut in the new backend.

## 2. Full implicit equations and moving interfaces

The56-entry input is q16,v16,d16,S3,S_z3,N,N_z. q contains the original14
coordinates plus tau and epsilon. The full scalar-clock action is varied
BEFORE imposing its multiplier equation. The normalized frame uses the
original lapse-gradient contribution to X and the complete temporal regulator.
No evolving polynomial graph is imposed on psi,Z or the other fields.

The first variational derivatives define

    E_a=L_qa-partial_t(Pi_a)-partial_z(F_a)=0,
    Pi_a=L_va, F_a=L_da,
    E_N=L_N-partial_z(L_Nz)=0,
    E_Si=L_Si-partial_z(L_Szi)=0.

The epsilon equation remains algebraic; the lapse and shifts remain constraint
variables. The holonomic unit-frame multiplier is reconstructed as in the
normalized Ward report when the corresponding chain rules are justified.
Neither the field equations nor their weak definition requires division by
g=b*w^2. Physical mode reduction and well-posedness do not follow from this
implicit representation.

At an internal interface z=a(t), distributional differentiation gives the
singular Euler coefficient a_dot*[Pi_a]-[F_a]. Without a declared surface
source, the required matching condition is

    [F_a]-a_dot*[Pi_a]=0.

The corresponding lapse/shift conditions include their own flux jumps, since
they have no time momenta. Node stationarity is not inserted into this formula.
A weak evolution must satisfy these equations, not merely omit interface
contributions when integrating periodic expressions. The previously computed
jerk delta is retained wherever it enters a differentiated equation.

## 3. A candidate action domain, not an invariant solution space

On a finite time interval times the periodic planar circle, a sufficient
candidate domain for ACTION INTEGRABILITY and smooth-test first variations is:
the dynamical q fields lie in L-infinity(time;H1(space)) intersect
H1(time;L2(space)); h remains uniformly positive definite; epsilon is bounded;
and the full first spacetime gradient of psi additionally lies in L3.
Take lapse positive and lapse/shift in W1-infinity. Physical epsilon>=0 and
timelike dust-clock gradient are additional solution-domain requirements.

In one spatial dimension the stated uniform H1 bound gives bounded field
values. Canonical/frame/curvature terms are quadratic products of first
derivatives, regulator terms have bounded coefficients times such products,
and the cubic force is integrable under the L3 condition. Conformal factors
are bounded on the resulting bounded psi chart. Smooth compact-time,
periodic-space first variations are meaningful, including at Y=0; no ordinary
third cusp tensor is invoked. Candidate charges and torus integrals are finite
where their stated matter/clock conditions hold.

This is an integrability argument, NOT proof of an invariant physical space,
existence, uniqueness, a constraint-preserving flow or a controlled interval.
It does not automatically justify the weak diffeomorphism Ward products,
radial-multiplier reconstruction, energy identity or their node traces.
Those need additional regularity/chain-rule or variational compactness arguments.
In particular, action-domain membership cannot replace the physical weak IVP.
The planar domain also does not establish general3D physical mode admission.

## 4. Quantified failure of a naive inverse estimate

For the REGISTERED node weight, set xi=k*(z-z_node), k=40,
g=b*e^2*sin(xi)^2, b=5/44,e=1/500. For n>=2 define

    phi(y)=(1-y^2)^4 on |y|<=1, zero outside,
    f_n(xi)=n*sin(xi)^2*phi(n*xi).

Each source is even, vanishes quadratically at the node and has a particular
removable quotient. Exact integrals and |sin(xi)|<=|xi| yield

    ||f_n||L2(dxi)^2 <= 65536/(14549535*n^3),
    ||f_n/g||L2(dxi)^2 = 5767168000000000*n/1989.

Physical z-measure norms squared are these values divided by40. Therefore
unweighted residual size can tend to zero while the divided-rate norm grows
without bound, even with these exact node zeros and reflection parity.
This rules out that naive inverse estimate; it does not rule out a controlled
graph/weighted norm or structural cancellation in the full nonlinear equations.
The sequence is NOT asserted to satisfy the physical constraints or be an
admitted perturbation. It supplies no physical ghost, cutoff or action no-go.
Its arbitrarily high frequencies are not identified with a physical EFT domain.

## 5. Independent controls and reproducibility

Four general metric/frame/scalar jets include nonflat spatial geometry and
nonzero lapse gradient. The full weak density, with its explicit boundary
divergence restored for comparison, agrees with the pinned ORIGINAL coordinate
implementation below5.00e-112 normalized error. All six metric curvature Euler
entries agree with an independent3D Ricci/Einstein variation below5.09e-46;
the lapse curvature variation agrees below9.16e-46. A nonflat conformal
benchmark separately fixes the GammaGamma/divergence signs. Deleting the
curvature lapse flux is rejected on all four jets.

Real first-variation controls agree below1.25e-112. Both exact node orientations
have finite first variations, agreement below1.27e-113, the original dust
multiplier equation and clock momentum, and positive lapse-defined dust.
Two complex steps1e-20 and1e-26,110 decimal working digits and normalized
tolerance1e-18 are retained. These are finite implementation controls, not
outward bounds on an evolved solution.

Backend: Analysis/MasterTests/r4c1_full_weak_action_v1.py, SHA256
330f25196806450238a71459873a3353036fac4ef15cab53da665ecbaa501105.
Audit: Analysis/MasterTests/test_01_r4c1_full_weak_action_v1.py, SHA256
3df13a8c5d550073796c7e94737dfd9591ef6f5326dfdbf74f865eacab7595bd.
Receipt: Analysis/MasterTests/outputs/r4c1_full_weak_action_v1_attempt_01/summary.json,
SHA256 2f4d3404eb587f362ee285b7fe3cfa99bdfcb7be5b643d3f2ff9133fdf84cb27.
Use --output with a fresh directory or --replay with the retained directory;
the latter returns READ_ONLY_REPLAY_EXACT. No earlier source, failed attempt,
sidecar, manuscript or retained PDF is overwritten.

## Next G1 work

Use this full variational system to establish a controlled coupled evolution
and estimates, including curvature, dust and the changing node domain. The
estimate must control the actual source-to-rate graph, interface terms and
constraint products, not just action integrability or small L2 residuals.
Finite Galerkin trajectories alone would still require a continuum/tail and
domain argument. Do not replace the target by another initial-jet checklist.

Methodological source: [Sarbach, Barausse and Preciado-Lopez, arXiv:1902.05130v2](https://arxiv.org/abs/1902.05130v2)
establishes Cauchy formulations for the vacuum two-derivative Einstein-aether
system under specified coupling conditions. Its frame method is relevant
background, but its theorem does not establish an IVP for this coupled
projected-regulator/dust action. No theorem is imported as physical clearance.

PROCEED_PROVISIONALLY for the variational backend and scoped identities.
HOLD_SUBSTANTIVE for the actual weak/graded IVP, evolved constraint/interface
estimates, background admission and time interval, physical modes/window/GR,
identifying matching and numerical prediction. Stage2 INCOMPLETE; Stage3
NOT_ENTERED; MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED;
UVIR-003 IN_PROGRESS; Stage4A CLOSED. No new parent/state adoption, vault
mutation, provider dispatch, publication, commit/push or deployment.
