# Initial acceleration audit V2 schema correction

Audit V1 was 10/11. Its endpoint loop verified all exported bounds, but an
extra assertion incorrectly expected 13 bound records. The actual schema
has 12 named bounds. V2 checks the exact required key set instead of a
mistyped count. All geometric, derivative, residual and physical thresholds
are unchanged. Preserve the failing audit source/receipt and primary result.
