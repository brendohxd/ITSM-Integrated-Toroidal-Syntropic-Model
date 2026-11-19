# A16.2 matched preparations: current flux prevents reservoir isolation

16 November 2026. High retained. Conditional initial comparison within the
unchanged R4C1/B1 linear export. Both original compensation prescriptions and
the prior scalar-state result are preserved. No new physical source is adopted.

## Frozen initial comparison

In the reconstructed scalar state, perturb either the reservoir field value
or its normalized-frame rate. For each input compare two preparations:

1. compensate its initial D using only the transverse-area coordinate rate;
2. compensate D using only the normalized-frame condensate phase rate.

Both hold D,Vx,Pi,P_n at zero and use the same reservoir input. Every other
scalar-state value is zero except the stated compensation. Exact inverse
reconstruction determines the full original twenty-state direction. These
are infinitesimal linear directions, not finite-amplitude unit perturbations.
The dust rate is computed with (O_dot+O L)E(QE)^-1, retaining observation-map
drift, not with the initial dust map times the scalar generator alone.

For both reservoir inputs at every ell=4,8,16,32,64 the two initial density
rates differ. Their Vx rates agree. The difference of preparations has zero
reservoir field and normalized-frame rate. This confirms that compensation
alone can change the response; it does not isolate a reservoir susceptibility.
The [comparison receipt](../../../Analysis/MasterTests/outputs/a16_matched_reservoir_v1_20261116/receipt.json)
exports exact directions, compensation coefficients and response differences.

## Actual matter-current dictionary

An additional audit was frozen after inspecting the reconstructed shift.
For the original dust action and future clock branch,

    j_tau^mu=-epsilon C^2 partial^mu tau,
    background j_tau^0=rho_m/C,
    delta tau_dot=C(alpha+beta Pi), beta=2/5.

Define the perturbation of densitized clock-current density relative to its
conserved background density and its normalized coordinate flux:

    N_tau=delta rho_m/rho_m+trace(M)/2-beta Pi,
    F_tau=delta(sqrt(-g) j_tau^x)/(a^3 rho_m/C)
         =-i ell T/(a^2 C)-Sx/a.

Here T=delta tau, Sx is the full reconstructed shift amplitude and the
background coordinate torus wave is along x. The code verifies the clock
multiplier relation, a^3 rho_m/C conservation and the exact map identity

    N_tau_dot+i ell F_tau=0

on the same background shell, with all coefficient drift. This identifies a
conserved clock current, not a new microscopic particle-number prescription.

In this export T=0 and Mxx=0; hence F_tau=-Sx/a and
N_tau=i p D+area-beta Pi. The shift contains Vx plus condensate, reservoir,
metric-rate and force contributions. Thus the matched frame variable Vx is
not the full coordinate flux of the conserved dust current. Frame-relative
velocity and coordinate flux in the evolving metric must not be conflated.

## What the audit decides

Both preparations also start with N_tau=0, but their F_tau values differ
for both reservoir inputs at all five modes. Their conserved-density rate
differences satisfy the same continuity identity exactly. The audit outcome
is therefore ACTUAL_CLOCK_FLUX_NOT_MATCHED, not an isolated reservoir response.

Energy density and conserved clock density are also distinct: even with
N_tau and its flux fixed, varying metric volume or conformal mass can change
the local energy-density contrast. Since p_dot=-H p, the identity gives

    D_dot=H D-a F_tau-(area_dot-beta Pi_dot)/(i p).

This separates current transport and geometric/conformal contributions in
the density rate. A density-rate difference alone is not evidence of a
reservoir pump, irreversible memory or organizing force.

Earlier rank and hidden-state calculations remain correct for their exact
maps and fixed chart. References to (D,Vx) as a dust pair must carry this
dictionary: they do not specify the complete conserved matter-current state
and geometry. Nothing here withdraws the closed twelve-value scalar chart,
or proves closure of a different, properly specified matter-state reduction.

## Evidence and checks

- [Initial comparison contract](RES001_A16_MATCHED_RESERVOIR_V1_CONTRACT_2026-11-16.md),
  [pins](RES001_A16_MATCHED_RESERVOIR_V1_INPUTS_2026-11-16.json),
  [executable](../../../Analysis/MasterTests/test_a16_matched_reservoir_v1.py):
  140/140 reconstruction, matching, compensation and rate checks.
- [Current audit contract](RES001_A16_MATTER_FLUX_V1_CONTRACT_2026-11-16.md),
  [pins](RES001_A16_MATTER_FLUX_V1_INPUTS_2026-11-16.json),
  [executable](../../../Analysis/MasterTests/test_a16_matter_flux_v1.py),
  [receipt](../../../Analysis/MasterTests/outputs/a16_matter_flux_v1_20261116/receipt.json):
  36/36 dictionary, exact conservation and preparation checks. The non-matching
  flux is an explicit scientific diagnostic, not a failed code assertion hidden
  by the check count. No target required equal or different responses.

Both executables have fresh-directory byte-identical receipt replays. These
are same-assistant computational checks. Original scientific evidence, sources,
sidecars and prior results are unchanged; no finite-time certificate is extended
to these new initial directions. Nonzero modes admit conjugate real fields;
their linear global perturbation averages vanish. Gauge/source admission and
nonlinear/global completion remain separate qualifications.

## Next task and boundaries

Specify which operational matter-current and metric quantities a source or
paired-state experiment holds fixed. Retain N_tau, its actual flux, geometric
volume and the conformal mass response explicitly. Determine compatible
compensations from the unchanged constraints before identifying a reservoir
channel. Coordinate flux alone is not a gauge-invariant measured velocity;
an observer/source prescription must accompany physical interpretation.

Do not repeat this unmatched proxy comparison as a new memory experiment.
No external source action, thermal state, dissipation/noise law, entropy sign,
matched acceleration or physical window is supplied. Review DEFERRED;
physics_pass=false; gate_effect=NONE; original G1–G6 and MAT matching remain open.
