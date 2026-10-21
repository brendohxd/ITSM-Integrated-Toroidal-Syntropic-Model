# Dimensional audit V2: correct an expected-digest transcription error

19 October 2026. Keep the V1 dimensional contract and failed V1 executable/
attempt01. V1 stopped in source verification, before dimensional mathematics,
because its hard-coded equations digest contained an extra 'd'. The original
equations bytes and original sidecar were checked against the external
pre-replay snapshot and remain unchanged.

V2 changes only this expected reference, adds source pins for V1 and this
addendum, and keeps all dimensional rules, tests, precision-independent exact
controls and scientific holds. Correct equations SHA-256:
4aa8b6ff0abea3840a4aaededd6a4a713a89a9c29477d23f1585ee8042723857

Freeze final V2 bytes after AST preflight; use fresh attempt02 and complete
read-only replay. No historical file, hash, receipt or sidecar is rewritten.
