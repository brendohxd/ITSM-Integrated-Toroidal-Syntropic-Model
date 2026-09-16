# BBN-001 external network control receipt — 16 September 2026

**Record type:** `ALTERALTERBBN_EXTERNAL_NETWORK_CONTROL`
**Status:** `CONTROL_ONLY`
**Physics pass:** `false`
**Gate effect:** `NONE`
**Publication status:** `NOT_A_PHYSICS_CLAIM`

## Purpose and boundary

An isolated AlterAlterBBN executable was compiled and run against its supplied
standard cosmology history. This establishes that a six-column external BBN
network interface can be exercised locally and that the network responds to a
controlled expansion-history perturbation. It does not supply an ITSM
early-time background or close BBN-001 as a physics gate.

The engine was not copied into the repository. The control records the pinned
source commit, executable hash and input-file hashes in the JSON receipts under
`Analysis/Cosmology/BBN-001/outputs/`.

## Frozen external control

The source commit was `98f086662ae897ffd3386293d80157ba88483a3f`, built with
the repository's explicit C compilation of the seven `src/*.c` translation
units and linked with the system math library. The executable SHA-256 was
`174bd31fe90233eabf1d92fd6133d90358875841d533c171771cc54dfa498d8f`.

The baseline input contained 6,174 rows with columns `t` (s), `T` (MeV),
`dTdt` (MeV²), `Tnu` (MeV), `H` (MeV) and `nb_etaf` (MeV³). The adapter
requires finite values, increasing time, decreasing photon temperature,
negative `dTdt`, and positive `Tnu`, `H` and `nb_etaf`. It rejects malformed
rows before invoking the engine; the five-column negative control returned
exit code 2 and wrote no receipt.

The source audit found that the network evolution calls the time-temperature
derivative, neutrino temperature and baryon-density accessors. The `H` column
is loaded and retained in the input format but is not independently consumed
by the pinned network source. This is a critical interface limitation: an
`H(z)` value alone cannot be treated as an AlterAlterBBN perturbation.

| Control | `Y_He` mass fraction | `D/H` | Receipt SHA-256 |
|---|---:|---:|---|
| baseline | `0.24667665786328` | `2.499761083682913e-05` | `3ad08a8e9ef0d5f3bd2d60aa326960896c66ddd057cd154f7738acbac80ac8d4` |
| `s=0.95` | `0.23764866953416` | `2.260778544772876e-05` | `5ffc4a0a75e90b6ee3572a6d854b31d88267541bf9a1a9380b2e28b2c06777cb` |
| `s=1.05` | `0.2553000186912` | `2.748955076981904e-05` | `a8aa54e01397db965198a8b145128f48ecd424f48b5645b10797698b987fbc7d` |

The scale controls use `t' = t/s`, `dT/dt' = s dT/dt` and `H' = sH`,
preserving the tabulated temperature trajectory under a pure time
reparameterisation. They are sensitivity controls, not a conditional ITSM
background or a fitted `DeltaN` mapping.

## Adjudication

The baseline is close to, but not an independent reproduction of, the bundled
CAMB/PArthENoPE table: the external-network result is a separate rate/network
implementation and its input history is not a frozen ITSM derivation. No
empirical helium likelihood, Planck/DESI covariance, nuclear-rate nuisance
marginalisation or three-way review was performed.

The following remain unchanged:

- `ITSM_mapping = NOT_DERIVED`;
- `external_BBN_likelihood = NOT_IMPLEMENTED`;
- `independent_reproduction = NOT_COMPLETED`;
- `three_way_consensus = NOT_MET`;
- `MAT-001 = BLOCKED`, `K_Q = NOT_DERIVED` and `V = NOT_COMPUTED`; and
- `UVIR-003`, TOP-X4, Rule 9 and publication status are unaffected.

The required next physics inputs remain an action-derived early-plenum
background, distinct `Q^mu`/charge-source treatment, `G_eff(z)`, perturbation
matching, frozen likelihood data and independent review.
