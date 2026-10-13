# G3N5 actual-observable finite-wavenumber correction: frozen contract

Date: 11 October 2026. Version 1. Stage 1 / Master Test 1 / R4C1/B1.
This is a formal coefficient certificate, NOT completion of dust closure.
The full corrected evolution, retained fast/wave response, useful remainder
and sharp/actual order remain required by the approved plan.

Use the pinned full generator, original H0-H3 lift, wave chart Tw, actual
dust observable, leading dust generator M and rotating B1 background. Keep
all 20 states/22 fields, constraints, J=1, v_dot(0)=1, r_dot(0)=1/4,
p=ell/a and coordinate/momentum drift. No new physical action or data.
The whole-interval boxes are t in [0,1/20], a,C,rho_m>0 and the preserved
Friedmann shell. No velocity quotient or inverse at rho_m=0 is admitted.

Compute R2 from the COMPLETE Laurent generator and H_j derivatives. Let
S select the two principal-kernel rows 3,13 in the Tw chart, and
G=S Tw H0. Verify the principal-kernel and invertibility conditions, then
N2=G^(-1) S Tw R2. This is the solvability correction to the lift chart,
not the instantaneous graph coefficient or a closed physical dust law.

Derive J2 from O_c H=I+ell^(-2)J2+..., using the actual observable. The
correction in normalized observable coordinates is
N_obs=N2+J2_dot+[J2,M]. Differentiate using the complete evolving background.
Recheck the normalized observation and projected residual. Retain the
unprojected fast/wave residual and original initial mismatch downstream.

Under H -> H(I+ell^(-2)Z(t)), verify exactly that
N2 -> N2+[M,Z]-Z_dot, J2 -> J2+Z and N_obs is unchanged.
This is an auxiliary-chart invariance check, not arbitrary physical field
or unit invariance of the complete action. Show that omitting J2_dot or
the observation normalization changes the coefficient.

Controls fixed before execution:

- Exact principal, constraint-shell, projected solvability, normalization,
  chart-invariance and matrix roundtrip checks. Nonzero formal coefficients
  are NOT accepted as convergence or stability proofs.
- Independent numerical time differentiation of J2 along the original
  background series at t=0,1/40,1/20. Step 1e-5; centered difference in the
  interior and three-point one-sided differences at endpoints. Compare the
  reconstructed N_obs against its symbolic value with 1e-6 relative plus
  1e-7 absolute allowance. These samples check implementation, not a remainder.
- All derivative/constraint terms stay. Original archive hash/size/mtime
  and available-sidecar preservation, fresh receipts and exact read-only replay.
- Export N2, J2, N_obs, G and exact initial N_obs. Do not integrate a newly
  projected dust equation, fit any acceleration, or alter old trajectories.

Review DEFERRED; physics_pass=false; gate_effect=NONE; Rule9_cleared=false.
Sharp order and controlled corrected-system remainder NOT_PROVED.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Stage 2 STOP_AND_ASSESS_DOMAIN_UNRESOLVED; stage 3 NOT ENTERED.
No commit, push, publication, provider/model dispatch or vault mutation.
