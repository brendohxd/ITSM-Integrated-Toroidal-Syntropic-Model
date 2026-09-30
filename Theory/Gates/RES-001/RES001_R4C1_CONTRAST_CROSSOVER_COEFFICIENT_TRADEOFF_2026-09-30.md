# R4C1-T2P4b: formal crossover versus force-coefficient trade-off

Date: 2026-09-30. Owner: conditional R4C1-v1 / Master Tests 2 and 3.
Status: `ANALYTIC_CONDITIONAL_PARAMETER_PREFLIGHT`; `physics_pass=false`,
`canonical_Test2_pass=false`, `canonical_Test3_pass=false`,
`gate_effect=NONE`, `Rule9_cleared=false`, `review_status=DEFERRED`.
No source, sidecar, frozen coefficient, numerical receipt or threshold is
changed. No observed `a0`, `H0`, galaxy curve or lensing datum enters.

## Pinned parents and scope

| Parent | Raw SHA-256 | Use here |
|---|---|---|
| [R4C1 action freeze](RES001_R4C1_ACTION_FREEZE_2026-09-25.md) | `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3` | Defines the positive `A`, `b`, `beta` action family. |
| [T2P1 periodic-force report](RES001_R4C1_PERIODIC_FORCE_REPORT_2026-09-29.md) | `5f178a121aae03fb5b4d47cf383586f0496a7d18262fc5b6069dc8be0fc658ad` | Supplies the *conditional* static contrast equation and B1 numbers. |
| [T2P4 order-of-limits note](RES001_R4C1_LONG_WAVELENGTH_ORDER_OF_LIMITS_NOTE_2026-09-30.md) | `95f8d2f83d06c085d86b5220dbdc2c5b7f0652d9f25e21858ae73c740f1726af` | Defines the single-cosine `delta` and formal `k -> 0` family. |
| [T2P4a B1-domain addendum](RES001_R4C1_LONG_WAVELENGTH_B1_DOMAIN_ADDENDUM_2026-09-30.md) | `726f63a79642c44de55db1602f65284ab76396f52a03199ff038f65a7c679fd3` | Proves non-overlap at the registered B1 `A=2/7` under its permissive horizon proxy. |
| [C1 coefficient report](RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_REPORT_2026-09-25.md) | `c4af4084ae83f7ed70d63f44700a0ebfc2c394ed7d79cd0061e3efe279b7dc0a` | Gives the separately conditional spherical `a_dyn` and proves `A` is not fixed by homogeneous/linear data. |

This note varies `A>0` **as a declared parameter continuation**, not a
retuning of the registered B1 point or its prior acceptance thresholds.
T2P4's equation is a frozen-frame, fixed-time, single-cosine **contrast**
problem, not the coupled metric/frame/dust/Euler system. C1's spherical
exterior force scale is a *different* conditional reduction. Eliminating a
common action coefficient across them does not prove a common physical
solution or an EFT domain.

## Necessary algebra for the conditional crossover

At B1 `t=0` in the same dimensionless reference units, let
`A_B1=2/7`, `b=5/11`, `beta=2/5`, `rho_bar=1/5`,
`H_E=sqrt(3469/4620)`, and `dot(psi_bar)=1/5`. T2P4 defines

```text
delta^2 = b^2 k^5 / (3 A beta epsilon),
delta_rho = epsilon cos(k x),    0 < epsilon < rho_bar.
```

For a declared fractional contrast cap `epsilon <= f rho_bar`, with
`0 < f < 1`, and a wavenumber `k >= eta k_H`, with `eta >= 1` and
`k_H = a_m H_m = H_E + beta dot(psi_bar)` at this initial state, the
diagnostic `delta <= 1` can occur only if

```text
A >= A_min(eta,f) := b^2 (eta k_H)^5 / (3 beta f rho_bar).
```

Conversely, **within this conditional scalar equation only**, and allowing
T2P4's declared change of torus period, choosing `k=eta k_H`,
`epsilon=f rho_bar`, and `A>=A_min` satisfies that diagnostic.
For the mere positive-density cap `f=1`, strict `epsilon<rho_bar` means
`A>A_min(eta,1)` is necessary and the listed threshold is an unattained
infimum. The actual quasistatic criterion is `k >> k_H`; `eta=1` is only
a permissive horizon proxy and `eta=10` below is illustrative, not an
observational or preregistered accuracy threshold.

| `eta` | `f` | `A_min` (infimum when `f=1`) | `A_min/A_B1` | Maximum conditional `a_dyn(A)/a_dyn(A_B1)` at threshold |
|---:|---:|---:|---:|---:|
| 1 | 1 | 0.6540397455 | 2.289139109 | 0.4368454481 |
| 1 | 0.1 | 6.540397455 | 22.89139109 | 0.04368454481 |
| 10 | 1 | 65403.97455 | 228913.9109 | 4.368454481e-6 |
| 10 | 0.1 | 654039.7455 | 2289139.109 | 4.368454481e-7 |

These values follow from exact rational `b,beta,rho_bar,A_B1` and
`k_H=sqrt(3469/4620)+2/25=0.946525129968...`; the table merely rounds
them. At the frozen `A_B1`, even `epsilon -> rho_bar` gives
`delta > sqrt(A_min(1,1)/A_B1)=1.51299...` at `k=k_H`.
For a **single-cosine** diagnostic on the registered `L=2*pi` period,
the first integer mode `k=1` instead requires
`A>625/726=0.8608815427...` under strict positive density;
at `A_B1` its `delta` infimum is `sqrt(4375/1452)=1.735824127...`.
That is not T2P1's original three-cosine source.

In C1's separate spherical approximation, holding `beta` and
`G_static>0` fixed gives `a_dyn(A)=beta^3/(12*pi*G_static*A)`. Therefore
`a_dyn(A)/a_dyn(A_B1)=A_B1/A`, as used in the table. Eliminating `A`
between C1 and T2P4's `k_*^5=3 A beta rho_bar/b^2` yields the exact
cross-diagnostic identity

```text
a_dyn(A) k_*^5 = beta^4 rho_bar / (4*pi*G_static*b^2).
```

It exposes a trade-off: raising `A` expands the formal crossover
wavenumber only as `A^(1/5)` while reducing the conditional square-root
force scale as `1/A`. Because the two reductions have **no proved common
validity region**, this identity is not an observational bound, a fitted
`C_chi`, or a physical no-go for all R4C1 parameter points.

## Decision

Changing `A` can algebraically evade T2P4a's *fixed-B1* `delta<=1`/horizon
non-overlap, so that restriction must not be enlarged to an all-`A` no-go.
It does not rescue Test 2: the required coupled on-shell solution,
quasistatic remainder, physical EFT cutoff and healthy Test-1 domain remain
absent. Nor does it rescue Test 3: C1 proves background and linear data
cannot choose `A`, and choosing it to obtain a desired acceleration is
parameter assignment. `delta<=1` itself is a crossover diagnostic, not a
force-law accuracy criterion. Master Tests 1-3, MAT-001, UVIR-003, Stage 4A
and publication holds remain unchanged; `K_Q=NOT_DERIVED`,
`V=NOT_COMPUTED`, and deferred Rule-9 review is not cleared.
