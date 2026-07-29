# UVIR-003 Stage-B mode-resolved transfer and robustness audit

Date: 2026-07-29

Status:

```text
Tracked kinetic-normalized mode pairs: COMPLETE
Transfer and pair-assignment numerics: PASS
Rank-two physical-mode separability: HOLD_COMPLEX_QUARTET
Infrared dominant-transfer attribution: XI_SEEDED_BUT_COMPLEX_QUARTET_MIXED
Nearby on-shell trajectory and parameter robustness: ROBUST_STRUCTURAL_HOLD
Retained-matter infrared instability: NOT_CLASSIFIED_DUE_TO_COMPLEX_QUARTET_MIXING
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: HOLD_COMPLEX_QUARTET_IR_MODE_ATTRIBUTION
```

## 1. Question addressed

The preceding fixed-comoving audit found a converged maximum
kinetic-normalized phase-space gain of

```text
1.37708e27
```

for the trajectory beginning at `q/H=0.01`. That singular value alone did not
show whether the gain belonged to:

1. the finite-`q` continuation of the homogeneous `Xi` time-translation gauge
   orbit;
2. one of the retained matter modes `Q_rho` or `Q_chi`;
3. a mixed mode created during the time-dependent evolution.

This follow-on constructs instantaneous kinetic-normalized pole-pair frames,
parallel-transports them, projects the exact transfer by initial mode
subspace, and repeats the calculation in a small on-shell background and
alignment-parameter neighborhood.

## 2. Kinetic-normalized frozen modes

For

```text
p = (Xi, Q_rho, Q_chi),
u = (K^(1/2) p, K^(1/2) p_dot/H),
```

let `N` denote the map from `(p,p_dot)` to `u`. At each fixed-comoving
trajectory point the frozen generator is

```text
G_frozen,u = N G_frozen,(p,p_dot) N^(-1),
```

where the coefficient derivatives and Hubble dilution are omitted only for
the instantaneous pole basis. The exact transfer still uses the complete
time-dependent generator with `K_dot`, `P_dot`, `3H`, and `N_dot`.

The six frozen eigenvalues are paired by minimizing the normalized residual
under

```text
lambda_j approximately equals -lambda_i.
```

For each nominal pair, the real and imaginary parts of the two eigenvectors
form a candidate real rank-two physical phase-space frame. The frame is
orthonormalized, pairs are assigned between adjacent times by Hungarian
matching on principal-angle overlap, and their orientations are
parallel-transported with an orthogonal Procrustes rotation.

This procedure treats arbitrary eigenvector phases and ordinary avoided
crossings without relying on sorted eigenvalues.

## 3. Structural obstruction: an off-axis complex quartet

The rank-two construction is not valid throughout the infrared trajectory.
For a finite interval the frozen real generator has an off-axis complex
quartet:

```text
lambda, lambda*, -lambda, -lambda*,
Re(lambda) != 0,
Im(lambda) != 0.
```

The corresponding real invariant space has rank four. It cannot be split
canonically into two continuously real rank-two pole-pair subspaces. This is
not a convergence failure or an arbitrary phase-choice problem.

For the baseline trajectory:

| Diagnostic | Result |
|---|---:|
| Coarse/fine transfer error | `1.30353e-4` |
| Maximum `lambda -> -lambda` pairing residual | `5.80869e-13` |
| Minimum assigned adjacent-subspace overlap | `0.664767` |
| Off-axis quartet time fraction | `0.0362047` |
| Maximum nominal-pair realification leakage | `0.432297` |
| Maximum frozen eigenvector condition number | `1.67666e4` |

The transfer and pair-assignment numerics pass. The nonzero realification
leakage is instead the diagnostic that the nominal rank-two split has entered
a rank-four complex-quartet interval.

## 4. Baseline transfer attribution

At the time of maximum full transfer gain, the maximizing initial right
singular vector has

```text
initial Xi-pair projection fraction = 0.9999313.
```

Thus the dominant transfer is overwhelmingly seeded by the initial
finite-`q` `Xi` gauge-continuation subspace.

That fact does not complete a physical classification:

