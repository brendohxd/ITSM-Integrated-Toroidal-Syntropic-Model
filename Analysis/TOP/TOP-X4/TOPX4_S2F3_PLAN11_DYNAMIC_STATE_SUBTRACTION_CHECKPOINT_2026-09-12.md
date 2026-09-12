# TOP-X4 X4-S2F3 Plan-11 Dynamic State/Subtraction Checkpoint

**Date:** 2026-09-12  
**Branch:** `recovery/v12-core-architecture`  
**Candidate:** `X4-S2F3`  
**Result:** `FAIL_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT`  
**Checks:** `11/12`  
**Physics pass:** `false`  
**Gate effect:** `NONE`

## Decision

The bounded checkpoint constructed the exact evolving charged-scalar mode
system on the registered A1 background and obtained a well-behaved ultraviolet
fourth-order scalar adiabatic diagnostic. It nevertheless fails its frozen
all-mode positivity requirement: the fourth-order WKB iterate becomes negative
for three preregistered low-momentum branch/mode combinations near the initial
hypersurface. The contract forbids relaxing that requirement after seeing the
result.

The failure does **not** establish a physical tachyon or disprove the parent.
All uniterated scalar frequencies remain real and positive. It establishes the
narrower result that this branchwise fourth-order WKB candidate is not a valid
positive-frequency construction over the complete registered mode/time grid.
The full coupled Hadamard state and stress subtraction therefore remain
unconstructed.

## Exact construction that passed

Writing `A=a^3*b`, `h=rho_dot/rho`, `Theta=3H_a+H_b`, `gamma=Theta/2`, and
`v=sqrt(A)*(sigma,pi)^T`, the unscaled quadratic action was reduced, up to the
declared total derivative, to

`L_2=1/2 v_dot^T v_dot+mu(v_sigma*v_pi_dot-v_pi*v_sigma_dot)-1/2 v^T K v`.

The executable symbolic check gives

- `K_ss=k_n^2+M_sigma^2-gamma^2-gamma_dot`;
- `K_pp=k_n^2-gamma^2-gamma_dot-2h*gamma-h^2-h_dot`;
- `K_sp=mu_dot+2mu*gamma=-2mu*h` after charge conservation;
- `v_ddot+2mu*J*v_dot+(K+mu_dot*J)v=0`, with `J=[[0,-1],[1,0]]`.

Its constant-background limit exactly reproduces the prior charged
amplitude-phase determinant. The omitted-mixing and wrong-charge-law mutations
are rejected. Both registered background integrations complete on a finite,
positive domain and conserve the global charge below the frozen `1e-9` bound.

## Failed preregistered check

The single failed check is
`registered_scalar_frequencies_and_WKB_iterates_are_positive`.

| `k_obs` | `n` | branch | minimum base `omega` | failed iterate | minimum `(W^(4))^2` | time |
|---:|---:|---|---:|---|---:|---:|
| 1 | 0 | charged minus | 0.5535334292462826 | `W^(4)` | -4.095439344137771 | 0.00125 |
| 1 | 0 | chi | 1.212813202206193 | `W^(4)` | -4.207735521640260 | 0 |
| 1 | 1 | charged minus | 0.7975854372899726 | `W^(4)` | -2.1315455444925533 | 0.00125 |

These failures occur despite positive base frequencies. They are consistent
with failure of a local finite-order branchwise adiabatic approximation in the
infrared/initial-boundary region, but that interpretation is not promoted to a
derived physical diagnosis without a coupled transport construction.

## UV and reproducibility evidence

- UV subset: `k_obs>=16`, all registered `n in {0,1,2,4}` and all three scalar branches.
- Maximum `|W^(2)-W^(0)|/W^(0)`: `3.2549481375587173e-4`.
- Maximum `|W^(4)-W^(2)|/W^(2)`: `4.1338354829389994e-6`.
- Every UV branch satisfies the frozen order hierarchy.
- Primary/witness envelope difference: `1.9412678207069711e-7`, below `2e-4`.
- Candidate scalar Wronskian residual is below `1e-12` wherever the iterate is positive.
- Two final executions produced byte-identical JSON with SHA-256
  `5d974893aab0d9c5e75a2aafd34e10e31db78ffe790cf7a3eaf997e388314fc4`.

## State and subtraction boundary

The run declares scalar branchwise order-0/2/4 WKB ingredients and the
decompactified-reference operation
`sum_n F(n/b)-b*integral dp_y F(p_y)`. It performs no stress integral or KK
sum. The following remain `NOT_CONSTRUCTED` or `NOT_DERIVED`:

- normalized transport for the coupled charged-scalar eigenvectors;
- a full Hadamard state for the evolving five-dimensional system;
- neutral Dirac spinor adiabatic states and determinant phase;
- covariant five-dimensional stress subtraction and local counterterm map;
- renormalized stress, self-consistent semiclassical background and physical
  constrained Hessian.

Adiabatic/Hadamard state control in Robertson-Walker settings and adiabatic
regularization with interactions are established methods, but applying them
to this coupled five-dimensional model requires the missing construction, not
just a scalar branch formula. Relevant primary records are Junker,
[`hep-th/9507097`](https://arxiv.org/abs/hep-th/9507097), Ferreiro and Pla,
[`arXiv:2206.08200`](https://arxiv.org/abs/2206.08200), and for Dirac fields,
Hollands, [`gr-qc/9906076`](https://arxiv.org/abs/gr-qc/9906076).

## Artifact integrity

| Artifact | SHA-256 |
|---|---|
| `Theory/Gates/TOP-X4/TOPX4_S2F3_DYNAMIC_STATE_SUBTRACTION_CONTRACT_2026-09-12.md` | `47ec59b4afef3d937bdaa0b2756c6002b5bb771aa0b540eb24a4fddca323ad4f` |
| `Analysis/TOP/TOP-X4/topx4_s2f3_dynamic_state_subtraction_checkpoint.py` | `add2d9e83a66f82dc0991522b045252c1142bf7de2e7074cdb0b1c1047570de9` |
| `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_dynamic_state_subtraction_summary.json` | `5d974893aab0d9c5e75a2aafd34e10e31db78ffe790cf7a3eaf997e388314fc4` |

All seven frozen input sidecars matched in the executable receipt.

## Stop boundary and next admissible step

No renormalized-stress calculation, Hessian, parity/anomaly completion, A4,
Ultra, phenomenology, manuscript revision, publication action or canonical
architecture change is authorized from this result. Rule-9 three-way
independent clearance is unmet; no independent reports were completed for this
checkpoint.

Any retry must be separately preregistered. The scientifically relevant next
design is a normalized coupled charged-scalar transport construction together
with the neutral Dirac adiabatic state. It must state how the initial
hypersurface and low-momentum sector are handled before deriving the covariant
five-dimensional subtraction/counterterm map. The failed all-mode contract
must remain visible as negative evidence.
