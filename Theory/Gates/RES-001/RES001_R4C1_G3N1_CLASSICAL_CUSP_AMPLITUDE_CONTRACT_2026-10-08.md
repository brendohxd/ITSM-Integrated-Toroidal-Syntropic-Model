# R4C1-G3N1: frozen classical cusp-amplitude diagnostic

Date: 8 October 2026. Owning programme: Test 1 conditional R4C1 viability.
Claim Conditional; research PROCEED_PROVISIONALLY; review DEFERRED.
physics_pass=false; Rule9_cleared=false; gate_effect=NONE.

## One question and scope

Does the known leading transverse force cusp admit a well-defined classical
amplitude Hamiltonian and unique evolution in an explicitly declared
frozen-coefficient, one-mode Galerkin probe, despite lacking an ordinary
third Taylor derivative? Is that one mode an invariant nonlinear subspace?

This is a prerequisite diagnostic, not a solution of the complete action.
Use the unchanged G3V quadratic and leading force coefficients. Do not
smooth the absolute value, change A or b, refit backgrounds, or assert that
uncomputed quartic/auxiliary terms vanish. Retaining only the known terms
defines this probe, not a replacement for the full R4C1 action.

The full second-order scalar/zero-mode constraints, regulator quartic
Schur reduction, evolving-background response, physical EFT domain/cutoff,
finite-density scattering and healthy GR limit remain open. A positive
probe result cannot establish any of them or close Test 1.

## Frozen parents

- G3V cross-check report:
  Theory/Gates/RES-001/RES001_R4C1_G3_VERTEX_REGULARITY_CROSSCHECK_REPORT_2026-10-08.md,
  SHA-256 0b35ad651859271e9310b8aeec5a0957805efe35cd05fbece96b498969c22409.
- G3V cross-check receipt:
  Analysis/MasterTests/outputs/r4c1_g3v_crosscheck_attempt_01/summary.json,
  SHA-256 b752415f0d5741c80a47dca5c699f7dc2ca54d31fc43ba04ded4c335939bf492.
- G3V coefficient grid:
  Analysis/MasterTests/outputs/r4c1_g3v_crosscheck_attempt_01/grid.json,
  SHA-256 bbb332d89a5a63af119c6f7c34580516ca450e19dc46c67a4d0a31c61d3a859b.
- G3V cross-check source:
  Analysis/MasterTests/test_01_r4c1_g3_coupled_vertex_regularity_crosscheck.py,
  SHA-256 4898f85f20e30bb0ba3c61492d97657bde0163b3bf74a67c60ba38d9cf027f19.
- Original G3V versioned report:
  Theory/Gates/RES-001/RES001_R4C1_G3_COUPLED_VERTEX_REGULARITY_REPORT_2026-10-08_v1.md,
  SHA-256 952b4315a5607358a4fc0250a9ab67efc90577dda77f006b357fc1cbd74eeb27.
- R4C1 action freeze:
  Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md,
  SHA-256 81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3.

All direct/transitive pins must match before execution. Preserve original
sources, hashes, receipts and failed assertions. The child uses a distinct
versioned executable and a new attempt directory. Replay is read-only.

## Spatial normalization, not a quantum Fourier normalization

The parent defines the local comoving canonical field X=a^(3/2) f w
and an averaged cusp coefficient C_X for X_amplitude cos(kz).
Use the spatial-average action density, not an integrated unitless volume.
Derive the cosine normalization explicitly: write X(t,z)=sqrt(2) q(t) cos(kz)
so that the averaged quadratic kinetic term is dot(q)^2/2.
The corresponding leading cusp coefficient is D=(sqrt(2))^3 C_X.
An integrated volume-normalized mode would introduce the appropriate volume
factor separately; this diagnostic does not construct quantum vertices.

For each frozen chart the selected averaged-density probe is

L = dot(q)^2/2 - omega^2 q^2/2 - D |q|^3,
omega^2 = parent canonical_frequency_squared.

Derive the Euler-Lagrange force, momentum, Hamiltonian, force regularity,
local Lipschitz bound and energy argument without an ordinary cubic Taylor
vertex. For time-dependent coefficients record the explicit energy-source
terms instead of claiming conservation. Only frozen coefficients are evolved.

