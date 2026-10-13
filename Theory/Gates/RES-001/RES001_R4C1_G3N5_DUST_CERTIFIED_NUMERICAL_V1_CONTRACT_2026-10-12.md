# G3N5 certified finite-mode numerical control — version 1

Date: 12 October 2026. Stage 1 / RES-001 / Master Test 1.
Operator selected this route after the complete finite-energy budget remained
too conservative. The action, diagnostic parameters, prepared initial-data
definition, five modes and complementary probes are NOT changed.

## Frozen scope and criteria

Use the original exported balanced 20-complex-state generator Az, actual dust
observable Oz=Obs B^-1 and all 22 reconstructed fields Fz=F B^-1. Retain all
four original initial columns. The first two are the original normalized formal
slow lift; the other two are the original projected-at-initial-time seed recipe
at indices 9 and 19, normalized by the largest complex component magnitude.
Projection is permitted ONLY in that existing initial-data construction.
Evolve the entire coupled generator thereafter. No discarded fast sector,
constant background, constraint projection, omitted basis/momentum drift,
mean-mode substitution or inserted acceleration target.

Time: [0,1/20]. Modes: ell=4,8,16,32,64, nonzero longitudinal chart. Positive
a,C,rho and the original rotating B1 Friedmann shell with angular charge 1.
The zero mode and other physical-domain questions are NOT certified here.
The saved 70-digit degree-40 background and leading-transfer polynomials are
treated as EXACT written decimal approximants, not automatically exact flows.
Their continuous residuals and initial discrepancies must be independently
enclosed against the declared background ODE and leading M generator.

Pre-execution computational criterion: certify <=1e-8 absolute error for each
column of the actual dust observable and each reconstructed field, at ALL times
in the interval. Pre-execution useful-model benchmark: <=1/100 in the induced
infinity norm for W_full-Phi_M, for unit W0 in the original two-column prepared
span, across the complete interval and every mode. The 1% number is a declared
dimensionless diagnostic benchmark, NOT an observational tolerance or evidence
for cosmological accuracy. Preserve and report failures if either criterion
cannot be met. A computational certificate alone does not complete the dust
milestone. No changing the benchmark after inspecting this new certificate.

## Arithmetic and continuous defect proof

Use standard-library signed-integer interval endpoints in units 2^-256. Every
multiplication/division/rational conversion rounds endpoints OUTWARD with exact
integer floor/ceiling. Zero-containing denominators are rejected. Square roots
use integer isqrt endpoint brackets. No unverified floating-point radius is used.
Polynomial degree 40 for global background/operator approximants; degree 24 for
each local full-state approximant. All omitted polynomial tails are bounded,
not discarded. Polynomial/inverse operations retain an explicit symmetric
remainder. For an inverse approximant V of P+e, bound

    (P+e)^-1 - V = [1-P V-e V]/(P+e).

Enclose the complete polynomial numerator, including low-degree arithmetic
residuals, and require a positive lower bound on the denominator magnitude.
Restriction to a time tile retains the inherited remainder and EVERY discarded
higher coefficient. Point-valued local coefficients are exact dyadic centers;
their difference from interval RHS coefficients enters the continuous defect.
Adjacent tile endpoints are summed exactly, so any jump must be detected.

Step count is a power of two, at least 32, chosen BEFORE trajectory evaluation
to make h times the global balanced-generator infinity-norm majorant <=1.
Refuse >32768 tiles rather than silently changing arithmetic or input scope.

Enclose background defect db, initial discrepancy eb0 and a Lipschitz constant
Lb on a convex positive-denominator box containing exact and approximate
backgrounds. Use continuation/Gronwall, and require the resulting eb to fit
strictly inside the box margin. Preserve exact constraint/charge identities;
do not reset a numerical solution to their shell. The inherited original exact
background-box and full Q-propagator proof remain explicit dependencies.

For the full-state error e_z, use the original T(b)=Tw(I+U/ell)^-1 C and
e_w=T(b)e_z. The verified FULL Q propagator bounds its homogeneous evolution
by exp(30(t-s)); Q is an evolution norm, not a physical Hamiltonian.

    e_z' = Az(b)e_z + [Az(b)-Az(bhat)] zhat - rz,

so the forcing includes BOTH the continuous numerical defect and the background
coefficient error. Bound Az's background derivative, full zhat amplitude and
T's infinity-to-Q norm. Include exact initial-data/rounding discrepancies.
Convert the propagated Q error to every actual observable and reconstructed
field, including their own background dependence. Separately enclose the
leading-transfer defect and background contribution. The difference of two
approximants is NOT claimed to be the physical model error without these terms.

Record rational/dyadic constants, all tile maxima and all domains. Endpoint or
sampled DOP853/Radau agreement is diagnostic ONLY, never the certificate.

## Verification, preservation and dispositions

Require exact-rational controls for interval primitives, positive/negative
division, square-root enclosure, zero-denominator rejection, inverse-tail and
restriction-tail retention. Require omitted-defect rejection and an independent
high-frequency skew-rotation Taylor control with a rigorous analytic remainder.
Verify inherited source/sidecar hashes and preserve input size/mtime metadata.
Compare against all original four-column trajectories without overwriting them;
report their complementary responses/nonmonotonic behaviour without retuning.
Require fresh receipts and exact read-only replay, including failures.

Validation, useful mathematical dust control, physical conclusions and deferred
review are separate flags. Full dust milestone remains OPEN unless ALL original
plan requirements and this finite-mode acceptance are satisfied. Goal remains
incomplete until all three original milestones are achieved.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Stage 2 stays STOP_AND_ASSESS_DOMAIN_UNRESOLVED; Stage 3 NOT ENTERED.
No new parent, target fit, provider/model dispatch, paid session, dependency
installation, runtime configuration change, vault mutation, commit, push or
publication. Source/report/failed-attempt/sidecar originals remain untouched.
