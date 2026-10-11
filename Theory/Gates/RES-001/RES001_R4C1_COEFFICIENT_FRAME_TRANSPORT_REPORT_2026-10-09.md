# R4C1-C3: conditional force-scale transport and H-tracking compatibility

Date: 9 October 2026. Version 1. Master Test 3 necessary-condition diagnostic.
Status: **Conditional**. 43/43 local checks and exact read-only replay.
`physics_pass=false`; `gate_effect=NONE`; `Rule9_cleared=false`; review DEFERRED.
This is not a physical a0(z) prediction or a canonical Test-3 pass.

## Result and the remaining physical assumption

The [frozen contract](RES001_R4C1_COEFFICIENT_FRAME_TRANSPORT_CONTRACT_2026-10-09.md)
asks how C1's separately conditional instantaneous spherical force scale
transports into B1's matter clock. It does not derive a new force response.
Keep the weak-potential, spherical, frozen-frame, regulator-subleading,
compensated-source and negligible backreaction/time-response assumptions.
No common physical validity domain between C1's reduction and B1 has been
demonstrated, and no quasistatic error bound or physical cutoff is supplied.

Use c=hbar=1, C=exp(beta psi_bar) and P=C_proj, with P still unspecified.
For the constant-local-C unit comparison of the same conditional Newtonian
component, the exact bookkeeping is

```text
r_m=C r_E; dt_m=C dt_E; M_E=C M_m; rho_E=C^4 rho_m
G_m=C^2 G_E; A_m=A/C; b_m=b; K_Q,m=K_Q/C^2; z_m=z_E/C^2
a_dyn,E=beta^3/(12*pi*G_E*A); a_dyn,m=a_dyn,E/C
S=H_E+beta psi_dot; H_m=S/C
C_dyn=a_dyn,m/H_m=beta^3/(12*pi*A*G_E*S)
C_chi=C_dyn/P^2, only if g_psi=P sqrt(g_bar*a0) is established.
```

G_E is C1's unspecified G_static, not bare G and not an independently derived
coupled G_eff(k,z). The A_m map is a local unit map, not time evolution of the
frozen Einstein-frame action constant A. The full conformal transformation
for C(t,x), including its derivative terms and adiabatic errors, remains part
of the missing physical calculation. Both first-order regulator terms and
the eliminated regulator density were retained in the constant-C checks.

With A and beta fixed, the necessary condition for constant C_chi is

```text
d/dt_E [G_E(t)*(H_E+beta psi_dot)*P(t)^2] = 0.
```

The diagnostic makes this missing matching requirement explicit; it does not
select A, P, G_E or C_chi. It assumes neither P=2/3 nor a measured acceleration
normalization. Positive psi-chart rescaling leaves the coefficient, conformal
factor and regulator-to-flux ratio invariant. Wrong matter-clock, mass and
acceleration-unit maps leave exact nonzero generic residuals; C=1 and
beta psi_dot=0 can be nondiagnostic special points.

## Target-free background witness, not a calibrated universe

From the unchanged B1 action equations,

```text
S_dot=-(u_dot^2+v_dot^2+r_dot^2+K_Q psi_dot^2+rho_E)/(2 M_cos^2)
      -3 beta H_E psi_dot-beta^2 rho_E/K_Q.
S_dot(initial)=-42179/66000-sqrt(4006695)/9625
              =-0.8470417887680418.
```

Under a separately declared constant-G_E, constant-P control, constant C_chi
therefore does not arise automatically even at B1's initial point. Running
G_E or P could compensate in principle, but neither function is derived here.
This is not an exclusion of those branches or of all ITSM parents.

The code reads B1's saved 801 samples on t_E in [0,4]; it does not reintegrate,
retune or fit the background. The endpoint t_ref=4 is only a benchmark
reference, not today's cosmic time. Its z_ref=a_m(t_ref)/a_m(t)-1 is a formal
scale-factor coordinate, not an observed-redshift prediction: a photon/
radiation model, physical units and an observational likelihood are absent.

Only for the declared constant-G_E/P control,

```text
a_dyn,m(t)/a_dyn,m(t_ref)=C_ref/C(t)
C_chi(t)/C_chi(t_ref)=S_ref/S(t).
```

