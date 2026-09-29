# R4C1-PD1: physical-domain and GR-limit preflight

Date: 2026-09-29. Owner: conditional R4C1-v1 / Master Test 1.
The [PD1 contract](RES001_R4C1_PHYSICAL_DOMAIN_PREFLIGHT_CONTRACT_2026-09-29.md)
was frozen before the executable and its first receipt. The action, B1
parameters, G1 calculation, S2 dispersion and S4H-U formal estimate are
unchanged. This is a necessary-condition and interpretation audit, not a new
stability proof or a parent-gate promotion.

**Decision:** The fixed-B1 zero-exchange shortcut is not pure GR in G1's
isolated frame/metric response control. The registered eta path has a
divergent canonical force coefficient. S4H-U has a nonempty **formal**
high-momentum mode range, but its intersection with a physically valid EFT
range is **undetermined** because no physical `p_max` has been derived.
Local validation passes 19/19 exact checks; `physics_pass=false`,
`gate_effect=NONE`, `Rule9_cleared=false`, `review_status=DEFERRED`.

## 1. Necessary GR conditions, not an all-path no-go

G1's already-varied isolated nonzero-mode frame/metric control gives

\[
G_{\rm static}=\frac{G_{\rm bare}}{1-\alpha_{14}/2},\qquad
G_{\rm cos}=\frac{G_{\rm bare}}{1+(\alpha_{13}+3\alpha_2)/2},\qquad
\alpha_i=(M_U^2/M_P^2)c_i.
\]

Provided these denominators are nonzero, equality requires
`alpha14+alpha13+3 alpha2=0`. For the unchanged B1 parameters the left
side is `11/30`, and `G_cos/G_static=5/6`. Replacing `alpha_i` with bare
`c_i` produces the false ratio `35/46`, rejected by the executable.
Setting only `beta=g_r=0` removes the two exchange interfaces, not the
independent frame stress. This rejects that **shortcut**, not every R4C1
route to GR. G1's separate algebraic Einstein-dust endpoint remains defined;
its health as a continuous finite-density propagating limit is unproved.
Neither the equality surface nor this quasistatic control is a complete PPN
metric, a globally isolated positive source on empty compact `T^3`, or an
interacting B1 inhomogeneous solution.

For a declared positive monomial family `K_Q=K0 eta^q`,
`A=A0 eta^a`, `q>0`, canonical normalization
`psi_c=sqrt(K_Q) psi` makes the spatial nonanalytic operator coefficient

\[
\frac{A}{K_Q^{3/2}}
=\frac{A_0}{K_0^{3/2}}\eta^{a-3q/2}.
\]

The coefficient is nondivergent as `eta->0` only if `a>=3q/2` (for fixed
positive `A0,K0`). This is **necessary only**; it does not establish weak
coupling, a healthy frame mode or a valid alternative family. G1's
registered `q=a=1` path fails it, giving
`2 sqrt(3)/(63 sqrt(eta))`. The same path loses its physical transverse
kinetic coefficient `K_T=eta/6`. Choosing a different exponent would be a
new declared path requiring its own background, constraints and force-law
audit, not a repair of the frozen G1 receipt.

## 2. Formal momenta versus an action-derived physical cutoff

In the frozen action, `Lambda` has mass dimension one and occurs in the
condensate sextic potential `lambda_6 s^3/(24 Lambda^2)`; B1 assigns it the
reference value 2. The `b` coefficient is dimensionless and names the
quartic-force regulator as a whole. Thus B1's script key `cutoff=2` is a
**potential parameter name**, not a derived upper physical momentum for the
frame/force/matter system. The action does not independently specify `M_*`
or a scattering/causality cutoff for that system.

Two dimension-one combinations can be formed from the frozen coefficients:

\[
p_b=\sqrt{K_Q/b}=\sqrt{33/5}\simeq2.57,\qquad
p_A=\sqrt{K_Q^{3/2}/A}
=\sqrt{21\sqrt3/2}\simeq4.26
\]

in B1 reference units. `p_b` is a coefficient scale for the formal quartic
dispersion; it is **not** an observed quadratic/quartic crossover, because
the action has no ordinary quadratic spatial `Y` term. `p_A` is the
inverse-square-root scale of the nonanalytic canonically normalized cubic
coefficient; it is **not** a derived scattering cutoff. Neither can be
inserted as `p_max` without a separate physical-amplitude/validity analysis.

S4H-U proves a sufficient reduced-graph formal estimate only for
`p=k/a>=p0=8*10^13` on `[0,4]`. Its conservative envelope `a<=60` makes
`k>=4.8*10^15` sufficient for the full interval; on an axial torus mode
`k=2 pi |n|`, `|n|>=8*10^14` is still more conservative. These are
mathematical sufficiency bounds, not experimentally calibrated momenta or
a necessity theorem. If a future uniform physical bound `p<=p_max` exists,
a particular mode meeting this conservative full-interval `k` threshold
would require `p_max>=k` at B1's `a(0)=1`. A mode admitted only at one time
would at least require `p_max>=p0` then. No such `p_max` is established.
The large gap between `p0` and the two coefficient scales raises a physical
validity question, but **does not prove the physical overlap empty**: those
scales are not cutoffs and `p0` is a deliberately loose bound.

## Verification and retained holds

The [executable](../../../Analysis/MasterTests/test_01_r4c1_physical_domain_preflight.py)
SHA-256 is `18f7ae3c70b6a9983365783270db32e12fcecd8fbf8317cd3c5b29738316b098`.
It parses the pinned B1 `PARAMS` literal without importing/running an older
receipt producer, pins the contract and six upstream sources, checks exact
rational/symbolic identities, and rejects bare-`c_i` substitution and the
registered divergent scaling. The [attempt-01 receipt](../../../Analysis/MasterTests/outputs/r4c1_pd1_attempt_01/summary.json)
SHA-256 is `a239aa72782c16bee3d96c7666afee779a43561c6b1e8a1ad2acc29b833d2675`;
all 19 local checks pass with zero failed/unknown checks. Its own fields
retain `physics_pass=false`, `gate_effect=NONE` and no physical overlap
claim. Source-level role classification of `Lambda`, `p_b` and `p_A` is
from the pinned action and reports, **not** independently proved by the
19-count. The result is not independent peer review.

The next genuine physics obligations remain: derive an interaction- and
constraint-compatible physical validity range; decide whether any valid mode
overlaps a sufficiently sharp evolution estimate; establish the full
constrained IVP and singular/zero-mode handling; and construct a healthy
continuous GR control or disposition the frozen candidate. Candidate
classical source-vector closure does not itself authorize canonical Test 1.
Test 2's pointwise force law and Test 3's blind `C_chi` remain open.

Master Test 1 `ACTION_INPUT_INCOMPLETE_HOLD_BEFORE_VARIATION` at the
canonical parent; R4C1 candidate remains `CONDITIONAL`.
MAT-001 `BLOCKED`; UVIR-003 `IN_PROGRESS`; `K_Q=NOT_DERIVED`;
`V=NOT_COMPUTED`; Stage 4A `CLOSED`; Rule 9 deferred, not cleared.
