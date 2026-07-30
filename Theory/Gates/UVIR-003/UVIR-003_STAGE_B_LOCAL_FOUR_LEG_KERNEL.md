# UVIR-003 Stage B local four-leg kernel

Date: 2026-07-30

Branch: `recovery/v12-core-architecture`

Calculation status: **PASS**

Subgate:
`PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL`

Full UVIR-003 gate: **IN PROGRESS**

MAT-001: **BLOCKED**

Physical `2-to-2` status:
**LOCAL FROZEN KERNEL DERIVED; COSMOLOGICAL S-MATRIX NOT ESTABLISHED**

## Result

The verified analytic cubic sources, full finite-`q` physical propagator,
analytic quartic contact, and three constraint-induced quartic Schur pairings
have now been combined on one declared local four-leg kinematic slice.

Across 24 elastic coupled-mode cases and 72 channel contractions, every
combined kernel is finite, nonzero, real within numerical tolerance, and
permutation consistent. Record

`PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL`.

This closes the local frozen-time analytic kernel assembly for the tested
slice. It does not supply cosmological asymptotic states, an S-matrix
normalization, a unitarity bound, a strong-coupling scale, or a physical
cutoff.

## Four-leg kinematics

The initial frozen-time snapshot of the representative dimensionless FRW
branch is used. Four equal-magnitude spatial momenta point to the vertices of
a regular tetrahedron:

`sum_i k_i = 0`,

`k_i dot k_j = -q^2/3` for `i != j`.

Consequently, every `s`, `t`, and `u` pair partition has the same strictly
nonzero internal momentum

`q_K = 2q/sqrt(3)`.

The all-incoming elastic frequency assignment is

`(a+, b+, a-, b-)`.

Thus the three channel frequencies are respectively the sum, zero-difference,
and mode-difference combinations, while total external frequency closes
exactly.

The external samples are `q/H=47.5,50,75,100`. Their corresponding internal
ratios are:

| External `q/H` | Internal `q_K/H` | Maximum adiabaticity | Minimum `abs(omega)/H` | Admitted |
|---:|---:|---:|---:|:---:|
| `47.5` | `54.8483` | `0.0717483` | `53.6572` | yes |
| `50` | `57.7350` | `0.0644395` | `56.4888` | yes |
| `75` | `86.6025` | `0.0289169` | `84.7894` | yes |
| `100` | `115.4701` | `0.0171202` | `113.0785` | yes |

Each internal trajectory was rerun through the complete fixed-comoving
controlled-domain audit. Passing external legs was not used as a substitute
for this check.

## Mode normalization

The three local coupled positive-frequency modes are ordered
`physical_pair_1` through `physical_pair_3`. No infrared `Xi`-pure identity is
imposed at high momentum.

For inverse kernel

`D(omega,q)=omega^2 K+i omega(P-P^T)+C`,

each mode satisfies

`v_dagger [2 omega K+i(P-P^T)] v = 1`.

The maximum on-shell kernel residual is `3.42e-15`, and the maximum
residue-normalization error is `3.33e-16`.

## Physical exchange assembly

For each partition `(ab|cd)`, the two polarized cubic sources are evaluated
with their exact per-leg lapse and scalar-shift resolvers:

`J_ab(-K)=V_3[p_a,p_b,e_K]`,

`J_cd(K)=V_3[p_c,p_d,e_-K]`.

The physical exchange contribution is

`W_ex(ab|cd) = -J_cd(K)^T D(K)^(-1) J_ab(-K)`.

The sum includes all three `s`, `t`, and `u` partitions. The maximum inverse
closure error is `4.75e-16`, and the minimum normalized separation from a
local propagator pole is `0.171148`.

## Reduced quartic contact

The polarized direct analytic contact is the verified

`d^4 L4[x,z1]/(d epsilon_1 ... d epsilon_4)`.

For each partition, the constraint pair source

`B_ab=(B_N, B_Sigma)`

is contracted through the exact nonzero-channel constraint inverse:

`W_Schur(ab|cd)=-B_cd^T C(q_K)^(-1) B_ab`.

The complete reduced contact on this slice is

`W_red = W_contact + sum W_Schur`,

and the assembled local kernel is

`W_local = W_red + sum W_ex`.

All channels are strictly nonzero, so the separate exact-`q_K=0` homogeneous
projector is not invoked in this calculation.

## Numerical audit

| Diagnostic | Result |
|---|---:|
| Elastic mode-pair cases | `24` |
| Physical channel contractions | `72` |
| Maximum external frequency closure divided by `H` | `0` |
| Maximum cubic-source leg-swap error | `5.99e-16` |
| Maximum component permutation error | `1.71e-14` |
| Maximum inverse closure error | `4.75e-16` |
| Minimum distance to a local pole | `0.171148` |
| Maximum total imaginary fraction | `1.93e-16` |
| Combined real-kernel range | `-62.1674` to `1.78508` |
| Cancellation-ratio range | `0.00502092` to `0.101546` |

The cancellation ratio is

`abs(W_local)/(abs(W_contact)+sum abs(W_Schur)+sum abs(W_ex))`.

The lower end shows that the combined kernel can be about `0.5%` of the sum
of absolute component magnitudes. This cancellation is numerically resolved,
but it makes the result sensitive to omitted physics and background or
kinematic changes. It must not be interpreted as a robust suppression scale
without further audits.

## Scientific boundary

This pass establishes:

- a complete elastic four-leg all-incoming convention;
- independently admitted nonzero `s`, `t`, and `u` channel trajectories;
- matched left/right physical cubic-source contractions;
- all three physical exchange contributions;
- the analytic quartic contact;
- all three nonzero-channel constraint-Schur contributions;
- a finite, real, nonzero and permutation-consistent local combined kernel.

It does not establish:

- asymptotic in/out states on the evolving FRW background;
- a cosmological S-matrix amplitude or cross section;
- an optical-theorem or partial-wave unitarity normalization;
- a strong-coupling scale or physical EFT cutoff;
- robustness away from the regular-tetrahedral kinematic slice;
- the exact nonanalytic `|grad(pi)|^3` contribution on a nonzero-gradient
  background;
- MAT-001.

## Reproduction

```powershell
python Analysis/UVIR/UVIR-003/uvir003_local_four_leg_kernel.py
```

Outputs:

- `Analysis/UVIR/UVIR-003/outputs/uvir003_local_four_leg_kernel_summary.json`
- `Analysis/UVIR/UVIR-003/outputs/uvir003_local_four_leg_kernel.csv`

Expected footer:

```text
Nonzero tetrahedral internal trajectories: ADMITTED
Matched physical exchange contractions: ASSEMBLED
Reduced quartic contact including constraint Schur: ASSEMBLED
Local frozen-time on-shell four-leg kernel: VERIFIED
Cosmological S-matrix amplitude: NOT_ESTABLISHED
Physical cutoff: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL
```

## Next required calculation

1. Extend the local kernel away from the regular-tetrahedral slice and audit
   approach to internal poles and exact homogeneous channels.
2. Define an adiabatic wave-packet or in-in observable normalization rather
   than assuming a cosmological S-matrix.
3. Derive the held exact-`|grad(pi)|^3` contribution on a declared
   nonzero-gradient background.
4. Only then formulate and test a declared perturbative-unitarity or
   EFT-validity criterion.
