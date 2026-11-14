# Differentiated R-tau trace reconstruction on the compatible initial jet

The [frozen calculation](RES001_RTAU_DIFFERENTIATED_TRACE_ASSEMBLY_V1_CONTRACT_2026-11-09.md)
assembles the actual compensated trace equation at the prepared first
jet. Its differentiated source lies in $H^{-2}$ under the declared
canonical and gauge rate hypotheses. On an exact compatible
Euler/auxiliary jet, the projected Green solution equals the direct
metric trace rate. The two leading background coefficient drifts are
enclosed numerically. The lower-order coefficient norms have not yet
been composed into a single outward numerical estimate.

## Canonical compensated current

Use original periodic coordinates, $D=\partial_z$ and $P=D^{-1}P_0$.
Put $M=N\mu$ and $I_o=I_{\rm other}=M\Sigma$. The
[corrected Sigma owner](RES001_RTAU_SIGMA_RECONSTRUCTION_REPAIR_V1_REPORT_2026-11-04.md)
constructs $I_o$ with the force and regulator removed from the
current calculation. Its canonical lapse flux $F$ is the frame
momentum and spatial curvature improvement with the regulator term
removed. In particular $F_p$ has support only in the ordinary frame
momenta. The clock momentum remains in the total spatial constraint.

Write $U_o$ for the ordinary material velocities and use the
[canonical graph coefficients](RES001_R4C1_RTAU_CANONICAL_DENSITY_GRAPH_V2_REPORT_2026-11-01.md)
in the compensated sector. Before integrating the lapse improvement
by parts their local rows are $A=L^o_q+B(S_z)^Tp_o$ and
$B_{\!d}=L^o_{Dq}+S^zp_o$, with the indices embedded in the full
configuration space and $B(S_z)^Tp_o$ the field-index variation of
the spatial Lie derivative. Let $\ell_M\delta q=\delta\log M$.
Define

$$
\begin{aligned}
\mathcal A X={}& A X+B_{\!d}DX-D(F_qX+F_dDX)
                     -I_o\ell_M X-M\alpha D X_\chi,\\
\mathcal B Y={}&-U_oY_o-D(F_pY)-McP Y_\xi .
\end{aligned}
$$

The exact canonical current relation becomes
$\mathcal A\delta q+\mathcal B\delta p=Mw$.
It uses $\delta\Sigma=w+cP\xi+\alpha D\chi$ and keeps the measure
term $I_o\delta\log M$. In particular it does not use a zero
compensated-density mean or impose another charge condition.

## Moving momentum normalization and trace operator

Write $\delta q=q_f+Q_f f$ with $Q_f f$ occupying the two transverse
diagonal entries $a^2 f$. Keep $q_f$ in its original gauge representation,
including the moving adapted moduli weights. Write
$\delta p=p_f+E(Tf+b)$, where $E$ inserts the three eliminated
canonical momentum slots. The [periodic inverse](RES001_R4C1_RTAU_COUPLED_PERIODIC_INVERSE_V1_REPORT_2026-11-01.md)
gives the following pre-normalized outputs:

$$
\begin{aligned}
 y_i&=-p_{e,i}f+a^{-2}P s_i &&(i=x,y),\\
 y_L&=\frac{P_{\rm tr}f}{2}+a^{-1}P(Rf+\omega s_L),\qquad
 \omega=\frac1{2a}.
\end{aligned}
$$

Set $u_i=a^{-2}$ for the transverse entries and $u_L=a^{-1}$.
Normalize as $\mathcal N_i(y_i,\eta_i)=y_i+u_i
(\eta_i-\langle y_i\rangle)/\langle u_i\rangle$. Splitting the terms
linear in $f$ from the free source/mean terms defines $Tf+b$.
The actual $s_i$ is

$$
 s_i=-D\big[B_i^Tp_f+(DB_i[q_f])^Tp\big]
         +\delta_{iL}(p_f\cdot Dq+p\cdot Dq_f).
$$

Differentiate this product rule along the actual rates, replacing
each of $B_i,p_f,q_f,p,Dq,Dq_f$ by its rate in turn.
In particular $\dot B_i=B_i(q_t)$ and the rate of $DB_i[q_f]$
is $DB_i[q_{f,t}]$ by linearity. No scalar shift or independent
frozen source rate is substituted.

For the part independent of $f_t$ the derivatives of the
pre-normalized outputs are

$$
\begin{aligned}
 y_{i,t}^{\rm rest}&=-p_{e,i,t} f+(a^{-2})_t P s_i+a^{-2}P s_{i,t},\\
 y_{L,t}^{\rm rest}&=P_{{\rm tr},t}f/2+(a^{-1})_t P(Rf+\omega s_L)\\
     &\quad +a^{-1}P(R_t f+\omega_t s_L+\omega s_{L,t}).
\end{aligned}
$$

