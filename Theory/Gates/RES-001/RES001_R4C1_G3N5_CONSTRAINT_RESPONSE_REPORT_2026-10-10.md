# G3N5: full kernel, constraint-domain reduction and coupled periodic linear evolution

Date: 10 October 2026. Version 1. Status: LOCAL_CHECKPOINT_COMPLETE.
Conditional research; physics_pass=false; gate_effect=NONE; Rule-9 DEFERRED.
The approved bounded calculation and its exact read-only replays are complete.
This is not completion of the broader Tests-1-3 programme or publication review.

## What this establishes

The frozen R4C1 action now has a cross-checked unreduced 22-field quadratic
operator, an explicit gauge/auxiliary reduction with a separate homogeneous
chart, and a reproducible constraint-compatible coupled linear IVP on the
registered finite periodic-T3 benchmark. This is more than an isolated probe
mode or a static determinant: every unreduced Euler equation is reconstructed
and checked during the coupled evolution. It is not full nonlinear Test-1
closure, a physical stability theorem, canonical matching or calibrated cosmology.

| Component | Local outcome | Boundary |
| --- | --- | --- |
| Full kernel v2 | 33/33; exact read-only replay | 22 fields, 110 value/first jets, x/y/z; unreduced |
| Independent temporal comparison | 13/13; exact replay | All 484 entries and the pure-time action match exactly |
| Constraint-response v1 | 120/125; FAIL retained | Five binary64 finite-difference refinement failures |
| Separate 70-digit response v2 | 124/124; exact read-only replay, exit 0 | Same action, parameters, initial data, domains and original FD criteria |

Native goal scope: [approved plan](../../Core/ITSM_G3N5_CONSTRAINT_RESPONSE_GOAL_PLAN_2026-10-10.md).
The former broad Tests-1-3 programme remains unfinished; this checkpoint
does not redefine its completion criteria.

## Action, fields, background and registered domain

The [kernel contract](RES001_R4C1_G3N5_RESPONSE_KERNEL_CONTRACT_2026-10-09.md),
[export-only addendum](RES001_R4C1_G3N5_EXPORT_V2_ADDENDUM_2026-10-09.md),
[temporal-comparison contract](RES001_R4C1_G3N5_KERNEL_TIME_COMPARISON_CONTRACT_2026-10-10.md),
[response contract](RES001_R4C1_G3N5_CONSTRAINT_RESPONSE_CONTRACT_2026-10-10.md)
and [precision addendum](RES001_R4C1_G3N5_RESPONSE_PRECISION_V2_ADDENDUM_2026-10-10.md)
were frozen before their respective scientific execution.

Retain the ADM lapse, three shifts, six symmetric spatial-metric fields,
three frame boosts, Cartesian du/dv/dr, Pi, dust T/Em, regulator Z and
independent norm/multiplier nu/LambdaU. Gravity, all four frame invariants,
canonical potentials/portal, dust, normalized-frame force, alignment and
regulator sectors are retained. Spatial Ricci is converted by its checked
periodic divergence identity, not discarded. The a^3 Euler measure and time
derivatives of background coefficients are retained.

Use B1's registered parameters unchanged, including K_Q=3, A=2/7, b=5/11,
zeta=1/13 and beta=2/5; these are declared action parameters, not microscopic
matching results. The background is the finite-charge, homogeneous aligned,
zero-winding B1 restriction. Its initial positive H is fixed by Friedmann
only initially; H is not reprojected. Coefficient evolution agrees with the
retained B1 data. No old background CSV or receipt-writing main is overwritten.

Benchmark: t_E in [0,0.05], coordinate periods 2*pi, modes (0,0,0),
(1,0,0), (0,1,0), (0,0,1), (1,2,3), with conjugate negative modes for real
nonzero-mode fields. Generic initial perturbations populate every reduced
coordinate; the mean initial dv_dot is adjusted exactly as preregistered
to give zero linearized total U(1)-charge variation. There is no external
forcing, target-data fit, physical torus-length calibration or derived EFT band.

At Y=0 the nonanalytic term has zero linear kernel. Its unsmoothed directional
cubic density and second-order force, including the infinite harmonic tail,
remain retained upstream and unsolved here. Linear success neither supplies
an ordinary third Taylor vertex nor replaces the nonlinear G3N4 response.

## Gauge and constraint content

All four active minus-Lie gauge families are checked in every unreduced
equation: exact initial identities use H0^2=3469/4620; sampled normalized
gauge residuals reach at most 5.012e-14. Direct Fourier Euler matrices match
independent reconstruction from the complete quadratic action, including its
time-dependent coefficients and measure. Source-rate agreement is 4.45e-16.

