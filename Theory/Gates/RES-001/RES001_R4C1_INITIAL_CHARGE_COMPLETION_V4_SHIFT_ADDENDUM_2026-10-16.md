# Initial charge completion V4: retain the reconstructed longitudinal shift

16 October 2026. Preserve V3, its sidecar and failed attempt03 unchanged.
V3 completed 379/391 controls. All12 failures concern the initial coefficient
slice: it incorrectly expected every shift component to vanish at quadratic
order. B1-frame and hierarchical data have nonzero second-harmonic Sz from
the constraint reconstruction (six family/eta points, both solvers). It is
not rounding noise, a failed physical solution, or a changed action.

V4 retains the archived Sx,Sy,Sz coefficients in the independent exact ADM
calculation, together with the original first transverse and third transverse
shift. Generalize the symbolic metric/projector proof to arbitrary three-vector
shift before testing whether these initial scalar currents and Y depend on it.
Only physical positions and velocities, not these algebraic shift variables,
are required to match the declared zero-position slice. This change is valid
only if exact arbitrary-shift cancellation is established. No archived shift,
constraint, source or acceptance tolerance is changed or dropped.

Pin all failed V3 artifacts. Fresh attempt04; V4 schema. Require the physical
formulas to remain byte-identical to V3 and the earlier failed V2; preserve the
failed narrower-slice controls. This remains an initial-order diagnostic, not
a solution of all local constraints or an evolved nonlinear stability result.
The original contract's domains, criteria, review debt and canonical holds apply.
