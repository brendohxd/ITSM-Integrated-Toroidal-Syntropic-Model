# Quartic node transport: full regulator scalar-jerk response V1

27 October 2026. Follows the bounded initial acceleration report, unchanged
R4C1 action, registered B1 eta=1/4,e=1/500,k=40 and complete quartic root box.
Conditional; review DEFERRED; G1-G6 INCOMPLETE; physics_pass=false.
The preceding TRANSPORT_WORKING_ALGEBRA remains unvalidated historical work.

## Test the actual differentiated constraint

Differentiate the full original regulator equation E_Z/b=Z+div(hp*grad psi)
-acc.grad psi on the initial slice. Retain the corrected general geometry
including (gamma*Vz-c*R)*partial_z(log sqrt(h)). Initial lapse1 and shift time
jets0 are declared gauge choices; do not silently change them. All metric
and frame second-time jets must remain until their cancellations are derived.
Z and Zdot are fixed in this response test. The scalar acceleration is the
already derived analytic initial function, not a newly projected profile.

Derive the response of j=psi_ttt to the actual coupled cusp acceleration.
Verify, rather than assume, the candidate formula

    delta j=-p*(ay_cusp[Vy]/w+trace(ay_cusp[hdiag])/2), w!=0.

Use the complete B(w)^-1 and exact twelve-component cusp force. Derive any
leading node coefficient from B(0)^-1, not from a vacuum frequency. Prove
required inverse-entry parity/zero crosses from the exact B conjugation and
nonsingularity. Bound inverse first/second derivatives using outward80-digit
matrix norms and the already certified inverse bound on |w|<=e/2.
Derive an explicit cubic remainder before asserting a nonzero cusp.

## Independent coordinate geometry controls

Use the full four-metric, normalized n, connection acceleration and volume-
weighted coordinate divergence. Construct independent Taylor fields retaining
all six metric second jets, all three frame second jets and their spatial
gradients. Working90 digits. At w/e=-1,-1/2,1/2,1 with both normal slopes,
compare partial_t(E_Z/b) before/after the actual coupled cusp acceleration,
first with unchanged j and then with the derived compensating j response.
Normalized corrected discrepancy <1e-30; require the uncorrected discrepancy
to exceed1e-25 for at least one registered control. These are derivative
response checks, not an adopted or evolved physical state.

Exact symbolic identities must verify the volume/metric cancellations. No
omission of a coupled trace term, frozen gravity or deletion of the original
cusp is permitted. No g=0 inversion or invented nodal derivative.

## Scope of a possible regularity conclusion

If a nonzero |w| scalar-jerk term survives the full controls and remainder,
state what mixed derivatives fail and which weaker initial regularity remains
possible. Do not require joint C4 psi merely to reject a candidate; identify
it as one strong class used in earlier sufficient hypotheses. A failure in
that class does not reject all actions, states, gauges or weak solutions.
Continuous initial acceleration and its prior certificate remain preserved.
Actual constraint/charge persistence and a justified weaker IVP still require
work; a regularity diagnosis alone does not complete G1 or the goal.

Freeze sources, fresh receipts, source checks and immutable replay. Preserve
all originals, failures and sidecars. No new action/state adoption, vault
mutation, paid dispatch, publication, commit/push or deployment.
