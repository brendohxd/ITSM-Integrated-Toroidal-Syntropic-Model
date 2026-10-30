# Full initial local Jacobi operator, with coefficient drift and clock/lapse pullback

29 October 2026, Australia/Perth. Conditional; review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE. G1-G6 INCOMPLETE.

## Result and consequence

The six registered initial point records now have the COMPLETE local
linearized Euler operator for Y=(q16,S3,N), including zeroth-, first- and
second-order time/spatial terms. Potentials, all original metric/frame/
matter/regulator fields, clock, multiplier, local lapse/shift equations and
coefficient drift remain. The full action was varied before reducing its
clock/multiplier constraint. A separate initial14-field clock/lapse and
nonzero-longitudinal-mode gauge pullback retains all three shift fields.

139/139 controls pass and all seven output files replay byte for byte. This
completes an operator-input step needed for actual source/continuation work.
It does not admit an evolved background, compute the full spatial constraint
inverse, establish a nodal domain, or clear G1/G2. The previous complex
principal branch and exact-band incompatibility remain unchanged.

## 1. Reuse and derivation

Reuse the [completed clock/density jet](RES001_R4C1_CLOCK_DENSITY_SOURCE_V1_REPORT_2026-10-29.md),
the full weak-action backend and the registered physical density/acceleration
records. The older canonical descriptor/two-form drift calculation is not
rerun or counted as this result: it is a different chart/formulation, while
the present calculation differentiates the explicit clock/multiplier and
lapse-gradient weak action on the newer quartic initial jets.

Let deltaA=Q*deltaY+T*deltaY_t+Z*deltaY_z describe the constant slot selectors
in the original56-slot first-jet chart. Unused multiplier derivative slots may
retain zero representatives in the density; its actual q-rate is retained
in the transport direction. Z here is a selector matrix, distinct from the
auxiliary FIELD Z. Let H=L_AA, Ht=Dt(H), Hz=Dz(H). For

    delta E=J0*delta Y+Jt*delta Y_t+Jz*delta Y_z
             +Jtt*delta Y_tt+Jtz*delta Y_tz+Jzz*delta Y_zz,

the complete coefficient matrices are

    J0 =Q^T H Q-T^T Ht Q-Z^T Hz Q,
    Jt =Q^T H T-T^T H Q-T^T Ht T-Z^T Hz T,
    Jz =Q^T H Z-Z^T H Q-T^T Ht Z-Z^T Hz Z,
    Jtt=-T^T H T,
    Jtz=-T^T H Z-Z^T H T,
    Jzz=-Z^T H Z.

These follow by varying E=Q^T*L_A-Dt(T^T*L_A)-Dz(Z^T*L_A), then retaining
both background derivatives of H. Each point file contains all six20-by20
matrices. Ht and Hz use the completed actual initial time/spatial directions,
including epsilon_dot=rho_dot-4*beta*p*rho and tau_ddot=beta*p. Their
deterministic hashes are stored; the executable regenerates their full values.

No third ordinary derivative of the cusp is taken at a node. These six
points are strictly off-node: two stored interior points, and both sides of
both nodes at the stored angular offset0.01. This is a local initial-jet
operator calculation, not a proof that those jets extend to a solution.

## 2. Clock/lapse and spatial-gauge pullback

The original varied multiplier/lapse pair remains algebraically regular.
The lapse row's multiplier coefficient is -1 in this initial volume chart,
with no multiplier derivative in that row. On the homogeneous-clock initial
slice, the original future-clock constraint in the declared perturbation
gauge delta tau=0 gives deltaN=-beta*deltaPsi. Use the same spatial gauge
delta h_xz=delta h_yz=delta h_zz=0 as the parent nonzero-k principal audit.
The resulting14 columns are

    hxx,hxy,hyy,Vx,Vy,Vz,u,v,r,psi,Z,Sx,Sy,Sz.

Let R be their initial embedding into Y; R_N,psi=-beta*N. In the original
unit-lapse/shift-time initial chart, the corresponding nonlinear lapse map is
N=N_background*exp(-beta*deltaPsi). The background clock and its spatial/mixed
jets are retained, rather than replaced with a different clock solution.
Direct variation checks this initial pullback, including the multiplier row.

The reduced initial matrices are R^T*J*R, with the zeroth-order correction

    (J0_pullback)_psi,psi += beta^2*N*E_N.

This follows from the second field variation of the nonlinear lapse map.
The measured E_N is nonzero and retained. The largest correction magnitude
is below4.265e-62 for these inputs; it is not set to zero just because the
background passes a numerical point tolerance. Its coefficient is checked
exactly. The finite numerical variation alone could not resolve such a tiny
correction at the frozen1e-18 criterion.

