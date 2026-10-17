# R4C1 source-aware cubic response: summable fields, physical window open

17 October 2026. Master Test 1 / RES-001 / unchanged-action Stage 2.
Conditional research result: 336/336 local checks; all nine cases and the
complete original summary reproduced exactly by the restartable companion.
Terminal READ_ONLY_PARALLEL_REPLAY_EXACT, exit0. The original serial CLI
was not observed to complete. Review DEFERRED; Rule9_cleared=false;
physics_pass=false; gate_effect=NONE. Full programme remains incomplete.

## Result and scope

The source-aware estimate improves the sufficient complete weighted
order-|e|^3 response bound from O(|m|^-1) to O(|m|^-3), for all nine
registered cases. All22 reconstructed field Fourier series at this order
are now absolutely summable, including density and multiplier. This
removes the previous negative-norm-only limitation for those fields.
It does not establish sharp decay, the full nonlinear solution, useful
accuracy, a physical cutoff, positive canonical energy or healthy GR.

The unchanged action, regular background, leading w(t)cos(40z) preparation,
coordinate2*pi torus and t in[0,1/20] remain. Families are archived_G3,
new_B1_frame and new_hierarchical, each at eta=1/4,1/64,1/1024. There is no
continuous-eta, eta=0 endpoint, arbitrary-background or all-direction result.
The response and lower coefficients use s_eta=eta^(7/2) normalization.
All20 nonzero-chart evolution states remain; the separate26-state mean and
retained m=+-2 bounds are inherited, not inserted into a singular inverse.

## Lower odd response with its initial transient

For signed odd n, the normalized lower equation is

```text
r_n_ddot+3H r_n_dot+[cV2(40n/a)^2+mV2]r_n=F c_n,
c_n=-4sin(n*pi/2)/[pi*n*(n^2-4)],
F=-3A psi_dot^3 w|w|/(f2*s_eta), f2=MU2(c1+c4).
```

Use the exact split r_n=u_n+B c_n/n^2, B=a^2 F/(1600cV2).
Then u obeys the same full operator with forcing -J c_n/n^2,
J=B_ddot+3H B_dot+mV2 B. Its initial data are NOT zero:
u_n(0)=-B(0)c_n/n^2, u_n_dot(0)=-B_dot(0)c_n/n^2.
The mass, friction, redshifting frequency and background/clock drift remain.

B and B_dot are continuous through w=0. B_ddot is bounded almost everywhere,
not a common classical second derivative at the cusp. Both sign branches,
matching and exact modified-energy identity are checked; no division by w
or delta impulse is introduced. The a.e. absolutely-continuous energy
argument applies across the zeros.

With outward rational background-box bounds MB>=|B|, MD>=|B_dot| and
MJ>=|J|, the exported constants are

```text
L=(5/4)(MD+41MB+MJ/20), R=L/12+MB, V=L+MD,
sqrt(Eu_n)<=L|c_n|/|n|,
|r_n|<=R|c_n|/n^2, |r_n_dot|<=V|c_n|/|n|.
```

These are continuous-time estimates. They use the inherited proved
cV2>=1/10, 40sqrt(cV2)/a>12, |mV2|<9 and energy Gronwall inequalities,
not sampled maxima. For |n|>=3, |c_n|<=(36/15)|n|^-3. Using
|m+-1|>=3|m|/4 for |m|>=4 gives seven-input decay powers
[5,4,5,4,3,3,4] and corresponding outward constants
[R(36/15)(4/3)^5,V(36/15)(4/3)^4,
 R(36/15)(4/3)^5,V(36/15)(4/3)^4,256/45,256/45,1024/105].

## Full fast particular response, not evolution on a projected graph

In the accepted full weighted chart,

```text
z_dot=Gz+Nf*s/d,
G=ell^2 Ffast_full+ell Lwave+drift+Nbar/d,
d=1-g/ell^2>=1, ell=40m,
Pnum=-embed_fast(Ffast_inverse*select_fast(Nf))/ell^2,
P=Pnum*s/d, z=v+P, v(0)=-P(0).
```

Here fast indices are9,19 in the twenty-state ordering. The complete
residual is retained:

```text
Pnum_total_dot=background_and_wave_derivative(Pnum)+Pnum*D_inputs,
Rnum=d*(slow_Nf+ell*Lwave*Pnum+drift*Pnum-Pnum_total_dot)
     +Nbar*Pnum+Pnum*d_dot,
v_dot=Gv+Rnum*s/d^2.
```

