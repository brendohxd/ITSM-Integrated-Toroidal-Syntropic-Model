# Weak canonical rate V2 implementation correction

3 November 2026. Inherit the complete scientific requirements of
[V1 specification](RES001_RTAU_WEAK_CANONICAL_RATE_V1_SPEC_2026-11-03.md).

V1 failed before returning a receipt: the linear shift-generator matrix
contains exact Python integer zeros, but its endpoint extractor assumed
every scalar already had an interval representation. V2 converts numeric
scalars to intervals at that extractor boundary. It preserves the same
matrix, equations, domains, bounds, rejection controls and acceptance.

Keep the V1 executable, specification, source sidecars and failure record
unchanged. Pin them in V2 and use a fresh output directory. Repeat the
entire calculation and immutable replay; do not reuse partial V1 results.
No physics, physical norm, compatible-generator or time-tube promotion.
