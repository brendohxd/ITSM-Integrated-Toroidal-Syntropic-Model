# R4C1 scalar/regulator range: a precise physical-domain obstruction

27 October 2026. Result ID R9-MT1-PHYSICAL-SECTOR-RANGE-V1.
Deliverable B, unchanged R4C1; Conditional bounded range/normalization analysis.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Result and its physical meaning

The retained two-form gives an explicit local canonical momentum p_Z=-g*s and
two cross-corrected source divisibility conditions. In the selected tilted
reference profile, g has quadratic zeros at BOTH alignment nodes. For C2 scalar
sources in an unweighted L2 evolution-rate chart, their values AND first spatial
derivatives must vanish at each node. Merely solving a nodal value equation is
insufficient. Moving those conditions adds background and node-transport terms.

This identifies exactly what an admission calculation for the negative scalar-rate
directions still owes. It does not show that those directions pass or fail the
actual evolving constraints. A regular-patch canonical change preserves the
negative curvature of a direction already admitted, but cannot supply admission
or turn the warning into a physical ghost theorem. The full physical tangent
space, physical normalization and frequency/window remain UNRESOLVED.

The unweighted L2 chart below is a declared diagnostic space, not a derived
physical norm. Weighted/mixed-order physical spaces are not excluded. The result
is an obstruction to inferring physical clearance from the supplied partial
inverse, nodal Schur tables and restricted Hessian, not a rejection of R4C1.

## 1. Exact range equations with all canonical crosses retained

Use the owning action's one-form in its retained canonical quotient chart:

    Theta = <P_a dQ^a - g(Q) s dZ> + PM dM,
    g = b sqrt(det h) V^T h V.

Here canonical configuration coordinates include the metric/frame local and
mean coordinates; spectator matter/scalar coordinates remain in their canonical
blocks. Dg is the full differential/Frechet derivative, not a derivative holding
the metric means fixed. Existing spatial/global constraints, charges, translation
section and chart restrictions are inherited, not solved again or deleted.

For a covector r in that chart, Omega v=r gives, with means included in the same
canonical pairing and spatial covectors interpreted in the owning average-L2
convention,

    v_Q = r_P,
    Phi_s = r_s,
    Phi_Z = r_Z - s Dg[r_P],
    v_Z = -Phi_s/g,
    v_s = Phi_Z/g,
    v_P = -r_Q + s (Dg)^* (Phi_s/g).                 (1)

The star is the adjoint into all retained canonical momentum/mean rows. In local
coordinates it is multiplication by the corresponding g derivative. The abstract
form retains nonlocal/restored quotient effects in r and its canonical projection;
it is not a license to discard them. Existing tests for Phi in
material_seed_feasibility_v1.py implement precisely this full cross correction.

For the perturbation problem the REQUIRED source is

    r = K u,  K u = Hessian(H) u - dOmega[u] Xdot.    (2)

No static Hessian substitution is made. The exact closed-two-form identity is
K-K^T+Omega_dot=0 when H has symmetric second variation and Omega_dot=dOmega[Xdot]
in this formulation. The method checks retain its nonzero drift. They do not
verify an exact evolving on-shell background for the stored R4C1 reference jet.

For bounded smooth coefficients and canonical source components, and subject
to the inherited quotient conditions, (1) shows that the scalar inverse requires
Phi_s/g and Phi_Z/g in L2. These are conditions for this range problem, not the
complete physical constraint surface or its temporal persistence.

## 2. Both-node criterion and explicit local constants

The frozen reference sector is new_B1_frame, eta=1/4, e=1/500, k=40,
theta=kz, w=e cos(theta), positive b, flat initial spatial metric. Neither b nor
the family coefficients are newly identified microscopic inputs. The exact
implicit initial construction remains distinct from rounded stored representatives.

Let x=z-z_* near EITHER node z_*=(pi/2+j*pi)/k. Then

    g=b e^2 sin(kx)^2.

For |kx|<=pi/2, elementary sine bounds give

    (4/pi^2) b e^2 k^2 x^2 <= g <= b e^2 k^2 x^2.   (3)

Thus, on a one-node neighborhood, whenever the norms exist,

    ||Phi/x^2||_2/(b e^2 k^2)
        <= ||Phi/g||_2
        <= pi^2 ||Phi/x^2||_2/(4 b e^2 k^2).         (4)

Choose disjoint neighborhoods of the two nodes and the compact complement, where
g has a positive minimum. For Phi in C2 on the circle, Taylor's formula proves

    Phi/g in L2 iff Phi(z_*)=partial_z Phi(z_*)=0
    at BOTH nodes.                                 (5)

Necessity: a nonzero constant or linear Taylor term divided by x^2 is not L2.
Sufficiency: the two zero traces imply |Phi|<=C*x^2 locally, so (3) bounds the
quotient; the complement is regular. Apply (5) separately to Phi_s and Phi_Z.
The node values of g and its first field differential vanish there, but this
does not identify a Hilbert-space kernel with a pointwise null row.

C2 matters: Phi=|x|^(3/2), localized by a smooth cutoff, is C1 with zero value
and first derivative at the node, yet |Phi/x^2|^2=1/|x| is not integrable.
For lower regularity retain the weighted divisibility condition itself. No
smoothness or unweighted norm is imposed as a theorem of the full physical theory.

The periodic controls cos(theta)^2 and sin(2theta) distinguish double and simple
zeros at both pi/2 and 3pi/2. These are method examples, not actual r=K*u values
for the stored negative-curvature probes. No such probe is admitted by them.

## 3. Moving constraints: what first material balance does and does not prove

