# Prepared temporal V2 implementation repair

The V1 run produced 24/26 checks. Both failures are exact spatial rotation
controls. In the symbolic test's tensor basis, Python integer division
`1/1` introduced a Float(1.0) on diagonal matrix basis entries. The numeric
100-digit full-action controls passed, but do not excuse failed exact
identities. Preserve V1 and its failing receipt without alteration.

V2 makes the SymPy basis's unit and denominator exact Integer objects.
It also constructs the frame interval as [-1,1]/10000 directly with outward
interval division. No equation, physical domain, acceptance threshold,
variable, action or parent result changes. Pin the failed source/receipt
and this specification. Recompute every check and exact read-only replay.
All scope limits of the V1 contract remain; physics_pass=false.
