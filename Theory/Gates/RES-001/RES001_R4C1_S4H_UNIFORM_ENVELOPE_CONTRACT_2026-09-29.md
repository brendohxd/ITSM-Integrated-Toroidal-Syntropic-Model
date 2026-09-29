# R4C1-S4H-U: explicit uniform formal-energy envelope contract

Date: 2026-09-29. Owner: conditional Master Test 1, registered R4C1-v1/B1.
This is a continuation of the unchanged S4H contract, not a replacement
for its earlier attempts. Freeze this contract before computing an interval
envelope. Rule-9 review is deferred, not cleared.

## Inputs, interval and domain

Use the pinned S4H moving-symbol sources and receipts and the B1G exact
homogeneous regularity report. Do not rerun an earlier receipt-writing
main or change the R4C1 action, B1 initial data, graph, chart or
normalization. The time interval is exactly [0,4]. The formal torus mode
has fixed comoving k=2*pi*|n| and p=k/a. Work only on the registered
regular B1 trajectory, nonzero modes and p>=1. A physical EFT cutoff is
not known; the formal p->infinity limit does not establish physical mode
admissibility.

Derive a rational enclosing box from B1G rather than CSV samples.
The proposed conservative box is H in [10^-5,1], s=u^2+v^2 in
[10^-12,5], |u|,|v|,|u_dot|,|v_dot|,|r_dot|<=3, |r|<=2,
|psi_dot|<=2, 10^-9<=rho_m<=3, 1<=a<=60 and 1/60<=C<=60.
The proof must use E0=3469/1400, H0<1, sqrt(2E0)<3,
sqrt(2E0/3)<2, the exact dust/charge integrals, and a justified
rational upper bound e<11/4; verify the required integer-power
inequalities without float roundoff. If this box cannot be proved,
reject this route.

## Required calculation

1. Verify exact source hashes and sidecars. Reconstruct the unchanged
   moving C(t,p), C2, C1, M0 and M1. Recheck both formal p^2 and p
   energy cancellations, including the complete moving-chart and
   fixed-comoving-k flow terms.
2. For each nonzero entry of M0, M1, C1, their B1-flow derivatives
   M0dot/M1dot, and R=C-p^2 C2-p C1, obtain a **certified explicit**
   coefficient-sum bound on the rational box. Normalize the numerator
   as a polynomial in the registered state variables and p; bound
   every coefficient by an exact algebraic ceiling, not a rounded
   decimal. Factor the denominator and prove a positive lower bound
   using only certified factors. For R, require numerator p-degree no
   greater than the p-degree supplied by denominator factors p and
   p^2+S, with S=396H^2+18psi_dot^2+
   6(r_dot^2+u_dot^2+v_dot^2)>=0. Reject any unrecognized factor,
   free symbol, denominator sign or degree, or unevaluated coefficient.
3. Convert entry bounds to explicit Frobenius constants B0, B1, BC1,
   BR, Bd0, Bd1. Use M0>=I/4 and p0=max(1,8 B1) to establish
   I/8<=M0+M1/p<=(B0+B1/p0)I for all t in [0,4], p>=p0.
   From the exact cancellation identity bound the symmetric
   energy-rate matrix by

       BE = 2 B0 BR + 2 B1 BC1 + Bd0
            + (2 B1 BR + Bd1 + B1)/p0.

   Then d(z^T M z)/dt <= 8 BE (z^T M z) on that formal domain.
   A fixed comoving mode requires k>=60 p0 to keep p>=p0
   under the conservative a<=60 bound. Report the resulting
   integer/power-of-ten constants even if they are enormous.
4. Independently check each denominator classification and exact
   degree condition. A finite sample, a statement that a supremum
   exists by compactness, or a numerical maximum does **not** satisfy
   this explicit-constant obligation. Preserve any failed attempt in
   a fresh non-overwriting output location.

## Interpretation and stop rules

A successful envelope would prove only a formal finite-time estimate
for this reduced regular B1 nonzero-mode graph on its explicitly
declared high-p domain. It would not establish that any of those modes
lie below a physical EFT cutoff, nor the full constrained initial-value
problem, singular/zero modes, all-sector stability, healthy GR recovery,
canonical action acceptance, weak-field closure, coefficient matching
or any observational prediction.

Keep physics_pass=false, gate_effect=NONE, Rule9_cleared=false and
review_status=DEFERRED. Master Tests 1-3, MAT-001, UVIR-003, Stage 4A,
Derived and publication statuses remain unchanged. If any required
inequality or factorization cannot be certified, report INCOMPLETE or
REJECTED_FOR_THIS_ENVELOPE with the exact failed condition, not a pass.
