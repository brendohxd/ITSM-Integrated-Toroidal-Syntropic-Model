# First material seed compatibility: bounded analytic feasibility V1

21 October 2026. Unchanged R4C1 / RES-001 / Stage2.
Result ID: R9-MT1-MATERIAL-SEED-FEASIBILITY-V1.
Operator approval: analytic background-admission and moving-node feasibility
checkpoint before another large numerical run. No state is adopted or evolved.

## Reuse the existing initial construction

INITIAL-ADMISSION-V1 already certifies the KNOWN implicit canonical initial
constraints, both charges and positive future dust in the registered planar
sector. Its report SHA is7237b9649f08fe16746660415f418dd93b0268b81edb0871e6105abdca7c47ef.
Inherit that result and its interval/replay qualifications, not its check count
as new work. Full initial-data admission, higher rank-changing consistency and
temporal persistence remain open. Finite Galerkin/midpoint exports must not be
mistaken for the exact implicit initial construction or an evolving solution.

## Analytic decision target, frozen before controls

Reuse the actual amplitude-momentum seed u_f and its complete graph image v=A u_f.
All action parameters, including eta, are HELD FIXED when varying the dynamical
amplitude rho. With volume J and the full restored shift multiplier W,

    delta H/dP_rho=P_rho/(J*s)+W*D rho.

Derive this from polar kinetic/current identities and the FULL nonlinear
momentum restoration; do not set W or its variations to zero. At the original
structural data P_rho=D rho=0, action-generated T_rho=0, hence D T_rho=0.
For the full auxiliary residual map Phi=(r_s,r_Z-B*r_P), derive

    (D_t Phi)_s[u_f]=-T_P_rho*f/p^2,
    (D_t Phi)_Z[u_f]=0,
    Phi_s[A u_f]=-F_rho*f/p^3,
    T_P_rho=-F_rho/p.

Test whether these cancel in the first MATERIAL compatibility condition,
not in the stronger frozen D(A^2) condition. Retain mean-metric terms and the
complete state-dependent B, including its time derivative. Moving-node and
spatial-jet transport terms must be accounted for; their seed terms vanish
only if Phi[u_f] is identically zero, not by a general stationary-node rule.

The independent bulk radial force at the flat structural data is

    F_rho=V_rho-j(z)^2*(1-2*zeta*rho^2*w^2)
                        /(rho^3*(1-zeta*rho^2*w^2)^2),
    V_rho=m2*rho+lambda4*rho^3/2+lambda6*rho^5/(4*Lambda^2)
           +g_r*rho*r_reservoir^2/2.

Here j(z) is the ACTUAL restored local phase density, not its spatial mean.
No target acceleration or microscopic matching is inserted. A cancellation
would remove this specific first-material seed obstruction, not prove full
background admission, higher consistency, positive physical energy or evolution.

## Background-defect bookkeeping, not another initialization

On the homogeneous dust-time, uniform s=p slice the original dust Hamiltonian
is <exp(beta*tau)*p_dust/s>. A mean-zero dust-momentum contrast d changes the
density row R_s=n*(Omega*T-dH)_s by exp(beta*tau)*d/p^2; it leaves the Z row
unchanged. The fixed-charge chart removes a constant P_dust contrast entirely.
Therefore such contrasts cannot repair a nonzero MEAN residual. The existing
certified mean equation remains necessary. This affine identity is a diagnostic
bridge, not permission to change the stored data, fit a target, or newly claim
the old initial construction has been completed again.

## Small independent controls only

Six cases: all3 original families at eta=1/4, n17, both node orientations.
Profiles f=1 and sin(theta). Requested100-digit original initialization.
These representative controls do not become all-eta continuum certification.

- Compute action-generated canonical rates with the full original functional,
  nonlinear Ricci, constraints, means, lapse flux and12-velocity response.
- Include the explicit global force clock: T_tau=1 on the diagnostic background
  tangent, following the original temporal formulation. This is NOT an ODE
  integration or a new adopted background. Perturbation tau remains fixed.
- Independently rebuild the original12x12 local temporal matrix and solve ALL
  velocities at X+/-h*T for h=1e-10 and1e-14. Never reuse the old specialized R
  at a changed metric/frame point. Take seed complex derivatives at1e-26.
- Compare the two-sided directional derivative of the actual state-dependent
  Phi against the analytic expression; include the FULL cross correction at
  the changed metric and s, not the flat B formula.
- Check the full-circle values and spectral first slopes of the material sum.
  Normalized finite errors must be strictly <1e-12 at h=1e-10 and <1e-20 at
  h=1e-14. Original baseline/force/graph identities use strict <1e-20.
- Preserve the separately NONZERO frozen next response and reject omission of
  the explicit changing-background term. Do not force a predicted outcome by
  projection or silently relax a failed bound.
- For the dust identity use a mean-zero contrast1e-9*(cos(2theta)+sin(theta)/7),
  independently solve the original temporal system and compare the full
  functional residual change with strict normalized error<1e-40. A constant
  contrast must remain a null chart direction. It is a TEMPORARY algebra
  control only, with original inputs preserved; no physical state adoption.
- Preserve the original background defects, global-clock row and transverse
  node rates. No sampled small defect is declared zero or certified continuous.

No ordinary third force derivative at alignment is authorized: the material
seed formula follows by differentiating the SMOOTH radial momentum sector,
where the force/cusp terms have no radial momentum dependence. No full-spectrum,
large evolution or physical cutoff calculation is included.

## Acceptance, preservation and stop

Frozen contract, versioned executable, fresh summary/independent/formulas,
analytic proof/owning report, complete fresh6-worker versus3-worker exact
read-only replay. Preserve the entire802-record/43-directory prior chain,
old hashes/sidecars/failures and unrelated edits. Use the standalone optimizer.

If first material compatibility is established, report it ONLY in that scope.
Full exact/evolving background admission, higher hierarchy, domain persistence,
nonlinear error control and physical interaction/GR window remain open. If the
formula or controls fail, preserve the failure and state the exact obstruction.
Stop this feasibility task before any larger evolution programme.

Stage1 bounded prepared-dust acceptance only; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1--3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED;
TOP-X4 unchanged; physics_pass=false; gate_effect=NONE.
Review DEFERRED, Rule9_cleared=false; inherit canonical-seed, weak-generator,
initial-admission and transitive review dependencies. No commit/push, publication,
vault mutation, paid provider dispatch, new parent or model/runtime change.
