# Quartic joint completion V1: fixed-domain computational plan

27 October 2026. Under contract SHA256
4e4834aff41237fc03235d48c9afa12ab0bc4ac1e0c2116b33f10cf72d03ab16.
Freeze before running new joint code. This is necessary-initial-data work;
full admission/persistence and G1-G6 remain incomplete even on success.

## Exact shift and field equations

Use the original generic initial energy and lapse-flux expressions, substituting
Z=U*w^2+W*w^4 and Zdot=Ud*w^2 AFTER their original derivation. Retain the local
flux and fixed phase/dust charges. Split the exact energy cusp
-2*A*p^3*w^2*abs(w); its periodic mean is -8*A*p^3*e^3/(3*pi).
This split changes no equation. Subtract the homogeneous energy analytically
before interval evaluation to preserve the known mean/node cancellations.

The unchanged shift operator is coercive in the inherited odd sector. Its new
source is the old source plus 5*b*p*W*w^5*w'. Derive a new approximate inverse
from the old three-term series plus its leading W response. Recompute the EXACT
residual and its H/U/W sensitivities; require the first three amplitude orders
to cancel. Bound the residual polynomial, use the same proved coercivity only
where its hypotheses are unchanged, and propagate the new inverse/gradient
errors through density and all root derivatives.

Derive the four necessary equations and verify the explicit quartic changes.
The local partial trace change -4181*W/625 is not the total derivative along
the constraint surface. Keep the shift-node dependence in the node-time velocity
elimination, its sensitivities, mean/node equations and second trace.

## Fixed-domain existence/uniqueness test

Use eta=1/4,e=1/500,k=40 and exact rational family/shared parameters. Set
H=Hbg+(Hbg/50)*yH, U=U0+(U0/50)*yU, W=34+4*yW,
with all y in [-1,1] and U0=Hbg*p+beta*rho0/K_Q as a bracket centre only.
Eliminate Ud with the original jointly valid node-time equation, checking its
positive coefficient. Use F=mean(E)+rho0, B=G-beta*F and the second trace Q.
Precondition them by the fixed leading scales

    dF=-6*Mcosmo*Hbg*(Hbg/50), dB=K_Q*(U0/50), dQ=-4*4181/625.

For f=(F/dF,B/dB,Q/dQ), T(y)=y-f(y). Bound DT on the entire box,
q=max row-sum bounds, and centre residuals c_i=|f_i(0)| bounds. Require
q<1 and c_i+row_i<1 for every row. These conditions give a contraction and
self-map of the closed box, hence a unique restricted root. Include exact-shift
error and sensitivity enclosures in every function/derivative, not a frozen
shift, patched velocity or point approximation.

Use pinned interval arithmetic at 80 digits and outward binary endpoints.
Angular quadrature enclosure uses fixed subdivisions 16,32,64,128,256 in that
order, stopping at the first certificate. Refine only angular subdivision;
do not widen H/U/W or change criteria after seeing failure. Prove positive
pointwise lapse-derived dust, nonsingular inherited complements and both charges.

## Independent controls and preservation

Independent approximate point solves use the uneliminated four equations,
100-digit arithmetic and normalized residual <1e-40. They are controls, not the
root certificate. Check the new shift source/response against a separately
assembled Fourier/Galerkin problem, using eight and twelve modes; compare
approximation errors with the proved inverse/gradient bounds rather than a fitted
convergence law. Retain all errors and failures.

Add nonzero-W original-coordinate scalar-current controls to verify its quadratic
normal change; 80 digits, normalized 1e-30, both slopes. No old primary source or
receipt is modified. Freeze new executable hashes before runs; fresh attempt
directories and immutable replay. At most four independent workers, parent-only
writes. A failed implementation is preserved before a new version. No new parent,
canonical adoption, physical clearance, publication or provider change.
