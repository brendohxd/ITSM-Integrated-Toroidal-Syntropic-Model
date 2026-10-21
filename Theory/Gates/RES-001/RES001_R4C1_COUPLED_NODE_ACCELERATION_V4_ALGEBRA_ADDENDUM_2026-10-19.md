# Coupled node V4: exact algebra optimization and interval-input repair

19 October 2026. Continue the unchanged R4C1 calculation under the V1 scientific
contract and V2/V3 execution addenda. The operator explicitly approved stopping
the current run and optimizing algebra without changing its equations or tests.

## Preserved attempts

V3 had already terminated, exit 1, when the stop instruction was checked. Its
source remains SHA-256
881e58aaecbb8b3f2133bc2cbf3bb55716cf4e6e703181b3fbe8ff5e5df55205.
The terminal output records completion of symbolic derivation and both coordinate
control tasks, then KeyError: 'slope' in interval evaluation. Task completion is
not evidence that their scientific checks passed. No final scientific receipts
were returned. Preserve attempt03, its source/sidecar and private output/progress
logs. This is not a physical rejection and no replacement datum may be invented
merely to make the evaluator run.

## Allowed exact transformations

1. Replace algebraic substitution by exact simultaneous atomic replacement ONLY
   for independent Symbol keys in these already-differentiated rational
   expressions, with no binding operators or key dependencies in replacements.
   Keep differentiation before restriction and every varied equation.
2. Reduce the substituted frame slope as a rational function of the signed
   nodal slope BEFORE replacing its even powers by k^2*alpha. Check orientation
   symmetry and every numerator/denominator reconstruction. Reject leftover
   odd powers or any unresolved slope variable. Both signs are retained.
   This enforces the registered identity slope^2=k^2*alpha; it is not a new
   state choice, frequency input, fitted coefficient or a division by amplitude.
3. Normalize the scalar defect by collecting only in alpha over expression
   coefficients, instead of expanding and factoring all physical parameters
   together. Simplify coefficients independently, in deterministic parallel
   order where useful. Prove the constant coefficient vanishes EXACTLY before
   dividing the polynomial by alpha, check coefficientwise reconstruction and
   retain the full denominator and its nonzero-endpoint/domain checks.
   Do not replace this by finite precision subtraction or a sampled limit.
4. Check interval-function free-symbol coverage explicitly before evaluation.
   A missing symbol is an implementation failure, never a default zero or an
   invitation to fill in an unapproved physical value.
5. Add ignored progress timings and check snapshots, including exact failed
   assertions, to make future long algebra steps auditable. Operational data
   remain excluded from deterministic scientific payloads.

## Acceptance and preservation

Add bounded execution-only controls for atomic replacement, signed even-rational
reduction, removable-zero rejection, and serial/parallel coefficient equivalence.
These do not replace the original coupled equations, independent coordinate
variations, all nine families/eta cases, continuous amplitude domain, original
precision, frozen partitions, source pinning or complete immutable replay.
Source and addendum final bytes must be frozen after AST preflight and before
execution. Use a fresh attempt04; further substantive changes require a new
version. Preserve all earlier files, hashes, failed checks and failed attempts.

A genuinely odd remaining slope or nonzero constant term is a substantive
derivation/check failure, not something to suppress for an execution PASS.
An unresolved scientific enclosure remains unresolved. No physical family or
initial state is admitted by this optimization.

Stage1 original bounded linear acceptance only; Stage2 INCOMPLETE; Stage3
NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; K_Q NOT_DERIVED;
V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED; TOP-X4 unchanged;
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.
Full initial admission/persistence, physical window, healthy GR and both
identifying matching inputs remain open. No state adoption/evolution, action,
provider/model/global-runtime change, vault mutation, manuscript/site edit,
publication/submission, commit or push is authorized here.

Implementation references:
- https://docs.sympy.org/latest/modules/core.html#sympy.core.basic.Basic.xreplace
- https://docs.sympy.org/latest/modules/polys/reference.html
