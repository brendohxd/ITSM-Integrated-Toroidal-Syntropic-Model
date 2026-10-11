# G3N5: complete background-condition match to B1

Date: 9 October 2026. Conditional R4C1-v1 / Master Test 1.
Local author-assistance; review DEFERRED; Rule9_cleared=false;
physics_pass=false; gate_effect=NONE.

## Verified result and scope

The checkpoint passes 62/62 local checks and exact read-only replay. All six
output/sidecar files retain identical bytes, hashes, lengths and timestamps.
All 130 source pins and 127 available sidecars match before and after execution;
the three inherited sidecar absences remain explicit.

The September [B1 report](RES001_R4C1_INTERACTING_BACKGROUND_REPORT_2026-09-25.md)
already supplies the interacting aligned background equations and a trajectory.
This checkpoint does not replace them or claim another on-shell trajectory.
It independently matches all 22 direct four-dimensional first-variation
tadpoles to those equations, retaining every spatial direction, lapse, three
shifts/boosts, six metric components, Cartesian scalars, raw normalization,
dust and auxiliaries. This is prerequisite input matching, not the quadratic
kernel, full nonlinear T3 evolution or physical stability.

An exact first-order dual ring supplies the metric/inverse/connection and
raw/normalized frame variations. The entire linear density agrees with a
separate compact formula. Metric compatibility and four frame invariants
agree exactly. Linear Ricci is retained as a nonzero local divergence with
zero periodic Euler operator for all fields. Alignment, projected Y and
regulator have zero first-order bulk contribution on this aligned z=0 branch
only; their higher-order operators are not removed. Independent homogeneous
variation retains lapse, raw norm sigma and multipliers until afterward:
eleven equations and the off-shell time-reparametrization Noether identity
match the direct result.

## Complete background map

Define rho=epsilon0*C^4, C=exp(beta*psi0),
M_cos^2=MP2+MU2*(c1+3*c2+c3)/2, K_s=sum(q_dot^2)+K_Q*psi_dot^2 with q=(u,v,r),
and U_tot as the full scalar/reservoir/portal/vacuum potential. Then
F=3*M_cos^2*H^2-K_s/2-U_tot-rho and A_bg=2*M_cos^2*H_dot+K_s+rho.
Use S_q=q_ddot+3H*q_dot+partial_q U_tot,
P_psi=K_Q*(psi_ddot+3H*psi_dot)+beta*rho and
D_dust=rho_dot+3H*rho-beta*rho*psi_dot.

| Variation | Euler coefficient per a^3 |
| --- | --- |
| alpha | F |
| Mxx,Myy,Mzz | (F+A_bg)/2 |
| du,dv,dr | -S_u,-S_v,-S_r |
| Pi | -P_psi |
| T | -D_dust/C |
| nu | -lambda_U+3*MU2*c2*H_dot-3*MU2*(c1+c3)*H^2 |
| shifts, boosts, off-diagonal metric | zero on this homogeneous background |
| Em,LambdaU,Z | zero on the zeroth-order constraint chart |

The last row does not discard response constraints: unit norm, tau0_dot=C
and z0=0 are already background conditions; their linearized constraints
remain in the pending quadratic kernel. The equation fixing lambda_U is
retained. Solved rates require a>0, C>0, K_Q>0 and M_cos^2>0, with the frozen
action domain. Preserve unsolved equations at singular boundaries; no inverse
density, scalar amplitude or charge is used. K_Q=0 retains beta*rho=0.

The exact off-shell identity is
F_dot=3H*A_bg-sum(q_dot*S_q)-psi_dot*P_psi-D_dust.
It establishes homogeneous constraint propagation without H reprojection,
not a general inhomogeneous theorem. A reversed psi source alone leaves
-2*beta*rho*psi_dot; a reversed dust source leaves the opposite residual.
Both mutants are rejected for generic nonzero exchange, not its nondiagnostic
zero endpoint. Zero exchange alone is not pure GR; only the additional
declared algebraic endpoint yields Einstein-dust equations. No healthy
continuous GR result follows.

## Independent density evidence and failures

The pinned original v1 exact-unexpanded routine is a different implementation;
its main/full-kernel calculation is not called. Two generic all-direction
off-shell local jets, not evolved backgrounds, use 50-digit precision:

| Jet | d=1e-3 | d=5e-4 | d=2.5e-4 |
| --- | ---: | ---: | ---: |
| 0 normalized error | 9.1495084e-9 | 2.2873771e-9 | 5.7184427e-10 |
| 1 normalized error | 2.0378002e-9 | 5.0945005e-10 | 1.2736251e-10 |

Both centered-first-difference controls satisfy the frozen final <=1e-5 and
decreasing/floor conditions. Ricci has its separate exact check. All checks,
equation exports, inputs and inherited failed rows were inspected. No new
failed/unknown row appears. The original G3 balance failure remains
1.1005635230674148e-7 against <1e-7; both N3 attempt-01 failures and their
original values/expressions remain in independent.json.

## Reproduction and provenance

[Contract](RES001_R4C1_G3N5_BACKGROUND_MATCHING_CONTRACT_2026-10-09.md):
bf932d7664d20abb0377c1bc1ff9c5ecf792ef157e0f8f12d0a37f55adc137ac.
Source: Analysis/MasterTests/test_01_r4c1_g3n5_background_matching_v1.py,
SHA-256 12211cb36f2b3263d988c5338f70ad80920644bc98ea19dad923029120fdfa52.
Outputs: Analysis/MasterTests/outputs/r4c1_g3n5_background_match_attempt_01.

- summary.json: c248ab693091c230f0c1880050488e88a0b7c2bd244e78031cad537bac554229.
- formulas.json: 5e04cadba6a1f385c7a25ca302d438e2afa2304e64fc7f5311f7d9ff094be112.
- independent.json: f2712b50ea4586379c3baf34a59fc8df03bf72669ec3ad7270a82a7ac050eb52.

Use the itsm_env Python interpreter, -B, and the new source, wrapped by
Scripts/itsm_context.py run -- for verbose output. Initial execution refuses
an existing output directory. Replay adds --replay and that existing directory.
Python 3.13.9, SymPy 1.14.0, mpmath 1.3.0. Logs remain private and ignored.

## Remaining full goal

Original full-kernel worker remains live without a terminal receipt at the
latest poll. Export-only v2 is prepared, not run, pending the earlier stop/
keep choice. No original worker was stopped or duplicated. Full-kernel
comparison, inhomogeneous constraints/initial data, nonlinear response/
evolution, physical Cauchy/DAE domain, stability, cutoff and healthy continuous
GR remain required. Retain homogeneous data and the unsmoothed harmonic tail.
This match supplies an input condition, not a narrower replacement goal.

Review DEFERRED, not cleared; Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 unchanged. Inherit all scientific/review debt. The memory skill kept
older B1 evidence authoritative and immutable; unavailable vault tools do
not establish corruption. No original scientific source, receipt or frozen
sidecar was edited. No action/manuscript/PDF/vault/provider/runtime/commit/
push/promotion/publication change was made.
