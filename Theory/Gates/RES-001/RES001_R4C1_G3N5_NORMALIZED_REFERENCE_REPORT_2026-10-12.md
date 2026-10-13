# G3N5 normalized-reference component checked; full finite-mode error open

Date: 12 October 2026. Version 1. Owner: Stage 1 / RES-001 / Master Test 1.
V2: 46/46 local checks, zero failures/unknowns, exact read-only artifact/sidecar
replay complete (terminal exit 0). This is a REFERENCE COMPONENT result,
not completion of the full-state error budget or the full dust milestone.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.

## Exact identity and scope

Use the same complete corrected lift Hc, actual observation Oc and
Mc=M+N2/ell^2. Let J=Oc Hc, S_ref=J_dot+J Mc-M J and
W_ref=J Phi_Mc J(0)^-1 W0. Its initial observable is W0 exactly. Then

    (W_ref-Phi_M W0)' = M(W_ref-Phi_M W0)
                           + S_ref Phi_Mc J(0)^-1 W0.

The forcing sign is positive. Whole-background interval bounds give

    ||W_ref-Phi_M W0||_infinity
      <= K_source K_J0_inverse t exp(lambda t) ||W0||_infinity,

for the registered rotating LINEAR B1 prepared family, original nonzero
ell=4,8,16,32,64 and 0<=t<=1/20. Time and input normalization are the registered
diagnostic coordinates; this is not an acceleration prediction or a physical
frequency/momentum validity window. No inverse of J(t) is required.

V2 extracts the COMPLETE actual observation polynomial and convolves it with
every corrected-lift coefficient. J0=I and J1=0 are simplified only after
exact on-shell identities and background-constraint preservation are proved.
The frozen observable N_obs is recovered at order ell^-2 by an identity, not
by inserting a target. ALL source coefficients 0..9 are retained. Higher
coefficients remain factored for exact interval bounds. J_dot, original
constraints, complex fields and momentum/basis drift are not discarded.
On-shell equivalence in this algebra is not projection of evolving states.

## Actual reference-error bounds

At t=0.05, the following multipliers bound the reference error relative to
||W0||_infinity. Displays are rounded; exact constants/expressions are in the
frozen receipt.

| Original ell | Reference-error bound multiplier |
|---|---:|
| 4 | 5.52868881091396 |
| 8 | 0.238608769768453 |
| 16 | 0.0141820570660286 |
| 32 | 0.0010911697622268 |
| 64 | 0.000125408601740431 |

The highest-mode reference component is bounded by approximately 1.25e-4
times the input norm. This is NOT the total error: retained original
fast/wave mismatch and complete forced response must still be added.
The ell=4 reference bound is itself loose. No accuracy tolerance was selected
after results, and no full finite-band usefulness claim is made.

## Independent controls and preserved attempts

All 15 original-map product-rule controls (five modes, t=0,0.025,0.05) pass
at 70 digits and the unchanged 1e-30 criterion. Maximum normalized residual:
1.01175092313514e-69. These are algebraic identity points, not new or projected
physical trajectories. Generic noncommuting-matrix/sign identities, omitted
J_dot rejection, initial normalizations and complete coefficient checks pass.
579 inherited input/source/available-sidecar metadata preserve their hashes,
sizes and mtimes through computation and replay. Original five modes, four
columns, all fields and nonmonotonic complementary probes remain untouched.

V1 was intentionally computationally interrupted before an algebra verdict.
Its command terminated with exit 1; no traceback/profile was captured. The
global free-momentum cancellation bottleneck was inferred from code structure,
not proved by a captured hot-line trace. Its frozen source, contract, progress
and interruption record are preserved. This is NOT a failed physical test or
an invalidated earlier theorem. V2 changes proof representation only.

The separate finite-energy V1 command was likewise deliberately interrupted
without a mathematical verdict and retained. The new complete-coefficient
finite-energy V2 calculation remains pending at this report's checkpoint;
no result or replay for it is inferred from the reference receipt.

## Reproducibility and remaining obligations

- [V2 contract](RES001_R4C1_G3N5_NORMALIZED_REFERENCE_V2_CONTRACT_2026-10-12.md):
  35e2ee212d00dbef48752b933503a2462c956685bd996f2aa21550bbb601a672.
- [V2 executable](../../../Analysis/MasterTests/test_01_r4c1_g3n5_dust_normalized_reference_v2.py):
  592e0369a52f9d5e0d6636c6223314b8af78be760a76321026795a6118824e2a.
- [Summary](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_normalized_reference_attempt_02/summary.json):
  5db4548cd8d74201310c4e046873b660e5cee33c70c7a7aa12b8f38dd219b47a.
- Formulas: 988d12bd27b55a1020ec2f99376327553b9e3c63348d9e58eb15757971d32ec7.
- Diagnostics: 7fb18f425feb600b31baf39170ab81fbffdee290f3c2ad2f8a2d12c17c49e97f.

Read-only replay reproduced every artifact and sidecar byte. Fresh overwrite
is refused. Private logs/context remain local, not publication artifacts.

Stage 1: scoped sharp asymptotic order two remains checked by the unchanged
earlier theorem. Complete/useful original finite-mode error control remains
OPEN. Stage 2 STOP_AND_ASSESS_DOMAIN_UNRESOLVED still requires explicit
operator action selection before its stopped coupled-interaction/window route
advances. Stage 3 NOT ENTERED: genuine matter-residue/nonlinear-force identifying
inputs remain absent. No new microscopic parent or TOP-X4 pivot.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Inherited reviews DEFERRED; no canonical/publication clearance. Native goal
ACTIVE/incomplete. No commit, push, publication, provider/model dispatch,
vault mutation or runtime configuration change.
