# G3N5: uniform prepared-dust upper rate, with practical-control gap

Date: 11 October 2026. Owner: Master Test 1 / conditional R4C1/B1, stage 1.
Result: CONDITIONAL_PREPARED_DUST_UPPER_RATE_TWO. Main v1 67/67; finite-
constant supplement 7/7; both exact read-only replays pass. This is not
completion of the full dust milestone: sharp/actual order and useful finite-
mode accuracy remain OPEN. physics_pass=false; gate_effect=NONE;
Rule9_cleared=false; review DEFERRED. Stage 2 admission and stage 3 unchanged.

## 1. New theorem and its precise limitation

For the ORIGINAL registered prepared graph data, the complete 20-state
evolution and ACTUAL two-state dust observable have a uniform error upper
bound on t in [0,1/20]. For coordinate ell>=15,

```text
||W_full(t)-Phi(t) W0||_infinity
    <= C2(t) ||W0||_infinity / ell^2.
```

All constants and C2(t) are explicit in the
[main formulas](../../../Analysis/MasterTests/outputs/r4c1_g3n5_prepared_dust_error_attempt_01/formulas.json).
Separate controlled finite-mode inequalities for ell=4,8 are retained in
the [constant supplement](../../../Analysis/MasterTests/outputs/r4c1_g3n5_prepared_finite_constants_attempt_01/finite_bounds.json).
The bound is derived from the unchanged generator, not fitted to the old
five-mode inverse-square trend. It includes fast forcing and initial mismatch.

C2(1/20) is approximately 168549167.52104756. This large prefactor makes the
estimate far too conservative to certify the small archived errors. It proves
an asymptotic UPPER order of two, not sharpness, a precise leading effective
dust correction after feedback, or useful finite-mode accuracy. Those stronger
requirements are not silently declared complete.

The theorem concerns a derivative-weighted linear transfer norm on the frozen
rotating B1 solution, with a,C,rho_m>0, J=1 and the preserved Friedmann shell.
Coordinate periods remain 2*pi; p=ell/a and p_dot=-H*p are retained. The
background still starts at v_dot=1,r_dot=1/4. It is not a nonlinear stability,
physical cutoff, all-direction Cauchy, zero-mode, healthy-GR or calibrated
cosmological prediction. Unit transfer columns may be scaled infinitesimally;
they are not new finite-amplitude physical initial conditions.

## 2. Corrected comparison lift is not a projection or replacement data

Use x_c=C z, z=B x, the full generator A_c=sum_d A_d ell^d, d=-2,...,2,
and the already action-derived leading dust flow M. Construct a comparison
lift H=sum_{j=0}^3 H_j/ell^j by the exact generator recurrence. Its residual
R_H=A_c H-H_dot-H M has zero coefficients at powers 2,1,0,-1 on the declared
preserved shell. The inverse matrices and shell reductions divide by no
background scalar velocity. Coordinate derivatives and momentum drift stay.

In particular the first forced fast correction is

```text
(H1)_(chi,D) = -22 i a rho_m / 25,
chi = p^2 Pi-i p psi_dot Vx.
```

The initial graph is NOT changed to H. Its difference from H has a leading
opposite fast component plus an explicitly bounded order-two remainder.
The actual graph-normalized original data are reconstructed exactly at t=0;
all initial values and the analytic inverse-ell-zero remainder are checked.

Whole-interval rational matrix norms bound every remaining source coefficient,
the reference-observable normalization and the initial mismatch. The prior
[full propagator](RES001_R4C1_G3N5_DUST_UNIFORM_PROPAGATOR_REPORT_2026-10-11.md)
and [retained fast-transfer lemma](RES001_R4C1_G3N5_DUST_FAST_TRANSFER_REPORT_2026-10-11.md)
control the full forced response. Actual evolution is never projected back
onto H, and no wave, phase, slow or fast state is deleted.

Writing constants as in the receipt, the explicit coefficient is

```text
C2(t)=(3/2) [ K_O {3 exp(30t)(C_other+2 K_W K_source t)
                    +9 kappa t exp(gamma t) C_fast}
             +3 K_Of exp(30t) C_fast
             +K_observation exp(21t/10) ].
```

The factor 3/2 bounds the conversion from two-observable operator 2-norm to
infinity norm. The separate ell=4,8 estimates use the full ell>=4 propagator
and exactly exported initial/observation constants, not the inverse requiring
ell>=15. Interval constants come from the ODE boxes, not sample maxima.

## 3. Archive controls are not the proof or new fitted results

All five modes, 257 times, both prepared columns, both complementary columns,
negative conjugate modes and all 22 original fields remain unchanged. The
following errors are ABSOLUTE infinity-norm transfer errors; the earlier
report's e_ell divides by the leading-Phi norm. Their difference in display
is a declared normalization, not changed trajectories or recalibrated physics.

