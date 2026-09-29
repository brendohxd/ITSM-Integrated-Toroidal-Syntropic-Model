# R4C1-S4B: one-extra-dust-derivative graph estimate disposition

Date: 2026-09-26. Master Test 1; conditional R4C1-v1/B1.
Validation: 169/169 implementation, provenance and analytic checks, twice with
byte-identical final JSON artifacts in the recorded `itsm_env` interpreter.
Review `DEFERRED`; `Rule9_cleared=false`; `physics_pass=false`; `gate_effect=NONE`.
Owning [preregistered contract](RES001_R4C1_MIXED_REGULARITY_CONTRACT_2026-09-26.md).

## Decision and scope

Append exactly the preregistered row `p v_d = p^2 delta tau/C` to S4A's complete
15-by-12 scalar graph, with `p=k/a` and fixed comoving `k=2*pi*n`. This creates
the 16-by-12 map `F_1`, and the new graph norm `||F_1 Z||^2` controls one extra
spatial derivative of the dust tilt. It is a stronger Sobolev domain, **not**
a uniformly equivalent renorming of S4A. The R4C1 action, B1 background,
S2 generator, coefficients, row weight and test thresholds were unchanged.

The fixed `F_1` metric is positive for each regular finite mode, but it cannot
yield a wave-number-independent instantaneous differential energy bound. An
exact initial-data sequence at the physical B1 initial coefficients has
logarithmic norm rate `r_1(p)` with

\[
   \lim_{p\to\infty}\frac{r_1(p)}{p}=\frac{\sqrt{6}}{2}>0.
\]

The limit is along allowed nonzero torus modes at `a=1`. Hence the largest
instantaneous logarithmic norm rate `mu_1(t=0,p)` is at least `r_1(p)` and is
unbounded in the formal high-`p` limit. This rejects the proposed *fixed*
one-extra-derivative graph differential estimate. It does **not** establish
unbounded finite-time evolution, ill-posedness in every space, an all-sector
instability, or validity of arbitrarily high modes beyond an EFT cutoff.

## Exact witness and derivative bookkeeping

Use `Z=(x,xdot)` and the pinned S2 reconstruction
`q=R x`, `qdot=Rdot x+R xdot`. The complete generator is
`A=[[0,I],[-W,-G]]`, with `W=Vc+Mcdot`. Define
`L_1=F_1dot+F_1 A`, `S_1=F_1^T F_1` and
`E_1=L_1^T F_1+F_1^T L_1`. The script checks `pdot=-H p`, the new row's
full derivative, and the twelve-component identity
`d||F_1 Z||^2/dt=Z^T E_1 Z`. Omitting `pdot`, `Fdot`, `Mcdot` or the new row
triggers registered rejection controls.

At `t=0`, B1 has `a=C=u=v_dot=r=1`, `u_dot=v=0`, `r_dot=1/4`,
`psi_dot=rho_m=1/5`, and the positive Friedmann value of `H`. Keep `H`
symbolic. In the original `q,qdot` chart choose `delta tau=1/p^2`,
`delta w_dot=sqrt(6)` and set `delta tau_dot` using the exact density row so
that `D=0`; all other independent original-chart entries vanish. Its density
velocity coefficient is

\[
   \frac{79200H^2+200p^2+1419}{240}>0
\]

for the declared `H>0`, `p>0` domain. The full graph then has exactly three
nonzero entries: row 11 is `1` (frame kinetic), row 14 is `1/p` (dust tilt),
and row 15 is `1` (added dust derivative). Thus
`||F_1 Z||^2=2+1/p^2`. In the exact expression
`r_1=(F_1 Z)^T L_1 Z/||F_1 Z||^2`, rows 11 and 14 each have zero
`r_1/p` limit, while row 15 has limit `sqrt(6)/2`. The total limit is
independent of the B1 value of `H`. The script verifies the full constrained
graph support and each limit symbolically, not by fitting large-`p` samples.

This witness was added **after** the initial successful 159-check numerical
scan exposed the high-frequency trend. That initial source and its three
receipts were preserved in the ignored `.local/itsm-context/s4b-initial-159`
snapshot. The preregistered norm, domain, action, parameters, grid and
tolerances were not changed; the ten extra checks strengthen the same result.

## Numerical diagnostics, not a closure theorem

All 54 sampled new metrics are positive. The largest sampled `mu_1` is
`1981.9927668144026` at `p=1608.4954`, `t=2`; the six `mu_1` values at
the largest `p` range from about `1972.74` to `1981.99`. The maximum raw
metric condition number is `6.399294414285555e16`. These finite samples are
consistent with, but are not needed to prove, the exact high-`p` obstruction.

The four saved S2 full-system endpoint transfers on `[0,4]` were reweighted
in the new initial/final graph metrics. No new perturbation integration is
claimed:

| Torus mode `n` | Graph amplification, DOP853 |
|---:|---:|
| 1 | 1.786211336430937 |
| 2 | 2.331833638480276 |
| 4 | 2.9703986669492077 |
| 8 | 3.343334812988193 |

The second saved solver agrees within the inherited threshold. Independent
60-decimal norm calculations differ by at most `3.271050690630045e-56`;
the centered full-energy derivative discrepancy is
`5.834784720679707e-10`. These are arithmetic checks, not 60-decimal
accuracy of the inherited double-precision B1 dynamics or a physical test.
Finite endpoint gains do not prove a uniform transfer estimate.

## Reproduction, review dependency and next bounded question

Run:

    python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_mixed_regularity.py

The [final summary receipt](../../../Analysis/MasterTests/outputs/test_01_r4c1_mixed_regularity_summary.json)
has SHA-256 `e98be1809f48d6aaf2316dc3109473cd2b5b4c4a362d173f0f633be5c9498a73`.
It pins executable SHA-256
`ee9bd6fe894e8595a52d97f02bebc3827c6a70dee473e4cff41dfa6cfb2c7552`,
inputs and the final matrix/sample artifacts. The saved prior S4A and S2
receipts are not rewritten.

R9-MT1-S4B inherits R9-MT1-S4A/S3/S2/S1/B1/VARIATION. Independent review
remains deferred; bounded negative-result/reconstruction reuse may proceed.
For the next separately declared estimate, isolate the coupled frame-kinetic/
dust-tilt principal block and test an explicitly constructed cross-term
symmetrizer or a direct finite-time fundamental-matrix bound. Any new norm
needs a declared domain and uniform-equivalence proof if that property is
claimed. Do not infer a successful symmetrizer from this report.

The full constrained IVP, homogeneous and singular branches, other spin
sectors, causality, physical cutoff, healthy GR recovery and matching remain
open. Master Test 1 and MAT-001 are not passed; UVIR-003 remains in progress;
`K_Q=NOT_DERIVED`, `V=NOT_COMPUTED`, and Stage 4A remains closed. No
canonical promotion or publication readiness follows.