```text
maximum full gain                    = 1.37708e27
maximum retained-matter-seeded gain = 3.23731e24
```

During the quartet interval the output cannot be decomposed into unique
rank-two `Xi` and retained-matter pole pairs. The matter-seeded subspaces also
amplify strongly. Therefore the result is neither:

- a proved retained-matter instability;
- a proved pure gauge artifact;
- a physical Lyapunov exponent;
- an all-background stability result.

It is a converged, `Xi`-seeded, mixed complex-quartet transfer.

## 5. Nearby robustness audit

Five cases were tested at initial `q/H=0.01`:

1. the reference branch;
2. an independently integrated on-shell branch with `rho_initial=0.95`;
3. an independently integrated on-shell branch with `rho_initial=1.05`;
4. the reference branch with `zeta_align=0.8`;
5. the reference branch with `zeta_align=1.2`.

The on-shell variations recompute the conserved charge, Friedmann-consistent
initial Hubble value, and complete background trajectory. The alignment
variations alter the perturbation kernel while leaving the homogeneous
alignment background zero.

| Case | Coarse/fine error | Quartet fraction | Maximum full gain | Initial `Xi` fraction | Maximum matter-seeded gain |
|---|---:|---:|---:|---:|---:|
| Baseline | `1.30353e-4` | `0.0362047` | `1.37708e27` | `0.999931` | `3.23731e24` |
| `rho_initial=0.95` | `1.90919e-4` | `0.0324594` | `1.28919e25` | `0.999776` | `6.18696e22` |
| `rho_initial=1.05` | `8.03746e-5` | `0.0362047` | `1.40758e28` | `0.999961` | `2.17268e25` |
| `zeta_align=0.8` | `1.39769e-4` | `0.0362047` | `1.28300e27` | `0.999912` | `3.58076e24` |
| `zeta_align=1.2` | `1.23092e-4` | `0.0362047` | `1.44948e27` | `0.999943` | `2.93411e24` |

Every case satisfies the transfer convergence threshold, has an
`Xi`-dominated maximizing initial vector, and enters an off-axis
complex-quartet interval. The gain magnitude is highly branch-sensitive, but
the structural obstruction is robust in this tested neighborhood.

## 6. Interpretation boundary

The preceding low-`q` audit established that `Xi` is the finite-`q`
continuation of the homogeneous time-translation gauge orbit. At finite `q`,
however, `Xi` remains a gauge-invariant coordinate in the reduced system.
Consequently:

- `Xi`-seeded does not mean automatically unphysical;
- quartet mixing prevents discarding the transfer as a pure gauge effect;
- the large matter-seeded gains prevent declaring the retained matter sector
  stable;
- the finite duration and narrow dimensionless neighborhood prevent a global
  instability claim.

The correct gate result is:

```text
HOLD_COMPLEX_QUARTET_IR_MODE_ATTRIBUTION
```

## 7. Next required calculation

A source-to-observable response audit is now required because frozen pole
pairs cease to provide a unique mode split:

1. construct source covectors that annihilate the homogeneous
   time-translation orbit and couple only to retained gauge-invariant
   observables built from `Q_rho` and `Q_chi`;
2. propagate the exact retarded response through the quartet interval without
   assigning rank-two pole identities there;
3. test whether the large transfer survives in retained matter observables
   after the gauge-continuation source component is removed;
4. repeat that response audit over the same nearby on-shell neighborhood;
5. only after this classification map a controlled exchange domain and
   assemble the gauge-regular exchange-plus-contact `2-to-2` amplitude.

No unitarity, strong-coupling, or physical-cutoff inference is permitted
before the source-projected physical response and amplitude are complete.

## 8. Reproduction

From the repository root:

```powershell
python Analysis\UVIR\UVIR-003\uvir003_mode_resolved_transfer_robustness.py
```

Deterministic outputs:

```text
Analysis/UVIR/UVIR-003/outputs/uvir003_mode_resolved_transfer_robustness_summary.json
Analysis/UVIR/UVIR-003/outputs/uvir003_mode_resolved_transfer_robustness.csv
```
