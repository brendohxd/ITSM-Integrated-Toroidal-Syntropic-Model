# R4C1-G3Z: subleading zero-sector inner frequency pencil

Date: 2026-09-30. Owner: Master Test 1 / R4C1-v1 / G3 family.
Frozen before this calculation. Conditional, review DEFERRED, gate effect NONE.

## Question and fixed scope

Derive, rather than guess from its defective leading symbol, the finite-rate
lambda=O(1) inner characteristic of G3's double zero-speed scalar branch.
Use G3S's exact full time-dependent canonical G,W matrices, their G3
coefficient/background family and physical p=k/a. Time derivatives have
already been taken at fixed comoving k. Do not import B1's evaluated symbol,
its graph-norm bound or classify positive roots as Jeans growth by fiat.

This is a frozen-event frequency asymptotic of the *full canonical equations*,
not their finite-time evolution, a physical norm theorem, a causal cutoff or
an EFT-admissibility certificate. Require 0<eta<=1,H>0,a,C>0,k!=0 and the
retained S1 auxiliary rank conditions. Do not invert eta=0.

## Calculation and falsifiable checks

1. Form P(lambda,p)=lambda^2 I+lambda G(p)+W(p) from the pinned G3S export.
   Eliminate the rank-one p^4 force block by its Schur complement, retaining
   the denominator terms needed through O(p^0). No growing cross block may
   be dropped. For the remaining coordinates (u,v,r,T,W), scale columns and
   rows by (1/p,1/p,1/p,1/p,1). Verify every prospective divergent coefficient
   cancels before taking the finite limit.
2. Eliminate the four propagating coordinates from that finite limit. Record
   the resulting scalar inner pencil, its lambda degree and coefficient
   rank domain. A nonquadratic, singular or unresolved result is reported,
   not forced into the expected double-root interpretation.
3. Independently compare the truncated Schur expansion with the exact
   rational Schur complement at a regular rational background event. Verify
   their limit at fixed lambda, and reject omission of the fast denominator's
   subleading term. Retain coupling to all three condensate/reservoir fields.
4. Evaluate every stored G3 eta, both background methods and
   t=(0,.5,1,2,3,4). Compare the two derived inner roots with the complete
   12-root canonical pencil at p=(20,40,80,160). Record normalized matching
   errors, residuals and real parts. The 0.05 p=160 reach criterion is a
   diagnostic, not a physical stability pass; do not retune parameters or
   acceptance conditions to meet it.
5. Pin direct and inherited inputs before calculation; record all failed or
   unknown checks. New numbered outputs only, refusal of existing targets,
   and pure byte-identical replay. No older receipt-producing main() calls.

Use the zero-sector [owning report](RES001_R4C1_EQUAL_NEWTON_SCALAR_REPORT_2026-09-30.md)
and preserve B1's [regularity disposition](RES001_R4C1_ZERO_BRANCH_REPORT_2026-09-26.md).
Interpret only the actual coefficients/roots obtained. Absence of a
lambda~p instability cannot rule out other rates without this analysis;
finite O(1) roots cannot by themselves prove a uniform evolution bound.

No observer targets, action changes, pressure insertion, PDF edits, provider
dispatch, commit, push or publication. Inherit R9-MT1-VARIATION/B1/G1/S1/S2/
S3/G2/G3/G3S, with review deferred. Canonical Tests 1–3 HOLD_SUBSTANTIVE,
physics_pass=false, Rule9_cleared=false; K_Q NOT_DERIVED,V NOT_COMPUTED,
MAT-001 BLOCKED, UVIR-003 IN_PROGRESS, Stage4A CLOSED, TOP-X4 unchanged.
