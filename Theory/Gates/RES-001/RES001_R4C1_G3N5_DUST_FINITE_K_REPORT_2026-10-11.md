# G3N5: full finite-mode evolution versus the action-derived dust slow branch

Date: 11 October 2026 (Australia/Perth). Version 1.
Disposition: CONDITIONAL_FINITE_MODE_DUST_COMPARISON_DIAGNOSTIC.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.

## Outcome and interpretation

The full constrained R4C1/B1 linear system agrees increasingly closely with
the derived leading dust equations for the two registered prepared slow
initial directions. All 95 local identity/numerical checks pass, exact
read-only replay passes, and the predeclared finite-sample slow-comparison
criterion is met. This is conditional consistency evidence for this branch,
not observational support for ITSM or proof of full physical stability.

The dust-observable discrepancy decreases from 0.695582% at ell=4 to
0.00252331% at ell=64. Its approximately fourfold decrease per doubling is
consistent with an ell^-2 correction on this sample, but is not a uniform
remainder theorem. Independent complementary plenum-phase probes generate
nonzero dust response; that response and the full balanced graph distance
are not uniformly monotonic across the sample. Prepared slow data cannot
be substituted for arbitrary initial data.

The [owning weighted-dust report](RES001_R4C1_G3N5_SLOW_DUST_WEIGHTED_REPORT_2026-10-11.md)
remains unchanged. Its K=-11/6, original ordinary-wave Jordan defect,
negative parent spatial energy and indefinite complete density Hamiltonian
are retained. No mode, global dust-charge sector or adverse sign is deleted.

## Frozen sources and reproduction

- [Pre-execution contract](RES001_R4C1_G3N5_DUST_FINITE_K_CONTRACT_2026-10-11.md):
  SHA-256 e8a27ba03b11cd0137ecf1b566db761f0d4ee356700911a500235e95fcd9221d.
- [Executable v1](../../../Analysis/MasterTests/test_01_r4c1_g3n5_dust_finite_k_v1.py):
  SHA-256 e6dbcd4d36c6bd1ac505ecc4d8190e43c16798588f131d1763e4dccdfe8e36f6.
  Frozen before first scientific execution; no executed source was edited.
- [Attempt-01 receipt](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_finite_k_attempt_01/summary.json):
  SHA-256 a4c884469c39682908d894e23cb5fbdaa370a4a46f5aa2c31ae4a14128c0f706.
  PASS_LOCAL_CHECKS, 95/95; no failed or unknown current checks.
- [Exact matrices](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_finite_k_attempt_01/matrices.json),
  [diagnostics](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_finite_k_attempt_01/diagnostics.json)
  and [full trajectories](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_finite_k_attempt_01/trajectories.json).
  The trajectory artifact retains all chart states and all 22 reconstructed
  fields, with complex values stored as explicit real/imaginary pairs.

```powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Analysis/MasterTests/test_01_r4c1_g3n5_dust_finite_k_v1.py --replay Analysis/MasterTests/outputs/r4c1_g3n5_dust_finite_k_attempt_01
```

Replay recomputes and byte-compares all four JSON outputs and their sidecars;
it passed. The main calculation preserves 401 input/sidecar files. The
before/after replay audit preserves 409 unique inputs/outputs/sidecars in
SHA-256, size and UTC last-write ticks. Source pins and Python snapshot
hash/size/mtime_ns checks also pass. Same-agent derivations and independent
numerical algorithms are not external Rule-9 review.

## Domain, observables and complete evolving system

Use the unchanged classical conditional B1 action and registered parameters,
including the conditional numerical K_Q=3; microscopic K_Q is not derived.
The coordinate torus periods are 2*pi, k=(ell,0,0), ell in {4,8,16,32,64},
and t_E in [0,0.05], at 257 comparison times. Negative conjugate modes and
both real Fourier quadratures are retained. Units are B1's registered
dimensionless normalization, not an inferred physical torus/EFT scale.

All ten complex chart coordinates and twenty first-order states evolve.
The source rebuilds the chart from the frozen action and independent Euler
export, verifies E0,E1,E2 against the saved A,R,K, and reconstructs all
auxiliaries, including Em and LambdaU. The full 22-field reconstruction and
independent dust-current identities vanish exactly on the explicit B1
Friedmann constraint; this on-shell redundancy is declared, not hidden.

For x=(y,y_dot), x_dot=L*x. Define the actual observable map O by

```text
delta_rho = C^4*Em + 4*beta*rho_m*Pi
D = delta_rho/(i*p*rho_m), p=ell/a, p_dot=-H*p
O*x = (D,Vx), beta=2/5
M = [[H,1],[6*rho_m/11,-H-2*psi_dot/5]]
R_observable = O_dot+O*L-M*O
```

L, O and R_observable are derived and exported without imposing M on the
full evolution. The background and leading transfer reuse the frozen
70-digit degree-40 data, evaluated by binary64 Horner arithmetic for the
new IVPs. The new perturbation integrations are not claimed to be 70-digit.

## Initial data and balancing are not an invariant restriction

The saved formal slow lift G maps (Vx,Vx_dot) to the full x, including
background derivatives and p drift. The instantaneous diagnostic graph is
E=G*(O*G)^(-1). Its sampled condition number ranges up to 18.98055; all
registered points are regular, with rho_m,C,a,p>0. No rho_m=0 or k=0 inverse
is taken. The homogeneous sector remains a separate owning calculation.

