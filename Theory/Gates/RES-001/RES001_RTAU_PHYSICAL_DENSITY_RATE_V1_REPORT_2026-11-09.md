# Initial R-tau physical-density rate retains the force principal terms

The [frozen calculation](RES001_RTAU_PHYSICAL_DENSITY_RATE_V1_CONTRACT_2026-11-09.md)
extends A09.1 on the prepared initial compatible chart. The actual physical
density rate carries two derivatives of the retained force pair. In
particular it cannot replace the corrected variable's zero material
principal row as an $L^2$-bounded rate. After retaining the principal
terms below, the remaining initial expression is bounded in the
registered mixed norm.

## Actual projected row

Write $D=\partial_z$, $P=D^{-1}P_0$, $\mathcal M=\partial_t-SD$ and
$\langle\cdot\rangle$ for the original coordinate mean. The
[physical-density map](RES001_RTAU_DENSITY_OPERATOR_DRIFT_V2_REPORT_2026-11-09.md)
is

$$
 \delta\rho=w+cP\xi-a_\rho\xi-hD\chi+B\,\delta q-j\zeta,\qquad
 a_\rho=p/\mu,\quad h=pf_{ps},\quad j=bZ.
$$

$B$ is the row of generic force and volume coefficients in that owner.
Its clock entry vanishes when $p$ and $s$ are held independent. The
bare clock does not enter the force or volume in those variables.
The clock-gradient and momentum contributions remain explicit above.

Use the [actual force rows](RES001_RTAU_ACTUAL_FORCE_PAIR_V2_REPORT_2026-11-05.md)
with $r=d_z-\beta ds$, $v=Nf_{ps}/f_{pp}$,
$g=2\kappa(a_\phi)_z+\kappa(a_z/a)a_\phi$ and $J$ the registered
ordinary-to-auxiliary first-derivative row. In this paragraph $a$ is the
background conformal scale, distinct from $a_\rho$. Then

$$
 \mathcal M\xi=dD^2\zeta+rD\zeta-vD\xi+R_\xi,\quad
 \mathcal M\zeta=-\kappa a_\phi D^2\xi-gD\xi-vD\zeta+JDY_{18}+R_\zeta .
$$

The clock kinematics are $\mathcal M\chi=a_\phi\xi-vD\chi+
K_{\chi}\delta q+g_\chi$, with the clock's paired gauge response
$g_\chi=(D\psi)\epsilon^z$ in original-coordinate notation. The vector
gauge displacement retains its harmonic input. The force owner already
accounts for the paired metric and clock correction in $R_\zeta$.

The physical-time observable equation is

$$
\begin{aligned}
 \partial_t\delta\rho={}&SD\delta\rho
 +j\kappa a_\phi D^2\xi-a_\rho dD^2\zeta\\
 &+(a_\rho v+jg-ha_\phi)D\xi
  +(cd-a_\rho r+jv)D\zeta-jJDY_{18}+R_\rho .
\end{aligned}
$$

$J$ acts on the full ordinary chart and retains the ordinary-to-force
derivative coupling. This is an observable projection of the coupled
operator, with the corrected $w$ coordinate still used for its energy.

## All-mode remainder

Let $\mathcal D_{\rm coeff}$ denote the material coefficient derivative
of the observable map at fixed unreduced arguments. It contains the
previously bounded explicit time derivative and minus $S$ times the
coefficient-only spatial derivative. The remainder is exactly

$$
 R_\rho=R_w+\mathcal D_{\rm coeff}
 +c(C_S+F_0)-a_\rho R_\xi-jR_\zeta-h C_\chi+B\,\mathcal M\delta q ,
$$

where the original-coordinate terms are

$$
\begin{aligned}
 C_S={}&S\langle\xi\rangle-\langle S\xi\rangle-P(S_z\xi),\\
 F_0={}&-d_z\zeta+2\langle d_z\zeta\rangle+P(d_{zz}\zeta)
 +r\zeta-\langle r\zeta\rangle-P(r_z\zeta)\\
 &-v\xi+\langle v\xi\rangle+P(v_z\xi)+P R_\xi,\\
 C_\chi={}&(a_\phi)_z\xi-vD^2\chi+(S_z-v_z)D\chi+
                   D(K_\chi\delta q+g_\chi).
