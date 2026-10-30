# Second node consistency: candidate algebra awaiting verification

27 October 2026. Working derivation for the next G1 task. NOT an accepted result,
not a physical failure or correction, no PASS or gate effect. Verify every term
against the original coordinate Euler equations before using these candidates.

Use x=z-z_*, w=slope*x-slope*k^2*x^3/6+O(x^5),
R=r1*x+r3*x^3/6+O(x^5), Z=U*w^2, Zdot=Ud*w^2 and psi_dot=p.
Let ty0=partial_z S_y at the node, and rho=rho_node+rho2*x^2+o(x^2).
The density is LOCAL, including the lapse-flux derivative. The exact joint
H/U/Ud construction, not its old U0/Ud0 continuation, is the intended input.

The original regulator equation suggests the regular-side scalar acceleration

    a_psi = -U -(3H-Hbg-R')p + p*R*w'/w,
    a0 = -U -(3H-Hbg-2r1)p,
    a2 = p*(2r3-r1*k^2)/3,
    a_psi = a0+a2*x^2+o(x^2).

Candidate next undivided trace:

    Q = a_Z(node)+2*a2+p*partial_z a_Vz(node).

Derive this from the COMPLETE E_Z, including its spatial-gradient coefficient,
and verify why any metric, shift or moving-node terms vanish or remain. The
full coupled off-diagonal metric acceleration may enter partial_z a_Vz; do not
replace it by a vacuum/frame-only estimate.

A candidate regular-side elimination of E_psi through quadratic normal order gives

    a_Z(node) = [K_Q*(a2+slope^2*a0)
      +K_Q*p*(-r3/2+(5H-2Hbg-3r1)*slope^2)
      +4*b*U*slope^2*k^2+3*b*U*ty0*slope^3+beta*rho2]
      /(b*slope^2).

Check all temporal-regulator and local-flux contributions explicitly. The C2
cusp's relevant composite terms may vanish through this normal order; prove
that statement in the actual equations rather than deleting a generic cusp
tensor or changing A. No sampled finite-angle fit certifies this node formula.

If these formulas survive, a local variation Z=U*w^2+W*w^4 at FIXED H/U/shift
jets would change a2 by -W*slope^2 and suggests a partial sensitivity

    partial_W Q = -(K_Q/b+14*slope^2).

This is only a candidate partial derivative, not the derivative along the true
constraint/root manifold. Adding W changes the shift, mean and joint equations;
all must be recomputed and certified together if this diagnostic is pursued.
No W value, corrected state, incompatibility verdict or physical admission is
established in this working note. Full G1-G6 remain incomplete.
