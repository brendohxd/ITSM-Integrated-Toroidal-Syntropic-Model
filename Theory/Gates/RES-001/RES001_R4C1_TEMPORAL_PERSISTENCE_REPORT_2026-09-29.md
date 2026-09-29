# R4C1-S4H: moving B1 chart reconstructed; temporal estimate incomplete

Date: 2026-09-29. Owner: Master Test 1 / conditional R4C1-v1/B1.
The [frozen contract](RES001_R4C1_TEMPORAL_PERSISTENCE_CONTRACT_2026-09-29.md)
precedes the executable and both attempts. The result is
`INCOMPLETE_TEMPORAL_PERSISTENCE`: `physics_pass=false`,
`gate_effect=NONE`, `review_status=DEFERRED`, `Rule9_cleared=false`.

## Exact chart result and its domain

The pinned S4A original selected minor is

\[
 \Delta_q=-\frac{\sqrt{66}\,k^4}{396 C^2 a^6\rho_m}
 \left[396H^2a^2+18a^2\dot\psi^2
 +6a^2(\dot r^2+\dot u^2+\dot v^2)+k^2\right].
\]

S4H checks the saved formula exactly. Its S4F twelve-row chart uses the
same first eleven selected rows and replaces the old dust-tilt row by
exactly `p` times that row, `p=k/a`; hence its original-variable minor
is **exactly** `p Delta_q`, without relying on a numerical determinant.
The canonical `x,xdot` minor is `p Delta_q det(R)^2`, and the script
checks the saved canonical minor against `Delta_q det(R)^2` exactly.
The bracket is at least `k^2>0` for real finite fields. The chart is
therefore nonzero on the explicitly regular domain
`a>0, C>0, rho_m>0, H>0, k!=0`; `H>0` is required for the canonical
transformation `R`. Graph comparison additionally uses `p>=1`.

This is a conditional algebraic chart statement. B1's saved 801-point
numerical trajectory samples positive `a,H,rho_m` on `[0,4]`; those
samples do **not** certify exact positivity between points or an
interval-validated solution. The `H=0`, `rho_m=0`, `a=0`, zero-mode and
auxiliary/singular branches remain outside this result.

## Moving reconstruction, not a finite-time proof

At six registered times and four axial torus modes, the executable
evaluates the full pinned 16-by-12 graph, its time derivative and the
12-by-12 S2 generator on the saved B1 trajectory. It forms the moving
chart generator with **fixed comoving** `k`, including `Fdot`, `Rdot`,
`Mcdot` and `pdot=-Hp`. The 24 sampled modes have
`1.44997679871326 <= p <= 1608.49543863797`. The maximum sampled
chart condition number is about `1.49860924519891e7`. At 70-digit
arithmetic precision, maximum relative selected-graph reconstruction
error is `3.7661658900635e-17` after conversion to double for the
diagnostic record; maximum relative replay error against S4F's exact
initial-event `C` over the four `t=0` modes is
`5.640018222270919e-16`. Omitting `Fdot` or `pdot` at the lowest initial
mode gives relative errors `56.875309479909326` and
`0.4642450916172642`, respectively. These controls reject two
specific bookkeeping omissions.

At the largest mode, the sampled phase-pair antisymmetric `p^2`
coefficient stays near `sqrt(165)/33`; the sampled symmetric residual
is small. This is a finite-mode consistency observation, **not** an
exact moving `C_2` identity, a spectrum theorem, or a bound on the
full energy-rate matrix. Instantaneous generator eigenvalues in the
detail are diagnostics, not invariant physical growth rates. The B1
CSV is double-precision integration output; 70-digit matrix arithmetic
does not upgrade the underlying trajectory or prove behavior between
saved times.

The 144 exact moving `C_2/C_1` limits, their denominator domains,
spectral persistence, a smooth positive corrected metric `M(t,p)`,
uniform graph-equivalence and energy constants, and the physical
EFT wave-number range are **not derived**. No finite-time constrained
IVP, strong-hyperbolicity, all-sector stability or physical viability
claim follows. The next calculation must extract the moving leading
symbol exactly, then decide whether S4G's projector construction can
extend over a declared B1 interval; a sampled scan cannot make that
decision.

## Attempts, integrity and review debt

Attempt 01 used ordinary double precision and failed one of 189 local
checks: the registered `t=0`, `n=256` replay discrepancy was
`1.8604143424167406e-5`, above the frozen `1e-7` tolerance. Its
[summary](../../../Analysis/MasterTests/outputs/r4c1_s4h_attempt_01/summary.json)
has SHA-256 `fbc22c05b8f9e16bb4f93045cca95a73f74b3161004e6b964d703b6b86405288`;
its [detail](../../../Analysis/MasterTests/outputs/r4c1_s4h_attempt_01/detail.json)
has SHA-256 `fc81b1a9d8378d25613ad524ed45c3e48d7e31922b1bccad34d01c252f049404`.
Both remain preserved as failed evidence. The original attempt-01
executable hash is recorded in its summary, but that exact source copy
was **not archived before the high-precision revision**; attempt 01 is
not a source-complete replay packet.

The revised executable uses 70-digit `mpmath` arithmetic without
changing the frozen inputs, grid, equations or tolerance. Fresh
attempt 02 passes 189/189 **local** checks, zero failed/unknown, with
63 recorded source hashes; this is not a physics-gate pass. Its
[summary](../../../Analysis/MasterTests/outputs/r4c1_s4h_attempt_02/summary.json)
has SHA-256 `20eaa579780061a8f839a586f3c08725d5098a0e2527857a3c54032c55bc69d7`,
and [detail](../../../Analysis/MasterTests/outputs/r4c1_s4h_attempt_02/detail.json)
has SHA-256 `37068a4e93c919194a1d28608e2bab086dd0f36df1583b0d6b9fd589b3e32007`.
The [executable](../../../Analysis/MasterTests/test_01_r4c1_temporal_persistence.py)
is SHA-256 `1d966f7d3f6d973f855b46ef67295cbd811ae3e69bc4b919a0cc1f3320b79c20`;
the contract is SHA-256
`3bb4fa5ec045715f4667ce1260fce2a146238e45079c683ef9862260857eb26e`.
The listed output/contract sidecars match. Only fresh non-colliding
attempt numbers may be used for replay.

R9-MT1-S4H inherits R9-MT1-S4G/S4F/S4E/S4D/S4C/S4B/S4A/S3/S2/S1/
B1/VARIATION. Review of the exact minor, source/flow bookkeeping,
high-precision replay, failed first attempt and scope remains deferred.
The local chart/sampled reconstruction may guide the exact moving
symbol calculation. `HOLD_SUBSTANTIVE` applies to any finite-time,
EFT, all-sector, canonical or downstream use. Master Test 1 remains
held; Tests 2 and 3 are incomplete. MAT-001 stays `BLOCKED`, UVIR-003
`IN_PROGRESS`, `K_Q=NOT_DERIVED`, `V=NOT_COMPUTED`, Stage 4A closed.
No Derived or publication promotion follows.
