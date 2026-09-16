# TOP-X4 `X4-S2F3` Plan-11 theorem-backed global scalar-state receipt

**Executed:** 2026-09-16
**Checkpoint status:** `PASS_GLOBAL_SCALAR_MATRIX_HADAMARD_STATE_HOLD_DIRAC_STRESS_AND_HESSIAN`
**Route:** `ROUTE_A_PSEUDODIFFERENTIAL_PROJECTION_THEOREM_BACKED`
**Physics pass:** `false`
**Gate effect:** `NONE`
**Rule-9:** `THREE_WAY_CLEARANCE_NOT_MET`

## 1. Binding result

The theorem-backed Route-A scalar-state construction passes `10/10` registered
checks. It applies the pseudodifferential Hadamard-state construction to the
registered smooth rank-three normally hyperbolic operator on the
`T^3_obs x S^1_y` Cauchy surface. The construction defines the positive and
negative frequency data from the arbitrary-order formal matrix symbol, uses a
Borel realization with smoothing remainder, patches the finite low modes with
positive Cauchy data, and evolves the coupled data exactly.

The checkpoint verifies:

- smooth positive scale factors and the Lorentzian normally hyperbolic
  principal symbol;
- a symmetric rank-three matrix potential with nonzero off-diagonal coupling;
- finite transpose-symmetric formal coefficients through orders `0`--`8`;
- positive finite-rank low-mode data;
- exact full rank-three Cauchy transport in all three registered directions;
- constant orthogonal bundle-basis covariance;
- the pure-gauge phase-aligned connection with its `2*mu` derivative mixing;
- agreement with the corrected `E=-H` and local `U_0`--`U_2` parametrix; and
- all ten preregistered rejecting mutations.

The strongest numerical full-matrix transport residuals are:

| Quantity | Maximum |
|---|---:|
| Symplectic residual | `1.90290818327174e-09` |
| Mode-normalization residual | `1.345559256036763e-09` |
| Isotropy residual | `3.8886326451286825e-17` |
| Basis-covariance residual | `8.401224619530195e-10` |

The registered zero-mode controls remain positive, with minimum Hamiltonian
eigenvalue `0.18686244398906132` and minimum `K` eigenvalue
`0.3888184154041395`.

## 2. Execution

Command:

```powershell
python Analysis\TOP\TOP-X4\topx4_s2f3_global_state_construction.py
```

Recorded output:

```text
PASS_GLOBAL_SCALAR_MATRIX_HADAMARD_STATE_HOLD_DIRAC_STRESS_AND_HESSIAN
checks=10/10
route=ROUTE_A_PSEUDODIFFERENTIAL_PROJECTION_THEOREM_BACKED
global_scalar_matrix_hadamard_state=THEOREM_BACKED_CONSTRUCTED
physics_pass=false
gate_effect=NONE
sha256=fef8df00183333cc6fb18382c77fab397cd7c2caf740752d6c29ebf36da44428
```

The JSON receipt is
`Analysis/TOP/TOP-X4/outputs/topx4_s2f3_global_state_construction_summary.json`.

## 3. Mathematical boundary

The Borel/smoothing step is a theorem-backed realization of the formal
all-order symbol; it is not a finite-order convergence claim and the JSON
file is not itself a wavefront object. Exact Cauchy evolution gives the
coupled bisolution from the realized data, while the pseudodifferential
construction supplies the Hadamard wavefront and positivity argument. The
finite-grid matrix transport is retained as a numerical consistency witness,
not as the microlocal proof.

The primary formal basis is the Gerard--Wrochna pseudodifferential
construction, with the vector-bundle microlocal scope recorded in the frozen
global-state contract. The receipt is therefore a mathematical scalar-state
construction checkpoint, not independent peer review of the repository
calculation.

## 4. Non-promotion boundary

The following remain closed or uncomputed:

- Dirac, graviton, ghost and parity/anomaly states;
- counterterm normalizations, determinant and renormalized stress;
- physical Hessian, radion stabilization, A4 and Ultra entry;
- `MAT-001`, `UVIR-003`, cosmological/BBN mapping and all downstream fits;
- Rule-9 independent three-way consensus; and
- publication or any `physics_pass` claim.

In particular, this state construction does not supply an action-derived BBN
background, `Q^mu`, `S_N` or `G_eff`; the BBN upstream-interface hold remains
binding.

## 5. Artifact hashes

| Artifact | SHA-256 |
|---|---|
| `topx4_s2f3_global_state_construction.py` | `7c33661479253abd79f13d386f44b8c840b18ec9e0d6dab77c92e03673621de3` |
| `topx4_s2f3_global_state_construction_summary.json` | `fef8df00183333cc6fb18382c77fab397cd7c2caf740752d6c29ebf36da44428` |
| `TOPX4_S2F3_GLOBAL_STATE_CONSTRUCTION_CONTRACT_2026-09-16.md` | `76309ff209d4aa5d69d8d510f7d1832fbfecdebfacecf30505f05b0c1252606a` |
| `PLAN.md` | `a935fbb4b2cc2206ed7a22910716203e427071e21d347214b59fea62bdc9c73f` |
| `topx4_s2f3_global_state_construction_preflight_summary.json` | `2685f5c7c0fcdf9f036e7660efd11b3509b5611f49b5cf243614d6b78fa1518c` |
| `topx4_s2f3_adiabatic_symbol_diagnostic_summary.json` | `80eed52925e24b477e41066d7835ece420c5fa4da2e0c9ab21259cd2010b2d86` |
| `topx4_s2f3_covariant_scalar_matrix_summary.json` | `c7f9b3e9d4f00c99df93f25b8d9eccf9162472fc3c66ee26fe19c43f389dd777` |
| `topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json` | `becaa3ef1ce19a8545335c49b868cc3479fcf1a7b4044ac1cda7f939fbfadc08` |
