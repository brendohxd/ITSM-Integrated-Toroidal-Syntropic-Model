# Cusp3 local initial jet V2: independent solver boundary

16 October 2026. Preserve V1 and its incomplete attempt01 record unchanged.
Exact prerequisites reached numerics, but the first independent mean-mode QR
solve raised "matrix is numerically singular" before a complete receipt.
The original23-by18 comparison matrix has rank18; independent numerical
singular values range0.041666666666666664 to1.9874694460964148.

The installed mpmath1.3.0 Householder implementation chooses its pivot using
sign(real(A[j,j])); an initial zero diagonal can yield a zero Householder
pivot even for a full-column-rank matrix. A separate3-by2 zero-diagonal
full-rank example reproduces the error. This diagnoses the comparison
algorithm, not a singular physical reduction at that event.

V2 solves the same row/column-scaled ORIGINAL augmented system through its
Hermitian normal equations at80 decimal digits, using LU. Retain ALL original
equations and check their residual with the unchanged1e-9 criterion and the
unchanged1e-7 comparison. Normal equations square the condition number; no
claim of certified solver-error control follows. Add exact full-rank real and
complex zero-diagonal controls to check the solver and conjugation.

No physical expression, source, reduction, domain, tolerance or old initial
datum changes. Fresh attempt02; pin V1, the incomplete record and this
addendum. The original frozen contract still governs. All physical-window,
nonlinear-admission, GR, matching, review and canonical holds remain open.
