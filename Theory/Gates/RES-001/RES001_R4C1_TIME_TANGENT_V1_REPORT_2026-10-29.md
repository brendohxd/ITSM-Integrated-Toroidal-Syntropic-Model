# Actual initial time-tangent forcing and an unresolved auxiliary-node warning

29 October 2026, Australia/Perth. Conditional; review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE. G1-G6 INCOMPLETE.

## Result and implication

The actual initial time derivative of the original Euler equations has now
been calculated at ten registered-profile points. All14 physical third-time
jets are solved there, retaining the full metric/frame/matter/regulator
response, local density/flux, clock and shift/lapse equations. The free second
multiplier time jet is solved from its varied current.306/306 implementation
and independent point controls pass; all21 output files replay exactly.

This goes beyond an operator inventory: it applies the original action and
the previous Jacobi coefficients to the actual time-tangent forcing. It
still does not establish a compatible nodal trace, evolved solution or G1
admission. A new numerical warning changes the next target: the cusp
contribution to the auxiliary third-time jet grows at the closer node
offsets, consistently with a candidate1/abs(w) response. An exact source
identity or controlled remainder is required before calling that a pole or
rejecting a regularity class. No additional physical rejection is certified
by the two finite offsets.

## 1. Preserve the accepted initial conditions and fields

The [quartic root](RES001_R4C1_QUARTIC_JOINT_COMPLETION_V1_REPORT_2026-10-27.md)
already supplies four necessary conditions: mean energy, scalar node field,
node-time equation and second regulator trace, including the exact constrained
shift and fixed charges. Their original proofs, root box and sidecars remain
unchanged. The physical construction stays eta=1/4,e=1/500,k=40, with the same
H,U,Ud,W. Future fields are not constrained to either initial polynomial.

The selected points are the two stored interiors and both sides of both
nodes at angular offsets0.01 and0.001. Existing current/clock results and
the [full initial Jacobi operator](RES001_R4C1_FULL_INITIAL_JACOBI_V1_REPORT_2026-10-29.md)
are reused, not recertified as a new background. In particular the local
physical-density rate comes from the independent Hamiltonian/lapse-flux
calculation. The multiplier rate is rho_dot-4*beta*p*rho; its spatial rate is
obtained by differentiating that Hamiltonian-derived rate, not assigned from
the clock current being tested.

## 2. Actual time-tangent equation and continuation jets

Write the original field equations as E_i=L_qi-Dt(L_vi)-Dz(L_di), retaining
all20 rows (q16,S3,N). Differentiate the full original action along the
completed initial jet. Spatial derivatives of the actual14 accelerations
and second spatial derivatives of the initial velocity are retained.

Let V20 denote this time derivative with the14 physical third-time jets
and second multiplier time jet still removed, but with all known background
and clock terms present. The future-clock root gives

    tau_ttt=beta*aPsi+beta^2*p^2

in the declared initial unit-lapse chart. If M is the original14 physical
time-mass matrix, solve M*j14=V14 at nonzero w. The clock row's coefficient
for the free second multiplier time jet is -1 in this initial volume chart;
it fixes epsilon_tt. Its absence from the physical14 rows is checked.
The final full20 differentiated equations are evaluated independently, with
every nonzero residual retained.

Second-time shift jets and their spatial derivatives are free gauge
channels, not silently fixed future dynamics. The exported representative
uses S_tt=0,partial_z(S_tt)=0 and stores all six linear compensation columns

    delta j14=-M^(-1)*H[v14,S3]*delta S_tt
               -M^(-1)*H[v14,Sz3]*delta partial_z(S_tt).

This does not require a stationary future shift or fixed future nodes.
The scalar-jerk response to these channels vanishes in these point controls.
They are retained for later gauge/domain analysis; a global gauge regularity
or pole-invariance theorem is not inferred from their finite-point values.

The scalar third-time jet also agrees with the separately varied original
regulator formula from the parent jerk calculation, including its metric
trace, shift/volume drift and actual aVy/w term. At the six stored points,
the new direct Euler time derivative agrees with the action of the sealed
full20 Jacobi matrices. This is not continual projection onto a slow graph.

## 3. Cusp bookkeeping and the auxiliary warning

An additional calculation removes only the cubic force summand IN MEMORY,
holding the physical root, fields, phase preparation and shift fixed. Its
local lapse-derived density is recomputed consistently. The A=0 summand is
algebraic bookkeeping; it is not an adopted alternate background/action or
a new mean-charge solution. The physical action/coefficient and all on-disk
sources remain unchanged. The physical-minus-analytic scalar-jerk difference
reproduces the parent's exact cusp kernel on every tested branch.