| ell | Original absolute prepared error | Certified endpoint bound display |
|---:|---:|---:|
| 4 | 0.007606705975110484 | 129322.35108445506 |
| 8 | 0.0017826951264717783 | 13657.766682455796 |
| 16 | 0.0004418373158664446 | 658395.185629092 |
| 32 | 0.00011046044682705425 | 164598.796407273 |
| 64 | 0.0000275942542774521 | 41149.69910181825 |

These very loose upper bounds are not observed growth or evidence of physical
instability. The differing low/high comparison estimates are not expected to
form a monotonic sequence across their domain boundary.

Worst normalized direct/Laurent residual difference: 1.6732233359403404e-14.
Worst observable reconstruction disagreement: 2.1186783114725702e-14.
Worst all-22-field reconstruction disagreement: 1.1052781145066174e-14.
Each actual error is checked against its time-dependent inequality at all
257 times, with only the frozen binary64 allowance. Nonmonotonic complementary
responses, original -11/6 coefficient, ordinary-wave Jordan defect and
indefinite physical Hamiltonian are retained rather than reclassified.

## 4. Remaining obstruction and focused next step

An exact arithmetic breakdown of C2(1/20) gives approximately
166892145.43047622 (99.0169%) from the conservative fast-to-other transfer
majorant. The retained-source contribution is 1514133.5970912655; other-
initial mismatch is 142689.24280831937. Direct fast observation contributes
147.94296457485513 and lift normalization 51.307707175883465.
These are terms of an UPPER BOUND, not measured contributions to the error.

The next bounded target is therefore a sharper retained-component/observation
estimate, especially the auxiliary comparison-propagator exponent. Use the
actual block structure and energy identities; do not lower a constant based
on observed errors or discard generated fast response. Separately derive the
observable's leading finite correction after feedback and establish or reject
sharp order, rather than inferring it from the finite sample or a formal
nonzero coefficient. The full stage remains OPEN_SHARPNESS_AND_USEFULNESS.

## 5. Reproduction, preservation and downstream boundary

[Main executable](../../../Analysis/MasterTests/test_01_r4c1_g3n5_prepared_dust_error_v1.py):
1a9e162f5985c8f2a7ee00ffc6eea227106bcf49afb238fd7dbaa55202096748.
[Main summary](../../../Analysis/MasterTests/outputs/r4c1_g3n5_prepared_dust_error_attempt_01/summary.json):
a637c7291ba1f3e1c1b3719f4c640de3b690c40bb0e9c6b38e7d9e37ab9f0e40.
Main formula hash: f99c5ee10bc26124cdd1a22ae2d496ce9281319c21bab762f59f01d256c53829.
Main diagnostics hash: fed0134d6e792417339144c6d1f4a1630f83f6fbe866b86d69a62b315ace35d4.

[Finite-constant exporter](../../../Analysis/MasterTests/test_01_r4c1_g3n5_prepared_finite_constants_v1.py):
724736b04905eb74f02608a971768f68891c681d3148c1ee792d63284026c8be.
[Supplement summary](../../../Analysis/MasterTests/outputs/r4c1_g3n5_prepared_finite_constants_attempt_01/summary.json):
7d0f2235bbd2d419ae3457b5dfc591c755c1d548584329d3f5dd1e259378cd03.
Supplement artifact hash: 96e5c39cbc6bb64717732ba9772ddbaa6cbf7f3b54c944a1245177b2c6eae6f6.
The exporter adds exact low-mode constants in a NEW directory; the original
main receipt and source remain byte-identical. Main and supplement preserve
473 and 481 input/source/available-sidecar files respectively. Both replays
recompute and match scientific JSON/sidecar bytes without receipt writes.

Private direct recurrence completed; no calculation from this checkpoint is
still running. The interrupted older exploratory source remains with no
mathematical verdict. All old failures and absent UVIR sidecars stay declared.
The memory skill keeps local proofs separate from canonical/physical clearance;
current source equations and receipts, not memory or model consensus, are evidence.
Standalone optimizer used; no guaranteed billing savings claimed.

Stage 2 still lacks full coupled physical interactions/window and healthy GR;
its action-selection stop is unchanged and may be reassessed by the operator.
Stage 3 NOT ENTERED: no microscopic residue/nonlinear force matching or sealed
numerical acceleration prediction. Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 UNCHANGED. Reviews of these and inherited operator/action entries are
DEFERRED, not cleared. No publication readiness, commit/push, submission,
paid provider/model dispatch, vault mutation, manuscript/PDF or deployment change.
