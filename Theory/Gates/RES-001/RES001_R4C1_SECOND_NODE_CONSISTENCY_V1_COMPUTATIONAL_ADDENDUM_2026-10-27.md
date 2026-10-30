# Second node consistency V1: geometric and trace controls

27 October 2026. Contract SHA256
03ee2cfc1d62f89633360a4963b2d20310a58d0ef61cb392112a539d0ab99cea.
Freeze before execution. This stage derives/tests the necessary trace and
evaluates approximate initial data; it does not certify its sign at the exact
joint root or complete G1.

1. Independently evaluate the regulator Euler equation in four-dimensional
   coordinates: E_Z/b=Z+div(hp*grad psi)-acc.grad psi, with the full ADM metric,
   future-unit frame and connection. Use four nontrivial Taylor-jet controls,
   both signed slopes, arbitrary metric/off-diagonal acceleration and spatial
   acceleration variation. Verify at the initial node that
   partial_t^2(E_Z/b)=aZ+partial_z^2(aPsi)+p*partial_z(aVz).
   Eighty working decimal digits; normalized tolerance 1e-30. Retain cubic and
   quartic scalar time jets; no metric-acceleration freezing. These are geometric
   identity controls, not physical background states.
2. Evaluate candidate nodal acceleration formulas on the same approximate
   corrected joint representative used by the 176-check diagnostic. Use the
   controlled shift's r1 and its r3, checking the exact original shift equation
   separately. Avoid division by w at the node by cancellation before evaluation.
3. Obtain local rho2 and the coupled longitudinal-frame acceleration slope from
   the full twelve-dimensional complement, retaining all metric accelerations.
   Use local initial jets through sufficient normal order, not a fit to finite
   angle data. Use 100 working decimal digits and complex steps 1e-25,1e-30;
   two-step normalized tolerance 1e-18. Use real numerical differentiation for
   Taylor coefficients, with the original reverse-AD gradients internally.
4. For coefficients through the required normal orders, establish why the C2
   cusp's composites make no contribution. A=0 may be used ONLY as an arithmetic
   device for extracting those coefficients once their vanishing order is stated;
   it is not a changed action or a deletion from the sampled acceleration field.
   Keep the nonzero original A in all general physical uses. No ordinary third
   cusp tensor is assumed at alignment.
5. Check the candidate partial sensitivity to Z=U*w^2+W*w^4 while H/U/shift jets
   are held fixed. This is a local sensitivity diagnostic, not a constraint-
   preserving background change. No W value or corrected root is adopted.

Record both-node approximate traces, local coefficients and all failed/unknown
controls. No diagnostic sign, printed precision or finite-angle agreement is
an exact-background exclusion. The later sign decision requires a validated
joint-root/shift enclosure or an equivalent exact undivided proof. The old fourteen
sample points were already inspected before this addendum; this is not a blind
confirmation of a previously sealed physical prediction.

Pin the previous executable/receipt, current contract/working note and original
dependencies. Fresh output directory, no overwriting; support immutable replay.
Preserve implementation failures in new versions. At most four independent
workers; parent alone writes receipts. No action/threshold/provider change.
