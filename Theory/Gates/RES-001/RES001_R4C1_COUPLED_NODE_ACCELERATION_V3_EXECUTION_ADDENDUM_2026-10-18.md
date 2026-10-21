# Coupled node V3 execution repair: preserve the multicore result and crash

18 October 2026. Keep the V1 scientific contract and V2 multicore requirements.
V2's 16-process smoke test matched serial results. Its full run completed all
77 derivative jobs using all 16 workers, then terminated with Windows status
3221225477 (0xC0000005) after metric-row assembly. No scientific receipt was
returned. This is an execution failure, not a rejected physical equation.
Keep the frozen source, attempt02 directory, private progress and fatal trace.

The trace is incomplete and coincides with a periodic diagnostic stack dump;
the exact native-crash cause is UNKNOWN. Do not claim that the process pool,
SymPy or the diagnostic timer has been uniquely established as the cause.

V3 retains all worker/case machinery and the exact physical density, parameters,
domains, precision and independent controls. It makes two explicit, testable
execution changes:

1. Disable periodic asynchronous stack dumps. Keep ordinary stage progress and
   fatal-exception diagnostics. No Python/package/runtime installation or global
   setting is changed.
2. Replace generic inversion of the nodal 3x3 metric coefficient matrix by its
   exact diagonal-plus-rank-one inverse, ONLY after checking all nine matrix
   entries against the matrix obtained from the original varied density:

       M = a I + b 11^T,
       a = -(MP2-MU2*(c1+c3))/4, b=(MP2+MU2*c2)/4.

   Require a!=0 and a+3b!=0 on every registered case. Compute the same solution
   of M*h_ddot+force=0 and check every original metric equation. Eliminate the
   frame acceleration by its exact affine coefficient, checking its second
   derivative vanishes and the original frame equation residual is zero.
   Do not replace the metric response with a prescribed background acceleration.

These are algebraically equivalent solve operations, not new physical inputs.
An entry/residual check failure must remain a failure. No failed check, family,
domain, unknown physical disposition or prior run may be dropped or relabeled.
Freeze final bytes before a fresh attempt03 and verify immutable replay if the
calculation reaches delivery. Worker-count equivalence and full physical controls
remain required. The parallel stage is not a completed physics audit.

All inherited scientific/review holds remain: Stage2 INCOMPLETE; Stage3 NOT_ENTERED;
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.
No state adoption/evolution, action/provider/model change, vault mutation,
manuscript/site edit, publication/submission, commit or push is included.
