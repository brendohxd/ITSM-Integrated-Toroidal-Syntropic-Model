# A16.2: controlled radial-rate pressure and geometry response

16 November 2026. Owning route: A16.2; conditional original R4C1/B1.
Disposition: COMPLETE_SCOPED_CONTINUOUS_FINITE_MODE_PRESSURE_RESPONSE.
The larger A16.2 history/physical-closure route remains OPEN.
physics_pass=false; gate_effect=NONE; Rule-9 review DEFERRED.

## Result and meaning

The radial condensate-rate direction identified by the
[initial pressure-state audit](RES001_A16_PRESSURE_STATE_V1_REPORT_2026-11-16.md)
has a controlled pressure and metric-area response throughout t in [0,0.05]
for ell=4,8,16,32,64. This is a fresh trajectory certificate for that direction,
not a transfer of the earlier four-column trajectory certificate.

The real pressure Fourier coefficient is negative over the certified sign
intervals of the four lower modes. At ell=64 it changes from negative to
positive. Thus the response is dependent on scale and evolution; it cannot
be represented as a universally fixed-sign response of this initial direction.

The full coupled equations already contain this effect. The result explains
why omitting condensate momentum loses pressure information. It supplies no
additional force, irreversible bath, entropy-production law, or new Campbell
mechanism. It is compatible with a finite deterministic full-state description;
it does not prove irreducible memory.

## Registered calculation

Use original-chart initial delta u_dot=1 (slot 16), other nineteen entries
zero, against the zero perturbation. This specifies a linear-response
normalization in the registered formal units, not a finite-amplitude state.
Initially the ten named current/geometry/force/reservoir/energy rows and the
combined scalar pressure all agree. The normalized modulus-squared rate
differs by 2 and the initial proper pressure rate differs by -2341/840.
Those initial holds are not imposed continuously during evolution.

The unchanged twenty-state generator, evolving eleven-component rotating
background, balancing drift and inherited constraint reconstruction remain.
No projection onto a slow graph, coefficient fit, regulator modification,
action change or assumption of a permanently matched current was introduced.

The observation is the combined canonical u,v,r scalar pressure including
the shared portal potential, with proper field rates and the reconstructed
lapse. The second observation is transverse scalar metric area. This is not
reservoir-only pressure or total stress from every sector. In particular the
previous initial pressure/area-acceleration identity is not asserted as a
universal finite-time relation after other variables evolve.

| ell | Real pressure coefficient at t=0.05 | Metric-area coefficient at t=0.05 | Continuous absolute pressure error, outward-rounded display |
| --- | ---: | ---: | ---: |
| 4 | -0.12140444 | 0.00004786001 | <3.08e-37 |
| 8 | -0.11670015 | 0.00004732341 | <4.89e-37 |
| 16 | -0.09870212 | 0.00004522053 | <2.61e-36 |
| 32 | -0.03881950 | 0.00003747722 | <1.67e-35 |
| 64 | +0.06056458 | 0.00001542246 | <1.18e-34 |

Displayed endpoint coefficients are rounded. Exact dyadic enclosures and
error budgets are in the receipts. These tiny errors describe numerical
accuracy for fixed conditional equations and exact registered inputs; they
are not empirical uncertainties or confidence in the physical model.

For ell=4,8,16, the real coefficient is certified negative on [1/640,1/20];
for ell=32, on [1/1280,1/20]. Their initial tile contains P(0)=0.
For ell=64 it is negative on [1/5120,163/5120] and positive on
[41/1280,1/20]. The intervening zero-containing tile brackets at least one
sign reversal between 0.0318359375 and 0.03203125. Uniqueness of that crossing
is not proved. Both zero-containing ell=64 tiles are retained in the receipt.
Signs refer to a real Fourier coefficient with the chosen phase, not pressure
everywhere in physical space.

## Error control and verification

The [frozen V3 contract](RES001_A16_PRESSURE_EVOLUTION_V3_CONTRACT_2026-11-16.md)
retains the original acceptance threshold <1e-8. The
[error argument](RES001_A16_PRESSURE_EVOLUTION_ERROR_ARGUMENT_V1_2026-11-16.md)
uses the pinned continuous background enclosure and full-vector Q-norm
propagator exp(30(t-s)). The old propagator proof applies to arbitrary vectors
in this registered linear chart; the old prepared-column accuracy does not.

