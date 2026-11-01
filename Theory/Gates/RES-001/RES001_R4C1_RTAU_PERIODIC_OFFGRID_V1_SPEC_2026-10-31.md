# Off-grid control for the frozen periodic candidate

Before execution, freeze re-evaluation of the 33-node candidate on 65 and
129 nodes shifted by 0.37 grid intervals. Reuse its exact stored coefficients,
H and omega; do not solve again or fit new data. Use full physical action
gradients and the new-grid derivative to evaluate E_S and lapse/density/charges.
Require full residual and both charge errors <1e-9, positive sampled density,
integrated momentum residual <1e-9. Check the omitted lapse-flux charge differs
from the correct charge by >1e-11. Record fine-grid residual Fourier content
outside the candidate's 16 retained harmonics without claiming it bounds the
infinite tail. Compare the two charge quadratures at <1e-10.

This is an independent discretization control using the same physical density,
not an external peer review or a rigorous continuum residual/inverse bound.
The periodic-preparation acceptance remains incomplete. Preserve sources,
fresh receipt and exact replay. physics_pass=false; review DEFERRED.
