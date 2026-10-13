# Useful finite-mode dust control, with original stored seeds covered

Date: 12 October 2026. Version 1. Stage 1 / RES-001 / Master Test 1.

The operator-selected certified finite-mode numerical error-control route is
verified within the registered linear B1 scope. All five modes have a
continuous-time prepared-dust error below the pre-execution 1% benchmark on
[0,0.05]. The exact initial-data recipe AND both original stored numerical
representations are covered. Original files, inputs, failed attempts, hashes
and scientific sidecars were not replaced.

Main certificate: 85/85 local checks and exact read-only replay. Independent
implementation/rational-majorant controls: 97/97 and exact replay. Original
stored-seed enclosure: 34/34 and exact replay. No failed/unknown checks in these
three receipts. Counts alone are not the proof; the continuous defect,
propagator, initial-data and background inequalities below supply the result.

physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.
This is not a healthy-GR result, a physical cutoff, a matched acceleration
prediction, a canonical promotion or independent peer-review clearance.

## Domain and preserved dynamics

Modes ell=4,8,16,32,64; 0<=t<=T=1/20 in the frozen diagnostic units. Original
rotating B1 background, Friedmann shell and angular charge J=1; positive a,C,rho.
The original exported Az evolves ALL 20 complex first-order states. Oz=Obs B^-1
and Fz=F B^-1 retain the actual dust observable and all 22 reconstructed fields.
All four original columns, time-dependent basis/momentum drift, constraints,
fast/wave response and rational inverse denominators are retained.

"Full" here means this complete frozen classical R4C1/B1 linear export. It does
not mean that omitted semiclassical stress/state, counterterm or quantum sectors
have been derived. The zero mode, singular endpoints, other backgrounds,
unprepared initial-data families and a physical frequency/momentum window are
outside this certificate. No repeated slow-graph or constraint projection.

The first two initial columns are the original normalized formal-lift recipe;
the complementary columns use the original index-9/index-19 seed prescription.
The graph is used only for that existing initial construction, not evolution.
Original saved arrays remain unchanged. Their differences from the exact recipe
are bounded separately; binary64 agreement is not claimed to be 256-bit equality.

## Continuous arithmetic and error proof

Interval endpoints are signed integers in units 2^-256. Rational conversion,
multiplication and division use exact outward floor/ceiling; sqrt uses isqrt
brackets. Zero-containing denominators are rejected. All polynomial tails have
explicit retained radii, including the identity

    (P+e)^-1 - V = [1-P V-e V]/(P+e).

The written degree-40 background/leading polynomials are approximants, not
assumed exact flows. Their complete continuous defects and initial discrepancies
are enclosed. A Lipschitz/continuation estimate gives

    e_b <= exp(L_b T) [e_b0 + T d_b],

strictly within the positive-domain box margin. The background error is below
2.089e-41; the leading-transfer error is below 3.243e-42. These are upward-rounded
displays; exact rational bounds and the declared box are in the certificate.
Exact Friedmann and charge identities are preserved without numerical resets.

Local degree-24 full-state polynomials use 32,32,32,64,256 dyadic time tiles
respectively, 416 total. The tile count is chosen from a generator majorant
before evolving a mode, with h||Az||_infinity<=1. Every lower-degree arithmetic
discrepancy, higher RHS coefficient and inherited operator remainder enters the
continuous defect. Point-dyadic endpoint sums are exact: no unbounded tile jump.

For e_z between the exact coupled flow and its polynomial approximation,

    e_z' = Az(b)e_z + [Az(b)-Az(bhat)] zhat - r_z.

With the original T(b)=Tw(I+U/ell)^-1 C, e_w=T(b)e_z, the inherited FULL Q
propagator gives exp(30(t-s)). Q is an evolution norm, NOT a physical Hamiltonian.
Including initial, background and numerical defects,

    E_Q <= exp(30T) K_T [e_z0 + T(d_z + L_A e_b Z_max)],
    E_observable <= K_O E_Q + L_O e_b Z_max,
    E_fields <= K_F E_Q + L_F e_b Z_max.

Every constant is explicitly enclosed on the declared domain. The actual
prepared-model error is bounded by the polynomial observable difference plus
twice the observed-column numerical radius and the leading-transfer radius.
This is a bound between sample times, not merely DOP853/Radau agreement.

The original stored seeds are also considered as exact JSON decimal lexemes
and as the original binary64 decoder's exact integer ratios. Same-action
solutions with different seed representations differ homogeneously. Add

    E_seed_Q <= exp(30T) K_T ||seed_stored-seed_exact||_infinity,

then convert with K_O/K_F. The larger stored-input radii below are reported
instead of attributing the exact-recipe's much smaller radius to rounded inputs.

## Useful finite-band result

