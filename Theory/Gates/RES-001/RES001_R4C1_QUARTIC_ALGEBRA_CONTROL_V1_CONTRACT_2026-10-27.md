# Quartic completion: exact algebra controls V1

27 October 2026. Supplemental controls for the frozen quartic joint V1
construction; they change no primary source, bracket or numerical criterion.
Conditional, review DEFERRED, physics_pass=false, gate_effect=NONE.

Before launch, freeze a separate executable which checks:

1. The ORIGINAL generic longitudinal shift source, after Z=U*w^2+W*w^4
   and Z1=(2U*w+4W*w^3)*wprime, differs from the quadratic source by
   exactly 5*b*p*W*w^5*wprime. Reject omission of this term.
2. The generic energy and local lapse-flux divergence have both reflection
   symmetries needed for the quarter-cell integral. Under the first reflection
   (w,wprime,wsecond,R,Z1) -> (-w,wprime,-wsecond,-R,-Z1);
   under the second -> (w,-wprime,wsecond,-R,-Z1). All other inputs are fixed.
   The inherited unique coercive shift has these symmetries: its coefficients
   are even, its forcing odd, and it is zero at the symmetry endpoints.
   Consequently four quarter-cell means equal the full periodic mean.
3. On this initial slice hp00=w^2, so the regulator's added W*w^4 changes
   the regular-side scalar acceleration by -W*w^2 at fixed other jets.
   Combine its quadratic coefficient -W*sigma^2 with the independently
   checked scalar-current contribution +12*b*W*sigma^4. The trace change
   is -(K_Q/b+14*sigma^2)*W, equal to -4181*W/625 in the fixed case.
   Reject a calculation which omits the scalar-acceleration contribution.

Use exact SymPy expressions, no float atoms or tolerance tests. Pin original
generic formulas, the quartic certificate and independent scalar-current
receipt; verify all inherited primary source hashes before and after.
Write a fresh receipt and require immutable replay. These checks support the
four-condition construction only, not background admission or a physical IVP.
