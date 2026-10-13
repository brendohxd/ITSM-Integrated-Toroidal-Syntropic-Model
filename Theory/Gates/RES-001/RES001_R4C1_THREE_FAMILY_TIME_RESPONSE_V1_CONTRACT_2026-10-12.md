# Unchanged R4C1: bounded time-dependent second-order response, V1 contract

12 October 2026. Freeze before execution. Owner: approved Stage-2 coupled-
interaction calculation. No new action, matching relation or physical family.
Use the checked generic action/Hessian, G3N4 source and corrected response-entry
V2. Do not re-run their completed audits or overwrite their receipts.

## Registered diagnostic scope

All three frozen families; eta=1/4 (an existing registered member, selected here
before evaluating the new trajectories, NOT by its observational coefficient).
Coordinate k=20,40,80; t in [0,0.05]; original controlled background prescription
and first-order transverse w(0)=1, w_dot(0)=0. This finite diagnostic subset is
not the whole eta/momentum domain. Use M_P=1 chart units, not an observed scale.
The response is a perturbative coefficient: no finite-amplitude accuracy or full
nonlinear solution is certified by its numerical integration.

Evolve every retained reduced coordinate and velocity. Keep the analytic mean
and complex +/-2k sources and the nonanalytic odd branch. Numerically evolve
n=1,3,5 odd transverse coefficients only, while retaining the EXACT infinite
odd source/Duhamel prescription and labelling its evolved tail UNCONTROLLED.
The finite odd sample is not a closed invariant manifold or full response.
No fundamental-only substitution, cubic smoothing or ordinary third derivative.

## Affine reduction and drift

With frozen clock/unit constraints T=nu=0, alpha=-beta*Pi, use the original
22-field Euler blocks E_A,E_B,E_D and the proper a^3 time measure. Let F select
the reduced coordinates and U the auxiliary sector. For nonzero mode retain
all three shifts and Z; for the mean retain all six metric coordinates and only
Z, never a k=0 shift inverse. Define

```text
D = U^dagger L_A U, Y = U^dagger L_A F, V = U^dagger L_B F,
Q0 = F - U D^-1 Y, Q1 = -U D^-1 V, u_s = -U D^-1 S_aux,
q = Q0 y + Q1 y_dot + u_s,
q_dot = Q0_dot y + (Q0+Q1_dot)y_dot + Q1 y_ddot + u_s_dot,
K_r = F^dagger L_K F - V^dagger D^-1 V,
A_r = F^dagger(E_A Q0 + E_B Q0_dot),
B_r = F^dagger(E_A Q1 + E_B(Q0+Q1_dot)),
f_r = F^dagger(S + E_A u_s + E_B u_s_dot),
y_ddot = K_r^-1(A_r y + B_r y_dot + f_r).
```

Retain inverse, basis and source drift; do not continuously project onto a slow
graph. Verify F^dagger(E_B Q1+E_D F)=-K_r and full auxiliary reconstruction.
Auxiliary accelerations are absent from the original Euler operator, not zero
physical accelerations. Recover density/normal multiplier from original lapse/
normal equations. Independently differentiate the recovered density along the
full background/first-mode/response flow and compare to the dust equation;
assigning density velocity from that equation alone is NOT acceptance.

## Numerical verification and rejection tests

Two independently integrated trajectories: DOP853 and Radau, rtol=1e-10,
atol=1e-12, max_step<=0.001, same original data/action. Finite time samples
include both endpoints and 19 interior points. Compare normalized retained
coordinate/velocity trajectories <=1e-7. This is a numerical cross-control,
not a rigorous continuous error certificate. No target data or coefficient.

Verify all 22 original sourced Euler rows <=1e-9 at sample times. Verify exact
source Fourier reconstruction <=1e-10, raw coefficient five-point chain rule
<=1e-8, and independent five-point recovered-density flow derivative <=1e-7.
Use two differencing steps and report both rather than selecting a passing one.
Retain signed kinetic spectra, including every negative mean eigenvalue.
Check the affine reduction on nonzero trial coordinates/velocities, not only
on the prepared zero-response initial state. Reject omitted Q0/Q1 drift,
affine forcing, dust/normal/clock constraints or mean terms using explicit
nonzero residual controls. No post-result threshold adjustment.

Fresh executable and attempt directory; pin all upstream bytes and sidecars;
immutable read-only replay; owning report and appended queue/review debt.
Failures are preserved and diagnosed before any new version. No edits to frozen
originals, failed attempts, old hashes or sidecars.

## Unchanged substantive holds

No all-eta/all-sector physical band, full evolved odd-tail/nonlinear remainder,
physical energy/fixed-charge/singular-domain reduction, complete quartic
interactions, healthy GR or full PPN clearance. Stage2 incomplete and
STOP_AND_ASSESS_DOMAIN_UNRESOLVED; Stage3 NOT ENTERED; identifying matter-residue
and nonlinear-force matching absent. Local numerics do not replace these inputs.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE;
Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Root goal ACTIVE/incomplete. No paper/PDF, publication, commit/push, provider,
model/runtime/dependency or vault operations.
