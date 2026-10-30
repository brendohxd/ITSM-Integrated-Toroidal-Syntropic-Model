# Normalized-frame constraint identities and conditional propagation

28 October 2026, Australia/Perth. Conditional; review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE. G1-G6 INCOMPLETE.

## Result and its practical meaning

The smooth off-shell ADM Ward identities are derived for the original R4C1
action in its normalized frame chart, with the vector Euler terms retained.
They supply a conditional constraint-propagation argument in unit lapse.
This replaces a generic Bianchi-only assertion with the actual normalized
variables, density weights, unit-multiplier reconstruction and residual sources.

The accepted V2 calculation passes105/105 exact, covariant-action, original
density-bridge, energy-identity and rejection controls. A fresh recomputation
is byte-exact.167 source pins and digest values remain unchanged. These are
same-author derivations/checks, not independent peer review or physical clearance.

The application to the quartic candidate is still incomplete. It requires an
EXISTING solution of all Euler equations in a class supporting the weak
variational identity and node/interface products. Initial acceleration, jerk,
node jets and sampled dust/phase consistency do not establish that solution
or class. No controlled time interval, actual IVP, physical mode map or
physical validity window is inferred here.

## 1. Geometric chart and the unit multiplier

Use future timelike U and its holonomic unit constraint. On that constraint,

    n^0=gamma/N,
    n^i=V^i-S^i*gamma/N,
    gamma^2=1+h_ij*V^i*V^j.

The unit-chart Jacobian is tangent, and its induced Gram form is positive.
At a spatial point basis h=I its Gram matrix is I-V*V.T/gamma^2; its inverse
is I+V*V.T. The exact full tangent projector is

    J*(I+V*V.T)*J.T=g_inverse+n*n.T.

Thus the three reduced vector equations supply precisely the tangent vector
equation. Write the unreduced vector Euler equation as F_a+lambda_U*U_a=0.
Its radial equation reconstructs lambda_U=U^a*F_a on U^2=-1. Combining
tangent equations with this reconstruction restores the full vector equation;
the radial equation is not silently discarded. The metric-induced variation
of n is included in the pullback of the metric equation. In particular,
delta(g_ab*n^a*n^b)=0 holds under the total chart variation, not by holding
n fixed during metric variation.

For an active infinitesimal diffeomorphism xi^mu the frame variation is

    delta V^i = xi^mu*partial_mu V^i - V^j*partial_j xi^i
                -(N*gamma*h_inverse[i,j]+S^i*V^j)*partial_j xi^0.

The last term is essential: V is not three spacetime scalars. The lapse,
shift and spatial metric transformations are derived from the original
four-dimensional Lie derivatives as well. Exact checks use arbitrary
advection/first jets, nonzero shift and arbitrary N/V at a spatial point
basis h=I. Spatial tensor covariance extends that basis calculation to any
positive h; no planar restriction is used in this algebra.

## 2. Off-shell equations, with density weights and vector sources

Define weight-one Euler densities by

    delta S = integral [E_N*delta N+E_Si*delta S^i
               +E_h^(ij)*delta h_ij+E_Vi*delta V^i+sum_f E_f*delta f].

The symmetric metric sum runs over all i,j: its off-diagonal entry is half
the coefficient for one independent off-diagonal h variation. Use
E_N=-Hperp and E_Si=-C_i, matching the original canonical lapse/shift audit.
The lapse constraint Hperp includes the gamma*h_inverse*pV divergence and
the FULL weight-one matter contribution. It is not physical scalar rho.

Let

    K_ij=(hdot_ij-Lie_S(h)_ij)/(2N),
    X^i=(Vdot^i-Lie_S(V)^i+gamma*h_inverse[i,j]*partial_j N)/N,
    fhat=(fdot-S^j*partial_j f)/N.

The reduced scalar list includes u,v,r,psi,Z,tau,epsilon. The unit multiplier
is reconstructed as above. Off shell, integration by parts gives

    Hperp_dot = partial_j(S^j*Hperp)
      +(1/N)*partial_j(N^2*h_inverse[i,j]*C_i)
      -2*K_ij*E_h^(ij)-X^i*E_Vi-sum_f fhat*E_f
      -partial_j(gamma*h_inverse[i,j]*E_Vi),

    C_k_dot = partial_j(S^j*C_k)+C_i*partial_k S^i+Hperp*partial_k N
      -E_h^(ij)*partial_k h_ij-E_Vi*partial_k V^i-sum_f E_f*partial_k f
      +2*partial_j(h_ik*E_h^(ij))-partial_j(V^j*E_Vk).

Repeated spatial indices are summed. Every term has the appropriate density
weight; no physical-density conversion is omitted. These are off-shell
identities: the Euler residuals remain arbitrary during the derivation.
Deleting the frame's foliation transformation or its divergence term fails
the explicit rejection controls. One must not replace these terms by a
stress assigned from Bianchi balance or impose their vanishing without a
solution of the corresponding Euler equations.

## 3. Conditional zero-constraint propagation, and an error-norm warning

ONLY conditional on an actual solution of all reduced Euler equations, their
unit-multiplier reconstruction, and a valid smooth or sufficiently justified
weak/interface identity, the sources above vanish. For unit lapse N=1,

    C_k_dot=partial_j(S^j*C_k)+C_i*partial_k S^i,
    Hperp_dot=partial_j(S^j*Hperp)+partial_j(h_inverse[i,j]*C_i).

For a periodic regular solution permitting the energy integration by parts,
spatially Lipschitz S and time-integrable coefficient bounds yield

    d/dt ||C||L2^2 <= [||div S||infinity
                       +2||sym(partial S)||operator,infinity]*||C||L2^2.

