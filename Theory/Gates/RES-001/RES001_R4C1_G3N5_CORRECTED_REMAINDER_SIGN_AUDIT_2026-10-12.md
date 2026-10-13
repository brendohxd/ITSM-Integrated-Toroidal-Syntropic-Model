# G3N5 corrected-remainder sign audit and preserved interruption

Date: 12 October 2026. Version 1. Stage 1 / Master Test 1 / conditional B1.
The new corrected-remainder v1 implementation contained an analytic forcing
sign error. It was interrupted, not silently repaired or accepted. V2 is a
new frozen source/contract and is RUNNING; no new acceptance result is claimed.

## Exact diagnosis

The residual convention is R_H=A_c H-H_dot-H M_c. For x_ref=H Phi_c J(0)^-1
and e=x_full-x_ref, direct subtraction gives

```text
e_dot=A_c e+(A_c H-H_dot-H M_c) Phi_c J(0)^-1
     =A_c e+R_H Phi_c J(0)^-1.
```

The retained initial mismatch evolves homogeneously under the full A_c.
The forced remainder has a PLUS Duhamel integral. V1 incorrectly propagated
the forced control with -R_H; its contract also contained that invalid sign.
Neither convention nor physical equations have changed. This is a defect in
the NEW decomposition implementation, not a discovered physical instability.

Scalar regression: x_dot=x, H=1,M=0 gives R_H=1 and e=exp(t)-1, satisfying
e_dot=e+1. The negative-sign residual is 2, not zero. V2 adds this and an
independent generic-matrix decomposition identity, explicitly rejecting the
negative sign, before the coupled control calculations.

## Preserved evidence and unaffected results

- [V1 source](../../../Analysis/MasterTests/test_01_r4c1_g3n5_corrected_dust_remainder_v1.py),
  unchanged SHA-256 82aeeb59a1eacf15e58a0313227dc17f6f17af7c92f0fe09e719793cd7a1af06.
- [V1 contract](RES001_R4C1_G3N5_CORRECTED_DUST_REMAINDER_CONTRACT_2026-10-12.md),
  unchanged SHA-256 bff52ca9a787c96c984f7e0f667d6c82920cbaba25a22b3ebe08e8b05a774748.
- [Interrupted-attempt record](../../../Analysis/MasterTests/outputs/r4c1_g3n5_corrected_dust_remainder_attempt_01/interruption.json),
  SHA-256 f7d132a7c7a297ac5c961f86a9308d1c64c6d8f0c08ba6779cd461882dfd2078.
- Private v1 progress/source logs retained. The interrupted handle returned
  terminal exit 1. No numerical PASS/FAIL or scientific acceptance finished.
  The interruption was for a demonstrated defect, not a timeout or silence.

Original trajectories, prepared data, action, parameters, hashes and all
earlier scientific receipts are untouched. The full order-two lift cancellation
is algebraic and not changed by this integration-sign repair. The 73/73 leading-
dust upper bound and completed exact replay use absolute source-norm inequalities;
they do not depend on this new signed control integration. The 29/29 formal
observable correction and exact replay also do not use this faulty integration.

## Repair and remaining acceptance

[V2 contract](RES001_R4C1_G3N5_CORRECTED_DUST_REMAINDER_V2_CONTRACT_2026-10-12.md):
30c247bb16bdc678932ff7749f1edc0c01ec27b75ff6cfea7a779e063c8f9385.
[V2 source](../../../Analysis/MasterTests/test_01_r4c1_g3n5_corrected_dust_remainder_v2.py):
1f3f84ff56c5521d27fc01d477be964c81723da23591837e0484f1c68f408bc9.
V2 retains v1 as an input-provenance dependency and uses fresh attempt_02
receipts. The forced RHS is now +R_H. All other full-state, original-data,
interval/source, paired solver, all-mode and replay requirements remain.
The forced-remainder norm inequality is unchanged because it bounds magnitude.

At this snapshot v2 is live and has derived the full first-correction lift.
Source constants, complete coupled controls, owning acceptance report and exact
replay still require results; no corrected-system bound is claimed yet.

Separate private exact diagnostics find that the leading dust observer sees
only the two slow coordinates, its first fast coefficient is zero, and proposed
fast/ordinary microtime witnesses cancel. Additional sector-coordinate identities
cancel slow-wave order-zero and slow-fast next-order couplings while retaining
every state. These are needed algebra, NOT a retained-response bound or actual-
order theorem. Initial transient candidates are not substituted for that proof.

The separate higher-lift prototype is still live and has no acceptance receipt.
Stage 1 and full goal remain OPEN. Sharp/actual order and useful finite-mode
accuracy remain unresolved. Stage 2 stop/physical-window and stage 3 matching
gaps unchanged. physics_pass=false; gate_effect=NONE; Rule9_cleared=false;
review DEFERRED. Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 UNCHANGED. No canonical promotion, publication, commit/push,
provider/model dispatch, vault mutation, manuscript/PDF or deployment change.
