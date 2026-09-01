# PKM1 non-affine auxiliary constraint-rank audit

**Calculation:** `PASS_LOCAL_DIRAC_SUBBLOCK`  
**Disposition:** `HOLD_PKM1_GLOBAL_PARENT_LOCAL_AUXILIARY_SECOND_CLASS_FOR_Y_GT_0`  
**Physics pass:** `false`

## Exact local result

For the deliberately constructed deep-static block

`F(Y,s)=Y^2/(2 a0^2 s)+(a0^2/6)s^3`, with `s>0`,

the stationary point is `s_star=sqrt(Y)/a0`. Eliminating `s` gives exactly

`F_eff=(2/3)Y^(3/2)/a0`.

Because the action contains no `dot(s)`, `p_s=0` is a primary constraint and
`dF/ds=0` is secondary. Their on-shell Poisson bracket is

`{p_s,C_s}=-2 a0 sqrt(Y)`.

It is nonzero for `Y>0`, so the pair is locally second class and removes the
two-dimensional `(s,p_s)` phase space: this susceptibility adds zero local
propagating degrees of freedom in that restricted patch.

## Hard zero-gradient boundary

As `Y -> 0+`, `s_star`, the stationary curvature, and the constraint bracket
all vanish. The strict `s>0` chart ends and the constraint rank changes. This
is not a technical nuisance: a gapped analytic heavy sector with an invertible
Hessian would generate an analytic integer-power series near `Y=0`, not an
exact fractional `Y^(3/2)` term. Exact deep behaviour therefore requires a
critical, singular, gapless, nonlocal, or explicitly nonanalytic ingredient.

## Scope and decision

The block is an engineered representation of the desired operator, not an
ITSM microscopic derivation. It also grows relative to `Y` at high
acceleration and therefore supplies no GR join. It is useful because it turns
the broad question into one sharp calculation: embed this block in a
finite-density `rho-Theta-metric` parent and test whether the complete
constraint algebra and characteristics remain healthy through `Y=0`.

MAT-001 remains `BLOCKED`; UVIR-003 remains `IN_PROGRESS`; no downstream gate
is opened.
