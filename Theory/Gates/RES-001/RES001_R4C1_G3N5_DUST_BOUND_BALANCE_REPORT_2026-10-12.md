# G3N5: tighter original-error bound, physical/useful domain still open

Date: 12 October 2026. Version 1. Owner: Stage 1 / RES-001 / Master Test 1.
V3: **72/72 local checks**, zero failures/unknowns, exact read-only scientific
artifact/sidecar replay complete, terminal exit 0. The mathematical sharp
order-two theorem is unchanged. This refines its conservative bounds, not the
physical action or any trajectory. physics_pass=false; gate_effect=NONE;
Rule9_cleared=false; review DEFERRED. Full dust milestone remains incomplete.

## 1. Why the earlier majorant was loose

The complete unweighted order-zero remainder coefficient is identically ZERO.
Bounding its unsimplified expression term by term loses those cancellations.
V3 proves that identity before replacing the expression by zero and exactly
normalizes the leading weighted coefficients 0..2. Every stored generator
term 0..5 remains present; none is truncated or numerically discarded.

Then derive constant positive slow/wave/fast scales from whole-background
operator norms. Their displays are d_s=559.8345200488371, d_w=11.978215147987868,
d_f=1. The scale matrix R and its inverse are exact rational matrices, commute
with the two principals, Q and block-diagonal drift, and have zero derivative.
The weighted generator/transform use R^-1 (...) R; the FULL corrected initial
numerator uses R^-1; the actual observation map uses R. Thus the physical
solution/observables are unchanged. This is not a fitted coupling, altered
initial condition, slow-graph projection or a change in Hamiltonian signs.

## 2. Verified improvement and remaining limitation

| Quantity | Earlier V2 bound | New V3 bound |
|---|---:|---:|
| Sufficient retained-response ell minimum | 8192 | 64 |
| Evolution-norm rate gamma | 93720.36411764711 | 238.45618776630846 |
| Sufficient sharpness-threshold size | 2248 decimal digits | 16 decimal digits |

The new exact sharpness threshold is ell>=1059434477693447. This replaces
neither the old receipt nor its accurate historical report; both remain
immutable. These thresholds are sufficient MATHEMATICAL domains, NOT physical
cutoffs or evidence that an EFT band reaches them. A large majorant is also
not measured dynamical instability or an all-action no-go.

The complete retained response obeys the same scoped inequality

    ||W_retained||_infinity
      <= C_ret exp(gamma t) ||W0||_infinity / ell^3,

for the registered rotating B1 shell on 0<=t<=1/20, ell>=64. Displays are
C_ret=285548.03797280614 and gamma=238.45618776630846. Exact rational constants,
full corrected initial numerator, scale matrices and all domains are in
[formulas.json](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_actual_order_attempt_03/formulas.json).
Q remains an evolution norm, NOT a physical Hamiltonian/ghost clearance.

Combining retained response, the unchanged positive forced remainder and
normalized reference expansion gives

    ||W_full-Phi_M W0-ell^-2 Z W0||_infinity
      <= C_total ell^-3 ||W0||_infinity,

with C_total display 151756832803.7868. The fixed nonzero coefficient
N_obs(0)[0,0]=372/1375, rational witness time and lower coefficient remain
unchanged. The inherited upper inequality plus the controlled lower witness
still establish sharp order two for the registered linear prepared family.
This is NOT a per-variable universal order or a numerical acceleration law.

Although the retained-response domain now includes the highest original mode
ell=64, the bound is still much larger than its sampled error. Useful accuracy
for ell=4,8,16,32,64 has NOT been established. No imposed desired tolerance,
observed slope or parameter retuning manufactured this improvement.

## 3. Independent verification and preserved inputs

At ell=64,128 and t=0,0.025,0.05, 70-digit raw-original-generator controls pass
the unchanged 1e-30 criterion; the maximum normalized residual is
2.4154265590547058e-67. The intentionally truncated formula is rejected at
every point. Algebraic shell identity samples are not projected evolution.
Independent DOP853/Radau coefficient controls retain their disagreement
2.7712207528729493e-15. All exact rescaling/inverse/commutator, drift, interval,
full corrected-data, expansion/witness and source checks pass.

563 inherited input/source/available-sidecar metadata preserve hashes, sizes
and mtimes through calculation and replay. Original five modes/four columns
and nonmonotonic complementary responses are untouched. V1's 46/52 failure,
V2's valid theorem and all earlier sign/representation attempts remain intact.
No unchanged original trajectory audit is presented as a new calculation.

## 4. Reproducibility and next route

- [V3 contract](RES001_R4C1_G3N5_DUST_ACTUAL_ORDER_V3_CONTRACT_2026-10-12.md):
  278a3121a3a8c994d7bbc0aa3a4e7545ba7e49a2cccda562b603a430a6a75664.
- [V3 executable](../../../Analysis/MasterTests/test_01_r4c1_g3n5_dust_actual_order_v3.py):
  7d7da3e67e5a24736baea8956c6ca717a3d52ebcb50b521d50543c8a50cad5ab.
- [Summary](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_actual_order_attempt_03/summary.json):
  7f0888a9096145c42257bcccf84b8e7fdc3d98a1f10e05bbfd4f68a00dcf5c60.
- Formulas: ef4a9f5f7c383be848174b0041f6cbf738dcbece93bd14566f2ba3e34426497b.
- Diagnostics: 017c4db3ecf4764e86e9032339ca0d03494d23dd38fbb7ba56cbc91454353ac2.

Read-only --replay of attempt_03 reproduced all artifact and sidecar bytes.
Fresh overwrite is refused; local logs/context are not publication artifacts.

Within Stage 1, the remaining substantive task is useful finite-mode error
control, not another repetition of completed order audits. Stage 2's stopped
coupled-interaction/window route requires an explicit operator action choice;
the asynchronous route question remains unanswered at this checkpoint. No
default option, goal continuation or earlier promise to reassess is approval.
Stage 3 remains NOT ENTERED: identifying matter-residue/nonlinear-force
matching inputs are absent. No microscopic parent or TOP-X4 pivot is adopted.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Rule-9/inherited reviews DEFERRED; no canonical/publication promotion.
Native goal ACTIVE/incomplete. No commit, push, publication, provider/model
dispatch, runtime reconfiguration or vault mutation.
