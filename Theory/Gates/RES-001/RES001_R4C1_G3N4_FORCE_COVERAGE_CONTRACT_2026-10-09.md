# R4C1-G3N4 force-coverage supplement: frozen controls

Date: 9 October 2026. Version 1. Test-1 / G3N4 only.
Conditional research; review DEFERRED; physics_pass=false; gate_effect=NONE.

## Boundary and provenance

The original G3N4 executable and receipt remain unchanged. Their 46 local
checks do not test the field-by-field claim about the other nonanalytic
force sources. This supplement supplies those missing controls, not a new
action, response solution, cutoff or physical Test-1 pass.

Owning G3N4 contract SHA-256:
a5f5880e894c544794fa46e7e68dfdd07c4960d44791751521b402cd8bb9a2b6.
Original executable SHA-256:
080bb2c0aef277dda5a57f3f61a449e4da2f92813f84af05f5fa711666e29144.
Original summary SHA-256:
6dde40b37ca40409566151c997bcc663edd923f1119fdcd019728a87dfd450e1.
Inherit the frozen R4C1 action, source pins, three absent sidecars and all
original scientific failures. No original receipt or sidecar is repaired.

## Exact calculation and rejection conditions

Retain all 22 response fields and their time/spatial jets in the inherited
(t,z) ADM/boost chart. For the original unsmoothed density
-A N sqrt(det h) Y^(3/2), derive the linear variation of the inverse metric,
normalized n, projected Y and volume directly. Use n in this sector, not
the independent off-unit U=(1+d nu)n belonging to L_U.

Keep e real and both signs; do not impose the first-order shift solution.
Check every field's value, time and spatial variation coefficient. Derive
the Euler sources including the 3H volume term. A source that starts at
order |e|^3 is not identically zero and is not a solved response.
Handle p=psi_dot=0, W=0 and e=0 without division by sqrt(Y), p or W.
The derivative of Y^(3/2) at Y=0 is zero on its nonnegative domain;
no ordinary cubic Taylor vertex or force smoothing is permitted.

Independent controls evaluate the exact unexpanded ADM inverse, n and
projected force density at 50 decimal digits. Compare centered response
differences at d=1e-8,5e-9,2.5e-9 for all field values plus Pi_t and Pi_z,
at both signs of e, p and W. Final normalized error must be <=1e-12 and
decrease across steps or remain <=1e-14 at the numerical floor. Include
separate p=0 and W=0 controls. Do not relabel generic jets as physical
solutions or upgrade inherited background precision.

Export exact directional amplitude degree for each Euler source, testing
both signs of e. Reject replacing e|e| by e^2, dropping the density's
volume variation, or using unnormalized U in the projected force.

Promote the previously separate exact source-identity cross-check into
this supplement's receipt: in the declared G3 family, verify
temporal residual=(H W-W_t) E_W and longitudinal residual=W_z E_W
against the original G3N4 exported formulas, without imposing E_W=0.
These are the registered temporal and longitudinal identities, not an
assertion about every three-dimensional diffeomorphism identity.

## Integrity, output and nonclaims

Create new versioned source, coefficient/control receipts and sidecars.
Refuse existing output directories; exact replay must be read-only.
Record every failed assertion, unknown and inherited failed attempt.
The original G3N4 46/46 result remains distinct from this supplement.
The combined source-ledger scope is only the registered plane-wave chart.

The complete response kernel, compatible initial data, nonlinear Cauchy/DAE
domain, stability, physical Hessian/cutoff and healthy continuous GR limit
remain substantive. Review alone remains DEFERRED, not cleared.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
No manuscript/PDF/vault change, provider dispatch, commit, push or release.