\end{aligned}
$$

$C_S$ is the commutator $P(SD)-SDP$ on the canonical momentum.
The clock commutator is $\mathcal M D\chi=D\mathcal M\chi+S_zD\chi$.
Both identities retain means and use the fixed original chart.

For an explicit bound write coefficient magnitudes as sup norms.
The contributions multiplying $c$ satisfy

$$
\begin{aligned}
\|C_S+F_0\|_2\le{}&
(2\|S\|_\infty+\|S_z\|_\infty+2\|v\|_\infty+\|v_z\|_\infty)\|\xi\|_2\\
&+(3\|d_z\|_\infty+\|d_{zz}\|_\infty+2\|r\|_\infty+\|r_z\|_\infty)
    \|\zeta\|_2+\|R_\xi\|_2.
\end{aligned}
$$

For $C_\chi$, the first three terms have the displayed multiplier bounds
against $\|\xi\|_2$ and $\|\chi\|_{H^2}$. The product term is bounded
by $(\|K_\chi\|_\infty+\|DK_\chi\|_\infty)\|\delta q\|_{H^1}
+\|g_\chi\|_{H^1}$. The paired gauge owner gives $H^1$ displacement
control, so smooth $D\psi$ preserves this bound.
The ordinary material field rate paired with $B$ is in $L^2$ from the
canonical velocity and gauge lifts. The corrected reconstruction bounds
$\|\xi\|_2,\|\zeta\|_2,\|\chi\|_{H^2},\|\delta q\|_{H^1}$ in the declared
compatible norm with all partners. With $U$ and $U_8$ as in the density
owner, $\|R_w\|_2\le102113U$, $\|R_\xi\|_2\le30709U$,
$\|R_\zeta\|_2\le5221U$ and the coefficient-only time drift is
at most $89U_8$. The spatial coefficient drift is a bounded product
on the same reconstruction using the spatial derivatives of the
five observable coefficients. These formulas give a finite all-mode
initial bound. A new single numerical total for $R_\rho$ was not evaluated.

## Actual nonzero order-two coefficient

$-a_\rho d=-bN\kappa p$. On $z\in[1.09,1.11]$ the whole-root enclosure
lies in $[-0.090894,-0.090893]$ after outward rounding. The prepared
compatible oscillatory family from the
[moving momentum proof](RES001_RTAU_MOVING_MOMENTUM_RATE_V1_REPORT_2026-11-09.md)
uses $\chi_n=n^{-2}f(z)e^{inz}$ supported in that cell, zero free ordinary
and clock momentum at leading order, and smooth finite-rank corrections
for the range and charge functionals. Then $\zeta_n=-\kappa D^2\chi_n$
plus a uniformly $H^1$-bounded remainder, while the free ordinary
and $\xi$ correction rates in the projected principal expression are
smooth fixed-direction terms. Pair $-a_\rho dD^2\zeta_n$ with
$f(z)e^{inz}$ using the complex $L^2$ inner product. The leading
contribution has magnitude of order $n^2$ because the coefficient
has one sign on the support. The $H^1$ error contributes at most
order $n$ after moving one derivative to the test. The first-order
terms also contribute at most order $n$. Thus the separate material
observable rate is unbounded into $L^2$ from the registered initial
state norm. This is a derivative-order statement about the observable.
It supplies no inference of a physical instability.

The [executable](../../../Analysis/MasterTests/test_rtau_physical_density_rate_v1.py)
checks the complete identity with independent Fourier convolution and
rejects omissions of the reverse coupling, means, clock gauge,
coefficient drift and clock commutator. The
[receipt](../../../Analysis/MasterTests/outputs/rtau_physical_density_rate_v1_20261109/receipt.json)
verified 388 source pins and 9/9 controls with byte-identical replay.
The moving trace/range/charge/gauge equations still require their actual
compatible transport assembly. A09.1 stays open for that part.
R-tau unadopted, review DEFERRED, physics_pass=false, gate_effect=NONE.
