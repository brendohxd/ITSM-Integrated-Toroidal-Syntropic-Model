# TOP-X4 `X4-S2F3` Dirac/parity/anomaly readiness receipt

**Executed:** 2026-09-16  
**Checkpoint status:** `HOLD_TOPX4_DIRAC_PARITY_ANOMALY_INPUTS_NOT_CLOSED`  
**Readiness checks:** `10/10`  
**Dirac completion:** `NOT_DERIVED`  
**Dirac Hadamard state:** `NOT_CONSTRUCTED`  
**Parity-odd determinant phase:** `NOT_DERIVED`  
**Anomaly cancellation:** `NOT_DERIVED`  
**Counterterm quantization:** `NOT_FIXED`  
**Physics pass:** `false`  
**Gate effect:** `NONE`

## 1. Binding result

This single-gate audit passes its bookkeeping and deterministic rejection
checks, but it confirms that the fermionic/parity-odd completion boundary is
still open. The existing static result is a zero-density parity-even
determinant control. The existing Dirac result is a finite-order first-order
projector with exact unitary transport. Neither is promoted to a complete
curved five-dimensional determinant or Hadamard state.

The audit also confirms that no parity-odd phase, anomaly cancellation,
quantized counterterm normalization, state-dependent finite-charge determinant
or curved gravity/ghost coupling is available for the physical backreaction
calculation.

## 2. Registered evidence and open inputs

| Evidence | Recorded scope | Binding limitation |
|---|---|---|
| Static determinant | `PASS_STATIC_PARITY_EVEN_DETERMINANT_HOLD_PARITY_ODD_AND_FINITE_CHARGE` | Parity-even, zero-density, static only |
| Finite-charge operator | `PASS_FINITE_CHARGE_OPERATOR_HOLD_DYNAMIC_STATE_STRESS_AND_HESSIAN` | Constant-background scalar variation only |
| Exact transport retry | `PASS_EXACT_SCALAR_DIRAC_TRANSPORT_HOLD_HADAMARD_STRESS_AND_HESSIAN` | First-order Dirac transport; `full_Hadamard_state=false` |
| D5 readiness | `PASS_5D_HADAMARD_COUNTERTERM_SCAFFOLD_HOLD_FULL_OPERATORS_STATE_AND_STRESS` | Universal scaffold; model-specific Dirac/parity data incomplete |
| Global scalar state | `PASS_GLOBAL_SCALAR_MATRIX_HADAMARD_STATE_HOLD_DIRAC_STRESS_AND_HESSIAN` | Scalar state only; no spinor/anomaly closure |
| Physical-Hessian readiness | `HOLD_PHYSICAL_HESSIAN_INPUTS_NOT_CLOSED` | Gravity/ghost/parity inputs remain unavailable |

The missing inputs are recorded explicitly as:

1. a complete curved five-dimensional Dirac operator with vielbein, spin
   connection, Clifford convention and finite-charge normalization;
2. a dimension-appropriate infinite-order Dirac Hadamard/pseudodifferential
   two-point construction with positivity and wavefront control;
3. the state-dependent finite-charge determinant and regulator definition;
4. a parity-odd determinant phase with reference/regulator, spin-structure and
   spectral-flow or equivalent global data;
5. local and global anomaly data for the frozen field content and allowed
   transformations; and
6. the complete quantized parity-odd counterterm basis and normalization.

## 3. Rejection receipts

All six registered shortcut attempts were rejected:

| ID | Attempt | Result |
|---|---|---|
| `TOPX4-DPA-R1` | Static parity-even determinant substituted for the finite-charge fermion action | `REJECTED` |
| `TOPX4-DPA-R2` | First-order Dirac projector called an infinite-order Hadamard state | `REJECTED` |
| `TOPX4-DPA-R3` | Squared Dirac operator used as parity-odd phase/anomaly clearance | `REJECTED` |
| `TOPX4-DPA-R4` | Unproved even-/four-dimensional structure called the repository-specific D5 result | `REJECTED` |
| `TOPX4-DPA-R5` | Missing anomaly/counterterm contributions set to zero | `REJECTED` |
| `TOPX4-DPA-R6` | Observational target used to select fermionic closure | `REJECTED` |

## 4. Status firewall

This receipt does not change `MAT-001=BLOCKED`, `K_Q=NOT_DERIVED`,
`V=NOT_COMPUTED`, `UVIR-003=IN_PROGRESS`, BBN-001's upstream-background hold,
`physics_pass=false`, Rule-9 clearance, A4/Ultra entry or publication status.
No new determinant, stress tensor, physical Hessian, cosmology result or
publication claim follows.

## 5. Reproducibility hashes

| Artifact | SHA-256 |
|---|---|
| `topx4_s2f3_dirac_parity_anomaly_readiness.py` | `93f0d1fcbd1e306f0614179f44b52ec978c93ea9f49060032eb744911257dfa6` |
| `topx4_s2f3_dirac_parity_anomaly_readiness_summary.json` | `a87901a070b0d9d81aaea599c6075bc06a6900da8df2a4d4d73ee5e60749d4a9` |
| `TOPX4_S2F3_DIRAC_PARITY_ANOMALY_READINESS_CONTRACT_2026-09-16.md` | `d49da5217c1078467424af3210c4f983db2f9d73195185b486bab9628c8a14f8` |
| `PLAN.md` | `a935fbb4b2cc2206ed7a22910716203e427071e21d347214b59fea62bdc9c73f` |
| `TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md` | `37205506697e1f70f12b9ea3d8b093ccbccf11bbf0c19b680d00a43f28c6f945` |

The executable and JSON output each have matching `.sha256` sidecars. This
receipt is local evidence preparation only; it is not an independent Rule-9
review report.
