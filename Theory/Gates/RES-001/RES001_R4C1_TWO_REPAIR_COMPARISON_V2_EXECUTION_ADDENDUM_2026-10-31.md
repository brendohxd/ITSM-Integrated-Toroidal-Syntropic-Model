# Two-repair comparison V2: exact background input types

31 October 2026. V1 returned 54/70. Both no-Float guards failed; exact
identities contained 1e-16-scale residuals, and the physical Hessian controls
stalled near 1.28e-17 instead of meeting the frozen 1e-35 tolerance.

The new backend's background arrays contained ordinary Python integers.
Division inside the original geometry routines therefore introduced machine
floats before symbolic differentiation. The physical numeric controls also
received integer-valued geometry entries rather than uniform multiprecision
values. This is a precision implementation defect, not a reason to accept
the failed comparisons or change the thresholds.

V2 converts ordinary integer constants to exact SymPy integers in symbolic
mode and multiprecision values in physical mode before density evaluation.
It then rebuilds the matrices from the source action. It does not rationalize
or round the already-computed approximate matrices into a desired result.

V1 backend, executable, receipt and their hashes remain immutable. The V1
scientific contract and candidate definitions still apply. No action,
coefficient, probe, tilt domain or tolerance is changed. Review DEFERRED;
physics_pass=false; gate_effect=NONE.
