# Prepared principal V3: point-inverse precision and rank minor

V2 is preserved at 21/25. It correctly restores the full phase cone and
certifies whole-root kinetic positivity. Four point-polynomial comparisons
still fail 1e-28: defects are 1.57e-26 to 2.74e-24 at actual centres and
1.13e-18 at the larger rational tilt control. These do not come from an
altered action or removed term. The point comparison used the midpoint of
the five-term Neumann inverse enclosure. The enclosure includes the inverse
but its midpoint omits the actual series tail; it is not that accurate.

V3 uses 24 terms plus the explicitly bounded 25th-order tail for POINT
comparisons. It retains the five-term enclosure for the whole-root bounds.
The 1e-28 acceptance tolerance, equations, physical data and V2 positive
bound remain unchanged. Record the point tail bound explicitly and require
it below 1e-40. No point numerical precision is inferred from enclosure
membership alone.

Add the bounded principal-rank extension allowed by V2. At the dust
characteristic omega=-S^z*k, construct the slow pencil
G+S^z*(B+B^T)+(S^z)^2*M. Bound an 8x8 minor using the actual whole-root
Hessian and shift Fourier-centre plus C2-ball uncertainty. A minor bound
establishes rank at least eight; it does NOT by itself establish an exact
ninth zero root for the whole inhomogeneous family. Keep that distinction.
The exact rest polynomial has a double zero root with one eigenvector;
actual tilted polynomial comparisons remain numerical controls rather than
an exhaustive continuum determinant proof or a hyperbolicity theorem.

All preceding contracts/versions/receipts remain immutable. Review DEFERRED;
physics_pass=false; R-tau unadopted; G1-G6 incomplete. No action/ensemble,
cutoff, provider, publication or runtime changes are authorized.
