# ITSM Core v12.0-alpha.7

Date: 29 July 2026
Label: Controlled exchange-domain checkpoint

## Scientific advance

This release completes the controlled-domain identification required by
`v12.0-alpha.6`.

At fixed comoving momentum on the representative evolving branch, a sampled
trajectory is admitted only when:

- the finite-`q` kinetic matrix remains positive;
- all coupled frozen poles remain real;
- coupled-mode and factorized-force adiabaticity remain below `0.1`;
- every physical frequency satisfies `|omega|/H >= 10`;
- pole pairing, realification and tracked-frame overlap pass; and
- the stored phase-space eigenspace projectors remain numerically idempotent.

## Gate result

Initial `q_phys/H=47.5,50,75,100` passes the declared criteria. The nearby
`45` sample remains real-pole and subhorizon but reaches
`max |omega_dot/omega^2|=0.110333`, while `47.5` reaches `0.0978296`.

The bounded subgate status is:

```text
PASS_CONTROLLED_REAL_POLE_ADIABATIC_EXCHANGE_DOMAIN
```

This brackets the sampled transition between `45` and `47.5`; it is not a
continuous proof that every unsampled momentum above `47.5` passes.

## Mode-label correction

The infrared robustness audit initializes a `gauge_continuation_Xi` label
only where that pair is more than `99%` `Xi`-pure. That label cannot be
imposed at high momentum.

The controlled-domain audit therefore tracks all three coupled finite-`q`
physical eigenspaces as unlabelled rank-two real frames, matched by
principal-angle overlap. The factorized Track-A `Pi` pole retains its
separate analytic audit. Actual retained-channel identification must come
from the vertex/source contraction.

## Exchange-channel rule

Passing external legs do not automatically admit a soft exchange channel.
Every nonzero internal `q_K=|k_a+k_b|` must independently satisfy the
controlled-domain gate and `det C(q_K) != 0`. Exact `q_K=0` uses the
separately audited homogeneous projector rather than a finite-`q`
substitution.

## Scientific boundary

This release does not close UVIR-003 and does not establish:

- a continuous or all-background controlled-domain boundary;
- retained-channel cubic vertex contractions;
- a nonzero-channel exchange amplitude;
- the combined exchange-plus-reduced-contact `2-to-2` amplitude;
- a cosmological S-matrix interpretation;
- a unitarity bound, strong-coupling scale, or physical cutoff; or
- MAT-001.

## Reproduction

From the repository root:

```powershell
python Analysis\UVIR\UVIR-003\uvir003_controlled_exchange_domain.py
```

Expected final status:

```text
STATUS: PASS_CONTROLLED_REAL_POLE_ADIABATIC_EXCHANGE_DOMAIN
```

The next required calculation is to contract the verified cubic pair source
with actual tracked finite-`q` physical-mode legs inside the admitted domain,
then assemble the gauge-regular nonzero-channel exchange term and combine it
with the reduced quartic contact before applying any unitarity criterion.
