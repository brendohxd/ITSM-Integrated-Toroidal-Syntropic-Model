# Joint completion V2: repair independent numeric matrix construction

19 October 2026. Keep the V1 contract and frozen V1 source, attempt01 and all
failed controls. V1 certified nine restricted interval roots, but its independent
metric/frame control then failed in all nine cases. The overall123-check result
was114 passed /9 failed, not a completed audit.

An installed-mpmath1.3.0 reproduction shows that matrix(3,3,callable) creates a
zero matrix: its third positional argument does not populate entries. The
SymPy callback constructor was incorrectly copied into the mpmath control.
This explains the numerical-singularity exception after the direct three-
equation point-root checks; it is not evidence that the varied metric operator
or physical reduced Hessian is singular.

V2 uses an explicit three-row list of the same nine evaluated original matrix
entries. Check every copied entry and its nonsingularity before the unchanged
original metric/frame solve. Keep every symbolic expression, velocity chain
rule, interval test, domain, precision and numerical tolerance unchanged.
Verify the original V1 interval certificates remain numerically identical,
excluding only the failed-control metadata flag.

Freeze final V2 bytes after AST preflight; use fresh attempt02 and complete
immutable replay. Do not edit V1 or its receipts, hashes or sidecars. The
restricted root result is not full initial admission, state adoption/evolution,
a physical window, healthy GR or microscopic matching. All scientific/review
holds and authority boundaries from the V1 contract remain unchanged.
