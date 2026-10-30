# V2: retain gamma(V,h) in the unit-chart Jacobian

28 October 2026. Conditional; no gate promotion. The V1 attempt is retained.

V1 passed100/104. Its four failures are the vector unit-tangent, Gram,
projector and multiplier-tangent checks. All normalized ADM Lie maps,
off-shell transport identities, covariant sector Lie controls and original
density bridges passed. The implementation differentiated n with respect
to V while treating the temporary symbolic gamma as independent.

The original chart is gamma^2=1+h_ij V^i V^j. At the local h=I point,

    J_total = partial_V(n)|gamma + partial_gamma(n)*V.T/gamma.

This required chain term is not optional. V2 changes precisely that Jacobian
construction, with an added rejection test that detects the frozen-gamma
error. All action, Lie/Ward formulas, points, tolerances and precision stay
the same. Pin and replay the failed V1 source/receipt rather than editing
them; run V2 into a fresh directory and require byte-exact replay.

Inherit every V1 scope limitation, including the unproved evolved weak
interfaces, regularity, IVP/background admission, physical window and matching.
No physical failure is inferred from this implementation error.
G1-G6 INCOMPLETE; physics_pass=false; gate_effect=NONE; review DEFERRED.
