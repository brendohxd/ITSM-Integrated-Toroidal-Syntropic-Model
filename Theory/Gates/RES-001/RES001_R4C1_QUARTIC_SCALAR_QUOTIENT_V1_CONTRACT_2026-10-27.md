# Quartic construction: scalar force quotient V1

27 October 2026. Continuation of the kinetic-extension bundle, unchanged action.
Conditional, review DEFERRED, physics_pass=false, G1 INCOMPLETE.

Derive the original regulator acceleration equation and scalar Euler forcing
on the initial h=I,N=1 slice, retaining local dust, the metric volume drift,
all initial shift derivatives and the original A*Y^(3/2) cusp. Use the original
full-coordinate density to check the derived formulas, not only their normal
Taylor coefficients. The mixed acceleration C.T*ay is not part of the forcing
and must be retained in the final Schur solution. Never invert g at w=0.

For w=e*cos(kz), R the exact odd constrained shift, and wp=partial_z w,
derive aPsi=-Z/w^2-p*(3H-Hbg-Rprime)+p*R*wp/w on w!=0. Substitute the
quartic Z profile only after variation. Derive the scalar forcing fpsi from
its time and space momenta, with coordinate accelerations set to zero only
when taking the forcing coefficient. Keep their kinetic coefficients separately.

Separate the full Schur numerator N=d*aPsi-fpsi into analytic and cusp terms.
Using R/w -> r1/sigma and wp -> sigma at either node, determine the constant
compatibility residual, linear normal coefficient and the leading cusp
coefficient of N/(b*w^2). Do not assume differentiability of |w|. Distinguish
the scalar quotient from the additional regular term (C/g).T*ay.
An isolated cusp coefficient does not establish a full acceleration theorem.

Use exact SymPy expressions for identities and the registered exact parameters.
Independently compare aPsi and fpsi against the full original AD/Euler operator
at theta=0,pi/4,pi/2+/-0.1,pi/2+/-0.01,pi/2+/-0.001 and 3pi/4,
excluding exact nodes for divisions. Use 90 digits, complex steps 1e-20/1e-26,
normalized discrepancy <1e-18. These are method controls on the declared
representative, not a continuum or exact-root certificate. Preserve all controls.

Enclose any reported leading cusp coefficient using the FULL certified quartic
H/U boxes and original Hbg enclosure, 80-digit outward intervals, no fitted
angular limit or narrowed post-result box. If a nonzero coefficient appears,
state the exact regularity implication and its hypotheses; do not turn it into
an all-action exclusion or silently remove the cusp. Fresh versioned executable,
receipts, source pins and immutable replay are required. Full force-remainder
constants, complement-force bounds, admission and persistence remain open unless
actually proved. No state adoption, new parent, dispatch, publication or push.
