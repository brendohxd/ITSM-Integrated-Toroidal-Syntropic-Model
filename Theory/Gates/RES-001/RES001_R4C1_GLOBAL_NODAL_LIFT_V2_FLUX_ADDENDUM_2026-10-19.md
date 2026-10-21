# V2 periodic-flux evaluation addendum

19 October 2026. Original V1 contract, action, inputs, rates and tolerances unchanged.

V1/attempt01 passes1018/1018 but its largest normalized initial-rate residual
is7.67403882709913e-9 against1e-8. Inspection locates the transverse V^z rate,
which should vanish on this initial slice. On the same worst G3 eta1/1024,
n33/node0 control, the direct flux form gives raw rate7.674038885990003e-9;
the periodic integration-by-parts form gives2.71373891146864e-17 with the
same inputs and complex step. Preserve V1 and all its receipts, not a failure
or a physical rejection. The new version addresses its narrow numeric margin.

The previously derived continuum identity is

    Hpsi=<(E+partial_z F)/s>=<E/s-F*partial_z(1/s)>.

V2 evaluates the scalar functional with the right-hand form, retaining the
left-hand form as Hdirect for a1e-8 comparison at every grid/node/case.
Keep the pointwise local lapse reconstruction p_psi=-(E+partial_z F)/s
UNCHANGED. Do not omit the physical flux: its scalar-rate derivative remains
essential even when the unweighted periodic divergence has zero mean.

Only restore_undivided (scalar evaluation/extra Hdirect return), grid_case
(equivalence check/record), and source pins change. Verify every other
function and class AST identical to V1. Preserve all original targets,
directions, clocks, means, charges, precision scales, shifts and tolerances.
Freeze V2 and sidecar before execution; fresh attempt02, full fresh read-only
replay, external before/after guards. No overwrite of V1 source/hash/receipt.

This is an arithmetic evaluation improvement, not completed momentum
evolution, nodal hierarchy, continuum admission, physical spectrum/window,
healthy GR or matching. All parent/review/publication holds remain.
