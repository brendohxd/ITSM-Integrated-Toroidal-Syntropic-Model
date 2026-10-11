# R4C1-G3K-C1: global preferred-clock entry audit

Date: 9 October 2026. Report v1. Conditional; PROCEED_PROVISIONALLY.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Decision and effect on the next route

The stated homogeneous nonzero fixed-sign tilted backgrounds do **not** admit
a globally single-valued REAL U-orthogonal clock on I x T3. The exact cycle
argument below establishes this for any continuous positive integrating
factor, not merely the sampled profiles. Local preferred-clock patches exist.

This rejects that global clock construction, not the R4C1 action, ITSM,
all tilted backgrounds, or every global time choice. In this metric the
coordinate t is already a global non-orthogonal geometric time:
g^{tt}=-1/N^2<0 and U(t)=gamma/N>0. Its admissibility for the coupled,
regulated physical evolution still requires a characteristic/constraint
analysis. Timelike relative to the metric does not settle that PDE question.

The healthy fixed-frame comparator has an exact orientation-preserving
paired-branch momentum-map band. That band is **not** the coupled physical
domain and **not** an action-derived EFT cutoff. Neither the geometric
obstruction nor comparator success classifies the parent complex roots.

Next owning scientific checkpoint: a separately frozen **G3K-C2 global
non-orthogonal-time / coupled-constraint-domain test**, starting in the actual
periodic dust-time chart. Retain the full regulator and pre-Schur constraints;
derive what is physically admissible rather than importing the comparator band.
Do not try a universal-cover boost as a global U-orthogonal cure. The aligned
nonanalytic multimode route remains an alternative under its own contract.

## Scope and frozen evidence

Owning [contract](RES001_R4C1_G3K_C1_CLOCK_ENTRY_CONTRACT_2026-10-09.md),
SHA-256 `00ad4d640181736a2e8049568df181b2d3a64f58de61f0aa836d989f708713b1`.
Parent [G3K report](RES001_R4C1_G3_FINITE_K_SCALAR_REPORT_2026-10-08.md),
SHA-256 `81c11fc9cc9efbb9ad6b2d6f0e2bd26653a13d2fb126031b4941ae326f782c31`.
The unchanged G3K/G3T candidate backgrounds and conditional G3 family are used.
No action, parameter, background, mode or acceptance threshold was changed.
No background or perturbation was reintegrated or fitted.

The original field key K is the assumed conditional K_Q. The family parameter
cutoff=2 is not an independently established physical EFT cutoff. Coordinate
L_x=1 is only a numerical witness convention; no physical torus size is selected.

## Exact geometry: local integrability is not global real time

For a_parallel,a_perp,N>0 and gamma=sqrt(1+w^2),

\[
g=\operatorname{diag}(-N^2,a_\parallel^2,a_\perp^2,a_\perp^2),\qquad
U=(\gamma/N,w/a_\parallel,0,0),\qquad U^2=-1,
\]

\[
\theta=U_\flat=-N\gamma\,dt+a_\parallel w\,dx.
\]

Homogeneity gives dtheta=(d(a_parallel*w)/dt) dt wedge dx and
theta wedge dtheta=0 exactly. Frobenius therefore supports local orthogonal
leaves. It does not prove a global real-valued preferred clock.

On a fixed-sign patch put s=sign(w), mu=s/(a_parallel*w)>0. A local potential is

