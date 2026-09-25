# Master Programme Test 1 — Covariant Action and Source Vector

**Date:** 2026-09-24  
**Status:** `ACTION_INPUT_INCOMPLETE_HOLD_BEFORE_VARIATION`  
**Programme:** [Master ITSM test programme](../Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md)  
**Gate ownership:** CRA-001 action/sector map and RES-001 route R2; UVIR-003/MAT-001 interfaces remain governed by their owning gates  
**Gate effect:** `NONE`

## 1. Objective

From one fully specified, generally covariant off-shell action, derive the
sector stress tensors, field equations, and exchange currents. Verify the
on-shell conservation identities, the regular zero-coupling limit, and the
declared recovery of GR. This contract does not accept a current inferred only
from the contracted Bianchi identity.

The v12 architecture distinguishes matter--plenum exchange, reservoir
throughput, and condensate-number transfer. Preserve those meanings:

\[
\nabla_\mu T_m^{\mu\nu}=Q_{mp}^{\nu},\qquad
\nabla_\mu T_P^{\mu\nu}=-Q_{mp}^{\nu}+Q_{syn}^{\nu},\qquad
\nabla_\mu T_R^{\mu\nu}=-Q_{syn}^{\nu},
\]

and separately

\[
\dot n+3Hn=S_N.
\]

These are target identities and sign conventions to be tested by variation,
not source equations to impose on the action. `Q_mp`, `Q_syn`, and `S_N` may be
related only if the same action derives that relationship.

## 2. Entry audit and current hold

The present action input does not meet the entry condition:

- `Manuscript/CoreRecovery/sections/02_core_architecture.tex` calls
  `S_complete=S_EH+S_Phi+S_U+S_align+S_psi+S_m+S_R+S_int+S_W` a schematic
  sector inventory and explicitly says it is not a completed microscopic
  action. `S_R` and `S_int` are not specified there as complete Lagrangians.
- `Manuscript/CoreRecovery/sections/04_conservation_exchange.tex` writes the
  three-sector balance identities and gives a candidate conformal matter
  metric. It does not derive the reservoir current from a reservoir action;
  it explicitly says no covariant plenum--matter/reservoir action or map from
  the thermodynamic control to `Q_syn^nu` is available.
- The active dashboard records RES-001 as a phenomenological GKSL control
  without a microscopic ITSM Hamiltonian, covariant reservoir stress, or
  derived `Q^mu`.

Therefore the current disposition is
`ACTION_INPUT_INCOMPLETE_HOLD_BEFORE_VARIATION`. This is an entry hold, not a
failed variation, a no-go theorem, or a physics-gate result. Do not fill the
missing action with a convenient constitutive current.

## 3. Required frozen input

Before variation begins, the owning action record must provide all of the
following in one named version:

1. The full covariant action, including gravity, Plenum fields, physical
   matter, reservoir degrees of freedom, and every interaction that transfers
   stress-energy. Include boundary/Gibbons--Hawking terms where the variational
   problem requires them.
2. All fields, symmetries, constraints, signature, units, coupling constants,
   mass dimensions, admissible field domain, and boundary/initial conditions.
3. A sector split assigning every interaction term to a stress tensor or
   defining an unambiguous shared interaction stress. State the allowed
   improvement/reassignment freedom and test whether the claimed transfer
   current changes under an equivalent split.
4. The exact matter metric and matter variables, including whether matter is
   minimally coupled to `g_munu` or to a specified effective metric.
5. The exact Plenum and reservoir actions. A phenomenological open-system
   closure may be evaluated as such, but it cannot be labelled action-derived.
6. Named interaction parameters whose exact-zero branches and nonzero limits
   can be evaluated without dividing by those parameters.
7. A predeclared operational meaning of the uncoupled GR limit. Vanishing
   exchange alone does not remove independent Plenum/reservoir stress or
   nonminimal gravitational terms.

If no candidate meets this input list, the outcome remains the entry hold and
the next required work is a separate action-selection/completion decision.

## 4. Frozen derivation obligations

Using the action and conventions in Section 3:

1. Vary with respect to the metric and every matter, Plenum, and reservoir
   field. Record the Euler--Lagrange equations and all boundary terms.
