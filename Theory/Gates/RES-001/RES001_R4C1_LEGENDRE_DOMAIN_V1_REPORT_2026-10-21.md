# Uniform partial Legendre chart on the registered configuration family

21 October 2026. Unchanged R4C1 Stage2; version1. Local203/203, no failed or
unknown checks; complete fresh read-only replay exact. This is an off-shell
chart-domain result, NOT physical stability, a Cauchy theorem or healthy GR.

## Meaning first

The full twelve-velocity partial Legendre matrix R is invertible for ALL
0<eta<=1 and |w|<=1/500 in each of the three frozen families, on
h=I, V=(0,w,0), u=r=sqrt(eta), v=0. This covers every value of the registered
small-tilt profile, including its alignment nodes, not just a spatial grid.

The conclusion is about this complement, not the scalar-rate/regulator sector.
It does not repair the vanishing g=b*sqrt(det h)*VhV two-form coefficient.
It is compatible with the earlier finite-node unweighted-inverse obstruction.
No new physical background, state, evolution or microscopic matching is adopted.

## Reconstruction from the unspecialized action

The proper velocities are six symmetric K_ij components in order
(00),(01),(02),(11),(12),(22), three frame X^i, and u_dot,v_dot,r_dot.
Before any family substitution, construct the original normalized-frame
quadratic density. With gamma=sqrt(1+w^2), V=(0,w,0), a=X+KV:

    B00 = V.a/gamma; B0j = a_j;
    Bi0 = (KV)_i; Bij = gamma*Kij;
    G = diag(-1,1,1,1); n=(gamma,0,w,0); acceleration=B^T*n;
    Lframe = -MU2/2 * [c1*tr(G B G B^T) + c2*(tr B)^2
                        + c3*tr(B^2) - c4*acceleration^T G acceleration];
    LADM = MP2/2 * [tr(K^2)-(tr K)^2];
    Lscalar = (u_dot^2+v_dot^2+r_dot^2)/2 - zeta*R2*w^2*v_dot^2/2;
    R = Hessian_y(LADM+Lframe+Lscalar).

All metric/frame velocity crosses and symmetric-component factors are retained.
An exact symbolic control adds arbitrary velocity-independent 4x4 shifts to B,
then retains the original regulator's acceleration term, scalar spatial
gradients, force, potential and spatial curvature. The Hessian of the additional
remainder is exactly zero. Thus those spatial/affine/constant pieces do not
change this partial temporal Hessian. They were not deleted from the independent
original-density point controls and are NOT declared irrelevant to dynamics.

The frozen planar-vertices parameter maps are substituted only AFTER this
generic differentiation. They are diagnostic choices, not identified microscopic
coefficients. In particular their inserted K_Q=3*eta is not a derivation of K_Q.

## Aligned inverse, signs and the singular endpoint

Define a=1-alpha13, Bc=1+alpha2 and D=2+alpha13+3*alpha2=3*Bc-a.
At w=0 the diagonal-K block is a*I3-Bc*J3, the off-diagonal-K block is
2a*I3, the frame block is (eta/6)*I3, and the scalar block is I3.
The executable verifies a complete exact eigenbasis, with eigenvalues

    a (twice), 2a (three times), -D (once), eta/6 (three times), 1 (three times).

Exact nonnegative Bernstein coefficients on eta in [0,1] prove, family by family:

    a>=7/8; D>=11/6; 65/72<=Bc<=16/15; D-Bc>=29/36.

The inverse of the diagonal-K block is I3/a-Bc*J3/(a*D). Its absolute row sum
is (D+Bc)/(a*D), bounded above by

    (8/7)*(1+(16/15)/(11/6)) = 696/385 < 2.

The remaining inverse rows are 1/(2a), 6/eta and1. Consequently the exact aligned
infinity norm is ||R0^-1||_infinity=6/eta for0<eta<=1. The unreduced partial
inertia is11 positive,1 negative,0 zero. The negative metric-conformal direction
is retained; this inertia is NOT a physical ghost classification.

At eta=0, for every w in the declared range, R has rank9 and three frame-velocity
null directions. R0^-1 does not extend there. A bound proportional to1/eta is
not a uniformly nonsingular GR-endpoint theorem or proof of GR failure.

## Whole-rectangle interval certificate

Form T=R0^-1*(R-R0) in exact symbolic arithmetic and cancel removable eta factors.
Every T entry has a finite eta=0 extension; only this extended T, not the inverse,
is evaluated at that endpoint. Use the contract's FIXED16 equal eta boxes on[0,1]
and8 equal w boxes on[-1/500,1/500], at80 decimal interval digits.

The recursive evaluator admits exact integers/rationals, sums/products, integer
powers and real square roots. It rejects binary64/SymPy Float coefficients,
unsupported functions and zero-containing denominators. All basic interval
operations have independent exact-Fraction endpoint controls. The recipes use
integer endpoints divided by exact integers; no lambdify float path is used.
The receipts retain all128 boxes/family, all12 absolute-row-sum enclosures/box,
exact dyadic rational endpoints and upward rational beta ceilings.

| Family | Exact beta ceiling | Bound ||R^-1||_infinity <= C/eta |
| --- | --- | --- |
| archived_G3 |187521/31250000 =0.006000672 | C=187500000/31062479, about6.03622138465 |
| new_B1_frame |4801603/1000000000 =0.004801603 | C=2000000000/331732799, about6.02894861777 |
| new_hierarchical |480179/100000000 =0.00480179 | C=600000000/99519821, about6.02894975062 |

