# ITSM Core v12.0-alpha.8

Date: 29 July 2026
Label: Mode-projected cubic pair-source checkpoint

## Scientific advance

This release performs the first physical-mode projection of the verified
finite-`q` analytic cubic kernel inside the controlled exchange domain
established by `v12.0-alpha.7`.

At the initial frozen-time snapshot of the representative branch:

- initial `q_phys/H=47.5,50,75,100` supplies admitted local kinematic points;
- the three positive-frequency coupled modes are residue normalized using the
  positive-pole derivative of the inverse quadratic kernel;
- two external equilateral legs are placed on shell;
- their cubic contraction produces an off-shell pair-source covector in
  `(Xi,Q_rho,Q_chi,Pi)`; and
- the complete finite-`q` inverse kernel is applied as a response diagnostic.

The modes are locally ordered `physical_pair_1` through `physical_pair_3`.
No infrared `Xi`-pure identity is assigned at high momentum.

## Gate result

Across 48 admitted mode/sign cases, every pair source and inverse response is
finite and nonzero. The numerical audits give:

```text
max on-shell kernel residual       = 3.41511e-15
max residue-normalization error    = 3.33067e-16
max external-leg swap error        = 6.10882e-16
max inverse-closure error           = 5.52503e-16
min constraint determinant margin  = 1.22180
min distance to a local pole        = 0.279523
```

The bounded subgate status is:

```text
PASS_MODE_PROJECTED_CUBIC_PAIR_SOURCE
```

## Track-A scope

For two coupled external legs, the verified analytic cubic kernel produces
zero `Pi` pair-source support in all tested cases. This is a statement about
this contraction only. It neither removes `Pi` from the physical basis nor
resolves the held nonanalytic `|grad pi|^3` vertex on a declared nonzero-gradient
background.

## Scientific boundary

This release does not close UVIR-003 and does not establish:

- a matched left/right pair-source contraction;
- a summed `s`, `t`, and `u` exchange contribution;
- the reduced quartic contact contribution;
- a physical `2-to-2` amplitude;
- a cosmological S-matrix interpretation;
- a unitarity bound, strong-coupling scale, or physical cutoff; or
- MAT-001.

## Reproduction

From the repository root:

```powershell
python Analysis\UVIR\UVIR-003\uvir003_mode_projected_cubic_pair_source.py
```

Expected final status:

```text
STATUS: PASS_MODE_PROJECTED_CUBIC_PAIR_SOURCE
```

The next calculation is to form matched left/right source contractions for
each admitted nonzero channel, sum the exchange channels, and combine them
with the already derived reduced quartic contact before applying any unitarity
criterion.
