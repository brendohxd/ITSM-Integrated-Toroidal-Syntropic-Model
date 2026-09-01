# UVIR-003 Stage B fixed-comoving adiabaticity and transfer audit

Date: 2026-07-29
Branch: `recovery/v12-core-architecture`
Scope: full time-dependent finite-`q` scalar transfer on the representative
evolving branch

Follow-on status: the required mode-resolved and nearby-robustness audit is
complete. Transfer and pair-assignment numerics pass, but an off-axis
complex quartet prevents a unique continuous real rank-two split between
the gauge-continuation and retained-matter pole pairs. The current status is
`HOLD_COMPLEX_QUARTET_IR_MODE_ATTRIBUTION`; see
`UVIR-003_STAGE_B_MODE_RESOLVED_TRANSFER_ROBUSTNESS.md`. This report remains
the full-transfer checkpoint and not the latest attribution result.

## Decision

The local frozen-pole HOLD has been advanced to a converged time-dependent
calculation at fixed comoving momentum. The result is

```text
HOLD_TIME_DEPENDENT_INFRARED_TRANSFER_INTERPRETATION.
```

The numerical transfer problem is resolved. The remaining hold is physical:
the deepest sampled infrared trajectory has very large gauge-invariant
phase-space amplification, but the present full-transfer singular value does
not identify which instantaneous physical eigenmode carries that gain.
Background squeezing and time-dependent normalization also produce nontrivial
gain in the clean high-momentum control. A mode-resolved transfer projection
is therefore required before the infrared result can be classified as a
physical instability.

The physical `2-to-2` amplitude, unitarity bound, strong-coupling scale, and
physical cutoff remain **not yet derived**.

## 1. Full time-dependent system

Use the finite-momentum physical variables

```text
p = (Xi, Q_rho, Q_chi)
```

and follow fixed comoving momentum `k`, so

```text
q_phys(t) = k/a(t).
```

For

```text
L2 = a^3 [
       1/2 p_dot^T K p_dot
       + p_dot^T P p
       + 1/2 p^T C p
     ],
```

the exact second-order equation is

```text
K p_ddot
+ [K_dot + 3 H K + P - P^T] p_dot
+ [P_dot + 3 H P - C] p
= 0.
```

This retains the coefficient derivatives and volume dilution omitted from a
frozen-background pole calculation.

The calculation independently reconstructs the canonical momentum

```text
pi_p = a^3 (K p_dot + P p)
```

and verifies the equivalent Hamiltonian generator for `(p,pi_p)`. The
time-domain transfer is evaluated in the declared gauge-invariant,
kinetic-normalized phase-space variables

```text
u = (K^(1/2) p, K^(1/2) p_dot/H).
```

This normalization is explicit, but its finite-duration singular values are
not Lyapunov exponents and are not invariant under arbitrary time-dependent
renormalizations.

## 2. Numerical method and verification

The 801-point verified FRW trajectory is used without changing the background.
Coefficient derivatives use second-order trajectory differences. The transfer
matrix is evolved with piecewise-linear generator interpolation and midpoint
Magnus matrix exponentials.

The default four substeps per trajectory interval are sufficient for all
sampled modes except the deepest infrared mode. The `q/H=0.01` trajectory
uses 32 adaptive substeps.

Across all five fixed-comoving trajectories:

| Diagnostic | Result |
|---|---:|
| Maximum coarse/fine transfer error | `1.30353e-4` |
| Maximum second-order/canonical residual | `1.05500e-4` |
| Maximum local Hamiltonian-generator defect | `4.06385e-16` |
| Minimum kinetic eigenvalue | `0.00226190` |
| Transfer numerical status | `PASS` |

The numerical hold from the first canonical fundamental-matrix attempt is
therefore removed. The current HOLD is not a solver-convergence failure.

## 3. Fixed-comoving results

The representative initial ratios are

```text
q_phys(t=0)/H(t=0) = 0.01, 0.1, 1, 10, 100.
```

Because `aH` decreases on the branch, the corresponding endpoint ratios are
approximately

```text
0.01775, 0.17746, 1.77456, 17.7456, 177.456.
```

| Initial `q/H` | Complex frozen-pole time fraction | Maximum normalized phase-space gain | Endpoint gain | Coarse/fine error |
|---:|---:|---:|---:|---:|
| `0.01` | `1.0000` | `1.37708e27` | `1.33159e27` | `1.30353e-4` |
| `0.1` | `1.0000` | `27.9986` | `10.6398` | `4.33514e-5` |
| `1` | `1.0000` | `26.6706` | `7.68450` | `4.63432e-5` |
| `10` | `0.18976` | `16.1049` | `5.00649` | `1.69649e-5` |
| `100` | `0` | `138.849` | `42.5094` | `3.57751e-5` |

