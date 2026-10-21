# Frozen contract: undivided nodal descriptor and tangent domain

19 October 2026. Unchanged R4C1 Stage2, conditional research only.
Use the live planar Hamiltonian and earlier regulator-node/regularity reports;
do not rerun their completed audits or replace the missing physical spectrum.

## Required result

Construct a force-clock differential-algebraic action that remains defined
at V=0 without inverting V^2. Retain the FULL metric/frame/matter complement,
original cusp, regulator, potential, curvature, dust, weighted lapse flux,
known spatial/global constraints, both charges and mean metric pairs.
Then derive its linearized descriptor and canonical tangent conditions at
the registered nodes. Determine whether its presymplectic map has a uniform
bounded inverse in the ordinary unweighted L2 field norm. Do not identify
matrix rank at a grid node with a global propagating-mode count.

## Algebra and scope

After original independent unit/dust variations and psi=tau, use s=psi_hat>0
as an independent variable and g=b*sqrt(h)*c, c=V^i h_ij V^j. Eliminate only
the nonsingular twelve-velocity R complement. In this gauge psi_i=0:

    E0(s)=sqrt(h)*[(P_y-ell(s))^T R^-1(P_y-ell(s))/2-f(s)]
    Hpsi(s)=<(E0(s)+Edust+partial_z F)/s>
    Theta=Theta_other-g*s*delta Z,  p_Z=-g*s.

Derive this by keeping p_Z+g*s=0 and Z_hat as multiplier in the first-order
action, varying before eliminating p_psi/lapse, and eliminating the pair
without dividing by g. The old spatial/global constraint solution is used
with p_Z=-g*s; no mean, harmonic or charge mode is newly dropped.

The complete two-form is dTheta. In particular retain BOTH -g*ds wedge dZ
AND -s*dg wedge dZ, with

    delta g=b*sqrt(h)*[c*tr(h^-1 delta h)/2
                     +V^T delta h V+2 delta V^T h V].

Check closure and a nonzero rejection witness for omission of dg (including
metric response). The linearized equation is

    Omega_ij delta Xdot^j
      +[(partial_k Omega_ij) Xdot_background^j-Hessian(Hpsi)_ik] delta X^k=0.

Background drift and the full functional Hessian are required; this formula
alone is not a computed spectrum. Do not set drift to zero or declare modes
physical without a valid background and controlled operator domain.

At a node, g=dg=0. The s row is the ALIGNED energy compatibility, not a
prescription to set Z_dot=0. Recover the original aligned momentum p_psi/
sqrt(h)=K_Q*s and original regulator row chi=Z+s div(V)=0 (psi_i=0).
Distinguish auxiliary node equations from the regular-side velocity inverse.

For initial h=I,s=p,V=(0,w(z),0), w(node)=0,wprime!=0, derive the moving-node
tangent identities

    delta p_Z(node)=0,
    delta p_Zprime(node)=-2*b*p*wprime*delta V_y(node),
    delta z_node=-delta V_y(node)/wprime,
    delta p_Zprime+delta z_node*p_Zsecond=0.

The old claim Fprime=0 applies in coordinates normal to the actual moving
surface, not by fixing its old coordinate position. Node-lifting transverse
perturbations must not be excluded by assuming every perturbed frame has
the same alignment surface. Record that issue explicitly.

## Uniform-inverse question with explicit constants

Use an L2-normalized compact scalar-rate variation supported at normal
distance |x|<=epsilon from a registered simple node. Hold the other reduced
coordinates/momenta fixed. Its image under Omega is only g*delta s in the
Z row. On h=I,w=+/-e*sin(k*x), prove

    ||Omega delta s||_2 <= b*e^2*k^2*epsilon^2/sqrt(85)

for the normalized C2 bump (1-x^2/epsilon^2)^3, with normalization integral
I0=2048/3003 and fourth moment I4/I0=1/85. Smooth bumps yield the same
vanishing-bound conclusion. Preserve domain/amplitude restrictions and do
not call this bound a physical cutoff, growth rate or all-formulation no-go.
No bounded inverse on the unrestricted unweighted L2 tangent space follows
if the bound tends to zero. A weighted/mixed-order DAE reduction may still
be possible and requires its own proof and physical window.

## Executable and verification

Freeze source/contract SHA sidecars before running. Fresh receipts and full
read-only exact replay; preserve original files, hashes and failures.
Use the standalone optimizer and bounded Windows-spawn case parallelism.

Implement the partial Legendre block using the original canonical full_blocks
with only the explicit scalar rate replacing the divided inverse, energy
excluding p_psi*s, and exact Y=c*s^2 in the force-clock gauge. Verify those
changes against the original density, never regularize by epsilon or omit
the cusp. Require only C2 cusp information, not a nonexistent cubic tensor.

Check all9 registered parameter cases at nodes, both slope orientations and
nearby regular points, using the original full density at100 digits and
independent quadratic polarization. Include nontrivial coupled velocities
and local curvature/flux controls; they are method controls, not a newly
adopted/evolved global background. Frozen normalized binary64 comparison
1e-8 and high-precision identities1e-45. Test moving and transverse node-
lifting variations, positivity guards and omitted metric/frame two-form
crosses. Evaluate the explicit inverse-bound constants at every family/eta
and independent high-precision bump quadratures at epsilon*k=1e-2,1e-3.

Keep failures, unknowns and parent holds visible. This milestone supplies
an undivided descriptor and a norm/domain obstruction, NOT a solved coupled
physical spectrum, node persistence, arbitrary3D closure, healthy GR or
Stage2 GO. Stage3 matching remains absent. No projection/state adoption,
new action/parent, vault-management write, model/provider/runtime change,
publication, manuscript/PDF/site, commit or push.
