# Initial first-variation precision hold resolved in the registered numerical scope

20 October 2026. Unchanged R4C1 Stage 2. Review DEFERRED.

## Finding and meaning

The coupled initial momentum/first-node-tangency calculation now passes its
frozen numerical checks: **2923/2923**, with complete fresh exact read-only
replay. The earlier current and differentiation-step failures were resolved
using better-conditioned, higher-precision first variations, not by changing
the action, candidate coefficients, physical domain or acceptance tolerances.

This permits provisional reuse of these INITIAL FIRST-VARIATION controls.
It does not establish an exact global on-shell background, existence or
persistence of a solution, the complete auxiliary nodal hierarchy, a physical
mode spectrum, a cutoff, a healthy GR limit or a physical validity window.
No candidate state has been adopted or evolved. Stage 2 remains INCOMPLETE.
Both identifying matching inputs remain absent; Stage 3 is NOT_ENTERED.

## What was calculated

All three registered families at eta=1/4,1/64,1/1024, e=1/500,k=40 retain the
same joint H/U/Ud inputs and original finite-mode shift. The 17/25/33 odd grids
and both shifted node orientations give 54 controls. Each was independently
recomputed at 80 and 100 decimal digits, retaining the two original complex
steps 1e-18 and 1e-22 for dense all-variable and complete-tangent checks.
These are finite-grid point controls, not amplitude-uniform interval bounds
or a continuum-domain certificate. Each odd shifted grid tests one exact node;
the opposite orientation is tested separately, not silently skipped.

The computation retains the coupled metric/frame/field/dust/regulator system,
both fixed charges with local fluctuations, three mean metric pairs, global
translation section, spatial constraints, lapse flux and metric/frame two-form
crosses. Qdot is computed from H_P, not reset to the expected profile. The
existing candidate Zdot and original undivided regulator sdot are retained as
declared inputs to this initial diagnostic. No continual slow-graph projection
or inverse of V^2 at a node is used. Complete auxiliary/background admission
remains a separate requirement; this is not a new exact background solution.

A stationary first-variation evaluator avoids the cancellation in the old
binary64 energy derivatives. At the base it solves the complete quadratic
temporal complement and verifies stationarity. With Lcal=volume*L0 and
P_y=(2*pi_h,p_V,p_u,p_v,p_r),

    dE0 = sum(y_a*dP_y,a) - dLcal at fixed solved y.

The reverse-mode evaluator differentiates the full nonlinear constraint
pullback. An independent unreduced generator keeps the original momenta fixed
and retains N*(p_Z+g*s)*Z_hat BEFORE substituting its constraint. The new local
density value and all 43 position/spatial-gradient/velocity/scalar-rate
derivatives are checked against the pinned original density at nodes and
signed neighbors. This is independent computational verification, not
independent Rule-9 review; parts of the original geometry are shared.

The local first Ricci variation -D^2(delta hxx+delta hyy) is retained in the
node-energy calculation. The closed-torus integrated first-divergence identity
does not delete local curvature. The nonzero curvature second variation and
all prior regularity restrictions remain binding.

**The stationary evaluator is a FIRST-DIFFERENTIAL tool, not an off-base
Hamiltonian or a physical Hessian.** The next second-variation calculation
must include the response of the solved temporal velocities, nonlinear
constraint pullback, full curvature and background-dependent two-form drift.
Reusing frozen velocities as a Hessian would be incorrect.

## Measured controls, not physical clearance

Largest values across all 108 precision records:

| Control | Maximum | Frozen criterion |
|---|---:|---:|
| Original versus reduced momentum generator | 6.140e-27 normalized | 1e-7 |
| Phase-current discrepancy | 3.474e-21 relative | 1e-4 |
| Dust-current discrepancy | 3.475e-21 relative | 1e-4 |
| Node-energy derivative | 3.033e-14 on registered scale | 1e-4 |
| Node chi derivative | 2.368e-83 reference units | 1e-8 |
| Full-period regulator row | 7.841e-25 on registered scale | 1e-4 |
| Original-density/43-derivative control | 2.653e-81 normalized | 1e-40 |
| Computed initial coordinate-rate comparison | 4.209e-30 normalized | 1e-8 |

The actual nonzero node-energy residual is retained, not set to zero. Both
complex-step and 80/100-digit derivative comparisons pass. Force outputs
retain 35 significant digits, sufficient for the frozen normalized 1e-10
interprecision comparison; this is not a claim of 100 certified significant
digits or an interval error proof. Explicit-time energy balance is tested
with H_tau=beta*Qdust/p, not an assumed conserved Hamiltonian. The largest
recorded energy-directional defect is 2.874e-16 reference units, below its
declared normalized criterion; it is not declared exactly zero.

