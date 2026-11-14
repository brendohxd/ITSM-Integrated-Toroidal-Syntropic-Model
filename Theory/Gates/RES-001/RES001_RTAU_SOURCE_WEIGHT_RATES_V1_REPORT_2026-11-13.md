# Initial density and clock source-weight rates

Conditional A09.1 source component under the
[frozen contract](RES001_RTAU_SOURCE_WEIGHT_RATES_V1_CONTRACT_2026-11-13.md).
This calculation supplies numerical measure and clock-compensation
weights for the differentiated free-source equation. The ordinary
rate-input multipliers and moving momentum-source rates remain open.

## Coefficients and spaces

Use M=N mu, P=D^{-1}P0 and the original corrected normal-form c and alpha.
The source equation retains Mw_t+M_t w and the compensation rates
-(M alpha)_t D chi-M alpha D chi_t-(Mc)_t P xi-Mc P xi_t.
The original periodic mean is retained; P annihilates only its prescribed
zero mode and supplies no new charge condition.

The initial conformal metric and its first time jet give

    M = exp(-beta psi) a^3,
    M_z = M(-beta psi_z+3 a_z/a),
    M_t = M(-beta psi_t+3 a_t/a).

The measure rates are enclosed over the whole prepared root ball and
circle. The corrected source chart reuses the original normal-form
c, c_z, c_t and alpha, alpha_z, alpha_t bounds. Product rules give

    ||(Mc)_t||sup <= ||M_t||sup ||c||sup+||M||sup ||c_t||sup,
    ||(M alpha)_t||sup <= ||M_t||sup ||alpha||sup+||M||sup ||alpha_t||sup.

These terms multiply P xi in L2 and D chi in L2. For the rougher rates,
multiplication by a smooth b has Hminus1 norm at most
||b||sup+||b_z||sup by duality with H1. The periodic derivative has
L2-to-Hminus1 norm at most one. On the nonzero integer Fourier modes,
P has Hminus2-to-Hminus1 norm at most sqrt(2), conservatively bounded
by two here. These facts justify the rate-input maps without improving
the regularity of chi_t or xi_t.

| Source contribution or coefficient | Outward upper bound |
| --- | --- |
| M_t multiplying w in L2 | 2.521163926 |
| (Mc)_t multiplying P xi in L2 | 0.011679746 |
| (M alpha)_t multiplying D chi in L2 | 0.000330327 |
| M multiplying w_t in Hminus1 | 1.000528151 |
| M alpha D chi_t from L2 to Hminus1 | 0.000124542 |
| Mc P xi_t from Hminus2 to Hminus1 | 0.000470441 |

All values use the registered control units and periodic Bessel norms.
These are individual source weights; actual state/rate reconstruction
and the full input-wise source composition retain their own bounds.

## Evidence and remaining work

The [executable](../../../Analysis/MasterTests/test_rtau_source_weight_rates_v1.py)
verified 399 source pins and six local controls. Exact symbolic controls
check the measure/product rates and periodic weak derivative pairing.
The Fourier multiplier ratio is checked algebraically; the integer-mode
lower bound |k|>=1 supplies the stated primitive norm. The
[receipt](../../../Analysis/MasterTests/outputs/rtau_source_weight_rates_v1_20261113/receipt.json)
contains the binary enclosures and input hashes. Its read-only replay
returned byte-identical receipt content.

The ordinary free-slot coefficient-drift result and these source weights
can now enter the actual free-source assembly. Needed next are the
ordinary rate-input multiplier norms, moving normalized momentum-source
rates, their dynamical means and the final compatible input-wise
composition. A09.1 INCOMPLETE, R-tau UNADOPTED, review DEFERRED,
Rule9_cleared=false, physics_pass=false, gate_effect=NONE.
