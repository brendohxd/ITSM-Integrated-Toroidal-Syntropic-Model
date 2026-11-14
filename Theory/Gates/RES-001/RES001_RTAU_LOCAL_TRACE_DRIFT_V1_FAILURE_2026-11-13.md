# Preserved local trace V1 interval failure

The first execution stopped before writing a receipt at the explicit
positivity assertion for the force-sector spatial invariant Y. Its
double-sum evaluation multiplied an interval by itself rather than using
the squared-diagonal form from the inherited stable evaluator. If that
interval contains zero, ordinary interval multiplication can produce a
negative lower endpoint even though the exact square is nonnegative.

V2 restores the existing sum of diagonal squares and off-diagonal cross
terms. It uses the same equations, action, inputs and acceptance test.
The V1 source and sidecar remain intact.

- V1 source SHA-256 `f4a9eaecd37cc162371f2a32e4a147c0111e1f75118a6859704d65738be88ce8`
- Execution transcript SHA-256 `42b40ab353747458e25e8a93ae841ac1b024c13fee8bf24b4ddc9155dd14ec28`

This failed evaluation supplies no coefficient bound or physical verdict.
