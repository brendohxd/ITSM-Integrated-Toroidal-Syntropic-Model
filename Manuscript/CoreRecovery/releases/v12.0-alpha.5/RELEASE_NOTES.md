# ITSM Core v12.0-alpha.5

Date: 29 July 2026
Label: Mode-resolved complex-quartet transfer checkpoint

## Scientific advance

This release completes the fixed-comoving, mode-resolved follow-on to the
UVIR-003 physical quadratic propagator audit.

It includes:

- the complete finite-`q` dressed cubic and reduced-quartic physical-basis
  kernels accumulated since `v12.0-alpha.4`;
- exact homogeneous internal-channel projectors that remove the nonexistent
  scalar shift and homogeneous `Xi` gauge orbit;
- finite-`q` physical inverse quadratic kernels and the separately projected
  exact-`q=0` response;
- converged fixed-comoving time-dependent transfer matrices with an
  independent canonical-Hamiltonian equivalence check;
- kinetic-normalized pole-pair frames, principal-angle assignment, and
  Procrustes parallel transport; and
- a five-case reference, on-shell-background, and alignment robustness audit.

The fixed-comoving calculation invalidates frozen-pole exponentiation in the
nonadiabatic domain. The initial `q/H=0.01` baseline retains a maximum
normalized phase-space gain of `1.37708e27`.

## Gate result

Every tested deepest-infrared case has an overwhelmingly `Xi`-seeded
maximizing initial singular vector. Every case also enters an off-axis complex
quartet whose real invariant space has rank four. The nominal
gauge-continuation and retained-matter pole pairs therefore have no unique
continuous real rank-two split through that interval, and matter-seeded
subspaces also amplify.

The release status is:

```text
HOLD_COMPLEX_QUARTET_IR_MODE_ATTRIBUTION
```

This is a robust structural hold, not a retained-matter instability finding
and not a pure gauge-artifact dismissal.

## Scientific boundary

This release does not close UVIR-003. It does not derive:

- a source-projected retained-matter response through the quartet interval;
- the complete gauge-regular cosmological `2-to-2`
  exchange-plus-reduced-contact amplitude;
- a unitarity or strong-coupling bound;
- a physical EFT cutoff;
- the local nonzero-gradient exact-`Y^(3/2)` reduction; or
- MAT-001.

`Xi` is gauge invariant at finite momentum even though it approaches the
homogeneous time-translation orbit as `q` approaches zero. Consequently the
Xi-seeded transfer cannot be discarded without the source-projected
observable audit.

## Reproduction

From the repository root:

```powershell
python Analysis\UVIR\UVIR-003\uvir003_physical_quadratic_propagators.py
python Analysis\UVIR\UVIR-003\uvir003_propagator_adiabaticity_transfer.py
python Analysis\UVIR\UVIR-003\uvir003_mode_resolved_transfer_robustness.py
```

Expected final mode-resolved status:

```text
STATUS: HOLD_COMPLEX_QUARTET_IR_MODE_ATTRIBUTION
```

The next required calculation is a source-to-observable retarded-response
audit that removes the homogeneous time-translation source direction and
measures retained `Q_rho,Q_chi` observables through the quartet interval.