For C>0, T=0 is the matter-clock time gauge. E_Em fixes alpha=-beta Pi.
E_LambdaU fixes nu=0; E_nu recovers LambdaU. E_alpha recovers Em, whose
evolution is checked in E_T. No normalization or dust equation is dropped.
For nonzero k the spatial gauge is k_i M_ij=0. The shift and Z equations
are eliminated only after their invertible auxiliary block is established.

With c13=c1+c3, the exact generic shift block is

~~~text
D_S=(k^2/a^2)*[(MP2-MU2*c13)*P_T/2-MU2*(c13+c2)*P_L]; D_Z=b.
~~~

Thus the inverse requires k!=0, a>0, b!=0, MP2-MU2*c13!=0 and
MU2*(c13+c2)!=0. Exact auxiliary-rank controls cover the regular block,
k=0, b=0, MU2=0, longitudinal-zero and tensor-coefficient-zero boundaries.
No inverse is applied on a singular boundary or claimed to continue through it.
Action-Schur and unreduced-Euler reductions agree exactly.

The k=0 mode is included, not excluded: homogeneous shifts are fixed by
translations, all six metric components remain, and Z=0 is solved separately.
The regular nonzero chart has ten coordinates; the mean chart has thirteen.
These are coordinate counts, not an asserted global physical DOF count.
The acceleration-matrix condition numbers are 49.5 and 18 respectively.

## Kinetic signatures are not hidden

| Registered chart | Time-matrix inertia | Interpretation retained |
| --- | --- | --- |
| Nonzero modes | 10 positive, 0 negative, 0 zero | Positive chart time block, not a full physical stability result |
| Homogeneous mode | 12 positive, 1 negative, 0 zero | Negative eigenvalue -0.55; physical energy/constraint interpretation remains open |

The signatures are unchanged between numerical methods. The high-precision
driver verifies background independence of the registered acceleration blocks.
Neither selecting only nonzero modes nor automatically labelling the mean
direction a physical ghost would be justified by this checkpoint alone.
Canonical energy, gradient/characteristic domains, cutoff overlap, nonlinear
control and the healthy continuous GR limit remain separate substantive work.

## Numerical verification and the preserved failed attempt

Both DOP853 and Radau complete all five coupled IVPs. Their largest normalized
solution discrepancy is 1.318e-10 against <=1e-7; all 22 analytic Euler
equations have maximum normalized residual 1.920e-14 against <=1e-9.
The mean linear-charge drift/amplitude is 3.279e-13 against <=1e-8.

Response v1 nonetheless remains FAIL_LOCAL_CHECKS, 120/125. Each of its
five binary64 finite-difference refinement checks fails: finest residuals
2.09e-9 to 1.16e-8 are below the bound, but coarse/fine ratios 0.325 to
0.446 violate >=4-or-both<=1e-10. These original failures remain in their
immutable receipt and are explicitly inherited in the new diagnostics.
No threshold, original equation, initial-data rule or numerical record is edited.

The new driver reuses the frozen v1 operator and reduction proofs; it never
calls v1's receipt-writing main. It uses 70-digit arithmetic and a degree-40
autonomous Taylor recurrence for the same background and coupled equations. Synthetic series
controls pass. True polynomial first/second derivatives, not the RHS alone,
test the reduced and full Euler equations. Degree-32/40 comparison gives
maximum response tail 2.594e-32 against <=1e-20; background tail is
5.850e-35 and Friedmann residual 5.261e-43. These are finite-window
convergence witnesses, not a rigorous global analytic-radius theorem.

Full Euler residuals from true polynomial derivatives are <=1.055e-37;
reduced residuals <=1.334e-37. The new full-field trajectories agree with
retained v1 trajectories within 1.940e-11 against <=1e-7. The mean
linear-charge drift/amplitude is 5.224e-41.

| Mode | 65-point FD error | 257-point FD error |
| --- | ---: | ---: |
| (0,0,0) | 4.314e-12 | 1.702e-14 |
| (1,0,0) | 9.468e-12 | 3.731e-14 |
| (0,1,0) | 9.466e-12 | 3.730e-14 |
| (0,0,1) | 9.468e-12 | 3.731e-14 |
| (1,2,3) | 9.678e-12 | 3.813e-14 |

