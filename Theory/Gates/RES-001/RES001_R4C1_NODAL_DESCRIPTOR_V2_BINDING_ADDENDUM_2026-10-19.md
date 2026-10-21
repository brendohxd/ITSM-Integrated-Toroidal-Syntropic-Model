# V2 original-helper binding addendum

19 October 2026. Original V1 contract, equations, domains and tolerances unchanged.

V1/attempt01 returned65/74 and remains FAILED. All9 cases raised
NameError: tensor_h is not defined on reaching the extracted partial block.
The independent point checks before that call are not a completed numerical
validation. Preserve V1 source/sidecar and all6 attempt01 files unchanged.

V2 adds module aliases tensor_h=canonical.tensor_h and HM=canonical.HM from
the already pinned original canonical module. These are the two external
geometry/component names required by that block. There is no substitute
implementation or numerical formula change. Compare ASTs before execution:
EVERY function must be identical between V1 and V2. Only the bindings and
additional source/failure/addendum pins change.

Freeze V2 and its sidecar before execution. Fresh attempt02; complete fresh
read-only replay and external metadata guard. Retain the failure and the
physical holds. No epsilon inverse, node removal, state/action change,
ordinary cubic cusp derivative or new physical claim is authorized.
