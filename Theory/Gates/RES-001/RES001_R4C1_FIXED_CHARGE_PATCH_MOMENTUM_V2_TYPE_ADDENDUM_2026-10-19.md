# V2 interval-input type addendum

19 October 2026. Original V1 contract and physics boundaries unchanged.

V1 / attempt_01 terminated before scientific receipts: maxupper passed an
exact Python integer from a constant matrix row to base.hi, which expects
an interval with _mpi_. The full traceback is retained in ignored private
output-6ec0e7e09b064480b96aa0f2b7eb7b88.txt (SHA-256
51f4db8814dbcdd445f863d18a2abadd44f65fe753aa5b1e62ffbe15a862ffb1).
V1 source, sidecar and empty attempt directory remain untouched. No failed
sign assertion is converted to a pass; none had been returned.

V2 normalizes all maxupper inputs with iv.mpf before taking absolute value
and the interval upper endpoint. Only that numerical utility and source-pin
metadata change. Before the new run, compare function ASTs and check that
every function except maxupper is identical to V1. Freeze V2 and sidecar;
use a fresh attempt_02 directory. No equation, charge ensemble, threshold,
precision, domain or rejection rule changes. Run a fresh full exact replay.

Clarification already implicit in V1's nonzero-mode gauge restriction: retain
the mean metric pairs and translation kernel, not just their constraints.
An odd reflected pair of compact F supports has int F=0, so the induced
pi_zz has zero mean. The reflection-invariant coefficient bounds and the
patch Poincare/Young inequality apply to each support. Radial chi can also
be chosen of zero mean. This does not invert the zero mode or remove a
homogeneous physical degree of freedom. It makes no additional physics claim.

This remains a constrained instantaneous momentum-form calculation, NOT a
full physical Hessian, Cauchy theorem, ghost diagnosis or physical cutoff.
No existing evidence is rewritten; no state/action change or gate promotion.
