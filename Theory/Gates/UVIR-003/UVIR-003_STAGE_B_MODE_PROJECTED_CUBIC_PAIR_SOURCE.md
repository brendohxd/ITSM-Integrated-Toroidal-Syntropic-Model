# UVIR-003 Stage B mode-projected cubic pair source

Date: 2026-07-29

Branch: `recovery/v12-core-architecture`

Calculation status: **PASS**

Subgate: `PASS_MODE_PROJECTED_CUBIC_PAIR_SOURCE`

Full UVIR-003 gate: **IN PROGRESS**

MAT-001: **BLOCKED**

Physical `2-to-2` amplitude: **NOT YET DERIVED**

## Result

The verified analytic finite-`q` cubic kernel has now been contracted with
two actual residue-normalized on-shell coupled physical-mode legs. The third
leg is retained as an off-shell four-component pair-source covector

`J_K = (J_Xi, J_Qrho, J_Qchi, J_Pi)`.

All 48 audited sources are finite and nonzero. Applying the already verified
finite-`q` inverse quadratic kernel produces finite responses with numerical
inverse closure below `5.53e-16`.

This establishes the missing interface between the factorized cubic
functional and local physical pole modes. It does not yet contract two pair
sources into an exchange amplitude.

## Kinematic prescription

The audit uses the initial frozen-time snapshot of the representative
dimensionless evolving branch. Each tested spatial channel is equilateral:

`q_1 = q_2 = q_K`, with `k_1+k_2+k_K=0`.

Every external and internal momentum therefore lies on the same admitted
controlled-domain trajectory. The admitted initial samples are

`q/H = 47.5, 50, 75, 100`.

The two external coupled legs use

`p_dot_i = -i Omega_i p_i`.

Both the sum-frequency `(+,+)` and difference-frequency `(+,-)` pairings are
audited. The all-incoming channel frequency is

`Omega_K = -(Omega_1+Omega_2)`.

The omitted `(-,-)` and `(-,+)` cases are respectively complex conjugates or
external-leg swaps of the audited cases on this real background.

## Mode normalization

At each `q/H`, the three positive-frequency coupled poles are ordered locally
as `physical_pair_1`, `physical_pair_2`, and `physical_pair_3`. No infrared
`Xi`-pure identity is assigned.

For inverse kernel

`D(omega,q)=omega^2 K+i omega(P-P^T)+C`,

each mode vector is normalized by

`v_dagger [2 omega K+i(P-P^T)] v = 1`.

Across the twelve sampled local modes:

- maximum on-shell kernel residual: `3.42e-15`;
- maximum residue-normalization error: `3.33e-16`;
- all positive-frequency residues remain positive.

## Pair-source construction

The complete per-leg lapse and scalar-shift resolvers are evaluated after the
two external modes and one internal coordinate basis vector are inserted.
For internal component `A`,

`J_A = V_3[p_1,p_2,e_A]`,

with `dot e_A=-i Omega_K e_A`.

This includes the time-dependent physical-basis map and the full analytic
gravity, aether, condensate, alignment, and Track-A contributions already
present in the verified cubic kernel.

The ordinary Taylor kernel of the held nonanalytic `|grad(pi)|^3` term is not
silently added. That term still requires a declared nonzero-gradient local
background.

## Numerical audit

The 48 cases comprise:

- four admitted momentum trajectories;
- six unordered pairs of the three coupled modes; and
- two independent external-frequency sign patterns.

| Diagnostic | Result |
|---|---:|
| Pair-source norm range | `17.4101` to `770.479` |
| Inverse-response norm range | `8.28461e-3` to `6.53619` |
| Maximum external-leg swap error | `6.10882e-16` |
| Maximum inverse-closure error | `5.52503e-16` |
| Minimum constraint-determinant relative margin | `1.22180` |
| Minimum distance to a local pole | `0.279523` |
| Inverse-kernel condition-number range | `6.77475e3` to `5.18769e5` |
| Maximum `Pi` fraction of a coupled-coupled source | `0` |

The largest response norm occurs for two `physical_pair_2` positive-frequency
legs at `q/H=100`; its channel lies `0.377288` in the declared normalized
distance from the nearest local pole. It is a dimensionless structural
diagnostic, not a measured amplitude.

## External-leg permutation

For the equilateral geometry, swapping external legs 1 and 2 while swapping
their mode/frequency data leaves the pair-source covector invariant to a
maximum relative error of `6.11e-16`. This verifies that the numerical
constraint substitution preserves the permutation symmetry of the polarized
cubic kernel.

## Track-A force component

For two external legs drawn from the coupled `(Xi,Q_rho,Q_chi)` block, the
analytic cubic pair source has

`J_Pi = 0`

in every audited case. This agrees with the quadratic factorization and the
fact that the analytic Track-A cubic terms contain the force fluctuation at
least quadratically. It does not remove `Pi` from the full theory and does not
classify the held nonanalytic local-gradient vertex.

## Scientific boundary

This pass establishes:

- residue-normalized on-shell coupled external legs;
- finite nonzero cubic pair-source covectors;
- correct channel-frequency insertion on the off-shell leg;
- constraint-resolver compatibility;
- external-leg permutation symmetry;
- finite nonzero-channel inverse-kernel responses;
- numerical separation from sampled propagator poles.

It does not establish:

- a left/right pair-source contraction;
- a summed `s`, `t`, and `u` exchange contribution;
- the reduced quartic contact contribution;
- an exchange-plus-contact `2-to-2` amplitude;
- an in/out state or S-matrix on the evolving cosmological background;
- a unitarity bound, strong-coupling scale, or physical cutoff.

## Reproduction

```powershell
python Analysis/UVIR/UVIR-003/uvir003_mode_projected_cubic_pair_source.py
```

Outputs:

- `Analysis/UVIR/UVIR-003/outputs/uvir003_mode_projected_cubic_pair_source_summary.json`
- `Analysis/UVIR/UVIR-003/outputs/uvir003_mode_projected_cubic_pair_source.csv`

Expected footer:

```text
Residue-normalized coupled mode legs: VERIFIED
Mode-projected cubic pair sources: NONZERO_AND_FINITE
External-leg permutation audit: PASS
Nonzero-channel inverse response: VERIFIED
Physical 2-to-2 amplitude: NOT_YET_DERIVED
UVIR-003: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_MODE_PROJECTED_CUBIC_PAIR_SOURCE
```

## Next required calculation

1. Declare a complete four-leg in/out kinematic configuration inside the
   controlled domain.
2. Construct matched left and right pair sources for each nonzero channel.
3. Contract them through the finite-`q` propagator and sum the declared
   channels.
4. Apply the separate homogeneous projector to exact `q_K=0` channels.
5. Add the reduced quartic contact before applying any unitarity criterion.
