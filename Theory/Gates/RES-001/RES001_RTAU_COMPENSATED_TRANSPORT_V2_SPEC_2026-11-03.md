# Compensated transport V2 implementation correction

3 November 2026. Inherit the complete V1 transport contract without changing
equations, inputs, domain, inequalities, constants or acceptance tests.

V1 is preserved with its source, sidecar and failure record. It failed at
the scalar-forward pullback coefficient before producing a receipt: a
point-mpf left operand attempted to coerce a nonzero-width interval during
addition. V2 explicitly converts that point coefficient to iv.mpf before
adding the interval r. This is a numeric-type correction, not a modified
transport estimate. Pin the V1 source/spec/failure as evidence. Use a fresh
V2 receipt and exact replay. Do not report the failed V1 as passing.

All original scope/physics/review holds and preservation requirements remain.
R-tau unadopted; review DEFERRED; physics_pass=false; gate_effect=NONE;
G1-G6 incomplete. No action adoption, vault mutation/sync or Git delivery.
