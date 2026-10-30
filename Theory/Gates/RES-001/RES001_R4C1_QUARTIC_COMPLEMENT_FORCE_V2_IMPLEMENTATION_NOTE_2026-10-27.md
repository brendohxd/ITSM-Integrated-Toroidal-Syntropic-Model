# Analytic complement force V2: preserve interval scalar context

27 October 2026. Same frozen analytic-force contract and computational addendum.
V1 source SHA256 c9b19d86391703d8386d8845c927d969d25567282a3c1d665c95a413a15b830c
is preserved. It stopped during the first whole-circle interval evaluation,
before a scientific receipt, with mpmath's "can only create mpf from zero-width
interval". The complete failure log is ignored local artifact
.local/itsm-context/output-c5cb214efc174bd1af97f113d59b2f92.txt,
SHA256 1d5737b78e65ee7cc618f8f6d5fc5593984cbc2449ced27190e200eb4e5f0ca6.

The directional arithmetic mixed an ordinary mp scalar with an interval
direction. mpmath attempted to convert a non-point interval to a point scalar.
V2 explicitly promotes both operands and their directions into interval context
whenever either operand is an interval, including power coefficients. Ordinary
point controls remain in point context. No enclosure was accepted from V1.
No source equation, field/domain, precision, tolerance or acceptance changes.
Freeze V2 before launch and pin V1 plus this note. Review DEFERRED; G1 open.
