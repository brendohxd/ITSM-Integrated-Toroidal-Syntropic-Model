# Unchanged R4C1: checked finite-time coupled response, V3 composite acceptance

12 October 2026. Owner: approved Stage-2 coupled-interaction/physical-window
route. This is a finite perturbative-response checkpoint, NOT a physical-window
certificate, healthy-GR result, complete nonlinear solution or Stage-2 GO.

## Scientific result

The coupled response now propagates over t in [0,0.05] in all three frozen
families at the preregistered existing eta=1/4 member and k=20,40,80. Two
independently integrated methods, DOP853 and Radau, give 18 trajectories and
1890 sampled full-22-field response records. They retain the analytic mean,
complex +/-2k, and sampled odd1/3/5 branches. The exact infinite odd force and
Duhamel prescription remain explicit, but their EVOLVED tail is not certified.
The finite odd sample is not asserted to be a closed invariant manifold.

All original sourced Euler equations pass their unchanged 1e-9 residual test.
Maximum normalized full-row residual: 4.807667320582697e-15. The recovered
dust-density derivative is independently differentiated along the joint
background/first-mode/response flow at BOTH frozen differencing steps; maximum
error 1.0163791885058675e-10, below 1e-7. Maximum two-method trajectory
disagreement: 6.273733596790485e-10, below 1e-7. These are chart-normalized
numerical consistency measures, NOT observational accuracy or a rigorous
continuous numerical/nonlinear error certificate.

The drifting affine reduction keeps the inverse/basis/source derivatives,
mean equation, metric/radion/amplitude/phase variables, auxiliary shifts/Z,
and dust/normal/clock constraints. General nonzero trial data test the
reduction beyond the initially prepared zero free-response state. Omitting
drift, affine offsets or constraint sectors is explicitly rejected.
All 378 sampled mean records retain negative signed kinetic eigenvalues;
no eigenvalue is discarded or declared physically healthy by this checkpoint.
Physical-energy/fixed-charge/singular-domain classification remains open.

The next substantive same-action work is a controlled evolved odd-tail and
nonlinear-remainder assessment, then the continuous ALL-sector physical
frequency/momentum domain with interaction/energy/GR/PPN evidence. Finite
mode agreement cannot replace those requirements. Genuine identifying
matching of matter residue AND nonlinear force remains missing; Stage3
is not entered. No coefficient or acceleration target was fitted or inserted.

## Version history: failures are not rewritten

Time V1 source-order wiring failure: source/sidecar and frozen contract retained.
It was interrupted after static inspection found a missing field-label
permutation. No completed numerical receipt/count is claimed; the optimizer
did not return its buffered stdout on interruption. The earlier initial-response
V2 (970/970 and exact replay) already mapped labels correctly and is unaffected.

Time V2 completed the trajectories but remains **FAIL_LOCAL_CHECKS,
10395/10449**, with 54 position-only mean-omission-control failures and no other
failed/unknown check. Exact read-only replay retains the same failure and exit1.
Its trajectory artifact is preserved byte-for-byte, not replaced by a rerun.

Time V3 is a separate **708/708** composite acceptance/control receipt. It
reuses the V2 trajectory bytes and all 10395 independently passed inherited
checks, while addressing every one of the 54 ineffective omission controls.
It does not relabel V2, delete its failures or add overlapping counts into a
fabricated aggregate pass total. V3 exact read-only replay passes708/708 and
returns exit0 with all receipt and sidecar bytes unchanged.

## Mean-metric omission diagnosis

The old test removed positions Mxz,Myz,Mzz but retained their velocities and
accelerations: it did not actually omit those dynamical fields. In the local
homogeneous classical action, constant positive spatial B in g_ij=a^2 B_ij
gives another on-shell background. Constant metric strains therefore lie in
the position kernel, without removing their time-dependent dynamics. All SIX
mean position columns are checked at all378 sampled mean events; maximum
normalized column norm 1.0180155829838267e-15. This is not a claim that distinct
torus moduli are gauge or that fixed global charge/physical energy is settled.