For the auxiliary difference delta(jZ), all four signed node branches give
the following values at the displayed precision:

| Angular distance from node | abs(w) | abs(w)*delta(jZ) |
|---|---|---|
| 0.01 | 1.9999666668e-5 | 1.0607503692254e-4 |
| 0.001 | 1.9999996667e-6 | 1.0607146465613e-4 |

A proposed original-action source-order coefficient is

    (K_Q/b)*(9/560000)=297/2800000=1.0607142857143e-4.

The product is computed from the diagnostic family's declared coefficients
and the previously derived scalar cusp coefficient, not fitted to these
values. The resemblance is evidence for prioritizing a proof, not that proof.
This is not the cosmological acceleration coefficient C_chi, a newly derived
canonical K_Q, a physical cutoff or an observational prediction.

The precise open step is to verify that ALL other differentiated scalar
source terms have a sufficiently controlled normal remainder, retaining
metric/frame jerks, aZ spatial derivatives, local matter current and gauge
channels. The working proposal is preserved in
RES001_R4C1_TIME_TANGENT_NODAL_WORKING_ALGEBRA_2026-10-29.md, explicitly marked
NOT VALIDATED. No power law is accepted by fitting the two offsets, and no
floating-point root residual is manually zeroed before division.

If a nonzero1/abs(w) term is proved, its consequences must specify the
time/spatial regularity being excluded. It would not by itself exclude every
C2 or distributional weak continuation, reject all R4C1 backgrounds or ITSM,
or authorize smoothing, a new parent/state or a future-boundary prescription.
The earlier scalar joint-C4 and principal-domain findings keep their scopes.

## 4. Verification and preservation

| Independent control | Largest observed normalized discrepancy |
|---|---|
| Original regulator scalar-jerk formula | Less than1.078e-42 |
| Sealed full20 Jacobi time-tangent action | Less than2.250e-42 |
| Completed full20 differentiated equations | Less than9.839e-46 |
| Independent lapse/three-shift time tangencies | Less than4.839e-47 |
| Exact parent scalar cusp kernel | Less than3.066e-48 |

All306 checks pass with no failed/unknown rows. The normalized criterion
remains1e-18. Arithmetic uses140 digits, the original Hessian step1e-26,
real central time steps1e-16/1e-20 and angular steps1e-18/1e-22. The worst
remaining step/initial/gauge-control discrepancy is below6.836e-28. Step
agreement and these finite values are not certified interval derivative or
time-error bounds. Same-author methods/replay are not independent peer review.

Executable: Analysis/MasterTests/test_01_r4c1_time_tangent_v1.py.
Contract: RES001_R4C1_TIME_TANGENT_V1_CONTRACT_2026-10-29.md.
Receipt: Analysis/MasterTests/outputs/r4c1_time_tangent_v1_attempt_01/summary.json.
Receipt SHA256: 9f31eb918c2ef34ccbbc372d6d9e99a44c528385e65cb94a58f985592cc23555.
204 inherited/current source and operator-export pins and sidecars are
verified before/after. Twenty point/partition files plus summary replay
byte for byte using a three-worker run and two-worker recomputation.
Scientific originals, earlier conditions/failures and all old sidecars remain
unchanged. Live indices receive backed-up append-only updates and current
digests. No manuscript/PDF/site, publication, commit/push, provider session,
new parent/state or vault mutation.

Continuity retrieval chk_13bc06404e93e5a9a83ea780 points to the prior
Theory/Gates/RES-001/RES001_R4C1_QUARTIC_TOTAL_JERK_V1_REPORT_2026-10-28.md.
Its live source was checked; its scalar-jerk result is preserved and is not
reinterpreted as a certified auxiliary-jerk pole.

## Next priority

Derive and bound the auxiliary nodal source balance from the generic varied
action BEFORE inserting the initial profiles. Either prove the candidate
nonzero pole with its regularity scope, or identify the missing cancellation
and compute the compatible continuation. Reuse the new time-tangent data;
do not substitute another grid/spectrum sweep for this source/remainder proof.
The nodal weak-domain, full global spatial inverse and mean/zero-mode
conditions, actual evolved admission, physical window/GR and identifying
matching remain substantive. G1-G6 INCOMPLETE; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED;
UVIR-003 IN_PROGRESS; Stage4A CLOSED. Review DEFERRED, not cleared.

PROCEED_PROVISIONALLY for the actual nonzero-tilt time-tangent calculation.
Nodal compatibility and the proposed pole are OPEN. Inherit all action/
variation/backend, clock-density/root/kinetic/force/cusp/jerk/node/constraint/
current/Ward and principal/finite-band/Jacobi review dependencies.
