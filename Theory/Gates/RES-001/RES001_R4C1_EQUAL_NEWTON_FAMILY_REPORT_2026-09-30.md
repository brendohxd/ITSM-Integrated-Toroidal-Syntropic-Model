# R4C1-G3: equal Newton couplings, tensor cone and an alternate GR approach

Date: 2026-09-30. Owner: Master Test 1 / conditional R4C1-v1.
Disposition: `CONDITIONAL_EQUAL_NEWTON_BACKGROUND_GR_LIMIT_OPEN`.
The [G3 contract](RES001_R4C1_EQUAL_NEWTON_FAMILY_CONTRACT_2026-09-30.md)
was frozen before execution. This is a separately declared coefficient and
initial-data family in the unchanged action; B1 and G1 keep their original
parameters and results. No observed acceleration, Hubble fit or galaxy data
enter. Independent review is deferred. `physics_pass=false`,
`canonical_Test1_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false`.

## 1. Direct tensor calculation

In the scalar-free, zero-exchange, zero-density on-shell Minkowski frame
control, take `U=partial_t`, lapse one, shift zero and the cross polarization
`gamma_xy=gamma_yx=epsilon q(t,z)`. Direct spatial Ricci contraction gives
the second-order Einstein spatial density

```text
M_P^2 [q qzz + (3/4) qz^2].
```

Its difference from `-M_P^2 qz^2/4` is the periodic surface term
`M_P^2 partial_z(q qz)`. Independently evaluating all four covariant frame
invariants shows that the first and third are `K_ij K^ij`, the second is
`K^2`, and the acceleration invariant vanishes on this aligned unit frame.
Combining EH/GHY and frame terms gives the physical tensor quadratic density

```text
L_tensor,2 = [(M_P^2-M_U^2 c_13) qdot^2-M_P^2 qz^2]/4,
c_tensor^2 = 1/(1-alpha_13).
```

Scalar/vector auxiliaries do not mix linearly with this tensor representation
on the isotropic vacuum control. Omitting the frame term or reversing its
kinetic sign fails the exact check. The matter metric is conformal, so its
vacuum light cone is the metric light cone used for this speed comparison.
This does not replace a full interacting-background tensor/PPN calculation.

## 2. Separately frozen family and finite-parameter result

Use `M_P^2=1`, `M_U^2=(2/3)eta`, `c_1=1/5`, `c_4=1/20`,
`c_2=-7/48`, `c_3=-1/80`, with `0<eta<=1`. Hence

```text
alpha_13=eta/8, alpha_14=eta/6, alpha_2=-7 eta/72,
alpha_L=eta/36, M_c^2=1-eta/12, M_t^2=1-eta/8,
G_cos/G_static=1,
K_vector=eta/6,
c_vector^2=4/5+3 eta/[8(8-eta)],
c_tensor^2=8/(8-eta),
D/H^2=144 (1-eta/12)(1-eta/8)/eta.
```

The vector result uses G1's metric-shift-reduced transverse coefficients;
the scalar `D` and kinetic-square structure are inherited from S1. All
listed kinetic weights are positive at finite positive `eta` on the expanding
regular nonzero-mode chart. This is a parameter evaluation of that certificate,
not a new full scalar constraint reduction or a gradient/hyperbolicity proof.
At `eta=1`, `c_tensor^2=8/7`, `c_vector^2=239/280`; sampled `D` ranges
from `2.441066845` to `104.07` on `[0,4]`.

Scale B1 `zeta,K_Q,b,g_r` by `eta`, `A` by `eta^(3/2)` and `beta` by
`eta^2`, as frozen before execution. The force invariants then obey

```text
A/K_Q^(3/2)=2 sqrt(3)/63,
b/K_Q=5/33,
beta/sqrt(K_Q)=(2 sqrt(3)/15) eta^(3/2).
```

This explicitly removes G1's divergent canonical cubic *on this different
path*. It neither changes G1 nor derives any microscopic coupling or cutoff.
Initial scalar/reservoir amplitudes and velocities scale as the contract
states; each member's conserved initial charge is `eta`. This is not a
fixed-nonzero-charge limit. The exact Einstein-dust endpoint is a separate
background control; the endpoint theory still has canonical spectator scalars.

## 3. Two-method background approach and the preserved failure

All six DOP853 and six Radau integrations finish on `[0,4]` with finite
sampled fields and positive `a,H,rho_m`, using `rtol=1e-11`, `atol=1e-13`.
The largest normalized two-method state difference is `1.539e-11`.
The largest normalized Friedmann residual, charge drift and dust-integral
drift across the recorded methods/family are below `1e-8`. The DOP853
maxima are respectively `5.654e-12`, `1.989e-11` and `3.117e-12`.

| eta | Maximum normalized metric/dust error against Einstein-dust |
|---:|---:|
| 1 | 1.035073234 |
| 1/4 | 0.292319345 |
| 1/16 | 0.086764089 |
| 1/64 | 0.023493392 |
| 1/256 | 0.006020876 |
| 1/1024 | 0.001515190 |

The errors decrease at each fixed refinement; the last ratio is
`3.973676366`. This supports a finite-time **background** approach, without
a cosmological calibration or uniform physical perturbation-limit claim.