The high-momentum trajectory is a controlled local-adiabatic subset:

```text
all tracked frozen poles real,
maximum |omega_dot/omega^2| = 0.0221546,
maximum force-mode adiabaticity = 0.000831236.
```

The factorized force mode has

```text
omega_Pi = sqrt(gamma/(K_Q M_star^2)) q_phys^2,
|omega_Pi_dot/omega_Pi^2| = 2H/omega_Pi.
```

It is adiabatic for the `q/H=10` and `100` trajectories under the diagnostic
normalization, but not in the lower-momentum trajectories.

## 4. What the transfer changes

The local frozen-pole growth integral is not quantitatively reliable in the
nonadiabatic domain. For example:

```text
initial q/H = 0.1:
integral max(Im omega) dt = 271.72,
full normalized transfer gain = 27.999.

initial q/H = 1:
integral max(Im omega) dt = 34.90,
full normalized transfer gain = 26.671.
```

Thus the frozen complex poles cannot be exponentiated to infer physical
growth. The time dependence that was omitted by the local kernel materially
changes the result.

The deepest infrared trajectory is different:

```text
initial q/H = 0.01:
maximum normalized transfer gain = 1.37708e27,
endpoint normalized transfer gain = 1.33159e27,
coarse/fine error = 1.30353e-4.
```

This is a converged candidate infrared amplification. It is not yet a physical
instability claim because:

1. the reported quantity is the largest singular value of the full
   kinetic-normalized phase-space transfer;
2. it has not been projected onto a continuously tracked physical eigenmode;
3. the high-`q` control also develops finite background squeezing despite
   having real adiabatic poles;
4. only one representative dimensionless branch has been tested;
5. the exact homogeneous `q=0` sector is deliberately not inferred from these
   finite-`k` trajectories.

## 5. Consequence

### Derived and verified

- fixed-comoving finite-`q` physical mode tracking;
- the exact time-dependent second-order equation including `K_dot`, `P_dot`,
  and `3H` terms;
- independent equivalence to the canonical Hamiltonian system;
- converged kinetic-normalized transfer matrices for all five trajectories;
- the failure of frozen-pole exponentiation in the nonadiabatic domain;
- a controlled high-`q` local-adiabatic subset;
- a converged candidate amplification in the deepest sampled infrared mode.

### Held

- attribution of the infrared gain to a continuously tracked physical
  eigenmode;
- interpretation of that gain as instability, gauge-continuation behavior, or
  background squeezing;
- robustness under nearby background and parameter variations;
- a global S-matrix domain.

### Not derived

- a finite-channel exchange amplitude;
- the projected centre-of-mass exchange contribution;
- the complete exchange-plus-contact `2-to-2` amplitude;
- a unitarity bound, strong-coupling scale, or physical cutoff.

## 6. Next required calculation

1. construct the instantaneous physical eigenvectors with kinetic
   normalization;
2. parallel-transport their phases and resolve avoided crossings;
3. project the full transfer onto each tracked mode;
4. identify whether the `q/H=0.01` gain belongs to the finite-`q` continuation
   of the homogeneous gauge orbit or to a retained matter mode;
5. repeat any retained growing mode under nearby branch/parameter variations;
6. only then declare a controlled exchange domain.

High-`q` exchange remains useful as a diagnostic cross-check, but no global
physical amplitude should be claimed while this hold remains.

UVIR-003 remains in progress and MAT-001 remains blocked.

## 7. Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_propagator_adiabaticity_transfer.py
```

Outputs:

```text
Analysis/UVIR/UVIR-003/outputs/uvir003_propagator_adiabaticity_transfer_summary.json
Analysis/UVIR/UVIR-003/outputs/uvir003_propagator_adiabaticity_transfer.csv
```

Expected footer:

```text
Fixed-comoving physical mode tracking: COMPLETE
Frozen-pole adiabaticity audit: COMPLETE
Gauge-invariant time-dependent transfer: COMPLETE
Transfer Hamiltonian/equivalence/convergence checks: PASS
High-q controlled adiabatic subset: PASS
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: HOLD_TIME_DEPENDENT_INFRARED_TRANSFER_INTERPRETATION
```