V3 reproduces every original position-only control, then removes q, q_dot AND
the used q_ddot entries together, without re-solving other fields to hide the
omission. Every proper truncation is rejected at the original >1e-12 threshold;
minimum normalized residual 0.001690532222636369. Every accepted trajectory
still retains all six mean metric degrees of freedom. No physical equation,
source value, parameter, numerical trajectory or tolerance was changed.

## Frozen evidence

Original time contract: `RES001_R4C1_THREE_FAMILY_TIME_RESPONSE_V1_CONTRACT_2026-10-12.md`,
SHA 28e0f0d199966f2ab6462a0eb49693198ed0628ad99cabe35d159da5b6488fb5.
V2 repair supplement: `RES001_R4C1_THREE_FAMILY_TIME_RESPONSE_V2_DISPOSITION_2026-10-12.md`,
SHA bbd822284f8ee7fe1d9b439420356e8b93ef1ca3ac3faebe2f982e26de706106.
V3 mean-control supplement: `RES001_R4C1_THREE_FAMILY_TIME_RESPONSE_V3_MEAN_CONTROL_CONTRACT_2026-10-12.md`,
SHA 21123d8d2ad9e1c4390e2b23c6a1d8f5c63d18d25bc3bae06470c8af873ab6c0.

V2 executable `Analysis/MasterTests/test_01_r4c1_three_family_time_response_v2.py`,
SHA 8fec650e4c7d373a480fa087a72fb676cd9289c3d210c4f133320379a246b7ba.
Original failed receipt directory: `Analysis/MasterTests/outputs/r4c1_three_family_time_response_attempt_02/`.
V2 summary SHA 32e55c59882515d00a604dc0eed5dae79b89961f7d8aee32846301c99dc4ab4d.
UNCHANGED trajectory SHA 8a3e5df7765aca174b520a53a8a0ca01848941ec34032cba648c3a198ee9320d.

V3 executable `Analysis/MasterTests/test_01_r4c1_three_family_time_response_acceptance_v3.py`,
SHA 0a91ee47d57eae8646119c7352349005b05997fd84fe2fc9017ccec2d522287c.
Fresh control directory: `Analysis/MasterTests/outputs/r4c1_three_family_time_response_attempt_03/`.
V3 summary SHA 7c43af5b34e8f08e9b74b49a7fe9316b2eddc5ed8376952df97fa70f5e425cea.
V3 mean controls SHA 2d38251c770d33eb4e24d8ebf516a1c280252b4c27da76f047830a4fbda33965.
V3 scope SHA db570a386eadcf2ad068c9696be9b01201d0210019965b2b50815ace68491516.
V3 preserves248 source pins and493 source/sidecar metadata records. Three inherited
UVIR documents have no sidecar; their source bytes are pinned, with no old
sidecar manufactured or overwritten. Ignored progress/log files remain private.

V2 execution log SHA edabf76cdc16ca216eb7d8f14ed396448a551a5ac07709af6fbb94bc213ee3ab.
V2 exact FAILED replay log SHA d5304fd3f3ceacab2b2f4e6e7d3900b7623bd7e1524ff914a2c51b3e84599e43.
V3 execution log SHA 594b12141037792b930f592eb4b77131f7394aa7a5b72745e086ab5a24508366.
V3 exact passed replay log SHA 4c55070ee9d8ab7b77ad212125e3dfa437567ed336160996aea0442ba3763346.

## Unchanged gate and review status

No physical family admitted. Stage2 incomplete, STOP_AND_ASSESS_DOMAIN_UNRESOLVED;
Stage3 NOT ENTERED; identifying matter-residue/nonlinear-force matching absent.
Full evolved odd-tail/nonlinear remainder, continuous physical band, complete
quartic/energy/fixed-charge/singular sectors, healthyGR/fullPPN remain substantive
holds, separate from deferred review. This is not an all-action no-go theorem.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE;
Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Root goal ACTIVE/incomplete. No paper/PDF/publication/commit/push, model/provider,
runtime/dependency or vault operations.
