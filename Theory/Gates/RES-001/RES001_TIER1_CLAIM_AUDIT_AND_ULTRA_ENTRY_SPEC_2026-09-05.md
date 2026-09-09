# RES-001 Tier-1 claim audit and Ultra entry specification

**Date:** 2026-09-05  
**Role:** Codex Role C — canonical claim and gate audit  
**Status:** `CURRENT_CONTROLS_QUARANTINED_NO_ROUTE_SELECTED`  
**Physics pass:** `false`  
**Gate effect:** none; RES-001 remains `OPEN_SCAFFOLD_ONLY`  
**Control:** `R0_NO_THROUGHPUT_CONTROL`

## 1. Decision

The current RES package does not demonstrate a paired-rate two-thermal-bath
GKSL model, local detailed balance, the Spohn entropy-production functional, a
microscopic ITSM reservoir Hamiltonian, a covariant reservoir stress tensor,
or an action-derived transfer current `Q_syn^mu`.

The authoritative present result is the later fail-closed route rubric:

```text
NO_ROUTE_SELECTABLE_ON_CURRENT_EVIDENCE
```

R1 is an unselected phenomenological constitutive form, R2 has no declared
reservoir action/interaction, R3 has no topology-to-current mechanism, and R0
is the nested no-throughput control.

## 2. What the code actually demonstrates

### 2.1 `res001_lindblad_master_equation.py`

This is a one-mode truncated oscillator/Kerr GKSL toy with independently
inserted pump and loss rates. It numerically integrates one initial state and
checks trace, occupation and an ad hoc entropy-balance expression.

It does **not**:

- construct matter, plenum or reservoir stress tensors;
- calculate a covariant divergence;
- derive either exchange current;
- derive the jump rates from a system-reservoir Hamiltonian;
- prove complete positivity by checking one density matrix trajectory;
- evaluate a bath-resolved Spohn functional; or
- derive its asserted cosmological `eta` bridge.

Its "3-sector conservation" function defines three constant four-vectors so
their components cancel algebraically. That is bookkeeping, not a Bianchi or
stress-tensor derivation. Its output `physics_pass: true` and statement that it
provides an exact microscopic foundation for a stationary anisotropic
attractor are quarantined.

Its JSON sidecar digest also fails against the current tracked JSON.

### 2.2 `res001_microscopic_hamiltonian_solver.py`

The file now contains an appropriate quarantine notice. The executed model is
a finite-dimensional two-mode **system** Hamiltonian plus inserted GKSL pump
and loss channels. It does not build the displayed reservoir continuum,
spectral density or system-bath couplings `g_q`, and it does not derive a
Markovian generator from them.

The reported `spohn_entropy_production` is a hand-written particle-flux
combination. It is not

\[
-\operatorname{Tr}\{\mathcal L(\rho)
[\ln\rho-\ln\rho_{\rm inv}]\}
\]

or a bath-resolved thermodynamic entropy production. A positive stationary
density matrix establishes positivity of that state, not complete positivity
of an arbitrary dynamical map. The GKSL form with non-negative coefficients
supplies CP by construction within the truncation; the reported eigenvalue
test is not its proof.

The stored JSON and its sidecar match, but cryptographic identity does not
repair the claim mismatch.

### 2.3 `res001_microscopic_lindblad_spohn_solver.py`

This is a single-mode (`N_FOCK=8`) Kerr model despite its "2-mode" label.
It defines `T_SYN=10` but never uses it. The ordinary bath up/down rates use a
chosen Drude spectral function and `T_BATH`; the additional `gamma_syn` is an
inserted unpaired raising channel.

For an interacting Kerr spectrum, one pair of rates evaluated at `omega_0`
and the unsplit operator `a` does not establish frequency-resolved Davies/KMS
detailed balance. The syntropic channel has no paired lowering rate and no KMS
relation to `T_SYN`. The script never computes a Spohn functional, although
its docstring says it does and quotes `sigma_NESS=0.3315`. The output contains
no such quantity.

The tiny Liouvillian residual, Hermiticity, trace and positive stationary-state
eigenvalues are genuine numerical properties of the inserted generator. They
support only a bounded phenomenological steady-state control.

Its JSON sidecar digest fails against the current tracked JSON.

### 2.4 Honest scaffold components

The following remain useful:

- `res001_qsyn_constitutive_inventory.py` separates `Q_mp` from `Q_syn` and
  inventories mutually exclusive R0/R1/R2/R3 routes;
- `res001_r1_constitutive_draft.py` keeps all R1 coefficients free, declares
  its positive-density domain and does not select the route;
- `res001_constitutive_route_evidence_rubric.py` correctly concludes that no
  route is selectable and lists the missing stress, entropy, parameter and
  stability evidence.

These are governance/closure controls, not a reservoir derivation.

## 3. Correct epistemic separation

