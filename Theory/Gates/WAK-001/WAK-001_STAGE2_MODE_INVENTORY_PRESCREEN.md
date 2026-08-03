# WAK-001 Stage 2 - finite-q mode-inventory pre-screen

**Date:** 2026-08-03
**Calculation status:** `PASS_WAK001_W2_5_MODE_COUNTING_PRESCREEN`
**W2.5 status:** Hold pending a coupled parent action
**Gate status:** Open
**Physics pass:** `false`
**Physical wake law:** Not yet derived

## Question

What does the Route-II trial field add to the declared finite-`q` scalar mode
inventory, and which algebraic outcomes would mean independence, constraint
redundancy or a ghost?

## Existing finite-q inventory

The current recovery architecture declares the gauge-regular scalar basis

```text
(Xi, Q_rho, Q_chi)
```

for the `g+U+Phi+alignment` block, with three positive kinetic directions in
the stated finite-`q` domain. The Track-A force mode `Pi` is factorized at
quadratic order. The pre-screen therefore labels the existing finite-`q`
canonical inventory as

```text
(Xi, Q_rho, Q_chi, Pi).
```

This is a mode-counting interface, not a claim that the full UVIR-003 coupled
stability or amplitude gate has passed. At exactly homogeneous momentum, `Xi`
is excluded as gauge and the counting must be redone in that separate domain.

## Three mutually exclusive interpretations

### A. Decoupled independent `W`

For an existing positive kinetic block $K_{\mathrm{old}}$, the source-free direct
sum is

\[
K_{\rm full}=K_{\rm old}\oplus Z_W.
\]

If $Z_W>0$, its determinant factorizes and its rank rises by one. The trial
action therefore adds one positive canonical pair **by construction**.

### B. Mixed independent `W`

For kinetic mixing vector $b$, positivity requires the Schur complement

\[
Z_{\rm eff}=Z_W-b^T K_{\rm old}^{-1}b>0.
\]

`Z_eff = 0` produces rank loss; `Z_eff < 0` produces one negative kinetic
direction in the tested block. A coupled calculation must evaluate this
quantity after the lapse, shift and unit-frame constraint are handled.

### C. Identified `W`

If a microscopic relation instead sets

\[
W=a_i q_{\rm old}^i,
\]

the map from the four existing coordinates to `(q_old,W)` still has rank four.
No new canonical pair exists. Retaining both the identified field and a
separate wake stress would double count the same mode.

These interpretations cannot be combined at one resolution scale.

## Executable pre-screen

Run:

```powershell
python Analysis\WAK\WAK-001\wak001_route2_mode_inventory_prescreen.py
```

The audit checks direct-sum determinant/rank/inertia, a healthy small-mixing
case, rank-loss and ghost negative controls, the zero-kinetic control and the
identified-field Jacobian rank. Ten checks pass. Two independent outputs match
at SHA-256
`673CB9B8183D070830FEF51F0746FA277816A772987D83E93A049579399508E8`.

Expected footer:

```text
STATUS: PASS_WAK001_W2_5_MODE_COUNTING_PRESCREEN
MODE INDEPENDENCE: NOT_YET_ESTABLISHED
HOLD: HOLD_MICROSCOPIC_MODE_IDENTITY_AND_COUPLED_MIXING
Physical wake law: NOT_YET_DERIVED
```

## Result

The algebraic classification passes. Because `J_W=0`, no mixing vector,
microscopic identification map or parent constraint allocation has been
declared, the present Route-II family adds `W` as a fifth finite-`q` scalar
pair by assumption. That is not evidence that a distinct physical wake mode
exists.

Record:

`HOLD_MICROSCOPIC_MODE_IDENTITY_AND_COUPLED_MIXING`.

## Next calculation

Supply one coupled quadratic parent action containing the current
`g+U+Phi+alignment+psi` block and the candidate `W` block. Eliminate its
constraints and compare the finite-`q` Hessian rank/inertia before and after
adding `W`. Reject Route II if the candidate is an identified combination,
causes rank loss or introduces a ghost. Keep `J_W=0`; interaction and exchange
remain unopened.
