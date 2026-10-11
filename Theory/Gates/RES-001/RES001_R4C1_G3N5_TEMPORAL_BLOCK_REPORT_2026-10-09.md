# G3N5 independent temporal-block report

Date: 9 October 2026. Version 1. Owner: existing G3N5 kernel checkpoint.
Conditional local research; Rule-9 DEFERRED; physics_pass=false; gate_effect=NONE.

## Outcome and what remains pending

The independent temporal-block executable passes 54/54 local controls and
replays exactly without changing its six output/sidecar files, lengths, or
last-write timestamps. It derives the pure time-velocity matrix for all 22
unreduced fields directly from the four-dimensional connection, retaining
all three shift/boost components and the independent frame-normal variation.

The full G3N5 110-jet executable remains live at the last session poll. Its
receipt is not yet available. Comparison with that kernel is therefore
explicitly pending; this control does not establish the G3N5 result, compatible
initial data, a physical Hessian, or full nonlinear evolution.

## Exact independent quadratic form

Let Mdot be the symmetric spatial metric perturbation's time derivative,
sigma=Tr(Mdot), and use MP2=M_P^2, MU2=M_U^2. Define

```text
c13=c1+c3
c14=c1+c4
c_theta=c1+3c2+c3
c_sum=c1+c2+c3+c4.
```

The pure velocity coefficient of the action density divided by background a^3 is

```text
L_vel = [(MP2-MU2 c13) Tr(Mdot^2) - (MP2+MU2 c2) sigma^2]/8
        - MU2 c_sum nu_dot^2/2 - MU2 c2 nu_dot sigma/2
        + MU2 c14 (Vx_dot^2+Vy_dot^2+Vz_dot^2)/2
        + [du_dot^2+dv_dot^2+dr_dot^2
           + K_Q Pi_dot^2+epsilon0 C^2 T_dot^2]/2.
```

Here C=exp(beta psi0). The frame-normal variable nu is not eliminated before
variation. The unit multiplier still imposes nu=0 and requires its time
preservation in the later constrained solve. A raw normal kinetic coefficient
is therefore not, by itself, a physical particle or ghost statement.

All 484 entries of the 22-by-22 Hessian from the direct covariant calculation
match the separately written form above exactly. Its seven zero velocity rows
are alpha, Sx,Sy,Sz, Em,Z,LambdaU. Their Euler/constraint equations must still
be retained. In particular a positive dust-clock kinetic term does not eliminate
the dust multiplier equation. Z's zero velocity row concerns this aligned
background only, not the earlier tilted dust-clock regulator block.

## Trace/normal block and singular-domain controls

Using Mdot=(sigma/3) I for this algebraic subblock, not as a physical ansatz,

```text
K_(sigma,nu) = [[-(2 MP2+MU2 c_theta)/12, -MU2 c2/2],
               [-MU2 c2/2,              -MU2 c_sum]]

det K_(sigma,nu)
 = MU2 [(2 MP2+MU2 c_theta)c_sum - 3 MU2 c2^2]/12.
```

The exact raw matrix rank is 15 on both registered generic coefficient sets.
This is not a count of propagating physical degrees of freedom. Exact boundary
controls give ranks 11 at MU2=0; 14 at K_Q=0 or epsilon0=0; 12 at c14=0;
10 at MP2-MU2 c13=0; and 14 at the registered c2=0,c4=-c1-c3 normal singular
control. These checks expose parameter-dependent raw degeneracy, not a physical
constraint classification or a healthy continuous GR limit.

Fourteen mutated-form comparisons (seven mutations at each coefficient set)
reject removing nu, removing its metric-trace mixing, dropping c4 from the
boost coefficient, reversing the Einstein sign, inserting a 2/3 projector
factor into the metric coefficient, inventing a lapse velocity, or replacing
C^2 by C^4 in the dust velocity coefficient.

## Independent numerical density control

Two all-field velocity jets were evaluated with a separately rebuilt,
unexpanded four-dimensional point-density at 50 decimal digits. At
d=1e-3,5e-4,2.5e-4 the normalized errors are

```text
case 0: 2.05466e-45, 1.54185e-44, 6.88738e-44
case 1: 5.50080e-46, 3.64046e-45, 2.06793e-44.
```

All satisfy the preregistered <=1e-38 bound. Error increases as the step shrinks
because this particular point-density is exactly quadratic and subtraction
reaches the arithmetic floor; no monotone-convergence claim is made.
These are illustrative local operator jets, not on-shell spacetime solutions
or microscopic K_Q matching values.

## Reproducibility and source preservation

[Contract](RES001_R4C1_G3N5_TEMPORAL_BLOCK_CONTRACT_2026-10-09.md), SHA-256
a71a15d2e2d8620ce7b58666abed3eb512d31138a7628c2c648c8fe94ab0adfe.
[Executable](../../../Analysis/MasterTests/test_01_r4c1_g3n5_temporal_block_v1.py), SHA-256
917724cb2cccf29bfebb594bc58b8f43eeab1af477508f08308fa4c06f8f36ee.
Both have matching sidecars. Output directory:
Analysis/MasterTests/outputs/r4c1_g3n5_time_block_attempt_01.

| Artifact | SHA-256 |
| --- | --- |
| summary.json | 5f079b1e9848dcbdcebac5ffeb7944d9d24f454684b1e0b288f5cebbfd84f265 |
| formulas.json | 2a900b83fdbf966390ac0fdbdec5e755d17c2e9ca224947c38cfd2c0e3ebbaaf |
| independent.json | d0074be2860e0d9a6a687d7936e6213366716fa2c57eb1ad6808e7c69a7dc591 |

All 128 inherited/new source pins and 125 available sidecars match before and
after execution. The same three inherited missing sidecars remain explicit.
The original G3 finite-difference balance failure and both superseded G3N3
attempt-01 failures remain in independent.json; no original file/hash was edited.

```powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3n5_temporal_block_v1.py
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3n5_temporal_block_v1.py --replay Analysis/MasterTests/outputs/r4c1_g3n5_time_block_attempt_01
```

Both exit 0. The new-output command refuses an existing destination. Private
execution/replay logs remain under ignored .local/itsm-context. The optimizer's
receipt summary was followed through its full saved artifact to EOF, including
pending requirements, inherited failures, and every declared hold.

## Next owning step and unchanged goal

Inspect the existing G3N5 run's actual terminal output, every failure/unknown,
and coverage. If it succeeds, replay it read-only and perform the independent
484-entry comparison in a new output directory with --compare-kernel. That
option has not yet been executed or validated against a completed parent.
Only then proceed to the coupled constraint/initial-data and response solve,
with homogeneous data, unsmoothed force, and its harmonic tail retained.

This control does not supply the spatial/mixed operator, physical spectrum,
Cauchy/DAE domain, full T3 evolution, cutoff or healthy continuous GR limit.
The eight-route goal and Tests 1-3 remain incomplete. Canonical K_Q and V remain
uncomputed, and the earlier C1/C2 findings are not altered.

Review dependency: R9-MT1-G3N5-TIME, inheriting R9-MT1-G3N5/G3N4 and all prior
scientific/review debt; DEFERRED, not cleared. Tests 1-3 HOLD_SUBSTANTIVE;
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; TOP-X4 unchanged; physics_pass=false; gate_effect=NONE.
No action replacement, manuscript/PDF/vault change, provider dispatch,
commit, push, canonical promotion or publication.
