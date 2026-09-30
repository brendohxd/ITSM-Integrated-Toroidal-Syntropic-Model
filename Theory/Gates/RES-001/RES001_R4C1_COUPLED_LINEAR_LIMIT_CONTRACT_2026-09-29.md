# R4C1-T2P3: coupled finite-mode linear-limit contract

Date: 2026-09-29. Owner: Master Test 2 / conditional R4C1-v1.
Status before execution: `CONDITIONAL`; `physics_pass=false`,
`gate_effect=NONE`, `Rule9_cleared=false`, `review_status=DEFERRED`.

This is a necessary-condition calculation for the *complete linear scalar
metric/frame/dust system* about the registered, interacting B1 background.
It is not a static galaxy, a nonlinear source family, a quasistatic error
estimate, a physical EFT window, or a canonical Test-2 pass. No observed
`a0`, Hubble calibration, galaxy data, or target coefficient enters.

## Frozen inputs

Check exact file bytes and any present sidecars before using these inputs:

| Input | SHA-256 |
|---|---|
| `Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md` | `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3` |
| `Theory/Gates/RES-001/RES001_R4C1_FIRST_VARIATION_REPORT_2026-09-25.md` | `4834ea7517fd0393015e1d94fa1c130d84e2796b0ae1667712c2b5cf4653692c` |
| `Theory/Gates/RES-001/RES001_R4C1_B1_GLOBAL_REGULARITY_REPORT_2026-09-29.md` | `82708666dfce4ef214b614bc7da31b294d7569539b97292aaa9a79e906e6266f` |
| `Theory/Gates/RES-001/RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md` | `0b5f06aa3ca91876895c0f1ab521093fa44034f04ce62d605d676f9190824b1b` |
| `Theory/Gates/RES-001/RES001_R4C1_SCALAR_PROPAGATION_REPORT_2026-09-26.md` | `653541272bfe9b1ddfd82d7083cd77ba30e421daa3b7162816783d5ed03633d9` |
| `Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_matrices.json` | `27d5a7130293866373ec1a98fbb6d0be0036421ef937416f77dd05b80f61349a` |
| `Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_summary.json` | `10bdc2ac1faeb30203cd75f5015ab41e64dd19b6cef37193f6987baf85bfc033` |
| `Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_matrices.json` | `6e5379d6fa05ee7a3c78c78d9d731de14f4346c28425857fd3a02ed155d30e70` |
| `Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_transfers.json` | `8f85326eaec6cbc8c14a42fffb776869f374e0edb63ec9045fa0b40ca0119330` |
| `Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_summary.json` | `56a4db658ae24d86211148abaffc1b9cf4d3d5aceed2e732df1270abda737735` |
| `Theory/Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md` | `81c7138568d44fd3197b88cb21efe67b17c406ada941f7ff778c2f8821ae074b` |

The S1/S2 outputs are inherited **conditional** calculations, not fresh
independent mathematical review. Do not run their receipt-writing `main()`
functions or modify their output files. Failed historical attempts remain
historical and cannot replace the pinned current matrices.

## Calculation and rejection rules

1. Keep the S1 cosine/sine convention: scalar perturbations and lapse have
   amplitude `cos(kx)`, and the longitudinal shift has amplitude `sin(kx)`.
   Use `k=2*pi*n`, finite nonzero `n`, `H>0`, `C>0`, `b>0`,
   `M_U^2 c_L>0`; do not invert a zero/singular branch.
2. Derive the matter-frame Newtonian-gauge potentials by applying the
   infinitesimal time shift `xi^0=T cos(kx)`, `T=a^2 S/k`, to the *full*
   conformal metric `g_tilde=C(psi)^2 g`. Verify that the transformed shift
   vanishes and that, with spatial metric convention `1-2 Psi_m`, one gets
   `Phi_m=alpha+beta*dpsi-dot(T)-beta*psi_dot*T` and
   `Psi_m=(H+beta*psi_dot)*T-beta*dpsi`.
   Using the S1 dust constraint, also verify
   `Phi_m=dot(dtau)/C-dot(T)-beta*psi_dot*T`.
   A calculation that omits `dot(T)`, the background conformal derivative,
   or the retained shift is rejected. These are linear potentials, not a
   measured radial-acceleration relation.
3. From `Y=O(lambda^2)` on the aligned B1 branch, establish that
   `-A Y^(3/2)=O(lambda^3)` and that the complete quadratic S1/S2 matrices
   are independent of `A`. This is a statement about second variation,
   not a Taylor expansion through the nonanalytic cubic vertex.
4. Use S1 invertibility and B1G regularity to prove that for each fixed
   finite nonzero mode the S2 linear ODE has a unique transfer over `[0,4]`.
   Scaling any consistent initial perturbation by `lambda` scales every
   first-order metric/frame/dust/scalar observable by exactly `lambda`.
   There is no claimed uniform-in-mode IVP or physical EFT cutoff.
5. Exhibit a nonzero dust source, not just a zero-source or pure-gauge
   vector. At the registered initial B1 state choose `dtau=1`, all other
   retained `q` and `qdot` amplitudes zero; reconstruct auxiliaries from S1.
   With `rho_m=epsilon_bar*C^4` and `epsilon_bar_dot=
   -3(H+beta*psi_dot)*epsilon_bar`, compute the Newtonian-gauge Jordan
   density contrast `depsilon_N=depsilon-epsilon_bar_dot*T`. Require it to
   have absolute amplitude above `1e-2` at `n=1`, well away from numeric
   cancellation. An auxiliary periodic Poisson comparator at fixed
   positive `G_ref` then has a nonzero acceleration amplitude linear in
   `lambda`.
6. For this nonzero-source direction, any finite first-order matter-frame
   acceleration derived from `Phi_m` is `O(lambda)`, while a fixed positive
   `sqrt(g_bar*a0)` term would be `O(sqrt(lambda))`. Thus the latter cannot
   be the arbitrarily small-amplitude *coupled linear* asymptote. Do not
   claim this rejects a nonlinear intermediate regime, another background,
   the full candidate, or every ITSM variant.
7. Cross-check the archived S2 finite-mode transfer shapes, finiteness and
   two-method normalized disagreement below `1e-5`. Check selected vector
   scaling to relative `1e-12`; report that a scaling check of a stored linear
   matrix is a consistency witness, not independent nonlinear evolution.
   Preserve any failed attempt and exact diagnostics.

Master Test 2, the physical projection factor, unique `C_chi`, `a0(z)`,
MAT-001, UVIR-003, Stage 4A and publication holds remain unchanged.
