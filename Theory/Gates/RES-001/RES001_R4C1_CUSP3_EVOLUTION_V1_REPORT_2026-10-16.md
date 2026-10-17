# R4C1: finite-mode evolution at the first omitted cusp order

16 October 2026. Master Test 1 / RES-001 / unchanged-action Stage 2.
Claim Conditional. Primary local controls421/421; separate source/current
audit430/430. Review DEFERRED; Rule9_cleared=false; physics_pass=false;
gate_effect=NONE. Native goal remains paused; this is approved bounded work.

## Result and interpretation

The completed INITIAL |e|^3 preparation has now been evolved for the spatial
mean and first even harmonic, rather than checked only at t=0. All three
registered families, three eta values and both numerical methods passed the
registered diagnostics. No charge reset or slow-graph projection was applied
to the integrated response coordinates.

The retained responses remain compatible with the action-derived sourced
equations, auxiliary constraints and conserved mean charges at the registered
sample times, including a freshly located zero of the leading wave. This is
positive evidence for perturbative finite-mode consistency over the tested
interval. It is NOT full-field nonlinear admission, a continuous-time error
certificate, energy positivity, a physical cutoff or a healthy GR limit.

The source/current audit is a second local program, not an independent human
or model review board. Its count includes provenance controls. Neither count
is a physical gate clearance or a statistical confidence level.

## Frozen scope and equations

Contract: `RES001_R4C1_CUSP3_EVOLUTION_V1_CONTRACT_2026-10-16.md` in this folder.
Initial authority: `RES001_R4C1_CUSP3_LOCAL_INITIAL_JET_V2_REPORT_2026-10-16.md`.
Generic action, coefficient maps and diagnostic initial recipe are unchanged.
No coefficients were identified by microscopic matching or target fitting.

- Families: archived_G3, new_B1_frame, new_hierarchical.
- eta=1/4,1/64,1/1024; no eta=0 endpoint inverse.
- Registered coordinate k=40; output harmonic labels0,2, momenta0,80.
- Coordinate time0<=t<=0.05 in the registered action units, not a claim of
  0.05 physical seconds. Each run has21 equally spaced nodes plus its leading
  wave zero. There are18 genuinely fresh integrations, not18 initial probes.
- Lower odd e|e| Fourier coefficients1,3 are evolved, alongside all13 mean
  and10 nonzero physical coordinates and their velocities at order |e|^3.
  The implemented real state has96 entries.
- Background and first wave are freshly integrated with dense output, not
  interpolated from the old archive. The old nodes remain immutable controls.

For these outputs, odd1,3 are complete source inputs at this perturbative
order: the first wave has Fourier support+/-1 and the mixed quadratic source
at n samples only n-1,n+1. This is exact mode selection for outputs0,2, NOT
closure of the entire spatial field or truncation control for other outputs.

Write EW=-f2*(W_tt+3H*W_t+mass*W-cV2*W_zz/a^2),
f2=MU2*(c1+c4). The lower cusp equation retains its force proportional to
-3*A*abs(psi_dot)^3*w*abs(w). Its zero initial displacement/velocity does not
remove its acceleration. The generic WWR sources are polarized before family
substitution, with the evolving basis, accelerations and auxiliary-source
time derivatives retained. The direct degree3 nonanalytic source is added
with exact coefficients of abs(cos(kz))^3. abs(w) is retained across the time
zero; no division by w or replacement by analytic w^3 is used.

Generic temporal and longitudinal source Ward identities were checked
exactly off shell. The combined sourced identities were checked numerically
at all registered nodes and roots. An independent32-point periodic DFT tests
the mixed-source convolution; it does not establish a full-field tail bound.

Algebraic reconstruction solves the action constraints, not fixed target
charges. Density drift is also obtained independently by differentiating
the primary lapse constraint, then compared with the density derivative from
the dust-clock Euler equation. This avoids using that Euler-assigned derivative
as its own conservation test.

For J=u*v_dot-v*u_dot, the mean angular-current correction includes

```text
Q3 = a^3*[u*delta(v_dot)+delta(u)*v_dot
          -v*delta(u_dot)-delta(v)*u_dot
          +(trace(delta M)/2-delta alpha)*J]
     -2*a^3*zeta*(u^2+v^2)*J*w*r1.
```

r1 is a complex Fourier coefficient, real for this preparation, NOT a cosine
amplitude. The last term is required. The separate audit binds the linear
row and this polarized offset to the earlier canonical angular-current export.
It also binds the evolving direct force to the original G3N4 nonanalytic
Euler export for positive and negative wave values.

## Measured numerical controls

Worst values over all registered cases/nodes/roots, with the contract's
normalizations (charge coefficients scaled by eta^(7/2)):

| Diagnostic | Maximum | Frozen acceptance |
| --- | ---: | ---: |
| Full22 sourced Euler residual | 1.0855435307097443e-15 | 1e-9 |
| Combined source Ward residual | 3.7950868870240143e-14 | 1e-9 |
| Independent lapse-density drift mismatch | 8.008621487539484e-15 | 1e-8 |
| Mean charge value/drift from initial zero | 4.144537262619789e-12 | 1e-7 |
| Mean charge time derivative | 1.6534083130403943e-17 | 1e-7 |
| Scaled DOP853/Radau state difference, all21 nodes | 3.102854253031432e-9 | 1e-7 |

