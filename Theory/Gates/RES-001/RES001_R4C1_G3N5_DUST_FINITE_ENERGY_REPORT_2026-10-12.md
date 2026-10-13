# G3N5 complete finite-mode energy budget; useful accuracy remains open

Date: 12 October 2026. Version 1. Stage 1 / RES-001 / Master Test 1.
V4: 89/89 local checks, zero failures/unknowns; exact read-only artifact and
sidecar replay complete, terminal exit 0. This establishes explicit FULL
linear finite-mode error bounds, not useful accuracy over the whole registered
band, a physical Hamiltonian/ghost clearance or a complete ITSM prediction.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.

## Complete error equation and bound

The same corrected lift Hc, actual observation Oc, normalization J=Oc Hc and
Mc=M+N2/ell^2 give W_ref=J Phi_Mc J(0)^-1 W0. The original full solution is
retained: its complete initial mismatch evolves in ALL 20 coupled first-order
states, together with the complete positive Duhamel forcing Rc Phi_Mc J0^-1.
No repeated projection onto the corrected graph is used. All metric/scalar/
matter constraints, momentum/basis drift, complex fields and inverse
denominators in the exported nonzero-mode system remain present.

Using the inherited time-dependent Q evolution norm and FULL propagator,
Q>=D>0, Q<=9I/8, exact column Q(0) energies and complete factored source
majorants yields

    ||W_full-Phi_M W0||_infinity <= [B_ret(t)+B_force(t)+B_ref(t)] ||W0||_infinity,

    B_ret = K_O K_initial exp(30t),
    B_force = K_O K_source K_J0_inverse t exp(max(30,lambda_lift)t),
    B_ref = K_normalized_reference K_J0_inverse t exp(lambda_reference t).

K_source uses the rigorous full product estimate

    ||Cw Rc||_(infinity -> Q)
       <= (3/2)||Cw||_2 sum_(j=3..6)||Rj||_2/ell^j,

with exact rational background-box majorants. Spectral norms are bounded by
max(one-norm,infinity-norm); no source term is discarded. The independently
verified normalized-reference component supplies B_ref. Exact constants and
expressions are in the frozen formulas, including the full original initial
mismatch, observation and coordinate/residual norm factors.

Domain: original ell=4,8,16,32,64, registered rotating LINEAR B1 prepared
family, 0<=t<=1/20, positive a,C,rho, angular charge J=1. The two prepared
columns span W0; all four archived columns/22 reconstructed fields and the
nonmonotonic complementary responses are preserved and checked. The accuracy
bound does not become a universal result for arbitrary unprepared data.
Time/input units are the diagnostic normalization, not a measured cosmological
clock or a demonstrated physical frequency/momentum window.

## Complete numerical budget and obstruction

All multipliers below are endpoint upper bounds at t=0.05 relative to
||W0||_infinity. Positive coefficient/rate terms also bound their components
on the entire time interval. Sampled error is a diagnostic archive maximum,
NOT a separately certified numerical error or proof at unsampled times.

| ell | Retained bound | Forced bound | Reference bound | Total bound | Sampled error |
|---|---:|---:|---:|---:|---:|
| 4 | 86.3454 | 932.1110 | 5.52869 | 1023.9852 | 0.007606706 |
| 8 | 3.88479 | 36.80272 | 0.238609 | 40.92612 | 0.001782695 |
| 16 | 0.524315 | 2.612793 | 0.0141821 | 3.151289 | 0.0004418373 |
| 32 | 0.167689 | 0.261135 | 0.00109117 | 0.4299154 | 0.0001104604 |
| 64 | 0.0724017 | 0.0303535 | 0.000125409 | 0.1028806 | 0.00002759425 |

