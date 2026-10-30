# Quartic construction: bounded continuous initial acceleration through both nodes

27 October 2026. Conditional; review DEFERRED; Rule9_cleared=false.
physics_pass=false; gate_effect=NONE. G1 and G1-G6 remain INCOMPLETE.

## Bounded result

The registered unchanged-action B1-frame eta=1/4,e=1/500,k=40 quartic
initial construction has a continuous fourteen-coordinate Euler acceleration
extension through BOTH alignment nodes. The result retains the exact implicit
root, constrained shift and its errors, metric/frame/condensate/reservoir
sources, local lapse flux, both charges and the original force cusp.

Conservative uniform component bounds over the entire periodic initial slice
and whole certified root box, in reference units, are

    |aPsi| < 0.129459,
    max_{twelve complement components}|ay| < 29.086701,
    |aZ| < 3146.179.

These are magnitude bounds, not predictions of those magnitudes, useful-accuracy
estimates or characteristic frequencies. The broad regulator bound is mainly
from conservative derivative enclosures. It certifies finiteness rather than
a small error. The narrower observed point values are not substituted for it.

The [previous node-operator report](RES001_R4C1_QUARTIC_NODE_OPERATOR_V1_REPORT_2026-10-27.md)
and [quartic root report](RES001_R4C1_QUARTIC_JOINT_COMPLETION_V1_REPORT_2026-10-27.md)
retain their original scopes, hashes and holds. Their earlier unresolved
initial-force bounds are now supplied by this report; no old receipt is edited.
In particular, the nonzero |w| cusp remains in aZ. It is not smoothed away.

This is an INITIAL acceleration extension, conditional on the inherited exact
construction and trusted symbolic/interval implementation. It is not a proof
of background admission, compatible higher time jets, constraint transport,
local well-posedness, stability or a solution on [0,0.05].

## 1. All twelve analytic complement forces from the original density

Partition the pinned original density exactly into analytic and original cusp
terms. An in-process AST copy removes precisely the cusp summand from the
force assignment; every other original expression is retained. No original
source file or physical coefficient is changed. The physical cusp forces are
added separately using the prior derived bounds.

Real directional arithmetic around the original reverse gradient computes
the needed Hessian-vector products by the product rule. Outward interval
scalars are used for enclosures; complex-step values are independent point
controls only. Retain the full proper-coordinate map, all six metric and
three frame velocities, condensate/reservoir, volume drift, shift derivatives
and the temporal regulator term. Spatial Ricci and comoving spatial dust
forces vanish on this flat homogeneous-clock N=1 slice only, as in the
original derivation; that omission is not extended into future evolution.

Sixteen angular interval boxes cover the WHOLE circle. Their twelve analytic
source bounds in coordinate order are below

    (0.659112,0,0,0.659298,0.003087,0.659041,
     0,0.106709,0.000016911,0.527921,0.737925,1.209035).

Root/shift uncertainty is propagated into every box. Rsecond comes from the
exact shift ODE, not an unbounded approximate derivative. The eliminated Ud
is enclosed in [63.8371486544,63.8468952812]. These fields are not evolved
by projection onto either initial polynomial profile.

Twelve signed control angles exercise both nodes and both sides at offsets
0.01 and0.001. Against the original analytic AD/Euler operator at two
complex steps, the worst normalized discrepancy is below9.34e-42. Physical
original minus analytic complement gradients also agree with the original
cusp force vector. All controls lie inside the outward whole-circle bounds.

## 2. Scalar numerator and quantitative removal of the node division

Use the accepted exact block solve

    aPsi=-fZ/g,
    ay=B^-1*(fy-C*aPsi),
    aZ=N/g+(C/g).T*ay, N=d*aPsi-fpsi, g=b*w^2.

The full kinetic complement has ||B^-1||inf<24.058. The scalar numerator's
analytic part is formed from the original scalar force and LOCAL lapse-derived
density, including its energy and flux. Substituting R=w*T and cancelling
before differentiation removes explicit powers of 1/w. No mean density
replacement or numerical residual deletion is made.

At either node the exact constant numerator is -G, where G is the certified
joint scalar node condition. The exact root has G=0. Local reflection gives
Nprime(0)=0. A separate exact orientation verifier checks both the normal
reflection and (wprime,T)->(-wprime,-T); both node numerators are identical.
The positive-slope calculation is therefore not silently applied to the
opposite orientation.

For every nearest-node half-cell, |x|<=pi/(2k) and
|w|>=|sigma*x|/2, sigma=e*k. Global shift bounds are recomputed over |w|<=e;
the earlier node-only Rthird bound is not used outside its domain. Bounds are

    |Rprime| < 8.248e-6, |Rsecond| < 0.000440,
    |Rthird| < 0.035191, |T| < 0.000207,
    |Tprime| < 0.047654, |Tsecond| < 5.021960.

