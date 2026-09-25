# Tests 1–3: bounded derivation and identifiability audit

Date: 2026-09-24. Status: preregistered local calculation; independent review pending.
Owner: Master ITSM programme Tests 1, 2, 3. Gate effect: NONE.

## Scope and sequence

Execute `--test 1`, inspect its result, then `--test 2`, then `--test 3`.
Test 1's complete-action entry hold remains binding. The calculations below
vary the already-declared conformal matter module and an explicitly separate
counterexample action. They do not supply an accepted ITSM reservoir parent.
Tests 2 and 3 audit conditional formulas and identifiability; they cannot
inherit a physical prediction from these limited Test 1 results.

### Test 1

Use signature (-+++), c=hbar=1, and
`T_munu=-2/sqrt(-g) delta S/delta g^munu`. The existing candidate matter metric
is `g_tilde=A(psi)^2 g`, `A=exp(beta psi)`, `beta=C_m` in this unit chart.
Derive its source, Ward identity and dust acceleration. Verify the source
sign independently by varying a canonical matter scalar in this metric.

To establish what the incomplete reservoir inventory does and does not fix,
use the following **nonuniqueness witness**, not a proposed replacement parent:

```
S = integral sqrt(-g) [Mpl^2 R/2 + L_P + L_R + L_m]
L_P = -1/2[(grad u)^2+(grad v)^2+Z(grad psi)^2] - V_P - W
L_R = -1/2(grad r)^2 - V_R
L_m = -A^2/2 (grad chi)^2 - A^4 V_m
s = u^2+v^2; Phi=(u+i v)/sqrt(2)
V_P = m_P^2 s/2 + lambda_P s^2/4
V_R = m_R^2 r^2/2 + lambda_R r^4/4
V_m = m_m^2 chi^2/2
W = lambda s r^2/4
```

Take Z>0, nonnegative squared masses and quartic couplings, real finite
fields, finite beta, and positive finite A. Fields can live on periodic T3;
metric variations have compact support in time or the appropriate Einstein
boundary term. The gravitational term has the usual GR metric variation.
The witness's canonical psi kinetic term is explicitly different from the
unmatched Track-A force action. No background, quantum reservoir, irreversible
thermodynamics, finite-density stability or new ITSM parent is asserted.

Derive all witness scalar equations, sector stresses and exchange identities.
Allocate W to P initially; then move a constant fraction eta of W to R and
derive the current's transformation. Check exact-zero beta/lambda branches
without dividing by either coupling; distinguish zero transfer from removal
of independently conserved stress. Verify U(1) charge conservation although
energy transfer can be nonzero. Use off-shell flat-chart jets plus independent
homogeneous FLRW continuity checks; the report must supply the covariant Ward
derivation and must not describe the jet calculation as a gravity solve.

### Test 2

Use exactly the conditional action in
`Manuscript/CoreRecovery/sections/05_weak_field.tex`, with positive
`C_m,C_IR,a0,G`. Vary its Newtonian and cubic-gradient terms; derive the
Euler force using the same conformal matter coupling; integrate the spherical
flux with a regular-origin condition and specified enclosed mass. Record
the weak, slow, quasistatic, symmetry and compensation assumptions explicitly.

Check the pointwise algebraic prescription on the nonspherical local
potential `Phi_N=(x^2+2 y^2)/2`: a nonzero curl rejects it as a general scalar
gradient. This is a local integrability counterexample, not a periodic galaxy
solution. Retain the torus zero-mean source condition and distinguish a local
compensated patch from an isolated global torus solution.

### Test 3

Freeze these coefficient branches before any new data comparison:
`1`, `2*pi`, `1/(2*pi)`, `sqrt(1-q_dec)/(2*pi)`, and an action-derived
result if one exists. No target acceleration, H0 measurement or fit is read
by the symbolic calculation. The analyst has already seen historical target
values; this is a data-independent calculation, not a claim of fresh analyst
blinding. The independent result is absent until an action supplies it.

Audit both field rescaling and the reference-scale reparameterization
`a0 -> ell*a0, C_IR -> ell*C_IR`, ell>0. Determine the invariant measured
by the static force and whether this action alone identifies C_chi.
Derive conditional redshift propagation for the frozen branches and compare
fixed-comoving, fixed-physical and Hubble-linked length assumptions.
Historical provenance coverage must be reported separately from derivation;
unread original PDFs cannot be claimed reconstructed by a text scan.

## Validation and stop rules

Each calculation must expose its symbolic residuals and counterexamples.
Reject a reversed matter-current sign, omitted interaction stress, identification
of charge transfer with energy transfer, a universal curl-free algebraic law,
or invariance of C_chi under a reference-scale relabeling. Report dimensions.
Hash the contract, executable and generated receipts. Any failed mathematical
identity stops the dependent calculation for diagnosis; never edit a criterion
to make a failed calculation appear successful.

All parent statuses remain: MAT-001 BLOCKED, UVIR-003 IN_PROGRESS,
K_Q NOT_DERIVED, V NOT_COMPUTED, Stage4A CLOSED, physics_pass=false,
gate_effect=NONE. Rule-9 review is NOT_COMPLETED. A completed local audit
does not complete Tests 1–3 as physical derivations of canonical ITSM.
