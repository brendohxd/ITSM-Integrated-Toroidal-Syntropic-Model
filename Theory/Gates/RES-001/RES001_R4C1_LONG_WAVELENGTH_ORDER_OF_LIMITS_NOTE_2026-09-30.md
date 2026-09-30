# R4C1-T2P4: a conditional long-wavelength order-of-limits test

Date: 2026-09-30. Owner: Master Test 2 / conditional R4C1-v1.
Status: `ANALYTIC_CONDITIONAL_ONLY`; `physics_pass=false`,
`gate_effect=NONE`, `Rule9_cleared=false`, `review_status=DEFERRED`.

This note asks whether the fixed-wavelength, weak-source result T2P2 rules out
*all* weak-field square-root behaviour. It does not. The example below is a
family of **different torus periods** and source amplitudes in T2P1's frozen-
frame spatial *contrast* equation. It is not a new solution of the full
action, a change to T2P1's registered `2*pi` numerical probe, or a derivation
of an ITSM galaxy law. No observational acceleration or Hubble input enters.

## Pinned parents and unaltered boundaries

| Source | SHA-256 |
|---|---|
| `RES001_R4C1_ACTION_FREEZE_2026-09-25.md` | `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3` |
| `RES001_R4C1_PERIODIC_FORCE_REPORT_2026-09-29.md` | `5f178a121aae03fb5b4d47cf383586f0496a7d18262fc5b6069dc8be0fc658ad` |
| `RES001_R4C1_WEAK_SOURCE_REPORT_2026-09-29.md` | `a47bd07a0ff07a78a1a8f08f3cf2ed8fc04939740ea5e3089596c52cb8483eb8` |
| `RES001_R4C1_COUPLED_LINEAR_LIMIT_REPORT_2026-09-29.md` | `0a947adceec27ba2b2ce3b3290928991de7d94727a7b9de9e6050b38e949b114` |
| `RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md` | `0b5f06aa3ca91876895c0f1ab521093fa44034f04ce62d605d676f9190824b1b` |

T2P2 proves source-linearity as its amplitude tends to zero on its **fixed**
torus. T2P3 proves a finite-mode coupled linear obstruction about B1, not a
bound uniform as the nonzero wavenumber tends to zero. The latter limit is
especially delicate because S1's auxiliary determinant is proportional to
`k^2` and its `k=0` chart is excluded. Nothing here changes those findings.

## Exact rescaling of the conditional contrast equation

In the dimensionless reference units of the T2P1 snapshot, take a cubic
torus of period `L=2*pi/k`, `k>0`, and a mean-zero source
`delta_rho=epsilon*cos(k*x)` independent of the other two coordinates.
Keep `A=2/7`, `b=5/11`, `beta=2/5` fixed, with `epsilon>0` small enough that
`rho_bar+delta_rho>0` for `rho_bar=1/5`. The **conditional**, not coupled,
spatial equation is

\[
  3A\,\partial_x(|\psi_x|\psi_x)-b\,\psi_{xxxx}
    =\beta\epsilon\cos(kx),\qquad \overline\psi=0.
\]

Write `y=k*x`, `g=psi_x=G*v(y)`, and

\[
  G=\sqrt{\frac{\beta\epsilon}{3Ak}},\qquad
  \delta=\frac{b k^2}{3AG}
         =\frac{b k^{5/2}}{\sqrt{3A\beta\epsilon}}.
\]

Integrating once and imposing the odd solution gives the exact periodic ODE

\[
  |v|v-\delta v''=\sin y,\qquad v(y+2\pi)=v(y),\quad v(-y)=-v(y).
\]

For every `delta>0`, the strictly convex functional

\[
 I_\delta[v]=\int_0^{2\pi}\left(
  \frac{|v|^3}{3}+\frac\delta2(v')^2-\sin(y)v\right)dy
\]

has one periodic `H^1` minimizer. Reflection plus uniqueness makes it odd,
so its mean is zero and it integrates to a periodic, mean-zero `psi`. As
`delta -> 0`, these minimizers converge **strongly in `L^3`** to
`v_0(y)=sgn(sin y)*sqrt(abs(sin y))`. To see this without a grid claim:
coercivity bounds them in `L^3`; weak subsequential limits minimize the
strictly convex `I_0`, by lower semicontinuity and smooth recovery sequences.
The unique minimizer is `v_0`. Convergence of the energies and of the linear
pairing then gives convergence of the `L^3` norms, hence strong `L^3`
convergence by uniform convexity. No pointwise error bound near the sine
nodes is claimed.

At **fixed** `k>0`, `epsilon -> 0` makes `delta -> infinity`; the regulator
recovers the T2P2 source-linear limit. But along the separately declared
family `epsilon=k^4`, `k -> 0`, one has

\[
 \delta=\frac{b}{\sqrt{3A\beta}}k^{1/2}\to0,\quad
 G=\sqrt{\frac\beta{3A}}k^{3/2}\to0,\quad
 \|\psi\|_\infty=O(G/k)=O(k^{1/2})\to0.
\]

The last bound follows from the uniform `L^3` bound on `v_delta` and the
one-dimensional periodic primitive. The contrast amplitude also tends to
zero as `k^4`. Thus a weak scalar potential and gradient can coexist with
dominance of the cubic-gradient term **in this family of static contrast
problems**. More generally, `k^5 << epsilon << k^3` is the formal overlap
between small `delta` and small scalar-potential amplitude, in these fixed
reference units. It is not a demonstrated physical EFT interval.

For comparison only, define the auxiliary periodic Newtonian potential by
`Phi_bar,xx=4*pi*G_ref*epsilon*cos(k*x)` with fixed `G_ref>0`. Then
`|Phi_bar,x|=(4*pi*G_ref*epsilon/k)*abs(sin y)` and its potential amplitude
is `O(epsilon/k^2)`. Along `epsilon=k^4` it is also weak. Away from sine nodes,
the signed scalar-gradient shape approaches the signed square root of that
auxiliary Newtonian force; globally, strong `L^3` convergence gives the same
normalized profile statement. Its *conditional* amplitude factor is

\[
 C_{\rm contrast}=\beta\sqrt{\frac{\beta}{12\pi A G_{\rm ref}}}.
\]

This factor depends on the freely chosen `A` and auxiliary `G_ref`; it is
**not** `C_chi`, `a0`, a derived `2/3` projection, or an action-derived
effective Newton constant. A pointwise ratio at a sine node is undefined.

## Decision and required next physics

The fixed-scale and joint long-wavelength limits do not commute in this
conditional elliptic reduction. Therefore T2P2/T2P3 must not be enlarged
into an all-scales no-go for square-root *shape*. Conversely, this new
family does not establish a physical weak-field window: its changing torus
period is outside T2P1's registered probe; the B1 mean field evolves; and
metric, frame, dust, Euler, time-derivative and regulator/EFT errors have
not been bounded. In particular, S1's `k -> 0` constraint inversion is not
uniformly justified. These omissions could remove the apparent window.

The next decisive Test-2 calculation is a **coupled**, on-shell
long-wavelength/source double-scaling analysis with a physical cutoff and
controlled quasistatic remainder. Until then `canonical_Test2_pass=false`;
Master Tests 1 and 3, MAT-001, UVIR-003, Stage 4A and all publication holds
are unchanged. Rule-9 review remains deferred, not cleared.
