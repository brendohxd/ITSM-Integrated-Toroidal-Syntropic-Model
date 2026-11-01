# Mixed operator V3 interval square representation

V2 completed its nested second variation but the raw endpoint inspection
encountered a complex interval. The stable rest norm was evaluated as
rest^T*h*rest using generic multiplication. A zero-crossing interval times
itself need not have a nonnegative lower endpoint. Its subsequent 3/2
power therefore acquired complex bounds; this is not physical complex
data and is not accepted as a real-domain result.

V3 evaluates the identical symmetric-metric form as

    sum_i h_ii*rest_i^2 + 2*sum_(i<j) h_ij*rest_i*rest_j.

The explicit powers preserve square nonnegativity on the prepared diagonal
metric. All off-diagonal metric variations and their mixed derivatives are
retained through the second sum. This is not a conformal-only force rewrite.
Add a strict positive rest-norm interval-domain guard before the 3/2 power.
Preserve V1/V2 sources, failure records and traces. No action, input domain,
field, equation, acceptance threshold or derivative control is changed.
