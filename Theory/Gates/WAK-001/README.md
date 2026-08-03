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

## Entry condition for substantive WAK-001 work

The route screen compares two mutually exclusive descriptions:

1. `W` is an internal plenum variable already contained in `T_P^{mu nu}`; or
2. `W` is an independent sector with its own `T_W^{mu nu}` and explicit
   exchange current.

Route II is selected only as the most auditable first calculation. Route I
remains the fallback if the independent field duplicates an existing mode.
No calculation may combine the descriptions.
