# BBN-001 bounded control

This directory contains a software/data control for the bundled CAMB BBN
tables. It is not a canonical ITSM cosmology gate and does not implement an
early-plenum action, `Q^mu`, `G_eff(z)`, or a BBN likelihood.

The control checks:

- all five bundled BBN tables load with the default axis request;
- the PRIMAT 2024 `Ombh2`/`ombh2` spelling difference is handled as a
  case-insensitive schema compatibility rule;
- interpolation gives finite, positive control outputs and preserves the
  `Y_p` nucleon-fraction to `Y_He` mass-fraction conversion;
- a `DeltaN` response sanity check behaves as expected for the standard
  PArthENoPE table; and
- the PRIMAT 2024 helium value is passed through the CAMB bridge.

Run from the repository root:

```powershell
python Analysis/Cosmology/BBN-001/bbn001_control.py
```

The focused unit tests are run from `CAMB_ITSM_Solver`:

```powershell
python -m unittest camb.tests.bbn_test
```

The JSON receipt and its SHA-256 sidecar are generated under `outputs/`.
Repeated runs must be byte-identical in the pinned runtime. A successful run
remains `CONTROL_ONLY`, `physics_pass=false`, and `gate_effect=NONE`.

## Action-derived input contract

The machine-readable prerequisite contract is
`bbn001_action_derived_input_contract.json`. It separates the external
network history (`T_gamma`, `dT_gamma/dt`, `T_nu`, `H` and baryon normalization)
from the ITSM closing inputs (physical units, plenum density, distinct
`Q_mp^mu`/`Q_syn^mu`, `S_N`, `G_eff` and perturbation matching). Field-name
presence is not value, dimensional or provenance validation, and the contract
does not supply any missing value.

Validate the frozen contract and the current preflight receipt with:

```powershell
python Analysis/Cosmology/BBN-001/bbn001_action_derived_input_contract.py
```

The current expected result is
`CONTRACT_VALIDATED_UPSTREAM_PHYSICS_BLOCKED` with `12/12` checks. The
validator confirms the contract hash, the preflight sidecar and the exact
missing-input receipt while retaining `physics_pass=false`,
`gate_effect=NONE` and `NOT_A_PHYSICS_CLAIM`.

## External network control

`bbn001_alteralterbbn_control.py` is an optional adapter for an externally
built AlterAlterBBN executable. It is not vendored, and the executable,
source commit and six-column input files must be supplied explicitly:

```powershell
python Analysis/Cosmology/BBN-001/bbn001_alteralterbbn_control.py `
  --executable <path-to-alteralterbbn> `
  --input-dir <alteralterbbn-io-directory> `
  --source-root <alteralterbbn-source-directory> `
  --label baseline
```

The adapter validates the external schema and abundance output, records input
and executable hashes, and fails closed on malformed input. The pinned
AlterAlterBBN source audit shows that its network uses `dTdt`, `Tnu` and the
baryon-density column; its supplied `H` column is retained but not consumed by
the network evolution. The resulting controls therefore demonstrate external
network reproducibility and expansion sensitivity only.

The 16 September 2026 isolated controls were:

| Control | `Y_He` mass fraction | `D/H` |
|---|---:|---:|
| baseline | `0.24667665786328` | `2.499761083682913e-05` |
| `0.95` expansion scale | `0.23764866953416` | `2.260778544772876e-05` |
| `1.05` expansion scale | `0.2553000186912` | `2.748955076981904e-05` |

Here the scale control reparameterises the external history as
`t' = t / s`, `dT/dt' = s dT/dt` and `H' = s H`; it is not an ITSM ansatz.
These records remain `CONTROL_ONLY`, with no derived early-plenum action,
`Q^mu`, `G_eff(z)`, perturbation matching or likelihood.

## Upstream-interface preflight

`bbn001_upstream_interface_preflight.py` audits the registered UVIR-003
background export against the external-network and ITSM closing-input
contracts:

```powershell
python Analysis/Cosmology/BBN-001/bbn001_upstream_interface_preflight.py
```

The current expected result is `BLOCKED_UPSTREAM_BACKGROUND` (exit code `2`).
The preflight consumes the frozen action-derived contract and finds the
dimensionless `t`/`H` trajectory but no physical photon-temperature history,
photon-temperature derivative, neutrino temperature, baryon history, unit
map, baryon normalization, early-plenum density, distinct transfer currents,
condensate-number source, action-derived `G_eff` or perturbation match. It
therefore refuses to infer any missing quantity. Its JSON contains the
`BBN001_ACTION_DERIVED_MISSING_INPUT_RECEIPT` with 12 blocking fields and
matching aliases, while separately recording that value and provenance
validation were not performed. The JSON receipt and SHA-256 sidecar are
written under `outputs/`; the result remains `physics_pass=false`,
`gate_effect=NONE` and `NOT_A_PHYSICS_CLAIM`.