For each family, sup||T||_infinity<=beta<1, so the convergent Neumann series gives
R^-1=(I+T)^-1 R0^-1 and C=6/(1-beta). All three also satisfy the convenient
common bound ||R^-1||_infinity<=200/(33*eta). This norm belongs to the declared
velocity component chart, not a canonically normalized physical energy space.
Continuity and symmetry along the connected w interval, with certified
nonsingularity, preserve the aligned11-positive/1-negative inertia.

These are executable enclosure proofs conditional on the exact reconstruction
and installed outward arithmetic, not proof-kernel verification. All installed
mpmath Python sources and version1.3.0 are recorded. The primary
[mpmath interval documentation](https://mpmath.readthedocs.io/en/latest/contexts.html#arbitrary-precision-interval-arithmetic-iv)
explains enclosure arithmetic and warns that support is experimental. That live
page documents a development version, not the installed version: the certificate
uses the pinned local implementation and its bounded primitive controls.

## Independent controls, replay and preservation

Nine owned Windows-spawn jobs cover three families and eta=1/4,1/64,1/1024;
each covers w=0,+/-1/500,+/-1/1000, for45 configurations. Direct quadratic
polarization of the pinned ORIGINAL list-contraction density retains nonzero
metric/frame/scalar spatial jets, Z, scalar rate, curvature, regulator and
potential. All78 independent Hessian entries are compared per configuration.
The original parameter loader retains its90-digit conversion; density arithmetic
uses100 digits and the frozen normalized comparison criterion is1e-55.

The largest normalized entry discrepancy is about8.3333400005e-92; the largest
quadratic third-difference residual is about1.7859177989e-101. Signed nonzero
tilts reject deletion of the metric/frame cross block. Point agreement checks
the independent formula; it is not the whole-rectangle proof.

All203 local checks pass. A complete fresh read-only replay, using8 rather than
the first run's9 workers, reproduces all three JSONs and sidecars byte-for-byte,
returns exit0 and prints READ_ONLY_REPLAY_EXACT. There are109 source pins and
307 native source/runtime metadata records. The separate raw-integer guard
matches722 records and37 pre-existing/new output-directory file sets exactly
across replay: no changed, added or missing record. Earlier timestamp transport
limitations remain documented; no historical file/sidecar was rewritten.
An initial optimizer display-budget invocation was rejected before the first
scientific command launched; retrying its permitted display size changed no
equation, input, threshold or frozen source.

| Artifact | SHA256 |
| --- | --- |
| Contract |9d1b8d95e54e1527d2df0dd68264f0cfeb3b780f032cb8729ce756730e1663d2 |
| Executable |8b2b229d4b180533a03cbf4fed4869742597098e14cf9828d08d88c2ac3df3cc |
| summary.json |94d038eadc170d02e428d5d2be5bc30e0296922c91bcf6b4f31aa966f0368d3b |
| independent.json |0be6a20e308e5a69ba289a20e8c0049864cea95fad2adcf32a7b02d3552d9901 |
| formulas.json |9e66f66868a3bc1ab83b016cd90aedacae56d86a7c37b982ea8d9aff1706ffae |
| Fresh replay log |c55a15551db15c648a03b9626da4808a621e439b4ca3a2132249376ff12cbd25 |
| Raw post-replay guard log |242346ce70bf8662f61b8900e6fe660e245a5f55e636858b765e68df7264d709 |

Executable: Analysis/MasterTests/test_01_r4c1_legendre_domain_v1.py.
Receipts: Analysis/MasterTests/outputs/r4c1_legendre_domain_v1_attempt_01/.
Both --output and --replay accept --workers1..16; there are only9 independent
point jobs and interval evaluation stays serial in the parent context. Only
the parent writes new receipts; replay writes none. Private runtime logs and
raw snapshots remain ignored. No speedup or billed-token savings are inferred.

## Next route and unchanged physical disposition

Use this partial-chart certificate as an input to deriving/testing the actual
weighted or mixed-order physical energy/perturbation space. The scalar/regulator
nodal degeneracy, both continuum-node traces, full auxiliary hierarchy and
persistence, full coupled physical modes/characteristics, nonlinear interaction
window/cutoff and justified healthy-GR recovery remain unresolved. The saved
full372 spectrum continuation is still incomplete; it was not advanced here.
Neither identifying matter-residue nor nonlinear-force matching input is supplied.

This does not admit any family as a physical GO or establish a positive physical
energy. Earlier six numerically consistent cases, twelve unresolved cases and
all negative-action/nonoscillatory evidence remain unchanged. Stage1 is complete
only in its registered bounded linear prepared-dust scope; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1--3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED;
TOP-X4 unchanged. Rule9 DEFERRED; Rule9_cleared=false; inherit the nodal,
global-reduction, tangency, descriptor, finite-node and transitive review debt.
Same-author algebra/replay is not independent scientific review.
physics_pass=false; gate_effect=NONE. No new action/parent, state adoption/
evolution, vault-management write, manuscript/site edit, publication, commit/
push, paid dispatch or model/package/global-runtime change. Root goal ACTIVE.
