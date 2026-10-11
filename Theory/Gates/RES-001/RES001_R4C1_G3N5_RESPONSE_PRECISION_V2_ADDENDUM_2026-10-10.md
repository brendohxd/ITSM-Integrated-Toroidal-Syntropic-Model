# G3N5 response v2: high-precision independent finite-difference witness

Date: 10 October 2026. Version 2; frozen before execution.
Conditional; physics_pass=false; gate_effect=NONE; review DEFERRED.

The immutable response-v1 summary
b13e97122e724e58465db28df036ee835fd305b31078146cb7a283da38ee9d95
reports 120/125: five refinement failures, not failed analytic gauge,
constraint, operator, trajectory-completion or solver-agreement checks.
Its finest finite-difference errors are 2.09e-9 to 1.16e-8, below 1e-5,
but coarse/fine ratios below one fail the unchanged refinement criterion.
This pattern suggests numerical precision/interpolation limitations; a
higher-precision calculation must test that explanation rather than assert it.

Keep the v1 executable, contract, every receipt, sidecar and failure untouched.
Pin v1 and reuse its exact Operator/chart implementation without edits.
No equations, parameters, initial data, gauge, mode, time interval, normalization,
original acceptance threshold or recorded kinetic sign is changed.

Create a new v2 driver and a separate output directory. For the independent
finite-difference witness, use 70-digit arithmetic and a degree-40 autonomous
Taylor-series recurrence for the same background and reduced linear IVP.
Use coefficient convolution and exact integer-power reciprocal recurrences;
do not finite-difference a binary64 sampled curve. Keep the original DOP853
and Radau runs as immutable independent numerical controls, not rewritten runs.

Required new checks:

1. Synthetic reciprocal and exponential-IVP series controls <=1e-60.
2. Verify exactly that each registered reduced acceleration block is
   background-independent before using a constant high-precision inverse.
3. Degree-40 versus its degree-32 prefix on the registered interval:
   normalized difference <=1e-20. This is a convergence witness, not a
   global analytic-radius or rigorous remainder theorem.
4. High-precision unreduced 22-field trajectories agree with retained v1
   trajectories <=1e-7, using the original amplitude/magnitude normalization.
5. True polynomial derivatives, not the supplied RHS alone, give normalized
   reduced and full Euler residuals <=1e-20. Check a,C,rho_m>0 and Friedmann
   <=1e-20, and the unchanged mean linear-charge drift criterion.
6. Recompute the original independent five-point first/second differences
   on precisely 65/129/257 samples with two excluded boundary points.
   Finest full-Euler normalized residual <=1e-5; coarse/fine improvement >=4
   or both <=1e-10. No threshold is relaxed; all five v1 failures remain
   explicitly inherited in v2 diagnostics.

Retain 70-digit Taylor coefficients so the witness is reconstructible. Report
the mean and nonzero-mode kinetic signatures unchanged. A negative mean-chart
eigenvalue cannot be hidden or automatically called a physical ghost; neither
the positive nonzero blocks nor successful finite-time evolution prove physical
stability, a cutoff, hyperbolicity or a healthy continuous GR limit.
Exact replay must be read-only, source-pinned and byte-matching.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
No action replacement, old-source/receipt/frozen-sidecar rewrite, manuscript,
PDF, vault, provider, runtime configuration, commit, push or publication.
