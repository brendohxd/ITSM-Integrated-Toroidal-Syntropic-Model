# R4C1-T2P2: finite `b` removes the arbitrarily weak-source square-root asymptote

Date: 2026-09-29. Owner: Master Test 2 / conditional R4C1-v1.
The [T2P2 contract](RES001_R4C1_WEAK_SOURCE_CONTRACT_2026-09-29.md)
(SHA-256 `53542c4c5c850bb299937634fc49abe702b4d54871b4f7181d15a2730a7ed271`)
was frozen before numerical execution. The action, B1 parameters, T2P1
force equation, spatial source *shape*, solver and torus periods were not
changed. Only the density-contrast amplitude was varied as declared.

**Decision:** In the frozen aligned-frame static `T^3` contrast reduction,
the finite positive `b` regulator makes the response **linear to first
order in source amplitude**, with a quadratic nonlinear correction.
Consequently its conditional matter force cannot have a fixed positive
square-root coefficient as an *arbitrarily weak-source, fixed-spatial-scale*
asymptote. This is not a claim about a physical coupled ITSM solution,
an intermediate window, another regulator, or every theory variant.
`physics_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false`,
`review_status=DEFERRED`, `canonical_Test2_pass=false`.

## 1. Exact spatial estimate

On the mean-zero space `H^2_0(T^3)`, fix
`f=(cos x+2 cos y+3 cos z)/50`, `A=2/7`, `b=5/11>0`,
`beta=2/5`, a cubic torus of period `2*pi`, and `epsilon>=0`. The
T2P1 conditional spatial functional is

\[
 J_\epsilon[\psi]=\int_{T^3}\!\left[
 A|\nabla\psi|^3+\frac b2(\Delta\psi)^2
 +\beta\epsilon f\psi\right]d^3x.
\]

As established by the same coercivity/strict-convexity argument used in
C2, it has a unique zero-mean weak minimizer. Its weak Euler equation is

\[
 b\langle\Delta\psi_\epsilon,\Delta\phi\rangle
 +3A\langle|\nabla\psi_\epsilon|\nabla\psi_\epsilon,
          \nabla\phi\rangle
 +\beta\epsilon\langle f,\phi\rangle=0.
\]

Choose `phi=psi_epsilon`. The nonlinear term is nonnegative. On the
zero-mean torus, `||psi||_2 <= C||Delta psi||_2`, so Cauchy–Schwarz gives
`b||Delta psi_epsilon||_2^2 <= beta epsilon C||f||_2
||Delta psi_epsilon||_2`. Thus
`||psi_epsilon||_(H^2)=O(epsilon)` with the fixed periodic elliptic norm.
The three Fourier modes in `f` have `Delta^2 f=f`, hence the exact
linear-response field is

\[
 \psi_1=-\frac{\beta}{b}f=-\frac{22}{25}f,
 \qquad b\Delta^2\psi_1+\beta f=0.
\]

Set `w=psi_epsilon-epsilon psi_1` and subtract the linear equation.
Testing with `w` yields
`b||Delta w||_2^2 <= 3A ||grad psi_epsilon||_4^2
||grad w||_2`. The three-dimensional Sobolev embedding
`H^2(T^3) -> W^{1,4}(T^3)`, together with the periodic elliptic
estimate above, bounds the right side by
`C epsilon^2 ||Delta w||_2`. Therefore

\[
 \|\psi_\epsilon-\epsilon\psi_1\|_{H^2}=O(\epsilon^2),
 \qquad \|\nabla\psi_\epsilon\|_2=O(\epsilon).
\]

The constants in these `O` statements depend on this fixed source,
torus and positive couplings; this is **not** an EFT, time-domain or
full-theory approximation-error bound. In particular, the FRW mean
scalar still has the T2P1 positive-dust time response, and the
contrast time derivative, perturbed Einstein/frame/dust equations and
matter Euler backreaction remain omitted.

For an explicitly **auxiliary** periodic Newtonian control,
`Delta Phi_bar=4*pi*G_static*epsilon*f` at fixed positive `G_static`.
Its nonzero gradient norm scales exactly as `epsilon`, whereas the
conditional conformal force norm `||beta grad psi_epsilon||_2` is
`O(epsilon)`. Thus
`||beta grad psi_epsilon||_2/sqrt(||grad Phi_bar||_2)
=O(sqrt(epsilon))->0`. A universal fixed positive coefficient multiplying
`sqrt(g_bar)` would instead require a nonzero limiting ratio. This
norm-level contradiction is scoped to the declared static reduction
and comparator; the estimate does not certify a pointwise physical RAR.

## 2. Frozen numerical controls

The [write-once attempt-01 receipt](../../../Analysis/MasterTests/outputs/r4c1_t2p2_attempt_01/summary.json)
(SHA-256 `334cbc20b5581968cab48e9ee8699f7f3e982527d4f4917185952dfbdb9e7722`)
passes **194/194 local checks**, with zero failed/unknown checks. A
byte-identical rerun reproduces it. The executable pins eight direct
sources, verifies T2P1's inherited source map and parses the unchanged
B1 literal only after those checks. Its SHA-256 is
`199d7d309a4fdd085bdd7a6c5f36c8d135759a3827d1bd3bfa4cfa09cca04cfc`.

The registered epsilons are `1,1/4,1/16,1/64,1/256`, on each of
`N=17,25,33`. At `N=33`, the relative RMS deviation from the exact
linear field decreases in that order:
`0.0813475, 0.0230150, 0.00595742, 0.00150279, 0.000376552`.
The last is below the frozen `1e-2` threshold. The registered
`beta*RMS(grad psi_epsilon)/sqrt(epsilon)` ratio between the last two
epsilons is `1.99775`, within the frozen `[1.5,2.5]` interval and
consistent with the analytic factor-two limit. The maximum normalized
strong residual is `3.258e-8`; the maximum specified weak residual is
`2.547e-8` (each threshold `1e-5`). The largest `N=25` to `33`
fundamental-cosine relative change is `2.851e-9` (threshold `5e-3`).
At `epsilon=1/256`, deliberately omitting `b` leaves normalized Euler
residual `0.999624`; the exact zero-source field and force control is
zero. These grid values corroborate the spatial proof but cannot bound
the omitted physics or certify continuum convergence by themselves.

## 3. Status, limits and next scientific obligation

C1's regulator-subleading spherical expression requires its own source-
and radius-dependent domain; it cannot be extrapolated down to arbitrary
source amplitude at a fixed spatial scale while `b` remains finite.
No statement here rules out a finite intermediate source window where
the cubic term is important. The physical existence and size of such a
window would have to be derived together with metric/frame/dust/Euler
response, a bounded quasistatic error and an action-derived EFT cutoff.
The `2/3` projection factor, `C_chi`, observed `a0` and `a0(z)` remain
undetermined. MAT-001 is `BLOCKED`, UVIR-003 `IN_PROGRESS`, Stage 4A
`CLOSED`; no Test 1–3 or publication promotion follows.

Rule-9 review is deferred, not cleared. Later independent review should
check the finite-`b` variational sign, zero-mean elliptic/Sobolev bounds,
the distinction between a norm-level asymptote and a physical RAR,
scaled-source normalization, omitted-regulator mutant and inherited
source pins. The next substantive Test-2 task remains a coupled
periodic-background weak-field calculation with controlled physical
domain, not another frozen-frame check count.