The benchmark's end/start ratios are 0.9644481035070235 and
6.634852123252589 respectively. The latter rejects an automatically constant
coefficient in this diagnostic, not a physical observational hypothesis.
Its maximum normalized separation from unity is 0.8492807403355099 against
the frozen 1e-4 rejection threshold. No absolute a0, C_chi, A or P is obtained.

## Verification and preserved failures

All 43 assertions pass. The exact symbolic checks cover local action-density,
source/flux and unit maps, background clock/continuity, the tracking identity,
chart invariance, regulator ordering and the wrong-map rejection controls.
Five-point centered finite differences use 201/401/801 saved sample subsets,
excluding two boundary points on each side. The finest normalized errors are:

| Transport control | 801-point error | 201-to-801 improvement |
| --- | ---: | ---: |
| Dust proper clock | 6.450609864952905e-11 | 207.24 |
| Matter expansion | 4.043915757812044e-9 | 203.53 |
| Matter dust continuity | 1.6224384502550038e-8 | 185.65 |
| Normalized force-scale log rate | 5.266402591797004e-10 | 194.78 |
| Normalized coefficient log rate | 5.0078330371405855e-9 | 214.09 |

Each satisfies this contract's new <=1e-6 error and >=4 improvement criteria.
They do not change any earlier threshold or certify unsampled/global evolution.
The original G3 `eta1_independent_fd_balances` failure remains
1.1005635230674148e-7 against <1e-7. Superseded N3 attempt-01 failures
`reject_direct_source_as_full_Z_solution` and
`all_direct_harmonics_exact_reconstruction` remain explicit in independent.json.

Before and after calculation, all 139 transitive source pins and 136 available
sidecars match. Three inherited UVIR-003 sidecar absences remain declared,
not repaired or hidden. Exact replay returns exit 0 without writing receipts;
all eight payload/sidecar files retain their hashes, sizes and timestamps.
There are no failed or unknown checks in this new receipt, but the substantive
physical inputs below remain absent. Model-authored controls are not an
independent external scientific review; the analyst is not blinded.

## Reproduction and immutable evidence

```text
python -B Analysis/MasterTests/test_03_r4c1_matter_frame_scale_transport_v1.py
python -B Analysis/MasterTests/test_03_r4c1_matter_frame_scale_transport_v1.py --replay Analysis/MasterTests/outputs/r4c1_c3_frame_transport_attempt_01
```

The first command refuses an existing attempt; use replay for retained evidence.
The [source](../../../Analysis/MasterTests/test_03_r4c1_matter_frame_scale_transport_v1.py)
has SHA-256 d76a6588cd2d99af742dd8a686349c19bc8bba7b87e86792ed90979ec3b1e830;
the contract has 3387bea692d703c047232f9fd242903690a3c7af978f4877a3d6567f218821ac.
Retained output directory: Analysis/MasterTests/outputs/r4c1_c3_frame_transport_attempt_01.

- summary.json: 1f1f5565a17113c88dead087e7f01366ab8c24b2e6a25cf7ecd6e3d097adf00f
- formulas.json: 6a6f4a8e2f5f26eb4474920e7b58c4d695ef7b56f11765d090c08d735d31e492
- independent.json: 1fb4e98010c6ce322fde2ad9f00097bce1d5070df995853b59f503d751d3d269
- normalized_profiles.csv: b1e66e393b6d9e1ba7b743c2a2eaa7657ef11cdda4f0c9635c2e0f2f333058e1

## Scientific and review boundary

Physical weak-field response, coupled G_eff, a common validity domain,
quasistatic remainder and physical a0(z) remain uncomputed. C_chi and P remain
NOT_DERIVED. Full Test-1 constraints/evolution/stability/healthy continuous GR,
coupled Test-2 response and independent target-free Test-3 matching remain
required; this necessary-condition checkpoint does not complete them.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.

Review dependencies: R4C1-C1, B1, G3N5 background matching and all inherited
scientific/review debt. Rule-9 review is DEFERRED, not cleared; it does not
alone block provisional research. Missing physical inputs still block their
dependent claims. Next scientific use requires the complete kernel and
compatible constraint solve before treating this transport as physical matching.
No action, old receipt, frozen sidecar, manuscript, PDF, vault or runtime
configuration is changed; no provider dispatch, commit, push or publication.
