# UVIR-003 Stage-B source-to-observable retarded response

Date: 2026-07-29

Gate: UVIR-003

Calculation status: PASS

Subgate status:
`PASS_GAUGE_PROJECTED_MATTER_RESPONSE_SURVIVES_WITH_SCOPE`

Full UVIR-003 gate: IN PROGRESS

MAT-001: BLOCKED

Physical `2-to-2` amplitude: NOT YET DERIVED

## 1. Question

The preceding mode-resolved audit found a converged, `Xi`-seeded infrared
transfer, but an off-axis complex quartet prevented a unique continuous
rank-two split between the gauge-continuation and retained-matter pole pairs.
That result could not determine whether removing the homogeneous
time-translation source also removed the large response in retained
observables.

This audit asks the narrower gauge-invariant question:

> Does a retarded response from generalized sources with no homogeneous
> time-translation or direct `Xi` support remain amplified when it is read
> only through `Q_rho` and `Q_chi`?

## 2. ITSM sector and scope

The coupled finite-momentum scalar block is

```text
p = (Xi, Q_rho, Q_chi),

Xi    = (q_phys/H) R,
Q_rho = delta_rho - (rho_dot/H) R,
Q_chi = rho [vartheta - (mu/H) R].
```

The full finite-`q` physical basis also contains the Track-A force mode `Pi`.
It is not discarded from the ITSM framework. At quadratic order on the
homogeneous zero-gradient branch its inverse kernel factorizes exactly,

```text
D_Pi = K_Q omega^2 - gamma q_phys^4/M_star^2,
```

so it is outside the coupled complex-quartet mixing block tested here.

The calculation retains the current recovery-branch action and conventions:
Einstein-Hilbert gravity, the independent constrained timelike aether, the
complex condensate, its alignment term, and the factorized Track-A force
sector. The parameter values are the existing dimensionless representative
branch, not a physical cosmological fit.

## 3. Gauge-projected sources and observables

Let

```text
S_m = [(0,1,0)^T, (0,0,1)^T]
```

select generalized impulses conjugate only to `(Q_rho,Q_chi)`. In the original
`(R,delta_rho,vartheta)` coordinates the corresponding covectors are

```text
s_rho = (-rho_dot/H, 1, 0),
s_chi = (-rho mu/H, 0, rho).
```

For the homogeneous time-translation orbit

```text
g_t = (H, rho_dot, mu),
```

both satisfy `s_A . g_t = 0`. Thus the sources annihilate the homogeneous
gauge orbit before any propagation is performed.

For the quadratic equation

```text
K p_ddot
 + [K_dot + 3 H K + P - P^T] p_dot
 + [P_dot + 3 H P - C] p
 = S_m f,
```

an impulsive source enters the first-order state `x=(p,p_dot)` through

```text
B_x = (0, K^(-1) S_m)^T.
```

The exact evolution is performed in the kinetic-normalized state

```text
u = (K^(1/2) p, K^(1/2) p_dot/H).
```

Source columns and observable rows are orthonormalized only inside their
two-dimensional retained-matter subspaces. The readout contains positions
`(Q_rho,Q_chi)` only. It has no `Xi` or velocity support.

## 4. Retarded response

Let `T_u(t,t_s)` be the exact time-dependent transfer matrix. The normalized
retarded response is

```text
R_m(t,t_s) = C_m(t) T_u(t,t_s) B_m(t_s),
t >= t_s.
```

Every source time and every later observation time on the 801-point
trajectory are evaluated. Interval propagators use midpoint-Magnus evolution.
The fine calculation uses 32 substeps per trajectory interval for the
`q/H=0.01` initial mode and is compared with 16 substeps.

The frozen generator is used only to mark the complex-quartet interval. It is
not exponentiated to compute the retarded response.

## 5. Projection and numerical checks

Across all five cases:

- the largest time-orbit annihilation residual is below `5.66e-17`;
- direct `Xi` source support is below `7.61e-21`;
- direct `Xi` readout support is below `4.94e-21`;
- the impulsive position jump and readout velocity support are exactly zero;
- source and readout orthonormality residuals are below `1.74e-15`;
- the largest coarse/fine response error is `5.48e-5`.

These checks separate the result from a direct excitation or observation of
the finite-`q` `Xi` gauge-continuation coordinate.

## 6. Baseline result

The baseline quartet occupies

```text
2.90 <= t <= 6.19,
0.0147614 <= q_phys/H <= 0.0178490.
```

The maximum normalized retained-matter response through that interval is

```text
||R_m||_2 = 1.43264e19.
```

It is sourced at the initial `q_phys/H=0.01` point and reaches its maximum at
`q_phys/H=0.0177456`. The maximizing source and output mixtures are

```text
source:  0.979149 Q_rho weight + 0.0208514 Q_chi weight,
output:  0.999725 Q_rho weight + 0.000275417 Q_chi weight.
```

The maximum response along paths that do not touch the detected quartet is
`4.13483e6`. The response therefore does not appear only because a nominal
rank-two pole label was continued through the quartet.

## 7. Nearby robustness

| Case | Coarse/fine error | Through-quartet response | Real-pole-only response | Input `Q_rho` weight | Output `Q_rho` weight |
|---|---:|---:|---:|---:|---:|
| baseline | `2.45742e-5` | `1.43264e19` | `4.13483e6` | `0.979149` | `0.999725` |
| on-shell `rho_initial=0.95` | `5.47691e-5` | `2.67849e17` | `8.13878e5` | `0.977043` | `0.999995` |
| on-shell `rho_initial=1.05` | `2.70658e-5` | `9.75967e19` | `1.36479e7` | `0.981108` | `0.998634` |
| `zeta_align=0.8` | `2.45839e-5` | `1.52756e19` | `4.40355e6` | `0.974929` | `0.999730` |
| `zeta_align=1.2` | `2.45632e-5` | `1.34410e19` | `3.88392e6` | `0.983026` | `0.999719` |

All tested cases retain an amplified `Q_rho/Q_chi` response after direct
`Xi` and time-translation source support is removed. The magnitude is
branch-sensitive, while the structural conclusion is robust in the tested
neighborhood.

## 8. Classification

Record

```text
PASS_GAUGE_PROJECTED_MATTER_RESPONSE_SURVIVES_WITH_SCOPE
```

for this bounded subcalculation.

This resolves the preceding attribution hold in the following limited sense:

- the large response cannot be dismissed solely as direct sourcing or
  readout of the homogeneous time-translation continuation;
- retained gauge-invariant matter observables respond strongly to
  retained-matter generalized impulses;
- no rank-two pole identity is assigned inside the complex quartet.

It does **not** establish:

- an all-background or asymptotic instability theorem;
- a physical cosmological parameter selection;
- a measured observable amplitude;
- an S-matrix element, unitarity violation, strong-coupling scale, or cutoff;
- MAT-001 matter coupling.

UVIR-003 therefore remains in progress and MAT-001 remains blocked.

## 9. Next required calculation

1. Identify a controlled real-pole, adiabatic exchange domain.
2. Project the verified cubic and reduced-quartic kernels onto the retained
   source and observable channels.
3. Assemble the gauge-regular exchange plus reduced-contact cosmological
   `2-to-2` amplitude.
4. Apply a declared unitarity criterion only to that completed physical
   amplitude.
5. Repeat any later physical parameter selection against observational and
   EFT constraints.

## 10. Reproduction

From the repository root:

```powershell
python Analysis\UVIR\UVIR-003\uvir003_source_observable_retarded_response.py
```

Deterministic outputs:

```text
Analysis/UVIR/UVIR-003/outputs/uvir003_source_observable_retarded_response_summary.json
Analysis/UVIR/UVIR-003/outputs/uvir003_source_observable_retarded_response_sources.csv
Analysis/UVIR/UVIR-003/outputs/uvir003_source_observable_retarded_response_trace.csv
```
