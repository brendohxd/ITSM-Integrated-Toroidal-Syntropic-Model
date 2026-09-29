# R4C1-C2: periodic on-shell force-coefficient identifiability contract

Date: 2026-09-29. Owner: Master Test 3 / conditional R4C1-v1.
This is an action-level identifiability **obstruction** in the same fixed
FRW, aligned-frame, static density-contrast reduction used by T2P1. It
does not establish a coupled physical torus, the local weak-field law,
an observed or derived `a0`, a unique `C_chi`, or Test-3 closure.

## Pinned inputs and prohibition on target insertion

Pin the following live file bytes by SHA-256 before any calculation:

| Source | SHA-256 |
|---|---|
| `Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md` | `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3` |
| `Theory/Gates/RES-001/RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_REPORT_2026-09-25.md` | `c4af4084ae83f7ed70d63f44700a0ebfc2c394ed7d79cd0061e3efe279b7dc0a` |
| `Theory/Gates/RES-001/RES001_R4C1_PERIODIC_FORCE_REPORT_2026-09-29.md` | `5f178a121aae03fb5b4d47cf383586f0496a7d18262fc5b6069dc8be0fc658ad` |
| `Analysis/MasterTests/test_02_r4c1_periodic_force.py` | `8e1b398c70cd1308252d743acbb4d2a7fcef02c28d3b79b0f124f5c3f85a6727` |
| `Analysis/MasterTests/outputs/r4c1_t2p1_attempt_02/summary.json` | `fb59f3bf28e1b57c5294448f011731e805fe2f7928d12d40de210abb24f762bc` |
| `Analysis/MasterTests/outputs/test_03_r4c1_coefficient_identifiability_summary.json` | `49b10df599d6158f02ae6e55febe054f5b6fe2e3a2b53ee70daf7196f44d2fcf` |
| `Theory/Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md` | `81c7138568d44fd3197b88cb21efe67b17c406ada941f7ff778c2f8821ae074b` |

No observed acceleration, Hubble calibration, galaxy, lensing or bTFR data
enter this calculation. The four historical `C_chi` comparators are not
selected or ranked. This is data-independent, **not** fresh analyst
blinding: the analyst has already seen the historical target context.
Changing `A` alone changes the invariant `A/K_Q^(3/2)` with `K_Q,b,beta`
and topology fixed; it is not a field-chart transformation.

## Exact conditional theorem to audit

On a cubic `T^3` of period `2*pi`, take the zero-mean `H^2` scalar space,
`delta_rho=(cos x+2 cos y+3 cos z)/50`, and the spatial functional

```
J_A[psi] = integral_T3 [A |grad psi|^3
                       + (b/2)(Delta psi)^2
                       + beta delta_rho psi],
b=5/11>0, beta=2/5>0, A>=0.
```

The continuum proof must show, without using a finite-grid PASS as the
premise: (i) coercivity and strict convexity on zero-mean `H^2`, hence a
unique weak minimizer for each `A>=0`; (ii) if `A_1 != A_2`, the two
minimizers cannot coincide for this nonzero source; and (iii) the cubic
gradient functional `P_A=integral |grad psi_A|^3` strictly decreases as
`A` increases. The identical-solution contradiction must subtract the
Euler equations and test with `psi`; it fails only for the excluded zero
source. The monotonicity argument must use the two strict minimizer
inequalities, not an assumed pointwise sign of the force field.

This theorem concerns the **conditional static contrast functional**. It
does not imply a physical cosmological/galaxy family or a unique observed
normalization. The homogeneous `A`-independence is inherited from pinned
C1, not reproved by a repeated ODE.

## Frozen numerical witness and rejection controls

- Reuse exactly T2P1's density, torus, zero-mean gauge, `b`, `beta`,
  pseudospectral solver and odd grids `N=17,25,33`. Set
  `A/A_B1 in {1/4,1,4}` with `A_B1=2/7`; start each branch from the
  analytic `A=0` linear solution. No parameter or threshold retuning.
- At every grid/branch require finite converged output, zero-mean `psi`
  within `1e-12`, and normalized strong Euler residual below `1e-5`.
  All six independent fundamental cosine/sine weak residuals must be
  below `1e-5`, normalized exactly as in T2P1.
- For each `A` branch, fundamental cosine coefficients at `N=25` and
  `N=33` must agree relatively within `5e-3` (denominator floor `1e-12`).
  This is a grid diagnostic, not a continuum error theorem.
- At each grid require `P_{A/4}>P_A>P_{4A}`. Each relative adjacent
  difference, normalized to `P_A`, must exceed `1e-4` to resolve it
  above the numerical residual. The zero-mean solution fields for each
  adjacent pair must differ in RMS by more than `1e-4` of the RMS B1
  solution. This is a witness to, not proof of, the continuum theorem.
- The zero-source control must have the same zero solution for all three
  `A`, documenting the theorem's nonzero-source premise. Reject the false
  assertion that the three nonzero-source responses are equal, and reject
  replacing the physical `A/K_Q^(3/2)` change by a chart rescaling.

Preserve any failed attempt with exact diagnostics; do not overwrite a
prior receipt. A locally passing C2 record remains `physics_pass=false`,
`gate_effect=NONE`, `Rule9_cleared=false`, `review_status=DEFERRED`,
`canonical_Test3_pass=false`, `C_chi=NOT_DERIVED`, `a0=NOT_PREDICTED`.
MAT-001, UVIR-003, Stage 4A and publication holds are unchanged.
