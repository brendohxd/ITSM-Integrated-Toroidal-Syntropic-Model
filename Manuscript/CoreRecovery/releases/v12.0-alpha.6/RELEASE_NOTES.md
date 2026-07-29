# ITSM Core v12.0-alpha.6

Date: 29 July 2026
Label: Gauge-projected matter response checkpoint

## Scientific advance

This release completes the source-to-observable follow-on required by the
`v12.0-alpha.5` complex-quartet attribution hold.

The calculation:

- applies generalized impulse covectors only in retained
  `(Q_rho,Q_chi)`;
- verifies that the corresponding original-field covectors annihilate the
  homogeneous time-translation orbit `(H,rho_dot,mu)`;
- reads out only retained gauge-invariant matter coordinates;
- orthonormalizes source and observable maps within their
  kinetic-normalized two-dimensional subspaces;
- propagates every source time to every later observation time using the
  exact time-dependent generator; and
- repeats the response audit over the same five reference,
  on-shell-background, and alignment cases.

The full finite-`q` framework still contains the Track-A force mode `Pi`. It
factorizes exactly from the coupled `(Xi,Q_rho,Q_chi)` quadratic block and is
therefore outside this complex-quartet mixing calculation rather than omitted
from ITSM.

## Gate result

Direct `Xi` source and readout support remain below `7.61e-21` and
`4.94e-21`, respectively. Time-orbit annihilation residuals are below
`5.66e-17`, source/readout orthonormality residuals are below `1.74e-15`, and
the largest coarse/fine response error is `5.48e-5`.

Every tested case retains amplified through-quartet response in
`(Q_rho,Q_chi)`, ranging from `2.67849e17` to `9.75967e19`. The baseline value
is `1.43264e19` and is predominantly radial in both its maximizing source and
output mixtures.

The bounded subgate status is:

```text
PASS_GAUGE_PROJECTED_MATTER_RESPONSE_SURVIVES_WITH_SCOPE
```

The large response therefore cannot be dismissed solely as direct sourcing
or observation of the homogeneous time-translation continuation.

## Scientific boundary

This release does not close UVIR-003 and does not establish:

- an all-background or asymptotic instability theorem;
- a physical cosmological parameter selection;
- an observed transfer amplitude;
- a completed cosmological `2-to-2` S-matrix element;
- a unitarity violation, strong-coupling scale, or physical cutoff;
- the local nonzero-gradient exact-`Y^(3/2)` reduction; or
- MAT-001.

The normalized finite-duration response is a structural diagnostic on the
tested dimensionless branch and neighborhood.

## Reproduction

From the repository root:

```powershell
python Analysis\UVIR\UVIR-003\uvir003_source_observable_retarded_response.py
```

Expected final status:

```text
STATUS: PASS_GAUGE_PROJECTED_MATTER_RESPONSE_SURVIVES_WITH_SCOPE
```

The next required calculation is to identify a controlled real-pole,
adiabatic exchange domain, project the verified interaction kernels onto the
retained source/observable channels, and assemble the gauge-regular
exchange-plus-reduced-contact `2-to-2` amplitude.