All five modes meet the unchanged <=1e-5 finest error and
>=4-or-both<=1e-10 refinement criteria (coarse/fine about 254). The
independent higher-precision trajectory and derivative calculation support
a numerical verification limitation in v1 on this benchmark, not an observed
mathematical inconsistency of the tested IVP. This comparison does not isolate
binary64 cancellation from dense-output interpolation error; the numerical
evaluation method changes both. It is not a stability proof.

## Integrity, reproduction and remaining obligations

All 154 transitive source pins and 151 available sidecars match before and
after the precision calculation. Three inherited UVIR-003 absences and
the original G3/N3 failures remain declared. The original response-v1
attempt remains byte/hash/size/timestamp-preserved. Full-kernel and temporal
comparison exact replays preserve their ten and four files respectively.
Response-v2 read-only replay returns READ_ONLY_REPLAY_EXACT, 124/124,
exit 0. All eight payload/sidecar files retain identical hashes, sizes and
UTC last-write timestamps. The twelve original response-v1 files retain
these same metadata properties, including the failed receipt.

~~~text
python -B Analysis/MasterTests/test_01_r4c1_g3n5_response_kernel_v2.py --replay Analysis/MasterTests/outputs/r4c1_g3n5_attempt_02
python -B Analysis/MasterTests/test_01_r4c1_g3n5_kernel_time_comparison_v1.py --replay Analysis/MasterTests/outputs/r4c1_g3n5_time_compare_attempt_01
python -B Analysis/MasterTests/test_01_r4c1_g3n5_constraint_response_v2.py --replay Analysis/MasterTests/outputs/r4c1_g3n5_constraint_response_attempt_02
~~~

Fresh runs refuse existing destinations. Retained evidence includes the
exact sparse kernel/Euler exports, reduction coefficients, original solver
trajectories, high-precision Taylor coefficients and reconstructed 22-field
trajectories. These mathematical and numerical cross-checks use declared frozen inputs
and local controls authored in this workflow; they are not independent
external referee review.

Receipt navigation: [full kernel](../../../Analysis/MasterTests/outputs/r4c1_g3n5_attempt_02/summary.json),
[temporal comparison](../../../Analysis/MasterTests/outputs/r4c1_g3n5_time_compare_attempt_01/summary.json),
[preserved failed v1](../../../Analysis/MasterTests/outputs/r4c1_g3n5_constraint_response_attempt_01/summary.json),
[70-digit v2](../../../Analysis/MasterTests/outputs/r4c1_g3n5_constraint_response_attempt_02/summary.json)
and [precision driver](../../../Analysis/MasterTests/test_01_r4c1_g3n5_constraint_response_v2.py).

Key SHA-256 anchors:

- Full-kernel summary: 560e369d7795ed8e06d0c2c26350d3b412a53c577da82f0669e68f6ee04f5666
- Temporal-comparison summary: 2fb997e71b2fe24cc3aa8e458a26663c65165bcba068b3a12e40aedaae11d261
- Failed response-v1 summary: b13e97122e724e58465db28df036ee835fd305b31078146cb7a283da38ee9d95
- Response-v2 summary: 04705ea37aa944a567387073b1eda81c824d447566d061ddfd684abfbf30649d
- Response-v2 source: 6c1f2417b7a17ae5a07df07ae0957e6f66259d15398d8db9a39e9b57b3ffea9f
- Response-v2 series coefficients: ca95d2b2cf38facbcad6367aa6ef211c2ec9a2915d8b7aa8b33cba02256d0d8a

Available for provisional reuse: full linear operator, explicit regular and
mean constraint charts, compatible first-order data/evolution and reproducible
coefficient maps on this declared branch. Still missing: nonlinear unsmoothed
source-driven evolution, physical characteristic/cutoff/stability interpretation
(including the mean sign), healthy continuous GR and the coupled physical
weak-field/microscopic matching inputs. The result does not compute G_eff,
PPN observables, canonical K_Q/V, the projection factor or a0(z).

Review scope inherits B1, background matching, G3N4, G3N5 kernel/comparison
and all earlier scientific/review debt. Rule-9 is DEFERRED, not cleared;
it does not alone prevent provisional research. Physical missing inputs
continue to block their dependent claims. Unchanged: Tests 1-3 HOLD_SUBSTANTIVE;
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; TOP-X4 unchanged; physics_pass=false; gate_effect=NONE.

No original scientific source/receipt/frozen sidecar/action/threshold is
rewritten. The queue and deferred-review register receive dated append-only
entries; their original byte prefixes and private pre-append copies are checked.
Only those mutable index sidecars and the new report's sidecar are refreshed.
No manuscript/PDF/vault/provider/runtime change, commit, push or publication.
