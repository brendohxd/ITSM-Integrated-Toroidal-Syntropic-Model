# A16.2: independent retained Volterra evolution

19 November 2026. High confirmed. Conditional unchanged original R4C1/B1.
Disposition: COMPLETE_SCOPED_INDEPENDENT_RETAINED_HISTORY_EVOLUTION.
The wider physical-mechanism/reduction route remains OPEN.
physics_pass=false; gate_effect=NONE; Rule-9 review DEFERRED.

## Result and meaning for ITSM

The eight retained variables have now been independently evolved using their
Volterra history law. Their full-system trajectory was not supplied to the
advancing function. The resulting retained state, pressure and retained rates
agree with the certified full response throughout [0,0.05] for all five
registered modes ell=4,8,16,32,64. The ell=64 positive endpoint is preserved.

This closes the computational consistency loop for the registered radial-rate
seed: the full scalar description, the two-time kernels, supplied-history
reconstruction, and independently advanced retained history all reproduce the
same response with controlled errors. The existing condensate state and its
causal history account for the tested apparent-memory effect.

This is a representation/evolution result inside the existing conditional
equations. It supplies no new fundamental force, entropy law, microscopic
matching relation, healthy physical modes or observational confirmation.
The earlier result that hidden initial motion dominates endpoint pressure,
with smaller nonzero feedback, is unchanged. It does not establish a general
small-feedback or short-memory approximation.

## What the independent algorithm actually advances

It consumes sealed coefficient inputs containing only A,P_R,L,Rh,Lp, the
time grid and initial data. The source archive's reference R/P curves and
original hidden generator are absent from that advancing input.

    J(t)=integral_0^t Rh(s)R(s) ds,
    R_dot=A R+L(h0+J), P=P_R R+Lp(h0+J).

Eight retained values and four causal quadrature accumulators are advanced.
The accumulators retain history information; this is not an eight-number
memory-free model or a claim that physical degrees of freedom were removed.
The solver uses degree-24 causal coefficient recurrences with the actual
kernel factors, hidden initial forcing and exact polynomial continuity at
tile joins. A constant forcing coordinate and zero padding are arithmetic
implementation details, not new physical fields.

R(0)=J(0)=0 and h0=(0,0,1/ell,0), corresponding to the same original unit
radial-rate seed. Source coefficients preserve the lapse, background/map
drift, momentum drift, constraints and ensemble of the parent calculation.
No new action or R-tau adoption occurs. Removing the hidden initial forcing
from zero initial retained/integral data gives the exact zero solution,
which misses the tested response.

Filtered inputs are hashed before advancement. Independent solution curves
are saved and hashed before reference curves are opened for comparison.
The advancing function performs no file reads and receives no full-state
trajectory. The algorithm shares validated arithmetic with earlier work;
it is an independent computational formulation, not independent peer review.

## Continuous error certificate

Numerical defects are bounded in both R_dot=A R+L(h0+J) and J_dot=Rh R,
including coefficient rounding and all polynomial-product tails. Physical
kernel/background uncertainties are included separately.

For analysis only, lift the numerical history to

    X_tilde=(R_hat,U_h(t,0)(h0+J_hat)).

Its mixed residual is (r_R,U_h r_J). The exact moving mixed-to-balanced map
and the existing full-vector Q-norm propagator bound the error of this lift.
Moving conjugacy on the registered shell and initial agreement are checked
explicitly. This analytic lift is not used to advance the trajectory. It
avoids applying a raw large-entry matrix majorant as an assumed physical
growth rate. See the [error argument](RES001_A16_VOLTERRA_ERROR_ARGUMENT_V1_2026-11-19.md).

In the parent's fixed formal units and perturbation normalization, the uniform
absolute bounds, displayed conservatively upward, are:

| ell | Retained-state error | Pressure error | Retained-rate error |
| --- | ---: | ---: | ---: |
| 4 | <1.48e-35 | <9.87e-36 | <1.80e-34 |
| 8 | <1.56e-34 | <3.89e-35 | <1.59e-33 |
| 16 | <3.90e-33 | <4.06e-34 | <3.60e-32 |
| 32 | <3.13e-31 | <1.47e-32 | <2.75e-30 |
| 64 | <2.85e-29 | <6.32e-31 | <3.35e-28 |

