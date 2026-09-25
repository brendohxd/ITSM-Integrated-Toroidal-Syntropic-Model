# R4C1 full classical variation / Ward checkpoint contract

Date: 2026-09-25. Action: R4C1-v1, unchanged.
Action SHA256: `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3`.
Status: `CONDITIONAL_CHECKPOINT_CONTRACT`; gate effect: `NONE`.

## Purpose

Continue the approved four-dimensional candidate toward Master Test 1 by
deriving its complete frame and connection-dependent metric variations.
Do not replace the action with a homogeneous ansatz or an easier scalar
witness. The previous scalar checkpoint remains evidence in its own scope.
This is classical variation, not quantum renormalization or parent adoption.

Use the first-order auxiliary action exactly as frozen. Independent variables
are the covariant metric g_ab, contravariant U^a, all frozen scalar fields and
multipliers. Let V_a^b=nabla_a U^b. Define partial derivatives of the scalar
Lagrangian holding g,U,V and scalar covariant gradients independently fixed:

```
P_c^a = partial L / partial V_a^c,
F_c = partial L / partial U^c,
B^{ab} = partial L / partial g_ab.
```

The use of covariant metric variation must be reconciled explicitly with the
inverse-metric stress convention in the first report. The connection term
from delta(nabla U) must not be omitted. Scalar equations, the constraint
equation, and all sector allocations must use the same action.

## Verification registered before the executable

1. Derive explicit P, F and B for the four frame invariants and normalized
   projector/acceleration regulator, including metric-induced changes in n.
2. Compare them with direct symbolic differentiation in all 16 V directions,
   four U directions and ten symmetric metric directions. Use a nonunit
   timelike U=(10/3,8/3,0,0) and a nonzero-gradient force jet. Couplings remain
   symbolic in these component checks. These pointwise tests supplement,
   rather than replace, the general tensor derivation.
3. Verify the coefficient of every metric-derivative variation using arbitrary
   symbolic delta g_ab and its first derivatives. Integrate by parts with
   the frozen boundaries to derive the connection contribution to stress.
4. Independently evaluate the resulting complete stress and Euler equations
   using exact rational Taylor jets of all fields and metric through degree
   three in four coordinates. Differentiate them to check all four components
   of the **off-shell** diffeomorphism Ward identity. Do not set the vector
   equations to zero by assertion, use Bianchi to assign a current, or impose
   a minisuperspace ansatz.
5. For reproducibility use dense polynomial coefficient seeds 4101 and 4102,
   numerators in [-2,2] over 20. Constant metric is diag(-1,1,1,1), with
   nonzero metric derivatives allowed. Seed 4101 uses U=(2,0,0,0), dpsi=(1,2,2,1);
   seed 4102 uses U=(10/3,8/3,0,0), dpsi=(-1,2,2,1). Thus ell=2, Y=9 at
   the expansion point. Use psi=0, (u,v,r,z,epsilon,lambda_U)=(1,2,1,1,2,1),
   tau=0 and dtau=(2,1/2,0,0). These are arbitrary off-shell local probes, not
   physical parameter fits or solved backgrounds. Their open neighbourhood
   has Lorentzian metric, timelike frame, timelike dust gradient and Y>0.
6. Fix nonzero rational probe coefficients: M_U^2=2/3; (c1,c2,c3,c4)=
   (1/5,-1/7,2/9,3/11); K_Q=3; A=2/7; b=5/11; zeta=1/13; beta=2/5;
   g_r=3/7; m^2=1; lambda_4=1/3; lambda_6=1/5; Lambda=2;
   m_r^2=2; lambda_r=1/7. They are not a healthy-spectrum claim.
7. Separately check the matter, reservoir, plenum and summed Ward identities,
   retaining scalar and vector equation residuals off shell. Test wrong
   connection-stress signs, omitted connection stress, and omission of the
   vector terms using explicit nonzero exact residuals.
8. Validate the Taylor arithmetic against independent symbolic expressions,
   not just the identity being tested. Demonstrate deterministic reruns and
   immutable action/contract hashes. Any unresolved residual fails the local
   checkpoint; do not repair it by tuning these registered jets or couplings.

## What a pass can and cannot establish

A pass would support the complete **classical conditional candidate**
variation and its conservation structure. Numeric exact jets cannot prove a
universal identity alone: accompany them with the general variation ledger.
They do not provide global T3 boundary/initial data, a finite-charge solution,
the physical constraint spectrum, healthy continuous GR recovery, a quantum
effective action, microscopic coefficients, or independent Rule-9 review.
The earlier zero-gradient force regularity boundary remains as documented;
the present higher-derivative jet checks are on Y>0, not a smoothing at Y=0.

All canonical statuses remain unchanged: Test 1 open; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
Rule9 NOT_CLEARED; physics_pass=false. TOP-X4 is untouched.
