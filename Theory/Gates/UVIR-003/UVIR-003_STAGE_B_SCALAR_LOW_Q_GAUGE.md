# UVIR-003 - Stage B low-q scalar gauge-orbit audit

Date: 2026-07-26
Branch: `recovery/v12-core-architecture`
Status: **homogeneous gauge orbit identified; physical q=0 kinetic block passed**

## Executive result

The kinetic direction that collapses in the finite-wavenumber scalar ADM
reduction is the homogeneous time-translation orbit of the verified FRW
background. It is not a third physical homogeneous scalar.

For reduced velocity variables

```text
(R_dot, delta_rho_dot, vartheta_dot),
```

the exact on-shell zero-wavenumber identity is

```text
K_red(q=0) (H, rho_dot, mu)^T = 0.
```

The null vector is tangent to
`(ln a(t), rho(t), Theta(t))` under a homogeneous shift of time. The two
independent gauge-invariant matter combinations are

```text
Q_rho   = delta_rho - (rho_dot/H) R,
Q_theta = vartheta - (mu/H) R.
```

After phase normalization with `rho Q_theta`, their two-by-two kinetic block
has inertia `2 positive, 0 negative` at all 801 points of the representative
trajectory. Its minimum eigenvalue is `0.9372858341`; the maximum condition
number is `1.066910396`.

This resolves the earlier rank-loss hold as a gauge-endpoint issue. It does
not establish nonlinear weak coupling or close UVIR-003.

## Finite-q alignment

The smallest-eigenvalue direction approaches the homogeneous time-shift orbit
continuously:

| `q_phys/H` | Minimum alignment cosine |
|---:|---:|
| `10^-3` | `0.9999999999999994` |
| `10^-2` | `0.9999999999995369` |
| `10^-1` | `0.9999999953682775` |
| `1` | `0.9999536228783938` |
| `10` | `0.8461618629161758` |

The approach is therefore not inferred from the exactly homogeneous identity
alone; it is also visible in the nonzero-wavenumber eigenvectors.

## Strong-coupling decision

Dividing cubic vertices by the vanishing norm of this direction would
canonically normalize a gauge orbit and can manufacture a spurious
momentum-dependent cutoff. The proposed scale obtained from the collapsing
quadratic eigenvalue alone is therefore rejected as gauge dependent.

The physical strong-coupling scale remains **not yet derived**. Its
calculation requires:

1. the complete cosmological cubic action evaluated on the first-order lapse
   and scalar-shift constraints;
2. the quartic contact vertex combined with cubic exchange;
3. projection and canonical normalization of physical eigenmodes only;
4. an explicit `2-to-2` unitarity criterion;
5. comparison with `H`, physical momenta and the declared EFT cutoff.

The subsequent three-dimensional flat-decoupling audit derives the complete
khronon cubic operator basis and proves that explicit second-order lapse and
shift solutions cancel from the reduced cubic action. It also shows that a
non-collinear on-shell three-point process is kinematically forbidden for the
linear dispersion, so the physical target is the constrained `2-to-2`
amplitude rather than an isolated cubic coefficient.

## Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_scalar_low_q_gauge.py
```

Outputs:

- `Analysis/UVIR/UVIR-003/outputs/uvir003_scalar_low_q_gauge_summary.json`
- `Analysis/UVIR/UVIR-003/outputs/uvir003_scalar_low_q_gauge_alignment.csv`

Expected footer:

```text
UVIR-003 low-q scalar null identity: VERIFIED
Collapsing direction: HOMOGENEOUS_TIME_TRANSLATION_ORBIT
Gauge-invariant q=0 kinetic inertia: 2_POSITIVE_0_NEGATIVE
Naive strong-coupling inference from lambda_min: REJECTED
Physical cubic interaction scale: NOT_YET_DERIVED
Full UVIR-003 gate: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_LOW_Q_GAUGE_ORBIT_AUDIT
```
