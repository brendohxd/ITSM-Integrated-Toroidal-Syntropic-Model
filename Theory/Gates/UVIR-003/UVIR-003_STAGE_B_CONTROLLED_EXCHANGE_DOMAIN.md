# UVIR-003 Stage B controlled exchange domain

Date: 2026-07-29

Branch: `recovery/v12-core-architecture`

Calculation status: **PASS**
Subgate:
`PASS_CONTROLLED_REAL_POLE_ADIABATIC_EXCHANGE_DOMAIN`

Full UVIR-003 gate: **IN PROGRESS**

MAT-001: **BLOCKED**
Physical `2-to-2` amplitude: **NOT YET DERIVED**

## Result

A nonempty controlled high-momentum exchange domain exists on the audited
representative evolving branch. At fixed comoving momentum, the sampled
trajectories beginning at

`q_phys/H = 47.5, 50, 75, 100`

pass all declared criteria. The nearby sample at `q_phys/H=45` fails only the
physical-mode adiabaticity criterion, reaching
`max |omega_dot/omega^2| = 0.110333`, while the `47.5` sample reaches
`0.0978296`.

This brackets the sampled transition between `45` and `47.5`. It does not
prove that every unsampled momentum above `47.5` passes, nor that the same
boundary holds on every background or parameter choice.

## Admission criteria

Each trajectory is admitted only if:

1. the finite-`q` kinetic matrix remains positive;
2. every frozen pole of the coupled physical scalar block is real;
3. `max |omega_dot/omega^2| < 0.1` for the tracked coupled modes;
4. the factorized Track-A force mode also has adiabaticity below `0.1`;
5. every physical frequency satisfies `|omega|/H >= 10`;
6. pole-pairing residual and realification leakage are below `1e-8`;
7. tracked pair assignment overlap remains above `0.5`; and
8. the stored phase-space mode projectors are idempotent to `1e-10`.

The threshold `0.1` is the same controlled-adiabatic criterion already used
by the fixed-comoving transfer audit. The `|omega|/H >= 10` condition makes
the local frozen-time exchange interpretation explicitly subhorizon.

## Sampled map

| Initial `q/H` | All coupled poles real | Max coupled adiabaticity | Min `|omega|/H` | Max force adiabaticity | Min kinetic eigenvalue | Admitted |
|---:|:---:|---:|---:|---:|---:|:---:|
| 10 | no | `1.42379e31` | `0` | `8.31236e-2` | `3.24418e-2` | no |
| 20 | yes | `1.36207` | `12.1460` | `2.07809e-2` | `2.30981e-2` | no |
| 30 | yes | `2.99971e-1` | `28.4322` | `9.23595e-3` | `1.56081e-2` | no |
| 40 | yes | `1.44581e-1` | `39.0832` | `5.19522e-3` | `1.07352e-2` | no |
| 45 | yes | `1.10333e-1` | `43.9932` | `4.10487e-3` | `9.02460e-3` | no |
| 47.5 | yes | `9.78296e-2` | `46.4471` | `3.68415e-3` | `8.30460e-3` | yes |
| 50 | yes | `8.74516e-2` | `48.9005` | `3.32494e-3` | `7.66041e-3` | yes |
| 75 | yes | `3.80804e-2` | `73.4169` | `1.47775e-3` | `3.84082e-3` | yes |
| 100 | yes | `2.21546e-2` | `97.9192` | `8.31236e-4` | `2.26190e-3` | yes |

The minimum assigned pair-subspace overlap is `0.911276` over the complete
scan. Maximum pole-pairing residual is `3.43e-15`; maximum realification
leakage is `1.31e-14`.

## Correct mode-label boundary

The earlier infrared robustness audit initializes a
`gauge_continuation_Xi` label only where the corresponding pair is more than
`99%` `Xi`-pure. That infrared label fails at high momentum and is not imposed
here.

Instead, this audit tracks all three coupled finite-`q` physical eigenspaces
as unlabelled rank-two real frames, ordered initially by frequency and then
matched by principal-angle overlap. The factorized `Pi` pole is treated
separately with its analytic dispersion. This is the correct interface for a
high-momentum exchange calculation; retained-channel identification must be
made from the actual vertex/source contraction rather than inherited from an
infrared purity label.

## Interaction-kernel interface

The audit verifies that its inputs are the already passed:

- factorized finite-`q` physical cubic kernel;
- complete physical pair-source kernel;
- factorized reduced quartic kernel; and
- separate exact homogeneous-channel projector prescription.

For an exchange calculation:

- every external finite-`q` leg must lie on an admitted trajectory;
- every nonzero internal `q_K=|k_a+k_b|` must independently lie in the
  controlled domain and satisfy `det C(q_K) != 0`;
- passing external legs do not admit a soft internal channel automatically;
- exact `q_K=0` is not obtained by substituting zero into the finite-`q`
  inverse and must use the separately audited homogeneous projector.

The numerical output stores the initial kinetic-normalized phase-space
projector for each of the three coupled physical pole pairs. These projectors
establish the eigenspace interface, not yet a completed vertex contraction.

## Scientific boundary

This pass establishes:

- a nonempty sampled real-pole, subhorizon, adiabatic domain;
- positive kinetic support throughout every admitted trajectory;
- controlled mode-frame tracking without an invalid high-`q` gauge label;
- compatibility with the verified cubic and reduced-quartic kernel inputs;
- the rule that internal channel momenta must pass the same domain gate.

It does not establish:

- a continuous analytic boundary in `q/H`;
- the same domain on all backgrounds or parameter choices;
- retained-channel cubic vertex contractions;
- a nonzero-channel exchange amplitude;
- the combined exchange-plus-contact `2-to-2` amplitude;
- an S-matrix interpretation on the evolving cosmological background;
- a unitarity bound, strong-coupling scale, or physical cutoff.

## Reproduction

```powershell
python Analysis/UVIR/UVIR-003/uvir003_controlled_exchange_domain.py
```

Outputs:

- `Analysis/UVIR/UVIR-003/outputs/uvir003_controlled_exchange_domain_summary.json`
- `Analysis/UVIR/UVIR-003/outputs/uvir003_controlled_exchange_domain.csv`

Expected footer:

```text
Controlled real-pole domain map: COMPLETE
Lowest admitted sampled initial q/H: 47.5
Finite-q cubic/reduced-quartic interface: VERIFIED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_CONTROLLED_REAL_POLE_ADIABATIC_EXCHANGE_DOMAIN
```

## Next required calculation

1. Contract the verified cubic pair source with actual tracked finite-`q`
   physical-mode legs inside the admitted domain.
2. Assemble the gauge-regular nonzero-channel propagator exchange term.
3. Apply the separate exact-`q_K=0` homogeneous projector where required.
4. Combine exchange with the reduced quartic contact before applying any
   declared unitarity criterion.
