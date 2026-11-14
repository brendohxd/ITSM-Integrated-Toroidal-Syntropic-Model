# Initial ordinary-current drift in all free slots

Conditional A09.1 component under the
[frozen contract](RES001_RTAU_FREE_COEFFICIENT_DRIFT_V1_CONTRACT_2026-11-13.md).
This extends the trace-input calculation to all ordinary free configuration
and momentum directions. It supplies the ordinary coefficient-drift terms
needed by the differentiated free-source equation. Clock compensation,
rate-input multipliers and moving-source composition remain open.

## Fixed-argument current rows

Use the canonical compensated current and ordinary lapse flux from the
[trace assembly](RES001_RTAU_DIFFERENTIATED_TRACE_ASSEMBLY_V1_REPORT_2026-11-09.md).
At fixed free arguments X and Y, write the ordinary parts as

    Aord X = a.X + b.DX - D(Fq.X + Fd.DX),
    Bord Y = -Uo.Yo - D(Fp.Y),
    a_i = Lo_qi + j_i - Io ell_i,
    b_i = Lo_Dqi + S^z po_i,
    ell_i = partial_qi log(N mu).

Here j_i is the field-index shift variation paired with po. The arrays
use the original fourteen-slot configuration embedding. The auxiliary
column is exactly absent from the ordinary action and flux, using the
inherited corrected-Sigma dependency proof. Per-cell interval overlap
with zero is recorded only as a consistency control. The physical
auxiliary observable retains its separate evolution and force terms.

The full current also has -M alpha D X_chi and -M c P Y_xi. Their rates
are separate outstanding compensation terms. No fixed compensated-density
charge is imposed. The original spatial and total charge constraints
remain those of the parent calculation.

## Actual coefficient derivatives

The calculation differentiates a, b, Fq, Fd, Uo and Fp at fixed free
arguments along the actual prepared initial jet. In particular

    ell_i,t = M_qi,t/M - M_qi M_t/M^2,
    a_i,t = Lo_qi,t + j_i,t - Io_t ell_i - Io ell_i,t,
    b_i,t = Lo_Dqi,t + S^z_t po_i + S^z po_i,t.

The ordinary current rate retains both measure factors. Canonical momentum
rates use the full action Euler rows, including force/regulator effects.
The lapse flux is differentiated with independent canonical momenta, so
its partials retain the background momentum rates. The certified third
spatial shift enclosure is included in the flux-rate gradient. Material
rates use U_t=a0-Lie_S q_t, with the original gauge-shift-rate cancellation.
All remaining acceleration and shift-rate bounds are inherited from the
same prepared original-coordinate Euler construction.

## Initial weak operator bounds

The coefficient rows have the following outward Euclidean sup bounds
over all sixteen circle cells and the full prepared root ball, in the
registered control units.

| Coefficient row | Outward upper bound |
| --- | --- |
| a_t | 17506.346138 |
| b_t | 2094.621428 |
| Fq_t | 0.002784719 |
| Fd_t | 0.673947171 |
| Uo_t | 411.328309 |
| Fp_t | 1.815456317 |

Pairing the divergence form against H1 tests yields

    ||Aord_t X||Hminus1 <= 19601.644297 ||X_nonaux||H1,
    ||Bord_t Y||Hminus1 <= 413.143765 ||Yo||L2.

The exact auxiliary absence makes the first bound independent of the
auxiliary input's weaker norm. The second applies to the twelve ordinary
momentum slots; the clock compensation remains explicit. These bounds
concern coefficient drift acting on initial free data. Applying the
undifferentiated rows to q_f,t in L2 or p_f,t in Hminus1 requires additional
multiplier bounds and the declared Hminus2 source space. Those uses are
not established by these sup norms alone.

## Verification and next step

The [executable](../../../Analysis/MasterTests/test_rtau_free_coefficient_drift_v1.py)
verified 397 source pins and passed 21 local controls, including all
fourteen columns and the auxiliary-absence consistency checks. The
[separate exact control](../../../Analysis/MasterTests/audit_rtau_free_coefficient_drift_v1.py)
passed five tests of the logarithmic measure-row derivative, both
canonical flux partial rates and retained product factors. These are
same-author controls. The
[receipt](../../../Analysis/MasterTests/outputs/rtau_free_coefficient_drift_v1_20261113/receipt.json)
stores the input-wise column enclosures and full dependency hashes.
Its read-only replay returned byte-identical receipt content.

Next quantify clock-compensation rates, weak rate-input multiplier norms
and the moving normalized free-momentum source, then compose the actual
Hminus2 source with the projected trace inverse. The finite constants
here are conservative initial bounds. They do not establish finite-time
accuracy, range persistence or a coupled energy/domain theorem. A09.1
INCOMPLETE, R-tau UNADOPTED, review DEFERRED, Rule9_cleared=false,
physics_pass=false, gate_effect=NONE.
