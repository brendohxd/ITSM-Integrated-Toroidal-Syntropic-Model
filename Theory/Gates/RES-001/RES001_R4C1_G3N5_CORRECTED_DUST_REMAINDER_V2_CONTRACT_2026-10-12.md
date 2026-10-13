# G3N5 corrected remainder v2: forcing-sign repair and regression

Date: 12 October 2026. Version 2. Supplements the
[v1 contract](RES001_R4C1_G3N5_CORRECTED_DUST_REMAINDER_CONTRACT_2026-10-12.md),
whose negative-forcing decomposition is INVALID and must not be adopted.
Its source, contract, sidecars, interrupted record and partial log remain intact.
This is an implementation repair, not a change to the action, parameters,
original physical initial data or any earlier accepted norm-only bound.

For R_H=A_c H-H_dot-H M_c, subtracting the reference equation gives

```text
e_dot=A_c e+R_H Phi_c J(0)^-1 W0,
W_full=W_ref+W_retained+O_c integral Gamma_c R_H Phi_c J(0)^-1 W0.
```

The forcing and integral therefore have PLUS signs. The norm inequality for
the absolute forced remainder is unchanged. V1 was interrupted after this
analytic defect was identified, not because a wait timed out; no completed
PASS/FAIL acceptance receipt exists for it. No physical conclusion is inferred.

Inherit every other v1 input, domain, exact cancellation, initial inverse,
source-interval, complete coupled integration, paired solver, all-five-mode/
four-column/22-field, source-metadata, immutable replay and acceptance rule.
Keep full original mismatch/forcing; do not replace physical evolution by a
projected dust equation. Actual convergence order and useful accuracy remain
open. The controlled remainder is after retaining the complete homogeneous
response, not a small-error theorem for a closed dust-only approximation.

Before first v2 execution add independent sign regressions:

1. Scalar x_dot=x, reference H=1,M=0: R_H=1 and e=exp(t)-1 must obey
   e_dot=e+1. The negative-sign residual must be explicitly nonzero.
2. Generic matrix A,H,H_dot,M,Phi: verify the full decomposition derivative
   with +R_H exactly, and reject the -R_H identity. These are mathematical
   sign checks, not new physical data or parameter fits.

Use source v2 and fresh corrected_dust_remainder_attempt_02 receipts. Do not
rewrite v1, its attempted directory, or any original source/hash/failed record.
All prior physical/canonical/review holds remain: physics_pass=false;
gate_effect=NONE; Rule9_cleared=false; review DEFERRED; Tests 1-3
HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED;
V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED. Stage 2 stop and stage 3
matching gap unchanged. No publication, provider/model dispatch, vault mutation,
commit or push.
