# Initial nonlocal trace-operator drift on the prepared R-tau jet

Conditional A09.1 result, 13 November 2026. The
[frozen contract](RES001_RTAU_NONLOCAL_TRACE_DRIFT_V1_CONTRACT_2026-11-09.md)
is completed for the nonlocal momentum block of the initial compensated
trace operator. The local current drift and full coupled energy remain open.

## Actual material rate

Use the original periodic coordinates and the same prepared action, root
ball and control units as the
[initial acceleration construction](RES001_R4C1_RTAU_INITIAL_ACCELERATION_V1_REPORT_2026-11-01.md).
Let $v=q_t$, $S$ be the background shift and $U=v-\mathcal L_Sq$.
The original-coordinate affine Euler equation gives
$q_{tt}=a_0+\mathcal L_{S_t}q$, with $a_0=M^{-1}R$ from the full action.
The tensor representations used in the shift Lie action are linear in
$q,Dq$. Consequently

$$
 U_t=q_{tt}-\mathcal L_{S_t}q-\mathcal L_Sv
     =a_0-\mathcal L_Sv.
$$

This retains the gauge shift rate through its exact cancellation. Setting
it to zero before differentiating would omit a required term. The
existing certified bound on the thirteen-component $a_0$ bounds each
of the three metric momentum coefficients. The Lie term is evaluated
on all sixteen inherited spatial cells with the full prepared root
uncertainty and actual velocity gradients. It uses only the shift and
its first derivative, so the unused higher shift jet can be set to zero
in this particular coefficient evaluation.

## Nonlocal block and all-mode estimate

The corrected trace operator contains
$K_{\rm mom}=-\sum_{i=x,y,L}U_iT_i$, where the $T_i$ are the original
mean-normalized eliminated-momentum lifts. Therefore

$$
 \dot K_{\rm mom}=-\sum_i(\dot U_iT_i+U_i\dot T_i),\qquad
 \|\dot K_{\rm mom}\|_{L^2\to L^2}
 \leq\sum_i(\|\dot U_i\|_\infty\|T_i\|
                         +\|U_i\|_\infty\|\dot T_i\|).
$$

The [momentum-drift receipt](../../../Analysis/MasterTests/outputs/rtau_trace_momentum_drift_v2_20261109/receipt.json)
supplies the normalized $\dot T_i$ bounds. The $T_i$ bounds are assembled
from its stored coefficient enclosures, including the longitudinal
primitive and all weighted mean terms. These bounds apply to all periodic
$L^2$ inputs. They introduce no Fourier truncation or extra compatibility
condition. Physical inputs still require the inherited range and charge
constraints.

| Bound in registered control units | Outward upper bound |
| --- | --- |
| $\|\dot U_x\|_\infty$ | 118.739285 |
| $\|\dot U_y\|_\infty$ | 118.739285 |
| $\|\dot U_L\|_\infty$ | 118.751099 |
| Transverse $x$ contribution to $\|\dot K_{\rm mom}\|$ | 0.001795724 |
| Transverse $y$ contribution | 0.002260530 |
| Longitudinal contribution | 228.395054 |
| Total $L^2\to L^2$ bound | 228.399110 |
| $\|G_2\dot K_{\rm mom}\|_{L^2\to L^2}$ | 2279.279844 |

The last line composes the total with the existing projected inverse
$G_2:H^{-2}\to L^2$, using the norm-one inclusion $L^2\subset H^{-2}$.
It controls this source contribution to the trace rate. The operator
derivative is at fixed trace input, while the full product rate also
contains the separate $K_{\rm mom}f_t$ term. All spaces use the normalized
periodic Bessel norms of the parent calculations.

The large longitudinal bound inherits the conservative particular
acceleration enclosure. It supplies a finite operator estimate, with
no conclusion about measured growth, useful evolution accuracy, a
physical cutoff or a finite-time admissible domain.

## Verification and remaining work

The [executable](../../../Analysis/MasterTests/test_rtau_nonlocal_trace_drift_v1.py)
verified 391 source pins and ten local controls. A nonconstant exact
rank-two tensor control checks cancellation of the shift rate and detects
omission of the Lie-velocity term. A separate product identity retains
both contributions to the block derivative. The
[receipt](../../../Analysis/MasterTests/outputs/rtau_nonlocal_trace_drift_v1_20261113/receipt.json)
replayed byte for byte and contains the full binary bounds and source pins.
These are same-author checks. Inherited Euler and reconstruction hypotheses
apply on the exact compatible initial jet. The finite numerical centre
retains its separate residual interpretation.

Next quantify the local compensated-current coefficient drift and moving
source terms, then compose them with this block in the corrected coupled
norm. The initial full comparison and the evolving energy/domain
calculation remain incomplete. R-tau UNADOPTED, review DEFERRED,
Rule9_cleared=false, physics_pass=false, gate_effect=NONE.
