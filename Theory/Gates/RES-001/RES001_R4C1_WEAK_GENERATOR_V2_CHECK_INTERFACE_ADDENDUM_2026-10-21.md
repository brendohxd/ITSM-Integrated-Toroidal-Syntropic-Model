# V2 check-interface addendum: preserve the actual legacy boundary rule

21 October 2026, BEFORE any V2 executable or scientific execution.
The V2 contract's sentence requiring rejection of a boundary-valued legacy
assertion is incorrect. Direct source inspection shows the original method is
`mp.isfinite(value) and value <= mp.mpf(tolerance)`, not a strict inequality.

This addendum supersedes ONLY that sentence. The adapter must call the pinned
original legacy method unchanged, accepting both below-threshold and equal-
threshold finite values and rejecting above-threshold and nonfinite values.
Test all four outcomes. The NEW response-factorization checks retain their
separately specified strict `<1e-20` rule. No numerical tolerance is relaxed.

The V1 source/failed receipts and the V2 contract retain their original bytes
and hashes. The local `inspect.getsource` attempt on an imported class raised
a module-discovery TypeError; inspecting the actual method function then
located the original implementation in `test_01_r4c1_initial_admission_v1.py`.
This was read-only source inspection, not a scientific calculation.

No physics/gate/review status changes. Scope and remaining requirements are
exactly the V1 contract plus the V2 adapter contract, with this explicit
pre-execution correction to the adapter's boundary self-test.