For a smooth moving simple alignment node z_*(t) and the actual linearized source
Phi(t,u(t)), define C0=Phi|_* and C1=partial_z Phi|_*. Persistence requires

    dC0/dt = [(partial_t Phi)[u] + Phi[udot]
                  + zdot_* partial_z Phi]_* = 0,
    dC1/dt = [partial_z((partial_t Phi)[u]+Phi[udot])
                  + zdot_* partial_z^2 Phi]_* = 0.  (6)

Explicit clock dependence, background change and the two-form drift in K remain.
The method control Phi=(x-t)^2 has partial_xt Phi=-2 and partial_xx Phi=2;
zdot_*=1 cancels them. Omitting node transport would incorrectly reject it.

The earlier first-material cancellation for amplitude-momentum seeds is retained.
It is neither erased by a frozen D(A^2) warning nor extended to the scalar-rate
energy probes. No higher hierarchy or exact nodal trajectory was constructed here.

## 4. Local canonical map and the energy warning

On a regular g>0 patch, set p_Z=-g*s. This makes Theta exactly the canonical
one-form, with the full differential

    delta p_Z = -g delta s - s Dg[delta Q].          (7)

Its scalar Jacobian factor is -g; the transformation has no inverse at alignment.
The metric/frame crosses in (7) are essential. For a fixed-configuration path
and fixed independent canonical momenta, g is constant along that path and
delta p_Z=-g*f. The second directional variation is therefore the same quadratic
form expressed in new variables: a local H_ss curvature corresponds to
H_pZpZ=H_ss/g^2 in the one-coordinate notation. This identity is along the stated
path, not a claim about the entire coupled Hessian or a physical pole.

Consequently this canonical change cannot make the negative restriction positive
by normalization. It also does not prove that the direction survives constraints,
that the clock Hamiltonian is a physical positive-control energy, or that a
negative value gives exponential classical growth. The global map and physical
mode count require the missing domain/admission analysis. Do not take |H| as a cure.

## 5. Verification and limits

Primary exact SymPy controls: 23/23, no failed/unknown checks. Independent
full-metric one-form finite-difference controls: V2 27/27, no failed/unknown checks.
Three positive-definite local metrics, nonzero frame vectors, all canonical
directions and both steps 1e-5,1e-6 were retained at 70-digit working precision.
The largest normalized two-form, inverse and drift-balance discrepancies were
about 1.012e-13, 1.806e-13 and 7.508e-13 respectively, below frozen 1e-8.
Deletion of canonical crosses and drift was rejected. Alignment null rows were
checked separately. These are local algebra/method controls, not three physical
backgrounds, a new full R4C1 evolution run or independent peer review.

Independent V1 failed before its first check because a square matrix was allocated
for a vector. Its source, sidecar and traceback remain. V2 changes that allocation
and docstring only, as documented in the implementation note. Neither equation
nor criterion was changed. Both successful executables were freshly recomputed
with READ_ONLY_REPLAY_EXACT; original receipt bytes were not rewritten.

| Artifact | SHA256 |
|---|---|
| Readiness contract | 431bbe4379aa756d0b22dd7c15ede57d48f6909bc3c9f7ea349442da1e1ca7fc |
| Range addendum | 2d5ca5d9df66cdffcb74ae3392dbcde575af743928063d2315fc5f10054635db |
| Primary executable V1 | 2ed789f136172dfcd2a57bfa6a04bef1d2dbb54bcc18795d1178e13984a6b012 |
| Primary summary | 3c671c7b55b2ce97a5457ab701ca5c0c439395f81b616a47f052ca6f9bb08dc8 |
| Independent V1, preserved failure | 0ae15599da93a33e3cd54c8618c6451e4dfd25c827c88517b38918c44c14cc04 |
| Independent V2 | ff41a169b3f141c8f9d6ebcc1bd11bbec14db59bae3d6b8e0934f0c73cc98461 |
| Independent V2 receipt | 4cab0ad482336d047b1b0040190bc1f458a39b19e2a97deeac84a20d1575d29d |

Primary directory: Analysis/MasterTests/outputs/r4c1_physical_sector_range_v1_attempt_01/.
Independent directory: Analysis/MasterTests/outputs/r4c1_physical_sector_range_independent_v2_attempt_01/.
Source dependency hashes and package versions are in the receipts. The source
owners and exact inherited pins are listed in the readiness contract. Those
upstream scientific pipelines were not rerun for this calculation.

## 6. Precise obstruction and stopping decision

Physical classification of the warning probes requires their ACTUAL full sources
K*u on a sufficiently controlled admitted background, a justified physical domain
(possibly weighted/mixed-order), both-node divisibility and its temporal
consistency, plus the normalized reduced coupled structure on that domain.
The supplied partial inverse and sampled nodal Schur blocks do not give these
objects; the source owners explicitly leave full admission/persistence open.
The present range lemma does not supply them either.

There is therefore no justified healthy-mode or ghost verdict. The bounded task
ends with an explicit range criterion and this substantive domain/background
obstruction, not a manufactured physical pass or an all-action no-go. Reusing the
range lemma provisionally is allowed; using it as physical clearance remains
HOLD_SUBSTANTIVE. No automatic additional hierarchy, spectrum or parent is opened.

Inherit original action/variation, nodal/global reduction, tangency/descriptor,
initial-admission, partial-Legendre, scalar-energy and material-seed review debts.
All are DEFERRED, not cleared. Stage1 retains only registered prepared-dust scope;
Stage2 INCOMPLETE; Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED.
No manuscript/site edit, publication, vault mutation, new state/action, commit,
push, model/provider dispatch or global runtime change occurred.
