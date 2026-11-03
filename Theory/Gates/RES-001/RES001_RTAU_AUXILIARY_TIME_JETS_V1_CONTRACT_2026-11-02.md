# Prepared R-tau auxiliary time-spatial jets V1

High explicitly confirmed 2 November. This bounded calculation supplies a
missing derivative block required by the physical-norm contract, not a substitute
for its global compatible-domain/physical estimate. R-tau remains unadopted.

From Z=-Delta_h psi in the existing planar sector, derive partial_t Z and its
first two spatial derivatives for the full six-component metric. Fixed-coordinate
time derivative only: callers must supply velocities in that same coordinate;
do not freeze a moving gauge, infer background existence, or remove physical flow.

Set A=h^{zz}, B=A tr(h^{-1} h_z)/2-(h^{-1} h_z h^{-1})^{zz}.
Then Z=-A psi_zz-B psi_z and
Z_t=-(A_t psi_zz+A psi_tzz+B_t psi_z+B psi_tz).
Differentiate with full Leibniz rule through two z derivatives. Return actual
derivatives, not Taylor coefficients. Required data: h, h_t through z order 3,
psi, psi_t through order 4. Missing jets must raise, not be filled with zero.
Require invertible physical spatial metric; indefinite examples are rejected.

Use exact rational Taylor arithmetic, differentiating the inverse metric by
its algebraic identity and retaining every metric cross term. Independently
compare against direct symbolic differentiation of the Laplace-Beltrami formula
for nonconstant positive full metrics and scalar/time profiles. Include constant
metric and pure spatial Lie transport controls and rejection tests for missing
jets/nonphysical metric. Exact equality is the frozen local algebra criterion.
Preserve and hash sources; fresh receipt, source-pinned read-only replay.

Derivative bookkeeping: the explicit auxiliary output needs two more psi
derivatives and one more metric derivative than its z output order; its time
output likewise requires psi_t and h_t. This does not identify the physical norm
of the coupled weak symplectic system or bound those jets on the certified root.
No projection, finite-band restriction, new action or numerical tolerance change.
Global inverse/range, charge/mean conditions, physical derivative counts for other
sectors, coefficient/tube bounds and finite-time preservation remain open.
No commit, publication, vault mutation or model/provider dispatch.
