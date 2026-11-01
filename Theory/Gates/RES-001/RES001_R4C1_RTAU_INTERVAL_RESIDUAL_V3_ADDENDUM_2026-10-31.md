# Interval residual implementation repairs through V3

V1 stopped before a receipt because a spatial interval jet attempted to
convert an adjoint node into a scalar interval. V2 uses Python's mixed-type
arithmetic dispatch to let the adjoint node own those operations. Sources,
seals and the private failure log remain preserved.

V2 passed the preliminary original-density and elementary-jet controls but
later produced a complex interval while taking a fractional power. Repeated
interval multiplication of the same interval loses the known nonnegativity
of its square. This gave an unnecessarily negative lower endpoint for a
sum of squares, not evidence of a negative physical force norm.

V3 uses the interval library's integer power for the VALUE coefficient of
integer jet powers, retaining the derivative-coefficient enclosures from
the product rule. This is a valid tighter enclosure for the same scalar
power. It does not restrict the cell, delete a derivative or change the
action, packet, precision or residual method. V1/V2 are preserved and neither
produced a scientific receipt. Pending V3 output must be inspected before
claiming any continuum bound or positivity result.

The conformal sum-of-squares force evaluation is compared with the original
physical density and gradients at real points. Those controls complement,
and do not replace, review of outward rounding and jet propagation rules.
No validated nonlinear inverse or existence theorem follows from these
implementation repairs. physics_pass=false; review DEFERRED.
