# Quartic initial construction: analytic force bounds and transport V1

27 October 2026. Operator confirmed Sol 6.1 High for this derivation bundle.
Conditional; review DEFERRED; physics_pass=false; G1-G6 INCOMPLETE.
Use the unchanged action and the existing exact quartic construction and
kinetic/cusp certificates. A contract is not completion of this calculation.

## Authority, inputs and frozen scope

Owning frontier: RES001_R4C1_QUARTIC_NODE_OPERATOR_V1_REPORT_2026-10-27.md,
SHA256 3ab43dd8e4b29d0925c85c6269f98abf3e0686c92881d4f1eb11de947a74efa3.
Keep B1 eta=1/4,e=1/500,k=40, p=1/20, original charges, lapse flux and
the entire certified quartic H/U/W box with exact Ud elimination. No new
parameter/action choice or adoption of a physical background.

The private ITSM vault was checked read-only for continuity in this turn:
source document doc_dbcad7f2789e7b5ea30ac12a, retrieved chunk
chk_1cf368b625f2d88fb1a19592, continuity packet
ctx_a66ef1dd7ed40e548882a0f8. Its source URI is the owning report above in
the canonical repository. Audit reports valid. These retrieval identifiers
are continuity references, not scientific evidence or claim admission.
The live report, equations, receipts and hashes remain authoritative.

## A. Full analytic complement forcing

Partition the ORIGINAL density exactly into analytic and original cusp pieces;
the cusp forces and coupling remainder are already derived. This partition
does not set physical A to zero or change the action. Compute all twelve
analytic Euler forces with the full coordinate metric/frame/scalar/reservoir
variables retained through variation, including volume drift and the original
initial spatial-force terms. Use an independently checked real directional
derivative/interval implementation if it avoids a large symbolic expansion.
No frozen-velocity envelope is a replacement for those derivatives.

Prove the coordinate source implementation against original AD/real Taylor
Euler controls before using it for bounds. Retain all twelve force components,
both signs and both nodes. Working precision>=90 digits, independent steps
1e-20/1e-26 where complex-step controls apply, normalized tolerance1e-18.
For enclosure use 80-digit outward intervals and exact rational inputs.
Do not use complex-step numbers as interval enclosures or claim sampled
agreement bounds the full profile.

## B. Removable analytic scalar quotient, quantitative bounds

The accepted scalar numerator N=d*aPsi-fpsi has constant node value -G.
Use the exact registered root G=0 and its proved reflection parity; do not
zero a small numerical residual. The cusp part has separate explicit bounds.

Near either node, set T=R/w by its removable analytic extension and use
|w|<=e/2, |kx|<=pi/6, |w|>=|sigma*x|/2, sigma^2=e^2*k^2. Reuse the
certified Qmax, Rsecond, M3=Rthird, and D for
|R*wprime/w-Rprime|<=D*w^2. The exact identities imply the bounds

    |T| <= 2*Qmax/|sigma|,
    |Tprime| <= D*|w|,
    |Tsecond| <= 2*M3/|sigma|+k^2*(2*Qmax/|sigma|)+2*|sigma|*D.

Primes here are physical normal-coordinate derivatives. Substitute R=w*T
in N_analytic and cancel algebraically BEFORE interval differentiation.
Use the original local lapse density, not its mean. Require no remaining
negative powers of w or an explicit proof of every removable factor.

For F(w,wprime,T,Rprime), bound the physical second derivative with the full
chain rule: velocities (wprime,-k^2*w,Tprime,Rsecond), accelerations
(-k^2*w,-k^2*wprime,Tsecond,Rthird). Retain mixed Hessian terms.
Let M_N enclose |partial_x^2 N_analytic| uniformly. Taylor's theorem then gives

    |N_analytic/w^2| <= 2*M_N/sigma^2

on the EXACT constraint root, using N(0)=Nprime(0)=0. A box enclosure of
derivatives may be broad but cannot replace this root-conditional cancellation.
Carry the actual bounded cross (C/g).T*ay into aZ. Away from nodes, use the
original undivided operator with a certified nonzero g bound. Cover the
whole periodic initial slice with overlapping domains; no untested gap.

## C. Nodal space and transport

Retain the nonzero |w| cusp and its coupled cubic remainder. Determine what
initial rates and mixed derivatives actually exist; do not assume arbitrary
smoothness or infer weak-solution existence from continuity. Reuse the full
general geometry in NODE_VELOCITY_TRANSPORT_V2, including the volume-gradient
term. Its old quadratic continuation is not a new quartic state certificate.
Differentiate the actual constraints and charges only where regularity permits.
Track node motion rather than imposing permanent alignment or projecting onto
the initial polynomial profiles. A new higher compatibility obstruction must
remain scoped to the actual continuation and regularity class.

## Acceptance and delivery

Produce exact formulas, explicit finite force/quotient bounds with constants and
domains, independent original-operator controls, fresh versioned receipts and
immutable replay. Checks must reject omitted drift, local flux, metric/frame
response, mixed chain-rule terms and invalid division at nodes. Preserve all
original sources, sidecars, failed attempts and existing dirty work.

Quantitative initial acceleration bounds do not by themselves prove admission
or persistence. Separate actual results from any remaining transport/IVP
hypotheses. Keep G1 open unless its full requirements are demonstrated; G2-G6
remain governed by their prerequisites. No publication, review dispatch, paid
session, vault proposal/sync, new parent, commit, push or runtime change.
