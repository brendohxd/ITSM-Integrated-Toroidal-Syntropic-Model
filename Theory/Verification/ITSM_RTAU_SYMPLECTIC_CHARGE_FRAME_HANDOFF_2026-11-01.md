# Prepared R-tau symplectic/charge frame handoff - 1 November 2026

Goal ACTIVE; High last acknowledged. Return-to-Medium request is already
pending. Do not infer a change or create confirmation-only wakeups.

Owner: [symplectic/charge-frame report](../Gates/RES-001/RES001_R4C1_RTAU_SYMPLECTIC_CHARGE_FRAME_V1_REPORT_2026-11-01.md).
25/25; exact immutable replay COMPLETE, terminal exit 0.
Receipt cd40137244f6969a8ba737e26a684721e89d9ea8b40bd5263769baa18e743a13.
No calculation remains running from this bundle.

Initial weak two-form is explicitly pulled through the actual coupled
inverse. Keep trace f, difference d, free field/momenta and harmonic moduli:

    Omega=average(a^2*df wedge dP+dd wedge dp_d
       +dhxy wedge dp_xy+sum_frame/scalars dq wedge dp)
       +sum_i dm_i wedge dPi_i,
    Pi_x/y=average(J*p_hxz/hyz), Pi_z=average(J^2*p_hzz).

Pi are not the original-coordinate eta means. Their fixed-configuration
eta derivatives are positive; after replacing f by density, their cross
terms remain. The density/trace-momentum block is G^* multiplication(a^2),
principal a/(N*k^2), with k^2 coefficient in
(0.99989638596212,1.00010362477486). It is weak/order -2, not a flat strong
L2 canonical pairing. An analytic 64-term Neumann representation tail is
<2.991e-17 in its stated bilinear norm; no 64-iteration PDE run is claimed.
All variable-coefficient adjoints, weighted means and pp cross blocks remain.

CRITICAL global interpretation: I=-H0 after spatial momentum reconstruction.
On the regular fixed-I/Q level, the characteristic span is (X_I,X_Q), and
X_H0=-X_I is physical unit-clock time evolution. Do not quotient this as
pure coordinate gauge or demand an invertible two-form on that restricted
level. Compute the ambient spatially reduced Hamiltonian flow and restrict
its trajectories to the fixed-charge level. Mathematical off-level I/Q
parameters define derivatives; they do not adopt a new physical ensemble.

Volume/phase/origin witnesses prove rank: |X_I Volume|>2.59884466,
|X_P origin|>2.94072401e-5, determinant>7.64248491e-5, with phase response1.
Residual spatial origin is gauge; time/phase witnesses are not automatically
adopted gauges. The zero characteristic speed at k!=0 is not thereby gauge.

NEXT deciding calculation: actual prepared canonical-density evolution
operator, with the quantitative physical norm still open. Efficient route:

    delta I_dot=partial_z(S^z*delta I+I*delta S^z
                         +delta(N*sqrt(h)*F^z)).

Use the already explicit clock current, 13-rate Legendre inverse, canonical
momentum equations, auxiliary secondary and gauge-velocity solve. This
encodes density-map drift through the exact equations and can avoid a
large unnecessary third-variation expansion. Compare with
G_Y=(T_dot+T*A_can)*T^-1; never omit T_dot. The old gauge-coordinate velocity
change must transform qdot/shift/momentum flow consistently. Do not assume
old original-coordinate rates already satisfy the adapted gauge.

The initial weak chart is established, not the quantitative generator,
physical mixed norm, nonlinear constraint manifold or finite-time theorem.
Retain charge/global/mean sectors, projector drift, zero-speed branch and
indefinite-gradient-energy warning. No further initial-spectrum inventory
or old homogeneous t=0.05 result substitutes for the evolution calculation.
R-tau unadopted; original R4C1 unchanged; G1-G6 incomplete. Review DEFERRED;
physics_pass=false; gate_effect=NONE. No paper/site change, action adoption,
external dispatch, vault mutation, publication, commit, push or deployment.
