# R4C1: planar coupled interaction vertices, V1

Date: 12 October 2026. Frozen before execution.
Owner: Master Test 1 / RES-001 / Stage 2 of the approved dust-GR-weak-field plan.
Authority: operator approval to continue the **unchanged** R4C1 action with a
bounded coupled-interaction/physical-window calculation. This checkpoint is an
input to that calculation, not a replacement acceptance rule for Stage 2.
Status: Conditional research; gate effect NONE; review DEFERRED.

## Question and registered scope

Derive the analytic interaction functional needed to couple two transverse
frame waves to the complete metric/frame/scalar/dust/regulator response. The
old fixed-metric vacuum scattering warning is not a coupled amplitude.

Use the frozen covariant action, its normalized off-shell force/alignment
projector and **independent** normal frame variation. Background fields are
homogeneous FLRW fields in the existing Cartesian chart, not a Minkowski
solution presumed at finite matter density. Keep the evolving scale factor,
Hubble drift, background scalar derivatives and all four frame invariants.
The first transverse direction is `Vy=W/a`, ADM shift `Ny=B/a`; W and B may
depend on **t,x,z** (no y dependence). Retain independent value/t/x/z jets of
all 22 response fields, with labels rather than positional source mapping:

`alpha,Sx,Sy,Sz,Mxx,Mxy,Mxz,Myy,Myz,Mzz,Vx,Vy,Vz,du,dv,dr,Pi,T,Em,Z,nu,LambdaU`.

Extract, before any family substitution or constraint solution:

1. the first-direction quadratic action;
2. the coefficient `e^2 d` of the analytic action, where d denotes an
   independent response variation (the generic WWR interaction functional);
3. its coefficients for all response jets and its Euler source ledger;
4. the analytic intrinsic `e^4` coefficient on the first-direction ray.

Einstein plus GHY uses the same ADM boundary convention as the frozen action.
The spatial Ricci term is independent of e in this chart, so has zero `e^2 d`
and `e^4` coefficients. This is **not** removal of spatial Ricci from the full
response Hessian; pin and retain its generic 110-jet export. All scalar,
matter, multiplier and auxiliary sectors remain in the action ledger even
when a coefficient vanishes on this specific first direction.

## Reduction and force cusp

Only after variation set the first transverse shift to
`B=sigma W`, `sigma=-alpha13/(MP2-alpha13)`. This is the nonzero transverse
mode solution, not a zero-mode Laplacian inverse. Export the unreduced result
as well. No response constraint, lapse, normal equation, matter equation or
homogeneous sector is eliminated in this checkpoint. An absence of a direct
source never means its coupled response is absent.

Retain all three diagnostic families and their approved scalings; derive
their vertices from the generic functional, never by changing coefficients
inside specialized B1 matrices. The family choices are not microscopic
matching predictions. Registered domain: `0<eta<=1`, `MP2-alpha13>0`.
The generic vector equation must retain the frame mass, not the canonically
rescaled mass, and both spatial derivatives.

The `-A Y^(3/2)` term at Y=0 does **not** possess an ordinary Taylor cubic
vertex. Keep its exact first-ray density `-A |psi_dot e W|^3`, its real
directional derivative and the leading response correction. For a fixed
response ray d=e^2, the force quartic correction is one-sided:
`-3 A |psi_dot|^3 sign(e) W |W| R_Vy` as coefficient of e^4. The physical
prepared response to this source itself changes sign under e reversal;
do not confuse that response with a fixed response ray. Do not smooth the
cusp, manufacture a polynomial vertex, insert an acceleration target, or
truncate the previously certified mathematical harmonic tail into a
physical UV domain.

## Controls frozen before execution

- Exact ADM inverse and normalized n identities in the quotient ring
  `e^5=d^2=e^3 d=0`; independent normal U=(1+d nu)n remains varied.
- Exact recovery of the old unspecialized collinear WWR functional by setting
  x derivatives to zero; the original source artifacts are not rewritten.
- Exact x/z exchange covariance, including metric off-diagonal labels.
- Exact quadratic vector equation and generic temporal/x/z source Ward
  identities with commuting mixed third derivative jets, including coefficient
  drift. Do not repeat the previously rejected incomplete derivative map.
- Exact fixed-metric H=B=0 fourth-order analytic control
  `MU2/2 * W^2 * [-c123 W_t^2+c1*(W_x^2+W_z^2)/a^2]`.
- Explicit degree and mass-dimension checks; all coefficients are densities
  of dimension four before canonical normalization.
- Independent high-precision **unexpanded** ADM/connection/action evaluations
  on two generic planar response jets. Three frozen steps (0.001, 0.0005,
  0.00025) must show decreasing normalized mixed-coefficient error, or a
  <=1e-12 floor, and final error <=5e-7. Separate fourth-coefficient controls
  use the same steps and criteria. These numerical controls are not rigorous
  physical error bounds.
- Exact nonanalytic first-ray and directional identities, plus independent
  positive/negative amplitude controls away from W=0. Include W=0 without
  division by W and reject calling the cusp analytic.
- Omission rejection: x-dependent and normal/regulator responses, shift
  coupling and mean-compatible source terms must be retained. Preserve the
  existing failed source-Ward and time-response attempts and immutable
  trajectories. No integrations of those completed trajectories are rerun.

## Acceptance, provenance and unresolved physical obligations

Acceptance here is a reproduced generic coupled interaction **functional**
and its controls. It is not an amputated physical eigenstate scattering
amplitude, a retarded response solve, a nonlinear solution remainder, a
partial-wave unitarity bound, a physical cutoff, or a physical frequency
window. Local momentum conservation in a coefficient export does not justify
a finite-density FLRW S-matrix. Endpoint terms, state normalization, coupled
constraint inverses, IR/zero-mode prescriptions and controlled background
adiabaticity still need assessment in the subsequent interaction calculation.

Stage 2 remains INCOMPLETE / STOP_AND_ASSESS_DOMAIN_UNRESOLVED unless its full
approved physical criteria are met by separate evidence. This checkpoint
does not supply a GO family, a healthy continuous GR limit, tensor/PPN
clearance or an all-action no-go theorem. Stage 3 remains NOT_ENTERED because
genuine matter-residue and nonlinear-force identifying inputs are absent.

Use a new versioned executable and fresh non-overwriting receipt directory;
pin all inherited sources/artifacts and their available sidecars before and
after execution, export failed assertions, immediately hash each artifact,
then perform byte-identical read-only replay and provenance QA. No existing
source, failed attempt, trajectory, receipt or scientific sidecar is changed.
Append the owning disposition to execution/review indexes only after results.

Register R9-MT1-PLANAR-WWR-V1, inheriting G3I/G3N4, three-family entry/response/
time-response/odd-tail debt and all applicable upstream debt. Review DEFERRED,
Rule9_cleared=false, physics_pass=false, gate_effect=NONE.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
No new parent, provider dispatch, model/runtime change, vault mutation,
manuscript/PDF edit, publication, commit or push.