All pass the frozen 1e-8 threshold. Continuous nominal differences from the
full reference are below 5e-45 (R), 4e-43 (P), and 4e-42 (R_dot).
An independently implemented DOP853 solve of the filtered Volterra realization
agrees to <4.45e-18 in R and <2.78e-17 in pressure at the diagnostic endpoints.
Those floating comparisons supplement the continuous proof; they do not
establish it. These tiny bounds quantify numerical accuracy for exact fixed
conditional inputs, not empirical uncertainty or physical model credibility.

The independently obtained endpoint pressure coefficients are approximately
-0.12140444, -0.11670015, -0.09870212, -0.03881950 and +0.06056458 as ell
runs through the five modes. Fourier signs are not claims about pressure
everywhere in physical space or the total cosmological stress.

## Verification, preservation and reproducibility

The main calculation passes 66/66 controls. An independent audit passes
148/148 using exact integer polynomial convolution with denominator 2^512
to recompute retained, quadrature and pressure residuals, plus rational box
and error-lift checks. It checks causal input isolation, zero initial data,
exact tile continuity, unchanged kernels and certified endpoint signs.
It does not import the production evolution solver or dyadic arithmetic.
These are same-assistant computational checks, not an external review panel.

The main and audit packages replay byte-identically, including all filtered
inputs, solution archives, receipts and sidecars. All 56 final preservation/
replay checks pass. The 779 frozen input hashes and main pre/post timestamps
are unchanged. V1 and V2 coefficient/solution archives are also identical.

V1's saved trajectories remain intact. V1 stopped when a NumPy boolean in
diagnostic metadata could not be serialized as JSON; it has no successful
main receipt. V2 converts the diagnostic/check metadata to native float/bool
types. Its equations, bounds, acceptance threshold and trajectories were not
changed. The failure is preserved in the
[attempt note](RES001_A16_VOLTERRA_EVOLUTION_V1_ATTEMPT_NOTE_2026-11-19.md).

Each ell directory contains coefficients_only.json.gz and solution.json.gz.
They store lossless integer dyadic polynomial coefficients with scale 2^256,
degree 24 and the declared tile grid, using deterministic gzip. Solution
fields R,J,P,R_rate are evaluated by the same local polynomial convention
as the [kernel owner](RES001_A16_NUMERICAL_KERNEL_V1_REPORT_2026-11-19.md).

- [Contract](RES001_A16_VOLTERRA_EVOLUTION_V2_CONTRACT_2026-11-19.md).
- [779-input manifest](RES001_A16_VOLTERRA_EVOLUTION_V2_INPUTS_2026-11-19.json).
- [Executable](../../../Analysis/MasterTests/test_a16_volterra_evolution_v2.py).
- [Main receipt](../../../Analysis/MasterTests/outputs/a16_volterra_evolution_v2_20261119/receipt.json), SHA256 `f7a68ed390b6284fb7a44a51e93466bae67b77f80f2ce4ac36302da065b07d98`.
- [Independent audit](../../../Analysis/MasterTests/outputs/a16_volterra_evolution_audit_v1_20261119/receipt.json), SHA256 `77d1f6025929e1bce1bab683f398e6db30909b126ce26a3134c8f31ec77e85c8`.
- [Replay/preservation receipt](../../../Analysis/MasterTests/outputs/a16_volterra_evolution_v2_verification_20261119/receipt.json).

## Next handoff and remaining physical questions

The exact history method is now computationally closed for this seed/domain.
Optional A16 follow-up is to test additional constraint-compatible initial
data and quantify controlled approximations, including relative errors near
pressure zeros and the retained-trajectory changes caused by deleting terms.
A16.5 time-scale separation remains open. A small endpoint feedback fraction
in one probe is not an all-time reduced-model error bound.

The registered higher-priority physical-domain/matching routes remain the
scientifically decisive work: actual healthy coupled modes, nonlinear
interactions and validity window, operational thermodynamic state and any
organizing mechanism, and genuinely identifying matter/force matching.
None is cleared by this computational equivalence. The goal is not promoted
to an observationally validated ITSM model. No paper/PDF, website, external
review, bulk vault sync, commit, push or deployment changed.
