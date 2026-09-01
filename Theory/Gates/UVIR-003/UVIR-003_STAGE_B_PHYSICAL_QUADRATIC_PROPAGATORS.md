# UVIR-003 Stage B physical quadratic propagators

Date: 2026-07-29
Branch: `recovery/v12-core-architecture`
Scope: local adiabatic finite-`q` propagators and the exact projected
homogeneous internal channel

Follow-on status: the required fixed-comoving WKB and time-domain calculation
has now been completed. It removes the numerical uncertainty but retains a
mode-attribution HOLD; see
`UVIR-003_STAGE_B_FIXED_COMOVING_TRANSFER.md`. This report remains the
frozen-kernel checkpoint and should not be read as the latest transfer result.

## Decision

The physical-basis inverse quadratic kernels are now constructed for both
the finite-`q` sector and the separately projected exact `q=0` sector. Their
algebraic inversion, kinetic inertia, pole pairing and pole residues have
been audited on the representative evolving branch.

The result is

```text
HOLD_LOCAL_ADIABATIC_PHYSICAL_QUADRATIC_PROPAGATORS.
```

The hold is not caused by a ghost, a constraint pole or a failed inverse.
All sampled kinetic matrices are positive and all finite-`q` constraint
matrices remain nonsingular. The obstruction is that the frozen-background
pole spectrum develops complex conjugate pairs at low and intermediate
`q/H` on parts of the evolving representative branch. A clean four-mode
real-pole, positive-residue regime is present at `q/H=100`, but it cannot be
extended to the full sampled domain without a controlled WKB or time-domain
audit.

The physical `2-to-2` amplitude, unitarity bound, strong-coupling scale and
physical cutoff therefore remain **not yet derived**.

## 1. Finite-momentum physical kernel

Use the verified physical variables

```text
p = (Xi, Q_rho, Q_chi, Pi),

Xi    = (q_phys/H) R,
Q_rho = delta_rho - (rho_dot/H) R,
Q_chi = rho [vartheta - (mu/H) R].
```

For the metric-condensate block, write

```text
y = (R, delta_rho, vartheta) = T p_m,
p_m = (Xi, Q_rho, Q_chi),
dot(y) = T dot(p_m) + dot(T) p_m.
```

If the reduced quadratic Lagrangian is

```text
L2 = 1/2 dot(y)^T K dot(y)
     + dot(y)^T P y
     + 1/2 y^T C y,
```

then the transformed matrices are

```text
K_p = T^T K T,

P_p = T^T K dot(T) + T^T P T,

C_p = dot(T)^T K dot(T)
      + dot(T)^T P T
      + T^T P^T dot(T)
      + T^T C T.
```

The fixed-comoving-mode identities

```text
q_dot   = -H q,
H_dot   = -(rho_dot^2 + rho^2 mu^2)/(2 M_cos^2),
rho_ddot = -3 H rho_dot + rho mu^2 - V_rho,
mu_dot  = mu(-3H - 2 rho_dot/rho)
```

are included in `dot(T)`.

Define the antisymmetric gyroscopic matrix

```text
A_p = P_p - P_p^T.
```

The factorized force mode contributes

```text
D_Pi(omega,q)
  = K_Q omega^2 - gamma q^4/M_star^2.
```

The local frozen-time inverse kernel and Feynman propagator convention are

```text
D(omega,q) = omega^2 K_p + i omega A_p + C_p,

G_F(omega,q) = i [D(omega,q) + i epsilon]^-1.
```

Because `Pi` is factorized at quadratic order,

```text
det D_4
  = det D_(Xi,Q_rho,Q_chi)
    [K_Q omega^2 - gamma q^4/M_star^2].
```

## 2. Exact homogeneous internal channel

The exact centre-of-mass spatial channel is not obtained by setting `q=0`
inside the finite-`q` inverse.

At exact `q=0`:

1. remove `Sigma=-D^2 beta`;
2. remove the homogeneous `Xi` time-translation gauge orbit;
3. retain the lapse constraint;
4. retain the physical variables `(Q_rho,Q_chi,Pi)`.

For `V != 0`, the constraint projector is

```text
C_projected^-1 =
  [[-1/(2V), 0],
   [       0, 0]].
```

In the gauge with the homogeneous curvature orbit removed,

```text
delta_rho = Q_rho,
vartheta  = Q_chi/rho,
vartheta_dot = Q_chi_dot/rho
                - rho_dot Q_chi/rho^2.
```

The retained lapse source is

