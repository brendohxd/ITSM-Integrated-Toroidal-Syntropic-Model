# R4C1-S2b: predeclared finite-positive-`b` transfer check

Date: 2026-09-30. Owner: conditional R4C1-v1 / Master Tests 1 and 2.
Status: `FROZEN_BEFORE_EXECUTABLE`, provisional diagnostic only.
`physics_pass=false`, `gate_effect=NONE`, Rule-9 review deferred.

## Scientific question and sources

Does the same **fully constrained linear scalar** B1 system admit accurate
finite-time evolution at positive regulator coefficients selected from the
formal contrast corridor? This is neither a nonlinear weak-field solution
nor a new B1 parameter adoption. Preserve all frozen receipts and sidecars.

Pin before execution:

- R4C1 action `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3`.
- S1 reduced matrices `27d5a7130293866373ec1a98fbb6d0be0036421ef937416f77dd05b80f61349a`.
- S2 canonical matrices `6e5379d6fa05ee7a3c78c78d9d731de14f4346c28425857fd3a02ed155d30e70`.
- S2 frozen transfers `8f85326eaec6cbc8c14a42fffb776869f374e0edb63ec9045fa0b40ca0119330`.
- S2 summary `56a4db658ae24d86211148abaffc1b9cf4d3d5aceed2e732df1270abda737735`.
- B1 executable `1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f`.
- B1 trajectory `0024b7307de64d780aca3d47401fc8175d59baa354d53912b80ab6842d346daa`.
- Finite-`b` exact principal checker `0e2c7f4babce65e04ad828e7f6da29248e4a3161b31ca174cdcd0980518aa7b5`.

The [S2 contract](RES001_R4C1_SCALAR_PROPAGATION_CONTRACT_2026-09-26.md)
governs the frozen baseline. This extension must not run its receipt-writing
`main()` or overwrite any pinned file. Verify source hashes and independent
S2 receipt dependency hashes before trusting the exported matrices.

## Frozen probes, equations and numerical checks

Keep B1's dimensionless initial data, `A=2/7`, `beta=2/5`, homogeneous
trajectory, and **unit spatial periods**. Use only `k=2*pi*n`:

| Case | n | b | Reason |
|---|---:|---:|---|
| baseline | 1 | 5/11 | Exact reproduction of the S2 reference transfer. |
| corridor-1 | 1 | 1/1250 | Single-cosine diagnostic at `epsilon=1/50` gives `delta^2≈0.914<1`. |
| corridor-2 | 2 | 1/10000 | Same diagnostic gives `delta^2≈0.457<1`. |

These are prospective algebraic witnesses, not values fit to an observed
acceleration, transfer, galaxy or likelihood. The necessary contrast relation
is `delta^2=b^2*k^5/(3*A*beta*epsilon)`; `delta<1` is not an accuracy
threshold for a square-root force law. No other `b` or `n` may be substituted
after seeing the output. The `b=0` endpoint remains excluded.

Use the *time-dependent* canonical S2 matrices, with
`W(b)=W(5/11)+(b-5/11)*dW/db`, unchanged `G,Mc`, and the exact
`dW/db=a^3 R^T(dV/db)R` from the S1 matrix export. Check that the B1
background RHS and initial state are independent of `b`; compare the dense
background to the pinned B1 trajectory, normalized maximum `<1e-8`.
Do not substitute a frozen-time eigenvalue or `Vc` alone for the EOM.

For each case evolve the full 12x12 fundamental matrix of `(x,xdot)` from
identity on `[0,4]` at 101 output times using DOP853 **and** Radau,
`rtol=1e-9`, `atol=1e-11`. Require success, finite arrays, two-method
normalized maximum discrepancy `<1e-5`, and canonical symplectic residual
`<1e-6` with `pi=xdot+Mc*x`. For baseline `n=1`, compare the new DOP853
endpoint against the frozen S2 DOP853 endpoint with normalized maximum
`<1e-7`; a mismatch invalidates this continuation. Record chart and
canonical amplifications and any finite local real exponents, but do not
interpret them alone as an invariant stability verdict. A failed numerical
criterion is `UNVALIDATED`, not permission to tune the probes or tolerances.

The diagnostic may establish only finite-time numerical consistency of
the reduced linear scalar chart at those exact points. It cannot establish
uniform well-posedness, physical EFT validity, all-sector stability,
nonlinear metric/frame/dust/Euler weak-field closure, a healthy GR limit,
`K_Q`, `V`, `C_chi` or canonical Test-1/2/3 promotion. Maintain
`MAT-001=BLOCKED`, `UVIR-003=IN_PROGRESS`, `Stage4A=CLOSED`,
`Rule9_cleared=false`, `physics_pass=false`. No commit or push.
