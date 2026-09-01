# ITSM Core v12.0-alpha.9

Date: 30 July 2026
Label: Local four-leg kernel checkpoint

## Scientific advance

This release completes the local analytic four-leg assembly requested by
`v12.0-alpha.8`.

Four residue-normalized coupled modes are placed on shell at the initial
frozen-time snapshot in an all-incoming elastic convention. Their
equal-magnitude spatial momenta occupy regular-tetrahedron vertices, so all
three pair partitions have strictly nonzero

`q_K=2q/sqrt(3)`.

Each internal trajectory is independently rerun through the fixed-comoving
controlled-domain audit.

## Assembled kernel

For every `s`, `t`, and `u` partition, the calculation combines:

- matched left/right physical cubic pair sources;
- the complete finite-`q` physical propagator;
- the polarized analytic quartic contact; and
- the corresponding constraint-induced quartic Schur pairing.

Across 24 elastic mode-pair cases and 72 channel contractions, all combined
local kernels are finite, nonzero, real within numerical tolerance, and
permutation consistent.

The bounded subgate status is:

```text
PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL
```

## Numerical audits

```text
maximum on-shell kernel residual        = 3.41511e-15
maximum residue-normalization error     = 3.33067e-16
maximum pair-source swap error          = 5.98691e-16
maximum component permutation error     = 1.70304e-14
maximum inverse-closure error            = 4.74692e-16
minimum distance to a local pole         = 0.171148
maximum total imaginary fraction         = 1.92562e-16
combined real-kernel range               = [-62.1674, 1.78508]
cancellation-ratio range                 = [0.00502092, 0.101546]
```

The lower cancellation ratio means that the combined kernel can be about
`0.5%` of the sum of absolute component magnitudes. This cancellation is
numerically resolved but remains a sensitivity to omitted physics,
backgrounds, and kinematics rather than a derived suppression scale.

## Scientific boundary

This release closes only the local frozen-time analytic four-leg kernel on
the tested regular-tetrahedral slice. It does not establish:

- asymptotic cosmological in/out states;
- an S-matrix amplitude or cross section;
- an optical-theorem or partial-wave unitarity normalization;
- a strong-coupling scale or physical EFT cutoff;
- robustness over general four-leg kinematics;
- the held nonanalytic `|grad(pi)|^3` contribution on a nonzero-gradient
  background; or
- MAT-001.

UVIR-003 therefore remains in progress.

## Reproduction

From the repository root:

```powershell
python Analysis\UVIR\UVIR-003\uvir003_local_four_leg_kernel.py
```

Expected final status:

```text
STATUS: PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL
```

The next calculation should extend the local kernel away from the
regular-tetrahedral slice, audit approach to internal poles and homogeneous
channels, and define an adiabatic wave-packet or in-in observable
normalization before any perturbative-unitarity criterion is attempted.
