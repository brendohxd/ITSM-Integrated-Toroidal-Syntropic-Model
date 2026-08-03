# WAK-001 Stage 2 - bookkeeping route selection

**Date:** 2026-08-03
**Gate status:** Open
**Decision class:** Conditional calculation-route selection
**Physical wake law:** Not yet derived

## Question

Which bookkeeping route gives the first WAK-001 calculation a falsifiable
energy and conservation structure without double-counting the plenum or the
Conditional static AQUAL-class force response?

The candidates are:

1. **Route I:** `W` is an internal non-equilibrium variable whose energy is
   already contained in the plenum stress tensor `T_P^{mu nu}`.
2. **Route II:** `W` is an independent effective sector with `T_W^{mu nu}` and
   an explicit exchange current `I_W^nu`.

These are mutually exclusive descriptions at a fixed level of resolution.

## Existing architecture constraints

The v12 architecture already permits an optional `S_W` in the schematic
action, but does not establish that the sector exists. It also requires:

- complete-system covariant stress-energy conservation;
- a well-posed initial-value problem for any wake variable;
- causal characteristics in the declared physical frame;
- positive or bounded energy accounting;
- a controlled static limit;
- separation of matter-plenum exchange `Q_mp^nu`, reservoir throughput
  `Q_syn^nu`, condensate charge transfer and wake exchange;
- no inference of directional stress from energy throughput alone.

The Stage-1 first-order relaxation template passes only a mathematical screen.
A damped equation is not by itself an action or an energy accounting.

## Route comparison

| Criterion | Route I: internal plenum variable | Route II: independent effective sector |
|---|---|---|
| New propagating degree of freedom | Not necessarily; may be a constitutive moment | Explicit unless later integrated out |
| Stress-energy location | Included in `T_P^{mu nu}` | Separate `T_W^{mu nu}` |
| Exchange bookkeeping | No `I_W^nu`; internal redistribution only | Requires interaction-derived `I_W^nu` with exact cancellation |
| Positive-energy audit | Requires a non-equilibrium free-energy or entropy-current closure | Can begin from a conservative quadratic action and Hamiltonian |
| Dissipation | Natural as effective constitutive physics, but requires entropy production and reservoir accounting | Cannot be inserted into a one-field conservative action; must arise from explicit coupling or coarse graining |
| Risk of double counting | High if a separate wake stress is later added | High if `W` duplicates a plenum mode already present in `Phi`, `U` or `psi` |
| Static AQUAL compatibility | Must show internal memory does not add the same static force twice | Can impose a decoupling or explicitly matched static correction |
| Current microscopic support | No derived constitutive law | No derived independent wake particle/field |

Neither route is presently a derived physical description.

## Decision

Adopt **Route II only as the first Conditional calculation route**, not as a
new ontological commitment.

Reasons:

1. A separate trial action provides the clearest initial Hamiltonian,
   characteristic and stress-tensor audit.
2. Exchange with the plenum can be required to cancel explicitly rather than
   hidden inside an unspecified dissipative closure.
3. The existing architecture already reserves an optional `S_W` slot, so the
   calculation tests a declared possibility rather than silently adding a new
   recovery claim.
4. If the independent field duplicates an existing physical mode, fails to
   decouple, or lacks a parent interaction, the route can be rejected cleanly
   and Route I reconsidered as a coarse-grained constitutive limit.

This selection means only:

> Route II is the most auditable next calculation.

It does not mean that the physical vacuum contains an additional fundamental
wake field.

## Minimal conservative calculation family

On a local preferred-frame patch, the trial quadratic density may be organised
as

```text
L_W = (Z_W/2) (D_U W)^2
      - (Z_W c_W^2/2) h^{mu nu} nabla_mu W nabla_nu W
      - (M_W^2/2) W^2
      + W J_W,

D_U = U^mu nabla_mu.
```

This expression defines a calculation family, not the ITSM wake action.
Necessary local linear conditions include:

```text
Z_W > 0,
0 <= c_W^2 <= 1          relative to the declared matter metric,
M_W^2 >= 0.
```

They are not sufficient for global causality or coupled stability. Variation
with respect to the metric and preferred frame must be retained when deriving
`T_W^{mu nu}` and the full constraint system.

`J_W` is intentionally unmatched. It may not be chosen to reproduce a desired
rotation curve, lensing offset or anisotropic pressure. Candidate sources must
be constructed from declared plenum/reservoir variables and tested for mode
duplication.

## Dissipation boundary

The Stage-1 relaxation coefficient cannot simply be appended to this
conservative action. A physical damping term requires one of:

- an explicit reservoir/bath interaction followed by controlled integration
  of bath modes;
- a Schwinger-Keldysh or equivalent open-system effective action;
- a covariant constitutive closure with a derived entropy current and
  non-negative entropy production.

Until one of those constructions exists, `tau_W` remains a toy relaxation
parameter and no dissipative stress tensor is claimed.

## Required Stage-2 calculations

| ID | Calculation | Required result |
|---|---|---|
| W2.1 | Vary the conservative trial family with respect to `W`, `g_mu_nu` and `U^mu` | Equation, stress tensor and frame response from one declared action |
| W2.2 | Canonical energy on a frozen local background | Positive quadratic Hamiltonian in the declared domain |
| W2.3 | Principal symbol | Hyperbolic characteristics and declared cone relation |
| W2.4 | Source-free and static limits | Decay/propagation separated; no duplicated AQUAL force |
| W2.5 | Mode inventory against `Phi`, `U` and `psi` | HOLD or FAIL if `W` is only a renamed existing mode |
| W2.6 | Interaction bookkeeping | Derive `I_W^nu`; verify the total divergence cancels identically |
| W2.7 | Negative controls | Wrong kinetic sign, acausal `c_W`, tachyonic mass and wrong exchange sign must fail |

W2.6 remains unmatched until a candidate interaction is declared. A free
quadratic pass cannot close Stage 2.

## Route-II fail and fallback criteria

Reject the independent-sector route if any of the following is unavoidable:

- `W` duplicates a propagating or constrained mode already counted in the
  condensate, preferred-frame or force sectors;
- a healthy Hamiltonian and causal characteristic structure cannot coexist;
- exchange conservation requires identifying `I_W^nu` with an unrelated
  current by hand;
- the static limit necessarily double-counts the Conditional AQUAL response;
- damping requires an unmodelled external sink outside the complete declared
  system;
- the only viable source is a target-shaped observational ansatz.

If Route II fails specifically because the wake is not an independent mode,
reopen Route I under a new constitutive subgate. Route I must then derive a
free-energy/entropy functional and cannot reuse the separate `T_W^{mu nu}`.

## Claim firewall after selection

| Statement | Classification |
|---|---|
| Route II is the first WAK-001 calculation route | Conditional methodology decision |
| A positive-energy independent scalar wake exists in ITSM | Not derived |
| The relaxation template follows from the trial action | Not derived |
| A wake modifies the static AQUAL force | Not derived |
| A wake explains galaxy or cluster observations | Not derived |
| Wake stress maintains `13/12` | Not derived; downstream CBR-002 only |

## Next action

Derive the free Route-II quadratic equation, canonical energy and principal
symbol in a fixed local preferred-frame patch. Keep `J_W = 0` for that first
screen. Only after the free mode inventory passes should an interaction source
or dissipative completion be proposed.