Exact full fast cancellation and the forced affine identity are checked.
Omitting denominator/input/basis drift or the compensating initial data
has a nonzero witness. No dynamical state is removed or continually reset.
The field and Euler-velocity reconstructions combine A*Pnum+d*Bsource
BEFORE bounding, so their exact source cancellation is retained.

The exact Laurent matrices determine, rather than presume, the powers:
particular-4, complete residual-3, full response-3 in every case.
Coefficientwise rational interval sums give CP,CR. With
CV=CP/4+CR/20 and CZ=CV+CP/4, the complete inherited Q-norm bound is

```text
sqrt(Ez_m(t))<=CZ exp(mu/40)|m|^-3,
sup_t sum_(|m|>N,m even) |m|^(2s) Ez_m(t)
 <=2CZ^2 exp(mu/20) N^(2s-5)/(5-2s), N>=4, s<5/2.
```

This includes the homogeneous initial compensation as well as the fast
particular response. The integer integral comparison also bounds the even
subset; signed-mode reality is retained. Exact case-dependent rational
constants, every matrix and every reconstructed bound are in case00--08.

## What regularity is now controlled

Worst common sufficient ranges for this PLANAR cubic sector:

| Reconstructed quantity | Coefficient bound | Spatial H^s range |
| --- | --- | --- |
| Ordinary nonzero metric/scalar/transverse fields and lapse | O(|m|^-4) | s<7/2 |
| Longitudinal Vz, shift Sz, regulator Z | O(|m|^-3) | s<5/2 |
| Density Em, multiplier LambdaU | O(|m|^-2) | s<3/2 |
| Ordinary Euler velocities | O(|m|^-3) | s<5/2 |
| Density Euler velocity | O(|m|^-2) | s<3/2 |
| Regulator Z Euler velocity | O(|m|^-1) | s<1/2 |

Gauge/symmetry-zero entries remain in the complete receipts. In particular,
B1-frame Sx/Sy and their Euler velocities vanish exactly in this sector;
the table reports worst-common nonzero estimates, not identical family rows.
The unused
LambdaU Euler-velocity slot is NOT an actual derivative bound: actual
LambdaU_dot remains NOT_BOUNDED. Absolute summability of all field series
does not assert summability of all velocity series or full classical
nonlinear PDE regularity. These sufficient bounds do not show saturation
or singularity of the true response.

## Why the physical window remains open

The mathematical Q norm is not a demonstrated positive canonical physical
energy. Its inherited amplification factor exp(mu/40) alone is enormous:

| Family | eta1/4: log10 factor | eta1/64 | eta1/1024 |
| --- | ---: | ---: | ---: |
| archived_G3 | 346.47 | 5284.50 | 84327.49 |
| new_B1_frame | 168.39 | 2515.20 | 40085.41 |
| new_hierarchical | 128.24 | 2458.94 | 40027.65 |

These are log10(exp(mu/40)), not log10 of the full prefactor and not
observed growth rates. They do NOT establish instability; they prevent
this estimate from certifying useful finite-amplitude physical accuracy.
The all-order constraint-compatible initial preparation, mixed-norm
nonlinear products/error estimate, physical energy/ensemble, admissible
frequency/momentum domain, directional and endpoint/GR evidence remain
substantive dependencies. No potential parameter or vacuum probe threshold
is renamed a physical cutoff. Earlier scattering/trace-energy/timing
warnings and nonmonotonic case findings remain unchanged.

In particular the fully read G3N2 transverse-multimode entry report of
9 October (SHAe0f066347d13bbd00566cf8f9af5857e424e4c8ce1102f1eebd457b419c9da19)
already finds a nonzero Frobenius three-form for the allowed transverse
waves and a RAW psi/Z velocity-block rank change at finite amplitude, with
an amplitude^-4 inverse contribution. That result is NOT the full constrained
physical Hessian or a physical ghost classification. The present cubic
response does not solve that finite-amplitude constraint/initial-data problem
or authorize a uniformly algebraic Z or U-orthogonal preferred-leaf extension.
This specific dependency must be handled before using the frozen linear
twenty-state response as a full nonlinear evolution/error theorem. Do not
repeat the completed raw-block/Frobenius calculation as if it were new.

The distinct transverse e^3 response is ALREADY in
RES001_R4C1_RETARDED_CUBIC_BACKREACTION_V2_REPORT_2026-10-13.md
(SHA782ee5d6a21bcabfeb2b99947c54e9c1b048cfcfd67e11bdcaa1f3ca34cfcd99).
Its full second-order coupled response and transverse third-order
coefficient/shift, plus point/clock infinite-tail bounds, are not every
third-order field. The next assessment must combine existing e^2,e|e|,
transverse e^3 and current |e|^3 information without repeating completed
calculations or assuming missing components close by symmetry.

