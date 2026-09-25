# R4C1-S1: interacting scalar constraints and kinetic diagnostic

Date: 2026-09-25. Owner: Master Test 1, conditional R4C1-v1 branch.
Status: FROZEN_BEFORE_EXECUTABLE. Gate effect: NONE.

## Scope and immutable inputs

Derive the classical scalar quadratic action on the B1 expanding background,
including the metric and dust constraints. A fixed-metric scalar Hessian is
not the requested object. Do not change B1 parameters, initial data, topology,
the action or acceptance tolerances to improve a result.

Pin these inputs in the executable:

- R4C1 action: `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3`.
- B1 executable: `1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f`.
- Full-variation executable imported by B1: `aa62287597554b3292f9186c815d0f3b2bcb4c1e7496a52af1db07af6a857dd0`.
- B1 receipt: `e7a9e0cbaf64657153ce497abf1b3ceb90c0722822a1913f94d5c7726176a9d7`.
- B1 trajectory: `0024b7307de64d780aca3d47401fc8175d59baa354d53912b80ab6842d346daa`.

Inherit R9-MT1-VARIATION and R9-MT1-B1 as unreviewed provenance. Review is
DEFERRED under ITSM_RULE9_DEFERRED_REVIEW_POLICY.md. This calculation proceeds
provisionally without reviewer dispatch, not as final gate clearance.

## Chart and reduction

Use signature -+++, natural units and B1 reference units. Spatial coordinate
periods are one. Work in spatially flat scalar gauge, with

```
ds^2 = -N^2 dt^2 + a^2 (dx + S dt)^2 + a^2 dy^2 + a^2 dz^2,
N = 1 + alpha,
U^0 = sqrt(1+w^2)/N,
U^x = w/a - S sqrt(1+w^2)/N, U^y = U^z = 0.
```

The exact parametrization eliminates only the regular unit-frame holonomic
constraint and its multiplier, retaining the longitudinal frame variable w.
Verify normalization and inverse metric to quadratic order. The temporal
gauge requires H != 0; the spatial scalar gauge requires k != 0. Do not take
H=0 or k=0 limits as physical reductions in this chart. Rotational symmetry
of the background permits a wavevector along x for the local Fourier symbol;
registered torus samples have integer wavevectors (n,0,0).

Use sqrt(2) cos(kx) for delta u, delta v, delta r, delta psi, delta tau,
alpha, delta epsilon and z; sqrt(2) sin(kx) for w and S. Thus each squared
basis function has unit spatial average. Set k=2*pi*n, not k=n.

Keep q=(delta u,delta v,delta r,delta psi,delta tau,w), their time derivatives
and y=(alpha,S,delta epsilon,z). Derive every quadratic block before solving
the four auxiliary equations. Do not impose the dust constraint on the
original matter action before varying; its multiplier equation is essential.
Retain frame connection terms, the alignment term and the auxiliary regulator.
The cubic |projected grad psi|^3 is C^2 at the aligned background and has
zero quadratic contribution, not an inserted ordinary gradient term.

Derive and publish matrices in the convention

```
<L^(2)>/a^3 = 1/2 qdot^T K qdot + qdot^T M q - 1/2 q^T V q
```

after elimination, along with the pre-constraint Hessian and auxiliary
solutions. These are time-dependent coefficient matrices; eigenvalues of V
alone are not mode frequencies. The equations are

```
K qddot + (Kdot + 3H K + M - M^T) qdot
         + (Mdot + 3H M + V) q = 0.
```

Identify the auxiliary determinant/rank domains before any inverse, including
vanishing regulator coefficient, wave number or frame combinations. Singular
domains need a new constrained treatment, not a pseudoinverse or epsilon fix.

## Registered checks

1. Exact inverse-metric and unit-frame identities through quadratic order.
2. Derive all four frame invariants from the metric connection, checking the
   B1 homogeneous action and absence of lapse/shift velocities in the final
   scalar quadratic density. Independently check the H=0 fixed-metric frame
   density; this last check is algebraic, not the physical H=0 scalar sector.
3. Derive the linear regulator operator from its covariant definition; check
   that auxiliary elimination yields -b (delta Delta_psi)^2/2. Check the dust
   multiplier equation from the uneliminated series, including conformal terms.
4. Check the canonical scalar, force and alignment expansions against direct
   expansions of their covariant/ADM densities. Use Cartesian u,v throughout.
5. Solve every auxiliary equation; require exact zero residuals. Compare direct
   substitution and the Schur complement. Check symmetric K and V and identify
   all remaining modes without inferring a ghost from the auxiliary signature.
6. Independently evaluate the full first-derivative frame density on perturbed
   jets and compare its central second difference to the quadratic formula.
   Use epsilon=(1e-3,5e-4,2.5e-4), fixed deterministic jets and relative error
   normalized by max(1,abs(expected)). Require finest error <1e-5 and decreasing
   errors, or explain a roundoff plateau without changing the tolerance.
7. Negative controls must detect wrong regulator sign, omission of the frame
   contribution to delta Delta_psi, premature removal of metric constraints,
   and incorrect unit-frame normalization.

Generate matrix formulas in a machine-readable artifact. Different field
dimensions mean raw eigenvalue magnitudes depend on the specified reference
chart. Inertia, not those magnitudes, is the meaningful no-ghost diagnostic.

## Numerical domain and decision rules

Reuse the pinned B1 trajectory (801 samples, t in [0,4]). Independently
reintegrate the same equations with Radau, rtol=1e-11, atol=1e-13; require
maximum component difference/(1+abs(reference)) <1e-7. Evaluate n=(1,2,4,8)
on both trajectories. Record physical k/a, K eigenvalues, inertia and auxiliary
conditioning. Classify eigenvalues only outside +/-1e-9*max(1,||K||_2); smaller
ones are UNRESOLVED, never counted as positive by fiat. Require numerical
symmetry and Schur/substitution agreement to relative 1e-9. A significant
negative reduced eigenvalue is a ghost diagnostic for that candidate and
domain. A positive result means only no detected negative kinetic mode on
these samples, unless separately strengthened by an exact algebraic proof.

Preserve failed checks and distinguish implementation validation from physics
outcomes. If reduction is incomplete, publish that fact rather than substituting
a metric-frozen calculation. Do not integrate perturbations or claim gradient,
mass, hyperbolicity, quantum/EFT, all-time or all-mode stability in this task.
B1 has no demonstrated EFT hierarchy, so numerical wavelengths are formal
classical probes, not certified physical observational scales.

Parent holds remain: MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED;
V NOT_COMPUTED; Stage4A CLOSED; Rule9_cleared=false; physics_pass=false.
No canonical Derived promotion, commit, push or publication is authorized.