The pulled-back multiplier column cancels after the FULL equations are
formed. The lapse equation and clock/current row remain available in the
full20 operator. This is not substitution of a zero dust Lagrangian before
variation, deletion of a physical mode, or proof of evolved current transport.

The spatial gauge is for nonzero longitudinal wave number. All full20
matrices are retained for the separate zero-mode/mean analysis; no global
metric mean pair or torus translation is silently assigned a solved value.

## 3. Independent controls and scope of accuracy

| Check | Largest observed normalized discrepancy |
|---|---|
| Whole time-coefficient drift, two real steps | Less than1.426e-33 |
| Whole spatial-coefficient drift, two real steps | Less than2.037e-35 |
| Direct variation of all20 original Euler rows | Less than6.764e-30 |
| Direct nonlinear clock/lapse pullback variation | Less than1.084e-34 |
| Previous full constrained principal reconstruction | Less than2.673e-48 |

The frozen criterion is1e-18. Calculations use110 digits and the sealed
65-digit point inputs. Real drift displacements1e-16/1e-20 are normalized
by the direction size, with complex step1e-26 inside the original Hessian
evaluation. Direct real Euler variations use independent perturbation jets
and the same two small displacement scales. Two-step agreement and these
point controls are not certified derivative-error intervals or evolution
error estimates. Same-author numerical methods are not independent peer review.

The second-order symmetry and first-order formal-adjoint drift identities
are also checked. Removing Ht/Hz changes the tested coefficient blocks by a
normalized amount exceeding0.591 at EVERY point. That is an implementation
effect in these reference charts, not an observed instability or growth rate.

For the principal reconstruction, remove only the VALUE of the background
shift by its real Doppler adaptation: c_original=c_adapted-S_background^z.
At c_adapted=-1,0,2 the leading symbol, followed by the principal three-shift
Schur complement, agrees with the parent11-field pencil. This leading-symbol
check does not invert the full lower-order spatial constraint operator.

All original nonzero Euler residuals, the lapse-residual connection and
all failed/unknown status fields are preserved. There are no failed or
unknown check rows in this receipt. No threshold was relaxed.

## 4. Reproduction and preservation

Contract: RES001_R4C1_FULL_INITIAL_JACOBI_V1_CONTRACT_2026-10-29.md.
Executable: Analysis/MasterTests/test_01_r4c1_full_initial_jacobi_v1.py.
Receipt: Analysis/MasterTests/outputs/r4c1_full_initial_jacobi_v1_attempt_01/summary.json.
Receipt SHA256: a431db3471b5ec87cf0d25313feb90016f4cf9c9990f997a3320839b8f29d1a1.

195 source/export pins and sidecars are checked before and after calculation.
Six point-operator files plus summary are exported. A three-worker original
run and two-worker recomputation return ALL_SEVEN_FILES_READ_ONLY_REPLAY_EXACT.
The seven JSON files total844638 bytes. Original research, failed attempts,
scientific sidecars and unrelated manuscript work are unchanged. Live indices
receive only backed-up append-only updates and their current digest records.

Continuity lookup: ITSM vault item chk_d9aa25efa0e3cb0768a0870e, source
Theory/Gates/RES-001/RES001_R4C1_FULL_WEAK_ACTION_V1_REPORT_2026-10-28.md.
This supplied a continuity pointer; the live pinned action/receipts above
provide the calculation inputs. No vault state or claim was mutated.

## Next actual G1 requirement

Use these coefficients to derive the actual time-tangent forcing and next
nodal background consistency, retaining the clock/density conversion,
spatial/mixed derivatives and any genuinely free continuation jets. The
earlier finite initial acceleration and scalar-jerk results must be reused,
not promoted to persistence. A solved next compatibility condition or a
precise incompatibility is the target; another refinement of a point check
is not a substitute for it.

For a reduced perturbation/frequency source, the full lower-order shift
constraint operator still needs a justified global spatial inverse, including
mean/zero-mode compatibility and inhomogeneous sources. The principal
pointwise Schur inverse cannot supply that inverse. Nodal traces/weights,
constraint/domain preservation, background existence and controlled time
remain substantive. No new state, parent, projector, cutoff or future-boundary
prescription is adopted. No full physical spectrum, physical window or
nonlinear cusp excitation is claimed.

G1-G6 INCOMPLETE; Stage2 INCOMPLETE; Stage3 NOT_ENTERED; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED.
PROCEED_PROVISIONALLY for the full initial local operator and declared
pullback. HOLD_SUBSTANTIVE for the remaining admission/source/domain/time/
window/matching claims. Inherit all action/variation/backend, clock-density,
root/kinetic/force/cusp/jerk/node/constraint/current/Ward, principal/finite-band
review dependencies. Review DEFERRED, not cleared. No manuscript/PDF, site,
publication, commit/push, new provider session or vault mutation.