Fresh degree-24 piecewise Taylor evolution uses outward-rounded 256-bit
dyadic intervals. All low-order rounding discrepancies, high-order tails,
initial balancing error and background/operator uncertainty enter the defect
bound. The 416 tiles have identical point endpoints at each join. Pressure
and area rows have their own box norms and background Lipschitz bounds.
There is no sampled-residual substitute for the continuous estimate.

For clarity, the certified state infinity norm uses complex moduli. Arithmetic
uses |Re|+|Im| as a conservative upper bound on individual complex quantities.
The resulting observation error bounds each component as well as its modulus;
the reported real and imaginary intervals are both enlarged by that error.

The main calculation passes 88/88 controls. An independent standard-library
rational audit passes 43/43, using an exact exponential series with a geometric
tail to check the error formula, observation budgets, full time coverage,
outward intervals, sign counts and tile hashes. It imports no solver or dyadic
arithmetic implementation. This is an independent computational check, not
independent scientific peer review.

A separate DOP853 solve evolves the actual background and original twenty
states, comparing against the balanced Taylor construction at every tile end.
Worst state disagreement is <4e-15 and observation disagreement <2.16e-16.
These floating comparisons are diagnostics, not the source of certification.
The state, pressure and area all pass their relevant numerical accuracy bounds.

Both packages replay byte-identically, including receipt sidecars; the full
trajectory tile file and its sidecar also match. Seven final replay/preservation
checks pass. All 671 frozen input hashes remain unchanged; the calculation's
pre/post source timestamp-and-hash preservation check also passes.

## Preserved failed attempts

V1 was stopped after inspection found object-identity comparisons of interval
instances in two controls; no trajectory certificate was produced. Its source,
contract and inputs remain. See the
[V1 note](RES001_A16_PRESSURE_EVOLUTION_V1_ATTEMPT_NOTE_2026-11-16.md).

V2 completed with 83/88 checks. Its only failures demanded exact equality of
rounded opposite-seed trajectories, amplitudes and defects. Midpoint flooring
is not odd. V2's failed receipt is unchanged. V3 bounds the actual discrepancy
using exp(norm(A)*h)*h*(d_plus+d_minus), including both measured defects;
it introduces no fitted tolerance. The V2 and V3 trajectory tile files are
byte-identical. See the
[V2 note](RES001_A16_PRESSURE_EVOLUTION_V2_ATTEMPT_NOTE_2026-11-16.md).

## Evidence and next action

- [V3 executable](../../../Analysis/MasterTests/test_a16_pressure_evolution_v3.py).
- [671-input manifest](RES001_A16_PRESSURE_EVOLUTION_V3_INPUTS_2026-11-16.json).
- [Main receipt](../../../Analysis/MasterTests/outputs/a16_pressure_evolution_v3_20261116/receipt.json), SHA256 `b4e19b0984f3e69536607b814039f5328ffc73866f8d06b59f1b96e2c1fa2066`.
- [Continuous tiles](../../../Analysis/MasterTests/outputs/a16_pressure_evolution_v3_20261116/tiles.json).
- [Independent audit](../../../Analysis/MasterTests/outputs/a16_pressure_evolution_audit_v1_20261116/receipt.json), SHA256 `675d14c19ac347a4e5d09b61b27f77413d310ec045b5ebec8e5f0874df5af3bb`.
- [Replay and preservation receipt](../../../Analysis/MasterTests/outputs/a16_pressure_evolution_v3_verification_20261116/receipt.json).

Next, if continuing A16.2: establish the finite-time augmented scalar-state
map and a controlled elimination of this demonstrated pressure/state response,
including hidden initial data and feedback. Do not replace this with another
unbounded derivative hierarchy or assume that pressure alone is a constitutive
closure. A useful reduced history law and its error remain open.

This finite set of modes does not establish nonlinear stability, a healthy
Hamiltonian, arbitrary-background evolution, a physical frequency window,
matter-residue matching or a universal acceleration coefficient. G1-G6/MAT
prerequisites remain with their live owners. The separate R-tau candidate is
unchanged and unadopted. No manuscript/PDF, website, publication, external
review dispatch, vault mutation, commit or push was performed in this task.