All H/U/W responses and exact inverse errors remain. Differentiate the exact
analytic numerator in(w,wprime,T,Rprime), retaining all four first and ten
distinct second derivatives and the factor two on mixed terms. The physical
chain derivative uses velocities(wprime,-k^2*w,Tprime,Rsecond) and
accelerations(-k^2*w,-k^2*wprime,Tsecond,Rthird). Its uniform second normal
derivative satisfies |Nsecond|<1.144065.

Taylor's theorem, G=0, reflection and the sine lower bound give

    |N_analytic/(b*w^2)| <= 2*sup|Nsecond|/(b*sigma^2)
                         < 3146.177.

An independent direct bound for |w|>=e/4 uses g>=2.8409090909e-8; it is
looser (<47157.090). The global half-cell Taylor proof covers the entire
circle, with the direct away-node region overlapping the node regions.
There is no uncovered gap at a patch boundary.

Four signed branches independently compare the complete physical chain
derivative to direct high-precision differentiation, with normalized errors
below3.74e-112. Omitting mixed terms changes a control by0.0036112077;
that rejection is actually exercised.

## 3. Full initial acceleration and the distinction from time evolution

Bound aPsi directly using the removable R/w quotient and the exact regulator
equation. Combine the bounded complement forcing, inverse and scalar cross
to bound all twelve ay. Add the separately derived cusp contribution and
recomputed global cusp remainder to the analytic aZ bound. Every resulting
bound is finite on the registered domain.

The analytic numerator is locally analytic and even at a node, with vanishing
constant term on the exact constraint root. Its quadratic division therefore
has a unique continuous limit. The cross C/g is polynomial and regular;
the physical cusp quotient is continuous with the already proved nonzero
|w| term. The full undivided Euler equations extend to the node by continuity.
The singular operator AT a point does not independently fix Ztt: continuity
of the regular-side solution fixes that nodal value in this scope.

No temporal existence theorem follows. In particular the cusp constrains
mixed regularity, and higher time derivatives of the actual regulator/metric/
frame equations must be checked before adopting a classical function space.
Do not silently require a smoothness class which the actual initial rates
do not satisfy, or declare a weak solution without its equations and estimates.

## 4. Verification and preserved implementation failures

- Complement-force V3:38/38, scalar-bound V1:13/13 and separate exact
  both-node orientation verifier:4/4. All accepted executables freshly replay
  byte-exact. The scalar bound pins137 source artifacts; orientation verifier
  inherits those plus its parent receipt and executable. No canonical promotion.
- Complement-force V1 stopped before an enclosure receipt because an ordinary
  mp scalar tried to absorb an interval direction. V2 stopped because leading
  interval parameters did not delegate multiplication to reverse AD Nodes.
  V3 preserves interval context and uses zero-direction AD-aware constants.
  Both earlier frozen sources, sidecars and ignored complete failure logs are
  preserved. No equations, tolerances or intervals were changed to obtain PASS.
- These are same-author independent controls and trusted numerical software,
  not proof-kernel verification or independent peer review.

| Receipt under Analysis/MasterTests/outputs/ | SHA256 |
|---|---|
| r4c1_quartic_complement_force_v3_attempt_01/summary.json | 41d889e9a55a2a6f35c919c23c97c4b764094ea0c8c25b17ece4c6a4a3ddda61 |
| r4c1_quartic_scalar_bound_v1_attempt_01/summary.json | f74df107b91e466e2c8d3c9d79107d968e2456beee16b26210adde7d43b1d756 |
| r4c1_quartic_initial_extension_orientation_v1_attempt_01/independent.json | 07b5687ba7f7eec31ab20dffdd638729ed2d9b4f5ee2d5c12e243642e9a481a2 |

## Next work and review debt

Continue the actual node-transport and mixed-time regularity calculation using
the original full regulator geometry and the derived coupled accelerations.
Track node motion, constraints and charges without imposing persistent
alignment or a fixed graph. Then assess initial-data admission and short-time
persistence in a justified function space. Do not rerun completed audits or
promote a bounded initial result into an evolved background.

Inherit quartic-root, node-operator/cusp, original density/variation, full
transport-geometry and scalar-coordinate review debt. The vault supplied
continuity only; no vault sync, proposal or claim admission was performed.
PROCEED_PROVISIONALLY for these scoped initial bounds; HOLD_SUBSTANTIVE for
background admission, physical modes, evolution, window/GR and identifying
matching. Stage2 INCOMPLETE; Stage3 NOT_ENTERED; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED.
No new parent/state adoption, dispatch, publication, commit/push or deployment.
