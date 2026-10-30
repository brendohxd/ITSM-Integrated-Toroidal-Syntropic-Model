# Exact finite-band continuation fails the initial acceleration test

29 October 2026, Australia/Perth. Conditional; review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE. G1-G6 INCOMPLETE.

## Result and scope

For the registered unchanged-action B1 eta=1/4, e=1/500, k=40 quartic
initial construction, the actual coupled Vy acceleration is not a
trigonometric polynomial. Therefore there is no continuation through these
data with Vy in one fixed finite spatial Fourier subspace and with C2 time
regularity into L2. This is a necessary compatibility test conditional on the
original initial equations; no evolved solution is assumed or constructed.

The result rejects an EXACT invariant band as a proposed workaround for the
[constrained principal obstruction](RES001_R4C1_CONSTRAINED_PRINCIPAL_V1_REPORT_2026-10-28.md).
It does not reject Galerkin approximations with independently controlled tails,
every weak solution, an independently justified effective description, or
ITSM as a whole. Imposing a projector changes the equations and is not done.
An EFT validity range need not mean an exactly band-limited field: this test
does not by itself calculate or rule out a physical EFT cutoff.

## Coupled initial calculation

Reuse the original 12-dimensional complement B(w), the exact
original-minus-cusp force partition and the regulator-determined scalar
acceleration. The (hxx,hyy,hzz,Vy) sector is exactly isolated inside B;
its metric crosses are retained. For w>0 its physical cusp force is

    f_cusp = (-A*p^3*w^3/2, -2*A*p^3*w^3,
              -A*p^3*w^3/2, -3*A*p^3*w^2)^T,
    A=1/28, p=1/20.

This is the cusp of the physical action, not a newly selected force. The
parent full-generator partition controls and total-jerk derivation are reused.
Solving B_sector*a_sector=f_cusp gives the exact Vy positive branch

    P(w) = -w^2*(2*w^6+173*w^4+2391*w^2+2214)
                   /[56000*(76*w^2+123)],
    aVy_cusp(w) = sign(w)*P(w),
    P(w) = C*w^2 + O(w^4), C=-9/28000.

P is even and analytic with no real denominator zero. The analytic initial
acceleration partition has removable analytic node limits, as established in
the [total-jerk report](RES001_R4C1_QUARTIC_TOTAL_JERK_V1_REPORT_2026-10-28.md),
sections 1-2. Its smooth node contribution cannot cancel the following jump.
The scalar/regulator and other complement terms are not discarded; the cusp
split is linear superposition in the original initial acceleration equation.
As an algebraic cross-check, the same coupled response reconstructs the
parent's complete cusp jerk kernel exactly, including its metric trace.

At each simple node, w=sigma*x+O(x^3), sigma=+/-2/25. Thus aVy_cusp is C1
but not C2 in the spatial normal coordinate. Its second normal derivative has
the exact oriented jump

    [partial_z^2 aVy] = 4*C*sigma*abs(sigma)
                      = -sign(sigma)*9/1093750.

The third WEAK normal derivative contains this coefficient times the node
delta. No ordinary third cusp derivative at a node is used. These are
reference-coordinate/unit coefficients of this registered initial datum,
not a measured observable, an invariant stability scale or a physical cutoff.

## Why the exact band is excluded

Let E_M be any fixed finite-dimensional spatial Fourier subspace. It is
closed in L2 and all its representatives are smooth. If Vy(t) belongs to E_M
on a time interval and is C2 into L2, difference quotients show that its
initial acceleration also belongs to E_M. But the acceleration just derived
has a nonzero second-derivative jump and no smooth representative. This is a
contradiction. The argument only needs the Vy equation, so it does not assume
that the constrained shift itself initially has finite Fourier support.

Weak integration by parts checks the full rational cusp kernel on a whole
profile period, including both node orientations. With theta=k*z, the tests
sin(theta) and sin(3*theta) give interface contributions respectively
+18/1093750 and -18/1093750. The regular third-derivative integral alone misses
these terms. Including them gives normalized discrepancies 0 at stored
precision and 2.04e-115 or less, against the frozen 1e-30 criterion.
These quadrature controls supplement the exact jump argument; they are not
rigorous time-evolution error bounds. On a torus with several profile periods,
the interface structure repeats at every corresponding node.

## Verification and preservation

Contract: RES001_R4C1_FINITE_BAND_DOMAIN_V1_CONTRACT_2026-10-29.md.
Executable: Analysis/MasterTests/test_01_r4c1_finite_band_domain_v1.py.
Receipt: Analysis/MasterTests/outputs/r4c1_finite_band_domain_v1_attempt_01/summary.json.
Receipt SHA256: 41761b47e4256e48fad9d06fbad531c84c2b02a82f346432469c3cda2a074868.
14/14 checks, no failed/unknown rows, and READ_ONLY_REPLAY_EXACT.177 inherited
and current source pins and their sidecars are checked before and after the
calculation. Same-author algebra, controls and replay are not independent
scientific review. Earlier sources, failed attempts and sidecars are preserved.

The 28 October Frobenius calculation is a normalized specialization/recheck
of a phenomenon already recorded in G3N2 and the 17 October CUSP3 source-aware
report, not a newly discovered obstruction. The full constrained principal
reduction and this exact-band compatibility argument have different scopes.

## Direction after this result

| Route | Evidence and remaining requirement |
|---|---|
| Standard unrestricted finite-Sobolev Cauchy estimate on the registered slices | Already obstructed by the full reduced non-real principal characteristics; not a review-only hold. |
| Exact invariant finite Fourier band with C2 time regularity into L2 | Rejected here for the registered initial construction. |
| Finite-mode approximation with tails, or a specially prepared weak-solution class | Not excluded here. Requires an actual invariant domain, constraint/interface propagation and uniform evolved error/existence estimates; finite-grid agreement alone is insufficient. |
| Choose an n-orthogonal foliation for this registered frame | The inherited nonzero Frobenius result obstructs that particular choice; other formulations are not all excluded. |
| Different initial state, branch-selection prescription, new projector, UV completion or parent action | Not selected or implemented. Requires a concrete proposal and the operator's action/state/prescription decision. |
| Numerical matter-residue and nonlinear-force matching | Existing genuine identifying inputs remain necessary; domain restrictions or assumed diagnostic coefficients do not supply them. |

The physical-domain preflight of 29 September remains binding: neither the
potential parameter nor a vacuum probe threshold is a derived physical cutoff.
The MAT physical matching route decision of 13 October distinguishes an
assumed bare ratio from a genuinely identified coupled residue; no new
identifying mechanism is supplied by this calculation. This is a bounded
assessment of these routes, not an exhaustive all-action survey.

The next same-action research question is whether a specified prepared weak
domain can retain the full constrained branch and the forced cusp tails with
controlled evolution. That problem remains open. Do not automatically launch
another large spectral or time-integration sweep, delete a branch, substitute
TOP-X4, or claim a physical window. If continuing requires a new physical
prescription, stop for the operator's choice before adopting it.

Earlier bounded dust, initial-jet, weak-action and Ward results remain scoped
and unchanged. G1-G6 INCOMPLETE; Stage2 INCOMPLETE; Stage3 NOT_ENTERED;
MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS;
Stage4A CLOSED. Review DEFERRED, not cleared. No manuscript, PDF, website,
vault mutation, provider dispatch, commit, push or publication in this task.
The native goal still requires the app/user to resume its usageLimited status.
