# A16.2 finite-state/history V2 symbolic-generator mismatch

16 November 2026. V2 completed 58/59 checks. The only failure was the hidden
characteristic-polynomial identity. SymPy charpoly replaced the requested
real symbol lam with a same-named symbol carrying only commutativity, so
poly.gen != lam. Subtracting expressions in those distinct symbols did not
produce zero. A separate direct det(lam I-K) calculation has exact residual
zero. V3 uses that direct determinant test. All matrices, bounds and physical
holds remain unchanged; V2 stays a failed receipt with its original hashes.
