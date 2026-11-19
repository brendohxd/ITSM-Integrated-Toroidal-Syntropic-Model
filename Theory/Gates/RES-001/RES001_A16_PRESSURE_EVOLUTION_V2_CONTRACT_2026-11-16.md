# A16.2 radial-rate pressure evolution: frozen V2 contract

Date: 16 November 2026. Conditional R4C1/B1 only; R-tau is not adopted.

Deciding question: does the previously identified radial-rate direction have
a controlled, nonzero pressure response beyond the initial event?

Use the unchanged exported twenty-state generator, eleven-variable rotating
background and exact field reconstruction. Initial original-chart perturbation
is delta u_dot=1 (slot 16), all other slots zero. This is a linear response
normalization, not a finite-amplitude perturbation. Retain all coupled states,
constraint reconstruction, lapse, shift, evolving balancing and background.
Do not project onto a slow graph. The zero solution is the comparison state.

Register ell=4,8,16,32,64 and t in [0,1/20]. Pressure means the combined
canonical u,v,r scalar pressure, including their portal potential:

    P = sum phi_dot [delta phi_dot - phi_dot alpha] - sum U_phi delta phi,
    delta phi_dot = (d_t F_phi + F_phi L) x.

The derivative of each observation row is retained. This is not the isolated
reservoir pressure, total stress of every sector, entropy, or a material EOS.

Reuse the pinned continuous background certificate and the full-vector Q-norm
propagator bound exp(30(t-s)). That bound is independent of the old four
initial columns; their trajectory accuracy certificate is not transferred.
Compute fresh degree-24 piecewise Taylor trajectories in outward-rounded
256-bit dyadic arithmetic, retaining low-order rounding and high-order defects,
inter-tile continuity, initial balancing error and background uncertainty.
Bound the new pressure observation on the declared background box. Accept
useful accuracy only if the newly computed absolute pressure error is <1e-8.

Report continuous pressure intervals tile by tile, with the global observation
error added to both real and imaginary parts. Identify certified nonzero sign
intervals and any unresolved/zero-containing tiles without suppressing reversals.
There is no required sign or monotonicity. In particular t=0 has P=0.

Controls: exact initial P=0 and proper pressure rate -2341/840; all eleven
previous held rows vanish initially; full scalar block invariance inherited
only under its pinned owner; zero response, negative-seed symmetry, arithmetic
controls, one-step agreement with the original four-column implementation,
independent DOP853 integration of true background plus all twenty states, and
byte-identical fresh replay. Solver agreement is a diagnostic, not a proof.
Pin all inherited scientific inputs and preserve source bytes and timestamps.

Failure of an accuracy inequality leaves the requested certificate open.
Even success is conditional finite-mode linear evolution, not a healthy
Hamiltonian, nonlinear stability, physical cutoff, irreversible memory,
microscopic matching, an organizing force or a universal equation of state.
physics_pass=false; gate_effect=NONE; Rule-9 review DEFERRED. No manuscript,
publication, commit, push, provider dispatch or vault mutation is included.

V2 changes endpoint-value equality in two numerical controls. V1 used Python
object identity for IV instances and was stopped before receipts; its source,
contract and input manifest remain intact. Equations, seed and acceptance
requirements are unchanged.
