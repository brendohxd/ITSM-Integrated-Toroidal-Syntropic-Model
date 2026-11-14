# Strong constraint lift V2: scalar/derivative arithmetic correction

4 November 2026. Inherits every scientific requirement of
RES001_RTAU_STRONG_CONSTRAINT_LIFT_V1_SPEC_2026-11-04.md unchanged.

V1 stopped on the first cell before producing bounds: mpmath's interval
left multiplication attempted to convert a nested first-differential object.
V2 evaluates the identical regulator product with the derivative object on
the left and the interval constant on the right. The mathematical product,
action, data, domain, norm and acceptance requirements are unchanged.

Preserve and pin V1 source, specification and failure. Use a new executable
and receipt directory; retain all scope holds and exact replay requirements.
Review DEFERRED; physics_pass=false; gate_effect=NONE; R-tau UNADOPTED.
