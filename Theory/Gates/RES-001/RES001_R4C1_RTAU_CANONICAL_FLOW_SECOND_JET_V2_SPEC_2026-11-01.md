# Prepared canonical flow second spatial jet V2

Freeze before execution. V1 passed15/15 and exact replay; preserve it.
Extend the same thirteen-rate inverse with

    M*dv_zz=rhs_zz-2*M_z*dv_z-M_zz*dv.

Use actual second spatial coefficients and the validated temporal inverse.
Retain 1e-35 inverse bounds and 1e-28 comparisons, now including the second
rate derivative. Independent prescribed rate jets must have nonzero second
coefficients. The Euler flux rows and all open-closure flags remain.

This is necessary for Zdot=-partial_t(Delta_h psi), which needs psi_dot,zz.
The former unused zero second-rate slot is not a physical approximation.
Point controls use the actual centre third shift derivative already present
in the clock factory. A whole-root derivative estimate must use the owning
equation-derived third-jet bound, not a differentiated C2 error radius.

Further auxiliary closure must return delta Z, delta Z_z and delta Z_zz
from the full variable-metric Laplacian, plus delta Zdot at the point.
The first three require metric jets through order3 and force jets through
order4. They cannot be obtained by filling missing jets with zero.
Use C=h^{zz}*tr(h^-1*h_z)/2-(h^-1*h_z*h^-1)^{zz} and
Delta psi=h^{zz}*psi_zz+C*psi_z. Time/field differentiation must retain
all metric components and their mixed variations. This auxiliary closure
is NOT implemented merely by completing the second rate inverse.

Full evolution/gauge/current closure and a physical norm remain open.
physics_pass=false; review DEFERRED; goal ACTIVE; no action adoption.
