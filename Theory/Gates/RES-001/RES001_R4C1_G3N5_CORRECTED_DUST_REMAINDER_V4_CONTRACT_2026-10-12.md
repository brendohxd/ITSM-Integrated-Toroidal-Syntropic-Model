# G3N5 corrected remainder v4: factored exact background derivatives

Date: 12 October 2026. Inherit all scientific requirements and controls from
[v3](RES001_R4C1_G3N5_CORRECTED_DUST_REMAINDER_V3_CONTRACT_2026-10-12.md).
Keep the positive forced response, all original states, five modes, four
columns, background/constraint/momentum drift, paired full-coupled solvers,
rejection tests and exact interval rules. No physical equation, action,
initial data, numerical tolerance or acceptance requirement changes.

Compute dq3=dt(q3) and df4=dt(f4) once using the frozen exact background flow.
Reuse those SAME exact expressions in coefficient identities, forced residual,
drift rejection and norm bounds. For the interval norms do not first cancel
the entire derivative into a single expanded multivariate fraction. Apply
v3's factor-preserving real/imaginary evaluator directly to the exact sums of
background derivatives. Cancellation changes representation, not the function;
both enclosures are valid but their constants need not coincide.

Require an exact quotient/chain-rule regression with an independent closed
derivative and an exact rational whole-box enclosure. Retain the existing
real/imaginary/mixed/zero-denominator controls, full source-identity checks and
all original-data/coupled-solver controls. A regression or shorter runtime does
not replace the whole-domain remainder proof or establish sharp convergence.

Add private progress phases around coefficient identities and interval norms;
these are diagnostic observations, not acceptance results. Keep v3 source,
contract and sidecars byte-identical. Record its interrupted calculation as
NOT_EVALUATED/SUPERSEDED_FOR_VALIDATED_FACTORED_DERIVATIVES, not physics failure
or an observation-timeout restart. Use fresh attempt_04 and preserve earlier
attempts, including v1's distinct invalid forcing sign.

Full retained mismatch response is never discarded. Sharp/actual convergence,
full dust closure and useful finite-mode accuracy remain outstanding unless
separately established. physics_pass=false; gate_effect=NONE;
Rule9_cleared=false; review DEFERRED; Tests 1-3 HOLD_SUBSTANTIVE;
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; TOP-X4 UNCHANGED. Stage 2 stop and Stage 3 matching gap unchanged.
No publication, provider/model dispatch, vault mutation, commit or push.
