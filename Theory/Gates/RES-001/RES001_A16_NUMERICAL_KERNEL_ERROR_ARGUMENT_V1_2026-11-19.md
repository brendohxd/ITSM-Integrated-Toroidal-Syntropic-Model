# A16.2 numerical kernel error argument V1

19 November 2026. Conditional B1, five registered modes, T=1/20.
All norms below are induced complex infinity norms (or the corresponding
vector norm). Bounds on absolute real plus imaginary parts are conservative.

The exact background b and its pinned polynomial b_hat differ by at most e_b.
Matrix coefficient norms N_X and background Lipschitz bounds L_X are over
the same enlarged certified box. Piecewise polynomial centers have arithmetic
errors that include coefficient widths, truncation tails and interval radii.

Forward and inverse fundamentals satisfy U'=D U, V'=-V D and U(0)=V(0)=I.
Thus (V U)'=0. The numerical inverse uses the transposed right equation,
not a numerical inverse or transpose of the forward propagator. Continuity
at tile joins is exact. If d_U,d_V bound their matrix residuals and M_U,M_V
bound polynomial amplitudes, then the absolute-norm Gronwall estimates are

    e_U <= exp(N_D T) T [d_U+L_D e_b M_U],
    e_V <= exp(N_D T) T [d_V+L_D e_b M_V].

The four-column stepper returns per-entry defects/amplitudes. Multiplying
their maxima by four bounds both row and column matrix sums, including the
transposed inverse evolution. Its sixteen padded zero states are arithmetic
padding only; the scientific hidden generator remains four dimensional.
The independent full reference retains the actual twenty-state dynamics.

Let centered factors be L_hat=B_hat U_hat, R_hat=V_hat C_hat and
Lp_hat=Ph_hat U_hat after all polynomial arithmetic. Their errors obey

    e_L  <= N_B e_U + L_B e_b M_U + a_L,
    e_Rh <= N_C e_V + M_V L_C e_b + a_Rh,
    e_Lp <= N_Ph e_U + L_Ph e_b M_U + a_Lp.

The a terms bound centering, arithmetic and model tails uniformly on each
tile. For factor-center amplitudes M_L,M_Rh,M_Lp, the full two-time errors are

    e_K  <= e_L M_Rh + M_L e_Rh + e_L e_Rh,
    e_Kp <= e_Lp M_Rh + M_Lp e_Rh + e_Lp e_Rh.

These estimates hold on the entire time square and therefore on its retarded
triangle. They do not depend on agreement only at discrete sample points.

The full twenty-state reference must match its original initial recipe,
all polynomial hashes, defect and amplitude before reusing its e_z bound.
A new observation O has error N_O e_z+L_O e_b M_z+a_O. This supplies errors
e_R,e_P,e_Rdot for the retained history, pressure and retained rate.

Integrate I_hat(t)=integral R_hat(s)Rref_hat(s) ds tile by tile. The nominal
integrand is polynomial. Indefinite integration retains coefficient intervals,
the carried prefix interval and every tail: discarding its degree-24 term
adds h |c_24|/25 and integrating its model remainder adds h radius. The new
degree-24 model thus bounds the entire partial integral, not just endpoints.
Its arithmetic uncertainties are carried into the reconstructed responses.
The additional physical integrand error is

    e_I <= T[e_Rh M_Rref + M_Rh e_R + e_Rh e_R].

For centered A and Pr, e_A=L_A e_b+a_A and e_Pr=L_Pr e_b+a_Pr. Let H bound
the actual U_h(t,0) norm from the separately justified hidden-block owner.
With M_I bounding the nominal integral and the registered h0, the complete
response errors are

    e_Pmem <= N_Pr e_R + e_Pr M_Rref
              +e_Lp (||h0||+M_I)+N_Ph H e_I+a_Pmem,

    e_Rdotmem <= N_A e_R + e_A M_Rref
                 +e_L (||h0||+M_I)+N_B H e_I+a_Rdotmem.

Both initial forcing and feedback remain. Agreement of these reconstructed
curves with the full response validates a history identity using a supplied
retained history. It does not certify independent retained-only evolution,
an approximation that removes memory, irreversible entropy or physical health.
