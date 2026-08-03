# WAK-001 Stage 1 - relaxation-template mathematical audit

**Date:** 2026-08-03
**Result:** `PASS_WAK001_RELAXATION_TEMPLATE_MATH`
**WAK-001 status after result:** Open
**Physical wake law:** Not yet derived

## Scope

This audit checks the internal mathematics of the minimal periodic-domain
template

```text
tau_W (partial_t + v_W partial_x) W + W = kappa_W S.
```

It does not select the template as an ITSM constitutive law. In particular,
the audit does not derive the tensor character of `W`, its microscopic source,
its stress tensor, its coupling to matter, or any coefficient value.

## Reproduction

```powershell
conda run -n itsm_env python Analysis\WAK\WAK-001\wak001_relaxation_template.py
```

Expected footer:

```text
PASS_WAK001_RELAXATION_TEMPLATE_MATH
WAK-001 gate: OPEN
Physical wake law: NOT_YET_DERIVED
```

## Declared toy point

The positive control uses dimensionless template values `tau_W = 2.5`,
`v_W = 0.4`, `kappa_W = 0.7`, and `c_matter = 1`. These are test inputs,
not fitted or predicted ITSM parameters.

## Verified identities

For a source-free Fourier mode `W ~ exp(lambda t + i k x)`, the script checks

```text
lambda = -1/tau_W - i v_W k.
```

The real part is negative for `tau_W > 0`. On a periodic domain the advective
term contributes only phase transport and the quadratic template energy
decays as `E(t)/E(0) = exp(-2t/tau_W)`.

For `S ~ exp(i k x - i omega t)`, the checked transfer function is

```text
W/S = kappa_W / [1 - i tau_W (omega - v_W k)].
```

It has a finite comoving-static limit and suppresses high detuning rather than
amplifying it.

## Verified output

```text
decay_rate: -0.4
characteristic_speed: 0.4
static_gain: 0.7
high_frequency_gain: 0.0279776268442
energy_ratio: 0.0407622039784
negative_controls_caught: 3
```

The negative controls require rejection of `tau_W = 0`, `tau_W < 0`, and a
transport speed outside the declared matter cone.

## Interpretation boundary

This pass establishes only that a first-order causal-decay template can meet a
minimal linear mathematical screen. It does not establish a covariant
dissipative theory, coupled positive energy, exact exchange cancellation,
UVIR-003 compatibility, a galactic force, a lensing response, a detached
cluster wake, or maintained anisotropic stress.

The AQUAL-class law remains the Conditional static IR baseline. Any eventual
static wake contribution must be matched without counting that response a
second time.

## Next decision

Before Stage 2, choose and justify one bookkeeping route from the gate spec:

- Route I: `W` is internal to the plenum and included in `T_P^{mu nu}`; or
- Route II: `W` is independent and has `T_W^{mu nu}` plus an explicit exchange
  current.

The present audit does not prefer either route. The choice must follow from
candidate microphysics, not from a desired galaxy or cluster outcome.
