# R4C1-G3DF: finite-k physical density on the prepared solution plane

Date: 2026-10-08. Owner: Master Test 1 / conditional R4C1-v1 / G3.
Frozen before the new density projection, sign sampling and error evaluation.
Planning uses G3D's derived leading action and G3F's existing grid; this
is not preregistration before all analytic reasoning. Review DEFERRED.

## Scope and frozen decision rules

1. Verify G3D by nonmutating byte-identity replay and register its bounded
   result. Preserve every inherited source, failure and receipt.
2. Reconstruct physical dust density from S1's generic auxiliary solutions
   with unchanged G3 parameters and G3S's map q=R x,
   qdot=Rdot x+R xdot. Use
   D=(C^4 delta_epsilon+4 beta rho_m delta_psi)/rho_m. No fitted Poisson law,
   imposed density equation, alternate action or changed initial data.
3. At fixed comoving k derive full phase generator A and density rows
   L0, L1=dot(L0)+L0 A, L2=dot(L1)+L1 A. Coefficient derivatives use the full
   registered G3S background flow. Check the original dust normalization
   and regulator constraints exactly and density row linearity.
4. Use PINNED archived G3F columns, not a claim of new full integrations:
   eta=(1,1/4,1/16), k=(20,40,80), t in [0,1], 101 equally spaced samples,
   DOP853 and Radau full-system runs plus archived truncated reference.
   Reintegrate only the background at G3F's original tolerances and initial
   data to evaluate rows. Require two-method background agreement <=1e-10
   and agreement with archived G3 trajectories <=1e-8 (normalized).
5. Multiply prepared embedding/columns by sqrt(eta)/k. Verify exactly
   that the large-k limit of [L0;L1] E sqrt(eta)/k equals G3D's T,
   det(T)=-(12-eta)/(a^5 rho_m). Normalize each finite-k solution plane with
   its ACTUAL initial (D,Ddot) map, so full density transfer starts at I.
   Normalize the leading reference by T(0)^-1. Export raw maps and initial
   mismatch; do not quietly tune away physical discrepancies.
6. Compare full density transfers with leading G3D transfer. Report separately
   density row, derivative row and combined phase error:
   max_t ||F_full-F_leading||_F/(1+||F_leading||_F), for the relevant row(s).
   Require combined error to decrease under BOTH k doublings at each eta
   and <=5% at k=80 at each eta. These are sampled diagnostic targets,
   not observed accuracy or physical EFT admissibility. Preserve failures;
   do not adjust grid, interval, initialization or threshold.
7. On each actual evolved prepared plane, form F=[L0;L1] Y N, where N is
   fixed initial-density normalization. Require sampled det(F)>0,
   finite maps and max condition number <1e8 before inversion. If rank fails,
   report it and do not infer action through that point. Compute
   Omega0=N^T E0^T J0 E0 N, K_plane=Omega0[0,1]/det(F), and
   B_plane=([L1;L2] Y N) F^-1. Report friction, mass, departure from G3D
   and kinetic ratio K_plane/(a^5 rho_m/k^2). Require K_plane>0 at all
   samples and relative two-form transport drift <=1e-7. Check B_plane's
   first row [0,1] and density-coordinate symplectic pullback <=1e-7
   (relative/normalized as exported). No accuracy threshold for the
   second-derivative generator: report even when small transfer errors
   coexist with oscillatory coefficient errors.
8. Require density-method discrepancy <=1e-7 normalized. Independently
   integrate leading dust equation from density initial I at background
   tolerances; require agreement <=1e-9 with G3E/G3D leading transfer.
   This isolates reconstruction/normalization consistency, not full physics.
   Record every failure/unknown as boolean receipt checks.

## Limits and evidence handling

The finite-k two-dimensional action is a restriction to a selected prepared
solution family, only where its density chart has rank two. Its effective
coefficients can depend on preparation. It is not a universal local
density-only reduction of twelve-dimensional phase space, an arbitrary
fast-wave result, positive-energy theorem or stationary quantum norm.
The 101-sample grid can miss high-frequency extrema; no continuous-time
error bound or fitted convergence exponent is claimed. No measured
wavelengths are assigned to this dimensionless chart. Physical EFT
cutoff/window, full PDE remainder, uniform eta endpoint and healthy full
GR recovery remain NOT_DERIVED/UNVERIFIED as inherited.

Pin direct/transitive inputs and archived columns. New script refuses
existing output directories and offers nonmutating byte-identity replay.
Hash new artifacts immediately; retain failed attempts. Register result,
substantive blockers and inherited deferred-review debt. No older
receipt-producing main() invoked. No memory mutation, provider dispatch,
PDF edit, commit, push, promotion or publication.

Inherit R9-MT1-VARIATION/B1/G1/S1/S2/S3/G2/G3/G3S/G3Z/G3E/G3A/G3F/G3D.
Canonical Tests 1-3 HOLD_SUBSTANTIVE; physics_pass=false; gate_effect=NONE;
Rule9_cleared=false; review DEFERRED. MAT-001 BLOCKED, UVIR-003 IN_PROGRESS,
K_Q NOT_DERIVED, V NOT_COMPUTED, Stage4A CLOSED, TOP-X4 unchanged.