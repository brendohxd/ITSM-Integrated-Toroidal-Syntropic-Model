# Ordinary current maps on the initial rough rate inputs

Conditional A09.1 component under the
[frozen contract](RES001_RTAU_RATE_INPUT_MULTIPLIERS_V1_CONTRACT_2026-11-14.md).
The ordinary current now has numerical bounds on L2 configuration rates
and Hminus1 ordinary momentum rates into Hminus2. This supplies the
undifferentiated ordinary rows needed by the differentiated free source.
The moving normalized momentum-source rate and final compatible
input-wise composition remain open.

## Weak maps

Use the original canonical current rows from the
[differentiated trace assembly](RES001_RTAU_DIFFERENTIATED_TRACE_ASSEMBLY_V1_REPORT_2026-11-09.md).
For the ordinary portions, with fixed initial coefficients,

    Aord X = a.X + b.DX - D(Fq.X + Fd.DX),
    Bord Y = -Uo.Yo - D(Fp.Y),
    a_i = Lo_qi + po.Lie_(0,S_z)(basis_i) - Io partial_qi log M,
    b_i = Lo_Dqi + S^z po_i.

The canonical ordinary lapse flux and measure M=N mu are retained.
All fourteen configuration columns are evaluated. The exact auxiliary
absence from the ordinary action/flux is inherited from the corrected
Sigma dependency proof; interval overlaps are consistency controls.
Yo contains the twelve ordinary canonical momentum slots. The force
clock compensation retains its separate source-weight bounds.

Multiplication by a smooth scalar or row b on Hminus1 has norm at most
sup|b|+sup|Db|, by duality with H1. The estimate uses Euclidean slot norms
and normalized periodic Bessel norms. D maps L2 to Hminus1 and Hminus1
to Hminus2 with norms at most one. These facts give

    ||Aord X||Hminus2 <=
      (a_sup + b_multiplier + Fq_sup + Fd_multiplier) ||X_nonaux||L2,
    ||Bord Y||Hminus2 <=
      (Uo_multiplier + Fp_multiplier) ||Yo||Hminus1.

The coefficient sup norms and spatial derivative bounds are evaluated
over all sixteen original circle cells with the full prepared root
uncertainty. The certified third spatial shift enclosure is retained.
The initial field and momentum arguments remain independent for this
operator estimate. Physical use inherits the actual range/charge and
gauge reconstruction conditions.

| Coefficient norm | Outward upper bound |
| --- | --- |
| a sup | 2.792983945 |
| b multiplier on Hminus1 | 0.180115196 |
| Fq sup | 0.000207762 |
| Fd multiplier on Hminus1 | 0.707673872 |
| Uo multiplier on Hminus1 | 3.189127326 |
| Fp multiplier on Hminus1 | 1.000475027 |
| Aord from L2 to Hminus2 | 3.680980773 |
| Bord from Hminus1 to Hminus2 | 4.189602352 |

These are initial operator constants in the registered control units.
The estimates apply directly to q_f,t in L2 and ordinary p_f,t in
Hminus1 without improving their regularity. They complement the
[coefficient-drift bounds](RES001_RTAU_FREE_COEFFICIENT_DRIFT_V1_REPORT_2026-11-13.md)
on the stronger initial arguments and the
[density/clock source weights](RES001_RTAU_SOURCE_WEIGHT_RATES_V1_REPORT_2026-11-13.md).

## Evidence and remaining work

The [executable](../../../Analysis/MasterTests/test_rtau_rate_input_multipliers_v1.py)
verified 401 source pins and passed 21 local controls. It reuses the
first-differential spatial Taylor engine, with its inherited exact
controls, rather than constructing an unused action Hessian. Exact
periodic integration by parts and the multiplier product rule retain
the spatial derivative term used in duality. The
[receipt](../../../Analysis/MasterTests/outputs/rtau_rate_input_multipliers_v1_20261114/receipt.json)
stores all column norms and dependency hashes. The read-only replay
returned byte-identical receipt content.

Next quantify the actual moving normalized momentum-source rate and
compose all differentiated source pieces with the independent means,
gauge/modulus rates and compatible trace inverse. The full Hminus2
source bound, physical-map composition and finite-time coupled energy
remain incomplete. R-tau UNADOPTED, review DEFERRED,
Rule9_cleared=false, physics_pass=false, gate_effect=NONE.
