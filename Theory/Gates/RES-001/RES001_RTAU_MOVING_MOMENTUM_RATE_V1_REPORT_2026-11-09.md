# Initial moving momentum lift has a first-order longitudinal force term

The [frozen component](RES001_RTAU_MOVING_MOMENTUM_RATE_V1_CONTRACT_2026-11-09.md)
extends A09.1 on the prepared initial slice. The moving reconstruction
relative to the free frame-momentum rate contains a nonzero first derivative
of the auxiliary force field. The transverse relative lifts have no such
term. The derivative remains explicit for the trace/range calculation.

## Actual moving constraint

In the original periodic chart use $D=\partial_z$, $P=D^{-1}P_0$ and
$\langle\cdot\rangle$ for the original coordinate mean. The
[canonical generator identity](RES001_RTAU_WEAK_CANONICAL_RATE_V2_REPORT_2026-11-03.md)
has spatial tangent

$$
 D[B(q)^T\delta p + (DB[\delta q])^T p]
 = e_L(\delta p\cdot Dq+p\cdot D\delta q).
$$

$B$ is linear in the fields. The actual first jet differentiates the two
terms on the left to $B^T\delta p_t+B(q_t)^T\delta p+
(DB[\delta q_t])^Tp+(DB[\delta q])^Tp_t$. This keeps the moving
metric/frame generator. At this slice both the metric and its first rate
have the registered diagonal conformal form, which gives the scalar
moving weights below at this instant.

For $i=x,y,L$ put $u_i=1/m_i$ with $m=(a^2,a^2,2a^2)$, and
$\ell_i=u_iV^z$. Let $\varrho=\delta p\cdot Dq+p\cdot D\delta q$,
$K_i=(DB_i[\delta q])^Tp$, and $x_i=-K_i+\delta_{iL}P\varrho$.
The [initial momentum lift](RES001_RTAU_MOMENTUM_RATE_LIFT_V1_REPORT_2026-11-04.md)
and [corrected Sigma reconstruction](RES001_RTAU_SIGMA_RECONSTRUCTION_REPAIR_V1_REPORT_2026-11-04.md)
give

$$
 \delta p_{e,i}=\ell_i\delta p_{f,i}+u_i(x_i+C_i),\qquad
 C_i=\frac{\eta_i-\langle\ell_i\delta p_{f,i}+u_ix_i\rangle}{\langle u_i\rangle}.
$$

$\eta_i$ is the retained eliminated-momentum mean. Compatible differentiation
requires $\langle\varrho_t\rangle=0$ in addition to the initial compatibility.
Keeping $\eta_{i,t}$ and moving the normalization gives the relative rate

$$
 \delta p_{e,i,t}-\ell_i\delta p_{f,i,t}
 =\ell_{i,t}\delta p_{f,i}
 +\mathcal P_i[u_i x_{i,t}+u_{i,t}(x_i+C_i)]
 +\frac{u_i}{\langle u_i\rangle}
       [\eta_{i,t}-\langle(\ell_i\delta p_{f,i})_t\rangle],
 \quad \mathcal P_i f=f-u_i\langle f\rangle/\langle u_i\rangle .
$$

The finite-rank term is needed even on compatible initial data. This
calculation retains mean rates as scalar inputs. It leaves their dynamical
determination and the evolution of the charge/range conditions open.

## Separation of the force derivative

In $\varrho_t$, the term $p\cdot D\delta q_t$ can be moved through the
primitive as $P_0(p\cdot\delta q_t)-P(Dp\cdot\delta q_t)$. The ordinary
canonical rates are in $H^{-1}$, the field rates are in $L^2$, and the
background rates entering the products are bounded on the prepared slice
in the [weak canonical rate owner](RES001_RTAU_WEAK_CANONICAL_RATE_V2_REPORT_2026-11-03.md).
The paired gauge terms are covered by the
[gauge rate owner](RES001_RTAU_PAIRED_GAUGE_RATE_V2_REPORT_2026-11-04.md).
For the force momentum $\xi=\delta\pi_\psi$ the
[actual force pair](RES001_RTAU_ACTUAL_FORCE_PAIR_V2_REPORT_2026-11-05.md)
has $\xi_t=dD^2\zeta+H^{-1}$ on the compatible mixed space,
where $d=bN\mu\kappa$ and $\zeta=\delta Z$. Its contribution to $\varrho_t$
has multiplier $s=D\psi$. For $g=sd$ the original periodic primitive gives

$$
 P(gD^2\zeta)=gD\zeta-g_z\zeta+2\langle g_z\zeta\rangle+P(g_{zz}\zeta).
$$

The last three terms map $L^2$ to $L^2$. The moving mean projection of
$u_i gD\zeta$ only adds an $L^2$-bounded finite-rank term because
$\langle u_i gD\zeta\rangle=-\langle D(u_i g)\zeta\rangle$.
The relative longitudinal rate therefore contains the genuine first-order
term $u_L s d\,D\zeta$, plus an $L^2$-bounded remainder at the initial slice
with the finite-dimensional rates retained. The transverse relative rates
have an $L^2$ remainder under the same conditions. This order classification
does not give a new full-generator numerical remainder constant.

The action-derived coefficient is bounded away from zero on the cell
$z\in[1.09,1.11]$ in the certified root ball, with
$u_Lsd\in[-1.905,-1.862]\,10^{-5}$ after outward rounding.
For a smooth envelope supported in that cell, choose an oscillatory clock
field proportional to $n^{-2}e^{inz}$ and zero free ordinary/frame input.
The corrected trace lift has an $H^2$ bound for these data because the
$D(Cp_{Vz})$ term vanishes for the chosen zero free momentum. The auxiliary
map therefore has $\zeta=-\kappa D^2\chi$ plus a uniformly $H^1$-bounded
metric and lower-order contribution. The weighted range and two charge
conditions are finitely many continuous linear functionals after the
initial reconstruction. Subtract a fixed smooth spanning set for their
image with coefficients tending to zero to place the oscillatory data in
their kernel. This follows from weak convergence of the bounded
oscillatory inputs and density of smooth inputs. The correction has
bounded smooth rates. Thus the first-order term grows in $L^2$ with $n$
on the compatible initial chart when considered as a separate map, even
after subtracting $\ell_L\delta p_{f,L,t}$. Its impact after the trace
Green operator and after combining physical observable terms remains
a separate calculation.

The [executable](../../../Analysis/MasterTests/test_rtau_moving_momentum_rate_v1.py)
verifies the mean-normalized differentiation and exact periodic product
rule independently of the coefficient enclosure. It checked 386 pinned
inputs and 10/10 controls. The
[receipt](../../../Analysis/MasterTests/outputs/rtau_moving_momentum_rate_v1_20261109/receipt.json)
replayed byte for byte. Next insert the isolated term into the differentiated
trace equation, classify the combined density remainder and solve the
remaining charge and gauge rate constraints. A09.1 stays open.
R-tau unadopted, review DEFERRED, physics_pass=false, gate_effect=NONE.
