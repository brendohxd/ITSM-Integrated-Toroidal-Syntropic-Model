# WAK-001 - Causal wake and memory gate

**Gate status:** Open
**Identity status:** Keep
**Current result:** No ITSM wake constitutive law has been derived.

WAK-001 tests whether the historical plenum-wake idea can be represented by a
causal, stable, energy-accounted response with a controlled static limit. It
does not assume that a wake exists merely because the vacuum is modelled as a
finite-density condensate.

The owning specification is
[`WAK-001_GATE_SPEC.md`](WAK-001_GATE_SPEC.md). The first executable object is
the deliberately minimal relaxation-template audit at
`Analysis/WAK/WAK-001/wak001_relaxation_template.py`.

Stage 2 selects Route II only as the first Conditional calculation route in
[`WAK-001_STAGE2_BOOKKEEPING_ROUTE.md`](WAK-001_STAGE2_BOOKKEEPING_ROUTE.md).
Its source-free template screen is recorded in
[`WAK-001_STAGE2_FREE_FIELD_SCREEN.md`](WAK-001_STAGE2_FREE_FIELD_SCREEN.md).
The local constrained field, metric and frame identities are recorded in
[`WAK-001_STAGE2_ACTION_VARIATION.md`](WAK-001_STAGE2_ACTION_VARIATION.md).
The finite-`q` mode-counting alternatives are recorded in
[`WAK-001_STAGE2_MODE_INVENTORY_PRESCREEN.md`](WAK-001_STAGE2_MODE_INVENTORY_PRESCREEN.md).
The cross-sector input contract and fail-closed stop are recorded in
[`WAK-001_STAGE2_COUPLED_HESSIAN_READINESS.md`](WAK-001_STAGE2_COUPLED_HESSIAN_READINESS.md).
The background-specific quadratic factorization is recorded in
[`WAK-001_STAGE2_ZERO_BACKGROUND_FACTORIZATION.md`](WAK-001_STAGE2_ZERO_BACKGROUND_FACTORIZATION.md).
The canonical microscopic-identity evidence inventory is recorded in
[`WAK-001_STAGE2_MICROSCOPIC_IDENTITY_INVENTORY.md`](WAK-001_STAGE2_MICROSCOPIC_IDENTITY_INVENTORY.md).
The common C1/C2/C3 comparison rubric and fail-closed no-selection decision are
recorded in
[WAK-001_STAGE2_IDENTITY_ROUTE_EVIDENCE_RUBRIC.md](WAK-001_STAGE2_IDENTITY_ROUTE_EVIDENCE_RUBRIC.md).

## Governing boundary

- The AQUAL-class force law remains the Conditional static IR baseline.
- A wake is an additional non-equilibrium or retarded sector, not a new name
  for the instantaneous force scalar.
- `Q_mp^nu`, `Q_syn^nu`, condensate charge transfer and wake exchange are
  distinct until an interaction action relates them.
- A numerical fit, lensing offset or Bullet Cluster explanation cannot be
  claimed before the matter vertex, physical metric and wake stress tensor
  have been derived.

## Current executable scope

The relaxation script validates only the mathematical properties of

```text
tau_W (partial_t + v_W partial_x) W + W = kappa_W S.
```

This is a constitutive template, not an adopted ITSM equation. Passing its
checks demonstrates that a causal decaying memory model is possible in
principle; it does not select `tau_W`, `v_W`, `kappa_W`, the source `S`, or the
observable coupled to `W`.

The conservative Route-II screen and W2.1 symbolic audit additionally verify
the free Hamiltonian and the local constrained variation identities. A generic
spatial `W` gradient sources the shared `U^mu` equation. The W2.5 pre-screen
then classifies the direct-sum, mixed and identified-field alternatives, but
cannot establish microscopic independence without one coupled parent action.
The readiness audit confirms that the prior reduced pieces did not declare
`W` cross-sector or constraint blocks, so a block-diagonal graft could not be
assumed. The subsequent zero-background audit derives factorization of the
W-dependent quadratic density specifically for `Wbar=0`, `nabla Wbar=0`,
`J_W=0` and no explicit bilinear interaction. Metric and frame coupling
returns at cubic order. The evidence inventory finds no canonical
identification map or independent microscopic derivation. The shared evidence
rubric therefore selects no route: C2 is the most developed calculation
scaffold only, while C1/C2/C3 remain Open. Stage 2 remains in progress under
the microscopic-identity and cubic-constraint holds.

## Entry condition for substantive WAK-001 work

The route screen compares two mutually exclusive descriptions:

1. `W` is an internal plenum variable already contained in `T_P^{mu nu}`; or
2. `W` is an independent sector with its own `T_W^{mu nu}` and explicit
   exchange current.

Route II is selected only as the most auditable first calculation. Route I
remains the fallback if the independent field duplicates an existing mode.
No calculation may combine the descriptions.
