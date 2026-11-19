# A16.2 new-seed pressure error argument

16 November 2026. Conditional linear R4C1/B1 calculation only.

Let b be the exact eleven-component background and b_hat its pinned degree-40
polynomial. The inherited continuation certificate gives ||b-b_hat||_infinity
<= e_b on [0,T], T=1/20, inside the declared enlarged background box.
Let z=B(b)x and z_dot=A(b)z. The full-vector transformation w=T_w(b,ell)z
has the inherited nonautonomous norm propagator exp(30(t-s)). Here T_w
denotes the complete transformation including the fast and mixed-order maps,
not merely the similarly named wave submatrix in the exported artifact.
It is an evolution norm, not a positive physical Hamiltonian.

For a continuous piecewise polynomial z_hat, bound its derivative defect
against A(b_hat), including every coefficient-rounding discrepancy, by d.
Let M bound ||z_hat||_infinity and L_A be the background Lipschitz bound of A.
With initial discrepancy e_0 and conversion bounds

    ||T_w v||_Q <= K_T ||v||_infinity,
    ||T_w_inverse w||_infinity <= K_I ||w||_Q,

variation of constants gives the uniform bounds

    e_w <= exp(30T) K_T [e_0 + T(d + L_A e_b M)],
    e_z <= K_I e_w.

The inter-tile polynomial endpoints are identical point dyadics. Thus there
are no uncounted jumps. The coefficient and tail defects are bounded on
entire tiles, rather than inferred from sampled residuals. No slow-graph
projection is applied. These estimates hold for the new seed because the
propagator is a full-vector operator bound; the old four-column numerical
accuracy certificate is not used as a new-seed accuracy assertion.

For either new observation row O(b), acting on z, calculate a box operator
norm N_O and background Lipschitz bound L_O. Then

    |O(b)z - O(b_hat)z_hat| <= N_O e_z + L_O e_b M.

The implemented complex norm uses |Re|+|Im| and therefore bounds both
components individually. Each reported real/imaginary tile interval is
enlarged by this error. A certified pressure sign is a sign of the real
Fourier-response coefficient for the chosen phase, not a claim of negative
pressure everywhere in physical space. Tiles containing zero are retained.

This establishes a route to a finite-mode numerical certificate if its
freshly evaluated constants and defects satisfy the frozen inequalities.
It does not assert that those numerical inequalities have already passed.
It also does not establish a nonlinear validity window, arbitrary-background
well-posedness, thermodynamic entropy, an irreversible bath, microscopic
matching or physical health. Rule-9 review is DEFERRED; physics_pass=false.
