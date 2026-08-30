# MAT-001 remediation R5 microscopic matching decision

**Date:** 2026-08-07

**Scoped status:** `PASS_MAT001_R5_IDENTIFIABILITY_AUDIT_HOLD`

**Matching verdict:** `HOLD_DECLARED_ACTION_UNDERDETERMINES_V`

**Global status unchanged:** MAT-001 `BLOCKED`; UVIR-003 `IN_PROGRESS`;
$V$ `NOT_COMPUTED`; $K_Q$ `NOT_DERIVED`; Stage 4A `CLOSED`

**Namespace:** This post-R1--R4 MAT remediation item is distinct from the
pre-existing UVIR-003 matching route R5, which is the Conditional AQUAL-class
IR anchor. That route fixes neither $K_Q$ nor $V$.

## 1. Question

Do the declared R3 conformal matter action and the Track-A force action fix the
signed, canonically normalized matter residue

\[
 V=\frac{C_m}{\sqrt{K_Q}}\,?
\]

This is an identifiability question, not another repository inventory. The
answer must follow from relations in the declared action, a microscopic
matching calculation, or a live normalized residue. A convenient field
normalization or a phenomenological target is not a derivation.

## 2. Declared effective action class

The relevant terms are

\[
 S_{\rm eff}\supset S_\psi[K_Q,A,\gamma,\ldots]
 +S_m[\Psi_m,A_m(\psi)^2g],
 \qquad
 A_m(\psi)=e^{C_m(\psi-\psi_*)}.
\]

The force time-kinetic term contains $K_Q$, while the conformal matter metric
contains $C_m$. The repository declares no symmetry, Ward identity,
microscopic threshold calculation, or matching equation relating those two
Wilson coefficients. Putting both terms in one effective action is necessary
for a residue calculation, but it does not by itself correlate independent
coefficients.

## 3. Exact normalization identity

For the positive field-chart transformation

\[
 \psi'=s\psi,\qquad s>0,
\]

the coefficients transform as

\[
 K_Q'=\frac{K_Q}{s^2},\qquad
 C_m'=\frac{C_m}{s}.
\]

Therefore

\[
 \frac{C_m'}{\sqrt{K_Q'}}
 =\frac{C_m}{\sqrt{K_Q}}=V.
\]

This proves that $V$ is the appropriate invariant. It does not assign a
value to $V$.

## 4. Identifiability result

Consider the coefficient map

\[
 F:(C_m,K_Q)\mapsto V=\frac{C_m}{\sqrt{K_Q}},
 \qquad K_Q>0,\quad C_m\ne0.
\]

Its Jacobian has rank one. At fixed nonzero $V$, the fibre is
one-dimensional. Explicitly, for every $\kappa>0$,

\[
 K_Q=\kappa,\qquad C_m=V\sqrt{\kappa}
\]

gives the same residue. This fixed-$V$ fibre contains the expected field
normalization redundancy. More importantly, because the declared action adds
no coefficient relation and no measured residue, $V$ itself is free to vary
between these action families. The action form therefore does not identify a
numeric value or bound for $V$.

## 5. Shortcut audit

| Proposed shortcut | Result | Disposition |
|---|---|---|
| Set $K_Q=1$ | Chooses a field normalization but supplies no physical residue | Rejected as matching |
| Set $C_m=C_{\rm IR}$ | Leaves $V=C_{\rm IR}/\sqrt{K_Q}$ dependent on unmatched $K_Q$ | Rejected as Derived closure |
| Fix $C_{\rm obs}$ and $C_{\rm IR}$ | Fixes the positive-branch $C_m=C_{\rm obs}^{2/3}C_{\rm IR}^{1/3}$, but still leaves $V\propto K_Q^{-1/2}$ | Insufficient |
| Use UVIR route R5 | AQUAL-class phenomenology constrains $C_{\rm obs}$, not $K_Q$ or the normalized residue | Conditional only |
| Use the RR2 response identity | Gives the form $g_{\rm can}=-V$, but no live Track-A matter amplitude or normalized pole residue exists | Open |

None closes MAT-001.

## 6. Decision and exact closure input

R5 returns `HOLD_DECLARED_ACTION_UNDERDETERMINES_V`. This is a positive
identifiability result about the present theory boundary, not a claim that no
microscopic completion can predict $V$.

The hold can be lifted only by at least one of:

1. a named microscopic parent action with a calculation of
   $g_\phi/\sqrt{Z_\phi}$;
2. a live on-shell signed matter-to-physical-mode residue in a declared chart;
3. an independently justified coefficient relation together with enough
   physical input to fix or rigorously bound $V$.

Another coefficient search, $C_m=C_{\rm IR}$, $K_Q=1$, an order-one
estimate, or a Conditional AQUAL fit cannot lift the hold.

## 7. Bounded pathway survey

A connected primary-literature search plus independent symbolic checks rejects a minimal shift-symmetric density portal as a standalone static-force route and identifies a scale-compensator/dilaton-superfluid parent as the first candidate capable of correlating normalization and matter coupling through one scale. That candidate changes or mixes the scalar mode content and is therefore advanced only to a bounded parent-action fork, not to matching closure. See [`MAT-001_R5_PATHWAY_SURVEY_2026-08-07.md`](MAT-001_R5_PATHWAY_SURVEY_2026-08-07.md).

## 8. Reproduction and controls

```powershell
python -m py_compile Analysis/MAT/MAT-001/R5_IDENTIFIABILITY/mat001_r5_microscopic_matching_decision.py
python -B Analysis/MAT/MAT-001/R5_IDENTIFIABILITY/mat001_r5_microscopic_matching_decision.py --self-test-mutations
python -B Analysis/MAT/MAT-001/R5_IDENTIFIABILITY/mat001_r5_microscopic_matching_decision.py
```

The mutation suite rejects premature $V$ promotion, an invented
$C_m$--$K_Q$ relation, deletion of the arbitrary-residue family, an
unbacked live-residue claim, and confusion with the UVIR route-R5 namespace.

Expected status:

```text
STATUS: PASS_MAT001_R5_IDENTIFIABILITY_AUDIT_HOLD
MAT-001: BLOCKED
V: NOT_COMPUTED
K_Q: NOT_DERIVED
Stage 4A: CLOSED
```

Current output SHA-256:
`20B6A0BD506755DCFB8933668C8F2DC99B90C8BC4917DF8982BB9F59C0C50F24`.

## 9. Scientific boundary

This scoped PASS establishes that the currently declared action class
underdetermines the normalized matter residue. It does not derive $C_m$,
$K_Q$, $V$, a UV completion, a stability domain, a physical cutoff, or a
MAT/UVIR PASS. Stage 4A remains closed.