\[
T_{\rm loc}=s\left[\int^t\frac{N\gamma}{a_\parallel w}\,dt'-x\right],\quad
dT_{\rm loc}=-\mu\theta,\quad
g^{-1}(dT_{\rm loc},dT_{\rm loc})=-\frac1{a_\parallel^2w^2},\quad
U(T_{\rm loc})=\mu>0.
\]

However T_loc(x+L_x)-T_loc(x)=-s L_x for arbitrary L_x>0. This real
potential exists on a patch or cover, but does not descend to the T3 quotient.
A circle-valued potential is not a real time function with ordered time values.

More generally, suppose a single-valued C1 REAL T satisfied dT=-mu theta,
with any continuous positive mu(t,x,y,z). Around the closed x-cycle at
fixed (t,y,z),

\[
0=\oint dT=-a_\parallel(t)w(t)\int_0^{L_x}\mu(t,x,y,z)\,dx.
\]

Continuity and strict positivity on this compact cycle imply
integral(mu dx)>=L_x min(mu)>0. With a_parallel>0 and w nonzero, the right
side is nonzero: a contradiction. Spatial dependence of mu cannot cancel it.
Negative tilt reverses the period sign, but not the contradiction. The aligned
w=0 control instead has the global real clock T=integral(N dt).

This is the analytic proof; numerical witnesses are supplemental. No theorem
about spatially varying/sign-changing frames or arbitrary global foliations
is asserted here. A coordinate boost on the universal cover leaves the quotient
identification to be enforced and cannot erase this cycle integral.

## Exact healthy-comparator map boundary

For C=c_psi^2>=0, d=b/K>0, v=w/gamma and real P,

\[
\Omega_\pm=\pm\sqrt{CP^2+dP^4},\qquad
\omega=\gamma\Omega+wP,\qquad p=\gamma P+w\Omega.
\]

For P>0,

\[
v_g=\frac{C+2dP^2}{\sqrt{C+dP^2}},\qquad
\frac{dp_\pm}{dP}=\gamma\pm wv_g.
\]

Both map slopes are positive precisely when |v|v_g<1; paired negative-P
branches give the same criterion. The one-sided origin limit is sqrt(C).
For C,d,P>0, v_g'=dP(3C+2dP^2)/(C+dP^2)^(3/2)>0.

Writing xi=dP^2 and u=v^2 C, the turning equation and positive solution are

\[
v^2(C+2\xi)^2-(C+\xi)=0,\qquad
\xi_+=\frac{1-4u+\sqrt{1+8u}}{8v^2},\qquad
P_{\rm turn}=\sqrt{\xi_+/d}.
\]

When 0<u<1 the polynomial is negative at zero and has positive leading
coefficient; its roots have opposite signs. Thus the admitted comparator
band is |P|<P_turn. Equality is excluded. Separate controls are retained:

- C=0: P_turn=1/(2|v|sqrt(d)) for d>0 and v nonzero.
- v=0 or d=0 with v^2 C<1: this comparator criterion supplies no finite bound.
- v^2 C=1: paired orientation is degenerate already at the origin.
- v^2 C>1: paired positive orientation fails already at the origin.

There is no division by the zero v or d controls. No numerical turn is
interpreted as a physical cutoff. The G3T stored turn belongs to C=0;
the G3K turn uses the nonzero-gradient C=6A sqrt(Y)/K, Y=(w psi_dot/N)^2.
They are different controls and must not be conflated.

## Executed checks and numerical evidence

The sealed v2 receipt reports **1032/1032 local checks**, zero failed and zero
unknown checks. An exact read-only replay reproduces all three JSON outputs
and their sidecars. Output hashes and last-write timestamps are unchanged
across replay. This is reproducibility, not independent scientific review.

All 24 initial states and 16 saved G3T jets at t=.0005,.001 were used. The
40 records are distinct **method-tagged jets**, at 32 eta/initial-tilt/time
coordinates: the DOP853/Radau pairs are not distinct physical backgrounds.
This disambiguates the contract's event count while retaining every registered
state record. Three common positive-mu profiles were integrated once each,
then evaluated on all 40 events, producing 120 weighted-period witnesses;
these are not 120 independent integrations or a proof for all mu.

| Quantity | Maximum normalized discrepancy/residual |
| --- | ---: |
| Geometric normalization/local-clock identities | 6.668e-16 |
| Closed turn against independently bracketed Brent / 50-digit bisection | 6.270e-16 |
| Turning polynomial residual | 4.180e-16 |
| Weighted periods: SciPy / 50-digit quadrature against Bessel integral | 1.111e-16 |
| Initial finite-C turn against G3K | 1.726e-16 |
| Separate initial C=0 turn against G3T | 1.678e-16 |

All satisfy the unchanged <=1e-10 contract. Every turn is bracketed from zero
with independent upper-bound doubling. Strict paired-branch probes at
P/P_turn=(0,.5,.9,.999,1.001,1.1,2) have their required inside/outside signs.
Conditional comparator P_turn ranges from 2.871563380634087 to
20.592474745243777 in the parent chart, not calibrated physical units.

The eta=1,w=.5 initial example has C=.05714285714285714 and
d=.15151515151515152. Its finite-C turn is 2.871563380634087; its C=0
turn is 2.8722813232690148. The small difference is retained, not rounded
away to force the two controls to coincide.

All 120 parent events, all 1,680 roots and their formal complex covectors are
copied without health selection. A separate value-by-value equality check
against the parent event list passes. Formal complex covectors remain formal,
not real particle-energy/momentum poles. The exact k=0 and w^2=1/5 zero
factors are retained without inversion; C1 does not solve continuation
through those pre-Schur constraint boundaries.

## Provenance, failure preservation and commands

The v2 run/replay verifies 84 source pins and 81 available source sidecars,
including all 75 inherited G3K direct/transitive source pins. Three inherited
documents have no sidecars; their actual bytes are still hash-pinned and checked:

- Theory/Gates/UVIR-003/UVIR-003_STAGE_B_FORCE_COMPLETION_OPTIONS.md
- Theory/Gates/UVIR-003/UVIR-003_STAGE_B_NONZERO_GRADIENT_FORCE_LOCAL.md
- Theory/Gates/UVIR-003/UVIR-003_STAGE_B_TRACK_A_FORCE_ADM_CUBIC.md

No sidecar was invented for those originals. A supplementary read-only check
of the parent G3K executable and sidecar matches its receipt's script SHA-256
`05f3c588d8424a9d7f65c69624b483394144da5ae242c75c54f238ef895e37de`.

The original G3 failed assertion eta1_independent_fd_balances remains false:
value 1.1005635230674148e-7, criterion <1e-7. Geometry/comparator success
does not repair that original GR/background-balance failure.

C1 v1 stopped on the duplicate label saved_time_1.0_0.25_25 before any
scientific output directory was written. Its source and sidecar are preserved.
V2 adds the solver method to the label, records v1 as a source pin, and changes
only version/output identifiers accordingly; equations, inputs, grids and
thresholds are unchanged. Ignored private failure log:
.local/itsm-context/output-97de8ece771e4a768c555b55e1f25ed0.txt,
SHA-256 `6040ec7373a3f214c943304096c32cf133a4f7ac0164430f995258ae1cfb2e19`.

Reproduce with the known working Python interpreter:

```text
python -B Scripts/itsm_context.py run -- python -B Analysis/MasterTests/test_01_r4c1_g3k_c1_clock_entry_v2.py --replay Analysis/MasterTests/outputs/r4c1_g3k_c1_attempt_02
```

Interpreter used: C:/Users/brend/anaconda3/envs/itsm_env/python.exe.
Normal execution refuses an existing destination. Replay performs no scientific
output writes. The optimizer's own private command logs are separate.

| Artifact | SHA-256 |
| --- | --- |
| v1 executable | c507867b48a425b1ad33aae80e8d8c2a5f19faf1f2a2e995264c65f7937de122 |
| v2 executable | d031e3347d00b956b9abebc4cded2bf199a993cf3348bc151303f17f90d79224 |
| attempt_02/formulas.json | c0b9bbf759deb1c96bbc6a4defac123ff5ed04dcd4ee5ce189f8d0d971173e43 |
| attempt_02/samples.json | 339373b084ba6b73c2eda87b58c215564afb86dab1ea55dbe3b68267e88c4cff |
| attempt_02/summary.json | 39818742f14afe951780c20425b206128b11bf8007e3b84efd5743979e3262e7 |

Outputs are under Analysis/MasterTests/outputs/r4c1_g3k_c1_attempt_02.
Successful run log SHA-256 d315e7d1ae0862c2ca72488b17f3e20c310076cee5580cdf401ffac3ed273ee3;
read-only replay log SHA-256 b8a0bd4182e67beb7b0a4f7b287ab3f61c070bc228abefdda57c1552bde098ca.

## Remaining substantive and review obligations

The coupled characteristic/Cauchy and energy-residue classification, physical
mode interpretation, pre-Schur boundary continuation, other directions and
vector/tensor sectors, full background/constraint completion, scattering,
action-derived physical EFT overlap and healthy continuous GR limit remain
open. C1 supplies none of these by comparison or check count. The G3V
zero-gradient ordinary-cubic-vertex obstruction and G3N1 limited classical
probe remain unchanged. A clock obstruction is not a physical ghost theorem.

Inherit R9-MT1-G3K and its full direct/transitive scientific and review debt,
including G3T/G3V/G3I/G3DF/G3D/G3F/G3A/G3E/G3Z/G3S/G3,
G2/G1/B1/S1/S2/S3/variation, applicable PD1 and Track-A. Retain the separate
G3V cross-check and G3N1 records. Rule-9-only review remains DEFERRED and does
not block supported provisional research. Missing physics still blocks
dependent use; canonical promotion/publication is not authorized.

Canonical Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
The full native goal is still active and incomplete. No manuscript/PDF edit,
vault mutation, provider dispatch, action change, commit, push, upload,
promotion or publication was performed.
