# Second-node enclosure V2: shared-parameter loader correction

27 October 2026. V1 stopped before mathematical checks with KeyError m2: the
family parameter map omits shared potential constants. Its source/sidecar and
traceback remain, with no scientific receipt. Private log:
output-f001d87735084c6084fed5b09e97a7d0.txt,
SHA256 ca5cc000ba9ebf57a6f1970512cef45a0942d1fc49914ccd3f5fcc09ba5f6a6a.

V2 adds the same AST-based shared-constant loading used by the existing canonical
parameter loader, retaining exact SymPy values and eta=1/4. The source's integral
float literals 1., 2. and 0. are represented as exact integers; nonintegral float
literals are rejected rather than silently rationalized. It changes no action,
equation, case, interval box, criterion or interpretation. The version docstring
and new AST import identify the correction. V1 remains unchanged. Freeze V2's
hash before execution; use a fresh V2 output directory. This is an implementation
input-loader failure, not a physics rejection or a changed scientific tolerance.
