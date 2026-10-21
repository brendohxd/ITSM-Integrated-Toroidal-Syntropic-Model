# R4C1 complete coarse-grid canonical matrices; spectrum remains unresolved

20 October 2026. Unchanged-action, retained-planar diagnostic. Computational
matrix construction has advanced; physical-domain clearance has not.

## Result and meaning

All eighteen registered n17 matrices are materialized: the nine inherited
family/eta cases, each at both node orientations. Each retains 372 canonical
coordinates, all prescribed non-quotiented means/zero modes, the coupled node
constraints and the evolving embedding. The 270 matrix controls pass.

The overall result is **305/347, UNRESOLVED**, not a passed spectrum. Its 42 failed
checks are eighteen complete-spectrum rescaling comparisons, eighteen left/right
conjugate-eigenvalue matching comparisons and six left-eigenpair residual checks.
All eighteen right-eigenpair residual controls pass. Nothing is deleted or made
to pass by loosening a tolerance, symmetrizing a matrix or dropping a direction.

This supplies complete finite matrices for conditioning and precision work.
It does not establish a stable physical spectrum, a ghost, a cutoff, healthy GR,
or a nonempty physical validity window. Nor is it an all-action no-go theorem.

## Frozen calculation

The [V1 contract](RES001_R4C1_CANONICAL_SPECTRUM_V1_CONTRACT_2026-10-20.md),
[V2 smoke addendum](RES001_R4C1_CANONICAL_SPECTRUM_V2_SMOKE_ADDENDUM_2026-10-20.md)
and [V3 execution addendum](RES001_R4C1_CANONICAL_SPECTRUM_V3_EXECUTION_ADDENDUM_2026-10-20.md)
own the scope. The cached second differential retains

    H''v = F_XX*v + F_Xy*(n*s)*(volume*R)^(-1)*F_yX*v,
    K*v = H''v - dOmega[v]*Xdot,
    S = E^T*(K*E - Omega*E_dot).

The factor n*s, full nonlinear Ricci, implicit temporal response, original C2
cusp limit with its rejection test, spatial/charge/mean restoration, exact-node
auxiliary coupling and background drift are retained. No C3 cusp derivative or
division by the vanishing node weight is introduced. The 372 count is the
finite retained-chart dimension, not a continuum propagating-DOF assertion.

V3 calls the frozen V2 `CanonicalChart`, `controls` and `materialize` functions;
it does not rewrite their equations. Matrices use 80-decimal construction and
are not numerically symmetrized. Maximum recorded normalized errors are:

| Matrix diagnostic | Maximum over eighteen matrices |
| --- | ---: |
| Canonical two-form pullback | 7.380e-81 |
| Constraint embedding | 4.441e-79 |
| Implicit temporal stationarity | 6.064e-78 |
| Reduced-form symmetry | 1.085e-37 |

These finite numerical controls are not certified continuum error bounds.

## Execution failure and scoped repair

V1's execution-only smoke failure remains preserved. V2 fixed the duplicate
smoke-check bookkeeping but its coarse-grid run later terminated with
`BrokenProcessPool`. Four complete case receipts survived, each with 15/17 checks:
all fifteen matrix controls passed, both numerical spectrum controls failed.

Windows Application events 1000/1001 at 15:17:32--15:17:38 local time record access
violations 0xc0000005 in `mkl_def.2.dll` 2025.0.1.0 for the actual Python workers
(including 15592, 9616, 29088, 5012). This identifies the native fault location, not
the underlying cause. Memory exhaustion, external interference and a scientific
rejection are not established by those events.

V3 uses the environment's already installed NumPy/OpenBLAS eigensolver instead
of invoking the SciPy/MKL eigensolver. Full matrices and their checks are sealed
in parent-only stage receipts BEFORE spectrum evaluation, and the algebra pool
exits before the separate serial spectrum stage. Completed AD graphs may be
garbage-collected. No package, host environment, provider, model or action changes.
There is no controlled benchmark or measured billed-token saving claim.

The four surviving V2 matrices were initially imported with pinned hashes and
all matrix data/checks unchanged. Their two old failed spectrum checks remain
verbatim in the new stage provenance and in the originals. The remaining fourteen
matrices were computed with fourteen bounded spawn workers (configured ceiling 16).
This run finished normally without the earlier native crash. V3's execution-only
smoke passes 15/15; the separate four-saved-case preflight is 72/81, unresolved.

## Why accurate right residuals are insufficient

NumPy/OpenBLAS reduces the worst right-eigenpair backward residual over all
eighteen cases to 1.814e-14, within the unchanged 1e-8 criterion. Nevertheless, a
small backward residual means an eigenpair approximately solves the matrix
equation; it does NOT imply a small eigenvalue forward error in a poorly
conditioned problem. Independent canonical-rescaling and conjugate-eigenvalue
matching remain essential. Their complete-spectrum 1e-6 criterion is unchanged.

The table reports the worse orientation for each diagnostic, independently:

| Family | eta | Canonical-rescaling discrepancy | Left conjugate-match discrepancy |
| --- | --- | ---: | ---: |
| Archived G3 | 1/4 | 2.592e-5 | 2.122e-5 |
| Archived G3 | 1/64 | 0.8326 | 0.7341 |
| Archived G3 | 1/1024 | 0.8779 | 0.9910 |
| New B1-frame | 1/4 | 2.056e-5 | 1.420e-5 |
| New B1-frame | 1/64 | 0.8866 | 0.7396 |
| New B1-frame | 1/1024 | 0.8049 | 0.9801 |
| New hierarchical | 1/4 | 1.832e-5 | 4.184e-5 |
| New hierarchical | 1/64 | 0.7450 | 0.5194 |
| New hierarchical | 1/1024 | 0.7852 | 0.9563 |

The six left-residual failures are both orientations at eta=1/1024 in all three
families; the worst is 4.062e-8 against 1e-8. Those residuals also reflect the
unresolved assignment of left eigenvectors to the right spectrum, not a new
physical constraint violation.

All 6696 returned modes are retained with unresolved classification. The
case-level certification rule withholds mode/energy-sign promotion when a full
comparison fails; this does not prove every individual mode is intrinsically
unresolvable or physically unstable. The stored conditioning-based uncertainty
is a heuristic estimate, NOT a certified eigenvalue enclosure. Constant
symplectic balancing is numerical preconditioning, not a physical energy norm.
Reference-proper-time conversion remains p*lambda_psi; no SI or microscopic
matching normalization is invented.

## Reproducibility and preservation

The complete fresh eight-worker read-only replay recomputed all eighteen
matrices from the frozen action, including the four initially imported matrices,
and reproduced every matrix, spectrum and aggregate byte exactly. It printed
`READ_ONLY_REPLAY_EXACT` and returned exit 1, correctly retaining the same
305/347 unresolved result and all 42 failed checks. This is an exact replay of
an unresolved spectrum, not a passed spectrum.

All 119 source pins and 238 source/sidecar metadata records remained unchanged;
all 80 output/sidecar files retained their bytes, sizes, mtimes and file set.
The external 400-record preservation guard also passed, including all 320
pre-run records, earlier failed attempts, originals and source sidecars. Mutable
queue/register updates are append-only with the previous bytes and sidecars
preserved in an ignored local backup; only those live index sidecars are refreshed.

Full output: `Analysis/MasterTests/outputs/r4c1_canonical_spectrum_v3_n17_attempt_01/`.
This contains 18 full matrix/sidecar pairs, 18 spectrum/sidecar pairs, the frozen
input manifest and three aggregate receipt/sidecar pairs: 80 files in total.
The manifest pins 119 sources with 238 file/sidecar metadata records.

| Aggregate receipt | SHA256 |
| --- | --- |
| summary.json | f533aa4456d51500e62b7aa5d424d36c3c3ab97cd879ffff8cc5ba286dc4f753 |
| independent.json | 75d7f1acc3c244d198383aa21e61c8f83fbb8f5d98078c12f474801b69f42bda |
| formulas.json | 0b70c587079dc436e5173d1cc2569837c3d66728994b46a8f5fd910f4e8efd69 |

Executable: `Analysis/MasterTests/test_01_r4c1_canonical_spectrum_v3.py`, SHA256
`cce30d6764af1c067785cc876f1c89c9214b977f4b49e79907e57f1256b6eb6f`.
Cached engine: `Analysis/MasterTests/r4c1_cached_second_variation_v1.py`, SHA256
`80e763e7200623280af240dda9d6b6af2ba612180a56fd42da3d988afabef3c3`.
Runtime/crash logs stay private and ignored. Original attempts and sidecars are
not overwritten. Both scientific executions completed without a native crash;
exit 1 records the retained numerical failures, not another process termination.

## Next bounded route and inherited holds

Resolve numerical conditioning/precision on these sealed complete matrices
before using eigenvalues to select a healthy family or physical sign. Retain
every direction, quotient only the already prescribed global symmetries, and
keep the existing rejection criteria. Do not mistake increasing a grid for
resolving a demonstrated precision problem. Subsequent n25/n33 convergence,
both simultaneous continuum-node traces, admissible perturbation space and
physical action/clock normalization remain required. Nonlinear persistence,
full coupled interaction/cutoff and healthy-GR/domain evidence are still open.

Stage1 remains complete only in its registered bounded linear prepared-dust
scope. Stage2 INCOMPLETE; Stage3 NOT_ENTERED; Tests1--3 HOLD_SUBSTANTIVE;
MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS;
Stage4A CLOSED; TOP-X4 unchanged. Both identifying weak-field matching inputs
remain absent. No numerical acceleration coefficient is predicted here.

Review DEFERRED; Rule9_cleared=false; inherit COUPLED-DESCRIPTOR-ACTION-V1 and
all transitive first-variation, nodal/planar, joint-root, regularity and canonical
review debt. Review alone is not this numerical or physical blocker.
physics_pass=false; gate_effect=NONE. No state adoption/evolution, action or
microscopic-parent change, vault mutation, manuscript/site work, publication,
commit or push.
