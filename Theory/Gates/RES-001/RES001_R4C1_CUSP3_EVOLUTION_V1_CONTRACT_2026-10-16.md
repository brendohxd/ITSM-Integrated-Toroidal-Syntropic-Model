# R4C1: first omitted cusp-order evolution diagnostic, V1 contract

16 October 2026. Master Test 1 / RES-001 / unchanged-action Stage 2.
Conditional research; Rule-9 review DEFERRED, physics_pass=false,
gate_effect=NONE. Native goal remains paused; this is the separately approved
bounded continuation. No publication, commit, push, dispatch or action change.

## Frozen question and scope

Do the completed initial |e|^3 constraints propagate, without charge resets or
slow-graph projection, for the spatial mean and first even harmonic?
Start from CUSP3-LOCAL-INITIAL-JET V2 and its immutable inputs, not new fitted
initial conditions. All three registered families and eta=1/4,1/64,1/1024;
fresh DOP853 and Radau integrations on t in [0,0.05], 21 equally spaced nodes
and a freshly located zero of the leading wave. k=40; coordinate output
momenta 0 and 80. No extrapolation to eta=0.

Evolve the lower e|e| odd Fourier coefficients n=1,3 and all physical
mean/nonzero response coordinates at order |e|^3, using the generic exported
action and evolving constraint elimination. Auxiliary reconstruction is not a
charge reset. For these two output harmonics ONLY, n=1,3 are complete inputs:
the leading wave has support +/-1, and the quadratic mixed source samples
n_out-(+/-1). Other even outputs and their norms are NOT being evolved or
certified. Preserve the infinite source spectrum in the parent result.

## Calculation

Use generic pre-shift WWR Euler sources; eliminate the transverse shift with
its generic sigma, then polarize each quadratic wave-jet monomial between
the leading wave and lower cusp response. Differentiate auxiliary sources
with evolving backgrounds and wave accelerations retained. Add the direct
nonanalytic force at degree |e|^3, with exact Fourier coefficients of
|cos(kz)|^3. Retain |w| at the time zero; never replace it by analytic w^3.

The lower response obeys its sourced transverse wave equation. It enters
the mixed sources, source Ward identities and mean angular current. The
|e|^3 angular charge includes -2*a^3*zeta*(u^2+v^2)*J*w*r_1,
J=u*v_dot-v*u_dot, with r_1 the complex Fourier coefficient (real here).
Do not confuse it with a cosine amplitude. Dust charge includes the
reconstructed local density and lapse/metric/clock terms. Independently
differentiate the primary lapse constraint to obtain density drift; compare
with the density derivative obtained from the clock Euler equation.

## Frozen controls and numerical criteria

- Bind polynomial sources exactly; prove generic source Ward identities and
  retained-mode selection, including the nonzero lower cusp acceleration.
- At initial time compare source, source drift and mean preparation with
  the accepted parent initial jets (mean and first even output).
- Independent periodic quadrature checks the mixed-source convolution.
- Fresh leading-wave nodes agree with immutable parent to normalized 1e-7;
  lower odd response agrees to 1e-7 in eta^(7/2)-scaled coordinates.
- Integrators: rtol=1e-10, atol=1e-12, max_step=0.001, dense output.
  Scaled full retained response comparison <=1e-7 with denominator
  1+|state_A|+|state_B|, not unscaled tiny-coefficient agreement.
- At all registered nodes and the wave zero: full22 normalized Euler
  residual <=1e-9; source temporal/longitudinal Ward residual <=1e-9;
  independently differentiated lapse drift <=1e-8; mean charge drift and
  time derivative <=1e-7 in eta^(7/2)-scaled coefficients, using denominator
  max(1, background coefficient scales). These are numerical diagnostics,
  not interval-certified continuous-time error bounds.
- Reject omitted mixed source, omitted auxiliary drift, omitted mixed angular
  current, and analytic-cubic force replacement by explicit nonzero witnesses.
- Check regular background/chart quantities at all sampled times. Report
  condition numbers as basis-dependent diagnostics, not physical cutoffs.
- Preserve input bytes, digests, sidecars, sizes and modification times;
  three inherited absent sidecars remain explicitly unverified.
- Fresh exclusive output directories; deterministic read-only replay.
  A canary of archived_G3, eta=1/4, DOP853 is an engineering run only;
  scientific acceptance requires all18 integrations and method comparisons.
  Interrupted/failed runs remain evidence, never silently rewritten.

## Non-conclusions and stop rule

No all-order nonlinear constraint solution, full infinite-mode remainder,
energy positivity, ghost/gradient clearance, physical frequency window,
scattering cutoff, healthy GR limit, microscopic matching or observational
prediction follows. Stage2 incomplete, Stage3 not entered; MAT-001 blocked,
K_Q not derived, V not computed, Stage4A closed, TOP-X4 unchanged.
If any prerequisite fails, preserve it and report the precise obstruction.
Do not relax these criteria after looking at results or choose a favorable
family to claim closure. Rule-9 debt remains inherited and deferred.
