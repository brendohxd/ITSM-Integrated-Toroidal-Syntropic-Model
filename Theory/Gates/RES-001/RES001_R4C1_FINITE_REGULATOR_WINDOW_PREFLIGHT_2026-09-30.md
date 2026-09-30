# R4C1-T2P4c: finite-regulator corridor in the conditional contrast equation

Date: 2026-09-30. Owner: conditional R4C1-v1 / Master Tests 2 and 3.
Status: `ANALYTIC_CONDITIONAL_PARAMETER_WINDOW`; `physics_pass=false`,
`canonical_Test2_pass=false`, `canonical_Test3_pass=false`,
`gate_effect=NONE`, `Rule9_cleared=false`, `review_status=DEFERRED`.
This is an append-only continuation prompted by the distinction between
changing `A` and changing `b`; it does not edit a frozen action, B1 receipt,
source file, previous note or sidecar. No observed `a0`, Hubble posterior,
galaxy or lensing datum selected a coefficient.

## Pinned source boundary

| Source | Raw SHA-256 | Relevant fact |
|---|---|---|
| [R4C1 action freeze](RES001_R4C1_ACTION_FREEZE_2026-09-25.md) | `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3` | Exploratory interior permits `b>0`; `b=0` omits the auxiliary and changes the endpoint problem. |
| [T2P4 order-of-limits note](RES001_R4C1_LONG_WAVELENGTH_ORDER_OF_LIMITS_NOTE_2026-09-30.md) | `95f8d2f83d06c085d86b5220dbdc2c5b7f0652d9f25e21858ae73c740f1726af` | Defines the single-cosine contrast equation and `delta`. |
| [T2P4b coefficient trade-off](RES001_R4C1_CONTRAST_CROSSOVER_COEFFICIENT_TRADEOFF_2026-09-30.md) | `907ee1b5cf5de1b4426add13d90da149747ad54049f299f758efbf38723de545` | Increasing `A` opens a formal crossover but lowers the separately conditional `a_dyn`. |
| [S1 scalar constraint report](RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md) | `0b5f06aa3ca91876895c0f1ab521093fa44034f04ce62d605d676f9190824b1b` | Auxiliary determinant is `C^8 M_U^2 b k^2 c_L`; exact reduced kinetic certificate contains no `b`, but `b=0` is a singular chart boundary. |
| [C1 coefficient report](RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_REPORT_2026-09-25.md) | `c4af4084ae83f7ed70d63f44700a0ebfc2c394ed7d79cd0061e3efe279b7dc0a` | Its conditional spherical leading scale `a_dyn=beta^3/(12*pi*G_static*A)` contains no explicit `b`; the finite-regulator correction must remain controlled. |
| [PD1 physical-domain report](RES001_R4C1_PHYSICAL_DOMAIN_PREFLIGHT_REPORT_2026-09-29.md) | `2f151504d695ee442585653982cbbabfca2f520e864a802de306c0b013f3abc4` | `p_b=sqrt(K_Q/b)` is a coefficient scale, **not** an EFT cutoff. |

The source-hashed [S1 matrix export](../../../Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_matrices.json)
is `27d5a7130293866373ec1a98fbb6d0be0036421ef937416f77dd05b80f61349a`;
its current sidecar matches. An in-memory scan of its encoded symbolic blocks
finds no standalone `b` in `K` or `M`, but finds it in `V`. This is a
source-level structural check, **not** a recomputation of the coupled mode
spectrum for a changed `b`.

## Exact nonempty *formal* window at fixed `A`

Keep the B1 reference `A=2/7`, `K_Q=3`, `beta=2/5`, `rho_bar=1/5` and
`H_E=sqrt(3469/4620)`, with `dot(psi_bar)=1/5`. In the T2P4 single-cosine
equation, let `0<epsilon<=f rho_bar`, `0<f<1`, and choose a mode
`k>=eta k_H`, where `eta>=1` and the initial matter-frame horizon proxy is
`k_H=H_E+beta dot(psi_bar)=0.946525129968...`. Its exact rescaling gives

```text
delta^2 = b^2 k^5/(3 A beta epsilon).
```

Consequently a **necessary** condition for the crossover diagnostic
`delta<=1` is

```text
0 < b <= b_max(eta,f)
      := sqrt(3 A beta f rho_bar)/(eta k_H)^(5/2).
```

Within **this conditional scalar problem only**, T2P4 permits changing the
torus period, so `k=eta k_H`, `epsilon=f rho_bar`, and any finite
`0<b<=b_max` give an explicit nonempty algebraic corridor. `eta=1` is a
permissive horizon proxy; a physical quasistatic use would need `eta >> 1`
and a controlled time/metric/frame/dust remainder. `delta<=1` is not a
predeclared accuracy threshold for a square-root force law.
The `f=1` rows below are limiting values as `f` approaches one; strict
positive total density requires `epsilon<rho_bar` and hence `b<b_max` there.

| `eta` | `f` | `b_max` | `b_max/(5/11)` |
|---:|---:|---:|---:|
| 1 | 1 (strict positive-density supremum) | 0.3004285672 | 0.6609428479 |
| 1 | 0.1 | 0.09500385465 | 0.2090084802 |
| 10 | 1 (strict positive-density supremum) | 0.0009500385465 | 0.002090084802 |
| 10 | 0.1 | 0.0003004285672 | 0.0006609428479 |

For the *single-cosine diagnostic* on the registered `L=2*pi` period,
`k=1` and `f=0.1` instead give the exact positive threshold
`b_max=sqrt(210)/175=0.08280786712...`; the frozen `b=5/11` lies above it.
This does **not** rerun T2P1's three-cosine source or its 46 checks.

This distinguishes the two levers. In C1's **separate conditional**
spherical exterior reduction, holding `A`, `beta` and `G_static` fixed
leaves its leading `a_dyn` formula unchanged when `b` changes, while its
explicit regulator-to-cubic flux ratio `2b/(3 A D R)` decreases with `b`
at fixed `D,R`. It does not prove a common periodic galaxy solution.
On homogeneous aligned B1, the projected gradient and `Delta_psi` vanish,
so the regulator gives no background first variation; a finite `b` change
does not itself select a new homogeneous history. S1's kinetic certificate
is `b`-free for `b>0`, but its auxiliary determinant tends to zero as
`b->0`. The reduced potential, full propagation pencil, zero-mode branch,
uniform inverse estimates, physical cutoff and nonlinear backreaction must
therefore be **recomputed**, not inherited from frozen B1. The coefficient
scale `sqrt(K_Q/b)` grows as `b` is reduced and cannot be asserted to be a
physical cutoff or safe validity range.

## Decision and next discriminating calculation

The finite-positive-`b` corridor means the previous frozen-B1 non-overlap
does **not** exclude all parameter points of the R4C1 action family. This
is a genuine conditional route worth testing, not a derivation of ITSM's
weak-field law or of `C_chi`. A target-independent follow-up should freeze
a finite set of positive `b` values spanning the corridor, then redo the
full constrained S1/S2 symbol and zero-branch/IVP diagnostics, establish an
action-derived physical validity range, and solve the coupled nonlinear
metric/frame/dust/Euler contrast problem with an independently bounded
quasistatic error. A small `b` cannot be used to claim that `b=0` is regular.

Master Tests 1-3, MAT-001, UVIR-003, Stage 4A and publication holds remain
unchanged; `K_Q=NOT_DERIVED`, `V=NOT_COMPUTED`, and Rule-9 review remains
deferred rather than cleared.
