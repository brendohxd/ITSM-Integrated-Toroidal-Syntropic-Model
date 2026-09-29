# R4C1-T2P2: finite-regulator weak-source scaling contract

Date: 2026-09-29. Owner: Master Test 2 / conditional R4C1-v1.
This is a necessary-condition audit of the *fixed-frame static contrast*
equation on compact `T^3`, not the full metric/frame/dust/Euler response.
The mean scalar retains T2P1's time-dependent positive-dust obligation.

## Frozen provenance and source family

Before calculation, verify exact SHA-256 bytes and any present sidecars:

| Source | SHA-256 |
|---|---|
| `Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md` | `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3` |
| `Theory/Gates/RES-001/RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_REPORT_2026-09-25.md` | `c4af4084ae83f7ed70d63f44700a0ebfc2c394ed7d79cd0061e3efe279b7dc0a` |
| `Theory/Gates/RES-001/RES001_R4C1_PERIODIC_FORCE_REPORT_2026-09-29.md` | `5f178a121aae03fb5b4d47cf383586f0496a7d18262fc5b6069dc8be0fc658ad` |
| `Analysis/MasterTests/test_02_r4c1_periodic_force.py` | `8e1b398c70cd1308252d743acbb4d2a7fcef02c28d3b79b0f124f5c3f85a6727` |
| `Analysis/MasterTests/outputs/r4c1_t2p1_attempt_02/summary.json` | `fb59f3bf28e1b57c5294448f011731e805fe2f7928d12d40de210abb24f762bc` |
| `Analysis/MasterTests/test_01_r4c1_interacting_background.py` | `1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f` |
| `Theory/Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md` | `81c7138568d44fd3197b88cb21efe67b17c406ada941f7ff778c2f8821ae074b` |

At reference `a=1`, retain B1 `A=2/7`, `b=5/11>0`, `beta=2/5`,
`K_Q=3`, `rho_bar=1/5`, cubic `2*pi` torus and the nonzero zero-mean
`f=(cos x+2cos y+3cos z)/50`. Only scale the contrast:
`delta_rho_epsilon=epsilon*f` for
`epsilon in {1,1/4,1/16,1/64,1/256}`. Total density remains positive.
No observed acceleration, galaxy, Hubble or lensing data enter.

## Exact theorem to establish independently of grid checks

For mean-zero `H^2(T^3)` and each `epsilon>=0`, minimize

```
J_epsilon[psi] = integral [A|grad psi|^3
                     + (b/2)(Delta psi)^2
                     + beta epsilon f psi].
```

The finite `b>0` form is coercive and strictly convex, hence has a unique
weak minimizer. Show from its weak Euler equation and the periodic
Poincare estimate that `||psi_epsilon||_(H2)=O(epsilon)`. Define the
exact linear-response field `psi_1=-(beta/b)*f`, since `Delta^2 f=f`.
Subtract its equation and test the difference to establish
`||psi_epsilon-epsilon*psi_1||_(H2)=O(epsilon^2)` for this fixed source
and fixed positive couplings. State the Sobolev embedding used to bound
the nonlinear flux. Do not infer an error bound for the omitted time,
metric, frame, dust or physical-EFT terms from this spatial estimate.

For the auxiliary periodic Newtonian comparison `Delta Phi_bar =
4*pi*G_static*epsilon*f` at fixed `G_static>0`, the baryonic gradient
is `O(epsilon)`. The conditional conformal matter force `beta grad psi`
is also `O(epsilon)`. At a fixed point or norm with nonzero baryonic
response, its ratio to `sqrt(g_bar)` is `O(sqrt(epsilon))->0`. Therefore
a fixed positive square-root coefficient cannot be the *arbitrarily
weak-source, fixed-scale* asymptote of this finite-`b` static reduction.
This does not reject an intermediate source/domain window, another
regulator, a coupled completion, or all ITSM variants.

## Frozen numerical controls

- Reuse T2P1's pseudospectral solver, zero-mean gauge and odd grids
  `N=17,25,33`; solve each of the five registered epsilon values from
  the exact `A=0` linear solution for that scaled source. No alteration
  of `A,b,beta`, source shape, topology, grids or thresholds after output.
- Every branch must be finite/converged, have `|mean psi|<1e-12`, and
  normalized strong and all six weak Fourier residuals below `1e-5`,
  using the **scaled** source amplitude for normalization. The analytic
  `A=0` residual must be below `1e-10`.
- For every epsilon, the three fundamental cosine coefficients must agree
  between `N=25` and `N=33` to relative `5e-3` (floor `1e-12`). Grid
  convergence is not a continuum proof.
- Let `R_e=RMS(psi_e-e*psi_1)/RMS(e*psi_1)`. Require `R_e` decrease
  strictly as epsilon descends through the five values and
  `R_(1/256)<1e-2`. This is a numerical witness to the analytic limit.
- Let `S_e=beta*RMS(grad psi_e)/sqrt(epsilon)`. Require `S_(1/64) /
  S_(1/256)` in `[1.5,2.5]`, a coarse control on the expected
  factor-two asymptotic. Do not identify this norm with an observed RAR.
- Omitting `b` from the Euler operator at `epsilon=1/256` must leave a
  normalized residual above `1e-2`; the zero-source `epsilon=0`
  control must have exactly zero field and force. A negative `b` is
  outside the theorem, not an allowed retuning.

Preserve failed attempts and original receipts. A passing local run
remains `physics_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false`,
`review_status=DEFERRED`, `canonical_Test2_pass=false`; no unique `C_chi`,
`a0`, physical cutoff, coupled weak-field law or publication clearance.
