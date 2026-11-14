# Initial weak local trace drift and momentum-block composition

Conditional A09.1 calculation under the
[frozen contract](RES001_RTAU_LOCAL_TRACE_DRIFT_V1_CONTRACT_2026-11-13.md).
The local compensated trace row has finite coefficient-rate bounds on
the prepared root ball. Together with the
[nonlocal momentum-block drift](RES001_RTAU_NONLOCAL_TRACE_DRIFT_V1_REPORT_2026-11-13.md),
these give an initial moving trace-operator bound from H1 to Hminus1.
The differentiated free source and full coupled energy remain open.

## Weak local operator

Let D denote the original periodic spatial derivative, h=a^2 and
Q f the transverse metric trace shape with entries h f in slots hxx
and hyy. Write Lo for the ordinary action with the force and regulator
removed by the established action split. Let po be its momenta and
U=q_t-Lie_S q. The compensated ordinary current is

    Io = Lo - po.U - D Fo,
    Fo = N gamma sum_i(hinv[i,z] po[V_i]) - N curvature_flux/2.

The ordinary clock and auxiliary momenta vanish by the inherited exact
action-dependency proof. Their removal here does not remove them from
the total momentum and charge constraints.

Define b=Lo_Dq+S^z po and the field-index row j by
j.X=po.Lie_(0,S_z) X with the field gradient held fixed. In the
transverse trace slots the local row is

    Lloc f = A f+B Df-D(C f+E Df),
    A = h(Lo_qxx+Lo_qyy) + j.Q + (D h)(b_xx+b_yy) - Io,
    B = h(b_xx+b_yy),
    C = Fo_q.Q+Fo_Dq.DQ,
    E = Fo_Dq.Q.

The term -Io retains the variation of the original measure M=N mu,
since delta log M=f in this trace direction. The scalar-compensation
terms involving chi and xi belong to the free source. They have no
additional trace input in this local block.

At fixed scalar test f, differentiating the moving Q and DQ gives

    (Lloc)_t f = A_t f+B_t Df-D(C_t f+E_t Df).

The coefficient calculation retains the derivatives of every displayed
factor. In particular Q_t has entries h_t in the two trace slots, and
its spatial derivative has entries D h_t. The original material-rate
identity U_t=a0-Lie_S q_t supplies the current rate. Canonical po_t
comes from the total action Euler rows Ltotal_q-D Ltotal_Dq. Although
the force/regulator sectors have no ordinary temporal momentum, their
field and gradient dependence contributes to these momentum rates.
The numerical evaluation retains those contributions.

For the time derivatives of Lo_q and Lo_Dq, the evaluator retains only
mixed action/time second derivatives. This avoids computing the unused
full Hessian. The time direction includes the full original-coordinate
acceleration and shift-rate enclosures, q_t, Dq_t and the prepared
auxiliary first rate. The lapse-flux derivative uses independent
canonical momenta and their Euler rates. Its spatial derivative also
uses the certified third spatial shift derivative from the clock-density
owner. Future conformal evolution is not assumed.

## Bounds and composition

All quantities use the registered original-coordinate control units and
normalized periodic Bessel norms. The bounds include all sixteen cells
and the entire prepared root uncertainty.

| Quantity | Outward upper bound |
| --- | --- |
| sup norm of A_t | 14577.982908 |
| sup norm of B_t | 2161.736137 |
| sup norm of C_t | 0.001319664 |
| sup norm of E_t | 0.793272890 |
| Local H1 to Hminus1 operator norm | 16740.513637 |
| Local plus nonlocal H1 to Hminus1 drift norm | 16968.912747 |

The weak bound follows by pairing the displayed divergence form against
an H1 test and applying Cauchy-Schwarz to each term. It needs no spatial
derivative of the coefficient rates. The nonlocal L2-to-L2 result embeds
in this same H1-to-Hminus1 estimate with norm-one inclusions. This bounds
the derivative of the moving trace operator on the initial jet. The
full time derivative of its output separately retains L f_t.

The constants are conservative, principally because of the inherited
acceleration and gauge enclosures. They give no finite-time accuracy,
physical stability or usable interaction-window conclusion.

## Verification and preserved corrections

The [V3 executable](../../../Analysis/MasterTests/test_rtau_local_trace_drift_v3.py)
verified 394 source pins and five local controls. The
[separate exact control](../../../Analysis/MasterTests/audit_rtau_local_trace_drift_v1.py)
passed five checks for mixed derivatives with a moving shape, the weak
divergence rate, measure-rate contribution and retained periodic mean.
It exercises the same mixed-time algebra engine as V3 through the
preserved V2 module. These are same-author implementation controls.

The [V1 failure](RES001_RTAU_LOCAL_TRACE_DRIFT_V1_FAILURE_2026-11-13.md)
preserves an interval positivity failure from the diagonal-product form.
The [V2 hold](RES001_RTAU_LOCAL_TRACE_DRIFT_V2_HOLD_2026-11-13.md)
preserves its omitted third-shift input and held bounds. V3 restores that
certified input. The original sources, sidecars and V2 receipt remain.

The [V3 receipt](../../../Analysis/MasterTests/outputs/rtau_local_trace_drift_v3_20261113/receipt.json)
records the complete binary enclosures and source pins. Its read-only
replay completed with byte-identical receipt content.

Next compose the actual differentiated free-source rates and physical
map terms in the corrected coupled norm. Initial weak boundedness of
the trace-operator drift does not establish range persistence, an exact
finite-centre Euler solution or an evolving energy/domain tube. R-tau
UNADOPTED, review DEFERRED, Rule9_cleared=false, physics_pass=false,
gate_effect=NONE. A09.1 and the full coupled programme remain incomplete.
