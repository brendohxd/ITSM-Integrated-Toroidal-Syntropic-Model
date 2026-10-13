# Retarded cubic V2: coefficient-wise exact compiler

Date: 13 October 2026. Frozen before V2 execution.
Original scientific contract:
`RES001_R4C1_RETARDED_CUBIC_BACKREACTION_V1_CONTRACT_2026-10-13.md`,
SHA `5d5cd3a16397a33bac46b398ea2987eca96915895305708a0a21c845bf375d94`.
All action, prepared-data, family/domain, source, force-cusp, solver,
acceptance, physical/canonical and review boundaries are inherited unchanged.

## V1 disposition

Source V1 SHA
`e0d4de2c9743f72d84aa1e18e8699b1a911fa99a5233b3ef70e0c9944e2b8da9`
and its sidecar remain unchanged. Session39201 was confirmed live through
repeated observations, then explicitly interrupted by the agent at the
generic symbolic stage on 13 October 01:18 +08:00. The implementation called
global rational cancellation/factorization on large expressions linear in
many response variables. That is unnecessary for this linear functional and
was the computational structure selected for replacement, not a physics
rejection or a changed test threshold.

The authoritative execution tool reports TERMINAL exit1 after Ctrl-C. It
returned no buffered output and no output-artifact path. The exclusive
progress file retains STARTED and GENERIC_THIRD_ORDER_EULER_DERIVATION.
No integration began, no completed check count or scientific receipt exists,
and no V1 PASS/FAIL physics verdict is claimed. Do not fabricate an exception
trace or call this an observation timeout. Do not overwrite or restart V1.

## Exact replacement, not a smaller functional

Write the complete exported WWR density as
`L=sum_j C_j(W,B,background) R_j`, with j covering every retained response
value/t/x/z jet before any constraints or family specialization. For either
first-direction variable q=W or B, product differentiation gives

`E_q[C_j R_j]=E_q[C_j] R_j
 - (partial C_j/partial q_t) partial_t R_j
 - (partial C_j/partial q_x) partial_x R_j
 - (partial C_j/partial q_z) partial_z R_j`.

Here E_q includes the evolving volume term -3H partial/partial q_t and the
full background/wave derivative maps. Derive coefficients separately and
collect equal response derivatives. Include commuting mixed derivatives:
the R_tx coefficient, for example, receives both
`-partial C_t/partial q_x` and `-partial C_x/partial q_t`.
Factor/cancel only the small individual coefficients, never a global
polynomial over all response variables. No sector or term is dropped.

Check the resulting unreduced W/B Euler expressions against direct expanded
product differentiation, using exact zero residuals without global
factorization. Check E_W+sigma E_B against the constrained first-direction
variation coefficient by coefficient, including all derivative weights.
Only then set the collinear x derivatives to zero for the registered timing
calculation; retain the generic planar coefficient proof. The intrinsic
contact, real force derivative, full kernel, affine drift, third-shift
reconstruction, zero-mode treatment and infinite tails are unchanged.

A compiler-only control may be run before the expensive integrations. Its
success is solely an algebraic implementation check, never an 18-case
result, physical clearance or completion of the full goal. V2 must refuse
to begin integrations if these compiler controls fail.

Use new source `test_01_r4c1_retarded_cubic_backreaction_v2.py` and fresh
`r4c1_retarded_cubic_backreaction_attempt_02` receipts, preserving all older
sources, failed/interrupted attempts and hashes. Perform immutable replay
and owning report/provenance QA once the full result exists. No duplicate
V1 process may be launched. Review DEFERRED, Rule9_cleared=false,
physics_pass=false, gate_effect=NONE; original parent/matching/publication
holds remain unchanged. No new parent, provider/model/runtime setup,
vault mutation, manuscript/PDF edit, commit, push or publication.
