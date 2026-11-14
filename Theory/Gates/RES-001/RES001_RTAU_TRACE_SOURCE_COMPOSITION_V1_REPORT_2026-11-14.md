# Initial differentiated trace source composed in the corrected input norm

Conditional A09.1 result under the
[frozen contract](RES001_RTAU_TRACE_SOURCE_COMPOSITION_V1_CONTRACT_2026-11-14.md).
The differentiated trace source now has a numerical Hminus2 bound in
all nine registered strong/global input norms. Applying the projected
trace inverse gives an L2 bound for its reconstructed trace rate on an
exact compatible Euler/auxiliary initial jet. This completes the bounded
initial trace-source composition. The full twenty-direction generator
comparison, evolving domain and coupled energy retain their own tests.

## Assembled identity and actual inputs

Use the original canonical decomposition

    delta q = q_f+Q f,
    delta p = p_f+E(T f+b).

The [differentiated trace owner](RES001_RTAU_DIFFERENTIATED_TRACE_ASSEMBLY_V1_REPORT_2026-11-09.md)
gives the exact initial identity

    L_Sigma f_t = M w_t+M_t w
                 -A_t delta q-B_t delta p
                 -A(q_f,t+Q_t f)
                 -B[p_f,t+E(T_t f+b_t)].

Here A and B include the ordinary current, measure, clock compensation
and canonical lapse flux. The composition retains the
[full free-slot drift](RES001_RTAU_FREE_COEFFICIENT_DRIFT_V1_REPORT_2026-11-13.md),
[rough rate-input maps](RES001_RTAU_RATE_INPUT_MULTIPLIERS_V1_REPORT_2026-11-14.md),
[clock/measure weights](RES001_RTAU_SOURCE_WEIGHT_RATES_V1_REPORT_2026-11-13.md)
and [actual normalized momentum-source rate](RES001_RTAU_FREE_MOMENTUM_SOURCE_RATE_V1_REPORT_2026-11-14.md).
Each term uses its declared Sobolev order before inclusion in Hminus2.

The eight corrected reconstruction inputs are w in L2, free ordinary
configuration including moduli in H1, free canonical momentum including
xi in L2, auxiliary force in L2, force mean, and the three original
eliminated-momentum means. The ninth input is the independent adapted
harmonic coordinate velocity. Their order is inherited verbatim from
the corrected density receipt. Let U be the sum of these nine norms.

The corrected momentum and force inverses supply full field H1,
momentum L2, force H2 and trace H1 bounds in that order. The weak canonical
rows are evaluated with the actual corrective shift bound. All three
mean rates use their dynamical gauge-closed bounds. No mean is set to
zero to simplify the source.

The free configuration rate is controlled through its actual decomposition

    q_f,t = delta q_t-Q f_t-Q_t f.

The independently established direct metric trace-rate bound supplies
f_t on the right. Thus the present Green-source estimate is conditional
on the existing compatible first-jet rate calculation. It does not
bootstrap a new solution or prove an independent existence theorem.
Free momentum rates are the selected original canonical slots, bounded
by the full weak rate rows. The original density advection S D w is
retained in w_t in Hminus1.

The moving b_t contribution uses all five action-source/rate inputs and
the three individual eta_i and eta_i,t partners. The T_t f term is
retained separately. Ordinary flux derivatives of the eliminated metric
momenta vanish by the canonical flux's frame-momentum dependency; their
material-velocity multipliers remain. The clock momentum rate stays in
Hminus2 and enters through its separately bounded primitive response.

## Numerical bounds and direct comparison

All values use the original benchmark's registered control units and
normalized periodic Bessel norms. Outward bounds per U are

| Output | Upper bound |
| --- | --- |
| Complete differentiated source in Hminus2 | 19285196 |
| Projected Green trace rate in L2 | 192454154 |
| Existing independent direct metric trace rate in L2 | 203916 |

The [receipt](../../../Analysis/MasterTests/outputs/rtau_trace_source_composition_v1_20261114/receipt.json)
exports all nine coefficients and every source contribution. The two
trace-rate estimates concern the same rate on an exact compatible jet.
Their analytical identification follows from the differentiated current
and constraint identities and uniqueness of the extended projected
trace inverse, as established in the trace owner. This calculation
adds the complete numerical source estimate; it does not compare a
finite numerical centre with an exact Euler solution.

The inverse-based estimate is substantially looser than the direct one.
Large coefficient, gauge and reconstruction bounds accumulate without
using the cancellations of the direct trace formula. Neither the large
upper bound nor agreement of the identities is a physical growth-rate
measurement, stability verdict or useful finite-time accuracy result.

## Verification and next decision

The [executable](../../../Analysis/MasterTests/test_rtau_trace_source_composition_v1.py)
verified 406 source pins and passed ten controls. Exact differentiation
checks the reconstructed source equation, including moving shape,
measure and normalized-source terms. Independent rational summation
checks the outward aggregate endpoints. Harmonic velocity and all three
dynamical mean channels remain nonzero. The read-only receipt replay
was byte-identical. These are same-author controls with inherited
deferred review dependencies.

Next audit the initial twenty-direction density-operator comparison
against its full acceptance criteria, carrying the physical-density
first- and second-order force terms and every moving-map contribution.
Then advance the supported coupled-energy/domain task. Initial
trace-source completion alone does not close A09.1's wider operator
comparison or A09.2's evolution requirement. R-tau UNADOPTED,
review DEFERRED, Rule9_cleared=false, physics_pass=false, gate_effect=NONE.
