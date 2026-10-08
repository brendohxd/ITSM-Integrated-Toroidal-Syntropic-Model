# R4C1-G2: equal Newton couplings versus the regular scalar kinetic chart

Date: 2026-09-30. Owner: conditional R4C1-v1 / Master Test 1.
Status: `POST_HOC_ANALYTIC_CONDITIONAL_OBSTRUCTION`.
`physics_pass=false`; `canonical_Test1_pass=false`; `gate_effect=NONE`;
`Rule9_cleared=false`; `review_status=DEFERRED`.

This is an algebraic continuation of the unchanged frozen action, not a new
action, background solution, parameter fit, or reviewed physical no-go.
The observation was made after inspecting the existing G1 and S1 results; it
was **not** preregistered as a numerical test. No observed acceleration,
Hubble value, galaxy data, or external gravity bound is used.

## Pinned inputs and scope

| Input | Raw SHA-256 | Fact used |
|---|---|---|
| [R4C1 action freeze](RES001_R4C1_ACTION_FREEZE_2026-09-25.md) | `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3` | Same frame invariants, matter coupling and fields; no added operators. |
| [G1 GR-limit report](RES001_R4C1_GR_LIMIT_REPORT_2026-09-25.md) | `b3f3483ae99c868ee60a09b8bd44dd5375dadbc137d04f239405c159a5a8c404` | Independently derived scalar-free, zero-exchange static and homogeneous Newton couplings and the transverse kinetic coefficient. |
| [S1 scalar constraint report](RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md) | `0b5f06aa3ca91876895c0f1ab521093fa44034f04ce62d605d676f9190824b1b` | Reduced nonzero-mode, aligned homogeneous scalar kinetic sum of squares and its regularity domain. |

The calculation compares **coefficient conditions**, not the G1 vacuum
control and interacting S1 trajectory as though they were the same solution.
It assumes one unchanged set of R4C1 frame coefficients could support both
controls. As in G1, `beta=g_r=0`, `Phi=r=0` and constant `psi` define the
Newton-coupling control; as in S1, the kinetic form is read on an aligned,
expanding homogeneous solution for nonzero `k` in its regular gauge chart.

## Exact compatibility calculation

Use G1's dimensionless `alpha_i=(M_U^2/M_P^2)c_i`, with positive finite
`M_P^2,M_U^2`, and define

```text
alpha_13=alpha_1+alpha_3,
alpha_14=alpha_1+alpha_4,
alpha_L=alpha_1+alpha_2+alpha_3=alpha_13+alpha_2.
```

G1 gives, with a common nonzero `G_bare`,

```text
G_static = G_bare / (1-alpha_14/2),
G_cos    = G_bare / (1+(alpha_13+3 alpha_2)/2).
```

For finite positive couplings, their equality is **necessary, not sufficient**
for a GR-like common normalization. Equating denominators yields

```text
alpha_2 = -(alpha_13+alpha_14)/3,
alpha_L = (2 alpha_13-alpha_14)/3.
```

The G1 physical transverse mode has `K_T=M_U^2 c_14=M_P^2 alpha_14`.
S1's reduced scalar kinetic form has, among positive square weights, the
independent coefficient

```text
D = 4 H^2 M_c^2 M_t^2 / (M_U^2 c_L),
M_c^2 = M_P^2 [1+(alpha_13+3 alpha_2)/2],
M_t^2 = M_P^2 (1-alpha_13).
```

On the equal-coupling locus, `M_c^2=M_P^2(1-alpha_14/2)`.
In the **`alpha_13=0` subfamily**, which includes B1's frame relation,
the equality condition becomes `alpha_2=alpha_L=-alpha_14/3` and
`M_t^2=M_P^2`. Positive finite `G_static` and transverse kinetic energy
require `0<alpha_14<2`. Consequently `M_c^2>0` while `M_U^2 c_L<0`, so
`D<0` for `H!=0`: the S1 reduced kinetic form has a negative scalar square.
The auxiliary block is still invertible when `c_L!=0`; this is a kinetic-sign
obstruction, not a false claim that the constraint matrix is singular.

At `alpha_14=0`, the attempted equality gives `alpha_L=0`; both the
transverse kinetic coefficient and S1's auxiliary determinant vanish. The
regular S1 reduction cannot be continued through that surface by division.
For `alpha_14<0` the transverse kinetic sign is wrong; for
`alpha_14>=2` the static Newton denominator is nonpositive or singular.
Thus exact equality, positive finite Newton coupling, positive transverse
kinetic coefficient, and S1 scalar no-ghost cannot coexist within this
`alpha_13=0` regular subfamily. This is a **necessary-condition failure** for
a healthy GR-normalized parent there, not a full all-sector instability proof.

For comparison, B1 has `alpha_13=0`, `alpha_14=1/6` and
`alpha_2=alpha_L=1/15`: its S1 kinetic signs are positive, while G1 finds
`G_cos/G_static=5/6`. Changing only `alpha_2` to force equality gives
`alpha_2=-1/18`, hence `D<0`; this is a diagnostic continuation, not a
new B1 solution. More generally, with `alpha_13=0`, `alpha_14>0`,
`alpha_L=alpha_2>0` and positive denominators, the exact ratio is strictly
below one.

The obstruction **does not extend to every R4C1 coefficient choice**.
Algebraically, on the equality locus with positive `M_c^2,M_t^2,K_T`,
S1's `D>0` instead requires `alpha_13>alpha_14/2` (and
`alpha_13<1`). For example, `alpha_14=1/6`, `alpha_13=1/8`,
`alpha_2=-7/72` gives `alpha_L=1/36` and equal G1 couplings with
positive listed kinetic factors. It is **not** a tested background,
tensor/PPN-consistent solution, stable EFT, or physical rescue.

## Verification and decision

An independent SymPy simplification of the two G1 denominators and the S1
coefficient definitions returned exactly
`alpha_2=-(alpha_13+alpha_14)/3`,
`alpha_L=(2 alpha_13-alpha_14)/3`, B1 ratio `5/6`, and the stated
counterexample rational values. The sign conclusion follows from S1's
analytic square decomposition, not from sampled eigenvalues or a check count.
The source derivations remain provisionally reusable with Rule-9 review
deferred; their independent physics review is not claimed here.

This rules out a simple frame-parameter repair of G1's `5/6` mismatch **while
simultaneously retaining `alpha_13=0` and S1's regular no-ghost scalar
branch**. It does not prove that equal Newton constants suffice for GR,
that `alpha_13!=0` is viable, that a singular or differently constrained
branch is healthy, or that every GR-connected R4C1 path fails. In particular,
the registered G1 `eta -> 0` family has its own vanishing transverse kinetic
and divergent canonical-force issue; this note neither repairs nor replaces
that limit analysis.

The next Test-1 action-selection/viability step must either examine a
separately frozen `alpha_13!=0` branch with tensor, scalar, PPN and EFT
checks, analyze a genuinely different constraint chart/action, or accept the
present candidate as conditional only. No canonical promotion follows.
Tests 2 and 3 remain held by the coupled force and blind coefficient gaps.
`MAT-001=BLOCKED`; `UVIR-003=IN_PROGRESS`; `K_Q=NOT_DERIVED`;
`V=NOT_COMPUTED`; `Stage4A=CLOSED`.