Check whether the force on cos(kz) contains a cos(3kz) component by exact
quadrant integration. A nonzero component MUST reject a claim that the
single-mode subspace is invariant. Report the ratio to the fundamental;
do not treat a Galerkin projection as the full nonlinear field evolution.

## Registered algebraic and dimensional checks

1. Exact cosine quadratic and absolute-cubic averages; canonical q residue.
2. Signed force on q>0 and q<0, its derivative at zero, and its local
   Lipschitz bound. Preserve the absence of a common higher derivative.
3. Regular Legendre map for this probe only; exact Hamilton equations.
4. Conserved frozen energy and the explicit time-dependent energy balance.
5. Positive frozen omega^2 and D imply a coercive probe potential and bounded
   phase trajectory; use this with local uniqueness, not as a full PDE theorem.
6. Exact third-harmonic forcing and the one-mode-invariance rejection.
7. Mass dimensions: a and w dimension 0; f and q dimension 1;
   dot(q) dimension 2; omega^2 dimension 2; C_X and D dimension 1;
   averaged L and H dimension 4; every amplitude-EOM term dimension 3.
8. Reject omitted cusp, sign-insensitive q^2 force, incorrect cosine
   normalization, false one-mode closure, and unqualified energy conservation
   on a changing background. A=0 is a harmonic control, not a GR limit.
9. No inference that the full velocity-dependent regulator/constraint sector
   shares this probe's regular Legendre map.

## Frozen sampling and numerical decisions

Inspect all 216 pinned parent events, without resampling or reintegration:
six eta values (1, 1/4, 1/16, 1/64, 1/256, 1/1024);
two archived methods; t=(0,0.5,1,2,3,4); k=(20,40,80).
Require finite positive kinetic_weight, gradient_weight, canonical_frequency_squared
and comoving_cusp_coefficient on this finite grid; no continuous-domain claim.

Numerical physical-chart probes use the 12 archived DOP853 rows at t=(0,4),
k=20 across all six eta values. Set initial tilt amplitude |W|=0.01, solely
as a probe choice, not a certified EFT amplitude:
q_star=a^(3/2) sqrt(kinetic_weight) |W|/sqrt(2).

Use y=q/q_star, tau=omega t and
gamma=3 D q_star/omega^2. Integrate the signed initial states (y,y')=(+/-1,0)
over tau in [0,8 pi]. Add explicitly synthetic gamma=(0,1/8,1) controls;
they are not retuned on-shell ITSM backgrounds or predictions.

Both DOP853 and Radau use rtol=1e-11, atol=1e-13, max_step=pi/32
and 401 common evaluation times. Require successful integration, normalized
energy drift <=2e-8, paired-method state disagreement <=2e-8, and parity
agreement <=2e-8. Compare the first zero crossing against a 50-digit mpmath
energy-quadrature quarter period, with normalized error <=2e-8.
The endpoint-substituted quadrature must be independently derived and used
without fitting an integration result.

For synthetic gamma=1 only, repeat each method with rtol=1e-8, atol=1e-10.
Require the fine state to remain within 2e-8 of the other fine method and
coarse-to-fine disagreement <=2e-6; report measured differences, without
requiring monotone improvement below numerical floors.
Effects smaller than the declared numerical tolerances are not resolved
physical nonlinear detections. The 50-digit quadrature does not upgrade
the precision of the archived background coefficients.

## Outcome and parent holds

Success means PASS_BOUNDED_CLASSICAL_GALERKIN_PROBE, with
single_mode_invariant=false if the harmonic test detects leakage.
It is not a Test-1 pass, full nonlinear Cauchy theorem, action acceptance,
stability or quantum-consistency proof. A failed registered assertion remains
a failure; no post-run threshold changes or relabeling are authorized.

Record R9-MT1-G3N1 as DEFERRED, inheriting G3V and all its parent scientific
and review dependencies. Canonical Tests 1-3 HOLD_SUBSTANTIVE;
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; TOP-X4 unchanged. No publication, commit/push, provider
dispatch, model change or vault mutation is authorized by this contract.