Both solvers use rtol1e-10, atol1e-12 and max_step0.001. No tolerance was
relaxed after looking at results. Comparisons use the scaled96-component
state, not agreement of tiny unscaled coefficients. They do not certify the
true solution error between sample points.

In particular, accelerations and algebraic variables are reconstructed from
the equations. Their small residuals test equation/reconstruction consistency;
they are NOT independent global ODE error estimates. The two-method
comparison and charge-value drift are separate controls.

The largest reduced kinetic condition number is1.1322316912500007e8. This is
basis-dependent conditioning information, not a physical cutoff or a proof of
strong coupling. Regular chart quantities passed at the sampled times;
sampling does not prove the absence of all singularities between them.

Explicit nonzero witnesses reject omitted mixed acceleration, omitted
auxiliary-source drift, omitted mixed angular current and analytic-cubic
replacement after the leading wave zero. Failed old attempts, higher initial
harmonic probes and previous nonmonotonic/retarded observations are unchanged.

## Reproducibility and preservation

Primary executable: `Analysis/MasterTests/test_01_r4c1_cusp3_evolution_v1.py`.
Audit: `Analysis/MasterTests/test_01_r4c1_cusp3_evolution_independent_audit_v1.py`.
Receipts under `Analysis/MasterTests/outputs/`:

- `r4c1_cusp3_evolution_canary_attempt_01/`:55/55, engineering only.
- `r4c1_cusp3_evolution_attempt_01/`:421/421, all18 runs and checkpoints.
- `r4c1_cusp3_evolution_independent_audit_attempt_01/`:430/430.

| Artifact | SHA-256 |
| --- | --- |
| Main executable | 78ae1f76b165d2a9039deac705b4896c5842785e86bba9458757821014e641d2 |
| Contract | c85f207a2cb81d9d7f942f09bc52eeae8e0b31397346ad3e839496bbc6df8498 |
| Primary summary | b9f8e6b17bf3cfaf01fac6ea1f400e645c36a21585c4d56c3b47f8c64c998fad |
| Trajectories | 0d8e0e9f324919bf6e2298b7169d869d34c12be93d17ff4ebfabb3195dde9268 |
| Formulas | 200e7f2f8d52158dcb0cdc94baa3e8a40449dad5e149ed55e3052f8a2f298ed4 |
| Primary verification | 20c6174e3382f8ab8ae1c72c5fb088cab36135c8208eb35c5783bfcc08ba6ae6 |
| Scope | ed2fe5f0e6997638ef7d63f7ac6d1ca247f065deaef2e022a5a1c80b0f739a5a |
| Audit executable | 834b49de835d4eb1d61ad69896fde9c8bee2ccae6a80de2aaa747eff83fa1552 |
| Audit verification | c2ab368b122e694d6c37b06df595c45d3ff147e5b54b611973ca6ca844c4485d |

366 source pins and729 source/sidecar hash-size-mtime records were preserved.
The three inherited absent sidecars remain explicitly absent/unverified.
No original evidence, old sidecar or earlier result was corrected in place.
Only the two living status indexes may receive a byte-preserving appended
checkpoint, with their original bytes/digests retained privately first.

Replay: both the independent audit and the full18-run calculation passed
exact read-only replay. The primary replay checked generated artifact bytes,
all18 case checkpoint bytes, sidecars and output hash-size-mtime preservation.

Reproduction, from repository root using the existing itsm_env interpreter:

```text
python -B Analysis/MasterTests/test_01_r4c1_cusp3_evolution_v1.py --replay Analysis/MasterTests/outputs/r4c1_cusp3_evolution_attempt_01
python -B Analysis/MasterTests/test_01_r4c1_cusp3_evolution_independent_audit_v1.py --replay Analysis/MasterTests/outputs/r4c1_cusp3_evolution_independent_audit_attempt_01
```

## Decision, inherited debt and next step

NONE_WITHIN_STATED_SAMPLED_RETAINED_MODE_SCOPE. Provisional reuse is limited
to that scope under R9-MT1-CUSP3-EVOLUTION-V1; no physical family receives GO.
Inherit CUSP3 initial-jet V2, initial-charge V4, homogeneous kinetic V3,
fixed-charge retarded V3, charge/domain V5, generic WWR/evolving reduction,
G3N4 force coverage and all transitive deferred review dependencies.

The next bounded physical question is the constrained finite-k energy and
quartic characteristics of the coupled modes, before inferring a physical
interaction window. Separately, all-order preparation/remainder, full-field
mode control and certified continuous evolution remain open. No need to
repeat these completed initial/finite-mode diagnostics as a review-only hold.

Stage1 complete only in registered linear B1 scope. Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 UNCHANGED. Genuine matter-residue/nonlinear-force matching, healthy
GR/local gravity and physical stability/domain evidence remain substantive.
No publication, manuscript/PDF, website, vault mutation, runtime/security
change, provider dispatch, commit or push was included.