## Verification and preservation

Nine cases37/37 each plus3 global checks:336/336; no failures or unknowns.
756 full-action probes on378 unchanged archived nodes;756 derivative
controls;756 stored lower comparisons;36 stored root-mode comparisons.
No new time integrations or observational targets.

| Control | Largest normalized residual | Frozen tolerance |
| --- | ---: | ---: |
| Complete affine identity | 8.081173804906076e-15 | 1e-9 |
| All22 reconstructed equations | 1.7628617687184562e-13 | 1e-9 |
| Generator | 1.3121711728194529e-14 | 1e-9 |
| Source | 3.1282922261795723e-16 | 1e-9 |
| Fourth-order directional derivative | 3.5395144701086334e-11 | 1e-7 |

All lower/root bound excesses are zero. The derivative tolerance is
separately frozen; action/constraint tolerances were not relaxed.
456 source pins and909 source/sidecar metadata records are preserved by the
original run and exact companion replay. All20 original evidence-file
hash/size/mtime records are unchanged. A separate post-replay check again
verified all nine case payloads/sidecars, source metadata and original files.
Three inherited absent sidecars are explicit, with source bytes hash-pinned.
Same-agent independent controls are not independent scientific peer review.

| Artifact | SHA-256 |
| --- | --- |
| Contract | 0535e0f45202e30c1ad9049f091d9a86bc88fbc2fdf2a5a7acf3e54315191b49 |
| Executable | 994f26566358ddaa01032f3608bddb8ce3f570fc23429d5a423c3289104c38a1 |
| Attempt01 summary | 35cd15dbedcb2ef6be3acfc41a1e43d9a1392100db1b05c7989c5a4f0e21bc90 |

The execution-only [replay addendum](RES001_R4C1_CUSP3_SOURCE_AWARE_WINDOW_V1_REPLAY_ADDENDUM_2026-10-17.md)
permits independent local processes to call the SAME frozen Case.run and
then use its ORIGINAL calculate/encode aggregation. Every case was freshly
recomputed; no interrupted serial progress was substituted for a result.
The original serial attempts did not finish and their traces are preserved.
Companion success is not recorded as completion of the original serial CLI.

Completed companion receipt: Analysis/MasterTests/outputs/
r4c1_cusp3_source_aware_replay_attempt_01/receipt.json,
SHA6668bb844df71a6502c6f4faaa061bd1f803542a1a2604bae5682dfb29105522.
It records all9 fresh cases, all10 original payloads exact,336/336,
source metadata909 and original evidence metadata20 preserved.
Runner SHA c66b7ac7b6dc1d1bd8d1825f516c4afe7f0aa5d8f00102d62aed8037c71175f0.
Addendum SHA 3b71d718fc27264953044fa61b6d8001bd0c0b0682223851375c6434ba61d2ab.

Reproduce into a NEW, nonexistent checkpoint directory (replace NEW with
a fresh identifier). Original scientific evidence is compared, not written:

```text
python -B Analysis/MasterTests/replay_01_r4c1_cusp3_source_aware_window_v1.py \
  --workers 2 \
  --output Analysis/MasterTests/outputs/r4c1_cusp3_source_aware_replay_attempt_NEW
```

Only an interrupted, unchanged checkpoint set may be resumed with --resume.
An existing completed receipt is protected against reuse/overwrite. Eight
private execution-guard tests cover sidecar, overwrite, path and source-pin
rejections; they are NOT additional scientific checks or peer review.

## Programme disposition

R9-MT1-CUSP3-SOURCE-AWARE-WINDOW-V1: provisional reuse is supported ONLY
for the stated fixed-case, prepared planar cubic estimate. No substantive
blocker remains within that bounded estimate. Review remains DEFERRED,
not cleared. Missing useful nonlinear error control, full finite-amplitude
constraints and physical energy/domain/GR evidence block stronger uses.
No physical family GO follows.
Inherit CUSP3-COUPLED-TAIL-V3/CONSTANTS-V1, LOW-RANK-WEIGHTED-EVOLUTION-V2,
lower odd response/root audit, CUSP3-EVOLUTION-V1, generic action/reduction
and all transitive deferred review debt.

Stage1 complete only in registered linear B1 dust scope; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED. Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 UNCHANGED. Matter-residue and nonlinear-force identifying inputs
remain missing: diagnostic action coefficients do not determine them.
No manuscript/PDF/site/vault, commit/push/publication/submission,
provider/model/runtime/security change is included.
