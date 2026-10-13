# G3N5 dust remainder: pre-execution contract

Date: 11 October 2026. Version 1. Conditional R4C1/B1, Master Test 1.
This contract precedes the new decomposition, expansion and bound executable.
It does not change the frozen finite-mode experiment or its criteria.

## Inputs and exact equations

Pin the complete finite-mode matrices, diagnostics, trajectories, summary,
their source/transitive evidence and available sidecars. The owning report
is RES001_R4C1_G3N5_DUST_FINITE_K_REPORT_2026-10-11.md. Preserve absent
UVIR sidecars explicitly. B1G supplies exact homogeneous interval bounds.
Retain all 20 first-order coordinates and reconstruct all 22 original fields.
Use ell>0, p=ell/a, p_dot=-H p, t in [0,1/20], rho_m>0 and a,C>0.
The five archive modes are ell=4,8,16,32,64, with both complex quadratures
and the inherited negative-mode conjugation. The zero mode is not inverted.

Let x_dot=L x, z=B x, A_z=(B_dot+B L) B_inverse,
O_z=O B_inverse, E_z=B G (O G)^(-1). Compute and verify the actual
invertibility domain of O G; do not assume sampled nonsingularity proves it.
Define W=O_z z and r=z-E_z W, with O_z r=0. This is an evolving exact
decomposition, not repeated projection of physical evolution onto G.

F=O_z_dot+O_z A_z; Delta=F E_z-M; R=F-M O_z;
S=A_z E_z-E_z_dot-E_z(M+Delta); J=A_z-E_z F.
Verify W_dot=(M+Delta) W+R r and r_dot=S W+J r, and the
constraint tangency identity, including O_z_dot. Keep all complement
directions and time-dependent terms. Extract the first nonzero inverse-p
term of Delta; distinguish instantaneous graph correction from an effective
closed slow generator after complementary feedback.

## Bound and acceptance

Attempt a rigorous prepared-data short-time remainder using the exact
homogeneous ODE, certified coefficient/graph bounds and retained fast
forcing. Pointwise/sample maxima and rounded Taylor coefficients are not
interval certificates. A valid finite-mode exponential majorant may be
reported separately; it must not be called a uniform high-p convergence
theorem. If complementary forcing lacks the required uniform control,
identify its missing estimate, retain the milestone as OPEN, and continue
only the independent GR/domain assessment authorized by the plan.

Numerical controls use the existing five-mode trajectories without replacing
or rewriting them. Exact algebra residuals must vanish after justified
simplification. Numeric reconstruction identities must have normalized
error <=1e-9; archive consistency <=1e-10. Bounds use outward-enclosing
rational/interval expressions, not fitted observed errors. Reject omitted
B_dot, momentum drift, fast forcing, and treating prepared complementary
seeds as eigenmodes. Hash/size/mtime and read-only exact replay must hold.

Outputs: formulas.json (exact decomposition/corrections), diagnostics.json
(archive comparisons and bound disposition), summary.json (checks,
precision, domain, inherited failures and substantive holds), with sidecars.
Normal execution refuses an existing output directory; replay makes no
writes. Any failed scientific attempt is preserved in a new attempt.

Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
No physical ghost/EFT/GR/weak-field or coefficient prediction follows from
this bounded calculation. No commit/push, publication or provider dispatch.
