# Actual free-momentum source rates and moving normalization

Conditional A09.1 result under the
[frozen contract](RES001_RTAU_FREE_MOMENTUM_SOURCE_RATE_V1_CONTRACT_2026-11-14.md).
The actual canonical source rates now have input-wise Hminus2 bounds.
After the periodic primitive and moving mean normalization, the three
free eliminated-momentum rates have Hminus1 bounds. These are the
projected reconstruction maps; physical use still requires the original
range and charge conditions.

## Actual source derivative

Use the original generator columns B_i(q), linear in the configuration.
With p the full background canonical momentum and p_f the free momentum,

    s_i = -D[B_i(q).p_f + DB_i[q_f].p]
          + delta_iL (p_f.Dq + p.Dq_f).

Its time derivative differentiates all eight background/argument factors.
In particular the derivative inside D contains B_i(q_t).p_f,
B_i(q).p_f,t, DB_i[q_f,t].p and DB_i[q_f].p_t. The scalar longitudinal
part contains p_f,t.Dq, p_f.Dq_t, p_t.Dq_f and p.Dq_f,t. The background
p_t uses the full action Euler rows; its clock component is retained.
The scalar free clock momentum rate has its own Hminus2 input norm.
Its column in B_i is exactly zero, so it enters only the longitudinal
scalar term. Multiplication there uses the Hminus2 norm of Dpsi, bounded
by its sup norm plus twice its first-derivative sup norm plus its
second-derivative sup norm. This keeps the weaker clock-rate assignment.

The source s_i is bounded in Hminus1 for q_f in H1 and p_f in L2.
For its derivative, q_f,t stays in L2, ordinary p_f,t stays in Hminus1,
and the clock momentum rate stays in Hminus2. Product duality and the
weak divergence form put the actual source rate in Hminus2. All thirteen
nonauxiliary background momenta are used here, in contrast to the
ordinary-only momenta of the compensated current row. The auxiliary
momentum is the inherited identically zero primary constraint.

## Integrating factor and retained means

At zero trace input let u=(a^-2,a^-2,a^-1) and omega=(1,1,1/(2a)).
The free reconstruction is

    y_i = u_i P(omega_i s_i),
    n_i = u_i/mean(u_i),
    b_i = y_i+n_i(eta_i-mean(y_i)),
    b_i,t = (I-n_i mean)y_i,t - n_i,t mean(y_i)
            +n_i eta_i,t+n_i,t eta_i,
    y_i,t = u_i,t P(omega_i s_i)
            +u_i P(omega_i,t s_i+omega_i s_i,t).

P is the original zero-mean periodic primitive. Its Hminus1-to-L2 and
Hminus2-to-Hminus1 norms are bounded conservatively by two. Multipliers
on Hminus1 use sup plus first derivative; multipliers on Hminus2 use
sup plus twice first derivative plus second derivative. The eta_i are
the original prescribed physical momentum means; eta_i,t must be taken
from the dynamical mean owner when closing the final estimate.

For u_i=a^-j and L=a_t/a, n_i,t=-j n_i(L-mean(u_i L)/mean(u_i)).
The full-circle L enclosure bounds this term without freezing the
weighted mean. The sixteen cells retain the full prepared root
uncertainty and the certified third spatial shift enclosure.

## Input-wise normalized rate bounds

Each column below bounds the indicated component of b_t in Hminus1.
Values are outward upper bounds in the registered control units.

| Input norm | Transverse x | Transverse y | Longitudinal |
| --- | --- | --- | --- |
| q_f in H1 | 14.483315 | 14.483315 | 19.820016 |
| p_f in L2, including clock momentum | 13.872888 | 13.872888 | 13.875032 |
| q_f,t in L2 | 7.643933 | 7.643933 | 7.912972 |
| Ordinary p_f,t in Hminus1 | 4.002633 | 4.002633 | 4.004340 |
| Clock momentum rate in Hminus2 | 0 | 0 | 0.001235644 |
| Absolute value of the corresponding eta_i | 0.000315617 | 0.000315617 | 0.000157785 |
| Absolute value of the corresponding eta_i,t | 1.000307740 | 1.000307740 | 1.000153858 |

The receipt separately stores the action-source s_i and s_i,t bounds.
It also composes b_t with the ordinary current's eliminated-metric
momentum slots using their actual Hminus1 multiplier norms. The ordinary
lapse flux depends on frame momenta, so it contributes no spatial
derivative of these three eliminated metric momentum rates.

The weak estimate retains the earlier longitudinal first-order force
term through the actual clock momentum rate. It does not replace the
previous L2 obstruction with an L2 rate bound. The known field, momentum,
gauge/modulus and dynamical mean estimates must still be substituted
into these input-wise maps before the full source is closed in the
registered mixed norm.

## Verification and remaining composition

The [executable](../../../Analysis/MasterTests/test_rtau_free_momentum_source_rate_v1.py)
verified 403 source pins and passed eleven controls. Exact nonconstant
periodic controls compare the full source product derivative and
normalized lift derivative, preserve eta_i,t, and detect omission of
normalization, integrating-factor and total clock-momentum terms.
The [receipt](../../../Analysis/MasterTests/outputs/rtau_free_momentum_source_rate_v1_20261114/receipt.json)
contains the complete source/rate matrices and column order.
The read-only replay returned byte-identical receipt content.

Next substitute the actual gauge-closed field and free momentum rate
bounds, dynamical means and initial reconstruction constants into the
full differentiated trace source. Retain the coefficient drift and
physical-density principal force terms, then compare with the independent
direct trace-rate bound. A09.1 INCOMPLETE, full coupled evolution OPEN,
R-tau UNADOPTED, review DEFERRED, Rule9_cleared=false,
physics_pass=false, gate_effect=NONE.