Pre-execution criteria: numerical error <=1e-8 for every observable/field column
throughout the interval, and prepared induced-infinity model error <=1/100 for
unit input coefficients in the original two-column prepared span. This is a
dimensionless diagnostic convention, not an observational tolerance, universal
cosmological accuracy claim or field-redefinition-independent physical cutoff.

Values below are rounded UP, using the worst of both stored representations.
Exact rational bounds, not decimal displays, are authoritative.

| ell | Continuous prepared-model error bound | Worst stored-input numerical error, dust/22 fields |
|---|---:|---:|
| 4 | 0.007607068 | 1.533e-11 |
| 8 | 0.001782788 | 6.395e-12 |
| 16 | 0.000441861 | 1.219e-10 |
| 32 | 0.000110465 | 2.168e-10 |
| 64 | 0.00002759470 | 1.574e-9 |

Thus the largest registered prepared error is below 0.761%, and the largest
stored-input numerical radius is below 1.574e-9. The old complete energy budget
remains a valid conservative bound; it was not edited into this sharper result.
The exact-recipe numerical radii range from about 1.96e-35 to 2.19e-28. Those
numbers have a distinct input meaning and do NOT describe the original rounded
trajectory arrays' solver error or their underlying physical-model uncertainty.

## Controls, complementary responses and provenance

Independent controls exercise the ACTUAL stepper at omega=8192, h=1/16384
against exact-Fraction sine/cosine series with alternating remainders, and at
zero generator with exact unchanged endpoints. Wide positive/negative interval,
sqrt, inverse/restriction-tail and zero-denominator controls pass. A separate
Fraction implementation recomputes the background, leading, Q, observation,
field and prepared-error majorants. Every tile/index/aggregate/hash chain is
checked; in-memory omission of a tile is rejected without modifying receipts.

All 257 original archive times, four columns and 22 fields are compared for each
mode. Archive comparison remains diagnostic; the defect proof certifies accuracy.
The original third complementary column's sampled maxima are about 0.00624047,
0.00282549, 0.01231081, 0.00496237, 0.00162039 for increasing ell. This NONMONOTONIC
response is preserved, not smoothed or replaced by an imposed ell^-2 law.

The prior [exact split](RES001_R4C1_G3N5_DUST_REMAINDER_REPORT_2026-10-11.md),
[corrected forcing](RES001_R4C1_G3N5_CORRECTED_REFERENCE_REMAINDER_REPORT_2026-10-12.md),
[sharp scoped order-two theorem](RES001_R4C1_G3N5_DUST_ACTUAL_ORDER_REPORT_2026-10-12.md),
[normalized reference](RES001_R4C1_G3N5_NORMALIZED_REFERENCE_REPORT_2026-10-12.md)
and [complete energy budget](RES001_R4C1_G3N5_DUST_FINITE_ENERGY_REPORT_2026-10-12.md)
remain frozen. The new result supplies the previously missing USEFUL finite-band
error-control component. No failed/interrupted attempt is relabelled PASS.

The final seed receipt verifies 324 source pins and preserves 645 source/input/
available-sidecar metadata; main certificate 315/627, independent controls
320/637. All three exact read-only replays completed with exit 0.

Reproduction: the versioned executables under Analysis/MasterTests are
`test_01_r4c1_g3n5_dust_certified_numerical_v1.py`,
`test_01_r4c1_g3n5_dust_certificate_controls_v1.py`, and
`test_01_r4c1_g3n5_dust_seed_enclosure_v1.py`. Each has its frozen pre-execution
contract and source sidecar; use --replay with its corresponding existing
attempt directory. Fresh runs refuse overwrites.

Receipt summary SHA-256 values:

- Main attempt_01: df6dff025f24f82afaf26ac699d419037d65546f6da7f823b50dbb54b12569e1.
- Controls attempt_01: c7f7f8354ca5a4cbc7c78aa6d7a5adb37f95a7b23f08f2ff9644eda23741b5aa.
- Seed enclosure attempt_01: 85ed17c65f0c53c6b01762ec224188be67c85d3ba3e8e725057d233c4d6526ff.

## Remaining programme and reviews

The selected Stage-1 useful numerical-control requirement is met in this
registered scope. Component receipts do not assert completion of the entire
three-stage programme or wider physical dust closure. Consolidate the original
Stage-1 acceptance packet before a broader completion claim; no physical gate
is promoted by this report. Inherited review dependencies remain DEFERRED.

Stage 2 remains STOP_AND_ASSESS_DOMAIN_UNRESOLVED. Full physical coupled
interactions/window, healthy GR, zero/singular endpoints and required constraint
evidence remain unresolved; the operator's next action-selection decision is
still required. No automatic TOP-X4 pivot. Stage 3 NOT ENTERED: genuinely
identifying matter-residue/nonlinear-force matching inputs remain absent.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Native goal ACTIVE/incomplete. No commit, push, publication, paid/provider/model
dispatch, new parent, dependency/runtime change or vault mutation. Vault access
was permitted read-only, but no native vault tool was exposed in this session.
