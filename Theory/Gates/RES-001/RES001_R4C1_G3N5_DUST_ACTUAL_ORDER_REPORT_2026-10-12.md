# G3N5 original dust error: mathematical sharp order two, useful domain open

Date: 12 October 2026. Version 1. Owner: Stage 1 / RES-001 / Master Test 1.
V2 result: **60/60 local checks**, zero failures/unknowns; read-only exact
scientific artifact/sidecar replay complete, terminal exit 0.
Disposition: **MATHEMATICAL_ORDER_TWO_CHECKED_USEFUL_DOMAIN_OPEN**.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.

## 1. Result and its exact scope

For the registered prepared two-column initial-data family of the LINEAR
rotating B1 diagnostic, the uniform original dust-observable error has sharp
mathematical asymptotic order ell^-2. This is derived from a controlled full
error expansion and a nonzero lower witness, not fitted to the five modes.
It is an operator/family statement with one explicit nonzero prepared column;
it does not assert the same leading coefficient for every individual variable
or arbitrary complementary initial state.

The sufficient domains are extremely conservative. The retained-response
estimate begins at ell>=8192. The sufficient lower-witness threshold is a
2248-digit integer, approximately 1.6605867155*10^2247. Its exact value is
`constants.sharp_order_min` in
[formulas.json](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_actual_order_attempt_02/formulas.json).
This is NOT a physical cutoff, an accessible EFT band or a new model scale.
There is no assertion that the physical theory reaches this mathematical
asymptotic domain. Useful error control at the original ell=4,8,16,32,64
remains OPEN; the full dust milestone and native goal remain incomplete.

## 2. Complete retained response, without graph projection

Retain all 20 states and the full rotating background/constraint/momentum
drift. Set eps=1/ell and use the coordinate change

    T=(I+eps^2 V)(I+eps S_wave)(I+eps^3 S_fast),
    D_eps=diag(eps^3 on slow, eps^2 on waves, eps on fast).

The complete weighted generator has its Q-skew dispersive and wave principals
plus a bounded remainder. Its exact nonprincipal numerator has no negative
epsilon powers. The constant weighted transform is I+N with N^2=0; the
whole-background Neumann bound controls its remaining inverse. Include dot(T)
and dot(Q). Q is an evolution norm, NOT a physical Hamiltonian/ghost clearance.

Bound the FULL corrected original-data numerator

    D_eps^-1 C_w(0)[E_orig J_obs(0)-H_c(0)],

not only the old-lift limit. The actual observation map has the required eps^3
factor after weighting. The resulting homogeneous mismatch response obeys

    ||W_retained||_infinity
      <= C_ret eps^3 exp(gamma t) ||W0||_infinity,

on the inherited B1 Friedmann/charge shell, 0<=t<=1/20, ell>=8192, with the
registered positive a,C,rho_m and nonzero-mode constraint domain. Exact rational
constants are sealed in formulas.json; displays are gamma=93720.36411764711,
C_ret=12853305.797499813, weighted initial numerator norm<=1.7996805418309343.
The large rate reflects a conservative norm majorant, not measured instability.

## 3. Controlled observable expansion and lower witness

Combine the complete retained-response bound with the previously replayed
positive forced-remainder bound and an explicit normalized reference expansion:

    W_full = Phi_M W0 + eps^2 Z W0 + R_total,
    dot(Z)=M Z+N_obs Phi_M, Z(0)=0,
    ||R_total||_infinity<=C_total eps^3 ||W0||_infinity.

N_obs includes the observation-chart drift/commutator; it is NOT just the
lift-chart N2. No state is repeatedly projected onto a slow graph. Exact
inverse, exponential and interval constants are retained. Integer upper
bounds for exponentials are used; no floating overflow represents a proof.
The complete C_total has display log10(C_total)=2243.376335711174, illustrating
why this certificate does not establish practical finite-mode accuracy.

The blindly computed initial observable coefficient is
N_obs(0)[0,0]=372/1375>0. A whole-interval Z'' bound gives the fixed rational
witness time (display) t_w=0.0021178436810168786 and lower coefficient
c_lower=0.00014324324533423254. At the sealed sufficient ell threshold,

    sup_[0,T] ||W_full-Phi_M W0||_infinity >= c_lower eps^2,

