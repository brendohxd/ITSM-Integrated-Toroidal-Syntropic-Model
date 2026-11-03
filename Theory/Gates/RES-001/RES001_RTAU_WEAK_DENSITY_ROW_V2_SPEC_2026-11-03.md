# Weak density row V2 multiplication dispatch correction

3 November 2026. Inherit all scientific requirements from the
[V1 specification](RES001_RTAU_WEAK_DENSITY_ROW_V1_SPEC_2026-11-03.md).

V1 failed before returning a receipt: mpmath's interval-left multiplication
attempted to convert a Taylor jet to an interval and raised
NotImplementedError. V2 moves the scalar coefficient to the right of the
same Taylor-jet product. The value, equation, derivative content, domain
and acceptance are unchanged. Preserve and pin V1 source, contract,
sidecars and failure record; use a fresh receipt and exact replay.
