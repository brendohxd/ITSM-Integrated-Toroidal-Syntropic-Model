# Coupled mean/node completion: frozen diagnostic contract

18 October 2026. Unchanged R4C1 action, all three registered families and
eta=1/4,1/64,1/1024. Follow NODE-ACCELERATION-V2, not an all-action no-go.

## Target and exclusions

Test whether the known initial constraints AND the necessary scalar node
acceleration condition admit a jointly solved (H,U) on the original planar
slice. Set Z=U*w^2 and retain Z_dot=Ud0*w^2 as an explicitly unproved velocity
continuation. Retain w=e*cos(40z), V_dot_y=-Hbg*w, both original global charges,
full lapse flux and exact shift inverse. No repaired state is adopted/evolved.
Passing this bounded task is not full higher-consistency admission, a temporal
IVP theorem, physical reduction, healthy GR or a physical validity window.

For each amplitude |e|<=1/500 freeze the independent brackets

    H in [49Hbg/50,51Hbg/50], U in [49U0/50,51U0/50],
    U0=Hbg*p+beta*rho0/K_Q, rho0=1/5.

These are diagnostic initial-data brackets, not new microscopic predictions.
Do not widen them after a failed enclosure; report UNRESOLVED or FAIL instead.
At e=0 U only labels the continued limiting system: Z=0 does not physically
identify U on the aligned stratum.

## Equations and proof requirements

Use F=<E>+rho0 and the exact necessary node defect G from the frozen V2 report.
Derive B=G-beta*F=K_Q*(U-U0)+alpha*D, alpha=e^2. This combination eliminates
only the constant mean term, not local flux, density or the coupled shift.

Recompute the shift residual/error bounds over the NEW H/U rectangle; old
U0-only remainder bounds may not be reused unchanged. The inherited polynomial
coefficients and complete residual may be reused. Retain their exact residual,
and derive H and U sensitivities of the exact inverse with controlled errors.
Show the operator is independent of H/U and the source is affine in both.

For every case and the continuous amplitude interval, establish strict opposite
F signs on the two H faces for all U, opposite B signs on the U faces for all H,
F_H<0 and B_U-B_H*F_U/F_H>0. Include inverse sensitivities in every derivative.
These give a unique solution of this restricted two-equation system, not full
initial admission. Alternatively report exactly which inequality is unresolved.
Prove local lapse-derived dust positivity and preserve the exact phase charge.
Keep node jets, both amplitude signs and finite-regularity caveats explicit.

If successful, enclose (U-U0)/e^2 via the solved equation, including its zero
limit, and hence control the change of Z relative to the old continuation.
Do not insert old H,R,rho into an isolated correction formula and call it coupled.
Do not relabel the original rejection or overwrite previous certificates.

## Independent controls and frozen numerics

Symbolic identities and mass dimensions are exact. Use mp.dps=110 for point
controls/endpoint inspection and mpmath.iv at80 decimal digits for outward
enclosures. Angular partitions16,32,64,128,256 are fixed in advance. No tolerance
or domain widening. Do not divide an absolute inverse error by alpha near zero:
retain the actual residual powers before scaling.

At |e|=1/500, compute high-precision approximate joint roots only as diagnostics,
using64-point periodic quadrature for the analytic part and the exact cusp mean.
Use the coupled analytic Jacobian, tolerance1e-60 and at most20 Newton steps.
Independently compare the exact-action odd-sector shift Galerkin systems at
8 and12 harmonics,64 quadrature nodes, normalized tolerance1e-30 at the frozen
angles0,pi/7,pi/2. Their agreement is not a certified inverse or nonlinear error
proof; the residual/coercivity argument remains the proof. No observational
comparison, family selection or target coefficient is involved.

## Artifacts and unchanged holds

Executable: Analysis/MasterTests/test_01_r4c1_coupled_node_completion_v1.py.
Fresh directory: Analysis/MasterTests/outputs/r4c1_coupled_node_completion_attempt_01.
Export formulas, proof/error constants, all cases, diagnostics and a summary.
Require fresh complete exact read-only replay, with separate byte and metadata
guards. Preserve source pins/sidecars/metadata and every failed attempt.

R9-MT1-COUPLED-NODE-COMPLETION-V1 inherits NODE-ACCELERATION-V2,
INITIAL-ADMISSION-V1, initial-constraint/node/canonical/preparation/generic-family
and transitive review debt. Review DEFERRED; Rule9_cleared=false.
Stage1 original bounded linear acceptance only; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 unchanged; physics_pass=false; gate_effect=NONE. Both identifying
matching inputs remain absent. No vault/manuscript/site, commit/push,
publication, new action/parent, provider or model/runtime change.