for W0=e1 (or its scaled column). This rules out a universal order-three
original-error claim. The existing replayed leading order-two upper bound
provides the other inequality, with separate original low-mode bounds retained.
No acceleration target, observed slope or desired coefficient fixes the witness.
This coefficient is a diagnostic response, NOT C_chi or a prediction of a0.

## 4. Failure caught and preserved

V1 completed with FAIL_LOCAL_CHECKS 46/52. Its new reconstruction retained
residual_numerator_0..2 but omitted stored terms 3,4,5. Six independent raw-
original-generator controls rejected that reconstruction at the frozen 1e-30
criterion. V1 source/contract/sidecars and all failed receipts remain untouched.

V2 imports every stored term 0..5, updates the complete weighted numerator and
its bounds, and explicitly rejects the intentionally truncated formula at all
six raw-generator control points. The action, frozen original generator,
original data and previously accepted forced/observable certificates have NOT
been repaired or rewritten. This was a defect in the NEW proof implementation.
The tolerance and precision were not relaxed to turn failure into PASS.

V1 summary SHA256:
a2ad4bb350581fc44d9175425f0ce9440600024c5d82944c6c11f51c6f31aedc.
Its candidate constants/order are not accepted evidence.

## 5. Independent controls and integrity

70-digit controls compare the complete transformed equation against the full
original balanced generator at ell=8192,16384 and t=0,0.025,0.05. Largest
normalized residual is 3.767248220419398e-63, below the unchanged 1e-30
criterion. Shell H is evaluated algebraically for these identity samples only;
no original trajectory or coefficient evolution is projected or changed.

Independent DOP853/Radau integrations of the observable coefficient agree to
2.7712207528729493e-15. Their numerical witness is 0.000573823168269903;
the analytic lower claim follows from exact bounds, not this sampled value.
All separation/inverse/partition/drift/complete-initial-data/domain checks pass.
551 inherited input/source/available-sidecar files preserve hashes, sizes and
mtimes through both calculation and replay. Original five modes, four columns
and nonmonotonic complementary responses are preserved; unchanged full-state
audits are reused, not re-solved or presented as new results.

## 6. Reproducibility and remaining gates

- [V2 contract](RES001_R4C1_G3N5_DUST_ACTUAL_ORDER_V2_CONTRACT_2026-10-12.md):
  a66a155ac2d490c96854678044379b7c1009e88c8c54465b904d99b8a5dc7226.
- [V2 executable](../../../Analysis/MasterTests/test_01_r4c1_g3n5_dust_actual_order_v2.py):
  5a81dd41d21f148560fa49112f207336bdee5469152e97a1cdf634e7b5c8cb87.
- [V2 summary](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_actual_order_attempt_02/summary.json):
  04a100622d6265936dd8501ae85bf6db9fa59b4afacf64c1c2bba086e259d478.
- Formulas: 127fe036d72342190389acd6436bf3f846bb42ab00e3637fa4f19766351bb8ca.
- Diagnostics: 3b9cf5f76b16fbd2404a883a104b79150de4e626e9d0c6605c707b1859d35dc0.

Exact read-only replay reproduces all three artifact and sidecar bytes.
Use the frozen V2 executable with --replay and attempt_02; fresh-run overwrite
is refused. Private logs/context are not publication artifacts.

The mathematical order question is resolved ONLY in the stated linear-family
asymptotic scope. Useful finite-band approximation and compatibility with a
physical window are not resolved. Stage 2 remains at its operator action-
selection reassessment point: full nonlinear coupled physical interactions,
physical band, healthy GR, zero/singular/fixed-charge reduction and full matter-
coupled local gravity are still needed. No action selection is inferred from
the operator's earlier agreement to reassess later. Stage 3 is NOT ENTERED;
genuine identifying matter-residue/nonlinear-force matching inputs are absent.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Rule-9 reviews/inherited dependencies remain DEFERRED; no canonical promotion,
publication, commit, push, provider/model dispatch or vault mutation occurs.
