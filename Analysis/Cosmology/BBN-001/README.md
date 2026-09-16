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
The preflight finds the dimensionless `t`/`H` trajectory but no physical
photon-temperature history, unit map, early-plenum density, distinct transfer
currents, condensate-number source or `G_eff`. It therefore refuses to infer
any missing quantity. Its JSON receipt and SHA-256 sidecar are written under
`outputs/`; the result remains `physics_pass=false` and
`gate_effect=NONE`.
