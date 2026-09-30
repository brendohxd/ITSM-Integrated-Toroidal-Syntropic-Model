# R4C1-S2b: finite-positive-`b` scalar transfer on the unit-period B1 torus

Date: 2026-09-30. Owner: conditional R4C1-v1 / Master Tests 1 and 2.
Status: `FINITE_B_LINEAR_TRANSFER_VALIDATED_ONLY`; `physics_pass=false`,
`gate_effect=NONE`, `Rule9_cleared=false`, review `DEFERRED`.

## Decision

The two positive-`b` witnesses selected in the [pre-execution contract](RES001_R4C1_FINITE_B_TRANSFER_CONTRACT_2026-09-30.md)
lie in the earlier *single-cosine algebraic* `delta<1` corridor on actual B1
torus modes `k=2*pi*n`. Their full **constraint-reduced linear scalar**
fundamental matrices evolve numerically on `t∈[0,4]`, with two independent
integrators agreeing and the canonical symplectic residual below the frozen
accuracy thresholds. This establishes a bounded finite-time calculation in
the conditional action family. It is **not** weak-field force-law closure,
stability, a physical EFT domain, or a Test-1/2/3 physics pass.

The contrast illustration at `k=1` in the earlier preflight uses a *different*
period choice; it must not be silently called a registered B1 mode. B1's
spatial periods are one, so this calculation uses `n=1,2` and `k=2*pi*n`.

## Provenance and method

The contract was hashed **before** the executable:
`f2635f9754d6a2b597711057b8294a2d3d0247c864a277bf2d7e2bb75ec4a108`.
The [new read-only executable](../../../Analysis/MasterTests/test_01_r4c1_finite_b_transfer.py)
has SHA-256 `e3cccca315776827a8fe74a07e1a60852ce941dabf68f85571ddbf76bf33a443`.
Its final stdout artifact in ignored `.local/itsm-context` has SHA-256
`68cbf91e5640d7e68f55a8797d11402958763c903f06a04c1826c85aee9c6006`.
Implementation/source-pin result: **45/45 passed, zero failed, validation PASS**;
the machine result explicitly records `physics_pass=false` and `gate_effect=NONE`.
The first local execution, output SHA-256
`b6ea0f9b16a04a893e542b99ec465e621c5ea2c7e2bb2b480d6d902ea4243ba0`,
omitted the contract's requested instantaneous-exponent *reporting*;
the final executable added that reporting without changing probes, equations,
thresholds, or frozen inputs. Both local outputs remain; only the final one
is cited for complete contract coverage. No original `main()` was called.

The executable verifies the contract/action, S1/S2 matrix and transfer
hashes, B1 source/trajectory, previous exact finite-`b` checker, and the
S2 receipt's transitive dependency hashes. It derives `dW/db` anew from the
S1 `V` and S2 time-dependent canonical transformation. The B1 RHS and
initial state compare exactly for the three `b` values at six times;
the dense background differs from the pinned trajectory by at most
`1.4064e-11` in the registered normalized metric. Baseline `n=1` DOP853
endpoint transfer matches the frozen S2 endpoint with normalized maximum
**0.0**, below `1e-7`.

Every row evolved the 12x12 matrix of `(x,xdot)` from identity on `[0,4]`
at 101 times with DOP853 and Radau, both `rtol=1e-9`, `atol=1e-11`.
Both methods finished with finite values for each row. The table reports
the DOP853 maximum sampled norms; the symplectic column is its maximum
normalized residual. The two-solver discrepancy covers the entire sampled
transfer, not just the endpoint.

| Case | `n`, `b` | Conditional `delta^2` | Two-solver discrepancy | Symplectic residual | Max `(x,xdot)` chart norm | Max canonical `(x,pi)` chart norm |
|---|---|---:|---:|---:|---:|---:|
| Frozen baseline reproduced | `1`, `5/11` | 295060.302 | `6.64e-10` | `1.65e-10` | 20.576 | 13.894 |
| Corridor-1 | `1`, `1/1250` | 0.913979 | `1.03e-10` | `5.31e-11` | 65.724 | 19.814 |
| Corridor-2 | `2`, `1/10000` | 0.456989 | `2.65e-10` | `5.39e-11` | 94.719 | 22.114 |

The frozen S2 `n=2,b=5/11` reference, not rerun here, has maxima 57.174
in `(x,xdot)` and 57.229 in `(x,pi)`. Thus the same-mode `n=2` chart norm
increases under this small `b`, while the canonical chart norm *decreases*.
Neither norm is a physical energy or gauge-invariant stability certificate.
The local instantaneous maximum positive real exponent at `t=0` is 1.177
for baseline `n=1`, 2.657 for corridor-1, and 2.533 for corridor-2; it
decreases by `t=4` in all three rows. Finite instantaneous growth is not an
all-time or UV gradient-instability classification.

Reproduce the final calculation:

```text
python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_finite_b_transfer.py
```

## Scientific boundary and next discriminant

The `delta<1` values are necessary algebraic crossover diagnostics, not a
demonstration of the square-root force law, controlled quasistatic error, or
agreement with any observed `a0`. The previous [exact principal audit](RES001_R4C1_FINITE_B_PRINCIPAL_SYMBOL_AUDIT_2026-09-30.md)
still shows a defective zero branch and wider condensate cone for every
finite `b>0` in this chart. The present finite-time runs neither remove
those defects nor prove that the smaller `b` values lie below an
action-derived physical cutoff. The `b=0` endpoint changes constraint rank.

The next Tier-1 obligation is an original-variable zero-branch/regularity
analysis and a coupled nonlinear metric/frame/dust/Euler contrast solution
with an independently bounded quasistatic remainder. Separately, Test 1
still needs full source-vector and GR-limit closure; Test 3 still needs a
blind action-derived `C_chi`. `K_Q=NOT_DERIVED`, `V=NOT_COMPUTED`,
`MAT-001=BLOCKED`, `UVIR-003=IN_PROGRESS`, `Stage4A=CLOSED` remain unchanged.
No commit, push, review dispatch, or publication promotion followed.