2. Define each sector stress tensor from the declared metric variation. For
   definiteness, use
   \(T_{a,\mu\nu}:=-2(\sqrt{-g})^{-1}\delta S_a/\delta g^{\mu\nu}\), where
   the varied variable is the inverse metric, and raise indices with
   \(g^{\mu\nu}\). If instead varying \(g_{\mu\nu}\), state and apply the
   corresponding chain rule. Do not omit interaction contributions.
3. Derive `Q_mp^nu` and `Q_syn^nu` from the varied field equations and
   diffeomorphism Ward identities. Show which field equations are used; do
   not solve for a transfer vector by rearranging total conservation alone.
4. Verify on shell that the sector identities sum to
   \(\nabla_\mu(T_m^{\mu\nu}+T_P^{\mu\nu}+T_R^{\mu\nu})=0\), with the
   recorded signs and all interaction stresses accounted for.
5. Verify that the transfer currents are finite, differentiable, and
   nonsingular on the declared physical domain, including backgrounds where
   the relevant interaction coupling vanishes. Compare the exact-zero branch
   with the limit from nonzero coupling.
6. Take the registered uncoupled limit. Demonstrate the Einstein equations
   reduce to the declared GR control with separately conserved sectors. Claim
   pure GR only if residual Plenum/reservoir stress reduces to a cosmological
   constant or decouples under the preregistered limit.
7. Keep the condensate U(1) charge equation separate. Derive any link between
   `S_N` and stress-energy throughput rather than identifying them by name.
8. Check covariance, sign conventions, index placement, mass dimensions, and
   the dependence of the reported currents on the chosen sector-stress split.

In natural units with coordinates of inverse-mass dimension, report
`[T_a^{mu nu}]=M^4` and `[Q^nu]=M^5`, or derive the equivalent dimensions for
the explicitly declared coordinate/unit chart.

## 5. Pass, hold, and failure criteria

**Pass Test 1 only if** the complete action is frozen; all field and metric
variations are reproducible; sector stresses and transfer currents follow
from those variations; total conservation holds on shell; the currents are
regular at exact zero coupling and in its limit; and the declared uncoupled
GR control is recovered without hidden source terms.

**Remain on hold** if any action sector, interaction allocation, physical
domain, boundary term, or GR-limit definition is missing or ambiguous.

**Fail the declared route** if the varied currents are singular or divergent
on its registered domain, total conservation fails on shell, the zero-coupling
branch disagrees with its limit, or the declared GR control cannot be
recovered. A failure applies to that frozen route, not automatically to every
ITSM action.

## 6. Evidence and review package

The eventual execution package must contain:

- the frozen action and provenance for every operator;
- a term-by-term variation ledger and independent symbolic derivation;
- a sector-stress allocation table and explicit Ward identities;
- exact-zero and small-nonzero coupling controls;
- dimensional, sign, and boundary checks;
- negative tests for Bianchi-only current assignment, omitted interaction
  stress, singular coupling division, and conflation of `Q_mp`, `Q_syn`, and
  `S_N`;
- a machine-readable receipt and hashes after the action has been frozen; and
- Rule-9 independent mathematical, numerical/provenance, and claim-hygiene
  review before any parent-gate decision.

The present contract is not the execution package. No variation or numerical
current calculation is reported as complete.

## 7. Scope firewall

This gate does not derive the weak-field force law, fix `C_proj=2/3`, derive
`C_chi`, compute `K_Q` or `V`, close UVIR-003, reopen Stage 4A, or pass MAT-001.
Those remain later programme tests with their existing owning contracts.

Binding current fields remain:

```text
test_01_action_input_complete=false
test_01_status=ACTION_INPUT_INCOMPLETE_HOLD_BEFORE_VARIATION
source_vector_derived=false
Q_mp_derived=false
Q_syn_derived=false
S_N_identified_with_Q_syn=false
UVIR-003=IN_PROGRESS
MAT-001=BLOCKED
K_Q=NOT_DERIVED
V=NOT_COMPUTED
Stage4A=CLOSED
physics_pass=false
gate_effect=NONE
```