A separate read-only cross-version comparison of every retained field and
mean momentum rate gives a maximum normalized V1/V3 difference below
3.010e-13. The large relative V1 failures involved tiny currents, not an
unannounced different force law. This comparison is not a state-admission
or physical-accuracy theorem.

An additional read-only 100-digit G3 eta=1/1024,n=17 diagnostic gives the
inherited s-row residual max|H_s+g*Zdot|/K_Q about 5.802e-20 and a node-energy
compatibility residual about 5.802e-20 on K_Q*p^2. This is ONE additional
diagnostic, not an all-domain auxiliary-row or exact on-shell certificate.

## Preserved history and execution

- V1 remains 833/880 with all 47 failed assertions and its exact failed replay.
- V2 remains a 2922/2922 passing first attempt. Its later independent x/17
  derivative probe found an 8.1634e-19 error: `1/z` with integer z created a
  binary64 adjoint weight. Its intended derivative precision was therefore
  limited even though its frozen tolerances passed. V2 was not rewritten;
  its full replay is not claimed or unnecessarily repeated.
- V3 changes that reciprocal to `mp.mpf(1)/z`, adds the independent odd-
  integer-division test and updates source pins. AST comparison confirms
  only that method and engine_controls changed; the other 50 functions/
  methods are identical to V2. V2/V3 formulas.json bytes are identical.

The first V3 run used at most 16 Windows-spawn workers. Complete fresh
eight-worker replay recomputed every control and returned exit zero and
READ_ONLY_REPLAY_EXACT. All six scientific payload/sidecar files are identical
and their sizes/mtimes unchanged. Sources cover 99 pins/198 metadata records;
the separate 254-record before/after guard preserves prior successes,
failures, sources, sidecars and new outputs. Private ignored runtime journals
remain local. No speedup or billed-token saving is inferred from worker count.

| Artifact | SHA-256 |
|---|---|
| V2 precision contract | cb960191f1a9270613c2f2c03fa82986ccae351d48a979115fc8c72e3d8da964 |
| V3 weight addendum | df86efc15fa0ae37957114909309df5772592b4abd629269928e967fddb59032 |
| test_01_r4c1_nodal_momentum_tangency_v3.py | b887c7a52102b7abb43a2875cb6e01607ecb46d39a95f4abb4cefab9795a73c0 |
| attempt_03/summary.json | 15620d36fbed613229d740bb3cb15980929f98ac8b4d4435a757dd93d6454dfe |
| attempt_03/independent.json | 75f02f299e568df9d031c9a58b2ed658411f3581d982e474f091ffb0e82f887a |
| attempt_03/formulas.json | a99cedccfa53fb81492dbe7bc43b048ca8d29294050dd2dea95d90b5b750bd5f |

Executable: Analysis/MasterTests/test_01_r4c1_nodal_momentum_tangency_v3.py.
Receipts: Analysis/MasterTests/outputs/r4c1_nodal_momentum_tangency_attempt_03/.

## Next substantive route and programme holds

Complete the auxiliary node/background conditions and admissible mixed-order
space, then the actual coupled descriptor Hessian AND two-form/background
drift. Retain both node traces, all constraints and means; neither nodeless
inversion nor a raw sign-only test supplies the physical mode problem.
The physical spectrum, nonlinear interaction/error control, frequency/momentum
window, arbitrary-direction completion and healthy GR recovery still require
evidence. No potential parameter or vacuum-probe scale is adopted as a cutoff.

Review DEFERRED; Rule9_cleared=false; inherit NODAL-MOMENTUM-TANGENCY-V1,
GLOBAL-NODAL-LIFT-V2, NODAL-DESCRIPTOR-V2, PLANAR-REDUCED-HAMILTONIAN-V1,
joint-root/regularity/canonical and transitive review debt. Only the registered
first-variation numerical hold is resolved. Stage1 remains complete only in
its bounded linear prepared-dust scope; Stage2 INCOMPLETE; Stage3 NOT_ENTERED;
Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED;
UVIR-003 IN_PROGRESS; Stage4A CLOSED; TOP-X4 unchanged; physics_pass=false;
gate_effect=NONE. No state adoption/evolution, new parent/action, smoothing,
provider/model/global-runtime change, vault mutation, manuscript/site edit,
publication, commit or push.
