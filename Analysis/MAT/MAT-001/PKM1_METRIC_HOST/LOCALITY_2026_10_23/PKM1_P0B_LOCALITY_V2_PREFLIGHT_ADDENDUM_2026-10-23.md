# Locality executable V2: symbolic inference repair

23 October 2026. Contract V1 and frozen_inputs_v1.json remain unchanged.

V1 attempt 01 completed with 98/99 local checks. The only failed assertion was
`P0-B stable tail derivative positive`: SymPy returned None for the positivity
predicate of the unsimplified derivative of y/(1+y). It was mapped to a failed
check, not treated as a physics pass. Exact factorization gives 1/(1+y)^2,
strictly positive for the declared y>0; the identity residual is zero.

V2 changes that predicate to ask positivity after exact factorization. The
force law, action, coefficients, observational inputs, orbital solvers,
tolerances and substantive physical holds are unchanged. The V1 executable,
SHA-256 sidecar and all failed-attempt files remain untouched. V2 uses fresh
write-once receipts and requires the existing separately implemented verifier.
This is a computation/inference repair, not a physical result or relaxed test.

V1 executable SHA256:
5e4d4c44f5d0dd69971aa5bc8807190769e91158993cd5ed8033a08f4b85d966.
Original receipt: receipts/primary_v1_attempt_01/summary.json.

Rule-9 DEFERRED; physics_pass=false; gate_effect=NONE. Repository integration
remains pending because the ITSM checkout rejected scoped apply-patch writes.

