# Inner Cauchy V2: subtract the exact particular state before matching

29 October 2026. Under the unchanged INNER_CAUCHY_V1_CONTRACT.
Conditional; Rule-9 DEFERRED; physics_pass=false; gate_effect=NONE.

Final mathematical audit invalidated V1's interpretation. Its executable,
digest and 17/17 receipt are preserved unchanged:
Analysis/MasterTests/outputs/r4c1_inner_cauchy_v1_attempt_01/summary.json,
SHA256 0900225c9e552850e37f82dc14f989b6291d8ad57adfad97ad0501750f5a302c.
The checks validated the interval propagation and homogeneous-basis inverse
but omitted a necessary affine-matching check. Computational PASS therefore
did not certify the reported connection or physical model rejection.

The ODE remains inhomogeneous beyond s=16. Matching its FULL state directly
to a homogeneous basis, as V1 did, does not continue the same solution. The
exact particular solution is

    Fp(s)=L*s/(20*a)+S0/(840*b*a^2),
    Gp(s)=-S0/(20*b*a).

V2 first checks these expressions in BOTH original ODE equations exactly,
then subtracts (Fp,Fp',Gp,Gp') from the certified Cauchy state. Only that
homogeneous remainder is connected to the infinity basis. It also checks
that adding the particular state back reconstructs the enclosed full state.
The independent DOP853 control continues to compare the FULL Cauchy state.

No source, Cauchy datum, parameter, model, interval precision, Taylor order,
Frobenius order, tail bound, matching point or criterion is changed. V2 pins
V1 and this note and writes a fresh receipt. Zero-containing corrected
coefficients must remain unresolved; no result is forced to match V1.

The unsealed V1 draft report/review entry had already repeated the invalid
interpretation. Exact draft bytes are backed up locally before a prominent
invalidity notice is added. No live research index recorded that conclusion.
The old source/receipt and previously sealed research evidence are untouched.
