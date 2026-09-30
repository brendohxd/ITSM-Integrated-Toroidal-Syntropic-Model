# R4C1: exact finite-positive-`b` scalar principal-symbol audit

Date: 2026-09-30. Owner: conditional R4C1-v1, Master Tests 1 and 2.
Status: `EXACT_PRINCIPAL_CONTINUATION_ONLY`; `physics_pass=false`,
`gate_effect=NONE`, `Rule9_cleared=false`, review `DEFERRED`.

This is an append-only continuation of the [finite-regulator preflight](RES001_R4C1_FINITE_REGULATOR_WINDOW_PREFLIGHT_2026-09-30.md).
It tests a change of the *exploratory* action-family parameter `b>0`, not a
revision of the frozen B1 point `b=5/11`. No original executable, result,
sidecar, action, or gate status was edited.

## Sources and executable check

The checked [S1 matrix export](../../../Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_matrices.json)
has SHA-256 `27d5a7130293866373ec1a98fbb6d0be0036421ef937416f77dd05b80f61349a`;
the [S2 matrix export](../../../Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_matrices.json)
has SHA-256 `6e5379d6fa05ee7a3c78c78d9d731de14f4346c28425857fd3a02ed155d30e70`.
The [S1 executable](../../../Analysis/MasterTests/test_01_r4c1_scalar_constraints.py)
has SHA-256 `977138ff89690608d21feb6e7f436ca0898ca86d1f9f702d536b2191648018ed`;
the [S2 executable](../../../Analysis/MasterTests/test_01_r4c1_scalar_propagation.py)
has SHA-256 `745fd890250e965f3d1e5d562d72667e12c16ca6608fad9a72439fa735fcbbda`.
The exact [read-only continuation check](../../../Analysis/MasterTests/test_01_r4c1_finite_b_principal.py),
SHA-256 `0e2c7f4babce65e04ad828e7f6da29248e4a3161b31ca174cdcd0980518aa7b5`,
passed **18/18 algebraic/source-pin assertions**. Its stdout SHA-256 is
`91f9d74438c2643d0bd2048ec12c8a47ad47e508cfb47804868751f2f8614a45`.
The test does not call either receipt-writing `main()` and writes no result files.
Reproduce with:

```text
python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_finite_b_principal.py
```

## Exact continuation at fixed B1 background and other parameters

S1's reduced kinetic and velocity-mixing matrices `K,M` contain no `b`;
its reduced potential `V` is affine in `b`. In S1 field order, the only
nonzero entries of `dV/db` are `(psi,psi)=p^4`,
`(psi,W)=(W,psi)=-psi_dot*p^3`, and `(W,W)=psi_dot^2*p^2`, where `p=k/a`.
The S2 canonical transformation `R` is independent of `b`. Thus `G` is
unchanged and `dW_c/db=dV_c/db=a^3 R^T(dV/db)R`. In canonical coordinates
`x_psi` (index 3) and `x_W` (index 5), that derivative is exactly

```text
       [ p^4/3                 -sqrt(2)*psi_dot*p^3 ]
       [ -sqrt(2)*psi_dot*p^3  6*psi_dot^2*p^2   ].
```

This matrix has rank one. For every fixed **positive** `b`, the fast
large-`p` branch has `omega_fast^2=(b/3)*p^4+o(p^4)`.
Its `p^3` coupling to the slow `W` coordinate and the direct slow `p^2`
entry cancel under the mandatory fast-mode Schur reduction:

```text
6*b*psi_dot^2 - [(-sqrt(2)*b*psi_dot)^2/(b/3)] = 0.
```

The entire slow `p^2` matrix is therefore **exactly independent of `b`**
on this fixed-background canonical chart, as is the slow `p` gyro matrix.
The S2 characteristic polynomial remains

```text
nu^2*(nu^2+1)^2*(nu^2+1+(u^2+v^2)/13)*(nu^2+1/3).
```

Consequently merely reducing finite `b` does not remove the chart's
defective zero branch or the condensate branch with speed squared
`1+(u^2+v^2)/13>1` when the condensate is nonzero. It *does* alter the
quartic coefficient and all finite-`p` dynamics; the frozen S2 numerical
transfer results cannot be inherited. A check omitting the cubic Schur
piece would falsely report `b`-dependence in the slow principal block and
is expressly rejected by the executable.

## Interpretation and remaining route

This narrows, but does **not** erase, the earlier positive corridor. A
smaller finite `b` still opens the conditional single-cosine algebraic
contrast window at fixed `A` without directly lowering that separate
spherical estimate of `a_dyn`. Yet this principal-symbol audit shows it
cannot by itself cure two existing propagation holds. Also, the large-`p`
separation of a quartic frequency `sqrt(b/3)*p^2` from an order-`p`
branch requires parametrically `p >> sqrt(3/b)` in B1 reference units;
the `k=1` window witnesses are **not** certified by that asymptotic regime.
This is an ordering estimate, not an EFT cutoff. The auxiliary determinant
is proportional to `b`; at `b=0` the constraint rank changes and this
continuation is invalid.

The next discriminating test is a separately frozen finite-`b`, finite-`k`
**full constrained** evolution and original-variable zero-branch analysis,
followed by a physical validity bound and nonlinear metric/frame/dust/Euler
contrast solve. No numerical `K_Q`, `V`, `C_chi`, weak-field closure, uniform
well-posedness, healthy GR limit, or canonical Test-1/2/3 pass follows.
`MAT-001=BLOCKED`, `UVIR-003=IN_PROGRESS`, `Stage4A=CLOSED` remain unchanged.
