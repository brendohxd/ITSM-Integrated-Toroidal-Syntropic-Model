# Weighted evolution V3: univariate Laurent extraction

17 October 2026. Supplements the original contract and V2 compute addendum.

V2 / attempt03 bypassed the multivariate GCD stall, then returned
ValueError: Non Laurent coefficient. The V2 extractor recognized powers only
from syntactic multiplicative factors. Equivalent unfactored denominators can
contain a common ell power which that syntactic test does not recognize.
The interrupted attempt, V2 executable and sidecars remain unchanged.

V3 uses exact numerator/denominator polynomials in ell for each additive term.
It requires a one-monomial denominator in ell and extracts every numerator
coefficient divided by that monomial's coefficient, retaining negative powers.
Every complete matrix entry is reconstructed and checked by exact expanded
rational numerator equality. A genuine nonmonomial denominator is rejected,
not approximated or expanded asymptotically. Test unfactored monomial
denominators, retained positive/negative powers, and a rejected non-Laurent
example independently before the scientific calculation.

This changes representation/parsing, not the action, constraints, background,
coordinate changes, norm, equations, remainder, numerical data or thresholds.
The scientific Derivation and interval-bound class ASTs must remain identical
to V1; the extractor's changed AST is explicit. V3 uses fresh attempt04 with
the original complete-source provenance and exact read-only replay.
All physical, canonical, review and authority boundaries are unchanged.