Here $p_{e,i,t}$ in the first formula is the **background** rate.
If $C_i=(\eta_i-\langle y_i\rangle)/\langle u_i\rangle$,
the rest of the normalized lift is exactly

$$
 (\dot T f+\dot b)_i
 =y_{i,t}^{\rm rest}+\dot u_i C_i
 +u_i\frac{\dot\eta_i-\langle y_{i,t}^{\rm rest}\rangle
                         -\langle\dot u_i\rangle C_i}{\langle u_i\rangle}.
$$

Use the actual $\dot\eta_i$ and gauge/modulus rates from the
[mean and trace owner](RES001_RTAU_GAUGE_MEAN_TRACE_RATE_V2_REPORT_2026-11-09.md).
This keeps the weighted normalization and the original means.
The Ward range and charge conditions from their
[owning calculation](RES001_RTAU_WARD_RANGE_RATE_V2_REPORT_2026-11-09.md)
apply to the exact compatible jet. The projected solve by itself
does not impose them.

## Assembled differentiated equation

With $L_\Sigma=\mathcal A Q_f+\mathcal B E T$ at this slice, the
differentiated source is

$$
\begin{aligned}
 L_\Sigma f_t={}&M w_t+\dot M w
  -\dot{\mathcal A}\delta q-\dot{\mathcal B}\delta p\\
 &-\mathcal A(q_{f,t}+\dot Q_f f)
  -\mathcal B\big[p_{f,t}+E(\dot T f+\dot b)\big].
\end{aligned}
$$

$\dot{\mathcal A}$ and $\dot{\mathcal B}$ differentiate every displayed
coefficient at fixed test arguments. In particular they retain the
derivatives of $F_q,F_d,F_p$, $I_o\ell_M$, $M\alpha$, $Mc$ and $U_o$.
The flux derivatives are the chain rule along the actual background
configuration, gradients and canonical momenta. The rate of $U_o$
is obtained by differentiating its temporal Legendre equation with
the actual background momentum and field rates. The pure-shift
velocity response cancels when passing to material velocity.
$\dot Q_f f$ is $2LQ_f f$ with $L=a_t/a$; the rate of the free
adapted chart weights belongs to $q_{f,t}$. Thus the entire moving
lift, rather than only the local second derivative, enters the
coefficient drift.

The coefficient terms are evaluated on the smooth prepared first
jet. The rough input assignments can be read without improving
any weak rate: $q_{f,t}\in L^2$, ordinary $p_{f,t}\in H^{-1}$,
clock $\xi_t\in H^{-2}$ and $w_t\in H^{-1}$ with physical advection.
Only ordinary frame momentum rates enter $D(F_p p_{f,t})$.
The clock momentum rate enters the current through $P\xi_t\in H^{-1}$.
The actual spatial source rates are in $H^{-2}$ and the primitive
raises them one order. The normalized momentum terms have weak
$H^{-1}$ rates, with their means interpreted as smooth dual
pairings. The drift acting on the initial reconstructed fields
uses $H^1$ configurations and $L^2$ momenta. These assignments
place the assembled source in $H^{-2}$.

On an exact compatible Euler/auxiliary jet the actual corrected
current and spatial Ward identities hold. Substituting the
gauge-closed field and momentum rates therefore gives this
differentiated equation with the direct metric rate
$f_t=(\delta\dot h_{xx}+\delta\dot h_{yy})/(2a^2)-2Lf$.
By uniqueness of the [extended projected trace inverse](RES001_RTAU_TRACE_GREEN_RATE_V2_REPORT_2026-11-09.md)
from $H^{-2}$ to $L^2$, the Green reconstruction equals that direct
rate on the exact compatible jet. This is an analytical comparison.
It does not substitute a finite numerical centre for an exact
solution or give a numerical residual comparison at that centre.

## Leading drift and checks

For the actual background $A_2=-Na$ and $C=N\gamma/a^2$.
Hence $\dot A_2=A_2(-\beta\psi_t+L)$ and
$\dot C=C(-\beta\psi_t+\dot\gamma/\gamma-2L)$.
First time jets of the full metric/frame $\gamma$ and lapse give
outward whole-root enclosures

$$
 \dot A_2\in[-0.786943,-0.786108],\qquad
 \dot C\in[-1.814007,-1.812094].
$$

The [executable](../../../Analysis/MasterTests/test_rtau_differentiated_trace_assembly_v1.py)
verifies the exact separated rate against direct differentiation
in a nonconstant periodic control with moving means and source
weights. It also checks the actual leading coefficients and 389
source pins. All 12 controls passed and the
[receipt](../../../Analysis/MasterTests/outputs/rtau_differentiated_trace_assembly_v1_20261109/receipt.json)
replayed byte for byte. A09.1 remains open for the complete
numerical lower-order drift estimate and its assembly into the
coupled energy. R-tau unadopted, review DEFERRED, physics_pass=false,
gate_effect=NONE.
