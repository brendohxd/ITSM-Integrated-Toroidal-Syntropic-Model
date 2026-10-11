# R4C1-G3N5 v2: exact expanded export, unchanged scientific calculation

Date: 9 October 2026. Version 2 export addendum, frozen before execution.
Conditional research; review DEFERRED; physics_pass=false; gate_effect=NONE.

## Diagnosed implementation boundary

The original v1 calculation has not produced a terminal scientific receipt.
Three identity-bound, read-only Python stack samples all located it in
SymPy polynomial-content/factorization calls beneath `tidy` at v1 line 42,
called by `derive` line 274 while formatting sector quadratic densities.
The samples inspected code metadata only: no process suspension, injection,
process writes, Python locals, packages or runtime settings were changed.
This locates an export bottleneck; it does not establish that any pending
independent control has passed. The private diagnostic log remains local.

Original executable SHA-256:
0863c4b150a3184d152263da2fa65f4f50f5b344653294cf8fc99326b62295f7.
Original response-kernel contract SHA-256:
11cf25cef8cc0192f1f690dbf1f7fee2f9e0268eff508d7fb1a65709907f2c02.
Private stack diagnostic SHA-256 (not a scientific receipt):
658a54392530271975f4452b540c2d48a5b5610ad1bf215ae0a584c610aadb98.

## Exactly permitted v2 changes

1. Create `test_01_r4c1_g3n5_response_kernel_v2.py`; preserve v1 and all its
   original hashes, receipts and diagnostic evidence without modification.
2. Serialize each expression in exact expanded form instead of requesting
   generic multivariate factorization solely for printing. This applies to
   densities, tadpoles, Euler operators, Ricci/boundary expressions, projected
   force gradient and sparse Hessian coefficients. The expression values do
   not change. Factorization used by original scientific residual checks is
   not replaced or weakened.
3. Verify every serialized expression by exact symbolic reconstruction.
   Store a round-trip audit with expression hash and term count. Reject any
   nonzero reconstructed difference; do not use a numerical tolerance here.
4. Add flushed stage messages to distinguish derivation, export and the
   independent controls. These messages are diagnostics, not evidence of a
   passing assertion. The optimizer's captured-output boundary is unchanged.
5. Add version/provenance metadata and a separate attempt directory that
   refuses overwrite. Preserve the original failed G3 and N3 checks and all
   inherited source pins. Exact replay remains read-only.

The original action, background chart, off-unit normal variation, all 22
fields, 110 value/first-derivative jets, all second jets, x/y/z derivatives,
volume factors, signs, units, periodic Ricci identity, Euler measure, all
original assertions, numerical jets, 50-digit precision, step sizes and
acceptance thresholds remain unchanged. No gauge, mode, parameter or domain
restriction is introduced by this addendum. No on-shell condition is added.

Verify the v1/v2 ASTs before running: unchanged helper functions and the
complete `derive` statements before its export block must agree exactly.
The original independent-control and exact-check functions must also agree.
Any later correction needs another frozen version, not a rewritten receipt.

## Outstanding work and nonclaims

This remains an unreduced quadratic kernel on the specified background,
not a coupled second-order solution, physical Hessian, stability proof,
general nonlinear initial-value evolution or healthy GR limit. The force's
unsmoothed directional cubic term and harmonic tail are not removed.
The temporal-block comparison still requires a separately versioned
comparator accepting this v2 source pin; its existing v1 receipt is untouched.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
Pending review alone does not block provisional research. Missing physics
still does. No manuscript/PDF/vault change, provider dispatch, runtime
reconfiguration, commit, push, canonical promotion or publication is supplied.
