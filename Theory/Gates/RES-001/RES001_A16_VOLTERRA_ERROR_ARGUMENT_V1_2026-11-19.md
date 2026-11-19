# Independent retained evolution: error lift V1

19 November 2026. Conditional registered R4C1/B1 and existing full-vector
propagator, [0,T], T=1/20. This is an error estimate, not advancing data.

The independent algorithm computes R_hat,J_hat from the filtered kernel law

    R_hat' ~= A_hat R_hat+L_hat(h0+J_hat),
    J_hat' ~= Rh_hat R_hat, R_hat(0)=J_hat(0)=0.

J consists of four causal quadrature accumulators. No original hidden-field
trajectory or supplied full-system R is needed to advance these equations.
Let the continuous numerical defects be d_R and d_J, including all coefficient
rounding and high-degree tails. Let M_R,M_J bound the nominal polynomials;
e_A,e_L,e_Rh,e_Pr,e_Lp are uniform physical coefficient/factor errors from the
validated kernel owner (with fresh A/P_R centering where needed). Then

    r_R = d_R+e_A M_R+e_L (||h0||+M_J),
    r_J = d_J+e_Rh M_R

bound their defects against the exact time-dependent factor equations.

For analysis only, define h_tilde=U_h(t,0)(h0+J_hat). The exact identity
U_h Rh=C gives

    h_tilde'-D h_tilde-C R_hat=U_h r_J,
    R_hat'-A R_hat-B h_tilde=r_R.

Let H bound ||U_h(t,0)||_infinity and J_b=B_balance E M_inverse map the
twelve mixed (R,h) values into the original balanced twenty-state chart.
Its moving conjugacy J_b'+J_b G_mixed=A_balanced J_b must be checked on the
registered exact background shell. Let N_b bound its operator norm. Initial
agreement with the original radial-rate seed is exact. The lifted residual
in that chart is at most

    F_b=N_b max(r_R,H r_J).

The inherited full-vector Q-norm propagator, with conversion bounds K_T,K_I,
therefore supplies the continuous balanced-state error

    e_z <= K_I exp(30T) K_T T F_b.

The true R/pressure/rate observations on that chart have box norms N_Rz,
N_Pz,N_Rdotz. Consequently the independent retained-state error is bounded by
N_Rz e_z. For the reconstructed numerical pressure, including its own final
arithmetic/tail bound a_P,

    e_P <= N_Pz e_z+e_Pr M_R+e_Lp (||h0||+M_J)+a_P.

The derivative of the nominal retained curve has error at most
N_Rdotz e_z+r_R. The background and kernel uncertainties are already present
in the e coefficients; the lift uses the exact background analytically.
No approximate background is substituted into this identity without a bound.

These estimates need a uniform full-vector propagator, not an unjustified
constant extrapolated from the initial event. They use the already-proved
conditional propagator and preserve its scientific qualifications. A numerical
reference is read only after the independent curves are sealed, for comparison.
This is a computational evolution equivalence with causal memory storage;
it is not an eight-variable memory-free theory, physical-health proof,
irreversible bath or microscopic matching result.