```text
J_N =
  -(V_rho + rho mu^2) Q_rho
  - rho_dot Q_rho_dot
  - rho^2 mu vartheta_dot.
```

Thus

```text
L2_q0,red = L2_q0,unconstrained + J_N^2/(4V).
```

Its Hessians define the exact projected `(Q_rho,Q_chi,Pi)` response kernel.
No homogeneous `Xi` propagator or scalar-shift inverse is introduced.

## 3. Verification

The representative diagnostic uses five trajectory snapshots and

```text
q_phys/H = 0.01, 0.1, 1, 10, 100.
```

The force normalization

```text
K_Q = gamma = M_star^2 = 1
```

is diagnostic only. It demonstrates the factorized pole and does not select
a physical parameter point.

Across all 25 finite-`q` samples:

| Diagnostic | Result |
|---|---:|
| Minimum physical kinetic eigenvalue | `0.006583568808` |
| Kinetic inertia | `4 positive, 0 negative` |
| Minimum constraint singular value | `0.06125947922` |
| Maximum off-shell inverse residual | `8.9134e-14` |
| Maximum plus/minus pole-pairing error | `3.8690e-15` |
| Maximum on-pole kernel residual | `1.4227e-15` |
| Minimum real positive-frequency residue denominator | `7.6841e-5` |

At `q/H=100`, all five snapshots have:

```text
4 positive real frequencies,
4 negative real frequencies,
positive positive-frequency residue denominators.
```

The minimum positive-frequency residue denominator in that high-`q`
subset is `0.1207408360`.

At lower and intermediate `q/H`, complex conjugate pole pairs appear on
parts of the representative trajectory. The exact projected `q=0` kinetic
matrix remains positive, but its frozen-background pole spectrum also
develops complex pairs away from the initial snapshot.

These complex local poles may represent a genuine infrared instability, or
they may reflect the failure of a frozen-time S-matrix description for modes
whose frequencies are not adiabatically separated from `H`. The present
calculation does not decide between those interpretations.

## 4. Consequence

### Derived and verified

- the finite-`q` physical inverse quadratic kernel;
- the exact projected `q=0` physical response kernel;
- the factorized `Pi` propagator;
- positive kinetic inertia over the representative scan;
- nonsingular finite-`q` constraints;
- numerical inverse closure;
- plus/minus pole pairing;
- positive residues for every sampled real positive-frequency pole;
- a clean high-`q` real-pole regime at `q/H=100`.

### Held

- a real-pole propagator basis over the full sampled finite-`q` domain;
- interpretation of the low/intermediate-`q` complex poles;
- an asymptotic scattering interpretation of the exact homogeneous channel.

### Not derived

- the nonzero-channel exchange amplitude;
- the exact centre-of-mass exchange contribution;
- the complete exchange-plus-contact `2-to-2` amplitude;
- a partial-wave or other declared unitarity bound;
- a strong-coupling scale or physical cutoff.

## 5. Next required calculation

Before assembling a physical amplitude:

1. separate leading WKB terms from first adiabatic corrections;
2. calculate a mode-by-mode adiabaticity measure such as
   `|omega_dot/omega^2|`;
3. evolve the time-dependent quadratic initial-value system through the
   complex-pole region using gauge-invariant observables;
4. determine whether the apparent infrared growth is basis/freeze
   dependent or persists in transfer matrices;
5. only then declare the momentum/frequency domain in which exchange
   propagators support an S-matrix interpretation.

High-`q` exchange may be assembled as a diagnostic cross-check, but it must
not be promoted to a global physical amplitude while this hold remains.

UVIR-003 remains in progress and MAT-001 remains blocked.

## 6. Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_physical_quadratic_propagators.py
```

Outputs:

```text
Analysis/UVIR/UVIR-003/outputs/uvir003_physical_quadratic_propagators_summary.json
Analysis/UVIR/UVIR-003/outputs/uvir003_physical_quadratic_propagators_poles.csv
```

Expected footer:

```text
Finite-q physical quadratic kernel: CONSTRUCTED
Exact q0 projected quadratic kernel: CONSTRUCTED
Propagator convention: VERIFIED
Representative finite-q kinetic inertia: 4_POSITIVE_0_NEGATIVE
Representative pole/residue audit: HOLD_LOCAL_ADIABATIC_POLE_OR_RESIDUE_AUDIT
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: HOLD_LOCAL_ADIABATIC_PHYSICAL_QUADRATIC_PROPAGATORS
```
