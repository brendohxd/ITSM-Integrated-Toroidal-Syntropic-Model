# Time-response V3: corrected mean-sector omission control, frozen supplement

12 October 2026. Freeze BEFORE V3 execution. No trajectories, action, sources,
initial data, parameter choices or original numerical tolerances are changed.
Reuse the completed V2 trajectories; do not re-integrate to improve their values.

V1 remains interrupted for its source-order wiring defect. V2 remains FAILED,
10395/10449, with 54 failed position-only mean-omission controls and no other
failed/unknown checks. Its immutable failed replay must still return exit1.
V2 source: 8fec650e4c7d373a480fa087a72fb676cd9289c3d210c4f133320379a246b7ba.
V2 summary: 32e55c59882515d00a604dc0eed5dae79b89961f7d8aee32846301c99dc4ab4d.
V2 trajectories: 8a3e5df7765aca174b520a53a8a0ca01848941ec34032cba648c3a198ee9320d.

## Why position-only deletion is not a valid omission test

The original test removed q_Mxz,q_Myz,q_Mzz from an instantaneous trial state,
but left their velocities and accelerations intact. It therefore did NOT omit
those dynamical fields. Its near-zero residual is not evidence that the mean
metric dynamics can be dropped.

In this local classical R4C1 action, a homogeneous on-shell background admits
g_ij(t)=a(t)^2 B_ij for ANY constant positive-definite spatial matrix B, with
the same time-dependent homogeneous matter/frame/scalar data. Spatial gradients
and spatial curvature vanish; the invariant extrinsic/frame rates are H times
the identity. The constant volume factor sqrt(det B) cancels from local field
equations. Linearizing this family yields constant mean spatial metric strains,
q_M constant, q_M_dot=q_M_ddot=0, in the kernel of the homogeneous Euler operator.
Thus its position columns E_A[:,M] vanish ON SHELL, whereas the velocity and
acceleration columns need not vanish. This lemma is scoped to the local
classical action; it does not identify different torus moduli as gauge, impose
fixed global charge, or settle physical energy/quantum Casimir sectors.

V3 must check this position-null identity for all SIX mean metric columns on
the existing registered time points. If it fails, keep the explanation open;
do not assume the null columns or remove the metric degrees of freedom.

## Corrected rejection and acceptance

At all 54 original trial events (18 runs, times0,.025,.05), reconstruct the
same nonzero trial state from the same background and mean source. Reproduce
the original position-only control and its near-zero residual. Then deliberately
truncate the Mxz,Myz,Mzz fields CONSISTENTLY: zero their q, q_dot AND the used
q_ddot entries, without re-solving the other fields to hide the omission.
Check the full original 22-field residual in the ORIGINAL normalization.
Require >1e-12 as before. The metric positions, velocities and accelerations
are all retained in the accepted trajectory, not removed from the model.

Verify full original trial residual <=1e-9, mean position-null columns <=1e-10
in normalized operator units, and exact expected old failure classification.
Every other original V2 check must remain passed, with no unknown or new failed
check. Pin every original source and artifact, verify all sidecars, record
byte/metadata preservation and immutable replay. V3 is a new composite
acceptance/omission-control receipt, NOT a rewrite or re-labelling of V2.
The V2 trajectory bytes remain the sole numerical trajectory artifact and
must be referenced by the original hash in V3, not copied as revised results.

## Unchanged scientific limits

Finite perturbative diagnostic: all3 families, eta1/4, k20/40/80, t[0,.05],
analytic mean/2k plus sampled odd1/3/5 with infinite forcing formula retained.
No certified continuous numerical/nonlinear remainder or evolved odd-tail
bound. All-eta/all-sector physical window, energy/fixed-charge/singular/quartic
sectors, healthyGR/fullPPN and identifying matching remain open. Negative mean
kinetic eigenvalues remain visible; this control does NOT classify them healthy.
Stage2 incomplete, STOP_AND_ASSESS_DOMAIN_UNRESOLVED; Stage3 NOT ENTERED.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE;
Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Root goal ACTIVE/incomplete. No paper/PDF/publication/commit/push, model/provider,
runtime/dependency or vault operations.
