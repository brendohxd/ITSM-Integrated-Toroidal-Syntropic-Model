# Quartic background: exact kinetic block and uniform complement V1

27 October 2026. First calculation in the full coupled acceleration/node-extension
bundle. Conditional; review DEFERRED; physics_pass=false; gate_effect=NONE.
G1 and the G1-G6 objective remain INCOMPLETE, even if this calculation succeeds.

Use the unchanged original normalized-frame density, the registered B1-frame
eta=1/4,e=1/500,k=40 and the certified quartic H/U/Ud/W initial construction.
Retain all six metric, three frame, three condensate/reservoir, scalar and
regulator velocity coordinates. Work in the original initial gauge h=I,N=1.
The coordinate velocity map has factors 1/2 for metric velocities and one for
frame/condensate/reservoir velocities; do not confuse proper and coordinate blocks.

Derive the complete 14-by-14 coordinate velocity Hessian from the original
density BEFORE reducing constraints. Establish the analytic twelve-direction
complement B(w), scalar cross C(w), scalar diagonal d(w), scalar/regulator cross
-g(w), g=b*w^2, and zero regulator diagonal/complement cross. Express all
coefficients exactly and keep the original nonanalytic force contribution.

Terms which are independent of these twelve proper velocities cannot change
their second derivatives. The cusp term may be excluded ONLY in this complement
calculation after its velocity independence is verified. Reconstruct the full
scalar/cross blocks separately from the original density on both w signs.
Do not set the physical A to zero or infer smoothness of a third cusp tensor.

Prove uniform nonsingularity of B on the whole registered w range [-1/500,1/500],
using pinned 80-digit outward interval arithmetic. Fix C0 to the exact rational
inverse of B(0); require ||I-C0*B(w)||_infinity<1. Use the resulting Neumann inverse
bound. Partition this range into 16,32,64,128,256 equal subintervals in that order,
stopping at first success, without widening the range or loosening the test.
If it fails, retain the exact result as unresolved. No positive-energy conclusion
follows merely from invertibility of the unreduced gravitational block.

Derive the exact Schur solve and which quotients still need a controlled limit.
Test the algebra independently against original full-density numerical Hessians
at both signed profile controls and nodes. Working precision 90 digits; complex
steps 1e-20 and 1e-26; normalized discrepancy <1e-18. At the node test the
undivided operator, never invert g=0. Register controls w/e=-1,-1/2,0,1/2,1.

The new executable must pin sources, write fresh receipts including exact
formulas and outward binary bounds, preserve old sources/sidecars and pass an
immutable replay. A failed implementation gets a preserved source and new version.
This is substantive operator evidence but not the whole acceleration-extension
acceptance: controlled full force quotients, node traces/regularity, actual
background consistency, constraint persistence and a coupled IVP remain required.
No new action, state adoption, microscopic matching input, provider dispatch,
publication, vault mutation, commit or push.