The explicit obstruction is CONSERVATIVENESS, not a failed operator identity:
full-state initial-mismatch energy and product/triangle forcing majorants lose
the correlations and oscillatory transfer cancellations that keep the actual
dust observable small. The lowest three bounds exceed the input norm; even
ell=64's bound is about 0.103 while its sampled error is about 2.76e-5.
Thus this estimate does NOT establish useful accuracy across all five modes.
No post-result tolerance was chosen to call it useful. A large majorant is
not measured instability, a physical cutoff or an all-action no-go theorem.

The operator explicitly selected the next route: STAY IN STAGE 1 and pursue
certified finite-mode numerical error control. The next proof must control
the full coupled numerical evolution and numerical/background defects across
the interval, not merely add solver agreement or sampled trajectories.
Existing useful reference bound and sharp asymptotic order-two theorem are
inputs, not substitutes for this remaining requirement.

## Independent controls, zero coefficient and preserved failures

Fifteen original-generator/source controls pass at 70 digits, criterion
1e-30; maximum normalized residual 1.46379865080953e-69. Generic noncommuting
coefficient-update identities, complete generator reconstruction, lower-order
cancellation, Q metrics/principals, initial normalization, omitted drift and
source controls all pass. No graph projection or new physical initial data.

R6 is computed and proved EXACTLY ZERO; its complete 20x2 matrix/key is retained.
R3,R4,R5 are genuine nonzero coefficients. Omission of EACH is detected above
1e-30 at at least one unchanged algebraic point for EVERY original mode.
V3's sole failure (71/72) wrongly demanded nonzero R6. Its FAIL source,
receipt and sidecars are preserved; read-only replay reproduced that failure.
V4 corrects the adversarial premise and strengthens genuine omission controls,
not the physical equations or numerical results. Crucially, V3 and V4 formulas
are BYTE-IDENTICAL: hash 682f7fc96bdb11a7a266ec10d0c6d95c6e91de39491ba3a4e220852d4f7be865.

Earlier computationally interrupted V1/V2 attempts remain preserved with no
mathematical verdict. A bounded private same-source V2 reproduction identified
R3 polynomial-GCD normalization as the slow operation; it is performance
evidence, not an admitted physics receipt. All private traces/logs remain local.
613 input/source/available-sidecar metadata preserve hashes, sizes and mtimes
through V4 computation and replay. No original trajectory, failed attempt,
scientific source or existing scientific sidecar was overwritten.

## Reproducibility and unpromoted gates

- [V4 contract](RES001_R4C1_G3N5_DUST_FINITE_ENERGY_V4_CONTRACT_2026-10-12.md):
  cf083f64ed76a91186ca4e1f6b69c63349274e02a01604dd375082d4a52a9072.
- [V4 executable](../../../Analysis/MasterTests/test_01_r4c1_g3n5_dust_finite_energy_v4.py):
  1e16a08d78a6152f78f3ceceb00dddca89f70928f04c76d293c8845fae9c9593.
- [Summary](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_finite_energy_attempt_04/summary.json):
  5310e9194079d2291a20e6857290f9a8f48ef9d33747e11b663139ea06dd08c7.
- Formulas: 682f7fc96bdb11a7a266ec10d0c6d95c6e91de39491ba3a4e220852d4f7be865.
- Diagnostics: 0a2a0846d6eea5cb7b5ff1ab1527dbf1cbe9a7528ed373b1e094d7e7c8c89a7e.

Fresh overwrite is refused. V4 passed-byte replay and V3 failed-byte replay
are both complete. The mathematical scoped sharp order two is unchanged.
Stage 1 remains OPEN for useful finite-band control. Stage 2 remains at
STOP_AND_ASSESS_DOMAIN_UNRESOLVED, with action selection deferred while the
operator-approved Stage-1 route continues. Stage 3 NOT ENTERED: genuinely
identifying matter-residue/nonlinear-force inputs remain absent.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Review/inherited dependencies DEFERRED; no canonical/publication clearance.
Native goal ACTIVE/incomplete. No new parent, commit, push, publication,
provider/model dispatch, vault mutation or runtime configuration change.
