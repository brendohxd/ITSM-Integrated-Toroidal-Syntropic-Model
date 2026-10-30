# Physical-sector range analysis V1: frozen computational addendum

27 October 2026. Extends, without rewriting, the physical-sector readiness V1
contract, SHA256 431bbe4379aa756d0b22dd7c15ede57d48f6909bc3c9f7ea349442da1e1ca7fc.
Frozen before new scientific executables are run. High-effort confirmation received.

## Bounded calculation

Derive the range of the retained one-form Theta=<P*dQ-g*s*dZ>+PM*dM,
g=b*sqrt(det h)*V^T*h*V. For r=K*u retain the full action-defined K including
background two-form drift. Work in the canonical quotient chart supplied by the
owners, conditional on its already stated regularity, means and charge constraints.
Do not claim that solving this range problem supplies the missing full temporal
constraint hierarchy or admits every direction physically.

The abstract proof must retain Dg acting on all metric/frame/mean coordinates.
Check the regular-patch Darboux map p_Z=-g*s; the cross-corrected scalar sources;
and both-node L2 divisibility for g=b*e^2*cos(kz)^2. State the smoothness needed
for a double-trace characterization and reject its extension to arbitrary C1 data.
Include the material derivative of both nodal conditions and node transport.
Explain what becomes of the fixed-configuration negative scalar-rate restriction
under this map, without upgrading it to a physical ghost classification.

## Frozen executable checks and independence

Primary: Analysis/MasterTests/test_01_r4c1_physical_sector_range_v1.py.
Exact SymPy controls: derive dTheta, inverse action, Darboux pullback/determinant,
quadratic nodal order, integrability exponents, both periodic nodes, the C1
borderline counterexample, and moving-node transport. Also test the closed-two-form
drift identity K-K^T+Omega_dot=0 with retained crosses and a symmetric test Hessian.
These are algebra/method controls, not an execution of the complete R4C1 operator.

Independent: Analysis/MasterTests/verify_01_r4c1_physical_sector_range_v1.py.
Do not import the primary executable. At three declared positive-definite local
metrics with nonzero frame vectors, form the one-form independently and finite-
difference it in every canonical coordinate, using 70-digit mpmath arithmetic
and steps 1e-5,1e-6. Compare the predicted inverse with a direct dense solve and
test the drift balance. Frozen normalized tolerance 1e-8 for both steps.
Use the full symmetric metric-component factors. Method controls are not new
on-shell B1 backgrounds or a replacement for the original constraint restoration.

At exact V=0 verify the two auxiliary null rows; reject inverse extension there.
At nonzero V reject deletion of the metric/frame cross term and drift by a
nonzero discrepancy greater than 1e-8 in at least one registered control.
No tolerance adjustment, smoothing, spectral fit, target coefficient, physical
cutoff or background adoption is authorized.

Both executables must refuse overwriting an existing output; immutable replay
must recompute and compare receipt bytes without writes. Pin the readiness
contract, this addendum, original coupled-descriptor code and material-seed code
in receipts, together with executable hashes and package versions. Failures are
preserved; any repaired implementation gets a new version rather than changing
the frozen source after launch.

## Interpretation and stop

If the range lemma is verified, state its exact hypotheses and the full physical
use still blocked: the actual r=K*u and its time dependence on an admitted
background must satisfy the full domain/consistency conditions. No scalar-rate
probe receives admission or a physical kinetic signature from this method test.
If those additional inputs remain unestablished, report a precise obstruction
and stop. Do not launch a higher hierarchy or a complete spectrum. Supply the E
decision report, retain all scientific gates and deferred review, and request a
return to Medium after the derivation and relevant verification are complete.
