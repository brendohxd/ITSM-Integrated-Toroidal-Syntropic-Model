# G3N5: corrected reference, retained response and controlled forced remainder

Date: 12 October 2026. Version 1. Owner: Stage 1 / Master Test 1 / RES-001.
Checkpoint: initial calculation complete, **100/100 local checks**, zero
failed/unknown checks. Immutable scientific replay has been launched and is
**PENDING at this report checkpoint**. Record its eventual outcome in a new
replay note; do not silently rewrite this report or infer replay clearance.

Disposition: **CONTROLLED_FORCED_REMAINDER_AFTER_RETAINED_RESPONSE**.
This closes a bounded mathematical lemma, NOT the full dust milestone.
Actual/sharp convergence order and useful finite-mode accuracy remain OPEN.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.

## 1. What changed, and what did not

The unchanged full 20-state generator, evolving charged B1 background, actual
dust observables, momentum drift and auxiliary constraint reconstruction are
the frozen inputs. No action, diagnostic parameter, physical initial data,
target coefficient or original trajectory has been changed. All five modes
ell=4,8,16,32,64 and all four archived columns remain unfiltered.

Starting from the stored exact R2 and formal lift-chart N2, construct the full
first-correction lift

    H_c = H0 + H1/ell + H2/ell^2 + (H3+q3)/ell^3 + H4/ell^4,
    M_c = M + N2/ell^2.

The ordinary-wave correction q3 and fast correction H4 cancel the complete
order-minus-two source, not only its slow projection. Retain every wave/fast
state. N2 is a lift-chart coefficient, not a microscopic matching result or
the directly observable correction. The previously checked normalized
observable coefficient remains N_obs=N2+dot(J2)+[J2,M].

V1's negative forcing was analytically invalid and remains preserved with its
[sign audit](RES001_R4C1_G3N5_CORRECTED_REMAINDER_SIGN_AUDIT_2026-10-12.md).
V2/V3 were incomplete representation-optimization attempts, NOT physics
failures. V4 retains positive forcing and all rejection/solver controls while
evaluating the SAME exact derivatives in factored form. It does not delete
drift, replace exact intervals by samples, or change equations to obtain PASS.

## 2. Exact full-state decomposition and the sign

Define J_obs=O_c H_c, J0=J_obs(0), and
Delta0=E_orig-H_c(0)J0^-1. Let Gamma_c propagate the full generator A_c;
Phi_c propagates M_c. Then

    R_H = A_c H_c - dot(H_c) - H_c M_c
        = R3_c/ell^3 + R4_c/ell^4 + R5_c/ell^5 + R6_c/ell^6,

    x_full(t) = H_c(t) Phi_c(t) J0^-1 W0
              + Gamma_c(t,0) Delta0 W0
              + integral_0^t Gamma_c(t,s) R_H(s) Phi_c(s) J0^-1 W0 ds.

The integral has a PLUS sign. Apply O_c to obtain W_ref, W_retained and
W_forced. The retained term includes the original fast/wave mismatch and is
not removed by continual projection onto a graph. No inverse of J_obs(t)
during evolution is required. The source coefficient bookkeeping, complete
order-two cancellation and original observation coefficient are checked.

## 3. Whole-interval bound and domains

Exact rational interval arithmetic bounds every source coefficient and
background derivative on the inherited rotating-background box. Denominators
must exclude zero; square-root enclosures are outward. Source bounds are
displayed as 886.9020479024745, 536.4579116963844, 1113.2183901404057 and 0
for powers 3,4,5,6 respectively. Exact rational constants and matrices are in
[formulas.json](../../../Analysis/MasterTests/outputs/r4c1_g3n5_corrected_dust_remainder_attempt_04/formulas.json).

The derived CONTINUUM domain is ell>=5, 0<=t<=1/20, on the registered B1
Friedmann shell, with a,C,rho_m positive and conserved background charge
a^3(u dot(v)-v dot(u))=1. This charge is distinct from the observation matrix
J_obs. Physical p=ell/a and dot(p)=-H p remain in the inherited generator.

J0^-1 has norm at most 2 on this continuum domain; the corrected reference
growth rate is at most 30. The inherited full-state transfer estimate and
explicit coordinate/observation/source norms give

    ||W_full-W_ref-W_retained||_infinity
      <= C3 t exp(30 t) ||W0||_infinity / ell^3.

C3 is the exact rational `continuum.C3` in formulas.json; its display value is
10883730.361973401. The inequality follows from the full Duhamel integral,
not a fitted power law or finite sample maximum. Separate exact J0 inverses
and point constants are retained for ALL five modes, including ell=4 below
the sufficient continuum threshold. None is removed as an inconvenient case.
These thresholds are comparison-chart/transfer domains, NOT physical cutoffs.

## 4. Independent controls and practical limitations