Gronwall gives C(t)=0 from C(0)=0 within that class. Once C=0,

    d/dt ||Hperp||L2^2 <= ||div S||infinity*||Hperp||L2^2,

and Hperp(0)=0 propagates. These are conditional constraint estimates, not
field-evolution estimates. They do not establish the required regularity
for the registered quartic construction. Extension to weak solutions needs
the relevant traces/products and energy identity; arbitrary distributions
are not covered simply by naming an L2 space. General spatially varying
lapse is retained in the off-shell equations but is not covered by this
particular sequential unit-lapse estimate.

A combined approximation estimate using only L2 momentum error is NOT
obtained: the Hamiltonian source differentiates C. Even the frozen N=1,
S=0,h=I subsystem has C_dot=0,Hperp_dot=div C. Taking a periodic component
C_z=sin(nz)/sqrt(n) gives ||C||L2 tending to zero while ||div C||L2 grows
like sqrt(n). This is a mathematical rejection control for that norm,
not a full-action physical instability or no-go result. Approximation
control needs spatial derivatives of C, a suitable mixed/graded norm or
another justified formulation. No such complete field-IVP estimate is
claimed by the present result.

## 4. Actual action controls and preserved failed attempt

The new covariant density uses all four ORIGINAL frame invariants in U,
its unit multiplier, normalized n/projector in the alignment/force/regulator,
canonical scalars and full potentials, original conformal dust/multiplier,
and the Einstein-Hilbert Ricci scalar. It retains metric first/second jets,
Christoffels and the metric dependence of n and its derivative. Four general
off-unit timelike jets include general nonzero first/second/third diffeomorphism
jets at a fixed point. Both complex steps1e-20 and1e-26 use110 decimal
working digits and the frozen normalized tolerance1e-18.

Sector-by-sector density Lie variations agree with the required divergence;
the largest normalized residual is below8.06e-43. Unit-chart non-gravity
contractions agree with the pinned original coordinate implementation below
4.04e-112. Omitting the inhomogeneous vector first-jet term produces
normalized mismatches exceeding4.62e-5. These finite numerical controls
check the implementation, not arbitrary-field theorems by sampling. The
analytic identity uses the covariant action and exact chart/Noether algebra.
Covariance alone cannot identify an action, hence the original-term inspection
and separate contraction bridge are retained.

The off-unit Lie controls have ell>=7/6 and strictly positive Y; the density
bridges use ell=1. These controls do NOT prove
analyticity at Y=0 or a weak interface theorem. Einstein-Hilbert curvature
is checked covariantly; the ADM/GHY difference is a boundary divergence for
the smooth compact-interior/periodic variations used here. No internal node
surface term is discarded in a weak extension. An explicit component-by-
component stress-tensor export and general3D constraint Poisson-algebra audit
are not supplied by these Lie controls.

V1 failed100/104: its symbolic vector-chart Jacobian held temporary gamma
fixed when differentiating with respect to V. Its four unit-tangent/Gram/
projector/multiplier checks detected the error; the Lie/transport equations
and covariant density controls passed. V1 and its exact failed replay remain
unchanged. The separately frozen V2 uses

    J_total=partial_V(n)|gamma+partial_gamma(n)*V.T/gamma

at h=I and adds a frozen-gamma rejection test. No action, Ward formula,
point, precision or tolerance was changed to obtain105/105.

## 5. Reproduction and next substantive requirement

Executables: Analysis/MasterTests/test_01_r4c1_normalized_adm_ward_v1.py
and test_01_r4c1_normalized_adm_ward_v2.py. Accepted V2 source SHA256:
0c040f9ca4ca76ec31835fda7b8ab25273eb3e33997beb4680b5453bc6d2f912.
V1 contract and V2 chain-rule addendum are dated28 October2026.

Receipts under Analysis/MasterTests/outputs/:

| Receipt | SHA256 |
| --- | --- |
| r4c1_normalized_adm_ward_v1_attempt_01/summary.json (failed) | d3e6afd41a995c2f2ef5144f2b14b5a4ae6d990d50063856972d7d2194ccd9a9 |
| r4c1_normalized_adm_ward_v2_attempt_01/summary.json | 3ee19a8c481126be7bbf18fb0084893da9ff203721d613e526f157add91076e4 |

Use --output with a fresh directory or --replay with the retained directory.
Both versions reproduce their exact scientific bytes; V1 still exits2 for
its failures, V2 exits0. No original scientific source, failed attempt,
sidecar, retained PDF or manuscript is overwritten.

The next G1 task is the ACTUAL evolved weak/graded formulation and estimates
at the rank-changing nodes: show that the full Euler equations possess a
solution in a class where the above products, interface identities and
constraint estimates apply. Retain all fields, evolving frame/basis, dust,
regulator, torus means and charges; do not evolve on an imposed slow graph.
Check initial compatibility in that formulation and solve genuinely free
continuation data if required. More sampled agreement or finite time jets
alone will not meet that requirement.

PROCEED_PROVISIONALLY for the smooth structural identity and stated conditional
constraint estimate. HOLD_SUBSTANTIVE for its actual weak application,
background admission, IVP/time interval, physical modes/window/GR, identifying
matching and numerical weak-field prediction. Stage2 INCOMPLETE; Stage3
NOT_ENTERED; MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED;
UVIR-003 IN_PROGRESS; Stage4A CLOSED. No new parent/state adoption, vault
mutation, provider dispatch, publication, commit/push or deployment.