| Layer | Current evidence | Allowed statement |
|---|---|---|
| Linear-algebra bookkeeping | inserted exchange vectors sum to zero | a declared partition can conserve in total by construction |
| GKSL syntax | non-negative inserted dissipator coefficients | the finite truncation defines a CP semigroup by construction, subject to the declared generator |
| Stationary-state numerics | small residual, unit trace, Hermiticity, positive eigenvalues for stored toy | the chosen phenomenological generator has a numerical stationary state |
| Thermal bath derivation | partial chosen one-bath rates only | no two-bath microscopic or local-detailed-balance claim |
| Spohn/second law | not implemented in the current corrected script | no verified Spohn claim |
| Covariant stress/current | absent | no derived `T_R^munu` or `Q_syn^mu` |
| ITSM map | absent | no syntropic cosmology, anisotropic drive or creation law |

## 4. Why total conservation does not fix `Q_syn^mu`

The identity

\[
\nabla_\mu(T_m^{\mu\nu}+T_p^{\mu\nu}+T_R^{\mu\nu})=0
\]

constrains only the sum. Writing

\[
\nabla_\mu T_p^{\mu\nu}=-Q_{mp}^{\nu}+Q_{syn}^{\nu}
\]

does not determine either constituent current. Infinitely many transfers give
the same total divergence. A specific `Q_syn^mu` must follow from an off-shell
interaction action, a controlled influence functional/open EFT, or a fully
specified constitutive law with its own entropy and stability conditions.

The cancellation coded in the original solver is therefore necessary
bookkeeping after a current is chosen, not a derivation of the current.

## 5. Corrected Ultra entry requirements

The Ultra reservoir plan must remain closed until the system parent emerging
from M2/M3-U1 (or a separately signed surviving parent) fixes its physical
degrees of freedom and stress tensor.

### E0 — prerequisites

1. Freeze the system/plenum parent action, background, physical mode basis and
   stress tensor.
2. Keep `Q_mp` and any condensate-number current distinct from `Q_syn`.
3. State the desired approximation: closed covariant R2 model, Schwinger-Keldysh
   influence functional, or local irreversible constitutive R1 closure.
4. Retain R0 as an exact nested zero-interaction/zero-throughput limit.

### E1 — microscopic/open-EFT declaration

1. Declare reservoir fields or Hilbert variables, their state, Hamiltonian or
   covariant action, and their stress tensor.
2. Declare one interaction with the surviving plenum variables; do not append
   jump operators independently of it.
3. If a master equation is used, derive the spectral densities, Bohr-frequency
   jump operators and rates, with the Born, Markov, secular and truncation
   assumptions stated and tested.
4. For every thermal bath, verify KMS/local detailed balance separately. A
   nonthermal syntropic bath must have an explicit state/correlation function
   and cannot inherit a temperature label.

### E2 — covariance and current derivation

1. Vary one off-shell total action where available to obtain `T_m`, `T_p` and
   `T_R` using one sign convention.
2. Derive `Q_mp` and `Q_syn` from the interacting equations/Ward identities,
   not from a desired background redshift law.
3. Demonstrate the uncoupled GR limit, diffeomorphism identity and the separate
   exchange equations on shell.
4. If the open EFT selects a frame or foliation, declare it and derive the
   energy and momentum projections of `Q_syn^mu`.

### E3 — thermodynamics

1. Compute energy currents from the Hamiltonian/action rather than occupation
   flux alone.
2. For a Davies/GKSL regime, evaluate the actual Spohn functional over a
   declared set of positive initial states and times and separate bath
   contributions.
3. Verify the first-law balance including interaction-energy conventions and
   work terms.
4. For a constitutive R1 route, construct an entropy current and show
   non-negative divergence in its full declared domain.

### E4 — stability and predictivity

1. Derive background fixed points and the complete linear perturbation system,
   including momentum transfer.
2. Test ghosts/gradient instabilities where fields are covariant, positivity,
   causality, secular-approximation validity and runaway pumping.
3. Match every remaining coefficient to microscopic parameters or report it
   free; no `H0`, `13/12`, `a0` or creation rate may be used as an input.
4. Prove the R0 nested limit and compare it with the interacting solution.

## 6. Route dispositions

| Route | Disposition | Exact next missing object |
|---|---|---|
| R0 no throughput | `READY_CONTROL` | none; retain as nested null model |
| R1 constitutive vector | `HOLD_INCOMPLETE_CLOSURE` | covariant entropy current, `T_R` matching, stable causal domain and coefficient origin |
| R2 action/open-EFT reservoir | `HOLD_PENDING_SYSTEM_PARENT_THEN_ULTRA` | `S_R` and `S_int` or an influence functional using the surviving system variables |
| R3 topology-locked throughput | `REJECT_CURRENT_SCOPED_CLASS` | no topology/modulus-to-current mechanism; cycle counting cannot supply one |
| Existing GKSL scripts | `PHENOMENOLOGICAL_STEADY_STATE_CONTROLS_ONLY` | honest paired-bath generator and real Spohn suite if retained as methods controls |

R2 is the only route capable in principle of meeting the full Tier-1 demand
for a derived covariant transfer current, but it is not selected or open for
execution until E0 is satisfied.

## 7. Gate and publication rule

No existing RES script, JSON, checksum or stationary-state residual changes a
physics gate. Any future paper may report a generic open-system methods control
only after its bath count, rates, detailed-balance conditions and entropy
functional match the code exactly. It may not be titled or described as a
microscopic ITSM reservoir derivation without E0–E4 evidence.

