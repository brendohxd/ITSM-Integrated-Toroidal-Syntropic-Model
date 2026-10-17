# Exact omission control for small eta, V2

17 October 2026. The V1 contract and failed V1 receipt remain immutable.
V1 attempt01 stopped after the third archived_G3 case, eta=1/1024:
186/189 checks passed. The failed scientific-control requirement was
reject_omitted_extra_inverse, with an absolute binary64 witness
1.0519200528062109e-15 against >1e-12. The two remaining failures record
uncomputed case/probe totals. Do not relabel V1 as successful.

The exact full inverse, complete coefficientwise generator, and independent
full-action comparisons passed in that third case. No interval estimate was
attempted for it. The first two archived_G3 estimates were completed.

V2 preserves the original action, all matrix equations, the exact inverse,
full generator, box/row bounds, cases and normalized <=1e-9 acceptance
thresholds. It changes the extra-inverse omission prerequisite explicitly:

* Retain the original absolute >1e-12 binary64 visibility result in a separate
  diagnostic field, including FAIL where appropriate. It is not weakened or
  rewritten and is not a proof that a smaller term vanishes.
* Prove symbolically that the complete inverse minus the old cubic inverse
  is nonzero. Export every nonzero entry and its exact expression.
* At the exact unchanged on-shell initial event, independently invert the
  complete 20x20 matrix with 90-decimal-digit mpmath arithmetic, ell=4,80.
  Require a strictly nonzero difference from the rejected inverse and <=1e-50
  RELATIVE discrepancy between that difference and the exact symbolic
  correction. Also require the corrected full inverse product residual and
  its dense-inverse discrepancy to be <=1e-60. Record absolute magnitudes;
  do not infer any physical interaction scale from them.

These independent exact/precision controls replace a binary64 visibility
prerequisite for this particular term. They do not lower any action/generator
accuracy requirement or delete a small term. All other V1 controls and stopping
rules remain. The V2 executable inherits unchanged derivation and bound method
ASTs, and records every former numeric control and the reason for its role.

Fresh exclusive attempt02, with exact read-only replay. All twenty states,
all nine registered cases, every derivative/remainder, and all 756 action
probes remain required. If these controls fail, retain that result and stop.
No physical/canonical gate change or expansion beyond the approved parent.