For each mode, integrate all 84 complex control variables: the two-state
reference fundamental matrix, full 20-by-2 retained response and full 20-by-2
positively forced response. Two separate DOP853 integrations use the frozen
tolerance/step refinements. Compare their complete reconstructed states and
all 22 prepared fields with the untouched archived trajectories at all 257
times. The two complementary archived columns are retained and checked for
full-field/observable reconstruction; they are NOT newly re-solved in this
two-column prepared-response control. Their original nonmonotonic results
are not rewritten or promoted into a different claim.

| ell | Sampled maximum forced remainder | Point bound at t=0.05 |
|---:|---:|---:|
| 4 | 0.05011249233356897 | 43347.57721867417 |
| 8 | 0.0035083441012230955 | 1164.3234862139211 |
| 16 | 0.0002284256911601744 | 61.27645064075249 |
| 32 | 0.000014376183206067763 | 4.816821399884198 |
| 64 | 0.0000008998341662904064 | 0.47346637734297137 |

Bounds are mathematically controlled but remain loose. The sampled remainder
column is NOT a convergence-order proof, a bound for W_full-W_ref alone, or
evidence that the first correction by itself improves every mode. Large
retained/forced terms can cancel; dropping either changes the calculation.

Worst paired-solver disagreement is 3.337317693502986e-15; full-state
decomposition residual is at most 6.717574217517838e-14; prepared 22-field
decomposition residual at most 3.855530335267065e-13. Direct source identity
residual is at most 1.5546947545541992e-14. All original four-column field and
observable reconstruction residuals remain below 1.623e-14.

The checks reject negative forcing, omitted correction drift and an interval
denominator containing zero. Exact real/imaginary/mixed decomposition,
quotient-rule derivative, matrix round-trip and source/metadata checks pass.
527 input/source/available-sidecar files retain hashes, sizes and mtimes.

## 5. What remains necessary

The controlled order-three statement concerns W_forced AFTER W_retained is
retained exactly. It does NOT prove that W_retained is negligible, that the
full original dust error has sharp order two, or that a closed two-state dust
law meets useful finite-mode accuracy. Those are substantive Stage-1 tasks.

Private weighted-sector identities and conservative interval candidates now
support a route to retained-response control, but their sufficient ell>=8192
threshold and large energy majorant are not physical-band or accuracy results.
The original-data weighted numerator is checked only for the old lift; a
complete corrected-lift initial bound, full controlled expansion and a
nonzero lower-order witness still require a separate frozen certificate.

Stage 2 remains STOP_AND_ASSESS_DOMAIN_UNRESOLVED. Full finite-density physical
coupled interactions, metric/matter mixing, gradients/characteristics,
zero/singular/fixed-charge domains, full matter-coupled PPN, healthy GR and a
nonempty physical validity window are NOT supplied by this linear lemma.
The operator will reassess action selection at that point; no parent switch
or automatic TOP-X4 pivot is made. Stage 3 is NOT ENTERED: genuine identifying
matter-residue and nonlinear-force matching inputs remain absent.

## 6. Reproducibility and inherited review

- [V4 contract](RES001_R4C1_G3N5_CORRECTED_DUST_REMAINDER_V4_CONTRACT_2026-10-12.md):
  ec006684bc7ff2aa3e31bd231743127d287b8d6d5067daea926966af7cce4891.
- [V4 executable](../../../Analysis/MasterTests/test_01_r4c1_g3n5_corrected_dust_remainder_v4.py):
  21419587770e4fad695d1d7c86f5038b0110d6de560a363e78fb78cf2a72b391.
- [Summary](../../../Analysis/MasterTests/outputs/r4c1_g3n5_corrected_dust_remainder_attempt_04/summary.json):
  f8ad05b485f7b384cdde29e5ab5e0227f074fee6c626555006ef010601c6496f.
- Formulas: bd2044eb3f770e3d4bbe89e3a72b145b80e100b44a2d0da8d33a3114c0d8e5d7.
- Diagnostics: 46cee32f8d32bb26885da57b36dc28d7ecb498ae10783314afc891c6998cc209.

Run the frozen executable with its default fresh attempt_04 (already exists,
so overwrite is refused), or use --replay followed by that attempt directory
for a READ-ONLY byte/sidecar comparison. Replay is pending at THIS checkpoint.
Originals, failed/interrupted versions, hashes and sidecars remain preserved.
No private logs/context are publication artifacts. No commit, push, provider
dispatch, manuscript edit or publication is performed.

R9-MT1-G3N5-CORRECTED-REMAINDER and its prepared/observable/uniform/fast,
exact split, G3N5/B1G/action review dependencies remain DEFERRED. Review alone
does not block provisional use of this scoped lemma; the substantive deficits
above do block stronger claims. Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 UNCHANGED. The full native goal remains ACTIVE and incomplete.