The two slow initial columns are E(0)*(1,0) and E(0)*(0,1); their actual dust
observables start at the same identity matrix as the leading transfer Phi.
Full evolution is unrestricted thereafter. E is used only for initial data
and comparison; the full state is never projected back onto it.

In the parent's SO(2) basis, numerical balancing uses positions
(p*h,p*TT+,p*TTx,Vx,Vy,Vz,p*du,p*dv,p*dr,chi), with
chi=p^2*Pi-i*p*psi_dot*Vx. Their derivative coordinates are divided by
(p,p,p,p,p,p,p,p,p,p^2), respectively. With z=B*x, the integrated generator
is (B_dot+B*L)*B^(-1); the exact inverse and B_dot contribution are verified.
This is a mixed-order numerical norm, not a canonical positive energy or
proved full-system well-posedness norm.

Two complementary probes start along balanced chi-position and chi-velocity
directions. Only at t=0, their E*O component is subtracted and each is
normalized to unit balanced vector norm. Their initial actual dust signal
is zero; they are not certified pure fast eigenmodes. All subsequent fast,
wave and dust responses are retained. Unit columns are transfer directions
for infinitesimal perturbations and may be scaled by an arbitrarily small
common amplitude; no finite-amplitude nonlinear evolution is claimed.

## Quantitative comparison

For slow columns X_s, the registered discrepancy is
e_ell=max_t||O*X_s-Phi||_inf/max(1,max_t||Phi||_inf). The graph distance is
max_t||B*(X_s-E*O*X_s)||_inf/max(1,||B*X_s||_inf), with the denominator
evaluated at each comparison time before taking the maximum. Complementary
dust transfer is max_t||O*X_probe||_inf for the two normalized probe columns.
These are different norms/initial-data families, not interchangeable errors.

| ell | Slow discrepancy e_ell | Balanced graph distance | Complementary dust transfer |
| --- | ---: | ---: | ---: |
| 4 | 6.9558246e-3 | 4.7999113e-3 | 2.3177881e-2 |
| 8 | 1.6301556e-3 | 4.7101977e-3 | 1.0477270e-2 |
| 16 | 4.0403071e-4 | 7.9441560e-3 | 1.5471615e-2 |
| 32 | 1.0100870e-4 | 4.0399200e-3 | 5.7759222e-3 |
| 64 | 2.5233102e-5 | 2.0255620e-3 | 1.8870966e-3 |

The fixed criterion e_64<=0.01, e_64<=e_32 and e_8>=4*e_64 is met;
e_8/e_64=64.603852. This boolean is separate from validation checks. The
sample supports the prepared slow approximation, but does not establish
its rate for all ell or all initial data. The complementary transfer is a
response amplitude, not a numerical error or proof of spontaneous instability.

The maximum slow observable-equation defect ||R_observable*X_s||_inf
decreases through 0.16157548, 0.03825236, 0.00945418, 0.00235705 and
0.000588862. The slower/nonmonotonic balanced graph distance is retained;
the favorable dust-observable result is not a claim that every full field
has the same convergence behavior.

## Independent numerical controls

All DOP853/Radau runs (rtol=1e-10, atol=1e-12) and refined DOP853 runs
(rtol=2e-12, atol=2e-14) complete the full window. Worst discrepancies are
3.3292762e-9 in normalized balanced state and 1.1119297e-10 in actual dust
observables, both below the frozen 2e-7 limit. These are smaller than the
reported slow-model discrepancy and complementary response.

The all-22 analytic normalized Euler residual is at most 1.9640816e-13
(limit 1e-9). Independent five-point differentiation of reconstructed fields
at T/4,T/2,3*T/4 uses the exact registered h and h/2 rules. The worst fine
normalized Euler residual is 4.4584253e-7 (limit 1e-5); all refinement
criteria pass. Steps and thresholds were not adjusted after execution.

Saved-background agreement is 1.0843989e-13, coefficient-rate residual
8.8817842e-16, and sampled Friedmann residual 1.2351231e-15 (all limits
1e-10). Fourier conjugation, complete reconstruction, observable leading
limit, balancing inverse/generator and all serialized round trips pass.

## Next bounded route and unchanged holds

The next useful route is an analytic slow/fast remainder calculation starting
from the exported R_observable and complete balanced generator. Identify the
first finite-p correction and retained fast forcing, then attempt a controlled
short-time estimate for the declared prepared-data family. More high-mode
sampling alone would not establish a uniform theorem or physical validity band.

All historical failed receipts and sidecars remain unchanged, including
nonzero main v1 103/106, separate principal v1 7/9 and binary64 response
120/125. The three inherited absent UVIR sidecars remain declared. The memory
skill's authority boundary keeps this classical B1 control distinct from
canonical cosmology and full physical stability; repository receipts remain
the scientific evidence, not historical memory or model agreement.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
All-direction evolution, physical cutoff/causality/ghost classification,
complete nonlinear source closure, healthy full GR, G_eff/PPN and microscopic,
weak-field and coefficient matching remain substantive. Rule-9 is DEFERRED,
not cleared; it does not alone prevent provisional reuse in this checked
domain. No publication-readiness or canonical promotion is claimed.

Only new research files and append-only queue/review entries are added;
only the two mutable index sidecars are refreshed. No manuscript/PDF,
vault/provider/runtime/model change, paid dispatch, commit, push, deployment
or submission is included.
