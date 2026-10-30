# Independent scalar normal-trace verification V1

27 October 2026. Additional necessary evidence before using the V2 interval
as a physical incompatibility. V2's numerical Q comparison reuses the candidate
scalar trace formula; it alone is not an independent proof of that formula.
Preserve V2 unchanged and complete this check against the original scalar current.

Using a full four-dimensional ADM metric, future-unit frame and connection,
evaluate the original scalar current with its regulator terms:

    J^mu = K_Q*n^mu*(n.grad psi)
      -b*(hp^{mu nu}*partial_nu Z+Z*acc^mu),
    E_psi = -div(J)-beta*rho.

The omitted cubic-force current contributes O(|x|^3) on these initial normal
jets and hence zero quadratic normal coefficient; establish this composite-order
statement. A=0 is only an arithmetic device for that coefficient, not a change
to the original action or its finite-angle force calculation.

For w=slope*x-slope*k^2*x^3/6+..., R=r1*x+r3*x^3/6+...,
Z=U*w^2, Zdot=Ud*w^2, psi_dot=p and aPsi=a0+a2*x^2+...,
the coefficient to check independently is

    E_psi[x^2] = b*slope^2*aZ
       -K_Q*(a2+slope^2*a0)
       -K_Q*p*(-r3/2+(5H-2Hbg-3r1)*slope^2)
       -4*b*U*slope^2*k^2-3*b*U*ty0*slope^3-beta*rho2.

Use four Taylor-jet controls with both slope signs, nonzero transverse shift
gradient, arbitrary metric acceleration/off-diagonal components, frame/scalar/
regulator accelerations and local density curvature. Compute the current and
its divergence independently in coordinates; import no primary enclosure code.
Eighty working digits, normalized tolerance 1e-30. Freeze source before run,
use a fresh receipt directory and immutable replay. A failed identity requires
reassessment of the candidate formula and enclosure use, not threshold weakening.

Only after the analytic coefficient derivation, original-row formulas, outward
interval and these independent checks are jointly assessed may the specified
continuation/regularity exclusion be reported. No full G1 admission, weak-solution
no-go, action rejection, corrected state or goal completion follows.