The original G3 attempt remains **112/113**, `FAIL_LOCAL_CHECKS`.
Its only failed assertion is the independently finite-differenced eta=1
sector balance on 801 points: reservoir residual `1.100563523e-7` exceeds
the frozen `1e-7` bound. The full spatial Einstein residual at that grid,
`2.427593385e-8`, passes. The action, family, acceptance bound, script and
failed receipt were preserved.

A separately frozen **post-failure** [refinement contract](RES001_R4C1_G3_FD_REFINEMENT_CONTRACT_2026-09-30.md)
then tests 801,1601,3201 time samples at the same integration tolerances and
unchanged physical parameters. Both fresh integrations reproduce their saved
801-point trajectories exactly. DOP853 maximum sector residuals become
`1.100563523e-7`, `7.143422960e-9`, `4.548167799e-10`; Radau gives
`1.100580140e-7`, `7.143331317e-9`, `4.543280288e-10`.
The consecutive improvements are about `15.4` and `15.7`, consistent with
the five-point derivative's fourth-order truncation error. At 3201 points,
the spatial Einstein residual is `2.646e-10` (DOP853) and `3.555e-10`
(Radau). The supplementary study passes **18/18** with the same `1e-7`
bound; it does not rewrite the original 801-point assertion or certify
continuum/physical stability. Both original and supplementary receipts replay
byte-identically in memory, with their respective failed/passed exit statuses.

## 4. General cone consequence and remaining GR question

As a post-run analytic consequence, combine the new vacuum tensor formula
with G2's common-coefficient equality condition and positive S1/G1 weights:
`alpha_13>alpha_14/2>0`, `alpha_13<1`. Therefore the control has
`c_tensor^2>1`. Indeed

```text
(c_tensor^2-1)-alpha_14/(2-alpha_14)
  = (2 alpha_13-alpha_14)/[(1-alpha_13)(2-alpha_14)] > 0.
```

The rational identity was independently simplified with SymPy. This compares
necessary **coefficient conditions across the two stated controls**, as G2
does; it is not a claim that they are the same solution. Equal Newton
couplings plus these positive kinetic signs cannot supply an exactly
matter-luminal tensor control at finite frame coupling. A wider tensor cone
alone is not an all-sector instability theorem or an observational exclusion;
no numerical GW/PPN bound is applied here.

On the chosen family, the tensor cone approaches the metric cone, but
`K_vector=eta/6` and `K_Q=3 eta` tend to zero, and S1's auxiliary block
loses rank at the endpoint. A finite canonical cubic is useful but does not
resolve unit-frame nonlinear interactions, strong coupling, the physical EFT
cutoff, the dust zero branch, or full interacting scalar/vector/tensor
well-posedness. Thus healthy continuous GR recovery remains **open**.
No all-path no-go follows from vanishing coefficients in this particular chart.
The next discriminating work is the alternate family's constrained interacting
symbol and endpoint canonical interactions, using this background with its
new coefficients rather than reusing B1's evaluated matrices unchanged.

## Provenance and reproduction

- G3 contract SHA-256: `4bb989979850468d4322baeec9cbdaaaadd8318825724042711c062fc944e9f8`.
- G3 executable SHA-256: `dfdec7c78ae4e57f247b2592b611e79d808d708813358a6dac015c387a7d9440`.
- [Original G3 receipt](../../../Analysis/MasterTests/outputs/r4c1_g3_attempt_01/summary.json): `930dc4300fe47698ef1b5938214811fda3b5aed6c4d96361e5f9cceebd4d7c75`.
- Both-method trajectory data: `b0179f04368a860baabe0d9713a65a809c638ffdab35edc7071a4656c77c6506`.
- Refinement contract SHA-256: `44ff0e69324dded972029696c445a70f76b94b856771e5e0302fa66b94d722a4`.
- Refinement executable SHA-256: `9992b5277b52efc955e778a7b0aa675a3f3d0d2bbaf662d4aef63865d009f4a7`.
- [Supplementary receipt](../../../Analysis/MasterTests/outputs/r4c1_g3_fd_attempt_01/summary.json): `00ceee7e06cca286baab567e169373ce2b5d1b8ec057f5a7fd5746d6c6748c98`.

Use `C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B` with
`Analysis/MasterTests/test_01_r4c1_equal_newton_family.py --replay`
(exit 1 reproduces the preserved failed 801-point check) and
`Analysis/MasterTests/test_01_r4c1_equal_newton_fd_refinement.py --replay`
(exit 0 reproduces the supplementary result). New output attempts refuse an
existing directory; source-pin mutation is rejected before output creation.
No earlier `main()` was invoked. Python 3.13.9/SymPy 1.14.0 and numerical
runtime versions are recorded in the receipts.

Review debt inherits R9-MT1-VARIATION/B1/G1/S1/G2. Independent review must
check the tensor boundary/normalization, coefficient comparisons, S1's generic
certificate, family initial constraints, refinement history and distinction
between background convergence and a healthy GR/EFT limit. Research use is
`PROCEED_PROVISIONALLY` for these precisely scoped diagnostics; the failed
801-point assertion cannot be reused as a passing check. Canonical Tests 1–3
remain `HOLD_SUBSTANTIVE`. `MAT-001=BLOCKED`, `UVIR-003=IN_PROGRESS`,
`K_Q=NOT_DERIVED`, `V=NOT_COMPUTED`, `Stage4A=CLOSED`; TOP-X4 is unchanged.
