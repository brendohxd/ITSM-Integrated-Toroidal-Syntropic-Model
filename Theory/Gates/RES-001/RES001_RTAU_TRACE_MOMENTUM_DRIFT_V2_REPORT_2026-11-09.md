# Initial drift of the projected R-tau momentum lift and frame flux

This is a Conditional A09.1 component on the registered prepared R-tau
initial root ball. It bounds the fixed-input trace part of the eliminated
momentum-map drift on all periodic modes. It also bounds one actual flux
coefficient in the weak differentiated trace source.

## Fixed-input momentum-map derivative

Use the original normalized circle mean and $P=D^{-1}P_0$, with
$\|P\|_{L^2\to L^2}=1$. In the
[differentiated trace owner](RES001_RTAU_DIFFERENTIATED_TRACE_ASSEMBLY_V1_REPORT_2026-11-09.md),
the unnormalized trace-dependent terms at fixed $f$ are

$$
 Y_i f=-p_{e,i} f\quad(i=x,y),\qquad
 Y_L f=P_{\rm tr}f/2+u_L P(R f),\qquad
 R=((Da)P_{\rm tr}-aDP_{\rm tr})/2 .
$$

Put $u_i=a^{-j_i}$ with $j=(2,2,1)$ and
$\mathcal P_i=I-(u_i/\langle u_i\rangle)\langle\cdot\rangle$.
Then $T_i=\mathcal P_iY_i$ and

$$
 \dot T_i=\mathcal P_i\dot Y_i-
   \partial_t(u_i/\langle u_i\rangle)\langle Y_i\,\cdot\,\rangle,
 \qquad
 \dot Y_L f=\dot P_{\rm tr}f/2+\dot u_L P(R f)+u_L P(\dot R f).
$$

The background momentum rates are the action Euler rows
$p_{i,t}=\mathscr L_{q_i}-D\mathscr L_{Dq_i}$. They include the actual
background shift through the action. The rate of $R$ differentiates all
four factors and includes $D\dot P_{\rm tr}$. The inherited clock-density
receipt bounds the third spatial shift derivative required by the latter.
The trace-dependent output has zero mean and zero mean rate. This split
retains the independent physical momentum means and their rates in the
source part of the full reconstruction.

Writing $L=a_t/a$ gives
$\partial_t(u_i/\langle u_i\rangle)=-j_i(u_i/\langle u_i\rangle)
(L-\langle u_i L\rangle/\langle u_i\rangle)$.
If $U_i$ bounds $\|u_i\|_\infty$ and $m_i>0$ bounds $\inf u_i$ from
below, the two operator factors are bounded by $1+U_i/m_i$ and
$j_i(U_i/m_i)(\sup L-\inf L)$. This uses the weighted mean even when
$L$ varies over the circle. All norms below use the registered control units.

| Quantity | Outward upper bound |
| --- | --- |
| $\|\dot T_x\|_{L^2\to L^2}$ | 0.000205795 |
| $\|\dot T_y\|_{L^2\to L^2}$ | 0.000216425 |
| $\|\dot T_L\|_{L^2\to L^2}$ | 0.335625 |
| $\|\dot R\|_\infty$ | 0.0195890 |

## Weak frame-flux contribution

On the registered conformal metric and its conformal first derivative,
the ordinary frame momentum flux has coefficient $C=N\gamma/a^2$ in
the $z$ slot. Its derivative retains lapse, frame and scale drift. The
spatial jet yields
$\|\dot C\|_\infty+\|D\dot C\|_\infty<1.813908$.
By duality this bounds multiplication on $H^{-1}$. Since
$\|D\|_{H^{-1}\to H^{-2}}\leq1$, the
[extended trace Green bound](RES001_RTAU_TRACE_GREEN_RATE_V2_REPORT_2026-11-09.md)
gives

$$
 \|G_2D(\dot C v)\|_{L^2}<18.102\|v\|_{H^{-1}}\qquad(v\ne0).
$$

Here $v$ is the argument of this coefficient-drift term. The complete
frame-flux derivative also contains $D(Cv_t)$, with its own rate-space
bound. The coefficient drift does not improve the Sobolev order of the
gradient of this Green response.

## Evidence and next step

The [frozen contract](RES001_RTAU_TRACE_MOMENTUM_DRIFT_V1_CONTRACT_2026-11-09.md),
[V2 executable](../../../Analysis/MasterTests/test_rtau_trace_momentum_drift_v2.py)
and [receipt](../../../Analysis/MasterTests/outputs/rtau_trace_momentum_drift_v2_20261109/receipt.json)
record the sixteen-cell enclosures, 388 verified pins, eight passing
controls and a byte-identical read-only replay. The exact periodic control
detects omitted normalization and longitudinal primitive drift. The
independent leading frame first jet is a coefficient consistency check.
The [V1 execution failure](RES001_RTAU_TRACE_MOMENTUM_DRIFT_V1_FAILURE_2026-11-09.md)
is preserved. The vault packet `ctx_b745591dc86efe75f914e77f` located the
earlier density handoff. Scientific inputs came from the pinned worktree.

To complete the trace-operator drift, the nonlocal block still needs the
material velocity coefficient rates as well as the $U_i\dot T_i$ terms
bounded here per $U_i$. The local current and other moving source terms
must also be bounded and composed in the corrected coupled norm. This
initial component supplies neither a finite-centre Euler solution nor an
evolving domain. Rule-9 review DEFERRED, Rule9_cleared=false,
physics_pass=false, gate_effect=NONE. R-tau remains unadopted.
